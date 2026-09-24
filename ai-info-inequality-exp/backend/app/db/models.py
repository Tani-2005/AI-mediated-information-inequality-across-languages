import datetime
import uuid
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Text, JSON, Index
from sqlalchemy.orm import relationship
from app.db.session import Base

def generate_uuid():
    return f"p_{uuid.uuid4()}"

def generate_ip_hash():
    return f"hash_{uuid.uuid4()}"[:32]

class Participant(Base):
    __tablename__ = "participants"

    participant_id = Column(String(64), primary_key=True, default=generate_uuid)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.UTC))
    status = Column(String(32), default="CONSENTED", nullable=False) # CONSENTED, SCREENED, BASELINE_DONE, RANDOMIZED, IN_PROGRESS, COMPLETED, EXCLUDED
    is_pilot = Column(Boolean, default=False, nullable=False)
    ip_hash = Column(String(64), default=generate_ip_hash, nullable=False, index=True) # Salted hash for temporary duplicate check

    consent_log = relationship("ConsentLog", back_populates="participant", uselist=False)
    screening_log = relationship("ScreeningLog", back_populates="participant", uselist=False)
    language_bg = relationship("LanguageBackground", back_populates="participant", uselist=False)
    ai_literacy = relationship("AILiteracy", back_populates="participant", uselist=False)
    randomization = relationship("RandomizationAllocation", back_populates="participant", uselist=False)
    task_sessions = relationship("TaskSession", back_populates="participant")
    telemetry_events = relationship("TelemetryEvent", back_populates="participant")

class ConsentLog(Base):
    __tablename__ = "consent_logs"

    consent_id = Column(Integer, primary_key=True, autoincrement=True)
    participant_id = Column(String(64), ForeignKey("participants.participant_id"), nullable=False, unique=True)
    agreed_to_terms = Column(Boolean, nullable=False)
    confirmed_age_residency = Column(Boolean, nullable=False)
    consent_timestamp = Column(DateTime, default=lambda: datetime.datetime.now(datetime.UTC), nullable=False)

    participant = relationship("Participant", back_populates="consent_log")

class ScreeningLog(Base):
    __tablename__ = "screening_logs"

    screening_id = Column(Integer, primary_key=True, autoincrement=True)
    participant_id = Column(String(64), ForeignKey("participants.participant_id"), nullable=False, unique=True)
    score_english = Column(Integer, nullable=False) # out of 3
    score_hindi = Column(Integer, nullable=False)   # out of 3
    passed = Column(Boolean, nullable=False)
    raw_responses = Column(JSON, nullable=False)
    completed_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.UTC), nullable=False)

    participant = relationship("Participant", back_populates="screening_log")

class LanguageBackground(Base):
    __tablename__ = "language_background"

    bg_id = Column(Integer, primary_key=True, autoincrement=True)
    participant_id = Column(String(64), ForeignKey("participants.participant_id"), nullable=False, unique=True)
    aoa_english = Column(Integer, nullable=False)
    aoa_hindi = Column(Integer, nullable=False)
    primary_home_lang = Column(String(64), nullable=False)
    medium_instruction_school = Column(String(64), nullable=False)
    medium_instruction_higher = Column(String(64), nullable=False)
    self_read_en = Column(Integer, nullable=False)
    self_write_en = Column(Integer, nullable=False)
    self_speak_en = Column(Integer, nullable=False)
    self_read_hi = Column(Integer, nullable=False)
    self_write_hi = Column(Integer, nullable=False)
    self_speak_hi = Column(Integer, nullable=False)
    freq_daily_en = Column(Float, nullable=False)
    freq_daily_hi = Column(Float, nullable=False)
    freq_daily_cs = Column(Float, nullable=False)
    ai_use_en = Column(Float, nullable=False)
    ai_use_hi = Column(Float, nullable=False)
    ai_use_mixed = Column(Float, nullable=False)
    completed_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.UTC), nullable=False)

    participant = relationship("Participant", back_populates="language_bg")

class AILiteracy(Base):
    __tablename__ = "ai_literacy"

    ails_id = Column(Integer, primary_key=True, autoincrement=True)
    participant_id = Column(String(64), ForeignKey("participants.participant_id"), nullable=False, unique=True)
    raw_responses = Column(JSON, nullable=False)
    total_score = Column(Integer, nullable=False) # 12 to 60
    stratum = Column(String(16), nullable=False) # LOW or HIGH
    completed_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.UTC), nullable=False)

    participant = relationship("Participant", back_populates="ai_literacy")

