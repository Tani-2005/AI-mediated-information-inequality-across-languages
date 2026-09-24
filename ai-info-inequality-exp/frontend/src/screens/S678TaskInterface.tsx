import React, { useState, useEffect } from 'react';
import { ScenarioDetails, ChatMessage } from '../types';
import { getScenarioDetails, sendChatMessage, submitTaskDecision, logTelemetryEvent } from '../services/api';

interface Props {
  participantId: string;
  taskId: string;
  position: number;
  assignedArm: string;
  onTaskCompleted: (allDone: boolean) => void;
}

export const S678TaskInterface: React.FC<Props> = ({
  participantId,
  taskId,
  position,
  assignedArm,
  onTaskCompleted,
}) => {
  const [scenario, setScenario] = useState<ScenarioDetails | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [prompt, setPrompt] = useState('');
  const [sending, setSending] = useState(false);

  // Form states
  const [isEligible, setIsEligible] = useState<boolean>(true);
  const [numField1, setNumField1] = useState<string>('');
  const [numField2, setNumField2] = useState<string>('');
  const [selectedDocs, setSelectedDocs] = useState<string[]>([]);
  const [confidenceScore, setConfidenceScore] = useState<number>(5);

  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getScenarioDetails(taskId).then((data) => {
      setScenario(data);
    });

    logTelemetryEvent(participantId, taskId, 'TASK_STARTED', {
      position,
      assigned_arm: assignedArm,
    });
  }, [taskId, participantId, position, assignedArm]);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim() || sending) return;

    const userText = prompt.trim();
    setPrompt('');
    setSending(true);

    const userMsg: ChatMessage = { sender: 'USER', text: userText, timestamp: new Date().toLocaleTimeString() };
    setMessages((prev) => [...prev, userMsg]);

    logTelemetryEvent(participantId, taskId, 'PROMPT_SUBMITTED', { prompt_text: userText });

    try {
      const res = await sendChatMessage(participantId, taskId, userText);
      const aiMsg: ChatMessage = { sender: 'AI', text: res.reply, timestamp: new Date().toLocaleTimeString() };
      setMessages((prev) => [...prev, aiMsg]);
      logTelemetryEvent(participantId, taskId, 'AI_RESPONSE_RECEIVED', { response_text: res.reply });
    } catch (err: any) {
      setError(err.message || 'Failed to send chat message.');
    } finally {
      setSending(false);
    }
  };

  const handleLinkClick = (title: string, url: string) => {
    logTelemetryEvent(participantId, taskId, 'LINK_CLICKED', { title, url });
    logTelemetryEvent(participantId, taskId, 'DOCUMENT_OPENED', { title, url });
    window.open(url, '_blank');
  };

  const handleDocToggle = (docId: string) => {
    setSelectedDocs((prev) =>
      prev.includes(docId) ? prev.filter((d) => d !== docId) : [...prev, docId]
    );
  };

  const handleFormSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);

    let submittedAnswers: any = { is_eligible: isEligible };

    if (taskId === 'PMEGP') {
      submittedAnswers.max_project_cost_lakhs = parseFloat(numField1) || 0;
      submittedAnswers.subsidy_percentage = parseFloat(numField2) || 0;
      submittedAnswers.mandatory_documents = selectedDocs;
    } else if (taskId === 'PM_VISHWAKARMA') {
      submittedAnswers.first_tranche_loan_inr = parseFloat(numField1) || 0;
      submittedAnswers.skill_stipend_per_day_inr = parseFloat(numField2) || 0;
      submittedAnswers.toolkit_incentive_grant_inr = 15000;
    } else if (taskId === 'PM_SVANIDHI') {
      submittedAnswers.first_tranche_loan_inr = parseFloat(numField1) || 0;
      submittedAnswers.interest_subsidy_percentage = parseFloat(numField2) || 0;
      submittedAnswers.max_annual_cashback_inr = 1200;
    }

    try {
      const res = await submitTaskDecision(participantId, taskId, submittedAnswers, confidenceScore);
      logTelemetryEvent(participantId, taskId, 'FINAL_DECISION_SUBMITTED', {
        submitted_answers: submittedAnswers,
        confidence_score: confidenceScore,
      });

      onTaskCompleted(res.all_tasks_completed);
    } catch (err: any) {
      setError(err.message || 'Failed to submit task decision.');
      setSubmitting(false);
    }
  };

  if (!scenario) {
    return <div className="p-8 text-center text-slate-400">Loading task scenario...</div>;
  }

  return (
    <div className="max-w-7xl mx-auto p-4 space-y-4">
      {/* HEADER */}
      <div className="flex flex-wrap items-center justify-between p-4 bg-slate-800 rounded-lg border border-slate-700">
        <div>
          <span className="text-xs text-slate-400 uppercase tracking-wider">Task {position} of 3</span>
          <h2 className="text-xl font-bold text-sky-400">{scenario.name}</h2>
        </div>
        <div className="text-xs text-slate-300 bg-slate-900 px-3 py-1.5 rounded border border-slate-700">
          Condition: <strong className="text-emerald-400">{assignedArm}</strong>
        </div>
      </div>

      {/* SPLIT PANE WORKSPACE */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* LEFT PANE: PERSONA & SOURCES (5 cols) */}
        <div className="lg:col-span-5 space-y-4">
          <div className="p-5 bg-slate-800 rounded-xl border border-slate-700 shadow-lg space-y-3">
            <h3 className="font-semibold text-slate-100 flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span> Persona Card
            </h3>
            <div className="p-4 bg-slate-900 rounded-lg text-sm text-slate-300 space-y-2 border border-slate-800">
              <p><strong>Name:</strong> {scenario.persona.name}</p>
              <p><strong>Age:</strong> {scenario.persona.age} | <strong>Gender:</strong> {scenario.persona.gender}</p>
              <p><strong>Location:</strong> {scenario.persona.location}</p>
              <p className="pt-2 text-slate-200">{scenario.persona.background_summary}</p>
            </div>
          </div>

          <div className="p-5 bg-slate-800 rounded-xl border border-slate-700 shadow-lg space-y-3">
            <h3 className="font-semibold text-slate-100 flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-sky-500"></span> Official Guidelines Reference Links
            </h3>
            <div className="space-y-2">
              {scenario.official_sources.map((src, i) => (
                <button
                  key={i}
                  onClick={() => handleLinkClick(src.title, src.url)}
                  className="w-full text-left p-3 bg-slate-900 hover:bg-slate-950 text-xs text-sky-400 border border-slate-700 rounded-lg flex items-center justify-between transition"
                >
                  <span>{src.title}</span>
                  <span className="text-slate-500">↗</span>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* RIGHT PANE: CHAT & FINAL DECISION FORM (7 cols) */}
        <div className="lg:col-span-7 space-y-4">
          {/* AI CHAT ASSISTANT */}
          <div className="p-5 bg-slate-800 rounded-xl border border-slate-700 shadow-lg flex flex-col h-[420px]">
            <h3 className="font-semibold text-slate-100 mb-2 flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-amber-500"></span> AI Assistant Chatbot
            </h3>

            <div className="flex-1 overflow-y-auto p-4 bg-slate-900 rounded-lg space-y-3 border border-slate-800 text-sm">
              {messages.length === 0 && (
                <p className="text-slate-500 text-xs text-center pt-8">
                  Ask the AI assistant any question regarding eligibility rules, project costs, subsidies, or required documents.
                </p>
              )}
              {messages.map((m, i) => (
                <div key={i} className={`flex ${m.sender === 'USER' ? 'justify-end' : 'justify-start'}`}>
                  <div
                    className={`max-w-[85%] p-3 rounded-xl text-xs leading-relaxed ${
                      m.sender === 'USER'
                        ? 'bg-sky-600 text-white rounded-br-none'
                        : 'bg-slate-800 text-slate-200 border border-slate-700 rounded-bl-none'
                    }`}
                  >
                    <p>{m.text}</p>
                    <span className="text-[10px] text-slate-400 block text-right mt-1">{m.timestamp}</span>
                  </div>
                </div>
              ))}
            </div>

            <form onSubmit={handleSendMessage} className="mt-3 flex gap-2">
              <input
                type="text"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Type prompt here..."
                disabled={sending}
                className="flex-1 p-2 bg-slate-900 border border-slate-700 rounded-lg text-sm text-white focus:outline-none focus:border-sky-500"
              />
              <button
                type="submit"
                disabled={sending || !prompt.trim()}
                className="px-4 py-2 bg-sky-600 hover:bg-sky-500 disabled:bg-slate-700 text-white text-sm font-medium rounded-lg transition"
              >
                {sending ? '...' : 'Send'}
              </button>
            </form>
          </div>

          {/* FINAL DECISION FORM */}
          <div className="p-5 bg-slate-800 rounded-xl border border-slate-700 shadow-lg space-y-4">
            <h3 className="font-semibold text-slate-100 flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-rose-500"></span> Final Decision Form
            </h3>

            {error && <div className="p-2 bg-rose-900/50 text-rose-300 rounded text-xs border border-rose-700">{error}</div>}

            <form onSubmit={handleFormSubmit} className="space-y-4 text-xs text-slate-200">
              <div>
                <label className="block mb-1 font-medium">1. Is the applicant eligible for this scheme?</label>
                <div className="flex gap-4">
                  <label className="flex items-center gap-1.5 cursor-pointer">
                    <input type="radio" name="elig" checked={isEligible === true} onChange={() => setIsEligible(true)} className="accent-sky-500" />
                    <span>Yes, Eligible</span>
                  </label>
                  <label className="flex items-center gap-1.5 cursor-pointer">
                    <input type="radio" name="elig" checked={isEligible === false} onChange={() => setIsEligible(false)} className="accent-sky-500" />
                    <span>No, Ineligible</span>
                  </label>
                </div>
              </div>

              {taskId === 'PMEGP' && (
                <>
                  <div>
                    <label className="block mb-1 font-medium">2. Maximum Project Cost Allowed for Manufacturing (in Lakhs INR):</label>
                    <input
                      type="number"
                      value={numField1}
                      onChange={(e) => setNumField1(e.target.value)}
                      placeholder="e.g. 50"
                      className="w-full p-2 bg-slate-900 border border-slate-700 rounded text-white"
                    />
                  </div>
                  <div>
                    <label className="block mb-1 font-medium">3. Margin Money / Subsidy Percentage (%):</label>
                    <input
                      type="number"
                      value={numField2}
                      onChange={(e) => setNumField2(e.target.value)}
                      placeholder="e.g. 35"
                      className="w-full p-2 bg-slate-900 border border-slate-700 rounded text-white"
                    />
                  </div>
                  <div>
                    <label className="block mb-1 font-medium">4. Mandatory Required Documents:</label>
                    <div className="grid grid-cols-2 gap-2 pt-1">
                      {[
                        { id: 'aadhaar_card', label: 'Aadhaar Card' },
                        { id: 'edp_certificate', label: 'EDP Training Certificate' },
                        { id: 'detailed_project_report', label: 'Detailed Project Report (DPR)' },
                        { id: 'rural_caste_certificate', label: 'Rural/Caste Certificate' },
                      ].map((doc) => (
                        <label key={doc.id} className="flex items-center gap-2 cursor-pointer bg-slate-900 p-2 rounded border border-slate-700">
                          <input
                            type="checkbox"
                            checked={selectedDocs.includes(doc.id)}
                            onChange={() => handleDocToggle(doc.id)}
                            className="accent-sky-500"
                          />
                          <span>{doc.label}</span>
                        </label>
                      ))}
                    </div>
                  </div>
                </>
              )}

              {taskId === 'PM_VISHWAKARMA' && (
                <>
                  <div>
                    <label className="block mb-1 font-medium">2. First Tranche Concessional Loan Cap (in INR):</label>
                    <input
                      type="number"
                      value={numField1}
                      onChange={(e) => setNumField1(e.target.value)}
                      placeholder="e.g. 100000"
                      className="w-full p-2 bg-slate-900 border border-slate-700 rounded text-white"
                    />
                  </div>
                  <div>
                    <label className="block mb-1 font-medium">3. Basic Skill Training Stipend Rate (in INR / day):</label>
                    <input
                      type="number"
                      value={numField2}
                      onChange={(e) => setNumField2(e.target.value)}
                      placeholder="e.g. 500"
                      className="w-full p-2 bg-slate-900 border border-slate-700 rounded text-white"
                    />
                  </div>
                </>
              )}

              {taskId === 'PM_SVANIDHI' && (
                <>
                  <div>
                    <label className="block mb-1 font-medium">2. First Tranche Working Capital Loan Limit (in INR):</label>
                    <input
                      type="number"
                      value={numField1}
                      onChange={(e) => setNumField1(e.target.value)}
                      placeholder="e.g. 10000"
                      className="w-full p-2 bg-slate-900 border border-slate-700 rounded text-white"
                    />
                  </div>
                  <div>
                    <label className="block mb-1 font-medium">3. Annual Interest Subsidy Rate (%):</label>
                    <input
                      type="number"
                      value={numField2}
                      onChange={(e) => setNumField2(e.target.value)}
                      placeholder="e.g. 7"
                      className="w-full p-2 bg-slate-900 border border-slate-700 rounded text-white"
                    />
                  </div>
                </>
              )}

              <div className="pt-2">
                <label className="block mb-1 font-medium">Decision Confidence Rating (1 = Low, 7 = High): {confidenceScore}</label>
                <input
                  type="range"
                  min="1"
                  max="7"
                  value={confidenceScore}
                  onChange={(e) => setConfidenceScore(parseInt(e.target.value))}
                  className="w-full accent-sky-500"
                />
              </div>

              <button
                type="submit"
                disabled={submitting}
                className="w-full py-2.5 px-4 bg-emerald-600 hover:bg-emerald-500 disabled:bg-slate-700 text-white font-semibold rounded-lg shadow transition duration-200 mt-2 text-sm"
              >
                {submitting ? 'Evaluating & Submitting...' : 'Submit Final Decision'}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};
