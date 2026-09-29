# Technical Productionization Audit

**Protocol Version:** `1.1.0-gemini-frozen`  
**Study Identifier:** `ENGLISH_HINDI_AI_INFO_INEQUALITY_2026`  
**Date:** 2026-09-27  
**Audit Purpose:** Comprehensive Codebase Infrastructure & Production Readiness Evaluation  

---

## Final Audit Status

```text
PRODUCTIONIZATION AUDIT PASSED WITH BLOCKERS
```

> [!IMPORTANT]  
> This audit evaluates the technical infrastructure, database architecture, security controls, configuration parameters, and deployment requirements needed to transition the application from local development (`SQLite` / `MockLLM`) to a secure production environment (`PostgreSQL` / `Google Gemini API`).  
>  
> **Methodological Freeze:** No changes have been made to Protocol v1.1.0, research questions, hypotheses, sample size ($N=144/171$), experimental arms, task scenarios, outcome scoring, or Gemini model configurations.

---

## 1. Current Architecture Overview

A direct inspection of the codebase yields the following architectural inventory:

- **Frontend SPA Framework:** React 18 (`^18.3.1`), Vite 5 (`^5.4.8`), TypeScript (`^5.6.2`), Tailwind CSS (`^3.4.13`), Lucide React (`^0.446.0`). Implements screens S1 to S10 (`frontend/src/App.tsx`).
- **Backend API Framework:** FastAPI (`0.115.0`), Python 3.11+, Uvicorn (`0.30.6`) ASGI web server.
- **Database Engine (Development):** Local SQLite (`backend/experiment.db`), accessed via SQLAlchemy 2.0 ORM (`2.0.35`). Table creation currently invoked on FastAPI startup (`Base.metadata.create_all` in `backend/app/main.py`). Alembic (`1.13.2`) included in dependencies.
- **ORM / Data Access Layer:** SQLAlchemy 2.0 models in `backend/app/db/models.py`. Session dependency managed via `get_db` generator in `backend/app/db/session.py`.
- **API Structure:** RESTful API under `/api/v1/` with 11 modular routers (`session`, `consent`, `screening`, `language_background`, `ai_literacy`, `randomization`, `tasks`, `chat`, `telemetry`, `post_task`, `debrief`).
- **LLM Provider Gateway:** `backend/app/core/llm_gateway.py`. Provider abstraction supporting `MockLLMProvider` (dev mock) and `GeminiProvider` (Google Gemini API via OpenAI-compatible endpoint `https://generativelanguage.googleapis.com/v1beta/openai`). Model lock enforces `gemini-3.5-flash` (build tag `3.5-flash-05-2026`).
- **Configuration Engine:** `backend/app/config.py` using Pydantic Settings (`BaseSettings`) and `ConfigDict(env_file=[".env", "backend/.env"], extra="ignore")`. Loads experimental parameters from `experiment_config.json`.
- **Authentication & State Control:** Pseudonymous UUID v4 tracking (`participant_id`). Zero passwords or PII stored. State progression strictly enforced by participant status (`CONSENTED` $\rightarrow$ `SCREENED` $\rightarrow$ `BASELINE_DONE` $\rightarrow$ `RANDOMIZED` $\rightarrow$ `IN_PROGRESS` $\rightarrow$ `COMPLETED`).
- **Telemetry System:** `POST /api/v1/telemetry/event` logging high-resolution events (`DOCUMENT_OPENED`, `DOC_VIEW_TIME` / `DocClicks`/`DocDuration`, `TAB_FOCUS_CHANGED` / `WindowBlur`, `TASK_STARTED`, `FINAL_DECISION_SUBMITTED`) to `telemetry_events` table.
- **Scoring Engine:** Deterministic rule engine (`backend/app/scoring/engine.py`) matching submitted structural fields against JSON ground-truth rubrics (`data/ground_truth/*.json`). 0.0 to 10.0 scale. Zero LLM-as-judge.
- **Background Workers & Queues:** None. Requests operate synchronously with 1 retry on HTTP 5xx/timeout for LLM proxy completions.
- **Object / File Storage:** None. All application state is relationally stored.

---

## 2. Database Schema & Migration Audit

An audit of `backend/app/db/models.py` identified 12 relational entities:

