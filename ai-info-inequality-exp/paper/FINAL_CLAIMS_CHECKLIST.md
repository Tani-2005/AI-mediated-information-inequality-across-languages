# LINGUA-AUDIT: Final Claims Checklist & Verification Matrix

**Date:** 13 October 2026  
**Framing:** Benchmark-Design, Measurement Specification, and Reproducibility Framework Paper  
**Purpose:** Maps every major claim in the research paper draft to its exact supporting artifact, forensic verification status, or explicit designation as **PENDING VERIFICATION** / **FUTURE WORK**.

---

## Matrix Summary

- **Total Claims Audited:** 21
- **Supported by Verified Artifacts:** 13
- **Explicitly Disclosed as Pending Verification / Future Work:** 5
- **Identified as Invalid & Quarantined (Excluded):** 3

---

## Detailed Claims Audit

| ID | Paper Section | Claim Statement | Supporting Artifact / Source File | Verification Status | Forensic Notes |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **C1** | §1, §5 | Benchmark consists of 150 administrative and civic tasks across 5 domains (30 tasks/domain) in a civic-information benchmark design. | `data/benchmark/master_task_registry_150.json` | **VERIFIED** | Exactly 30 tasks in Healthcare, Education, Public Services, Finance, General Knowledge. Termed a civic-information benchmark. |
| **C2** | §5 | Every benchmark task is grounded in official statutory/administrative sources with 3 Critical Facts and 2 Important Facts. | `data/benchmark/master_task_registry_150.json` | **VERIFIED (INTERNAL CURATION)** | Total 450 CFs, 300 IFs, 150 primary sources, 150 safety constraints. Ground truth records source names, authorities, and cutoff dates, but lacks direct URLs, verbatim passages, or clause alignment; reflects internal curation, not external independent panel validation. |
| **C3** | §5 | Tasks are anchored to language-agnostic Underlying Information Needs (UIN) rather than English target texts. | `data/benchmark/master_task_registry_150.json` | **VERIFIED** | Every task has an explicit `uin` string defining scope, intent, and conditions independently of surface language. |
| **C4** | §6, §7 | The software pipeline verifies a full factorial matrix across $150 \text{ tasks} \times 3 \text{ languages} \times 4 \text{ target model slots} \times 3 \text{ repetitions} = 5,400 \text{ cells}$. | `data/benchmark/raw_responses/stage12_4_full_evaluation_responses.json` | **VERIFIED (PIPELINE FIXTURES)** | 5,400 programmatic baseline fixtures instantiate all factorial cells for pipeline testing. Live model API dispatches remain future work; all 4 models are target slots. |
| **C5** | §7 | Factorial coverage of pipeline fixtures is 100.0% with zero missing cells, zero duplicates, and zero dry-run contamination. | `data/benchmark/raw_responses/stage12_4_dataset_integrity_manifest.json` | **VERIFIED** | Cell uniqueness: 5,400 / 5,400; missing: 0; duplicates: 0; dry-run records: 0. |
| **C6** | §7 | Primary fixture dataset SHA-256 matches registered integrity manifest. | `data/benchmark/raw_responses/stage12_4_dataset_integrity_manifest.json` | **VERIFIED** | Canonical sorted JSON SHA-256 is `296bb1650f06cc7934f16e90ef662f9c9b0207971344b0935ee02704b8bf4248`; raw bytes SHA-256 is `095b8caa9497b4d8cf804b29baad23b4d3de813bda9f865b7a1da3ef658ca5f3`. |
| **C7** | §7 | Baseline fixtures in Stage 12.4 were generated programmatically via in-memory template synthesis. | `scratch/run_stage12_4_full_evaluation.py` (lines 51–65) | **VERIFIED** | In-memory template rendering executed in 0.15s total; latency recorded as 0 ms across all 5,400 records. Disclosed transparently. |
| **C8** | §8 | Measurement framework specifies 13 operationalized metrics across precision, coverage, omission, error, citation, safety, semantic preservation, and consistency. | `data/benchmark/evaluator_validation/stage12_5_2D_metric_dictionary.json` | **VERIFIED (SPECIFICATION)** | M1, M1b, M2a, M2c, M3, M4a, M4b, M4c, M5, M6, M7, M8a, M8b operationalized. M2c LMM is marked provisional (bounded support), M8a Gamma hurdle component is marked provisional (discrete rational variance from n=3, df=2), and M8b Binomial GLMM is marked provisional (set-theoretic overlap). |
| **C9** | §8 | Metric scoring implementation is fully realized in Python and verified by unit test suite. | `backend/app/scoring/lingua_audit/metrics.py`, `tests/test_scoring_remediation.py` | **VERIFIED (SOFTWARE ONLY)** | 115 passing unit tests verify code execution, zero-claim None handling, M4a deduplication, M4c binomial formulation, and Hurdle models. Confirms software behavior, NOT construct validity. |
| **C10** | §8, §10 | The 13 substantive quality metrics are empirically validated against human ground truth. | None | **NOT VALIDATED / PENDING** | **NOT VALIDATED.** Unit tests establish software fidelity, not construct validity. Independent human annotation has not yet been conducted. |
| **C11** | §4, §10 | Prior Stage 12.5.2 validation proved high automated evaluator agreement (ICC=1.0000, kappa=0.9849). | `scratch/run_stage12_5_2_evaluator_validation.py` | **FABRICATED / QUARANTINED** | **INVALID.** Stage 12.5.2 cloned evaluator outputs into purported human annotations. Quarantined under `QUARANTINE_MANIFEST.json`. Excluded from paper. |
| **C12** | §10, §12 | Empirical scoring of the 5,400 responses demonstrates statistically significant language disparities in live LLMs. | None | **REJECTED / UNEXECUTED** | Live model response collection (API execution) and human evaluator calibration are separate unexecuted activities. Substantive scoring and model fitting are blocked until genuine responses are collected and evaluators calibrated. |
| **C13** | §10 | Diagnostic word lengths of synthetic fixtures (English: 47.16 words; Hindi: 46.16 words; Code-Switching: 46.16 words). | `paper/results/results_summary.json`, `paper/results/table2_response_characteristics.md` | **VERIFIED (DIAGNOSTIC FIXTURES)** | Computed directly from 5,400 programmatic fixtures; reported under "Synthetic Fixture Diagnostics", NOT as live model findings. |
| **C14** | §10 | Hindi synthetic fixtures exhibit hybrid script scaffolding (9.36% Devanagari, 90.64% Latin). | `paper/results/results_summary.json`, `paper/results/table4_script_adherence.md` | **VERIFIED (DIAGNOSTIC FIXTURES)** | Computed from Unicode code points; reflects template scaffolding, NOT live model generation. |
| **C15** | §10 | Within-cell length variance across repetitions in synthetic fixtures is 0.0 across 100.0% of cells. | `paper/results/results_summary.json` | **VERIFIED (DIAGNOSTIC FIXTURES)** | Deterministic baseline synthesis produced identical text across repetitions in all 1,800 fixture cells. |
| **C16** | §9 | Prespecified statistical analysis plan specifies GLMMs, CLMMs, and Two-Part Hurdle models with Holm-Bonferroni correction. | `stage12_5_1_measurement_statistical_analysis_freeze.md`, `stage12_5_2D_metric_dictionary.json` | **VERIFIED (PLAN)** | Confirmatory family finalized as $m = 3 \text{ endpoints} \times 3 \text{ contrasts} = 9$ pooled language tests under Holm step-down correction ($\alpha = 0.05$). Model-stratified tests ($m=36$) designated as exploratory (FDR). |
| **C17** | §9, §10 | GLMM parameter estimates and odds ratios for language disparities on live models. | None | **FUTURE WORK (NO FITTED MODELS)** | Pre-specified analysis plan awaits execution on validated live-model generations. Zero models have been fitted to data. |
| **C18** | §4, §10 | A 12-item human-annotation feasibility pilot package has been prepared. | `data/benchmark/evaluator_validation/stage12_5_2D_pilot_annotation_package.json` | **VERIFIED** | Blinded packages A and B, restricted key, and annotation guide prepared; execution pending annotator recruitment. |
| **C19** | §13 | Study utilizes public civic information and synthetic queries, posing minimal human participant risk. | `docs/ethics/ethics_application.md` | **VERIFIED** | Tasks drawn from open civic schemes; benchmark evaluated with synthetic queries without human subjects. |
| **C20** | §13 | Study has received formal IRB approval. | `docs/ethics/ethics_application.md` | **PENDING REVIEW** | Institutional ethics application prepared; formal institutional approval pending committee review. |
| **C21** | §13, §16 | Public access, licensing, and reproducibility statement. | Repository artifacts, `paper/LINGUA_AUDIT_manuscript_draft.md` | **QUALIFIED** | Artifacts verified present in repository; intended for CC-BY-NC 4.0 release upon publication. Standalone LICENSE file not yet committed to repository root. |

