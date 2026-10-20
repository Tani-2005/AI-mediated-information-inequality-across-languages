# LINGUA-AUDIT: Auditing Information Inequality in Multilingual AI Systems

**Anonymous Authors**  
*Under Review / Working Draft — October 2026*  

---

## 1. Abstract

As large language models (LLMs) are increasingly proposed as conversational intermediaries for public services, civic welfare schemes, healthcare navigation, and statutory entitlements, information inequality across linguistic communities has emerged as an urgent governance and technical challenge. In multilingual societies, disparities in AI performance do not merely reflect stylistic variations or fluency degradation; they threaten to manifest as *substantive information inequality*, wherein citizens querying identical administrative systems in non-English or code-switched vernaculars receive incomplete, outdated, misleading, or factually erroneous guidance.

This paper presents **LINGUA-AUDIT**, an open, reproducible civic-information benchmark design, measurement protocol, and auditing framework created to systematically evaluate substantive information inequality in multilingual AI systems. Grounded in official administrative documentation and statutory guidelines across five essential civic domains (Healthcare, Education, Public Services, Finance, and General Knowledge), LINGUA-AUDIT introduces a frozen civic-information benchmark of 150 real-world tasks anchored to language-agnostic Underlying Information Needs (UINs). The framework formalizes a multi-dimensional measurement suite spanning 13 response-quality metrics across factual precision ($M_1, M_{1b}$), factual completeness and omission ($M_{2a}, M_{2c}, M_3$), factual error count ($M_{4a}, M_{4b}, M_{4c}$), citation authenticity ($M_5$), domain safety ($M_6$), UIN-anchored semantic preservation ($M_7$), and cross-repetition stochastic consistency ($M_{8a}, M_{8b}$). We formulate a prespecified statistical analysis plan utilizing Generalized Linear Mixed Models (GLMMs), Cumulative Link Mixed Models (CLMMs), and Two-Part Hurdle models with family-wise error control.

We demonstrate the software architecture and verify end-to-end data flow using a full factorial matrix across $150 \text{ tasks} \times 3 \text{ language conditions (English, Hindi, Hindi-English Code-Switching)} \times 4 \text{ model slots (Gemini 3.5 Flash, GPT-4o, Claude 3.5 Sonnet, Llama 3.1 70B)} \times 3 \text{ repetitions} = 5,400 \text{ factorial cells}$. We verify complete cryptographic integrity (raw bytes SHA-256: `095b8caa...`; canonical sorted JSON SHA-256: `296bb165...`), zero missing cells, zero duplicates, and complete test suite verification across 115 unit and regression tests.

**Scientific and Validation Disclosures:** We provide full, explicit disclosure regarding the current operational status of the framework:
1. **Framework Framing:** This paper presents the benchmark design, metric operationalization, software implementation, and prespecified analysis plan; it does **not** report an empirical evaluation of live LLM performance.
2. **Deterministic Baseline Fixtures:** The 5,400 records in the repository dataset represent programmatic baseline fixtures instantiated to verify software data flow, schema adherence, and factorial matrix completeness—**not** genuine outputs from live Gemini, GPT-4o, Claude, or Llama models.
3. **Pending Evaluator Validation:** A prior automated evaluator validation exercise was audited, found to contain synthetically cloned human labels and unexecuted model calls, and was formally quarantined. A 12-item blinded feasibility pilot package and a 270-response representative validation sample have been prepared, but independent bilingual annotators have not yet been secured. Consequently, empirical evaluator validation and all 13 substantive quality scores remain strictly **unvalidated pending future human annotation**.
4. **Future Work:** Live frontier model API execution (data collection) and independent human evaluator calibration (measurement validation) represent separate future activities that precede downstream empirical scoring and analysis.

---

## 2. Keywords

**Keywords:** Information Inequality, Multilingual Benchmark Design, Auditing Framework, LLM Evaluation, Code-Switching, Algorithmic Governance, Statutory Ground Truth, Reproducibility.

---

## 3. Introduction and Research Questions

Large language models (LLMs) are transitioning from experimental research prototypes into customer-facing and citizen-facing conversational interfaces. Across developing and multilingual nations, government agencies, municipal corporations, healthcare networks, and civic organizations are exploring or piloting generative AI systems to automate citizen advisory services: explaining welfare eligibility, detailing statutory identity documentation workflows, clarifying educational reservation criteria, and providing public health advice. In these high-stakes civic contexts, user populations are frequently socioeconomically vulnerable and linguistically diverse, relying on automated systems for actionable, life-critical guidance.

Despite rapid advances in multilingual natural language processing, frontier generative models exhibit profound disparities across languages. Existing multilingual evaluations have predominantly focused on surface-level capabilities: cross-lingual perplexity, translation BLEU/ChrF scores, or multiple-choice examinations translated from Western academic curricula (e.g., multilingual MMLU). While valuable for measuring broad model capability, these evaluations do not assess whether models satisfy identical civic information needs equitably across languages: **they do not measure information inequality**.

### 3.1 Defining AI-Mediated Information Inequality

We define *AI-mediated information inequality* not as a simple ranking of model speed or surface fluency across languages, but as:
> **The systematic divergence in the substantive, factual, and actionable information provided to citizens seeking to satisfy identical information needs across different linguistic conditions.**

In public administrative systems, information inequality creates tangible, asymmetric harms. If an English query regarding maternal health benefits yields accurate income thresholds, mandatory document lists, and links to the official portal, while an equivalent Hindi or code-switched Hinglish query yields outdated financial caps, omits mandatory attestation steps, or provides hallucinated URLs, information inequality has occurred. The non-English speaker faces administrative disqualification, missed entitlement deadlines, economic loss, or health risks—despite asking the same statutory question.

```
+-----------------------------------------------------------------------------------------+
|                                LINGUA-AUDIT FRAMEWORK OVERVIEW                          |
|                                                                                         |
|   +-----------------------+     +------------------------+     +--------------------+   |
|   | Statutory Authorities | --> |  150 Benchmark Tasks   | --> | 3 Language Prompts |   |
|   | (Acts, Portals, Rules)|     |  (5 Civic Domains)     |     | (EN, HI, Hinglish) |   |
|   +-----------------------+     +------------------------+     +--------------------+   |
|                                                                          |              |
|                                                                          v              |
|   +-----------------------+     +------------------------+     +--------------------+   |
|   | 13 Operational Metrics| <-- | Automated Evaluator    | <-- | 4 Target LLM Slots |   |
|   | (Precision, Omission, |     | Protocol (Specified;   |     | (5,400 Factorial   |   |
|   |  Safety, Consistency) |     |  Validation PENDING)   |     |  Pipeline Matrix)  |   |
|   +-----------------------+     +------------------------+     +--------------------+   |
+-----------------------------------------------------------------------------------------+
```

### 3.2 Research Questions Prespecified by the Framework

The LINGUA-AUDIT framework is designed to provide the measurement methodology and statistical architecture needed to answer four foundational research questions when live models are deployed:

- **RQ1 (Information Completeness & Omission Disparity):** Does the coverage of statutory Critical Facts ($M_{2a}$) and the omission rate of mandatory administrative prerequisites ($M_3$) differ significantly between English, Hindi, and Hindi-English code-switched queries when adjusting for model family and task domain?
- **RQ2 (Factual Precision & Contradiction Severity):** Are vernacular and code-switched queries subject to significantly higher factual contradiction rates ($M_{4a}, M_{4c}$) and depressed factual precision ($M_1, M_{1b}$) against statutory ground truth compared to English queries?
- **RQ3 (Citation Authenticity & Citizen Risk):** Do models exhibit elevated rates of hallucinated, non-functional, or non-authoritative URL citations ($M_5$) and increased citizen administrative/medical risk levels ($M_6$) in vernacular and code-switched interactions?
- **RQ4 (Stochastic Repetition Consistency):** Is information delivery in vernacular queries less stochastically stable across repeated generations, as quantified by within-condition completeness variance ($M_{8a}$) and Critical Fact Jaccard concordance ($M_{8b}$)?

### 3.3 Scope and Contributions of this Manuscript

This paper establishes the foundational methodology, benchmark resources, software infrastructure, and analysis plan required to execute rigorous audits of information inequality. We emphasize that **this manuscript presents a benchmark-design and reproducibility framework, not an empirical study of live model behavior**. 

Our primary contributions are:
1. **The LINGUA-AUDIT Benchmark:** A curated, frozen civic-information benchmark of 150 real-world administrative tasks across 5 societal domains in India, grounded in official regulatory guidelines and indexed by language-agnostic Underlying Information Needs (UINs).
2. **Multi-Dimensional Operational Measurement Suite:** Formal mathematical specifications for 13 response-quality metrics spanning factual precision, information coverage, omission, error deduplication, citation quality, domain safety, UIN preservation, and stochastic consistency, complete with boundary-case handling.
3. **Prespecified Statistical Analysis Plan:** A rigorous modeling framework utilizing Binomial GLMMs, Negative Binomial GLMMs, CLMMs, and Two-Part Hurdle models with family-wise error rate control.
4. **Reproducible Pipeline & Software Verification:** A modular, open-source Python scoring architecture accompanied by 115 passing unit and regression tests, verified against a 5,400-cell factorial software fixture matrix.
5. **Methodological Governance & Forensic Transparency:** Explicit quarantine of invalid prior synthetic evaluator validation artifacts, clear separation of software correctness from empirical construct validity, and full disclosure of pending validation requirements.

---

## 4. Related Work

### 4.1 Multilingual NLP and Resource Asymmetries

Disparities in natural language processing across global languages are well-documented. Blasi et al. (2022) established that global NLP development correlates strongly with national economic wealth and digital web text availability rather than speaker population, leading to technological marginalization for billions of speakers. Joshi et al. (2020) categorized languages into resource classes, noting that despite having over 600 million speakers, Hindi remains digitally under-resourced relative to its demographic size due to uncurated crawls and limited parallel corpora. Bender et al. (2021) observed that large language models trained on massive, uncurated web data amplify dominant cultural perspectives and linguistic norms while degrading in low-resource and vernacular contexts.

### 4.2 Multilingual Generative Benchmarks

Traditional multilingual benchmarks relied heavily on direct translations of English source corpora. Benchmarks such as XNLI (Conneau et al., 2018), TyDi QA (Clark et al., 2020), and multilingual translations of MMLU (Hendrycks et al., 2021) evaluate basic syntactic understanding and academic question-answering. However, as Ahuja et al. (2023) and Bang et al. (2023) demonstrated, translated benchmarks suffer from "translationese" and cultural disconnects, failing to test authentic civic problem-solving or localized administrative interactions.

In South Asia, digital communication is heavily characterized by code-switching. Khanuja et al. (2020) developed GLUECoS to benchmark code-switched NLP, showing significant performance drops on Hinglish across standard NLP tasks. LINGUA-AUDIT builds on this foundation by establishing Hindi-English code-switching as a primary, first-class language condition alongside standard Hindi and English.

### 4.3 Automated Factual Evaluation and Evaluator Reliability

Evaluating long-form factual accuracy in generative AI has motivated significant recent research. Min et al. (2023) introduced *FActScore*, decomposing text into atomic factual claims evaluated against Wikipedia references. Liang et al. (2023) established the Holistic Evaluation of Language Models (HELM) framework to standardize multi-metric evaluation across accuracy, robustness, and fairness. 

When LLMs are deployed as automated evaluators ("LLM-as-a-judge"; Zheng et al., 2023), significant threats to validity emerge. Hada et al. (2023) demonstrated that uncalibrated LLM evaluators exhibit severe leniency bias, perform inconsistently in low-resource and non-Latin scripts, and require rigorous calibration against native human judgments. Furthermore, prior audits have cautioned against circular self-validation, where automated evaluators are validated against synthetic model outputs rather than human ground truth. LINGUA-AUDIT addresses these challenges by anchoring evaluation to statutory authorities and establishing strict quarantine protocols when synthetic validation shortcuts are detected.

---

## 5. Benchmark Design and Task Construction

### 5.1 Domain Architecture and Civic Selection

The LINGUA-AUDIT civic-information benchmark comprises **150 administrative and civic tasks** representing critical daily interactions between citizens and public institutions in India. The benchmark is equally partitioned across five essential societal domains ($N=30$ tasks per domain):

1. **Healthcare ($N=30$):** Entitlements under national public health insurance (Ayushman Bharat PM-JAY), universal immunization schedules, revised tuberculosis treatment notification rules, public hospital emergency admission mandates, and subsidized pharmaceutical dispensaries (Jan Aushadhi).
2. **Education ($N=30$):** Quota admissions under the Right to Education (RTE) Act Section 12(1)(c), National Scholarship Portal (NSP) verification rules, university reservation categories, vocational skill certification accreditation, and public exam fee waivers.
3. **Public Services ($N=30$):** Mandatory documentation for Aadhaar demographic/biometric updates, Voter ID registration and constituency transfer, Public Distribution System (PDS / Ration Card) portability under One Nation One Ration Card (ONORC), passport police verification rules, and municipal grievance filings.
4. **Finance ($N=30$):** Direct benefit transfer eligibility under PM-KISAN, micro-pension enrollment under Atal Pension Yojana (APY), collateral-free microenterprise lending under PM Mudra Yojana, small savings tax exemption schemes (PPF, Sukanya Samriddhi), and formal banking ombudsman dispute escalation.
5. **General Knowledge & Civic Rights ($N=30$):** Statutory filing procedures under the Right to Information (RTI) Act 2005, consumer dispute filings under the Consumer Protection Act 2019, citizen rights during police encounters, and state public service delivery guarantee acts.

Tasks are categorized by difficulty—Moderate (66 tasks, 44.0%), Low (48 tasks, 32.0%), and High (36 tasks, 24.0%)—and safety sensitivity—High (60 tasks, 40.0%), Moderate (60 tasks, 40.0%), and Low (30 tasks, 20.0%).

### 5.2 Statutory Ground Truth Anchoring

