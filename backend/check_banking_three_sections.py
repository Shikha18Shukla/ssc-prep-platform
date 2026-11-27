"""Validate Banking Clerk/PO three-section chapter allocation.

Default mode is read-only against the live database. ``--create-tests`` performs
real create/answer/submit checks and is deliberately restricted to a disposable
database whose URL contains ``scratch``.
"""

from __future__ import annotations

import argparse
import os
import uuid
from collections import Counter, defaultdict
from pathlib import Path

from psycopg import connect
from psycopg.rows import dict_row
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.database.session import SessionLocal
from app.models import Question, TestQuestion
from app.schemas.tests import TestCreate
from app.services.test_service import create_test, get_test_availability, save_answer, submit_test
from banking_three_sections_common import (
    EXAM_SLUGS,
    SECTION_COUNTS,
    SECONDS_PER_QUESTION,
    SUBJECT_SLUGS,
    expected_sections,
    normalize_question_text,
    plan_allocation,
    split_allocation,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = PROJECT_ROOT / "reports"

QUERY = """
SELECT
    e.id::text AS exam_id,
    s.id::text AS subject_id,
    e.slug AS exam_slug,
    s.slug AS subject_slug,
    c.id::text AS chapter_id,
    c.slug AS chapter_slug,
    c.name AS chapter_name,
    q.id::text AS question_id,
    q.question_text AS question_text,
    q.is_active AS is_active,
    q.section AS section,
    q.created_at AS created_at
FROM exams e
JOIN subjects s ON s.exam_id = e.id
JOIN chapters c ON c.subject_id = s.id
LEFT JOIN questions q ON q.chapter_id = c.id
WHERE e.slug = ANY(%s) AND s.slug = ANY(%s)
ORDER BY e.slug, s.display_order, c.display_order, c.slug, q.created_at, q.id
"""


def fetch_state(database_url: str) -> tuple[list[dict], str | None]:
    with connect(database_url) as conn:
        conn.read_only = True
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(QUERY, (list(EXAM_SLUGS), list(SUBJECT_SLUGS)))
            rows = cur.fetchall()
            cur.execute(
                "SELECT id::text AS id FROM users WHERE is_active ORDER BY created_at, id LIMIT 1"
            )
            user_row = cur.fetchone()
    return rows, user_row["id"] if user_row else None


def build_chapters(rows: list[dict]) -> list[dict]:
    chapters: dict[tuple[str, str, str], dict] = {}
    for row in rows:
        chapter_key = (row["exam_slug"], row["subject_slug"], row["chapter_id"])
        chapters.setdefault(chapter_key, {
            **{k: row[k] for k in ("exam_id", "subject_id", "exam_slug", "subject_slug", "chapter_id", "chapter_slug", "chapter_name")},
            "rows": [],
        })
        if row["question_id"] is not None:
            chapters[chapter_key]["rows"].append(row)
    return sorted(chapters.values(), key=lambda item: (item["exam_slug"], item["subject_slug"], item["chapter_slug"]))


def check_static(chapters: list[dict], failures: list[str]) -> dict[tuple[str, str, str], dict]:
    all_section_names = [
        name
        for chapter in chapters
        for name in expected_sections(chapter["exam_slug"], chapter["subject_slug"], chapter["chapter_slug"])
    ]
    plan_by_chapter: dict[tuple[str, str, str], dict] = {}

    with connect(os.environ["DATABASE_URL"]) as conn:
        conn.read_only = True
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                "SELECT section, chapter_id::text AS chapter_id, count(*) AS rows "
                "FROM questions WHERE section = ANY(%s) GROUP BY section, chapter_id",
                (all_section_names,),
            )
            global_sections = defaultdict(list)
            for row in cur.fetchall():
                global_sections[row["section"]].append(row)

    for chapter in chapters:
        key = (chapter["exam_slug"], chapter["subject_slug"], chapter["chapter_id"])
        expected_names = expected_sections(chapter["exam_slug"], chapter["subject_slug"], chapter["chapter_slug"])
        actual_names = sorted({row["section"] for row in chapter["rows"] if row["section"] in expected_names})
        if actual_names != sorted(expected_names):
            failures.append(f"{key}: expected exactly {expected_names}, found {actual_names}")
            continue

        for name in global_sections:
            if name in expected_names and len(global_sections[name]) != 1:
                failures.append(f"{name}: section reused by multiple chapters")

        active_rows = [row for row in chapter["rows"] if row["is_active"]]
        planned_ids, _ = plan_allocation(active_rows)
        expected_ids = split_allocation(planned_ids)
        planned_id_set = set(planned_ids)
        all_selected_ids: list[str] = []
        all_selected_texts: list[str] = []
        section_details: dict[str, dict] = {}

        for part, name in enumerate(expected_names, start=1):
            rows = [row for row in chapter["rows"] if row["section"] == name]
            active = [row for row in rows if row["is_active"]]
            count = SECTION_COUNTS[part - 1]
            if len(rows) != count or len(active) != count:
                failures.append(f"{name}: expected {count} active rows, found total={len(rows)} active={len(active)}")
            ids = [row["question_id"] for row in active]
            if len(set(ids)) != len(ids):
                failures.append(f"{name}: duplicate question ids")
            if set(ids) != set(expected_ids[f"part_{part}"]):
                failures.append(f"{name}: contents differ from deterministic allocation")
            if [row["question_id"] for row in active] != expected_ids[f"part_{part}"]:
                failures.append(f"{name}: stored order differs from deterministic allocation")
            all_selected_ids.extend(ids)
            all_selected_texts.extend(normalize_question_text(row["question_text"]) for row in active)
            section_details[name] = {
                "count": count,
                "ids": ids,
                "duration": count * SECONDS_PER_QUESTION,
            }

        if len(all_selected_ids) != sum(SECTION_COUNTS) or len(set(all_selected_ids)) != sum(SECTION_COUNTS):
            failures.append(f"{key}: 40 section question ids are not unique")
        duplicate_texts = [text for text, total in Counter(all_selected_texts).items() if total > 1]
        if duplicate_texts:
            failures.append(f"{key}: {len(duplicate_texts)} repeated question contents across sections")

        surplus = [row for row in active_rows if row["question_id"] not in planned_id_set]
        assigned_surplus = [row["question_id"] for row in surplus if row["section"] not in (None, "")]
        if assigned_surplus:
            failures.append(f"{key}: {len(assigned_surplus)} surplus questions were assigned")

        plan_by_chapter[key] = {
            **chapter,
            "sections": section_details,
            "surplus": len(surplus),
        }
    return plan_by_chapter


