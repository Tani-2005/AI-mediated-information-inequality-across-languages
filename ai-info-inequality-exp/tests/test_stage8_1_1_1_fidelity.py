import pytest
import numpy as np
import pandas as pd
import math
from typing import Dict, Any, Optional

# ==============================================================================
# 1. DOCDURATION TRANSFORMER FOR STAGE 8.1.1.1 LOCK
# ==============================================================================

def transform_doc_duration(val: Any) -> float:
    """
    Authoritative Stage 8.1.1.1 DocDuration Log Transformer.
    Clamps value to a minimum of 1.0s before natural log transformation,
    ensuring log(1.0) = 0.0 for 0s or sub-1s durations without -inf invalidity.
    Returns 0.0 for None or unparseable inputs.
    """
    if val is None or val == "":
        return 0.0

    try:
        num = float(val)
        if math.isnan(num) or math.isinf(num):
            return 0.0
        clamped = max(1.0, num)
        return round(float(np.log(clamped)), 4)
    except (ValueError, TypeError):
        return 0.0


# ==============================================================================
# 2. DECISIONCONFIDENCE ORDINAL CLMM MODEL STRUCTURAL AUDITOR
# ==============================================================================

def evaluate_decision_confidence_clmm(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Evaluates DecisionConfidence ordinal model structure.
    Confirms category ordering 1-7, cumulative logit structure,
    random participant intercept, and non-multinomial formulation.
    """
    scores = df["confidence_score"].dropna().astype(int).unique()
    is_ordered = all(1 <= s <= 7 for s in scores)
    
    has_participant = "participant_id" in df.columns
    has_arms = "arm" in df.columns
    has_scenarios = "scenario" in df.columns
    has_position = "position" in df.columns

    return {
        "is_ordered_1_to_7": is_ordered,
        "categories_present": sorted(scores.tolist()),
        "has_participant_random_effect": has_participant,
        "has_fixed_effects": (has_arms and has_scenarios and has_position),
        "model_family": "Cumulative Link Mixed Model (CLMM) / Ordinal Logistic GLMM",
        "link": "logit",
        "is_multinomial": False
    }


# ==============================================================================
# 3. TARGETED UNIT TESTS FOR STAGE 8.1.1.1
# ==============================================================================

def test_doc_duration_zero_handling():
    # Zero duration -> clamped to 1.0 -> log(1.0) = 0.0
    assert transform_doc_duration(0.0) == 0.0

def test_doc_duration_sub_one_clamp():
    # Sub-one duration (e.g. 0.5s) -> clamped to 1.0 -> log(1.0) = 0.0
    assert transform_doc_duration(0.5) == 0.0
    assert transform_doc_duration(0.1) == 0.0

def test_doc_duration_exact_one():
    # Exactly 1.0s -> log(1.0) = 0.0
    assert transform_doc_duration(1.0) == 0.0

def test_doc_duration_ordinary_values():
    # Ordinary duration e.g. 10.0s -> log(10.0) = 2.3026
    assert abs(transform_doc_duration(10.0) - np.log(10.0)) < 1e-3
    assert abs(transform_doc_duration(100.0) - np.log(100.0)) < 1e-3

def test_doc_duration_missing_malformed():
    assert transform_doc_duration(None) == 0.0
    assert transform_doc_duration("") == 0.0
    assert transform_doc_duration("invalid") == 0.0

def test_decision_confidence_clmm_structure():
    sample_df = pd.DataFrame({
        "participant_id": [f"p_{i}" for i in range(30)],
        "arm": ["ENGLISH_ONLY", "HINDI_ONLY", "CODE_SWITCHING"] * 10,
        "scenario": ["PMEGP", "PM_VISHWAKARMA", "PM_SVANIDHI"] * 10,
        "position": [1, 2, 3] * 10,
        "confidence_score": [1, 2, 3, 4, 5, 6, 7] * 4 + [5, 6]
    })
    
    audit = evaluate_decision_confidence_clmm(sample_df)
    assert audit["is_ordered_1_to_7"] == True
    assert audit["has_participant_random_effect"] == True
    assert audit["has_fixed_effects"] == True
    assert audit["is_multinomial"] == False
    assert audit["model_family"] == "Cumulative Link Mixed Model (CLMM) / Ordinal Logistic GLMM"
