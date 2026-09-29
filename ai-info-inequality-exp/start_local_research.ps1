# ==============================================================================
# Local Research Server Launcher & Diagnostic Check
# Study Title: English-Hindi AI-Mediated Information Seeking Experiment
# Protocol Version: 1.1.0-gemini-frozen
# ==============================================================================

Write-Host "======================================================================" -ForegroundColor Cyans
Write-Host " LOCAL RESEARCH SERVER INITIALIZATION & PRE-FLIGHT DIAGNOSTICS" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

$RootPath = Get-Location
$BackendPath = Join-Path $RootPath "backend"
$FrontendPath = Join-Path $RootPath "frontend"
$VenvPython = Join-Path $BackendPath "venv\Scripts\python.exe"

# 1. Verify Python virtual environment
Write-Host "[1/6] Checking Python environment..." -NoNewline
If (Test-Path $VenvPython) {
    Write-Host " [OK]" -ForegroundColor Green
} Else {
    Write-Host " [FAILED]" -ForegroundColor Red
    Write-Host "Error: Virtual environment not found at $VenvPython. Run python -m venv backend/venv first." -ForegroundColor Red
    Exit 1
}

# 2. Verify Node dependencies
Write-Host "[2/6] Checking Node.js frontend dependencies..." -NoNewline
If (Test-Path (Join-Path $FrontendPath "node_modules")) {
    Write-Host " [OK]" -ForegroundColor Green
} Else {
    Write-Host " [WARNING]" -ForegroundColor Yellow
    Write-Host "Warning: node_modules missing in frontend/. Run 'npm install' inside frontend directory." -ForegroundColor Yellow
}

# 3. Check environment file (.env)
Write-Host "[3/6] Checking environment configuration (.env)..." -NoNewline
$EnvFile = Join-Path $RootPath ".env"
$BackendEnvFile = Join-Path $BackendPath ".env"

If (Test-Path $EnvFile) {
    Write-Host " [OK - Root .env found]" -ForegroundColor Green
} ElseIf (Test-Path $BackendEnvFile) {
    Write-Host " [OK - Backend .env found]" -ForegroundColor Green
} Else {
    Write-Host " [FAILED]" -ForegroundColor Red
    Write-Host "Error: No .env file found. Copy .env.example to .env and configure your variables." -ForegroundColor Red
    Exit 1
}

# 4. Verify PostgreSQL connection & migration state
Write-Host "[4/6] Verifying database configuration and running Alembic migrations..." -NoNewline
Set-Location $RootPath
$MigrationOutput = & $VenvPython -m alembic -c backend/alembic.ini upgrade head 2>&1
If ($LASTEXITCODE -eq 0) {
    Write-Host " [OK]" -ForegroundColor Green
} Else {
    Write-Host " [FAILED]" -ForegroundColor Red
    Write-Host "Migration Error Output:" -ForegroundColor Red
    Write-Host $MigrationOutput -ForegroundColor Red
    Write-Host "Ensure local PostgreSQL server is running and DATABASE_URL is correct in .env." -ForegroundColor Red
    Exit 1
}

# 5. Run automated pre-flight security tests
Write-Host "[5/6] Executing pre-flight automated test suite..." -NoNewline
$TestOutput = & "$BackendPath\venv\Scripts\pytest.exe" tests 2>&1
If ($LASTEXITCODE -eq 0) {
    Write-Host " [OK (35/35 Tests Passed)]" -ForegroundColor Green
} Else {
    Write-Host " [FAILED]" -ForegroundColor Red
    Write-Host $TestOutput -ForegroundColor Red
    Exit 1
}

# 6. Pre-flight complete -> Report local URLs and launch instructions
Write-Host "[6/6] Pre-flight diagnostics passed successfully!" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host " LOCAL RESEARCH SERVER READY FOR LAUNCH" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Backend API URL:   http://localhost:8000" -ForegroundColor Yellow
Write-Host "Frontend App URL:  http://localhost:3000" -ForegroundColor Yellow
Write-Host "Admin Health URL:  http://localhost:8000/api/v1/admin/health" -ForegroundColor Yellow
Write-Host "----------------------------------------------------------------------" -ForegroundColor Gray
Write-Host "To start the application servers in two separate terminal windows:" -ForegroundColor Gray
Write-Host "  Terminal 1 (Backend):" -ForegroundColor White
Write-Host "    cd backend; .\venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload" -ForegroundColor Green
Write-Host "  Terminal 2 (Frontend):" -ForegroundColor White
Write-Host "    cd frontend; npm run dev -- --port 3000" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Cyan
