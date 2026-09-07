import { Loader2 } from "lucide-react";

export function LoadingState({ message = "Loading..." }) {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <Loader2 className="h-6 w-6 text-slate-400 animate-spin" />
      <p className="mt-3 text-sm text-slate-500">{message}</p>
    </div>
  );
}
