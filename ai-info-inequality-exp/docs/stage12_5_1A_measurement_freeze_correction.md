# STAGE 12.5.1A — MEASUREMENT FREEZE CORRECTION & DEPENDENCY AUDIT
## LINGUA-AUDIT: A Reproducible Framework for Auditing Information Inequality in Multilingual AI Systems

---

### 0. PURPOSE & SCIENTIFIC AUDIT STATUS

This document provides the mandatory **methodological correction and dependency audit** following Stage 12.5.1. It resolves 16 specific methodological ambiguities (Issues A through P) identified during external review of the measurement freeze.

**HARD RULE ENFORCED:** Zero substantive model responses from the 5,400 production dataset (`stage12_4_full_evaluation_responses.json`) were scored, evaluated, or substantively inspected during this stage. Metadata-only sampling design and structural audits were conducted strictly using non-content identifiers.

---

### 1. ISSUE-BY-ISSUE METHODOLOGICAL RESOLUTIONS

---

#### ISSUE A — M1 FACTUAL PRECISION

1. **Official Metric Name:** **`FACTUAL PRECISION`** ($M_1$). The term "accuracy" is explicitly retired as a formal metric name to eliminate conceptual confusion with completeness.
2. **Construct Definition:** Factual Precision measures the exact truthfulness of the verifiable factual statements actually asserted by the model, independently of response length or information completeness.
3. **Formula & Denominators:**
   $$M_1 = \frac{N_{\text{Supported}}}{N_{\text{Supported}} + N_{\text{Contradicted}} + N_{\text{Unsupported}}}$$
   - **$N_{\text{Supported}}$ (Numerator):** Count of atomic claims directly supported by ground-truth sources.
   - **$N_{\text{Contradicted}}$:** Count of atomic claims contradicting ground-truth sources.
   - **$N_{\text{Unsupported}}$:** Count of verifiable factual claims asserted by the model that lack ground-truth backing or cannot be verified.
   - **Denominator:** Total verifiable factual claims asserted ($N_{\text{Supported}} + N_{\text{Contradicted}} + N_{\text{Unsupported}}$).
4. **Atomic Claim Definition:** The minimal self-contained propositional statement expressing a single factual relation (entity, attribute, value, or condition).
5. **Hedged / Conditional Claims:** Claims with uncertainty framing ("According to rules...", "It is likely...") are scored based on the underlying factual proposition; hedging phrases are recorded as qualitative flags.
6. **Precision vs. Completeness Distinction:** $M_1$ measures precision (veracity of what was said); $M_2$ measures recall (coverage of expected benchmark facts). A response with a single true sentence achieves $M_1 = 1.0$ (100% precision) but $M_2 = 0.1$ (10% completeness).

---

#### ISSUE B — M2 COMPLETENESS WEIGHTING & PROVENANCE

1. **Provenance Audit:** In Protocol 1.1.0/1.0.0 and Stage 12.3 task registries, benchmark facts were explicitly stratified into Critical Facts ($\text{CF}$) and Important Facts ($\text{IF}$). However, assigning a fixed scalar weight ratio ($1.0 : 0.5$) in Stage 12.5.1 was a analytical convention rather than an empirically established truth.
2. **Primary Completeness Reporting Structure:**
   - **$M_{2\text{a}}$ Critical Fact Coverage (PRIMARY COMPLETENESS ENDPOINT):**
     $$M_{2\text{a}} = \frac{\sum_{c \in \text{CF}} \mathbf{1}(\text{CF}_c \text{ covered})}{|\text{CF}|}$$
   - **$M_{2\text{b}}$ Important Fact Coverage (SECONDARY COMPLETENESS ENDPOINT):**
     $$M_{2\text{b}} = \frac{\sum_{i \in \text{IF}} \mathbf{1}(\text{IF}_i \text{ covered})}{|\text{IF}|}$$
   - **$M_{2\text{c}}$ Weighted Completeness Index (SENSITIVITY / SECONDARY CONVENTION):**
     $$M_{2\text{c}} = \frac{\sum_{c \in \text{CF}} \mathbf{1}(\text{CF}_c) + 0.5 \sum_{i \in \text{IF}} \mathbf{1}(\text{IF}_i)}{|\text{CF}| + 0.5 |\text{IF}|}$$
     *Note:* $M_{2\text{c}}$ is explicitly declared as a sensitivity convention. Primary confirmatory hypotheses shall be evaluated on $M_{2\text{a}}$.

