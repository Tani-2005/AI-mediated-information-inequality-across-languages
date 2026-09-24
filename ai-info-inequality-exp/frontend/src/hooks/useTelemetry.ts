import { useEffect } from 'react';
import { logTelemetryEvent } from '../services/api';

export function useTelemetry(participantId: string | null, taskId: string | null) {
  useEffect(() => {
    if (!participantId) return;

    const handleFocus = () => {
      logTelemetryEvent(participantId, taskId, 'TAB_FOCUS_CHANGED', {
        focused: true,
        note: 'Browser tab gained focus. Exploratory off-screen time logger.',
      });
    };

    const handleBlur = () => {
      logTelemetryEvent(participantId, taskId, 'TAB_FOCUS_CHANGED', {
        focused: false,
        note: 'Browser tab lost focus. Exploratory off-screen time logger.',
      });
    };

    window.addEventListener('focus', handleFocus);
    window.addEventListener('blur', handleBlur);

    return () => {
      window.removeEventListener('focus', handleFocus);
      window.removeEventListener('blur', handleBlur);
    };
  }, [participantId, taskId]);

  const logCustomEvent = (eventType: string, eventData: any) => {
    if (!participantId) return;
    logTelemetryEvent(participantId, taskId, eventType, eventData);
  };

  return { logCustomEvent };
}
