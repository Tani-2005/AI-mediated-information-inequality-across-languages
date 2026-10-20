"""
Targeted Audit Tests for Stage 12.5.2C Implementation Verification.
Tests end-to-end quarantine enforcement, fail-closed security guards,
strict omission vs non-coverage handling (M3), pleasantry-dilution robustness (M4c),
and paired cross-lingual prompt blinding (M7).
"""

import os
import json
import pytest

from backend.app.scoring.lingua_audit.schemas import (
    AtomicClaimCategory,
    FactCoverageStatus,
    AtomicClaim,
    FactMatch,
    ResponseScoringInput,
)
from backend.app.scoring.lingua_audit.metrics import calculate_response_metrics
from backend.app.scoring.lingua_audit.quarantine import (
    check_not_quarantined,
    safe_load_scoring_data,
)
from backend.app.scoring.lingua_audit.evaluator_protocol import (
    build_cross_lingual_semantic_prompt,
    CROSS_LINGUAL_SEMANTIC_PRESERVATION_SCHEMA,
)


def test_quarantine_fail_closed_on_direct_and_tampered_paths(tmp_path):
    """Verifies that quarantine fails closed on both exact hashes and tampered pathnames."""
    # 1. Existing quarantined file fails
    quarantined_file = os.path.join(
        "data", "benchmark", "evaluator_validation", "stage12_5_2_validation_results.json"
    )
    with pytest.raises(PermissionError) as exc_info:
        check_not_quarantined(quarantined_file)
    assert "quarantined" in str(exc_info.value).lower()

    # 2. Tampered file with quarantined filename but altered hash fails closed
    fake_quarantined = tmp_path / "stage12_5_2_validation_results.json"
    fake_quarantined.write_text('{"tampered": true}', encoding="utf-8")
    with pytest.raises(PermissionError) as exc_tamper:
        check_not_quarantined(str(fake_quarantined))
    assert "fail-closed" in str(exc_tamper.value).lower()


def test_safe_load_scoring_data():
    """Verifies safe_load_scoring_data permits legitimate files and blocks quarantined files."""
    # Valid file loads cleanly
    valid_file = os.path.join("experiment_config.json")
    data = safe_load_scoring_data(valid_file)
    assert isinstance(data, dict)
    assert "development_config" in data

    # Quarantined file raises PermissionError
    quarantined_file = os.path.join(
        "data", "benchmark", "evaluator_validation", "stage12_5_2_validation_results.json"
    )
    with pytest.raises(PermissionError):
        safe_load_scoring_data(quarantined_file)


def test_m3_strict_omission_vs_contradiction_separation():
    """Verifies that contradicted facts are distinguished from strictly omitted facts, preventing double counting."""
    # Scenario: 2 Critical Facts total.
    # CF1 is strictly OMITTED (model never mentions it).
    # CF2 is CONTRADICTED (model actively asserts a falsehood about it, e.g. wrong cap).
    inp = ResponseScoringInput(
        response_id="R_TEST",
        task_id="T_TEST",
        language="en",
        model="gpt-4o",
        repetition=1,
        claims=[
            AtomicClaim(claim_id="C1", text="Wrong cap Rs. 10 Lakh", category=AtomicClaimCategory.CONTRADICTED, matched_fact_ids=["CF2"]),
        ],
        critical_facts=[
            FactMatch(fact_id="CF1", is_critical=True, status=FactCoverageStatus.OMITTED),
            FactMatch(fact_id="CF2", is_critical=True, status=FactCoverageStatus.CONTRADICTED),
        ],
        important_facts=[],
        citations=[],
    )

    metrics = calculate_response_metrics(inp)

    # Total non-coverage includes both omitted and contradicted facts: (2 - 0) / 2 = 1.0
    assert metrics.m3_critical_omission == 1.0

    # Strict omission ONLY counts CF1 (not CF2): 1 / 2 = 0.50
    assert metrics.m3_strict_omission == 0.50

    # Factual error count catches CF2: 1
    assert metrics.m4a_error_count == 1


