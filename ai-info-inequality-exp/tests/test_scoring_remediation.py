"""
Unit and Integration Tests for LINGUA-AUDIT Scoring Architecture Remediation.
Verifies deterministic metric calculations, quarantine guards, synthetic replication detection,
inter-rater agreement calculations, and prompt blinding.
"""

import os
import json
import hashlib
import random
import numpy as np
import pytest

from backend.app.scoring.lingua_audit.schemas import (
    AtomicClaimCategory,
    FactCoverageStatus,
    CitationStatus,
    AtomicClaim,
    FactMatch,
    CitationEvaluation,
    ResponseScoringInput,
    ResponseMetrics,
)
from backend.app.scoring.lingua_audit.metrics import (
    calculate_response_metrics,
    calculate_cell_consistency_metrics,
    evaluate_composite_citation_grade,
)
from backend.app.scoring.lingua_audit.quarantine import (
    verify_quarantined_artifacts,
    detect_synthetic_replication,
    check_not_quarantined,
)
from backend.app.scoring.lingua_audit.agreement import (
    compute_quadratic_weighted_kappa,
    compute_icc_2_1_with_diagnostics,
)
from backend.app.scoring.lingua_audit.evaluator_protocol import (
    build_blinded_evaluation_prompt,
    EVALUATOR_JSON_SCHEMA,
)


def test_detection_of_synthetic_or_copied_reference_records():
    """Detects both exact cloning (Human 1) and manufactured perturbations (Human 2)."""
    # 1. Exact clone test (evaluator vs human 1 in 12.5.2)
    records_eval = [{"id": i, "score": 4, "text": f"resp_{i}"} for i in range(100)]
    records_h1 = [dict(r) for r in records_eval]

    is_synth, ratio, diag = detect_synthetic_replication(records_eval, records_h1)
    assert is_synth is True
    assert ratio == 1.0
    assert diag["is_exact_clone"] is True

    # 2. Manufactured perturbation test (evaluator vs human 2 in 12.5.2)
    records_h2 = [dict(r) for r in records_eval]
    records_h2[45]["score"] = 3
    records_h2[80]["score"] = 3

    is_synth_2, ratio_2, diag_2 = detect_synthetic_replication(records_eval, records_h2)
    assert is_synth_2 is True
    assert ratio_2 == 0.98
    assert diag_2["is_manufactured_perturbation"] is True
    assert diag_2["discrepancy_count"] == 2

    # 3. Genuine independent human ratings test
    rng = random.Random(999)
    records_genuine = [{"id": i, "score": rng.choice([2, 3, 4]), "text": f"resp_{i}"} for i in range(100)]
    is_synth_3, ratio_3, diag_3 = detect_synthetic_replication(records_eval, records_genuine)
    assert is_synth_3 is False
    assert ratio_3 < 0.80


def test_quarantine_manifest_and_guard():
    """Verifies quarantine manifest integrity and security guards."""
    manifest_path = os.path.join(
        "data", "benchmark", "evaluator_validation", "QUARANTINE_MANIFEST.json"
    )
    res = verify_quarantined_artifacts(manifest_path)
    assert res["total_quarantined"] == 4
    for v in res["verified"]:
        assert v["matches"] is True, f"Hash mismatch on {v['path']}"

    # Guard check: Attempting to pass quarantined file raises PermissionError
    quarantined_script = os.path.join("scratch", "run_stage12_5_2_evaluator_validation.py")
    with pytest.raises(PermissionError) as exc_info:
        check_not_quarantined(quarantined_script)
    assert "SECURITY & INTEGRITY ALERT" in str(exc_info.value)


