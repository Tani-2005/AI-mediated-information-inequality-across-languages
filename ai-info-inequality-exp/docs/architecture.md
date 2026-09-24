# Architecture Overview

This document details the software architecture for the English-Hindi AI-Mediated Information Seeking RCT application.

## Key Modules
1. **Frontend SPA**: React 18, Vite, TypeScript, Tailwind CSS. Implements screens S1 to S10.
2. **Backend API**: FastAPI (Python 3.11+). Handles session control, screening pass/fail, server-side block randomization, deterministic ground-truth scoring, and telemetry logging.
3. **LLM Proxy Stub**: `POST /api/v1/chat/message` operates as a zero-cost development mock stub. Zero OpenAI credits are consumed in development mode.
4. **Database**: SQLite for local development (`backend/experiment.db`), PostgreSQL-compatible schema for production.
