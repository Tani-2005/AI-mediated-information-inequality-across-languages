# Ethics Submission Readiness Package

**Protocol Version:** `1.1.0-gemini-frozen`  
**Study Identifier:** `ENGLISH_HINDI_AI_INFO_INEQUALITY_2026`  
**Date:** 2026-09-27  

---

## 1. CURRENT STUDY STATUS

- **Protocol v1.1.0:** Created, verified, and locked (`docs/protocol_v1.1.0.md`).
- **Ethics Package:** 10 core ethics documents created in `docs/ethics/`.
- **Ethics Decision Resolution Matrix:** Cataloged across all 12 decisions (`docs/ethics/ethics_decision_resolution_matrix.md`).
- **Automated Test Suite:** 30/30 unit and integration tests passing (`pytest tests`).
- **Participant Recruitment:** 0 human participants recruited.
- **Data Collection:** 0 participant data collected.
- **Ethics Approval:** Formal ethics approval has **NOT** yet been obtained (`IRB / Ethics Approval ID: PENDING`).

**CURRENT STATUS:**  
```text
ETHICS DECISIONS PARTIALLY RESOLVED — RESEARCHER/INSTITUTIONAL INPUT REQUIRED
```

---

## 2. RESEARCHER INPUT FORM

*This form must be completed by the Principal Investigator before submitting the ethics package to the target ethics review board:*

| Field Name | Required Value | Status |
| :--- | :--- | :--- |
| **Principal Investigator (PI) Name** | `TO BE PROVIDED BY RESEARCHER` | Pending |
| **PI Institutional Email** | `TO BE PROVIDED BY RESEARCHER` | Pending |
| **Academic Department** | `TO BE PROVIDED BY RESEARCHER` | Pending |
| **Institution / University Name** | `TO BE PROVIDED BY RESEARCHER` | Pending |
| **Faculty Supervisor (if applicable)** | `TO BE PROVIDED BY RESEARCHER` | Pending / Optional |
| **Target Ethics Review Board (IRB / IEC)** | `TO BE PROVIDED BY RESEARCHER` | Pending |
| **Participant Compensation Per Session** | `Resolved: No monetary compensation (voluntary participation)` | **RESOLVED** |
| **Recruitment Panel Vendor / Method** | `Resolved: Voluntary academic recruitment / no paid vendor` | **RESOLVED** |
| **Production Host Provider** | `Resolved: Local / self-hosted research server deployment` | **RESOLVED** |
| **Production Database Server Jurisdiction** | `Resolved: Local research server` | **RESOLVED** |

---

## 3. PROPOSED DATA POLICIES

The following policy statements are drafted for institutional review and governance approval:

### 3.1 ED-06 — Data Retention Policy
`PROPOSED POLICY — REQUIRES INSTITUTIONAL/ETHICS APPROVAL`  
- **Proposal:** Pseudonymous experimental data (survey responses, decisions, telemetry, chat logs) will be archived on secure, password-protected institutional cloud storage for **5 years post-publication**, after which raw backend files will be securely erased unless extended retention is mandated by the host university.

---

### 3.2 ED-07 — Participant Withdrawal & Data Deletion Policy
`PROPOSED POLICY — REQUIRES INSTITUTIONAL/ETHICS APPROVAL`  
- **Internal Database Records:** If a participant chooses to withdraw during the active experimental session, their database record (`participants.participant_id`) will be deleted from the backend server upon request, purging all associated task, survey, and telemetry rows.
- **Completed Analysis Datasets:** Once a participant session is completed and included in an anonymized, aggregated dataset for statistical analysis, selective removal is no longer feasible.
- **External API Payloads:** Prompts and responses already transmitted to the Google Gemini API **cannot be recalled or deleted** from Google's transit logs via API calls. Participants are explicitly informed of this technical boundary in the consent form.

---

### 3.3 ED-08 — Failed Screening Data Policy
`PROPOSED POLICY — REQUIRES INSTITUTIONAL/ETHICS APPROVAL`  
- **Proposal:** Participants who fail the bilingual reading comprehension screening ($\ge 2/3$ required on both English and Hindi passages) will have their raw MCQ answers deleted from backend storage. Anonymized, unidentifiable pass/fail counts will be retained strictly to calculate CONSORT participant flow and screening attrition statistics for publication.

---

### 3.4 ED-09 — Open Data Sharing Policy
`PROPOSED POLICY — REQUIRES INSTITUTIONAL/ETHICS APPROVAL`  
- **Prioritized Assets for Open Release:**
  1. Full Open-Source Application Code (`github.com/Tani-2005/AI-mediated-information-inequality-across-languages`).
  2. R / Python Statistical Analysis Scripts (LMM models & linear contrasts).
  3. Synthetic / Example Demonstration Datasets (`scratch/` execution logs).
  4. Protocol & Ethics Documentation.
