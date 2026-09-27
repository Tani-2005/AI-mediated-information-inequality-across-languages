# Protocol v1.1.0: English-Hindi AI-Mediated Information Seeking Experiment

**Protocol Version:** `1.1.0-gemini-frozen`  
**Study Identifier:** `ENGLISH_HINDI_AI_INFO_INEQUALITY_2026`  
**Status:** DRAFT COMPLETE — PENDING FINAL HUMAN REVIEW & ETHICS APPROVAL  
**Production LLM Provider:** Google Gemini API (`generativelanguage.googleapis.com`)  
**Model Identifier:** `gemini-3.5-flash`  
**Model Version Tag:** `3.5-flash-05-2026`  

---

## 1. Study Overview

### 1.1 Study Title
*Linguistic Inequality in AI-Mediated Information Seeking: An English-Hindi Randomized Controlled Trial*

### 1.2 Protocol Version
`1.1.0-gemini-frozen` (Supersedes Protocol `1.0.0-frozen` following production provider transition to Google Gemini API).

### 1.3 Study Purpose
The objective of this study is to systematically evaluate how linguistic disparities between English, Hindi, and Code-Switching (Hinglish) impact decision quality, task efficiency, verification behavior, and cognitive workload when bilingual Indian citizens interact with modern Large Language Model (LLM) search/civic entitlement assistants.

### 1.4 Phenomenon Investigated
The study investigates **AI-mediated information inequality across languages**—specifically whether interacting in a non-English / Indic language (Hindi) or code-switching with an AI assistant introduces structural information asymmetry, higher error rates, or reduced decision quality when evaluating complex government entitlement rules compared to interacting in English.

### 1.5 Distinction from LLM Benchmarking
This study is a **human-subject Randomized Controlled Trial (RCT)**. Unlike automated NLP benchmarks (e.g., MMLU, IndicGenBench, BHRAM-IL) that assess standalone LLM generation quality or hallucination rates in isolation, this study measures human-AI interaction outcomes: human decision quality, document verification clicks, task completion times, prompting patterns, and subjective workload when human participants use an AI assistant as an information tool.

---

## 2. Research Problem and Theoretical Framework

### 2.1 Theoretical Framing
The study is grounded in Cognitive Load Theory, Information Seeking Behavior frameworks, and Digital Inequality theories. It evaluates the following operational causal chain:

$$\text{LANGUAGE CONDITION} \longrightarrow \text{VERIFICATION / PROMPTING / RELIANCE} \longrightarrow \text{CIVIC DECISION QUALITY}$$

1. **Language Condition:** The enforced communication language of the AI assistant (`ENGLISH_ONLY`, `HINDI_ONLY`, `CODE_SWITCHING`).
2. **Mediating Process Behaviors:** User verification clicks (`DocClicks`), verification duration (`DocDuration`), prompting frequency, and automation reliance.
3. **Information-Seeking Task Outcome:** Final civic decision quality score (0.0 to 10.0) calculated against deterministic ground-truth rules.

---

## 3. Research Questions

### 3.1 Primary Research Question
- **RQ1:** Does interaction language (`ENGLISH_ONLY` vs. `HINDI_ONLY` vs. `CODE_SWITCHING`) significantly affect final Decision Quality Scores when bilingual Indian citizens use an AI assistant to evaluate complex civic entitlement scenarios?

### 3.2 Secondary Research Questions
- **RQ2:** Does a Code-Switching AI interaction condition (`CODE_SWITCHING`) significantly mitigate decision quality disparities relative to a single-language Hindi condition (`HINDI_ONLY`)?
- **RQ3:** To what extent does baseline AI literacy (measured via AILS) moderate the relationship between interaction language condition and final decision quality?

### 3.3 Historical Note on Superseded Formulations
Earlier exploratory drafts included preliminary questions assessing automated model accuracy in isolation. Protocol `1.0.0-frozen` and `1.1.0-gemini-frozen` formally supersede all preliminary formulations by anchoring strictly on human decision quality in an RCT design.

---

## 4. Hypotheses

