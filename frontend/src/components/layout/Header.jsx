import { Menu } from "lucide-react";
import { useState } from "react";
import { useApp } from "../../context/AppContext";

export function Header({ onMenuToggle }) {
  const { patients, selectedPatientId, setSelectedPatientId, createPatient } = useApp();
  const [creating, setCreating] = useState(false);
  const [name, setName] = useState("");

  const handleCreate = async (event) => {
    event.preventDefault();
    if (!name.trim()) return;
    const patient = await createPatient(name.trim());
    setSelectedPatientId(patient.id);
    setName("");
    setCreating(false);
  };

  return (
    <header className="flex items-center justify-between px-4 lg:px-8 py-3 border-b border-slate-200 bg-white">
      <div className="flex items-center gap-3">
        <label className="hidden sm:flex items-center gap-2 text-xs text-slate-500">
          Patient
          <select value={selectedPatientId} onChange={(event) => setSelectedPatientId(Number(event.target.value))} className="rounded-lg border border-slate-200 bg-white px-2 py-1.5 text-sm text-slate-700">
            {patients.map((patient) => <option key={patient.id} value={patient.id}>{patient.name}</option>)}
          </select>
        </label>
        <button type="button" onClick={() => setCreating((value) => !value)} className="hidden sm:block text-xs font-medium text-slate-600 underline underline-offset-2">New patient</button>
        {creating && <form onSubmit={handleCreate} className="absolute right-16 top-12 z-10 flex gap-1 rounded-lg border border-slate-200 bg-white p-2 shadow-sm"><input autoFocus value={name} onChange={(event) => setName(event.target.value)} placeholder="Patient name" className="w-32 rounded border border-slate-200 px-2 py-1 text-xs" /><button className="text-xs font-medium text-slate-700">Add</button></form>}
        <button
          onClick={onMenuToggle}
          className="lg:hidden p-2 rounded-lg text-slate-600 hover:bg-slate-100"
          aria-label="Toggle navigation"
        >
          <Menu className="h-5 w-5" />
        </button>
        <span className="text-sm text-slate-500 hidden sm:block">Demo workspace · Sample reports only</span>
      </div>
      <div className="flex items-center gap-3">
        <div className="h-8 w-8 rounded-full bg-slate-200 flex items-center justify-center">
          <span className="text-xs font-medium text-slate-600">SP</span>
        </div>
      </div>
    </header>
  );
}
