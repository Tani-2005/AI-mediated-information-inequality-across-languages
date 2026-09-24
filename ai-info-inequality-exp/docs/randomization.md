# Randomization Engine Documentation

The randomization engine (`backend/app/randomization/engine.py`) enforces server-side stratified block randomization:
- **Eligibility Check**: Verifies that participant has completed Consent, passed Screening, completed LEAP-Q, and submitted AILS prior to allocation.
- **Stratification**: Assigns participant to `LOW` AILS (<36) or `HIGH` AILS ($\ge 36$).
- **Permuted Block Allocation**: Uses randomized block sizes of 3 and 6 to allocate participants 1:1:1 across `ENGLISH_ONLY`, `HINDI_ONLY`, and `CODE_SWITCHING`.
- **Allocation Concealment**: Allocation is calculated strictly on the backend API. Zero block sequence information is exposed to the frontend client.
