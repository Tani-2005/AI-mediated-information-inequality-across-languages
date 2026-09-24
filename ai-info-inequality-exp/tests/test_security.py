import pytest
from app.scoring.engine import ScoringEngine

def test_ground_truth_isolation():
    # Verify that scenario details API payload excludes ground truth answers
    details = ScoringEngine.load_rubric("PMEGP")
    
    public_payload = {
        "task_id": details["task_id"],
        "name": details["name"],
        "domain": details["domain"],
        "persona": details["persona"],
        "official_sources": details["official_sources"]
    }

    assert "ground_truth_rubric" not in public_payload
    assert "correct_answer" not in str(public_payload)