def check_availability(plan_by_chapter: dict, failures: list[str]) -> None:
    db = SessionLocal()
    try:
        for chapter in plan_by_chapter.values():
            for section_name, detail in chapter["sections"].items():
                result = get_test_availability(
                    db,
                    uuid.UUID(chapter["exam_id"]),
                    uuid.UUID(chapter["subject_id"]),
                    "CHAPTER_WISE",
                    uuid.UUID(chapter["chapter_id"]),
                    None,
                    None,
                    detail["count"],
                    None,
                    section_name,
                )
                if result["available_question_count"] != detail["count"]:
                    failures.append(f"{section_name}: availability returned {result['available_question_count']}")
                if detail["count"] not in result["allowed_question_counts"]:
                    failures.append(f"{section_name}: count {detail['count']} not allowed")
                if not result["can_satisfy_request"]:
                    failures.append(f"{section_name}: availability cannot satisfy request")
    finally:
        db.close()


def check_create_tests(plan_by_chapter: dict, user_id: str | None, failures: list[str]) -> int:
    if not user_id:
        raise SystemExit("no active user available for test creation checks")
    db = SessionLocal()
    created = 0
    try:
        for chapter in plan_by_chapter.values():
            for section_name, detail in chapter["sections"].items():
                payload = TestCreate(
                    exam_id=uuid.UUID(chapter["exam_id"]),
                    subject_id=uuid.UUID(chapter["subject_id"]),
                    subcategory_id=None,
                    test_type="CHAPTER_WISE",
                    chapter_id=uuid.UUID(chapter["chapter_id"]),
                    chapter_ids=None,
                    difficulty=None,
                    question_count=detail["count"],
                    section_filter=section_name,
                )
                attempt = create_test(db, uuid.UUID(user_id), payload)
                created += 1
                if attempt.question_count != detail["count"]:
                    failures.append(f"{section_name}: attempt has {attempt.question_count} questions")
                if attempt.duration_seconds != detail["duration"]:
                    failures.append(f"{section_name}: duration {attempt.duration_seconds} != {detail['duration']}")
                if attempt.chapter_id != uuid.UUID(chapter["chapter_id"]):
                    failures.append(f"{section_name}: attempt chapter mismatch")

                rows = db.execute(
                    select(TestQuestion)
                    .where(TestQuestion.test_attempt_id == attempt.id)
                    .order_by(TestQuestion.question_order)
                    .options(joinedload(TestQuestion.question).joinedload(Question.options))
                ).scalars().unique().all()
                attempt_sections = {row.question.section for row in rows}
                if attempt_sections != {section_name}:
                    failures.append(f"{section_name}: attempt questions from {attempt_sections}")
                attempt_ids = [row.question_id for row in rows]
                expected_ids = [uuid.UUID(value) for value in detail["ids"]]
                if attempt_ids != expected_ids:
                    failures.append(f"{section_name}: attempt order differs from deterministic plan")

                first = rows[0]
                correct = next((option.option_key for option in first.question.options if option.is_correct), None)
                if correct is None:
                    failures.append(f"{section_name}: first question has no correct option")
                    continue
                save_answer(db, attempt.id, first.id, correct, uuid.UUID(user_id))
                submitted = submit_test(db, attempt.id, uuid.UUID(user_id))
                if submitted.correct_count != 1 or submitted.wrong_count != 0:
                    failures.append(f"{section_name}: scoring mismatch")
                if submitted.unanswered_count != detail["count"] - 1:
                    failures.append(f"{section_name}: unanswered count mismatch")
                if submitted.score != 2.0:
                    failures.append(f"{section_name}: score mismatch")
    finally:
        db.close()
    return created


