# LINGUA-AUDIT: Comprehensive Novelty Assessment and Prior-Work Review

**Reviewer / Typesetting Specialist:** Academic Editor & Literature Reviewer  
**Date of Assessment:** 15 October 2026  
**Subject:** Scientific Novelty, Literature Grounding, and Boundary Positioning of LINGUA-AUDIT  
**Target Repository Artifact:** `paper/latex_preprint_v2/`

---

## 1. Search Strategy and Scope

### Methodology
To ensure an evidence-grounded assessment of LINGUA-AUDIT's distinctiveness, a multi-source literature search was conducted across:
- **Major Venues & Indexes:** ACL Anthology (ACL, EMNLP, NAACL, EACL, Findings), arXiv (cs.CL, cs.AI, cs.CY), ACM Digital Library (FAccT, AIES), IEEE Xplore, NeurIPS Datasets & Benchmarks Track, and official industry/national research project releases.
- **Search Date:** 15 October 2026.
- **Query Families:**
  1. *Public-sector & citizen-facing AI:* `"citizen query"`, `"civic information"`, `"public administration"`, `"government schemes"`, `"e-governance benchmark"`.
  2. *Multilingual Indic QA & Generation:* `"Indic QA"`, `"IndicGenBench"`, `"IndQA"`, `"MILU"`, `"Bhashini evaluation"`, `"BharatGen"`.
  3. *Code-switching in LLM evaluations:* `"code-switching benchmark"`, `"Hinglish LLM evaluation"`, `"GLUECoS"`.
  4. *Factual accuracy & omission:* `"FActScore multilingual"`, `"omission disparity"`, `"statutory ground truth"`, `"information inequality across languages"`.

---

## 2. Comparative Analysis Matrix

Table 1 systematically evaluates LINGUA-AUDIT against the most closely related contemporary benchmarks and frameworks.

| Benchmark / Project | Authors & Venue (Year) | Geographic & Domain Scope | Languages & Modalities | Ground Truth & Source Authority | Metrics Evaluated | Empirical vs. Framework | Key Overlap & Critical Differentiation |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| **CitizenQuery-UK** | Majithia et al. (2026), arXiv:2602.04064 | United Kingdom public sector (welfare, tax, health, immigration) | English only (Monolingual) | Grounded in official `gov.uk` documentation (~22,000 synthetic pairs) | FActScore-adapted factuality, abstention frequency, verbosity, consistency | **Empirical study** (evaluated live frontier & open models) | **Overlap:** Evaluates high-stakes citizen queries against government guidelines.<br>**Differentiation:** Monolingual English only; does not evaluate cross-lingual information inequality, Indic languages, or code-switching. |
| **IndQA** | OpenAI (2025), OpenAI Research Release | India (Law, health, history, culture, regional affairs) | 12 Indian languages + Hinglish + English | Domain-expert curated questions with reference answers | Accuracy, cultural fluency, regional reasoning | **Empirical benchmark** | **Overlap:** Evaluates Indian regional contexts and Hinglish.<br>**Differentiation:** Focuses on cultural fluency, proverbs, and broad cultural reasoning rather than statutory public administration compliance or administrative omission penalties. |
| **IndicGenBench** | Singh et al. (2024), Findings of ACL 2024 | General NLP (Generation, translation, summarization, QA) | 29 Indic languages | Standard NLP reference corpora (Wikipedia, news, translated datasets) | BLEU, ChrF, ROUGE, Exact Match, BERTScore | **Empirical benchmark** | **Overlap:** Comprehensive evaluation of Indic generation.<br>**Differentiation:** Evaluates classical NLP task capabilities; does not evaluate administrative service delivery, statutory truth, or factual omission. |
| **INDIC QA BENCHMARK** | Singh et al. (2024), Findings of EMNLP 2024 | General knowledge / reading comprehension | 11 Indian languages | Context-grounded Wikipedia passages and synthetic QA pairs | Contextual F1, Exact Match, Translate-Test consistency | **Empirical benchmark** | **Overlap:** Evaluates question answering across major Indian languages.<br>**Differentiation:** Context-grounded reading comprehension (CQA) with provided passages, not open-ended retrieval of statutory rules or civic procedural instructions. |
| **GLUECoS** | Khanuja et al. (2020), ACL 2020 | General NLP | English-Hindi and English-Spanish code-switching | Curated Twitter/social text corpora | Task-specific accuracy, F1 across 6 classification/QA tasks | **Empirical benchmark** | **Overlap:** Pioneered systematic code-switching benchmarking in Hinglish.<br>**Differentiation:** Evaluates sentence-level classification/NLI; does not audit generative LLM factual completeness or civic information delivery. |
| **MILU** | Doddapaneni et al. (2024), IndiaAI / IIT Madras | Multitask knowledge (Social sciences, policy, regional domains) | 11 Indic languages | Multiple-choice questions adapted from Indian curricula | Accuracy (0/1 multiple-choice selection) | **Empirical benchmark** | **Overlap:** Evaluates Indian policy and knowledge domains in Indic scripts.<br>**Differentiation:** Multiple-choice examination paradigm; cannot measure long-form procedural omissions, hallucinated URLs, or safety warnings. |
| **LINGUA-AUDIT** *(This Work)* | Deep (2026), Preprint | **India (5 Civic Domains: Healthcare, Education, Public Services, Finance, General Knowledge)** | **Matched Triad: English, Standard Hindi, Romanized Hinglish** | **150 tasks anchored to official central/state statutory guidelines, 450 Critical Facts, 300 Important Facts** | **13 operational metrics: precision ($M_1$), coverage ($M_{2a}$), omission ($M_3$), deduplicated error ($M_{4a}$), citation authenticity ($M_5$), safety ($M_6$), UIN preservation ($M_7$), stability ($M_8$)** | **Reproducibility framework & benchmark design** (prespecified analysis plan, 5,400 software fixtures, empirical models unexecuted) | **Distinctive Focus:** Systematically operationalizes *substantive information inequality* by anchoring evaluation to language-agnostic Underlying Information Needs (UINs) rather than English comparator texts, combined with a prespecified GLMM statistical analysis plan. |

