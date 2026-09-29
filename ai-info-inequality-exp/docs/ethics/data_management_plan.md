# Data Management Plan (DMP)

**Study Title:** Linguistic Inequality in AI-Mediated Information Seeking: An English-Hindi Randomized Controlled Trial  
**Protocol Version:** `1.1.0-gemini-frozen`  
**Study Identifier:** `ENGLISH_HINDI_AI_INFO_INEQUALITY_2026`  

---

## 1. Data Inventory & Classification

The study collects and manages 5 distinct tiers of data:

| Tier | Data Type | Contains PII? | Examples | Storage Location | Access Controls |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Tier 1** | **Personally Identifiable Information (PII)** | NO | Real name, email, payment handles | N/A (No compensation or PII collected) | N/A |
| **Tier 2** | **Pseudonymous Research Data** | NO | Survey answers (LEAP-Q, AILS), decisions, confidence, NASA-TLX | Experiment database (`participants`, `final_decisions`) | Research team only |
| **Tier 3** | **Interaction & Telemetry Data** | NO | Prompts, AI responses, clicks, view durations, window blur events | Experiment database (`messages`, `telemetry_events`) | Research team only |
| **Tier 4** | **Technical & Infrastructure Data** | NO | HTTP status, latency ms, retry count, language leakage flags | Experiment database (`technical_errors`) | Technical admin only |
| **Tier 5** | **Temporary Security Logs** | NO (Salted) | Salted 32-character IP hash (`ip_hash`) | Experiment database (`participants` table) | Auto-purged post-study |

---

## 2. Pseudonymization & Identity Isolation

- **Participant Identifier:** Each participant is assigned a random UUID v4 string (`p_...`). All database records across all 12 SQLAlchemy tables reference this UUID.
- **Compensation Isolation:** Participation is voluntary without monetary compensation. No financial payment handles or participant PII are collected or linked to the experimental database.

---

## 3. External AI Provider Data Flow (Google Gemini API)

- **Transmitted Data:** Task scenario context and user prompt text.
- **Isolated Data (NOT Transmitted):** Real names, email addresses, participant UUIDs, IP addresses, AILS scores, ground-truth rubrics, or research hypotheses.
- **Transport Security:** All API traffic uses HTTPS / TLS 1.3 encryption.

---

## 4. Database Security & Storage Architecture

- **Development Storage:** Local SQLite database (`backend/experiment.db`).
- **Production Storage:** Local PostgreSQL database deployment on self-hosted research server with disk encryption at rest (AES-256) and local TLS in transit. No cloud hosting for application or database is utilized.
- **Backend Access Control:** API keys (`GEMINI_API_KEY`) and database credentials are stored in environment variables, excluded from Git repositories via `.gitignore`.

---

## 5. Data Retention, Archiving & Open Science

- **Primary Data Retention Period:** `DATA RETENTION PERIOD: ETHICS DECISION REQUIRED` (e.g. 5 or 10 years post-publication).
- **Open Data Sharing Policy:** `OPEN DATA POLICY: ETHICS DECISION REQUIRED` (Decision required regarding public repository release of de-identified response matrices).
- **Security Incident Response Plan:** In the event of an unauthorized data breach, the PI will immediately notify the Institutional Ethics Committee within 24 hours.
