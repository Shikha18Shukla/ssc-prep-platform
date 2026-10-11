import { apiFetch } from "@/services/api";

export interface TestOption { option_key: string; option_text: string }
export interface ActiveQuestion {
  test_question_id: string;
  question_order: number;
  question_text: string;
  options: TestOption[];
  selected_option: string | null;
}
export interface ActiveTest {
  id: string;
  exam_id: string;
  subject_id: string;
  chapter_id: string | null;
  test_type: "CHAPTER_WISE" | "MISCELLANEOUS";
  difficulty: string | null;
  question_count: number;
  duration_seconds: number;
  started_at: string;
  deadline_at: string;
  status: "IN_PROGRESS" | "COMPLETED" | "AUTO_SUBMITTED";
  questions: ActiveQuestion[];
}
export interface TestSummary {
  id: string;
  status: "IN_PROGRESS" | "COMPLETED" | "AUTO_SUBMITTED";
  question_count: number;
  attempted_count: number;
  unanswered_count: number;
  correct_count: number | null;
  wrong_count: number | null;
  score: number | null;
  scoring_pending: boolean;
  duration_seconds: number;
  time_taken_seconds: number | null;
  started_at: string;
  submitted_at: string | null;
}
export interface TestResult extends TestSummary {
  review: Array<{
    question_order: number;
    question_text: string;
    options: TestOption[];
    selected_option: string | null;
    correct_option: string;
    explanation: string | null;
    is_correct: boolean;
  }>;
}
export interface DashboardHistory {
  tests_attempted: number;
  average_score: number | null;
  best_score: number | null;
  previous_tests: TestSummary[];
}

export interface TestSelection {
  exam_id: string;
  subject_id: string;
  test_type: "CHAPTER_WISE" | "MISCELLANEOUS";
  subcategory_id: string | null;
  chapter_id: string | null;
  difficulty: string | null;
  question_count: number;
}
export interface TestAvailability {
  available_question_count: number;
  allowed_question_counts: number[];
  can_satisfy_request: boolean;
}

export function getTestAvailability(token: string, selection: Omit<TestSelection, "question_count"> & { question_count?: number }) {
  const params: Record<string, string> = {
    exam_id: selection.exam_id,
    subject_id: selection.subject_id,
    test_type: selection.test_type,
  };
  if (selection.chapter_id) params.chapter_id = selection.chapter_id;
  if (selection.subcategory_id) params.subcategory_id = selection.subcategory_id;
  if (selection.difficulty) params.difficulty = selection.difficulty;
  if (selection.question_count !== undefined) params.question_count = String(selection.question_count);
  return apiFetch<TestAvailability>("/tests/availability", { token, params });
}

export function createTest(token: string, selection: TestSelection) {
  return apiFetch<ActiveTest>("/tests", { token, method: "POST", body: JSON.stringify(selection) });
}
export function getTest(token: string, id: string) {
  return apiFetch<ActiveTest>(`/tests/${id}`, { token });
}
export function saveTestAnswer(token: string, id: string, tqId: string, selected_option: string) {
  return apiFetch<TestSummary>(`/tests/${id}/questions/${tqId}/answer`, {
    token, method: "PUT", body: JSON.stringify({ selected_option }),
  });
}
export function submitTest(token: string, id: string) {
  return apiFetch<TestSummary>(`/tests/${id}/submit`, { token, method: "POST" });
}
export function getTestResult(token: string, id: string) {
  return apiFetch<TestResult>(`/tests/${id}/result`, { token });
}
export function getTestHistory(token: string) {
  return apiFetch<DashboardHistory>("/tests/history/me", { token });
}
