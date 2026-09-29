# Final Researcher Decision Worksheet & Pre-Submission Guide

**Protocol Version:** `1.1.0-gemini-frozen`  
**Study Identifier:** `ENGLISH_HINDI_AI_INFO_INEQUALITY_2026`  
**Date:** 2026-09-27  

> [!IMPORTANT]  
> This worksheet prepares the Principal Investigator (PI) to complete the remaining researcher-driven and institutional decisions required before formal submission to an Institutional Review Board (IRB) or Institutional Ethics Committee (IEC).  
>  
> **No participant recruitment or human data collection may begin until formal ethics approval is obtained.**

---

## SECTION 1 — RESEARCHER INPUTS

*Please complete the fields below with your actual investigator, institutional, and infrastructure details:*

### ED-01 — Principal Investigator & Institution
- **Full Name of PI:** `TO BE PROVIDED BY RESEARCHER`
- **Institutional Email:** `TO BE PROVIDED BY RESEARCHER`
- **Academic Department / School:** `TO BE PROVIDED BY RESEARCHER`
- **University / Institution Name:** `TO BE PROVIDED BY RESEARCHER`
- **Faculty Supervisor (if student PI):** `TO BE PROVIDED BY RESEARCHER`
- **Institutional Mailing Address:** `TO BE PROVIDED BY RESEARCHER`
- **Investigator Status:** `TO BE PROVIDED BY RESEARCHER` (e.g., Faculty / Postdoc / PhD Candidate / Student)

---

### ED-03 — Participant Compensation & Rate
- **Final Decision:** `RESOLVED (NO PARTICIPANT COMPENSATION)`
- **Policy:** Participation is strictly voluntary. No monetary or financial compensation is provided to participants.

---

### ED-04 — Recruitment Method & Panel Vendor Selection
- **Final Decision:** `RESOLVED (VOLUNTARY RECRUITMENT / NO PAID PANEL VENDOR)`
- **Policy:** Recruitment will utilize voluntary academic notices and approved volunteer outreach as permitted by the reviewing institution. No paid recruitment panel vendor (such as Prolific or Qualtrics Panel) is used.
- **Recruitment Copy Rule:** Recruitment copy MUST remain strictly neutral describing user interaction with AI-assisted information systems, avoiding revealing specific language-disadvantage hypotheses.

---

### ED-10 — Production Hosting & Infrastructure
- **Final Decision:** `RESOLVED (LOCAL / SELF-HOSTED DEPLOYMENT)`
- **Architecture:** Participant Browser → Local React/Vite → Local FastAPI → Local PostgreSQL (with Google Gemini API over HTTPS as the only external network service).
- **Cloud Infrastructure Status:** No cloud-hosted application or managed cloud database (AWS, GCP, Azure, Firebase, Cloud Run, etc.) is utilized.

---

## SECTION 2 — PROPOSED POLICIES FOR ETHICS REVIEW

*The following policy proposals are prepared for formal review by your target ethics committee:*

### ED-06 — Data Retention Proposal
`PROPOSED — NOT YET APPROVED`  
- **Pseudonymous Research Records (`participants`, `final_decisions`, `messages`, `telemetry`):** Retained in secure, encrypted local storage for **5 years post-publication**, after which raw backend database files will be securely purged.
- **Financial Compensation Records (PII):** N/A — Participation is strictly voluntary without monetary compensation or external panel platform PII collection.
- **Screening & Baseline Records:** Retained in pseudonymous form for 5 years post-publication.
- **Analysis Datasets & Code:** Anonymized statistical datasets and R/Python analysis code deposited in permanent open science archives (e.g. OSF / Zenodo).

---

### ED-07 — Participant Withdrawal & Data Deletion Proposal
`PROPOSED — NOT YET APPROVED`  
1. **Withdrawal Before Task Completion:** If a participant exits during the session, their active database row will be deleted from the backend server upon request, purging all associated incomplete task, survey, and telemetry entries.
2. **Withdrawal After Task Completion:** Completed sessions included in an anonymized, aggregated dataset for statistical analysis cannot be selectively deleted post-analysis.
3. **Internal Database Deletion:** Cascading SQL delete query purges all relational rows matching `participants.participant_id`.
4. **Externally Transmitted AI Prompts:** User prompts and task text already transmitted to the Google Gemini API **cannot be recalled or deleted from Google's transit logs**. Participants are explicitly informed of this technical boundary on the informed consent form.

---

### ED-08 — Failed Screening Data Handling Proposal
`PROPOSED — NOT YET APPROVED`  
- **Eligibility Determination:** Screening responses ($0\text{--}3$ score on English and Hindi passages) are evaluated immediately on screen S2 to branch participants to onboarding or exclusion.
- **Privacy Minimization:** Raw MCQ answer selections of ineligible participants will be deleted from backend storage.
- **Aggregate Audit Record:** Anonymized pass/fail counts (without IP hashes, timestamps, or raw answers) will be retained strictly to calculate CONSORT participant flow diagrams and screening attrition statistics for publication.

---

