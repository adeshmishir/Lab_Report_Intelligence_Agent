async function request(path, options) {
  const response = await fetch(path, options);
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(payload?.error?.message || "LabLens could not complete that request.");
  }
  return payload;
}

export function listReports() {
  return request("/api/reports");
}

export function getReport(reportId) {
  return request(`/api/reports/${reportId}`);
}

export function uploadReport(file) {
  const formData = new FormData();
  formData.append("file", file);
  return request("/api/reports/upload", { method: "POST", body: formData });
}

export function normalizeReport(report) {
  const date = report.report_date ? new Date(`${report.report_date}T00:00:00`) : null;
  return {
    ...report,
    name: report.original_filename,
    fileName: report.original_filename,
    dateFormatted: date ? date.toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" }) : "Date not provided",
    tests: report.tests_count ?? report.results?.length ?? 0,
    attentionCount: report.attention_count ?? 0,
    results: report.results || [],
  };
}

export function getTrends() {
  return request("/api/trends");
}