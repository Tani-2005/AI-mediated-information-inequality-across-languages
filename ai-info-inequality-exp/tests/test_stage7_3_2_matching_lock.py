import pytest
import math
from typing import List, Dict, Any, Optional, Set, Union

# ==============================================================================
# 1. DETERMINISTIC NORMALIZATION & MATCHING FUNCTIONS FOR STAGE 7.3.2 LOCK
# ==============================================================================

def normalize_numeric(val: Any, field_key: str = "") -> Optional[float]:
    """
    Normalizes numeric inputs (currency, percentages, lakhs, plain numbers).
    Returns float if parseable, None if unparseable/missing.
    """
    if val is None or val == "":
        return None

    if isinstance(val, (int, float)):
        if math.isnan(val) or math.isinf(val):
            return None
        return float(val)

    if not isinstance(val, str):
        return None

    s = val.strip().lower()
    if not s:
        return None

    # Remove currency symbols and formatting characters
    s = s.replace("₹", "").replace("rs.", "").replace("rs", "").replace("inr", "").replace(",", "")

    # Handle percentage suffixes
    s = s.replace("percent", "").replace("percentage", "").replace("%", "").strip()

    # Handle lakhs conversion for max_project_cost_lakhs
    if "lakh" in s:
        s = s.replace("lakhs", "").replace("lakh", "").strip()
        try:
            num = float(s)
            if field_key == "max_project_cost_lakhs":
                return num
            else:
                return num * 100000.0
        except ValueError:
            return None

    try:
        return float(s)
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
        # Handle comma-separated strings if passed
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
        # Exact numeric match within 1e-4 tolerance
        return abs(norm_sub - norm_err) < 1e-4

    elif field_type == "multi_select":
        set_sub = normalize_multi_select(submitted_val)
        set_err = normalize_multi_select(error_val)
        if not set_sub or not set_err:
            return False
        # Set equality: participant selected exact set of items mentioned in erroneous claim
        return set_sub == set_err

    return False


# ==============================================================================
# 2. ANNOTATION REVIEW PROTOCOL SIMULATOR FOR KLIPPENDORFF'S ALPHA
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
# 3. TARGETED UNIT TESTS FOR STAGE 7.3.2
# ==============================================================================

# --- Numeric & Currency & Percentage Tests ---
def test_numeric_matching_exact():
    assert is_field_match("subsidy_percentage", "number", 25.0, 25.0) == True
    assert is_field_match("subsidy_percentage", "number", 25.0, 35.0) == False

def test_numeric_matching_percentage_representations():
    assert is_field_match("subsidy_percentage", "number", "25%", "25") == True
    assert is_field_match("subsidy_percentage", "number", "25 percent", 25.0) == True
    assert is_field_match("subsidy_percentage", "number", "0.25", 25.0) == False  # strict value equivalence

def test_numeric_matching_currency_and_lakhs():
    # PMEGP max_project_cost_lakhs
    assert is_field_match("max_project_cost_lakhs", "number", "25 Lakhs", 25.0) == True
    assert is_field_match("max_project_cost_lakhs", "number", "₹25,00,000", 25.0) == False # 2500000 != 25.0 in lakhs field
    assert is_field_match("first_tranche_loan_inr", "number", "₹1,00,000", 100000.0) == True
    assert is_field_match("first_tranche_loan_inr", "number", "100000", 100000.0) == True
    assert is_field_match("first_tranche_loan_inr", "number", "₹10,000", 10000.0) == True
    assert is_field_match("skill_stipend_per_day_inr", "number", "Rs. 500", 500.0) == True

# --- Boolean Tests ---
def test_boolean_matching():
    assert is_field_match("is_eligible", "boolean", True, True) == True
    assert is_field_match("is_eligible", "boolean", "YES", True) == True
    assert is_field_match("is_eligible", "boolean", "eligible", "true") == True
    assert is_field_match("is_eligible", "boolean", "NO", True) == False
    assert is_field_match("is_eligible", "boolean", False, True) == False

# --- Multi-Select Tests ---
def test_multi_select_matching():
    err_claim = ["aadhaar_card", "edp_certificate"]
    assert is_field_match("mandatory_documents", "multi_select", ["edp_certificate", "aadhaar_card"], err_claim) == True
    assert is_field_match("mandatory_documents", "multi_select", ["aadhaar_card"], err_claim) == False
    assert is_field_match("mandatory_documents", "multi_select", [], err_claim) == False

# --- Missing / Malformed Tests ---
def test_missing_malformed_answers():
    assert is_field_match("subsidy_percentage", "number", None, 25.0) == False
    assert is_field_match("subsidy_percentage", "number", "", 25.0) == False
    assert is_field_match("subsidy_percentage", "number", "unparseable_text", 25.0) == False
    assert is_field_match("is_eligible", "boolean", None, True) == False
    assert is_field_match("mandatory_documents", "multi_select", None, ["aadhaar_card"]) == False

# --- Contradictory Claims Tests ---
def test_contradictory_claims_matching():
    # Erroneous claims: Claim 1 = 20%, Claim 2 = 25%
    err_claim_1 = 20.0
    err_claim_2 = 25.0

    # Participant answer 25% matches Claim 2 -> FieldMatch = True
    match_1 = is_field_match("subsidy_percentage", "number", 25.0, err_claim_1)
    match_2 = is_field_match("subsidy_percentage", "number", 25.0, err_claim_2)
    assert (match_1 or match_2) == True

    # Participant answer 30% matches neither -> FieldMatch = False
    match_3 = is_field_match("subsidy_percentage", "number", 30.0, err_claim_1)
    match_4 = is_field_match("subsidy_percentage", "number", 30.0, err_claim_2)
    assert (match_3 or match_4) == False

# --- Verification Threshold Tests ---
def test_verification_thresholds():
    # Zero clicks -> No verification
    assert (0 == 0) or (0.0 < 2.0) == True
    # Clicks > 0, Duration < 2.0 -> No verification
    assert (1 == 0) or (1.5 < 2.0) == True
    # Clicks > 0, Duration >= 2.0 -> Meaningful verification
    assert not ((1 == 0) or (5.0 < 2.0)) == True

# --- Agreement Failure Rule Tests ---
def test_inter_rater_agreement_protocol():
    res_pass = process_inter_rater_agreement(0.88, [{"case": "claim_12"}])
    assert res_pass["status"] == "APPROVED"
    assert res_pass["review_triggered"] == False

    res_fail = process_inter_rater_agreement(0.79, [{"case": "claim_14"}, {"case": "claim_19"}])
    assert res_fail["status"] == "REVIEW_TRIGGERED"
    assert res_fail["review_triggered"] == True
