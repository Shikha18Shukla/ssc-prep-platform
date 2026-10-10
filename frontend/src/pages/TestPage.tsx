import { useCallback, useEffect, useMemo, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { useAuth } from "@/hooks";
import { ApiError } from "@/services/api";
import { getTest, saveTestAnswer, submitTest } from "@/services/tests";
import type { ActiveTest } from "@/services/tests";

function message(error: unknown) { return error instanceof ApiError || error instanceof Error ? error.message : "Unable to load this test."; }
function clock(seconds: number) { return `${Math.floor(seconds / 60).toString().padStart(2, "0")}:${(seconds % 60).toString().padStart(2, "0")}`; }

export default function TestPage() {
  const { testId = "" } = useParams();
  const { token } = useAuth();
  const navigate = useNavigate();
  const [test, setTest] = useState<ActiveTest | null>(null);
  const [current, setCurrent] = useState(0);
  const [remaining, setRemaining] = useState(0);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const load = useCallback(async () => {
    if (!token || !testId) return;
    try {
      setError("");
      const result = await getTest(token, testId);
      setTest(result);
      if (result.status !== "IN_PROGRESS") navigate(`/tests/${testId}/results`, { replace: true });
    } catch (e) { setError(message(e)); }
    finally { setLoading(false); }
  }, [token, testId, navigate]);

  useEffect(() => { void load(); }, [load]);
  useEffect(() => {
    if (!test || test.status !== "IN_PROGRESS") return;
    const update = () => setRemaining(Math.max(0, Math.ceil((Date.parse(test.deadline_at) - Date.now()) / 1000)));
    update();
    const timer = window.setInterval(update, 250);
    return () => window.clearInterval(timer);
  }, [test]);

  const finish = useCallback(async () => {
    if (!token || submitting) return;
    setSubmitting(true);
    try {
      await submitTest(token, testId);
      navigate(`/tests/${testId}/results`, { replace: true });
    } catch (e) { setError(message(e)); setSubmitting(false); }
  }, [token, testId, navigate, submitting]);
  useEffect(() => { if (test?.status === "IN_PROGRESS" && Date.parse(test.deadline_at) <= Date.now()) void finish(); }, [test?.status, test?.deadline_at, remaining, finish]);

  const answers = useMemo(() => new Map(test?.questions.map((question, index) => [index, Boolean(question.selected_option)]) ?? []), [test]);
  async function choose(option: string) {
    if (!test || !token || saving || test.status !== "IN_PROGRESS") return;
    const question = test.questions[current];
    const previous = question.selected_option;
    setTest({ ...test, questions: test.questions.map((item, index) => index === current ? { ...item, selected_option: option } : item) });
    setSaving(true);
    try {
      await saveTestAnswer(token, test.id, question.test_question_id, option);
    } catch (e) {
      setTest((value) => value ? { ...value, questions: value.questions.map((item) => item.test_question_id === question.test_question_id ? { ...item, selected_option: previous } : item) } : value);
      setError(message(e));
      if (Date.parse(test.deadline_at) <= Date.now()) void finish();
    } finally { setSaving(false); }
  }

  if (loading) return <main className="mx-auto max-w-4xl p-6" aria-live="polite">Loading your test…</main>;
  if (!test) return <main className="mx-auto max-w-2xl p-6"><p role="alert" className="rounded bg-red-50 p-4 text-red-800">{error || "Test session unavailable."}</p><Link className="mt-4 inline-block text-blue-700 underline" to="/dashboard">Return to dashboard</Link></main>;
  const question = test.questions[current];
  if (!question) return <main className="p-6">This test has no questions. Please contact support.</main>;
  const answeredCount = [...answers.values()].filter(Boolean).length;

  return <main className="mx-auto max-w-5xl px-4 py-6 text-[#2D3436] sm:py-10" style={{ fontFamily: "Inter, 'Noto Sans Devanagari', sans-serif" }}>
    <header className="mb-5 flex flex-wrap items-center justify-between gap-4 rounded-lg border bg-white p-4">
      <div><p className="text-sm font-semibold text-[#007BFF]">SSC Practice · {test.difficulty}</p><h1 className="text-xl font-bold">Question {current + 1} of {test.question_count}</h1></div>
      <div role="timer" aria-live="off" className={`rounded-md px-4 py-2 text-xl font-bold tabular-nums ${remaining <= 60 ? "bg-red-100 text-red-800" : "bg-blue-50 text-blue-800"}`}>Time left {clock(remaining)}</div>
    </header>
    <div className="grid gap-5 lg:grid-cols-[1fr_250px]">
      <section className="rounded-lg border bg-white p-5 sm:p-8" aria-label="Current question">
        <p className="text-xs font-semibold uppercase tracking-wide text-gray-500">{answeredCount} of {test.question_count} answered</p>
        <h2 className="mt-4 whitespace-pre-wrap text-lg font-semibold leading-relaxed">{question.question_text}</h2>
        <div className="mt-6 grid gap-3">
          {question.options.map((option) => <button key={option.option_key} type="button" disabled={saving || submitting || remaining <= 0} aria-pressed={question.selected_option === option.option_key} onClick={() => void choose(option.option_key)} className={`flex min-h-14 items-start gap-3 rounded-lg border p-4 text-left transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#007BFF] disabled:opacity-60 ${question.selected_option === option.option_key ? "border-[#007BFF] bg-blue-50" : "hover:border-[#007BFF]/60"}`}><span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full border font-semibold">{option.option_key}</span><span>{option.option_text}</span></button>)}
        </div>
        {saving && <p className="mt-3 text-sm text-gray-600" role="status">Saving answer…</p>}
        {error && <p className="mt-3 rounded bg-red-50 p-3 text-sm text-red-800" role="alert">{error} <button className="ml-2 underline" onClick={() => void load()}>Reconnect</button></p>}
        <div className="mt-7 flex flex-wrap justify-between gap-3 border-t pt-5">
          <button type="button" disabled={current === 0} onClick={() => setCurrent((value) => value - 1)} className="rounded border px-4 py-2 disabled:opacity-45">← Previous</button>
          {current < test.questions.length - 1 ? <button type="button" onClick={() => setCurrent((value) => value + 1)} className="rounded bg-[#007BFF] px-5 py-2 font-semibold text-white">Next →</button> : <button type="button" disabled={submitting || saving} onClick={() => void finish()} className="rounded bg-[#FF6B35] px-5 py-2 font-semibold text-white disabled:opacity-60">{submitting ? "Submitting…" : "Submit Test"}</button>}
        </div>
      </section>
      <aside className="h-fit rounded-lg border bg-white p-4" aria-label="Question palette">
        <h2 className="font-bold">Question palette</h2><p className="mt-1 text-xs text-gray-600">Green = answered · gray = unanswered</p>
        <div className="mt-4 grid grid-cols-5 gap-2">{test.questions.map((item, index) => <button key={item.test_question_id} type="button" aria-label={`Go to question ${index + 1}${item.selected_option ? ", answered" : ", unanswered"}`} aria-current={index === current ? "step" : undefined} onClick={() => setCurrent(index)} className={`h-10 rounded border text-sm font-semibold ${index === current ? "ring-2 ring-[#007BFF]" : ""} ${item.selected_option ? "border-green-300 bg-green-100 text-green-900" : "bg-gray-100"}`}>{index + 1}</button>)}</div>
        <button type="button" disabled={submitting || saving} onClick={() => void finish()} className="mt-5 w-full rounded border border-[#FF6B35] px-4 py-2 font-semibold text-[#a7471a] disabled:opacity-50">Submit test</button>
      </aside>
    </div>
    <p className="mt-4 text-center text-xs text-gray-500">Your answers are saved to this session. Refreshing will not change the questions or reset the deadline.</p>
  </main>;
}
