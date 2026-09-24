import React from 'react';

interface Props {
  assignedArm: string;
  onBeginTasks: () => void;
}

export const S5TaskOnboarding: React.FC<Props> = ({ assignedArm, onBeginTasks }) => {
  return (
    <div className="max-w-3xl mx-auto p-6 bg-slate-800 rounded-xl shadow-2xl border border-slate-700 my-8 space-y-6">
      <h2 className="text-2xl font-bold text-sky-400">
        Task Onboarding & Instructions
      </h2>
      
      <div className="p-4 bg-slate-900 rounded-lg border border-slate-700 space-y-3 text-sm text-slate-300">
        <p>You have been assigned to your experimental trial session.</p>
        
        <div className="p-3 bg-sky-950/60 border border-sky-700/50 rounded-lg text-sky-200">
          <strong>Language Condition:</strong> {assignedArm === 'ENGLISH_ONLY' ? 'English Only' : assignedArm === 'HINDI_ONLY' ? 'Hindi Only (हिंदी)' : 'Unconstrained Code-Switching'}
        </div>

        <h3 className="font-semibold text-slate-100 pt-2">How to Complete Each Task:</h3>
        <ol className="list-decimal list-inside space-y-2">
          <li>Read the applicant <strong>Persona Card</strong> displayed on the left pane.</li>
          <li>Use the <strong>AI Chat Assistant</strong> on the right pane to ask questions and find relevant rules, limits, and document requirements.</li>
          <li>Refer to official guideline links provided in the left pane whenever needed.</li>
          <li>Fill out the <strong>Final Decision Form</strong> at the bottom right when you are confident in your evaluation.</li>
        </ol>
      </div>

      <button
        onClick={onBeginTasks}
        className="w-full py-3 px-6 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold rounded-lg shadow-lg transition duration-200"
      >
        Begin Task 1 of 3
      </button>
    </div>
  );
};
