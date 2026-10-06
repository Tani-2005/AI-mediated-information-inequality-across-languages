import hashlib
import pytest
from typing import List, Dict, Any, Optional

# ==============================================================================
# 1. CANONICAL DOC DURATION ALGORITHM
# ==============================================================================
def derive_task_doc_duration(events: List[Dict[str, Any]]) -> float:
    """
    Canonical DocDuration Algorithm (Stage 7.3.1 Locked Specification).
    Computes total active viewing time (seconds) for official documents.
    Explicitly handles disconnects by falling back to the last recorded telemetry
    event timestamp (t_last) if no formal submission event is present.
    """
    if not events:
        return 0.0

    # Sort events by timestamp ASC
    sorted_events = sorted(events, key=lambda x: x["timestamp"])

    doc_events = [e for e in sorted_events if e["event_type"] in ("DOCUMENT_OPENED", "LINK_CLICKED")]
    if not doc_events:
        return 0.0

    total_active_seconds = 0.0
    current_start = None
    is_focused = True
    last_blur_time = None
    offscreen_time = 0.0

    terminal_event_types = {"FINAL_DECISION_SUBMITTED", "TASK_COMPLETED"}

    for idx, e in enumerate(sorted_events):
        etype = e["event_type"]
        ts = e["timestamp"]

        if etype in ("DOCUMENT_OPENED", "LINK_CLICKED"):
            if current_start is not None:
                # Close preceding interval
                raw_dur = ts - current_start
                active_dur = max(0.0, min(600.0, raw_dur - offscreen_time))
                total_active_seconds += active_dur

            current_start = ts
            offscreen_time = 0.0
            is_focused = True
            last_blur_time = None

        elif etype == "TAB_FOCUS_CHANGED":
            if current_start is not None:
                focused = e.get("event_data", {}).get("focused", True)
                if not focused and is_focused:
                    is_focused = False
                    last_blur_time = ts
                elif focused and not is_focused:
                    is_focused = True
                    if last_blur_time is not None:
                        offscreen_time += (ts - last_blur_time)
                        last_blur_time = None

        elif etype in terminal_event_types:
            if current_start is not None:
                raw_dur = ts - current_start
                active_dur = max(0.0, min(600.0, raw_dur - offscreen_time))
                total_active_seconds += active_dur
                current_start = None

    # DISCONNECT / UNEXPECTED TERMINATION FALLBACK:
    # If session ended without a formal terminal event, close open interval at t_last
    if current_start is not None:
        t_last = sorted_events[-1]["timestamp"]
        raw_dur = t_last - current_start
        if not is_focused and last_blur_time is not None:
            offscreen_time += (t_last - last_blur_time)
        active_dur = max(0.0, min(600.0, raw_dur - offscreen_time))
        total_active_seconds += active_dur

    return round(max(0.0, total_active_seconds), 2)


# ==============================================================================
# 2. CLAIM-LEVEL AUTOMATION BIAS DERIVATION ENGINE
# ==============================================================================
class ClaimAnnotation:
    def __init__(self, message_id: str, claim_id: str, decision_field: str,
                 claim_text: str, label: str, error_value: Any = None):
        self.message_id = message_id
        self.claim_id = claim_id
        self.decision_field = decision_field
        self.claim_text = claim_text
        self.label = label  # CORRECT, ERROR, AMBIGUOUS, NOT_RELEVANT
        self.error_value = error_value

