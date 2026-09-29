# Pilot Study Protocol (N = 6–10)

**Protocol Version:** `1.1.0-gemini-frozen`  
**Study Identifier:** `ENGLISH_HINDI_AI_INFO_INEQUALITY_2026`  
**Target Pilot Sample Size:** $N = 6\text{--}10$ participants  
**Status:** READY FOR EXECUTION FOLLOWING FORMAL ETHICS APPROVAL  
**Date:** 2026-09-27  

> [!IMPORTANT]  
> **Prerequisite:** Human participant recruitment and pilot execution are strictly prohibited until formal Institutional Review Board (IRB) / Institutional Ethics Committee (IEC) approval is obtained (`IRB / Ethics Approval ID: PENDING`).

---

## 1. Pilot Purpose & Objectives

The $N = 6\text{--}10$ pilot study is a **feasibility, technical auditing, and measurement validation study**. It is **NOT** a confirmatory hypothesis-testing study.

### Primary Audit Objectives:
1. **Session Duration Baseline:** Establish the empirical distribution of total session completion times and individual task durations.
2. **Instruction & Interface Clarity:** Identify confusing onboarding instructions, ambiguous task descriptions, or usability friction in the React SPA interface.
3. **Telemetry & Event Logging Parity:** Verify 100% capture fidelity for user interaction events (`DocClicks`, `DocDuration`, `WindowBlur`, prompt reformulations) without data drops or missingness.
4. **LLM Provider Integration & Latency:** Evaluate Google Gemini API (`gemini-3.5-flash`) real-time responsiveness, token consumption, HTTP status distribution, and latency under actual session conditions.
5. **Language Leakage Audit:** Empirically measure language leakage rates across `ENGLISH_ONLY`, `HINDI_ONLY`, and `CODE_SWITCHING` arms.
6. **Deterministic Scoring Engine Audit:** Confirm that participant final submitted decisions evaluate cleanly against backend ground-truth rubrics (`backend/app/scoring/engine.py`) without rubric ambiguity, unhandled edge cases, or artificial ceiling/floor effects.
7. **Participant Burden & Workload:** Audit subjective cognitive workload (NASA-TLX) and participant-reported fatigue.

> [!CAUTION]  
> **Anti-Hacking Safeguard:** Pilot data MUST NOT be used to selectively alter study design, change hypotheses, or adjust primary outcome definitions to favor expected findings.

---

## 2. Pilot Sample & Allocation

- **Sample Size:** $N = 6\text{--}10$ bilingual English-Hindi Indian adults aged 18–65.
- **Arm Allocation:** Participants will be allocated across the 3 frozen experimental language arms:
  - `ENGLISH_ONLY`: 2 to 3 participants
  - `HINDI_ONLY`: 2 to 3 participants
  - `CODE_SWITCHING`: 2 to 3 participants
- **Allocation Procedure:** Allocations will be executed via the backend `RandomizationEngine` using server-side stratified block randomization based on baseline AILS total scores (median split threshold = 36).
- **Separation Guarantee:** Pilot participants are excluded from the main confirmatory trial dataset ($N = 144$). Pilot data will be analyzed strictly for feasibility and will **NOT** be pooled into the final inferential RCT analysis.

---

## 3. Pilot Task Scenarios & Counterbalancing

The pilot evaluates the exact three frozen civic entitlement scenarios specified in Protocol v1.1.0:

1. **PMEGP (Prime Minister Employment Generation Programme):** Micro-manufacturing enterprise entitlement evaluation.
2. **PM Vishwakarma:** Artisan credit & skill grant entitlement evaluation.
3. **PM SVANidhi:** Street vendor micro-credit entitlement evaluation.

### Counterbalancing:
Task presentation order is counterbalanced across positions 1, 2, and 3 using the frozen $3 \times 3$ Latin Square design (`ORDER_1`, `ORDER_2`, `ORDER_3`).

---

## 4. Collected Operational Variables

The pilot collects the complete variable dictionary specified in Protocol v1.1.0:

| Variable | Type | Measurement / Role | Database Table |
| :--- | :--- | :--- | :--- |
| `DecisionQuality` | Continuous (0.0–10.0) | Primary Outcome (Rubric Match) | `final_decisions` |
| `DocClicks` | Discrete Count | Secondary Outcome (Document Clicks) | `telemetry_events` |
| `DocDuration` | Continuous (seconds) | Secondary Outcome (Document Inspection Duration) | `telemetry_events` |
| `TaskCompletionTime` | Continuous (seconds) | Process Variable (Elapsed Task Time) | `task_sessions` |
| `NASA_TLX_Composite` | Continuous (1–20) | Exploratory Workload Score | `post_task_measures` |
| `DecisionConfidence` | Discrete Likert (1–7) | Exploratory Outcome | `final_decisions` |
| `PromptCount` | Discrete Count | Process Variable (Prompt Turns) | `messages` |
| `AutomationBiasIndicator` | Binary (0 / 1) | Exploratory Outcome | `final_decisions` + `telemetry` |
| `WindowBlur` | Count / Dwell (ms) | Exploratory Process Var (Off-screen Focus) | `telemetry_events` |
| `LanguageLeakageFlag` | Binary (0 / 1) | Technical Telemetry | `messages` |
| `APILatencyTokens` | Integer (ms / count) | Infrastructure Monitoring | `messages` |
| `TaskSessionStatus` | String Enum | Session Integrity (COMPLETED / TIMED_OUT) | `task_sessions` |

---

## 5. Pilot Feasibility Success Criteria

Prior to pilot execution, the following explicit feasibility benchmarks must be satisfied:

1. **Session Completion Rate:** $\ge 90\%$ of enrolled pilot participants complete all 3 task sessions without unrecoverable software crashes.
2. **Telemetry Capture Completeness:** $100\%$ of interaction events (`DocClicks`, `DocDuration`, `WindowBlur`) logged cleanly to `telemetry_events` with $0\%$ missing event schemas.
3. **API Integrity & Failure Rate:** Google Gemini API HTTP 5xx error or connection timeout rate $< 5\%$; zero unhandled 4xx endpoint errors.
4. **Scoring Engine Ambiguity:** $0\%$ unhandled response exceptions in `backend/app/scoring/engine.py`; all submitted decision structures yield a valid 0.0–10.0 score.
5. **Instruction Comprehension:** $100\%$ of pilot participants report understanding the task persona objective and interface controls during debriefing.
6. **Language Leakage Bound:** $0\%$ unauthorized language leakage in single-language arms (`ENGLISH_ONLY`, `HINDI_ONLY`) attributable to backend prompt errors.

*Non-Frozen Threshold Rule:*  
`PILOT DECISION RULE — REQUIRES RESEARCHER/ETHICS APPROVAL` (Any proposed operational change triggered by pilot findings must be formally logged in the Change-Control Decision Log).

---

## 6. Pre-Pilot Execution Checklist

Before launching the $N = 6\text{--}10$ pilot:
- [ ] Formal IRB / Ethics Approval Certificate obtained.
- [ ] Principal Investigator details populated in ethics package.
- [ ] Participant compensation rate and payment vendor finalized.
- [ ] Production PostgreSQL database provisioned with encrypted backups.
- [ ] Production `GEMINI_API_KEY` verified on a billing-enabled / paid Google Cloud project.
- [ ] Pilot participant debriefing checklist printed/formatted for administration.