| Table Name | Primary Key | Foreign Keys & Constraints | Indexes / Uniques | Nullable Fields |
| :--- | :--- | :--- | :--- | :--- |
| `participants` | `participant_id` (String64 UUID v4) | None | `ip_hash` (Index) | None |
| `consent_logs` | `consent_id` (Integer) | FK `participants.participant_id` | `participant_id` (Unique) | None |
| `screening_logs` | `screening_id` (Integer) | FK `participants.participant_id` | `participant_id` (Unique) | None |
| `language_background` | `bg_id` (Integer) | FK `participants.participant_id` | `participant_id` (Unique) | None |
| `ai_literacy` | `ails_id` (Integer) | FK `participants.participant_id` | `participant_id` (Unique) | None |
| `randomization_allocations` | `alloc_id` (Integer) | FK `participants.participant_id` | `participant_id` (Unique) | None |
| `task_sessions` | `session_id` (Integer) | FK `participants.participant_id` | None | `completed_at` (Nullable) |
| `messages` | `message_id` (Integer) | FK `task_sessions.session_id`, `participants.participant_id` | `task_session_id` (Index) | `tokens_used`, `latency_ms` (Nullable) |
| `telemetry_events` | `event_id` (Integer) | FK `participants.participant_id` | `participant_id` (Index) | `task_id` (Nullable) |
| `final_decisions` | `decision_id` (Integer) | FK `task_sessions.session_id`, `participants.participant_id` | `task_session_id` (Unique) | None |
| `post_task_measures` | `measure_id` (Integer) | FK `participants.participant_id` | `participant_id` (Unique) | `feedback_comments` (Nullable) |
| `technical_errors` | `error_id` (Integer) | None | None | `participant_id`, `task_id`, `context_data` (Nullable) |

### PostgreSQL Migration Requirements:
1. **DB Driver:** Add `psycopg2-binary` to `backend/requirements.txt`.
2. **Schema Migration Tooling:** Replace runtime `Base.metadata.create_all(bind=engine)` in `main.py` with versioned Alembic migration scripts (`alembic upgrade head`) executed prior to server startup.
3. **JSON Column Types:** SQLAlchemy `JSON` columns automatically map to PostgreSQL `JSONB` for optimized indexing and query performance.
4. **Timezone Handling:** PostgreSQL enforces `TIMESTAMP WITH TIME ZONE`. Database models already use `datetime.now(datetime.UTC)` defaults.

---

## 3. Configuration & Environment Audit

| Variable Name | Category | Hard-coded Default | Production Requirement | Secrets Governance |
| :--- | :--- | :--- | :--- | :--- |
| `APP_ENV` | Public Config | `"development"` | Set to `"production"` | Environment variable |
| `USE_MOCK_LLM` | Public Config | `True` | Set to `False` | Environment variable |
| `IS_PILOT_MODE` | Public Config | `False` | Set to `False` (or `True` for pilot) | Environment variable |
| `LLM_ENABLED` | Public Config | `True` | Set to `True` | Environment variable |
| `LLM_PROVIDER` | Public Config | `"gemini"` | Set to `"gemini"` | Environment variable |
| `GEMINI_API_KEY` | **Secret** | `""` | **MUST be set via Secret Manager** | **NEVER in Git** |
| `GEMINI_BASE_URL` | Public Config | `"https://generativelanguage.googleapis.com/v1beta/openai"` | Must match official endpoint | Environment variable |
| `GEMINI_MODEL` | Public Config | `"gemini-3.5-flash"` | Locked to `"gemini-3.5-flash"` | Environment variable |
| `DATABASE_URL` | **Secret** | `sqlite:///.../experiment.db` | **PostgreSQL Connection String** | Secrets Manager |
| `CORS_ALLOWED_ORIGINS` | Public Config | `"http://localhost:3000,..."` | **Production Domain Only** | Environment variable |

---

## 4. Security Audit & Risk Classification

### `CRITICAL`
- **Missing DB Driver:** `psycopg2-binary` is missing from `backend/requirements.txt`, which prevents connecting to a PostgreSQL database.

### `HIGH`
- **Runtime Schema Generation:** `Base.metadata.create_all(bind=engine)` is called on application startup in `app/main.py`. In a multi-worker production server (e.g. Gunicorn with 4 workers), concurrent startup calls create database DDL lock contention and race conditions.
- **Permissive Development CORS:** Default `CORS_ALLOWED_ORIGINS` permits unencrypted `http://localhost:3000`. Production deployment must strictly restrict CORS to the single HTTPS production domain.

### `MEDIUM`
- **Lack of API Rate-Limiting:** Public endpoints (e.g., `POST /api/v1/session/start`) lack rate-limiting middleware, exposing the server to bot spam or denial-of-service.
- **Detailed Exception Tracebacks:** FastAPI default exception handlers expose internal stack traces during 500 errors if `debug=True` is accidentally enabled.

### `LOW`
- **Local SQLite File Persistence:** Local development environment writes to `backend/experiment.db`, which is vulnerable to lock contention under concurrent multi-user load.

### `INFORMATIONAL`
- **Zero PII Storage:** Codebase verification confirms zero PII (names, emails, payment details) is stored in the database. All tracking uses UUID v4 (`p_...`) and salted IP hashes (`ip_hash`).

---

## 5. Deployment Infrastructure Dependencies

### REQUIRED
- **Python 3.11+ Runtime:** For running the FastAPI backend API server.
- **Node.js 18+ / Vite Build Environment:** For compiling the React SPA into static assets.
- **PostgreSQL 14+ Database Instance:** Production relational storage.
- **`psycopg2-binary` Driver:** For SQLAlchemy PostgreSQL connectivity.
- **HTTPS Web Server / Reverse Proxy (Nginx / Caddy / Cloudflare):** For TLS 1.3 termination, HTTP-to-HTTPS redirection, and serving static frontend assets.
- **ASGI Process Manager (Gunicorn / Uvicorn):** Running `uvicorn app.main:app --workers 4`.
- **Paid Google Cloud Gemini API Key:** Billing-enabled `GEMINI_API_KEY` for LLM completions.

