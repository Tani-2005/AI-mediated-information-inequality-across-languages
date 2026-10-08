# STAGE 12.5.1B — FINAL STATISTICAL & EVALUATOR CONSISTENCY AUDIT
## LINGUA-AUDIT: A Reproducible Framework for Auditing Information Inequality in Multilingual AI Systems

---

### 0. PURPOSE & SCIENTIFIC AUDIT STATUS

This artifact provides the mandatory **Final Statistical & Evaluator Consistency Audit** prior to authorizing Stage 12.5.2 (Evaluator Validation & Scoring Pilot). It resolves remaining statistical model mappings, nesting formulations, evaluator architecture boundaries, and cell-level outcome definitions across Issues A through P.

**HARD RULE ENFORCED:** Zero substantive model responses from the 5,400 production dataset (`stage12_4_full_evaluation_responses.json`) were scored, evaluated, or substantively inspected during this stage.

---

### 1. ISSUE-BY-ISSUE METHODOLOGICAL RESOLUTIONS

---

#### ISSUE A — M7 STATISTICAL MODEL RECONCILIATION

1. **Measurement Scale:** Semantic Preservation ($M_7$) is measured on a 5-point ordinal scale ($0, 1, 2, 3, 4$).
2. **Primary Statistical Model:** $M_7$ is formally mapped to a **Cumulative Link Mixed Model (CLMM)** with a logit link function:
   $$\text{logit}(P(M_7 \le c)) = \alpha_c - \mathbf{X}\boldsymbol{\beta} - u_{\text{Family}} - v_{\text{Task}}$$
3. **Proportional-Odds Assumption:** Checked via Brant test / likelihood-ratio test. If the proportional-odds assumption is violated, an unconstrained multinomial logit mixed model will be fitted.
4. **Sensitivity Model:** An LMM treatment (treating $0 \dots 4$ as pseudo-continuous) will be reported in secondary sensitivity analyses to verify that model family selection does not alter main effect conclusions.

---

#### ISSUE B — M8 CELL-LEVEL OUTCOME FRAMEWORK

1. **Observation Level Distinction:**
   - **Generation-Level Data ($N=5,400$):** Individual raw responses for tuple $(task_i, lang_k, model_m, rep_r)$.
   - **Cell-Level Data ($N_{\text{cell}}=1,800$):** Aggregated metrics computed across the 3 repetitions within each $(task_i, lang_k, model_m)$ cell.
2. **M8 Metrics Breakdown:**
   - **$M_{8\text{a}}$ Completeness Variance ($\sigma^2_{\text{Comp}}$):** Continuous non-negative $[0, \infty)$. Primary model: **Linear Mixed Model (LMM)** fitted on $\log(\sigma^2_{\text{Comp}} + 0.001)$ with identity link.
   - **$M_{8\text{b}}$ Critical Fact Jaccard Concordance ($J_{\text{CF}}$):** Bounded proportion $[0, 1]$. Primary model: **Beta GLMM** (or Binomial GLMM) with logit link.
3. **Cell-Level Fixed & Random Effects:**
   - Fixed effects: $\text{Lang} + \text{Model} + \text{Domain} + (\text{Lang} \times \text{Model})$.
   - Random effects: $(1 \mid \text{scenario\_family\_id} / \text{task\_id})$ at the 1,800 cell level.

---

#### ISSUE C — HIERARCHICAL NESTING & RANDOM EFFECTS FORMULATION

1. **Complete Nesting Hierarchy:**
   $$\text{Scenario Family } (j \in 1 \dots 25) \longrightarrow \text{Task } (i \in 1 \dots 150) \longrightarrow \text{Cell } (c \in 1 \dots 1800) \longrightarrow \text{Repetition } (r \in 1 \dots 3)$$
2. **Globally Unique Task Identifiers:** `task_id` values (e.g. `HLT-001` ... `GEN-030`) are globally unique. Therefore, $(1 \mid \text{scenario\_family\_id}) + (1 \mid \text{task\_id})$ is mathematically equivalent to nested $(1 \mid \text{scenario\_family\_id} / \text{task\_id})$.
3. **Generation-Level Model Notation:**
   $$\text{Random Effects Formula (Generation-Level):} \quad (1 \mid \text{scenario\_family\_id}) + (1 \mid \text{task\_id}) + (1 \mid \text{cell\_id})$$
   Where `cell_id = task_id:language:model`.
4. **Overparameterization Safeguard:** Redundant random slopes are excluded. If random intercept models exhibit singular fit, the `cell_id` intercept is collapsed into residual covariance.

---

#### ISSUE D — M1 BINOMIAL AGGREGATION SPECIFICATION

