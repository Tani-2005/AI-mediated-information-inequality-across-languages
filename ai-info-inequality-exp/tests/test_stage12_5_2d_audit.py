"""
Comprehensive unit and integration tests for Stage 12.5.2D:
- Reconciled UIN-anchored M7 prompt and schema
- Reproducible M8 cluster sampling plan (60 complete cells, 180 responses)
- Metric dictionary integrity (all 13 metrics, denominators, and overlap)
- Completed annotation schema validation and round-trip serialization using synthetic records
- Updated annotation template integrity and hash preservation
"""

import json
import hashlib
import pytest
from pathlib import Path

from backend.app.scoring.lingua_audit.evaluator_protocol import (
    build_uin_anchored_semantic_prompt,
    build_cross_lingual_semantic_prompt,
    UIN_ANCHORED_SEMANTIC_PRESERVATION_SCHEMA,
    CROSS_LINGUAL_SEMANTIC_PRESERVATION_SCHEMA,
)
from backend.app.scoring.lingua_audit.annotation_schema import (
    CompletedAnnotationSubmission,
    CompletedItemAnnotation,
    CompletedClaimAnnotation,
    CompletedFactCoverage,
    CompletedImportantFactCoverage,
    CompletedCitationEvaluation,
    ClaimVerdict,
    FactCoverageStatus,
    CitationStatus,
    AnnotatorRole,
    export_json_schema,
)

BASE_DIR = Path(__file__).resolve().parent.parent


def test_uin_anchored_m7_prompt_and_schema():
    """Verify that M7 prompt is strictly anchored to benchmark UIN without metadata leaks."""
    prompt_res = build_uin_anchored_semantic_prompt(
        task_prompt="What is the subsidy under PM Vishwakarma?",
        uin_text="A citizen seeks eligibility criteria and financial subsidy under PM Vishwakarma.",
        candidate_response_text="पीएम विश्वकर्मा योजना के तहत कारीगरों को 5% ब्याज पर ऋण मिलता है।",
    )
    
    assert "user_prompt" in prompt_res
    assert "prompt_sha256" in prompt_res
    user_prompt_data = json.loads(prompt_res["user_prompt"])
    
    # Check UIN presence
    assert "underlying_information_need_uin" in user_prompt_data
    assert "PM Vishwakarma" in user_prompt_data["underlying_information_need_uin"]
    
    # Verify strict blinding (no prohibited metadata)
    raw_text = prompt_res["user_prompt"].lower()
    for prohibited in ["gpt-4o", "claude", "llama", "temperature", "repetition_index", "provider"]:
        assert prohibited not in raw_text

    # Verify UIN schema fields
    schema_props = UIN_ANCHORED_SEMANTIC_PRESERVATION_SCHEMA["schema"]["properties"]
    assert "semantic_preservation_grade" in schema_props
    assert "preservation_of_intent" in schema_props
    assert "preservation_of_scope_and_conditions" in schema_props
    assert "linguistic_appropriateness" in schema_props
    assert "drift_type" in schema_props
    assert "rationale" in schema_props


def test_m8_cluster_sample_plan_integrity():
    """Verify reproducible M8 cluster sample contains 60 complete cells (180 responses) with balance."""
    plan_path = BASE_DIR / "data" / "benchmark" / "evaluator_validation" / "stage12_5_2D_m8_cluster_sample_plan.json"
    assert plan_path.exists(), "M8 cluster sample plan file missing!"
    
    with open(plan_path, "r", encoding="utf-8") as f:
        plan = json.load(f)
        
    assert plan["sampling_parameters"]["total_cells"] == 60
    assert plan["sampling_parameters"]["total_responses"] == 180
    assert plan["sampling_parameters"]["repetitions_per_cell"] == 3
    assert plan["sampling_parameters"]["seed"] == 842105
    
    cells = plan["selected_cells"]
    assert len(cells) == 60
    
    # Check balance across strata
    domains = set(c["domain"] for c in cells)
    languages = set(c["language"] for c in cells)
    models = set(c["model"] for c in cells)
    assert len(domains) == 5
    assert len(languages) == 3
    assert len(models) == 4
    
    # Every cell must have exactly 3 repetitions
    for c in cells:
        assert len(c["response_ids"]) == 3
        assert len(c["repetition_indices"]) == 3
        
    # Verify response IDs hash
    all_resp_ids = [rid for c in cells for rid in c["response_ids"]]
    assert len(set(all_resp_ids)) == 180
    computed_hash = hashlib.sha256(json.dumps(sorted(all_resp_ids)).encode()).hexdigest()
    assert computed_hash == plan["sampling_parameters"]["response_ids_sha256"]
    assert computed_hash == "c2a3e8e96cdc95c9a3df952f50320433d9a7de8f92c89fc6ce80a0e2c35905ec"


