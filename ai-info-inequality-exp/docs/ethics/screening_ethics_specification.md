# Screening & Eligibility Ethics Specification

**Protocol Version:** `1.1.0-gemini-frozen`  
**Study Identifier:** `ENGLISH_HINDI_AI_INFO_INEQUALITY_2026`  
**Status:** DRAFT COMPLETE — OPEN ETHICS DECISION REMAIN  

---

## 1. Screening Purpose & Rationale

To ensure that all randomized participants possess sufficient bilingual reading comprehension to meaningfully interact in any assigned language arm (`ENGLISH_ONLY`, `HINDI_ONLY`, or `CODE_SWITCHING`), participants undergo a standardized bilingual reading comprehension screening on screen S2.

---

## 2. Screening Instruments & Variables

1. **English Comprehension Sub-Test:**  
   - Instrument: Short passage describing civic entitlement rules followed by 3 Multiple-Choice Questions (`q1`, `q2`, `q3`).  
   - Scoring: 1 point per correct response (Score range: 0 to 3).  
   - Pass threshold: $\ge 2 / 3$.

2. **Hindi Comprehension Sub-Test:**  
   - Instrument: Short passage in Devanagari script describing civic entitlement rules followed by 3 Multiple-Choice Questions (`q4`, `q5`, `q6`).  
   - Scoring: 1 point per correct response (Score range: 0 to 3).  
   - Pass threshold: $\ge 2 / 3$.

---

## 3. Exclusion Logic & Participant Flow

- **Pass Condition:** Participant MUST score $\ge 2/3$ on the English sub-test **AND** $\ge 2/3$ on the Hindi sub-test.
- **Exclusion Condition:** Participants scoring $< 2/3$ on either sub-test are immediately flagged as `EXCLUDED` (`participant.status = "EXCLUDED"`).
- **Participant Messaging:** Excluded participants view a polite notification: *"Thank you for your interest. Based on screening criteria, you are not eligible to complete this study session."* They are prevented from proceeding to LEAP-Q, AILS, or arm randomization.

---

## 4. Open Ethics Decisions Regarding Screening Data

### 4.1 Handling & Retention of Failed Screening Data
`ETHICS DECISION REQUIRED`  
- **Option A (Immediate Purge):** Permanently delete all screening responses and IP hashes for ineligible participants immediately upon screening failure.  
- **Option B (Anonymized Aggregate Log):** Retain anonymized screening pass/fail counts (without IP hashes or timestamps) to document CONSORT screening flow and report attrition rates in academic publications.

### 4.2 Screening Failure Policy
- In accordance with the study policy, participation is voluntary and no monetary compensation is provided to any participant regardless of screening outcome.

---

## 5. Fairness, Accessibility & Non-Discrimination

- **Objective Criteria:** Screening evaluates basic functional reading comprehension using standardized factual passages.
- **Language Rights:** Tests ensure participants are not randomized into a language condition in which they cannot read or comprehend basic civic instructions.
- **Non-Discrimination:** Exclusions are based solely on task-relevant reading comprehension thresholds and digital literacy requirements.