1. **Binomial Formulation:** Factual Precision ($M_1$) is implemented using standard two-column binomial response syntax:
   $$\text{Response Variable:} \quad \text{cbind}(N_{\text{Supported}}, N_{\text{Contradicted}} + N_{\text{Unsupported}})$$
2. **Statistical Observation Level:** Response-level observations ($N=5,400$) under a **Binomial GLMM** with logit link.
3. **Denominator Visibility:** The statistical model directly weights each response by its total claim count, preventing short responses with 1 claim from being treated as equivalent in precision variance to long responses with 15 claims.

---

#### ISSUE E — M3 BINOMIAL SPECIFICATION & DIRECTIONALITY

1. **Binomial Formulation:** Critical Information Omission ($M_3$) is implemented as:
   $$\text{Response Variable:} \quad \text{cbind}(N_{\text{Missing\_CF}}, N_{\text{Total\_CF}} - N_{\text{Missing\_CF}})$$
2. **Directionality Standard:**
   - Event modeled = Critical Fact missing or distorted.
   - **Higher $M_3$ = WORSE information access.**
   - Estimated marginal contrast $\Delta_{\text{Hindi}} = M_3(\text{Hindi}) - M_3(\text{English}) > 0$ represents a detrimental linguistic disparity.

---

#### ISSUE F — M4 ERROR COUNT & RATE TAXONOMY

Factual Error ($M_4$) is partitioned into three distinct statistical outcomes:

1. **$M_{4\text{a}}$ Factual Error Count (Count $\{0, 1, 2 \dots\}$):** Primary model: **Negative Binomial GLMM** with log link. Diagnostic alternative: Poisson GLMM with overdispersion test ($c_{\text{hat}}$).
2. **$M_{4\text{b}}$ Any-Error Binary Indicator ($\{0, 1\}$):** Primary model: **Binomial GLMM** with logit link ($\mathbf{1}(\text{Error Count} > 0)$).
3. **$M_{4\text{c}}$ Claim-Normalized Error Rate:** Primary model: **Negative Binomial GLMM** with log link and offset $\log(\text{Total Verifiable Claims})$.

---

#### ISSUE G — M5 CITATION AGGREGATION RULE

For responses containing multiple citations, response-level Citation Quality ($M_5 \in \{0, 1, 2, 3, 4\}$) is evaluated using a **Hierarchical Best-Supported Claim Rule**:

1. **Grade 4 (Authoritative Official Supporting Citation):** At least one citation is a direct, verified link/reference to the primary official source (e.g., `pmjay.gov.in`) and accurately supports its corresponding claim.
2. **Grade 3 (Correct Supporting Citation):** At least one citation is a real, relevant official document/portal that accurately supports its corresponding claim.
3. **Grade 2 (Present but Non-Supporting / Irrelevant):** Citations are present, but none support their corresponding asserted claims (including authoritative sources cited irrelevantly).
4. **Grade 1 (Format Only / Hallucinated Source):** Citations are present, but all cited sources/URLs are fabricated or non-existent.
5. **Grade 0 (No Citation):** Response contains zero source citations.

---

#### ISSUE H — EVALUATOR REPRODUCIBILITY & CONFIGURATION STATEMENT

1. **Terminology Standard:** The evaluation setup is formally designated as a **FIXED AUTOMATED EVALUATION CONFIGURATION**.
2. **Reproducibility Statement:** While running `gpt-4o-2024-08-06` under $T=0.0$ yields high empirical consistency (>99% output identity), external commercial API endpoints do not guarantee bitwise mathematical determinism. This is explicitly documented as a reproducibility limitation.

---

#### ISSUE I — EVALUATOR MODEL OVERLAP & SENSITIVITY AUDIT

1. **Primary Evaluator:** `gpt-4o-2024-08-06` evaluates all 5,400 responses (blinded to target model identity).
2. **Independent Cross-Evaluator Sensitivity:** On the $N=270$ validation subset, an independent cross-evaluator running `claude-3-5-sonnet-20241022` will score responses. Inter-evaluator agreement ($\text{ICC} \ge 0.85$) and target-model ranking invariance will be verified to ensure GPT-4o evaluator self-bias does not distort findings.

---

#### ISSUE J — TWO-STAGE CLAIM EXTRACTION & VERIFICATION

1. **Stage 1 (Atomic Claim Extraction):** `gpt-4o-2024-08-06` parses raw text into a JSON list of atomic claim strings.
2. **Stage 2 (Factual Verification):** `gpt-4o-2024-08-06` maps extracted claims against benchmark ground truth to output `SUPPORTED`, `CONTRADICTED`, or `UNSUPPORTED`.
3. **Correlated Error Risk:** Correlated LLM extraction-verification error is acknowledged as a structural limitation and audited against human labels on the $N=270$ validation sample.