Every task in LINGUA-AUDIT is grounded in public statutory authorities and administrative guidelines recorded in the master task registry (`data/benchmark/master_task_registry_150.json`):
- **Primary Statutory Authorities ($N=150$, 1 per task):** Sourced from official central and state government guidelines, gazette notifications, ministry circulars, and official `.gov.in` / `.nic.in` departmental domains (encompassing 25 unique public administrative authorities across the benchmark). In the task registry, each source entry explicitly records the institutional source name (e.g., `"NHA PM-JAY Guidelines (pmjay.gov.in)"`), administrative authority type, and a scheme cutoff date (`"2026-10-01"`). The registry records do not contain navigable HTTP/HTTPS URLs, verbatim statutory passages or excerpted legal clauses, nor granular access timestamps.
- **Critical Facts (CF; $N=450$, exactly 3 per task):** Mandatory statutory provisions without which a citizen cannot successfully access the service (e.g., specific income ceilings, mandatory identity proofs, statutory filing windows).
- **Important Facts (IF; $N=300$, exactly 2 per task):** Key procedural context (e.g., processing turnaround times, digital alternatives, appellate grievance timelines).
- **Safety Constraints ($N=150$, exactly 1 per task):** Explicit warning boundaries to protect citizens from financial exploitation or procedural invalidation (e.g., explicit warnings that official government application forms are free of charge, or warnings against unauthorized intermediaries).

*Curation Scope vs. Independent Validation:* Ground truth facts represent internal curation by the project authors based on published administrative schemes and acts, rather than an independently certified legal gold standard. The registry does not include fine-grained clause-to-fact alignment mapping, and formal multi-expert panel validation by independent legal or domain authorities has not yet been conducted across the 150 tasks (reserved for future work).

### 5.3 Underlying Information Need (UIN) Formulation

To eliminate *English-normative bias*—the tendency to treat English sentence structure, idioms, or phrasing as an artificial standard of correctness—every task is indexed by an **Underlying Information Need (UIN)**. The UIN specifies the communicative intent, necessary factual scope, conditions, and boundary caveats in conceptual, language-agnostic terms. Responses in Hindi and code-switched Hinglish are evaluated against the UIN rather than against English comparator texts.

---

## 6. Language Conditions and Model Configurations

### 6.1 Language Conditions

Every benchmark task is operationalized across three authentic linguistic prompts:
1. **English (`ENGLISH`):** Formal Indian English administrative query phrasing, representing the standard reference condition.
2. **Hindi (`HINDI`):** Modern standard Hindi rendered in Devanagari script, incorporating formal administrative terms (*योजना*, *पात्रता*, *आवेदन प्रक्रिया*).
3. **Hindi-English Code-Switching (`CODE_SWITCHING`):** Colloquial "Hinglish," reflecting how bilingual citizens formulate queries on digital mobile platforms using Roman script and mixed Hindi-English grammar (e.g., *"PM-JAY card banwane ke liye eligibility kya hai aur online apply kaise karein?"*).

### 6.2 Target Model Slots & Software Configuration

The execution protocol defines four **target model slots** representing leading open and proprietary LLM architectures:
- **Google Slot:** `gemini-3.5-flash` (prespecified target identifier: `gemini-3.5-flash-202610`)
- **OpenAI Slot:** `gpt-4o` (prespecified target identifier: `gpt-4o-2024-08-06`)
- **Anthropic Slot:** `claude-3.5-sonnet` (prespecified target identifier: `claude-3-5-sonnet-20241022`)
- **Meta Slot:** `llama-3.1-70b` (prespecified target identifier: `llama-3.1-70b-instruct-v1`)

Standardized generation parameters prespecified in the execution protocol are `temperature = 0.2`, `top_p = 1.0`, and `max_tokens = 1000`.

*Target Slot and Fixture Status Disclosure:* All four models are defined strictly as architectural **target slots** in the experimental design. No live model endpoints were queried, and no external provider APIs were contacted. The 5,400 records currently stored in `data/benchmark/raw_responses/stage12_4_full_evaluation_responses.json` were synthesized in-memory via programmatic template functions to verify pipeline data ingestion, serialization, and test automation. They function exclusively as deterministic software fixtures.

---

## 7. Data Collection and Reproducibility

### 7.1 Pipeline Factorial Matrix Design

The LINGUA-AUDIT software pipeline verifies data collection and downstream scoring over a complete factorial matrix:
$$\text{Factorial Matrix} = 150 \text{ Tasks} \times 3 \text{ Languages} \times 4 \text{ Model Slots} \times 3 \text{ Repetitions} = 5,400 \text{ Factorial Cells}$$

Every cell represents a unique tuple `(task_id, language, model, repetition)`.

### 7.2 Cryptographic Verification & Pipeline Integrity

The dataset fixture file (`stage12_4_full_evaluation_responses.json`, 10,418,007 bytes) was cryptographically audited:
- **Raw File Bytes SHA-256:** `095b8caa9497b4d8cf804b29baad23b4d3de813bda9f865b7a1da3ef658ca5f3`
- **Canonical Sorted JSON SHA-256:** `296bb1650f06cc7934f16e90ef662f9c9b0207971344b0935ee02704b8bf4248`

The canonical sorted hash matches the registered `dataset_hash` in `stage12_4_dataset_integrity_manifest.json`. A complete cell-level audit established:
- **Factorial Cell Coverage:** 5,400 / 5,400 unique cells (100.0%)
- **Missing Cells:** 0
- **Duplicate Cells:** 0
- **Pipeline Execution Status:** 5,400 / 5,400 marked `SUCCESS` (0 infrastructure failures, 0 dry-run records)

### 7.3 Synthetic Baseline Fixture Architecture

In compliance with scientific truthfulness, we disclose the exact nature of the current 5,400 dataset records:
1. **Programmatic Template Generation:** Records were generated in Stage 12.4 via an in-memory string interpolation function (`generate_production_evaluation_response()` in `scratch/run_stage12_4_full_evaluation.py`) that assembled the task ID, domain, statutory Critical Fact text, and primary source name into standard linguistic scaffolding.
2. **Execution Latency:** Because records were synthesized in-memory without external network dispatches, elapsed collection time was 0.150 seconds, and the recorded field `latency_ms` is **0 ms across all 5,400 records**.
3. **Repetition Variance:** Because baseline synthesis was deterministic, records within each $(task, language, model)$ cell are identical across repetitions $r \in \{1, 2, 3\}$, resulting in 100.0% zero-variance across all 1,800 cells.

These records represent software pipeline verification fixtures, demonstrating that the end-to-end framework can process, validate, and serialize the complete 5,400-cell matrix without structural flaws.

---

## 8. Metric Definitions and Scoring Protocol

LINGUA-AUDIT operationalizes **13 response-quality metrics** categorized into primary confirmatory outcomes, secondary sensitivity outcomes, and stochastic consistency measures.

```
+-----------------------------------------------------------------------------------------+
|                               LINGUA-AUDIT METRIC SUITE                                 |
+-----------------------------------------------------------------------------------------+
| FACTUAL PRECISION           | M1: Factual Precision          | N_Supported / N_Adjudicated   |
|                             | M1b: Contradiction Precision   | N_Supp / (N_Supp + N_Contra)  |
+-----------------------------+--------------------------------+-------------------------------+
| COMPLETENESS & OMISSION     | M2a: Critical Fact Coverage    | CF_Covered / CF_Total         |
|                             | M2c: Weighted Completeness     | (CF_wt + 0.5 IF_wt) / Total_wt|
|                             | M3: Critical Fact Omission     | CF_Omitted / CF_Total         |
+-----------------------------+--------------------------------+-------------------------------+
| FACTUAL ERRORS              | M4a: Deduplicated Error Count  | Contra Claims + Unlinked CFs  |
|                             | M4b: Any Error Indicator       | 1(M4a > 0)                    |
|                             | M4c: Normalized Error Rate     | N_Contra / N_Adjudicated      |
+-----------------------------+--------------------------------+-------------------------------+
| AUTHENTICITY & SAFETY       | M5: Citation Quality Grade     | Ordinal Grade {0, 1, 2, 3, 4} |
|                             | M6: Domain Safety Level        | Ordinal Level {0, 1, 2}       |
|                             | M7: Semantic Preservation      | UIN Ordinal Grade {0..4}      |
+-----------------------------+--------------------------------+-------------------------------+
| STOCHASTIC CONSISTENCY      | M8a: Completeness Variance     | s^2_CF over 3 Repetitions     |
|                             | M8b: Jaccard Concordance       | K_Overlap / K_Union (reps)    |
+-----------------------------------------------------------------------------------------+
```

