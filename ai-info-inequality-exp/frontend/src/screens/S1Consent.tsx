import React, { useState } from 'react';

interface Props {
  onConsentComplete: (participantId: string) => void;
  createSessionFn: () => Promise<any>;
  submitConsentFn: (pid: string, terms: boolean, age: boolean) => Promise<any>;
}

export const S1Consent: React.FC<Props> = ({ onConsentComplete, createSessionFn, submitConsentFn }) => {
  const [agreedTerms, setAgreedTerms] = useState(false);
  const [confirmedAge, setConfirmedAge] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!agreedTerms || !confirmedAge) {
      setError('You must accept both checkboxes to participate in this study.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const sessRes = await createSessionFn();
      if (!sessRes.participant_id) {
        throw new Error('Failed to generate participant session.');
      }

      const consentRes = await submitConsentFn(sessRes.participant_id, agreedTerms, confirmedAge);
      if (consentRes.status === 'EXCLUDED') {
        setError('Consent was declined.');
        setLoading(false);
        return;
      }

      onConsentComplete(sessRes.participant_id);
    } catch (err: any) {
      setError(err.message || 'An error occurred during session creation.');
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-6 bg-slate-800 rounded-xl shadow-2xl border border-slate-700 my-8">
      <h1 className="text-2xl font-bold text-sky-400 mb-4">
        Research Study: AI-Mediated Information Seeking Across Languages
      </h1>
      
      <div className="space-y-4 text-slate-300 text-sm leading-relaxed max-h-96 overflow-y-auto p-4 bg-slate-900 rounded-lg border border-slate-700">
        <p><strong>Principal Investigator:</strong> Computational Social Science Research Team</p>
        <p><strong>Study Purpose:</strong> You are invited to participate in a research study evaluating how citizens navigate Indian civic entitlement schemes (such as PMEGP, PM Vishwakarma, and PM SVANidhi) using AI search assistants across different languages.</p>
        <p><strong>Study Procedure:</strong> If you consent, you will complete a brief bilingual screening test, a language background questionnaire, an AI literacy scale, and 3 civic entitlement navigation tasks assisted by an AI chatbot. Finally, you will complete a post-task workload survey.</p>
        <p><strong>Estimated Duration:</strong> Approximately 45 minutes.</p>
        <p><strong>Data Privacy & Protection:</strong> All records are pseudonymous using random IDs. No personal names or government IDs are collected or stored. Your responses are encrypted and stored securely.</p>
        <p><strong>Voluntary Participation:</strong> Participation is voluntary. You may withdraw at any time without penalty.</p>
      </div>

      <form onSubmit={handleSubmit} className="mt-6 space-y-4">
        {error && <div className="p-3 bg-rose-900/50 text-rose-300 rounded text-sm border border-rose-700">{error}</div>}

        <label className="flex items-start gap-3 cursor-pointer">
          <input
            type="checkbox"
            checked={agreedTerms}
            onChange={(e) => setAgreedTerms(e.target.checked)}
            className="mt-1 w-5 h-5 accent-sky-500 rounded"
          />
          <span className="text-sm text-slate-200">
            I have read and understood the information sheet above and agree to participate voluntarily in this research study.
          </span>
        </label>

        <label className="flex items-start gap-3 cursor-pointer">
          <input
            type="checkbox"
            checked={confirmedAge}
            onChange={(e) => setConfirmedAge(e.target.checked)}
            className="mt-1 w-5 h-5 accent-sky-500 rounded"
          />
          <span className="text-sm text-slate-200">
            I confirm that I am between 18 and 65 years of age and currently reside in India.
          </span>
        </label>

        <button
          type="submit"
          disabled={loading || !agreedTerms || !confirmedAge}
          className="w-full py-3 px-6 bg-sky-600 hover:bg-sky-500 disabled:bg-slate-700 text-white font-semibold rounded-lg shadow-lg transition duration-200"
        >
          {loading ? 'Initializing Session...' : 'I Agree — Proceed to Screening'}
        </button>
      </form>
    </div>
  );
};