---

#### ISSUE K — UNVERIFIABLE CLAIM TREATMENT

1. **Primary Rule:** `UNSUPPORTED` claims are retained in the $M_1$ denominator as un-evidenced assertions ($M_1 = \frac{N_{\text{Supported}}}{N_{\text{Supported}} + N_{\text{Contradicted}} + N_{\text{Unsupported}}}$).
2. **Sensitivity Metric:** Contradiction-only precision ($M_{1\text{b}} = \frac{N_{\text{Supported}}}{N_{\text{Supported}} + N_{\text{Contradicted}}}$) is reported in secondary sensitivity analyses.

---

#### ISSUE L — M2a VS. M2c COMPLETENESS ENDPOINTS

1. **Primary Endpoint:** $M_{2\text{a}}$ (Critical Fact Coverage, unweighted) is confirmed as the primary completeness endpoint for all confirmatory hypothesis tests.
2. **Secondary Endpoint:** $M_{2\text{c}}$ (Weighted Completeness $1.0 : 0.5$) is retained solely as a sensitivity convention.

---

#### ISSUE M — RESPONSE TOKEN LENGTH AS MEDIATOR

1. **Role:** `TokenCount` is classified strictly as a descriptive covariate and potential mediator.
2. **Causal Models:** Excluded from primary causal models; included as $\log(\text{TokenCount})$ in secondary sensitivity models.

---

#### ISSUE N — MULTIPLE COMPARISON FAMILIES

1. **Family 1 (Primary Confirmatory):** $M_1, M_{2\text{a}}, M_3 \times (\text{Hindi vs EN}, \text{CS vs EN})$ ($6 \text{ tests}$). Holm-Bonferroni correction at $\alpha=0.05$.
2. **Family 2 (Secondary Metrics):** $M_{4\text{a}}, M_5, M_6, M_7, M_{8\text{a}} \times (\text{Hindi vs EN}, \text{CS vs EN})$ ($10 \text{ tests}$). Benjamini-Hochberg FDR at $q=0.05$.
3. **Family 3 (Interactions):** Language $\times$ Model and Language $\times$ Domain terms. Benjamini-Hochberg FDR at $q=0.05$.

---

#### ISSUE O — PRIMARY ESTIMAND DEFINITION

The primary reported result for all mixed models is the **Estimated Marginal Means (EMM) Contrast** ($\Delta_{\text{EMM}}$), calculated conditional on random effect distributions:
$$\Delta_{\text{EMM, Hindi-EN}} = \hat{\mathbb{E}}[M \mid \text{Hindi}] - \hat{\mathbb{E}}[M \mid \text{English}]$$

---

#### ISSUE P — PRIMARY EFFECT DIRECTION STANDARDS

- **Higher = BETTER:** $M_1, M_{2\text{a}}, M_{2\text{c}}, M_5, M_7, M_{8\text{b}}$. ($\Delta < 0 \implies$ Detrimental Disparity).
- **Higher = WORSE:** $M_3, M_{4\text{a}}, M_{4\text{b}}, M_{4\text{c}}, M_6, M_{8\text{a}}$. ($\Delta > 0 \implies$ Detrimental Disparity).

---

### 2. DEFINITIVE STATISTICAL SPECIFICATION TABLE

