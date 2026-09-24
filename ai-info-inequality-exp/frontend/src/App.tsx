import React, { useState } from 'react';
import { S1Consent } from './screens/S1Consent';
import { S2Screening } from './screens/S2Screening';
import { S3LanguageBackground } from './screens/S3LanguageBackground';
import { S4AILiteracy } from './screens/S4AILiteracy';
import { S5TaskOnboarding } from './screens/S5TaskOnboarding';
import { S678TaskInterface } from './screens/S678TaskInterface';
import { S9PostTask } from './screens/S9PostTask';
import { S10Debrief } from './screens/S10Debrief';
import { useTelemetry } from './hooks/useTelemetry';
import {
  createSession,
  submitConsent,
  submitScreening,
  submitLanguageBackground,
  submitAILiteracy,
  allocateRandomization,
  initializeTasks,
  submitPostTaskMeasures,
  completeDebrief,
} from './services/api';

export const App: React.FC = () => {
  const [step, setStep] = useState<
    'S1_CONSENT' | 'S2_SCREENING' | 'S3_LEAPQ' | 'S4_AILS' | 'S5_ONBOARDING' | 'S678_TASKS' | 'S9_POST_TASK' | 'S10_DEBRIEF' | 'EXCLUDED'
  >('S1_CONSENT');

  const [participantId, setParticipantId] = useState<string | null>(null);
  const [assignedArm, setAssignedArm] = useState<string>('ENGLISH_ONLY');
  const [taskOrder, setTaskOrder] = useState<string[]>(['PMEGP', 'PM_VISHWAKARMA', 'PM_SVANIDHI']);
  const [currentTaskIndex, setCurrentTaskIndex] = useState<number>(0);

  const currentTaskId = step === 'S678_TASKS' ? taskOrder[currentTaskIndex] : null;

  // Initialize exploratory telemetry tab-focus hook
  useTelemetry(participantId, currentTaskId);

  const handleConsentComplete = (pid: string) => {
    setParticipantId(pid);
    setStep('S2_SCREENING');
  };

  const handleScreeningComplete = (passed: boolean) => {
    if (passed) {
      setStep('S3_LEAPQ');
    } else {
      setStep('EXCLUDED');
    }
  };

  const handleLEAPQComplete = () => {
    setStep('S4_AILS');
  };

  const handleAILSComplete = async (stratum: string) => {
    if (!participantId) return;
    try {
      const randRes = await allocateRandomization(participantId);
      setAssignedArm(randRes.assigned_arm);

      const taskRes = await initializeTasks(participantId);
      if (taskRes.tasks) {
        setTaskOrder(taskRes.tasks);
      }
      setStep('S5_ONBOARDING');
    } catch (err) {
      console.error('Randomization allocation error:', err);
    }
  };

  const handleBeginTasks = () => {
    setCurrentTaskIndex(0);
    setStep('S678_TASKS');
  };

  const handleTaskCompleted = (allDone: boolean) => {
    if (allDone || currentTaskIndex >= taskOrder.length - 1) {
      setStep('S9_POST_TASK');
    } else {
      setCurrentTaskIndex((prev) => prev + 1);
    }
  };

  const handlePostTaskComplete = () => {
    setStep('S10_DEBRIEF');
  };

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 font-sans flex flex-col">
      {/* HEADER BAR */}
      <header className="py-3 px-6 bg-slate-950 border-b border-slate-800 flex justify-between items-center text-xs">
        <span className="font-bold text-sky-400">AI-Mediated Information Seeking RCT (Protocol v1.0.0-frozen)</span>
        {participantId && (
          <span className="text-slate-400 font-mono">
            PID: {participantId.substring(0, 14)}... | Status: <strong className="text-emerald-400">{step}</strong>
          </span>
        )}
      </header>

      {/* MAIN CONTAINER */}
      <main className="flex-1 container mx-auto px-4">
        {step === 'S1_CONSENT' && (
          <S1Consent
            onConsentComplete={handleConsentComplete}
            createSessionFn={createSession}
            submitConsentFn={submitConsent}
          />
        )}

        {step === 'S2_SCREENING' && participantId && (
          <S2Screening
            participantId={participantId}
            onScreeningComplete={handleScreeningComplete}
            submitScreeningFn={submitScreening}
          />
        )}

        {step === 'S3_LEAPQ' && participantId && (
          <S3LanguageBackground
            participantId={participantId}
            onLEAPQComplete={handleLEAPQComplete}
            submitLEAPQFn={submitLanguageBackground}
          />
        )}

        {step === 'S4_AILS' && participantId && (
          <S4AILiteracy
            participantId={participantId}
            onAILSComplete={handleAILSComplete}
            submitAILiteracyFn={submitAILiteracy}
          />
        )}

        {step === 'S5_ONBOARDING' && (
          <S5TaskOnboarding assignedArm={assignedArm} onBeginTasks={handleBeginTasks} />
        )}

        {step === 'S678_TASKS' && participantId && (
          <S678TaskInterface
            participantId={participantId}
            taskId={taskOrder[currentTaskIndex]}
            position={currentTaskIndex + 1}
            assignedArm={assignedArm}
            onTaskCompleted={handleTaskCompleted}
          />
        )}

        {step === 'S9_POST_TASK' && participantId && (
          <S9PostTask
            participantId={participantId}
            onPostTaskComplete={handlePostTaskComplete}
            submitPostTaskFn={submitPostTaskMeasures}
          />
        )}

        {step === 'S10_DEBRIEF' && participantId && (
          <S10Debrief participantId={participantId} completeDebriefFn={completeDebrief} />
        )}

        {step === 'EXCLUDED' && (
          <div className="max-w-md mx-auto p-8 bg-slate-800 rounded-xl border border-rose-800 my-16 text-center space-y-4">
            <h2 className="text-xl font-bold text-rose-400">Screening Disqualification</h2>
            <p className="text-xs text-slate-300">
              Thank you for your time. Based on the criterion-referenced bilingual screening rules, you do not qualify for this specific research study.
            </p>
          </div>
        )}
      </main>
    </div>
  );
};

export default App;
