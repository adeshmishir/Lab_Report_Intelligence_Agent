import { useEffect, useState } from "react";
import { getTrends } from "../api/client";
import { TrendChart } from "../components/trends/TrendChart";
import { TrendSummary } from "../components/trends/TrendSummary";
import { useApp } from "../context/AppContext";

export default function Trends() {
  const { selectedPatientId } = useApp();
  const [trendData, setTrendData] = useState({});
  const [selectedTest, setSelectedTest] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    getTrends(selectedPatientId)
      .then((payload) => {
        setTrendData(payload.data || {});
        setSelectedTest((current) => current || payload.tests?.[0] || "");
      })
      .catch((requestError) => setError(requestError.message))
      .finally(() => setLoading(false));
  }, [selectedPatientId]);

  const data = trendData[selectedTest] || [];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-slate-900 tracking-tight">Trends</h1>
        <p className="mt-1 text-sm text-slate-500">
          Compare the same test across different report dates.
        </p>
      </div>

      {loading ? <p className="text-sm text-slate-500">Loading trends...</p> : error ? <p className="text-sm text-red-600">{error}</p> : Object.keys(trendData).length === 0 ? <p className="text-sm text-slate-500">No numeric results are available for trend analysis yet.</p> : <div className="flex items-center gap-3">
        <label htmlFor="test-select" className="text-sm text-slate-500">
          Test
        </label>
        <select
          id="test-select"
          value={selectedTest}
          onChange={(e) => setSelectedTest(e.target.value)}
          className="rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-slate-900"
        >
          {Object.keys(trendData).map((test) => (
            <option key={test} value={test}>
              {test}
            </option>
          ))}
        </select>
      </div>}

      <TrendChart data={data} testName={selectedTest} />

      <TrendSummary testName={selectedTest} data={data} />

      <p className="text-xs text-slate-400">Values are read from processed reports in your workspace.</p>
    </div>
  );
}