### ED-09 — Open Data Sharing Proposal
`PROPOSED — NOT YET APPROVED`  
- **Prioritized Assets for Open Release:**
  1. Open-Source Web Application Codebase (`github.com/Tani-2005/AI-mediated-information-inequality-across-languages`).
  2. R and Python Statistical Analysis Scripts (LMM models, orthogonal linear contrasts).
  3. Synthetic / Example Demonstration Datasets (`scratch/` logs).
  4. Protocol and Ethics Documentation.
- **Participant-Level Data Protection:** Raw individual participant files containing free-text chat prompts or timestamps will **NOT** be publicly released. Only fully anonymized, non-identifiable numerical summary matrices may be deposited on open research repositories (OSF / Zenodo), subject to institutional ethics committee approval.

---

## SECTION 3 — INSTITUTIONAL INFORMATION REQUIRED

*The following items cannot be determined independently by the researcher and require guidance from your university / institutional ethics office:*

- [ ] **Ethics Committee Official Name:** `INSTITUTIONAL INPUT REQUIRED`
- [ ] **Application Submission Portal / Workflow:** `INSTITUTIONAL INPUT REQUIRED`
- [ ] **Required Standard Ethics Application Form:** `INSTITUTIONAL INPUT REQUIRED`
- [ ] **Formal Risk Level Classification:** `INSTITUTIONAL INPUT REQUIRED` (Proposed: Low / Minimal Risk)
- [ ] **Mandatory Data Archiving Period:** `INSTITUTIONAL INPUT REQUIRED`
- [ ] **Mandatory Withdrawal Wording & Rights:** `INSTITUTIONAL INPUT REQUIRED`
- [ ] **Independent Ethics Complaints Contact Email/Phone:** `INSTITUTIONAL INPUT REQUIRED`
- [ ] **Data Protection / GDPR / DPA Compliance Requirements:** `INSTITUTIONAL INPUT REQUIRED`
- [ ] **International Data Transfer & External API Policy Approval:** `INSTITUTIONAL INPUT REQUIRED`
- [ ] **Supervisor / Departmental Sign-off Requirements:** `INSTITUTIONAL INPUT REQUIRED`
- [ ] **Required Data Hosting Jurisdiction Constraints:** `INSTITUTIONAL INPUT REQUIRED`

---

## SECTION 4 — GEMINI PRIVACY & DATA USE VERIFICATION (ED-11)

**Exact Provider Product / Service:**  
Google Gemini API (`generativelanguage.googleapis.com/v1beta/openai` endpoint).

**Official Documentation Source:**  
- **Document Title:** *Google AI Studio and Gemini API Terms of Service*
- **URL:** `https://ai.google.dev/terms`
- **Verification Date:** September 27, 2026
- **Relevant Section:** Section 3 (*Data Rights, Governance & Privacy*)

**Official Data Terms & Billing Requirement:**
1. **Free-Tier API Keys:** Prompts and generated responses submitted using free-tier API keys MAY be logged and reviewed by human reviewers to train and improve Google models.
2. **Paid / Billing-Enabled API Projects (Pay-As-You-Go):** When an API key belongs to a Google Cloud project with **billing enabled (Paid Tier)**, Google's official documentation explicitly states:  
   *"Google does not use your prompts or responses to train Google models."*

**Research Compatibility Finding:**  
- The planned use is **COMPATIBLE with participant data privacy constraints ONLY IF deployed using a paid, billing-enabled Gemini API project**. Using a free-tier key is strictly prohibited for human participant data.

**Technical Boundaries & Limitations:**  
- `NOT ESTABLISHED BY CURRENT OFFICIAL DOCUMENTATION`: Standard Google Gemini API documentation does not publish specific log retention duration windows or provide API endpoints for retroactively purging payload logs from Google transit infrastructure.

---

## SECTION 5 — FINAL BLOCKERS REGISTER

| Item | Owner | Status | Blocking? |
| :--- | :--- | :--- | :--- |
| **PI & Investigator Details** | Researcher | Unresolved | **YES** |
| **Institution Name** | Researcher | Unresolved | **YES** |
| **Ethics Committee Name** | Institution | Unresolved | **YES** |
| **Compensation Rate** | Researcher | Resolved (No Compensation) | **NO** |
| **Recruitment Panel Vendor** | Researcher | Resolved (Voluntary / No Vendor) | **NO** |
| **Data Retention Period** | Institution | Unresolved | **YES** |
| **Withdrawal Policy** | Institution | Unresolved | **YES** |
| **Screening Data Policy** | Institution | Unresolved | **YES** |
| **Open Data Policy** | Institution | Unresolved | **YES** |
| **Production Cloud Hosting** | Researcher | Resolved (Local / Self-Hosted) | **NO** |
| **Gemini Billing Verification** | Researcher / Tech | Verify Paid Tier Billing | **YES** |
| **Ethics Complaints Contact** | Institution | Unresolved | **YES** |

---

## SECTION 6 — NEXT ACTION

```text
NEXT ACTION: RESEARCHER MUST COMPLETE THE DECISION WORKSHEET AND IDENTIFY THE TARGET INSTITUTION/ETHICS REVIEW PATH.
```

```text
No participant recruitment or human data collection may begin until formal ethics approval is obtained.
```