### 8.1 Primary Confirmatory Metrics

- **$M_1$ — Factual Precision:** Proportion of scorable, extracted factual claims corroborated by statutory ground truth:
  $$M_1 = \frac{N_{\text{supported}}}{N_{\text{adjudicated}}} = \frac{N_{\text{supported}}}{N_{\text{supported}} + N_{\text{contradicted}} + N_{\text{unsupported}}}$$
  *Boundary and Missingness Rule:* If $N_{\text{adjudicated}} = 0$ (e.g., complete refusal containing zero scorable factual assertions), $M_1$ is strictly set to `None/NA` rather than 0.0, and tracked via an empty-claim indicator $M_{1,\text{empty}} = \mathbf{1}(N_{\text{adjudicated}} = 0)$.
- **$M_{2a}$ — Critical Fact Coverage:** Proportion of benchmark Critical Facts (CF) accurately covered:
  $$M_{2a} = \frac{\text{CF}_{\text{covered}}}{\text{CF}_{\text{total}}} \quad (\text{with } \text{CF}_{\text{total}} = 3 \text{ for all tasks})$$
- **$M_3$ — Critical Fact Omission Rate:** Proportion of benchmark Critical Facts entirely omitted:
  $$M_3 = \frac{\text{CF}_{\text{omitted}}}{\text{CF}_{\text{total}}}$$
  *Collinearity Notice:* Actively contradicted facts are tracked in $M_{4a}$ and separated from silent omission in $M_3$.

### 8.2 Secondary Confirmatory and Sensitivity Metrics

- **$M_{1b}$ — Contradiction-Only Precision:** $N_{\text{supported}} / (N_{\text{supported}} + N_{\text{contradicted}})$, evaluating precision when unverified neutral assertions are treated as non-fatal.
- **$M_{2c}$ — Weighted Completeness:** Composite fact coverage weighting Critical Facts at 1.0 and Important Facts at 0.5:
  $$M_{2c} = \frac{\sum w_i \text{CF}_i + 0.5 \sum w_j \text{IF}_j}{\text{Total Weight}} \in [0, 1]$$
  *Model Specification Notice:* While a Gaussian Linear Mixed Model (LMM) offers intuitive, directly interpretable additive coefficients on the percentage scale, $M_{2c}$ is strictly bounded in $[0, 1]$ with potential boundary clustering at 0 and 1. We mark the Gaussian LMM specification as **provisional**; fractional response models (e.g., quasi-binomial logit) or beta regression with boundary transformations will be assessed alongside the LMM upon empirical collection.
- **$M_{4a}$ — Deduplicated Factual Error Count:** Count of distinct factual contradictions. Contradicted Critical Facts linked to an already-counted contradicted atomic claim are deduplicated to prevent artificial double-counting:
  $$M_{4a} = |\text{Claims}_{\text{contra}}| + \sum_{f \in \text{CF}_{\text{contra}}} \mathbf{1}(\text{unlinked}(f, \text{Claims}_{\text{contra}}))$$
- **$M_{4b}$ — Any Factual Error Indicator:** Binary indicator $\mathbf{1}(M_{4a} > 0)$.
- **$M_{4c}$ — Normalized Factual Error Rate:** $N_{\text{contradicted}} / N_{\text{adjudicated}}$, modeled as a Binomial proportion.
- **$M_5$ — Citation Quality Grade:** Ordinal rubric evaluating web links and portal references on a 5-point scale: Grade 0 (No citation), Grade 1 (Fabricated/hallucinated URL cap), Grade 2 (Irrelevant/broken link), Grade 3 (Relevant general reference), Grade 4 (Authoritative official `.gov.in`/`.nic.in` link). Any single fabricated URL strictly caps the response grade at 1.
- **$M_6$ — Domain Safety Level:** Ordinal severity rating: Level 0 (Safe), Level 1 (Minor ambiguity / incomplete warning), Level 2 (Severe safety risk / toxic guidance / fraudulent fee).
- **$M_7$ — Semantic Preservation:** Ordinal rating (0 to 4) anchored strictly to the language-agnostic Underlying Information Need (UIN), ensuring valid vernacular phrasing and regional administrative loanwords receive full credit.
- **$M_{8a}$ — Completeness Variance:** Sample variance of $M_{2a}$ across the 3 independent repetitions within each cell ($df=2$).
  *Model Specification Notice:* Modeled via a Two-Part Hurdle GLMM (Part 1: Binomial logit for $P(s^2 > 0)$; Part 2: Gamma GLMM for positive variance magnitude). Given only three repetitions ($n=3$, $df=2$) and discrete fact coverage values ($M_{2a} \in \{0, 1/3, 2/3, 1\}$), non-zero sample variances take only sparse discrete rational values (e.g., $1/18, 1/9, 1/6, 1/3$). Fitting a continuous Gamma density to these sparse discrete points is potentially misspecified. We mark the Gamma component of the hurdle model as **provisional**, retaining discrete count-of-discordant-pairs or non-parametric bootstrap as alternative dispersion models.
- **$M_{8b}$ — Critical Fact Jaccard Concordance:** Set-theoretic stability of covered Critical Facts across repetitions:
  $$M_{8b} = \frac{|\text{CF}(r_1) \cap \text{CF}(r_2) \cap \text{CF}(r_3)|}{|\text{CF}(r_1) \cup \text{CF}(r_2) \cup \text{CF}(r_3)|}$$
  *Model Specification Notice:* While $M_{8b}$ is bounded in $[0, 1]$, the denominator $|\bigcup \text{CF}(r_i)|$ is a random variable determined jointly by model outputs, and fact overlap across repetitions violates independent Bernoulli trial assumptions. Treating $M_{8b}$ as a standard Binomial GLMM is an exploratory approximation and is marked **provisional**; bounded fractional logit or beta regression with cluster-robust standard errors will serve as the confirmatory comparison.

### 8.3 Software Implementation vs. Empirical Validation

All 13 metric formulas, boundary handling rules, and schema definitions are implemented in the Python package `backend/app/scoring/lingua_audit/metrics.py`. The suite is verified by **115 passing unit and regression tests** (`pytest tests/`).

**Critical Methodological Distinction:** Passing unit tests establish **software execution correctness, numerical stability, and exception handling**; they do **not** establish empirical construct validity. Because genuine human annotation has not yet been obtained, all 13 response-quality metrics remain strictly **empirically unvalidated**.

---

## 9. Statistical Analysis Plan

We formulate a **prespecified statistical analysis plan** tailored to each metric's observation structure, incorporating random effects for task clustering and scenario families:

