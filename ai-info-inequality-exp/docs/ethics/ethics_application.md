# Formal Human-Participant Ethics Application

**Study Title:** Linguistic Inequality in AI-Mediated Information Seeking: An English-Hindi Randomized Controlled Trial  
**Protocol Version:** `1.1.0-gemini-frozen`  
**Study Identifier:** `ENGLISH_HINDI_AI_INFO_INEQUALITY_2026`  
**Ethics Approval ID:** `PENDING`  
**Date:** 2026-09-27  

---

## 1. Study Identification & Institutional Information

- **Study Title:** Linguistic Inequality in AI-Mediated Information Seeking: An English-Hindi Randomized Controlled Trial
- **Protocol Version:** `1.1.0-gemini-frozen`
- **Principal Investigator (PI):** `[TO BE COMPLETED BY RESEARCHER]`
- **Institutional Affiliation:** `[TO BE COMPLETED BY RESEARCHER]`
- **Academic Supervisor / Department Head:** `[TO BE COMPLETED BY RESEARCHER]`
- **Target Review Board:** `[TO BE COMPLETED BY RESEARCHER]` (e.g., Institutional Review Board / Institutional Ethics Committee)
- **Ethics Approval Status:** `PENDING` (Human participant recruitment and data collection CANNOT begin before formal IRB approval)

---

## 2. Background and Rationale

Generative Artificial Intelligence (AI) search engines and Large Language Models (LLMs) are increasingly deployed as primary search and information-seeking interfaces for public entitlements and government welfare programs. However, LLMs exhibit significant variance in tokenization efficiency, pre-training corpora representation, and generation fidelity across languages. 

While bilingual Indian citizens frequently navigate online environments in English, Hindi, or a mix of both (Code-Switching / Hinglish), it is unknown whether interacting with AI assistants in non-English languages introduces systematic information inequality—such as higher error rates, increased verification burdens, or degraded civic decision quality.

Evaluating human participants in a controlled experimental setting is necessary because automated LLM benchmarks assess generation quality in isolation without capturing human decision-making, verification behaviors, prompting strategies, automation reliance, or subjective cognitive workload.

---

## 3. Research Questions

- **Primary Research Question (RQ1):** Does interaction language (`ENGLISH_ONLY` vs. `HINDI_ONLY` vs. `CODE_SWITCHING`) significantly affect final Decision Quality Scores when bilingual Indian citizens use an AI assistant to evaluate complex civic entitlement scenarios?
- **Secondary Research Question 1 (RQ2):** Does a Code-Switching AI interaction condition (`CODE_SWITCHING`) significantly mitigate decision quality disparities relative to a single-language Hindi condition (`HINDI_ONLY`)?
- **Secondary Research Question 2 (RQ3):** To what extent does baseline AI literacy (measured via AILS) moderate the relationship between interaction language condition and final decision quality?

---

## 4. Hypotheses

- **H1 (Language Disadvantage):** Participants assigned to the `ENGLISH_ONLY` arm will achieve significantly higher Decision Quality Scores than participants assigned to the `HINDI_ONLY` arm ($\mu_{\text{English}} - \mu_{\text{Hindi}} > 0$).
- **H2 (Code-Switching Mitigation):** Participants assigned to the `CODE_SWITCHING` arm will achieve significantly higher Decision Quality Scores than participants assigned to the `HINDI_ONLY` arm ($\mu_{\text{CodeSwitching}} - \mu_{\text{Hindi}} > 0$).
- **H3 (AI-Literacy Moderation):** Baseline AI Literacy (AILS total score) will significantly moderate the effect of language condition on Decision Quality, such that higher AI literacy attenuates the decision quality gap between English and Hindi interactions.

---

## 5. Study Design

The study is a **3 Between-Subjects Language Arms $\times$ 3 Within-Subjects Civic Tasks** mixed experimental design:
- **Between-Subjects Factor:** Language Arm (`ENGLISH_ONLY`, `HINDI_ONLY`, `CODE_SWITCHING`).
- **Within-Subjects Factor:** Civic Entitlement Scenario (`PMEGP`, `PM_VISHWAKARMA`, `PM_SVANIDHI`).
- **Analyzable Sample Size ($N$):** $N = 144$ (48 participants per arm; total $144 \times 3 = 432$ task sessions).
- **Recruitment Target ($N$):** $N = 171$ (includes 15% planned attrition/dropout allowance).
- **Counterbalancing:** $3 \times 3$ Latin-Square task ordering (`ORDER_1`, `ORDER_2`, `ORDER_3`) to control for fatigue and order effects.

---

## 6. Participant Population & Sampling

- **Target Population:** English-Hindi bilingual Indian adults aged 18–65 residing in India.
- **Inclusion Criteria:**
  1. Age 18–65 years.
  2. Resident of India.
  3. Self-reported basic digital literacy (ability to use web browsers and chat interfaces).
  4. Bilingual comprehension passage screening pass ($\ge 2/3$ on English sub-test AND $\ge 2/3$ on Hindi sub-test).