def evaluate_automation_bias(
    annotations: List[ClaimAnnotation],
    submitted_answers: Dict[str, Any],
    doc_clicks: int,
    doc_duration: float
) -> Dict[str, Any]:
    """
    Claim-Level AutomationBias Derivation Engine (Stage 7.3.1 Locked Specification).
    Evaluates field-level matching and aggregates to task-level indicator.
    """
    no_verification = (doc_clicks == 0) or (doc_duration < 2.0)
    
    field_matches = {}
    field_auto_bias = {}

    # Group annotations by decision field
    field_claims: Dict[str, List[ClaimAnnotation]] = {}
    for ann in annotations:
        if ann.label == "NOT_RELEVANT":
            continue
        field_claims.setdefault(ann.decision_field, []).append(ann)

    for field, claims in field_claims.items():
        submitted_val = submitted_answers.get(field)

        # Check if submitted value is blank / missing
        if submitted_val is None or submitted_val == "":
            field_matches[field] = False
            field_auto_bias[field] = 0
            continue

        # Filter claims labeled ERROR (AMBIGUOUS is treated as AI_Factual_Error = 0)
        error_claims = [c for c in claims if c.label == "ERROR"]

        if not error_claims:
            field_matches[field] = False
            field_auto_bias[field] = 0
            continue

        # Deterministic match: Submitted value equals ANY error_value for that field
        matched_any_error = False
        for err_c in error_claims:
            if submitted_val == err_c.error_value:
                matched_any_error = True
                break
            # Handle float comparison tolerance for numeric fields
            elif isinstance(submitted_val, (int, float)) and isinstance(err_c.error_value, (int, float)):
                if abs(float(submitted_val) - float(err_c.error_value)) < 1e-4:
                    matched_any_error = True
                    break

        field_matches[field] = matched_any_error
        field_auto_bias[field] = 1 if (matched_any_error and no_verification) else 0

    task_automation_bias = 1 if any(b == 1 for b in field_auto_bias.values()) else 0

    return {
        "no_verification": no_verification,
        "field_matches": field_matches,
        "field_auto_bias": field_auto_bias,
        "task_automation_bias": task_automation_bias
    }


# ==============================================================================
# 3. UNIT TESTS FOR ISSUE 4.1: MD5 PARTICIPANT ORDERING
# ==============================================================================
def test_md5_ordering_determinism():
    p_id = "p_test_uuid_999"
    order1 = (int(hashlib.md5(p_id.encode("utf-8")).hexdigest(), 16) % 3) + 1
    order2 = (int(hashlib.md5(p_id.encode("utf-8")).hexdigest(), 16) % 3) + 1
    assert order1 == order2
    assert order1 in (1, 2, 3)

def test_md5_ordering_range_distribution():
    sample_ids = [f"p_uuid_{i:04d}" for i in range(100)]
    orders = [(int(hashlib.md5(pid.encode("utf-8")).hexdigest(), 16) % 3) + 1 for pid in sample_ids]
    assert set(orders) == {1, 2, 3}


# ==============================================================================
# 4. UNIT TESTS FOR ISSUE 4.2: CANONICAL DOC DURATION (CASES 1-8)
# ==============================================================================
def test_doc_duration_case1_immediate_submit():
    # Case 1: One document, immediate submit 15 seconds later
    events = [
        {"event_type": "DOCUMENT_OPENED", "timestamp": 10.0},
        {"event_type": "FINAL_DECISION_SUBMITTED", "timestamp": 25.0}
    ]
    assert derive_task_doc_duration(events) == 15.0

def test_doc_duration_case2_blur_focus():
    # Case 2: One doc, blur for 10s, focus for 10s, submit
    events = [
        {"event_type": "DOCUMENT_OPENED", "timestamp": 0.0},
        {"event_type": "TAB_FOCUS_CHANGED", "timestamp": 10.0, "event_data": {"focused": False}},
        {"event_type": "TAB_FOCUS_CHANGED", "timestamp": 20.0, "event_data": {"focused": True}},
        {"event_type": "FINAL_DECISION_SUBMITTED", "timestamp": 30.0}
    ]
    # Total raw = 30s, offscreen = 10s -> Active = 20s
    assert derive_task_doc_duration(events) == 20.0

