import { Link } from "react-router-dom";
import { FileText } from "lucide-react";
import { useApp } from "../context/AppContext";
import { StatusBadge } from "../components/common/StatusBadge";
import { EmptyState } from "../components/common/EmptyState";

export default function Reports() {
  const { reports, reportsLoading, error } = useApp();

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-slate-900 tracking-tight">Reports</h1>
        <p className="mt-1 text-sm text-slate-500">All uploaded lab reports and their results.</p>
      </div>

      {reportsLoading ? (
        <p className="text-sm text-slate-500">Loading reports...</p>
      ) : error ? (
        <p className="text-sm text-red-600">{error}</p>
      ) : reports.length === 0 ? (
        <EmptyState
          icon={FileText}
          title="No reports yet"
          description="Upload a lab report from the dashboard to get started."
        />
      ) : (
        <div className="rounded-xl border border-slate-200 bg-white overflow-hidden">
          <table className="w-full">
            <thead>
              <tr className="border-b border-slate-100">
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Report</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Date</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider hidden sm:table-cell">Tests</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-50">
              {reports.map((report) => (
                <tr key={report.id} className="hover:bg-slate-50/50">
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-3">
                      <div className="h-9 w-9 rounded-lg bg-slate-100 flex items-center justify-center">
                        <span className="text-xs font-semibold text-slate-500">
                          {report.name.split(/[\s_.-]+/).map((w) => w[0]).join("").slice(0, 2).toUpperCase()}
                        </span>
                      </div>
                      <span className="text-sm font-medium text-slate-900">{report.name}</span>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-sm text-slate-500">{report.dateFormatted}</td>
                  <td className="px-6 py-4 text-sm text-slate-500 hidden sm:table-cell">{report.tests} results</td>
                  <td className="px-6 py-4"><StatusBadge status={report.status} /></td>
                  <td className="px-6 py-4">
                    <Link
                      to={`/reports/${report.id}`}
                      className="text-sm font-medium text-slate-600 hover:text-slate-900 underline underline-offset-2"
                    >
                      View report
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}