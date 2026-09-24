import datetime
import pytest
from app.db.models import TelemetryEvent

def test_telemetry_event_logging(db, fully_eligible_participant):
    event = TelemetryEvent(
        participant_id=fully_eligible_participant.participant_id,
        task_id="PMEGP",
        timestamp=datetime.datetime.utcnow(),
        event_type="TAB_FOCUS_CHANGED",
        event_data={"focused": False, "dwell_time_ms": 1240}
    )
    db.add(event)
    db.commit()

    saved = db.query(TelemetryEvent).filter(TelemetryEvent.participant_id == fully_eligible_participant.participant_id).first()
    assert saved is not None
    assert saved.event_type == "TAB_FOCUS_CHANGED"
    # Verify event classification remains exploratory focus metadata, not web search
    assert "focused" in saved.event_data
