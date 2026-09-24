import React, { useState } from 'react';

interface Props {
  participantId: string;
  onLEAPQComplete: () => void;
  submitLEAPQFn: (pid: string, data: any) => Promise<any>;
}

export const S3LanguageBackground: React.FC<Props> = ({ participantId, onLEAPQComplete, submitLEAPQFn }) => {
  const [formData, setFormData] = useState({
    aoa_english: 6,
    aoa_hindi: 0,
    primary_home_lang: 'Hindi',
    medium_instruction_school: 'Hindi',
    medium_instruction_higher: 'English',
    self_read_en: 8,
    self_write_en: 8,
    self_speak_en: 8,
    self_read_hi: 9,
    self_write_hi: 9,
    self_speak_hi: 9,
    freq_daily_en: 40,
    freq_daily_hi: 50,
    freq_daily_cs: 10,
    ai_use_en: 60,
    ai_use_hi: 30,
    ai_use_mixed: 10,
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      await submitLEAPQFn(participantId, formData);
      onLEAPQComplete();
    } catch (err: any) {
      setError(err.message || 'Failed to submit language background.');
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-6 bg-slate-800 rounded-xl shadow-2xl border border-slate-700 my-8 space-y-6">
      <h2 className="text-2xl font-bold text-sky-400">
        Language Experience & Proficiency Questionnaire (LEAP-Q)
      </h2>
      <p className="text-sm text-slate-300">
        Please provide details regarding your language background, age of acquisition, and self-assessed proficiency.
      </p>

      {error && <div className="p-3 bg-rose-900/50 text-rose-300 rounded text-sm border border-rose-700">{error}</div>}

      <form onSubmit={handleSubmit} className="space-y-6 text-sm text-slate-200">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block mb-1">Age of Acquisition (English, years)</label>
            <input
              type="number"
              value={formData.aoa_english}
              onChange={(e) => setFormData({ ...formData, aoa_english: parseInt(e.target.value) || 0 })}
              className="w-full p-2 bg-slate-900 border border-slate-700 rounded text-white"
            />
          </div>
          <div>
            <label className="block mb-1">Age of Acquisition (Hindi, years)</label>
            <input
              type="number"
              value={formData.aoa_hindi}
              onChange={(e) => setFormData({ ...formData, aoa_hindi: parseInt(e.target.value) || 0 })}
              className="w-full p-2 bg-slate-900 border border-slate-700 rounded text-white"
            />
          </div>
        </div>

        <div className="grid grid-cols-3 gap-4">
          <div>
            <label className="block mb-1">Primary Home Language</label>
            <select
              value={formData.primary_home_lang}
              onChange={(e) => setFormData({ ...formData, primary_home_lang: e.target.value })}
              className="w-full p-2 bg-slate-900 border border-slate-700 rounded text-white"
            >
              <option value="Hindi">Hindi</option>
              <option value="English">English</option>
              <option value="Bilingual">Both equally</option>
              <option value="Other">Other</option>
            </select>
          </div>
          <div>
            <label className="block mb-1">School Medium of Instruction</label>
            <select
              value={formData.medium_instruction_school}
              onChange={(e) => setFormData({ ...formData, medium_instruction_school: e.target.value })}
              className="w-full p-2 bg-slate-900 border border-slate-700 rounded text-white"
            >
              <option value="Hindi">Hindi Medium</option>
              <option value="English">English Medium</option>
              <option value="Bilingual">Bilingual</option>
            </select>
          </div>
          <div>
            <label className="block mb-1">Higher Ed Medium of Instruction</label>
            <select
              value={formData.medium_instruction_higher}
              onChange={(e) => setFormData({ ...formData, medium_instruction_higher: e.target.value })}
              className="w-full p-2 bg-slate-900 border border-slate-700 rounded text-white"
            >
              <option value="English">English Medium</option>
              <option value="Hindi">Hindi Medium</option>
              <option value="Bilingual">Bilingual</option>
            </select>
          </div>
        </div>

        {/* PROFICIENCY LIKERT SCALES */}
        <div className="p-4 bg-slate-900 rounded-lg border border-slate-700 space-y-3">
          <h3 className="font-semibold text-sky-300">Self-Reported Proficiency (1 = Very Poor, 10 = Expert/Native)</h3>
          
          <div className="grid grid-cols-3 gap-4 text-xs">
            <div>
              <p className="font-medium text-slate-300">English Reading: {formData.self_read_en}</p>
              <input type="range" min="1" max="10" value={formData.self_read_en} onChange={(e) => setFormData({ ...formData, self_read_en: parseInt(e.target.value) })} className="w-full accent-sky-500" />
            </div>
            <div>
              <p className="font-medium text-slate-300">English Writing: {formData.self_write_en}</p>
              <input type="range" min="1" max="10" value={formData.self_write_en} onChange={(e) => setFormData({ ...formData, self_write_en: parseInt(e.target.value) })} className="w-full accent-sky-500" />
            </div>
            <div>
              <p className="font-medium text-slate-300">English Speaking: {formData.self_speak_en}</p>
              <input type="range" min="1" max="10" value={formData.self_speak_en} onChange={(e) => setFormData({ ...formData, self_speak_en: parseInt(e.target.value) })} className="w-full accent-sky-500" />
            </div>
          </div>

          <div className="grid grid-cols-3 gap-4 text-xs pt-2">
            <div>
              <p className="font-medium text-slate-300">Hindi Reading: {formData.self_read_hi}</p>
              <input type="range" min="1" max="10" value={formData.self_read_hi} onChange={(e) => setFormData({ ...formData, self_read_hi: parseInt(e.target.value) })} className="w-full accent-amber-500" />
            </div>
            <div>
              <p className="font-medium text-slate-300">Hindi Writing: {formData.self_write_hi}</p>
              <input type="range" min="1" max="10" value={formData.self_write_hi} onChange={(e) => setFormData({ ...formData, self_write_hi: parseInt(e.target.value) })} className="w-full accent-amber-500" />
            </div>
            <div>
              <p className="font-medium text-slate-300">Hindi Speaking: {formData.self_speak_hi}</p>
              <input type="range" min="1" max="10" value={formData.self_speak_hi} onChange={(e) => setFormData({ ...formData, self_speak_hi: parseInt(e.target.value) })} className="w-full accent-amber-500" />
            </div>
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full py-3 px-6 bg-sky-600 hover:bg-sky-500 disabled:bg-slate-700 text-white font-semibold rounded-lg shadow-lg transition duration-200"
        >
          {loading ? 'Saving LEAP-Q Responses...' : 'Save & Continue to AI Literacy Scale'}
        </button>
      </form>
    </div>
  );
};
