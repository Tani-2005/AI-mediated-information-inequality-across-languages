import React, { useState } from 'react';

interface Props {
  participantId: string;
  onScreeningComplete: (passed: boolean) => void;
  submitScreeningFn: (pid: string, responses: Record<string, string>) => Promise<any>;
}

export const S2Screening: React.FC<Props> = ({ participantId, onScreeningComplete, submitScreeningFn }) => {
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSelect = (qId: string, value: string) => {
    setAnswers((prev) => ({ ...prev, [qId]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (Object.keys(answers).length < 6) {
      setError('Please answer all 6 screening questions before submitting.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const res = await submitScreeningFn(participantId, answers);
      if (res.passed) {
        onScreeningComplete(true);
      } else {
        onScreeningComplete(false);
      }
    } catch (err: any) {
      setError(err.message || 'Screening submission failed.');
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-slate-800 rounded-xl shadow-2xl border border-slate-700 my-8 space-y-6">
      <h2 className="text-2xl font-bold text-sky-400">
        Criterion-Referenced Bilingual Comprehension Screening
      </h2>
      <p className="text-sm text-slate-300">
        Please read the two passages below (one in English, one in Hindi) and answer the 3 multiple-choice questions for each passage.
      </p>

      {error && <div className="p-3 bg-rose-900/50 text-rose-300 rounded text-sm border border-rose-700">{error}</div>}

      <form onSubmit={handleSubmit} className="space-y-8">
        {/* ENGLISH SECTION */}
        <div className="p-5 bg-slate-900 rounded-lg border border-slate-700 space-y-4">
          <h3 className="text-lg font-semibold text-emerald-400">Section A: English Comprehension Passage</h3>
          <p className="text-sm text-slate-300 italic bg-slate-950 p-4 rounded border border-slate-800">
            "Public libraries play a pivotal role in democratizing access to information within municipal communities. Beyond providing physical books, modern community libraries offer public internet workstations, digital literacy workshops, and subscription-based research databases free of charge to registered residents. Recent civic evaluations indicate that adults who regularly utilize community learning centers report higher confidence when navigating online public service portals."
          </p>

          <div className="space-y-4">
            <div>
              <p className="text-sm font-medium text-slate-200 mb-2">1. What primary role do public libraries play according to the passage?</p>
              <div className="space-y-1">
                {['A. Selling academic textbooks', 'B. Democratizing access to information in municipal communities', 'C. Managing municipal tax collection', 'D. Regulating internet service providers'].map((opt) => (
                  <label key={opt} className="flex items-center gap-2 text-sm text-slate-300 cursor-pointer">
                    <input type="radio" name="q1" value={opt[0]} onChange={() => handleSelect('q1', opt[0])} className="accent-sky-500" />
                    {opt}
                  </label>
                ))}
              </div>
            </div>

            <div>
              <p className="text-sm font-medium text-slate-200 mb-2">2. What services do modern libraries offer besides physical books?</p>
              <div className="space-y-1">
                {['A. Public internet workstations and digital literacy workshops', 'B. Paid private tutoring', 'C. Commercial software sales', 'D. Foreign language travel services'].map((opt) => (
                  <label key={opt} className="flex items-center gap-2 text-sm text-slate-300 cursor-pointer">
                    <input type="radio" name="q2" value={opt[0]} onChange={() => handleSelect('q2', opt[0])} className="accent-sky-500" />
                    {opt}
                  </label>
                ))}
              </div>
            </div>

            <div>
              <p className="text-sm font-medium text-slate-200 mb-2">3. What correlation is reported for adults who use community learning centers?</p>
              <div className="space-y-1">
                {['A. Higher interest in purchasing books', 'B. Lower frequency of internet usage', 'C. Higher confidence when navigating online public service portals', 'D. Preference for physical government forms'].map((opt) => (
                  <label key={opt} className="flex items-center gap-2 text-sm text-slate-300 cursor-pointer">
                    <input type="radio" name="q3" value={opt[0]} onChange={() => handleSelect('q3', opt[0])} className="accent-sky-500" />
                    {opt}
                  </label>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* HINDI SECTION */}
        <div className="p-5 bg-slate-900 rounded-lg border border-slate-700 space-y-4">
          <h3 className="text-lg font-semibold text-amber-400">अनुभाग B: हिंदी समझ गद्यांश (Hindi Comprehension Passage)</h3>
          <p className="text-sm text-slate-300 italic bg-slate-950 p-4 rounded border border-slate-800">
            "सार्वजनिक डिजिटल सेवा केंद्र (CSC) ग्रामीण क्षेत्रों में नागरिकों को विभिन्न सरकारी योजनाओं का लाभ पहुंचाने में महत्वपूर्ण भूमिका निभाते हैं। ये केंद्र न केवल पेंशन और राशन कार्ड आवेदन जैसी सेवाएं प्रदान करते हैं, बल्कि किसानों को कृषि मौसम परामर्श और मृदा स्वास्थ्य जानकारी प्राप्त करने में भी सहायता करते हैं। हालिया मूल्यांकनों से पता चलता है कि नियमित रूप से CSC सेवाओं का उपयोग करने वाले ग्रामीण नागरिकों को सरकारी प्रक्रियाओं को समझने में कम समय लगता है।"
          </p>

          <div className="space-y-4">
            <div>
              <p className="text-sm font-medium text-slate-200 mb-2">4. गद्यांश के अनुसार सार्वजनिक डिजिटल सेवा केंद्र (CSC) की क्या भूमिका है?</p>
              <div className="space-y-1">
                {['A. ग्रामीण क्षेत्रों में नागरिकों को सरकारी योजनाओं का लाभ पहुंचाना', 'B. प्राइवेट बैंक खाते खोलना', 'C. स्कूल की पुस्तकें बेचना', 'D. केवल मोबाइल रिचार्ज करना'].map((opt) => (
                  <label key={opt} className="flex items-center gap-2 text-sm text-slate-300 cursor-pointer">
                    <input type="radio" name="q4" value={opt[0]} onChange={() => handleSelect('q4', opt[0])} className="accent-sky-500" />
                    {opt}
                  </label>
                ))}
              </div>
            </div>

            <div>
              <p className="text-sm font-medium text-slate-200 mb-2">5. CSC केंद्र किसानों को किन विषयों पर जानकारी प्रदान करते हैं?</p>
              <div className="space-y-1">
                {['A. केवल ट्रैक्टर बिक्री', 'B. विदेश यात्रा वीजा', 'C. कृषि मौसम परामर्श और मृदा स्वास्थ्य जानकारी', 'D. कीटनाशक का वाणिज्यिक उत्पादन'].map((opt) => (
                  <label key={opt} className="flex items-center gap-2 text-sm text-slate-300 cursor-pointer">
                    <input type="radio" name="q5" value={opt[0]} onChange={() => handleSelect('q5', opt[0])} className="accent-sky-500" />
                    {opt}
                  </label>
                ))}
              </div>
            </div>

            <div>
              <p className="text-sm font-medium text-slate-200 mb-2">6. नियमित रूप से CSC का उपयोग करने वाले ग्रामीणों पर क्या प्रभाव देखा गया है?</p>
              <div className="space-y-1">
                {['A. उन्हें इंटरनेट उपयोग में अधिक समस्या होती है', 'B. उन्हें सरकारी प्रक्रियाओं को समझने में कम समय लगता है', 'C. वे केवल फोन कॉल करते हैं', 'D. वे कागजी फॉर्म ही पसंद करते हैं'].map((opt) => (
                  <label key={opt} className="flex items-center gap-2 text-sm text-slate-300 cursor-pointer">
                    <input type="radio" name="q6" value={opt[0]} onChange={() => handleSelect('q6', opt[0])} className="accent-sky-500" />
                    {opt}
                  </label>
                ))}
              </div>
            </div>
          </div>
        </div>

        <button
          type="submit"
          disabled={loading || Object.keys(answers).length < 6}
          className="w-full py-3 px-6 bg-sky-600 hover:bg-sky-500 disabled:bg-slate-700 text-white font-semibold rounded-lg shadow-lg transition duration-200"
        >
          {loading ? 'Evaluating Screening Answers...' : 'Submit Screening Answers'}
        </button>
      </form>
    </div>
  );
};
