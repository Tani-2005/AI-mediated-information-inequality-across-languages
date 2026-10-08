# STAGE 12.5.1D — FINAL BOUNDARY-OUTCOME & CLAIM-DENOMINATOR CORRECTION
## LINGUA-AUDIT: A Reproducible Framework for Auditing Information Inequality in Multilingual AI Systems

---

### 0. PURPOSE & SCIENTIFIC AUDIT STATUS

This artifact represents the **Final Pre-Pilot Methodological Correction** prior to authorizing Stage 12.5.2 (Evaluator Validation & Scoring Pilot). It resolves four remaining methodological boundary issues:
1. **$M_{8\text{b}}$ Jaccard Concordance boundary values ($0.0$ and $1.0$)**
2. **$M_{8\text{a}}$ Completeness Variance zero values ($\sigma^2_{\text{Comp}} = 0$)**
3. **$M_1$ Factual Precision claim-denominator taxonomy & terminology**
4. **$M_5$ Citation Quality multi-citation deterministic case audit (Cases A–I)**

**HARD RULE ENFORCED:** Zero substantive model responses from the 5,400 production dataset (`stage12_4_full_evaluation_responses.json`) were scored, evaluated, or substantively inspected during this stage.

---

### 1. METHODOLOGICAL CORRECTIONS & RESOLUTIONS

---

#### ISSUE 1 — M8b JACCARD CONCORDANCE BOUNDARY VALUES ($J_{\text{CF}} \in [0, 1]$)

1. **Boundary Issue:** Critical Fact Jaccard Concordance $J_{\text{CF}} = \frac{|\text{CF}(r_1) \cap \text{CF}(r_2) \cap \text{CF}(r_3)|}{|\text{CF}(r_1) \cup \text{CF}(r_2) \cup \text{CF}(r_3)|}$ yields discrete fraction values in $[0, 1]$, frequently taking exact boundary values $0.0$ (zero overlap across repetitions) and $1.0$ (perfect concordance). A standard Beta GLMM is defined only on the open interval $(0, 1)$ and fails at boundaries.
2. **Epsilon Hack Rejection:** Arbitrary data transformations (e.g. $0 \rightarrow \epsilon, 1 \rightarrow 1-\epsilon$) are explicitly rejected as unscientific.
3. **Primary Model Specification (Binomial GLMM Overlap Model):**
   $$J_{\text{CF}} = \frac{K_{\text{overlap}}}{K_{\text{union}}}$$
   Where $K_{\text{overlap}} = |\text{CF}(r_1) \cap \text{CF}(r_2) \cap \text{CF}(r_3)|$ and $K_{\text{union}} = |\text{CF}(r_1) \cup \text{CF}(r_2) \cup \text{CF}(r_3)|$.
   
   $M_{8\text{b}}$ is modeled as a **Binomial GLMM** with logit link using two-column count syntax:
   $$\text{Response Variable:} \quad \text{cbind}(K_{\text{overlap}}, K_{\text{union}} - K_{\text{overlap}})$$
   *Properties:* Handles $K_{\text{overlap}} = 0$ ($J=0.0$) and $K_{\text{overlap}} = K_{\text{union}}$ ($J=1.0$) naturally without data transformations.
4. **Empty Union Boundary ($K_{\text{union}} = 0$):** If a cell exhibits zero Critical Fact coverage across all 3 repetitions ($K_{\text{union}} = 0$), it is excluded from the binomial GLMM and logged in a secondary zero-coverage binary indicator model ($M_{8\text{b,empty}} = \mathbf{1}(K_{\text{union}} = 0)$).
5. **Sensitivity Model:** Zero-and-One-Inflated Beta (ZOIB) regression is specified as sensitivity analysis.

---

#### ISSUE 2 — M8a COMPLETENESS VARIANCE ZERO-VARIANCE TREATMENT ($\sigma^2_{\text{Comp}} \ge 0$)

