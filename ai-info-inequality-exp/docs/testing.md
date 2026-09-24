# Automated Test Suite Documentation

The backend test suite is executed using Pytest:
```bash
cd backend
.\venv\Scripts\pytest ..\tests
```

## Test Coverage
1. `test_randomization.py`: Tests AILS stratum cutoffs, prerequisite eligibility checks, permuted block allocations (sizes 3 & 6), and 1:1:1 arm balance.
2. `test_screening.py`: Tests criterion-referenced screening pass/fail thresholds ($\ge 2/3$ on both English & Hindi).
3. `test_scoring.py`: Tests deterministic 0-10 scoring engine for full credit, partial credit, and missing fields across all 3 scenarios.
4. `test_session_flow.py`: Tests state transitions, preventing randomization prior to screening and preventing double decision submissions.
5. `test_telemetry.py`: Tests telemetry event schema generation and exploratory tab focus logging.
6. `test_security.py`: Tests ground-truth answer key isolation from public API scenario payloads.