def test_doc_duration_case3_multiple_blur_cycles():
    # Case 3: Multiple focus/blur cycles
    events = [
        {"event_type": "DOCUMENT_OPENED", "timestamp": 0.0},
        {"event_type": "TAB_FOCUS_CHANGED", "timestamp": 5.0, "event_data": {"focused": False}},
        {"event_type": "TAB_FOCUS_CHANGED", "timestamp": 15.0, "event_data": {"focused": True}}, # 10s off
        {"event_type": "TAB_FOCUS_CHANGED", "timestamp": 25.0, "event_data": {"focused": False}},
        {"event_type": "TAB_FOCUS_CHANGED", "timestamp": 35.0, "event_data": {"focused": True}}, # 10s off
        {"event_type": "FINAL_DECISION_SUBMITTED", "timestamp": 50.0}
    ]
    # Total raw = 50s, offscreen = 20s -> Active = 30s
    assert derive_task_doc_duration(events) == 30.0

def test_doc_duration_case4_multiple_documents():
    # Case 4: Doc 1 opened (20s), Doc 2 opened (30s), submit
    events = [
        {"event_type": "DOCUMENT_OPENED", "timestamp": 0.0},
        {"event_type": "DOCUMENT_OPENED", "timestamp": 20.0},
        {"event_type": "FINAL_DECISION_SUBMITTED", "timestamp": 50.0}
    ]
    # Doc 1 = 20s, Doc 2 = 30s -> Total = 50s
    assert derive_task_doc_duration(events) == 50.0

def test_doc_duration_case5_no_document_opened():
    # Case 5: No document opened
    events = [
        {"event_type": "PROMPT_SUBMITTED", "timestamp": 0.0},
        {"event_type": "FINAL_DECISION_SUBMITTED", "timestamp": 100.0}
    ]
    assert derive_task_doc_duration(events) == 0.0

def test_doc_duration_case6_negative_malformed_interval():
    # Case 6: Negative/malformed intervals (clamped to 0.0)
    events = [
        {"event_type": "DOCUMENT_OPENED", "timestamp": 20.0},
        {"event_type": "FINAL_DECISION_SUBMITTED", "timestamp": 15.0} # Skewed ts
    ]
    assert derive_task_doc_duration(events) == 0.0

def test_doc_duration_case7_exceeding_600_seconds_cap():
    # Case 7: Single interval exceeding 600s cap (700s -> clamped to 600s)
    events = [
        {"event_type": "DOCUMENT_OPENED", "timestamp": 0.0},
        {"event_type": "FINAL_DECISION_SUBMITTED", "timestamp": 700.0}
    ]
    assert derive_task_doc_duration(events) == 600.0

def test_doc_duration_case8_disconnect_fallback():
    # Case 8: Disconnect (no submission event). Closed at last recorded event timestamp
    events = [
        {"event_type": "DOCUMENT_OPENED", "timestamp": 10.0},
        {"event_type": "PROMPT_SUBMITTED", "timestamp": 40.0} # Last event before disconnect
    ]
    # Open interval closed at t_last (40.0s) -> Active = 30.0s
    assert derive_task_doc_duration(events) == 30.0


# ==============================================================================
# 5. UNIT TESTS FOR ISSUE 4.3: AUTOMATION BIAS CASES (A THROUGH H)
# ==============================================================================
def test_automation_bias_case_a_correct_ai_claim():
    # Case A: Correct AI claim + participant matches -> AutomationBias = 0
    anns = [ClaimAnnotation("m1", "c1", "subsidy_percentage", "Subsidy is 35%", "CORRECT", 35.0)]
    res = evaluate_automation_bias(anns, {"subsidy_percentage": 35.0}, doc_clicks=0, doc_duration=0.0)
    assert res["task_automation_bias"] == 0

def test_automation_bias_case_b_incorrect_ai_claim_no_verification():
    # Case B: Incorrect AI claim + participant matches + no verification -> AutomationBias = 1
    anns = [ClaimAnnotation("m1", "c1", "subsidy_percentage", "Subsidy is 25%", "ERROR", 25.0)]
    res = evaluate_automation_bias(anns, {"subsidy_percentage": 25.0}, doc_clicks=0, doc_duration=0.0)
    assert res["task_automation_bias"] == 1

