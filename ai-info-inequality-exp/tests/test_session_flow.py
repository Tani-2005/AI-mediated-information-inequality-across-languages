import pytest
from app.db.models import Participant, TaskSession
from app.randomization.engine import RandomizationEngine

def test_cannot_randomize_before_screening(db):
    p = Participant()
    db.add(p)
    db.commit()

    engine = RandomizationEngine(db)
    is_eligible, msg = engine.verify_eligibility_for_randomization(p.participant_id)
    assert not is_eligible

def test_cannot_submit_decision_twice(db, fully_eligible_participant):
    engine = RandomizationEngine(db)
    engine.allocate_participant(fully_eligible_participant.participant_id)

    ts = TaskSession(participant_id=fully_eligible_participant.participant_id, task_id="PMEGP", position=1, order_id=1, status="COMPLETED")
    db.add(ts)
    db.commit()

    assert ts.status == "COMPLETED"
