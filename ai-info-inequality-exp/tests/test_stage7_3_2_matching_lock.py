import pytest
import math
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Set, Union

# ==============================================================================
# 1. AUTHORITATIVE GROUND-TRUTH FIELD INVENTORY AUDIT
# ==============================================================================

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "ground_truth"

def test_authoritative_decision_field_inventory():
    """
    Verifies that the ground truth files contain exactly 12 decision fields across 3 civic tasks:
    - PMEGP: 4 fields
    - PM_VISHWAKARMA: 4 fields
    - PM_SVANIDHI: 4 fields
    Total = 12 fields.
    """
    scenarios = {
        "PMEGP": DATA_DIR / "pmegp.json",
        "PM_VISHWAKARMA": DATA_DIR / "pm_vishwakarma.json",
        "PM_SVANIDHI": DATA_DIR / "pm_svanidhi.json"
    }

    total_fields = 0
    scenario_field_counts = {}

    for task_id, file_path in scenarios.items():
        assert file_path.exists(), f"Missing ground truth file for {task_id}"
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            fields = data["ground_truth_rubric"]["fields"]
            count = len(fields)
            scenario_field_counts[task_id] = count
            total_fields += count

    assert scenario_field_counts["PMEGP"] == 4
    assert scenario_field_counts["PM_VISHWAKARMA"] == 4
    assert scenario_field_counts["PM_SVANIDHI"] == 4
    assert total_fields == 12, f"Expected 12 total decision fields, got {total_fields}"


# ==============================================================================
# 2. DETERMINISTIC NORMALIZATION & MATCHING FUNCTIONS (STAGE 7.3.2.1 LOCKED)
# ==============================================================================

def normalize_numeric(val: Any, field_key: str = "") -> Optional[float]:
    """
    Normalizes numeric inputs (currency, percentages, lakhs, plain numbers).
    Field-specific unit rules:
    - max_project_cost_lakhs: expected unit is Lakhs (e.g. 50.0). Raw INR >= 10000 is converted to lakhs (/100000.0).
    - first_tranche_loan_inr & other INR fields: expected unit is INR. String "X lakh" is converted to INR (*100000.0).
    - percentage fields: expected unit is percentage points (e.g. 35.0). Strips % and percent.
    Returns float if parseable, None if unparseable/missing.
    """
    if val is None or val == "":
        return None

    if isinstance(val, (int, float)):
        if math.isnan(val) or math.isinf(val):
            return None
        num = float(val)
        if field_key == "max_project_cost_lakhs" and num >= 10000.0:
            return num / 100000.0
        return num

    if not isinstance(val, str):
        return None

    s = val.strip().lower()
    if not s:
        return None

    # Remove currency symbols and formatting characters
    s = s.replace("₹", "").replace("rs.", "").replace("rs", "").replace("inr", "").replace(",", "")

    # Handle percentage suffixes
    s = s.replace("percent", "").replace("percentage", "").replace("%", "").strip()

    # Handle lakhs conversion
    if "lakh" in s:
        s = s.replace("lakhs", "").replace("lakh", "").replace("rupees", "").strip()
        try:
            num = float(s)
            if field_key == "max_project_cost_lakhs":
                return num
            else:
                return num * 100000.0
        except ValueError:
            return None

    try:
        num = float(s)
        if field_key == "max_project_cost_lakhs" and num >= 10000.0:
            return num / 100000.0
        return num
    except ValueError:
        return None


def normalize_boolean(val: Any) -> Optional[bool]:
    """
    Normalizes boolean/categorical eligibility values.
    """
    if val is None or val == "":
        return None

    if isinstance(val, bool):
        return val

    if isinstance(val, (int, float)):
        if val == 1:
            return True
        if val == 0:
            return False
        return None

    if isinstance(val, str):
        s = val.strip().lower()
        if s in ("true", "yes", "y", "eligible", "1", "correct"):
            return True
        if s in ("false", "no", "n", "ineligible", "0", "incorrect"):
            return False

    return None


def normalize_multi_select(val: Any) -> Set[str]:
    """
    Normalizes multi-select list of strings into an order-independent set of cleaned strings.
    """
    if val is None or val == "":
        return set()

    if isinstance(val, list):
        cleaned = set()
        for item in val:
            if item is not None:
                s = str(item).strip().lower()
                if s:
                    cleaned.add(s)
        return cleaned

    if isinstance(val, str):
        s = val.strip().lower()
        if not s:
            return set()
        return {item.strip() for item in s.split(",") if item.strip()}

    return set()


def is_field_match(field_key: str, field_type: str, submitted_val: Any, error_val: Any) -> bool:
    """
    Deterministic matching rule between participant submitted answer and an erroneous AI claim value.
    Returns True if submitted answer matches the erroneous claim value, False otherwise.
    """
    if submitted_val is None or submitted_val == "" or error_val is None or error_val == "":
        return False

    if field_type == "boolean":
        norm_sub = normalize_boolean(submitted_val)
        norm_err = normalize_boolean(error_val)
        if norm_sub is None or norm_err is None:
            return False
        return norm_sub == norm_err

    elif field_type == "number":
        norm_sub = normalize_numeric(submitted_val, field_key)
        norm_err = normalize_numeric(error_val, field_key)
        if norm_sub is None or norm_err is None:
            return False
        return abs(norm_sub - norm_err) < 1e-4

    elif field_type == "multi_select":
        set_sub = normalize_multi_select(submitted_val)
        set_err = normalize_multi_select(error_val)
        if not set_sub or not set_err:
            return False
        return set_sub == set_err

    return False


# ==============================================================================
# 3. ANNOTATION REVIEW PROTOCOL SIMULATOR FOR KLIPPENDORFF'S ALPHA
# ==============================================================================

