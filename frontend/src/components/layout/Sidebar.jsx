import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  FileText,
  MessageCircle,
  TrendingUp,
  Settings,
  FlaskConical,
} from "lucide-react";

const navItems = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard },
  { to: "/reports", label: "Reports", icon: FileText },
  { to: "/ask", label: "Ask LabLens", icon: MessageCircle },
  { to: "/trends", label: "Trends", icon: TrendingUp },
];

const bottomItems = [
  { to: "/settings", label: "Settings", icon: Settings },
];

export function Sidebar() {
  return (
    <aside className="hidden lg:flex lg:flex-col lg:w-60 lg:border-r lg:border-slate-200 lg:bg-white">
      <div className="flex items-center gap-2.5 px-5 py-5 border-b border-slate-100">
        <div className="flex items-center justify-center h-8 w-8 rounded-lg bg-slate-900">
          <FlaskConical className="h-4 w-4 text-white" />
        </div>
        <span className="text-base font-semibold text-slate-900 tracking-tight">LabLens</span>
      </div>

      <nav className="flex-1 px-3 py-4 space-y-1">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.to === "/"}
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors ${
                isActive
                  ? "bg-slate-100 text-slate-900"
                  : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
              }`
            }
          >
            <item.icon className="h-4 w-4 shrink-0" />
            {item.label}
          </NavLink>
        ))}
      </nav>

      <div className="px-3 py-4 border-t border-slate-100 space-y-1">
        {bottomItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors ${
                isActive
                  ? "bg-slate-100 text-slate-900"
                  : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
              }`
            }
          >
            <item.icon className="h-4 w-4 shrink-0" />
            {item.label}
          </NavLink>
        ))}
        <div className="px-3 pt-3">
          <p className="text-xs text-slate-400">Demo workspace</p>
          <p className="text-xs text-slate-400">Sample reports only</p>
        </div>
      </div>
    </aside>
  );
}