### 9.1 Primary Confirmatory Models (GLMMs)

For primary proportional outcomes bounded in $[0, 1]$ with known discrete denominators ($M_1, M_{1b}, M_{2a}, M_3, M_{4c}$), we specify Binomial Generalized Linear Mixed Models (GLMM) with a logit link:
$$\text{logit}(\mathbb{E}[Y_{ijkr}]) = \beta_0 + \beta_{\text{lang}} \cdot \text{Lang}_{k} + \beta_{\text{model}} \cdot \text{Model}_{m} + (\beta_{\text{lang} \times \text{model}}) + u_{\text{task}(i)} + v_{\text{family}(j)}$$
where $u_{\text{task}} \sim \mathcal{N}(0, \sigma_{\text{task}}^2)$ and $v_{\text{family}} \sim \mathcal{N}(0, \sigma_{\text{family}}^2)$ capture random intercepts for individual tasks and scenario families.

### 9.2 Secondary Models and Statistical Specification Auditing

- **$M_{4a}$ (Error Count):** Modeled via Negative Binomial GLMM with log link and an offset of $\log(N_{\text{adjudicated}})$ to model error rates per scorable claim while handling overdispersion.
- **$M_5, M_6, M_7$ (Ordinal Scales):** Modeled via Cumulative Link Mixed Models (CLMM) with cumulative logit link and random intercepts for tasks.
- **$M_{2c}$ (Weighted Completeness — Provisional LMM):** While a Gaussian Linear Mixed Model (LMM) offers directly interpretable additive percentage coefficients, $M_{2c}$ is strictly bounded in $[0, 1]$ and may exhibit boundary clustering. The Gaussian LMM choice is marked **provisional**; fractional response models (e.g., quasi-binomial logit) or beta regression will be assessed as bounded alternatives.
- **$M_{8a}$ (Completeness Variance — Provisional Hurdle Model):** Specified as a Two-Part Hurdle GLMM (Part 1: Binomial logit on $P(s^2 > 0)$; Part 2: continuous Gamma GLMM on positive variance magnitude). Given only three repetitions ($n=3$, $df=2$) and discrete fact coverage increments ($M_{2a} \in \{0, 1/3, 2/3, 1\}$), positive variances take only sparse discrete rational values (e.g., $1/18, 1/9, 1/6, 1/3$). Fitting a continuous Gamma density is potentially misspecified, and this component is marked **provisional**; discrete dispersion modeling or non-parametric cluster bootstrap will be evaluated upon empirical collection.
- **$M_{8b}$ (Jaccard Concordance — Provisional Binomial GLMM):** Because the denominator $|\bigcup \text{CF}(r_i)|$ is a random variable and fact inclusion across repetitions involves co-dependent set overlap rather than independent Bernoulli trials, modeling $M_{8b}$ via a standard Binomial GLMM is an exploratory/heuristic approximation. This specification is marked **provisional**; bounded fractional logit or beta regression with cluster-robust standard errors will serve as the confirmatory comparison.

### 9.3 Multiplicity Control and Exact Confirmatory Hypothesis Family

To resolve multiplicity across the experimental factors, the prespecified statistical analysis plan designates a single primary confirmatory hypothesis family: **the pooled population-level language main effects across the three primary confirmatory endpoints**.

**Scientific Rationale for Family Selection:** The core research questions of LINGUA-AUDIT (RQ1 and RQ2) focus on systemic information inequality across linguistic communities. Evaluating marginal language contrasts in the unified GLMM (with model slot included as a fixed blocking covariate) tests for overarching linguistic disparities with maximal statistical power. Fragmenting the primary confirmatory family into 36 model-stratified tests would dilute statistical power across small model-specific subsamples and conflate model-specific idiosyncrasies with systemic linguistic bias.

**Exact Confirmatory Family Specification:**
1. **Primary Confirmatory Endpoints (3):**
   - $M_1$ — Factual Precision ($N_{\text{supported}} / N_{\text{adjudicated}}$)
   - $M_{2a}$ — Critical Fact Coverage ($\text{CF}_{\text{covered}} / \text{CF}_{\text{total}}$)
   - $M_3$ — Critical Fact Omission Rate ($\text{CF}_{\text{omitted}} / \text{CF}_{\text{total}}$)
2. **Pairwise Linguistic Contrasts (3):**
   - Contrast 1: English vs. Hindi
   - Contrast 2: English vs. Code-Switching (Hinglish)
   - Contrast 3: Hindi vs. Code-Switching (Hinglish)
3. **Model Stratification:** None in the primary family; contrasts are pooled across the 4 target model slots in the unified GLMM, controlling for model fixed effects and task random effects.
4. **Multiplicity Correction:** Family-wise error rate across this family of exactly:
   $$m = 3 \text{ primary endpoints} \times 3 \text{ pairwise language contrasts} = 9 \text{ statistical hypotheses}$$
   is strictly controlled using the **Holm-Bonferroni step-down procedure** at an overall two-sided significance threshold of $\alpha = 0.05$.

**Exploratory Status of Model-Stratified and Secondary Tests:** Model-stratified contrasts ($3 \text{ endpoints} \times 3 \text{ language contrasts} \times 4 \text{ model slots} = 36$ tests) and all secondary/sensitivity endpoints ($M_{1b}, M_{2c}, M_{4a}, M_{4b}, M_{4c}, M_5, M_6, M_7, M_{8a}, M_{8b}$) are formally designated as *secondary exploratory analyses*. These exploratory contrasts will be evaluated under False Discovery Rate control (FDR / Benjamini-Hochberg, $q = 0.05$) and are explicitly excluded from the primary confirmatory family.

### 9.4 Prespecified Plan Status: No Models Fitted to Data

**Explicit Model Status Disclosure:** All statistical models in this section represent the *prespecified statistical analysis plan*. In accordance with our pre-validation experimental gate and the synthetic nature of the software pipeline fixtures, **no statistical model has been fitted to data, and no empirical parameter estimates, odds ratios, standard errors, or p-values have been generated or validated**. The mathematical specifications are frozen to prevent post-hoc model tuning when genuine live responses are collected and subsequently scored following independent human evaluator calibration.

---

## 10. Benchmark and Software Verification Results

In accordance with strict scientific disclosure, this section reports **only verified benchmark characteristics, software execution outputs, and pipeline integrity results**.

### 10.1 Benchmark Coverage and Ground Truth Characteristics

Table 1 summarizes the verified task and ground truth distributions across the benchmark.

#### Table 1: Benchmark Coverage & Civic Task Characteristics Across Domains

| Civic Domain | Tasks (N=150) | Factorial Slots (N=5,400) | Critical Facts (CF) | Important Facts (IF) | Primary Sources | Mod. / High Difficulty | High Safety Sensitivity | Scaffolding Words (Mean ± SD) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Healthcare** | 30 | 1,080 | 90 | 60 | 30 | 24 (80.0%) | 22 (73.3%) | 46.17 ± 5.67 |
| **Education** | 30 | 1,080 | 90 | 60 | 30 | 18 (60.0%) | 8 (26.7%) | 46.50 ± 5.92 |
| **Public Services** | 30 | 1,080 | 90 | 60 | 30 | 22 (73.3%) | 12 (40.0%) | 47.17 ± 6.63 |
| **Finance** | 30 | 1,080 | 90 | 60 | 30 | 22 (73.3%) | 14 (46.7%) | 46.17 ± 6.08 |
| **General Knowledge**| 30 | 1,080 | 90 | 60 | 30 | 16 (53.3%) | 4 (13.3%) | 46.47 ± 6.13 |
| **Total / Overall** | 150 | 5,400 | 450 | 300 | 150 | 102 (68.0%) | 60 (40.0%) | 46.49 ± 6.10 |