### RECOMMENDED
- **Automated Database Backups:** Daily PostgreSQL `pg_dump` snapshots with Point-In-Time Recovery (PITR).
- **Process Supervisor:** Systemd service unit or Docker container supervisor for automated restart on failure.

### OPTIONAL / UNNECESSARY (DO NOT INTRODUCE)
- *Kubernetes, Microservices, Redis, Celery / RabbitMQ, Kafka, GraphQL, Elasticsearch, Third-Party Analytics Trackers.*

---

## 6. Proposed Production Topology

```text
                               ┌────────────────────────────────────────────────────────┐
                               │                    Participant Browser                 │
                               └───────────────────────────┬────────────────────────────┘
                                                           │
                                                           │ HTTPS (TLS 1.3)
                                                           ▼
                               ┌────────────────────────────────────────────────────────┐
                               │          Nginx Reverse Proxy & Web Server              │
                               │          (TLS Termination & Static Asset Host)         │
                               └─────────────┬────────────────────────────┬─────────────┘
                                             │                            │
                            Static SPA Files │                            │ API Proxy (/api/v1/*)
                                             ▼                            ▼
                               ┌──────────────────────────┐  ┌──────────────────────────┐
                               │   React 18 Static Bundle │  │ FastAPI ASGI Server      │
                               │   (HTML / JS / CSS)      │  │ (Gunicorn / Uvicorn)     │
                               └──────────────────────────┘  └────────────┬─────────────┘
                                                                          │
                                                ┌─────────────────────────┴─────────────────────────┐
                                                │                                                   │
                                                ▼                                                   ▼
                               ┌──────────────────────────────────┐               ┌──────────────────────────────────┐
                               │ PostgreSQL Database              │               │ Google Gemini API                │
                               │ (Encrypted Storage at Rest)      │               │ (HTTPS REST API Endpoint)        │
                               └──────────────────────────────────┘               └──────────────────────────────────┘
```

---

## 7. Hosting Provider Criteria

The selection of a production cloud provider must satisfy the following technical criteria:
1. **Managed PostgreSQL Support:** Native PostgreSQL 14+ with automated patching and SSL/TLS enforced connections.
2. **Geographic Data Jurisdiction:** Ability to select server region (e.g. India `ap-south-1` Mumbai) if mandated by the ethics board.
3. **Encryption Standards:** Storage disk encryption at rest (AES-256) and TLS 1.3 in transit.
4. **Secrets Management:** Secure environment variable management for storing `GEMINI_API_KEY` and database connection strings.
5. **Cost Predictability:** Low-cost, transparent pricing model appropriate for academic research grant budgets.

---

## 8. Ordered Production Migration Plan

1. **Dependency Preparation:** Add `psycopg2-binary` to `backend/requirements.txt`.
2. **Migration Tooling Setup:** Generate initial Alembic migration scripts and remove runtime `Base.metadata.create_all` from `app/main.py`.
3. **Database Provisioning:** Provision PostgreSQL 14+ instance on selected cloud host and execute `alembic upgrade head`.
4. **Environment Population:** Populate production environment variables (`APP_ENV=production`, `USE_MOCK_LLM=false`, `LLM_PROVIDER=gemini`, `GEMINI_API_KEY`, `DATABASE_URL`, `CORS_ALLOWED_ORIGINS`).
5. **Backend Deployment:** Deploy FastAPI backend using Gunicorn with 4 Uvicorn ASGI workers behind Nginx.
6. **Frontend Deployment:** Compile React SPA (`npm run build`) and deploy static bundle to Nginx / static web host.
7. **Smoke Verification:** Execute real API smoke test and complete automated test suite (`pytest tests`).
8. **Final Production Freeze:** Lock configuration and establish production readiness.

---

## 9. Production Blockers Register

| Issue Description | Severity | Required Action | Blocks Deployment? |
| :--- | :--- | :--- | :--- |
| **Missing PostgreSQL Driver** | `CRITICAL` | Add `psycopg2-binary` to `backend/requirements.txt`. | **YES** |
| **Unprovisioned PostgreSQL DB** | `CRITICAL` | Provision managed PostgreSQL database instance. | **YES** |
| **Unpopulated Secrets (`GEMINI_API_KEY`)** | `CRITICAL` | Store paid Gemini API key in production secrets manager. | **YES** |
| **Development CORS Configuration** | `HIGH` | Update `CORS_ALLOWED_ORIGINS` to production domain only. | **YES** |
| **Runtime DDL Table Creation** | `HIGH` | Replace `Base.metadata.create_all` in `main.py` with Alembic migrations. | **YES** |
| **Unconfigured Process Supervisor** | `MEDIUM` | Configure Gunicorn/Uvicorn systemd unit or container process manager. | **YES** |

---

## 10. Test Suite Result

- **Command:** `pytest tests`
- **Result:** `30 passed in 1.90s` (100% pass rate).
