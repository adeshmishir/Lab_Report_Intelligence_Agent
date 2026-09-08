import { FileText, Clock, Hash, AlertTriangle } from "lucide-react";
import { useApp } from "../context/AppContext";
import { StatCard } from "../components/dashboard/StatCard";
import { UploadReport } from "../components/dashboard/UploadReport";
import { RecentReports } from "../components/dashboard/RecentReports";

function getGreeting() {
  const hour = new Date().getHours();
  if (hour < 12) return "Good morning";
  if (hour < 17) return "Good afternoon";
  return "Good evening";
}

export default function Dashboard() {
  const { reports, reportsLoading, error, refreshReports, refreshPatients, refreshReportsForPatient } = useApp();

  const handleUploaded = async (upload) => {
    await refreshPatients();
    if (upload?.patient_id) {
      await refreshReportsForPatient(upload.patient_id);
    } else {
      await refreshReports();
    }
  };

  const attentionCount = reports.reduce((acc, report) => acc + report.attentionCount, 0);

  const totalTests = reports.reduce((acc, r) => acc + r.tests, 0);

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-semibold text-slate-900 tracking-tight">{getGreeting()}</h1>
        <p className="mt-1 text-sm text-slate-500">
          Here's a quick look at your uploaded lab reports.
        </p>
        <span className="inline-flex items-center rounded-full bg-slate-100 px-2.5 py-0.5 text-xs font-medium text-slate-600 mt-2">
          Sample data
        </span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          icon={FileText}
          label="Reports"
          value={reports.length}
          note={{ text: "Reports uploaded", isUp: true }}
          variant="default"
        />
        <StatCard
          icon={Clock}
          label="Latest Report"
          value={reports[0]?.dateFormatted || "Not provided"}
          note={{ text: "Most recent report", isUp: true }}
          variant="info"
        />
        <StatCard
          icon={Hash}
          label="Results Tracked"
          value={totalTests}
          note={{ text: "Lab results", isUp: true }}
          variant="default"
        />
        <StatCard
          icon={AlertTriangle}
          label="Needs Attention"
          value={attentionCount}
          note={{ text: "Outside reference range", isUp: false }}
          variant="warning"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
        <div className="lg:col-span-2">
          <UploadReport onUploaded={handleUploaded} />
        </div>
        <div className="lg:col-span-3">
          {reportsLoading ? <p className="text-sm text-slate-500">Loading reports...</p> : <RecentReports reports={reports} />}
        </div>
      </div>

      {error && <p className="text-sm text-red-600">{error}</p>}

      <footer className="pt-4 border-t border-slate-100">
        <p className="text-xs text-slate-400">
          LabLens provides informational summaries from uploaded sample reports. It does not diagnose conditions or recommend treatments.
        </p>
      </footer>
    </div>
  );
}