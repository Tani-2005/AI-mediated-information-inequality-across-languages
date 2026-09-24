import React, { useState } from 'react';

interface Props {
  participantId: string;
  onPostTaskComplete: () => void;
  submitPostTaskFn: (pid: string, rawTlx: Record<string, number>, comments?: string) => Promise<any>;
}

const TLX_ITEMS = [
  { id: 'mental_demand', label: 'Mental Demand', desc: 'How much mental and perceptual activity was required?' },
  { id: 'physical_demand', label: 'Physical Demand', desc: 'How much physical activity was required?' },
  { id: 'temporal_demand', label: 'Temporal Demand', desc: 'How much time pressure did you feel due to the pace?' },
  { id: 'performance', label: 'Performance', desc: 'How successful do you think you were in accomplishing the goals?' },
  { id: 'effort', label: 'Effort', desc: 'How hard did you have to work to accomplish your level of performance?' },
  { id: 'frustration', label: 'Frustration', desc: 'How insecure, discouraged, irritated, or annoyed did you feel?' },
];

export const S9PostTask: React.FC<Props> = ({ participantId, onPostTaskComplete, submitPostTaskFn }) => {
  const [tlxScores, setTlxScores] = useState<Record<string, number>>({
    mental_demand: 10,
    physical_demand: 2,
    temporal_demand: 8,
    performance: 15,
    effort: 12,
    frustration: 5,
  });
  const [comments, setComments] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      await submitPostTaskFn(participantId, tlxScores, comments);
      onPostTaskComplete();
    } catch (err: any) {
      setError(err.message || 'Failed to submit post-task measures.');
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-6 bg-slate-800 rounded-xl shadow-2xl border border-slate-700 my-8 space-y-6">
      <h2 className="text-2xl font-bold text-sky-400">
        Post-Task Measures (Raw NASA-TLX)
      </h2>
      <p className="text-sm text-slate-300">
        Please rate your overall workload across the 3 tasks on a scale from 1 (Very Low) to 20 (Very High).
      </p>

      {error && <div className="p-3 bg-rose-900/50 text-rose-300 rounded text-sm border border-rose-700">{error}</div>}

      <form onSubmit={handleSubmit} className="space-y-6">
        {TLX_ITEMS.map((item) => (
          <div key={item.id} className="p-4 bg-slate-900 rounded-lg border border-slate-700 space-y-2">
            <div className="flex justify-between items-center text-sm font-semibold text-slate-200">
              <span>{item.label}</span>
              <span className="text-sky-400">{tlxScores[item.id]} / 20</span>
            </div>
            <p className="text-xs text-slate-400">{item.desc}</p>
            <input
              type="range"
              min="1"
              max="20"
              value={tlxScores[item.id]}
              onChange={(e) => setTlxScores({ ...tlxScores, [item.id]: parseInt(e.target.value) })}
              className="w-full accent-sky-500"
            />
          </div>
        ))}

        <div className="p-4 bg-slate-900 rounded-lg border border-slate-700 space-y-2">
          <label className="block text-sm font-semibold text-slate-200">Optional Overall Feedback / Comments</label>
          <textarea
            rows={3}
            value={comments}
            onChange={(e) => setComments(e.target.value)}
            placeholder="Share any comments about your experience using the AI assistant..."
            className="w-full p-2 bg-slate-950 border border-slate-800 rounded text-xs text-white"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full py-3 px-6 bg-sky-600 hover:bg-sky-500 disabled:bg-slate-700 text-white font-semibold rounded-lg shadow-lg transition duration-200"
        >
          {loading ? 'Submitting Workload Measures...' : 'Complete Study & View Debrief'}
        </button>
      </form>
    </div>
  );
};
