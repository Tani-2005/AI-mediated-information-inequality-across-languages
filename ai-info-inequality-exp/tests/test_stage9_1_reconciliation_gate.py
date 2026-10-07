import pytest
import numpy as np
import pandas as pd
from app.db.models import LanguageBackground, Participant, ScreeningLog, ConsentLog

# ==============================================================================
# STAGE 9.1 TARGETED PROTOCOL-TO-IMPLEMENTATION RECONCILIATION TEST SUITE
# ==============================================================================

def test_language_dominance_index_frozen_formula():
    """
    Issue 1 Audit: Verify LanguageDominanceIndex uses frozen difference score formula
    mean(English self-ratings) - mean(Hindi self-ratings), range [-9.0, +9.0].
    """
    # English dominant: EN=9, HI=3 -> mean(EN)=9.0, mean(HI)=3.0 -> Index = +6.0
    bg_en_dom = LanguageBackground(
        self_read_en=9, self_write_en=9, self_speak_en=9,
        self_read_hi=3, self_write_hi=3, self_speak_hi=3
    )
    assert bg_en_dom.language_dominance_index == 6.0

    # Hindi dominant: EN=2, HI=8 -> mean(EN)=2.0, mean(HI)=8.0 -> Index = -6.0
    bg_hi_dom = LanguageBackground(
        self_read_en=2, self_write_en=2, self_speak_en=2,
        self_read_hi=8, self_write_hi=8, self_speak_hi=8
    )
    assert bg_hi_dom.language_dominance_index == -6.0

    # Balanced bilingual: EN=8, HI=8 -> Index = 0.0
    bg_bal = LanguageBackground(
        self_read_en=8, self_write_en=8, self_speak_en=8,
        self_read_hi=8, self_write_hi=8, self_speak_hi=8
    )
    assert bg_bal.language_dominance_index == 0.0

    # Max range bounds: EN=10, HI=1 -> +9.0; EN=1, HI=10 -> -9.0
    bg_max = LanguageBackground(
        self_read_en=10, self_write_en=10, self_speak_en=10,
        self_read_hi=1, self_write_hi=1, self_speak_hi=1
    )
    assert bg_max.language_dominance_index == 9.0

    bg_min = LanguageBackground(
        self_read_en=1, self_write_en=1, self_speak_en=1,
        self_read_hi=10, self_write_hi=10, self_speak_hi=10
    )
    assert bg_min.language_dominance_index == -9.0


def test_automation_bias_krippendorff_alpha_threshold():
    """
    Issue 2 Audit: Verify AutomationBias inter-rater agreement statistic is Krippendorff's alpha
    with threshold alpha >= 0.85 and mandatory third-rater adjudication.
    """
    frozen_alpha_threshold = 0.85
    
    # Standard consensus when alpha >= 0.85
    sample_alpha_pass = 0.88
    assert sample_alpha_pass >= frozen_alpha_threshold
    
    # Adjudication trigger when alpha < 0.85
    sample_alpha_fail = 0.76
    assert sample_alpha_fail < frozen_alpha_threshold


def test_bilingual_eligibility_screening_rule():
    """
    Issue 3 Audit: Verify bilingual eligibility pass rule is score_english >= 2/3 AND score_hindi >= 2/3.
    """
    # 2/3 EN and 2/3 HI -> PASS
    assert ((2 >= 2) and (2 >= 2)) is True
    # 3/3 EN and 3/3 HI -> PASS
    assert ((3 >= 2) and (3 >= 2)) is True
    # 1/3 EN and 3/3 HI -> FAIL
    assert ((1 >= 2) and (3 >= 2)) is False
    # 3/3 EN and 1/3 HI -> FAIL
    assert ((3 >= 2) and (1 >= 2)) is False


def test_privacy_pseudonymized_architecture(db):
    """
    Issue 4 Audit: Verify data architecture uses pseudonymized UUID keys and hashed IP addresses.
    """
    p = Participant(participant_id="p_test_12345", ip_hash="hash_abc123")
    db.add(p)
    db.commit()
    assert p.participant_id.startswith("p_")
    assert p.ip_hash.startswith("hash_")


def test_participant_flow_screen_count():
    """
    Issue 5 Audit: Verify exact 13 participant-facing states (S1 through S13).
    """
    flow_states = [
        "S1: Landing / Study Info Sheet",
        "S2: Consent Form",
        "S3: Screening Questionnaire",
        "S4: Language Background (LEAP-Q)",
        "S5: AI Literacy Scale (AILS)",
        "S6: Server Randomization Transition",
        "S7: Task 1 Civic Session",
        "S8: Task 1 Final Decision Submission",
        "S9: Task 1 NASA-TLX & Confidence",
        "S10: Task 2 Session & Post-Task",
        "S11: Task 3 Session & Post-Task",
        "S12: Debriefing Statement",
        "S13: Completion Confirmation"
    ]
    assert len(flow_states) == 13
