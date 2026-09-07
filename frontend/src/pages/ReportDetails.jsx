import { useParams, Link } from "react-router-dom";
import { useState } from "react";
import { ArrowLeft, FileText, ChevronDown, ChevronUp } from "lucide-react";
import { useApp } from "../context/AppContext";
import { StatusBadge } from "../components/common/StatusBadge";
import { ResultTable } from "../components/reports/ResultTable";
import { EmptyState } from "../components/common/EmptyState";
import { Button } from "../components/common/Button";

export default function ReportDetails() {
  const { id } = useParams();
  const { reports } = useApp();
  const [showRawText, setShowRawText] = useState(false);

  const report = reports.find((r) => r.id === Number(id));

  if (!report) {
    return (
      <div className="space-y-6">
        <Link to="/reports" className="inline-flex items-center gap-1.5 text-sm text-slate-500 hover:text-slate-700">
          <ArrowLeft className="h-4 w-4" /> Back to reports
        </Link>
        <EmptyState
          icon={FileText}
          title="Report not found"
          description="The report you're looking for doesn't exist or hasn't been uploaded yet."
        />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <Link to="/reports" className="inline-flex items-center gap-1.5 text-sm text-slate-500 hover:text-slate-700">
        <ArrowLeft className="h-4 w-4" /> Back to reports
      </Link>

      <div>
        <div className="flex items-start justify-between gap-4">
          <div>
            <h1 className="text-2xl font-semibold text-slate-900 tracking-tight">{report.name}</h1>
            <p className="mt-1 text-sm text-slate-500">{report.dateFormatted}</p>
          </div>
          <StatusBadge status={report.status} />
        </div>
      </div>

      <div className="rounded-xl border border-slate-200 bg-white p-6">
        <h2 className="text-sm font-semibold text-slate-900 mb-4">Report overview</h2>
        <dl className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div>
            <dt className="text-xs text-slate-400">Uploaded file</dt>
            <dd className="text-sm text-slate-700 mt-1">{report.fileName}</dd>
          </div>
          <div>
            <dt className="text-xs text-slate-400">Report date</dt>
            <dd className="text-sm text-slate-700 mt-1">{report.dateFormatted}</dd>
          </div>
          <div>
            <dt className="text-xs text-slate-400">Processing status</dt>
            <dd className="mt-1"><StatusBadge status={report.status} /></dd>
          </div>
        </dl>
      </div>

      <div>
        <h2 className="text-sm font-semibold text-slate-900 mb-3">Results</h2>
        <ResultTable results={report.results} />
      </div>

      <div className="rounded-xl border border-slate-200 bg-white">
        <button
          onClick={() => setShowRawText(!showRawText)}
          className="flex items-center justify-between w-full px-6 py-4 text-left"
        >
          <span className="text-sm font-semibold text-slate-900">View extracted source text</span>
          {showRawText ? (
            <ChevronUp className="h-4 w-4 text-slate-400" />
          ) : (
            <ChevronDown className="h-4 w-4 text-slate-400" />
          )}
        </button>
        {showRawText && (
          <div className="px-6 pb-6 border-t border-slate-100 pt-4">
            <pre className="text-xs text-slate-600 whitespace-pre-wrap font-mono bg-slate-50 rounded-lg p-4">
              {report.rawText}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}