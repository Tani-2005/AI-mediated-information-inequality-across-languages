# Ethics Decision Resolution Matrix

**Protocol Version:** `1.1.0-gemini-frozen`  
**Study Identifier:** `ENGLISH_HINDI_AI_INFO_INEQUALITY_2026`  
**Status:** ETHICS DECISIONS PARTIALLY RESOLVED — RESEARCHER/INSTITUTIONAL INPUT REQUIRED  
**Date:** 2026-09-27  

---

## 1. Classification & Resolution Matrix for All 12 Open Decisions

| ID | Decision | Category | Current Status | Required Action | Blocking? |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ED-01** | **PI & Institutional Details** | `RESEARCHER DECISION` | `RESEARCHER INPUT REQUIRED` | Researcher must provide real name, email, department, and university name. | **YES** |
| **ED-02** | **Target Ethics Committee** | `DEPENDS ON INSTITUTION` | `INSTITUTIONAL DECISION REQUIRED` | Depends on host university/institution's specific IRB or IEC board name and submission portal. | **YES** |
| **ED-03** | **Compensation Amount & Rate** | `RESEARCHER DECISION` | `RESOLVED — NO MONETARY COMPENSATION` | Participation is voluntary without monetary compensation. | **NO** |
| **ED-04** | **Recruitment Platform** | `RESEARCHER DECISION` | `RESOLVED — VOLUNTARY RECRUITMENT` | Recruitment via voluntary academic notices as permitted by reviewing institution. No paid panel vendor used. | **NO** |
| **ED-05** | **Session Duration Baseline** | `ALREADY RESOLVED` | `FINAL SESSION DURATION — TO BE ESTABLISHED DURING APPROVED PILOT` | Frozen protocol explicitly specifies duration will be established during approved pilot testing ($N=6\text{--}10$). | **NO** |
| **ED-06** | **Data Retention Period** | `INSTITUTIONAL DECISION` | `INSTITUTIONAL DECISION REQUIRED` | Ethics committee must specify mandatory data retention period (e.g., 5 years, 10 years, or permanent archive). | **YES** |
| **ED-07** | **Withdrawal Deletion Policy** | `INSTITUTIONAL DECISION` | `INSTITUTIONAL DECISION REQUIRED` | Ethics committee must establish whether pseudonymous data collected up to withdrawal is purged or retained under ITT. | **YES** |
| **ED-08** | **Failed Screening Data Policy** | `INSTITUTIONAL DECISION` | `INSTITUTIONAL DECISION REQUIRED` | Ethics committee must specify whether screening fail logs are purged immediately or kept as anonymized aggregate counts. | **YES** |
| **ED-09** | **Open Data Sharing Policy** | `INSTITUTIONAL DECISION` | `OPEN DATA POLICY — INSTITUTIONAL/ETHICS DECISION REQUIRED` | Ethics committee must approve open access data sharing framework (anonymized response matrix on OSF/Zenodo). | **YES** |
| **ED-10** | **Hosting Jurisdiction** | `RESEARCHER DECISION` | `RESOLVED — LOCAL / SELF-HOSTED DEPLOYMENT` | Self-hosted local deployment (Participant Browser → Local React/Vite → Local FastAPI → Local PostgreSQL, with Google Gemini API over HTTPS as external service). No cloud app/DB hosting. | **NO** |
| **ED-11** | **Gemini API Privacy Terms** | `EXTERNAL VERIFICATION REQUIRED` | `EXTERNALLY VERIFIED FROM OFFICIAL GOOGLE DOCUMENTATION` | Google Gemini API Terms verified against official Google Terms of Service (paid tier non-training policy). | **YES** |
| **ED-12** | **Ethics Complaints Contact** | `DEPENDS ON INSTITUTION` | `INSTITUTIONAL DECISION REQUIRED` | Independent ethics committee contact email/phone assigned by target institution upon application submission. | **YES** |

---

## 2. Detailed Technical & Methodological Resolutions

### 2.1 Gemini API Privacy Verification (ED-11)
- **API Service Used:** Google Gemini API (`generativelanguage.googleapis.com/v1beta/openai`).
- **Official Google Terms of Service Policy (Google AI Studio & Gemini API Terms of Service):**
  - **Free Tier API Keys:** Google's official documentation states: *"For free tier API keys, Google may use your prompts, responses, and API usage data to train and improve Google products and technologies."*
  - **Paid Tier / Commercial API Keys (Pay-as-you-go with billing enabled):** Google's official documentation states: *"When you enable billing for your Gemini API project, Google does not use your prompts or responses to train Google models."* (Source: Google AI Studio Data Governance & Privacy Terms, `https://ai.google.dev/terms`).
