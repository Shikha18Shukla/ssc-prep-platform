"""Validate, dry-run and idempotently import the reviewed Discount question bank."""

import argparse
import json
import re
import sys
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))

from sqlalchemy import select

from app.database.session import SessionLocal, engine
from app.models import Chapter, Exam, Question, Subject, Subcategory
from app.services.question_import_service import import_questions

BATCH = BASE / "data" / "discount_verified_batch.json"
LEVELS = ("EASY", "MEDIUM", "HARD")
TARGET = {level: 30 for level in LEVELS}
PDF_SOURCE = "Verified from supplied Discount PDF, page "
ORIGINAL_SOURCE = "Original SSC-style practice question"


def normalized(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def number_masked(value):
    value = normalized(value)
    value = re.sub(r"\d[\d,]*(?:\.\d+)?%?", " <number> ", value)
    return " ".join(re.sub(r"[^a-z<> ]", " ", value).split())


def load_batch():
    payload = json.loads(BATCH.read_text(encoding="utf-8"))
    records = payload.get("questions") if isinstance(payload, dict) else None
    if not isinstance(records, list) or len(records) != 90:
        raise ValueError("Discount batch must contain exactly 90 questions")
    if Counter(row.get("difficulty") for row in records if isinstance(row, dict)) != TARGET:
        raise ValueError("Discount batch must contain exactly 30 questions per difficulty")
    required = {"subject_slug", "subcategory_slug", "chapter_slug", "question_text", "options",
                "correct_option", "explanation", "difficulty", "is_pyq", "source"}
    stems = []
    for index, row in enumerate(records, 1):
        if not isinstance(row, dict):
            raise ValueError(f"Row {index} must be a JSON object")
        missing = required - set(row)
        if missing:
            raise ValueError(f"Row {index} is missing fields: {sorted(missing)}")
        if (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) != (
            "maths", "arithmetic-maths", "discount"
        ):
            raise ValueError(f"Row {index} has an incorrect catalog mapping")
        if row["difficulty"] not in LEVELS or row["is_pyq"] is not False:
            raise ValueError(f"Row {index} has invalid difficulty or PYQ status")
        if row.get("pyq_year") is not None or row.get("pyq_exam_name") is not None:
            raise ValueError(f"Row {index} has PYQ-only metadata")
        source = row["source"]
        if not (source == ORIGINAL_SOURCE or source.startswith(ORIGINAL_SOURCE + ";")
                or source.startswith(PDF_SOURCE) and "; exam/year not stated" in source):
            raise ValueError(f"Row {index} has unrecognized provenance: {source!r}")
        if not isinstance(row["question_text"], str) or not row["question_text"].strip():
            raise ValueError(f"Row {index} has an empty question")
        if not isinstance(row["explanation"], str) or not row["explanation"].strip():
            raise ValueError(f"Row {index} has an empty explanation")
        options = row["options"]
        if not isinstance(options, dict) or set(options) != set("ABCD"):
            raise ValueError(f"Row {index} must have exactly A-D options")
        option_values = [options[key] for key in "ABCD"]
        if any(not isinstance(value, str) or not value.strip() for value in option_values):
            raise ValueError(f"Row {index} has an empty option")
        if len({normalized(value) for value in option_values}) != 4:
            raise ValueError(f"Row {index} has non-distinct options")
        if row["correct_option"] not in options:
            raise ValueError(f"Row {index} has an invalid answer key")
        stems.append(row["question_text"])
    for index, stem in enumerate(stems):
        for prior in stems[:index]:
            if normalized(stem) == normalized(prior) or number_masked(stem) == number_masked(prior):
                raise ValueError(f"Exact or number-masked duplicate in batch: {stem!r} / {prior!r}")
            if SequenceMatcher(None, normalized(stem), normalized(prior)).ratio() >= .92:
                raise ValueError(f"Near-duplicate wording in batch needs review: {stem!r} / {prior!r}")
    return records


def chapter_context(db):
    return db.execute(
        select(Exam, Subject, Subcategory, Chapter)
        .join(Subject, Subject.exam_id == Exam.id)
        .join(Subcategory, Subcategory.subject_id == Subject.id)
        .join(Chapter, Chapter.subcategory_id == Subcategory.id)
        .where(Exam.slug == "ssc", Exam.is_active.is_(True), Subject.slug == "maths",
               Subject.is_active.is_(True), Subcategory.slug == "arithmetic-maths",
               Subcategory.is_active.is_(True), Chapter.slug == "discount", Chapter.is_active.is_(True))
    ).one_or_none()


def counts(questions):
    result = Counter()
    for question in questions:
        status = "active" if question.is_active else "inactive"
        kind = "PYQ" if question.is_pyq else "ordinary"
        result[(question.difficulty.value, kind, status)] += 1
    return result


def print_counts(label, values):
    print(label)
    for level in LEVELS:
        print(level, {f"{status}_{kind}": values[(level, kind, status)]
                      for status in ("active", "inactive") for kind in ("ordinary", "PYQ")})


def options_and_answer(question):
    option_map = {option.option_key: option.option_text for option in question.options}
    answer = next((option.option_key for option in question.options if option.is_correct), None)
    return option_map, answer


def plan_missing(records, existing):
    """Preserve current rows, count active ordinary questions, and fill only deficits."""
    by_key = {normalized(row["question_text"]): row for row in records}
    known = {}
    active_ordinary = Counter()
    for question in existing:
        key = normalized(question.question_text)
        if key in known:
            raise ValueError(f"Existing Discount chapter has an exact duplicate: {question.question_text!r}")
        known[key] = question
        expected = by_key.get(key)
        if expected:
            db_options, db_answer = options_and_answer(question)
            if (db_options != expected["options"] or db_answer != expected["correct_option"]
                    or question.difficulty.value != expected["difficulty"] or question.is_pyq):
                raise ValueError(f"Existing exact match conflicts with reviewed bank: {question.question_text!r}")
        if question.is_active and not question.is_pyq:
            active_ordinary[question.difficulty.value] += 1
    for row in records:
        key = normalized(row["question_text"])
        for question in existing:
            prior = normalized(question.question_text)
            if key == prior:
                continue
            if number_masked(row["question_text"]) == number_masked(question.question_text):
                raise ValueError(f"Number-masked duplicate against existing chapter: {row['question_text']!r}")
            if SequenceMatcher(None, key, prior).ratio() >= .92:
                raise ValueError(f"Near-duplicate against existing chapter needs review: {row['question_text']!r}")
    for level in LEVELS:
        if active_ordinary[level] > TARGET[level]:
            raise ValueError(f"{level} already has {active_ordinary[level]} active ordinary questions; preserving rows")
    selected = []
    for level in LEVELS:
        deficit = TARGET[level] - active_ordinary[level]
        for row in records:
            key = normalized(row["question_text"])
            existing_question = known.get(key)
            if row["difficulty"] != level or existing_question is not None or deficit == 0:
                continue
            selected.append(row)
            known[key] = True
            deficit -= 1
        if deficit:
            raise ValueError(f"Reviewed bank cannot fill the remaining {level} deficit of {deficit}")
    return selected


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="validate and preview without inserting")
    args = parser.parse_args(argv)
    engine.echo = False
    records = load_batch()
    print("BATCH", len(records), dict(Counter(row["difficulty"] for row in records)))
    print("PROVENANCE", {"verified_pdf": sum(row["source"].startswith(PDF_SOURCE) for row in records),
                        "original": sum(row["source"].startswith(ORIGINAL_SOURCE) for row in records)})
    with SessionLocal() as db:
        context = chapter_context(db)
        if context is None:
            raise SystemExit("Active SSC -> Maths -> Arithmetic Maths -> Discount chapter was not found uniquely")
        _, _, category, chapter = context
        existing = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        before = counts(existing)
        print("CHAPTER", chapter.id, chapter.name, chapter.slug)
        print("SUBCATEGORY", category.id, category.name, category.slug)
        print_counts("BEFORE", before)
        try:
            selected = plan_missing(records, existing)
        except ValueError as exc:
            raise SystemExit(str(exc)) from exc
        print("PLANNED_INSERTS", len(selected), dict(Counter(row["difficulty"] for row in selected)))
        if not selected:
            print("NOOP: active ordinary targets met; zero inserts and zero duplicates")
            return
        payload = json.dumps({"questions": selected}, ensure_ascii=False).encode("utf-8")
        preview = import_questions(db, payload, "application/json", BATCH.name, True)
        print("DRY_RUN", preview.model_dump())
        if preview.aborted or preview.errors or preview.would_import != len(selected) or preview.duplicates:
            raise SystemExit("Importer dry-run did not approve every planned insert")
        if args.dry_run:
            print("NO_DATABASE_CHANGES")
            return
        imported = import_questions(db, payload, "application/json", BATCH.name, False)
        print("IMPORT", imported.model_dump())
        if imported.aborted or imported.errors or imported.imported != len(selected):
            raise SystemExit("Import did not match its validated dry run")
        after_rows = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        after = counts(after_rows)
        print_counts("AFTER", after)
        print("INSERTED", imported.imported, "TOTAL_CHAPTER_ROWS", len(after_rows))
        if any(after[(level, "ordinary", "active")] != 30 for level in LEVELS):
            raise SystemExit("Post-import counts do not equal 30 active ordinary questions per difficulty")
        if any(after[(level, "PYQ", state)] != before[(level, "PYQ", state)]
               for level in LEVELS for state in ("active", "inactive")):
            raise SystemExit("Import unexpectedly changed PYQ rows")
        print("IDEMPOTENCY_CHECK: run the same importer again; it will report NOOP with zero inserts")


if __name__ == "__main__":
    main()
