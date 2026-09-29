# Final Ethics Package Status & Consistency Determination

**Protocol Version:** `1.1.0-gemini-frozen`  
**Study Identifier:** `ENGLISH_HINDI_AI_INFO_INEQUALITY_2026`  
**Target Architecture:** Local React/Vite → Local FastAPI → Local PostgreSQL (Google Gemini API over HTTPS as sole external network service)  
**Final Status:** `ETHICS PACKAGE READY FOR INSTITUTIONAL SUBMISSION`

---

## 1. Executive Summary & Audit Overview

The final ethics consistency audit and cleanup of the research ethics package (`docs/ethics/`) is complete. All stale decisions, cloud deployment references, paid panel vendor requirements, and definitive self-classification wording have been reconciled to align strictly with frozen Protocol v1.1.0, established researcher decisions, and the local self-hosted deployment architecture.

No modifications were made to research questions, hypotheses, sample size ($N = 144$ complete, $N = 171$ target recruitment), experimental arms (`ENGLISH_ONLY`, `HINDI_ONLY`, `CODE_SWITCHING`), civic task scenarios, randomization logic, AILS thresholding ($<36 = \text{LOW}$, $\ge 36 = \text{HIGH}$), scoring logic, telemetry definitions, Gemini LLM prompts, model configurations, or application codebase.

---

## 2. Researcher Decisions Finalized

The Principal Investigator / Research Team has finalized the following 4 core decisions:

1. **ED-03 (Participant Compensation):** `RESOLVED (NO PARTICIPANT COMPENSATION)`  
   Participation is entirely voluntary without monetary compensation, financial incentives, or performance-based rewards.
2. **ED-04 (Recruitment Methodology):** `RESOLVED (VOLUNTARY ACADEMIC RECRUITMENT)`  
   Recruitment relies on voluntary academic notices, departmental bulletin boards, and approved volunteer outreach. No paid panel vendor (e.g. Prolific, Qualtrics Panel) is used.
3. **ED-10 (Infrastructure Architecture):** `RESOLVED (LOCAL / SELF-HOSTED DEPLOYMENT)`  
   The application runs entirely locally on a self-hosted research machine (`Participant Browser → Local React/Vite → Local FastAPI → Local PostgreSQL`). No cloud-hosted app server, cloud database, AWS, GCP, Azure, or Firebase is used.
4. **ED-11 (LLM Data Privacy Terms):** `RESOLVED (PAID GEMINI API TIER)`  
   Production deployment mandates a billing-enabled Google Gemini API project. Under Google Cloud terms of service for paid API tiers, customer prompts and responses are **not** logged, retained for model training, or used for product improvement.

---

## 3. Institutional Decisions Still Open (Submitted to IEC/IRB)

The following 5 decisions remain open institutional-policy questions to be formally determined by the reviewing Institutional Ethics Committee (IEC) / Institutional Review Board (IRB):

1. **ED-06 (Mandatory Data Retention Period):** Archive pseudonymous research data for 5 years (proposed) vs 10 years post-publication.
2. **ED-07 (Participant Withdrawal Policy):** Retain pseudonymous Intention-To-Treat (ITT) data collected prior to withdrawal (proposed) vs complete database purge upon withdrawal request.
3. **ED-08 (Screening Failure Data Retention):** Retain pseudonymous pass/fail screening counts for CONSORT reporting (proposed) vs immediate purge.
4. **ED-09 (Open Data Sharing Policy):** Publish de-identified response matrices on public repositories (OSF/Zenodo) upon peer-reviewed publication (proposed).
5. **ED-12 (Independent Complaints Contact):** IEC secretary email and phone number to be populated on final participant information sheets.

---

## 4. External Ethics-Review Decisions Still Open

1. **Formal Risk Classification:**  
   The ethics package describes identified risks (cognitive fatigue, AI inaccuracies/misinformation, privacy in transit) and mitigation measures without independently declaring a final regulatory classification. Formal risk classification rests entirely with the reviewing IEC/IRB.
2. **Approval Certificate:**  
   Formal clearance and issuance of the institutional ethics protocol approval certificate prior to human participant recruitment.

---

## 5. Explicit Audit Confirmations