- **Exclusion Criteria:**
  1. AI/NLP researchers, AI software developers, or professional prompt engineers.
  2. Failure to pass bilingual comprehension screening.
  3. Incomplete completion of all 3 task sessions.
- **Sampling Strategy:** Voluntary convenience sampling of English-Hindi bilingual digital citizens as permitted by the reviewing institution.

---

## 7. Planned Recruitment

- **Recruitment Platform:** Voluntary academic recruitment / institutional volunteer pool as permitted by the reviewing institution. No paid recruitment panel vendor is utilized.
- **Recruitment Notice:** Neutral recruitment text describing the study as research on user interaction with AI-assisted information systems. Detailed hypotheses regarding language disadvantage are withheld during recruitment to prevent participant response bias.

---

## 8. Screening and Eligibility Pipeline

1. **Bilingual Comprehension Screening:** 3 English passage MCQs and 3 Hindi passage MCQs testing basic reading comprehension. Score $\ge 2/3$ on BOTH sub-tests required to proceed.
2. **Language Background (LEAP-Q):** Assesses Age of Acquisition, home language, medium of instruction, and self-rated 1–10 proficiencies.
3. **AI Literacy Scale (AILS):** 12 Likert-scale items (score range 12–60) used for backend stratification (median split threshold = 36: `LOW` vs `HIGH`).
4. **Handling Failed Screening Data:** `ETHICS DECISION REQUIRED` (Decision required: whether to immediately purge failed screening responses or retain anonymized aggregate counts to document screening fail rates).

---

## 9. Participant Procedure & Estimated Duration

### 9.1 Participant Journey
1. **Consent (S1):** Review information sheet and provide digital affirmative consent.
2. **Screening (S2):** Complete English and Hindi comprehension sub-tests.
3. **LEAP-Q (S3):** Complete language background questionnaire.
4. **AILS (S4):** Complete 12-item AI Literacy Scale.
5. **Randomization (S5):** Server-side allocation to language arm (`ENGLISH_ONLY`, `HINDI_ONLY`, or `CODE_SWITCHING`).
6. **Onboarding (S6):** Instructions on interacting with the AI interface and accessing verification documents.
7. **Task Execution (S7 $\times$ 3):** Complete 3 civic entitlement evaluation tasks in Latin-Square order.
8. **Post-Task Measures (S8 $\times$ 3):** Submit self-reported confidence and 6-item raw NASA-TLX workload scale after each task.
9. **Debriefing (S10):** Receive comprehensive debriefing statement, official government scheme links, and researcher contact information.

### 9.2 Duration
`Final estimated duration to be established during approved pilot testing.`

---

## 10. AI Interaction Disclosure

Participants interact with a real-time Generative AI model powered by the **Google Gemini API** (`gemini-3.5-flash`, build version `3.5-flash-05-2026`). 

**Key Disclosures:**
- Participants are explicitly informed that they are interacting with an AI language model.
- Participants are warned that AI responses may contain inaccuracies, incomplete information, or misleading statements.
- Tasks are simulated research scenarios; participants are instructed not to rely on AI outputs for real-world personal entitlement applications.

---

## 11. Civic-Information Risk & Mitigation

The study utilizes real Indian government welfare schemes (PMEGP, PM Vishwakarma, PM SVANidhi) as realistic task domains.

**Risk Mitigation:**
1. **Simulated Scenarios:** All task prompts present hypothetical citizen personas.
2. **Disclaimers:** Onboarding explicitly states that information generated during the study is strictly for research evaluation.
3. **Official Links Provided:** Comprehensive debriefing provides direct links to official government web portals (e.g. `kviconline.gov.in`, `pmvishwakarma.gov.in`, `pmsvanidhi.mohua.gov.in`).

---

## 12. Structured Risk Assessment

| Risk Description | Likelihood | Severity | Mitigation Strategy | Residual Risk |
| :--- | :--- | :--- | :--- | :--- |
| **Inaccurate AI Output:** Participant receives incorrect scheme eligibility rules from LLM. | High | Low | Clear onboarding warnings; task scenarios are hypothetical; official scheme links provided in debrief. | Minimal |
| **Civic Misinformation:** Participant misinterprets research tasks as personal welfare advice. | Low | Medium | Explicit disclaimers during consent, onboarding, and debriefing; no PII collected. | Minimal |
| **Cognitive Fatigue / Frustration:** Completing 3 detailed entitlement tasks causes mental tiredness. | Moderate | Low | Enforced breaks between tasks; NASA-TLX monitoring; right to withdraw at any time without penalty. | Low |
| **Language Discomfort:** Assignment to a less-preferred language arm (`HINDI_ONLY` or `ENGLISH_ONLY`). | Moderate | Low | Pre-screening ensures bilingual competence in both languages before randomization. | Minimal |
| **Data Privacy Leakage:** Unauthorized disclosure of participant interaction data. | Low | Medium | Pseudonymous UUID v4 tracking; temporary salted IP hash; zero PII stored; encrypted HTTPS transit. | Minimal |
| **Third-Party API Data Exposure:** Transmission of prompts to Google Gemini API. | Low | Low | Zero PII or participant identifiers sent in API payloads; backend-only proxy isolation. | Minimal |