1. **Zero-Variance Issue:** $M_{8\text{a}}$ (Completeness Variance) is computed from $n=3$ repetitions ($df=2$). When all 3 repetitions yield identical completeness scores (e.g. $1.0, 1.0, 1.0$), sample variance is **exactly zero** ($\sigma^2_{\text{Comp}} = 0$). Log transformation $\log(0)$ is mathematically undefined.
2. **Primary Specification (Two-Part Hurdle Model):**
   - **Part 1 (Binary Variance Indicator GLMM):** Models the probability of any repetition inconsistency occurring ($Y_{\text{inconsistent}} = \mathbf{1}(\sigma^2_{\text{Comp}} > 0)$) using a Binomial GLMM with logit link.
   - **Part 2 (Positive Variance Magnitude Model):** For cells with $\sigma^2_{\text{Comp}} > 0$, a **Gamma GLMM** with log link models variance magnitude:
     $$\mathbb{E}[\sigma^2_{\text{Comp}} \mid \sigma^2_{\text{Comp}} > 0] = \exp(\mathbf{X}\boldsymbol{\beta})$$
3. **Sensitivity Model:** A pragmatic $\log(1 + \sigma^2_{\text{Comp}})$ LMM treatment is retained for secondary reporting.

---

#### ISSUE 3 — M1 CLAIM-DENOMINATOR TAXONOMY & TERMINOLOGY

1. **Terminology Resolution:** The ambiguous term "Total Asserted Verifiable Claims" is formally replaced by **`Total Extracted Factual Claims Adjudicated`** ($N_{\text{adjudicated}}$).
2. **Claim Taxonomy & Denominator Rules:** Every extracted atomic claim is classified into one of four mutually exclusive categories:

| Claim Category | Classification Definition | Enters $M_1$ Denominator? | Enters $M_1$ Numerator? |
| :--- | :--- | :---: | :---: |
| **1. `SUPPORTED`** | Factual claim directly backed by frozen ground-truth sources. | **YES** | **YES ($+1$)** |
| **2. `CONTRADICTED`** | Factual claim directly contradicting frozen ground-truth sources. | **YES** | **NO ($0$)** |
| **3. `UNSUPPORTED`** | Factual claim asserted by model that lacks evidence in frozen source set. | **YES** | **NO ($0$)** |
| **4. `GENUINELY_UNSCORABLE`**| Non-adjudicable statements (subjective opinions, conversational pleasantries, formatting math, or duplicate non-independent claims). | **EXCLUDED** | **NO ($0$)** |

3. **Official Primary $M_1$ Formula:**
   $$M_1 = \frac{N_{\text{Supported}}}{N_{\text{Supported}} + N_{\text{Contradicted}} + N_{\text{Unsupported}}}$$
4. **Official Sensitivity Metric $M_{1\text{b}}$ (Contradiction-Only Precision):**
   $$M_{1\text{b}} = \frac{N_{\text{Supported}}}{N_{\text{Supported}} + N_{\text{Contradicted}}}$$

---

#### ISSUE 4 — M5 MULTIPLE-CITATION DETERMINISTIC CASE AUDIT (CASES A–I)

The **Composite Response Citation Quality Rubric** ($M_5 \in \{0, 1, 2, 3, 4\}$) is audited across 9 synthetic test cases to verify complete determinism:

```
Case A: 2 Citations (Both authoritative official sources, both support claims)
        → Grade 4 (Authoritative & Fully Supporting)

Case B: 2 Citations (1 authoritative supporting, 1 real portal but irrelevant to claim)
        → Grade 2 (Present but Insufficient / Mixed)

Case C: 2 Citations (1 correct supporting, 1 real portal contradicting claim)
        → Grade 2 (Present but Insufficient / Mixed)

Case D: 2 Citations (1 real authoritative supporting, 1 fabricated fake URL)
        → Grade 1 (Format Only / Fabricated — fake URL caps grade at 1)

Case E: 2 Citations (Both real portals, neither supports asserted claims)
        → Grade 2 (Present but Insufficient / Mixed)

Case F: 0 Citations in response
        → Grade 0 (No Citation)

Case G: 1 Citation (URL domain non-existent / unreachable)
        → Grade 1 (Format Only / Fabricated)

Case H: 1 Citation (1 real authoritative URL supporting 3 separate claims)
        → Grade 4 (Authoritative & Fully Supporting)

Case I: 3 Citations (3 distinct real supporting URLs backing the same claim)
        → Grade 3 (Correct & Relevant Supporting) [Grade 4 if one is authoritative]
```

*Audit Verdict:* The rubric produces **exactly one deterministic grade** for all possible multi-citation configurations.

---

### 2. DEFINITIVE STATISTICAL SPECIFICATION TABLE (UPDATED)

