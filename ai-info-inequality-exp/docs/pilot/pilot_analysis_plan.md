# Pilot Data Analysis & Feasibility Audit Plan (N = 6–10)

**Protocol Version:** `1.1.0-gemini-frozen`  
**Study Identifier:** `ENGLISH_HINDI_AI_INFO_INEQUALITY_2026`  
**Focus:** Technical Feasibility, Data Parity, Instrument Validation  
**Date:** 2026-09-27  

---

## 1. Methodological Scope & Strict Analytical Boundaries

> [!CAUTION]  
> **NO CONFIRMATORY HYPOTHESIS TESTING:**  
> The $N = 6\text{--}10$ pilot study is strictly descriptive and diagnostic. **NO inferential hypothesis testing** ($p$-values, $t$-tests, ANOVA, or Linear Mixed-Effects Model parameter estimation) will be conducted on pilot data to test Hypotheses H1, H2, or H3.  
>  
> **DATA SEPARATION MANDATE:**  
> Pilot data will **NOT** be pooled, merged, or combined into the final $N = 144$ confirmatory RCT dataset. Pilot data serves exclusively to audit system mechanics prior to launching full trial recruitment.

---

## 2. Quantitative Feasibility & Diagnostic Audits

The pilot analysis evaluates 7 technical audit modules:

### 2.1 Session Integrity & Completion Rate Audit
- **Metrics:** Total enrolled pilot participants, completed 3-task sessions, dropouts, screening failure count.
- **Target:** $\ge 90\%$ completed sessions among randomized participants.

### 2.2 Telemetry Event Capture Audit
- **Metrics:** Total `telemetry_events` rows generated, missingness count, schema validation errors.
- **Specific Checks:** Verify that every `DOCUMENT_OPENED`, `DOC_VIEW_TIME` (`DocClicks` / `DocDuration`), and `TAB_FOCUS_CHANGED` (`WindowBlur`) event contains valid participant IDs, timestamps, and JSON event payloads.
- **Target:** $0\%$ schema validation errors; $100\%$ capture parity.

### 2.3 LLM Provider & Infrastructure Performance Audit
- **Metrics:** API request latency ($\text{mean}, \text{median}, \text{p95}$ in ms), prompt token count, completion token count, HTTP status code distribution (200 OK vs 5xx errors).
- **Target:** Median latency $< 3000\text{ ms}$; HTTP 5xx error rate $< 5\%$.

### 2.4 Language Leakage Rate Audit
- **Metrics:** Total AI response turns, count of responses with `language_leakage_flag = True`, leakage rate by experimental arm (`ENGLISH_ONLY` vs `HINDI_ONLY` vs `CODE_SWITCHING`).
- **Target:** $0\%$ leakage in single-language arms caused by system prompt formatting errors.

### 2.5 Deterministic Scoring Engine & Distribution Audit
- **Metrics:** Calculated Decision Quality Scores (range $0.0\text{--}10.0$), sub-score breakdown match rate, execution exceptions in `backend/app/scoring/engine.py`.
- **Ceiling / Floor Check:** Inspect score distributions to ensure tasks do not display extreme ceiling effects (all scores $= 10.0$) or floor effects (all scores $= 0.0$).
- **Target:** $0$ engine exceptions; clean score differentiation across task responses.

### 2.6 Session Duration & Task Timing Audit
- **Metrics:** Task completion time per scenario (PMEGP, PM Vishwakarma, PM SVANidhi), total session completion duration (minutes from Consent S1 to Debrief S10).
- **Purpose:** Establish empirical session duration baseline for participant information sheets and panel compensation calculations.

### 2.7 Subjective Workload & Confidence Score Audit
- **Metrics:** Raw 6-item NASA-TLX workload distributions, composite workload score, self-reported decision confidence (1–7 Likert).
- **Target:** Verify scale completion clarity and response variability without missing items.

---

## 3. Qualitative Issue Logging Framework

During pilot debriefing, the researcher will record qualitative friction points using a structured diagnostic log:

| Category | Diagnostic Question | Observed Friction / Feedback | Remediation Action |
| :--- | :--- | :--- | :--- |
| **Instruction Clarity** | Were task scenario goals clear to the participant? | `[LOG OBSERVED ISSUE]` | Clarify onboarding text |
| **AI Assistant Usability** | Did the user understand how to prompt the assistant? | `[LOG OBSERVED ISSUE]` | UI prompt hint adjustments |
| **Verification Interface** | Was document viewing intuitive? | `[LOG OBSERVED ISSUE]` | Highlight document tab buttons |
| **Language Naturalness** | Did Hindi/Code-Switching outputs read naturally? | `[LOG OBSERVED ISSUE]` | System prompt constraint review |
| **Participant Burden** | Did the participant report excessive fatigue? | `[LOG OBSERVED ISSUE]` | Enforce break screen timer |

---

## 4. Post-Pilot Change-Control Decision Log

If pilot data reveals technical failures, instruction ambiguities, or scoring errors, proposed modifications MUST be formally evaluated and logged using the decision table below prior to main RCT launch:

| Issue ID | Observed Problem | Empirical Evidence | Proposed Change | Protocol v1.1.0 Impact | Ethics Amendment Required? | Primary Hypotheses / Outcomes Affected? | Final Decision |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **PILOT-01** | `[Describe problem]` | `[e.g., 2/8 pilot sessions timed out]` | `[e.g., Increase task timeout]` | `[Yes / No]` | `[Yes / No]` | `[MUST BE NONE]` | `[APPROVED / REJECTED]` |
| **PILOT-02** | `[Describe problem]` | `[e.g., Telemetry drop on blur]` | `[e.g., Fix JS event listener]` | `[No - Bug fix]` | `[No]` | `[NONE]` | `[APPROVED / REJECTED]` |

> [!IMPORTANT]  
> **Change-Control Constraint:** No modifications to primary hypotheses (H1, H2, H3), sample size ($N=144$), experimental arms, task scenarios, or primary statistical models are permitted based on pilot data. Any operational bug fixes must preserve complete methodological parity with Protocol v1.1.0.
