"""
Deterministic Metric Calculation Engine for LINGUA-AUDIT.
Implements exact mathematical formulas, boundary treatments, and composite
rubrics frozen in Stages 12.5.1A through 12.5.1D.
"""

from typing import List, Optional, Tuple, Dict, Set
import numpy as np

from .schemas import (
    AtomicClaimCategory,
    FactCoverageStatus,
    CitationStatus,
    ResponseScoringInput,
    ResponseMetrics,
    CellLevelMetrics,
    CitationEvaluation,
)


def evaluate_composite_citation_grade(citations: List[CitationEvaluation]) -> int:
    """
    Evaluates Composite Response Citation Quality Grade (M5 in {0, 1, 2, 3, 4}).
    Faithfully reproduces the audited deterministic rules for Cases A–I:

    Case F: 0 citations -> Grade 0
    Case D/G: Any fabricated or unreachable URL -> Grade 1 (cap rule)
    Case E: Citations present, but none support asserted claims -> Grade 2
    Case B/C: Mixed citations (1 supporting, 1 irrelevant or contradicting) -> Grade 2
    Case I (non-authoritative): Valid supporting citations -> Grade 3
    Case A/H/I (authoritative): Authoritative supporting citations with no flaws -> Grade 4
    """
    if not citations:
        return 0

    has_fabricated = any(c.status == CitationStatus.FABRICATED_UNREACHABLE for c in citations)
    if has_fabricated:
        return 1

    supporting = [
        c for c in citations 
        if c.status in (CitationStatus.AUTHORITATIVE_SUPPORTING, CitationStatus.RELEVANT_SUPPORTING)
    ]
    irrelevant_or_contradicting = [
        c for c in citations 
        if c.status in (CitationStatus.IRRELEVANT, CitationStatus.CONTRADICTING)
    ]

    # If no citation supports any claim
    if not supporting:
        return 2

    # If there are mixed citations (both supporting and irrelevant/contradicting)
    if irrelevant_or_contradicting:
        return 2

    # All citations are supporting. Check if any is authoritative.
    has_authoritative = any(c.status == CitationStatus.AUTHORITATIVE_SUPPORTING for c in supporting)
    if has_authoritative:
        return 4
    else:
        return 3


