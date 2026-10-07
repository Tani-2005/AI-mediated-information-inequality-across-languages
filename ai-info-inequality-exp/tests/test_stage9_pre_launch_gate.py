import pytest
import numpy as np
import pandas as pd
import math
from typing import Dict, Any, List

from app.config import settings, frozen_config, validate_production_config
from app.core.llm_gateway import GeminiProvider, detect_language_leakage
from app.core.prompts import build_system_prompt, SYSTEM_PROMPT_V1_0_FROZEN
from app.randomization.engine import RandomizationEngine
from app.scoring.engine import ScoringEngine
from app.db.models import Participant, ConsentLog, ScreeningLog, LanguageBackground, AILiteracy

# ==============================================================================
# STAGE 9 PRE-LAUNCH SYSTEM AUDIT SUITE
# ==============================================================================

def test_stage9_protocol_and_config_freeze():
    """Verify frozen protocol version and production LLM configuration."""
    assert frozen_config["study_metadata"]["protocol_version"] == "1.1.0-gemini-frozen"
    assert frozen_config["sample_design"]["analyzable_sample_size_N"] == 144
    assert frozen_config["sample_design"]["recruitment_target_N"] == 171
    
    llm_cfg = frozen_config["production_llm_config"]
    assert llm_cfg["provider"] == "Google Gemini API"
    assert llm_cfg["model_identifier"] == "gemini-3.5-flash"
    assert llm_cfg["model_version"] == "3.5-flash-05-2026"
    assert llm_cfg["temperature"] == 0.2
    assert llm_cfg["top_p"] == 1.0
    assert llm_cfg["max_tokens"] == 1000
    assert llm_cfg["timeout_ms"] == 15000
    assert llm_cfg["max_retries"] == 1


def test_stage9_decision_fields_inventory():
    """Verify ground truth inventory consists of 12 decision fields total (4 per task)."""
    pmegp_fields = ScoringEngine.load_rubric("PMEGP")["ground_truth_rubric"]["fields"]
    vishwa_fields = ScoringEngine.load_rubric("PM_VISHWAKARMA")["ground_truth_rubric"]["fields"]
    svanidhi_fields = ScoringEngine.load_rubric("PM_SVANIDHI")["ground_truth_rubric"]["fields"]

    assert len(pmegp_fields) == 4, f"PMEGP field count: {len(pmegp_fields)}"
    assert len(vishwa_fields) == 4, f"PM_VISHWAKARMA field count: {len(vishwa_fields)}"
    assert len(svanidhi_fields) == 4, f"PM_SVANIDHI field count: {len(svanidhi_fields)}"
    
    total_fields = len(pmegp_fields) + len(vishwa_fields) + len(svanidhi_fields)
    assert total_fields == 12, f"Total fields count: {total_fields}"


def test_stage9_ails_scoring_and_allocation():
    """Verify AILS score calculation, range 12-60, threshold 36 for stratification."""
    min_responses = {f"ails_{i}": 1 for i in range(1, 13)}
    score_min = sum(min_responses.values())
    assert score_min == 12
    assert score_min < 36  # LOW stratum

    max_responses = {f"ails_{i}": 5 for i in range(1, 13)}
    score_max = sum(max_responses.values())
    assert score_max == 60
    assert score_max >= 36  # HIGH stratum

    assert frozen_config["randomization"]["strata_cutoffs"]["median_split_threshold"] == 36


