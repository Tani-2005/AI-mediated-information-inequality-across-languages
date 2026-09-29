import sys
from pathlib import Path

# Add backend to sys.path
backend_path = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from fastapi.testclient import TestClient
from app.main import app
from app.db.session import SessionLocal
from app.db.models import Participant, PostTaskMeasure, TaskSession

client = TestClient(app)

def run_synthetic_participant():
    db = SessionLocal()
    try:
        print("--- START SYNTHETIC PARTICIPANT FLOW ---")
        # 1. Create Session
        r_sess = client.post("/api/v1/session/create", json={"is_pilot": False})
        pid = r_sess.json()["participant_id"]
        print(f"Created participant: {pid}")

        # 2. Consent
        client.post("/api/v1/consent/submit", json={
            "participant_id": pid, "agreed_to_terms": True, "confirmed_age_residency": True
        })

        # 3. Screening
        client.post("/api/v1/screening/submit", json={
            "participant_id": pid,
            "responses": {"q1": "B", "q2": "A", "q3": "C", "q4": "A", "q5": "C", "q6": "B"}
        })

        # 4. Language Background
        client.post("/api/v1/language-background/submit", json={
            "participant_id": pid,
            "aoa_english": 5, "aoa_hindi": 0, "primary_home_lang": "Hindi",
            "medium_instruction_school": "English", "medium_instruction_higher": "English",
            "self_read_en": 8, "self_write_en": 8, "self_speak_en": 8,
            "self_read_hi": 8, "self_write_hi": 8, "self_speak_hi": 8,
            "freq_daily_en": 50.0, "freq_daily_hi": 40.0, "freq_daily_cs": 10.0,
            "ai_use_en": 50.0, "ai_use_hi": 50.0, "ai_use_mixed": 0.0
        })

        # 5. AI Literacy
        client.post("/api/v1/ai-literacy/submit", json={
            "participant_id": pid,
            "responses": {f"ails_{i}": 4 for i in range(1, 13)}
        })

        # 6. Randomization & Tasks initialization
        client.post("/api/v1/randomization/allocate", json={"participant_id": pid})
        client.post("/api/v1/tasks/initialize", json={"participant_id": pid})

        sessions = db.query(TaskSession).filter(TaskSession.participant_id == pid).order_by(TaskSession.position.asc()).all()
        print(f"Initialized {len(sessions)} task sessions: {[s.task_id for s in sessions]}")

        # Iterative Task Flow: Task -> Decision -> Post-Task NASA-TLX
        for idx, sess in enumerate(sessions, 1):
            # Task Decision
            res_dec = client.post("/api/v1/tasks/decision/submit", json={
                "participant_id": pid,
                "task_id": sess.task_id,
                "submitted_answers": {
                    "is_eligible": True,
                    "first_tranche_loan_inr": 100000,
                    "skill_stipend_per_day_inr": 500,
                    "max_project_cost_lakhs": 50,
                    "subsidy_percentage": 35
                },
                "confidence_score": 6
            })
            ts_id = res_dec.json()["task_session_id"]
            print(f"Task {idx} ({sess.task_id}) Decision Submitted. TaskSession ID: {ts_id}")

            # NASA-TLX Post-Task Submission
            res_post = client.post("/api/v1/post-task/submit", json={
                "participant_id": pid,
                "task_session_id": ts_id,
                "task_id": sess.task_id,
                "nasa_tlx_raw": {
                    "mental_demand": 10 + idx * 2,
                    "physical_demand": 2,
                    "temporal_demand": 5 + idx,
                    "performance": 15,
                    "effort": 12,
                    "frustration": idx
                },
                "feedback_comments": f"Feedback after Task {idx}"
            })
            print(f"Task {idx} Post-Task Workload Submitted. Status: {res_post.json()['status']}")

        # Verification in Database
        records = db.query(PostTaskMeasure).filter(PostTaskMeasure.participant_id == pid).all()
        print(f"\n--- VERIFICATION IN DATABASE ---")
        print(f"Total PostTaskMeasure records for participant {pid}: {len(records)}")
        for r in records:
            print(f"  - Measure ID: {r.measure_id} | TaskSession ID: {r.task_session_id} | Task ID: {r.task_id} | Mental Demand: {r.nasa_tlx_raw['mental_demand']} | Comment: {r.feedback_comments}")

        assert len(records) == 3, f"Expected 3 records, found {len(records)}"
        print("\nFlow verification SUCCESSFUL!")
    finally:
        db.close()

if __name__ == "__main__":
    run_synthetic_participant()
