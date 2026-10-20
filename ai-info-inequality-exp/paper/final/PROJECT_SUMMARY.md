# LINGUA-AUDIT: Project Summary & Master's Portfolio Dossier

**Project Title:** LINGUA-AUDIT: Auditing Information Inequality in Multilingual AI Systems  
**Author:** Tanya Deep  
**Affiliation:** BMS Institute of Technology and Management, Bengaluru, India  
**Institutional Contact:** `1by23is231@bmsit.in`  
**Current Status:** Preregistered Benchmark Design, Measurement Specification, and Software Auditing Protocol (Frozen Pre-Validation State)  
**Authoritative Final Deliverables:**  
- Final Word Manuscript: [`paper/final/LINGUA_AUDIT_final.docx`](./LINGUA_AUDIT_final.docx)  
- Final Verification PDF: [`paper/final/LINGUA_AUDIT_final.pdf`](./LINGUA_AUDIT_final.pdf)  
- Complete Master Task Registry: [`data/benchmark/master_task_registry_150.json`](../../data/benchmark/master_task_registry_150.json)  
- Cryptographic Verification Manifest: [`data/benchmark/raw_responses/stage12_4_dataset_integrity_manifest.json`](../../data/benchmark/raw_responses/stage12_4_dataset_integrity_manifest.json)  
- Modular Scoring Package: [`backend/app/scoring/lingua_audit/`](../../backend/app/scoring/lingua_audit/)  

---

## 1. Research Problem and Motivation

As generative artificial intelligence (AI) systems and large language models (LLMs) are deployed as automated conversational interfaces for public services, citizen welfare schemes, and civic administration, disparities in model performance across linguistic communities threaten to produce **substantive information inequality**. In developing and multilingual societies such as India, hundreds of millions of citizens interact with digital platforms in non-English vernaculars (e.g., standard Hindi) and informal colloquial dialects (e.g., Romanized Hindi-English code-switching, commonly known as *Hinglish*).

Existing multilingual NLP evaluations predominantly assess surface-level linguistic fluency, cross-lingual perplexity, translation BLEU/ChrF scores, or multiple-choice examinations translated from Western academic curricula (e.g., multilingual MMLU). While informative for measuring general model capability, these benchmarks do not assess whether language models satisfy identical, life-critical civic information needs equitably across languages. If an AI assistant provides accurate statutory income caps, required identity proofs, and official portal URLs in English, but omits mandatory administrative prerequisites, provides hallucinated links, or states outdated financial thresholds in Hindi or Hinglish, citizens suffer severe asymmetric harms: administrative disqualification, missed entitlement deadlines, or economic exploitation.

The core motivation of **LINGUA-AUDIT** is to establish the benchmark design, multi-dimensional measurement specifications, and statistical testing framework required to systematically audit AI-mediated information inequality in statutory civic contexts.

---

## 2. Nearest-Neighbour Benchmark & Defensible Research Gap

### Focused Nearest-Neighbour Analysis

To establish a defensible research gap, LINGUA-AUDIT was critically benchmarked against the closest published research:

1. **Functional / Domain Nearest Neighbour: CitizenQuery-UK** (Majithia et al., 2026; *arXiv:2602.04064*, Open Data Institute / University of Oxford / King's College London):
   - *Accomplishment:* CitizenQuery evaluated LLM factuality, abstention, and verbosity on 22,000+ synthetic citizen queries grounded in authoritative UK public administration data (`gov.uk`).
   - *Limitation relative to LINGUA-AUDIT:* CitizenQuery is exclusively monolingual (UK English), relies on synthetic queries, and does not evaluate cross-lingual disparities, code-switching, or mixed-effects statistical hypothesis testing across language conditions.
2. **Linguistic Nearest Neighbours:**
   - **IndicGenBench** (Singh et al., *ACL 2024*, Google Research India): Evaluated generative capabilities across 29 Indic languages on traditional NLP tasks (translation, summarization, QA) using parallel corpora, but did not evaluate public administration entitlements, omission, or Hinglish code-switching.
   - **IndQA** (OpenAI, 2025): Evaluated cultural fluency across 12 Indian languages (including Hinglish) using 2,278 expert-curated prompts and rubrics across cultural/historical domains, but does not provide an open-source statutory ground-truth benchmark or a prespecified GLMM statistical analysis plan.
   - **GLUECoS** (Khanuja et al., *ACL 2020*): Standardized evaluation for code-switched NLP on discriminative tasks (sentiment, POS, NLI), but did not address generative factuality or civic entitlement guidance.
   - **FActScore** (Min et al., *EMNLP 2023*): Established atomic claim precision ($M_1$) for English Wikipedia biographies, but omitted statutory omission, citation authenticity, and domain safety.

### One-Sentence Research Gap

> *“CitizenQuery established an evaluation framework for citizen queries against authoritative government portals in monolingual English; LINGUA-AUDIT contributes a civic-information benchmark design and statistical mixed-effects protocol specifically structured to audit substantive information disparities across English, Devanagari Hindi, and Romanized Hinglish code-switching in Indian statutory welfare administration.”*

---

## 3. The Project's Actual Contribution

LINGUA-AUDIT contributes a **reproducible benchmark design, measurement specification, and software auditing protocol**. Its contributions are strictly methodological, computational, and pre-experimental:

1. **Frozen Civic-Information Benchmark (150 Tasks):** 150 administrative tasks partitioned equally across five essential societal domains in India (Healthcare, Education, Public Services, Finance, General Knowledge), anchored to language-agnostic Underlying Information Needs (UINs) and 25 unique public administrative authorities.
2. **Multi-Dimensional Operational Measurement Suite (13 Metrics):** Precise mathematical operationalizations with explicit boundary handling for factual precision ($M_1, M_{1b}$), critical fact coverage ($M_{2a}, M_{2c}$), critical fact omission ($M_3$), deduplicated error count ($M_{4a}, M_{4b}, M_{4c}$), citation quality grading ($M_5$), domain safety levels ($M_6$), UIN-anchored semantic preservation ($M_7$), and repetition consistency ($M_{8a}, M_{8b}$).
3. **Prespecified Statistical Analysis Plan:** A rigorous mixed-effects modeling plan specifying Binomial GLMMs, Negative Binomial GLMMs, Cumulative Link Mixed Models (CLMMs), and Two-Part Hurdle models, featuring a designated primary confirmatory family of $m=9$ pooled language main-effect contrasts under Holm–Bonferroni step-down correction ($\alpha = 0.05$).
4. **Reproducible Python Scoring Engine:** A tested Python package (`backend/app/scoring/lingua_audit/`) accompanied by 115 passing unit and regression tests verifying mathematical behavior, boundary conditions, zero-claim edge cases, and serialization integrity.
5. **Exemplary Research Governance:** Explicit forensic quarantine of invalid prior synthetic evaluator validation artifacts, clear separation of software correctness from empirical construct validity, and full disclosure of pending validation gates.

---

## 4. Technical and Methodological Work Completed

- **Curated Benchmark Database:** Formatted 150 tasks in `data/benchmark/master_task_registry_150.json` containing 450 statutory Critical Facts (CFs; exactly 3/task), 300 Important Facts (IFs; exactly 2/task), 150 safety constraints (1/task), and 150 language-agnostic UIN specifications.
- **Factorial Software Pipeline Architecture:** Verified complete end-to-end data ingestion, schema adherence, and cryptographic integrity across a $150 \text{ tasks} \times 3 \text{ languages} \times 4 \text{ model slots} \times 3 \text{ repetitions} = 5,400 \text{-cell}$ factorial matrix.
- **Cryptographic Verification Manifest:** Calculated and verified SHA-256 signatures for the raw file (`095b8caa...`) and sorted canonical JSON serialization (`296bb165...`), confirming 100.0% cell completeness, 0 missing cells, 0 duplicate cells, and 0 infrastructure failures.
- **Feasibility Pilot Instrumentation:** Prepared blinded 12-item human annotation packages (`stage12_5_2D_pilot_annotator_A.json` and `B.json`), a restricted rater key, an annotator manual, and a 270-response representative validation sample for future human-in-the-loop calibration.
- **Typesetting & OpenXML Engineering:** Engineered an automated document generation pipeline producing a 14-page, single-column preprint ([`LINGUA_AUDIT_final.docx`](./LINGUA_AUDIT_final.docx)) adhering to strict academic typography, unclipped tables, display equations, and IEEE numbered referencing.

---

## 5. Verified Software and Reproducibility Achievements

- **115 Passing Unit & Regression Tests:** Full passing test suite (`pytest tests/`) validating metrics calculation, error deduplication logic, Hurdle model formulation, and JSON schema compliance.
- **Zero-Contamination Fixture Profiling:** Transparent diagnostic verification confirming that all 5,400 response records were synthesized in-memory in 0.150 seconds, with recorded latency of 0 ms and 100.0% zero-variance across repetitions, verifying pipeline execution without misrepresenting synthetic data as model output.
- **Forensic Audit & Quarantine Protocol:** Documented the forensic audit of a compromised synthetic validation attempt in Stage 12.5.2 (which cloned evaluator outputs into purported human annotations), established `QUARANTINE_MANIFEST.json`, and completely removed contaminated statistics from the manuscript.

---

## 6. Work Not Yet Completed (Explicit Limitations)

In compliance with academic integrity, the following components are explicitly identified as unexecuted:

1. **Live Model API Execution:** No live commercial endpoints (Gemini, GPT-4o, Claude, Llama) were queried; the four model entries represent architectural slots in the benchmark execution protocol.
2. **Empirical Construct Validation:** All 13 response-quality metrics remain empirically unvalidated; unit tests establish algorithmic execution correctness, not human agreement.
3. **Independent Human Rater Calibration:** Independent bilingual human annotators have not yet been recruited or scored; inter-rater reliability ($\text{Krippendorff's } \alpha$) has not been calculated.
4. **Fitted Statistical Models:** No statistical models have been fitted to genuine response data; zero parameter estimates, odds ratios, or $p$-values have been generated.
5. **External Legal Certification:** Task ground-truth references represent internal author curation from published government circulars and acts, without external legal-expert panel certification, direct URLs, or clause-level mapping.
6. **Institutional Ethics Approval:** Institutional ethics committee review remains formally pending.

---

## 7. Master's Application CV & Personal Statement Description

*Below is a truthful, academically rigorous description suitable for a graduate application CV, personal statement, or research portfolio:*

> **LINGUA-AUDIT: Auditing Information Inequality in Multilingual AI Systems**  
> *Independent Research Project | BMS Institute of Technology and Management (2026)*  
> - Conceptualized and developed a reproducible benchmark design and statistical auditing protocol to evaluate substantive information inequality across English, Hindi, and Hindi-English code-switching (Hinglish) in civic administrative AI.  
> - Curated 150 statutory civic tasks grounded in 25 public administrative authorities across 5 societal domains in India, formalizing 13 operational metrics spanning factual precision, omission, deduplicated errors, and cross-repetition variance.  
> - Formulated a prespecified mixed-effects statistical analysis plan utilizing Binomial GLMMs, CLMMs, and Two-Part Hurdle models with family-wise error rate control ($m=9$ pooled language tests under Holm–Bonferroni step-down correction).  
> - Engineered a modular Python scoring engine verified by 115 passing unit tests across a 5,400-cell factorial software fixture matrix with cryptographic SHA-256 integrity checks.  
> - Enforced rigorous research integrity by auditing and quarantining flawed synthetic evaluator self-validation artifacts, establishing an explicit pre-registration gate separating software verification from future human construct validation and live model evaluation.  
> - Authored a 14-page preprint manuscript formatted to international academic standards with complete technical appendices and open-science documentation.
