import React, { useEffect, useState } from 'react';

interface Props {
  participantId: string;
  completeDebriefFn: (pid: string) => Promise<any>;
}

export const S10Debrief: React.FC<Props> = ({ participantId, completeDebriefFn }) => {
  const [completionCode, setCompletionCode] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    completeDebriefFn(participantId).then((res) => {
      setCompletionCode(res.completion_code);
      setLoading(false);
    });
  }, [participantId, completeDebriefFn]);

  return (
    <div className="max-w-2xl mx-auto p-8 bg-slate-800 rounded-xl shadow-2xl border border-slate-700 my-12 text-center space-y-6">
      <div className="w-16 h-16 bg-emerald-950/80 border border-emerald-500 text-emerald-400 rounded-full flex items-center justify-center mx-auto text-2xl font-bold">
        ✓
      </div>
      
      <h2 className="text-3xl font-bold text-slate-100">Study Completed!</h2>

      <p className="text-slate-300 text-sm leading-relaxed">
        Thank you for participating in this research study investigating linguistic inequality and AI-mediated information seeking across English and Hindi.
      </p>

      {loading ? (
        <div className="text-slate-400 text-sm">Generating verification completion code...</div>
      ) : (
        <div className="p-4 bg-slate-900 rounded-lg border border-slate-700 space-y-2">
          <span className="text-xs text-slate-400 uppercase tracking-wider block">Your Verification Completion Code</span>
          <span className="text-2xl font-mono font-bold text-sky-400">{completionCode}</span>
          <p className="text-[11px] text-slate-500 pt-1">Please copy and save this code for your records or incentive verification.</p>
        </div>
      )}

      <div className="text-xs text-slate-400 pt-4 border-t border-slate-700">
        If you have any questions regarding this study, please contact the Principal Investigator at research-study@university.edu.
      </div>
    </div>
  );
};
