export function StatusBadge({ status }) {
  const styles = {
    normal: "bg-emerald-50 text-emerald-700 ring-emerald-600/20",
    high: "bg-amber-50 text-amber-700 ring-amber-600/20",
    low: "bg-red-50 text-red-700 ring-red-600/20",
    processed: "bg-emerald-50 text-emerald-700 ring-emerald-600/20",
    pending: "bg-amber-50 text-amber-700 ring-amber-600/20",
    error: "bg-red-50 text-red-700 ring-red-600/20",
  };

  const labels = {
    normal: "Normal",
    high: "High",
    low: "Low",
    processed: "Processed",
    pending: "Pending",
    error: "Error",
  };

  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ring-1 ring-inset ${styles[status] || styles.pending}`}
    >
      {labels[status] || status}
    </span>
  );
}
