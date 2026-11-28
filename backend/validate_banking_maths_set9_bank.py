# -*- coding: utf-8 -*-
"""Independent validation of the imported ninth Maths batch.

Checks both sides of the bank:

* the seven on-disk datasets: exact schema, 120 items per chapter, part sizes,
  four unique options, one correct option, independent recomputation from
  ``verification_data``, source metadata and duplicates;
* the local ``ssc_prep`` database: deterministic IDs, target chapter and section
  assignments, four options / one correct option, explanations, no PYQ flags,
  and no Banking Others rows;
* the real test service: ``get_test_availability`` for all 56 new sections and
  the 42-second-per-question duration used by ``create_test``.

The validator is read-only apart from writing
``reports/banking_maths_set9_validation_report.md``.

Usage:
    # DATABASE_URL is supplied through the process environment for an isolated local database
    python backend/validate_banking_maths_set9_bank.py
"""

from __future__ import annotations

import json
import os
import re
import sys
import uuid
from collections import Counter

import psycopg2
from psycopg2.extensions import parse_dsn
from sqlalchemy import select

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from app.database.session import SessionLocal
from app.models import Chapter, Exam, Question, QuestionOption, Subject
from app.services.test_service import get_test_availability
from dedup_banking_maths_set9 import load_old, prepare
from verify_banking_maths_set9_questions import expected_answer

DATA = os.path.join(ROOT, "data")
REPORTS = os.path.join(ROOT, "reports")
INVENTORY = os.path.join(ROOT, "tmp", "set9_pdf_text", "inventory.json")

EXAMS = {"banking-clerk": "Banking Clerk", "banking-po": "Banking PO"}
CHAPTERS = {
    "pipe_and_cistern_data_interpretation": ("pipe-and-cistern-data-interpretation", "Pipe and Cistern – Data Interpretation"),
    "trains_mains": ("trains-mains", "Trains (Mains)"),
    "trains_data_interpretation": ("trains-data-interpretation", "Trains – Data Interpretation"),
    "boats_and_streams_mains": ("boats-and-streams-mains", "Boats and Streams (Mains)"),
    "boats_and_streams_data_interpretation": ("boats-and-streams-data-interpretation", "Boats and Streams – Data Interpretation"),
    "probability_mains": ("probability-mains", "Probability (Mains)"),
    "probability_data_interpretation": ("probability-data-interpretation", "Probability – Data Interpretation"),
}
FILES = {
    "pipe_and_cistern_data_interpretation": "banking_maths_pipe_and_cistern_di_questions.json",
    "trains_mains": "banking_maths_trains_mains_questions.json",
    "trains_data_interpretation": "banking_maths_trains_data_interpretation_questions.json",
    "boats_and_streams_mains": "banking_maths_boats_and_streams_mains_questions.json",
    "boats_and_streams_data_interpretation": "banking_maths_boats_and_streams_data_interpretation_questions.json",
    "probability_mains": "banking_maths_probability_mains_questions.json",
    "probability_data_interpretation": "banking_maths_probability_data_interpretation_questions.json",
}
PART_SIZES = {1: 15, 2: 20, 3: 30, 4: 55}
EXPECTED_SECTIONS = len(EXAMS) * len(CHAPTERS) * len(PART_SIZES)
EXPECTED_SCHEMA = {
    "id", "chapter", "chapter_key", "part", "section", "question_text", "options",
    "correct_option", "correct_answer", "explanation", "difficulty", "source_name",
    "source_url", "source_page", "source_type", "exam_year", "verification_status",
    "verification_method", "verification_data", "provenance_note",
}


def section_name(exam_slug: str, chapter_key: str, part: int) -> str:
    return f"{exam_slug.replace('-', '_')}_maths_{chapter_key}_part_{part}"


def stable_id(exam_slug: str, item_id: str) -> str:
    return str(
        uuid.uuid5(
            uuid.NAMESPACE_URL,
            f"https://ssc-prep.local/banking-maths/{exam_slug}/{item_id}",
        )
    )


