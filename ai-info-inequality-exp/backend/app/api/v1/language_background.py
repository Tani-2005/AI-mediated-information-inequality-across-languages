from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.db.models import Participant, LanguageBackground

router = APIRouter(prefix="/language-background", tags=["LEAP-Q"])

class LEAPQSubmitRequest(BaseModel):
    participant_id: str
    aoa_english: int
    aoa_hindi: int
    primary_home_lang: str
    medium_instruction_school: str
    medium_instruction_higher: str
    self_read_en: int
    self_write_en: int
    self_speak_en: int
    self_read_hi: int
    self_write_hi: int
    self_speak_hi: int
    freq_daily_en: float
    freq_daily_hi: float
    freq_daily_cs: float
    ai_use_en: float
    ai_use_hi: float
    ai_use_mixed: float

@router.post("/submit")
def submit_language_background(req: LEAPQSubmitRequest, db: Session = Depends(get_db)):
    participant = db.query(Participant).filter(Participant.participant_id == req.participant_id).first()
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found.")

    if not participant.screening_log or not participant.screening_log.passed:
        raise HTTPException(status_code=400, detail="Must pass bilingual screening before submitting LEAP-Q.")

    bg = db.query(LanguageBackground).filter(LanguageBackground.participant_id == req.participant_id).first()
    if not bg:
        bg = LanguageBackground(**req.dict())
        db.add(bg)
    
    db.commit()
    return {"status": "SUCCESS", "participant_id": req.participant_id}