---

#### ISSUE C — SCENARIO-FAMILY / TASK NESTING STRUCTURE

1. **Benchmark Nesting Verification:** The benchmark contains 25 scenario families, each containing exactly 6 task variants ($25 \times 6 = 150 \text{ tasks}$). Tasks within the same family share identical domain taxonomies and core UIN templates.
2. **Non-Independence Declaration:** $150 \text{ tasks} \neq 150 \text{ independent scenarios}$. Tasks are strictly nested within Scenario Families.
3. **Statistical Model Random Effects Specification:**
   $$\text{Random Effects Structure:} \quad (1 \mid \text{scenario\_family\_id} / \text{task\_id}) \quad \equiv \quad (1 \mid \text{scenario\_family\_id}) + (1 \mid \text{scenario\_family\_id}:\text{task\_id})$$
   - $(1 \mid \text{scenario\_family\_id})$ estimates variance across the 25 scenario families ($\sigma^2_{\text{Family}}$).
   - $(1 \mid \text{scenario\_family\_id}:\text{task\_id})$ estimates variance across task variants nested within family ($\sigma^2_{\text{Task}|\text{Family}}$).

---

#### ISSUE D — REPETITION STRUCTURE

1. **Observation Level:** The generation-level observation unit is $y_{ijkmr}$, where $r \in \{1, 2, 3\}$.
2. **Repetition Status:** Repetitions are repeated stochastic LLM generations ($T=0.2$) of the exact same prompt cell $(i, k, m)$.
3. **Statistical Representation:** Repetitions are **non-independent repeated observations**. They are modeled via a random intercept for prompt cell instance $(1 \mid \text{cell\_id})$ or grouped residual covariance. Repetition index is NEVER treated as a fixed effect or independent task.

---

#### ISSUE E — M8 RESPONSE CONSISTENCY OPERATIONALIZATION

Response Consistency ($M_8$) is formally operationalized across the 3 repetitions ($r_1, r_2, r_3$) within each $(i, k, m)$ cell as two distinct cell-level endpoints:

1. **$M_{8\text{a}}$ Completeness Variance ($\sigma^2_{\text{Comp}}$):**
   $$\sigma^2_{\text{Comp}} = \frac{1}{2} \sum_{r=1}^3 \left( M_{2\text{a}}(r) - \bar{M}_{2\text{a}} \right)^2$$
2. **$M_{8\text{b}}$ Factual Jaccard Concordance ($J_{\text{CF}}$):**
   $$J_{\text{CF}} = \frac{|\text{CF}(r_1) \cap \text{CF}(r_2) \cap \text{CF}(r_3)|}{|\text{CF}(r_1) \cup \text{CF}(r_2) \cup \text{CF}(r_3)|}$$
   - **Factual Unit:** Binary coverage indicator for each canonical Critical Fact $\text{CF}_c$ in the task registry.
   - **Synonyms & Normalization:** Fact coverage is mapped to canonical ground-truth IDs ($\text{CF}_1, \text{CF}_2 \dots$); wording variations matching the same ID map to the same factual unit.
   - **Empty Coverage Case:** If a cell exhibits zero CF coverage across all 3 repetitions ($|\cup| = 0$), $J_{\text{CF}}$ is defined as $1.0$ (trivially concordant absence of coverage) and flagged in sensitivity logs.
   - **Level of Analysis:** Cell-level ($150 \times 3 \times 4 = 1,800$ cell values).

---

#### ISSUE F — HUMAN VALIDATION SAMPLING SPECIFICATION