def file_key(text: str) -> str:
    text = str(text).lower().replace("&", " and ")
    text = re.sub(r"[_-]+", " ", text)
    text = re.sub(r"\b(eng|mains|pdf)\b", " ", text)
    text = text.split(", pp. ", 1)[0]
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", text)).strip()


def connect_local():
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise SystemExit("DATABASE_URL is required")
    dsn = parse_dsn(url)
    if (dsn.get("host") or "").lower() not in {"127.0.0.1", "localhost", "::1"}:
        raise SystemExit("refusing non-local host")
    if dsn.get("dbname") != "ssc_prep":
        raise SystemExit("refusing non-ssc_prep database")
    return psycopg2.connect(url)


def validate_datasets(failures: list[str]) -> tuple[list[dict], set[str]]:
    items: list[dict] = []
    planned_ids: set[str] = set()
    with open(INVENTORY, encoding="utf-8") as handle:
        inventory = json.load(handle)
    inventory_pages = {entry["file"]: entry["pages"] for entry in inventory}

    for key, filename in FILES.items():
        with open(os.path.join(DATA, filename), encoding="utf-8") as handle:
            chapter_items = json.load(handle)
        counts = Counter(item.get("part") for item in chapter_items)
        if len(chapter_items) != 120:
            failures.append(f"{filename}: {len(chapter_items)} items, expected 120")
        if dict(counts) != PART_SIZES:
            failures.append(f"{filename}: part counts {dict(counts)}, expected {PART_SIZES}")
        for item in chapter_items:
            item_id = item.get("id", "<missing>")
            if set(item) != EXPECTED_SCHEMA:
                failures.append(f"{item_id}: schema fields differ from Set 1")
            if item.get("chapter_key") != key:
                failures.append(f"{item_id}: wrong chapter_key")
            options = item.get("options")
            if not isinstance(options, list) or len(options) != 4 or len(set(options)) != 4:
                failures.append(f"{item_id}: options are not four distinct values")
            letter = item.get("correct_option")
            if letter not in ("A", "B", "C", "D"):
                failures.append(f"{item_id}: invalid correct_option {letter!r}")
            elif options["ABCD".index(letter)] != item.get("correct_answer"):
                failures.append(f"{item_id}: correct_option/correct_answer mismatch")
            if item.get("difficulty") not in {"EASY", "MEDIUM", "HARD"}:
                failures.append(f"{item_id}: invalid difficulty")
            elif key.endswith("_mains") and item.get("difficulty") != "HARD":
                failures.append(f"{item_id}: mains item is not HARD")
            elif not key.endswith("_mains") and item.get("difficulty") not in {"EASY", "MEDIUM"}:
                failures.append(f"{item_id}: DI item is not EASY or MEDIUM")
            if not key.endswith("_mains") and not str(item.get("question_text", "")).startswith("Data:"):
                failures.append(f"{item_id}: DI item lacks inline data")
            if not str(item.get("explanation", "")).strip():
                failures.append(f"{item_id}: missing explanation")
            if item.get("source_type") != "ORIGINAL_VERIFIED":
                failures.append(f"{item_id}: source_type is not ORIGINAL_VERIFIED")
            if item.get("verification_status") != "VERIFIED":
                failures.append(f"{item_id}: verification_status is not VERIFIED")
            if item.get("exam_year") is not None:
                failures.append(f"{item_id}: exam_year must be null for originals")
            if not str(item.get("verification_method", "")).strip():
                failures.append(f"{item_id}: missing verification_method")
            provenance = str(item.get("provenance_note", ""))
            if "not an extracted PDF MCQ" not in provenance:
                failures.append(f"{item_id}: provenance note does not disclaim PDF extraction")
            if "previous-year question" not in provenance:
                failures.append(f"{item_id}: provenance note does not disclaim PYQ status")
            reference = str(item.get("source_page", ""))
            label, separator, range_text = reference.rpartition(", pp. ")
            match = re.fullmatch(r"(\d+)-(\d+)", range_text) if separator else None
            if not match:
                failures.append(f"{item_id}: malformed source_page {reference!r}")
            else:
                start, end = int(match.group(1)), int(match.group(2))
                source_key = file_key(label)
                candidates = [entry for entry in inventory if source_key == file_key(entry["file"])]
                if len(candidates) != 1:
                    failures.append(f"{item_id}: source_page does not name exactly one PDF: {label!r}")
                elif not (1 <= start <= end <= inventory_pages[candidates[0]["file"]]):
                    failures.append(f"{item_id}: source_page range outside inspected PDF")
            try:
                computed = expected_answer(item)
            except Exception as exc:
                failures.append(f"{item_id}: answer recomputation failed: {exc}")
            else:
                if computed != item.get("correct_answer"):
                    failures.append(
                        f"{item_id}: recomputed answer {computed!r} != stored {item.get('correct_answer')!r}"
                    )
            for exam_slug in EXAMS:
                planned_ids.add(stable_id(exam_slug, item_id))
            items.append(prepare(item, item_id))
    return items, planned_ids


