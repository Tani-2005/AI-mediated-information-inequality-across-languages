# Ethics Submission Action List & Pre-Flight Roadmap

**Protocol Version:** `1.1.0-gemini-frozen`  
**Study Identifier:** `ENGLISH_HINDI_AI_INFO_INEQUALITY_2026`  
**Status:** RESEARCHER DECISIONS RESOLVED — READY FOR INSTITUTIONAL ETHICS REVIEW  

---

## 1. BLOCKING BEFORE ETHICS SUBMISSION

The following administrative items must be populated before final submission to the review board:

1. **Populate Researcher Identity (ED-01):** Insert Principal Investigator name, institutional email, academic department, and university name into `ethics_application.md` and `participant_information_sheet.md`.
2. **Identify Ethics Review Board (ED-02):** Select target Institutional Review Board (IRB) or Institutional Ethics Committee (IEC).
3. **Formulate Institutional Policies (ED-06, ED-07, ED-08, ED-09):** Submit institutional proposals for data retention duration, withdrawal deletion rules, screening failure data handling, and open data sharing for IEC approval.
4. **Ensure Paid Gemini API Billing (ED-11):** Confirm project uses a billing-enabled Google Gemini API key to ensure data non-training compliance.

*Note:* ED-03 (No compensation), ED-04 (Voluntary academic recruitment), and ED-10 (Local self-hosted architecture) are finalized by researcher decision.

---

## 2. REQUIRES INSTITUTIONAL DECISION

The target Institutional Review Board / Ethics Committee must formally decide and approve:

1. **Mandatory Data Retention Period (ED-06):** Duration research records must be archived post-publication (e.g. 5 vs 10 years).
2. **Withdrawal Data Policy (ED-07):** Approval of ITT retention vs database purge upon participant withdrawal.
3. **Screening Failure Retention (ED-08):** Approval to retain anonymized screening pass/fail counts for CONSORT reporting.
4. **Open Data Release (ED-09):** Approval to publish de-identified response matrices on public repositories (OSF/Zenodo).
5. **Ethics Complaints Contact (ED-12):** Institutional ethics contact details to be listed on participant information sheets.

---

## 3. FINALIZED RESEARCHER DECISIONS

The Principal Investigator has established:

1. **Participant Compensation (ED-03):** `RESOLVED` — Voluntary participation, no monetary compensation.
2. **Recruitment Method (ED-04):** `RESOLVED` — Voluntary academic recruitment / no paid panel vendor.
3. **Infrastructure Architecture (ED-10):** `RESOLVED` — Local self-hosted deployment (Participant Browser → Local React/Vite → Local FastAPI → Local PostgreSQL database, with Google Gemini API as the only external service).
4. **PI & Supervisor Names (ED-01):** Administrative details to be inserted into submission templates.

---

## 4. REQUIRES EXTERNAL VERIFICATION

Completed against official provider documentation:

1. **Google Gemini API Privacy Terms (ED-11):**  
   - *Status:* **EXTERNALLY VERIFIED.**  
   - *Requirement:* Production deployment MUST use a Paid / Billing-Enabled Gemini API project. Google terms state that prompts/responses are NOT used for model training under paid API tiers. Free-tier API keys MUST NOT be used.

---

## 5. CAN BE COMPLETED AFTER APPROVAL / DURING PILOT

The following items are deferred until formal ethics approval is granted:

1. **Execute $N=6\text{--}10$ Human Pilot:** Run approved pilot testing to establish empirical session duration baseline (ED-05).
2. **Finalize Local PostgreSQL Deployment:** Verify local database setup on self-hosted research server.
3. **Initiate Participant Recruitment:** Post voluntary recruitment notice on approved academic channels ONLY after receiving formal ethics approval certificate.

