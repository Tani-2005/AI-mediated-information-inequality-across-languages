import React, { useState } from 'react';

interface Props {
  participantId: string;
  onAILSComplete: (stratum: string) => void;
  submitAILiteracyFn: (pid: string, responses: Record<string, number>) => Promise<any>;
}

const AILS_ITEMS = [
  { id: 'ails1', text: 'I understand the basic concepts of how Artificial Intelligence and machine learning operate.' },
  { id: 'ails2', text: 'I can distinguish between AI-generated content and human-written content.' },
  { id: 'ails3', text: 'I frequently use AI assistants (like ChatGPT, Gemini, Perplexity) for daily information seeking.' },
  { id: 'ails4', text: 'I know how to formulate effective prompts to obtain precise answers from AI tools.' },
  { id: 'ails5', text: 'I critically evaluate the accuracy of information provided by AI tools before trusting it.' },
  { id: 'ails6', text: 'I am aware that AI models can generate plausible-sounding but false information (hallucinations).' },
  { id: 'ails7', text: 'I understand how data privacy and security apply when using conversational AI platforms.' },
  { id: 'ails8', text: 'I feel confident using AI tools to solve complex information seeking problems.' },
  { id: 'ails9', text: 'I know how to verify claims made by AI tools against external authoritative sources.' },
  { id: 'ails10', text: 'I am aware of potential cultural and linguistic biases present in AI models.' },
  { id: 'ails11', text: 'I can identify situations where using an AI search tool is preferable to a traditional web search engine.' },
  { id: 'ails12', text: 'I stay informed about recent advancements and limitations in consumer AI technologies.' },
];

export const S4AILiteracy: React.FC<Props> = ({ participantId, onAILSComplete, submitAILiteracyFn }) => {
  const [responses, setResponses] = useState<Record<string, number>>({
    ails1: 4, ails2: 4, ails3: 4, ails4: 4, ails5: 4, ails6: 4,
    ails7: 4, ails8: 4, ails9: 4, ails10: 4, ails11: 4, ails12: 4,
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleRatingChange = (id: string, value: number) => {
    setResponses((prev) => ({ ...prev, [id]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const res = await submitAILiteracyFn(participantId, responses);
      onAILSComplete(res.stratum);
    } catch (err: any) {
      setError(err.message || 'Failed to submit AI Literacy Scale.');
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-slate-800 rounded-xl shadow-2xl border border-slate-700 my-8 space-y-6">
      <h2 className="text-2xl font-bold text-sky-400">
        AI Literacy Scale (AILS)
      </h2>
      <p className="text-sm text-slate-300">
        Please rate your agreement with each statement on a scale from 1 (Strongly Disagree) to 5 (Strongly Agree).
      </p>

      {error && <div className="p-3 bg-rose-900/50 text-rose-300 rounded text-sm border border-rose-700">{error}</div>}

      <form onSubmit={handleSubmit} className="space-y-4">
        {AILS_ITEMS.map((item, idx) => (
          <div key={item.id} className="p-4 bg-slate-900 rounded-lg border border-slate-700 flex flex-col md:flex-row md:items-center justify-between gap-4">
            <span className="text-sm text-slate-200">
              <strong className="text-sky-400 mr-2">{idx + 1}.</strong> {item.text}
            </span>
            
            <div className="flex items-center gap-3 self-end md:self-auto">
              {[1, 2, 3, 4, 5].map((val) => (
                <label key={val} className="flex flex-col items-center text-xs text-slate-400 cursor-pointer">
                  <span>{val}</span>
                  <input
                    type="radio"
                    name={item.id}
                    value={val}
                    checked={responses[item.id] === val}
                    onChange={() => handleRatingChange(item.id, val)}
                    className="accent-sky-500 mt-1"
                  />
                </label>
              ))}
            </div>
          </div>
        ))}

        <button
          type="submit"
          disabled={loading}
          className="w-full py-3 px-6 bg-sky-600 hover:bg-sky-500 disabled:bg-slate-700 text-white font-semibold rounded-lg shadow-lg transition duration-200 mt-6"
        >
          {loading ? 'Submitting & Randomizing...' : 'Submit & Trigger Server-Side Randomization'}
        </button>
      </form>
    </div>
  );
};
