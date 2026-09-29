import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import get_db
from app.db.models import Participant, ConsentLog, ScreeningLog, LanguageBackground, AILiteracy, TaskSession, PostTaskMeasure

client = TestClient(app)

@pytest.fixture(autouse=True)
def override_db(db):
    def _get_test_db():
        try:
            yield db
        finally:
            pass
    app.dependency_overrides[get_db] = _get_test_db
    yield
    app.dependency_overrides.clear()

def create_full_participant_via_api():
    # 1. Create session
    res_sess = client.post("/api/v1/session/create", json={"is_pilot": False})
    assert res_sess.status_code == 200, res_sess.text
    pid = res_sess.json()["participant_id"]

    # 2. Submit consent
    res_cons = client.post("/api/v1/consent/submit", json={
        "participant_id": pid,
        "agreed_to_terms": True,
        "confirmed_age_residency": True
    })
    assert res_cons.status_code == 200, res_cons.text

    # 3. Submit screening
    res_scr = client.post("/api/v1/screening/submit", json={
        "participant_id": pid,
        "responses": {
            "q1": "B", "q2": "A", "q3": "C",
            "q4": "A", "q5": "C", "q6": "B"
        }
    })
    assert res_scr.status_code == 200, res_scr.text

    # 4. Submit language background
    res_bg = client.post("/api/v1/language-background/submit", json={
        "participant_id": pid,
        "aoa_english": 5, "aoa_hindi": 0, "primary_home_lang": "Hindi",
        "medium_instruction_school": "English", "medium_instruction_higher": "English",
        "self_read_en": 8, "self_write_en": 8, "self_speak_en": 8,
        "self_read_hi": 8, "self_write_hi": 8, "self_speak_hi": 8,
        "freq_daily_en": 50.0, "freq_daily_hi": 40.0, "freq_daily_cs": 10.0,
        "ai_use_en": 50.0, "ai_use_hi": 50.0, "ai_use_mixed": 0.0
    })
    assert res_bg.status_code == 200, res_bg.text

    # 5. Submit AI literacy
    ails_resp = {f"ails_{i}": 4 for i in range(1, 13)}
    res_ails = client.post("/api/v1/ai-literacy/submit", json={
        "participant_id": pid,
        "responses": ails_resp
    })
    assert res_ails.status_code == 200, res_ails.text

    # 6. Allocate randomization
    res_rand = client.post("/api/v1/randomization/allocate", json={"participant_id": pid})
    assert res_rand.status_code == 200, res_rand.text

    # 7. Initialize 3 task sessions
    res_init = client.post("/api/v1/tasks/initialize", json={"participant_id": pid})
    assert res_init.status_code == 200, res_init.text

    return pid

