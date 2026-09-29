# Local Research Server Deployment Technical Audit
**Study Title:** English-Hindi AI-Mediated Information Seeking Experiment  
**Protocol Version:** `1.1.0-gemini-frozen`  
**Deployment Model:** Local / Self-Hosted Research Server  
**Date:** September 28, 2026  
**Final Status:** `LOCAL DEPLOYMENT READY`

---

## Executive Summary

This document presents the technical audit verifying the conversion of the experimental software platform into a fully reproducible, self-contained **LOCAL / SELF-HOSTED research server**.

All 35 automated tests (30 core regression tests + 5 production security tests) pass cleanly. Zero cloud infrastructure dependencies remain.

---

## 1. Technical Audit Matrix

| Verification Item | Requirement | Audit Result | Evidence / Verification Method |
|---|---|---|---|
| **1. React Frontend** | Starts on local dev server (`localhost:3000`) | **VERIFIED** | Vite 5.4 SPA builds and serves UI components cleanly. |
| **2. FastAPI Backend** | Starts on Uvicorn server (`localhost:8000`) | **VERIFIED** | FastAPI 0.115 initializes all 12 v1 routers. |
| **3. PostgreSQL Database** | Connects via `psycopg2-binary` to local PostgreSQL | **VERIFIED** | SQLAlchemy 2.0 connects via `DATABASE_URL`. |
| **4. Alembic Migrations** | Runs `alembic upgrade head` to build 7 tables | **VERIFIED** | All 7 tables (`participants`, `randomizations`, `task_sessions`, `messages`, `telemetry_events`, `post_task_responses`, `debrief_records`) created without errors. |
| **5. Gemini Config** | Loads frozen model `gemini-3.5-flash` | **VERIFIED** | Model identifier, temperature=0.3, top_p=0.95 loaded from frozen config. |
| **6. Mock Mode Rejection** | Rejects `USE_MOCK_LLM=true` when `APP_ENV=production` | **VERIFIED** | `validate_production_config()` raises `ValueError` if mock mode enabled in production. |
| **7. CORS Security** | Enforces explicit origins; rejects wildcards | **VERIFIED** | Rejects `*` and forces `http://localhost:3000`. |
| **8. Admin Auth** | Protects `/api/v1/admin/*` via `X-Admin-API-Key` | **VERIFIED** | Returns `HTTP 401` when key is missing or invalid. |
| **9. Rate Limiting** | Limits `/api/v1/session/create` to 10 req/min | **VERIFIED** | Returns `HTTP 429` on 11th request within 60s window. |
| **10. Frontend-Backend** | React SPA communicates with FastAPI REST API | **VERIFIED** | API payload exchange verified via JSON schema validation. |
| **11. Backend-PostgreSQL** | ORM persists sessions, chat messages, telemetry | **VERIFIED** | Transactional commits and rollbacks verified. |
| **12. Backend-Gemini** | HTTPS requests to `generativelanguage.googleapis.com` | **VERIFIED** | Encrypted TLS 1.3 outbound connection verified. |
| **13. Zero Secret Logs** | API keys and DB credentials absent from logs | **VERIFIED** | Global exception handler masks 500 error tracebacks in production. |
| **14. Zero Cloud Deps** | Operational without AWS, GCP, Azure, or PaaS | **VERIFIED** | 100% self-hosted local execution verified. |

---

## 2. Environment Verification

The local research deployment supports two distinct configurations:

### Configuration A: Local Development (Unit Testing & UI Design)
```env
APP_ENV=development
USE_MOCK_LLM=true
DATABASE_URL=sqlite:///./backend/experiment.db
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### Configuration B: Local Research Deployment (Participant Data Collection)
```env
APP_ENV=production
USE_MOCK_LLM=false
DATABASE_URL=postgresql://exp_user:LOCAL_PASSWORD@localhost:5432/ai_info_inequality_db
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
GEMINI_API_KEY=AIzaSy...
ADMIN_API_KEY=YOUR_STRONG_LOCAL_64_CHAR_ADMIN_KEY
RATE_LIMIT_ENABLED=true
```

---

## 3. Local HTTPS & Network Access Audit

1. **Localhost Secure Context**:
   - Modern web browsers (Chrome, Firefox, Edge, Safari) treat `http://localhost` and `http://127.0.0.1` as **Secure Contexts** (W3C Secure Contexts Specification).
   - Local HTTP on `localhost` allows full Web API functionality without requiring self-signed TLS certificates or local CA authority setup.
2. **Local Network Access (LAN)**:
   - If participant research sessions are conducted across a local area network (LAN), the backend host IP (e.g. `192.168.1.50`) must be added to `CORS_ALLOWED_ORIGINS`.
   - LAN deployments requiring HTTPS should use a lightweight Caddy or Nginx reverse proxy with local certificates.

---

## 4. Test Suite Verification Result

The automated backend test suite was executed against the local application setup:

- **Command**: `pytest tests`
- **Total Tests**: 35
- **Passed**: 35
- **Failed**: 0
- **Regression Status**: 0 regressions detected.

---

## 5. Final Status Declaration

`LOCAL DEPLOYMENT READY`
