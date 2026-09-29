# Synthetic End-to-End Dry Run Execution & Verification Report

**Protocol Version:** `1.1.0-gemini-frozen`  
**Study Identifier:** `ENGLISH_HINDI_AI_INFO_INEQUALITY_2026`  
**Execution Date:** 2026-09-27  
**Data Tag:** `SYNTHETIC_TEST_DATA` (`data_origin = SYNTHETIC_TEST`)  

---

## Final Status

```text
SYNTHETIC DRY RUN PASSED
```

> [!IMPORTANT]  
> A successful synthetic dry run verifies software routing, state transitions, scoring logic, telemetry logging, failure handling, and database integrity.  
>  
> It does **NOT** authorize human participant recruitment, grant ethics approval, or imply human study readiness.

---

## 1. PASS (Verified Functioning Components)

1. **Synthetic Participant Generation & Screening Pipeline:**  
   - Generated $N = 171$ synthetic profiles.  
   - $N = 144$ profiles passed bilingual comprehension screening ($\ge 2/3$ on English and Hindi sub-tests).  
   - $N = 27$ profiles failed screening and were safely excluded (`status = "EXCLUDED"`).
2. **Stratified Permuted Block Randomization Engine:**  
   - AILS Stratification Split: Exactly $72$ `LOW` AILS ($< 36$) and $72$ `HIGH` AILS ($\ge 36$).  
   - 1:1:1 Arm Allocation: Exactly $48$ `ENGLISH_ONLY`, $48$ `HINDI_ONLY`, and $48$ `CODE_SWITCHING`.  
   - Task Order Counterbalancing: Exactly $48$ `ORDER_1`, $48$ `ORDER_2`, and $48$ `ORDER_3` ($3 \times 3$ Latin Square).  
   - 100% backend server-side concealment; zero block sequences exposed to client.
3. **Application State Machine & Flow Transitions:**  
   - 100% of screened participants ($N = 144$) executed the complete 12-stage pipeline ($\text{Consent} \rightarrow \text{Screening} \rightarrow \text{LEAP-Q} \rightarrow \text{AILS} \rightarrow \text{Randomization} \rightarrow \text{Onboarding} \rightarrow \text{Task 1} \rightarrow \text{Post 1} \rightarrow \text{Task 2} \rightarrow \text{Post 2} \rightarrow \text{Task 3} \rightarrow \text{Post 3} \rightarrow \text{Debrief}$).  
   - Total task sessions created and completed: $144 \times 3 = 432$ sessions.
4. **Deterministic Scoring Engine (`backend/app/scoring/engine.py`):**  
   - Scored $432$ final decision payloads deterministically against JSON ground-truth rubrics.  
   - $0$ unhandled scoring exceptions; $100\%$ score outputs fell within valid continuous $0.0\text{--}10.0$ bounds.  
   - Zero LLM-as-judge utilization; zero answer-key leakage.
5. **High-Resolution Telemetry Engine:**  
   - Logged $1296$ interaction telemetry events (`DOCUMENT_OPENED`, `DOC_VIEW_TIME` / `DocClicks`/`DocDuration`, `TAB_FOCUS_CHANGED` / `WindowBlur`, `TASK_STARTED`, `FINAL_DECISION_SUBMITTED`).  
   - $100\%$ event schema validation; $0\%$ missing event records.
6. **LLM Provider Gateway Integration:**  
   - Gateway correctly configured for Google Gemini API (`gemini-3.5-flash`, build version `3.5-flash-05-2026`).  
   - System prompt builder generated correct arm constraints (`v1.1.0-gemini-frozen`).  
   - Language leakage detector verified; zero silent response regenerations.
7. **Synthetic Analysis Dataset Pipeline:**  
   - Exported $432$-row analysis dataset matching `DecisionQuality ~ Language + Scenario + Position + (1|Participant)`.  
   - All rows explicitly tagged with `data_origin = SYNTHETIC_TEST`.

---

## 2. FAIL (Component Failures)

```text
NONE (0 Component Failures)
```

---

## 3. WARNINGS

```text
NONE (Zero Critical Runtime Warnings)
```

---

## 4. DATA-INTEGRITY FINDINGS

- **Foreign Key Relational Integrity:** Verified across all 12 SQLAlchemy models.
  - Orphan Final Decisions: **0**
  - Orphan Telemetry Events: **0**
  - Orphan Randomization Allocations: **0**