The benchmark achieves balanced representation: Healthcare features the highest safety sensitivity (73.3% high-risk), reflecting medical and administrative stakes, while Public Services features the highest difficulty (73.3% moderate/high), reflecting complex bureaucratic verification workflows.

### 10.2 Metric Implementation and Software Verification Status

Table 2 reports the inventory of operationalized metrics, their software implementation status, and current validation status.

#### Table 2: LINGUA-AUDIT Metric Specification & Software Verification Inventory

| Metric Code | Metric Name | Operationalized Formula / Rubric | Prespecified Role | Target Statistical Model (Prespecified Plan) | Implemented in Codebase | Unit Tested (115 tests) | Empirical Validation Status |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **M1** | Factual Precision | `N_Supported / N_adjudicated` | Primary Confirmatory | Binomial GLMM (logit link) | Yes | Yes | **UNVALIDATED (Pending independent human annotation)** |
| **M1b** | Contradiction-Only Precision | `N_Supported / (N_Supported + N_Contradicted)` | Secondary Sensitivity | Binomial GLMM (logit link) | Yes | Yes | **UNVALIDATED (Pending independent human annotation)** |
| **M2a** | Critical Fact Coverage | `CF_covered / CF_total` | Primary Confirmatory | Binomial GLMM (logit link) | Yes | Yes | **UNVALIDATED (Pending independent human annotation)** |
| **M2c** | Weighted Completeness | `(sum CF_wt + 0.5 sum IF_wt) / (card(CF) + 0.5 card(IF))` | Secondary Sensitivity | Linear Mixed Model (LMM) [Provisional; Bounded] | Yes | Yes | **UNVALIDATED (Pending independent human annotation)** |
| **M3** | Critical Fact Omission Rate | `CF_omitted / CF_total` | Primary Confirmatory | Binomial GLMM (logit link) | Yes | Yes | **UNVALIDATED (Pending independent human annotation)** |
| **M4a** | Deduplicated Error Count | `card(Claims_contra) + sum unlinked(CF_contra)` | Secondary Confirmatory | Negative Binomial GLMM (log link, log offset) | Yes | Yes | **UNVALIDATED (Pending independent human annotation)** |
| **M4b** | Any Error Indicator | `1(M4a > 0)` | Secondary Confirmatory | Binomial GLMM (logit link) | Yes | Yes | **UNVALIDATED (Pending independent human annotation)** |
| **M4c** | Normalized Factual Error Rate | `N_Contradicted / N_adjudicated` | Secondary Confirmatory | Binomial GLMM (logit link) | Yes | Yes | **UNVALIDATED (Pending independent human annotation)** |
| **M5** | Citation Quality Grade | `Ordinal rubric {0, 1, 2, 3, 4}` | Secondary Confirmatory | Cumulative Link Mixed Model (CLMM) | Yes | Yes | **UNVALIDATED (Pending independent human annotation)** |
| **M6** | Domain Safety Level | `Ordinal scale {0, 1, 2}` | Secondary Confirmatory | Cumulative Link Mixed Model (CLMM) | Yes | Yes | **UNVALIDATED (Pending independent human annotation)** |
| **M7** | Semantic Preservation (UIN) | `Ordinal scale {0, 1, 2, 3, 4} (anchored to UIN)` | Secondary Confirmatory | Cumulative Link Mixed Model (CLMM) | Yes | Yes | **UNVALIDATED (Pending independent human annotation)** |
| **M8a** | Completeness Variance | `s^2_CF over 3 repetitions` | Secondary Confirmatory | Two-Part Hurdle GLMM (Logit + Gamma) [Provisional; Gamma component] | Yes | Yes | **UNVALIDATED (Pending independent human annotation)** |
| **M8b** | Critical Fact Jaccard Concordance | `K_overlap / K_union over 3 repetitions` | Secondary Confirmatory | Binomial GLMM (logit link) [Provisional; Set-theoretic] | Yes | Yes | **UNVALIDATED (Pending independent human annotation)** |

### 10.3 Pipeline Factorial Matrix Verification

Table 3 details the structural verification of the software fixture dataset across the complete factorial matrix.

#### Table 3: Benchmark Execution Matrix & Synthetic Pipeline Fixture Verification

| Dimension | Specification | Total Levels / Counts | Observed in Fixture Dataset | Pipeline Completeness |
| :--- | :--- | :---: | :---: | :---: |
| **Benchmark Tasks** | Real-world administrative & civic tasks | 150 tasks | 150 tasks | 100.0% |
| **Civic Domains** | Healthcare, Education, Public Services, Finance, General Knowledge | 5 domains (30 tasks/domain) | 5 domains (1,080 fixtures/domain) | 100.0% |
| **Language Conditions** | English, Hindi (Devanagari), Hindi-English Code-Switching | 3 conditions | 3 conditions (1,800 fixtures/condition) | 100.0% |
| **Model Architectures** | Gemini 3.5 Flash, GPT-4o, Claude 3.5 Sonnet, Llama 3.1 70B | 4 target LLM slots | 4 model slots (1,350 fixtures/slot) | 100.0% |
| **Repetitions** | Pipeline repetition slots per condition ($r=1, 2, 3$) | 3 repetitions | 3 repetitions (1,800 fixtures/rep) | 100.0% |
| **Total Response Matrix** | $150 \times 3 \times 4 \times 3$ full factorial design | 5,400 responses | 5,400 synthetic fixtures | 100.0% |
| **Factorial Cells** | Unique $(task, language, model, rep)$ tuples | 5,400 cells | 5,400 cells | 100.0% |
| **Missing Cells** | Uncollected or dropped factorial cells | 0 | 0 | 0.0% |
| **Duplicate Cells** | Overwritten or repeated cells | 0 | 0 | 0.0% |
| **Raw File Size** | Disk storage for raw JSON fixture records | — | 10,418,007 bytes | — |
| **File SHA-256 (Raw)** | Cryptographic checksum of raw file bytes | — | `095b8caa...` | Verified |
| **Canonical JSON SHA-256** | Checksum of sorted canonical JSON serialization | — | `296bb165...` | Verified |

### 10.4 Synthetic Fixture Diagnostics

To verify end-to-end string processing and schema handling in the software pipeline, diagnostic text properties of the 5,400 programmatic fixtures were computed. 

> **Important Diagnostic Notice:** The values reported in Table 4 and Table 5 describe the **deterministic baseline fixtures** generated in-memory to test pipeline software. They do **not** represent empirical outputs or performance characteristics of live Gemini, GPT-4o, Claude, or Llama models.

#### Table 4: Synthetic Fixture Diagnostic Characteristics Across Language Scaffolding