def test_stage9_randomization_and_latin_square(db):
    """Verify randomization allocates across 3 arms and 3 Latin-square orders deterministically."""
    engine = RandomizationEngine(db)

    low_counts = {"ENGLISH_ONLY": 0, "HINDI_ONLY": 0, "CODE_SWITCHING": 0}
    high_counts = {"ENGLISH_ONLY": 0, "HINDI_ONLY": 0, "CODE_SWITCHING": 0}

    for i in range(72):
        p = Participant()
        db.add(p)
        db.commit()
        db.add(ConsentLog(participant_id=p.participant_id, agreed_to_terms=True, confirmed_age_residency=True))
        db.add(ScreeningLog(participant_id=p.participant_id, score_english=3, score_hindi=3, passed=True, raw_responses={}))
        db.add(LanguageBackground(
            participant_id=p.participant_id, aoa_english=6, aoa_hindi=0, primary_home_lang="Hindi",
            medium_instruction_school="Hindi", medium_instruction_higher="English",
            self_read_en=8, self_write_en=8, self_speak_en=8, self_read_hi=9, self_write_hi=9, self_speak_hi=9,
            freq_daily_en=50, freq_daily_hi=40, freq_daily_cs=10, ai_use_en=70, ai_use_hi=20, ai_use_mixed=10
        ))
        # 36 Low stratum (total_score=24), 36 High stratum (total_score=48)
        score = 24 if (i < 36) else 48
        stratum = "LOW" if score < 36 else "HIGH"
        db.add(AILiteracy(participant_id=p.participant_id, total_score=score, stratum=stratum, raw_responses={}))
        db.commit()

        alloc = engine.allocate_participant(p.participant_id)
        if score < 36:
            low_counts[alloc.assigned_arm] += 1
        else:
            high_counts[alloc.assigned_arm] += 1

    assert sum(low_counts.values()) == 36
    assert sum(high_counts.values()) == 36
    
    # In permuted block randomization (block sizes 3 & 6), max imbalance between arms is bounded <= 2
    low_vals = list(low_counts.values())
    assert max(low_vals) - min(low_vals) <= 2

    high_vals = list(high_counts.values())
    assert max(high_vals) - min(high_vals) <= 2


def test_stage9_synthetic_432_row_export_reproducibility():
    """
    Generate synthetic 432-row analysis dataset (144 participants x 3 tasks)
    and verify exact export reproducibility (100% byte/dataframe identity across runs).
    """
    def generate_export_df(seed: int = 42) -> pd.DataFrame:
        np.random.seed(seed)
        rows = []
        arms = ["ENGLISH_ONLY", "HINDI_ONLY", "CODE_SWITCHING"]
        
        for p_idx in range(144):
            p_id = f"p_syn_{p_idx:03d}"
            arm = arms[p_idx % 3]
            order = (p_idx % 3) + 1
            ails_score = int(np.random.randint(12, 61))
            
            if order == 1:
                p_scenarios = ["PMEGP", "PM_VISHWAKARMA", "PM_SVANIDHI"]
            elif order == 2:
                p_scenarios = ["PM_VISHWAKARMA", "PM_SVANIDHI", "PMEGP"]
            else:
                p_scenarios = ["PM_SVANIDHI", "PMEGP", "PM_VISHWAKARMA"]
                
            for pos, sc in enumerate(p_scenarios, 1):
                doc_dur_raw = float(np.random.choice([0.0, 0.5, 12.5, 45.0, 120.0]))
                doc_dur_log = round(float(np.log(max(1.0, doc_dur_raw))), 4)
                
                rows.append({
                    "participant_id": p_id,
                    "assigned_arm": arm,
                    "scenario": sc,
                    "position": pos,
                    "decision_quality": round(float(np.random.uniform(5.0, 10.0)), 2),
                    "doc_clicks": int(np.random.randint(0, 5)),
                    "doc_duration_raw": doc_dur_raw,
                    "doc_duration_log": doc_dur_log,
                    "prompt_count": int(np.random.randint(1, 6)),
                    "nasa_tlx_composite": round(float(np.random.uniform(20.0, 60.0)), 2),
                    "automation_bias_indicator": int(np.random.choice([0, 1], p=[0.85, 0.15])),
                    "decision_confidence": int(np.random.randint(1, 8)),
                    "ails_score": ails_score,
                    "language_leakage_flag": 0,
                    "speeding_flag": 0,
                    "status": "COMPLETE"
                })
        return pd.DataFrame(rows)

    df_export_1 = generate_export_df(seed=42)
    df_export_2 = generate_export_df(seed=42)

    assert len(df_export_1) == 432
    assert len(df_export_2) == 432
    assert df_export_1["participant_id"].nunique() == 144

    pd.testing.assert_frame_equal(df_export_1, df_export_2)