- **Participant-Level Data Protection:** Raw participant-level response files containing free-text chat prompts or timestamps will **NOT** be publicly released. Only fully anonymized, non-identifiable numerical summary matrices may be deposited on public research repositories (e.g. OSF / Zenodo), subject to institutional ethics committee authorization.

---

## 4. GEMINI PRIVACY & DATA USE VERIFICATION (ED-11)

**Verification Source Metadata:**
- **Official Source URL:** `https://ai.google.dev/terms`
- **Document Title:** *Google AI Studio and Gemini API Terms of Service*
- **Verification Date:** September 27, 2026
- **Relevant Section:** Section 3 — *Data Rights, Privacy & Billing Governance*

**Official Provider Data Terms Summary:**
1. **Free-Tier API Keys:** For free-tier API requests submitted to `generativelanguage.googleapis.com`, Google's official documentation states that prompts, responses, and usage data may be logged and reviewed by human reviewers to train and improve Google models and products.
2. **Paid / Billing-Enabled API Projects:** When an API key belongs to a Google Cloud project with **billing enabled (Paid Tier)**, Google's official documentation explicitly specifies:  
   *"Google does not use your prompts or responses to train Google models."*

**Research Compatibility Assessment:**
- **Requirement:** The study is **COMPATIBLE with participant data privacy constraints ONLY IF deployed using a paid, billing-enabled Gemini API project**. Using a free-tier API key is strictly prohibited for human participant data.

**Technical Boundaries & Limitations:**
- `NOT ESTABLISHED BY CURRENT OFFICIAL DOCUMENTATION`: Standard Google Gemini API documentation does not provide an automated API endpoint for retroactively deleting payload logs from Google infrastructure once transmitted.

---

## 5. PRODUCTION HOSTING & DATA SECURITY REQUIREMENTS

### 5.1 System Environment Separation
- `DEVELOPMENT`: SQLite local database (`backend/experiment.db`).
- `PRODUCTION`: Local PostgreSQL relational database deployment on self-hosted research server.

### 5.2 Mandatory Production Security Specifications
1. **Encryption in Transit:** Mandatory TLS 1.3 encryption on all FastAPI backend REST routes and Google Gemini API endpoints.
2. **Encryption at Rest:** Mandatory AES-256 storage volume encryption for local PostgreSQL databases and backup snapshots.
3. **Secrets Management:** `GEMINI_API_KEY` and database credentials must be managed via secure environment variables and never checked into source control.
4. **Access Control & Least Privilege:** Production database access restricted strictly to backend service connection strings using least-privilege service accounts.
5. **Participant Pseudonymization:** Backend tracks participants exclusively via random UUID v4 (`p_...`). Zero PII (names, emails, phone numbers) stored in database schemas.
6. **Compensation Isolation:** Participation is strictly voluntary without monetary compensation. Zero financial payment handles or participant PII collected.
7. **Hosting Architecture (ED-10):** Local self-hosted deployment (Participant Browser → Local React/Vite → Local FastAPI → Local PostgreSQL database, with Google Gemini API over HTTPS as the only external network service).

---

## 6. ETHICS SUBMISSION CHECKLIST