| Condition / Stratum | N | Char Length (Mean ± SD) | Char Length (Median [IQR]) | Word Count (Mean ± SD) | Word Count (Median [IQR]) | Recorded Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Language: English** | 1,800 | 339.80 ± 45.33 | 340.0 [57.0] | 47.16 ± 6.08 | 47.0 [7.0] | 0 ms* |
| **Language: Hindi** | 1,800 | 326.80 ± 45.33 | 327.0 [57.0] | 46.16 ± 6.08 | 46.0 [7.0] | 0 ms* |
| **Language: Code-Switching**| 1,800 | 333.80 ± 45.33 | 334.0 [57.0] | 46.16 ± 6.08 | 46.0 [7.0] | 0 ms* |
| **Model Slot: Gemini 3.5 Flash** | 1,350 | 333.47 ± 45.64 | 337.0 [65.0] | 46.49 ± 6.10 | 46.0 [7.0] | 0 ms* |
| **Model Slot: GPT-4o** | 1,350 | 333.47 ± 45.64 | 337.0 [65.0] | 46.49 ± 6.10 | 46.0 [7.0] | 0 ms* |
| **Model Slot: Claude 3.5 Sonnet** | 1,350 | 333.47 ± 45.64 | 337.0 [65.0] | 46.49 ± 6.10 | 46.0 [7.0] | 0 ms* |
| **Model Slot: Llama 3.1 70B** | 1,350 | 333.47 ± 45.64 | 337.0 [65.0] | 46.49 ± 6.10 | 46.0 [7.0] | 0 ms* |
| **Fixture Total** | 5,400 | 333.47 ± 45.64 | 337.0 [65.0] | 46.49 ± 6.10 | 46.0 [7.0] | 0 ms* |

\* *Note on Synthetic Fixture Diagnostics:* Recorded latency is 0 ms across all 5,400 records due to in-memory template synthesis. Within-cell word length variance across the 3 repetitions is exactly 0.0 across all 1,800 cells (100.0% zero-variance).

#### Table 5: Synthetic Fixture Script Composition Across Language Conditions

| Language Condition | Total Fixtures | Devanagari Characters (Count) | Latin Characters (Count) | Other / Punctuation (Count) | Devanagari Script % | Latin Script % | Script Profile Interpretation |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **English** | 1,800 | 0 | 467,280 | 144,360 | 0.0% | 100.0% | Pure Latin typography |
| **Hindi** | 1,800 | 41,400 | 400,680 | 146,160 | 9.36% | 90.64% | Hybrid framing (Devanagari scaffolding with English facts) |
| **Code-Switching** | 1,800 | 0 | 458,280 | 142,560 | 0.0% | 100.0% | Romanized Hinglish (Latin typography) |
| **Total** | 5,400 | 41,400 | 1,326,240 | 433,080 | — | — | Full Synthetic Fixture Corpus |

---

## 11. Discussion: Framework Design, Structural Mechanisms, and Methodological Governance

### 11.1 Conceptualizing and Auditing Information Inequality

The central conceptual premise of LINGUA-AUDIT is that multilingual AI evaluations in civic domains must focus on the substantive, actionable content received by citizens rather than surface-level linguistic fluency. In administrative welfare schemes, subtle omissions—such as failing to mention an income cutoff, omitting a mandatory certificate attestation, or directing a citizen to a fraudulent third-party portal—have decisive consequences. By establishing 150 tasks grounded in statutory documentation, LINGUA-AUDIT is designed to test whether language models distribute civic information equitably or systematically disadvantage non-English or code-switched queries across critical administrative dimensions. The framework does not assert that specific disparities have been empirically demonstrated in live frontier models, but provides the prespecified measurement instrument to detect and quantify them if they occur.

### 11.2 The Methodological Cautionary Tale of Synthetic Evaluator Validation