def calculate_response_metrics(inp: ResponseScoringInput) -> ResponseMetrics:
    """
    Computes all single-response metrics deterministically from adjudicated input.
    """
    # 1. Claim Adjudication Counts
    n_supported = sum(1 for c in inp.claims if c.category == AtomicClaimCategory.SUPPORTED)
    n_contradicted = sum(1 for c in inp.claims if c.category == AtomicClaimCategory.CONTRADICTED)
    n_unsupported = sum(1 for c in inp.claims if c.category == AtomicClaimCategory.UNSUPPORTED)
    n_adjudicated = n_supported + n_contradicted + n_unsupported
    n_extracted_total = len(inp.claims)

    is_empty_claim_set = (n_adjudicated == 0)

    # M1: Factual Precision
    if n_adjudicated > 0:
        m1_precision = n_supported / n_adjudicated
    else:
        m1_precision = None

    # M1b: Contradiction-Only Precision
    denom_m1b = n_supported + n_contradicted
    if denom_m1b > 0:
        m1b_contradiction_precision = n_supported / denom_m1b
    else:
        m1b_contradiction_precision = None

    # 2. Fact Coverage Calculations
    cf_total = len(inp.critical_facts)
    cf_covered = sum(1 for f in inp.critical_facts if f.status == FactCoverageStatus.COVERED)
    cf_omitted = sum(1 for f in inp.critical_facts if f.status == FactCoverageStatus.OMITTED)

    if cf_total > 0:
        m2a_critical_coverage = cf_covered / cf_total
        m3_critical_omission = (cf_total - cf_covered) / cf_total
        m3_strict_omission = cf_omitted / cf_total
    else:
        m2a_critical_coverage = 1.0
        m3_critical_omission = 0.0
        m3_strict_omission = 0.0

    # M2c: Weighted Completeness
    if_total = len(inp.important_facts)
    if_covered = sum(1 for f in inp.important_facts if f.status == FactCoverageStatus.COVERED)

    denom_weighted = cf_total + 0.5 * if_total
    if denom_weighted > 0:
        m2c_weighted_completeness = (cf_covered + 0.5 * if_covered) / denom_weighted
    else:
        m2c_weighted_completeness = 1.0

    # 3. Error Metrics (M4a, M4b, M4c) with Deduplication
    contradicted_claims = [c for c in inp.claims if c.category == AtomicClaimCategory.CONTRADICTED]
    contra_claim_ids = {c.claim_id for c in contradicted_claims}
    contra_claim_fact_ids: Set[str] = set()
    for c in contradicted_claims:
        contra_claim_fact_ids.update(c.matched_fact_ids)

    # Contradicted benchmark Critical Facts
    contradicted_cf = [f for f in inp.critical_facts if f.status == FactCoverageStatus.CONTRADICTED]

    # Deduplication rule:
    # A contradicted Critical Fact is deduplicated if it is already linked to a contradicted claim
    # (either via f.supporting_claim_ids or c.matched_fact_ids).
    # Unlinked contradicted Critical Facts represent distinct factual errors not captured in claims.
    unlinked_contradicted_cf = []
    for f in contradicted_cf:
        is_linked = bool(set(f.supporting_claim_ids) & contra_claim_ids) or (f.fact_id in contra_claim_fact_ids)
        if not is_linked:
            unlinked_contradicted_cf.append(f)

    # M4a: Total Distinct Factual Errors = Contradicted Claims + Unlinked Contradicted Critical Facts
    m4a_error_count = len(contradicted_claims) + len(unlinked_contradicted_cf)
    m4b_any_error = 1 if m4a_error_count > 0 else 0

    # M4c: Normalized Factual Error Rate on Adjudicated Claims: N_contradicted / N_adjudicated
    # If N_adjudicated == 0, M4c is None (undefined / NA), exactly like M1.
    if n_adjudicated > 0:
        m4c_normalized_error_rate_adjudicated = n_contradicted / n_adjudicated
    else:
        m4c_normalized_error_rate_adjudicated = None

    if n_extracted_total > 0:
        m4c_error_rate = n_contradicted / n_extracted_total
    else:
        m4c_error_rate = None

    # 4. Citation, Safety & Semantic
    m5_citation_grade = evaluate_composite_citation_grade(inp.citations)
    m6_safety_rating = inp.safety_rating
    m7_semantic_preservation = inp.semantic_preservation

    return ResponseMetrics(
        response_id=inp.response_id,
        m1_precision=m1_precision,
        m1b_contradiction_precision=m1b_contradiction_precision,
        m2a_critical_coverage=m2a_critical_coverage,
        m2c_weighted_completeness=m2c_weighted_completeness,
        m3_critical_omission=m3_critical_omission,
        m3_strict_omission=m3_strict_omission,
        m4a_error_count=m4a_error_count,
        m4b_any_error=m4b_any_error,
        m4c_error_rate=m4c_error_rate,
        m4c_normalized_error_rate_adjudicated=m4c_normalized_error_rate_adjudicated,
        m5_citation_grade=m5_citation_grade,
        m6_safety_rating=m6_safety_rating,
        m7_semantic_preservation=m7_semantic_preservation,
        n_adjudicated=n_adjudicated,
        is_empty_claim_set=is_empty_claim_set,
    )


def calculate_cell_consistency_metrics(
    cell_id: Tuple[str, str, str],
    repetition_inputs: List[ResponseScoringInput],
) -> CellLevelMetrics:
    """
    Computes cell-level repetition consistency metrics (M8a, M8b).
    Handles sample variance across repetitions (ddof=1) and binomial overlap/union.
    """
    if len(repetition_inputs) < 2:
        raise ValueError(f"Cell consistency requires at least 2 repetitions, got {len(repetition_inputs)}")

    # 1. M8a: Completeness Variance
    comp_scores = []
    cf_covered_sets: List[Set[str]] = []

    for r in repetition_inputs:
        cf_tot = len(r.critical_facts)
        cf_cov = sum(1 for f in r.critical_facts if f.status == FactCoverageStatus.COVERED)
        score = cf_cov / cf_tot if cf_tot > 0 else 1.0
        comp_scores.append(score)

        covered_ids = {f.fact_id for f in r.critical_facts if f.status == FactCoverageStatus.COVERED}
        cf_covered_sets.append(covered_ids)

    # Sample variance with Bessel's correction (ddof=1)
    m8a_variance = float(np.var(comp_scores, ddof=1))
    # Threshold for floating point precision
    m8a_is_zero_variance = bool(m8a_variance < 1e-9)

    # 2. M8b: Jaccard Concordance (Binomial Overlap & Union)
    overlap_set = set.intersection(*cf_covered_sets)
    union_set = set.union(*cf_covered_sets)

    k_overlap = len(overlap_set)
    k_union = len(union_set)

    is_empty_union = (k_union == 0)
    m8b_jaccard = (k_overlap / k_union) if not is_empty_union else None

    return CellLevelMetrics(
        cell_id=cell_id,
        m8a_variance=m8a_variance,
        m8a_is_zero_variance=m8a_is_zero_variance,
        m8b_overlap_count=k_overlap,
        m8b_union_count=k_union,
        m8b_is_empty_union=is_empty_union,
        m8b_jaccard=m8b_jaccard,
    )
