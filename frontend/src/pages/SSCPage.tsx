import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "@/hooks";
import { ApiError } from "@/services/api";
import { createTest, getTestAvailability } from "@/services/tests";
import type { TestSelection } from "@/services/tests";
import { getActiveExams, getExamSubjects, getSubjectSubcategories, getSubjectChapters } from "@/services/catalog";
import type { CatalogChapter, CatalogExam, CatalogSubject, CatalogSubcategory, PracticeLevel, QuestionCount } from "@/types";

const SECONDS_PER_QUESTION = 36;
const UNAVAILABLE_EXAMS = ["Railway", "Banking", "Police"];
const LEVELS: Array<{ id: PracticeLevel; title: string; description: string }> = [
  { id: "EASY", title: "Easy", description: "Concept building" },
  { id: "MEDIUM", title: "Medium", description: "Build consistency" },
  { id: "HARD", title: "Hard", description: "Challenge yourself" },
  { id: "PYQ", title: "Previous Year Questions", description: "Practice SSC PYQs" },
];

function errorMessage(error: unknown): string {
  if (error instanceof ApiError || error instanceof Error) return error.message;
  return "Something went wrong while loading the SSC practice options.";
}

const cardClass = "w-full rounded-lg border border-[#2D3436]/15 bg-white p-5 text-left transition hover:border-[#007BFF] hover:shadow-sm focus:outline-none focus-visible:ring-2 focus-visible:ring-[#007BFF] focus-visible:ring-offset-2";
const primaryButtonClass = "inline-flex min-h-11 items-center justify-center rounded-md bg-[#007BFF] px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-[#0069d9] focus:outline-none focus-visible:ring-2 focus-visible:ring-[#007BFF] focus-visible:ring-offset-2 disabled:cursor-wait disabled:opacity-60";
const secondaryButtonClass = "inline-flex min-h-11 items-center justify-center rounded-md border border-[#2D3436]/25 bg-white px-5 py-2.5 text-sm font-semibold text-[#2D3436] transition hover:border-[#007BFF] hover:text-[#007BFF] focus:outline-none focus-visible:ring-2 focus-visible:ring-[#007BFF] focus-visible:ring-offset-2";

