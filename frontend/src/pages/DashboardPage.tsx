import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../hooks";
import { ApiError } from "@/services/api";
import { getTestHistory } from "@/services/tests";
import type { DashboardHistory } from "@/services/tests";

function score(value: number | null) { return value === null ? "—" : Number(value.toFixed(2)).toString(); }
export default function DashboardPage() {
  const { user, token } = useAuth();
  const [history, setHistory] = useState<DashboardHistory | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    if (!token) return;
    getTestHistory(token).then(setHistory).catch((e: unknown) => setError(e instanceof ApiError || e instanceof Error ? e.message : "Unable to load your test history.")).finally(() => setLoading(false));
  }, [token]);
  const welcomeText = user?.full_name ? `Welcome back, ${user.full_name} 👋` : "Welcome back 👋";
  const primaryBtn = "inline-flex items-center justify-center rounded-md bg-[#007BFF] px-6 py-3 text-base font-semibold text-white transition-colors hover:bg-[#0069d9] focus:outline-none focus-visible:ring-2 focus-visible:ring-[#007BFF] focus-visible:ring-offset-2";
  const stats = [
    { label: "Tests Attempted", value: history ? String(history.tests_attempted) : "—" },
    { label: "Best Score", value: history ? score(history.best_score) : "—" },
    { label: "Average Score", value: history ? score(history.average_score) : "—" },
    { label: "Accuracy", value: "—" },
  ];
  return <div className="overflow-x-hidden bg-[#F8F9FA] text-[#2D3436]" style={{ fontFamily: "Inter, 'Noto Sans Devanagari', sans-serif" }}>
    <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6 sm:py-12">
      <section aria-labelledby="welcome-heading" className="flex flex-col gap-6 rounded-lg border border-[#2D3436]/10 bg-white p-6 sm:p-8 md:flex-row md:items-center md:justify-between"><div><h1 id="welcome-heading" className="break-words text-2xl font-bold sm:text-3xl">{welcomeText}</h1><p className="mt-2 text-[#2D3436]/75">Keep building your preparation one test at a time.</p></div><div className="flex shrink-0 flex-col gap-2 md:items-end"><Link to="/ssc" className={primaryBtn}>Start Practice</Link><p className="text-sm text-[#2D3436]/65 md:max-w-xs md:text-right">Choose a subject, difficulty level, and test size to begin.</p></div></section>
      <section aria-labelledby="summary-heading" className="mt-10"><h2 id="summary-heading" className="text-xl font-bold">Preparation Summary</h2><dl className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">{stats.map((stat) => <div key={stat.label} className="rounded-lg border border-[#2D3436]/10 bg-white p-5"><dt className="text-sm font-medium text-[#2D3436]/70">{stat.label}</dt><dd className="mt-2 text-3xl font-bold">{loading ? "…" : stat.value}</dd></div>)}</dl></section>
      <div className="mt-10 grid gap-6 lg:grid-cols-3"><section aria-labelledby="recent-heading" className="rounded-lg border border-[#2D3436]/10 bg-white p-6 sm:p-8 lg:col-span-2"><h2 id="recent-heading" className="text-xl font-bold">Previous Tests</h2>
        {error ? <p role="alert" className="mt-5 rounded bg-red-50 p-4 text-red-800">{error}</p> : loading ? <p className="mt-5 text-sm text-gray-600" role="status">Loading test history…</p> : !history?.previous_tests.length ? <div className="mt-6 rounded-md border border-dashed border-[#2D3436]/20 bg-[#F8F9FA] px-6 py-10 text-center"><p className="text-lg font-semibold">No tests attempted yet.</p><p className="mt-1 text-sm text-[#2D3436]/70">Your completed tests will appear here.</p><Link to="/ssc" className={`${primaryBtn} mt-6`}>Start Your First Test</Link></div> : <ul className="mt-5 divide-y">{history.previous_tests.map((test) => <li key={test.id} className="flex flex-wrap items-center justify-between gap-3 py-4"><div><p className="font-semibold">{test.question_count}-question test</p><p className="text-sm text-gray-600">{new Date(test.started_at).toLocaleString()} · {test.status === "IN_PROGRESS" ? "In progress" : test.status === "AUTO_SUBMITTED" ? "Auto-submitted" : "Completed"}</p></div><div className="flex items-center gap-3"><span className="font-semibold">{test.score === null ? "—" : score(test.score)}</span><Link className="text-sm font-semibold text-[#007BFF] underline" to={test.status === "IN_PROGRESS" ? `/tests/${test.id}` : `/tests/${test.id}/results`}>{test.status === "IN_PROGRESS" ? "Resume" : "Review"}</Link></div></li>)}</ul>}
      </section><aside className="self-start rounded-lg border border-[#2D3436]/10 border-l-4 border-l-[#FF6B35] bg-white p-6"><h2 className="text-base font-semibold">Preparation Tip</h2><p className="mt-2 text-sm leading-relaxed text-[#2D3436]/75">Focus on accuracy first, then gradually work on speed.</p></aside></div>
    </div>
  </div>;
}