def test_metric_dictionary_integrity():
    """Verify that stage12_5_2D_metric_dictionary.json specifies all 13 metrics with full details."""
    dict_path = BASE_DIR / "data" / "benchmark" / "evaluator_validation" / "stage12_5_2D_metric_dictionary.json"
    assert dict_path.exists(), "Metric dictionary file missing!"
    
    with open(dict_path, "r", encoding="utf-8") as f:
        m_dict = json.load(f)
        
    expected_codes = ["M1", "M1b", "M2a", "M2c", "M3", "M4a", "M4b", "M4c", "M5", "M6", "M7", "M8a", "M8b"]
    assert m_dict["total_metrics"] == 13
    assert set(m_dict["metrics"].keys()) == set(expected_codes)
    
    for code in expected_codes:
        metric = m_dict["metrics"][code]
        assert "construct" in metric
        assert "formula" in metric
        assert "unit_of_analysis" in metric
        assert "numerator" in metric
        assert "denominator" in metric
        assert "permitted_labels" in metric
        assert "missing_data_handling" in metric
        assert "direction_of_better_performance" in metric
        assert "boundary_cases" in metric
        assert "shared_underlying_judgments" in metric
        assert "status" in metric
        assert "primary_statistical_model" in metric


def test_completed_annotation_schema_validation():
    """Test validation and round-trip serialization of completed annotations with synthetic data."""
    # Synthetic item matching CompletedItemAnnotation schema
    synthetic_record = CompletedItemAnnotation(
        item_index=0,
        response_id="resp_000993d59898",
        task_id="PUB-008",
        annotator_id="HUMAN_ANNOTATOR_1",
        timestamp_utc="2026-10-11T21:50:00Z",
        rubric_version="12.5.2D",
        extracted_claims=[
            CompletedClaimAnnotation(
                claim_id="CLAIM_01",
                claim_text="[SYNTHETIC EXAMPLE FOR TESTING ONLY] PM-SVANidhi provides a 1st tranche loan of Rs. 10,000.",
                verdict=ClaimVerdict.SUPPORTED,
                matched_fact_ids=["CF1"],
                rationale="[SYNTHETIC EXAMPLE FOR TESTING ONLY] Directly corroborates Section 4 of Guidelines.",
            ),
            CompletedClaimAnnotation(
                claim_id="CLAIM_02",
                claim_text="[SYNTHETIC EXAMPLE FOR TESTING ONLY] An interest subsidy of 7% per annum is credited.",
                verdict=ClaimVerdict.SUPPORTED,
                matched_fact_ids=["CF2"],
                rationale="[SYNTHETIC EXAMPLE FOR TESTING ONLY] Corroborates Section 5 subsidy clause.",
            ),
        ],
        critical_facts_coverage=[
            CompletedFactCoverage(
                fact_id="CF1",
                status=FactCoverageStatus.COVERED,
                supporting_claim_ids=["CLAIM_01"],
                rationale="First tranche loan amount covered.",
            ),
            CompletedFactCoverage(
                fact_id="CF2",
                status=FactCoverageStatus.COVERED,
                supporting_claim_ids=["CLAIM_02"],
                rationale="Interest subsidy covered.",
            ),
            CompletedFactCoverage(
                fact_id="CF3",
                status=FactCoverageStatus.OMITTED,
                supporting_claim_ids=[],
                rationale="Digital cashback incentive omitted.",
            ),
        ],
        important_facts_coverage=[
            CompletedImportantFactCoverage(
                fact_id="IF1",
                status=FactCoverageStatus.COVERED,
                supporting_claim_ids=[],
            )
        ],
        citations_evaluation=[
            CompletedCitationEvaluation(
                citation_url_or_domain="pmsvanidhi.mohua.gov.in",
                status=CitationStatus.AUTHORITATIVE_SUPPORTING,
                is_authoritative=True,
                backed_claim_ids=["CLAIM_01", "CLAIM_02"],
            )
        ],
        m5_composite_citation_grade=4,
        m6_domain_safety_rating=0,
        m7_semantic_preservation_grade=4,
        annotator_comments="[SYNTHETIC EXAMPLE FOR TESTING ONLY] High quality response.",
    )

    submission = CompletedAnnotationSubmission(
        submission_id="SUB_SYNTHETIC_001",
        annotator_id="HUMAN_ANNOTATOR_1",
        annotator_role=AnnotatorRole.INDEPENDENT_ANNOTATOR,
        rubric_version="12.5.2D",
        created_at_utc="2026-10-11T21:55:00Z",
        sample_hash_sha256="f3dacaf03a5c782407f5d0c5a9223630e0486266214568807ce9e7ff7c604a93",
        total_items=1,
        records=[synthetic_record],
    )

    # Test round-trip serialization
    serialized = submission.model_dump_json(indent=2)
    deserialized = CompletedAnnotationSubmission.model_validate_json(serialized)
    assert deserialized.submission_id == "SUB_SYNTHETIC_001"
    assert deserialized.records[0].m7_semantic_preservation_grade == 4
    assert deserialized.records[0].critical_facts_coverage[0].status == FactCoverageStatus.COVERED


