/**
 * Shared TypeScript type definitions.
 */

/** Supported exam categories. */
export type ExamCategory = "ssc" | "railway" | "banking" | "police";

/** SSC subjects. */
export type SSCSubject = "gk-gs" | "maths" | "english" | "reasoning";

/** Question difficulty levels. */
export type Difficulty = "easy" | "medium" | "hard" | "pyq";

/** Allowed number of questions per test. */
export type QuestionCount = 10 | 15 | 20 | 25;

/** Seconds allocated per question. */
export const SECONDS_PER_QUESTION = 36 as const;

/** Exam category metadata for display. */
export interface ExamCategoryInfo {
  id: ExamCategory;
  label: string;
  available: boolean;
}

/** Subject metadata for display. */
export interface SubjectInfo {
  id: SSCSubject;
  label: string;
}

/** Difficulty level metadata for display. */
export interface DifficultyInfo {
  id: Difficulty;
  label: string;
  description: string;
}
