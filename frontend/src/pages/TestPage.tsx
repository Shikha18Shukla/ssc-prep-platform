import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { useAuth } from "@/hooks";
import { ApiError } from "@/services/api";
import { getTest, saveTestAnswer, submitTest } from "@/services/tests";
import type { ActiveTest } from "@/services/tests";

function message(error: unknown) { return error instanceof ApiError || error instanceof Error ? error.message : "Unable to load this test."; }
function clock(seconds: number) { return `${Math.floor(seconds / 60).toString().padStart(2, "0")}:${(seconds % 60).toString().padStart(2, "0")}`; }
function pendingKey(testId: string) { return `ssc_pending_answers:${testId}`; }
function readPending(testId: string): Record<string, string> {
  try {
    const value = JSON.parse(sessionStorage.getItem(pendingKey(testId)) || "{}");
    return value && typeof value === "object" && !Array.isArray(value) ? value as Record<string, string> : {};
  } catch { return {}; }
}
function writePending(testId: string, answers: Record<string, string>): boolean {
  try {
    if (Object.keys(answers).length) sessionStorage.setItem(pendingKey(testId), JSON.stringify(answers));
    else sessionStorage.removeItem(pendingKey(testId));
    return true;
  } catch { return false; }
}

export default function TestPage() {
  const { testId = "" } = useParams();
  const { token } = useAuth();
  const navigate = useNavigate();
  const [test, setTest] = useState<ActiveTest | null>(null);
  const [current, setCurrent] = useState(0);
  const [remaining, setRemaining] = useState(0);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [pendingCount, setPendingCount] = useState(0);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const autoSubmitStarted = useRef(false);

  const syncPending = useCallback(async (): Promise<boolean> => {
    if (!token || !testId) return false;
    const pending = readPending(testId);
    for (const [questionId, selectedOption] of Object.entries(pending)) {
      try {
        await saveTestAnswer(token, testId, questionId, selectedOption);
        delete pending[questionId];
        writePending(testId, pending);
      } catch (e) {
        if (e instanceof ApiError && e.status === 409) {
          try {
            const latest = await getTest(token, testId);
            if (latest.status !== "IN_PROGRESS") {
              const unconfirmed = Object.keys(pending).length;
              writePending(testId, {});
              setPendingCount(0);
              navigate(`/tests/${testId}/results${unconfirmed ? `?unconfirmed=${unconfirmed}` : ""}`, { replace: true });
              return false;
            }
          } catch { /* Keep the local draft if status could not be checked. */ }
        }
        setPendingCount(Object.keys(pending).length);
        setError(`An answer is still waiting to save. Keep this tab open or retry when connected. ${message(e)}`);
        return false;
      }
    }
    setPendingCount(0);
    setError("");
    return true;
  }, [token, testId, navigate]);

  const load = useCallback(async () => {
    if (!token || !testId) return;
    try {
      setError("");
      const result = await getTest(token, testId);
      if (result.status !== "IN_PROGRESS") {
        const unconfirmed = Object.keys(readPending(testId)).length;
        writePending(testId, {});
        setPendingCount(0);
        navigate(`/tests/${testId}/results${unconfirmed ? `?unconfirmed=${unconfirmed}` : ""}`, { replace: true });
      } else {
        const pending = readPending(testId);
        setPendingCount(Object.keys(pending).length);
        setTest({
          ...result,
          questions: result.questions.map((question) => ({
            ...question,
            selected_option: pending[question.test_question_id] || question.selected_option,
          })),
        });
        if (Object.keys(pending).length) void syncPending();
      }
    } catch (e) {
      setPendingCount(Object.keys(readPending(testId)).length);
      setError(message(e));
    }
    finally { setLoading(false); }
  }, [token, testId, navigate, syncPending]);

  useEffect(() => { void load(); }, [load]);
  useEffect(() => {
    if (!test || test.status !== "IN_PROGRESS") return;
    const update = () => setRemaining(Math.max(0, Math.ceil((Date.parse(test.deadline_at) - Date.now()) / 1000)));
    update();
    const timer = window.setInterval(update, 250);
    return () => window.clearInterval(timer);
  }, [test]);

  const finish = useCallback(async () => {
    if (!token || submitting || saving) return;
    setSubmitting(true);
    try {
      if (Object.keys(readPending(testId)).length && !(await syncPending())) {
        setSubmitting(false);
        return;
      }
      await submitTest(token, testId);
      writePending(testId, {});
      navigate(`/tests/${testId}/results`, { replace: true });
    } catch (e) { setError(message(e)); setSubmitting(false); }
  }, [token, testId, navigate, submitting, saving, syncPending]);
  useEffect(() => {
    if (test?.status !== "IN_PROGRESS") return;
    const retry = async () => {
      if (await syncPending() && Date.parse(test.deadline_at) <= Date.now()) {
        autoSubmitStarted.current = false;
        void finish();
      }
    };
    window.addEventListener("online", retry);
    return () => window.removeEventListener("online", retry);
  }, [test?.status, test?.deadline_at, syncPending, finish]);
  useEffect(() => {
    if (test?.status === "IN_PROGRESS" && Date.parse(test.deadline_at) <= Date.now() && !autoSubmitStarted.current) {
      autoSubmitStarted.current = true;
      void finish();
    }
  }, [test?.status, test?.deadline_at, remaining, finish]);

  const answers = useMemo(() => new Map(test?.questions.map((question, index) => [index, Boolean(question.selected_option)]) ?? []), [test]);
  async function choose(option: string) {
    if (!test || !token || saving || test.status !== "IN_PROGRESS") return;
    const question = test.questions[current];
    setTest({ ...test, questions: test.questions.map((item, index) => index === current ? { ...item, selected_option: option } : item) });
    const pending = readPending(test.id);
    pending[question.test_question_id] = option;
    const draftStored = writePending(test.id, pending);
    setPendingCount(Object.keys(pending).length);
    setSaving(true);
    try {
      await saveTestAnswer(token, test.id, question.test_question_id, option);
      delete pending[question.test_question_id];
      writePending(test.id, pending);
      setPendingCount(Object.keys(pending).length);
      setError("");
    } catch (e) {
      setError(draftStored
        ? `Answer not confirmed by the server. Your choice is kept in this tab and will retry when connected. ${message(e)}`
        : `Answer could not be saved locally or confirmed by the server. Keep this page open and retry. ${message(e)}`);
      if (Date.parse(test.deadline_at) <= Date.now()) void finish();
    } finally { setSaving(false); }
  }

  if (loading) return <main className="mx-auto max-w-4xl p-6" aria-live="polite">Loading your test…</main>;
  if (!test) return <main className="mx-auto max-w-2xl p-6">
    <p role="alert" className="rounded bg-red-50 p-4 text-red-800">{error || "Test session unavailable."}</p>
    {pendingCount > 0 && <p className="mt-3 rounded bg-amber-50 p-3 text-amber-950">{pendingCount} answer{pendingCount === 1 ? " is" : "s are"} saved in this tab and still need server confirmation. Retry to reconnect before leaving this page.</p>}
    <button type="button" className="mt-4 rounded bg-[#007BFF] px-4 py-2 font-semibold text-white" onClick={() => void load()}>Retry connection</button>
    <Link className="ml-4 inline-block text-blue-700 underline" to="/dashboard">Return to dashboard</Link>
  </main>;
  const question = test.questions[current];
  if (!question) return <main className="p-6">This test has no questions. Please contact support.</main>;
  const answeredCount = [...answers.values()].filter(Boolean).length;

  return <main className="mx-auto max-w-5xl px-4 py-6 text-[#2D3436] sm:py-10">
    <header className="mb-5 flex flex-wrap items-center justify-between gap-4 rounded-lg border bg-white p-4">
      <div><p className="text-sm font-semibold text-[#007BFF]">SSC Practice · {test.test_type === "MISCELLANEOUS" ? "Miscellaneous" : "Chapter-wise"}{test.difficulty ? ` · ${test.difficulty}` : ""}</p><h1 className="text-xl font-bold">Question {current + 1} of {test.question_count}</h1></div>
      <div role="timer" aria-live="off" className={`rounded-md px-4 py-2 text-xl font-bold tabular-nums ${remaining <= 60 ? "bg-red-100 text-red-800" : "bg-blue-50 text-blue-800"}`}>Time left {clock(remaining)}</div>
    </header>
    <div className="grid gap-5 lg:grid-cols-[1fr_250px]">
      <section className="rounded-lg border bg-white p-5 sm:p-8" aria-label="Current question">
        <p className="text-xs font-semibold uppercase tracking-wide text-gray-500">{answeredCount} of {test.question_count} answered</p>
        <h2 className="mt-4 whitespace-pre-wrap text-lg font-semibold leading-relaxed">{question.question_text}</h2>
        {question.image_url && <img className="mx-auto mt-5 max-h-[32rem] w-full rounded border object-contain" src={question.image_url} alt="Question figure and answer choices A through D" />}
        <div className="mt-6 grid gap-3">
          {question.options.map((option) => <button key={option.option_key} type="button" disabled={saving || submitting || remaining <= 0} aria-pressed={question.selected_option === option.option_key} onClick={() => void choose(option.option_key)} className={`flex min-h-14 items-start gap-3 rounded-lg border p-4 text-left transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#007BFF] disabled:opacity-60 ${question.selected_option === option.option_key ? "border-[#007BFF] bg-blue-50" : "hover:border-[#007BFF]/60"}`}><span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full border font-semibold">{option.option_key}</span><span>{option.option_text}</span></button>)}
        </div>
        {saving && <p className="mt-3 text-sm text-gray-600" role="status">Saving answer…</p>}
        {pendingCount > 0 && <p className="mt-3 text-sm font-medium text-amber-800" role="status">{pendingCount} answer{pendingCount === 1 ? "" : "s"} waiting for server confirmation.</p>}
        {error && <p className="mt-3 rounded bg-red-50 p-3 text-sm text-red-800" role="alert">{error} <button className="ml-2 underline" onClick={() => void load()}>Reconnect</button>{pendingCount > 0 && <button className="ml-2 underline" onClick={() => void syncPending()}>Retry save</button>}</p>}
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
    <p className="mt-4 text-center text-xs text-gray-500">Confirmed answers are saved on the server. Unconfirmed choices are kept in this browser tab and retry when connectivity returns. Refreshing does not change the questions or reset the deadline.</p>
  </main>;
}
