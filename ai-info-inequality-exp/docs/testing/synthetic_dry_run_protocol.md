# Synthetic End-to-End Dry Run Protocol

**Protocol Version:** `1.1.0-gemini-frozen`  
**Study Identifier:** `ENGLISH_HINDI_AI_INFO_INEQUALITY_2026`  
**Data Tag:** `SYNTHETIC_TEST_DATA` (`data_origin = SYNTHETIC_TEST`)  
**Status:** EXECUTED & VERIFIED  
**Date:** 2026-09-27  

> [!IMPORTANT]  
> **CONTEXT & ISOLATION MANDATE:**  
> The human-participant phase has NOT started. No real participants, no recruitment, and no production database deployment exist.  
>  
> All data generated under this protocol are **SYNTHETIC / HYPOTHETICAL TEST FIXTURES ONLY** created to evaluate software routing, state transitions, scoring, telemetry, failure injection, and database integrity.  
>  
> Synthetic records are explicitly tagged with `data_origin = SYNTHETIC_TEST` and MUST NEVER enter or be combined with the confirmatory $N = 144$ trial dataset.

---

## 1. Synthetic Participant Population & Profiles

A synthetic test sample of $N = 171$ profiles was generated to evaluate the complete enrollment and screening pipeline:

1. **Screened Analyzable Candidates ($N = 144$):**
   - **English-Dominant Bilinguals:** High English proficiency, lower Hindi AoA.
   - **Hindi-Dominant Bilinguals:** High Hindi proficiency, English as L2.
   - **Balanced Bilinguals:** Equivalent self-rated reading/speaking proficiencies.
   - **Low AI Literacy Stratum (`LOW`, $N = 72$):** AILS total score $< 36$.
   - **High AI Literacy Stratum (`HIGH`, $N = 72$):** AILS total score $\ge 36$.
2. **Screening Exclusions ($N = 27$):**
   - Failures on English sub-test ($< 2/3$).
   - Failures on Hindi sub-test ($< 2/3$).
   - Failures on both sub-tests.
3. **Incomplete Sessions:** Synthetic test cases simulating session disconnects and mid-task dropouts.

---

## 2. Full Application Flow Verification

Every synthetic candidate executes the 12-stage participant journey:

$$\text{Consent (S1)} \rightarrow \text{Screening (S2)} \rightarrow \text{LEAP-Q (S3)} \rightarrow \text{AILS (S4)} \rightarrow \text{Randomization (S5)} \rightarrow \text{Onboarding (S6)}$$
$$\rightarrow \text{Task 1 (S7)} \rightarrow \text{Post 1 (S8)} \rightarrow \text{Task 2 (S7)} \rightarrow \text{Post 2 (S8)} \rightarrow \text{Task 3 (S7)} \rightarrow \text{Post 3 (S8)} \rightarrow \text{Debrief (S10)}$$

### State Machine Audit:
- **`CONSENTED` $\rightarrow$ `SCREENED` / `EXCLUDED`:** Correctly branches based on $2/3$ sub-test threshold.
- **`SCREENED` $\rightarrow$ `BASELINE_DONE`:** Enforces completion of LEAP-Q and AILS prior to block allocation.
- **`BASELINE_DONE` $\rightarrow$ `RANDOMIZED`:** Enforces server-side block allocation and stratum assignment.
- **`RANDOMIZED` $\rightarrow$ `IN_PROGRESS` $\rightarrow$ `COMPLETED`:** Tracks task session progress across 3 repeated tasks.

---

## 3. Server-Side Randomization & Stratification Audit Protocol

The synthetic dry run evaluates backend `RandomizationEngine` allocation across $N = 171$ participants ($N = 144$ screened candidates):

1. **1:1:1 Arm Allocation Target:** 48 `ENGLISH_ONLY`, 48 `HINDI_ONLY`, 48 `CODE_SWITCHING`.
2. **AILS Stratification Balance:** 72 `LOW` AILS ($< 36$), 72 `HIGH` AILS ($\ge 36$).
3. **Permuted Block Sizes:** Randomly permuted blocks of 3 and 6 per stratum.
4. **Counterbalancing:** $3 \times 3$ Latin Square task orders (`ORDER_1`, `ORDER_2`, `ORDER_3`), 48 participants per order sequence.
5. **Session Integrity:** Every screened participant receives exactly 3 tasks, receiving each scenario (PMEGP, PM Vishwakarma, PM SVANidhi) exactly once without duplication.

---

## 4. LLM Gateway & Language Condition Protocol

