import { Link } from "react-router-dom";
import { Home } from "lucide-react";
import { Button } from "../components/common/Button";

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center py-24 text-center">
      <p className="text-6xl font-bold text-slate-200">404</p>
      <h1 className="mt-4 text-lg font-semibold text-slate-900">Page not found</h1>
      <p className="mt-2 text-sm text-slate-500">The page you're looking for doesn't exist.</p>
      <Link to="/" className="mt-6">
        <Button>
          <Home className="h-4 w-4" /> Back to dashboard
        </Button>
      </Link>
    </div>
  );
}