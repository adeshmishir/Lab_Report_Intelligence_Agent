import { useState } from "react";
import { useApp } from "../context/AppContext";
import { TrendChart } from "../components/trends/TrendChart";
import { TrendSummary } from "../components/trends/TrendSummary";

const TEST_OPTIONS = ["HbA1c", "Glucose", "LDL", "Hemoglobin"];

export default function Trends() {
  const { trendData } = useApp();
  const [selectedTest, setSelectedTest] = useState("HbA1c");

  const data = trendData[selectedTest] || [];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-slate-900 tracking-tight">Trends</h1>
        <p className="mt-1 text-sm text-slate-500">
          Compare the same test across different report dates.
        </p>
      </div>

      <div className="flex items-center gap-3">
        <label htmlFor="test-select" className="text-sm text-slate-500">
          Test
        </label>
        <select
          id="test-select"
          value={selectedTest}
          onChange={(e) => setSelectedTest(e.target.value)}
          className="rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-slate-900"
        >
          {TEST_OPTIONS.map((test) => (
            <option key={test} value={test}>
              {test}
            </option>
          ))}
        </select>
      </div>

      <TrendChart data={data} testName={selectedTest} />

      <TrendSummary testName={selectedTest} data={data} />

      <p className="text-xs text-slate-400">Sample/demo values shown above.</p>
    </div>
  );
}