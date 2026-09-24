# Experiment Configuration Documentation

The frozen experimental parameters are specified in `experiment_config.json`:
- Study ID: `ENGLISH_HINDI_AI_INFO_INEQUALITY_2026`
- Protocol Version: `1.0.0-frozen`
- Analyzable Sample Target: $N = 144$ ($48$ per arm across 3 arms)
- Recruitment Allowance Target: $N = 171$
- Stratification: AI Literacy Scale (AILS) median split ($<36 \rightarrow$ LOW, $\ge 36 \rightarrow$ HIGH)
- Block Sizes: Permuted blocks of size 3 and 6
- Allocation Ratio: 1:1:1 (`ENGLISH_ONLY`, `HINDI_ONLY`, `CODE_SWITCHING`)
- Tasks: PMEGP, PM_VISHWAKARMA, PM_SVANIDHI
- Order Counterbalancing: $3 \times 3$ Latin Square
- Primary Outcome: Decision Quality Score ($0.0 - 10.0$)
- Planned Model: `DecisionQuality ~ Language + Scenario + Position + (1|Participant)`
- Production Model Snapshot Placeholder: `gpt-4o-2024-08-06` (Temp 0.2, Top_p 1.0, Max Tokens 1000, Timeout 15s)
