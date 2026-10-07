import { Outlet } from "react-router-dom";

export function RootLayout() {
  return (
    <div className="flex min-h-screen flex-col bg-background">
      {/* Header */}
      <header className="border-b border-gray-200 bg-card">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
          <h1 className="text-xl font-bold text-primary">SSC Prep Platform</h1>
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
