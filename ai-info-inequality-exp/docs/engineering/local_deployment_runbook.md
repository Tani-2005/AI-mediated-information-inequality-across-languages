# Local Research Deployment Runbook
**Study Title:** English-Hindi AI-Mediated Information Seeking Experiment  
**Protocol Version:** `1.1.0-gemini-frozen`  
**Deployment Model:** Local / Self-Hosted Research Server  
**Date:** September 28, 2026  
**Status:** `LOCAL DEPLOYMENT READY`

---

## 1. Prerequisites

Before setting up the local research server, verify that the host machine satisfies the following software dependencies:

- **Operating System**: Windows 10/11, macOS, or Linux.
- **Python**: Python 3.11+ (Python 3.13 recommended).
- **Node.js**: Node 18.x or 20.x LTS with `npm`.
- **PostgreSQL**: Local PostgreSQL 14, 15, or 16 server installation.
- **Git**: Git SCM.
- **Internet Access**: HTTPS outgoing connection to `generativelanguage.googleapis.com` for Gemini API calls.

---

## 2. PostgreSQL Setup

1. **Verify Local PostgreSQL Service**:
   Ensure the local PostgreSQL service is running on default port `5432`:
   ```powershell
   # Windows PowerShell test
   Get-Service -Name "postgresql*"
   ```

2. **Create Dedicated Database & User**:
   Open a PostgreSQL shell (`psql`) as administrator (`postgres` superuser):
   ```sql
   -- Create dedicated database user
   CREATE USER exp_user WITH PASSWORD 'YOUR_STRONG_LOCAL_DB_PASSWORD';

   -- Create research database
   CREATE DATABASE ai_info_inequality_db OWNER exp_user;

   -- Grant permissions
   GRANT ALL PRIVILEGES ON DATABASE ai_info_inequality_db TO exp_user;
   ```

3. **Formulate Connection String**:
   ```
   postgresql://exp_user:YOUR_STRONG_LOCAL_DB_PASSWORD@localhost:5432/ai_info_inequality_db
   ```

---

## 3. Environment Configuration

1. **Copy Template File**:
   Copy `.env.example` to create `.env` in the root workspace directory:
   ```powershell
   Copy-Item .env.example .env
   ```

2. **Configure Local Research Variables in `.env`**:
   ```env
   # Application Environment
   APP_ENV=production

   # Local PostgreSQL Database URL
   DATABASE_URL=postgresql://exp_user:YOUR_STRONG_LOCAL_DB_PASSWORD@localhost:5432/ai_info_inequality_db

   # Gemini API Credentials (FROZEN MODEL: gemini-3.5-flash)
   LLM_PROVIDER=gemini
   GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai
   GEMINI_MODEL=gemini-3.5-flash
   GEMINI_API_KEY=AIzaSy...YOUR_ACTUAL_GEMINI_API_KEY

   # Research Data Collection Switches (MUST DISABLE MOCK MODE)
   USE_MOCK_LLM=false
   LLM_ENABLED=true
   IS_PILOT_MODE=false
   MAX_SESSION_COUNT=200
   MAX_API_CALLS_PER_SESSION=30

   # Security & Administrative Credentials
   CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
   RATE_LIMIT_ENABLED=true
   RATE_LIMIT_PER_MINUTE=10
   ADMIN_API_KEY=YOUR_STRONG_LOCAL_64_CHAR_ADMIN_KEY
   ```

---

## 4. Database Migration Procedure

1. **Activate Python Virtual Environment**:
   ```powershell
   .\backend\venv\Scripts\Activate.ps1
   ```

2. **Execute Alembic Migrations**:
   Do **NOT** use `Base.metadata.create_all()`. Apply schema migrations exclusively via Alembic:
   ```powershell
   python -m alembic -c backend/alembic.ini upgrade head
   ```

3. **Verify Created Schema**:
   Connect to PostgreSQL and verify that all 7 core tables are present:
   ```sql
   \c ai_info_inequality_db
   \dt
   -- Tables: alembic_version, debrief_records, messages, participants, post_task_responses, randomizations, task_sessions, telemetry_events
   ```

