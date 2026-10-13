"""Validate, dry-run, and idempotently import the reviewed Speed-Time-Distance bank."""
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

BATCH = BASE / "data" / "speed_time_distance_verified_batch.json"
LEVELS = ("EASY", "MEDIUM", "HARD")
TARGET = {level: 30 for level in LEVELS}


def normalized(text):
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def number_masked(text):
    value = normalized(text)
    value = re.sub(r"\d[\d,]*(?:\.\d+)?%?", " <number> ", value)
    return " ".join(re.sub(r"[^a-z<> ]", " ", value).split())


def load_batch():
    payload = json.loads(BATCH.read_text(encoding="utf-8"))
    records = payload.get("questions") if isinstance(payload, dict) else None
    if not isinstance(records, list) or len(records) != 90:
        raise ValueError("Speed Time & Distance batch must contain exactly 90 questions")
    counts = Counter(row.get("difficulty") for row in records if isinstance(row, dict))
    if counts != TARGET:
        raise ValueError(f"Expected 30 questions per difficulty; found {dict(counts)}")
    required = {
        "subject_slug", "subcategory_slug", "chapter_slug", "question_text", "options",
        "correct_option", "explanation", "difficulty", "is_pyq", "source",
    }
    for row_no, row in enumerate(records, 1):
        if not isinstance(row, dict):
            raise ValueError(f"Row {row_no} must be an object")
        missing = required - set(row)
        if missing:
            raise ValueError(f"Row {row_no} missing fields: {sorted(missing)}")
        if (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) != (
            "maths", "arithmetic-maths", "speed-time-and-distance"
        ):
            raise ValueError(f"Row {row_no} has incorrect catalog mapping")
        if row["difficulty"] not in LEVELS or row["is_pyq"] is not False:
            raise ValueError(f"Row {row_no} has invalid difficulty or PYQ metadata")
        if row.get("pyq_year") is not None or row.get("pyq_exam_name") is not None:
            raise ValueError(f"Row {row_no} contains PYQ-only metadata")
        if row["source"] != "Original SSC-style practice question":
            raise ValueError(f"Row {row_no} has unexpected provenance")
        if not isinstance(row["question_text"], str) or not row["question_text"].strip():
            raise ValueError(f"Row {row_no} has an empty question")
        if not isinstance(row["explanation"], str) or not row["explanation"].strip():
            raise ValueError(f"Row {row_no} has an empty explanation")
        options = row["options"]
        if not isinstance(options, dict) or set(options) != {"A", "B", "C", "D"}:
            raise ValueError(f"Row {row_no} must contain exactly four A-D options")
        if any(not isinstance(value, str) or not value.strip() for value in options.values()):
            raise ValueError(f"Row {row_no} has an empty option")
        if len({normalized(value) for value in options.values()}) != 4:
            raise ValueError(f"Row {row_no} has non-distinct options")
        if row["correct_option"] not in options:
            raise ValueError(f"Row {row_no} has an invalid answer key")
    return records


def chapter_context(db):
    return db.execute(
        select(Exam, Subject, Subcategory, Chapter)
        .join(Subject, Subject.exam_id == Exam.id)
        .join(Subcategory, Subcategory.subject_id == Subject.id)
        .join(Chapter, Chapter.subcategory_id == Subcategory.id)
        .where(
            Exam.slug == "ssc", Exam.is_active.is_(True),
            Subject.slug == "maths", Subject.is_active.is_(True),
            Subcategory.slug == "arithmetic-maths", Subcategory.is_active.is_(True),
            Chapter.slug == "speed-time-and-distance", Chapter.is_active.is_(True),
        )
    ).one_or_none()


def counts(rows):
    result = Counter()
    for row in rows:
        status = "active" if row.is_active else "inactive"
        kind = "PYQ" if row.is_pyq else "ordinary"
        result[(row.difficulty.value, kind, status)] += 1
    return result


def print_counts(label, result):
    print(label)
    for level in LEVELS:
        print(level, {
            f"{state}_{kind}": result[(level, kind, state)]
            for state in ("active", "inactive") for kind in ("ordinary", "PYQ")
        })


def options_and_answer(question):
    values = {option.option_key: option.option_text for option in question.options}
    answer = next((option.option_key for option in question.options if option.is_correct), None)
    return values, answer


