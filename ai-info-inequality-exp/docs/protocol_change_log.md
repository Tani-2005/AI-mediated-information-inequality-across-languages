# Protocol Change Log

**Project:** English-Hindi AI-Mediated Information Seeking Experiment  
**Protocol Version Transition:** `1.0.0-frozen` → `1.1.0-gemini-frozen`  
**Date:** 2026-09-25  

---

## 1. Summary of Protocol Modification

```text
Original:
Provider = OpenAI Direct API
Model = gpt-4o-2024-08-06
System Prompt Version = v1.0.0-frozen

Selected & Verified Production Configuration:
Provider = Google Gemini API
Model = gemini-3.5-flash
Base URL = https://generativelanguage.googleapis.com/v1beta/openai
System Prompt Version = v1.1.0-gemini-frozen

Reason:
Operational/API-credit constraint on the OpenAI account prior to participant recruitment.

Participant Data Collected Before Change:
NONE
```

---

## 2. Technical Reasons for Change

- The OpenAI API account reached zero available API credit balance during production integration testing.
- Official model enumeration via Google's API (`https://generativelanguage.googleapis.com/v1beta/models`) verified that `gemini-3.5-flash` is an active, stable production model supporting chat completions, system instructions, and bilingual output (English & Hindi).

---

## 3. Empirical Model Availability & Candidate Selection

Official model enumeration returned 50 models from Google's API endpoint. Candidate comparison for stable production Flash models:

| Model Identifier | Official API Listing | Stable? | English | Hindi | System Instruction | Temperature (0.2) | Max Tokens (1000) | Live API Status | Selection Decision |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`gemini-3.5-flash`** | YES | YES | YES | YES | YES | Supported | Supported | **HTTP 200 OK** | **SELECTED** |
| **`gemini-3.8-flash`** | YES | YES | YES | YES | YES | Supported | Supported | HTTP 503 (High Demand) | Excluded (Transient Spikes) |
| **`gemini-2.5-flash`** | YES | NO | N/A | N/A | N/A | N/A | N/A | HTTP 404 (Deprecated) | Excluded (Deprecated) |
| **`gemini-2.0-flash`** | NO | NO | N/A | N/A | N/A | N/A | N/A | HTTP 404 (Deprecated) | Excluded (Deprecated) |
| **`gemini-1.5-flash`** | NO | NO | N/A | N/A | N/A | N/A | N/A | HTTP 404 (Not Found) | Excluded (Not Found) |

### Selection Justification:
`gemini-3.5-flash` was selected based **ONLY** on official API availability, snapshot stability, parameter compatibility, and empirical HTTP 200 verification. No claim is made that it is "better" or "more accurate" than other models.

---

## 4. Methodological and Scientific Implications

1. **Non-Equivalence Acknowledgment:**  
   Google Gemini `gemini-3.5-flash` and OpenAI `gpt-4o-2024-08-06` are **not** scientifically or architecturally identical models. Their pre-training corpora, tokenizers, fine-tuning, and Indic language capabilities differ.
2. **Timing of Change:**  
   Because **ZERO human participant data** has been collected, the model change is introduced prior to study execution and pre-registration freeze. No post-hoc data splitting or selective model replacement has occurred.
3. **Internal Validity:**  
   All experimental arms (`ENGLISH_ONLY`, `HINDI_ONLY`, `CODE_SWITCHING`) within the randomized trial will interact with the exact same production model snapshot (`gemini-3.5-flash`). Therefore, the primary contrast ($C_1: \mu_{English} - \mu_{Hindi} \neq 0$) remains unconfounded within the study.

---

## 5. Methodological Elements Remaining STRICTLY UNCHANGED

- **Research Questions & Hypotheses:** Unchanged.
- **Target Population:** English-Hindi bilingual Indian adults aged 18–65 residing in India.
- **Experimental Arms (3):** `ENGLISH_ONLY`, `HINDI_ONLY`, `CODE_SWITCHING`.
- **Sample Size Design ($N=144$ analyzable):** 48 participants per arm, total recruitment target $N=171$.
- **Randomization Structure:** 1:1:1 stratified block randomization (block sizes 3 & 6) concealed server-side based on 12-item AI Literacy Scale (AILS).
- **Civic Task Scenarios (3):** PMEGP, PM Vishwakarma, PM SVANidhi.
- **Counterbalancing:** 3×3 Latin-Square task ordering across positions 1, 2, and 3.
- **Primary Outcome Measure:** Continuous Decision Quality Score (0.0 to 10.0) evaluated against deterministic ground-truth rubrics (no LLM-as-judge).
- **Statistical Model:** Linear Mixed-Effects Model (LMM): `DecisionQuality ~ Language + Scenario + Position + (1|Participant)`.
