from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict
from app.db.session import get_db
from app.db.models import Participant, ScreeningLog

router = APIRouter(prefix="/screening", tags=["Screening"])

ENGLISH_ANSWER_KEY = {"q1": "B", "q2": "A", "q3": "C"}
HINDI_ANSWER_KEY = {"q4": "A", "q5": "C", "q6": "B"}

class ScreeningSubmitRequest(BaseModel):
    participant_id: str
    responses: Dict[str, str] # {"q1": "B", "q2": "A", ...}

@router.post("/submit")
def submit_screening(req: ScreeningSubmitRequest, db: Session = Depends(get_db)):
    participant = db.query(Participant).filter(Participant.participant_id == req.participant_id).first()
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found.")

    score_en = 0
    for q_id, ans in ENGLISH_ANSWER_KEY.items():
        if req.responses.get(q_id) == ans:
            score_en += 1

    score_hi = 0
    for q_id, ans in HINDI_ANSWER_KEY.items():
        if req.responses.get(q_id) == ans:
            score_hi += 1

    # Pass rule: >= 2/3 on BOTH sub-tests
    passed = (score_en >= 2) and (score_hi >= 2)

    screening = db.query(ScreeningLog).filter(ScreeningLog.participant_id == req.participant_id).first()
    if not screening:
        screening = ScreeningLog(
            participant_id=req.participant_id,
            score_english=score_en,
            score_hindi=score_hi,
            passed=passed,
            raw_responses=req.responses
        )
        db.add(screening)
    else:
        screening.score_english = score_en
        screening.score_hindi = score_hi
        screening.passed = passed
        screening.raw_responses = req.responses

    if passed:
        participant.status = "SCREENED"
    else:
        participant.status = "EXCLUDED"

    db.commit()

    return {
        "participant_id": req.participant_id,
        "passed": passed,
        "score_english": score_en,
        "score_hindi": score_hi,
        "status": participant.status
    }
