# Table 1: Benchmark Execution Matrix & Synthetic Pipeline Fixture Verification

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
| **File SHA-256 (Raw)** | Cryptographic checksum of raw file bytes | — | `095b8caa9497b4d8cf804b29baad23b4d3de813bda9f865b7a1da3ef658ca5f3` | Verified |
| **Canonical JSON SHA-256** | Checksum of sorted canonical JSON serialization | — | `296bb1650f06cc7934f16e90ef662f9c9b0207971344b0935ee02704b8bf4248` | Verified |

> **Software Verification Notice:** The 5,400 records in `stage12_4_full_evaluation_responses.json` represent programmatic pipeline fixtures instantiated to verify end-to-end data flow and factorial matrix completeness, NOT genuine outputs from live frontier models.