| # | Domain | Audit Finding / Confirmation | Status |
|---|---|---|---|
| **1** | **Infrastructure** | **Local / Self-Hosted Architecture:** Confirmed across all ethics documents (`Participant Browser → Local React/Vite → Local FastAPI → Local PostgreSQL`). Google Gemini API over HTTPS is the sole external network service. Zero cloud servers, cloud databases, or region requirements. | **CONFIRMED** |
| **2** | **Compensation** | **No Participant Compensation:** Confirmed across all participant-facing and administrative ethics documents (`ethics_application.md`, `participant_information_sheet.md`, `recruitment_notice.md`, `screening_ethics_specification.md`, `data_management_plan.md`). Participation is 100% voluntary with zero monetary payment or financial handles. | **CONFIRMED** |
| **3** | **Recruitment** | **Volunteer Recruitment / No Paid Panel:** Confirmed that recruitment uses voluntary academic notices without paid panel vendors (Prolific, Qualtrics Panel). Neutral recruitment copy preserves the blind by avoiding disclosure of the language-disadvantage hypothesis. | **CONFIRMED** |
| **4** | **Risk Classification** | **Classification Left to Ethics Authority:** All definitive self-classifications ("This study is Minimal Risk") replaced with neutral wording stating that identified risks are described, while formal risk classification rests with the reviewing IEC/IRB. | **CONFIRMED** |
| **5** | **NASA-TLX Protocol** | **Per-Task Repeated Measurements Documented:** Confirmed that all ethics documents (`ethics_application.md`, `participant_information_sheet.md`, `screening_ethics_specification.md`, `ethics_decision_resolution_matrix.md`) explicitly document that NASA-TLX workload is measured 3 times per session—immediately following each of the 3 civic tasks. | **CONFIRMED** |

---

## 6. Audit Term Consistency Table (Search Results Across `docs/ethics/`)

The table below catalogs every remaining occurrence of audited terms across all files in `docs/ethics/` following final cleanup:

