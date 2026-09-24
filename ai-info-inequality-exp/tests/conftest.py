import sys
from pathlib import Path
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.db.session import Base
from app.db.models import Participant, ConsentLog, ScreeningLog, LanguageBackground, AILiteracy

TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture
def db():
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def fully_eligible_participant(db):
    p = Participant()
    db.add(p)
    db.commit()

    consent = ConsentLog(participant_id=p.participant_id, agreed_to_terms=True, confirmed_age_residency=True)
    screening = ScreeningLog(participant_id=p.participant_id, score_english=3, score_hindi=3, passed=True, raw_responses={})
    bg = LanguageBackground(
        participant_id=p.participant_id, aoa_english=6, aoa_hindi=0, primary_home_lang="Hindi",
        medium_instruction_school="Hindi", medium_instruction_higher="English",
        self_read_en=8, self_write_en=8, self_speak_en=8, self_read_hi=9, self_write_hi=9, self_speak_hi=9,
        freq_daily_en=50, freq_daily_hi=40, freq_daily_cs=10, ai_use_en=70, ai_use_hi=20, ai_use_mixed=10
    )
    ails = AILiteracy(participant_id=p.participant_id, raw_responses={}, total_score=45, stratum="HIGH")

    db.add_all([consent, screening, bg, ails])
    p.status = "BASELINE_DONE"
    db.commit()
    db.refresh(p)
    return p
