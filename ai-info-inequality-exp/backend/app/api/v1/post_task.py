from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict, Optional
from app.db.session import get_db
from app.db.models import Participant, PostTaskMeasure

router = APIRouter(prefix="/post-task", tags=["Post-Task"])

class PostTaskSubmitRequest(BaseModel):
    participant_id: str
    nasa_tlx_raw: Dict[str, int] # 6 items 1-20: mental_demand, physical_demand, temporal_demand, performance, effort, frustration
    feedback_comments: Optional[str] = None

@router.post("/submit")
def submit_post_task_measures(req: PostTaskSubmitRequest, db: Session = Depends(get_db)):
    participant = db.query(Participant).filter(Participant.participant_id == req.participant_id).first()
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found.")

    if len(req.nasa_tlx_raw) != 6:
        raise HTTPException(status_code=400, detail="NASA-TLX requires ratings for all 6 items.")

    composite_score = sum(req.nasa_tlx_raw.values()) / 6.0

    post_measure = db.query(PostTaskMeasure).filter(PostTaskMeasure.participant_id == req.participant_id).first()
    if not post_measure:
        post_measure = PostTaskMeasure(
            participant_id=req.participant_id,
            nasa_tlx_raw=req.nasa_tlx_raw,
            tlx_composite_score=composite_score,
            feedback_comments=req.feedback_comments
        )
        db.add(post_measure)

    participant.status = "COMPLETED"
    db.commit()

    return {
        "participant_id": req.participant_id,
        "tlx_composite_score": composite_score,
        "status": participant.status
    }