def test_m4c_normalized_error_rate_pleasantry_robustness():
    """Verifies that conversational pleasantries do not dilute normalized error rate when computed on adjudicated claims."""
    # Response A: 2 claims (1 supported, 1 contradicted), 0 pleasantries
    inp_concise = ResponseScoringInput(
        response_id="R_A",
        task_id="T1",
        language="en",
        model="gpt-4o",
        repetition=1,
        claims=[
            AtomicClaim(claim_id="C1", text="Valid fact", category=AtomicClaimCategory.SUPPORTED),
            AtomicClaim(claim_id="C2", text="False fact", category=AtomicClaimCategory.CONTRADICTED),
        ],
        critical_facts=[],
        important_facts=[],
        citations=[],
    )

    # Response B: Exact same factual claims + 8 pleasantries
    inp_verbose = ResponseScoringInput(
        response_id="R_B",
        task_id="T1",
        language="en",
        model="gpt-4o",
        repetition=1,
        claims=[
            AtomicClaim(claim_id="C1", text="Valid fact", category=AtomicClaimCategory.SUPPORTED),
            AtomicClaim(claim_id="C2", text="False fact", category=AtomicClaimCategory.CONTRADICTED),
        ] + [
            AtomicClaim(claim_id=f"P_{i}", text=f"Polite pleasantry {i}", category=AtomicClaimCategory.GENUINELY_UNSCORABLE)
            for i in range(8)
        ],
        critical_facts=[],
        important_facts=[],
        citations=[],
    )

    m_a = calculate_response_metrics(inp_concise)
    m_b = calculate_response_metrics(inp_verbose)

    # Raw claim denominator is diluted by pleasantries:
    assert m_a.m4c_error_rate == pytest.approx(0.50)
    assert m_b.m4c_error_rate == pytest.approx(0.10)

    # But adjudicated claim denominator is invariant to pleasantries:
    assert m_a.m4c_normalized_error_rate_adjudicated == pytest.approx(0.50)
    assert m_b.m4c_normalized_error_rate_adjudicated == pytest.approx(0.50)


def test_paired_cross_lingual_semantic_preservation_prompt():
    """Verifies build_cross_lingual_semantic_prompt properly pairs vernacular and English text without leaking metadata."""
    payload = build_cross_lingual_semantic_prompt(
        task_prompt="What are the loan terms under PM-SVANidhi?",
        vernacular_response_text="पीएम स्वनिधि योजना के तहत पहला ऋण ₹10,000 है।",
        english_reference_text="Under the PM SVANidhi scheme, the first loan tranche is Rs. 10,000.",
    )

    prompt = payload["user_prompt"]
    assert "gpt-4o" not in prompt.lower()
    assert "provider" not in prompt.lower()
    assert "repetition" not in prompt.lower()
    assert "candidate_vernacular_response" in prompt
    assert "comparator_english_response" in prompt
    assert CROSS_LINGUAL_SEMANTIC_PRESERVATION_SCHEMA["strict"] is True


def test_uin_anchored_semantic_preservation_prompt():
    """Verifies build_uin_anchored_semantic_prompt properly evaluates candidate against UIN without English dependency."""
    from backend.app.scoring.lingua_audit.evaluator_protocol import (
        build_uin_anchored_semantic_prompt,
        UIN_ANCHORED_SEMANTIC_PRESERVATION_SCHEMA,
    )

    payload = build_uin_anchored_semantic_prompt(
        task_prompt="What are the loan terms under PM-SVANidhi?",
        uin_text="A street vendor seeks the first tranche loan amount and collateral terms under PM-SVANidhi.",
        candidate_response_text="पीएम स्वनिधि योजना के तहत पहला ऋण ₹10,000 है बिना किसी गारंटी के।",
    )

    prompt = payload["user_prompt"]
    assert "gpt-4o" not in prompt.lower()
    assert "provider" not in prompt.lower()
    assert "underlying_information_need_uin" in prompt
    assert "candidate_response" in prompt
    assert UIN_ANCHORED_SEMANTIC_PRESERVATION_SCHEMA["strict"] is True
