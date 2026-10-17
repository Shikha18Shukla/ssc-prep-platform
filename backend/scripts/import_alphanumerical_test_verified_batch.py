"""Validate and idempotently import the reviewed Alphanumerical Test bank."""

import argparse
import json
import sys
import unicodedata
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))

from sqlalchemy import select

from app.database.session import SessionLocal, engine
from app.models import Chapter, Exam, Question, Subject
from app.services.question_import_service import import_questions

BATCH = BASE / "data" / "alphanumerical_test_verified_batch.json"
LEDGER = BASE / "data" / "alphanumerical_test_answer_ledger.json"
EXPECTED_CHAPTER_ID = "d6e05bdf-64ee-4e28-9994-ee8649702c9c"
LEVELS = ("EASY", "MEDIUM", "HARD")
TARGET = {"EASY": 10, "MEDIUM": 12, "HARD": 8}
ORIGINAL = "Original SSC-style practice question"


def normalized(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def load_batch():
    rows = json.loads(BATCH.read_text(encoding="utf-8")).get("questions")
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    if not isinstance(rows, list) or len(rows) != 30 or len(ledger) != 30:
        raise ValueError("Alphanumerical Test batch and ledger must each contain 30 records")
    if Counter(row.get("difficulty") for row in rows) != Counter(TARGET):
        raise ValueError("Alphanumerical Test difficulty distribution must be 10/12/8")
    seen = set()
    for index, (row, audit) in enumerate(zip(rows, ledger), start=1):
        if (row.get("subject_slug"), row.get("chapter_slug")) != ("reasoning", "alphanumerical-test"):
            raise ValueError(f"Row {index} catalog mismatch")
        if row.get("is_pyq") is not False or row.get("pyq_year") is not None or row.get("pyq_exam_name") is not None:
            raise ValueError(f"Row {index} contains invalid Normal/PYQ metadata")
        if row.get("difficulty") not in LEVELS or not row.get("question_text", "").strip():
            raise ValueError(f"Row {index} has an invalid difficulty or stem")
        if not row.get("explanation", "").strip() or len(row.get("source", "")) > 255:
            raise ValueError(f"Row {index} is missing an explanation or has an invalid source")
        options = row.get("options")
        if not isinstance(options, dict) or set(options) != set("ABCD"):
            raise ValueError(f"Row {index} must have options A-D")
        if any(not isinstance(value, str) or not value.strip() for value in options.values()):
            raise ValueError(f"Row {index} has an empty or non-text option")
        if len({normalized(value) for value in options.values()}) != 4:
            raise ValueError(f"Row {index} options are not distinct")
        answer_key = row.get("correct_option")
        if answer_key not in options or sum(normalized(value) == normalized(options[answer_key]) for value in options.values()) != 1:
            raise ValueError(f"Row {index} must have exactly one correctly keyed option")
        stem_key = normalized(row["question_text"])
        if stem_key in seen:
            raise ValueError(f"Duplicate batch stem in row {index}")
        seen.add(stem_key)
        if (audit.get("row"), audit.get("question"), audit.get("difficulty"), audit.get("source")) != (
            index, row["question_text"], row["difficulty"], row["source"]
        ):
            raise ValueError(f"Row {index} does not align with the answer ledger")
        if audit.get("expected_answer") != options[answer_key] or not audit.get("independent_reasoning", "").strip():
            raise ValueError(f"Row {index} answer or independent reasoning conflicts with the ledger")
        if row["source"] != ORIGINAL and not (
            row["source"].startswith("Alphanumerical test ") and "PDF page " in row["source"]
            and "exam/year not stated" in row["source"]
        ):
            raise ValueError(f"Row {index} has unsupported provenance")
    return rows


def chapter_context(db):
    return db.execute(
        select(Exam, Subject, Chapter)
        .join(Subject, Subject.exam_id == Exam.id)
        .join(Chapter, Chapter.subject_id == Subject.id)
        .where(
            Exam.slug == "ssc", Exam.is_active.is_(True), Subject.slug == "reasoning",
            Subject.is_active.is_(True), Chapter.slug == "alphanumerical-test",
            Chapter.is_active.is_(True), Chapter.subcategory_id.is_(None),
        )
    ).one_or_none()


def count_rows(questions):
    result = Counter()
    for question in questions:
        state = "active" if question.is_active else "inactive"
        kind = "PYQ" if question.is_pyq else "normal"
        result[(state, kind, question.difficulty.value)] += 1
    return result


def plan_missing(rows, existing):
    active_normal = sum(q.is_active and not q.is_pyq for q in existing)
    by_stem = {normalized(row["question_text"]): row for row in rows}
    known = {}
    for question in existing:
        key = normalized(question.question_text)
        if key in known:
            raise ValueError("Existing chapter contains duplicate normalized stems; stop for review")
        known[key] = question
        expected = by_stem.get(key)
        if expected is None:
            continue
        actual_options = {option.option_key: option.option_text for option in question.options}
        correct_keys = [option.option_key for option in question.options if option.is_correct]
        if (
            question.question_text != expected["question_text"]
            or question.explanation != expected["explanation"]
            or question.difficulty.value != expected["difficulty"]
            or question.is_pyq is not False
            or question.pyq_year is not None
            or question.pyq_exam_name is not None
            or question.source != expected["source"]
            or not question.is_active
            or actual_options != expected["options"]
            or correct_keys != [expected["correct_option"]]
        ):
            raise ValueError(f"Existing question conflicts with canonical batch: {question.question_text!r}")
    if active_normal >= 30:
        missing = [row for row in rows if normalized(row["question_text"]) not in known]
        if missing:
            raise ValueError("Chapter already meets the 30-Normal minimum; expanding requires user approval")
        return []
    deficit = 30 - active_normal
    selected = []
    for row in rows:
        key = normalized(row["question_text"])
        if key in known:
            continue
        selected.append(row)
        known.add(key)
        if len(selected) == deficit:
            break
    if len(selected) != deficit:
        raise ValueError(f"Only {len(selected)} new batch rows are available for a deficit of {deficit}")
    return selected


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="preview inserts without writing")
    args = parser.parse_args(argv)
    engine.echo = False
    rows = load_batch()
    print("BATCH", len(rows), dict(Counter(row["difficulty"] for row in rows)))
    print("SOURCES", {"pdf_derived": sum(row["source"] != ORIGINAL for row in rows), "original": sum(row["source"] == ORIGINAL for row in rows), "pyq": 0})
    with SessionLocal() as db:
        context = chapter_context(db)
        if context is None:
            raise SystemExit("Active SSC -> Reasoning -> Alphanumerical Test chapter not found uniquely")
        _, _, chapter = context
        if str(chapter.id) != EXPECTED_CHAPTER_ID:
            raise SystemExit(f"Alphanumerical Test chapter id mismatch: expected {EXPECTED_CHAPTER_ID}, found {chapter.id}")
        existing = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        before = count_rows(existing)
        active_normal_before = sum(before[("active", "normal", level)] for level in LEVELS)
        active_pyq_before = sum(before[("active", "PYQ", level)] for level in LEVELS)
        print("CHAPTER", chapter.id, chapter.name, chapter.slug)
        print("BEFORE", {"active_normal": active_normal_before, "active_pyq": active_pyq_before, "all_records": len(existing)})
        try:
            selected = plan_missing(rows, existing)
        except ValueError as exc:
            raise SystemExit(str(exc)) from exc
        print("PLANNED_INSERTS", len(selected), dict(Counter(row["difficulty"] for row in selected)))
        if not selected:
            print("NOOP: no additional records needed; zero inserts")
            return
        payload = json.dumps({"questions": selected}, ensure_ascii=False).encode("utf-8")
        preview = import_questions(db, payload, "application/json", BATCH.name, True)
        print("DRY_RUN", preview.model_dump())
        if preview.aborted or preview.errors or preview.would_import != len(selected) or preview.duplicates:
            raise SystemExit("Importer dry run did not approve every planned insert")
        if args.dry_run:
            print("NO_DATABASE_CHANGES")
            return
        result = import_questions(db, payload, "application/json", BATCH.name, False)
        print("IMPORT", result.model_dump())
        if result.aborted or result.errors or result.imported != len(selected):
            raise SystemExit("Import count did not match the approved dry run")
        after_rows = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        after = count_rows(after_rows)
        active_normal_after = sum(after[("active", "normal", level)] for level in LEVELS)
        active_pyq_after = sum(after[("active", "PYQ", level)] for level in LEVELS)
        if active_normal_after < 30 or active_pyq_after != active_pyq_before or len(after_rows) != len(existing) + len(selected):
            raise SystemExit("Post-import count or preservation verification failed")
        after_by_stem = {normalized(question.question_text): question for question in after_rows}
        for row in rows:
            question = after_by_stem.get(normalized(row["question_text"]))
            if question is None or not question.is_active or question.is_pyq or question.source != row["source"]:
                raise SystemExit(f"Post-import record or provenance verification failed: {row['question_text']!r}")
            actual_options = {option.option_key: option.option_text for option in question.options}
            correct_keys = [option.option_key for option in question.options if option.is_correct]
            if (
                question.question_text != row["question_text"]
                or question.explanation != row["explanation"]
                or question.difficulty.value != row["difficulty"]
                or question.pyq_year is not None
                or question.pyq_exam_name is not None
                or actual_options != row["options"]
                or correct_keys != [row["correct_option"]]
            ):
                raise SystemExit(f"Post-import content/options verification failed: {row['question_text']!r}")
        print("AFTER", {"active_normal": active_normal_after, "active_pyq": active_pyq_after, "all_records": len(after_rows)})
        print("POST_IMPORT_COUNTS_VERIFIED")


if __name__ == "__main__":
    main()
