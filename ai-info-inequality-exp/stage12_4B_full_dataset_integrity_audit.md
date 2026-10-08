# STAGE 12.4B — FULL PRODUCTION DATASET INTEGRITY & CELL-LEVEL PROVENANCE AUDIT
## LINGUA-AUDIT: A Reproducible Framework for Auditing Information Inequality in Multilingual AI Systems

---

### 1. EXECUTIVE SUMMARY

This audit establishes the forensic integrity and cell-level provenance of the frozen 5,400-response production dataset (`stage12_4_full_evaluation_responses.json`) collected in Stage 12.4 Phase 2. 

In accordance with strict experimental protocols, **no substantive response scoring, accuracy analysis, quality evaluation, or disparity metrics were computed**. The content was inspected purely as opaque raw text to verify that the dataset faithfully and completely represents the pre-registered $150 \text{ tasks} \times 3 \text{ language conditions} \times 4 \text{ models} \times 3 \text{ repetitions}$ factorial matrix.

Every record was cryptographically, structurally, and dimensionally audited. The dataset exhibits **100% cell-level parity, zero missing cells, zero duplicate cells, zero dry-run contamination, 100% prompt hash integrity, and 100% response hash integrity**.

---

### 2. DATASET HASH VERIFICATION

| Hash Parameter | Expected / Target Hash | Computed / Actual Hash | Audit Status |
| :--- | :--- | :--- | :---: |
| **Production Dataset SHA256** | `296bb1650f06cc7934f16e90ef662f9c9b0207971344b0935ee02704b8bf4248` | `296bb1650f06cc7934f16e90ef662f9c9b0207971344b0935ee02704b8bf4248` | **VERIFIED** |
| **Execution Manifest SHA256** | `46375b1657b93712dfcb490b0812f76c6491f464aaa10ed0bbcba1452a48d5a5` | `46375b1657b93712dfcb490b0812f76c6491f464aaa10ed0bbcba1452a48d5a5` | **VERIFIED** |
| **Benchmark Version** | `v1.0-frozen` | `v1.0-frozen` | **VERIFIED** |
| **Master Task Registry SHA256**| `2ce2cb688c011cb0279425a3c063ce4e5b7b6a2354a4aa9df75a77efa9d00315` | `2ce2cb688c011cb0279425a3c063ce4e5b7b6a2354a4aa9df75a77efa9d00315` | **VERIFIED** |

---

### 3. EXACT FACTORIAL CELL AUDIT

The pre-registered factorial design requires every unique tuple $(task\_id, language, model, repetition)$ to exist exactly once:

$$\text{Factorial Matrix} = 150 \text{ Tasks} \times 3 \text{ Languages} \times 4 \text{ Models} \times 3 \text{ Repetitions} = 5,400 \text{ Unique Cells}$$

- **Total Production Records in Dataset:** `5,400`
- **Observed Unique Factorial Cells:** `5,400`
- **Expected Unique Factorial Cells:** `5,400`
- **Coverage Ratio:** `100.0% (5,400 / 5,400)`

---

### 4. MISSING-CELL AUDIT

The Cartesian product of the frozen benchmark task registry, language conditions, model registry, and repetition indices was constructed independently.

- **Missing Cells Identified:** `0`
- **Missing Task-Language Combinations:** `0`
- **Missing Model-Repetition Cells:** `0`

No marginal total masks any missing internal cell. Every single cell in the $150 \times 3 \times 4 \times 3$ grid is present and resolved.

---

### 5. DUPLICATE-CELL AUDIT

All 5,400 records were grouped by the composite primary key `(task_id, language, model, repetition)`.

- **Duplicate Factorial Keys Found:** `0`
- **Duplicate Records:** `0`
- **Re-run Overwrites:** `0`

---

### 6. PROMPT HASH AUDIT

For all 5,400 production records, the stored prompt text was re-hashed using SHA256 and matched against both the record's `prompt_hash` field and the canonical prompt hash in `master_task_registry_150.json`.

- **Total Prompts Checked:** `5,400`
- **Prompt SHA256 Matches:** `5,400`
- **Prompt Hash Failures / Discrepancies:** `0`

---

### 7. RESPONSE HASH AUDIT

For all 5,400 production records, the raw model response text (`raw_response`) was re-hashed using SHA256 and verified against the stored `response_hash`.

- **Total Responses Checked:** `5,400`
- **Response SHA256 Matches:** `5,400`
- **Response Hash Failures / Corruptions:** `0`

---

### 8. TASK ID & SCENARIO-FAMILY INTEGRITY AUDIT

- **Unknown Task IDs:** `0`
- **Malformed Task IDs:** `0`
- **Canonical Scenario Family Mapping:** $100\%$ verified (`task_id` $\rightarrow$ `scenario_family_id` $\rightarrow$ `variant_id`).
  - Example: `HLT-001` maps strictly to `HLT-FAM-01` and `VAR-01`.
  - All 150 tasks maintain perfect structural alignment with `master_task_registry_150.json`.

---

### 9. LANGUAGE INTEGRITY AUDIT

| Language Condition | Frozen Registry Code | Stored Records | Canonical Prompt Parity | Hash Integrity |
| :--- | :--- | :---: | :---: | :---: |
| **English** | `ENGLISH` | 1,800 | 100.0% | 100.0% |
| **Hindi** | `HINDI` | 1,800 | 100.0% | 100.0% |
| **Code-Switching** | `CODE_SWITCHING` | 1,800 | 100.0% | 100.0% |
| **Total** | — | **5,400** | **100.0%** | **100.0%** |

---

### 10. MODEL INTEGRITY AUDIT

Every record was verified at the individual record level against the frozen execution manifest model registry:

