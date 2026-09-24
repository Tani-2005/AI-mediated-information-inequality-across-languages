# Linguistic Inequality in AI-Mediated Information Seeking: Experimental Application

This repository contains the frozen experimental web application for the randomized controlled trial investigating linguistic inequality, verification behavior, and decision quality in English vs. Hindi AI-mediated information seeking across civic entitlement scenarios (PMEGP, PM-Vishwakarma, PM-SVANidhi).

---

## 📌 Repository Architecture

```text
ai-info-inequality-exp/
├── frontend/                     # React + Vite + TypeScript + Tailwind CSS SPA
├── backend/                      # FastAPI Python 3.11+ Backend & Scorer
├── data/                         # Ground-truth scenario matrices & rubrics
├── tests/                        # Pytest suite (Randomization, Scoring, Security, API)
├── docs/                         # Pre-registration & technical documentation
├── experiment_config.json        # Frozen experiment manifest
└── README.md
```

---

## ⚡ Quick Start (Local Development Mode)

### 1. Backend Setup
```bash
cd backend
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
alembic upgrade head
pytest
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

The application runs in **Development Mock Mode** (`USE_MOCK_LLM=true`) by default, returning deterministic mock LLM responses without consuming OpenAI API credits.

---

## 🔒 Security & Privacy Protocol
- Participant IDs are pseudonymous UUIDs.
- No personal names or government identifiers are collected or stored.
- Ground-truth scoring matrices exist strictly server-side.
- Payment compensation is handled via an unlinked third-party system.

---

## 📜 Pre-Registration Manifest
- Protocol Version: `1.0.0-frozen`
- Planned LMM: `DecisionQuality ~ Language + Scenario + Position + (1|Participant)`
- Primary Contrast: English vs. Hindi ($C_1: \mu_{\text{English}} - \mu_{\text{Hindi}} \neq 0$)
- Target Analyzable $N = 144$ ($48$ per arm)