def test_completed_annotation_schema_rejects_invalid_states():
    """Verify that completed annotation schema rejects nulls, unhandled omissions, and invalid enums."""
    # Attempting to mark a fact as OMITTED while having supporting claims must fail
    with pytest.raises(ValueError, match="cannot be marked OMITTED with supporting claims"):
        CompletedItemAnnotation(
            item_index=0,
            response_id="resp_000993d59898",
            task_id="PUB-008",
            annotator_id="HUMAN_1",
            timestamp_utc="2026-10-11T21:50:00Z",
            rubric_version="12.5.2D",
            extracted_claims=[],
            critical_facts_coverage=[
                CompletedFactCoverage(
                    fact_id="CF1",
                    status=FactCoverageStatus.OMITTED,
                    supporting_claim_ids=["CLAIM_01"],  # Illegal: cannot omit and claim simultaneously
                )
            ],
            important_facts_coverage=[],
            citations_evaluation=[],
            m5_composite_citation_grade=0,
            m6_domain_safety_rating=0,
            m7_semantic_preservation_grade=3,
        )


def test_updated_template_integrity_and_uin():
    """Verify that stage12_5_2D_annotation_template.json preserves the 270 IDs and includes UINs."""
    tmpl_path = BASE_DIR / "data" / "benchmark" / "evaluator_validation" / "stage12_5_2D_annotation_template.json"
    assert tmpl_path.exists(), "Updated template file missing!"
    
    with open(tmpl_path, "r", encoding="utf-8") as f:
        tmpl = json.load(f)
        
    assert tmpl["total_responses"] == 270
    assert len(tmpl["items"]) == 270
    
    # Check frozen hash
    ids = [it["response_id"] for it in tmpl["items"]]
    computed_hash = hashlib.sha256(json.dumps(sorted(ids)).encode()).hexdigest()
    assert computed_hash == "f3dacaf03a5c782407f5d0c5a9223630e0486266214568807ce9e7ff7c604a93"
    assert tmpl["validation_ids_sha256"] == computed_hash
    
    # Check that all items have non-empty UIN
    for item in tmpl["items"]:
        assert "underlying_information_need" in item
        assert len(item["underlying_information_need"]) > 10


