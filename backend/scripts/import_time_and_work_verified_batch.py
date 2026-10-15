"""Validate, preview and idempotently import the reviewed Time & Work bank."""
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

BATCH = BASE / "data" / "time_and_work_verified_batch.json"
LEVELS = ("EASY", "MEDIUM", "HARD")
TARGET = {level: 30 for level in LEVELS}
PDF_FILES = {
    "Time and Work 01_.pdf": {4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22},
    "Time and Work 02.pdf": {6, 7, 9, 10, 11, 12, 13, 14, 15, 16},
    "_Time and Work 03.pdf": {6, 7, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 22, 23},
    "_Time and Work 04_.pdf": {6, 7, 8, 9, 10, 11, 12, 13, 15, 18, 19, 20, 21, 22},
    "_Time and Work 05_ Class Notes.pdf": {4, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18},
}
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
        raise ValueError("Time & Work batch must contain exactly 90 questions")
    if Counter(row.get("difficulty") for row in records if isinstance(row, dict)) != TARGET:
        raise ValueError("Time & Work batch must have 30 per difficulty")
    required = {"subject_slug", "subcategory_slug", "chapter_slug", "question_text", "options", "correct_option", "explanation", "difficulty", "is_pyq", "source"}
    pdf_rows = original_rows = 0
    stems = []
    for index, row in enumerate(records, 1):
        if not isinstance(row, dict) or required - row.keys():
            raise ValueError(f"Row {index} missing required fields")
        if (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) != ("maths", "arithmetic-maths", "time-and-work"):
            raise ValueError(f"Row {index} has a catalog mismatch")
        if row["difficulty"] not in LEVELS or row["is_pyq"] is not False or row.get("pyq_year") is not None or row.get("pyq_exam_name") is not None:
            raise ValueError(f"Row {index} has invalid difficulty or PYQ metadata")
        source = row["source"]
        if source == ORIGINAL_SOURCE:
            original_rows += 1
        elif source.startswith("Verified from supplied PDF:") and "; exam/year not stated" in source:
            match = re.fullmatch(r"Verified from supplied PDF: (.+), page (\d+); exam/year not stated", source)
            if not match or match.group(1) not in PDF_FILES or int(match.group(2)) not in PDF_FILES[match.group(1)]:
                raise ValueError(f"Row {index} has invalid PDF provenance: {source!r}")
            pdf_rows += 1
        else:
            raise ValueError(f"Row {index} has unrecognized provenance: {source!r}")
        if not row["question_text"].strip() or not row["explanation"].strip() or len(source) > 255:
            raise ValueError(f"Row {index} has empty text or overlong source metadata")
        options = row["options"]
        if not isinstance(options, dict) or set(options) != set("ABCD"):
            raise ValueError(f"Row {index} must have A-D options")
        values = [options[key] for key in "ABCD"]
        if any(not isinstance(value, str) or not value.strip() for value in values) or len({normalized(value) for value in values}) != 4:
            raise ValueError(f"Row {index} has invalid or repeated options")
        if row["correct_option"] not in options:
            raise ValueError(f"Row {index} has an invalid answer key")
        stems.append(row["question_text"])
    if (pdf_rows, original_rows) != (69, 21):
        raise ValueError(f"Expected 69 PDF and 21 original questions, got {pdf_rows}/{original_rows}")
    for index, stem in enumerate(stems):
        for prior in stems[:index]:
            if normalized(stem) == normalized(prior):
                raise ValueError(f"Normalized duplicate in batch: {stem!r}")
            if number_masked(stem) == number_masked(prior):
                raise ValueError(f"Number-masked duplicate in batch: {stem!r} / {prior!r}")
            if SequenceMatcher(None, normalized(stem), normalized(prior)).ratio() >= .92:
                raise ValueError(f"Lexical near-duplicate in batch: {stem!r} / {prior!r}")
    return records


