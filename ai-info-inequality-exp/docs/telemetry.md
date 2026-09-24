# Telemetry Logging Documentation

Telemetry events follow a structured JSON schema:
```json
{
  "participant_id": "p_...",
  "task_id": "PMEGP",
  "timestamp": "2026-09-24T10:00:00.000Z",
  "event_type": "EVENT_NAME",
  "event_data": {}
}
```

## Tracked Events
- `SCREEN_STARTED` / `SCREEN_COMPLETED`
- `TASK_STARTED` / `TASK_COMPLETED`
- `PROMPT_SUBMITTED` / `AI_RESPONSE_RECEIVED`
- `LINK_CLICKED` / `DOCUMENT_OPENED` / `DOC_VIEW_TIME` (Secondary outcome: direct interface verification action rate)
- `TAB_FOCUS_CHANGED` (Exploratory telemetry: off-screen focus time. MUST NOT be labeled as external web searching)
- `FINAL_DECISION_SUBMITTED`
- `TECHNICAL_ERROR`
