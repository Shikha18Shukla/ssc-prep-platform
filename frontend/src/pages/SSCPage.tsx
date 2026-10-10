import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "@/hooks";
import { ApiError } from "@/services/api";
import { createTest } from "@/services/tests";
import {
  getActiveExams,
  getChapterAvailability,
  getExamSubjects,
  getSubjectSubcategories,
  getSubjectChapters,
} from "@/services/catalog";
import type {
  CatalogChapter,
  CatalogExam,
  CatalogSubject,
  CatalogSubcategory,
  ChapterAvailability,
  PracticeLevel,
  QuestionCount,
} from "@/types";

const STEPS = ["Exam", "Subject", "Category", "Chapter", "Level", "Questions", "Summary"];
const QUESTION_COUNTS: QuestionCount[] = [10, 15, 20, 25];
const SECONDS_PER_QUESTION = 36;
const UNAVAILABLE_EXAMS = ["Railway", "Banking", "Police"];

const LEVELS: {
  id: PracticeLevel;
  title: string;
  description: string;
}[] = [
  { id: "EASY", title: "Easy", description: "Concept Building" },
  { id: "MEDIUM", title: "Medium", description: "Build consistency" },
  { id: "HARD", title: "Hard", description: "Challenge yourself" },
  { id: "PYQ", title: "Previous Year Questions", description: "Practice SSC PYQs" },
];

function errorMessage(error: unknown): string {
  if (error instanceof ApiError) return error.message;
  if (error instanceof Error) return error.message;
  return "Something went wrong while loading the SSC practice options.";
}

const cardClass =
  "w-full rounded-lg border border-[#2D3436]/15 bg-white p-5 text-left transition hover:border-[#007BFF] hover:shadow-sm focus:outline-none focus-visible:ring-2 focus-visible:ring-[#007BFF] focus-visible:ring-offset-2";
const primaryButtonClass =
  "inline-flex min-h-11 items-center justify-center rounded-md bg-[#007BFF] px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-[#0069d9] focus:outline-none focus-visible:ring-2 focus-visible:ring-[#007BFF] focus-visible:ring-offset-2 disabled:cursor-wait disabled:opacity-60";
const secondaryButtonClass =
  "inline-flex min-h-11 items-center justify-center rounded-md border border-[#2D3436]/25 bg-white px-5 py-2.5 text-sm font-semibold text-[#2D3436] transition hover:border-[#007BFF] hover:text-[#007BFF] focus:outline-none focus-visible:ring-2 focus-visible:ring-[#007BFF] focus-visible:ring-offset-2";

