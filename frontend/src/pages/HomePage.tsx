import type { ReactNode } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../hooks";

type Exam = {
  name: string;
  description: string;
  available: boolean;
};

const EXAMS: Exam[] = [
  { name: "SSC", description: "Focused SSC preparation", available: true },
  { name: "Railway", description: "Railway exam preparation", available: false },
  { name: "Banking", description: "Banking exam preparation", available: false },
  { name: "Police", description: "Police exam preparation", available: false },
];

type Benefit = {
  title: string;
  description: string;
  icon: ReactNode;
};

// Small inline icons so no extra dependency is needed.
const iconProps = {
  className: "h-5 w-5",
  fill: "none",
  stroke: "currentColor",
  strokeWidth: 1.8,
  strokeLinecap: "round" as const,
  strokeLinejoin: "round" as const,
  viewBox: "0 0 24 24",
  "aria-hidden": true,
};

const BENEFITS: Benefit[] = [
  {
    title: "Structured Practice",
    description: "Practice questions in an organized way.",
    icon: (
      <svg {...iconProps}>
        <path d="M4 5h16M4 12h16M4 19h10" />
      </svg>
    ),
  },
  {
    title: "Timed Tests",
    description: "Build speed and accuracy through timed practice.",
    icon: (
      <svg {...iconProps}>
        <circle cx="12" cy="13" r="8" />
        <path d="M12 9v4l2.5 2M9 2h6" />
      </svg>
    ),
  },
  {
    title: "Performance Tracking",
    description: "Understand your progress and identify areas to improve.",
    icon: (
      <svg {...iconProps}>
        <path d="M4 20V10M10 20V4M16 20v-7M22 20H2" />
      </svg>
    ),
  },
];

