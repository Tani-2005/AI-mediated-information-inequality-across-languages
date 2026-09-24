from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.db.models import Participant, ConsentLog

router = APIRouter(prefix="/consent", tags=["Consent"])

class ConsentSubmitRequest(BaseModel):
    participant_id: str
    agreed_to_terms: bool
    confirmed_age_residency: bool

@router.post("/submit")
def submit_consent(req: ConsentSubmitRequest, db: Session = Depends(get_db)):
    participant = db.query(Participant).filter(Participant.participant_id == req.participant_id).first()
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found.")

    if not req.agreed_to_terms or not req.confirmed_age_residency:
        participant.status = "EXCLUDED"
        db.commit()
        return {"status": "EXCLUDED", "message": "Informed consent was not provided."}

    consent = db.query(ConsentLog).filter(ConsentLog.participant_id == req.participant_id).first()
    if not consent:
        consent = ConsentLog(
            participant_id=req.participant_id,
            agreed_to_terms=req.agreed_to_terms,
            confirmed_age_residency=req.confirmed_age_residency
        )
        db.add(consent)

    participant.status = "CONSENTED"
    db.commit()
    return {"status": "CONSENTED", "participant_id": req.participant_id}
