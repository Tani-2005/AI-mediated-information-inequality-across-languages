# Final Documentation-Level Reproducibility & Model Availability Audit

**Date:** 2026-09-25  
**Protocol Version Transition:** `1.0.0-frozen` → `1.1.0-gemini-frozen`  
**Project:** English-Hindi AI-Mediated Information Seeking Experiment  
**Target Provider:** Google Gemini API (`generativelanguage.googleapis.com`)  

---

## A. Exact Model Lifecycle Status

From official Google Gemini API metadata (`https://generativelanguage.googleapis.com/v1beta/models`):
- **Model Identifier:** `gemini-3.5-flash`
- **Build Version Tag:** `3.5-flash-05-2026` (Release May 2026)
- **Lifecycle Stage:** Active Production Stable Release
- **Deprecation Policy:** Google Gemini API models follow a formal deprecation lifecycle. When a model version approaches end-of-life, Google provides a minimum 90-day deprecation window before sunsetting the model endpoint with HTTP 404 (as observed during empirical testing of deprecated models `gemini-2.0-flash` and `gemini-2.5-flash`).

---

## B. Is `gemini-3.5-flash` Immutable?

**NO.** In Google's API architecture:
- `gemini-3.5-flash` is a **stable model identifier** pointing to build version `3.5-flash-05-2026`.
- Unlike point-in-time date-stamped snapshots (e.g. OpenAI's `gpt-4o-2024-08-06`), Google reserves the right to issue minor weight patches under a static family identifier.
- Therefore, calling `gemini-3.5-flash` a "byte-for-byte immutable frozen snapshot" is scientifically imprecise. It is a **stable production model identifier**.

---

## C. Exact Reproducibility Metadata Frozen

To achieve maximum scientific reproducibility under Gemini API's model lifecycle, the following exact metadata matrix is logged and frozen:

1. **`model_identifier`**: `gemini-3.5-flash`
2. **`model_version`**: `3.5-flash-05-2026`
3. **`provider`**: `Google Gemini API` (`generativelanguage.googleapis.com`)
4. **`api_endpoint`**: `https://generativelanguage.googleapis.com/v1beta/openai/chat/completions`
5. **`system_prompt_version`**: `v1.1.0-gemini-frozen`
6. **`generation_parameters`**: `temperature: 0.2`, `top_p: 1.0`, `max_tokens: 1000`
7. **`session_telemetry`**: Request timestamp, HTTP status, `model` field returned in API response (`gemini-3.5-flash`), `prompt_tokens`, `completion_tokens`, and full response text.

---

## D. Configuration Terminology Correction

The configuration terminology in [`experiment_config.json`](file:///c:/Antigravity%20Projects/AI-mediated%20information%20inequality%20across%20languages/ai-info-inequality-exp/experiment_config.json), [`config.py`](file:///c:/Antigravity%20Projects/AI-mediated%20information%20inequality%20across%20languages/ai-info-inequality-exp/backend/app/config.py), [`llm_gateway.py`](file:///c:/Antigravity%20Projects/AI-mediated%20information%20inequality%20across%20languages/ai-info-inequality-exp/backend/app/core/llm_gateway.py), and test suites has been updated from `model_snapshot` to **`model_identifier`**, with `model_version` explicitly added:

```json
{
  "production_llm_config": {
    "provider": "Google Gemini API",
    "model_identifier": "gemini-3.5-flash",
    "model_version": "3.5-flash-05-2026",
    "base_url": "https://generativelanguage.googleapis.com/v1beta/openai",
    "temperature": 0.2,
    "top_p": 1.0,
    "max_tokens": 1000,
    "timeout_ms": 15000,
    "max_retries": 1,
    "retry_condition": "HTTP_5XX_OR_TIMEOUT_ONLY"
  }
}
```

---

## E. Methodological Elements Preserved STRICTLY UNCHANGED

- **Research Questions & Hypotheses:** Unchanged.
- **Target Population:** English-Hindi bilingual Indian adults aged 18–65 residing in India.
- **Experimental Arms (3):** `ENGLISH_ONLY`, `HINDI_ONLY`, `CODE_SWITCHING`.
- **Sample Size Design ($N=144$ analyzable):** 48 participants per arm, total recruitment target $N=171$.
- **Civic Task Scenarios (3):** PMEGP, PM Vishwakarma, PM SVANidhi.
- **Counterbalancing:** 3×3 Latin-Square task ordering across positions 1, 2, and 3.
- **Primary Outcome Measure:** Continuous Decision Quality Score (0.0 to 10.0) evaluated against deterministic ground-truth rubrics.
- **Statistical Model:** Linear Mixed-Effects Model (LMM): `DecisionQuality ~ Language + Scenario + Position + (1|Participant)`.

---

## F. Final Status

```text
TECHNICALLY READY FOR PROTOCOL RE-FREEZE
```

> [!IMPORTANT]  
> A successful real API smoke test and model availability audit establishes technical readiness, provider integrity, model availability, and response handling.  
>  
> It does **NOT** establish model quality, multilingual equivalence, or experimental validity.  
>  
> **Human recruitment remains contingent on formal ethics approval.**
