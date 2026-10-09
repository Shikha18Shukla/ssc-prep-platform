/** Database-backed exam catalog API calls. */

import { apiFetch } from "@/services/api";
import type {
  CatalogChapter,
  CatalogExam,
  CatalogSubject,
  CatalogSubcategory,
  ChapterAvailability,
  PracticeLevel,
  QuestionCount,
} from "@/types";

export function getActiveExams(token: string) {
  return apiFetch<CatalogExam[]>("/exams", { token });
}

export function getExamSubjects(token: string, examId: string) {
  return apiFetch<CatalogSubject[]>(`/exams/${examId}/subjects`, { token });
}

export function getSubjectSubcategories(token: string, subjectId: string) {
  return apiFetch<CatalogSubcategory[]>(
    `/exams/subjects/${subjectId}/subcategories`,
    { token },
  );
}

export function getSubjectChapters(
  token: string,
  subjectId: string,
  subcategoryId?: string,
) {
  const params = subcategoryId ? { subcategory_id: subcategoryId } : undefined;
  return apiFetch<CatalogChapter[]>(`/exams/subjects/${subjectId}/chapters`, {
    token,
    params,
  });
}

export function getChapterAvailability(
  token: string,
  chapterId: string,
  level: PracticeLevel,
  questionCount?: QuestionCount,
) {
  const params: Record<string, string> = { level };
  if (questionCount !== undefined) {
    params.question_count = String(questionCount);
  }

  return apiFetch<ChapterAvailability>(
    `/exams/chapters/${chapterId}/availability`,
    { token, params },
  );
}
