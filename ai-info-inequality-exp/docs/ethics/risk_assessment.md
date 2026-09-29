# Comprehensive Risk Register

**Study Title:** Linguistic Inequality in AI-Mediated Information Seeking: An English-Hindi Randomized Controlled Trial  
**Protocol Version:** `1.1.0-gemini-frozen`  
**Study Identifier:** `ENGLISH_HINDI_AI_INFO_INEQUALITY_2026`  

---

## Risk Register Matrix

| ID | Risk Description | Participant Impact | Likelihood | Severity | Mitigation Strategy | Residual Risk |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **R-01** | **Inaccurate AI Output:** LLM generates incorrect or misleading scheme eligibility rules. | Participant relies on incorrect rules during task decision. | High | Low | Tasks are hypothetical simulations; onboarding warnings provided; official scheme links provided in debrief. | Minimal |
| **R-02** | **Civic Misinformation:** Participant misinterprets research tasks as personal welfare application. | Participant makes real-world financial or welfare decisions based on AI prompts. | Low | Medium | Explicit disclaimers on consent screen, onboarding, and debriefing; no real personal data collected. | Minimal |
| **R-03** | **Mental Fatigue / Burden:** Completing 3 entitlement tasks causes cognitive tiredness. | Participant experiences mild frustration or fatigue. | Moderate | Low | Enforced break screens between tasks; 6-item NASA-TLX workload monitoring; voluntary withdrawal allowed. | Low |
| **R-04** | **Language Discomfort:** Participant assigned to a less-preferred language condition. | Participant experiences mild communication difficulty. | Moderate | Low | Pre-screening requires demonstrated bilingual reading comprehension ($\ge 2/3$ in English & Hindi) before randomization. | Minimal |
| **R-05** | **Data Privacy Exposure:** Unauthorized access to participant database. | Breach of interaction logs or survey responses. | Low | Medium | Pseudonymous UUID v4 tracking; zero PII stored in DB; encrypted local PostgreSQL storage; salted IP hash. | Minimal |
| **R-06** | **Third-Party API Data Leak:** User prompts sent to Google Gemini API. | Exposure of prompt text to cloud API. | Low | Low | Zero PII or participant identifiers included in API payloads; backend-only proxy architecture. | Minimal |
| **R-07** | **API Service Interruption:** Gemini API timeout or HTTP 5xx failure during session. | Participant task session interrupted. | Low | Low | Backend retry logic (1 retry on 5xx/timeout); technical failure handling; replacement rule activated. | Minimal |
| **R-08** | **Demand Characteristics:** Participant infers research hypothesis and alters behavior. | Compromised research validity. | Moderate | Low | Neutral recruitment copy; detailed language comparison hypotheses withheld until debriefing. | Minimal |

---

## Risk Classification Summary
Formal risk classification rests with the reviewing Institutional Ethics Committee (proposed classification for review: Low / Minimal Risk based on identified mitigation factors).
