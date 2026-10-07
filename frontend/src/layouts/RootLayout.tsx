import { Link, Outlet } from "react-router-dom";
import { useAuth } from "@/hooks";

export function RootLayout() {
  const { user, isAuthenticated, logout } = useAuth();

  return (
    <div className="flex min-h-screen flex-col bg-background">
      {/* Header */}
      <header className="border-b border-gray-200 bg-card sticky top-0 z-50 shadow-xs">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
          <Link
            to={isAuthenticated ? "/dashboard" : "/"}
            className="text-xl font-bold text-primary flex items-center gap-2 hover:opacity-90 transition"
          >
            <span>SSC Prep Platform</span>
          </Link>

          <nav className="flex items-center gap-3 sm:gap-4">
            {isAuthenticated ? (
              <div className="flex items-center gap-3">
                <Link
                  to="/dashboard"
                  className="text-sm font-medium text-content hover:text-primary transition hidden sm:inline"
                >
                  Dashboard
                </Link>
                <span className="text-xs text-gray-400 hidden sm:inline">|</span>
                <span className="text-sm text-gray-600 max-w-[160px] truncate hidden md:inline">
                  {user?.full_name || user?.email}
                </span>
                <button
                  type="button"
                  onClick={logout}
                  className="rounded-lg border border-gray-200 bg-white px-3 py-1.5 text-xs font-semibold text-content hover:bg-gray-50 transition cursor-pointer"
                >
                  Sign Out
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-2 sm:gap-3">
                <Link
                  to="/login"
                  className="rounded-lg px-3.5 py-1.5 text-sm font-medium text-content hover:text-primary transition"
                >
                  Sign In
                </Link>
                <Link
                  to="/signup"
                  className="rounded-lg bg-primary px-3.5 py-1.5 text-sm font-semibold text-white shadow-xs hover:bg-primary-600 transition"
                >
                  Sign Up
                </Link>
              </div>
            )}
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="mx-auto w-full max-w-7xl flex-1 px-4 py-8 sm:px-6 lg:px-8">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-200 bg-card">
        <div className="mx-auto max-w-7xl px-4 py-6 text-center text-sm text-gray-500 sm:px-6 lg:px-8">
          &copy; {new Date().getFullYear()} SSC Prep Platform. All rights
          reserved.
        </div>
      </footer>
    </div>
  );
}
