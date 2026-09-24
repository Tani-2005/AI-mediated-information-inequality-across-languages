const API_BASE = '/api/v1';

export async function createSession(isPilot: boolean = false) {
  const res = await fetch(`${API_BASE}/session/create`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ is_pilot: isPilot }),
  });
  return res.json();
}

export async function submitConsent(participantId: string, agreedTerms: boolean, confirmedAge: boolean) {
  const res = await fetch(`${API_BASE}/consent/submit`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      participant_id: participantId,
      agreed_to_terms: agreedTerms,
      confirmed_age_residency: confirmedAge,
    }),
  });
  return res.json();
}

export async function submitScreening(participantId: string, responses: Record<string, string>) {
  const res = await fetch(`${API_BASE}/screening/submit`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      participant_id: participantId,
      responses,
    }),
  });
  return res.json();
}

export async function submitLanguageBackground(participantId: string, data: any) {
  const res = await fetch(`${API_BASE}/language-background/submit`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ participant_id: participantId, ...data }),
  });
  return res.json();
}

export async function submitAILiteracy(participantId: string, responses: Record<string, number>) {
  const res = await fetch(`${API_BASE}/ai-literacy/submit`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ participant_id: participantId, responses }),
  });
  return res.json();
}

export async function allocateRandomization(participantId: string) {
  const res = await fetch(`${API_BASE}/randomization/allocate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ participant_id: participantId }),
  });
  return res.json();
}

export async function initializeTasks(participantId: string) {
  const res = await fetch(`${API_BASE}/tasks/initialize`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ participant_id: participantId }),
  });
  return res.json();
}

export async function getScenarioDetails(taskId: string) {
  const res = await fetch(`${API_BASE}/tasks/scenario/${taskId}`);
  return res.json();
}

export async function sendChatMessage(participantId: string, taskId: string, prompt: string) {
  const res = await fetch(`${API_BASE}/chat/message`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ participant_id: participantId, task_id: taskId, prompt }),
  });
  return res.json();
}

export async function submitTaskDecision(participantId: string, taskId: string, submittedAnswers: any, confidenceScore: number) {
  const res = await fetch(`${API_BASE}/tasks/decision/submit`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      participant_id: participantId,
      task_id: taskId,
      submitted_answers: submittedAnswers,
      confidence_score: confidenceScore,
    }),
  });
  return res.json();
}

export async function logTelemetryEvent(participantId: string, taskId: string | null, eventType: string, eventData: any) {
  try {
    await fetch(`${API_BASE}/telemetry/event`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        participant_id: participantId,
        task_id: taskId,
        timestamp: new Date().toISOString(),
        event_type: eventType,
        event_data: eventData,
      }),
    });
  } catch (err) {
    console.error('Telemetry send error:', err);
  }
}

export async function submitPostTaskMeasures(participantId: string, nasaTlxRaw: Record<string, number>, comments?: string) {
  const res = await fetch(`${API_BASE}/post-task/submit`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      participant_id: participantId,
      nasa_tlx_raw: nasaTlxRaw,
      feedback_comments: comments,
    }),
  });
  return res.json();
}

export async function completeDebrief(participantId: string) {
  const res = await fetch(`${API_BASE}/debrief/complete`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ participant_id: participantId }),
  });
  return res.json();
}
