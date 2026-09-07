export function StatusBadge({ status }) {
  const styles = {
    normal: "bg-emerald-50 text-emerald-700 ring-emerald-600/20",
    high: "bg-amber-50 text-amber-700 ring-amber-600/20",
    low: "bg-red-50 text-red-700 ring-red-600/20",
    processed: "bg-emerald-50 text-emerald-700 ring-emerald-600/20",
    pending: "bg-amber-50 text-amber-700 ring-amber-600/20",
    error: "bg-red-50 text-red-700 ring-red-600/20",
    good: "bg-emerald-50 text-emerald-700 ring-emerald-600/20",
    missing_value: "bg-amber-50 text-amber-700 ring-amber-600/20",
    missing_unit: "bg-amber-50 text-amber-700 ring-amber-600/20",
    missing_reference_range: "bg-amber-50 text-amber-700 ring-amber-600/20",
    ambiguous_value: "bg-amber-50 text-amber-700 ring-amber-600/20",
    duplicate_test: "bg-slate-100 text-slate-600 ring-slate-500/20",
    conflicting_values: "bg-red-50 text-red-700 ring-red-600/20",
    unreadable: "bg-red-50 text-red-700 ring-red-600/20",
    invalid: "bg-red-50 text-red-700 ring-red-600/20",
  };

  const labels = {
    normal: "Normal",
    high: "High",
    low: "Low",
    processed: "Processed",
    pending: "Pending",
    error: "Error",
    good: "Good",
    missing_value: "Needs review",
    missing_unit: "Missing unit",
    missing_reference_range: "Missing range",
    ambiguous_value: "Needs review",
    duplicate_test: "Duplicate",
    conflicting_values: "Conflicting result",
    unreadable: "Needs review",
    invalid: "Needs review",
  };

  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ring-1 ring-inset ${styles[status] || styles.pending}`}
    >
      {labels[status] || status}
    </span>
  );
}