export default function SSCPage() {
  const { token } = useAuth();
  const navigate = useNavigate();
  const [step, setStep] = useState(0);
  const [exams, setExams] = useState<CatalogExam[]>([]);
  const [subjects, setSubjects] = useState<CatalogSubject[]>([]);
  const [subcategories, setSubcategories] = useState<CatalogSubcategory[]>([]);
  const [chapters, setChapters] = useState<CatalogChapter[]>([]);
  const [examId, setExamId] = useState<string | null>(null);
  const [subjectId, setSubjectId] = useState<string | null>(null);
  const [testType, setTestType] = useState<"CHAPTER_WISE" | "MISCELLANEOUS" | null>(null);
  const [subcategoryId, setSubcategoryId] = useState<string | null>(null);
  const [categoryChosen, setCategoryChosen] = useState(false);
  const [chapterId, setChapterId] = useState<string | null>(null);
  const [level, setLevel] = useState<PracticeLevel | null>(null);
  const [questionCount, setQuestionCount] = useState<QuestionCount | null>(null);
  const [availableCount, setAvailableCount] = useState<number | null>(null);
  const [availableCounts, setAvailableCounts] = useState<QuestionCount[]>([]);
  const [chaptersLoaded, setChaptersLoaded] = useState(false);
  const [chaptersError, setChaptersError] = useState("");
  const [subcategoriesError, setSubcategoriesError] = useState("");
  const [loading, setLoading] = useState({ exams: true, subjects: false, subcategories: false, chapters: false, availability: false, count: false, start: false });
  const [error, setError] = useState("");

  useEffect(() => {
    if (!token) { setError("Your session has expired. Please sign in again."); setLoading(v => ({ ...v, exams: false })); return; }
    let current = true;
    getActiveExams(token).then(setExams).catch(e => current && setError(errorMessage(e))).finally(() => current && setLoading(v => ({ ...v, exams: false })));
    return () => { current = false; };
  }, [token]);

  useEffect(() => {
    if (!token || !examId) return;
    let current = true;
    setLoading(v => ({ ...v, subjects: true }));
    getExamSubjects(token, examId).then(items => current && setSubjects(items)).catch(e => current && setError(errorMessage(e))).finally(() => current && setLoading(v => ({ ...v, subjects: false })));
    return () => { current = false; };
  }, [token, examId]);

  useEffect(() => {
    if (!token || !subjectId) return;
    let current = true;
    setSubcategories([]);
    setSubcategoriesError("");
    setLoading(v => ({ ...v, subcategories: true }));
    getSubjectSubcategories(token, subjectId).then(items => current && setSubcategories(items)).catch(e => current && setSubcategoriesError(errorMessage(e))).finally(() => current && setLoading(v => ({ ...v, subcategories: false })));
    return () => { current = false; };
  }, [token, subjectId]);

  useEffect(() => {
    if (!token || !subjectId || testType !== "CHAPTER_WISE" || step !== 4) return;
    let current = true;
    setChapters([]);
    setChaptersLoaded(false);
    setChaptersError("");
    setLoading(v => ({ ...v, chapters: true }));
    getSubjectChapters(token, subjectId, subcategoryId ?? undefined).then(items => {
      if (!current) return;
      setChapters(items);
      setChaptersLoaded(true);
    }).catch(e => {
      if (current) setChaptersError(errorMessage(e));
    }).finally(() => current && setLoading(v => ({ ...v, chapters: false })));
    return () => { current = false; };
  }, [token, subjectId, testType, subcategoryId, step]);

  const selectedExam = exams.find(item => item.id === examId);
  const selectedSubject = subjects.find(item => item.id === subjectId);
  const selectedChapter = chapters.find(item => item.id === chapterId);
  const selectedSubcategory = subcategories.find(item => item.id === subcategoryId);
  const needsDifficulty = selectedSubject?.slug === "maths" || selectedSubject?.slug === "reasoning";

  function selection(count?: number): Omit<TestSelection, "question_count"> & { question_count?: number } {
    return { exam_id: examId!, subject_id: subjectId!, test_type: testType!, subcategory_id: testType === "CHAPTER_WISE" ? subcategoryId : null, chapter_id: testType === "CHAPTER_WISE" ? chapterId : null, difficulty: level, ...(count === undefined ? {} : { question_count: count }) };
  }

  useEffect(() => {
    if (step !== 6 || !token || !examId || !subjectId || !testType || (testType === "CHAPTER_WISE" && !chapterId)) return;
    let current = true;
    setLoading(value => ({ ...value, availability: true }));
    setAvailableCount(null);
    setAvailableCounts([]);
    setError("");
    getTestAvailability(token, {
      exam_id: examId,
      subject_id: subjectId,
      test_type: testType,
      subcategory_id: testType === "CHAPTER_WISE" ? subcategoryId : null,
      chapter_id: testType === "CHAPTER_WISE" ? chapterId : null,
      difficulty: level,
    }).then(result => {
      if (!current) return;
      setAvailableCount(result.available_question_count);
      setAvailableCounts(result.allowed_question_counts);
    }).catch(error => {
      if (current) setError(errorMessage(error));
    }).finally(() => current && setLoading(value => ({ ...value, availability: false })));
    return () => { current = false; };
  }, [step, token, examId, subjectId, testType, chapterId, subcategoryId, level]);

  function chooseExam(item: CatalogExam) {
    setExamId(item.id); setSubjectId(null); setTestType(null); setChapterId(null); setSubcategoryId(null); setLevel(null); setQuestionCount(null); setError(""); setStep(1);
  }
  function chooseSubject(item: CatalogSubject) {
    setSubjectId(item.id); setTestType(null); setChapterId(null); setSubcategoryId(null); setCategoryChosen(false); setLevel(null); setQuestionCount(null); setError(""); setStep(2);
  }
  function continueFromType() {
    if (!testType) return;
    setError(""); setLevel(null); setQuestionCount(null);
    setStep(testType === "CHAPTER_WISE" ? 3 : needsDifficulty ? 5 : 6);
  }
  function chooseChapter(item: CatalogChapter) {
    setChapterId(item.id); setLevel(null); setQuestionCount(null); setAvailableCount(null); setAvailableCounts([]); setError(""); setStep(needsDifficulty ? 5 : 6);
  }
  function chooseCategory(id: string | null) {
    setSubcategoryId(id);
    setCategoryChosen(true);
    setChapterId(null);
    setChapters([]);
    setChaptersLoaded(false);
    setChaptersError("");
    setLoading(v => ({ ...v, chapters: true }));
    setStep(4);
  }
  function chooseLevel(item: PracticeLevel) {
    setLevel(item); setError(""); setQuestionCount(null); setAvailableCount(null); setAvailableCounts([]); setStep(6);
  }
  async function chooseCount(count: QuestionCount) {
    if (!token || !examId || !subjectId || !testType || (testType === "CHAPTER_WISE" && !chapterId)) return;
    setLoading(v => ({ ...v, count: true })); setError("");
    try {
      const result = await getTestAvailability(token, selection(count));
      setAvailableCount(result.available_question_count);
      if (!result.can_satisfy_request) {
        setError(`Only ${result.available_question_count} eligible questions are available for this selection. Choose another option or a smaller question count.`);
        return;
      }
      setQuestionCount(count); setStep(7);
    } catch (e) { setError(errorMessage(e)); }
    finally { setLoading(v => ({ ...v, count: false })); }
  }
  async function startTest() {
    if (!token || !examId || !subjectId || !testType || !questionCount || (testType === "CHAPTER_WISE" && !chapterId)) return;
    setLoading(v => ({ ...v, start: true })); setError("");
    try { const attempt = await createTest(token, { ...selection(questionCount), question_count: questionCount }); navigate(`/tests/${attempt.id}`); }
    catch (e) { setError(errorMessage(e)); }
    finally { setLoading(v => ({ ...v, start: false })); }
  }

  function back() {
    if (step === 7) setStep(6);
    else if (step === 6) setStep(needsDifficulty ? 5 : testType === "CHAPTER_WISE" ? 4 : 2);
    else if (step === 5) setStep(testType === "CHAPTER_WISE" ? 4 : 2);
    else if (step === 4) setStep(3);
    else if (step === 3) setStep(2);
    else if (step > 0) setStep(step - 1);
    setError("");
  }

  const steps: Array<{ step: number; label: string }> = [
    { step: 0, label: "Exam" }, { step: 1, label: "Subject" }, { step: 2, label: "Test type" },
    ...(testType === "CHAPTER_WISE" ? [{ step: 3, label: "Category" }, { step: 4, label: "Chapter" }] : []),
    ...(needsDifficulty && testType ? [{ step: 5, label: "Difficulty" }] : []),
    { step: 6, label: "Questions" }, { step: 7, label: "Summary" },
  ];
  const activeProgress = steps.findIndex(item => item.step === step);
  const durationSeconds = (questionCount ?? 0) * SECONDS_PER_QUESTION;

  return <main className="mx-auto max-w-4xl bg-[#F8F9FA] text-[#2D3436]" style={{ fontFamily: "Inter, 'Noto Sans Devanagari', sans-serif" }}>
    <div className="rounded-lg border border-[#2D3436]/10 bg-white p-5 shadow-sm sm:p-8">
      <header className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div><p className="text-sm font-semibold uppercase tracking-wide text-[#007BFF]">SSC Practice</p><h1 className="mt-1 text-2xl font-bold sm:text-3xl">Set up your practice</h1><p className="mt-2 text-sm text-[#2D3436]/70">Choose a subject, test type, and question count.</p></div>
        <Link to="/dashboard" className={secondaryButtonClass}>Back to Dashboard</Link>
      </header>
      <ol aria-label="Practice setup progress" className="mt-7 grid grid-cols-3 gap-2 sm:grid-cols-4 lg:grid-cols-8">{steps.map(({ label }, index) => <li key={label} aria-current={activeProgress === index ? "step" : undefined} className={`rounded-md px-2 py-2 text-center text-xs font-semibold sm:text-sm ${activeProgress === index ? "bg-[#007BFF] text-white" : index < activeProgress ? "bg-[#28C76F]/15 text-[#197a45]" : "bg-[#F8F9FA] text-[#2D3436]/55"}`}><span className="mr-1">{index + 1}.</span>{label}</li>)}</ol>
      <div className="mt-8" aria-live="polite">
        {step > 0 && step < 7 && <button type="button" onClick={back} className={`${secondaryButtonClass} mb-5`}>{step === 4 ? "← Back to categories" : "← Back"}</button>}
        {error && (step === 1 || step === 3) && <p role="alert" className="mb-5 rounded-md bg-red-50 p-4 text-sm text-red-800">{error}</p>}
        {step === 0 && <section aria-labelledby="exam-heading"><h2 id="exam-heading" className="text-xl font-bold">Choose an exam</h2>{loading.exams ? <p role="status" className="mt-4">Loading active exams…</p> : error ? <p role="alert" className="mt-4 text-red-700">{error}</p> : <div className="mt-4 grid gap-3 sm:grid-cols-2">{exams.map(item => <button key={item.id} type="button" onClick={() => chooseExam(item)} className={cardClass}><span className="text-lg font-bold">{item.name}</span>{item.description && <span className="mt-1 block text-sm text-[#2D3436]/70">{item.description}</span>}</button>)}{UNAVAILABLE_EXAMS.map(name => <div key={name} aria-disabled="true" className="rounded-lg border border-dashed p-5 text-[#2D3436]/55">{name} · Unavailable</div>)}</div>}</section>}
        {step === 1 && <section aria-labelledby="subject-heading"><h2 id="subject-heading" className="text-xl font-bold">Choose a subject</h2><p className="mt-1 text-sm text-gray-600">{selectedExam?.name}</p>{loading.subjects ? <p role="status" className="mt-4">Loading subjects…</p> : <div className="mt-4 grid gap-3 sm:grid-cols-2">{subjects.map(item => <button key={item.id} type="button" onClick={() => chooseSubject(item)} className={cardClass}><span className="text-lg font-bold">{item.name}</span>{item.description && <span className="mt-1 block text-sm text-gray-600">{item.description}</span>}</button>)}</div>}</section>}
        {step === 2 && <section aria-labelledby="type-heading"><h2 id="type-heading" className="text-xl font-bold">Choose a test type</h2><p className="mt-1 text-sm text-gray-600">{selectedSubject?.name}</p><div className="mt-4 grid gap-3 sm:grid-cols-2">{(["CHAPTER_WISE", "MISCELLANEOUS"] as const).map(type => { const selected = testType === type; return <button key={type} type="button" aria-pressed={selected} onClick={() => setTestType(type)} className={`${cardClass} ${selected ? "border-[#007BFF] bg-blue-50 ring-2 ring-[#007BFF]/30" : ""}`}><span className="text-lg font-bold">{type === "CHAPTER_WISE" ? "Chapter-wise Test" : "Miscellaneous Test"}</span><span className="mt-2 block text-sm text-[#2D3436]/70">{type === "CHAPTER_WISE" ? "Practice questions from one selected chapter." : "Practice questions randomly drawn across this subject’s chapters."}</span><span className="mt-3 block text-sm font-semibold text-[#007BFF]">{selected ? "Selected" : "Select test type"}</span></button>; })}</div><button type="button" disabled={!testType} onClick={continueFromType} className={`${primaryButtonClass} mt-5`}>Continue</button></section>}
        {step === 3 && testType === "CHAPTER_WISE" && <section aria-labelledby="category-heading"><h2 id="category-heading" className="text-xl font-bold">Choose a category</h2><p className="mt-1 text-sm text-gray-600">{selectedSubject?.name}</p><nav aria-label={`${selectedSubject?.name ?? "Subject"} categories`} className="mt-4 max-w-lg"><div className="flex flex-col gap-2"><button type="button" aria-pressed={categoryChosen && subcategoryId === null} onClick={() => chooseCategory(null)} className={`${secondaryButtonClass} w-full justify-start text-left ${categoryChosen && subcategoryId === null ? "border-[#007BFF] bg-blue-50 text-[#007BFF]" : ""}`}>All categories</button>{subcategories.map(item => <button key={item.id} type="button" aria-pressed={categoryChosen && subcategoryId === item.id} onClick={() => chooseCategory(item.id)} className={`${secondaryButtonClass} w-full justify-start text-left ${categoryChosen && subcategoryId === item.id ? "border-[#007BFF] bg-blue-50 text-[#007BFF]" : ""}`}>{item.name}</button>)}</div>{loading.subcategories && <p role="status" className="mt-3 text-sm text-gray-600">Loading categories…</p>}{subcategoriesError && <p role="alert" className="mt-3 rounded-md bg-red-50 p-3 text-sm text-red-800">Unable to load categories: {subcategoriesError}</p>}{!loading.subcategories && !subcategoriesError && subcategories.length === 0 && <p className="mt-3 text-sm text-gray-600">No categories are configured for this subject. Choose All categories to browse its chapters.</p>}</nav></section>}
        {step === 4 && testType === "CHAPTER_WISE" && <section aria-labelledby="chapter-heading"><h2 id="chapter-heading" className="text-xl font-bold">Choose a chapter</h2><p className="mt-1 text-sm text-gray-600">{selectedSubject?.name}{categoryChosen ? ` · ${selectedSubcategory?.name ?? "All categories"}` : ""}</p><div aria-live="polite" className="mt-4">{loading.chapters || (!chaptersLoaded && !chaptersError) ? <p role="status" className="text-sm text-gray-600">Loading chapters…</p> : chaptersError ? <p role="alert" className="rounded-md bg-red-50 p-4 text-sm text-red-800">Unable to load chapters: {chaptersError}</p> : chapters.length ? <div className="grid gap-3 sm:grid-cols-2">{chapters.map(item => <button key={item.id} type="button" onClick={() => chooseChapter(item)} className={cardClass}><span className="text-lg font-bold">{item.name}</span>{item.description && <span className="mt-1 block text-sm text-gray-600">{item.description}</span>}</button>)}</div> : <p role="status" className="rounded-md bg-orange-50 p-4 text-sm">No chapters are available for the selected category.</p>}</div></section>}
        {step === 5 && needsDifficulty && <section aria-labelledby="level-heading"><h2 id="level-heading" className="text-xl font-bold">{level === "PYQ" ? "Previous year questions" : "Choose a difficulty"}</h2><p className="mt-1 text-sm text-gray-600">{selectedSubject?.name}{selectedChapter ? ` · ${selectedChapter.name}` : " · all eligible chapters"}</p><div className="mt-4 grid gap-3 sm:grid-cols-2">{LEVELS.map(item => { const selected = level === item.id; return <button key={item.id} type="button" aria-pressed={selected} onClick={() => chooseLevel(item.id)} className={`${cardClass} ${selected ? "border-[#007BFF] bg-blue-50 ring-2 ring-[#007BFF]/30" : ""}`}><span className="text-lg font-bold">{item.title}</span><span className="mt-1 block text-sm text-gray-600">{item.description}</span>{item.id === "PYQ" && <span className="mt-2 inline-block rounded-full bg-orange-50 px-2.5 py-1 text-xs font-semibold text-orange-800">Filtered independently from difficulty</span>}</button>; })}</div></section>}
        {step === 6 && <section aria-labelledby="count-heading"><h2 id="count-heading" className="text-xl font-bold">Choose question count</h2><p className="mt-1 text-sm text-gray-600">{level ? LEVELS.find(item => item.id === level)?.title : "All difficulty levels"} · 36 seconds per question</p>{!needsDifficulty && <fieldset className="mt-4"><legend className="text-sm font-semibold">Question set</legend><div className="mt-2 flex flex-wrap gap-2"><button type="button" aria-pressed={!level} onClick={() => { setLevel(null); setAvailableCount(null); setAvailableCounts([]); }} className={`${secondaryButtonClass} ${!level ? "border-[#007BFF] text-[#007BFF]" : ""}`}>Standard questions</button><button type="button" aria-pressed={level === "PYQ"} onClick={() => { setLevel("PYQ"); setAvailableCount(null); setAvailableCounts([]); }} className={`${secondaryButtonClass} ${level === "PYQ" ? "border-[#007BFF] text-[#007BFF]" : ""}`}>Previous Year Questions (PYQ)</button></div></fieldset>}{loading.availability ? <p role="status" className="mt-4 text-sm">Checking eligible questions…</p> : availableCount !== null && <p className="mt-4 text-sm text-gray-600">{availableCount} eligible active questions available.</p>}{!loading.availability && availableCounts.length === 0 && availableCount === 0 && <p role="status" className="mt-4 rounded-md bg-orange-50 p-4 text-sm text-orange-900">No eligible verified questions are available for this selection yet. More verified questions are needed before a test can start.</p>}<div className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-4">{availableCounts.map(count => <button key={count} type="button" disabled={loading.count || loading.availability} onClick={() => void chooseCount(count)} className={`${cardClass} text-center disabled:opacity-50`}><span className="block text-2xl font-bold">{count}</span><span className="mt-1 block text-sm text-gray-600">{count * SECONDS_PER_QUESTION / 60} minutes</span></button>)}</div>{loading.count && <p role="status" className="mt-3 text-sm">Confirming question availability…</p>}{error && <p role="alert" className="mt-3 rounded-md bg-red-50 p-3 text-sm text-red-800">{error}</p>}</section>}
        {step === 7 && <section aria-labelledby="summary-heading"><h2 id="summary-heading" className="text-xl font-bold">Review your selection</h2><dl className="mt-4 grid gap-3 sm:grid-cols-2">{[["Exam", selectedExam?.name], ["Subject", selectedSubject?.name], ["Test type", testType === "CHAPTER_WISE" ? "Chapter-wise" : "Miscellaneous"], ...(selectedSubcategory && testType === "CHAPTER_WISE" ? [["Category", selectedSubcategory.name] as [string, string]] : []), ...(selectedChapter ? [["Chapter", selectedChapter.name] as [string, string]] : []), ["Question set", level ? LEVELS.find(item => item.id === level)?.title : needsDifficulty ? "" : "Standard questions"], ["Question count", questionCount ? `${questionCount} questions` : ""], ["Duration", `${durationSeconds / 60} minutes (${durationSeconds} seconds)`]].map(([label, value]) => <div key={label} className="rounded-md bg-[#F8F9FA] p-4"><dt className="text-xs font-semibold uppercase tracking-wide text-gray-500">{label}</dt><dd className="mt-1 font-semibold">{value}</dd></div>)}</dl>{error && <p role="alert" className="mt-4 rounded-md bg-red-50 p-4 text-sm text-red-800">{error}</p>}<div className="mt-5 flex flex-col gap-3 sm:flex-row"><button type="button" onClick={() => setStep(6)} className={secondaryButtonClass}>← Change question count</button><button type="button" disabled={loading.start} onClick={() => void startTest()} className={primaryButtonClass}>{loading.start ? "Creating test…" : "Start Test"}</button></div></section>}
      </div>
    </div>
  </main>;
}
