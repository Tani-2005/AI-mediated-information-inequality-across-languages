from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict
from app.db.session import get_db
from app.db.models import Participant, AILiteracy
from app.randomization.engine import RandomizationEngine

router = APIRouter(prefix="/ai-literacy", tags=["AILS"])

class AILiteracySubmitRequest(BaseModel):
    participant_id: str
    responses: Dict[str, int] # 12 items, ratings 1-5

@router.post("/submit")
def submit_ai_literacy(req: AILiteracySubmitRequest, db: Session = Depends(get_db)):
    participant = db.query(Participant).filter(Participant.participant_id == req.participant_id).first()
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found.")

    if not participant.language_bg:
        raise HTTPException(status_code=400, detail="Must complete language background before AILS.")

    if len(req.responses) != 12:
        raise HTTPException(status_code=400, detail="AILS requires responses for all 12 items.")

    total_score = sum(req.responses.values())
    
    randomizer = RandomizationEngine(db)
    stratum = randomizer.get_stratum(total_score)

    ails_record = db.query(AILiteracy).filter(AILiteracy.participant_id == req.participant_id).first()
    if not ails_record:
        ails_record = AILiteracy(
            participant_id=req.participant_id,
            raw_responses=req.responses,
            total_score=total_score,
            stratum=stratum
        )
        db.add(ails_record)

    participant.status = "BASELINE_DONE"
    db.commit()

    return {
        "participant_id": req.participant_id,
        "total_score": total_score,
        "stratum": stratum,
        "status": participant.status
    }
