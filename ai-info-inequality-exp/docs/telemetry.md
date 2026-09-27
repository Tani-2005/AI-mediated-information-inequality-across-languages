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

## Tracked Events & Standardized Classification
- `SCREEN_STARTED` / `SCREEN_COMPLETED`: Process flow logging
- `TASK_STARTED` / `TASK_COMPLETED`: Task lifecycle tracking
- `PROMPT_SUBMITTED` / `AI_RESPONSE_RECEIVED`: Interaction tracking
- `LINK_CLICKED` / `DOCUMENT_OPENED` / `DOC_VIEW_TIME` (`DocClicks` / `DocDuration`): **Secondary Outcomes** (Direct interface verification action rate & document inspection time)
- `TAB_FOCUS_CHANGED` (`WindowBlur`): **Exploratory Process Variable** (Off-screen focus/blur dwell time; strictly MUST NOT be classified as external web searching)
- `FINAL_DECISION_SUBMITTED`: Task completion tracking
- `TECHNICAL_ERROR`: System error logging