| Audited Term | File | Line | Context / Content Summary | Consistency Status |
|---|---|---|---|---|
| `compensation` | `screening_ethics_specification.md` | L45 | States participation is voluntary with no monetary compensation provided. | **CORRECT** |
| `compensation` | `recruitment_notice.md` | L30 | States participation is voluntary without monetary compensation. | **CORRECT** |
| `compensation` | `participant_information_sheet.md` | L61 | States participation is entirely voluntary; no monetary compensation provided. | **CORRECT** |
| `compensation` | `final_researcher_decision_worksheet.md` | L30 | ED-03 resolved: No monetary compensation. | **CORRECT** |
| `compensation` | `final_researcher_decision_worksheet.md` | L56 | Financial records: N/A (no monetary compensation or PII collected). | **CORRECT** |
| `compensation` | `ethics_submission_readiness_package.md` | L38 | Confirms ED-03 resolved: Voluntary participation without monetary compensation. | **CORRECT** |
| `compensation` | `ethics_submission_readiness_package.md` | L113 | Confirms zero financial payment handles or participant PII collected. | **CORRECT** |
| `compensation` | `ethics_submission_action_list.md` | L38 | Documents ED-03 finalized as voluntary participation, no monetary compensation. | **CORRECT** |
| `compensation` | `ethics_open_decisions.md` | L15 | ED-03 status: `RESOLVED: No monetary compensation`. | **CORRECT** |
| `compensation` | `ethics_decision_resolution_matrix.md` | L16, L84 | ED-03 status: `RESOLVED — NO MONETARY COMPENSATION`. | **CORRECT** |
| `compensation` | `ethics_application.md` | L149, L156 | Section 14 confirms no monetary or financial compensation is provided. | **CORRECT** |
| `compensation` | `data_management_plan.md` | L15, L26 | Tier 1 & Section 3 confirm N/A (No compensation or payment PII collected). | **CORRECT** |
| `recruitment vendor` | `ethics_application.md` | L42 | Section 4 confirms voluntary academic recruitment / no paid panel vendor used. | **CORRECT** |
| `recruitment vendor` | `final_researcher_decision_worksheet.md` | L37 | ED-04 policy confirms no paid recruitment panel vendor is used. | **CORRECT** |
| `recruitment vendor` | `ethics_open_decisions.md` | L16 | ED-04 resolved: Voluntary recruitment / no paid vendor. | **CORRECT** |
| `recruitment vendor` | `ethics_decision_resolution_matrix.md` | L17 | ED-04 resolved: Voluntary recruitment / no paid vendor. | **CORRECT** |
| `recruitment vendor` | `ethics_submission_readiness_package.md` | L172 | ED-04 resolved: Voluntary academic recruitment / no paid panel vendor. | **CORRECT** |
| `recruitment vendor` | `ethics_submission_action_list.md` | L18 | ED-04 finalized: Voluntary academic recruitment / no paid vendor. | **CORRECT** |
| `Prolific` | `final_researcher_decision_worksheet.md` | L37 | Documents ED-04 decision: No paid panel vendor (e.g. Prolific or Qualtrics Panel) used. | **CORRECT (Negative Context)** |
| `Prolific` | `ethics_open_decisions.md` | L16 | Documents ED-04 resolution: Voluntary recruitment replaces paid panels (Prolific/Qualtrics). | **CORRECT (Negative Context)** |
| `Prolific` | `ethics_decision_resolution_matrix.md` | L17 | Documents ED-04 resolution: Voluntary recruitment replaces paid panels (Prolific/Qualtrics). | **CORRECT (Negative Context)** |
| `Qualtrics Panel` | `final_researcher_decision_worksheet.md` | L37 | Documents ED-04 decision: No paid panel vendor (e.g. Prolific or Qualtrics Panel) used. | **CORRECT (Negative Context)** |
| `Qualtrics Panel` | `ethics_open_decisions.md` | L16 | Documents ED-04 resolution: Voluntary recruitment replaces paid panels (Prolific/Qualtrics). | **CORRECT (Negative Context)** |
| `Qualtrics Panel` | `ethics_decision_resolution_matrix.md` | L17 | Documents ED-04 resolution: Voluntary recruitment replaces paid panels (Prolific/Qualtrics). | **CORRECT (Negative Context)** |
| `cloud hosting` | `ethics_application.md` | L217 | Confirms local architecture; no cloud hosting for app or DB is utilized. | **CORRECT (Negative Context)** |
| `cloud hosting` | `data_management_plan.md` | L41 | Confirms local PostgreSQL; no cloud hosting for app or DB is utilized. | **CORRECT (Negative Context)** |
| `cloud hosting` | `final_researcher_decision_worksheet.md` | L145 | ED-10 resolved: Local / Self-Hosted (No production cloud hosting). | **CORRECT (Negative Context)** |
| `cloud database` | `final_researcher_decision_worksheet.md` | L45 | Confirms no cloud-hosted app or managed cloud database is utilized. | **CORRECT (Negative Context)** |
| `cloud database` | `ethics_decision_resolution_matrix.md` | L45 | Confirms no cloud-hosted app server or managed cloud database is utilized. | **CORRECT (Negative Context)** |
| `database region` | *None* | N/A | 0 occurrences remaining. | **CORRECT** |
| `AWS` / `GCP` / `Azure` / `Firebase` | `final_researcher_decision_worksheet.md` | L45 | Documents that AWS, GCP, Azure, Firebase are NOT utilized under ED-10. | **CORRECT (Negative Context)** |
| `AWS` / `GCP` / `Azure` / `Firebase` | `ethics_decision_resolution_matrix.md` | L45 | Documents that AWS, GCP, Azure, Firebase are NOT utilized under ED-10. | **CORRECT (Negative Context)** |
| `minimal risk` | `ethics_application.md` | L143 | Section 13 states formal risk classification rests with reviewing IEC (proposed: Low / Minimal Risk). | **CORRECT** |
| `minimal risk` | `risk_assessment.md` | L25 | Section 1 states formal classification rests with reviewing IEC (proposed: Low / Minimal Risk). | **CORRECT** |
| `minimal risk` | `participant_information_sheet.md` | L71 | Section 9 states formal classification rests with reviewing IEC. | **CORRECT** |
| `minimal risk` | `final_researcher_decision_worksheet.md` | L97 | ED-05/Risk states formal risk level classification is IEC input required (proposed: Low / Minimal Risk). | **CORRECT** |

---

## 7. Final Submission Blockers Assessment

### Blockers Remaining Prior to Ethics Submission: ZERO

1. **Protocol Consistency:** 100% Consistent with Protocol v1.1.0-gemini-frozen.
2. **Infrastructure Parity:** 100% Consistent with local self-hosted deployment.
3. **Compensation Parity:** 100% Consistent with voluntary non-monetary participation.
4. **Recruitment Parity:** 100% Consistent with voluntary academic recruitment.
5. **Risk Wording Parity:** 100% Deferred to reviewing IEC/IRB authority.
6. **Administrative Template Fields:** `[Insert PI Name]`, `[Insert Target IEC]` placeholders are available for direct insertion upon formal portal upload.

---

## 8. Final Status Determination

```text
ETHICS PACKAGE READY FOR INSTITUTIONAL SUBMISSION
```

*The ethics submission package is fully reconciled, internally consistent, and ready for submission to the target Institutional Ethics Committee / Institutional Review Board.*