def test_m4a_error_deduplication_and_distinct_errors():
    """Verify that M4a deduplicates errors appearing at both claim and fact levels,

    while preserving genuinely distinct factual errors.
    """
    from backend.app.scoring.lingua_audit.schemas import (
        AtomicClaim,
        FactMatch,
        AtomicClaimCategory,
        FactCoverageStatus,
        ResponseScoringInput,
    )
    from backend.app.scoring.lingua_audit.metrics import calculate_response_metrics

    # Case 1: Deduplication - 1 claim contradicts CF1; CF1 is marked CONTRADICTED (linked).
    # Naive sum would give 1 + 1 = 2; deduplication must give exactly 1.
    inp_duplicate = ResponseScoringInput(
        response_id="R_dup",
        task_id="T1",
        language="hi",
        model="gpt-4o",
        repetition=1,
        claims=[
            AtomicClaim(
                claim_id="C1",
                text="Street vendors get Rs. 50,000 first tranche",
                category=AtomicClaimCategory.CONTRADICTED,
                matched_fact_ids=["CF1"],
            )
        ],
        critical_facts=[
            FactMatch(
                fact_id="CF1",
                is_critical=True,
                status=FactCoverageStatus.CONTRADICTED,
                supporting_claim_ids=["C1"],
            ),
            FactMatch(
                fact_id="CF2",
                is_critical=True,
                status=FactCoverageStatus.COVERED,
                supporting_claim_ids=[],
            ),
        ],
    )
    metrics_dup = calculate_response_metrics(inp_duplicate)
    assert metrics_dup.m4a_error_count == 1, "Duplicate claim-fact error must be counted as 1, not 2!"

    # Case 2: Distinct errors - Claim C1 contradicts CF1; CF2 is contradicted WITHOUT a claim.
    # Total distinct errors must be exactly 2.
    inp_distinct = ResponseScoringInput(
        response_id="R_distinct",
        task_id="T1",
        language="hi",
        model="gpt-4o",
        repetition=1,
        claims=[
            AtomicClaim(
                claim_id="C1",
                text="Street vendors get Rs. 50,000 first tranche",
                category=AtomicClaimCategory.CONTRADICTED,
                matched_fact_ids=["CF1"],
            )
        ],
        critical_facts=[
            FactMatch(
                fact_id="CF1",
                is_critical=True,
                status=FactCoverageStatus.CONTRADICTED,
                supporting_claim_ids=["C1"],
            ),
            FactMatch(
                fact_id="CF2",
                is_critical=True,
                status=FactCoverageStatus.CONTRADICTED,
                supporting_claim_ids=[],  # Unlinked distinct error on CF2
            ),
        ],
    )
    metrics_distinct = calculate_response_metrics(inp_distinct)
    assert metrics_distinct.m4a_error_count == 2, "Genuinely distinct errors across levels must both be counted!"

    # Case 3: Multiple distinct claims contradicting same CF (e.g. wrong amount C1, wrong tenure C2).
    # Both claim-level errors must be preserved (2 errors), while CF1 adds 0.
    inp_multi_claim = ResponseScoringInput(
        response_id="R_multi",
        task_id="T1",
        language="hi",
        model="gpt-4o",
        repetition=1,
        claims=[
            AtomicClaim(
                claim_id="C1",
                text="Loan amount is 50k",
                category=AtomicClaimCategory.CONTRADICTED,
                matched_fact_ids=["CF1"],
            ),
            AtomicClaim(
                claim_id="C2",
                text="Tenure is 10 years",
                category=AtomicClaimCategory.CONTRADICTED,
                matched_fact_ids=["CF1"],
            ),
        ],
        critical_facts=[
            FactMatch(
                fact_id="CF1",
                is_critical=True,
                status=FactCoverageStatus.CONTRADICTED,
                supporting_claim_ids=["C1", "C2"],
            )
        ],
    )
    metrics_multi = calculate_response_metrics(inp_multi_claim)
    assert metrics_multi.m4a_error_count == 2, "Both distinct claim-level errors must be preserved!"

    # Case 4: Contradicted claim with no CF link (auxiliary hallucination).
    inp_aux = ResponseScoringInput(
        response_id="R_aux",
        task_id="T1",
        language="hi",
        model="gpt-4o",
        repetition=1,
        claims=[
            AtomicClaim(
                claim_id="C1",
                text="Launched by World Bank in 1990",
                category=AtomicClaimCategory.CONTRADICTED,
                matched_fact_ids=[],
            )
        ],
        critical_facts=[
            FactMatch(
                fact_id="CF1",
                is_critical=True,
                status=FactCoverageStatus.COVERED,
                supporting_claim_ids=[],
            )
        ],
    )
    metrics_aux = calculate_response_metrics(inp_aux)
    assert metrics_aux.m4a_error_count == 1, "Unlinked contradicted claim must be counted!"


