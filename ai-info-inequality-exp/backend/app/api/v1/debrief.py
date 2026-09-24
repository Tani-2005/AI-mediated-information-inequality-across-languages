import hashlib
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.db.models import Participant

router = APIRouter(prefix="/debrief", tags=["Debrief"])

class DebriefCompleteRequest(BaseModel):
    participant_id: str

@router.post("/complete")
def complete_session(req: DebriefCompleteRequest, db: Session = Depends(get_db)):
    participant = db.query(Participant).filter(Participant.participant_id == req.participant_id).first()
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found.")

    # Generate completion verification code
    completion_code = f"COMP-{hashlib.sha256(req.participant_id.encode()).hexdigest()[:8].upper()}"

    participant.status = "COMPLETED"
    db.commit()

    return {
        "participant_id": req.participant_id,
        "completion_code": completion_code,
        "status": "COMPLETED",
        "debrief_statement": "Thank you for participating in this research study investigating AI-mediated information seeking across languages."
    }