### Gateway Parameters Frozen:
```text
Provider: Google Gemini API
Model Identifier: gemini-3.5-flash
Model Version Tag: 3.5-flash-05-2026
Base URL: https://generativelanguage.googleapis.com/v1beta/openai
Temperature: 0.2
Top-p: 1.0
Max Output Tokens: 1000
Timeout: 15 seconds (15000 ms)
Max Retries: 1 (HTTP 5xx / timeout only)
```

### Language Condition Checks:
- **`ENGLISH_ONLY`:** System prompt constraint enforces exclusive English output (`SHA256: 349e9577...`).
- **`HINDI_ONLY`:** System prompt constraint enforces exclusive Devanagari Hindi output (`SHA256: 0768ec1d...`).
- **`CODE_SWITCHING`:** System prompt constraint permits fluid Hinglish/English/Hindi mixing (`SHA256: 6bfe684d...`).
- **Leakage Detection:** Server-side regex pattern matcher flags off-target language tokens without silent response regeneration.

---

## 5. Scoring Engine Audit Protocol

Evaluates `backend/app/scoring/engine.py` against JSON ground-truth rubrics in `data/ground_truth/`:
- **Scoring Range:** Continuous 0.0 to 10.0 per task.
- **Scoring Dimensions:** Eligibility check (2 pts), monetary threshold rules (2 pts), subsidy/stipend rates (3 pts), document/grant vouchers (3 pts).
- **Zero LLM-As-Judge:** Evaluated 100% deterministically by exact structural field matching.
- **Format Integrity:** Test malformed, missing, and extra field answer payloads.

---

## 6. Telemetry & Database Relational Integrity Audit

### Telemetry Tracked:
- Participant UUID (`p_syn_...`), Task ID, Scenario, Arm, Prompts, AI Responses, Timestamps, Latency (ms), Tokens used, Document Clicks (`DocClicks`), Document View Duration (`DocDuration`), Prompt Count, Task Completion Time, Confidence (1–7), NASA-TLX Composite, Language Leakage Flag, Window Blur Events (`WindowBlur`), Final Decision Payload.

### Database Integrity Checks:
- Foreign Key Constraints across all 12 SQLAlchemy models.
- Zero orphan records in `final_decisions`, `telemetry_events`, or `randomization_allocations`.
- Explicit relational mapping: 1 Participant $\rightarrow$ 3 Task Sessions $\rightarrow$ 1 Final Decision per task session.

---

## 7. Failure-Injection Audit Matrix

The dry run subjects the architecture to 10 controlled failure injection scenarios:

1. **Gemini Timeout (15s Exceeded):** Triggers `httpx.TimeoutException`; caught safely; retried once; logs `TECHNICAL_ERROR`.
2. **Gemini HTTP 5xx Server Error:** Caught safely; retried once; logs `TECHNICAL_ERROR`.
3. **Malformed LLM Completion:** Safe JSON parser fallback handles non-standard completions without backend crash.
4. **Participant Page Refresh:** Frontend reads `participant_id` from local storage and resumes active task session state from backend DB.
5. **Duplicate Final Decision Submission:** Backend returns `400 Bad Request` or handles SQL unique constraint on `task_session_id`.
6. **Incomplete Task Session:** Session marked `STARTED` or `INCOMPLETE`; excluded from final LMM analysis dataset.
7. **Missing Telemetry Event:** Telemetry validator rejects malformed event payloads with `422 Unprocessable Entity`.
8. **Invalid Decision Payload Format:** Scoring engine safely handles missing fields and assigns `0.0` score breakdown without throwing unhandled exceptions.
9. **Language Leakage Event:** Detects leakage, sets `language_leakage_flag = True`, logs event, and delivers text without artificial latency spikes.
10. **Database Write Transaction Failure:** Session rollback prevents partial row writes and preserves relational integrity.

---

## 8. Synthetic Analysis Dataset Structure

Generates a synthetic analysis dataset matching the confirmatory LMM input format:
$$\text{DecisionQuality} \sim \text{Language} + \text{Scenario} + \text{Position} + (1|\text{Participant})$$

- **Dimensions:** 144 Participants $\times$ 3 Tasks $= 432$ rows.
- **Variables:** `participant_id`, `assigned_arm`, `scenario_id`, `position`, `decision_quality_score`, `doc_clicks`, `doc_duration`, `task_completion_time`, `nasa_tlx_composite`, `confidence_score`, `data_origin = "SYNTHETIC_TEST"`.

> [!CAUTION]  
> **NO INFERENTIAL TESTING:** Synthetic datasets are used exclusively to confirm model parameter formatting and data pipeline compatibility. They MUST NOT be analyzed for $p$-values or cited as empirical evidence for H1, H2, or H3.
