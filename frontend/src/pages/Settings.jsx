export default function Settings() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-slate-900 tracking-tight">Settings</h1>
        <p className="mt-1 text-sm text-slate-500">Manage your workspace preferences.</p>
      </div>

      <div className="rounded-xl border border-slate-200 bg-white p-6">
        <h2 className="text-sm font-semibold text-slate-900 mb-4">Account</h2>
        <dl className="space-y-4">
          <div>
            <dt className="text-xs text-slate-400">Workspace</dt>
            <dd className="text-sm text-slate-700 mt-1">Demo workspace</dd>
          </div>
          <div>
            <dt className="text-xs text-slate-400">Plan</dt>
            <dd className="text-sm text-slate-700 mt-1">Sample mode</dd>
          </div>
          <div>
            <dt className="text-xs text-slate-400">Data mode</dt>
            <dd className="text-sm text-slate-700 mt-1">Demo data only</dd>
          </div>
        </dl>
      </div>

      <div className="rounded-xl border border-slate-200 bg-white p-6">
        <h2 className="text-sm font-semibold text-slate-900 mb-2">About LabLens</h2>
        <p className="text-sm text-slate-500">Version 0.1.0 · Phase 1</p>
        <p className="text-xs text-slate-400 mt-2">
          LabLens provides informational summaries from uploaded sample reports. It does not diagnose conditions or recommend treatments.
        </p>
      </div>
    </div>
  );
}