export default function HomePage() {
  const { isAuthenticated } = useAuth();

  const startLink = isAuthenticated ? "/ssc" : "/login";
  const dashboardLink = isAuthenticated ? "/dashboard" : "/login";

  const primaryBtn =
    "inline-flex items-center justify-center rounded-md bg-[#007BFF] px-6 py-3 text-base font-semibold text-white transition-colors hover:bg-[#0069d9] focus:outline-none focus-visible:ring-2 focus-visible:ring-[#007BFF] focus-visible:ring-offset-2";
  const secondaryBtn =
    "inline-flex items-center justify-center rounded-md border border-[#2D3436]/25 bg-white px-6 py-3 text-base font-semibold text-[#2D3436] transition-colors hover:border-[#007BFF] hover:text-[#007BFF] focus:outline-none focus-visible:ring-2 focus-visible:ring-[#007BFF] focus-visible:ring-offset-2";

  return (
    <div
      className="overflow-x-hidden bg-[#F8F9FA] text-[#2D3436]"
      style={{ fontFamily: "Inter, 'Noto Sans Devanagari', sans-serif" }}
    >
      {/* Hero (unchanged) */}
      <section className="border-b border-[#2D3436]/10 bg-white">
        <div className="mx-auto max-w-6xl px-4 py-16 sm:px-6 sm:py-20 lg:py-28">
          <div className="max-w-2xl">
            <h1 className="text-4xl font-bold leading-tight tracking-tight sm:text-5xl">
              Prepare Smarter. Practice Better.
            </h1>
            <p className="mt-5 max-w-xl text-lg leading-relaxed text-[#2D3436]/75">
              Practice competitive exams with structured questions, timed
              tests, and focused preparation.
            </p>
            <div className="mt-8 flex flex-col gap-3 sm:flex-row">
              <Link to={startLink} className={primaryBtn}>
                Start Preparing
              </Link>
              <Link to={dashboardLink} className={secondaryBtn}>
                View Dashboard
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* 1. Choose Your Exam */}
      <section
        aria-labelledby="exams-heading"
        className="mx-auto max-w-6xl px-4 py-14 sm:px-6 sm:py-16"
      >
        <h2 id="exams-heading" className="text-2xl font-bold sm:text-3xl">
          Choose Your Exam
        </h2>
        <p className="mt-2 max-w-xl text-[#2D3436]/75">
          Start your preparation with the exam you're targeting.
        </p>

        <div className="mt-8 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
          {EXAMS.map((exam) =>
            exam.available ? (
              <article
                key={exam.name}
                className="flex flex-col rounded-lg border-2 border-[#007BFF] bg-white p-6 shadow-md"
              >
                <div className="flex items-center justify-between gap-3">
                  <h3 className="text-2xl font-bold">{exam.name}</h3>
                  <span className="rounded-full bg-[#28C76F]/15 px-3 py-1 text-xs font-semibold text-[#1a8f4d]">
                    Available
                  </span>
                </div>
                <p className="mt-3 flex-1 text-sm leading-relaxed text-[#2D3436]/75">
                  {exam.description}
                </p>
                <Link to="/ssc" className={`${primaryBtn} mt-6 w-full`}>
                  Start Preparing
                </Link>
              </article>
            ) : (
              <article
                key={exam.name}
                aria-disabled="true"
                className="flex flex-col rounded-lg border border-dashed border-[#2D3436]/25 bg-white/60 p-6 opacity-70"
              >
                <div className="flex items-center justify-between gap-3">
                  <h3 className="text-xl font-semibold text-[#2D3436]/70">
                    {exam.name}
                  </h3>
                  <span className="rounded-full bg-[#FF6B35]/15 px-3 py-1 text-xs font-semibold text-[#c2410c]">
                    Coming Soon
                  </span>
                </div>
                <p className="mt-3 flex-1 text-sm leading-relaxed text-[#2D3436]/60">
                  {exam.description}
                </p>
                <button
                  type="button"
                  disabled
                  className="mt-6 w-full cursor-not-allowed rounded-md border border-[#2D3436]/20 bg-[#F8F9FA] px-6 py-3 text-base font-semibold text-[#2D3436]/50"
                >
                  Not available yet
                </button>
              </article>
            )
          )}
        </div>
      </section>

      {/* 2. Why SSC Prep */}
      <section
        aria-labelledby="benefits-heading"
        className="border-y border-[#2D3436]/10 bg-white"
      >
        <div className="mx-auto max-w-6xl px-4 py-14 sm:px-6 sm:py-16">
          <h2 id="benefits-heading" className="text-2xl font-bold sm:text-3xl">
            Why SSC Prep
          </h2>
          <ul className="mt-8 grid gap-5 md:grid-cols-3">
            {BENEFITS.map((benefit) => (
              <li
                key={benefit.title}
                className="rounded-lg border border-[#2D3436]/10 bg-[#F8F9FA] p-6"
              >
                <span className="flex h-10 w-10 items-center justify-center rounded-md bg-[#007BFF]/10 text-[#007BFF]">
                  {benefit.icon}
                </span>
                <h3 className="mt-4 font-semibold">{benefit.title}</h3>
                <p className="mt-1 text-sm leading-relaxed text-[#2D3436]/75">
                  {benefit.description}
                </p>
              </li>
            ))}
          </ul>
        </div>
      </section>

      {/* 3. Final CTA */}
      <section
        aria-labelledby="cta-heading"
        className="mx-auto max-w-6xl px-4 py-14 sm:px-6 sm:py-16"
      >
        <div className="flex flex-col items-start justify-between gap-6 rounded-lg border border-[#2D3436]/10 bg-white p-8 md:flex-row md:items-center">
          <div className="max-w-xl">
            <h2 id="cta-heading" className="text-2xl font-bold">
              Ready to start practicing?
            </h2>
            <p className="mt-2 text-[#2D3436]/75">
              Begin your SSC preparation and build your confidence one test at
              a time.
            </p>
          </div>
          <Link to={startLink} className={`${primaryBtn} w-full md:w-auto`}>
            Start SSC Preparation
          </Link>
        </div>
      </section>
    </div>
  );
}