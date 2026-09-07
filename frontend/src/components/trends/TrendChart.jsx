export function TrendChart({ data, testName }) {
  if (!data || data.length === 0) return null;

  const values = data.filter((d) => d.value !== null);
  if (values.length === 0) return <p className="text-sm text-slate-400 text-center py-8">No data available for {testName}.</p>;

  const maxVal = Math.max(...values.map((d) => d.value)) * 1.1;
  const minVal = Math.min(...values.map((d) => d.value)) * 0.9;
  const range = maxVal - minVal || 1;

  const points = data.map((d, i) => {
    const x = (i / (data.length - 1)) * 100;
    const y = d.value !== null ? ((d.value - minVal) / range) * 100 : null;
    return { x, y, ...d };
  });

  const validPoints = points.filter((p) => p.y !== null);
  const pathD =
    validPoints.length > 0
      ? validPoints.map((p, i) => `${i === 0 ? "M" : "L"} ${p.x} ${100 - p.y}`).join(" ")
      : "";

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-6">
      <div className="relative" style={{ height: 240 }}>
        <svg viewBox="0 0 100 100" className="w-full h-full" preserveAspectRatio="none">
          <line x1="0" y1="0" x2="100" y2="0" stroke="#e2e8f0" strokeWidth="0.3" />
          <line x1="0" y1="25" x2="100" y2="25" stroke="#e2e8f0" strokeWidth="0.3" />
          <line x1="0" y1="50" x2="100" y2="50" stroke="#e2e8f0" strokeWidth="0.3" />
          <line x1="0" y1="75" x2="100" y2="75" stroke="#e2e8f0" strokeWidth="0.3" />
          <line x1="0" y1="100" x2="100" y2="100" stroke="#e2e8f0" strokeWidth="0.3" />

          {pathD && (
            <path d={pathD} fill="none" stroke="#0f172a" strokeWidth="0.8" strokeLinecap="round" strokeLinejoin="round" />
          )}

          {validPoints.map((p, i) => (
            <circle key={i} cx={p.x} cy={100 - p.y} r="1.5" fill="#0f172a" />
          ))}
        </svg>

        <div className="absolute inset-0 flex items-end justify-between px-1 pb-0">
          {data.map((d, i) => (
            <div key={i} className="flex flex-col items-center" style={{ width: `${100 / data.length}%` }}>
              <span className="text-xs text-slate-500 mb-1">
                {d.value !== null ? d.value : "—"}
              </span>
              <span className="text-[10px] text-slate-400">{d.date}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}