def test_m1_claim_adjudication_and_denominators():
    """Tests M1 and M1b formulas and zero-denominator handling."""
    # Standard mixed claims
    claims = [
        AtomicClaim(claim_id="C1", text="Supported fact 1", category=AtomicClaimCategory.SUPPORTED),
        AtomicClaim(claim_id="C2", text="Supported fact 2", category=AtomicClaimCategory.SUPPORTED),
        AtomicClaim(claim_id="C3", text="Supported fact 3", category=AtomicClaimCategory.SUPPORTED),
        AtomicClaim(claim_id="C4", text="Contradicted fact", category=AtomicClaimCategory.CONTRADICTED),
        AtomicClaim(claim_id="C5", text="Unsupported claim", category=AtomicClaimCategory.UNSUPPORTED),
        AtomicClaim(claim_id="C6", text="Thank you polite", category=AtomicClaimCategory.GENUINELY_UNSCORABLE),
    ]

    inp = ResponseScoringInput(
        response_id="R1",
        task_id="T1",
        language="hi",
        model="gpt-4o",
        repetition=1,
        claims=claims,
        critical_facts=[
            FactMatch(fact_id="CF1", is_critical=True, status=FactCoverageStatus.COVERED),
            FactMatch(fact_id="CF2", is_critical=True, status=FactCoverageStatus.OMITTED),
        ],
        important_facts=[],
        citations=[],
        safety_rating=0,
    )

    metrics = calculate_response_metrics(inp)
    assert metrics.n_adjudicated == 5
    assert metrics.is_empty_claim_set is False
    # M1 = 3 / 5 = 0.60
    assert metrics.m1_precision == pytest.approx(0.60)
    # M1b = 3 / (3 + 1) = 0.75
    assert metrics.m1b_contradiction_precision == pytest.approx(0.75)
    # M4a = 1, M4b = 1
    assert metrics.m4a_error_count == 1
    assert metrics.m4b_any_error == 1
    assert metrics.m4c_error_rate == pytest.approx(1 / 6)

    # Empty claim set boundary
    empty_inp = ResponseScoringInput(
        response_id="R2",
        task_id="T1",
        language="hi",
        model="gpt-4o",
        repetition=1,
        claims=[AtomicClaim(claim_id="C1", text="Hello", category=AtomicClaimCategory.GENUINELY_UNSCORABLE)],
        critical_facts=[],
        important_facts=[],
        citations=[],
    )
    empty_metrics = calculate_response_metrics(empty_inp)
    assert empty_metrics.n_adjudicated == 0
    assert empty_metrics.is_empty_claim_set is True
    assert empty_metrics.m1_precision is None
    assert empty_metrics.m1b_contradiction_precision is None


def test_m5_composite_citation_grading_cases_a_through_i():
    """Verifies deterministic composite citation quality rubric across Cases A–I."""
    # Case F: 0 citations -> Grade 0
    assert evaluate_composite_citation_grade([]) == 0

    # Case G: 1 fabricated URL -> Grade 1
    case_g = [CitationEvaluation(url="http://fake.xyz", domain="fake.xyz", is_authoritative=False, status=CitationStatus.FABRICATED_UNREACHABLE)]
    assert evaluate_composite_citation_grade(case_g) == 1

    # Case D: 1 authoritative supporting + 1 fabricated URL -> Grade 1 (cap rule)
    case_d = [
        CitationEvaluation(url="https://pmjay.gov.in", domain="pmjay.gov.in", is_authoritative=True, status=CitationStatus.AUTHORITATIVE_SUPPORTING),
        CitationEvaluation(url="http://fake.xyz", domain="fake.xyz", is_authoritative=False, status=CitationStatus.FABRICATED_UNREACHABLE),
    ]
    assert evaluate_composite_citation_grade(case_d) == 1

    # Case E: 2 valid URLs, neither supporting -> Grade 2
    case_e = [
        CitationEvaluation(url="https://news.com", domain="news.com", is_authoritative=False, status=CitationStatus.IRRELEVANT),
        CitationEvaluation(url="https://blog.org", domain="blog.org", is_authoritative=False, status=CitationStatus.IRRELEVANT),
    ]
    assert evaluate_composite_citation_grade(case_e) == 2

    # Case B: 1 authoritative supporting + 1 irrelevant -> Grade 2 (mixed)
    case_b = [
        CitationEvaluation(url="https://pmjay.gov.in", domain="pmjay.gov.in", is_authoritative=True, status=CitationStatus.AUTHORITATIVE_SUPPORTING),
        CitationEvaluation(url="https://news.com", domain="news.com", is_authoritative=False, status=CitationStatus.IRRELEVANT),
    ]
    assert evaluate_composite_citation_grade(case_b) == 2

    # Case C: 1 supporting + 1 contradicting -> Grade 2 (mixed)
    case_c = [
        CitationEvaluation(url="https://portal.gov.in", domain="portal.gov.in", is_authoritative=True, status=CitationStatus.AUTHORITATIVE_SUPPORTING),
        CitationEvaluation(url="https://contrary.org", domain="contrary.org", is_authoritative=False, status=CitationStatus.CONTRADICTING),
    ]
    assert evaluate_composite_citation_grade(case_c) == 2

    # Case I (non-authoritative): 2 valid supporting -> Grade 3
    case_i = [
        CitationEvaluation(url="https://trustednews.com", domain="trustednews.com", is_authoritative=False, status=CitationStatus.RELEVANT_SUPPORTING),
        CitationEvaluation(url="https://ngo.org", domain="ngo.org", is_authoritative=False, status=CitationStatus.RELEVANT_SUPPORTING),
    ]
    assert evaluate_composite_citation_grade(case_i) == 3

    # Case A: 2 authoritative supporting -> Grade 4
    case_a = [
        CitationEvaluation(url="https://pmjay.gov.in", domain="pmjay.gov.in", is_authoritative=True, status=CitationStatus.AUTHORITATIVE_SUPPORTING),
        CitationEvaluation(url="https://nha.gov.in", domain="nha.gov.in", is_authoritative=True, status=CitationStatus.AUTHORITATIVE_SUPPORTING),
    ]
    assert evaluate_composite_citation_grade(case_a) == 4

    # Case H: 1 authoritative supporting backing 3 claims -> Grade 4
    case_h = [
        CitationEvaluation(url="https://pmjay.gov.in", domain="pmjay.gov.in", is_authoritative=True, status=CitationStatus.AUTHORITATIVE_SUPPORTING, backed_claim_ids=["C1", "C2", "C3"])
    ]
    assert evaluate_composite_citation_grade(case_h) == 4


