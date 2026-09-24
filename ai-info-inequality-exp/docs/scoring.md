# Deterministic Scoring Engine Documentation

The primary outcome (**Decision Quality Score**, 0.0 - 10.0 scale) is evaluated 100% deterministically by `backend/app/scoring/engine.py` using JSON ground-truth rubrics stored in `data/ground_truth/`:
- **PMEGP**: Eligibility (2 pts), Max Project Cost Rs. 50L (2 pts), Special Category Rural Subsidy 35% (3 pts), Mandatory Documents (3 pts).
- **PM-Vishwakarma**: Eligibility (2 pts), Tranche 1 Loan Rs. 1,00,000 (2 pts), Training Stipend Rs. 500/day (3 pts), Toolkit Voucher Rs. 15,000 (3 pts).
- **PM-SVANidhi**: Eligibility (2 pts), 1st Tranche Loan Rs. 10,000 (2 pts), Interest Subsidy 7% (3 pts), Max Annual Cashback Rs. 1,200 (3 pts).

Zero LLM-as-a-judge is utilized. Answers are scored objectively.
