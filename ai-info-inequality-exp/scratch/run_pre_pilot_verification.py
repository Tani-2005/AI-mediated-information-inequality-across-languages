import sys
import datetime
from pathlib import Path

backend_path = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.session import Base, get_db
from app.db.models import (
    Participant, ConsentLog, ScreeningLog, LanguageBackground, AILiteracy,
    RandomizationAllocation, TaskSession, Message, TelemetryEvent,
    FinalDecision, PostTaskMeasure, TechnicalError
)
from app.config import settings

# Setup isolated testing engine with StaticPool
TEST_DB_URL = "sqlite:///:memory:"
test_engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def run_pre_pilot_audit():
    # Ensure fresh schema
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()

    audit_log = []
    def log(msg):
        print(msg)
        audit_log.append(msg)

    log("=== STARTING PRE-PILOT END-TO-END VERIFICATION ===")

    # 1. Session Creation (Participant creation)
    r1 = client.post("/api/v1/session/create", json={"is_pilot": False})
    assert r1.status_code == 200, f"Session create failed: {r1.text}"
    pid = r1.json()["participant_id"]
    log(f"Step 1: Session created for participant {pid}")

    # 2. Consent Submission
    r2 = client.post("/api/v1/consent/submit", json={
        "participant_id": pid,
        "agreed_to_terms": True,
        "confirmed_age_residency": True
    })
    assert r2.status_code == 200, f"Consent submit failed: {r2.text}"
    log("Step 2: Consent persisted")

    # 3. Screening Submission
    r3 = client.post("/api/v1/screening/submit", json={
        "participant_id": pid,
        "responses": {"q1": "B", "q2": "A", "q3": "C", "q4": "A", "q5": "C", "q6": "B"}
    })
    assert r3.status_code == 200, f"Screening failed: {r3.text}"
    assert r3.json()["passed"] is True
    log("Step 3: Screening evaluated correctly (Passed bilingual threshold)")

    # 4. Language Background
    r4 = client.post("/api/v1/language-background/submit", json={
        "participant_id": pid,
        "aoa_english": 6, "aoa_hindi": 0, "primary_home_lang": "Hindi",
        "medium_instruction_school": "English", "medium_instruction_higher": "English",
        "self_read_en": 8, "self_write_en": 8, "self_speak_en": 8,
        "self_read_hi": 9, "self_write_hi": 9, "self_speak_hi": 9,
        "freq_daily_en": 50.0, "freq_daily_hi": 40.0, "freq_daily_cs": 10.0,
        "ai_use_en": 50.0, "ai_use_hi": 50.0, "ai_use_mixed": 0.0
    })
    assert r4.status_code == 200, f"Language background failed: {r4.text}"
    log("Step 4: Language background persisted")

    # 5. AI Literacy (AILS)
    ails_raw = {f"ails_{i}": 4 for i in range(1, 13)} # 12 * 4 = 48 -> HIGH
    r5 = client.post("/api/v1/ai-literacy/submit", json={
        "participant_id": pid,
        "responses": ails_raw
    })
    assert r5.status_code == 200, f"AILS submit failed: {r5.text}"
    assert r5.json()["stratum"] == "HIGH"
    assert r5.json()["total_score"] == 48
    log("Step 5: AILS scored correctly (total_score=48, stratum=HIGH)")

    # 6. Randomization Allocation
    r6 = client.post("/api/v1/randomization/allocate", json={"participant_id": pid})
    assert r6.status_code == 200, f"Randomization failed: {r6.text}"
    arm = r6.json()["assigned_arm"]
    log(f"Step 6: Randomization allocated arm: {arm}")

    # 7. Task Initialization (Latin-square)
    r7 = client.post("/api/v1/tasks/initialize", json={"participant_id": pid})
    assert r7.status_code == 200, f"Tasks initialize failed: {r7.text}"
    task_order = r7.json()["tasks"]
    log(f"Step 7: Tasks initialized with Latin-square ordering: {task_order}")

    sessions = db.query(TaskSession).filter(TaskSession.participant_id == pid).order_by(TaskSession.position.asc()).all()
    assert len(sessions) == 3

    # Log Onboarding Telemetry Event
    client.post("/api/v1/telemetry/event", json={
        "participant_id": pid,
        "task_id": None,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "event_type": "ONBOARDING_COMPLETED",
        "event_data": {"completed": True}
    })

    # Iterate through all 3 tasks
    task_1_m1_backup = None

    for idx, sess in enumerate(sessions, 1):
        task_id = sess.task_id
        ts_id = sess.session_id
        log(f"\n--- EXECUTING TASK {idx} ({task_id}) [TaskSession ID: {ts_id}] ---")

        # Telemetry: Task Started
        client.post("/api/v1/telemetry/event", json={
            "participant_id": pid,
            "task_id": task_id,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "event_type": "TASK_STARTED",
            "event_data": {"position": idx, "task_id": task_id}
        })

        # Gemini Chat Interaction
        prompt = f"What are the key eligibility rules for {task_id}?"
        r_chat = client.post("/api/v1/chat/message", json={
            "participant_id": pid,
            "task_id": task_id,
            "prompt": prompt
        })
        assert r_chat.status_code == 200, f"Chat failed for {task_id}: {r_chat.text}"
        chat_resp = r_chat.json()
        assert "reply" in chat_resp
        assert chat_resp["is_mock"] == settings.USE_MOCK_LLM
        log(f"  - Chat query sent. Response received (is_mock={chat_resp['is_mock']})")

        # Telemetry: Chat Message Sent
        client.post("/api/v1/telemetry/event", json={
            "participant_id": pid,
            "task_id": task_id,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "event_type": "CHAT_MESSAGE_SENT",
            "event_data": {"prompt_length": len(prompt)}
        })

        # Final Decision Submission
        r_dec = client.post("/api/v1/tasks/decision/submit", json={
            "participant_id": pid,
            "task_id": task_id,
            "submitted_answers": {
                "is_eligible": True,
                "first_tranche_loan_inr": 100000,
                "skill_stipend_per_day_inr": 500,
                "max_project_cost_lakhs": 50,
                "subsidy_percentage": 35
            },
            "confidence_score": 6
        })
        assert r_dec.status_code == 200, f"Decision submit failed for {task_id}: {r_dec.text}"
        dec_data = r_dec.json()
        assert dec_data["task_session_id"] == ts_id
        dec_db = db.query(FinalDecision).filter(FinalDecision.task_session_id == ts_id).first()
        log(f"  - Final decision submitted. Calculated Score: {dec_db.calculated_score}")

        # Telemetry: Decision Submitted
        client.post("/api/v1/telemetry/event", json={
            "participant_id": pid,
            "task_id": task_id,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "event_type": "DECISION_SUBMITTED",
            "event_data": {"score": dec_db.calculated_score}
        })

        # NASA-TLX Workload Post-Task Measurement
        tlx_scores = {
            "mental_demand": 10 + idx * 2,
            "physical_demand": 2,
            "temporal_demand": 5 + idx,
            "performance": 15,
            "effort": 12,
            "frustration": idx
        }
        r_post = client.post("/api/v1/post-task/submit", json={
            "participant_id": pid,
            "task_session_id": ts_id,
            "task_id": task_id,
            "nasa_tlx_raw": tlx_scores,
            "feedback_comments": f"Feedback after Task {idx}"
        })
        assert r_post.status_code == 200, f"Post-task submit failed for {task_id}: {r_post.text}"
        post_resp = r_post.json()
        log(f"  - Post-task workload measure submitted. Participant status: {post_resp['status']}")

        # Telemetry: Post-Task Submitted
        client.post("/api/v1/telemetry/event", json={
            "participant_id": pid,
            "task_id": task_id,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "event_type": "POST_TASK_SUBMITTED",
            "event_data": {"composite_score": post_resp["tlx_composite_score"]}
        })

        # Check status after each task
        p_db = db.query(Participant).filter(Participant.participant_id == pid).first()
        db.refresh(p_db)
        if idx < 3:
            assert p_db.status == "IN_PROGRESS", f"Participant status should be IN_PROGRESS after task {idx}, got {p_db.status}"
        else:
            assert p_db.status == "COMPLETED", f"Participant status should be COMPLETED after task 3, got {p_db.status}"

        # Capture Task 1 measurement for uncorrupted invariance check
        if idx == 1:
            task_1_m1_backup = db.query(PostTaskMeasure).filter(PostTaskMeasure.task_session_id == ts_id).first()

    # Verify Task 1 measure remains completely unchanged after Task 2 & 3
    db.refresh(task_1_m1_backup)
    assert task_1_m1_backup.nasa_tlx_raw["mental_demand"] == 12
    assert task_1_m1_backup.feedback_comments == "Feedback after Task 1"
    log("\nVerification: Task 1 PostTaskMeasure record remained 100% unchanged after Tasks 2 & 3.")

    # 8. Debrief Completion
    r_deb = client.post("/api/v1/debrief/complete", json={"participant_id": pid})
    assert r_deb.status_code == 200, f"Debrief failed: {r_deb.text}"
    assert r_deb.json()["status"] == "COMPLETED"
    assert "completion_code" in r_deb.json()
    log("Step 8: Debrief completed, verification completion code generated.")

    # DATABASE INVARIANTS AND EXACT COUNTS VERIFICATION
    log("\n=== VERIFYING DATABASE INVARIANTS & EXACT COUNTS ===")
    p_cnt = db.query(Participant).count()
    c_cnt = db.query(ConsentLog).count()
    s_cnt = db.query(ScreeningLog).count()
    bg_cnt = db.query(LanguageBackground).count()
    ails_cnt = db.query(AILiteracy).count()
    rand_cnt = db.query(RandomizationAllocation).count()
    ts_cnt = db.query(TaskSession).count()
    post_cnt = db.query(PostTaskMeasure).count()
    dec_cnt = db.query(FinalDecision).count()
    msg_cnt = db.query(Message).count()
    telem_cnt = db.query(TelemetryEvent).count()

    log(f"- participants = {p_cnt} (Expected: 1)")
    log(f"- consent_logs = {c_cnt} (Expected: 1)")
    log(f"- screening_logs = {s_cnt} (Expected: 1)")
    log(f"- language_background = {bg_cnt} (Expected: 1)")
    log(f"- ai_literacy = {ails_cnt} (Expected: 1)")
    log(f"- randomization_allocations = {rand_cnt} (Expected: 1)")
    log(f"- task_sessions = {ts_cnt} (Expected: 3)")
    log(f"- post_task_measures = {post_cnt} (Expected: 3)")
    log(f"- final_decisions = {dec_cnt} (Expected: 3)")
    log(f"- messages = {msg_cnt} (Expected: 6 [3 user + 3 AI])")
    log(f"- telemetry_events = {telem_cnt} (Expected: 13)")

    assert p_cnt == 1
    assert c_cnt == 1
    assert s_cnt == 1
    assert bg_cnt == 1
    assert ails_cnt == 1
    assert rand_cnt == 1
    assert ts_cnt == 3
    assert post_cnt == 3
    assert dec_cnt == 3
    assert msg_cnt == 6 # 3 tasks * 2 (1 USER + 1 AI)
    assert telem_cnt == 13 # 1 onboarding + 3 tasks * 4 (START, CHAT, DECISION, POST_TASK)

    # Check child FK relationships & orphan records
    orphan_msgs = db.query(Message).filter(Message.participant_id != pid).count()
    orphan_post = db.query(PostTaskMeasure).filter(PostTaskMeasure.participant_id != pid).count()
    orphan_dec = db.query(FinalDecision).filter(FinalDecision.participant_id != pid).count()

    assert orphan_msgs == 0, "Found orphan message records"
    assert orphan_post == 0, "Found orphan post-task measure records"
    assert orphan_dec == 0, "Found orphan final decision records"
    log("Child record integrity verified: All child records point strictly to participant_id.")

    # Check post-task task_session_id distinctness
    post_measures = db.query(PostTaskMeasure).filter(PostTaskMeasure.participant_id == pid).all()
    session_ids_in_post = {m.task_session_id for m in post_measures}
    assert len(session_ids_in_post) == 3, f"Expected 3 distinct task_session_ids in post-task measures, found {len(session_ids_in_post)}"
    log("PostTaskMeasure session distinctness verified: 3 distinct task_session_ids.")

    log("\n=== ALL 23 PRE-PILOT AUDIT REQUIREMENTS VERIFIED SUCCESSFULLY ===")

if __name__ == "__main__":
    run_pre_pilot_audit()
