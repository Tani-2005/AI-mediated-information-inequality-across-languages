from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Any
from app.db.session import get_db
from app.db.models import Participant, TaskSession, Message, TelemetryEvent
from app.config import settings
from app.core.llm_gateway import get_llm_provider
from app.scoring.engine import ScoringEngine

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatMessageRequest(BaseModel):
    participant_id: str
    task_id: str
    prompt: str

@router.post("/message")
def send_chat_message(req: ChatMessageRequest, db: Session = Depends(get_db)):
    if not settings.LLM_ENABLED:
        raise HTTPException(status_code=503, detail="LLM system is currently disabled by emergency switch.")

    participant = db.query(Participant).filter(Participant.participant_id == req.participant_id).first()
    if not participant or not participant.randomization:
        raise HTTPException(status_code=400, detail="Participant must be randomized to use chat.")

    task_session = (
        db.query(TaskSession)
        .filter(TaskSession.participant_id == req.participant_id, TaskSession.task_id == req.task_id)
        .first()
    )
    if not task_session:
        raise HTTPException(status_code=404, detail="Task session not found.")

    # Check session API call limit safeguard
    existing_messages_count = (
        db.query(Message)
        .filter(Message.task_session_id == task_session.session_id, Message.sender == "USER")
        .count()
    )
    if existing_messages_count >= settings.MAX_API_CALLS_PER_SESSION:
        raise HTTPException(status_code=429, detail="Maximum session chat prompt limit reached.")

    assigned_arm = participant.randomization.assigned_arm

    # Store USER Message
    user_msg = Message(
        task_session_id=task_session.session_id,
        participant_id=req.participant_id,
        task_id=req.task_id,
        sender="USER",
        message_text=req.prompt,
        is_mock=settings.USE_MOCK_LLM
    )
    db.add(user_msg)
    db.commit()

    # Load conversation history for gateway
    history_msgs = (
        db.query(Message)
        .filter(Message.task_session_id == task_session.session_id)
        .order_by(Message.message_id.asc())
        .all()
    )
    conv_history = []
    for m in history_msgs[:-1]: # exclude latest user prompt
        role = "user" if m.sender == "USER" else "assistant"
        conv_history.append({"role": role, "content": m.message_text})

    # Persona summary (isolated context)
    scenario_data = ScoringEngine.load_rubric(req.task_id)
    persona_summary = scenario_data["persona"]["background_summary"]

    # Generate response via LLM Gateway Provider
    provider = get_llm_provider()
    try:
        llm_out = provider.generate_response(
            task_id=req.task_id,
            assigned_arm=assigned_arm,
            persona_summary=persona_summary,
            user_prompt=req.prompt,
            conversation_history=conv_history
        )
    except Exception as e:
        # Log technical error
        db.add(TelemetryEvent(
            participant_id=req.participant_id,
            task_id=req.task_id,
            timestamp=user_msg.created_at,
            event_type="TECHNICAL_ERROR",
            event_data={"error_type": "LLM_GENERATION_FAILED", "message": str(e)}
        ))
        db.commit()
        raise HTTPException(status_code=502, detail=f"AI service unavailable: {str(e)}")

    reply_text = llm_out["text"]
    tokens_used = llm_out["tokens_used"].get("total_tokens", 0)
    latency_ms = llm_out["latency_ms"]
    leakage_flag = llm_out["language_leakage_flag"]

    ai_msg = Message(
        task_session_id=task_session.session_id,
        participant_id=req.participant_id,
        task_id=req.task_id,
        sender="AI",
        message_text=reply_text,
        tokens_used=tokens_used,
        latency_ms=latency_ms,
        language_leakage_flag=leakage_flag,
        is_mock=llm_out["is_mock"]
    )
    db.add(ai_msg)

    if leakage_flag:
        db.add(TelemetryEvent(
            participant_id=req.participant_id,
            task_id=req.task_id,
            timestamp=ai_msg.created_at,
            event_type="LANGUAGE_LEAKAGE_DETECTED",
            event_data={
                "message_id": ai_msg.message_id,
                "assigned_arm": assigned_arm,
                "text_snippet": reply_text[:100]
            }
        ))

    db.commit()

    return {
        "participant_id": req.participant_id,
        "task_id": req.task_id,
        "assigned_arm": assigned_arm,
        "reply": reply_text,
        "is_mock": llm_out["is_mock"],
        "language_leakage_flag": leakage_flag,
        "model_snapshot": llm_out["model_snapshot"]
    }
