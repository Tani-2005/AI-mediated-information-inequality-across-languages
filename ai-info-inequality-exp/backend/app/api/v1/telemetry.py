import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict, Any, Optional
from app.db.session import get_db
from app.db.models import Participant, TelemetryEvent

router = APIRouter(prefix="/telemetry", tags=["Telemetry"])

class TelemetryEventRequest(BaseModel):
    participant_id: str
    task_id: Optional[str] = None
    timestamp: datetime.datetime
    event_type: str
    event_data: Dict[str, Any]

@router.post("/event")
def log_telemetry_event(req: TelemetryEventRequest, db: Session = Depends(get_db)):
    participant = db.query(Participant).filter(Participant.participant_id == req.participant_id).first()
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found.")

    event = TelemetryEvent(
        participant_id=req.participant_id,
        task_id=req.task_id,
        timestamp=req.timestamp,
        event_type=req.event_type,
        event_data=req.event_data
    )
    db.add(event)
    db.commit()

    return {"status": "LOGGED", "event_id": event.event_id}