export default function SSCPage() {
  const { token } = useAuth();
  const navigate = useNavigate();
  const [step, setStep] = useState(0);
  const [exams, setExams] = useState<CatalogExam[]>([]);
  const [subjects, setSubjects] = useState<CatalogSubject[]>([]);
  const [subcategories, setSubcategories] = useState<CatalogSubcategory[]>([]);
  const [chapters, setChapters] = useState<CatalogChapter[]>([]);
  const [selectedExamId, setSelectedExamId] = useState<string | null>(null);
  const [selectedSubjectId, setSelectedSubjectId] = useState<string | null>(null);
  const [selectedSubcategoryId, setSelectedSubcategoryId] = useState<string | null>(null);
  const [selectedChapterId, setSelectedChapterId] = useState<string | null>(null);
  const [selectedLevel, setSelectedLevel] = useState<PracticeLevel | null>(null);
  const [selectedQuestionCount, setSelectedQuestionCount] =
    useState<QuestionCount | null>(null);
  const [availability, setAvailability] = useState<ChapterAvailability | null>(null);
  const [startLoading, setStartLoading] = useState(false);
  const [startError, setStartError] = useState("");

  const [examsLoading, setExamsLoading] = useState(true);
  const [subjectsLoading, setSubjectsLoading] = useState(false);
  const [subcategoriesLoading, setSubcategoriesLoading] = useState(false);
  const [chaptersLoading, setChaptersLoading] = useState(false);
  const [availabilityLoading, setAvailabilityLoading] = useState(false);
  const [countValidationLoading, setCountValidationLoading] = useState(false);
  const [examsError, setExamsError] = useState("");
  const [subjectsError, setSubjectsError] = useState("");
  const [subcategoriesError, setSubcategoriesError] = useState("");
  const [chaptersError, setChaptersError] = useState("");
  const [availabilityError, setAvailabilityError] = useState("");
  const [reload, setReload] = useState({ exams: 0, subjects: 0, subcategories: 0, chapters: 0, availability: 0 });

  useEffect(() => {
    if (!token) {
      setExamsError("Your session has expired. Please sign in again.");
      setExamsLoading(false);
      return;
    }

    let current = true;
    setExamsLoading(true);
    setExamsError("");
    getActiveExams(token)
      .then((items) => {
        if (current) setExams(items);
      })
      .catch((error: unknown) => {
        if (current) setExamsError(errorMessage(error));
      })
      .finally(() => {
        if (current) setExamsLoading(false);
      });

    return () => {
      current = false;
    };
  }, [token, reload.exams]);

  useEffect(() => {
    if (!token || !selectedExamId) return;
    let current = true;
    setSubjects([]);
    setSubjectsError("");
    setSubjectsLoading(true);
    getExamSubjects(token, selectedExamId)
      .then((items) => {
        if (current) setSubjects(items);
      })
      .catch((error: unknown) => {
        if (current) setSubjectsError(errorMessage(error));
      })
      .finally(() => {
        if (current) setSubjectsLoading(false);
      });
    return () => {
      current = false;
    };
  }, [token, selectedExamId, reload.subjects]);

  useEffect(() => {
    if (!token || !selectedSubjectId) return;
    let current = true;
    setSubcategories([]);
    setSubcategoriesError("");
    setSubcategoriesLoading(true);
    getSubjectSubcategories(token, selectedSubjectId)
      .then((items) => {
        if (!current) return;
        setSubcategories(items);
        if (items.length === 0 && step === 2) setStep(3);
      })
      .catch((error: unknown) => { if (current) setSubcategoriesError(errorMessage(error)); })
      .finally(() => { if (current) setSubcategoriesLoading(false); });
    return () => { current = false; };
  }, [token, selectedSubjectId, reload.subcategories]);

  useEffect(() => {
    if (!token || !selectedSubjectId) return;
    let current = true;
    setChapters([]);
    setChaptersError("");
    setChaptersLoading(true);
    getSubjectChapters(token, selectedSubjectId, selectedSubcategoryId ?? undefined)
      .then((items) => {
        if (current) setChapters(items);
      })
      .catch((error: unknown) => {
        if (current) setChaptersError(errorMessage(error));
      })
      .finally(() => {
        if (current) setChaptersLoading(false);
      });
    return () => {
      current = false;
    };
  }, [token, selectedSubjectId, selectedSubcategoryId, reload.chapters]);

  useEffect(() => {
    if (!token || !selectedChapterId || !selectedLevel || step !== 5) return;
    let current = true;
    setAvailability(null);
    setAvailabilityError("");
    setAvailabilityLoading(true);
    getChapterAvailability(token, selectedChapterId, selectedLevel)
      .then((result) => {
        if (current) setAvailability(result);
      })
      .catch((error: unknown) => {
        if (current) setAvailabilityError(errorMessage(error));
      })
      .finally(() => {
        if (current) setAvailabilityLoading(false);
      });
    return () => {
      current = false;
    };
  }, [token, selectedChapterId, selectedLevel, step, reload.availability]);

  const selectedExam = exams.find((exam) => exam.id === selectedExamId);
  const selectedSubject = subjects.find((subject) => subject.id === selectedSubjectId);
  const selectedSubcategory = subcategories.find((subcategory) => subcategory.id === selectedSubcategoryId);
  const selectedChapter = chapters.find((chapter) => chapter.id === selectedChapterId);
  const selectedLevelInfo = LEVELS.find((level) => level.id === selectedLevel);

  function chooseExam(exam: CatalogExam) {
    setSelectedExamId(exam.id);
    setSelectedSubjectId(null);
    setSelectedSubcategoryId(null);
    setSelectedChapterId(null);
    setSelectedLevel(null);
    setSelectedQuestionCount(null);
    setAvailability(null);
    setStep(1);
  }

  function chooseSubject(subject: CatalogSubject) {
    setSelectedSubjectId(subject.id);
    setSelectedSubcategoryId(null);
    setSelectedChapterId(null);
    setSelectedLevel(null);
    setSelectedQuestionCount(null);
    setAvailability(null);
    setStep(2);
  }

  function chooseSubcategory(subcategory: CatalogSubcategory) {
    setSelectedSubcategoryId(subcategory.id);
    setSelectedChapterId(null);
    setSelectedLevel(null);
    setSelectedQuestionCount(null);
    setAvailability(null);
    setStep(3);
  }

  function chooseChapter(chapter: CatalogChapter) {
    setSelectedChapterId(chapter.id);
    setSelectedLevel(null);
    setSelectedQuestionCount(null);
    setAvailability(null);
    setStep(4);
  }

  function chooseLevel(level: PracticeLevel) {
    setSelectedLevel(level);
    setSelectedQuestionCount(null);
    setAvailability(null);
    setAvailabilityError("");
    setStep(5);
  }

  async function chooseQuestionCount(count: QuestionCount) {
    if (!token || !selectedChapterId || !selectedLevel) return;
    setCountValidationLoading(true);
    setAvailabilityError("");
    try {
      const result = await getChapterAvailability(
        token,
        selectedChapterId,
        selectedLevel,
        count,
      );
      setAvailability(result);
      if (!result.can_satisfy_request) {
        setAvailabilityError(
          `There are only ${result.available_question_count} active questions for this selection. Choose a smaller count or another level.`,
        );
        return;
      }
      setSelectedQuestionCount(count);
      setStep(6);
    } catch (error) {
      setAvailabilityError(errorMessage(error));
    } finally {
      setCountValidationLoading(false);
    }
  }

  const durationSeconds = selectedQuestionCount
    ? selectedQuestionCount * SECONDS_PER_QUESTION
    : 0;
  const durationMinutes = durationSeconds / 60;

  async function startTest() {
    if (!token || !selectedExamId || !selectedSubjectId || !selectedChapterId || !selectedLevel || !selectedQuestionCount) return;
    setStartLoading(true);
    setStartError("");
    try {
      const attempt = await createTest(token, {
        exam_id: selectedExamId,
        subject_id: selectedSubjectId,
        subcategory_id: selectedSubcategoryId,
        chapter_id: selectedChapterId,
        difficulty: selectedLevel,
        question_count: selectedQuestionCount,
      });
      navigate(`/tests/${attempt.id}`);
    } catch (error) {
      setStartError(errorMessage(error));
    } finally {
      setStartLoading(false);
    }
  }

  return (
    <div
      className="mx-auto max-w-4xl bg-[#F8F9FA] text-[#2D3436]"
      style={{ fontFamily: "Inter, 'Noto Sans Devanagari', sans-serif" }}
    >
      <div className="rounded-lg border border-[#2D3436]/10 bg-white p-5 shadow-sm sm:p-8">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
          <div>
            <p className="text-sm font-semibold uppercase tracking-wide text-[#007BFF]">
              SSC Practice
            </p>
            <h1 className="mt-1 text-2xl font-bold sm:text-3xl">
              Set up your practice
            </h1>
            <p className="mt-2 text-sm text-[#2D3436]/70">
              Choose a subject, chapter, level, and question count.
            </p>
          </div>
          <Link to="/dashboard" className={secondaryButtonClass}>
            Back to Dashboard
          </Link>
        </div>

        <ol
          aria-label="Practice setup progress"
          className="mt-7 grid grid-cols-3 gap-2 sm:grid-cols-6"
        >
          {STEPS.filter((label) => label !== "Category" || subcategories.length > 0 || step === 2).map((label, visibleIndex) => {
            const index = STEPS.indexOf(label);
            const activeIndex = step;
            return (
            <li
              key={label}
              aria-current={activeIndex === index ? "step" : undefined}
              className={`rounded-md px-2 py-2 text-center text-xs font-semibold sm:text-sm ${
                activeIndex === index
                  ? "bg-[#007BFF] text-white"
                  : index < activeIndex
                    ? "bg-[#28C76F]/15 text-[#197a45]"
                    : "bg-[#F8F9FA] text-[#2D3436]/55"
              }`}
            >
              <span className="mr-1">{visibleIndex + 1}.</span>{label}
            </li>
          );})}
        </ol>

        <div className="mt-8" aria-live="polite">
          {step > 0 && step < 6 && (
            <button
              type="button"
              onClick={() => setStep((current) => current === 3 && subcategories.length === 0 ? 1 : current === 2 && subcategories.length === 0 ? 1 : Math.max(0, current - 1))}
              className={`${secondaryButtonClass} mb-5`}
            >
              ← Back
            </button>
          )}

          {step === 0 && (
            <section aria-labelledby="exam-step-heading">
              <h2 id="exam-step-heading" className="text-xl font-bold">
                Choose an exam
              </h2>
              {examsLoading ? (
                <p className="mt-4 text-sm text-[#2D3436]/70">Loading active exams…</p>
              ) : examsError ? (
                <div role="alert" className="mt-4 rounded-md bg-[#EA5455]/10 p-4 text-sm text-[#a72f38]">
                  <p>{examsError} Check that the API is running and you are signed in.</p>
                  <button type="button" onClick={() => setReload((value) => ({ ...value, exams: value.exams + 1 }))} className="mt-3 font-semibold underline">Retry</button>
                </div>
              ) : (
                <>
                  {!exams.some((exam) => exam.slug === "ssc") && (
                    <p role="status" className="mt-4 rounded-md bg-[#FF6B35]/10 p-4 text-sm text-[#8d3b17]">
                      SSC is not active in the catalog yet. Run the backend seed script to enable SSC and configure its subjects.
                    </p>
                  )}
                  <div className="mt-4 grid gap-3 sm:grid-cols-2">
                    {exams.map((exam) => (
                      <button
                        key={exam.id}
                        type="button"
                        onClick={() => chooseExam(exam)}
                        className={`${cardClass} border-l-4 border-l-[#007BFF]`}
                      >
                        <span className="text-lg font-bold">{exam.name}</span>
                        {exam.description && (
                          <span className="mt-1 block text-sm text-[#2D3436]/70">
                            {exam.description}
                          </span>
                        )}
                        <span className="mt-3 block text-sm font-semibold text-[#007BFF]">
                          Select exam →
                        </span>
                      </button>
                    ))}
                    {UNAVAILABLE_EXAMS.map((name) => (
                      <div
                        key={name}
                        aria-disabled="true"
                        className="rounded-lg border border-dashed border-[#2D3436]/20 bg-[#F8F9FA] p-5 text-[#2D3436]/55"
                      >
                        <span className="font-semibold">{name}</span>
                        <span className="ml-2 text-xs font-semibold text-[#FF6B35]">
                          Unavailable
                        </span>
                      </div>
                    ))}
                  </div>
                </>
              )}
            </section>
          )}

          {step === 1 && (
            <section aria-labelledby="subject-step-heading">
              <h2 id="subject-step-heading" className="text-xl font-bold">
                Choose a subject
              </h2>
              <p className="mt-1 text-sm text-[#2D3436]/65">{selectedExam?.name}</p>
              {subjectsLoading ? (
                <p className="mt-4 text-sm text-[#2D3436]/70">Loading subjects…</p>
              ) : subjectsError ? (
                <div role="alert" className="mt-4 rounded-md bg-[#EA5455]/10 p-4 text-sm text-[#a72f38]">
                  <p>{subjectsError}</p>
                  <button type="button" onClick={() => setReload((value) => ({ ...value, subjects: value.subjects + 1 }))} className="mt-3 font-semibold underline">Retry</button>
                </div>
              ) : subjects.length === 0 ? (
                <p className="mt-4 rounded-md bg-[#FF6B35]/10 p-4 text-sm text-[#8d3b17]">
                  No active subjects are configured for this exam. Run the backend seed script to add the SSC subjects.
                </p>
              ) : (
                <div className="mt-4 grid gap-3 sm:grid-cols-2">
                  {subjects.map((subject) => (
                    <button key={subject.id} type="button" onClick={() => chooseSubject(subject)} className={cardClass}>
                      <span className="text-lg font-bold">{subject.name}</span>
                      {subject.description && <span className="mt-1 block text-sm text-[#2D3436]/70">{subject.description}</span>}
                      <span className="mt-3 block text-sm font-semibold text-[#007BFF]">Choose subject →</span>
                    </button>
                  ))}
                </div>
              )}
            </section>
          )}

          {step === 2 && (
            <section aria-labelledby="category-step-heading">
              <h2 id="category-step-heading" className="text-xl font-bold">Choose a category</h2>
              <p className="mt-1 text-sm text-[#2D3436]/65">{selectedSubject?.name}</p>
              {subcategoriesLoading ? <p className="mt-4 text-sm">Loading categories…</p> : subcategoriesError ? <div role="alert" className="mt-4 rounded-md bg-[#EA5455]/10 p-4 text-sm text-[#a72f38]">{subcategoriesError}<button type="button" onClick={() => setReload((v) => ({ ...v, subcategories: v.subcategories + 1 }))} className="ml-2 underline">Retry</button></div> : <div className="mt-4 grid gap-3 sm:grid-cols-2">{subcategories.map((subcategory) => <button key={subcategory.id} type="button" onClick={() => chooseSubcategory(subcategory)} className={cardClass}><span className="text-lg font-bold">{subcategory.name}</span><span className="mt-3 block text-sm font-semibold text-[#007BFF]">Choose category →</span></button>)}</div>}
            </section>
          )}

          {step === 3 && (
            <section aria-labelledby="chapter-step-heading">
              <h2 id="chapter-step-heading" className="text-xl font-bold">Choose a chapter</h2>
              <p className="mt-1 text-sm text-[#2D3436]/65">{selectedSubject?.name}{selectedSubcategory ? ` · ${selectedSubcategory.name}` : ""}</p>
              {chaptersLoading ? (
                <p className="mt-4 text-sm text-[#2D3436]/70">Loading chapters…</p>
              ) : chaptersError ? (
                <div role="alert" className="mt-4 rounded-md bg-[#EA5455]/10 p-4 text-sm text-[#a72f38]">
                  <p>{chaptersError}</p>
                  <button type="button" onClick={() => setReload((value) => ({ ...value, chapters: value.chapters + 1 }))} className="mt-3 font-semibold underline">Retry</button>
                </div>
              ) : chapters.length === 0 ? (
                <div className="mt-4 rounded-md border border-[#FF6B35]/30 bg-[#FF6B35]/10 p-4 text-sm text-[#713112]">
                  <p className="font-semibold">No chapters are available yet.</p>
                  <p className="mt-1">Chapters need to be populated for this subject before practice can be set up. No sample chapters or questions have been added.</p>
                </div>
              ) : (
                <div className="mt-4 grid gap-3 sm:grid-cols-2">
                  {chapters.map((chapter) => (
                    <button key={chapter.id} type="button" onClick={() => chooseChapter(chapter)} className={cardClass}>
                      <span className="text-lg font-bold">{chapter.name}</span>
                      {chapter.description && <span className="mt-1 block text-sm text-[#2D3436]/70">{chapter.description}</span>}
                      <span className="mt-3 block text-sm font-semibold text-[#007BFF]">Choose chapter →</span>
                    </button>
                  ))}
                </div>
              )}
            </section>
          )}

          {step === 4 && (
            <section aria-labelledby="level-step-heading">
              <h2 id="level-step-heading" className="text-xl font-bold">Choose a level</h2>
              <p className="mt-1 text-sm text-[#2D3436]/65">{selectedChapter?.name}</p>
              <div className="mt-4 grid gap-3 sm:grid-cols-2">
                {LEVELS.map((level) => (
                  <button key={level.id} type="button" onClick={() => chooseLevel(level.id)} className={cardClass}>
                    <span className="text-lg font-bold">{level.title}</span>
                    <span className="mt-1 block text-sm text-[#2D3436]/70">{level.description}</span>
                    {level.id === "PYQ" && <span className="mt-2 inline-block rounded-full bg-[#FF6B35]/10 px-2.5 py-1 text-xs font-semibold text-[#a7471a]">Filtered as previous-year questions</span>}
                  </button>
                ))}
              </div>
            </section>
          )}

          {step === 5 && (
            <section aria-labelledby="count-step-heading">
              <h2 id="count-step-heading" className="text-xl font-bold">Choose question count</h2>
              <p className="mt-1 text-sm text-[#2D3436]/65">
                {selectedLevelInfo?.title} · 36 seconds per question
              </p>
              {availabilityLoading ? (
                <p className="mt-4 text-sm text-[#2D3436]/70">Checking active questions…</p>
              ) : availabilityError && !availability ? (
                <div role="alert" className="mt-4 rounded-md bg-[#EA5455]/10 p-4 text-sm text-[#a72f38]">
                  <p>{availabilityError}</p>
                  <button type="button" onClick={() => setReload((value) => ({ ...value, availability: value.availability + 1 }))} className="mt-3 font-semibold underline">Retry</button>
                </div>
              ) : availability && availability.allowed_question_counts.length === 0 ? (
                <div role="status" className="mt-4 rounded-md bg-[#FF6B35]/10 p-4 text-sm text-[#713112]">
                  <p className="font-semibold">There are not enough active questions for this selection.</p>
                  <p className="mt-1">Found {availability.available_question_count}; at least 10 are needed. Try another level or ask an administrator to populate this chapter’s question bank.</p>
                </div>
              ) : availability ? (
                <>
                  <p className="mt-4 text-sm text-[#2D3436]/70">
                    {availability.available_question_count} active question{availability.available_question_count === 1 ? "" : "s"} available for this level.
                  </p>
                  <div className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-4">
                    {QUESTION_COUNTS.map((count) => {
                      const enabled = availability.allowed_question_counts.includes(count);
                      return (
                        <button
                          key={count}
                          type="button"
                          disabled={!enabled || countValidationLoading}
                          onClick={() => void chooseQuestionCount(count)}
                          className={`rounded-lg border p-4 text-center transition focus:outline-none focus-visible:ring-2 focus-visible:ring-[#007BFF] disabled:cursor-not-allowed disabled:opacity-45 ${enabled ? "border-[#007BFF]/40 bg-white hover:border-[#007BFF] hover:shadow-sm" : "border-[#2D3436]/10 bg-[#F8F9FA]"}`}
                        >
                          <span className="block text-2xl font-bold">{count}</span>
                          <span className="mt-1 block text-sm text-[#2D3436]/70">{(count * SECONDS_PER_QUESTION) / 60} minutes</span>
                        </button>
                      );
                    })}
                  </div>
                  {countValidationLoading && <p className="mt-3 text-sm text-[#2D3436]/70">Rechecking availability…</p>}
                  {availabilityError && <p role="alert" className="mt-3 rounded-md bg-[#EA5455]/10 p-3 text-sm text-[#a72f38]">{availabilityError}</p>}
                </>
              ) : null}
            </section>
          )}

          {step === 6 && (
            <section aria-labelledby="summary-step-heading">
              <h2 id="summary-step-heading" className="text-xl font-bold">Review your selection</h2>
              <dl className="mt-4 grid gap-3 sm:grid-cols-2">
                {[
                  ["Exam", selectedExam?.name],
                  ["Subject", selectedSubject?.name],
                  ...(selectedSubcategory ? [["Category", selectedSubcategory.name] as [string, string]] : []),
                  ["Chapter", selectedChapter?.name],
                  ["Level", selectedLevelInfo?.title],
                  ["Question count", selectedQuestionCount ? `${selectedQuestionCount} questions` : undefined],
                  ["Duration", `${durationMinutes} minutes (${durationSeconds} seconds)`],
                ].map(([label, value]) => (
                  <div key={label} className="rounded-md bg-[#F8F9FA] p-4">
                    <dt className="text-xs font-semibold uppercase tracking-wide text-[#2D3436]/60">{label}</dt>
                    <dd className="mt-1 font-semibold">{value}</dd>
                  </div>
                ))}
              </dl>
              {startError && <p role="alert" className="mt-5 rounded-md bg-[#EA5455]/10 p-4 text-sm text-[#a72f38]">{startError}</p>}
              <div className="mt-5 flex flex-col gap-3 sm:flex-row">
                <button type="button" onClick={() => setStep(5)} className={secondaryButtonClass}>← Change question count</button>
                <button type="button" disabled={startLoading} onClick={() => void startTest()} className={primaryButtonClass}>
                  {startLoading ? "Creating test…" : "Start Test"}
                </button>
              </div>
            </section>
          )}
        </div>
      </div>
    </div>
  );
}
