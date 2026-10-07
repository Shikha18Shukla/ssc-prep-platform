import { Link } from "react-router-dom";
import { useAuth } from "@/hooks";

export function HomePage() {
  const { isAuthenticated, user } = useAuth();

  return (
    <div className="flex flex-col items-center justify-center py-12">
      <div className="w-full max-w-card rounded-xl bg-card p-8 shadow-sm border border-gray-100">
        <h2 className="mb-4 text-2xl font-bold text-content">
          Welcome to SSC Prep Platform
        </h2>
        <p className="leading-relaxed text-gray-600">
          Your comprehensive preparation platform for SSC competitive exams.
          Practice with timed MCQ tests, track your progress, and ace your
          exams.
        </p>

        <div className="mt-6 flex flex-wrap gap-3">
          <span className="rounded-full bg-primary-50 px-4 py-1.5 text-sm font-medium text-primary">
            SSC
          </span>
          <span className="rounded-full bg-gray-100 px-4 py-1.5 text-sm font-medium text-gray-400">
            Railway — Coming Soon
          </span>
          <span className="rounded-full bg-gray-100 px-4 py-1.5 text-sm font-medium text-gray-400">
            Banking — Coming Soon
          </span>
          <span className="rounded-full bg-gray-100 px-4 py-1.5 text-sm font-medium text-gray-400">
            Police — Coming Soon
          </span>
        </div>

        <div className="mt-8 pt-6 border-t border-gray-100 flex items-center justify-between">
          {isAuthenticated ? (
            <div className="flex items-center justify-between w-full">
              <span className="text-sm text-gray-600">
                Logged in as <strong className="text-content">{user?.full_name || user?.email}</strong>
              </span>
              <Link
                to="/dashboard"
                className="rounded-lg bg-primary px-5 py-2.5 text-sm font-semibold text-white shadow-xs hover:bg-primary-600 transition"
              >
                Go to Dashboard &rarr;
              </Link>
            </div>
          ) : (
            <div className="flex items-center gap-3 w-full sm:w-auto">
              <Link
                to="/signup"
                className="rounded-lg bg-primary px-5 py-2.5 text-sm font-semibold text-white shadow-xs hover:bg-primary-600 transition text-center"
              >
                Get Started
              </Link>
              <Link
                to="/login"
                className="rounded-lg border border-gray-200 bg-white px-5 py-2.5 text-sm font-medium text-content hover:bg-gray-50 transition text-center"
              >
                Sign In
              </Link>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