### 4.1 H1: Language Disadvantage
Participants assigned to the `ENGLISH_ONLY` arm will achieve significantly higher Decision Quality Scores than participants assigned to the `HINDI_ONLY` arm:
$$\mu_{\text{English}} - \mu_{\text{Hindi}} > 0$$

### 4.2 H2: Code-Switching Mitigation
Participants assigned to the `CODE_SWITCHING` arm will achieve significantly higher Decision Quality Scores than participants assigned to the `HINDI_ONLY` arm:
$$\mu_{\text{CodeSwitching}} - \mu_{\text{Hindi}} > 0$$

### 4.3 H3: AI-Literacy Moderation
Baseline AI Literacy (AILS total score) will significantly moderate the effect of language condition on Decision Quality, such that higher AI literacy attenuates the decision quality gap between English and Hindi interactions.

---

## 5. Study Design

### 5.1 Factorial Structure
The study utilizes a **3 Between-Subjects Arms $\times$ 3 Within-Subjects Repeated Tasks** mixed experimental design:
- **Between-Subjects Factor:** Experimental Language Arm (`ENGLISH_ONLY`, `HINDI_ONLY`, `CODE_SWITCHING`).
- **Within-Subjects Factor:** Civic Entitlement Task Scenario (`PMEGP`, `PM_VISHWAKARMA`, `PM_SVANIDHI`).

### 5.2 Sample Targets
- **Analyzable Sample Size ($N$):** $N = 144$ participants (48 participants per arm).
- **Recruitment Target ($N$):** $N = 171$ participants (incorporating a 15% planned attrition/dropout allowance).
- **Total Task Sessions Analyzed:** $144 \times 3 = 432$ task sessions.

### 5.3 Task Order Counterbalancing
To control for order and fatigue effects, task presentation order is counterbalanced across positions 1, 2, and 3 using a $3 \times 3$ Latin-Square design (`ORDER_1`, `ORDER_2`, `ORDER_3`).

---

## 6. Experimental Conditions

### 6.1 `ENGLISH_ONLY`
- **Constraint:** System prompt strictly enforces exclusive communication in English.
- **Behavior:** The AI assistant responds solely in English regardless of user query formatting.

### 6.2 `HINDI_ONLY`
- **Constraint:** System prompt strictly enforces exclusive communication in Hindi (Devanagari script).
- **Behavior:** The AI assistant responds solely in Hindi (Devanagari script).

### 6.3 `CODE_SWITCHING`
- **Constraint:** System prompt permits fluid communication in English, Hindi (Devanagari script), or Romanized Hindi/Hinglish.
- **Behavior:** The AI assistant adapts naturally to user language patterns and code-switching.

---

## 7. Participants

### 7.1 Target Population
Bilingual English-Hindi Indian adults aged 18–65 residing in India.

### 7.2 Eligibility Criteria
1. Age 18–65 years old.
2. Resident of India.
3. Self-reported basic digital literacy (ability to navigate web applications).
4. **Bilingual Comprehension Screening:** Must pass both English ($\ge 2/3$) and Hindi ($\ge 2/3$) reading comprehension passage sub-tests.

### 7.3 Exclusion Criteria
1. AI/NLP researchers, AI software developers, or professional prompt engineers.
2. Failure to pass bilingual comprehension screening.
3. Failure to complete all 3 task sessions.

### 7.4 Baseline Instruments
- **LEAP-Q:** Language Experience and Proficiency Questionnaire (Age of Acquisition, primary home language, medium of instruction, daily usage %, self-rated 1-10 proficiencies).
- **AILS:** 12-item AI Literacy Scale (5-point Likert items, score range 12–60; median split threshold = 36).

### 7.5 Sampling Method & Non-Representative Statement
Convenience and purposive sampling via online Indian panels. The sample is acknowledged as non-representative of the entire Indian population; results generalize specifically to bilingual digital citizens.

### 7.6 Participant Replacement Rule
Participants who drop out or disconnect before completing all 3 task sessions are classified as `INCOMPLETE` and replaced sequentially until $N = 144$ complete sessions are attained.

---

## 8. Sample Size and Power