def write_report(plan_by_chapter: dict, failures: list[str], created: int, create_mode: bool) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    name = "banking_three_section_create_test_report.md" if create_mode else "banking_three_section_validation_report.md"
    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for chapter in plan_by_chapter.values():
        grouped[(chapter["exam_slug"], chapter["subject_slug"])].append(chapter)

    report = [
        "# Banking Three-Section Validation Report",
        "",
        "Mode: **read-only live validation**." if not create_mode else "Mode: **disposable copy with real create/answer/submit checks**.",
        "",
        "Checks cover every chapter under Banking Clerk/PO English, General/Banking Awareness and Computer. Static checks confirm exactly three sections, exact 10/15/15 active counts, deterministic contents and order, unique ids, no repeated content across the three sections, no section reuse, and preserved surplus questions. Availability is checked through the real service.",
        "",
        f"Chapters checked: **{len(plan_by_chapter)}**. Sections checked: **{len(plan_by_chapter) * 3}**. Tests created: **{created}**. Failures: **{len(failures)}**.",
        "",
        "## Grouped totals",
        "",
        "| Exam | Subject | Chapters | Sections | Questions allocated | Surplus preserved |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for (exam, subject), chapters in sorted(grouped.items()):
        report.append(
            f"| {exam} | {subject} | {len(chapters)} | {len(chapters) * 3} | "
            f"{sum(sum(detail['count'] for detail in chapter['sections'].values()) for chapter in chapters)} | "
            f"{sum(chapter['surplus'] for chapter in chapters)} |"
        )
    report.extend([
        "",
        "## Durations",
        "",
        f"Section 1: {SECTION_COUNTS[0]} questions / {SECTION_COUNTS[0] * SECONDS_PER_QUESTION} seconds. "
        f"Sections 2 and 3: {SECTION_COUNTS[1]} questions / {SECTION_COUNTS[1] * SECONDS_PER_QUESTION} seconds.",
        "",
        "## Failures",
        "",
    ])
    if failures:
        report.extend([f"- {failure}" for failure in failures])
    else:
        report.append("None.")
    report.extend(["", "## Result", "", "ALL CHECKS PASSED" if not failures else "VALIDATION FAILED", ""])
    (REPORT_DIR / name).write_text("\n".join(report), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--create-tests", action="store_true")
    args = parser.parse_args()

    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise SystemExit("DATABASE_URL must be set to the local development database")
    if args.create_tests and "scratch" not in database_url:
        raise SystemExit("refusing destructive test creation outside a scratch database")

    rows, user_id = fetch_state(database_url)
    chapters = build_chapters(rows)
    failures: list[str] = []
    plan_by_chapter = check_static(chapters, failures)
    check_availability(plan_by_chapter, failures)
    created = check_create_tests(plan_by_chapter, user_id, failures) if args.create_tests else 0
    write_report(plan_by_chapter, failures, created, args.create_tests)
    print(
        f"{'create-test' if args.create_tests else 'validation'} "
        f"{'passed' if not failures else 'failed'}: {len(plan_by_chapter)} chapters, "
        f"{created} tests created, {len(failures)} failures"
    )
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