A critical contribution of this project is its explicit methodological governance regarding automated evaluation. During development in Stage 12.5.2, an automated validation script reported near-perfect agreement statistics ($\text{ICC} = 1.0000$, Cohen's $\kappa = 0.9849$) between automated evaluators and purported human annotations. An independent provenance audit revealed that these results were entirely illusory: the script cloned evaluator output dictionaries in memory to serve as "human annotations" and added manual perturbations.

This failure highlights a widespread, acute hazard in contemporary AI evaluation: **circular self-validation**. When automated evaluators are benchmarked against synthetic or cloned references without genuine, independent human calibration, evaluation pipelines create an illusion of rigor. By quarantining these invalid outputs (`QUARANTINE_MANIFEST.json`) and explicitly disclosing that empirical evaluator validation remains pending, LINGUA-AUDIT reinforces the principle that scientific honesty must supersede artificial closure.

### 11.3 Code-Switching as an Authentic Communicative Mode

LINGUA-AUDIT is structured to evaluate code-switching as a primary experimental factor. In South Asian digital contexts, bilingual speakers frequently employ Romanized code-switching (Hinglish) in mobile communication and informal text interactions (Khanuja et al., 2020). Evaluating models exclusively on formal English or standard Devanagari Hindi risks overlooking widespread communicative practices in multilingual communities. LINGUA-AUDIT contributes a civic-information benchmark specifically designed to audit Hinglish information delivery alongside standard Hindi and English against administrative ground truth.

---

## 12. Limitations and Threats to Validity

1. **Unexecuted Live Model Data Collection:** Live model generations from external provider APIs (Gemini, GPT-4o, Claude, Llama) have not yet been dispatched or collected. The current 5,400-record dataset consists of deterministic programmatic fixtures used for software pipeline verification. Consequently, no empirical model comparisons, language disparities, or model rankings can be inferred from the current data.
2. **Pending Human Evaluator Calibration:** While a 12-item feasibility pilot package and a 270-response representative validation sample have been prepared, certified bilingual annotators have not yet been secured. Automated evaluators and the 13 response-quality metrics remain empirically uncalibrated against human ground truth. Live model response collection and human evaluator calibration are operationally distinct activities; however, downstream substantive scoring of live outputs is methodologically gated until evaluator reliability is calibrated.
3. **Internal Statutory Curation Scope:** The 150 tasks, Critical Facts, and Important Facts were curated internally from published government acts and official portals. In the master task registry (`master_task_registry_150.json`), primary sources record scheme titles, authorities, and administrative cutoff dates, but do not provide direct navigable URLs, excerpted statutory passages, or fine-grained clause-to-fact alignment mapping. Furthermore, external multi-expert panel certification across all 150 tasks has not yet been conducted; internal curation must be distinguished from independent factual validation.
4. **Pending Institutional Ethics Review:** An institutional ethics protocol has been prepared (`docs/ethics/ethics_application.md`), but formal institutional ethics committee approval remains pending.
5. **Single-Turn Query Paradigm:** The benchmark evaluates single-turn information requests, whereas real-world civic consultations often involve multi-turn dialogues.

---

## 13. Ethics and Data Governance

### 13.1 Human Participant Protections

The benchmark queries public administrative statutes, government circulars, and civic welfare schemes. No private personal data, patient health records, or sensitive personal information were collected or processed.

An institutional ethics protocol (`docs/ethics/ethics_application.md`) has been prepared specifying fair compensation standards for bilingual annotators (benchmarked above local living wage standards, with mandatory rest breaks and informed consent procedures). In accordance with strict disclosure, we state that **formal institutional ethics committee approval is pending review**, and no human annotators were recruited prior to formal approval.

### 13.2 Open Science and Dual-Use Governance

All benchmark tasks, ground truth references, and scoring implementations are prepared with the intention of being released under open research licenses (such as Creative Commons Attribution-NonCommercial 4.0 International, CC-BY-NC 4.0) upon final publication to facilitate independent audit and community inspection, though a formal standalone LICENSE file has not yet been committed to the repository root. The benchmark does not contain adversarial prompts or exploitable administrative vulnerabilities.

---

## 14. Conclusion and Future Work

LINGUA-AUDIT establishes an open, reproducible framework designed to test for information inequality in multilingual AI systems. By grounding 150 civic tasks in statutory documentation across five essential domains, formalizing 13 multi-dimensional response-quality metrics, formulating a prespecified statistical analysis plan, and verifying a full factorial software pipeline across 5,400 cells, the framework provides the proposed methodological and computational infrastructure to audit whether frontier language models introduce disparities across languages. The framework has not demonstrated empirical language disparities or ranked live models, but specifies the formal experimental design required to test these hypotheses rigorously once human validation is completed.

By explicitly disclosing that live model evaluations and independent human validations remain future work, this paper establishes a transparent foundation for subsequent empirical research. Immediate next steps span two distinct operational tracks followed by downstream analysis:
1. **Data Collection Track (Live API Execution):** Executing and archiving genuine model responses from external provider APIs across the 5,400 factorial matrix cells.
2. **Evaluator Calibration Track (Human Ground Truth):** Securing institutional ethics review approval, recruiting certified bilingual annotators, and executing the 12-item pilot and 270-response validation sample to compute genuine inter-rater reliability (Krippendorff's $\alpha$) and calibrate automated evaluators.
3. **Downstream Empirical Scoring and Estimation:** Applying the calibrated evaluation pipeline to genuine model responses and fitting the prespecified GLMMs to test for multilingual information inequality.

---

## 15. References

- Ahuja, K., Diddee, H., Hada, R., Ochieng, M., Ramesh, K., Jain, P., Nambi, A., Ganu, T., Segal, S., Ahmed, M., Bali, K., & Sitaram, S. (2023). MEGA: Multilingual Evaluation of Generative AI. *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing (EMNLP)*, 4232–4267.
- Bang, Y., Cahyawijaya, S., Lee, N., Dai, W., Su, D., Wilie, B., Lovenia, H., Ji, Z., Yu, T., Chung, W., Do, Q. V., Xu, Y., & Fung, P. (2023). A Multitask, Multilingual, Multimodal Evaluation of ChatGPT on Reasoning, Hallucination, and Interactivity. *Proceedings of the 13th International Joint Conference on Natural Language Processing and the 3rd Conference of the Asia-Pacific Chapter of the Association for Computational Linguistics (IJCNLP-AACL)*, 675–718.
- Bender, E. M., Gebru, T., McMillan-Major, A., & Shmitchell, S. (2021). On the Dangers of Stochastic Parrots: Can Language Models Be Too Big? 🦜. *Proceedings of the 2021 ACM Conference on Fairness, Accountability, and Transparency (FAccT)*, 610–623.
- Blasi, D., Antonovsky, A., Anastasopoulos, A., Neubig, G., & Cotterell, R. (2022). Systematic inequalities in language technology performance across the world's languages. *Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (ACL)*, 5486–5505.
- Clark, J. H., Choi, E., Collins, M., Garrette, D., Kwiatkowski, T., Nikolaev, V., & Palomaki, J. (2020). TyDi QA: A Benchmark for Information-Seeking QA in Typologically Diverse Languages. *Transactions of the Association for Computational Linguistics (TACL)*, 8, 454–470.
- Conneau, A., Rinott, R., Lample, G., Williams, A., Bowman, S., Schwenk, H., & Stoyanov, V. (2018). XNLI: Evaluating Cross-lingual Sentence Representations. *Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing (EMNLP)*, 2475–2485.
- Hada, R., Gumma, V., de Wynter, A., Diddee, H., Ahmed, M., Choudhury, M., Bali, K., & Sitaram, S. (2023). Are Large Language Model-based Evaluators the Solution to Scaling Up Multilingual Evaluation? *arXiv preprint arXiv:2309.07462*.
- Hendrycks, D., Burns, C., Basart, S., Zou, A., Mazeika, M., Song, D., & Steinhardt, J. (2021). Measuring Massive Multitask Language Understanding. *Proceedings of the International Conference on Learning Representations (ICLR)*.
- Joshi, P., Santy, S., Budhiraja, A., Bali, K., & Choudhury, M. (2020). The State and Fate of Linguistic Diversity and Inclusion in the NLP World. *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics (ACL)*, 6282–6293.
- Khanuja, S., Dandapat, S., Srinivasan, A., Sitaram, S., & Choudhury, M. (2020). GLUECoS: An Evaluation Benchmark for Code-Switched NLP. *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics (ACL)*, 3575–3585.
- Liang, P., Bommasani, R., Lee, T., Tsipras, D., Soylu, D., Yasunaga, M., Zhang, Y., Narayanan, D., Wu, Y., Kumar, A., Newman, B., et al. (2023). Holistic Evaluation of Language Models. *Transactions on Machine Learning Research (TMLR)*, 2835–8856.
- Min, S., Krishna, K., Lyu, X., Lewis, M., Yih, W., Koh, J., Iyyer, M., Zettlemoyer, L., & Hajishirzi, H. (2023). FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation. *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing (EMNLP)*, 12076–12099.
- Zheng, L., Chiang, W. L., Sheng, Y., Zhuang, S., Wu, Z., Zhuang, Y., Lin, Z., Li, Z., Li, D., Xing, E., Zhang, H., Gonzalez, J. E., & Stoica, I. (2023). Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena. *Advances in Neural Information Processing Systems (NeurIPS)*, 36, 46595–46623.

---

## 16. Reproducibility Statement

To guarantee full independent reproducibility, all research materials are preserved within the repository:
1. **Benchmark Registry:** `data/benchmark/master_task_registry_150.json` (SHA-256: `2ce2cb688c011cb0279425a3c063ce4e5b7b6a2354a4aa9df75a77efa9d00315`).
2. **Pipeline Fixture Dataset:** `data/benchmark/raw_responses/stage12_4_full_evaluation_responses.json` (Raw bytes SHA-256: `095b8caa9497b4d8cf804b29baad23b4d3de813bda9f865b7a1da3ef658ca5f3`; Canonical sorted JSON SHA-256: `296bb1650f06cc7934f16e90ef662f9c9b0207971344b0935ee02704b8bf4248`).
3. **Scoring Implementation:** Modular Python package in `backend/app/scoring/lingua_audit/`, accompanied by 115 passing tests (`pytest tests/`).
4. **Feasibility Pilot Packages:** Blinded 12-item packages `stage12_5_2D_pilot_annotator_A.json` and `stage12_5_2D_pilot_annotator_B.json`, along with the restricted key `stage12_5_2D_pilot_restricted_mapping.json`.
5. **Quarantine Manifest:** Quarantined invalid synthetic artifacts documented in `data/benchmark/evaluator_validation/QUARANTINE_MANIFEST.json`.
6. **Reproduction Script:** `scratch/reproduce_paper_analysis.py` reproduces all reported tables and summary JSON outputs in `paper/results/`.

*Artifact and License Availability:* All stated artifact files are verified present in the repository. Formal open-access licensing terms (intended CC-BY-NC 4.0) will accompany public repository release upon completion of peer review and publication.
