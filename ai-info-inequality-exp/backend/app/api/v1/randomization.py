from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.randomization.engine import RandomizationEngine

router = APIRouter(prefix="/randomization", tags=["Randomization"])

class RandomizeRequest(BaseModel):
    participant_id: str

@router.post("/allocate")
def allocate_participant(req: RandomizeRequest, db: Session = Depends(get_db)):
    randomizer = RandomizationEngine(db)
    
    is_eligible, msg = randomizer.verify_eligibility_for_randomization(req.participant_id)
    if not is_eligible:
        raise HTTPException(status_code=400, detail=msg)

    try:
        allocation = randomizer.allocate_participant(req.participant_id)
        return {
            "participant_id": req.participant_id,
            "stratum": allocation.stratum,
            "assigned_arm": allocation.assigned_arm,
            "allocated_at": allocation.allocated_at
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Randomization error: {str(e)}")
