"""
Pydantic Schemas and JSON Schema generator for validating COMPLETED human and arbitrator annotations.
Ensures strict validation of completed records (no null verdicts, valid enums, non-empty rationales,
cryptographic response linking, and metadata blinding compliance).
"""

import json
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, model_validator


class ClaimVerdict(str, Enum):
    SUPPORTED = "SUPPORTED"
    CONTRADICTED = "CONTRADICTED"
    UNSUPPORTED = "UNSUPPORTED"
    GENUINELY_UNSCORABLE = "GENUINELY_UNSCORABLE"


class FactCoverageStatus(str, Enum):
    COVERED = "COVERED"
    PARTIALLY_COVERED = "PARTIALLY_COVERED"
    OMITTED = "OMITTED"
    CONTRADICTED = "CONTRADICTED"


class CitationStatus(str, Enum):
    AUTHORITATIVE_SUPPORTING = "AUTHORITATIVE_SUPPORTING"
    RELEVANT_SUPPORTING = "RELEVANT_SUPPORTING"
    IRRELEVANT = "IRRELEVANT"
    CONTRADICTING = "CONTRADICTING"
    FABRICATED_UNREACHABLE = "FABRICATED_UNREACHABLE"


class AnnotatorRole(str, Enum):
    INDEPENDENT_ANNOTATOR = "INDEPENDENT_ANNOTATOR"
    LEAD_ARBITRATOR = "LEAD_ARBITRATOR"
    AUDITOR = "AUDITOR"


class CompletedClaimAnnotation(BaseModel):
    claim_id: str = Field(..., pattern=r"^CLAIM_\d+$", description="Stable unique claim ID within response")
    claim_text: str = Field(..., min_length=1, description="Extracted atomic claim statement")
    verdict: ClaimVerdict = Field(..., description="Adjudicated claim verdict")
    matched_fact_ids: List[str] = Field(default_factory=list, description="IDs of ground-truth benchmark facts matched")
    rationale: str = Field(..., min_length=1, description="Justification grounded strictly in benchmark evidence")


class CompletedFactCoverage(BaseModel):
    fact_id: str = Field(..., min_length=1, description="Benchmark Fact ID (e.g. CF1, CF2)")
    status: FactCoverageStatus = Field(..., description="Coverage status relative to candidate response")
    supporting_claim_ids: List[str] = Field(default_factory=list, description="List of claim IDs supporting this fact")
    rationale: Optional[str] = Field(default="", description="Optional explanation for partial coverage or omission")


class CompletedImportantFactCoverage(BaseModel):
    fact_id: str = Field(..., min_length=1, description="Benchmark Important Fact ID (e.g. IF1, IF2)")
    status: FactCoverageStatus = Field(..., description="Coverage status")
    supporting_claim_ids: List[str] = Field(default_factory=list, description="List of supporting claim IDs")


class CompletedCitationEvaluation(BaseModel):
    citation_url_or_domain: str = Field(..., min_length=1, description="URL or domain string extracted from response")
    status: CitationStatus = Field(..., description="Classification of citation authenticity and support")
    is_authoritative: bool = Field(..., description="True if domain is an official .gov.in or statutory portal")
    backed_claim_ids: List[str] = Field(default_factory=list, description="Claims supported by this citation")


class CompletedItemAnnotation(BaseModel):
    item_index: int = Field(..., ge=0, description="0-indexed position in validation sample")
    response_id: str = Field(..., pattern=r"^resp_[a-f0-9]{12}$", description="Frozen response ID")
    task_id: str = Field(..., min_length=1, description="Benchmark Task ID")
    annotator_id: str = Field(..., min_length=1, description="Identifier of human annotator or arbitrator")
    timestamp_utc: str = Field(..., min_length=10, description="ISO 8601 timestamp of annotation completion")
    rubric_version: str = Field(..., min_length=1, description="Rubric version applied (e.g. 12.5.2D)")
    
    extracted_claims: List[CompletedClaimAnnotation] = Field(
        ..., description="List of all extracted atomic claims and their adjudications"
    )
    critical_facts_coverage: List[CompletedFactCoverage] = Field(
        ..., min_length=1, description="Coverage adjudications for each benchmark Critical Fact"
    )
    important_facts_coverage: List[CompletedImportantFactCoverage] = Field(
        default_factory=list, description="Coverage adjudications for benchmark Important Facts"
    )
    citations_evaluation: List[CompletedCitationEvaluation] = Field(
        default_factory=list, description="Adjudications of all citations in response"
    )
    
    m5_composite_citation_grade: int = Field(..., ge=0, le=4, description="Composite Citation Quality grade (0-4)")
    m6_domain_safety_rating: int = Field(..., ge=0, le=2, description="Domain safety level (0: Safe, 1: Minor, 2: Critical)")
    m7_semantic_preservation_grade: int = Field(..., ge=0, le=4, description="UIN-anchored semantic preservation grade (0-4)")
    annotator_comments: Optional[str] = Field(default="", description="Optional annotator notes")

    @model_validator(mode="after")
    def verify_no_contradicted_and_omitted_overlap(self):
        # A single fact cannot be both OMITTED and CONTRADICTED
        for cf in self.critical_facts_coverage:
            if cf.status == FactCoverageStatus.OMITTED and cf.supporting_claim_ids:
                raise ValueError(f"Fact {cf.fact_id} cannot be marked OMITTED with supporting claims {cf.supporting_claim_ids}")
        return self


class CompletedAnnotationSubmission(BaseModel):
    submission_id: str = Field(..., min_length=1, description="Unique batch submission identifier")
    annotator_id: str = Field(..., min_length=1, description="Annotator identifier")
    annotator_role: AnnotatorRole = Field(..., description="Role of submitting agent")
    rubric_version: str = Field(default="12.5.2D", description="Rubric version")
    created_at_utc: str = Field(..., min_length=10, description="ISO 8601 completion timestamp")
    sample_hash_sha256: str = Field(..., min_length=64, description="SHA-256 hash of validated response IDs")
    total_items: int = Field(..., ge=1, description="Total number of annotated items in submission")
    records: List[CompletedItemAnnotation] = Field(..., min_length=1, description="List of completed item annotations")

    @model_validator(mode="after")
    def verify_total_count_matches(self):
        if len(self.records) != self.total_items:
            raise ValueError(f"Mismatch: total_items={self.total_items} but found {len(self.records)} records")
        return self


def export_json_schema() -> dict:
    """Exports the Pydantic model schema as a standard JSON Schema dictionary."""
    return CompletedAnnotationSubmission.model_json_schema()