def test_m8a_completeness_variance_and_hurdle():
    """Verifies cell-level M8a completeness sample variance and Hurdle zero-indicator."""
    # 3 repetitions with identical coverage (e.g., 2/2 covered each time)
    rep1 = ResponseScoringInput(response_id="R1", task_id="T1", language="en", model="gpt-4o", repetition=1, critical_facts=[FactMatch(fact_id="CF1", is_critical=True, status=FactCoverageStatus.COVERED)])
    rep2 = ResponseScoringInput(response_id="R2", task_id="T1", language="en", model="gpt-4o", repetition=2, critical_facts=[FactMatch(fact_id="CF1", is_critical=True, status=FactCoverageStatus.COVERED)])
    rep3 = ResponseScoringInput(response_id="R3", task_id="T1", language="en", model="gpt-4o", repetition=3, critical_facts=[FactMatch(fact_id="CF1", is_critical=True, status=FactCoverageStatus.COVERED)])

    cell_zero_var = calculate_cell_consistency_metrics(("T1", "en", "gpt-4o"), [rep1, rep2, rep3])
    assert cell_zero_var.m8a_variance == pytest.approx(0.0)
    assert cell_zero_var.m8a_is_zero_variance is True

    # 3 repetitions with varying coverage (1.0, 0.0, 1.0)
    rep_vary2 = ResponseScoringInput(response_id="R2", task_id="T1", language="en", model="gpt-4o", repetition=2, critical_facts=[FactMatch(fact_id="CF1", is_critical=True, status=FactCoverageStatus.OMITTED)])
    cell_pos_var = calculate_cell_consistency_metrics(("T1", "en", "gpt-4o"), [rep1, rep_vary2, rep3])
    # scores: 1.0, 0.0, 1.0 -> mean = 2/3 -> var = ((1/3)^2 + (-2/3)^2 + (1/3)^2) / 2 = (1/9 + 4/9 + 1/9)/2 = 6/18 = 0.333333
    assert cell_pos_var.m8a_variance == pytest.approx(1/3)
    assert cell_pos_var.m8a_is_zero_variance is False


def test_m8b_jaccard_and_empty_union():
    """Verifies M8b binomial overlap representation and empty-union boundary rule."""
    # Repetition 1 covers CF1, CF2
    r1 = ResponseScoringInput(response_id="R1", task_id="T1", language="en", model="gpt-4o", repetition=1, critical_facts=[FactMatch(fact_id="CF1", is_critical=True, status=FactCoverageStatus.COVERED), FactMatch(fact_id="CF2", is_critical=True, status=FactCoverageStatus.COVERED)])
    # Repetition 2 covers CF1, CF2
    r2 = ResponseScoringInput(response_id="R2", task_id="T1", language="en", model="gpt-4o", repetition=2, critical_facts=[FactMatch(fact_id="CF1", is_critical=True, status=FactCoverageStatus.COVERED), FactMatch(fact_id="CF2", is_critical=True, status=FactCoverageStatus.COVERED)])
    # Repetition 3 covers CF1 only
    r3 = ResponseScoringInput(response_id="R3", task_id="T1", language="en", model="gpt-4o", repetition=3, critical_facts=[FactMatch(fact_id="CF1", is_critical=True, status=FactCoverageStatus.COVERED), FactMatch(fact_id="CF2", is_critical=True, status=FactCoverageStatus.OMITTED)])

    cell = calculate_cell_consistency_metrics(("T1", "en", "gpt-4o"), [r1, r2, r3])
    # Overlap: {CF1} -> 1, Union: {CF1, CF2} -> 2
    assert cell.m8b_overlap_count == 1
    assert cell.m8b_union_count == 2
    assert cell.m8b_is_empty_union is False
    assert cell.m8b_jaccard == pytest.approx(0.5)

    # Empty union boundary: all repetitions omit all facts
    r_empty1 = ResponseScoringInput(response_id="R1", task_id="T1", language="en", model="gpt-4o", repetition=1, critical_facts=[FactMatch(fact_id="CF1", is_critical=True, status=FactCoverageStatus.OMITTED)])
    r_empty2 = ResponseScoringInput(response_id="R2", task_id="T1", language="en", model="gpt-4o", repetition=2, critical_facts=[FactMatch(fact_id="CF1", is_critical=True, status=FactCoverageStatus.OMITTED)])
    cell_empty = calculate_cell_consistency_metrics(("T1", "en", "gpt-4o"), [r_empty1, r_empty2])
    assert cell_empty.m8b_union_count == 0
    assert cell_empty.m8b_is_empty_union is True
    assert cell_empty.m8b_jaccard is None