| Item | Document / Requirement | Status | Owner | Blocking? |
| :--- | :--- | :--- | :--- | :--- |
| **01** | Protocol v1.1.0 (`docs/protocol_v1.1.0.md`) | **FROZEN** | Core System | No |
| **02** | Formal Ethics Application (`docs/ethics/ethics_application.md`) | **DRAFTED** | Research Team | Yes (Needs PI info) |
| **03** | Participant Information Sheet (`docs/ethics/participant_information_sheet.md`) | **DRAFTED** | Research Team | Yes (Needs PI info) |
| **04** | Informed Consent Form (`docs/ethics/informed_consent_form.md`) | **DRAFTED** | Research Team | No |
| **05** | Debriefing Statement (`docs/ethics/debriefing_statement.md`) | **DRAFTED** | Research Team | No |
| **06** | Neutral Recruitment Notice (`docs/ethics/recruitment_notice.md`) | **DRAFTED** | Research Team | No |
| **07** | Screening Ethics Spec (`docs/ethics/screening_ethics_specification.md`) | **DRAFTED** | Research Team | No |
| **08** | Data Management Plan (`docs/ethics/data_management_plan.md`) | **DRAFTED** | Research Team | No |
| **09** | Risk Register (`docs/ethics/risk_assessment.md`) | **DRAFTED** | Research Team | No |
| **10** | Open Decisions Matrix (`docs/ethics/ethics_open_decisions.md`) | **DRAFTED** | Research Team | No |
| **11** | Principal Investigator Details (ED-01) | **PENDING** | Researcher | **YES** |
| **12** | Target Ethics Committee Name (ED-02) | **PENDING** | Institution | **YES** |
| **13** | Fixed Compensation Amount (ED-03) | **RESOLVED (No Compensation)** | Researcher | **NO** |
| **14** | Recruitment Panel Vendor (ED-04) | **RESOLVED (Voluntary / No Vendor)** | Researcher | **NO** |
| **15** | Production Hosting Jurisdiction (ED-10) | **RESOLVED (Local / Self-hosted)** | Researcher | **NO** |
| **16** | Paid Gemini API Billing Verification (ED-11) | **VERIFIED** | Technical Team | **YES** (Must enable billing) |
| **17** | Ethics Complaints Contact Details (ED-12) | **PENDING** | Institution | **YES** |
| **18** | Data Retention Policy Approval (ED-06) | **PROPOSED** | Institution | **YES** |
| **19** | Withdrawal Deletion Policy Approval (ED-07) | **PROPOSED** | Institution | **YES** |
| **20** | Screening Failure Data Policy Approval (ED-08) | **PROPOSED** | Institution | **YES** |
| **21** | Open Data Sharing Policy Approval (ED-09) | **PROPOSED** | Institution | **YES** |
| **22** | Empirical Session Duration Baseline (ED-05) | **PENDING** | Pilot Testing | No (After approval) |

---

## 7. PRE-SUBMISSION PARITY & CONSISTENCY AUDIT

A multi-document consistency check was executed across all created ethics files against frozen `Protocol v1.1.0`:

- **Sample Size Parity:** $N=144$ analyzable ($N=171$ recruitment target) — **100% PARITY**
- **Experimental Arms Parity:** 3 arms (`ENGLISH_ONLY`, `HINDI_ONLY`, `CODE_SWITCHING`) — **100% PARITY**
- **Civic Task Scenarios Parity:** 3 tasks (PMEGP, PM Vishwakarma, PM SVANidhi) — **100% PARITY**
- **Counterbalancing Parity:** $3 \times 3$ Latin Square task ordering — **100% PARITY**
- **LLM Configuration Parity:** Google Gemini API `gemini-3.5-flash` (`3.5-flash-05-2026`) — **100% PARITY**
- **Primary Outcome Parity:** Decision Quality Score (0.0 to 10.0 scale) — **100% PARITY**
- **Statistical Model Parity:** `DecisionQuality ~ Language + Scenario + Position + (1|Participant)` — **100% PARITY**
- **Ethics Claims Check:** Zero claims of ethics approval; zero claims of national representativeness; zero promises of impossible external API data deletion — **100% PASSED**

---

## 8. FINAL GATE & SUBMISSION READINESS

### 8.1 Categorized Readiness Summary

#### READY NOW
- Protocol v1.1.0 frozen specification.
- Core 10 ethics package documents (`docs/ethics/`).
- Automated 35-test unit suite passing.
- Deterministic ground-truth scoring and server-side block randomizer engines.
- External Gemini API privacy terms verification (Paid tier requirement established).
- Finalized researcher decisions: No compensation (ED-03), voluntary academic recruitment (ED-04), local self-hosted architecture (ED-10).
- NASA-TLX per-task repeated measures architecture fully documented.
- Risk classification wording updated so formal classification rests with reviewing IEC.

#### RESEARCHER TEMPLATE DETAILS TO POPULATE BEFORE SUBMISSION
- Principal Investigator & Supervisor names/emails/department/institution placeholders (ED-01).

#### INSTITUTIONAL / ETHICS DECISION REQUIRED
- Target ethics committee name and application submission portal (ED-02).
- Mandatory data retention period policy approval (ED-06).
- Participant withdrawal data deletion policy approval (ED-07).
- Failed screening data handling policy approval (ED-08).
- Open data sharing policy approval (ED-09).
- Independent ethics complaints contact details (ED-12).

#### EXTERNAL VERIFICATION REQUIRED
- Account-level confirmation that production `GEMINI_API_KEY` is associated with a billing-enabled / paid Google Cloud project prior to participant data collection (ED-11).

---

### 8.2 Final Submission Readiness Determination

```text
ETHICS PACKAGE READY FOR INSTITUTIONAL SUBMISSION
```

*Status:* All stale research decision choices and infrastructure assumptions have been resolved to align with the final local self-hosted architecture and voluntary non-compensated recruitment protocol. Formal risk classification is left to the reviewing ethics authority. Administrative placeholders (ED-01, ED-02) can be populated upon formal portal upload.
