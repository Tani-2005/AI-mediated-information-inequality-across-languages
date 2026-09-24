import hashlib
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.db.models import Participant, TaskSession

router = APIRouter(prefix="/session", tags=["Session"])

class SessionCreateRequest(BaseModel):
    is_pilot: bool = False

class SessionResponse(BaseModel):
    participant_id: str
    status: str
    is_pilot: bool

@router.post("/create", response_model=SessionResponse)
def create_session(req: SessionCreateRequest, request: Request, db: Session = Depends(get_db)):
    client_ip = request.client.host if request.client else "127.0.0.1"
    ip_hash = hashlib.sha256(f"{client_ip}_SALT_2026".encode()).hexdigest()

    participant = Participant(is_pilot=req.is_pilot, ip_hash=ip_hash)
    db.add(participant)
    db.commit()
    db.refresh(participant)

    return SessionResponse(
        participant_id=participant.participant_id,
        status=participant.status,
        is_pilot=participant.is_pilot
    )

@router.get("/{participant_id}")
def get_session_state(participant_id: str, db: Session = Depends(get_db)):
    participant = db.query(Participant).filter(Participant.participant_id == participant_id).first()
    if not participant:
        raise HTTPException(status_code=404, detail="Participant session not found.")

    assigned_arm = participant.randomization.assigned_arm if participant.randomization else None
    
    # Active tasks
    tasks = db.query(TaskSession).filter(TaskSession.participant_id == participant_id).order_by(TaskSession.position.asc()).all()
    task_states = [{"task_id": t.task_id, "position": t.position, "status": t.status} for t in tasks]

    return {
        "participant_id": participant.participant_id,
        "status": participant.status,
        "assigned_arm": assigned_arm,
        "is_pilot": participant.is_pilot,
        "task_states": task_states
    }