*Risk Classification Justification:* Formal risk classification rests with the reviewing Institutional Ethics Committee (proposed classification for review: Low / Minimal Risk based on identified factors).

---

## 13. Benefits Analysis

- **Direct Participant Benefits:** None. Participation is entirely voluntary without monetary compensation.
- **Societal & Scientific Benefits:** Provides empirical evidence on language disparities in generative AI systems, informing the design of equitable multilingual AI public services and Indic language NLP infrastructure.

---

## 14. Participant Compensation

- **Compensation Amount:** No monetary or financial compensation is provided to participants.
- **Payment Rule:** Participation is strictly voluntary.

---

## 15. Voluntary Participation & Withdrawal

- **Voluntary Status:** Participation is entirely voluntary.
- **Withdrawal Policy:** Participants may exit the study at any time by closing their browser or clicking "Withdraw".
- **Data Deletion Upon Withdrawal:** `ETHICS DECISION REQUIRED` (Decision required: specify whether pseudonymous data collected up to the point of withdrawal is retained in an intent-to-treat framework or purged upon request).

---

## 16. Deception

**No deception is used in this study.** Participants are accurately informed that they are interacting with an AI assistant evaluating government entitlement rules. The specific research hypotheses comparing language performance are withheld prior to task completion solely to prevent demand characteristics and behavioral reactivity. Full hypotheses are disclosed during debriefing.

---

## 17. Debriefing

Upon completion (or withdrawal), participants view a comprehensive Debriefing Statement explaining:
- Full research goals and language arm comparison rationale.
- Disclaimer that AI responses were generated for research evaluation only.
- Direct web links to official government scheme portals.
- Contact information for the research team and institutional ethics board.

---

## 18. Complete Data Inventory

| Data Element | Purpose | Necessary? | Identifiable? | Retention Period | Shared with Gemini API? |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Participant UUID** (`p_...`) | Pseudonymous session tracking | Yes | No | `ETHICS DECISION REQUIRED` | No |
| **Bilingual Screening Scores** | Eligibility verification | Yes | No | `ETHICS DECISION REQUIRED` | No |
| **LEAP-Q Responses** | Demographic background control | Yes | No | `ETHICS DECISION REQUIRED` | No |
| **AILS Total Score & Stratum** | Block randomization | Yes | No | `ETHICS DECISION REQUIRED` | No |
| **User Prompts** | Task interaction analysis | Yes | No | `ETHICS DECISION REQUIRED` | Yes (Task text only) |
| **AI Responses** | Quality & leakage analysis | Yes | No | `ETHICS DECISION REQUIRED` | N/A (Generated by API) |
| **Final Decisions & Answers** | Primary outcome scoring | Yes | No | `ETHICS DECISION REQUIRED` | No |
| **Confidence & NASA-TLX** | Subjective workload outcomes | Yes | No | `ETHICS DECISION REQUIRED` | No |
| **Document Clicks & Duration** | Secondary outcome verification | Yes | No | `ETHICS DECISION REQUIRED` | No |
| **Window Blur Events** | Off-screen focus process tracking | Yes | No | `ETHICS DECISION REQUIRED` | No |
| **Temporary IP Hash** | Duplicate submission prevention | Yes | Pseudonymous (Salted) | Purged post-study | No |

---

## 19. External AI Provider Data Handling

Prompts submitted by participants are proxied through the backend FastAPI service to the **Google Gemini API** (`generativelanguage.googleapis.com`).

**Data Isolation:**
- **Transmitted:** Task scenario context and user prompt text.
- **NOT Transmitted:** Real name, email, IP address, participant UUID, AILS score, ground-truth rubrics, or research hypotheses.

---

## 20. Data Security & Storage Architecture

- **Pseudonymization:** All backend database tables reference random UUID v4 (`p_...`) identifiers.
- **API Key Security:** Gemini API keys are stored exclusively in backend environment variables (`GEMINI_API_KEY`) and never exposed to client browsers.
- **Database Architecture:** Local self-hosted architecture (Participant Browser → Local React/Vite → Local FastAPI → Local PostgreSQL database, with Google Gemini API over HTTPS as the only external network service). No cloud hosting for the application or database is utilized.

---

## 21. Data Retention & Open Science Policies

- **Data Retention Period:** `DATA RETENTION PERIOD: ETHICS DECISION REQUIRED`
- **Open Data Sharing:** `OPEN DATA POLICY: ETHICS DECISION REQUIRED` (Decision required on publishing fully anonymized participant response matrices on open research repositories such as OSF or Zenodo).

---

## 22. Ethical Justification Summary

The potential risks to participants are minimal, manageable, and strictly mitigated through disclaimers, pseudonymity, and debriefing. The scientific value of identifying language-mediated AI information inequality provides critical public benefit for equitable digital access in multilingual societies. The ethical balance strongly supports approval.
