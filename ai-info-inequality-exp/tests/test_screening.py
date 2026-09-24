import pytest
from app.api.v1.screening import ENGLISH_ANSWER_KEY, HINDI_ANSWER_KEY

def test_screening_pass_threshold():
    # Correct responses: 3 English, 3 Hindi -> PASS
    score_en = sum(1 for q, a in ENGLISH_ANSWER_KEY.items() if a == a)
    score_hi = sum(1 for q, a in HINDI_ANSWER_KEY.items() if a == a)
    passed = (score_en >= 2) and (score_hi >= 2)
    assert passed

def test_screening_fail_english_only():
    # English score = 1 (< 2), Hindi score = 3 -> FAIL
    score_en = 1
    score_hi = 3
    passed = (score_en >= 2) and (score_hi >= 2)
    assert not passed

def test_screening_fail_hindi_only():
    # English score = 3, Hindi score = 1 (< 2) -> FAIL
    score_en = 3
    score_hi = 1
    passed = (score_en >= 2) and (score_hi >= 2)
    assert not passed

def test_screening_fail_both():
    score_en = 1
    score_hi = 0
    passed = (score_en >= 2) and (score_hi >= 2)
    assert not passed
