# Production Hosting Architecture Decision Document
**Study Title:** English-Hindi AI-Mediated Information Seeking Experiment  
**Protocol Version:** `1.1.0-gemini-frozen`  
**Milestone:** Productionization Milestone 3 — Production Hosting Architecture  
**Date:** September 28, 2026  
**Final Decision:** `LOCAL / SELF-HOSTED`

---

## Executive Summary

The principal researcher has formally decided **NOT to use public cloud hosting infrastructure** (AWS, GCP, Azure, Firebase, Render, Vercel, or DigitalOcean). 

The experimental application supporting Protocol v1.1.0 (`gemini-3.5-flash` / `3.5-flash-05-2026`) is converted to a reproducible **LOCAL / SELF-HOSTED research deployment server**. The **ONLY** external network service required by the application is the Google Gemini API over HTTPS.

---

## 1. Target Local Architecture

```
Participant Browser (Local Machine / Laboratory Setup)
    │
    │ 1. Local HTTP (http://localhost:3000)
    ▼
React / Vite Frontend Server (Static Single Page Application)
    │
    │ 2. Local HTTP REST API Requests (http://localhost:8000/api/v1/...)
    ▼
FastAPI Application Backend (Python 3.13 / Uvicorn Server on 127.0.0.1:8000)
    │
    ├─────────────────────────────────────────┐
    │ 3. Local TCP Connection (Port 5432)     │ 4. External HTTPS (TLS 1.3)
    ▼                                         ▼
Local PostgreSQL Database Server          Google Gemini API Gateway
(ai_info_inequality_db on 127.0.0.1:5432) (generativelanguage.googleapis.com)
```

---

## 2. Removal of Cloud Deployment Assumptions

All former assumptions requiring cloud infrastructure have been formally removed from the deployment pipeline:

- **Cloud Run / App Runner / Container Apps**: Replaced by local Uvicorn process managed directly on the research server.
- **Firebase / S3 / CloudFront**: Replaced by local Vite preview/development web server.
- **Managed Cloud PostgreSQL (Cloud SQL / RDS)**: Replaced by local PostgreSQL 14+ engine.
- **Cloud Secret Managers**: Replaced by local `.env` environment configuration protected by `.gitignore`.
- **Cloud Load Balancers & DNS**: Replaced by loopback binding (`localhost` / `127.0.0.1`).

---

## 3. Deployment Summary & Reference Documents

1. **Local Runbook**: Detailed step-by-step setup, database creation, backup, and startup instructions are documented in [`docs/engineering/local_deployment_runbook.md`](file:///c:/Antigravity%20Projects/AI-mediated%20information%20inequality%20across%20languages/ai-info-inequality-exp/docs/engineering/local_deployment_runbook.md).
2. **Technical Audit**: Complete empirical verification of local components is recorded in [`docs/engineering/local_deployment_audit.md`](file:///c:/Antigravity%20Projects/AI-mediated%20information%20inequality%20across%20languages/ai-info-inequality-exp/docs/engineering/local_deployment_audit.md).
3. **Automated Launcher**: Reproducible pre-flight checks and launch commands are automated in [`start_local_research.ps1`](file:///c:/Antigravity%20Projects/AI-mediated%20information%20inequality%20across%20languages/ai-info-inequality-exp/start_local_research.ps1).

---

## 4. Final Status Statement

`LOCAL / SELF-HOSTED`
