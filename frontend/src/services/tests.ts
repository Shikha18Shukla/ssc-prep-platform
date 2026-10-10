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
  chapter_id: string;
  difficulty: string;
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

export function createTest(token: string, selection: {
  exam_id: string; subject_id: string; subcategory_id: string | null;
  chapter_id: string; difficulty: string; question_count: number;
}) {
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
