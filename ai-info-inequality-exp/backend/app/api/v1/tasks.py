import random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict, Any, List
from app.db.session import get_db
from app.db.models import Participant, TaskSession, FinalDecision
from app.scoring.engine import ScoringEngine

router = APIRouter(prefix="/tasks", tags=["Tasks"])

LATIN_SQUARES = {
    1: ["PMEGP", "PM_VISHWAKARMA", "PM_SVANIDHI"],
    2: ["PM_VISHWAKARMA", "PM_SVANIDHI", "PMEGP"],
    3: ["PM_SVANIDHI", "PMEGP", "PM_VISHWAKARMA"]
}

class InitializeTasksRequest(BaseModel):
    participant_id: str

class DecisionSubmitRequest(BaseModel):
    participant_id: str
    task_id: str
    submitted_answers: Dict[str, Any]
    confidence_score: int # 1 to 7

@router.post("/initialize")
def initialize_tasks(req: InitializeTasksRequest, db: Session = Depends(get_db)):
    participant = db.query(Participant).filter(Participant.participant_id == req.participant_id).first()
    if not participant or not participant.randomization:
        raise HTTPException(status_code=400, detail="Participant must be randomized before initializing tasks.")

    existing_tasks = db.query(TaskSession).filter(TaskSession.participant_id == req.participant_id).all()
    if existing_tasks:
        return {"status": "ALREADY_INITIALIZED", "count": len(existing_tasks)}

    # Select Latin Square Order balanced across participant IDs
    order_id = (hash(req.participant_id) % 3) + 1
    scenario_order = LATIN_SQUARES[order_id]

    created_sessions = []
    for pos, task_id in enumerate(scenario_order, start=1):
        ts = TaskSession(
            participant_id=req.participant_id,
            task_id=task_id,
            position=pos,
            order_id=order_id,
            status="STARTED" if pos == 1 else "PENDING"
        )
        db.add(ts)
        created_sessions.append(ts)

    participant.status = "IN_PROGRESS"
    db.commit()

    return {"status": "INITIALIZED", "order_id": order_id, "tasks": [t.task_id for t in created_sessions]}

@router.get("/scenario/{task_id}")
def get_scenario_details(task_id: str):
    try:
        rubric_data = ScoringEngine.load_rubric(task_id)
        # Exclude ground truth answer keys from frontend payload
        return {
            "task_id": rubric_data["task_id"],
            "name": rubric_data["name"],
            "domain": rubric_data["domain"],
            "persona": rubric_data["persona"],
            "official_sources": rubric_data["official_sources"]
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Scenario not found: {str(e)}")

@router.post("/decision/submit")
def submit_final_decision(req: DecisionSubmitRequest, db: Session = Depends(get_db)):
    participant = db.query(Participant).filter(Participant.participant_id == req.participant_id).first()
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found.")

    task_session = (
        db.query(TaskSession)
        .filter(TaskSession.participant_id == req.participant_id, TaskSession.task_id == req.task_id)
        .first()
    )
    if not task_session:
        raise HTTPException(status_code=404, detail="Task session not found.")

    if task_session.status == "COMPLETED":
        raise HTTPException(status_code=400, detail="Decision already submitted for this task.")

    # Compute score deterministically using server-side ScoringEngine
    total_score, breakdown = ScoringEngine.score_decision(req.task_id, req.submitted_answers)

    decision = FinalDecision(
        task_session_id=task_session.session_id,
        participant_id=req.participant_id,
        task_id=req.task_id,
        submitted_answers=req.submitted_answers,
        confidence_score=req.confidence_score,
        calculated_score=total_score,
        score_breakdown=breakdown
    )
    db.add(decision)

    task_session.status = "COMPLETED"

    # Unlock next task if available
    next_task = (
        db.query(TaskSession)
        .filter(TaskSession.participant_id == req.participant_id, TaskSession.position == task_session.position + 1)
        .first()
    )
    if next_task:
        next_task.status = "STARTED"

    db.commit()

    return {
        "participant_id": req.participant_id,
        "task_id": req.task_id,
        "score_calculated": True,
        "next_position": next_task.position if next_task else None,
        "all_tasks_completed": next_task is None
    }