---

## 5. Application Startup Sequence

### Automated Pre-Flight Check (Launcher Script)
Run the PowerShell pre-flight diagnostic launcher:
```powershell
.\start_local_research.ps1
```

### Manual Two-Terminal Startup Procedure

#### Terminal 1: FastAPI Backend Application
```powershell
cd backend
.\venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```
*Backend Root Verification:* Open browser to `http://localhost:8000/`. Expected response:
`{"status":"RUNNING","study_id":"ENGLISH_HINDI_AI_INFO_INEQUALITY_2026","protocol_version":"1.1.0-gemini-frozen","mode":"PRODUCTION"}`

#### Terminal 2: React Frontend SPA
```powershell
cd frontend
npm run dev -- --port 3000
```
*Frontend User Interface:* Open browser to `http://localhost:3000/`.

---

## 6. Gemini API Gateway Verification

Test active communication with Google Gemini API:

```powershell
# Send test request via curl / PowerShell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/session/create" -Method Post -ContentType "application/json" -Body '{"is_pilot": false}'
```

Verify that Gemini API responses complete cleanly during active chat messages and that no raw API credentials appear in logs or client-side web tools.

---

## 7. Administrative Endpoint Access

Test administrative endpoints using the configured `ADMIN_API_KEY`:

```powershell
# Test Admin Health Check
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/admin/health" -Headers @{"X-Admin-API-Key"="YOUR_STRONG_LOCAL_64_CHAR_ADMIN_KEY"}
```
Expected Output:
```json
{
  "status": "HEALTHY",
  "app_env": "production",
  "llm_enabled": true,
  "use_mock_llm": false,
  "stats": {
    "total_participants": 1,
    "total_task_sessions": 0
  }
}
```

---

## 8. Database Backup & Recovery Procedure

### Backup Creation (End of Session / Daily)
To create a complete local binary backup of the PostgreSQL database:
```powershell
# Create timestamped local backup file
$BackupFile = "backup_ai_info_inequality_" + (Get-Date -Format "yyyyMMdd_HHmmss") + ".dump"
pg_dump -h localhost -U exp_user -d ai_info_inequality_db -F c -b -v -f $BackupFile
```

### Backup Verification
Verify the backup file exists and has non-zero size (> 10 KB).

### Database Restore Procedure (Disaster Recovery)
```powershell
# Drop and recreate empty database
psql -h localhost -U postgres -c "DROP DATABASE ai_info_inequality_db;"
psql -h localhost -U postgres -c "CREATE DATABASE ai_info_inequality_db OWNER exp_user;"

# Restore database from dump
pg_restore -h localhost -U exp_user -d ai_info_inequality_db -v $BackupFile
```

---

## 9. Safe System Shutdown

To stop the local research server:
1. In **Terminal 1** (Backend): Press `CTRL + C` to stop Uvicorn.
2. In **Terminal 2** (Frontend): Press `CTRL + C` to stop Vite.
3. Verify no lingering background Python processes remain on port 8000.

---

## 10. Troubleshooting Guide

| Issue | Root Cause | Solution |
|---|---|---|
| `ValueError: USE_MOCK_LLM=True is prohibited in production` | `USE_MOCK_LLM=true` in `.env` while `APP_ENV=production` | Change `USE_MOCK_LLM=false` in `.env`. |
| `ValueError: GEMINI_API_KEY is not configured` | Empty `GEMINI_API_KEY` in `.env` | Add valid Gemini API key to `.env`. |
| `psycopg2.OperationalError: connection to server at "localhost"` | Local PostgreSQL service stopped or invalid credentials | Start PostgreSQL service; verify password in `DATABASE_URL`. |
| `401 Unauthorized` on `/api/v1/admin/*` | Missing or mismatched `X-Admin-API-Key` | Provide exact `ADMIN_API_KEY` value in HTTP header. |
| `429 Too Many Requests` on `/session/create` | Exceeded 10 requests/minute rate limit | Wait 60 seconds or adjust `RATE_LIMIT_PER_MINUTE` in `.env`. |