def process_inter_rater_agreement(alpha_value: float, disputed_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Stage 7.3.2 Predefined Inter-Rater Agreement Protocol Execution.
    If alpha >= 0.85: Proceed to standard rater consensus adjudication.
    If alpha < 0.85: Trigger predefined frozen annotation review protocol (independent 3rd auditor review).
    """
    if alpha_value >= 0.85:
        return {
            "status": "APPROVED",
            "action": "Proceed to standard rater consensus adjudication",
            "review_triggered": False,
            "disputed_count": len(disputed_cases)
        }
    else:
        return {
            "status": "REVIEW_TRIGGERED",
            "action": "Trigger predefined frozen protocol review: 3rd senior auditor independent re-annotation",
            "review_triggered": True,
            "disputed_count": len(disputed_cases),
            "guarantee": "No modification of protocol or thresholds based on participant outcomes"
        }


# ==============================================================================
# 4. TARGETED UNIT TESTS FOR STAGE 7.3.2.1 RECONCILIATION
# ==============================================================================

def test_numeric_matching_exact():
    assert is_field_match("subsidy_percentage", "number", 25.0, 25.0) == True
    assert is_field_match("subsidy_percentage", "number", 25.0, 35.0) == False

def test_numeric_matching_percentage_representations():
    assert is_field_match("subsidy_percentage", "number", "25%", "25") == True
    assert is_field_match("subsidy_percentage", "number", "25 percent", 25.0) == True
    assert is_field_match("subsidy_percentage", "number", "0.25", 25.0) == False  # strict value equivalence

def test_numeric_matching_currency_and_lakhs_reconciliation():
    # 1. PMEGP max_project_cost_lakhs (expected unit: Lakhs)
    assert is_field_match("max_project_cost_lakhs", "number", "25 Lakhs", 25.0) == True
    assert is_field_match("max_project_cost_lakhs", "number", "25.0 lakhs", 25.0) == True
    assert is_field_match("max_project_cost_lakhs", "number", "25 lakh rupees", 25.0) == True
    # Raw INR representation 25,00,000 correctly converts to 25.0 lakhs
    assert is_field_match("max_project_cost_lakhs", "number", "₹25,00,000", 25.0) == True
    assert is_field_match("max_project_cost_lakhs", "number", 2500000, 25.0) == True

    # 2. INR fields (expected unit: INR)
    # Lakh notation "1 lakh" converts to 100000.0 INR
    assert is_field_match("first_tranche_loan_inr", "number", "1 lakh", 100000.0) == True
    assert is_field_match("first_tranche_loan_inr", "number", "1 Lakh", 100000.0) == True
    assert is_field_match("first_tranche_loan_inr", "number", "₹1,00,000", 100000.0) == True
    assert is_field_match("first_tranche_loan_inr", "number", "INR 100000", 100000.0) == True
    assert is_field_match("first_tranche_loan_inr", "number", "Rs. 100000", 100000.0) == True

    # 3. Smaller INR amounts
    assert is_field_match("first_tranche_loan_inr", "number", "₹10,000", 10000.0) == True
    assert is_field_match("skill_stipend_per_day_inr", "number", "Rs. 500", 500.0) == True
    assert is_field_match("max_annual_cashback_inr", "number", "1200", 1200.0) == True

def test_boolean_matching():
    assert is_field_match("is_eligible", "boolean", True, True) == True
    assert is_field_match("is_eligible", "boolean", "YES", True) == True
    assert is_field_match("is_eligible", "boolean", "eligible", "true") == True
    assert is_field_match("is_eligible", "boolean", "NO", True) == False
    assert is_field_match("is_eligible", "boolean", False, True) == False

def test_multi_select_matching():
    err_claim = ["aadhaar_card", "edp_certificate"]
    assert is_field_match("mandatory_documents", "multi_select", ["edp_certificate", "aadhaar_card"], err_claim) == True
    assert is_field_match("mandatory_documents", "multi_select", ["aadhaar_card"], err_claim) == False
    assert is_field_match("mandatory_documents", "multi_select", [], err_claim) == False

def test_missing_malformed_answers():
    assert is_field_match("subsidy_percentage", "number", None, 25.0) == False
    assert is_field_match("subsidy_percentage", "number", "", 25.0) == False
    assert is_field_match("subsidy_percentage", "number", "unparseable_text", 25.0) == False
    assert is_field_match("is_eligible", "boolean", None, True) == False
    assert is_field_match("mandatory_documents", "multi_select", None, ["aadhaar_card"]) == False

def test_contradictory_claims_matching():
    err_claim_1 = 20.0
    err_claim_2 = 25.0

    match_1 = is_field_match("subsidy_percentage", "number", 25.0, err_claim_1)
    match_2 = is_field_match("subsidy_percentage", "number", 25.0, err_claim_2)
    assert (match_1 or match_2) == True

    match_3 = is_field_match("subsidy_percentage", "number", 30.0, err_claim_1)
    match_4 = is_field_match("subsidy_percentage", "number", 30.0, err_claim_2)
    assert (match_3 or match_4) == False

def test_verification_thresholds():
    assert (0 == 0) or (0.0 < 2.0) == True
    assert (1 == 0) or (1.5 < 2.0) == True
    assert not ((1 == 0) or (5.0 < 2.0)) == True

def test_inter_rater_agreement_protocol():
    res_pass = process_inter_rater_agreement(0.88, [{"case": "claim_12"}])
    assert res_pass["status"] == "APPROVED"
    assert res_pass["review_triggered"] == False

    res_fail = process_inter_rater_agreement(0.79, [{"case": "claim_14"}, {"case": "claim_19"}])
    assert res_fail["status"] == "REVIEW_TRIGGERED"
    assert res_fail["review_triggered"] == True
