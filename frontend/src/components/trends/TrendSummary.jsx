import { TrendingUp } from "lucide-react";

export function TrendSummary({ testName, data }) {
  const values = data.filter((d) => d.value !== null);
  if (values.length < 2) {
    return (
      <div className="rounded-xl border border-slate-200 bg-white p-5">
        <div className="flex items-center gap-2 mb-2">
          <TrendingUp className="h-4 w-4 text-slate-400" />
          <h4 className="text-sm font-semibold text-slate-900">Trend summary</h4>
        </div>
        <p className="text-sm text-slate-500">
          Not enough data points to show a trend for {testName}.
        </p>
      </div>
    );
  }

  const first = values[0].value;
  const last = values[values.length - 1].value;
  const diff = (last - first).toFixed(1);
  const direction = diff > 0 ? "increased" : diff < 0 ? "decreased" : "remained the same";

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-5">
      <div className="flex items-center gap-2 mb-2">
        <TrendingUp className="h-4 w-4 text-slate-400" />
        <h4 className="text-sm font-semibold text-slate-900">Trend summary</h4>
      </div>
      <p className="text-sm text-slate-600">
        Your {testName} {direction} by {diff > 0 ? "+" : ""}
        {diff} between the first and latest sample report.
      </p>
    </div>
  );
}