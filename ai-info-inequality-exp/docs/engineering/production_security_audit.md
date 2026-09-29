# Production Security and Configuration Hardening Audit
**Study Title:** English-Hindi AI-Mediated Information Seeking Experiment  
**Protocol Version:** `1.1.0-gemini-frozen`  
**Milestone:** Productionization Milestone 2 (Security & Hardening)  
**Date:** September 27, 2026  
**Status:** `SECURITY HARDENING COMPLETE WITH NON-BLOCKING RISKS`

---

## Executive Summary

This document presents the security, configuration, and transport hardening audit for the experimental platform supporting Protocol v1.1.0 (`gemini-3.5-flash` / `3.5-flash-05-2026`). All core research parameters (research questions, hypotheses, $N=144/171$, 3 arms, 3 scenarios, scoring rubrics, telemetry schemas, and Gemini generation parameters) remain **100% frozen and unmodified**.

All 35 automated tests (30 core regression tests + 5 targeted production security tests) pass cleanly.

---

## 1. Security Changes

The following key security features and architectural controls were implemented in the backend:

1. **Production Configuration Guard (`validate_production_config`)**:
   - Programmatically blocks application startup in `APP_ENV=production` if `USE_MOCK_LLM=True`, `GEMINI_API_KEY` is missing/empty, SQLite is specified in `DATABASE_URL`, or `CORS_ALLOWED_ORIGINS` contains wildcard (`*`) or localhost domains.
2. **Rate Limiting Engine (`app/core/rate_limit.py`)**:
   - Implemented an in-memory thread-safe sliding window rate limiter (`RateLimiter`) enforcing limits on public session creation (`/api/v1/session/create`).
3. **Administrative Access Control (`app/core/auth.py`)**:
   - Protected administrative and data export endpoints (`/api/v1/admin/*`) via mandatory `X-Admin-API-Key` header authentication (`require_admin_auth`).