def test_post_task_three_sessions_three_records(db):
    pid = create_full_participant_via_api()
    sessions = db.query(TaskSession).filter(TaskSession.participant_id == pid).order_by(TaskSession.position.asc()).all()
    assert len(sessions) == 3

    tlx_task1 = {"mental_demand": 15, "physical_demand": 2, "temporal_demand": 10, "performance": 18, "effort": 14, "frustration": 3}
    tlx_task2 = {"mental_demand": 8, "physical_demand": 1, "temporal_demand": 5, "performance": 12, "effort": 7, "frustration": 2}
    tlx_task3 = {"mental_demand": 18, "physical_demand": 3, "temporal_demand": 15, "performance": 19, "effort": 16, "frustration": 6}

    # Task 1 decision & post-task workload
    dec1 = client.post("/api/v1/tasks/decision/submit", json={
        "participant_id": pid,
        "task_id": sessions[0].task_id,
        "submitted_answers": {"is_eligible": True, "first_tranche_loan_inr": 100000, "skill_stipend_per_day_inr": 500, "max_project_cost_lakhs": 50, "subsidy_percentage": 35},
        "confidence_score": 6
    })
    assert dec1.status_code == 200, dec1.text
    ts1_id = dec1.json()["task_session_id"]

    post1 = client.post("/api/v1/post-task/submit", json={
        "participant_id": pid,
        "task_session_id": ts1_id,
        "task_id": sessions[0].task_id,
        "nasa_tlx_raw": tlx_task1,
        "feedback_comments": "Task 1 complete"
    })
    assert post1.status_code == 200, post1.text

    # Verify Task 1 post-task measure persisted
    m1 = db.query(PostTaskMeasure).filter(PostTaskMeasure.task_session_id == ts1_id).first()
    assert m1 is not None
    assert m1.nasa_tlx_raw["mental_demand"] == 15

    # Task 2 decision & post-task workload
    dec2 = client.post("/api/v1/tasks/decision/submit", json={
        "participant_id": pid,
        "task_id": sessions[1].task_id,
        "submitted_answers": {"is_eligible": True, "first_tranche_loan_inr": 100000, "skill_stipend_per_day_inr": 500, "max_project_cost_lakhs": 50, "subsidy_percentage": 35},
        "confidence_score": 5
    })
    assert dec2.status_code == 200, dec2.text
    ts2_id = dec2.json()["task_session_id"]

    post2 = client.post("/api/v1/post-task/submit", json={
        "participant_id": pid,
        "task_session_id": ts2_id,
        "task_id": sessions[1].task_id,
        "nasa_tlx_raw": tlx_task2,
        "feedback_comments": "Task 2 complete"
    })
    assert post2.status_code == 200, post2.text

    # Task 3 decision & post-task workload
    dec3 = client.post("/api/v1/tasks/decision/submit", json={
        "participant_id": pid,
        "task_id": sessions[2].task_id,
        "submitted_answers": {"is_eligible": True, "first_tranche_loan_inr": 100000, "skill_stipend_per_day_inr": 500, "max_project_cost_lakhs": 50, "subsidy_percentage": 35},
        "confidence_score": 7
    })
    assert dec3.status_code == 200, dec3.text
    ts3_id = dec3.json()["task_session_id"]

    post3 = client.post("/api/v1/post-task/submit", json={
        "participant_id": pid,
        "task_session_id": ts3_id,
        "task_id": sessions[2].task_id,
        "nasa_tlx_raw": tlx_task3,
        "feedback_comments": "Task 3 complete"
    })
    assert post3.status_code == 200, post3.text
    assert post3.json()["status"] == "COMPLETED"

    # Verify exactly 3 distinct post-task measures exist for participant
    all_measures = db.query(PostTaskMeasure).filter(PostTaskMeasure.participant_id == pid).all()
    assert len(all_measures) == 3

    # CRITICAL: Verify Task 1 measurement was NOT overwritten by Task 2 or Task 3
    db.refresh(m1)
    assert m1.nasa_tlx_raw["mental_demand"] == 15
    assert m1.feedback_comments == "Task 1 complete"

def test_post_task_duplicate_submission_rejected(db):
    pid = create_full_participant_via_api()
    sessions = db.query(TaskSession).filter(TaskSession.participant_id == pid).order_by(TaskSession.position.asc()).all()

    tlx_task = {"mental_demand": 10, "physical_demand": 2, "temporal_demand": 8, "performance": 15, "effort": 12, "frustration": 5}
    ts_id = sessions[0].session_id

    # 1st submission -> 200 OK
    resp1 = client.post("/api/v1/post-task/submit", json={
        "participant_id": pid,
        "task_session_id": ts_id,
        "task_id": sessions[0].task_id,
        "nasa_tlx_raw": tlx_task
    })
    assert resp1.status_code == 200, resp1.text

    # Duplicate submission for same task_session_id -> 400 Bad Request
    resp2 = client.post("/api/v1/post-task/submit", json={
        "participant_id": pid,
        "task_session_id": ts_id,
        "task_id": sessions[0].task_id,
        "nasa_tlx_raw": tlx_task
    })
    assert resp2.status_code == 400
    assert "already submitted" in resp2.json()["detail"]

def test_post_task_cross_participant_submission_blocked(db):
    pid1 = create_full_participant_via_api()
    pid2 = create_full_participant_via_api()

    s1 = db.query(TaskSession).filter(TaskSession.participant_id == pid1).first()

    tlx_task = {"mental_demand": 10, "physical_demand": 2, "temporal_demand": 8, "performance": 15, "effort": 12, "frustration": 5}

    # Participant 2 attempts to submit post-task measures for Participant 1's task_session_id -> 403 Forbidden
    resp = client.post("/api/v1/post-task/submit", json={
        "participant_id": pid2,
        "task_session_id": s1.session_id,
        "task_id": s1.task_id,
        "nasa_tlx_raw": tlx_task
    })
    assert resp.status_code == 403
    assert "does not belong" in resp.json()["detail"]