def test_automation_bias_case_c_incorrect_ai_claim_with_verification():
    # Case C: Incorrect AI claim + participant matches + meaningful verification -> AutomationBias = 0
    anns = [ClaimAnnotation("m1", "c1", "subsidy_percentage", "Subsidy is 25%", "ERROR", 25.0)]
    res = evaluate_automation_bias(anns, {"subsidy_percentage": 25.0}, doc_clicks=2, doc_duration=45.0)
    assert res["no_verification"] == False
    assert res["task_automation_bias"] == 0

def test_automation_bias_case_d_incorrect_ai_claim_no_match():
    # Case D: Incorrect AI claim + participant does not match -> AutomationBias = 0
    anns = [ClaimAnnotation("m1", "c1", "subsidy_percentage", "Subsidy is 25%", "ERROR", 25.0)]
    res = evaluate_automation_bias(anns, {"subsidy_percentage": 35.0}, doc_clicks=0, doc_duration=0.0)
    assert res["field_matches"]["subsidy_percentage"] == False
    assert res["task_automation_bias"] == 0

def test_automation_bias_case_e_ambiguous_ai_claim():
    # Case E: Ambiguous AI claim -> AI_Factual_Error = 0 -> AutomationBias = 0
    anns = [ClaimAnnotation("m1", "c1", "subsidy_percentage", "Subsidy may vary between 20% and 40%", "AMBIGUOUS", None)]
    res = evaluate_automation_bias(anns, {"subsidy_percentage": 25.0}, doc_clicks=0, doc_duration=0.0)
    assert res["task_automation_bias"] == 0

def test_automation_bias_case_f_two_independent_field_errors():
    # Case F: Two independent erroneous claims affecting two fields
    anns = [
        ClaimAnnotation("m1", "c1", "max_project_cost_lakhs", "Max cost is 25 Lakhs", "ERROR", 25.0),
        ClaimAnnotation("m1", "c2", "subsidy_percentage", "Subsidy is 20%", "ERROR", 20.0)
    ]
    # Participant matches field 1
    res = evaluate_automation_bias(anns, {"max_project_cost_lakhs": 25.0, "subsidy_percentage": 35.0}, doc_clicks=0, doc_duration=0.0)
    assert res["field_auto_bias"]["max_project_cost_lakhs"] == 1
    assert res["field_auto_bias"]["subsidy_percentage"] == 0
    assert res["task_automation_bias"] == 1

def test_automation_bias_case_g_contradictory_claims_same_field():
    # Case G: Two contradictory claims affecting same field (e.g. 20% vs 25%)
    anns = [
        ClaimAnnotation("m1", "c1", "subsidy_percentage", "Subsidy is 20%", "ERROR", 20.0),
        ClaimAnnotation("m2", "c2", "subsidy_percentage", "Alternatively subsidy is 25%", "ERROR", 25.0)
    ]
    # Participant matches the second erroneous claim (25.0)
    res = evaluate_automation_bias(anns, {"subsidy_percentage": 25.0}, doc_clicks=0, doc_duration=0.0)
    assert res["field_matches"]["subsidy_percentage"] == True
    assert res["task_automation_bias"] == 1

def test_automation_bias_case_h_blank_unsubmitted_answer():
    # Case H: Participant answer is blank/unsubmitted -> AutomationBias = 0
    anns = [ClaimAnnotation("m1", "c1", "subsidy_percentage", "Subsidy is 25%", "ERROR", 25.0)]
    res = evaluate_automation_bias(anns, {"subsidy_percentage": None}, doc_clicks=0, doc_duration=0.0)
    assert res["field_matches"]["subsidy_percentage"] == False
    assert res["task_automation_bias"] == 0