### 8.1 Planning Assumptions
- **Analyzable $N$:** 144 (48 per arm).
- **Recruitment $N$:** 171 (15% planning attrition).
- **Planning Effect Size ($d$):** $d = 0.40$ (Cohen's $d$, non-empirical planning prior).
- **Intraclass Correlation ($\text{ICC} / \rho$):** $\rho = 0.20$ (planning assumption for within-subject task cluster correlation).
- **Significance Level ($\alpha$):** $\alpha = 0.05$ (two-tailed).

### 8.2 Power Basis
Power calculations indicate that $N = 144$ participants completing 3 tasks each ($N = 432$ total observations) provides $>80\%$ power to detect $d = 0.40$ for the primary orthogonal contrast $C_1: \mu_{\text{English}} - \mu_{\text{Hindi}} \neq 0$ under a Linear Mixed-Effects Model.

---

## 9. Experimental Tasks

The study evaluates 3 real-world Indian government entitlement schemes:

### 9.1 PMEGP (Prime Minister Employment Generation Programme)
- **Domain:** Micro-Manufacturing Enterprise Entitlement.
- **Core Rules:** Maximum project cost Rs. 50 Lakhs; Rural special category subsidy 35%; mandatory documents (Aadhaar, Project Report, EDP Certificate).
- **Official Ground Truth Source:** Ministry of MSME, Government of India.

### 9.2 PM Vishwakarma
- **Domain:** Artisan Credit & Skill Grant Entitlement.
- **Core Rules:** Tranche 1 loan Rs. 1,00,000 at 5% interest; skill training stipend Rs. 500/day; modern toolkit voucher Rs. 15,000.
- **Official Ground Truth Source:** Ministry of MSME, Government of India.

### 9.3 PM SVANidhi
- **Domain:** Street Vendor Micro-Credit Entitlement.
- **Core Rules:** 1st tranche loan Rs. 10,000; interest subsidy 7% per annum; maximum annual digital cashback Rs. 1,200.
- **Official Ground Truth Source:** Ministry of Housing and Urban Affairs (MoHUA), Government of India.

### 9.4 Operational Scoring Source
Scoring is executed 100% deterministically by `backend/app/scoring/engine.py` using JSON ground-truth rubrics stored in `data/ground_truth/`. Zero LLM-as-judge is used.

---

## 10. Experimental Procedure

The participant workflow follows a 12-stage sequential pipeline:

$$\text{Consent (S1)} \rightarrow \text{Screening (S2)} \rightarrow \text{LEAP-Q (S3)} \rightarrow \text{AILS (S4)} \rightarrow \text{Randomization (S5)} \rightarrow \text{Onboarding (S6)}$$
$$\rightarrow \text{Task 1 (S7)} \rightarrow \text{Post-Task 1 (S8)} \rightarrow \text{Task 2 (S7)} \rightarrow \text{Post-Task 2 (S8)} \rightarrow \text{Task 3 (S7)} \rightarrow \text{Post-Task 3 (S8)} \rightarrow \text{Debrief (S10)}$$

- **Implementation Parity:** Confirmed against React SPA router (`frontend/src/App.tsx`) and FastAPI API endpoints (`/consent`, `/screening`, `/language-bg`, `/ai-literacy`, `/randomize`, `/task`, `/telemetry`, `/post-task`).

---

## 11. Randomization and Counterbalancing

### 11.1 Allocation Ratio
1:1:1 allocation across `ENGLISH_ONLY`, `HINDI_ONLY`, and `CODE_SWITCHING`.

### 11.2 Stratification
Stratified on baseline AILS total score:
- `LOW` AILS: Total score $< 36$
- `HIGH` AILS: Total score $\ge 36$

### 11.3 Permuted Block Allocation
Randomized block sizes of 3 and 6 implemented via backend `RandomizationEngine`.

### 11.4 Allocation Concealment
100% backend server-side allocation. Block sequences and upcoming arm assignments are never exposed to the frontend client.

### 11.5 Task Counterbalancing
$3 \times 3$ Latin Square task ordering across positions 1, 2, and 3. Position is included as a fixed effect covariate in the LMM.

---

## 12. Measures and Variables

### 12.1 Variable Dictionary

| Variable | Type | Scale | Role | Measurement | Data Source |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `DecisionQuality` | Continuous | 0.0 – 10.0 | **Primary Outcome** | Deterministic Ground-Truth Rubric Match | `final_decisions` table |
| `DocClicks` | Discrete Count | $0 - \infty$ | **Secondary Outcome** | Direct interface verification document click count | `telemetry_events` table |
| `DocDuration` | Continuous (s) | $0 - \infty$ | **Secondary Outcome** | Total document inspection duration (seconds) | `telemetry_events` table |
| `TaskCompletionTime` | Continuous (s) | $0 - \infty$ | **Process Variable** | Elapsed time from task start to decision submit | `task_sessions` table |
| `NASA_TLX_Composite` | Continuous | 1 – 20 | **Exploratory Outcome** | 6-item Raw NASA-TLX Subjective Workload Scale | `post_task_measures` table |
| `DecisionConfidence` | Discrete Likert | 1 – 7 | **Exploratory Outcome** | Self-reported post-task confidence score | `final_decisions` table |
| `PromptCount` | Discrete Count | $1 - \infty$ | **Process Variable** | Total user prompt turns submitted per task | `messages` table |
| `AutomationBiasIndicator` | Binary | 0 / 1 | **Exploratory Outcome** | Acceptance of incorrect AI statements without verification | `final_decisions` + `telemetry` |
| `WindowBlur` | Discrete Count / Dwell (ms) | $0 - \infty$ | **Exploratory Process Variable** | Off-screen focus/blur event count & dwell time (NOT external web search) | `telemetry_events` table |
| `LanguageLeakageFlag` | Binary | 0 / 1 | **Technical Telemetry** | Automated regex flag detecting off-target language in AI response | `messages` table |
| `AILS_Score` | Discrete Score | 12 – 60 | **Stratification / Moderator** | 12-item AI Literacy Scale total score | `ai_literacy` table |
| `LEAP_Q_Variables` | Mixed | 1-10 / % / Yrs | **Covariates / Background** | Language Age of Acquisition, self-rated proficiencies, usage % | `language_background` table |

---

## 13. AI System Configuration

### 13.1 Production Model Configuration
```text
Provider: Google Gemini API
Model Identifier: gemini-3.5-flash
Model Version Tag: 3.5-flash-05-2026
Base URL: https://generativelanguage.googleapis.com/v1beta/openai
Endpoint: https://generativelanguage.googleapis.com/v1beta/openai/chat/completions
Temperature: 0.2
Top-p: 1.0
Max Output Tokens: 1000
Timeout: 15 seconds (15000 ms)
Maximum Retries: 1
Retry Condition: HTTP 5xx or Connection Timeout ONLY
```

### 13.2 System Prompt Version & Hashes
- **System Prompt Version:** `v1.1.0-gemini-frozen`
- **SHA-256 Hashes:**
  - `ENGLISH_ONLY`: `349e957733bbbf89718dd995dba169706f033b692d449221d6a431b023e7fc4d`
  - `HINDI_ONLY`: `0768ec1d898c07e1347fabc4987250d6a4660bf7d5e88536e05d3c99f9b75348`
  - `CODE_SWITCHING`: `6bfe684d2e56453d9d32452efe3ba3c897c7e6d3b3a1c94f10b2158cae7e74b2`

### 13.3 Provider Hardening
- Zero Groq fallback.
- Zero OpenAI fallback.
- Zero automatic model substitution.
- Provider isolation validated by unit test `test_gemini_transport_destination_isolation`.

---

## 14. Language Leakage

### 14.1 Definition
Language leakage occurs when the AI assistant generates responses containing non-target language tokens (e.g., English text in `HINDI_ONLY` arm).

### 14.2 Detection & Logging
Detecting server-side via regex. Sets `language_leakage_flag = True` in `messages` table and logs event `LANGUAGE_LEAKAGE_DETECTED`.

### 14.3 Participant Delivery
Leakage responses are delivered directly to the participant without silent retries to preserve natural interaction flow and latency bounds.

---

## 15. Ground Truth and Scoring

### 15.1 Deterministic Engine
Evaluated by `backend/app/scoring/engine.py` against JSON rubrics.

### 15.2 Decision Quality Scale
Continuous 0.0 to 10.0 scale per task.

### 15.3 Zero LLM-As-Judge
Scoring uses exact structural field matching. LLM-as-judge is strictly excluded.

---

## 16. Statistical Analysis Plan

### 16.1 Primary Statistical Model (LMM)
$$\text{DecisionQuality} \sim \text{Language} + \text{Scenario} + \text{Position} + (1|\text{Participant})$$

- **Family:** Linear Mixed-Effects Model (LMM).
- **Fixed Effects:** `Language` (3 levels), `Scenario` (3 levels), `Position` (3 levels).
- **Random Effect:** Participant random intercept `(1|Participant)`.
- **Primary Contrast:** Orthogonal contrast $C_1: \mu_{\text{English}} - \mu_{\text{Hindi}} \neq 0$ at $\alpha = 0.05$.

### 16.2 Secondary Models
- **Code-Switching Contrast:** $C_2: \mu_{\text{CodeSwitching}} - \mu_{\text{Hindi}} \neq 0$.
- **Moderation Model:** $\text{DecisionQuality} \sim \text{Language} \times \text{AILS\_Score} + \text{Scenario} + \text{Position} + (1|\text{Participant})$.

### 16.3 Excluded Legacy Models
PROCESS Model 4/6 mediation macros, Welch t-tests, and participant mean collapsing are strictly excluded.

---

## 17. Missing Data and Exclusions

### 17.1 Participant Incompleteness
Participants who do not complete all 3 tasks are excluded from primary LMM analysis and replaced.

### 17.2 Technical Failures
Task sessions with unrecoverable HTTP 5xx errors are flagged `TECHNICAL_FAILURE`.

### 17.3 Unspecified Rules
- Specific outlier trimming rules (>3 SD task duration): `NOT YET SPECIFIED`.

---

## 18. Ethics and Data Protection

### 18.1 Informed Consent & Pseudonymity
Digitally recorded on screen S1. Participants tracked via pseudonymous UUID v4 (`p_...`). Zero PII collected.

### 18.2 IP Hash & Data Transmission
Salted 32-character IP hash used for temporary duplicate checking; discarded post-study. Zero PII transmitted to Gemini API.

### 18.3 IRB Approval Prerequisite
$$\text{IRB / Ethics Approval ID: PENDING}$$

**HUMAN RECRUITMENT CANNOT BEGIN BEFORE FORMAL ETHICS APPROVAL.**

---

## 19. Reproducibility Matrix

- **Protocol Version:** `1.1.0-gemini-frozen`
- **Provider:** Google Gemini API
- **Model Identifier:** `gemini-3.5-flash`
- **Model Version:** `3.5-flash-05-2026`
- **System Prompt Version:** `v1.1.0-gemini-frozen`
- **Parameters:** `temperature=0.2`, `top_p=1.0`, `max_tokens=1000`
- **Analysis Formula:** `DecisionQuality ~ Language + Scenario + Position + (1|Participant)`

---

## 20. Protocol Deviations and Amendments

Any substantive changes post-freeze must be logged in `docs/protocol_change_log.md`. Silent changes are prohibited.

---

## 21. Implementation Status

### 21.1 Implemented
- React 18 SPA frontend (S1–S10).
- FastAPI backend with 12 SQLAlchemy entities.
- Stratified block randomization engine.
- Deterministic scoring engine.
- Telemetry event tracking API.
- Google Gemini API provider integration & unit test suite (30/30 tests passing).

### 21.2 Not Yet Implemented
- Production PostgreSQL database deployment (dev uses SQLite).
- Participant recruitment platform webhook integration (e.g. Prolific/Qualtrics).

### 21.3 Operational Prerequisites
- Formal IRB / Ethics approval.
- Production environment variable population (`GEMINI_API_KEY`).

---

## 22. Current Study Status

```text
PROTOCOL CONSISTENT AND READY FOR FORMAL FREEZE
```

```text
HUMAN RECRUITMENT: NOT AUTHORIZED PENDING ETHICS APPROVAL
```