| Metric Code | Metric Name | Unit | Scale | Primary Statistical Model | Boundary / Zero Treatment | Fixed Effects | Random Effects | Primary Estimand ($\Delta_{\text{EMM}}$) | Direction | Multiplicity Family | Primary / Sensitivity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **$M_1$** | Factual Precision | Gen ($N=5.4\text{k}$) | Prop $[0, 1]$ | Binomial GLMM | $N_{\text{adjudicated}}$ Denominator | $\text{Lang} + \text{Model} + \text{Domain}$ | $(1|\text{fam}) + (1|\text{task}) + (1|\text{cell})$ | $\hat{p}_{\text{Hindi}} - \hat{p}_{\text{EN}}$ (Risk Diff) | Higher = Better | Family 1 | **PRIMARY** |
| **$M_{1\text{b}}$** | Contradiction Precision | Gen ($N=5.4\text{k}$) | Prop $[0, 1]$ | Binomial GLMM | Excludes Unsupported | $\text{Lang} + \text{Model} + \text{Domain}$ | $(1|\text{fam}) + (1|\text{task}) + (1|\text{cell})$ | $\hat{p}_{\text{Hindi}} - \hat{p}_{\text{EN}}$ (Risk Diff) | Higher = Better | Sensitivity | Sensitivity |
| **$M_{2\text{a}}$** | Critical Fact Coverage | Gen ($N=5.4\text{k}$) | Discrete $\{0 \dots 1\}$| Binomial GLMM | `cbind(CF_cov, CF_tot - CF_cov)` | $\text{Lang} + \text{Model} + \text{Domain}$ | $(1|\text{fam}) + (1|\text{task}) + (1|\text{cell})$ | $\hat{p}_{\text{Hindi}} - \hat{p}_{\text{EN}}$ (Risk Diff) | Higher = Better | Family 1 | **PRIMARY** |
| **$M_{2\text{c}}$** | Weighted Completeness | Gen ($N=5.4\text{k}$) | Prop $[0, 1]$ | Linear Mixed Model (LMM)| Identity Link | $\text{Lang} + \text{Model} + \text{Domain}$ | $(1|\text{fam}) + (1|\text{task}) + (1|\text{cell})$ | $\text{EMM}_{\text{Hindi}} - \text{EMM}_{\text{EN}}$ | Higher = Better | Sensitivity | Sensitivity |
| **$M_3$** | Critical Omission Rate | Gen ($N=5.4\text{k}$) | Prop $[0, 1]$ | Binomial GLMM | `cbind(CF_mis, CF_tot - CF_mis)` | $\text{Lang} + \text{Model} + \text{Domain}$ | $(1|\text{fam}) + (1|\text{task}) + (1|\text{cell})$ | $\hat{p}_{\text{Hindi}} - \hat{p}_{\text{EN}}$ (Risk Diff) | Higher = Worse | Family 1 | **PRIMARY** |
| **$M_{4\text{a}}$** | Factual Error Count | Gen ($N=5.4\text{k}$) | Count $\{0, 1 \dots\}$ | Negative Binomial GLMM | Log Link | $\text{Lang} + \text{Model} + \text{Domain} + \log(\text{Claims})$| $(1|\text{fam}) + (1|\text{task})$ | Rate Ratio ($\text{RR}_{\text{Hindi/EN}}$)| Higher = Worse | Family 2 | Secondary |
| **$M_{4\text{b}}$** | Any Error Indicator | Gen ($N=5.4\text{k}$) | Binary $\{0, 1\}$ | Binomial GLMM | Logit Link | $\text{Lang} + \text{Model} + \text{Domain}$ | $(1|\text{fam}) + (1|\text{task})$ | Odds Ratio ($\text{OR}_{\text{Hindi/EN}}$)| Higher = Worse | Family 2 | Secondary |
| **$M_{4\text{c}}$** | Normalized Error Rate | Gen ($N=5.4\text{k}$) | Rate $[0, \infty)$ | Negative Binomial GLMM | Log Link + Offset | $\text{Lang} + \text{Model} + \text{Domain} + \text{Offset}$ | $(1|\text{fam}) + (1|\text{task})$ | Rate Ratio ($\text{RR}_{\text{Hindi/EN}}$)| Higher = Worse | Family 2 | Secondary |
| **$M_5$** | Citation Quality Grade| Gen ($N=5.4\text{k}$) | Ordinal $\{0 \dots 4\}$ | Cumulative Link (CLMM) | Cumulative Logit | $\text{Lang} + \text{Model} + \text{Domain}$ | $(1|\text{fam})$ | Cum Odds Ratio ($\text{COR}$) | Higher = Better | Family 2 | Secondary |
| **$M_6$** | Domain Safety Level | Gen ($N=5.4\text{k}$) | Ordinal $\{0, 1, 2\}$ | Cumulative Link (CLMM) | Cumulative Logit | $\text{Lang} + \text{Model} + \text{Domain}$ | $(1|\text{fam})$ | Cum Odds Ratio ($\text{COR}$) | Higher = Worse | Family 2 | Secondary |
| **$M_7$** | Semantic Preservation | Gen ($N=5.4\text{k}$) | Ordinal $\{0 \dots 4\}$ | Cumulative Link (CLMM) | Cumulative Logit | $\text{Lang} + \text{Model} + \text{Domain}$ | $(1|\text{fam})$ | Cum Odds Ratio ($\text{COR}$) | Higher = Better | Family 2 | Secondary |
| **$M_{8\text{a}}$** | Completeness Variance | Cell ($N=1.8\text{k}$) | Prop $[0, 1]$ | Two-Part Hurdle GLMM | Binomial Logit + Gamma Log | $\text{Lang} + \text{Model} + \text{Domain}$ | $(1|\text{fam}) + (1|\text{task})$ | Hurdle OR & Gamma $\Delta_{\text{EMM}}$| Higher = Worse | Family 2 | Secondary |
| **$M_{8\text{b}}$** | Jaccard Concordance | Cell ($N=1.8\text{k}$) | Discrete Prop | Binomial GLMM | `cbind(K_over, K_union - K_over)`| $\text{Lang} + \text{Model} + \text{Domain}$ | $(1|\text{fam}) + (1|\text{task})$ | $\hat{p}_{\text{Hindi}} - \hat{p}_{\text{EN}}$ (Risk Diff) | Higher = Better | Family 2 | Secondary |