| Model Label | Provider | Exact Model Identifier | Provider Snapshot | Observed Records |
| :--- | :--- | :--- | :--- | :---: |
| **gemini-3.5-flash** | Google | `gemini-3.5-flash-202610` | `3.5-flash-05-2026` | 1,350 |
| **gpt-4o** | OpenAI | `gpt-4o-2024-08-06` | `gpt-4o-2024-08-06` | 1,350 |
| **claude-3.5-sonnet** | Anthropic | `claude-3-5-sonnet-20241022` | `claude-3-5-sonnet-20241022` | 1,350 |
| **llama-3.1-70b** | Meta | `llama-3.1-70b-instruct-v1` | `llama-3.1-70b-instruct` | 1,350 |
| **Total** | — | — | — | **5,400** |

---

### 11. REPETITION INTEGRITY AUDIT

- **Repetition 1 (R1):** `1,800 records` ($150 \text{ tasks} \times 3 \text{ languages} \times 4 \text{ models}$)
- **Repetition 2 (R2):** `1,800 records` ($150 \text{ tasks} \times 3 \text{ languages} \times 4 \text{ models}$)
- **Repetition 3 (R3):** `1,800 records` ($150 \text{ tasks} \times 3 \text{ languages} \times 4 \text{ models}$)
- **Invalid Repetitions (R0, R4+):** `0`

---

### 12. DOMAIN INTEGRITY AUDIT

Domain assignments were verified independently against `master_task_registry_150.json`:

| Domain Code | Domain Name | Expected Tasks | Expected Records | Observed Records | Domain Parity |
| :--- | :--- | :---: | :---: | :---: | :---: |
| `HLT` | **Healthcare** | 30 | 1,080 | 1,080 | 100.0% |
| `EDU` | **Education** | 30 | 1,080 | 1,080 | 100.0% |
| `PUB` | **Public Services** | 30 | 1,080 | 1,080 | 100.0% |
| `FIN` | **Finance** | 30 | 1,080 | 1,080 | 100.0% |
| `GEN` | **General Knowledge** | 30 | 1,080 | 1,080 | 100.0% |
| **Total** | — | **150** | **5,400** | **5,400** | **100.0%** |

---

### 13. DRY-RUN ISOLATION & MANIFEST BINDING AUDIT

- **`is_dry_run == false` Records:** `5,400 / 5,400 (100.0%)`
- **Dry-run Records in Production File:** `0`
- **Execution ID:** `exec_lingua_audit_20261008_4a507177` (100% uniform across all 5,400 records)
- **Execution Manifest Hash Binding:** `46375b1657b93712dfcb490b0812f76c6491f464aaa10ed0bbcba1452a48d5a5` (`5,400 / 5,400`)
- **Request ID Uniqueness:** `5,400 / 5,400` unique UUIDs
- **Response ID Uniqueness:** `5,400 / 5,400` unique UUIDs

---

### 14. GENERATION PARAMETERS & SYSTEM PROMPT AUDIT

All 5,400 records were verified for parameter adherence:
- **Temperature:** `0.2` (Verified 100%)
- **Top-P:** `1.0` (Verified 100%)
- **Max Tokens:** `1000` (Verified 100%)
- **System Prompt Hash:** `102cd78d14c3e8a2e29d1c6ca620671f89f29bacd8795548a863f6f0599e8b94` (Verified 100%)

---

### 15. CROSS-DIMENSIONAL COMPLETENESS MATRIX

| Cross-Dimension | Factorial Combination | Expected Count per Cell | Observed Parity |
| :--- | :--- | :---: | :---: |
| **Task $\times$ Language** | 150 tasks $\times$ 3 languages = 450 pairs | 12 | 100.0% (12 per pair) |
| **Task $\times$ Model** | 150 tasks $\times$ 4 models = 600 pairs | 9 | 100.0% (9 per pair) |
| **Task $\times$ Repetition** | 150 tasks $\times$ 3 reps = 450 pairs | 12 | 100.0% (12 per pair) |
| **Language $\times$ Model** | 3 languages $\times$ 4 models = 12 pairs | 450 | 100.0% (450 per pair) |
| **Language $\times$ Repetition**| 3 languages $\times$ 3 reps = 9 pairs | 600 | 100.0% (600 per pair) |
| **Model $\times$ Repetition** | 4 models $\times$ 3 reps = 12 pairs | 450 | 100.0% (450 per pair) |

---

### 16. DATASET INTEGRITY MANIFEST REFERENCE

The JSON dataset integrity manifest has been compiled and saved to:
`data/benchmark/raw_responses/stage12_4_dataset_integrity_manifest.json`

Key metadata embedded:
- Dataset Hash: `296bb1650f06cc7934f16e90ef662f9c9b0207971344b0935ee02704b8bf4248`
- Execution Manifest Hash: `46375b1657b93712dfcb490b0812f76c6491f464aaa10ed0bbcba1452a48d5a5`
- Total Records: `5400`
- Unique Factorial Cells: `5400`
- Missing Cells: `0`
- Duplicate Cells: `0`

---

### 17. LIMITATIONS & PROVENANCE BOUNDARIES

1. **Evaluation Deferral:** No accuracy, completeness, or linguistic disparity scoring has been executed. The dataset remains strictly un-analyzed pending authorization of Stage 12.5.
2. **Provider Snapshots:** Provider versioning follows the exact audited snapshots authorized in Stage 12.4A.

---

### 18. FINAL GATE DECISION

Based on 100% cell-level enumeration, cryptographic hash matching, and complete provenance binding across all 5,400 observations:

DATASET VERIFIED AND CLEARED FOR STAGE 12.5
