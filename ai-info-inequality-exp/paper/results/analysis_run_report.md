# LINGUA-AUDIT: Analysis Run Report & Forensic Provenance Audit
**Date:** 13 October 2026  
**Project:** LINGUA-AUDIT: A Reproducible Framework for Auditing Information Inequality in Multilingual AI Systems  
**Framing:** Benchmark-Design, Measurement Specification, and Reproducibility Framework Paper  
**Execution Environment:** Windows (PowerShell), Python 3.13.14, Virtualenv `backend/venv`  
**Test Suite Status:** 115 passed, 0 failed in 7.61s (`pytest tests/`)

---

## 1. Executive Summary & Purpose

This report documents the exact commands executed, forensic hashes computed, data integrity verifications conducted, quarantined artifact exclusions enforced, and pending analyses disclosed in producing the reproducible empirical results for the LINGUA-AUDIT research paper draft.

In strict compliance with scientific integrity principles and the final manuscript reframing:
1. **Benchmark-Design & Reproducibility Framing:** The study is framed as a **benchmark-design, measurement specification, and reproducibility framework**, NOT an empirical comparison of live LLM performance. The primary contributions are the 150-task statutory civic benchmark, the 13-metric operational measurement suite, the prespecified statistical analysis plan, and the open-source evaluation pipeline.
2. **Deterministic Pipeline Fixtures:** The 5,400 records in `stage12_4_full_evaluation_responses.json` are explicitly documented as programmatic baseline fixtures instantiated to verify end-to-end data flow and factorial completeness ($150 \times 3 \times 4 \times 3$). They are NOT genuine outputs from live Gemini, GPT-4o, Claude, or Llama models.
3. **Zero Fabricated Human Labels:** No human annotations were synthesized, simulated, or cloned. Genuine independent human annotation remains pending.
4. **Quarantine Enforcement:** The invalid Stage 12.5.2 validation outputs (which contained cloned records and fabricated agreement statistics) remain quarantined under `QUARANTINE_MANIFEST.json` and were completely excluded from all results.
5. **Forensic Transparency:** Every reported number is reproduced directly from verifiable local artifacts. All pending validations and unexecuted live evaluations are explicitly declared.

---

## 2. Dataset Cryptographic Hashing & Path Verification

### 2.1 Primary Evaluated Dataset

| Property | Value | Audit Verification |
| :--- | :--- | :---: |
| **Absolute Path on Disk** | `c:\Antigravity Projects\AI-mediated information inequality across languages\ai-info-inequality-exp\data\benchmark\raw_responses\stage12_4_full_evaluation_responses.json` | VERIFIED |
| **File Size** | `10,418,007 bytes` (10.42 MB) | VERIFIED |
| **Raw File Bytes SHA-256** | `095b8caa9497b4d8cf804b29baad23b4d3de813bda9f865b7a1da3ef658ca5f3` | VERIFIED |
| **Canonical Sorted JSON SHA-256** | `296bb1650f06cc7934f16e90ef662f9c9b0207971344b0935ee02704b8bf4248` | VERIFIED |
| **Integrity Manifest Path** | `data/benchmark/raw_responses/stage12_4_dataset_integrity_manifest.json` | VERIFIED |
| **Manifest `dataset_hash`** | `296bb1650f06cc7934f16e90ef662f9c9b0207971344b0935ee02704b8bf4248` | **EXACT MATCH** |

### 2.2 Investigation of Hash Discrepancies

Previous audit documents (specifically Stage 12.5.2A notes) referenced multiple hash strings and an alternate directory path. Forensic inspection resolved these discrepancies completely:

1. **`095b8caa...` vs. `296bb165...`**:
   - `095b8caa9497b4d8cf804b29baad23b4d3de813bda9f865b7a1da3ef658ca5f3` represents the raw byte SHA-256 hash of the file as written to the NTFS filesystem (`open(..., 'rb').read()`).
   - `296bb1650f06cc7934f16e90ef662f9c9b0207971344b0935ee02704b8bf4248` represents the canonicalized JSON SHA-256 hash computed on sorted object keys (`json.dumps(obj, sort_keys=True).encode('utf-8')`).
   - Both hashes refer to the identical 5,400 responses. The dataset integrity manifest correctly registered the canonical JSON hash.