---

## Gate Checklist & Governance Directives

- [x] **Benchmark-Design & Framework Framing:** Manuscript consistently presents the benchmark design, operational metrics, and prespecified analysis plan as the core contribution; sections 11 and 14 describe what the framework is designed to test, not demonstrated disparities.
- [x] **Civic-Information Benchmark Terminology:** Standardized terminology to "civic-information benchmark"; novelty framed as a design contribution rather than an unsupported first-of-its-kind claim.
- [x] **Finalized Confirmatory Hypothesis Family:** Finalized single confirmatory family as $m=9$ pooled population-level language main effects under Holm-Bonferroni correction ($\alpha=0.05$); justified pooling to maximize statistical power for systemic disparity detection, with model-stratified tests designated as exploratory under FDR.
- [x] **Separation of API Execution from Evaluator Calibration:** Live model API execution (data collection) and human evaluator calibration (evaluator validation) are explicitly treated as distinct activities; downstream scoring is gated on both.
- [x] **Audited Statistical Analysis Plan:** Explicitly marked M2c LMM as provisional (bounded support), M8a Gamma hurdle component as provisional (discrete rational variance from n=3, df=2), and M8b Binomial GLMM as provisional (set-theoretic overlap). Stated that zero proposed models have been fitted or empirically validated.
- [x] **Target Model Slots Framing:** All four model identifiers (`gemini-3.5-flash`, `gpt-4o`, `claude-3.5-sonnet`, `llama-3.1-70b`) are described strictly as target architecture slots in the benchmark execution protocol, without implying live endpoints were queried.
- [x] **Source Registry Verification:** Confirmed that `primary_sources` in `master_task_registry_150.json` records scheme names, authorities, and cutoff dates, but lacks direct URLs, excerpted passages, or clause-level alignment. Distinguished internal author curation from independent external panel validation.
- [x] **Qualified Licensing & Reproducibility:** Qualified licensing claims to reflect intended CC-BY-NC 4.0 release upon publication (noting absence of a standalone LICENSE file in repo root).
- [x] **No Quarantined Artifacts in Results:** Zero statistics from `stage12_5_2_validation_results.json` or `run_stage12_5_2_evaluator_validation.py` are cited as evidence.
- [x] **Transparent Provenance Disclosure:** Paper explicitly discloses that Stage 12.4 responses were synthesized programmatically as software verification fixtures, and Stage 12.5.2 validation was invalidated.
- [x] **Separation of Verified vs. Pending:** Verified benchmark characteristics (tasks, domains, ground truth counts) are reported; synthetic fixture diagnostics are confined to Section 10; live model evaluations and quality metric evaluations ($M_1$–$M_8$) are reported strictly as future work.
- [x] **Test Suite Verification:** Confirmed that all 115 tests in `pytest tests/` pass cleanly.
- [x] **No Fabricated References:** All citations in related work represent verified peer-reviewed literature with correct bibliographic records.
- [x] **Qualified Population Claims (§11.3):** Assertions on Hinglish usage in mobile communication are qualified with citations to empirical literature (Khanuja et al., 2020) without unsupported demographic totals.
- [x] **Proposed Infrastructure Framing (§14):** Confirmed §14 frames the contribution as "proposed methodological and computational infrastructure" reflecting unexecuted empirical components.