class RandomizationAllocation(Base):
    __tablename__ = "randomization_allocations"

    alloc_id = Column(Integer, primary_key=True, autoincrement=True)
    participant_id = Column(String(64), ForeignKey("participants.participant_id"), nullable=False, unique=True)
    stratum = Column(String(16), nullable=False) # LOW or HIGH
    block_id = Column(Integer, nullable=False)
    block_size = Column(Integer, nullable=False) # 3 or 6
    assigned_arm = Column(String(32), nullable=False) # ENGLISH_ONLY, HINDI_ONLY, CODE_SWITCHING
    allocated_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.UTC), nullable=False)

    participant = relationship("Participant", back_populates="randomization")

class TaskSession(Base):
    __tablename__ = "task_sessions"

    session_id = Column(Integer, primary_key=True, autoincrement=True)
    participant_id = Column(String(64), ForeignKey("participants.participant_id"), nullable=False)
    task_id = Column(String(32), nullable=False) # PMEGP, PM_VISHWAKARMA, PM_SVANIDHI
    position = Column(Integer, nullable=False) # 1, 2, or 3
    order_id = Column(Integer, nullable=False) # 1, 2, or 3 (Latin Square Order)
    status = Column(String(32), default="STARTED", nullable=False) # STARTED, COMPLETED, TIMED_OUT
    started_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.UTC), nullable=False)
    completed_at = Column(DateTime, nullable=True)

    participant = relationship("Participant", back_populates="task_sessions")
    messages = relationship("Message", back_populates="task_session")
    final_decision = relationship("FinalDecision", back_populates="task_session", uselist=False)

class Message(Base):
    __tablename__ = "messages"

    message_id = Column(Integer, primary_key=True, autoincrement=True)
    task_session_id = Column(Integer, ForeignKey("task_sessions.session_id"), nullable=False)
    participant_id = Column(String(64), ForeignKey("participants.participant_id"), nullable=False)
    task_id = Column(String(32), nullable=False)
    sender = Column(String(16), nullable=False) # USER, AI
    message_text = Column(Text, nullable=False)
    tokens_used = Column(Integer, nullable=True)
    latency_ms = Column(Integer, nullable=True)
    language_leakage_flag = Column(Boolean, default=False, nullable=False)
    is_mock = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.UTC), nullable=False)

    task_session = relationship("TaskSession", back_populates="messages")

class TelemetryEvent(Base):
    __tablename__ = "telemetry_events"

    event_id = Column(Integer, primary_key=True, autoincrement=True)
    participant_id = Column(String(64), ForeignKey("participants.participant_id"), nullable=False)
    task_id = Column(String(32), nullable=True)
    timestamp = Column(DateTime, nullable=False)
    event_type = Column(String(64), nullable=False)
    event_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.datetime.now(datetime.UTC), nullable=False)

    participant = relationship("Participant", back_populates="telemetry_events")

class FinalDecision(Base):
    __tablename__ = "final_decisions"

    decision_id = Column(Integer, primary_key=True, autoincrement=True)
    task_session_id = Column(Integer, ForeignKey("task_sessions.session_id"), nullable=False, unique=True)
    participant_id = Column(String(64), ForeignKey("participants.participant_id"), nullable=False)
    task_id = Column(String(32), nullable=False)
    submitted_answers = Column(JSON, nullable=False)
    confidence_score = Column(Integer, nullable=False) # 1 to 7 Likert
    calculated_score = Column(Float, nullable=False) # 0.0 to 10.0
    score_breakdown = Column(JSON, nullable=False)
    submitted_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    task_session = relationship("TaskSession", back_populates="final_decision")

class PostTaskMeasure(Base):
    __tablename__ = "post_task_measures"

    measure_id = Column(Integer, primary_key=True, autoincrement=True)
    participant_id = Column(String(64), ForeignKey("participants.participant_id"), nullable=False, unique=True)
    nasa_tlx_raw = Column(JSON, nullable=False) # 6 items 1-20
    tlx_composite_score = Column(Float, nullable=False)
    feedback_comments = Column(Text, nullable=True)
    submitted_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

class TechnicalError(Base):
    __tablename__ = "technical_errors"

    error_id = Column(Integer, primary_key=True, autoincrement=True)
    participant_id = Column(String(64), nullable=True)
    task_id = Column(String(32), nullable=True)
    error_type = Column(String(64), nullable=False)
    error_message = Column(Text, nullable=False)
    context_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

Index("idx_telemetry_participant", TelemetryEvent.participant_id)
Index("idx_messages_session", Message.task_session_id)