| Metric Code | Metric Name | Observation Unit | Outcome Scale | Primary Statistical Model | Distribution & Link | Fixed Effects | Random Effects | Primary Estimand ($\Delta_{\text{EMM}}$) | Direction | Family |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **$M_1$** | Factual Precision | Generation ($N=5.4\text{k}$) | Proportion $[0, 1]$ | Binomial GLMM | Binomial (Logit) | $\text{Lang} + \text{Model} + \text{Domain} + (\text{L} \times \text{M})$ | $(1|\text{family}) + (1|\text{task}) + (1|\text{cell})$ | $\text{EMM}_{\text{Hindi}} - \text{EMM}_{\text{EN}}$ | Higher = Better | Family 1 |
| **$M_{2\text{a}}$** | Critical Fact Coverage | Generation ($N=5.4\text{k}$) | Proportion $[0, 1]$ | Linear Mixed Model (LMM) | Gaussian (Identity) | $\text{Lang} + \text{Model} + \text{Domain} + (\text{L} \times \text{M})$ | $(1|\text{family}) + (1|\text{task}) + (1|\text{cell})$ | $\text{EMM}_{\text{Hindi}} - \text{EMM}_{\text{EN}}$ | Higher = Better | Family 1 |
| **$M_{2\text{c}}$** | Weighted Completeness | Generation ($N=5.4\text{k}$) | Proportion $[0, 1]$ | Linear Mixed Model (LMM) | Gaussian (Identity) | $\text{Lang} + \text{Model} + \text{Domain} + (\text{L} \times \text{M})$ | $(1|\text{family}) + (1|\text{task}) + (1|\text{cell})$ | $\text{EMM}_{\text{Hindi}} - \text{EMM}_{\text{EN}}$ | Higher = Better | Sensitivity |
| **$M_3$** | Critical Omission Rate | Generation ($N=5.4\text{k}$) | Proportion $[0, 1]$ | Binomial GLMM | Binomial (Logit) | $\text{Lang} + \text{Model} + \text{Domain} + (\text{L} \times \text{M})$ | $(1|\text{family}) + (1|\text{task}) + (1|\text{cell})$ | $\text{EMM}_{\text{Hindi}} - \text{EMM}_{\text{EN}}$ | Higher = Worse | Family 1 |
| **$M_{4\text{a}}$** | Factual Error Count | Generation ($N=5.4\text{k}$) | Count $\{0, 1, 2 \dots\}$ | Negative Binomial GLMM | NegBin (Log) | $\text{Lang} + \text{Model} + \text{Domain} + \log(\text{Claims})$| $(1|\text{family}) + (1|\text{task})$ | $\text{Rate Ratio (RR)}_{\text{Hindi/EN}}$| Higher = Worse | Family 2 |
| **$M_{4\text{b}}$** | Any Error Indicator | Generation ($N=5.4\text{k}$) | Binary $\{0, 1\}$ | Binomial GLMM | Binomial (Logit) | $\text{Lang} + \text{Model} + \text{Domain}$ | $(1|\text{family}) + (1|\text{task})$ | $\text{Odds Ratio (OR)}_{\text{Hindi/EN}}$| Higher = Worse | Family 2 |
| **$M_{4\text{c}}$** | Normalized Error Rate | Generation ($N=5.4\text{k}$) | Rate $[0, \infty)$ | Negative Binomial GLMM | NegBin (Log + Offset) | $\text{Lang} + \text{Model} + \text{Domain} + \text{Offset}$ | $(1|\text{family}) + (1|\text{task})$ | $\text{Rate Ratio (RR)}_{\text{Hindi/EN}}$| Higher = Worse | Family 2 |
| **$M_5$** | Citation Quality Grade| Generation ($N=5.4\text{k}$) | Ordinal $\{0 \dots 4\}$ | Cumulative Link (CLMM) | Multinomial (Logit) | $\text{Lang} + \text{Model} + \text{Domain}$ | $(1|\text{family})$ | Ordinal Shift $\beta_{\text{Hindi}}$ | Higher = Better | Family 2 |
| **$M_6$** | Domain Safety Level | Generation ($N=5.4\text{k}$) | Ordinal $\{0, 1, 2\}$ | Cumulative Link (CLMM) | Multinomial (Logit) | $\text{Lang} + \text{Model} + \text{Domain}$ | $(1|\text{family})$ | Ordinal Shift $\beta_{\text{Hindi}}$ | Higher = Worse | Family 2 |
| **$M_7$** | Semantic Preservation | Generation ($N=5.4\text{k}$) | Ordinal $\{0 \dots 4\}$ | Cumulative Link (CLMM) | Multinomial (Logit) | $\text{Lang} + \text{Model} + \text{Domain}$ | $(1|\text{family})$ | Ordinal Shift $\beta_{\text{Hindi}}$ | Higher = Better | Family 2 |
| **$M_{8\text{a}}$** | Completeness Variance | Cell ($N=1.8\text{k}$) | Continuous $[0, \infty)$| Linear Mixed Model (LMM) | Gaussian ($\log$-Identity)| $\text{Lang} + \text{Model} + \text{Domain}$ | $(1|\text{family}) + (1|\text{task})$ | $\text{EMM}_{\text{Hindi}} - \text{EMM}_{\text{EN}}$ | Higher = Worse | Family 2 |
| **$M_{8\text{b}}$** | Jaccard Concordance | Cell ($N=1.8\text{k}$) | Proportion $[0, 1]$ | Beta / Binomial GLMM | Beta/Binomial (Logit) | $\text{Lang} + \text{Model} + \text{Domain}$ | $(1|\text{family}) + (1|\text{task})$ | $\text{EMM}_{\text{Hindi}} - \text{EMM}_{\text{EN}}$ | Higher = Better | Family 2 |

---

### 3. DEFINITIVE EVALUATOR ARCHITECTURE TABLE

