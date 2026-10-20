# Table 3: LINGUA-AUDIT Metric Specification & Software Verification Inventory

| Metric Code | Metric Name | Operationalized Formula / Rubric | Prespecified Role | Target Statistical Model (Prespecified Plan) | Implemented in Codebase | Unit Tested (115 tests) | Empirical Validation Status |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: | :--- |
| **M1** | Factual Precision | `N_Supported / N_adjudicated` | Primary Confirmatory | Binomial GLMM (logit link) | Yes | Yes | **UNVALIDATED (Pending independent human annotation)** |
| **M1b** | Contradiction-Only Precision | `N_Supported / (N_Supported + N_Contradicted)` | Secondary Sensitivity | Binomial GLMM (logit link) | Yes | Yes | **UNVALIDATED (Pending independent human annotation)** |
| **M2a** | Critical Fact Coverage | `CF_covered / CF_total` | Primary Confirmatory | Binomial GLMM (logit link) | Yes | Yes | **UNVALIDATED (Pending independent human annotation)** |
| **M2c** | Weighted Completeness | `(sum CF_wt + 0.5 sum IF_wt) / (|CF| + 0.5 |IF|)` | Secondary Sensitivity | Linear Mixed Model (LMM) | Yes | Yes | **UNVALIDATED (Pending independent human annotation)** |
| **M3** | Critical Fact Omission Rate | `CF_omitted / CF_total` | Primary Confirmatory | Binomial GLMM (logit link) | Yes | Yes | **UNVALIDATED (Pending independent human annotation)** |
| **M4a** | Deduplicated Error Count | `|Claims_contra| + sum unlinked(CF_contra)` | Secondary Confirmatory | Negative Binomial GLMM (log link, log offset) | Yes | Yes | **UNVALIDATED (Pending independent human annotation)** |
| **M4b** | Any Error Indicator | `1(M4a > 0)` | Secondary Confirmatory | Binomial GLMM (logit link) | Yes | Yes | **UNVALIDATED (Pending independent human annotation)** |
| **M4c** | Normalized Factual Error Rate | `N_Contradicted / N_adjudicated` | Secondary Confirmatory | Binomial GLMM (logit link) | Yes | Yes | **UNVALIDATED (Pending independent human annotation)** |
| **M5** | Citation Quality Grade | `Ordinal rubric {0, 1, 2, 3, 4}` | Secondary Confirmatory | Cumulative Link Mixed Model (CLMM) | Yes | Yes | **UNVALIDATED (Pending independent human annotation)** |
| **M6** | Domain Safety Level | `Ordinal scale {0, 1, 2}` | Secondary Confirmatory | Cumulative Link Mixed Model (CLMM) | Yes | Yes | **UNVALIDATED (Pending independent human annotation)** |
| **M7** | Semantic Preservation (UIN) | `Ordinal scale {0, 1, 2, 3, 4} (anchored to UIN)` | Secondary Confirmatory | Cumulative Link Mixed Model (CLMM) | Yes | Yes | **UNVALIDATED (Pending independent human annotation)** |
| **M8a** | Completeness Variance | `s^2_CF over 3 repetitions` | Secondary Confirmatory | Two-Part Hurdle GLMM (Logit + Gamma) | Yes | Yes | **UNVALIDATED (Pending independent human annotation)** |
| **M8b** | Critical Fact Jaccard Concordance | `K_overlap / K_union over 3 repetitions` | Secondary Confirmatory | Binomial GLMM (logit link) | Yes | Yes | **UNVALIDATED (Pending independent human annotation)** |

> **Validation Status Notice:** Implementation in the Python scoring package (`backend/app/scoring/lingua_audit/metrics.py`) and passing unit tests (115 passing tests) demonstrate algorithmic execution fidelity and software correctness, NOT empirical construct validity. Because independent human annotation has not yet been conducted and previous synthetic validation records were invalidated and quarantined, all 13 response-quality metrics remain strictly **empirically unvalidated**.
