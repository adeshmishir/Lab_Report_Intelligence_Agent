import { StatusBadge } from "../common/StatusBadge";

export function ResultTable({ results }) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white overflow-hidden">
      <table className="w-full">
        <thead>
          <tr className="border-b border-slate-100">
            <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Test</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Value</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Unit</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider hidden md:table-cell">Reference range</th>
            <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Status</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-50">
          {results.map((result, idx) => (
            <tr key={idx} className="hover:bg-slate-50/50">
              <td className="px-6 py-3.5 text-sm font-medium text-slate-900">{result.test}</td>
              <td className="px-6 py-3.5 text-sm text-slate-700 tabular-nums">{result.value}</td>
              <td className="px-6 py-3.5 text-sm text-slate-500">{result.unit}</td>
              <td className="px-6 py-3.5 text-sm text-slate-400 hidden md:table-cell">{result.reference}</td>
              <td className="px-6 py-3.5"><StatusBadge status={result.status} /></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}