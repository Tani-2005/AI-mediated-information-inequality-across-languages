# LINGUA-AUDIT: Auditing Information Inequality in Multilingual AI Systems

[![Status: Frozen Benchmark & Protocol](https://img.shields.io/badge/Status-Frozen_Benchmark_%26_Protocol-blue.svg)](#)
[![Tests: 115 Passed](https://img.shields.io/badge/Tests-115_Passed-brightgreen.svg)](#)
[![License: CC-BY-NC 4.0](https://img.shields.io/badge/License-CC--BY--NC_4.0-lightgrey.svg)](#)
[![Python: 3.11+](https://img.shields.io/badge/Python-3.11+-informational.svg)](#)
[![Author: Tanya Deep](https://img.shields.io/badge/Author-Tanya_Deep-purple.svg)](#)

> **A Reproducible Civic-Information Benchmark Design, Measurement Specification, and Statistical Auditing Protocol for Multilingual AI Systems**

---

## 📌 Author and Project Metadata

- **Author:** Tanya Deep
- **Affiliation:** BMS Institute of Technology and Management, Bengaluru, India
- **Institutional Contact:** [`1by23is231@bmsit.in`](mailto:1by23is231@bmsit.in)
- **Status:** Preregistered Benchmark Design & Software Framework (Frozen Pre-Validation State — October 2026)

---

## 📄 Authoritative Manuscript & Deliverables

The complete, publication-ready preprint and portfolio documentation are available in the repository:

| Document | Format | Description |
| :--- | :---: | :--- |
| [**Final Manuscript (Word)**](./ai-info-inequality-exp/paper/final/LINGUA_AUDIT_final.docx) | `.docx` | 14-page publication-quality Word deliverable (editable OpenXML, booktabs tables, display equations, IEEE citations). |
| [**Final Manuscript (PDF)**](./ai-info-inequality-exp/paper/final/LINGUA_AUDIT_final.pdf) | `.pdf` | Verification PDF exported via Microsoft Word COM automation. |
| [**Project Summary Dossier**](./ai-info-inequality-exp/paper/final/PROJECT_SUMMARY.md) | `.md` | Comprehensive research summary, nearest-neighbour analysis, and master's portfolio statement. |
| [**Master Task Registry**](./ai-info-inequality-exp/data/benchmark/master_task_registry_150.json) | `.json` | Frozen benchmark of 150 statutory civic tasks with 450 Critical Facts, 300 Important Facts, and 150 UINs. |
| [**Modular Scoring Engine**](./ai-info-inequality-exp/backend/app/scoring/lingua_audit/) | Python | Tested Python implementation of all 13 response-quality metrics and boundary rules. |
| [**Cryptographic Manifest**](./ai-info-inequality-exp/data/benchmark/raw_responses/stage12_4_dataset_integrity_manifest.json) | `.json` | Registered SHA-256 integrity hashes for the 5,400-cell factorial software matrix. |

---

## 🔍 Research Problem and Overview

As large language models (LLMs) are deployed as conversational intermediaries for public services, statutory welfare schemes, and civic administration, disparities in model performance across linguistic communities threaten to produce **substantive information inequality**. In multilingual societies like India, citizens querying digital systems in non-English vernaculars (standard Hindi) or informal colloquial dialects (Romanized Hindi-English code-switching, commonly known as *Hinglish*) risk receiving incomplete, outdated, misleading, or factually erroneous guidance.

Existing multilingual evaluations predominantly assess surface-level capabilities: cross-lingual perplexity, translation BLEU/ChrF scores, or multiple-choice examinations translated from Western academic curricula (e.g., multilingual MMLU). While valuable for broad capability measurement, **they do not measure information inequality**.

**LINGUA-AUDIT** establishes an open, reproducible civic-information benchmark design, measurement protocol, and auditing framework to systematically audit whether generative AI systems satisfy identical civic information needs equitably across languages.

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

---

## 🎯 Key Contributions

1. **Curated Civic-Information Benchmark (150 Tasks):**
   - Grounded in 25 official statutory authorities across five essential domains in India: **Healthcare** ($N=30$), **Education** ($N=30$), **Public Services** ($N=30$), **Finance** ($N=30$), and **General Knowledge & Civic Rights** ($N=30$).
   - Indexed by language-agnostic **Underlying Information Needs (UINs)** to eliminate English-normative translation bias.
2. **Multi-Dimensional Operational Measurement Suite (13 Metrics):**
   - **Factual Precision:** $M_1$ (Supported / Adjudicated claims), $M_{1b}$ (Contradiction precision).
   - **Completeness & Omission:** $M_{2a}$ (Critical Fact coverage), $M_{2c}$ (Weighted completeness), $M_3$ (Critical Fact omission rate).
   - **Factual Errors:** $M_{4a}$ (Deduplicated contradiction count), $M_{4b}$ (Any error indicator), $M_{4c}$ (Normalized contradiction rate).
   - **Authenticity & Safety:** $M_5$ (Citation quality grade on 5-point ordinal scale), $M_6$ (Domain safety risk level on 3-point scale), $M_7$ (UIN-anchored semantic preservation).
   - **Stochastic Consistency:** $M_{8a}$ (Sample variance of fact coverage over 3 repetitions), $M_{8b}$ (Set-theoretic Critical Fact Jaccard concordance).
3. **Prespecified Mixed-Effects Statistical Analysis Plan:**
   - Unified Binomial GLMMs, Negative Binomial GLMMs, CLMMs, and Two-Part Hurdle models controlling for task clustering ($u_{\text{task}}$) and scenario family ($v_{\text{family}}$).
   - Explicit family-wise error control across a designated confirmatory family of **$m=9$ pooled language main-effect contrasts** under **Holm–Bonferroni step-down correction** ($\alpha = 0.05$).
4. **Reproducible Software Architecture:**
   - Full factorial matrix across $150 \text{ tasks} \times 3 \text{ languages} \times 4 \text{ target model slots} \times 3 \text{ repetitions} = 5,400 \text{ cells}$.
   - Verified by **115 passing unit and regression tests** (`pytest`).
5. **Methodological Governance:**
   - Audited and quarantined compromised synthetic self-validation scripts (`QUARANTINE_MANIFEST.json`).
   - Transparent separation of software verification correctness from empirical construct validity.

---

## 🔬 Nearest-Neighbour Novelty Comparison

| Benchmark | Focus | Overlap with LINGUA-AUDIT | Defensible Distinction of LINGUA-AUDIT |
| :--- | :--- | :--- | :--- |
| **CitizenQuery-UK**<br>*(Majithia et al., 2026)* | Evaluates LLM factuality and abstention on 22,000+ UK citizen queries mapped to `gov.uk`. | Focuses on public administration, welfare schemes, and official government data. | CitizenQuery is monolingual (UK English). LINGUA-AUDIT evaluates multilingual disparities across English, Hindi, and Romanized Hinglish code-switching with a prespecified GLMM statistical framework. |
| **IndQA**<br>*(OpenAI, 2025)* | Evaluates cultural fluency across 12 Indian languages and Hinglish (2,278 prompts). | Tests regional Indian languages and Hinglish with expert rubrics. | IndQA focuses on cultural, historical, and lifestyle reasoning. LINGUA-AUDIT focuses on statutory administrative welfare entitlements with an open-source GLMM statistical plan. |
| **IndicGenBench**<br>*(Singh et al., ACL 2024)* | Evaluates generation across 29 Indic languages on translation, summarization, and QA. | Evaluates LLM capabilities on Indic languages. | IndicGenBench evaluates broad cross-lingual NLP using parallel corpora. LINGUA-AUDIT evaluates civic entitlement guidance, administrative omission, and Hinglish code-switching. |
| **FActScore**<br>*(Min et al., EMNLP 2023)* | Decomposes text into atomic claims evaluated against Wikipedia. | Atomic factuality decomposition ($M_1$). | FActScore evaluates entity precision in English biographies. LINGUA-AUDIT extends this to statutory civic schemes, administrative omission ($M_3$), and citation authenticity ($M_5$). |

> **One-Sentence Research Gap:**  
> *“CitizenQuery established an automated evaluation framework for citizen queries against authoritative government portals in monolingual English; LINGUA-AUDIT contributes a civic-information benchmark design and statistical mixed-effects protocol specifically structured to audit substantive information disparities across English, Devanagari Hindi, and Romanized Hinglish code-switching in Indian statutory welfare administration.”*

---

## ⚖️ Scientific Integrity and Disclosures

To maintain strict scientific transparency, the operational status of LINGUA-AUDIT is explicitly disclosed:

1. **Framework Scope:** This repository presents a benchmark-design and reproducibility framework; it does **not** report an empirical comparison or ranking of commercial LLMs.
2. **Software Verification Fixtures:** The 5,400 records in the dataset are deterministic, programmatic baseline fixtures instantiated in-memory (latency 0 ms, 100% zero within-cell variance across repetitions) to verify schema adherence, data ingestion, and pipeline integrity—**not** live model API outputs.
3. **Pending Evaluator Validation:** While a 12-item blinded feasibility pilot package and a 270-response representative sample have been prepared, independent bilingual human annotators have not yet been scored. Consequently, all 13 response-quality metrics remain **empirically unvalidated**.
4. **Target Model Slots:** The four named models (`gemini-3.5-flash`, `gpt-4o`, `claude-3.5-sonnet`, `llama-3.1-70b`) represent architectural target slots in the execution protocol; no external commercial endpoints were queried.
5. **No Fitted Statistical Models:** Zero statistical models have been fitted to data; no odds ratios, variance components, or $p$-values are claimed.
6. **Internal Statutory Curation:** Ground truth facts represent internal curation by the project authors from published administrative guidelines and gazettes, without external legal-panel certification or clause-level mapping.
7. **Pending Institutional Ethics Review:** An institutional ethics protocol has been prepared (`docs/ethics/ethics_application.md`); formal institutional approval is pending review.

---

## 📂 Repository Architecture

```text
.
├── ai-info-inequality-exp/
│   ├── backend/
│   │   └── app/
│   │       └── scoring/
│   │           └── lingua_audit/          # Modular Python scoring engine (13 operational metrics)
│   ├── data/
│   │   └── benchmark/
│   │       ├── master_task_registry_150.json               # 150 curated tasks (450 CFs, 300 IFs, 150 UINs)
│   │       ├── raw_responses/                              # 5,400 synthetic software verification fixtures
│   │       │   └── stage12_4_dataset_integrity_manifest.json # Cryptographic SHA-256 registry
│   │       └── evaluator_validation/
│   │           ├── QUARANTINE_MANIFEST.json                # Quarantined invalid synthetic validation artifacts
│   │           └── stage12_5_2D_pilot_annotation_package.json # Blinded 12-item human feasibility pilot
│   ├── paper/
│   │   ├── final/                                          # Authoritative frozen deliverables
│   │   │   ├── LINGUA_AUDIT_final.docx                     # Final 14-page editable Word manuscript
│   │   │   ├── LINGUA_AUDIT_final.pdf                      # Final verification PDF
│   │   │   ├── PROJECT_SUMMARY.md                          # Master's portfolio dossier & CV description
│   │   │   ├── README.md                                   # Deliverable documentation
│   │   │   ├── references.bib                              # Complete BibTeX bibliography
│   │   │   └── build_final_word_preprint.py                # Automated OpenXML document generator
│   │   ├── word_preprint/                                  # Development Word draft and rendered page checks
│   │   ├── latex_preprint_v2/                              # Compilable LaTeX preprint sources
│   │   └── FINAL_CLAIMS_CHECKLIST.md                       # 21-claim forensic verification matrix
│   ├── tests/                                              # Pytest suite (115 passing tests)
│   └── docs/                                               # Audit reports, pre-registration, and ethics protocol
└── README.md                                               # Root repository overview (this file)
```

---

## ⚡ Quick Start & Verification

### Running the Test Suite (115 Tests)

To verify the scoring formulas, boundary edge-case handling, and software pipeline integrity:

```bash
cd ai-info-inequality-exp
# Using the project's virtual environment:
$env:PYTHONPATH="."
.\backend\venv\Scripts\pytest.exe .\tests
# ======================= 115 passed in 6.83s =======================
```

### Reproducing the Final Word Deliverable

To regenerate the authoritative 14-page Word document from source code:

```bash
cd ai-info-inequality-exp
.\backend\venv\Scripts\python.exe .\paper\final\build_final_word_preprint.py
# Successfully generated: paper/final/LINGUA_AUDIT_final.docx (14 pages)
```

---

## 📖 Citation

If you reference the LINGUA-AUDIT benchmark design, measurement specifications, or auditing protocol in your research, please cite:

```bibtex
@misc{deep2026linguaaudit,
  author       = {Tanya Deep},
  title        = {{LINGUA-AUDIT: Auditing Information Inequality in Multilingual AI Systems}},
  year         = {2026},
  month        = {October},
  note         = {Preprint manuscript, BMS Institute of Technology and Management, Bengaluru, India},
  howpublished = {Available at \url{https://github.com/Tani-2005/AI-mediated-information-inequality-across-languages}}
}
```

---

## 📄 License

This research framework and benchmark repository are intended for open scientific release under the **Creative Commons Attribution-NonCommercial 4.0 International License (CC-BY-NC 4.0)** upon final publication.
