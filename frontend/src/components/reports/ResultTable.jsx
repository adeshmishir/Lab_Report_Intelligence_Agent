import { StatusBadge } from "../common/StatusBadge";

export function ResultTable({ results }) {
  const qualityDetails = {
    missing_value: "A value was not provided or could not be read.",
    missing_unit: "The report did not include a unit.",
    missing_reference_range: "The report did not include a reference range.",
    ambiguous_value: "The extracted value needs review.",
    conflicting_values: "This test appears more than once with different values.",
    duplicate_test: "This identical result appeared more than once.",
  };

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
              <td className="px-6 py-3.5 text-sm font-medium text-slate-900">
                {result.test_name_normalized || result.test}
                {(result.test_name_original || result.test) !== (result.test_name_normalized || result.test) && (
                  <span className="block text-xs font-normal text-slate-400">Reported as: {result.test_name_original}</span>
                )}
              </td>
              <td className="px-6 py-3.5 text-sm text-slate-700 tabular-nums">
                {result.value_numeric ?? result.value_text ?? (result.status === "missing_value" ? "Needs review" : result.value) ?? "Not provided"}
              </td>
              <td className="px-6 py-3.5 text-sm text-slate-500">{result.unit || "Not provided"}</td>
              <td className="px-6 py-3.5 text-sm text-slate-400 hidden md:table-cell">
                {result.reference_text || result.reference || (result.reference_low != null || result.reference_high != null
                  ? `${result.reference_low ?? ""}-${result.reference_high ?? ""}` : "Not provided")}
              </td>
              <td className="px-6 py-3.5" title={qualityDetails[result.data_quality || result.status] || undefined}>
                <StatusBadge status={result.data_quality || result.status} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}