1. **Sample Size:** $N = 270$ responses ($5.0\%$ of production dataset).
2. **Sampling Mechanism:** Stratified random sampling without replacement, executed via a deterministic script (`scratch/generate_validation_sample.py`) using fixed random seed `428571`.
3. **Sampling Strata:** $5 \text{ domains} \times 3 \text{ languages} \times 4 \text{ models} = 60 \text{ strata}$.
4. **Stratum Allocation:** Exactly 4.5 responses per stratum $\rightarrow 30$ strata allocated 4 responses, 30 strata allocated 5 responses = 270 total responses.
5. **Repetition Handling:** Sampling selects specific cell tuples $(task\_id, language, model, repetition)$; at most 1 repetition per cell tuple is drawn into the validation sample.
6. **Blinding:** Selection relies strictly on metadata. Response content is not inspected during sampling.

---

#### ISSUE G — RELIABILITY ACCEPTANCE RULES & FAILURE PROTOCOL

1. **Status of Thresholds:** Reliability targets ($\text{Cohen's } \kappa \ge 0.80$, $\text{ICC}(2,1) \ge 0.85$, $\kappa_w \ge 0.75$) are **ACCEPTANCE THRESHOLDS**, not pre-assumed results.
2. **Enforced Decision Tree:**
   - **IF THRESHOLDS PASS:** The automated evaluator pipeline is approved; proceed to score the full 5,400 dataset.
   - **IF THRESHOLDS FAIL:** STOP full scoring immediately. Perform a qualitative audit of human-LLM disagreement cases *on the 270 validation subset only*. Refine evaluator prompt rubrics under a documented version update (`v1.1-evaluator`). Re-evaluate agreement on a secondary validation subset ($N=270$, seed `428572`). Do NOT proceed to full scoring until thresholds are met.

---

#### ISSUE H — AUTOMATED EVALUATOR SPECIFICATION & BLINDING

1. **Evaluator Model:** `gpt-4o-2024-08-06` (Primary) / `claude-3-5-sonnet-20241022` (Secondary cross-evaluator).
2. **Generation Parameters:** Temperature $T=0.0$, Top-P $1.0$, Max Tokens $1500$, Structured JSON Schema output.
3. **Failure Policy:** Max 3 retries on API rate-limits or schema parsing errors; terminal errors logged as `EVAL_FAILED`.
4. **Evaluator Blinding Rules:**
   - **Stripped Metadata:** Evaluator prompt receives ZERO metadata regarding target model label, model provider, repetition index, request ID, or experimental language arm assignment (`ENGLISH`, `HINDI`, `CODE_SWITCHING`).
   - **Natural Language Text:** The raw text of the response remains un-translated and un-modified, as language is intrinsic to the response being evaluated against ground truth.

---

#### ISSUE I — GROUND-TRUTH PRESENTATION TO EVALUATOR

1. **Information Provided to Evaluator:**
   - Benchmark Task UIN string
   - Canonical Ground-Truth Facts ($\text{CF}_1 \dots \text{CF}_n$, $\text{IF}_1 \dots \text{IF}_m$)
   - Official Primary Source metadata
   - Target Raw LLM Response text
2. **Stripped Information:** Non-task benchmark metadata, extraneous domain facts, and other language prompt realizations are excluded.
3. **Semantic Preservation Anchor:** Evaluator compares the target response strictly against the **UIN string**. The English prompt realization is NOT used as semantic gold.

---

#### ISSUE J — CLAIM EXTRACTION ARCHITECTURE

1. **Two-Stage Evaluator Architecture:**
   - **Stage 1 (Claim Extraction):** Evaluator extracts all verifiable atomic factual propositions from the raw response into a JSON array of claim strings.
   - **Stage 2 (Factual Verification):** Evaluator evaluates each extracted claim against ground truth to output `SUPPORTED`, `CONTRADICTED`, or `UNSUPPORTED`.
2. **Correlated Evaluator Error Acknowledgment:** Using the same LLM engine for extraction and verification introduces potential correlated error; this risk is explicitly acknowledged and validated via the $N=270$ human validation audit in Stage 12.5.2.

---

#### ISSUE K — PARTIAL CORRECTNESS MAPPING

1. **Claim Precision ($M_1$):** Fractional claim scoring is eliminated. Claims map strictly to categorical outcomes: `SUPPORTED` ($1.0$), `CONTRADICTED` ($0.0$), `UNSUPPORTED` ($0.0$).
2. **Fact Coverage ($M_{2\text{a}}$):** Evaluated as binary coverage ($1.0$ for full coverage, $0.0$ for missing/incorrect). Minor partial coverage ($0.5$) is restricted strictly to sensitivity metric $M_{2\text{c}}$.

---

#### ISSUE L — UNVERIFIABLE CLAIM TREATMENT

1. **Primary Rule:** Unverifiable claims (`UNSUPPORTED`) represent un-evidenced assertions and are included in the denominator of Factual Precision ($M_1$):
   $$M_1 = \frac{N_{\text{Supported}}}{N_{\text{Supported}} + N_{\text{Contradicted}} + N_{\text{Unsupported}}}$$
2. **Secondary Sensitivity Metric ($M_{1\text{b}}$):** A strict contradiction-only precision metric excluding unsupported claims will be reported side-by-side:
   $$M_{1\text{b}} = \frac{N_{\text{Supported}}}{N_{\text{Supported}} + N_{\text{Contradicted}}}$$

---

#### ISSUE M — RESPONSE LENGTH TREATMENT

1. **Role of Response Length:** Token count ($\text{TokenCount}$) is classified strictly as a **DESCRIPTIVE COVARIATE** and potential mediating mechanism.
2. **Primary Causal Models:** Excluded from primary LMMs/GLMMs to avoid controlling away genuine mechanisms of linguistic information inequality.
3. **Sensitivity Models:** Included as a log-transformed covariate ($\log(\text{TokenCount})$) in secondary sensitivity models.

---

#### ISSUE N — STATISTICAL MODEL DISTRIBUTION MAPPING TABLE

| Metric | Outcome Scale | Distribution Family | Link Function | Fixed Effects | Random Effects |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **$M_1$ Factual Precision** | Proportion $[0, 1]$ | Binomial GLMM | Logit | $\text{Lang} + \text{Model} + \text{Domain} + (\text{Lang} \times \text{Model})$ | $(1 \mid \text{family} / \text{task})$ |
| **$M_{2\text{a}}$ CF Completeness** | Proportion $[0, 1]$ | Linear Mixed Model (LMM) | Identity | $\text{Lang} + \text{Model} + \text{Domain} + (\text{Lang} \times \text{Model})$ | $(1 \mid \text{family} / \text{task})$ |
| **$M_3$ Critical Omission** | Proportion $[0, 1]$ | Binomial GLMM | Logit | $\text{Lang} + \text{Model} + \text{Domain} + (\text{Lang} \times \text{Model})$ | $(1 \mid \text{family} / \text{task})$ |
| **$M_4$ Hallucination Count** | Count $\{0, 1, 2 \dots\}$ | Negative Binomial GLMM | Log | $\text{Lang} + \text{Model} + \text{Domain} + \log(\text{Claims})$ | $(1 \mid \text{family} / \text{task})$ |
| **$M_5$ Citation Quality** | Ordinal $\{0 \dots 4\}$ | Cumulative Link (CLMM) | Logit | $\text{Lang} + \text{Model} + \text{Domain}$ | $(1 \mid \text{family})$ |
| **$M_6$ Domain Safety** | Ordinal $\{0, 1, 2\}$ | Cumulative Link (CLMM) | Logit | $\text{Lang} + \text{Model} + \text{Domain}$ | $(1 \mid \text{family})$ |
| **$M_7$ Semantic Preservation**| Ordinal $\{0 \dots 4\}$ | Cumulative Link (CLMM) | Logit | $\text{Lang} + \text{Model} + \text{Domain}$ | $(1 \mid \text{family})$ |
| **$M_{8\text{a}}$ Comp. Variance** | Continuous $[0, \infty)$| LMM ($\log$-transformed) | Identity | $\text{Lang} + \text{Model} + \text{Domain}$ | $(1 \mid \text{family})$ |

---

#### ISSUE O — MULTIPLE COMPARISON FAMILIES

To control false discovery rates without over-correcting independent constructs:

1. **Family 1 (Primary Confirmatory Family):**
   - *Metrics:* $M_1 \text{ Precision}$, $M_{2\text{a}} \text{ CF Completeness}$, $M_3 \text{ Critical Omission}$.
   - *Contrasts:* $\text{Hindi vs English}$, $\text{Code-Switch vs English}$ ($3 \times 2 = 6 \text{ hypothesis tests}$).
   - *Correction:* **Holm-Bonferroni procedure** at overall $\alpha = 0.05$.
2. **Family 2 (Secondary Metrics Family):**
   - *Metrics:* $M_4, M_5, M_6, M_7, M_{8\text{a}}$.
   - *Contrasts:* $\text{Hindi vs English}$, $\text{Code-Switch vs English}$ ($5 \times 2 = 10 \text{ hypothesis tests}$).
   - *Correction:* **Benjamini-Hochberg FDR procedure** at $q = 0.05$.
3. **Family 3 (Interaction & Exploratory Family):**
   - *Tests:* Language $\times$ Model and Language $\times$ Domain interaction terms.
   - *Correction:* **Benjamini-Hochberg FDR procedure** at $q = 0.05$.

---

#### ISSUE P — PRIMARY OUTCOME HIERARCHY RE-VERIFICATION

The confirmatory testing hierarchy is locked and re-verified as:

1. **Primary Triad (Confirmatory):**
   - $M_1$ Factual Precision
   - $M_{2\text{a}}$ Critical Fact Coverage (Primary Completeness)
   - $M_3$ Critical Information Omission Rate
2. **Secondary Endpoints:**
   - $M_4$ Hallucination Count & Rate
   - $M_5$ Citation Quality Grade
   - $M_6$ Domain Safety Level
   - $M_7$ Semantic Preservation Grade
   - $M_8$ Response Consistency Variance & Jaccard Concordance
3. **Exploratory Analyses:**
   - Code-Switching vs. Hindi Mitigation Contrast
   - Response Length Adjustment Sensitivity Models
   - Exploratory Factor Analysis for MI³ Unidimensionality

---

### 2. FINAL LIST OF FROZEN DECISIONS

1. Formal metric name for $M_1$ is **Factual Precision**.
2. Primary completeness metric is **$M_{2\text{a}}$ Critical Fact Coverage** (unweighted). $M_{2\text{c}}$ weighted completeness is retained solely as a secondary convention.
3. Hierarchical random-effects model is locked as **$(1 \mid \text{scenario\_family\_id} / \text{task\_id})$**.
4. Repetitions are represented as **nested repeated observations** within cell.
5. $M_8$ consistency is operationalized as **Completeness Variance ($\sigma^2_{\text{Comp}}$)** and **Critical Fact Jaccard Concordance ($J_{\text{CF}}$)**.
6. Validation sampling uses **stratified random sampling ($N=270$, seed `428571`)** without content inspection.
7. Evaluator blinding strips all language, model, repetition, and provider metadata.
8. Evaluator reliability targets ($\kappa \ge 0.80, \text{ICC} \ge 0.85$) are strictly enforced **acceptance thresholds**.
9. Response token length is classified as a **descriptive covariate**, excluded from primary causal models.
10. Multiple comparisons are partitioned into 3 distinct hypothesis families using Holm-Bonferroni ($\alpha=0.05$) and Benjamini-Hochberg FDR ($q=0.05$).

---

### 3. OUTSTANDING LIMITATIONS

1. **Evaluator Model Snapshots:** Evaluator output consistency depends on the fixed commercial snapshots (`gpt-4o-2024-08-06`, `claude-3-5-sonnet-20241022`).
2. **Correlated Evaluator Error:** Same-model extraction and judgment risks correlated LLM evaluator errors, which must be rigorously audited against human labels in Stage 12.5.2.

---

### 4. FINAL GATE DECISION

```
CORRECTION COMPLETE — CLEARED FOR STAGE 12.5.2
```

---

### 5. HARD STOP DECLARATION

**HARD STOP ENFORCED:** The 5,400 production responses in `stage12_4_full_evaluation_responses.json` remain strictly un-scored and un-analyzed. No automated evaluation script will be executed until **Stage 12.5.2 (*Evaluator Validation & Scoring Pilot*)** is formally initiated.