def check_batch(records, existing):
    """Reject collisions, except an identical active ordinary replay."""
    by_stem = {normalized(row["question_text"]): row for row in records}
    stems = [row["question_text"] for row in records]
    for index, stem in enumerate(stems):
        for prior in stems[:index]:
            a, b = normalized(stem), normalized(prior)
            if a == b or number_masked(stem) == number_masked(prior):
                raise ValueError(f"Exact or number-masked duplicate in batch: {stem!r} / {prior!r}")
            if SequenceMatcher(None, a, b).ratio() >= .92:
                raise ValueError(f"Near-duplicate wording in batch: {stem!r} / {prior!r}")

    existing_stems = {}
    for question in existing:
        key = normalized(question.question_text)
        if key in existing_stems:
            raise ValueError(f"Existing chapter contains an exact duplicate: {question.question_text!r}")
        existing_stems[key] = question

    for row in records:
        key = normalized(row["question_text"])
        for question in existing:
            prior_key = normalized(question.question_text)
            if key == prior_key:
                db_options, db_answer = options_and_answer(question)
                if (db_options != row["options"] or db_answer != row["correct_option"]
                        or question.difficulty.value != row["difficulty"]
                        or question.is_pyq or not question.is_active):
                    raise ValueError(f"Existing exact-match question conflicts with reviewed row: {row['question_text']!r}")
                continue
            if number_masked(row["question_text"]) == number_masked(question.question_text):
                raise ValueError(f"Number-masked duplicate against existing chapter: {row['question_text']!r}")
            if SequenceMatcher(None, key, prior_key).ratio() >= .92:
                raise ValueError(f"Near-duplicate against existing chapter: {row['question_text']!r}")
    return set(existing_stems)


def plan_missing(records, existing):
    existing_stems = check_batch(records, existing)
    present = Counter(
        row.difficulty.value for row in existing if row.is_active and not row.is_pyq
    )
    for level in LEVELS:
        if present[level] > TARGET[level]:
            raise ValueError(
                f"{level} already has {present[level]} active ordinary questions; target is 30; preserving records and stopping"
            )
    selected = []
    for level in LEVELS:
        deficit = TARGET[level] - present[level]
        for row in records:
            key = normalized(row["question_text"])
            if row["difficulty"] == level and key not in existing_stems and deficit:
                selected.append(row)
                existing_stems.add(key)
                deficit -= 1
        if deficit:
            raise ValueError(f"Batch cannot fill the remaining {level} deficit of {deficit}")
    return selected


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="validate and report without committing")
    args = parser.parse_args(argv)
    engine.echo = False
    records = load_batch()
    print("BATCH", len(records), dict(Counter(row["difficulty"] for row in records)))
    with SessionLocal() as db:
        context = chapter_context(db)
        if context is None:
            raise SystemExit("Active SSC → Maths → Arithmetic Maths → Speed Time & Distance chapter was not found uniquely")
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
            print("NOOP: active ordinary targets already met; zero inserts")
            return
        data = json.dumps({"questions": selected}, ensure_ascii=False).encode("utf-8")
        preview = import_questions(db, data, "application/json", BATCH.name, True)
        print("DRY_RUN", preview.model_dump())
        if preview.aborted or preview.errors or preview.would_import != len(selected) or preview.duplicates:
            raise SystemExit("Importer dry-run did not approve every planned insert")
        if args.dry_run:
            print("NO_DATABASE_CHANGES")
            return
        result = import_questions(db, data, "application/json", BATCH.name, False)
        print("IMPORT", result.model_dump())
        if result.aborted or result.errors or result.imported != len(selected):
            raise SystemExit("Import failed or inserted a different count than dry run")
        after_rows = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        after = counts(after_rows)
        print_counts("AFTER", after)
        print("INSERTED", result.imported, "TOTAL_CHAPTER_ROWS", len(after_rows))
        if any(after[(level, "ordinary", "active")] != 30 for level in LEVELS):
            raise SystemExit("Post-import verification failed: expected exactly 30 active ordinary per difficulty")
        if any(after[(level, kind, state)] != before[(level, kind, state)] for level in LEVELS for kind in ("PYQ",) for state in ("active", "inactive")):
            raise SystemExit("Import unexpectedly changed PYQ counts")


if __name__ == "__main__":
    main()
