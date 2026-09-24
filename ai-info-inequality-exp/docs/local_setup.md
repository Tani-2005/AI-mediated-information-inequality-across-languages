# Local Setup Guide

## Requirements
- Python 3.11+
- Node.js v20+ & npm

## Backend Execution
```bash
cd backend
venv\Scripts\activate  # Windows
# source venv/bin/activate # Linux/Mac

pytest ..\tests        # Run full backend test suite
uvicorn app.main:app --reload --port 8000
```

## Frontend Execution
```bash
cd frontend
npm install
npm run dev -- --port 3000
```
Access the application at `http://localhost:3000`.
