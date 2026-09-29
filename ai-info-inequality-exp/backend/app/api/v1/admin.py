from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Participant, TaskSession, TelemetryEvent, Message
from app.core.auth import require_admin_auth
from app.config import settings

router = APIRouter(prefix="/admin", tags=["Admin"], dependencies=[Depends(require_admin_auth)])

@router.get("/health")
def admin_health(db: Session = Depends(get_db)):
    """Administrative health check returning system parameters."""
    participant_count = db.query(Participant).count()
    session_count = db.query(TaskSession).count()
    
    return {
        "status": "HEALTHY",
        "app_env": settings.APP_ENV,
        "llm_enabled": settings.LLM_ENABLED,
        "use_mock_llm": settings.USE_MOCK_LLM,
        "stats": {
            "total_participants": participant_count,
            "total_task_sessions": session_count
        }
    }

@router.get("/export/summary")
def admin_export_summary(db: Session = Depends(get_db)):
    """Administrative summary export of completed participant sessions."""
    completed = db.query(Participant).filter(Participant.status == "DEBRIEFED").count()
    in_progress = db.query(Participant).filter(Participant.status != "DEBRIEFED").count()
    
    return {
        "completed_sessions": completed,
        "in_progress_sessions": in_progress,
        "telemetry_events_count": db.query(TelemetryEvent).count(),
        "total_messages": db.query(Message).count()
    }
