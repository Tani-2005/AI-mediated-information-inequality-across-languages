import pytest
from app.scoring.engine import ScoringEngine

def test_pmegp_full_credit_scoring():
    answers = {
        "is_eligible": True,
        "max_project_cost_lakhs": 50.0,
        "subsidy_percentage": 35.0,
        "mandatory_documents": ["aadhaar_card", "edp_certificate", "detailed_project_report", "rural_caste_certificate"]
    }
    score, breakdown = ScoringEngine.score_decision("PMEGP", answers)
    assert score == 10.0
    assert breakdown["is_eligible"]["points_earned"] == 2.0
    assert breakdown["max_project_cost_lakhs"]["points_earned"] == 2.0
    assert breakdown["subsidy_percentage"]["points_earned"] == 3.0
    assert breakdown["mandatory_documents"]["points_earned"] == 3.0

def test_pm_vishwakarma_full_credit_scoring():
    answers = {
        "is_eligible": True,
        "first_tranche_loan_inr": 100000.0,
        "skill_stipend_per_day_inr": 500.0,
        "toolkit_incentive_grant_inr": 15000.0
    }
    score, breakdown = ScoringEngine.score_decision("PM_VISHWAKARMA", answers)
    assert score == 10.0

def test_pm_svanidhi_full_credit_scoring():
    answers = {
        "is_eligible": True,
        "first_tranche_loan_inr": 10000.0,
        "interest_subsidy_percentage": 7.0,
        "max_annual_cashback_inr": 1200.0
    }
    score, breakdown = ScoringEngine.score_decision("PM_SVANIDHI", answers)
    assert score == 10.0

def test_scoring_missing_fields():
    answers = {
        "is_eligible": True
        # missing other fields
    }
    score, breakdown = ScoringEngine.score_decision("PMEGP", answers)
    assert score == 2.0
    assert breakdown["max_project_cost_lakhs"]["status"] == "MISSING"

def test_scoring_partial_credit_multiselect():
    answers = {
        "is_eligible": True,
        "max_project_cost_lakhs": 50.0,
        "subsidy_percentage": 35.0,
        "mandatory_documents": ["aadhaar_card", "edp_certificate"] # 2 of 4 items
    }
    score, breakdown = ScoringEngine.score_decision("PMEGP", answers)
    assert score == 8.5 # 2 + 2 + 3 + 1.5