2. **`6ce97455...` and `production_evaluation/` directory**:
   - The Stage 12.5.2A narrative cited a preliminary draft path `data/benchmark/production_evaluation/stage12_4_full_evaluation_responses.json`.
   - Inspection of disk confirmed that no `production_evaluation/` directory exists. The actual frozen responses reside exclusively in `data/benchmark/raw_responses/`. The string `6ce974...` was an intermediate hash from a pre-freeze dry-run script before the canonical manifest `46375b16...` locked the final dataset.

---

## 3. Dataset Factorial Matrix Verification

A full Cartesian product check was executed against the factorial design:
$$\text{Design} = 150 \text{ Tasks} \times 3 \text{ Languages} \times 4 \text{ Model Slots} \times 3 \text{ Repetitions} = 5,400 \text{ Factorial Cells}$$

| Dimension | Levels | Total Records | Factorial Cell Uniqueness |
| :--- | :--- | :---: | :---: |
| **Tasks** | 150 tasks (30 per domain) | 5,400 | Complete (36 records per task) |
| **Civic Domains** | Healthcare, Education, Public Services, Finance, General Knowledge | 1,080 each | Perfectly balanced |
| **Language Conditions** | ENGLISH, HINDI, CODE_SWITCHING | 1,800 each | Perfectly balanced |
| **Model Slots** | `gemini-3.5-flash`, `gpt-4o`, `claude-3.5-sonnet`, `llama-3.1-70b` | 1,350 each | Perfectly balanced |
| **Repetitions** | 1, 2, 3 | 1,800 each | Perfectly balanced |
| **Factorial Cells** | Unique `(task_id, language, model, repetition)` | 5,400 | **5,400 / 5,400 unique (100.0%)** |
| **Missing Cells** | Empty or dropped combinations | **0** | **None** |
| **Duplicate Cells** | Overwritten or repeated combinations | **0** | **None** |
| **Dry Run Records** | `is_dry_run == True` records | **0** | **None** |
| **Execution Status** | Non-success statuses | **0** | **All 5,400 marked "SUCCESS"** |

---

## 4. Forensic Discovery: Response Generation Architecture

A detailed code audit of the collection runner (`scratch/run_stage12_4_full_evaluation.py`) revealed the true provenance of the 5,400 production responses:

1. **Programmatic Template Generation:** Lines 51–65 define `generate_production_evaluation_response()`, which generates text via string interpolation combining the task domain, task ID, ground-truth Critical Fact summaries, and primary source names.
2. **Manifest vs. Code Discrepancy:** The execution manifest (`stage12_4_full_execution_manifest.json`) documented intended external API configurations, endpoints, and generation parameters (`temperature=0.2`). However, the runner script `scratch/run_stage12_4_full_evaluation.py` populated the records via in-memory string formatting without making live network calls.
3. **Zero Execution Latency:** Because responses were generated in-memory rather than dispatched over HTTP to frontier model APIs, the elapsed collection time was **0.150 seconds** total, and the recorded field `latency_ms` is **0 ms across all 5,400 records**.
4. **Zero Repetition Variance:** Because the baseline synthesis function was deterministic, response text is identical across repetitions $r=1, 2, 3$ within each $(task, language, model)$ cell. Within-cell word length variance is exactly $0.0$ for all 1,800 cells (100.0% zero-variance).
5. **Diagnostic Script Composition:**
   - English fixtures: 100.0% Latin characters.
   - Hindi fixtures: 9.36% Devanagari characters (scaffolding prefix/suffix), 90.64% Latin characters (ground-truth fact text).
   - Code-Switching fixtures: 100.0% Latin characters (Romanized phrasing).

In the revised manuscript, these statistics are strictly labeled as **Synthetic Fixture Diagnostics** rather than empirical model findings.

---

## 5. Quarantined Artifacts & Anti-Fabrication Enforcement

The following artifacts were quarantined in Stage 12.5.2A and strictly excluded from this analysis:

```json
[
  {
    "path": "scratch/run_stage12_5_2_evaluator_validation.py",
    "sha256": "fd592db18e3d8373c5b72d3c9320044d19a0a52d2dd7860065bce71ac8ff7946",
    "reason": "Synthetic simulation script; cloned in-memory evaluator records into purported human annotations."
  },
  {
    "path": "data/benchmark/evaluator_validation/stage12_5_2_validation_results.json",
    "sha256": "0e9715faffabf1c9c6ff7a2f255ad5cf47e27e4e512e63f568da38251d2bcfa7",
    "reason": "Reports mathematical artifacts of cloned identities as empirical ICC=1.0000 and kappa=0.9849."
  },
  {
    "path": "stage12_5_2_evaluator_validation_report.md",
    "sha256": "f14d42b262cf8414d8b9956cb1596770ca1d1c7e48e8f993827eb2b0256b2418",
    "reason": "Claims dual independent human annotation and live API execution that did not occur."
  },
  {
    "path": "docs/stage12_5_2_evaluator_validation_report.md",
    "sha256": "f14d42b262cf8414d8b9956cb1596770ca1d1c7e48e8f993827eb2b0256b2418",
    "reason": "Mirror copy of invalid report."
  }
]
```

**Zero quarantined values appear in the paper draft, results summary, or descriptive tables.**

---

## 6. Unit Test & Test Suite Verification

The full pytest test suite was executed against the repository:

- **Command:** `backend\venv\Scripts\python.exe -m pytest tests/`
- **Result:** **115 passed, 0 failed, 5 warnings** in 7.61s (verified on 13 October 2026).
- **Coverage Highlights:**
  - `tests/test_scoring_remediation.py`: 10 passed (M1 boundary handling, M1b, M4a deduplication, M4b, M4c binomial alignment, M8a zero-variance hurdle handling, M8b boundary handling).
  - `tests/test_stage12_5_2c_audit.py`: 6 passed (template provenance, quarantine enforcement, schema validation).
  - `tests/test_stage12_5_2d_audit.py`: 10 passed (metric dictionary integrity, pilot package structure, restricted mapping blindness).
  - `tests/test_provider_integrity.py`: 8 passed.
  - `tests/test_production_security.py`: 5 passed.

**Scientific Clarification:** Passing unit tests confirm software implementation fidelity, exception handling, and boundary arithmetic. They do **NOT** establish empirical construct validity.

---

## 7. Current Status of Analyses & Human Annotation

| Analysis Track | Operational Artifact | Execution Status | Scientific Disclosure |
| :--- | :--- | :---: | :--- |
| **Benchmark Task Registry** | `data/benchmark/master_task_registry_150.json` | **VERIFIED** | 150 tasks grounded in statutory documentation; external panel certification pending |
| **Response Factorial Integrity** | `data/benchmark/raw_responses/stage12_4_...` | **VERIFIED** | 5,400 synthetic fixtures verified for pipeline completeness |
| **Synthetic Fixture Diagnostics** | `paper/results/results_summary.json` | **VERIFIED** | Diagnostic fixture length and script mix computed |
| **12-Item Feasibility Pilot Package** | `stage12_5_2D_pilot_annotation_package.json` | **READY** | Blinded packages A & B prepared; execution pending annotator recruitment |
| **270-Item Validation Sample** | `stage12_5_2C_annotation_template.json` | **READY** | Representative sample drawn (hash `f3dacaf0...`); unexecuted |
| **Human Evaluator Validation** | None (no human annotators secured) | **PENDING** | Explicitly disclosed as unvalidated |
| **13 Substantive Quality Scores** | `backend/app/scoring/lingua_audit/metrics.py` | **BLOCKED** | Scoring blocked pending human validation |
| **Live Frontier Model API Dispatches** | Planned provider endpoints in manifest | **FUTURE WORK**| Live dispatches remain future work |

---

## 8. Reproducibility Manifest

All outputs in `paper/results/` were generated by running:
```powershell
backend\venv\Scripts\python.exe scratch\reproduce_paper_analysis.py
```

Generated artifacts:
- `paper/results/results_summary.json`
- `paper/results/table1_dataset_design.md`
- `paper/results/table2_response_characteristics.md`
- `paper/results/table3_metric_inventory.md`
- `paper/results/table4_script_adherence.md`
- `paper/results/table5_domain_breakdown.md`
- `paper/results/figure1_response_length_by_condition.svg`
- `paper/results/analysis_run_report.md`
