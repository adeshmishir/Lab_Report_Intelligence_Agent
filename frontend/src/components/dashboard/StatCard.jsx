import { ArrowUpRight, ArrowDownRight } from "lucide-react";

const iconStyles = {
  default: "bg-slate-100 text-slate-600",
  success: "bg-emerald-50 text-emerald-600",
  warning: "bg-amber-50 text-amber-600",
  danger: "bg-red-50 text-red-600",
  info: "bg-sky-50 text-sky-600",
};

export function StatCard({ icon: Icon, label, value, note, variant = "default" }) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-5">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-slate-500">{label}</p>
          <p className="mt-2 text-2xl font-semibold text-slate-900 tracking-tight">{value}</p>
        </div>
        <div className={`rounded-full p-2.5 ${iconStyles[variant]}`}>
          <Icon className="h-4 w-4" />
        </div>
      </div>
      {note && (
        <p className="mt-2 text-xs text-slate-400 flex items-center gap-1">
          {note.isUp ? (
            <ArrowUpRight className="h-3 w-3" />
          ) : (
            <ArrowDownRight className="h-3 w-3" />
          )}
          {note.text}
        </p>
      )}
    </div>
  );
}