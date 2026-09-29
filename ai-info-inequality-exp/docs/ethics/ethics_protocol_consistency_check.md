# Ethics Package vs. Protocol v1.1.0 Consistency Verification Audit

**Audit Date:** 2026-09-27  
**Protocol Version:** `1.1.0-gemini-frozen`  
**Ethics Package Directory:** `docs/ethics/`  
**Target Reference Document:** [`docs/protocol_v1.1.0.md`](file:///c:/Antigravity%20Projects/AI-mediated%20information%20inequality%20across%20languages/ai-info-inequality-exp/docs/protocol_v1.1.0.md)  

---

## 1. Parameter Consistency Verification Matrix

| Parameter / Dimension | Frozen Protocol v1.1.0 Value | Ethics Package Documents Value | Audit Result | Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Protocol Version** | `1.1.0-gemini-frozen` | `1.1.0-gemini-frozen` | **100% PARITY** | Consistent across all 10 documents |
| **Study Title** | *Linguistic Inequality in AI-Mediated Information Seeking: An English-Hindi Randomized Controlled Trial* | *Linguistic Inequality in AI-Mediated Information Seeking: An English-Hindi Randomized Controlled Trial* | **100% PARITY** | Exact title match |
| **Target Population** | English-Hindi bilingual Indian adults aged 18–65 residing in India | English-Hindi bilingual Indian adults aged 18–65 residing in India | **100% PARITY** | Exact population match |
| **Analyzable Sample ($N$)** | $N = 144$ (48 per arm) | $N = 144$ (48 per arm) | **100% PARITY** | Exact sample match |
| **Recruitment Target ($N$)** | $N = 171$ (15% attrition) | $N = 171$ (15% attrition) | **100% PARITY** | Exact recruitment target match |
| **Experimental Arms (3)** | `ENGLISH_ONLY`, `HINDI_ONLY`, `CODE_SWITCHING` | `ENGLISH_ONLY`, `HINDI_ONLY`, `CODE_SWITCHING` | **100% PARITY** | Exact 3 arms match |
| **Civic Tasks (3)** | PMEGP, PM Vishwakarma, PM SVANidhi | PMEGP, PM Vishwakarma, PM SVANidhi | **100% PARITY** | Exact 3 task scenarios match |
| **Counterbalancing** | $3 \times 3$ Latin-Square ordering | $3 \times 3$ Latin-Square ordering | **100% PARITY** | Order counterbalancing match |
| **Production LLM Provider** | Google Gemini API (`generativelanguage.googleapis.com`) | Google Gemini API (`generativelanguage.googleapis.com`) | **100% PARITY** | Exact provider match |
| **Model Identifier** | `gemini-3.5-flash` | `gemini-3.5-flash` | **100% PARITY** | Exact model identifier match |
| **Model Version Tag** | `3.5-flash-05-2026` | `3.5-flash-05-2026` | **100% PARITY** | Exact model version match |
| **System Prompt Version** | `v1.1.0-gemini-frozen` | `v1.1.0-gemini-frozen` | **100% PARITY** | Prompt version match |
| **Primary Outcome** | Continuous Decision Quality Score (0.0 to 10.0) | Continuous Decision Quality Score (0.0 to 10.0) | **100% PARITY** | Primary outcome match |
| **Secondary Outcomes** | `DocClicks` (counts), `DocDuration` (seconds) | `DocClicks` (counts), `DocDuration` (seconds) | **100% PARITY** | Secondary outcomes match |
| **Exploratory Process Var** | `WindowBlur` (off-screen focus dwell time; NOT web search) | `WindowBlur` (off-screen focus dwell time; NOT web search) | **100% PARITY** | Telemetry classification match |
| **Scoring Engine** | Deterministic engine (`backend/app/scoring/engine.py`), zero LLM-as-judge | Deterministic engine (`backend/app/scoring/engine.py`), zero LLM-as-judge | **100% PARITY** | Ground-truth scoring match |
| **Randomization Engine** | Server-side stratified block allocation (AILS median split = 36) | Server-side stratified block allocation (AILS median split = 36) | **100% PARITY** | Randomization engine match |
| **Primary Model (LMM)** | `DecisionQuality ~ Language + Scenario + Position + (1|Participant)` | `DecisionQuality ~ Language + Scenario + Position + (1|Participant)` | **100% PARITY** | LMM statistical formula match |
| **Approval Status** | `PENDING` (Human recruitment NOT authorized) | `PENDING` (Human recruitment NOT authorized) | **100% PARITY** | Approval status match |

---

## 2. Discrepancy Summary
- **Total Discrepancies Identified:** **0**
- **Protocol Modifications Made:** **0** (Protocol v1.1.0 remained strictly untouched).
- **Audit Conclusion:** The Human-Participant Ethics Application Package (`docs/ethics/`) is in 100% perfect structural, technical, and methodological alignment with frozen `Protocol v1.1.0`.
