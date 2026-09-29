"""
Synthetic End-to-End Dry Run Script
ENGLISH_HINDI_AI_INFO_INEQUALITY_2026
Protocol v1.1.0-gemini-frozen
"""

import sys
import os
import json
import random
import datetime
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.session import Base
from app.db.models import (
    Participant, ConsentLog, ScreeningLog, LanguageBackground,
    AILiteracy, RandomizationAllocation, TaskSession, Message,
    TelemetryEvent, FinalDecision, PostTaskMeasure, TechnicalError
)
from app.randomization.engine import RandomizationEngine
from app.scoring.engine import ScoringEngine
from app.core.prompts import build_system_prompt, SYSTEM_PROMPT_V1_1_GEMINI
from app.core.llm_gateway import GeminiProvider, MockLLMProvider, get_llm_provider
from app.config import settings, frozen_config

def run_dry_run():
    print("=== STARTING SYNTHETIC EXPERIMENT DRY RUN ===")
    
    # 1. Create isolated in-memory SQLite database for dry run
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    # 2. Randomization Simulation (N = 171 synthetic participants)
    print("\n--- 1. RANDOMIZATION & STRATIFICATION AUDIT (N=171) ---")
    randomizer = RandomizationEngine(db)
    
    arm_counts = {"ENGLISH_ONLY": 0, "HINDI_ONLY": 0, "CODE_SWITCHING": 0}
    stratum_counts = {"LOW": 0, "HIGH": 0}
    order_counts = {1: 0, 2: 0, 3: 0}

    synthetic_participants = []

    for i in range(171):
        # Create synthetic participant
        p = Participant(
            participant_id=f"p_syn_{i+1:03d}",
            is_pilot=False,
            status="CONSENTED",
            ip_hash=f"hash_syn_{i+1:03d}"
        )
        db.add(p)
        db.commit()

        # Consent
        c = ConsentLog(
            participant_id=p.participant_id,
            agreed_to_terms=True,
            confirmed_age_residency=True
        )
        db.add(c)

        # Screening (make 144 pass, 27 fail to test screening exclusion)
        should_pass = i < 144
        score_en = 3 if should_pass else random.choice([0, 1])
        score_hi = 3 if should_pass else random.choice([0, 1])
        
        s = ScreeningLog(
            participant_id=p.participant_id,
            score_english=score_en,
            score_hindi=score_hi,
            passed=should_pass,
            raw_responses={"q1": "B", "q2": "A", "q3": "C", "q4": "A", "q5": "C", "q6": "B"}
        )
        db.add(s)

        if not should_pass:
            p.status = "EXCLUDED"
            db.commit()
            continue

        p.status = "SCREENED"
        
        # LEAP-Q
        l = LanguageBackground(
            participant_id=p.participant_id,
            aoa_english=6,
            aoa_hindi=3,
            primary_home_lang="Hindi",
            medium_instruction_school="Hindi",
            medium_instruction_higher="English",
            self_read_en=8, self_write_en=8, self_speak_en=8,
            self_read_hi=8, self_write_hi=8, self_speak_hi=8,
            freq_daily_en=50.0, freq_daily_hi=40.0, freq_daily_cs=10.0,
            ai_use_en=70.0, ai_use_hi=20.0, ai_use_mixed=10.0
        )
        db.add(l)

        # AILS
        ails_score = random.randint(12, 35) if (i % 2 == 0) else random.randint(36, 60)
        stratum = randomizer.get_stratum(ails_score)
        stratum_counts[stratum] += 1

        a = AILiteracy(
            participant_id=p.participant_id,
            raw_responses={f"item_{j}": (ails_score // 12) for j in range(1, 13)},
            total_score=ails_score,
            stratum=stratum
        )
        db.add(a)
        p.status = "BASELINE_DONE"
        db.commit()

        # Randomize
        alloc = randomizer.allocate_participant(p.participant_id)
        arm_counts[alloc.assigned_arm] += 1
        synthetic_participants.append(p.participant_id)

    print(f"Total Synthetic Participants Created: 171")
    print(f"Screening Passed (Analyzable Candidates): 144")
    print(f"Screening Excluded: 27")
    print(f"Stratum Counts: {stratum_counts}")
    print(f"Arm Allocation Counts: {arm_counts}")

    # 3. Complete Flow Execution for 144 Screened Participants
    print("\n--- 2. APPLICATION FLOW & SCORING AUDIT ---")
    scoring_engine = ScoringEngine()
    LATIN_SQUARE_ORDERS = {
        1: ["PMEGP", "PM_VISHWAKARMA", "PM_SVANIDHI"],
        2: ["PM_VISHWAKARMA", "PM_SVANIDHI", "PMEGP"],
        3: ["PM_SVANIDHI", "PMEGP", "PM_VISHWAKARMA"]
    }

    total_tasks_created = 0
    total_decisions_scored = 0
    total_telemetry_logged = 0

    for idx, p_id in enumerate(synthetic_participants):
        p = db.query(Participant).filter(Participant.participant_id == p_id).first()
        order_id = (idx % 3) + 1
        order_counts[order_id] += 1
        scenarios = LATIN_SQUARE_ORDERS[order_id]

        p.status = "IN_PROGRESS"
        db.commit()

        for pos, scenario in enumerate(scenarios, start=1):
            ts = TaskSession(
                participant_id=p_id,
                task_id=scenario,
                position=pos,
                order_id=order_id,
                status="STARTED"
            )
            db.add(ts)
            db.commit()
            total_tasks_created += 1

            # Telemetry Task Start
            t_start = TelemetryEvent(
                participant_id=p_id,
                task_id=scenario,
                timestamp=datetime.datetime.now(datetime.UTC),
                event_type="TASK_STARTED",
                event_data={"position": pos, "order_id": order_id}
            )
            db.add(t_start)

            # Document Clicks & Duration
            t_doc = TelemetryEvent(
                participant_id=p_id,
                task_id=scenario,
                timestamp=datetime.datetime.now(datetime.UTC),
                event_type="DOCUMENT_OPENED",
                event_data={"doc_id": f"GUIDELINES_{scenario}", "view_duration_ms": 45000}
            )
            db.add(t_doc)

            # Window Blur
            t_blur = TelemetryEvent(
                participant_id=p_id,
                task_id=scenario,
                timestamp=datetime.datetime.now(datetime.UTC),
                event_type="TAB_FOCUS_CHANGED",
                event_data={"focused": False, "dwell_time_ms": 1200}
            )
            db.add(t_blur)
            total_telemetry_logged += 3

            # Submit Message
            msg_user = Message(
                task_session_id=ts.session_id,
                participant_id=p_id,
                task_id=scenario,
                sender="USER",
                message_text=f"What are the eligibility criteria for {scenario}?"
            )
            db.add(msg_user)

            # Model Response Simulation
            sys_prompt = build_system_prompt(p.randomization.assigned_arm, "v1.1.0-gemini-frozen")
            msg_ai = Message(
                task_session_id=ts.session_id,
                participant_id=p_id,
                task_id=scenario,
                sender="AI",
                message_text=f"Official details for {scenario} under assigned arm {p.randomization.assigned_arm}.",
                tokens_used=120,
                latency_ms=850,
                language_leakage_flag=False,
                is_mock=True
            )
            db.add(msg_ai)

            # Final Decision Answers
            if scenario == "PMEGP":
                submitted_ans = {
                    "is_eligible": True,
                    "max_project_cost_manufacturing": 5000000,
                    "subsidy_pct_special_rural": 35.0,
                    "mandatory_documents": ["Aadhaar Card", "Project Report", "EDP Certificate"]
                }
            elif scenario == "PM_VISHWAKARMA":
                submitted_ans = {
                    "is_eligible": True,
                    "tranche_1_loan_amount": 100000,
                    "skill_training_stipend_per_day": 500,
                    "toolkit_incentive_grant": 15000
                }
            else: # PM_SVANIDHI
                submitted_ans = {
                    "is_eligible": True,
                    "first_tranche_loan_amount": 10000,
                    "interest_subsidy_pct": 7.0,
                    "annual_digital_cashback_max": 1200
                }

            dq_score, breakdown = scoring_engine.score_decision(scenario, submitted_ans)

            fd = FinalDecision(
                task_session_id=ts.session_id,
                participant_id=p_id,
                task_id=scenario,
                submitted_answers=submitted_ans,
                confidence_score=6,
                calculated_score=dq_score,
                score_breakdown=breakdown
            )
            db.add(fd)
            total_decisions_scored += 1

            ts.status = "COMPLETED"
            ts.completed_at = datetime.datetime.now(datetime.UTC)
            db.commit()

        # Post-task measures submitted once per participant at end of session
        ptm = PostTaskMeasure(
            participant_id=p_id,
            nasa_tlx_raw={"mental": 10, "physical": 2, "temporal": 8, "performance": 18, "effort": 12, "frustration": 4},
            tlx_composite_score=9.0,
            feedback_comments="Synthetic feedback string."
        )
        db.add(ptm)

        p.status = "COMPLETED"
        db.commit()

    print(f"Total Task Sessions Created: {total_tasks_created}")
    print(f"Total Decisions Scored: {total_decisions_scored}")
    print(f"Total Telemetry Events Logged: {total_telemetry_logged}")
    print(f"Order Counterbalancing Distribution: {order_counts}")

    # 4. Database Integrity Verification
    print("\n--- 3. DATABASE RELATIONAL INTEGRITY VERIFICATION ---")
    
    # Check for orphan records
    orphan_decisions = db.query(FinalDecision).filter(~FinalDecision.task_session_id.in_(db.query(TaskSession.session_id))).count()
    orphan_telemetry = db.query(TelemetryEvent).filter(~TelemetryEvent.participant_id.in_(db.query(Participant.participant_id))).count()
    orphan_allocations = db.query(RandomizationAllocation).filter(~RandomizationAllocation.participant_id.in_(db.query(Participant.participant_id))).count()
    
    print(f"Orphan Final Decisions: {orphan_decisions}")
    print(f"Orphan Telemetry Events: {orphan_telemetry}")
    print(f"Orphan Randomization Allocations: {orphan_allocations}")

    # Check session counts per participant
    participant_task_counts = {}
    for p_id in synthetic_participants:
        count = db.query(TaskSession).filter(TaskSession.participant_id == p_id, TaskSession.status == "COMPLETED").count()
        participant_task_counts[count] = participant_task_counts.get(count, 0) + 1
    
    print(f"Completed Tasks Per Screened Participant: {participant_task_counts}")

    # 5. Failure Injection Audit
    print("\n--- 4. FAILURE INJECTION AUDIT ---")
    
    # Injection 1: Scoring engine malformed input format
    try:
        dq_bad, breakdown_bad = scoring_engine.score_decision("PMEGP", {"invalid_field": 999})
        print(f"Failure Test 1 (Malformed Answer Format): Score={dq_bad} (Safe fallback handled)")
    except Exception as e:
        print(f"Failure Test 1 Exception: {e}")

    # Injection 2: Duplicate allocation attempt
    try:
        alloc_dup = randomizer.allocate_participant(synthetic_participants[0])
        print(f"Failure Test 2 (Duplicate Randomization): Unexpectedly Succeeded")
    except ValueError as e:
        print(f"Failure Test 2 (Duplicate Randomization Safeguard): PASSED ({e})")

    # Injection 3: Provider identity mismatch check
    try:
        gemini_provider = GeminiProvider()
        gemini_provider.validate_provider_configuration()
        print(f"Failure Test 3 (Gemini Config Validation): PASSED")
    except Exception as e:
        print(f"Failure Test 3 Gemini Validation: {e}")

    print("\n=== SYNTHETIC DRY RUN EXECUTION COMPLETE ===")

if __name__ == "__main__":
    run_dry_run()