- **Research Compatibility Finding:**  
  The planned use is **COMPATIBLE with research participant data ONLY IF the production deployment uses a Paid / Billing-Enabled Gemini API key**. If a free-tier key is used, prompts are subject to Google model training, which violates standard participant privacy guarantees.
- **Data Recall / Deletion Limitation:**  
  `NOT ESTABLISHED BY CURRENT OFFICIAL DOCUMENTATION` — Once a prompt payload is transmitted over the API connection, Google does not provide an automated API mechanism to recall, edit, or delete submitted request payloads from API transit logs.

---

### 2.2 Production Database & Hosting Jurisdiction (ED-10)
- **Architecture:** Local / self-hosted research server deployment (Participant Browser → Local React/Vite → Local FastAPI → Local PostgreSQL database, with Google Gemini API over HTTPS as the only external network service).
- **Cloud Infrastructure Status:** No cloud-hosted application server or managed cloud PostgreSQL database (AWS, GCP, Azure, Firebase, Cloud Run, etc.) is utilized.
- **Jurisdiction:** Local self-hosted research system.

---

### 2.3 Screening Data Retention & Deletion Policy (ED-08)
- **Technical Capability:** The backend records English sub-test score, Hindi sub-test score, pass/fail flag, and raw MCQ responses in the `screening_logs` table.
- **Categorization:**
  1. *Eligibility Determination Data:* Sub-test scores ($0\text{--}3$) needed immediately to branch participant to consent/randomization or exit.
  2. *Research Attrition Data:* Anonymized pass/fail counts needed for CONSORT flow diagrams.
- **Policy Determination:** `INSTITUTIONAL DECISION REQUIRED` (Ethics board must specify whether raw responses of ineligible participants are deleted immediately or retained in anonymized aggregate form).

---

### 2.4 Technical Assessment of Withdrawal Data Rights (ED-07)

1. **Can an enrolled participant be identified in the database using their pseudonymous ID (`p_...`)?**  
   **YES.** The backend database maintains relational records indexed by `participant_id` (UUID v4).
2. **Can their research records in the backend database be deleted?**  
   **YES.** Executing a database delete query on `participants.participant_id` cascades across all 12 SQLAlchemy tables, completely purging their survey responses, messages, telemetry, decisions, and workload scores.
3. **Can their Gemini-transmitted prompts/responses be recalled or deleted from Google's servers?**  
   **NO.** Google's API architecture does not support remote deletion of completed API HTTP requests. Prompts already transmitted to Google Gemini API cannot be recalled.
4. **What happens after data have been fully anonymized/de-identified for publication?**  
   Once data are stripped of identifiers and aggregated in a public release dataset, individual responses can no longer be identified or selectively deleted.

---

### 2.5 Open Data Sharing Policy Framework (ED-09)

- **Source Code (`github.com/Tani-2005/AI-mediated-information-inequality-across-languages`):** Fully public open source.
- **Analysis Code (R / Python LMM scripts):** Fully public open source.
- **Synthetic / Example Data (`scratch/` simulations):** Fully public open source.
- **Participant-Level Research Data:** `OPEN DATA POLICY — INSTITUTIONAL/ETHICS DECISION REQUIRED`  
  *Recommendation:* Only fully anonymized response matrices (stripped of IP hashes, timestamps, and free-text comments) should be published on repositories such as OSF or Zenodo, subject to institutional ethics board approval.

---

### 2.6 Compensation Ethics Requirement (ED-03)

- **Status:** `RESOLVED — NO MONETARY COMPENSATION`
- **Ethical Mandate:** Participation is strictly voluntary without monetary compensation. Compensation **MUST NOT** depend on:
  1. Decision Quality Score or task accuracy.
  2. Correctness of civic entitlement answers.
  3. Experimental language arm assignment (`ENGLISH_ONLY`, `HINDI_ONLY`, or `CODE_SWITCHING`).

---

### 2.7 Session Duration Baseline (ED-05)

- **Status:** `FINAL SESSION DURATION — TO BE ESTABLISHED DURING APPROVED PILOT`
- **Rationale:** Preserves the frozen protocol mandate that exact session completion duration will be measured empirically during the ethics-approved pilot ($N = 6\text{--}10$).
