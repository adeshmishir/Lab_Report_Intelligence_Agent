import { Menu } from "lucide-react";

export function Header({ onMenuToggle }) {
  return (
    <header className="flex items-center justify-between px-4 lg:px-8 py-3 border-b border-slate-200 bg-white">
      <div className="flex items-center gap-3">
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