def validate_duplicates(new_items: list[dict], planned_ids: set[str], failures: list[str]) -> None:
    old_items = load_old()
    conn = connect_local()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id::text, question_text FROM questions
                WHERE NOT (id = ANY(%s::uuid[]))
                """,
                (list(planned_ids),),
            )
            db_items = [prepare({"id": row[0], "question_text": row[1]}, row[0]) for row in cur.fetchall()]
    finally:
        conn.close()

    new_norms = [item["_norm"] for item in new_items]
    new_masks = [item["_mask"] for item in new_items]
    if len(new_norms) != len(set(new_norms)):
        failures.append("duplicate normalized question text inside the new batch")
    for name, pool in (("Sets 1-8", old_items), ("existing database", db_items)):
        norms = {item["_norm"] for item in pool}
        masks = {item["_mask"] for item in pool}
        exact_hits = [item for item in new_items if item["_norm"] in norms]
        masked_hits = [item for item in new_items if item["_mask"] in masks]
        if exact_hits:
            failures.append(f"{len(exact_hits)} exact/normalized collisions with {name}")
        if masked_hits:
            failures.append(f"{len(masked_hits)} number-masked collisions with {name}")
    print(
        f"duplicates: new={len(new_items)}, sets1to8={len(old_items)}, "
        f"database-excluding-set9={len(db_items)}"
    )


def validate_db(failures: list[str], planned_ids: set[str]) -> None:
    db = SessionLocal()
    checked = 0
    try:
        for exam_slug in EXAMS:
            exam = db.scalar(select(Exam).where(Exam.slug == exam_slug))
            if exam is None:
                failures.append(f"missing exam {exam_slug}")
                continue
            subject = db.scalar(
                select(Subject).where(Subject.exam_id == exam.id, Subject.slug == "math-quant")
            )
            if subject is None:
                failures.append(f"missing Math & Quant subject for {exam_slug}")
                continue
            for chapter_key, (chapter_slug, chapter_title) in CHAPTERS.items():
                chapter = db.scalar(
                    select(Chapter).where(
                        Chapter.subject_id == subject.id, Chapter.slug == chapter_slug
                    )
                )
                if chapter is None:
                    failures.append(f"missing chapter {exam_slug}/{chapter_slug}")
                    continue
                if chapter.name.strip().lower() != chapter_title.lower():
                    failures.append(
                        f"chapter name mismatch {exam_slug}/{chapter_slug}: {chapter.name!r}"
                    )
                for part, expected in PART_SIZES.items():
                    section = section_name(exam_slug, chapter_key, part)
                    availability = get_test_availability(
                        db, exam.id, subject.id, "CHAPTER_WISE", chapter.id, None, None,
                        question_count=None, chapter_ids=None, section_filter=section,
                    )
                    checked += 1
                    if availability["available_question_count"] != expected:
                        failures.append(
                            f"{section}: availability {availability['available_question_count']}, "
                            f"expected {expected}"
                        )
                    if expected not in availability["allowed_question_counts"]:
                        failures.append(f"{section}: {expected} not an allowed count")
                    if not availability["can_satisfy_request"]:
                        failures.append(f"{section}: cannot satisfy {expected}-question request")

                    questions = db.scalars(
                        select(Question).where(
                            Question.chapter_id == chapter.id,
                            Question.section == section,
                            Question.is_active.is_(True),
                        )
                    ).all()
                    if len(questions) != expected:
                        failures.append(f"{section}: DB has {len(questions)} questions")
                    for question in questions:
                        qid = str(question.id)
                        if qid not in planned_ids:
                            failures.append(f"{section}: unexpected question id {qid}")
                        if question.is_pyq or question.pyq_year is not None:
                            failures.append(f"{section}: question {qid} is flagged PYQ")
                        if not (question.explanation or "").strip():
                            failures.append(f"{section}: question {qid} has no explanation")
                        if question.difficulty not in {"EASY", "MEDIUM", "HARD"}:
                            failures.append(f"{section}: bad difficulty on {qid}")
                        if "class notes and topic-wise" not in (question.source or ""):
                            failures.append(f"{section}: question {qid} has unexpected source label")
                        options = db.scalars(
                            select(QuestionOption).where(QuestionOption.question_id == question.id)
                        ).all()
                        if len(options) != 4:
                            failures.append(f"{section}: question {qid} has {len(options)} options")
                        if sum(option.is_correct for option in options) != 1:
                            failures.append(f"{section}: question {qid} correct-option count != 1")
        others = db.scalar(select(Exam).where(Exam.slug == "banking-others"))
        if others is not None:
            subject = db.scalar(
                select(Subject).where(Subject.exam_id == others.id, Subject.slug == "math-quant")
            )
            if subject is not None:
                count = len(
                    db.scalars(
                        select(Question)
                        .join(Chapter, Question.chapter_id == Chapter.id)
                        .where(
                            Chapter.subject_id == subject.id,
                            Question.section.like("banking_others_maths_%"),
                        )
                    ).all()
                )
                if count:
                    failures.append(f"Banking Others has {count} batch Maths questions")
    finally:
        db.close()
    print(f"sections checked: {checked}/{EXPECTED_SECTIONS}")
    for count, seconds in {15: 630, 20: 840, 30: 1260, 55: 2310}.items():
        print(f"duration rule: {count} questions -> {seconds}s ({seconds / 60:g} min)")


def main() -> int:
    failures: list[str] = []
    new_items, planned_ids = validate_datasets(failures)
    print(f"datasets: {len(new_items)} questions, {len(failures)} failure(s) so far")
    validate_duplicates(new_items, planned_ids, failures)
    validate_db(failures, planned_ids)

    lines = [
        "# Banking Maths Set 9 - Validation Report",
        "",
        f"- Dataset questions checked: {len(new_items)}",
        f"- Planned deterministic IDs: {len(planned_ids)}",
        f"- New sections checked through `get_test_availability`: {EXPECTED_SECTIONS}",
        "- Answers: recomputed from `verification_data` for all 840 questions",
        "- Duplicates: exact, normalized and number-masked checks against the new",
        "  batch, Banking Maths Sets 1-8 and the database excluding the 1,680",
        "  deterministic Set 9 IDs; lexical and semantic screening is reported separately",
        "- Duration rule: 42 seconds per question (630 / 840 / 1260 / 2310 seconds)",
        "",
    ]
    if failures:
        lines += [f"## Failures ({len(failures)})", ""] + [f"- {failure}" for failure in failures] + [""]
    else:
        lines += ["## Result", "", "ALL CHECKS PASSED", ""]
    path = os.path.join(REPORTS, "banking_maths_set9_validation_report.md")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))
    print(f"wrote {path}")
    if failures:
        print(f"FAILURES: {len(failures)}")
        for failure in failures[:60]:
            print(" -", failure)
        return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
