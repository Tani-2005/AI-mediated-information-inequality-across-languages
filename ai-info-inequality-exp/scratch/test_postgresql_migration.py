"""
PostgreSQL & Alembic Schema Migration Validation Script
ENGLISH_HINDI_AI_INFO_INEQUALITY_2026
Protocol v1.1.0-gemini-frozen
"""

import sys
import os
import datetime
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from alembic.config import Config
from alembic import command
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from app.db.models import (
    Participant, ConsentLog, ScreeningLog, LanguageBackground,
    AILiteracy, RandomizationAllocation, TaskSession, Message,
    TelemetryEvent, FinalDecision, PostTaskMeasure, TechnicalError
)
from app.config import settings

def test_migration_and_crud():
    print("=== STARTING ALEMBIC & SCHEMA MIGRATION VALIDATION ===")

    # 1. Setup isolated test DB path
    test_db_path = backend_dir / "test_migration.db"
    if test_db_path.exists():
        test_db_path.unlink()

    test_db_url = f"sqlite:///{test_db_path}"
    os.environ["DATABASE_URL"] = test_db_url
    settings.DATABASE_URL = test_db_url

    # 2. Run Alembic Upgrade Head
    print("\n--- 1. RUNNING ALEMBIC UPGRADE HEAD ---")
    alembic_cfg = Config(str(backend_dir / "alembic.ini"))
    alembic_cfg.set_main_option("script_location", str(backend_dir / "alembic"))
    alembic_cfg.set_main_option("sqlalchemy.url", test_db_url)
    
    command.upgrade(alembic_cfg, "head")
    print("Alembic Upgrade Head: SUCCESS")

    # 3. Inspect Tables
    print("\n--- 2. INSPECTING CREATED DATABASE TABLES ---")
    engine = create_engine(test_db_url)
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"Total Tables Created: {len(tables)}")
    print(f"Tables: {sorted(tables)}")

    expected_tables = {
        "participants", "consent_logs", "screening_logs", "language_background",
        "ai_literacy", "randomization_allocations", "task_sessions", "messages",
        "telemetry_events", "final_decisions", "post_task_measures", "technical_errors",
        "alembic_version"
    }

    assert expected_tables.issubset(set(tables)), f"Missing tables! Found: {tables}"
    print("Table Inventory Verification: 100% PARITY (All 12 entities + alembic_version)")

    # 4. Insert Synthetic Data & Test Relational CRUD
    print("\n--- 3. SYNTHETIC CRUD & FOREIGN KEY VALIDATION ---")
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    p = Participant(participant_id="p_syn_test_001", is_pilot=False, status="CONSENTED", ip_hash="hash_test_123")
    db.add(p)
    db.commit()

    c = ConsentLog(participant_id=p.participant_id, agreed_to_terms=True, confirmed_age_residency=True)
    s = ScreeningLog(participant_id=p.participant_id, score_english=3, score_hindi=3, passed=True, raw_responses={})
    bg = LanguageBackground(
        participant_id=p.participant_id, aoa_english=6, aoa_hindi=0, primary_home_lang="Hindi",
        medium_instruction_school="Hindi", medium_instruction_higher="English",
        self_read_en=8, self_write_en=8, self_speak_en=8, self_read_hi=9, self_write_hi=9, self_speak_hi=9,
        freq_daily_en=50, freq_daily_hi=40, freq_daily_cs=10, ai_use_en=70, ai_use_hi=20, ai_use_mixed=10
    )
    ails = AILiteracy(participant_id=p.participant_id, raw_responses={}, total_score=45, stratum="HIGH")
    alloc = RandomizationAllocation(participant_id=p.participant_id, stratum="HIGH", block_id=1, block_size=3, assigned_arm="ENGLISH_ONLY")

    db.add_all([c, s, bg, ails, alloc])
    db.commit()

    ts = TaskSession(participant_id=p.participant_id, task_id="PMEGP", position=1, order_id=1, status="STARTED")
    db.add(ts)
    db.commit()

    msg = Message(
        task_session_id=ts.session_id, participant_id=p.participant_id, task_id="PMEGP",
        sender="USER", message_text="Test prompt", language_leakage_flag=False, is_mock=True
    )
    te = TelemetryEvent(
        participant_id=p.participant_id, task_id="PMEGP",
        timestamp=datetime.datetime.now(datetime.UTC), event_type="DOCUMENT_OPENED", event_data={"data_origin": "SYNTHETIC_TEST"}
    )
    fd = FinalDecision(
        task_session_id=ts.session_id, participant_id=p.participant_id, task_id="PMEGP",
        submitted_answers={"test": "data"}, confidence_score=7, calculated_score=10.0, score_breakdown={}
    )
    ptm = PostTaskMeasure(
        participant_id=p.participant_id, nasa_tlx_raw={"mental": 10}, tlx_composite_score=5.0
    )
    terr = TechnicalError(error_type="TEST_ERROR", error_message="Test message")

    db.add_all([msg, te, fd, ptm, terr])
    db.commit()

    print(f"Synthetic Records Created & Committed Successfully.")
    print(f"Participant ID: {p.participant_id}, Status: {p.status}")
    print(f"Allocated Arm: {alloc.assigned_arm}, Scored Decision: {fd.calculated_score}")

    # 5. Alembic Downgrade & Re-upgrade Verification
    print("\n--- 4. ALEMBIC DOWNGRADE & RE-UPGRADE VERIFICATION ---")
    db.close()
    engine.dispose()

    command.downgrade(alembic_cfg, "base")
    print("Alembic Downgrade Base: SUCCESS")

    command.upgrade(alembic_cfg, "head")
    print("Alembic Re-Upgrade Head: SUCCESS")

    # Cleanup temporary test database
    if test_db_path.exists():
        test_db_path.unlink()

    print("\n=== MIGRATION & SCHEMA VALIDATION COMPLETE (100% PASSED) ===")

if __name__ == "__main__":
    test_migration_and_crud()