4. **Security Headers Middleware**:
   - Added automated security headers (`X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `X-XSS-Protection: 1; mode=block`, `Referrer-Policy: strict-origin-when-cross-origin`, and `Strict-Transport-Security: max-age=31536000; includeSubDomains` in production).
5. **Production Error Response Sanitization**:
   - Registered a global uncaught exception handler suppressing internal stack traces, SQL errors, and file paths on HTTP 500 responses in production.
   - Sanitized Gemini/LLM gateway exceptions on HTTP 502 responses in production.

---

## 2. Configuration Changes

The configuration system (`app/config.py`) now enforces explicit environment separation:

| Environment Variable | Development Default | Test Default | Production Requirement |
|---|---|---|---|
| `APP_ENV` | `"development"` | `"test"` | `"production"` |
| `USE_MOCK_LLM` | `True` | `True` / `False` | **MUST BE `False`** |
| `DATABASE_URL` | `sqlite:///...` | `sqlite:///:memory:` | **MUST BE PostgreSQL connection string** |
| `GEMINI_API_KEY` | `""` (or mock) | `""` | **MUST BE valid Gemini API Key** |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:3000` | `http://testserver` | **MUST BE explicit production HTTPS domain(s)** |
| `RATE_LIMIT_ENABLED` | `True` | `False` | **`True`** |
| `RATE_LIMIT_PER_MINUTE` | `10` | `1000` | **Configurable (Default: 10/min)** |
| `ADMIN_API_KEY` | `""` (permissive in dev) | `"test-admin-key"` | **MUST BE strong secret string** |

---

## 3. Endpoint Classification

Every endpoint across the API surface has been audited and classified:

| Endpoint Path | Method | Category | Auth Level | Exposed Data / Function |
|---|---|---|---|---|
| `/` | `GET` | System | Public | Root status & protocol version |
| `/api/v1/session/create` | `POST` | Participant-Facing | Public (Rate Limited) | Creates participant record, computes salted SHA-256 IP hash |
| `/api/v1/session/{id}` | `GET` | Participant-Facing | Participant ID | Retrieves task flow state |
| `/api/v1/consent/submit` | `POST` | Participant-Facing | Participant ID | Stores consent decision |
| `/api/v1/screening/submit` | `POST` | Participant-Facing | Participant ID | Stores language eligibility answers |
| `/api/v1/language-background/submit` | `POST` | Participant-Facing | Participant ID | Stores self-reported language proficiency |
| `/api/v1/ai-literacy/submit` | `POST` | Participant-Facing | Participant ID | Stores AILS-10 responses |
| `/api/v1/randomization/assign` | `POST` | Participant-Facing | Participant ID | Assigns experimental arm & scenario sequence |
| `/api/v1/tasks/{id}/start` | `POST` | Participant-Facing | Participant ID | Begins task timer |
| `/api/v1/tasks/{id}/complete` | `POST` | Participant-Facing | Participant ID | Stores final response & calculates rubric score |
| `/api/v1/chat/message` | `POST` | Participant-Facing | Participant ID | Queries Gemini LLM Gateway & stores transcript |
| `/api/v1/telemetry/log` | `POST` | Participant-Facing | Participant ID | Stores fine-grained interaction telemetry |
| `/api/v1/post-task/submit` | `POST` | Participant-Facing | Participant ID | Stores NASA-TLX workload & confidence ratings |
| `/api/v1/debrief/complete` | `POST` | Participant-Facing | Participant ID | Concludes session |
| `/api/v1/admin/health` | `GET` | Administrative | Admin API Key (`X-Admin-API-Key`) | System status & database counters |
| `/api/v1/admin/export/summary` | `GET` | Administrative | Admin API Key (`X-Admin-API-Key`) | Aggregated participant session counts |

---

## 4. Secret-Handling Audit

1. **Repository Audit Findings**:
   - No hardcoded API keys, database passwords, or JWT secrets exist in tracked source files (`.py`, `.ts`, `.tsx`, `.json`, `.md`).
   - `.env` files contain template placeholders (`GEMINI_API_KEY=""`, `DATABASE_URL=""`). `.env` is explicitly included in `.gitignore`.
2. **Frontend Exposure Prevention**:
   - Frontend code (`frontend/src`) interacts exclusively via relative backend API endpoints (`/api/v1/...`). Gemini API keys are **NEVER** exposed to client-side code or browser network requests.
3. **Log & Exception Sanitization**:
   - In production mode, exception handlers suppress connection string details, database passwords, and API key strings from HTTP responses and stdout logs.

---

## 5. Logging Audit

To ensure compliance with participant privacy requirements while preserving study telemetry:

- **Participant Content Minimization**:
  - IP addresses are converted to anonymized SHA-256 hashes (`sha256(ip + salt)`) immediately at session creation. Raw IP addresses are **NEVER** logged or stored.
  - Standard application stdout/stderr logs emit only technical execution metadata (HTTP status, endpoint route, response latency, technical error codes).
- **Separation of Infrastructure Logs vs. Research Data**:
  - `RESEARCH DATA`: Participant chat transcripts, prompt texts, search queries, scoring results, and telemetry events are stored strictly in the encrypted PostgreSQL database (`messages`, `telemetry_events`, `task_sessions` tables) for scientific analysis.
  - `APPLICATION LOGS`: Server stdout handles container/web-server health, HTTP request tracing, and exception alerts, stripped of PII.

---

## 6. CORS Audit

- **Audit Result**: Wildcard origins (`*`) and localhost/loopback origins (`localhost`, `127.0.0.1`) are completely stripped from production configuration requirements.
- **Enforcement**: `validate_production_config()` checks `CORS_ALLOWED_ORIGINS` on startup in `production` mode. If any wildcard or localhost origin is present, backend startup aborts immediately with a `ValueError`.
- **Production Setup**: Must be set via environment variable:
  ```env
  CORS_ALLOWED_ORIGINS="https://exp.yourdomain.org"
  ```

---

## 7. Rate-Limit Configuration

- **Target Endpoint**: `/api/v1/session/create` (Public session initialization endpoint).
- **Mechanism**: In-memory sliding window algorithm (`RateLimiter` class in `app/core/rate_limit.py`) keyed exclusively by client IP address.
- **Rationale**: Prevents automated bot request flooding, denial-of-service, or database table bloat without interfering with legitimate participant task flow.
- **Research Independence**: **Zero participant research variables** (e.g. assigned arm, language background, task responses) are used for rate-limiting calculations.
- **Configuration**:
  ```env
  RATE_LIMIT_ENABLED=True
  RATE_LIMIT_PER_MINUTE=10
  ```
- **Response**: Returns clean `HTTP 429 Too Many Requests` with payload `{"detail": "Rate limit exceeded. Please try again later."}`.

---

## 8. Production Error Handling

- **Global Exception Handler**:
  - Registered in `app/main.py`. In `production`, any uncaught exception returns:
    ```json
    {
      "detail": "An internal server error occurred."
    }
    ```
- **Gateway Error Sanitization**:
  - LLM Gateway exceptions in `app/api/v1/chat.py` return `HTTP 502` with detail `"AI service temporarily unavailable."` in production, concealing provider error traces and internal hostnames.

---

## 9. Security Headers

The following HTTP security headers are injected into every API response via FastAPI middleware:

```http
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Strict-Transport-Security: max-age=31536000; includeSubDomains (Production only)
```

---

## 10. Dependency Findings

- **Backend Dependencies (`requirements.txt`)**:
  - `fastapi==0.115.0`, `uvicorn==0.30.6`, `pydantic==2.9.2`, `sqlalchemy==2.0.35`, `psycopg2-binary==2.9.9`.
  - All core libraries are pinned to recent stable security releases. No high-risk vulnerability flags detected locally.
- **Frontend Dependencies (`package.json`)**:
  - `react==^18.3.1`, `vite==^5.4.8`, `typescript==^5.6.2`, `tailwindcss==^3.4.13`.
  - Lightweight component footprint without unnecessary third-party utility dependencies.

---

## 11. Remaining Risks Assessment

Remaining risks are audited and categorized according to severity:

| Risk ID | Severity | Description | Mitigation Status / Recommendation |
|---|---|---|---|
| **RISK-01** | `INFORMATIONAL` | **TLS Termination at Reverse Proxy**: Backend application relies on upstream Nginx / Cloudflare / Cloud Run reverse proxy for HTTPS termination before reaching Uvicorn. | Standard production deployment pattern. Documented in transport architecture. Non-blocking. |
| **RISK-02** | `INFORMATIONAL` | **Single-Node In-Memory Rate Limiting**: The sliding-window rate limiter stores IP request timestamps in Uvicorn process memory. If scaled horizontally across multiple instances without sticky sessions, rate limits execute per-instance. | Acceptable for N=171 single-host deployment. Non-blocking. |
| **RISK-03** | `LOW` | **Database Password Rotation Protocol**: Production PostgreSQL password must be set via environment variable `DATABASE_URL` during deployment. | Operational deployment requirement. No secrets stored in codebase. Non-blocking. |
| **RISK-04** | `LOW` | **Admin API Key Secret Entropy**: Administrative endpoints rely on `X-Admin-API-Key`. A cryptographically strong 64-character secret must be generated for production. | Operational deployment requirement. Non-blocking. |

---

## Transport Architecture Summary

```
Browser (Participant / React SPA)
  │
  │ HTTPS (TLS 1.3)
  ▼
Frontend CDN / Web Server (HTTPS)
  │
  │ HTTPS API Proxying
  ▼
FastAPI Uvicorn Application (Production Security Hardened)
  │                                    │
  │ TLS Connection                     │ HTTPS API Calls (TLS 1.3)
  ▼                                    ▼
PostgreSQL Production Database       Google Gemini API Gateway
(Encrypted at Rest & in Transit)     (gemini-3.5-flash / 3.5-flash-05-2026)
```

---

## Verification Summary

- **Total Test Count**: 35 tests
- **Test Result**: 35 PASSED, 0 FAILED
- **Security Tests Covered**:
  - `test_security_headers`: PASSED
  - `test_admin_endpoint_auth`: PASSED
  - `test_rate_limiting_enforcement`: PASSED
  - `test_production_config_validation`: PASSED
  - `test_production_error_sanitization`: PASSED

---

## Final Status Declaration

`SECURITY HARDENING COMPLETE WITH NON-BLOCKING RISKS`