---

## 3. Evaluation of Candidate Novelty Claims

| Candidate Claim | Classification | Justification & Literature Grounding |
| :--- | :---: | :--- |
| **1. Benchmark of Indian civic-information tasks grounded in official administrative sources** | **Related prior work exists, but precise combination is distinctive** | CitizenQuery (Majithia et al., 2026) demonstrated citizen-query evaluation on UK government guidelines, and MILU / IndQA touch upon Indian policy/legal domains. However, an open, task-anchored benchmark focusing specifically on Indian administrative welfare schemes across 5 core societal domains is a valuable, localized contribution. |
| **2. Matched English, Devanagari Hindi, and Romanized Hindi-English code-switching conditions** | **Related prior work exists, but precise combination is distinctive** | GLUECoS (Khanuja et al., 2020) and IndQA (2025) included Hinglish. LINGUA-AUDIT's distinctiveness lies in using **matched parallel triads** anchored to the exact same statutory Underlying Information Need (UIN), directly testing whether the choice of linguistic framing penalizes citizen advisory content. |
| **3. Language-agnostic Underlying Information Needs (UINs) to compare substantive information** | **Potentially distinctive design contribution** | Most multilingual QA benchmarks (TyDi QA, Indic-QA) evaluate surface text match or translation consistency. Anchoring evaluation to conceptual, language-agnostic UINs to bypass English-normative bias is a sound and distinctive methodological proposal in civic evaluation. |
| **4. Multi-dimensional measurement of critical-fact coverage, omission, error deduplication, citations, and safety** | **Related prior work exists, but metric suite is uniquely tailored** | Individual metrics exist: FActScore (Min et al., 2023) measures precision; CitizenQuery (2026) measures abstention and factuality; HELM (Liang et al., 2023) measures safety. LINGUA-AUDIT formalizes an integrated 13-metric suite explicitly penalizing statutory omission ($M_3$) and deduplicating error counts ($M_{4a}$), which is critical for administrative integrity. |
| **5. Prespecified statistical analysis plan with family-wise error control (GLMMs + Holm-Bonferroni)** | **Clearly distinctive in AI benchmarking** | Almost all NLP benchmarks report raw descriptive means and sample-level rankings. Prespecifying a formal GLMM/CLMM framework with a pre-registered confirmatory family of 9 pooled hypotheses under Holm-Bonferroni correction imports rigorous epidemiological/biostatistical standards into AI auditing. |
| **6. Software pipeline with explicit separation between implementation verification and empirical validation** | **Methodological governance contribution** | The explicit disclosure of deterministic fixtures, quarantine of invalid cloned evaluator scripts, and refusal to claim empirical validation prior to certified human annotation serves as a cautionary methodological benchmark. |

---

## 4. Recommended Bounded Novelty Statement for LINGUA-AUDIT

The following formulation accurately bounds the contribution without overclaiming:

> *"LINGUA-AUDIT contributes a civic-information benchmark design, an operational measurement suite, and an open reproducibility framework tailored to evaluate substantive information inequality across languages. While recent efforts have explored citizen queries in monolingual English (e.g., CitizenQuery; Majithia et al., 2026) or evaluated broad cultural fluency across Indic languages (e.g., IndQA, IndicGenBench, Indic-QA), LINGUA-AUDIT specifically targets administrative welfare and civic navigation in India across a matched triad of English, standard Hindi, and Romanized code-switching (Hinglish). Its core methodological contribution lies in anchoring evaluations to language-agnostic Underlying Information Needs (UINs) rather than English comparator texts, formalizing 13 multidimensional response-quality metrics that penalize mandatory statutory omissions, and formulating a prespecified statistical analysis plan with family-wise error control. The framework establishes the computational and measurement foundation necessary to audit whether language models introduce disparities in civic guidance once human-calibrated evaluations are completed."*

---

## 5. Unsupported Claims to Avoid or Remove

1. **Do NOT claim to be the "first" or "only" civic benchmark:** CitizenQuery-UK (Majithia et al., Feb 2026) established citizen-query auditing for UK public services.
2. **Do NOT claim to be the "first" to evaluate Hinglish LLM capabilities:** GLUECoS (2020) and IndQA (2025) previously incorporated Hindi-English code-switching.
3. **Do NOT claim to have "demonstrated" or "proven" information inequality:** No live model API endpoints were queried, and the 5,400 records are software pipeline fixtures.
4. **Do NOT claim to provide an "independently certified statutory benchmark":** The ground-truth registry reflects internal author curation from published schemes, without verbatim statutory clause mapping or multi-expert legal panel certification.
5. **Do NOT claim that metric unit tests establish construct validity:** Passing unit tests verify software execution, not human alignment or measurement validity.

---

## 6. Limitations of the Search

- Literature in generative AI evaluation is expanding rapidly; preprints deposited after October 2026 or under non-indexed institutional repositories may not be captured.
- Certain proprietary benchmark initiatives from industrial labs (e.g., internal telecommunications or state portal chatbots) remain private and cannot be independently audited.
