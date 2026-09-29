from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict, Optional
from app.db.session import get_db
from app.db.models import Participant, TaskSession, PostTaskMeasure

router = APIRouter(prefix="/post-task", tags=["Post-Task"])

class PostTaskSubmitRequest(BaseModel):
    participant_id: str
    task_session_id: int
    task_id: str
    nasa_tlx_raw: Dict[str, int] # 6 items 1-20: mental_demand, physical_demand, temporal_demand, performance, effort, frustration
    feedback_comments: Optional[str] = None

@router.post("/submit")
def submit_post_task_measures(req: PostTaskSubmitRequest, db: Session = Depends(get_db)):
    participant = db.query(Participant).filter(Participant.participant_id == req.participant_id).first()
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found.")

    task_session = db.query(TaskSession).filter(TaskSession.session_id == req.task_session_id).first()
    if not task_session:
        raise HTTPException(status_code=404, detail="Task session not found.")

    if task_session.participant_id != req.participant_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Task session does not belong to the specified participant."
        )

    if len(req.nasa_tlx_raw) != 6:
        raise HTTPException(status_code=400, detail="NASA-TLX requires ratings for all 6 items.")

    existing_measure = db.query(PostTaskMeasure).filter(PostTaskMeasure.task_session_id == req.task_session_id).first()
    if existing_measure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Post-task measure already submitted for this task session."
        )

    composite_score = sum(req.nasa_tlx_raw.values()) / 6.0

    post_measure = PostTaskMeasure(
        participant_id=req.participant_id,
        task_session_id=req.task_session_id,
        task_id=req.task_id,
        nasa_tlx_raw=req.nasa_tlx_raw,
        tlx_composite_score=composite_score,
        feedback_comments=req.feedback_comments
    )
    db.add(post_measure)

    # Check if all 3 task sessions are completed and have post-task measures submitted
    total_sessions = db.query(TaskSession).filter(TaskSession.participant_id == req.participant_id).count()
    completed_measures = (
        db.query(PostTaskMeasure)
        .filter(PostTaskMeasure.participant_id == req.participant_id)
        .count()
    )

    if total_sessions >= 3 and (completed_measures + 1) >= total_sessions:
        participant.status = "COMPLETED"

    db.commit()

    return {
        "participant_id": req.participant_id,
        "task_session_id": req.task_session_id,
        "task_id": req.task_id,
        "tlx_composite_score": composite_score,
        "status": participant.status
    }
