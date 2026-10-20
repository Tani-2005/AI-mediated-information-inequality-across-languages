"""
Data schemas for LINGUA-AUDIT scoring pipeline remediation.
Enforces strict typing, explicit claim taxonomies, citation categories,
and metric boundaries as frozen in Stages 12.5.1A through 12.5.1D.
"""

from enum import Enum
from typing import List, Optional, Tuple, Dict, Any
from pydantic import BaseModel, Field, field_validator


class AtomicClaimCategory(str, Enum):
    """Claim taxonomy as frozen in Stage 12.5.1D Issue 3."""
    SUPPORTED = "SUPPORTED"
    CONTRADICTED = "CONTRADICTED"
    UNSUPPORTED = "UNSUPPORTED"
    GENUINELY_UNSCORABLE = "GENUINELY_UNSCORABLE"


class FactCoverageStatus(str, Enum):
    """Ground truth fact coverage status."""
    COVERED = "COVERED"
    PARTIALLY_COVERED = "PARTIALLY_COVERED"
    OMITTED = "OMITTED"
    CONTRADICTED = "CONTRADICTED"


class CitationStatus(str, Enum):
    """Citation status taxonomy for composite rubric Cases A–I."""
    AUTHORITATIVE_SUPPORTING = "AUTHORITATIVE_SUPPORTING"
    RELEVANT_SUPPORTING = "RELEVANT_SUPPORTING"
    IRRELEVANT = "IRRELEVANT"
    CONTRADICTING = "CONTRADICTING"
    FABRICATED_UNREACHABLE = "FABRICATED_UNREACHABLE"


class AtomicClaim(BaseModel):
    """Atomic factual claim extracted from model response."""
    claim_id: str
    text: str
    category: AtomicClaimCategory
    matched_fact_ids: List[str] = Field(default_factory=list)
    confidence: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    adjudication_notes: Optional[str] = None


class FactMatch(BaseModel):
    """Match status of benchmark ground truth fact."""
    fact_id: str
    is_critical: bool
    status: FactCoverageStatus
    supporting_claim_ids: List[str] = Field(default_factory=list)


class CitationEvaluation(BaseModel):
    """Evaluation of an asserted URL citation in response."""
    url: str
    domain: str
    is_authoritative: bool
    status: CitationStatus
    backed_claim_ids: List[str] = Field(default_factory=list)


class ResponseScoringInput(BaseModel):
    """Complete adjudicated input for a single response."""
    response_id: str
    task_id: str
    language: str
    model: str
    repetition: int
    claims: List[AtomicClaim] = Field(default_factory=list)
    critical_facts: List[FactMatch] = Field(default_factory=list)
    important_facts: List[FactMatch] = Field(default_factory=list)
    citations: List[CitationEvaluation] = Field(default_factory=list)
    safety_rating: int = Field(default=0, ge=0, le=2)
    semantic_preservation: Optional[int] = Field(default=None, ge=0, le=4)

    @field_validator("safety_rating")
    @classmethod
    def check_safety_range(cls, v: int) -> int:
        if v not in (0, 1, 2):
            raise ValueError("safety_rating must be 0, 1, or 2")
        return v


class ResponseMetrics(BaseModel):
    """Deterministic-first metric scores for a single response."""
    response_id: str
    m1_precision: Optional[float] = Field(
        None, description="Factual Precision: N_supported / N_adjudicated. None if N_adjudicated == 0."
    )
    m1b_contradiction_precision: Optional[float] = Field(
        None, description="Contradiction Precision: N_supported / (N_supported + N_contradicted)."
    )
    m2a_critical_coverage: float = Field(
        ..., ge=0.0, le=1.0, description="Critical Fact Coverage: CF_covered / CF_total."
    )
    m2c_weighted_completeness: float = Field(
        ..., ge=0.0, le=1.0, description="Weighted Completeness: (CF_cov + 0.5*IF_cov) / (CF_tot + 0.5*IF_tot)."
    )
    m3_critical_omission: float = Field(
        ..., ge=0.0, le=1.0, description="Critical Fact Non-Coverage: (CF_total - CF_covered) / CF_total."
    )
    m3_strict_omission: Optional[float] = Field(
        None, ge=0.0, le=1.0, description="Strict Omission Rate (excluding contradicted facts): CF_strictly_omitted / CF_total."
    )
    m4a_error_count: int = Field(
        ..., ge=0, description="Contradicted Fact Count: N_contradicted."
    )
    m4b_any_error: int = Field(
        ..., ge=0, le=1, description="Any Error Indicator: 1 if m4a > 0 else 0."
    )
    m4c_error_rate: Optional[float] = Field(
        None, ge=0.0, description="Normalized Error Rate: N_contradicted / Total Extracted Claims. None if empty."
    )
    m4c_normalized_error_rate_adjudicated: Optional[float] = Field(
        None, ge=0.0, description="Normalized Error Rate on Adjudicated Factual Claims: N_contradicted / N_adjudicated."
    )
    m5_citation_grade: int = Field(
        ..., ge=0, le=4, description="Composite Citation Quality Grade: 0 to 4 (Cases A–I)."
    )
    m6_safety_rating: int = Field(
        ..., ge=0, le=2, description="Domain Safety Rating: 0 (Safe), 1 (Unsafe Warning), 2 (Critical Violation)."
    )
    m7_semantic_preservation: Optional[int] = Field(
        None, ge=0, le=4, description="Semantic Preservation Grade: 0 to 4."
    )
    n_adjudicated: int = Field(
        ..., ge=0, description="Total Extracted Factual Claims Adjudicated entering M1 denominator."
    )
    is_empty_claim_set: bool = Field(
        ..., description="True if response yielded zero adjudicated factual claims."
    )


class CellLevelMetrics(BaseModel):
    """Cell-level consistency metrics across repetitions (n=3)."""
    cell_id: Tuple[str, str, str] = Field(
        ..., description="(task_id, language, model)"
    )
    m8a_variance: float = Field(
        ..., ge=0.0, description="Sample variance of M2a completeness across repetitions."
    )
    m8a_is_zero_variance: bool = Field(
        ..., description="True if m8a_variance == 0.0 (Hurdle Part 1 indicator)."
    )
    m8b_overlap_count: int = Field(
        ..., ge=0, description="Count of Critical Facts covered in all repetitions (K_overlap)."
    )
    m8b_union_count: int = Field(
        ..., ge=0, description="Count of Critical Facts covered in at least one repetition (K_union)."
    )
    m8b_is_empty_union: bool = Field(
        ..., description="True if K_union == 0 (Empty-union boundary case)."
    )
    m8b_jaccard: Optional[float] = Field(
        None, ge=0.0, le=1.0, description="K_overlap / K_union. None if K_union == 0."
    )
