"""Validate, preview, and idempotently import original Average questions."""
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
from app.models import Chapter, Difficulty, Exam, Question, Subject, Subcategory
from app.services.question_import_service import import_questions

BATCH = BASE / "data" / "average_verified_batch.json"
LEVELS = ("EASY", "MEDIUM", "HARD")
TARGET = {level: 30 for level in LEVELS}


def normalized(text):
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def number_masked(text):
    text = unicodedata.normalize("NFKC", text).casefold()
    text = re.sub(r"\d[\d,]*(?:\.\d+)?%?", " <n> ", text)
    return " ".join(re.sub(r"[^a-z<> ]", " ", text).split())


def load_batch():
    payload = json.loads(BATCH.read_text(encoding="utf-8"))
    records = payload.get("questions") if isinstance(payload, dict) else None
    if not isinstance(records, list) or len(records) != 90:
        raise ValueError("Average batch must contain exactly 90 questions")
    counts = Counter(row.get("difficulty") for row in records if isinstance(row, dict))
    if counts != TARGET:
        raise ValueError(f"Expected 30 questions per difficulty; found {dict(counts)}")
    required = {"subject_slug", "subcategory_slug", "chapter_slug", "question_text", "options", "correct_option", "explanation", "difficulty", "is_pyq", "source"}
    stems = []
    for row_no, row in enumerate(records, 1):
        missing = required - set(row)
        if missing:
            raise ValueError(f"Row {row_no} missing fields: {sorted(missing)}")
        if (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) != ("maths", "arithmetic-maths", "average"):
            raise ValueError(f"Row {row_no} has incorrect catalog mapping")
        if row["difficulty"] not in LEVELS or row["is_pyq"] is not False:
            raise ValueError(f"Row {row_no} has invalid difficulty or PYQ metadata")
        if row.get("pyq_year") is not None or row.get("pyq_exam_name") is not None:
            raise ValueError(f"Row {row_no} contains PYQ-only metadata")
        if row["source"] != "Original SSC-style practice question":
            raise ValueError(f"Row {row_no} has unexpected provenance")
        if not isinstance(row["question_text"], str) or not row["question_text"].strip() or not row["explanation"].strip():
            raise ValueError(f"Row {row_no} has empty question or explanation")
        options = row["options"]
        if not isinstance(options, dict) or set(options) != {"A", "B", "C", "D"}:
            raise ValueError(f"Row {row_no} must contain exactly four A-D options")
        if any(not isinstance(value, str) or not value.strip() for value in options.values()):
            raise ValueError(f"Row {row_no} has an empty option")
        if len({normalized(value) for value in options.values()}) != 4 or row["correct_option"] not in options:
            raise ValueError(f"Row {row_no} has non-distinct options or an invalid key")
        stems.append(row["question_text"])
    for i, stem in enumerate(stems):
        for prior in stems[:i]:
            if normalized(stem) == normalized(prior) or number_masked(stem) == number_masked(prior):
                raise ValueError(f"Exact or number-masked duplicate: {stem!r} / {prior!r}")
            if SequenceMatcher(None, normalized(stem), normalized(prior)).ratio() >= .92:
                raise ValueError(f"High lexical similarity needs review: {stem!r} / {prior!r}")
    return records


def chapter_context(db):
    return db.execute(
        select(Exam, Subject, Subcategory, Chapter)
        .join(Subject, Subject.exam_id == Exam.id)
        .join(Subcategory, Subcategory.subject_id == Subject.id)
        .join(Chapter, Chapter.subcategory_id == Subcategory.id)
        .where(Exam.slug == "ssc", Exam.is_active.is_(True), Subject.slug == "maths", Subject.is_active.is_(True),
               Subcategory.slug == "arithmetic-maths", Subcategory.is_active.is_(True),
               Chapter.slug == "average", Chapter.is_active.is_(True))
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
        print(level, {f"{state}_{kind}": result[(level, kind, state)]
                      for state in ("active", "inactive") for kind in ("ordinary", "PYQ")})


def options_and_answer(question):
    values = {option.option_key: option.option_text for option in question.options}
    answer = next((option.option_key for option in question.options if option.is_correct), None)
    return values, answer


def plan_missing(records, existing):
    """Keep existing records and choose only the unrepresented deficit per level."""
    by_stem = {normalized(row["question_text"]): row for row in records}
    present = Counter()
    existing_stems = set()
    for question in existing:
        key = normalized(question.question_text)
        expected = by_stem.get(key)
        if expected is not None:
            db_options, db_answer = options_and_answer(question)
            if (db_options != expected["options"] or db_answer != expected["correct_option"]
                    or question.difficulty.value != expected["difficulty"] or question.is_pyq
                    or not question.is_active):
                raise ValueError(f"Existing same-stem record conflicts with reviewed ordinary data: {question.question_text!r}")
        if question.is_active and not question.is_pyq:
            present[question.difficulty.value] += 1
            existing_stems.add(key)
    for level in LEVELS:
        if present[level] > TARGET[level]:
            raise ValueError(f"{level} already has {present[level]} active ordinary questions; target is 30; preserving records and stopping")
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
            raise ValueError(f"Reviewed batch cannot fill the remaining {level} deficit of {deficit}")
    return selected


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="validate and report without writing")
    args = parser.parse_args(argv)
    engine.echo = False
    records = load_batch()
    print("BATCH", len(records), dict(Counter(row["difficulty"] for row in records)))
    with SessionLocal() as db:
        context = chapter_context(db)
        if context is None:
            raise SystemExit("Active SSC → Maths → Arithmetic Maths → Average chapter was not found uniquely")
        _, _, _, chapter = context
        existing = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        before = counts(existing)
        print("CHAPTER", chapter.id, chapter.name, chapter.slug)
        print_counts("BEFORE", before)
        try:
            selected = plan_missing(records, existing)
        except ValueError as exc:
            raise SystemExit(str(exc)) from exc
        print("PLANNED_INSERTS", len(selected), dict(Counter(row["difficulty"] for row in selected)))
        if not selected:
            print("NOOP: active ordinary targets already met; no database changes made")
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
            raise SystemExit("Import failed or inserted a different count than the validated dry run")
        after_rows = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        after = counts(after_rows)
        print_counts("AFTER", after)
        print("INSERTED", result.imported, "TOTAL_CHAPTER_ROWS", len(after_rows))
        if any(after[(level, "ordinary", "active")] != 30 for level in LEVELS):
            raise SystemExit("Post-import verification failed: expected 30 active ordinary questions per difficulty")
        if any(after[(level, "PYQ", status)] != before[(level, "PYQ", status)] for level in LEVELS for status in ("active", "inactive")):
            raise SystemExit("Import unexpectedly changed PYQ counts")


if __name__ == "__main__":
    main()
