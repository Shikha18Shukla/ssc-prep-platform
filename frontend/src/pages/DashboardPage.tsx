import { Link } from "react-router-dom";
import { useAuth } from "../hooks";

// Placeholder values only. These will be connected to real data
// once the test engine and analytics exist in a later stage.
const SUMMARY_STATS = [
  { label: "Tests Attempted", value: "0" },
  { label: "Best Score", value: "—" },
  { label: "Average Score", value: "—" },
  { label: "Accuracy", value: "—" },
];

export default function DashboardPage() {
  const { user } = useAuth();

  // user can be briefly unavailable while auth is loading
  const welcomeText = user?.full_name
    ? `Welcome back, ${user.full_name} 👋`
    : "Welcome back 👋";

  const primaryBtn =
    "inline-flex items-center justify-center rounded-md bg-[#007BFF] px-6 py-3 text-base font-semibold text-white transition-colors hover:bg-[#0069d9] focus:outline-none focus-visible:ring-2 focus-visible:ring-[#007BFF] focus-visible:ring-offset-2";

  return (
    <div
      className="overflow-x-hidden bg-[#F8F9FA] text-[#2D3436]"
      style={{ fontFamily: "Inter, 'Noto Sans Devanagari', sans-serif" }}
    >
      <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6 sm:py-12">
        {/* Welcome + primary action */}
        <section
          aria-labelledby="welcome-heading"
          className="flex flex-col gap-6 rounded-lg border border-[#2D3436]/10 bg-white p-6 sm:p-8 md:flex-row md:items-center md:justify-between"
        >
          <div className="min-w-0">
            <h1
              id="welcome-heading"
              className="break-words text-2xl font-bold sm:text-3xl"
            >
              {welcomeText}
            </h1>
            <p className="mt-2 text-[#2D3436]/75">
              Keep building your preparation one test at a time.
            </p>
          </div>
          <div className="flex shrink-0 flex-col gap-2 md:items-end">
            <Link to="/ssc" className={primaryBtn}>
              Start Practice
            </Link>
            <p className="text-sm text-[#2D3436]/65 md:max-w-xs md:text-right">
              Choose a subject, difficulty level, and test size to begin.
            </p>
          </div>
        </section>

        {/* Preparation summary */}
        <section aria-labelledby="summary-heading" className="mt-10">
          <h2 id="summary-heading" className="text-xl font-bold">
            Preparation Summary
          </h2>
          <dl className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {SUMMARY_STATS.map((stat) => (
              <div
                key={stat.label}
                className="rounded-lg border border-[#2D3436]/10 bg-white p-5"
              >
                <dt className="text-sm font-medium text-[#2D3436]/70">
                  {stat.label}
                </dt>
                <dd className="mt-2 text-3xl font-bold">{stat.value}</dd>
              </div>
            ))}
          </dl>
        </section>

        {/* Recent tests + tip */}
        <div className="mt-10 grid gap-6 lg:grid-cols-3">
          <section
            aria-labelledby="recent-heading"
            className="rounded-lg border border-[#2D3436]/10 bg-white p-6 sm:p-8 lg:col-span-2"
          >
            <h2 id="recent-heading" className="text-xl font-bold">
              Recent Tests
            </h2>

            <div className="mt-6 flex flex-col items-center rounded-md border border-dashed border-[#2D3436]/20 bg-[#F8F9FA] px-6 py-10 text-center">
              <span className="flex h-12 w-12 items-center justify-center rounded-full bg-[#007BFF]/10 text-[#007BFF]">
                <svg
                  className="h-6 w-6"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth={1.8}
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  viewBox="0 0 24 24"
                  aria-hidden="true"
                >
                  <path d="M9 4h6a1 1 0 0 1 1 1v1H8V5a1 1 0 0 1 1-1Z" />
                  <path d="M8 6H6a1 1 0 0 0-1 1v13a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V7a1 1 0 0 0-1-1h-2" />
                  <path d="M9 13h6M9 17h4" />
                </svg>
              </span>
              <p className="mt-4 text-lg font-semibold">
                No tests attempted yet.
              </p>
              <p className="mt-1 text-sm text-[#2D3436]/70">
                Your completed tests will appear here.
              </p>
              <Link to="/ssc" className={`${primaryBtn} mt-6`}>
                Start Your First Test
              </Link>
            </div>
          </section>

          <aside
            aria-labelledby="tip-heading"
            className="self-start rounded-lg border border-[#2D3436]/10 border-l-4 border-l-[#FF6B35] bg-white p-6"
          >
            <h2 id="tip-heading" className="text-base font-semibold">
              Preparation Tip
            </h2>
            <p className="mt-2 text-sm leading-relaxed text-[#2D3436]/75">
              Focus on accuracy first, then gradually work on speed.
            </p>
          </aside>
        </div>
      </div>
    </div>
  );
}