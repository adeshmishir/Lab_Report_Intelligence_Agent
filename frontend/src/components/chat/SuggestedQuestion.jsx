import { suggestedQuestions } from "../../data/demoData";

export function SuggestedQuestion({ onClick }) {
  return (
    <div className="flex flex-wrap gap-2 mb-6">
      {suggestedQuestions.map((q) => (
        <button
          key={q}
          onClick={() => onClick(q)}
          className="text-xs text-slate-600 bg-white border border-slate-200 rounded-full px-3.5 py-1.5 hover:bg-slate-50 hover:border-slate-300 transition-colors"
        >
          {q}
        </button>
      ))}
    </div>
  );
}