def test_quadratic_weighted_kappa():
    """Verifies quadratic weighted Cohen's kappa calculation."""
    r1 = [0, 1, 2, 3, 4]
    r2 = [0, 1, 2, 3, 4]
    kappa, diag = compute_quadratic_weighted_kappa(r1, r2, 0, 4)
    assert kappa == pytest.approx(1.0)
    assert diag["status"] == "VALID"

    # Mild disagreement (off by 1)
    r1_mild = [0, 1, 2, 3, 4]
    r2_mild = [1, 2, 3, 4, 4]
    kappa_mild, _ = compute_quadratic_weighted_kappa(r1_mild, r2_mild, 0, 4)
    assert kappa_mild > 0.60


def test_icc_diagnostics_and_zero_variance():
    """Verifies ICC diagnostics for identical columns and zero-variance degeneration."""
    # Degenerate matrix: all subjects have identical rating
    matrix_zero_var = np.array([[2.0, 2.0], [2.0, 2.0], [2.0, 2.0]])
    icc_zero, diag_zero = compute_icc_2_1_with_diagnostics(matrix_zero_var)
    assert icc_zero is None
    assert diag_zero["status"] == "DEGENERATE_ZERO_TOTAL_VARIANCE"

    # Genuine variable ratings with identical columns
    matrix_cloned = np.array([[1.0, 1.0], [2.0, 2.0], [3.0, 3.0], [4.0, 4.0]])
    icc_cloned, diag_cloned = compute_icc_2_1_with_diagnostics(matrix_cloned)
    assert icc_cloned == pytest.approx(1.0)
    assert diag_cloned["is_identical_columns"] is True
    assert diag_cloned["warning"] is not None


def test_reproducible_sampling_algorithm():
    """Verifies that seed 428571 stratified random sampling reproducibly yields the exact frozen validation hash."""
    responses_file = os.path.join(
        "data", "benchmark", "raw_responses", "stage12_4_full_evaluation_responses.json"
    )
    if not os.path.exists(responses_file):
        pytest.skip("Full responses file not present")

    with open(responses_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    responses = data if isinstance(data, list) else data["responses"]

    strata = {}
    for r in responses:
        key = (r["domain"], r["language"], r["model"])
        if key not in strata:
            strata[key] = []
        strata[key].append(r)

    sorted_strata = sorted(strata.items(), key=lambda x: x[0])
    rng = random.Random(428571)
    sample = []
    for idx, (k, pool) in enumerate(sorted_strata):
        cnt = 5 if idx < 30 else 4
        sample.extend(rng.sample(pool, cnt))

    validation_ids = sorted([r["response_id"] for r in sample])
    reconstructed_hash = hashlib.sha256(json.dumps(validation_ids).encode("utf-8")).hexdigest()

    expected_hash = "f3dacaf03a5c782407f5d0c5a9223630e0486266214568807ce9e7ff7c604a93"
    assert reconstructed_hash == expected_hash


def test_blinded_prompt_construction():
    """Verifies that prompt construction enforces complete metadata blinding."""
    gt = {
        "critical_facts": [{"id": "CF1", "fact_statement": "Coverage limit is Rs. 5 Lakh", "key_terms": ["5 lakh"]}],
        "important_facts": [{"id": "IF1", "fact_statement": "Aadhaar required"}],
        "official_sources": ["https://pmjay.gov.in"],
    }

    payload = build_blinded_evaluation_prompt(
        task_prompt="What is the benefit under PM-JAY?",
        raw_response_text="The scheme offers Rs. 5 Lakh coverage per family per year.",
        benchmark_ground_truth=gt,
    )

    user_prompt = payload["user_prompt"]
    assert "gpt-4o" not in user_prompt.lower()
    assert "claude" not in user_prompt.lower()
    assert "openai" not in user_prompt.lower()
    assert "anthropic" not in user_prompt.lower()
    assert "repetition" not in user_prompt.lower()
    assert "language" not in user_prompt.lower()
    assert payload["prompt_sha256"] is not None
    assert EVALUATOR_JSON_SCHEMA["strict"] is True