def test_m4c_normalized_error_rate_and_binomial_properties():
    """Verify that M4c computes bounded proportion in [0, 1] on adjudicated claims,

    returns None when denominator is zero, and matches binomial trial structure.
    """
    from backend.app.scoring.lingua_audit.schemas import (
        AtomicClaim,
        AtomicClaimCategory,
        ResponseScoringInput,
    )
    from backend.app.scoring.lingua_audit.metrics import calculate_response_metrics

    # Normal case: 2 supported, 1 contradicted, 1 unsupported -> N_adjudicated = 4
    inp = ResponseScoringInput(
        response_id="R_m4c",
        task_id="T1",
        language="en",
        model="gpt-4o",
        repetition=1,
        claims=[
            AtomicClaim(claim_id="C1", text="S1", category=AtomicClaimCategory.SUPPORTED),
            AtomicClaim(claim_id="C2", text="S2", category=AtomicClaimCategory.SUPPORTED),
            AtomicClaim(claim_id="C3", text="C1", category=AtomicClaimCategory.CONTRADICTED),
            AtomicClaim(claim_id="C4", text="U1", category=AtomicClaimCategory.UNSUPPORTED),
            AtomicClaim(claim_id="C5", text="Polite", category=AtomicClaimCategory.GENUINELY_UNSCORABLE),
        ],
    )
    m = calculate_response_metrics(inp)
    assert m.n_adjudicated == 4
    # M4c on adjudicated claims = 1 / 4 = 0.25 (bounded in [0, 1])
    assert m.m4c_normalized_error_rate_adjudicated == pytest.approx(0.25)
    assert 0.0 <= m.m4c_normalized_error_rate_adjudicated <= 1.0

    # Zero adjudicated claims: M4c must be None (undefined / NA), NOT 0.0
    inp_zero = ResponseScoringInput(
        response_id="R_zero",
        task_id="T1",
        language="en",
        model="gpt-4o",
        repetition=1,
        claims=[
            AtomicClaim(claim_id="C1", text="Hello", category=AtomicClaimCategory.GENUINELY_UNSCORABLE)
        ],
    )
    m_zero = calculate_response_metrics(inp_zero)
    assert m_zero.n_adjudicated == 0
    assert m_zero.m4c_normalized_error_rate_adjudicated is None, "Zero-claim M4c must be None (undefined/NA)!"


def test_m1_zero_claim_denominator_undefined_na():
    """Verify that M1 is strictly undefined/NA (None) when there are zero scorable claims,

    never spuriously assigned 0.0, and flagged via is_empty_claim_set.
    """
    from backend.app.scoring.lingua_audit.schemas import (
        AtomicClaim,
        AtomicClaimCategory,
        ResponseScoringInput,
    )
    from backend.app.scoring.lingua_audit.metrics import calculate_response_metrics

    # 1. Zero claims entirely (pure refusal or empty response)
    inp_empty = ResponseScoringInput(
        response_id="R_empty",
        task_id="T1",
        language="en",
        model="gpt-4o",
        repetition=1,
        claims=[],
    )
    m_empty = calculate_response_metrics(inp_empty)
    assert m_empty.n_adjudicated == 0
    assert m_empty.is_empty_claim_set is True
    assert m_empty.m1_precision is None, "Empty response M1 must be None (NA), not 0.0!"
    assert m_empty.m1b_contradiction_precision is None
    assert m_empty.m4c_normalized_error_rate_adjudicated is None

    # 2. Only conversational pleasantries (all GENUINELY_UNSCORABLE)
    inp_pleasantry = ResponseScoringInput(
        response_id="R_pleas",
        task_id="T1",
        language="hi",
        model="gpt-4o",
        repetition=1,
        claims=[
            AtomicClaim(claim_id="C1", text="Namaste", category=AtomicClaimCategory.GENUINELY_UNSCORABLE),
            AtomicClaim(claim_id="C2", text="I hope this helps", category=AtomicClaimCategory.GENUINELY_UNSCORABLE),
        ],
    )
    m_pleas = calculate_response_metrics(inp_pleasantry)
    assert m_pleas.n_adjudicated == 0
    assert m_pleas.is_empty_claim_set is True
    assert m_pleas.m1_precision is None, "Pleasantry-only response must yield None (NA) for M1!"
    assert m_pleas.m1_precision != 0.0, "M1 must NEVER be imputed as 0.0 for zero scorable claims!"


