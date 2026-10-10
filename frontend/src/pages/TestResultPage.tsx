import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { useAuth } from "@/hooks";
import { ApiError } from "@/services/api";
import { getTestResult } from "@/services/tests";
import type { TestResult } from "@/services/tests";

function fmtDuration(seconds: number | null) {
  if (seconds === null) return "—";
  return `${Math.floor(seconds / 60)}m ${seconds % 60}s`;
}
export default function TestResultPage() {
  const { testId = "" } = useParams();
  const { token } = useAuth();
  const [result, setResult] = useState<TestResult | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    if (!token) return;
    getTestResult(token, testId).then(setResult).catch((e: unknown) => setError(e instanceof ApiError || e instanceof Error ? e.message : "Unable to load result.")).finally(() => setLoading(false));
  }, [token, testId]);
  return <main className="mx-auto max-w-4xl px-4 py-8 text-[#2D3436] sm:py-12" style={{ fontFamily: "Inter, 'Noto Sans Devanagari', sans-serif" }}>
    <header className="rounded-lg border bg-white p-6 sm:p-8"><p className="font-semibold text-[#007BFF]">SSC Practice · Results</p><h1 className="mt-1 text-2xl font-bold">Test summary</h1>
      {loading ? <p className="mt-4" role="status">Loading results…</p> : error ? <p role="alert" className="mt-4 rounded bg-red-50 p-4 text-red-800">{error}</p> : result && <>
        <dl className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-3">
          {[["Total questions", result.question_count], ["Attempted", result.attempted_count], ["Unanswered", result.unanswered_count], ["Correct", result.correct_count ?? "—"], ["Incorrect", result.wrong_count ?? "—"], ["Time taken", fmtDuration(result.time_taken_seconds)], ["Score", result.score === null ? "Pending" : `${result.score} / ${result.question_count * 2}`]].map(([label, value]) => <div key={String(label)} className="rounded-md bg-[#F8F9FA] p-4"><dt className="text-xs font-semibold uppercase text-gray-500">{label}</dt><dd className="mt-1 text-lg font-bold">{value}</dd></div>)}
        </dl>
        <p className="mt-4 text-sm text-gray-600">Scoring: +2 correct, −0.5 incorrect, 0 unanswered.</p>
        <div className="mt-5 flex gap-3"><Link to="/ssc" className="rounded bg-[#007BFF] px-5 py-2 font-semibold text-white">Practice again</Link><Link to="/dashboard" className="rounded border px-5 py-2 font-semibold">Dashboard</Link></div>
      </>}
    </header>
    {result && !loading && !error && <section className="mt-6 space-y-4" aria-labelledby="review-title"><h2 id="review-title" className="text-xl font-bold">Question review</h2>{result.review.map((question) => <article key={question.question_order} className="rounded-lg border bg-white p-5"><h3 className="font-semibold">{question.question_order}. {question.question_text}</h3><div className="mt-3 space-y-2">{question.options.map((option) => <p key={option.option_key} className={`rounded p-2 text-sm ${option.option_key === question.correct_option ? "bg-green-50 font-semibold text-green-900" : option.option_key === question.selected_option ? "bg-red-50 text-red-900" : ""}`}><span className="mr-2 font-bold">{option.option_key}.</span>{option.option_text}{option.option_key === question.correct_option ? " · Correct answer" : option.option_key === question.selected_option ? " · Your answer" : ""}</p>)}</div><p className="mt-3 text-sm">{question.selected_option ? `Your answer: ${question.selected_option}` : "Unanswered"} · {question.is_correct ? "Correct" : question.selected_option ? "Incorrect" : "Not answered"}</p>{question.explanation && <p className="mt-2 rounded bg-[#F8F9FA] p-3 text-sm">{question.explanation}</p>}</article>)}</section>}
  </main>;
}
