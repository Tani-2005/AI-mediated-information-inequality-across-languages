# Table 2: Synthetic Fixture Diagnostic Characteristics Across Language Scaffolding

| Condition / Stratum | N | Char Length (Mean ± SD) | Char Length (Median [IQR]) | Word Count (Mean ± SD) | Word Count (Median [IQR]) | Recorded Latency |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Language: English** | 1,800 | 339.8 ± 45.33 | 340.0 [57] | 47.16 ± 6.08 | 47.0 [7] | 0 ms* |
| **Language: Hindi** | 1,800 | 326.8 ± 45.33 | 327.0 [57] | 46.16 ± 6.08 | 46.0 [7] | 0 ms* |
| **Language: Code-Switching**| 1,800 | 333.8 ± 45.33 | 334.0 [57] | 46.16 ± 6.08 | 46.0 [7] | 0 ms* |
| **Model Slot: Gemini 3.5 Flash** | 1,350 | 333.47 ± 45.64 | 337.0 [65] | 46.49 ± 6.1 | 46.0 [7] | 0 ms* |
| **Model Slot: GPT-4o** | 1,350 | 333.47 ± 45.64 | 337.0 [65] | 46.49 ± 6.1 | 46.0 [7] | 0 ms* |
| **Model Slot: Claude 3.5 Sonnet** | 1,350 | 333.47 ± 45.64 | 337.0 [65] | 46.49 ± 6.1 | 46.0 [7] | 0 ms* |
| **Model Slot: Llama 3.1 70B** | 1,350 | 333.47 ± 45.64 | 337.0 [65] | 46.49 ± 6.1 | 46.0 [7] | 0 ms* |
| **Fixture Total** | 5,400 | 333.47 ± 45.63 | 337.0 [65] | 46.49 ± 6.1 | 46.0 [7] | 0 ms* |

*\*Note on Synthetic Fixture Diagnostics:* Latency is recorded as 0 ms across all 5,400 records because the fixtures were programmatically generated via in-memory template synthesis. Within-cell word length variance across the 3 repetitions is exactly 0.0 across all 1,800 cells (100.0% zero-variance). These diagnostic statistics reflect software testing fixtures, NOT live model evaluations.
