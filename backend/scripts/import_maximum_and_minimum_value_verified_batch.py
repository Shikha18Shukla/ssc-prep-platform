"""Validate, dry-run, and idempotently import the reviewed chapter batch."""
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

BATCH = BASE / "data" / "maximum_and_minimum_value_verified_batch.json"
LEDGER = BASE / "data" / "maximum_and_minimum_value_answer_ledger.json"
LEVELS = ("EASY", "MEDIUM", "HARD")
TARGET = {level: 30 for level in LEVELS}
ORIGINAL = "Original SSC-style practice question"
CHAPTER_ID = "7e7cfd86-403a-4397-99a1-e17d1b5a9e31"


def normalized(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def check_stems(stems, existing=()):
    seen = []
    for stem in stems:
        for prior in seen:
            if SequenceMatcher(None, normalized(stem), normalized(prior)).ratio() >= .97:
                raise ValueError(f"Duplicate or near-duplicate stems: {stem!r} / {prior!r}")
        seen.append(stem)
    for stem in stems:
        for prior in existing:
            if normalized(stem) != normalized(prior) and SequenceMatcher(None, normalized(stem), normalized(prior)).ratio() >= .97:
                raise ValueError(f"Near-duplicate against existing chapter item: {stem!r}")


def load_batch():
    payload = json.loads(BATCH.read_text(encoding="utf-8"))
    rows = payload.get("questions") if isinstance(payload, dict) else None
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    if not isinstance(rows, list) or len(rows) != 90 or not isinstance(ledger, list) or len(ledger) != 90:
        raise ValueError("Batch and answer ledger must each contain exactly 90 rows")
    if Counter(row.get("difficulty") for row in rows) != TARGET:
        raise ValueError("Difficulty distribution must be 30 EASY, 30 MEDIUM, 30 HARD")
    required = {"subject_slug", "subcategory_slug", "chapter_slug", "question_text", "options", "correct_option", "explanation", "difficulty", "is_pyq", "source"}
    for i, (row, audit) in enumerate(zip(rows, ledger), 1):
        if required - set(row):
            raise ValueError(f"Row {i} is missing {required - set(row)}")
        if (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) != ("maths", "advanced-maths", "maximum-and-minimum-value"):
            raise ValueError(f"Row {i} has incorrect catalog slugs")
        if row["is_pyq"] is not False or row.get("pyq_year") is not None or row.get("pyq_exam_name") is not None:
            raise ValueError(f"Row {i} has unsupported PYQ metadata")
        if row["source"] != ORIGINAL and not (row["source"].startswith("Maximum and  Minimum Value.pdf, PDF page ") and "exam/year not stated" in row["source"]):
            raise ValueError(f"Row {i} has invalid provenance")
        options = row["options"]
        if set(options) != set("ABCD") or any(not isinstance(v, str) or not v.strip() for v in options.values()) or len({normalized(v) for v in options.values()}) != 4:
            raise ValueError(f"Row {i} must have four distinct nonempty options")
        if row["correct_option"] not in options or not row["question_text"].strip() or not row["explanation"].strip():
            raise ValueError(f"Row {i} has an invalid stem, key, or explanation")
        if (audit.get("row"), audit.get("question"), audit.get("difficulty"), audit.get("expected_answer")) != (i, row["question_text"], row["difficulty"], options[row["correct_option"]]):
            raise ValueError(f"Row {i} does not match its independent answer ledger")
        if not audit.get("independent_reasoning", "").strip() or audit.get("source") != row["source"]:
            raise ValueError(f"Row {i} lacks ledger reasoning or aligned provenance")
    check_stems([r["question_text"] for r in rows])
    return rows


def chapter_context(db):
    return db.execute(
        select(Exam, Subject, Subcategory, Chapter)
        .join(Subject, Subject.exam_id == Exam.id)
        .join(Subcategory, Subcategory.subject_id == Subject.id)
        .join(Chapter, Chapter.subcategory_id == Subcategory.id)
        .where(Exam.slug == "ssc", Subject.slug == "maths", Subcategory.slug == "advanced-maths", Chapter.slug == "maximum-and-minimum-value")
    ).one_or_none()


def counts(rows):
    return Counter((q.difficulty.value, q.is_active, q.is_pyq) for q in rows)


def plan_missing(records, existing):
    expected = {normalized(r["question_text"]): r for r in records}
    known, active = {}, Counter()
    for q in existing:
        key = normalized(q.question_text)
        if key in known:
            raise ValueError(f"Existing exact duplicate: {q.question_text!r}")
        known[key] = q
        row = expected.get(key)
        if row:
            actual = {o.option_key: o.option_text for o in q.options}
            correct = [o.option_key for o in q.options if o.is_correct]
            if actual != row["options"] or correct != [row["correct_option"]] or q.difficulty.value != row["difficulty"] or q.is_pyq or not q.is_active:
                raise ValueError(f"Existing batch match conflicts with expected row: {q.question_text!r}")
        if q.is_active and not q.is_pyq:
            active[q.difficulty.value] += 1
    check_stems([r["question_text"] for r in records], [q.question_text for q in existing if normalized(q.question_text) not in expected])
    deficits = {level: 30 - active[level] for level in LEVELS}
    if any(n < 0 for n in deficits.values()):
        raise ValueError(f"Existing active ordinary count exceeds target: {deficits}")
    selected = []
    for row in records:
        level = row["difficulty"]
        if normalized(row["question_text"]) not in known and deficits[level] > 0:
            selected.append(row)
            deficits[level] -= 1
    if any(deficits.values()):
        raise ValueError(f"Batch cannot fill chapter targets: {deficits}")
    return selected


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    engine.echo = False
    rows = load_batch()
    print("BATCH", len(rows), dict(Counter(r["difficulty"] for r in rows)))
    print("PROVENANCE", {"source_derived": sum(r["source"] != ORIGINAL for r in rows), "original": sum(r["source"] == ORIGINAL for r in rows), "pyq": 0})
    with SessionLocal() as db:
        context = chapter_context(db)
        if context is None:
            raise SystemExit("Active SSC -> Maths -> Advanced Maths -> Maximum and Minimum Value chapter not found uniquely")
        _, _, _, chapter = context
        if str(chapter.id) != CHAPTER_ID:
            raise SystemExit(f"Chapter ID mismatch: expected {CHAPTER_ID}, found {chapter.id}")
        existing = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        print("CHAPTER", chapter.id, chapter.name, "BEFORE", dict(counts(existing)))
        selected = plan_missing(rows, existing)
        print("PLANNED_INSERTS", len(selected), dict(Counter(r["difficulty"] for r in selected)))
        if not selected:
            print("NOOP: target counts already met; zero inserts")
            return
        body = json.dumps({"questions": selected}, ensure_ascii=False).encode()
        preview = import_questions(db, body, "application/json", BATCH.name, True)
        print("DRY_RUN", preview.model_dump())
        if preview.aborted or preview.errors or preview.would_import != len(selected) or preview.duplicates:
            raise SystemExit("Importer dry run rejected the planned rows")
        if args.dry_run:
            print("NO_DATABASE_CHANGES")
            return
        result = import_questions(db, body, "application/json", BATCH.name, False)
        print("IMPORT", result.model_dump())
        if result.aborted or result.errors or result.imported != len(selected):
            raise SystemExit("Import did not match the successful dry run")
        after = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        final = counts(after)
        print("AFTER", dict(final))
        if any(final[(level, True, False)] != 30 for level in LEVELS) or any(q.is_pyq and q.is_active for q in after):
            raise SystemExit("Post-import chapter counts do not match the requested target")
        if len({normalized(q.question_text) for q in after if q.is_active and not q.is_pyq}) != 90:
            raise SystemExit("Post-import active ordinary stems are not distinct")
        for q in after:
            if q.is_active and not q.is_pyq and len(q.options) != 4 or q.is_active and not q.is_pyq and sum(o.is_correct for o in q.options) != 1:
                raise SystemExit(f"Invalid stored options for {q.question_text!r}")
        print("POST_IMPORT_VERIFIED")


if __name__ == "__main__":
    main()