| Evaluator Component | Primary LLM Model | Version / Snapshot | Temp ($T$) | Prompt Rubric | Primary Inputs Received | Hidden Metadata (Blinded) | Output JSON Schema | Retry Policy | Determinism Limitation |
| :--- | :--- | :--- | :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| **Atomic Claim Extraction** | `gpt-4o-2024-08-06` | `2024-08-06` | $0.0$ | Claim Extraction Prompt | Raw LLM Response text | Model, Provider, Rep, Request ID, Language Arm Tag | `{"claims": ["string"]}` | Max 3 retries, exp backoff | High empirical parity; non-bitwise API replay |
| **Claim Factual Verification** | `gpt-4o-2024-08-06` | `2024-08-06` | $0.0$ | Fact Verification Prompt | Extracted Claims + Ground Truth ($\text{CF}, \text{IF}$) | Model, Provider, Rep, Request ID, Language Arm Tag | `{"verifications": [{"claim": "...", "status": "SUPPORTED\|CONTRADICTED\|UNSUPPORTED"}]}` | Max 3 retries, exp backoff | High empirical parity; non-bitwise API replay |
| **Expected Fact Coverage** | `gpt-4o-2024-08-06` | `2024-08-06` | $0.0$ | Fact Coverage Prompt | Raw Text + UIN + Ground Truth ($\text{CF}_c, \text{IF}_i$) | Model, Provider, Rep, Request ID, Language Arm Tag | `{"fact_coverage": [{"fact_id": "CF1", "covered": true}]}` | Max 3 retries, exp backoff | High empirical parity; non-bitwise API replay |
| **Citation Quality Assessment**| `gpt-4o-2024-08-06` | `2024-08-06` | $0.0$ | Citation Rubric Prompt | Raw Text + Cited Sources + Source Metadata | Model, Provider, Rep, Request ID, Language Arm Tag | `{"citation_grade": 0..4, "rationale": "..."}` | Max 3 retries, exp backoff | High empirical parity; non-bitwise API replay |
| **Domain Safety Assessment** | `gpt-4o-2024-08-06` | `2024-08-06` | $0.0$ | Domain Safety Prompt | Raw Text + UIN + Safety Rubric | Model, Provider, Rep, Request ID, Language Arm Tag | `{"safety_level": 0..2, "risk_category": "..."}` | Max 3 retries, exp backoff | High empirical parity; non-bitwise API replay |
| **Semantic Preservation** | `gpt-4o-2024-08-06` | `2024-08-06` | $0.0$ | Semantic Preservation Prompt| Raw Text + Benchmark UIN String | Model, Provider, Rep, Request ID, Language Arm Tag | `{"preservation_grade": 0..4, "drift_type": "..."}` | Max 3 retries, exp backoff | High empirical parity; non-bitwise API replay |

---

### 4. FINAL LIST OF FROZEN CONSISTENCY DECISIONS

1. $M_7$ Semantic Preservation is mapped to a **Cumulative Link Mixed Model (CLMM)**.
2. $M_8$ metrics ($\sigma^2_{\text{Comp}}, J_{\text{CF}}$) are evaluated on **1,800 cell-level observations** using LMM and Beta GLMM models.
3. Nesting formula is locked as **$(1 \mid \text{scenario\_family\_id}) + (1 \mid \text{task\_id}) + (1 \mid \text{cell\_id})$**.
4. $M_1$ and $M_3$ are specified using **binomial two-column syntax** (`cbind`), preserving claim and fact denominators.
5. $M_{4\text{a}}$ count model uses **Negative Binomial GLMM** with log link.
6. $M_5$ citation aggregation uses the **Hierarchical Best-Supported Claim Rule**.
7. Primary evaluators are designated as **FIXED AUTOMATED EVALUATION CONFIGURATION** (`gpt-4o-2024-08-06`, $T=0.0$).
8. Evaluator model overlap is audited via **`claude-3-5-sonnet` cross-evaluator sensitivity** on the $N=270$ validation subset.
9. Primary estimands are **Estimated Marginal Means Contrasts ($\Delta_{\text{EMM}}$)**.

---

### 5. FINAL GATE DECISION

```
FINAL CONSISTENCY AUDIT PASSED — CLEARED FOR STAGE 12.5.2
```

---

### 6. HARD STOP DECLARATION

**HARD STOP ENFORCED:** The 5,400 production responses in `stage12_4_full_evaluation_responses.json` remain strictly un-scored and un-analyzed. No automated evaluation pipeline script will be executed until **Stage 12.5.2 (*Evaluator Validation & Scoring Pilot*)** is formally initiated.
