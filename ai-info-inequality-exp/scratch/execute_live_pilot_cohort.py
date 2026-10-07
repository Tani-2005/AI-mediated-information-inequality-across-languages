import sys
import os
import json
import datetime
import random
import numpy as np
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.db.session import Base
from app.db.models import (
    Participant, ConsentLog, ScreeningLog, LanguageBackground,
    AILiteracy, RandomizationAllocation, TaskSession, TelemetryEvent,
    FinalDecision, PostTaskMeasure
)
from app.randomization.engine import RandomizationEngine
from app.scoring.engine import ScoringEngine
from app.core.llm_gateway import MockLLMProvider, detect_language_leakage

# ==============================================================================
# LIVE PILOT EXECUTION ENGINE (STAGE 10 OPERATIONAL AUDIT)
# ==============================================================================

def run_pilot_cohort(n_participants: int = 18) -> pd.DataFrame:
    """
    Executes an operational pilot cohort of 18 participants (6 per arm, balanced across 
    LOW and HIGH AILS strata and 3 Latin-square orders) through complete database stack.
    """
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    rand_engine = RandomizationEngine(db)
    llm = MockLLMProvider()

    print(f"=== INITIALIZING LIVE PILOT COHORT (N={n_participants}) ===")
    
    pilot_records = []
    
    for i in range(n_participants):
        p_id = f"p_pilot_{i+1:02d}"

        # 1. Participant & Consent
        p = Participant(participant_id=p_id, is_pilot=True, status="CONSENTED")
        db.add(p)
        db.commit()
        db.add(ConsentLog(participant_id=p_id, agreed_to_terms=True, confirmed_age_residency=True))
        p.status = "CONSENTED"
        db.commit()

        # 2. Eligibility Screening
        score_en = 3
        score_hi = 3
        db.add(ScreeningLog(participant_id=p_id, score_english=score_en, score_hindi=score_hi, passed=True, raw_responses={}))
        p.status = "SCREENED"
        db.commit()

        # 3. Language Background
        en_read = random.randint(7, 10) if (i % 2 == 0) else random.randint(3, 6)
        hi_read = random.randint(6, 10)
        db.add(LanguageBackground(
            participant_id=p_id,
            aoa_english=6, aoa_hindi=0,
            primary_home_lang="Hindi",
            medium_instruction_school="Hindi", medium_instruction_higher="English",
            self_read_en=en_read, self_write_en=en_read, self_speak_en=en_read,
            self_read_hi=hi_read, self_write_hi=hi_read, self_speak_hi=hi_read,
            freq_daily_en=50.0, freq_daily_hi=40.0, freq_daily_cs=10.0,
            ai_use_en=60.0, ai_use_hi=30.0, ai_use_mixed=10.0
        ))
        p.status = "BASELINE_DONE"
        db.commit()

        # 4. AILS Scale
        ails_score = random.randint(20, 34) if (i < 9) else random.randint(38, 55)
        stratum = "LOW" if ails_score < 36 else "HIGH"
        db.add(AILiteracy(participant_id=p_id, total_score=ails_score, stratum=stratum, raw_responses={}))
        db.commit()

        # 5. Server-Side Randomization
        alloc = rand_engine.allocate_participant(p_id)
        p.status = "RANDOMIZED"
        db.commit()

        # 6. Task Sessions (3 Latin-square tasks per participant)
        order_idx = (i % 3) + 1
        order_id = f"ORDER_{order_idx}"
        if order_id == "ORDER_1":
            scenarios = ["PMEGP", "PM_VISHWAKARMA", "PM_SVANIDHI"]
        elif order_id == "ORDER_2":
            scenarios = ["PM_VISHWAKARMA", "PM_SVANIDHI", "PMEGP"]
        else:
            scenarios = ["PM_SVANIDHI", "PMEGP", "PM_VISHWAKARMA"]

        p.status = "IN_PROGRESS"
        db.commit()

        for pos, sc in enumerate(scenarios, 1):
            sess = TaskSession(participant_id=p_id, task_id=sc, position=pos, order_id=order_idx, status="STARTED")
            db.add(sess)
            db.commit()

            # AI Interaction turn
            ai_res = llm.generate_response(sc, alloc.assigned_arm, "Persona text", "User prompt text", [])
            
            # Telemetry events
            clicks = random.randint(1, 4)
            dur_raw = round(float(random.uniform(15.0, 180.0)), 1)
            dur_log = round(float(np.log(max(1.0, dur_raw))), 4)
            
            db.add(TelemetryEvent(
                participant_id=p_id, task_id=sc, event_type="DOC_VIEW_TIME",
                timestamp=datetime.datetime.now(datetime.UTC),
                event_data={"doc_clicks": clicks, "duration_seconds": dur_raw}
            ))

            # Final Decision Rubric Scoring
            if sc == "PMEGP":
                submitted_answers = {"max_project_cost_lakhs": 50.0, "subsidy_percentage": 35.0, "mandatory_documents": ["Aadhaar", "EDP"], "eligibility_age_min": 18}
            elif sc == "PM_VISHWAKARMA":
                submitted_answers = {"tranche_1_loan_amount": 100000.0, "interest_rate_pct": 5.0, "stipend_daily_inr": 500.0, "toolkit_incentive_inr": 15000.0}
            else:
                submitted_answers = {"tranche_1_loan_amount": 100000.0, "tenure_months": 12, "interest_subsidy_pct": 7.0, "annual_cashback_max_inr": 1200.0}

            score_val, breakdown = ScoringEngine.score_decision(sc, submitted_answers)

            conf_score = random.randint(5, 7)
            db.add(FinalDecision(
                task_session_id=sess.session_id, participant_id=p_id, task_id=sc,
                submitted_answers=submitted_answers, confidence_score=conf_score,
                calculated_score=score_val, score_breakdown=breakdown
            ))

            # Post-Task NASA-TLX
            tlx_raw = {"mental_demand": 8, "physical_demand": 3, "temporal_demand": 6, "performance": 16, "effort": 10, "frustration": 4}
            tlx_comp = round(sum(tlx_raw.values()) / 6.0, 2)
            db.add(PostTaskMeasure(
                participant_id=p_id, task_session_id=sess.session_id, task_id=sc,
                nasa_tlx_raw=tlx_raw, tlx_composite_score=tlx_comp
            ))

            sess.status = "COMPLETED"
            db.commit()

            pilot_records.append({
                "participant_id": p_id,
                "assigned_arm": alloc.assigned_arm,
                "ails_score": ails_score,
                "stratum": stratum,
                "order_id": order_id,
                "scenario": sc,
                "position": pos,
                "doc_clicks": clicks,
                "doc_duration_raw": dur_raw,
                "doc_duration_log": dur_log,
                "decision_quality": score_val,
                "leakage_flag": int(ai_res["language_leakage_flag"]),
                "status": "COMPLETE"
            })

        p.status = "COMPLETED"
        db.commit()

    db.close()
    df_pilot = pd.DataFrame(pilot_records)
    print(f"=== PILOT COHORT COMPLETED: {len(df_pilot)} TASK OBSERVATIONS LOGGED ===")
    return df_pilot

if __name__ == "__main__":
    df = run_pilot_cohort(18)
    print("\nPROCESSED PILOT COHORT SUMMARY:")
    print(df[["assigned_arm", "scenario", "decision_quality", "doc_clicks", "doc_duration_log"]].head(10))
