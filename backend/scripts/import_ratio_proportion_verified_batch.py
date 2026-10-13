"""Validate, preview, and idempotently import Ratio & Proportion questions."""
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

BATCH = BASE / "data" / "ratio_proportion_verified_batch.json"
LEVELS = ("EASY", "MEDIUM", "HARD")
EXPECTED = {level: 30 for level in LEVELS}
REQUIRED = {
    "subject_slug", "subcategory_slug", "chapter_slug", "question_text", "options",
    "correct_option", "explanation", "difficulty", "is_pyq", "source",
}


def normalized(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def number_masked(value):
    value = unicodedata.normalize("NFKC", value).casefold()
    value = re.sub(r"\d[\d,]*(?:\.\d+)?%?", " <number> ", value)
    return " ".join(re.sub(r"[^a-z<> ]", " ", value).split())


def load_batch():
    payload = json.loads(BATCH.read_text(encoding="utf-8"))
    records = payload.get("questions") if isinstance(payload, dict) else None
    if not isinstance(records, list) or len(records) != 90:
        raise ValueError("Combined Ratio & Proportion batch must contain exactly 90 questions")
    counts = Counter(record.get("difficulty") for record in records if isinstance(record, dict))
    if any(counts[level] != EXPECTED[level] for level in LEVELS):
        raise ValueError(f"Expected 30 questions per difficulty, found {dict(counts)}")
    stems = []
    for index, record in enumerate(records, 1):
        missing = REQUIRED - set(record)
        if missing:
            raise ValueError(f"Row {index}: missing fields {sorted(missing)}")
        if record["subject_slug"] != "maths" or record["subcategory_slug"] != "arithmetic-maths" or record["chapter_slug"] != "ratio-and-proportion":
            raise ValueError(f"Row {index}: incorrect catalog mapping")
        if record["difficulty"] not in LEVELS or record["is_pyq"] is not False:
            raise ValueError(f"Row {index}: invalid difficulty or PYQ metadata")
        if record.get("pyq_year") is not None or record.get("pyq_exam_name") is not None:
            raise ValueError(f"Row {index}: ordinary practice questions cannot have PYQ metadata")
        if not isinstance(record["question_text"], str) or not record["question_text"].strip():
            raise ValueError(f"Row {index}: question text is empty")
        if not isinstance(record["explanation"], str) or not record["explanation"].strip():
            raise ValueError(f"Row {index}: explanation is empty")
        if record["source"] != "Original SSC-style practice question":
            raise ValueError(f"Row {index}: unexpected or missing provenance")
        options = record["options"]
        if not isinstance(options, dict) or set(options) != {"A", "B", "C", "D"}:
            raise ValueError(f"Row {index}: options must contain exactly A-D")
        if any(not isinstance(value, str) or not value.strip() for value in options.values()):
            raise ValueError(f"Row {index}: every option must be non-empty text")
        if len({normalized(value) for value in options.values()}) != 4:
            raise ValueError(f"Row {index}: options are not distinct")
        if record["correct_option"] not in options:
            raise ValueError(f"Row {index}: answer key is not A-D")
        stems.append(record["question_text"])

    for i, a in enumerate(stems):
        for b in stems[:i]:
            if normalized(a) == normalized(b):
                raise ValueError(f"Exact duplicate stems found: {a!r} / {b!r}")
            if number_masked(a) == number_masked(b):
                raise ValueError(f"Number-masked duplicate stems found: {a!r} / {b!r}")
            if SequenceMatcher(None, normalized(a), normalized(b)).ratio() >= 0.92:
                raise ValueError(f"High-lexical-similarity stems need review: {a!r} / {b!r}")
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
            Chapter.slug == "ratio-and-proportion", Chapter.is_active.is_(True),
        )
    ).one_or_none()


def count_rows(rows):
    counts = Counter()
    for question in rows:
        counts[(question.difficulty.value, "PYQ" if question.is_pyq else "ordinary", "active" if question.is_active else "inactive")] += 1
    return counts


def print_counts(label, counts):
    print(label)
    for level in LEVELS:
        print(level, {
            f"{status}_{kind}": counts[(level, kind, status)]
            for status in ("active", "inactive") for kind in ("ordinary", "PYQ")
        })


def check_existing_is_safe(records, existing):
    expected = {normalized(row["question_text"]): row for row in records}
    for question in existing:
        source = expected.get(normalized(question.question_text))
        if source is None:
            raise ValueError(f"Chapter has an unrelated existing question; refusing import: {question.question_text!r}")
        db_options = {option.option_key: option.option_text for option in question.options}
        answer = next((option.option_key for option in question.options if option.is_correct), None)
        if (db_options != source["options"] or answer != source["correct_option"]
                or question.difficulty.value != source["difficulty"] or question.is_pyq
                or not question.is_active):
            raise ValueError(f"Existing exact-match question differs from the reviewed batch: {question.question_text!r}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="validate and report, without changing the database")
    args = parser.parse_args(argv)
    engine.echo = False
    records = load_batch()
    data = BATCH.read_bytes()
    print("BATCH", len(records), dict(Counter(record["difficulty"] for record in records)))
    with SessionLocal() as db:
        context = chapter_context(db)
        if context is None:
            raise SystemExit("Active SSC → Maths → Arithmetic Maths → Ratio & Proportion chapter was not found uniquely")
        _, _, _, chapter = context
        existing = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        before = count_rows(existing)
        print("CHAPTER", chapter.id, chapter.name, chapter.slug)
        print_counts("BEFORE", before)
        try:
            check_existing_is_safe(records, existing)
        except ValueError as exc:
            raise SystemExit(str(exc)) from exc

        preview = import_questions(db, data, "application/json", BATCH.name, True)
        print("DRY_RUN", preview.model_dump())
        if preview.aborted or preview.errors or preview.would_import + preview.duplicates != len(records):
            raise SystemExit("Database importer dry-run did not validate the complete batch")
        if args.dry_run:
            print("NO_DATABASE_CHANGES")
            return

        result = import_questions(db, data, "application/json", BATCH.name, False)
        print("IMPORT", result.model_dump())
        if result.aborted or result.errors or result.imported != preview.would_import:
            raise SystemExit("Import failed or committed a different number of rows than the validated preview")
        after_rows = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        after = count_rows(after_rows)
        print_counts("AFTER", after)
        print("ADDED", result.imported, "DUPLICATES", result.duplicates)
        print("TOTAL", len(after_rows))
        if len(after_rows) != 90 or any(after[(level, "ordinary", "active")] != 30 for level in LEVELS):
            raise SystemExit("Post-import verification failed: expected 30 active ordinary questions at each difficulty")
        if any(after[(level, "PYQ", status)] for level in LEVELS for status in ("active", "inactive")):
            raise SystemExit("Post-import verification failed: unexpected PYQ records in Ratio & Proportion")
        if any(after[(level, "ordinary", "inactive")] for level in LEVELS):
            raise SystemExit("Post-import verification failed: unexpected inactive ordinary records")


if __name__ == "__main__":
    main()