def chapter_context(db):
    return db.execute(
        select(Exam, Subject, Subcategory, Chapter)
        .join(Subject, Subject.exam_id == Exam.id)
        .join(Subcategory, Subcategory.subject_id == Subject.id)
        .join(Chapter, Chapter.subcategory_id == Subcategory.id)
        .where(
            Exam.slug == "ssc", Exam.is_active.is_(True), Subject.slug == "maths", Subject.is_active.is_(True),
            Subcategory.slug == "arithmetic-maths", Subcategory.is_active.is_(True),
            Chapter.slug == "time-and-work", Chapter.is_active.is_(True),
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
        print(level, {f"{status}_{kind}": counts[(level, kind, status)] for status in ("active", "inactive") for kind in ("ordinary", "PYQ")})


def existing_answer(question):
    options = {option.option_key: option.option_text for option in question.options}
    answer = next((option.option_key for option in question.options if option.is_correct), None)
    return options, answer


def plan_missing(records, existing):
    by_key = {normalized(row["question_text"]): row for row in records}
    known = {}
    active = Counter()
    for question in existing:
        key = normalized(question.question_text)
        if key in known:
            raise ValueError(f"Existing Time & Work exact duplicate: {question.question_text!r}")
        known[key] = question
        expected = by_key.get(key)
        if expected:
            options, answer = existing_answer(question)
            if (options != expected["options"] or answer != expected["correct_option"] or question.difficulty.value != expected["difficulty"] or question.is_pyq or not question.is_active):
                raise ValueError(f"Existing exact match conflicts with batch: {question.question_text!r}")
        if question.is_active and not question.is_pyq:
            active[question.difficulty.value] += 1
    for row in records:
        for question in existing:
            if normalized(row["question_text"]) == normalized(question.question_text):
                continue
            if number_masked(row["question_text"]) == number_masked(question.question_text):
                raise ValueError(f"Number-masked duplicate against existing: {row['question_text']!r}")
            if SequenceMatcher(None, normalized(row["question_text"]), normalized(question.question_text)).ratio() >= .92:
                raise ValueError(f"Near duplicate against existing: {row['question_text']!r}")
    deficits = {level: 30 - active[level] for level in LEVELS}
    if any(count < 0 for count in deficits.values()):
        raise ValueError(f"Existing active ordinary counts exceed targets; preserving all rows: {deficits}")
    selected = []
    for row in records:
        key, level = normalized(row["question_text"]), row["difficulty"]
        if key in known or deficits[level] == 0:
            continue
        selected.append(row)
        known[key] = True
        deficits[level] -= 1
    if any(deficits.values()):
        raise ValueError(f"Batch cannot fill difficulty targets: {deficits}")
    return selected


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    engine.echo = False
    records = load_batch()
    print("BATCH", len(records), dict(Counter(row["difficulty"] for row in records)))
    print("PROVENANCE", {"pdf": sum(row["source"].startswith("Verified from supplied PDF:") for row in records), "original": sum(row["source"] == ORIGINAL_SOURCE for row in records)})
    with SessionLocal() as db:
        context = chapter_context(db)
        if context is None:
            raise SystemExit("Active SSC -> Maths -> Arithmetic Maths -> Time & Work chapter not found uniquely")
        _, _, category, chapter = context
        existing = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        before = count_rows(existing)
        print("CHAPTER", chapter.id, chapter.name, chapter.slug)
        print("SUBCATEGORY", category.id, category.name, category.slug)
        print_counts("BEFORE", before)
        try:
            selected = plan_missing(records, existing)
        except ValueError as exc:
            raise SystemExit(str(exc)) from exc
        print("PLANNED_INSERTS", len(selected), dict(Counter(row["difficulty"] for row in selected)))
        if not selected:
            print("NOOP: active ordinary targets met; zero inserts")
            return
        preview = import_questions(db, json.dumps({"questions": selected}, ensure_ascii=False).encode(), "application/json", BATCH.name, True)
        print("DRY_RUN", preview.model_dump())
        if preview.aborted or preview.errors or preview.would_import != len(selected) or preview.duplicates:
            raise SystemExit("Importer dry run did not approve every planned insert")
        if args.dry_run:
            print("NO_DATABASE_CHANGES")
            return
        result = import_questions(db, json.dumps({"questions": selected}, ensure_ascii=False).encode(), "application/json", BATCH.name, False)
        print("IMPORT", result.model_dump())
        if result.aborted or result.errors or result.imported != len(selected):
            raise SystemExit("Import result differs from the approved dry run")
        after_rows = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        after = count_rows(after_rows)
        print_counts("AFTER", after)
        if any(after[(level, "ordinary", "active")] != 30 for level in LEVELS):
            raise SystemExit("Post-import active ordinary counts differ from target")
        print("POST_IMPORT_COUNTS_VERIFIED", len(after_rows))


if __name__ == "__main__":
    main()