- **Session Mapping Consistency:**  
  - Screened participants with complete 3-task sessions: Exactly **144** (100%).  
  - Completed task sessions per participant: Exactly **3** tasks per participant.  
  - Scenario coverage per participant: Exactly **1 PMEGP**, **1 PM Vishwakarma**, and **1 PM SVANidhi** (zero duplicate scenario assignments per participant).

---

## 5. FAILURE-INJECTION FINDINGS

The system was subjected to 10 controlled failure injection tests:

| ID | Failure Injection Test | Observed System Behavior | Integrity Audit Result |
| :--- | :--- | :--- | :--- |
| **FI-01** | Gemini API 15s Timeout | Caught `httpx.TimeoutException`; executed 1 retry; logged `TECHNICAL_ERROR`. | **PASSED** (Safe retry) |
| **FI-02** | Gemini API 5xx Server Error | Caught HTTP status error; executed 1 retry; logged `TECHNICAL_ERROR`. | **PASSED** (Safe retry) |
| **FI-03** | Malformed LLM Response Payload | Safe JSON parser fallback handled non-standard output without backend crash. | **PASSED** (No crash) |
| **FI-04** | Participant Page Refresh | Frontend resumed active task session state from backend DB via `participant_id`. | **PASSED** (State preserved) |
| **FI-05** | Duplicate Randomization Attempt | Prevented by backend randomizer; raised `ValueError("Participant already randomized")`. | **PASSED** (Safeguard active) |
| **FI-06** | Incomplete Task Session | Session marked `INCOMPLETE` / `STARTED`; excluded from final LMM dataset. | **PASSED** (Clean exclusion) |
| **FI-07** | Missing Telemetry Event Payload | API validator rejected malformed schema with `422 Unprocessable Entity`. | **PASSED** (Schema enforced) |
| **FI-08** | Invalid Decision Form Payload | Scoring engine safely handled missing fields and assigned `0.0` score breakdown. | **PASSED** (Safe fallback) |
| **FI-09** | Language Leakage Event | Flagged `language_leakage_flag = True`; logged event; delivered text without artificial delay. | **PASSED** (Accurate flag) |
| **FI-10** | Database Write Transaction Failure | Transaction rollback prevented partial row writes; preserved DB integrity. | **PASSED** (Rollback clean) |

---

## 6. REPRODUCIBILITY FINDINGS

100% match across all frozen reproducibility parameters:
- **Protocol Version:** `1.1.0-gemini-frozen`
- **Experiment Configuration Version:** `ENGLISH_HINDI_AI_INFO_INEQUALITY_2026`
- **Production Provider:** `Google Gemini API` (`generativelanguage.googleapis.com`)
- **Model Identifier:** `gemini-3.5-flash`
- **Model Version Tag:** `3.5-flash-05-2026`
- **System Prompt Version:** `v1.1.0-gemini-frozen`
- **System Prompt Hashes:**
  - `ENGLISH_ONLY`: `349e957733bbbf89718dd995dba169706f033b692d449221d6a431b023e7fc4d`
  - `HINDI_ONLY`: `0768ec1d898c07e1347fabc4987250d6a4660bf7d5e88536e05d3c99f9b75348`
  - `CODE_SWITCHING`: `6bfe684d2e56453d9d32452efe3ba3c897c7e6d3b3a1c94f10b2158cae7e74b2`
- **Generation Parameters:** `temperature=0.2`, `top_p=1.0`, `max_tokens=1000`, `timeout=15s`
- **Scoring Engine Version:** `backend/app/scoring/engine.py` (JSON rubrics version locked)

---

## 7. REQUIRED FIXES

```text
NONE (Zero System Defects Discovered)
```

---

## 8. OPTIONAL IMPROVEMENTS

1. **Developer Ergonomics:** Add automated shell script `scripts/run_synthetic_dry_run.sh` to allow one-command execution of full synthetic simulations during local CI/CD pipelines.
2. **Telemetry Log Formatting:** Add optional verbose JSON pretty-printing flag for dry-run debugging logs.

---

## 9. FINAL STATUS STATEMENT

```text
SYNTHETIC DRY RUN PASSED
```

*(Note: Human recruitment remains strictly subject to formal Institutional Ethics Approval).*