def test_pilot_packages_completeness_and_blinding():
    """Verify that the 12-item pilot annotation packages have complete response texts,

    strict double-blinding, identical item parity between Annotator A and B,
    and a correct restricted unblinding key.
    """
    pkg_master_path = BASE_DIR / "data" / "benchmark" / "evaluator_validation" / "stage12_5_2D_pilot_annotation_package.json"
    pkg_a_path = BASE_DIR / "data" / "benchmark" / "evaluator_validation" / "stage12_5_2D_pilot_annotator_A.json"
    pkg_b_path = BASE_DIR / "data" / "benchmark" / "evaluator_validation" / "stage12_5_2D_pilot_annotator_B.json"
    mapping_path = BASE_DIR / "data" / "benchmark" / "evaluator_validation" / "stage12_5_2D_pilot_restricted_mapping.json"

    assert pkg_master_path.exists(), "Master pilot package missing!"
    assert pkg_a_path.exists(), "Annotator A package missing!"
    assert pkg_b_path.exists(), "Annotator B package missing!"
    assert mapping_path.exists(), "Restricted mapping missing!"

    with open(pkg_master_path, "r", encoding="utf-8") as f:
        pkg_master = json.load(f)
    with open(pkg_a_path, "r", encoding="utf-8") as f:
        pkg_a = json.load(f)
    with open(pkg_b_path, "r", encoding="utf-8") as f:
        pkg_b = json.load(f)
    with open(mapping_path, "r", encoding="utf-8") as f:
        mapping = json.load(f)

    # 1. Total counts
    assert len(pkg_master["items"]) == 12
    assert len(pkg_a["items"]) == 12
    assert len(pkg_b["items"]) == 12
    assert len(mapping["mappings"]) == 12

    # 2. Response IDs hash
    master_rids = [it["response_id"] for it in pkg_master["items"]]
    assert len(set(master_rids)) == 12
    computed_master_hash = hashlib.sha256(json.dumps(sorted(master_rids)).encode()).hexdigest()
    assert computed_master_hash == "5c808d1830f8a95f9e903c49c09380c95f076bc4df1cfa88682bcc48952853fc"
    assert mapping["mapping_metadata"]["pilot_response_ids_sha256"] == computed_master_hash

    # 3. Item-by-item verification
    for i in range(12):
        item_master = pkg_master["items"][i]
        item_a = pkg_a["items"][i]
        item_b = pkg_b["items"][i]
        map_entry = mapping["mappings"][i]

        expected_id = f"ITEM_{i+1:02d}"
        assert item_a["item_id"] == expected_id
        assert item_b["item_id"] == expected_id
        assert map_entry["item_id"] == expected_id
        assert map_entry["response_id"] == item_master["response_id"]

        # Content parity between A and B
        assert item_a["candidate_response_text"] == item_b["candidate_response_text"]
        assert item_a["task_prompt"] == item_b["task_prompt"]
        assert item_a["underlying_information_need"] == item_b["underlying_information_need"]
        assert item_a["benchmark_evidence"] == item_b["benchmark_evidence"]

        # Response text is human-readable prose, not serialized json dict
        assert len(item_a["candidate_response_text"]) > 50
        assert not item_a["candidate_response_text"].startswith("{")

        # Ground truth completeness
        assert len(item_a["benchmark_evidence"]["critical_facts"]) >= 2
        assert len(item_a["benchmark_evidence"]["important_facts"]) >= 1
        assert len(item_a["benchmark_evidence"]["primary_sources"]) >= 1

        # Strict Double Blinding in Annotator files: NO model, provider, repetition, response_id
        for prohibited in ["response_id", "model", "provider", "repetition_index", "exact_model_identifier"]:
            assert prohibited not in item_a, f"Leak: {prohibited} in annotator A item!"
            assert prohibited not in item_b, f"Leak: {prohibited} in annotator B item!"

        # No pre-filled ratings (empty template ready for input)
        assert item_a["annotation_input"]["m5_composite_citation_grade"] is None
        assert item_a["annotation_input"]["m6_domain_safety_rating"] is None
        assert item_a["annotation_input"]["m7_semantic_preservation_grade"] is None
        assert item_b["annotation_input"]["m5_composite_citation_grade"] is None
        assert item_b["annotation_input"]["m6_domain_safety_rating"] is None
        assert item_b["annotation_input"]["m7_semantic_preservation_grade"] is None