---

### 3. CROSS-DOCUMENT CONSISTENCY AUDIT & CORRECTION CHAIN

A systematic audit across all Stage 12.5.x artifacts documents the complete correction chain:

1. **$M_1$ Denominator Terminology:** "Total Asserted Verifiable Claims" (Stage 12.5.1A/B) is formally superseded by **`Total Extracted Factual Claims Adjudicated`** ($N_{\text{adjudicated}}$).
2. **$M_{8\text{b}}$ Boundary Treatment:** Beta GLMM (Stage 12.5.1B/C) is formally superseded by the **Binomial GLMM Overlap Model** (`cbind(K_overlap, K_union - K_overlap)`).
3. **$M_{8\text{a}}$ Zero-Variance Treatment:** $\log(\sigma^2_{\text{Comp}} + 0.001)$ LMM (Stage 12.5.1B/C) is formally superseded by the **Two-Part Hurdle GLMM** (Binomial + Gamma).
4. **$M_5$ Multi-Citation Rules:** "Best-Supported Claim" (Stage 12.5.1B) is formally superseded by the **Composite Response Citation Quality Rubric (Cases A–I)**.

---

### 4. OUTSTANDING LIMITATIONS

1. **Derived Small-n Repetition Variance:** Repetition consistency ($M_{8\text{a}}, M_{8\text{b}}$) is derived from $n=3$ repetitions per cell ($df=2$), representing a pragmatic cell-level consistency estimate.
2. **Commercial API Non-Bitwise Replay:** Fixed evaluator configuration (`gpt-4o-2024-08-06`, $T=0.0$) provides high empirical consistency but lacks guaranteed bitwise mathematical determinism.

---

### 5. FINAL GATE DECISION

```
FINAL METHODOLOGICAL FREEZE PASSED — CLEARED FOR STAGE 12.5.2
```

---

### 6. HARD STOP DECLARATION

**HARD STOP ENFORCED:** The 5,400 production responses in `stage12_4_full_evaluation_responses.json` remain strictly un-scored and un-analyzed. Automated scoring pipeline execution is prohibited until **Stage 12.5.2 (*Evaluator Validation & Scoring Pilot*)** is formally initiated.
