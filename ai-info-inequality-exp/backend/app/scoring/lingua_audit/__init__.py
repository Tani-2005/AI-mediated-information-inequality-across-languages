"""
LINGUA-AUDIT Scoring Architecture Package
Provides deterministic-first scoring, schema validation, quarantine enforcement,
and inter-rater agreement computation for multilingual AI information inequality audits.
"""

from .schemas import (
    AtomicClaimCategory,
    FactCoverageStatus,
    CitationStatus,
    AtomicClaim,
    FactMatch,
    CitationEvaluation,
    ResponseScoringInput,
    ResponseMetrics,
    CellLevelMetrics,
)

from .metrics import (
    calculate_response_metrics,
    calculate_cell_consistency_metrics,
    evaluate_composite_citation_grade,
)

from .quarantine import (
    verify_quarantined_artifacts,
    detect_synthetic_replication,
    check_not_quarantined,
    safe_load_scoring_data,
)

from .agreement import (
    compute_quadratic_weighted_kappa,
    compute_icc_2_1_with_diagnostics,
)

from .evaluator_protocol import (
    EVALUATOR_JSON_SCHEMA,
    UIN_ANCHORED_SEMANTIC_PRESERVATION_SCHEMA,
    CROSS_LINGUAL_SEMANTIC_PRESERVATION_SCHEMA,
    build_blinded_evaluation_prompt,
    build_uin_anchored_semantic_prompt,
    build_cross_lingual_semantic_prompt,
)

__all__ = [
    "AtomicClaimCategory",
    "FactCoverageStatus",
    "CitationStatus",
    "AtomicClaim",
    "FactMatch",
    "CitationEvaluation",
    "ResponseScoringInput",
    "ResponseMetrics",
    "CellLevelMetrics",
    "calculate_response_metrics",
    "calculate_cell_consistency_metrics",
    "evaluate_composite_citation_grade",
    "verify_quarantined_artifacts",
    "detect_synthetic_replication",
    "check_not_quarantined",
    "safe_load_scoring_data",
    "compute_quadratic_weighted_kappa",
    "compute_icc_2_1_with_diagnostics",
    "EVALUATOR_JSON_SCHEMA",
    "UIN_ANCHORED_SEMANTIC_PRESERVATION_SCHEMA",
    "CROSS_LINGUAL_SEMANTIC_PRESERVATION_SCHEMA",
    "build_blinded_evaluation_prompt",
    "build_uin_anchored_semantic_prompt",
    "build_cross_lingual_semantic_prompt",
]
