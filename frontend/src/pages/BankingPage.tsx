import { useEffect, useMemo, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "@/hooks";
import { ApiError } from "@/services/api";
import { getActiveExams, getExamSubjects, getSubjectChapterCounts, getSubjectChapters } from "@/services/catalog";
import { createTest, getTestAvailability } from "@/services/tests";
import type { CatalogChapter, CatalogExam, CatalogSubject } from "@/types";

type Mode = "CHAPTER_WISE" | "MISCELLANEOUS";
const card = "w-full rounded-lg border border-[#2D3436]/15 bg-white p-5 text-left transition hover:border-[#007BFF] hover:shadow-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#007BFF]";
const testCard = card + " h-full flex flex-col";
const button = "inline-flex min-h-11 items-center justify-center rounded-md bg-[#007BFF] px-5 py-2.5 text-sm font-semibold text-white hover:bg-[#0069d9] disabled:cursor-not-allowed disabled:opacity-50";
const secondary = "inline-flex min-h-11 items-center justify-center rounded-md border border-[#2D3436]/25 bg-white px-5 py-2.5 text-sm font-semibold";
const message = (e: unknown) => e instanceof ApiError || e instanceof Error ? e.message : "Unable to load Banking practice.";

// Current Affairs test configurations (defined outside component for type safety)
const caTestConfigs = {
  1: { section: 'current_affairs_test_1', count: 50, minutes: 35, title: 'Current Affairs Test 1', subtitle: '50 Questions · 35 Minutes' },
  2: { section: 'current_affairs_test_2', count: 100, minutes: 70, title: 'Current Affairs Test 2', subtitle: '100 Questions · 70 Minutes' },
  3: { section: 'current_affairs_test_3', count: 150, minutes: 105, title: 'Current Affairs Test 3', subtitle: '150 Questions · 105 Minutes' },
  4: { section: 'current_affairs_test_4', count: 70, minutes: 49, title: 'Current Affairs Test 4', subtitle: '70 Questions · 49 Minutes' },
  5: { section: 'current_affairs_test_5', count: 74, minutes: 52, title: 'Current Affairs Test 5', subtitle: '74 Questions · 52 Minutes' },
  6: { section: 'current_affairs_test_6', count: 56, minutes: 40, title: 'Current Affairs Test 6', subtitle: '56 Questions · 40 Minutes' },
} as const;
const poTestConfigs = {
  1: { section: "banking_po_current_affairs_test_1", count: 56, minutes: 40, title: "Current Affairs Test 1", subtitle: "56 Questions · 40 Minutes" },
  2: { section: "banking_po_current_affairs_test_2", count: 70, minutes: 49, title: "Current Affairs Test 2", subtitle: "70 Questions · 49 Minutes" },
  3: { section: "banking_po_current_affairs_test_3", count: 100, minutes: 70, title: "Current Affairs Test 3", subtitle: "100 Questions · 70 Minutes" },
  4: { section: "banking_po_current_affairs_test_4", count: 75, minutes: 53, title: "Current Affairs Test 4", subtitle: "75 Questions · 53 Minutes" },
  5: { section: "banking_po_current_affairs_test_5", count: 75, minutes: 53, title: "Current Affairs Test 5", subtitle: "75 Questions · 53 Minutes" },
  6: { section: "banking_po_current_affairs_test_6", count: 50, minutes: 35, title: "Current Affairs Test 6", subtitle: "50 Questions · 35 Minutes" },
  7: { section: "banking_po_current_affairs_test_7", count: 75, minutes: 53, title: "Current Affairs Test 7", subtitle: "75 Questions · 53 Minutes" },
} as const;

// Maths chapters are split into four progressive parts.  Section names are
// unique per exam because the backend filters questions by section alone.
const mathsChapterKeys: Record<string, string> = {
  "vedic-maths-tricks-calculation-techniques": "vedic_maths",
  simplification: "simplification",
  approximation: "approximation",
  "missing-number-series": "missing_series",
  "wrong-number-series": "wrong_series",
  "quadratic-equations": "quadratic_equations",
  "number-system": "number_system",
  percentage: "percentage",
  "ratio-and-proportion": "ratio_proportion",
  "profit-loss-and-discount": "profit_loss_discount",
  "simple-interest": "simple_interest",
  "compound-interest": "compound_interest",
  "mixture-and-alligation": "mixture_alligation",
  "problems-on-age": "problems_on_age",
  partnership: "partnership",
  "time-and-work": "time_and_work",
  "pipe-and-cistern": "pipe_and_cistern",
  average: "average",
  "speed-time-and-distance": "speed_time_distance",
  "problems-on-trains": "problems_on_trains",
  "boats-and-streams": "boats_and_streams",
  "mensuration-2d": "mensuration_2d",
  "mensuration-3d": "mensuration_3d",
  permutations: "permutations",
  combinations: "combinations",
  probability: "probability",
  "data-interpretation": "data_interpretation",
  "caselet-data-interpretation": "caselet_data_interpretation",
  "percentage-arithmetic-mains": "percentage_arithmetic_mains",
  "percentage-data-interpretation-mains": "percentage_data_interpretation_mains",
  "ratio-arithmetic-mains": "ratio_arithmetic_mains",
  "ratio-data-interpretation-mains": "ratio_data_interpretation_mains",
  "profit-and-loss-mains": "profit_and_loss_mains",
  "profit-and-loss-data-interpretation": "profit_and_loss_data_interpretation",
  "mixture-and-alligation-mains": "mixture_alligation_mains",
  "mixture-and-alligation-data-interpretation": "mixture_alligation_data_interpretation",
  "ages-mains": "ages_mains",
  "ages-data-interpretation": "ages_data_interpretation",
  "partnership-mains": "partnership_mains",
  "partnership-data-interpretation": "partnership_data_interpretation",
  "time-and-work-mains": "time_and_work_mains",
  "time-and-work-data-interpretation": "time_and_work_data_interpretation",
  "time-speed-and-distance-mains": "time_speed_and_distance_mains",
  "simple-and-compound-interest-mains": "simple_and_compound_interest_mains",
  "simple-and-compound-interest-data-interpretation": "simple_and_compound_interest_data_interpretation",
  "pipe-and-cistern-mains": "pipe_and_cistern_mains",
  "pipe-and-cistern-data-interpretation": "pipe_and_cistern_data_interpretation",
  "trains-mains": "trains_mains",
  "trains-data-interpretation": "trains_data_interpretation",
  "boats-and-streams-mains": "boats_and_streams_mains",
  "boats-and-streams-data-interpretation": "boats_and_streams_data_interpretation",
  "probability-mains": "probability_mains",
  "probability-data-interpretation": "probability_data_interpretation",
};
const mathsParts = [
  { part: 1, count: 15, minutes: 10.5, title: "Part 1", subtitle: "15 Questions · 10.5 Minutes", level: "Easy" },
  { part: 2, count: 20, minutes: 14, title: "Part 2", subtitle: "20 Questions · 14 Minutes", level: "Easy to Moderate" },
  { part: 3, count: 30, minutes: 21, title: "Part 3", subtitle: "30 Questions · 21 Minutes", level: "Moderate to Advanced" },
  { part: 4, count: 55, minutes: 38.5, title: "Part 4", subtitle: "55 Questions · 38.5 Minutes", level: "Advanced" },
] as const;

// English, General/Banking Awareness and Computer chapters are split into
// three fixed sections for Banking Clerk and Banking PO only.
const threeSectionSubjects = new Set(["english", "general-banking-awareness", "computer"]);
const threeSectionExamSlugs = new Set(["banking-clerk", "banking-po"]);
const threeSectionParts = [
  { part: 1, count: 10, minutes: 7, title: "Section 1", subtitle: "10 Questions · 7 Minutes" },
  { part: 2, count: 15, minutes: 10.5, title: "Section 2", subtitle: "15 Questions · 10.5 Minutes" },
  { part: 3, count: 15, minutes: 10.5, title: "Section 3", subtitle: "15 Questions · 10.5 Minutes" },
] as const;
const slugKey = (value: string) => value.replace(/-/g, "_");
const usesThreeSections = (item: CatalogExam | null, subject: CatalogSubject | null) =>
  Boolean(item && threeSectionExamSlugs.has(item.slug) && subject && threeSectionSubjects.has(subject.slug));

export default function BankingPage() {
  const { token } = useAuth(); const navigate = useNavigate();
  const [exams, setExams] = useState<CatalogExam[]>([]); const [subjects, setSubjects] = useState<CatalogSubject[]>([]); const [chapters, setChapters] = useState<CatalogChapter[]>([]);
  const [exam, setExam] = useState<CatalogExam | null>(null); const [subject, setSubject] = useState<CatalogSubject | null>(null); const [mode, setMode] = useState<Mode | null>(null);
  const [mathsChapter, setMathsChapter] = useState<CatalogChapter | null>(null);
  const [threeSectionChapter, setThreeSectionChapter] = useState<CatalogChapter | null>(null);
  const [step, setStep] = useState(0); const [selected, setSelected] = useState<string[]>([]); const [counts, setCounts] = useState<Record<string, number>>({}); const [questionCount, setQuestionCount] = useState<number | null>(null);
  const [loading, setLoading] = useState(false); const [error, setError] = useState("");

  useEffect(() => { if (!token) return; getActiveExams(token).then(items => setExams(items.filter(x => x.slug.startsWith("banking-")))).catch(e => setError(message(e))); }, [token]);

  const selectedChapters = useMemo(() => chapters.filter(c => selected.includes(c.id)), [chapters, selected]);

  async function chooseExam(item: CatalogExam) {
    if (!token) return;
    setExam(item); setError(""); setLoading(true);
    setMode(null); setQuestionCount(null);
    try { setSubjects(await getExamSubjects(token, item.id)); setStep(1); }
    catch (e) { setError(message(e)); }
    finally { setLoading(false); }
  }

  async function chooseSubject(item: CatalogSubject) {
    if (!token) return;
    setSubject(item); setError(""); setLoading(true);
    setMode(null); setQuestionCount(null);
    try {
      const [list, availability] = await Promise.all([
        getSubjectChapters(token, item.id),
        getSubjectChapterCounts(token, item.id),
      ]);
      setChapters(list);
      setSelected([]);
      setMathsChapter(null);
      setThreeSectionChapter(null);
      setCounts(Object.fromEntries(availability.map(row => [row.chapter_id, row.question_count])));
      // Current Affairs: step 2 shows CA test cards; others: step 2 shows test mode selection
      setStep(2);
    } catch (e) {
      setError(message(e));
    } finally {
      setLoading(false);
    }
  }

  async function startCAFTest(section: string, count: number, chapterId: string | null = null) {
    if (!token || !exam || !subject) return;
    const cfg = { section, count };
    setLoading(true); setError("");
    try {
      const selection = {
        exam_id: exam.id,
        subject_id: subject.id,
        test_type: "CHAPTER_WISE" as Mode,
        chapter_id: chapterId,
        chapter_ids: undefined,
        subcategory_id: null,
        difficulty: null,
        section_filter: cfg.section,
      };
      const availability = await getTestAvailability(token, { ...selection, question_count: cfg.count });
      if (!availability.can_satisfy_request) {
        setError("There are no questions available for this test selection yet.");
        return;
      }
      const createPayload = {
        exam_id: exam.id,
        subject_id: subject.id,
        test_type: "CHAPTER_WISE" as Mode,
        chapter_id: chapterId,
        chapter_ids: undefined,
        subcategory_id: null,
        difficulty: null,
        question_count: cfg.count,
        section_filter: cfg.section,
      };
      const attempt = await createTest(token, createPayload);
      navigate(`/tests/${attempt.id}`);
    } catch (e) {
      setError(message(e));
    } finally { setLoading(false); }
  }

  function startMathsPart(part: number, count: number) {
    if (!exam || !mathsChapter) return;
    const chapterKey = mathsChapterKeys[mathsChapter.slug];
    if (!chapterKey) {
      setError("This chapter does not have a Maths test yet.");
      return;
    }
    const section = `${exam.slug.replace(/-/g, "_")}_maths_${chapterKey}_part_${part}`;
    void startCAFTest(section, count, mathsChapter.id);
  }

  function startThreeSectionPart(part: number, count: number) {
    if (!exam || !subject || !threeSectionChapter || !usesThreeSections(exam, subject)) return;
    const section = `${slugKey(exam.slug)}_${slugKey(subject.slug)}_${slugKey(threeSectionChapter.slug)}_part_${part}`;
    void startCAFTest(section, count, threeSectionChapter.id);
  }

  async function startTestMiscellaneous() {
    if (!token || !exam || !subject || !mode || !selected.length) return;
    setLoading(true); setError("");
    try {
      const selection = {
        exam_id: exam.id,
        subject_id: subject.id,
        test_type: mode,
        chapter_id: mode === "CHAPTER_WISE" ? selected[0] : null,
        chapter_ids: mode === "MISCELLANEOUS" ? selected : undefined,
        subcategory_id: null,
        difficulty: null,
      };
      const availability = await getTestAvailability(token, selection);
      const count = questionCount ?? availability.allowed_question_counts[availability.allowed_question_counts.length - 1];
      if (!count || !availability.allowed_question_counts.includes(count)) {
        setError("There are no questions available for this selection yet. Please check back after Banking questions are uploaded.");
        return;
      }
      const attempt = await createTest(token, { ...selection, question_count: count });
      navigate(`/tests/${attempt.id}`);
    } catch (e) {
      setError(message(e));
    } finally { setLoading(false); }
  }

  const availableTotal = selectedChapters.reduce((n, c) => n + (counts[c.id] ?? 0), 0);

  return (
    <main className="mx-auto max-w-4xl text-[#2D3436]">
      <div className="rounded-lg border border-[#2D3436]/10 bg-white p-5 shadow-sm sm:p-8">
        <header className="flex flex-col justify-between gap-4 sm:flex-row sm:items-start">
          <div>
            <p className="text-sm font-semibold uppercase tracking-wide text-[#007BFF]">Banking Practice</p>
            <h1 className="mt-1 text-2xl font-bold sm:text-3xl">
              {step === 0 && "Choose an exam"}
              {step === 1 && "Choose a subject"}
              {step === 2 && (subject?.slug === 'current-affairs' ? "Current Affairs Practice Tests" : subject?.slug === 'math-quant' ? "Choose a Maths chapter" : usesThreeSections(exam, subject) ? "Choose a chapter" : "Choose a test mode")}
              {step === 3 && (subject?.slug === 'math-quant' ? `${mathsChapter?.name ?? "Maths"} · Choose a part` : usesThreeSections(exam, subject) ? `${threeSectionChapter?.name ?? "Chapter"} · Choose a section` : mode === "CHAPTER_WISE" ? "Choose a chapter" : "Choose chapters")}
            </h1>
            <p className="mt-2 text-sm text-gray-600">{exam?.name}{subject ? ` · ${subject.name}` : ""}</p>
          </div>
          <Link to="/dashboard" className={secondary}>Back to Dashboard</Link>
        </header>

        {step > 0 && (
          <button type="button" className={`${secondary} mt-5`} onClick={() => { setError(""); setStep(step - 1); }}>
            ← Back
          </button>
        )}

        {error && <p role="alert" className="mt-4 rounded-md bg-red-50 p-4 text-sm text-red-800">{error}</p>}
        {loading && <p role="status" className="mt-4 text-sm">Loadingâ€¦</p>}

        {/* Step 0: Choose exam */}
        {!loading && step === 0 && (
          <div className="mt-5 grid gap-3 sm:grid-cols-3">
            {exams.map(item => (
              <button key={item.id} type="button" className={card} onClick={() => void chooseExam(item)}>
                <span className="text-lg font-bold">{item.name.replace("Banking ", "")}</span>
                <span className="mt-1 block text-sm text-gray-600">Banking exam preparation</span>
              </button>
            ))}
            {!exams.length && <p className="text-sm text-gray-600">Banking syllabus is not available yet. Apply the latest database migration and reload.</p>}
          </div>
        )}

        {/* Step 1: Choose subject */}
        {step === 1 && (
          <div className="mt-5 grid gap-3 sm:grid-cols-2">
            {subjects.map(item => (
              <button key={item.id} type="button" className={card} onClick={() => void chooseSubject(item)}>
                <span className="text-lg font-bold">{item.name}</span>
                <span className="mt-1 block text-sm text-gray-600">View chapters</span>
              </button>
            ))}
          </div>
        )}

        {/* Step 2: Current Affairs â†’ show 6 test cards; others â†’ show test mode selection */}
        {step === 2 && (
          <div className="mt-5">
            {subject && subject.slug === 'current-affairs' ? (
              /* Current Affairs: Show 6 test cards immediately */
              <div className="space-y-4">
                <h3 className="font-semibold text-lg text-center">Current Affairs Practice Tests</h3>
                  <div className="grid gap-4 sm:grid-cols-2">
                    {exam?.slug === 'banking-po' && Object.values(poTestConfigs).map((cfg) => (
                      <div key={cfg.section} className={testCard}>
                        <h3 className="font-semibold text-sm uppercase text-[#007BFF]">{cfg.title}</h3>
                        <p className="mt-1 text-sm text-gray-600">{cfg.count} Questions · {cfg.minutes} Minutes</p>
                        <button type="button" className={`${button} mt-3`} onClick={() => void startCAFTest(cfg.section, cfg.count)}>Start Test</button>
                      </div>
                    ))}
                    {exam?.slug !== 'banking-po' && Object.values(caTestConfigs).map((cfg) => (
                      <div key={cfg.section} className={testCard}>
                        <h3 className="font-semibold text-sm uppercase text-[#007BFF]">{cfg.title}</h3>
                        <p className="mt-1 text-sm text-gray-600">{cfg.count} Questions · {cfg.minutes} Minutes</p>
                        <button type="button" className={`${button} mt-3`} onClick={() => void startCAFTest(cfg.section, cfg.count)}>Start Test</button>
                      </div>
                    ))}
                 </div>
              </div>
            ) : subject?.slug === 'math-quant' ? (
              /* Maths: choose a chapter, then one of its four parts */
              <div className="grid gap-3 sm:grid-cols-2">
                {chapters.map((chapter) => {
                  const count = counts[chapter.id] ?? 0;
                  const hasParts = Boolean(mathsChapterKeys[chapter.slug]);
                  return (
                    <button
                      key={chapter.id}
                      type="button"
                      className={card}
                      disabled={!hasParts || count === 0}
                      onClick={() => { setMathsChapter(chapter); setStep(3); }}
                    >
                      <span className="text-lg font-bold">{chapter.name}</span>
                      <span className="mt-1 block text-sm text-gray-600">
                        {hasParts && count > 0 ? `${count} questions · 4 parts` : "Question bank coming soon"}
                      </span>
                    </button>
                  );
                })}
                {!chapters.length && <p className="text-sm text-gray-600">No Maths chapters are available yet.</p>}
              </div>
            ) : usesThreeSections(exam, subject) ? (
              /* Three-section subjects: choose a chapter, then one of its sections */
              <div className="grid gap-3 sm:grid-cols-2">
                {chapters.map((chapter) => {
                  const count = counts[chapter.id] ?? 0;
                  return (
                    <button
                      key={chapter.id}
                      type="button"
                      className={card}
                      disabled={count === 0}
                      onClick={() => { setThreeSectionChapter(chapter); setStep(3); }}
                    >
                      <span className="text-lg font-bold">{chapter.name}</span>
                      <span className="mt-1 block text-sm text-gray-600">
                        {count > 0 ? `${count} questions · 3 sections` : "Question bank coming soon"}
                      </span>
                    </button>
                  );
                })}
                {!chapters.length && <p className="text-sm text-gray-600">No chapters are available yet for this subject.</p>}
              </div>
            ) : (
              /* Non-Current Affairs: Show test mode selection */
              <div className="grid gap-3 sm:grid-cols-2">
                {([["CHAPTER_WISE", "Chapter-wise Test", "Practice one selected chapter at a time."], ["MISCELLANEOUS", "Mix Questions", "Random questions from selected chapters."]] as const).map(([id, title, desc]) => (
                  <button key={id} type="button" className={card} onClick={() => { setMode(id); setStep(3); }}>
                    <span className="text-lg font-bold">{title}</span>
                    <span className="mt-1 block text-sm text-gray-600">{desc}</span>
                  </button>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Step 3 (Maths): four progressive parts for the selected chapter */}
        {step === 3 && subject?.slug === 'math-quant' && mathsChapter && (
          <div className="mt-5 grid gap-4 sm:grid-cols-2">
            {mathsParts.map((p) => (
              <div key={p.part} className={testCard}>
                <h3 className="font-semibold text-sm uppercase text-[#007BFF]">{p.title}</h3>
                <p className="mt-1 text-sm text-gray-600">{p.subtitle}</p>
                <p className="mt-1 text-xs font-semibold uppercase tracking-wide text-gray-500">{p.level}</p>
                <button type="button" className={`${button} mt-3`} onClick={() => startMathsPart(p.part, p.count)}>Start Test</button>
              </div>
            ))}
          </div>
        )}

        {/* Step 3: three fixed sections for English, General/Banking Awareness and Computer */}
        {step === 3 && usesThreeSections(exam, subject) && threeSectionChapter && (
          <div>
            <div className="mt-5 flex flex-wrap items-center justify-between gap-3">
              <button
                type="button"
                className={secondary}
                onClick={() => { setError(""); setThreeSectionChapter(null); setStep(2); }}
              >
                ← Back to chapters
              </button>
              <p className="text-sm text-gray-600">40 questions across 3 sections</p>
            </div>
            <div className="mt-4 grid gap-4 sm:grid-cols-2">
              {threeSectionParts.map((p) => (
                <div key={p.part} className={testCard}>
                  <h3 className="font-semibold text-sm uppercase text-[#007BFF]">{p.title}</h3>
                  <p className="mt-1 text-sm text-gray-600">{p.subtitle}</p>
                  <p className="mt-1 text-xs font-semibold uppercase tracking-wide text-gray-500">{threeSectionChapter.name}</p>
                  <button type="button" className={`${button} mt-3`} onClick={() => startThreeSectionPart(p.part, p.count)}>Start Test</button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Step 3: Chapter selection and test configuration (for the remaining subjects) */}
        {step === 3 && subject?.slug !== 'math-quant' && !usesThreeSections(exam, subject) && (
          <div>
            <div className="mt-5 flex flex-wrap items-center justify-between gap-3">
              {mode === "MISCELLANEOUS" && selected.length > 0 && availableTotal > 0 && (
                <div className="flex gap-2">
                  <button type="button" className={secondary} onClick={() => setSelected(chapters.map(c => c.id))}>Select All</button>
                  <button type="button" className={secondary} onClick={() => setSelected([])}>Deselect All</button>
                </div>
              )}
              {subject && subject.slug !== 'current-affairs' && (
                <p className="text-sm text-gray-600">{selectedChapters.length} selected · {availableTotal} questions available</p>
              )}
            </div>

            {mode === "MISCELLANEOUS" && selected.length > 0 && availableTotal > 0 && (
              <label className="mt-5 block text-sm font-semibold">
                Question count
                <select
                  className="mt-2 block min-h-11 w-full rounded border px-3"
                  value={questionCount ?? Math.min(25, availableTotal)}
                  onChange={e => setQuestionCount(Number(e.target.value))}
                >
                  {[10, 15, 20, 25].filter(n => n <= availableTotal).concat(availableTotal < 10 ? [availableTotal] : []).map(n => (
                    <option key={n} value={n}>{n}</option>
                  ))}
                </select>
              </label>
            )}

            {selected.length > 0 && (
              <button type="button" className={`${button} mt-5`} disabled={loading || !availableTotal} onClick={() => void startTestMiscellaneous()}>
                {!availableTotal ? "Waiting for Banking questions" : "Start Test"}
              </button>
            )}

            {!chapters.length && (
              <p role="status" className="mt-4 rounded-md bg-gray-50 p-4 text-sm text-gray-600">
                No chapters available yet for this subject.
              </p>
            )}

            {chapters.length > 0 && (
              <div className="mt-4 grid gap-2">
                {chapters.map((chapter, index) => {
                  const active = selected.includes(chapter.id);
                  const count = counts[chapter.id] ?? 0;
                  return (
                    <button
                      key={chapter.id}
                      type="button"
                      disabled={count === 0 && mode === "CHAPTER_WISE"}
                      aria-pressed={active}
                      className={`${card} flex items-center justify-between gap-3 ${active ? "border-[#007BFF] bg-blue-50" : ""} disabled:cursor-not-allowed disabled:opacity-60`}
                      onClick={() => setSelected(old => mode === "CHAPTER_WISE" ? [chapter.id] : active ? old.filter(id => id !== chapter.id) : [...old, chapter.id])}
                    >
                      <span className="font-semibold">{index + 1}. {chapter.name}</span>
                      <span className="shrink-0 text-sm text-gray-600">{count ? `${count} questions` : "No questions yet"}</span>
                    </button>
                  );
                })}
              </div>
            )}
          </div>
        )}
      </div>
    </main>
  );
}