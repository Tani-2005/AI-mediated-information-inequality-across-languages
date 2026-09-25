# Official Empirical Model Availability Audit & Real Smoke Test Report: Google Gemini API

**Date:** 2026-09-25  
**Protocol Version Transition:** `1.0.0-frozen` → `1.1.0-gemini-frozen`  
**Project:** English-Hindi AI-Mediated Information Seeking Experiment  
**Target Provider:** Google Gemini API (`generativelanguage.googleapis.com`)  

---

## 1. Official API Model Enumeration

Querying Google's official model-listing API (`https://generativelanguage.googleapis.com/v1beta/models`) with the configured `GEMINI_API_KEY` returned **50 models**.

### Candidate Comparison Table (Stable Flash Production Models):

| Model Identifier | Official API Listing | Stable? | English Support | Hindi Support | System Instruction | Temperature (0.2) | Max Tokens (1000) | Live API Status | Selection Decision |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`gemini-3.5-flash`** | YES | YES | YES | YES | YES | Supported | Supported | **HTTP 200 OK** | **SELECTED** |
| **`gemini-3.8-flash`** | YES | YES | YES | YES | YES | Supported | Supported | HTTP 503 (High Demand) | Excluded (Transient Spikes) |
| **`gemini-2.5-flash`** | YES | NO | N/A | N/A | N/A | N/A | N/A | HTTP 404 (Deprecated) | Excluded (Deprecated) |
| **`gemini-2.0-flash`** | NO | NO | N/A | N/A | N/A | N/A | N/A | HTTP 404 (Deprecated) | Excluded (Deprecated) |
| **`gemini-1.5-flash`** | NO | NO | N/A | N/A | N/A | N/A | N/A | HTTP 404 (Not Found) | Excluded (Not Found) |

### Exclusion Criteria:
- Preview models (`gemini-3-flash-preview`, `gemini-3.1-pro-preview`, `gemini-3.1-flash-lite-preview`) were excluded to prevent non-reproducible model shifts.
- Dynamic aliases (`gemini-flash-latest`) were excluded because underlying model snapshots can change without notice.
- Deprecated models (`gemini-2.5-flash`, `gemini-2.0-flash`) were excluded due to API 404 rejections.

---

## 2. Selected Protocol Candidate

```text
SELECTED PRODUCTION MODEL:
gemini-3.5-flash
```

### Technical Selection Basis:
Selection is based **ONLY** on API availability, snapshot stability, parameter compatibility, and live HTTP 200 verification. No claim is made that `gemini-3.5-flash` is "better" or "more capable" than other models.

---

## 3. Updated Frozen Configuration

```json
{
  "production_llm_config": {
    "provider": "Google Gemini API",
    "model_snapshot": "gemini-3.5-flash",
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

## 4. Real Synthetic Smoke Test Verification

Executed **EXACTLY ONE** real synthetic request using `gemini-3.5-flash` against `https://generativelanguage.googleapis.com/v1beta/openai/chat/completions`:

```text
Provider            : Google Gemini API
Endpoint            : https://generativelanguage.googleapis.com/v1beta/openai/chat/completions
Requested Model     : gemini-3.5-flash
Actual Model        : gemini-3.5-flash
HTTP Status         : 200 OK
Latency             : 11,797 ms
Input Tokens        : 128
Output Tokens       : 231
Total Tokens        : 359
Retry Count         : 0
Language Leakage    : False
Is Mock             : False
Estimated Cost      : $0.000079 USD
```

### Verification Checks:
- [x] HTTP Status is `200 OK`.
- [x] Provider is `Google Gemini API`.
- [x] Requested model matches actual model (`gemini-3.5-flash`).
- [x] Endpoint is `generativelanguage.googleapis.com`.
- [x] `is_mock = false`.
- [x] **Zero** fallback or third-party gateways contacted.

---

## 5. Security & Isolation Confirmation

- [x] `GEMINI_API_KEY` is backend-only.
- [x] No API key in frontend, logs, or git commits.
- [x] Requests were routed **EXCLUSIVELY** to `https://generativelanguage.googleapis.com`.
- [x] **NO** participant PII, AILS scores, ground-truth rubrics, or research hypotheses sent in prompt payloads.

---

## 6. Automated Test Suite Execution

Ran complete test suite via `.\backend\venv\Scripts\pytest tests`:

```text
======================= 30 passed in 1.67s =======================
```

---

## 7. Critical Methodological Disclaimer

> [!IMPORTANT]  
> A successful real API smoke test establishes:  
> **API connectivity + provider integrity + model availability + response handling + logging + security.**  
>  
> It does **NOT** establish model quality, multilingual equivalence, or experimental validity. One response cannot establish model quality.  
>  
> **Human recruitment remains contingent on formal ethics approval.**

---

## 8. Final Status

```text
READY FOR PROTOCOL RE-FREEZE
```

### Protocol Change Log Status:
The selection of `gemini-3.5-flash` has been fully updated in [`docs/protocol_change_log.md`](file:///c:/Antigravity%20Projects/AI-mediated%20information%20inequality%20across%20languages/ai-info-inequality-exp/docs/protocol_change_log.md). No further modifications to the change log are required.
