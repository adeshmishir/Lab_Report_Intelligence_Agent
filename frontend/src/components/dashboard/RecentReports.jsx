import { Link } from "react-router-dom";
import { StatusBadge } from "../common/StatusBadge";

export function RecentReports({ reports }) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white overflow-hidden">
      <div className="px-6 py-4 border-b border-slate-100">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-semibold text-slate-900">Recent reports</h3>
          <Link to="/reports" className="text-xs font-medium text-slate-500 hover:text-slate-700">
            View all
          </Link>
        </div>
      </div>
      <div className="divide-y divide-slate-100">
        {reports.map((report) => (
          <div key={report.id} className="px-6 py-3.5 flex items-center justify-between hover:bg-slate-50/50">
            <div className="flex items-center gap-4 min-w-0">
              <div className="h-9 w-9 rounded-lg bg-slate-100 flex items-center justify-center shrink-0">
                <span className="text-xs font-semibold text-slate-500">
                  {report.name.split(" ").map((w) => w[0]).join("")}
                </span>
              </div>
              <div className="min-w-0">
                <p className="text-sm font-medium text-slate-900 truncate">{report.name}</p>
                <p className="text-xs text-slate-400 mt-0.5">{report.dateFormatted}</p>
              </div>
            </div>
            <div className="flex items-center gap-4 ml-4 shrink-0">
              <span className="text-xs text-slate-400 hidden sm:block">{report.tests} tests</span>
              <StatusBadge status={report.status} />
              <Link
                to={`/reports/${report.id}`}
                className="text-xs font-medium text-slate-600 hover:text-slate-900 underline underline-offset-2"
              >
                View report
              </Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}