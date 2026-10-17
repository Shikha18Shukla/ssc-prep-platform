"""Validate, dry-run, and idempotently import the Classification Normal bank."""

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
from app.models import Chapter, Difficulty, Exam, Question, Subject
from app.services.question_import_service import import_questions

BATCH = BASE / "data" / "classification_verified_batch.json"
LEDGER = BASE / "data" / "classification_answer_ledger.json"
EXPECTED_CHAPTER_ID = "8179a4a3-b760-4a0d-bb35-a71dc5964b0b"
LEVELS = {"EASY": 10, "MEDIUM": 12, "HARD": 8}
ORIGINAL = "Original SSC-style practice question"


def norm(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def load_artifacts():
    rows = json.loads(BATCH.read_text(encoding="utf-8")).get("questions")
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    if not isinstance(rows, list) or len(rows) != 30 or not isinstance(ledger, list) or len(ledger) != 30:
        raise ValueError("Classification batch and ledger must each contain exactly 30 records")
    if Counter(row.get("difficulty") for row in rows) != Counter(LEVELS):
        raise ValueError("Difficulty distribution must be 10 EASY, 12 MEDIUM, 8 HARD")
    stems, signatures = set(), set()
    for i, (row, audit) in enumerate(zip(rows, ledger), 1):
        if (row.get("subject_slug"), row.get("subcategory_slug"), row.get("chapter_slug")) != ("reasoning", None, "classification"):
            raise ValueError(f"Row {i} has incorrect catalog metadata")
        if row.get("is_pyq") is not False or row.get("pyq_year") is not None or row.get("pyq_exam_name") is not None:
            raise ValueError(f"Row {i} is not valid Normal metadata")
        if not row.get("question_text", "").strip() or not row.get("explanation", "").strip():
            raise ValueError(f"Row {i} is missing its stem or explanation")
        if row["difficulty"] not in LEVELS:
            raise ValueError(f"Row {i} has an invalid difficulty")
        options = row.get("options")
        if not isinstance(options, dict) or set(options) != set("ABCD"):
            raise ValueError(f"Row {i} must have exactly options A-D")
        if any(not isinstance(v, str) or not v.strip() for v in options.values()) or len({norm(v) for v in options.values()}) != 4:
            raise ValueError(f"Row {i} options must be four distinct, nonempty strings")
        key = row.get("correct_option")
        if key not in options:
            raise ValueError(f"Row {i} has an invalid answer key")
        source = row.get("source")
        if not isinstance(source, str) or not source or len(source) > 255:
            raise ValueError(f"Row {i} has invalid source metadata")
        if source != ORIGINAL and not (source.startswith("Classification 0") and "lecture slide " in source and "exam/year not stated" in source):
            raise ValueError(f"Row {i} has unsupported source provenance")
        stem = norm(row["question_text"])
        if stem in stems:
            raise ValueError(f"Duplicate stem in row {i}")
        stems.add(stem)
        if audit.get("row") != i or audit.get("question") != row["question_text"]:
            raise ValueError(f"Row {i} does not align with the ledger")
        if audit.get("expected_answer") != options[key] or audit.get("correct_option") != key:
            raise ValueError(f"Row {i} answer conflicts with ledger")
        if audit.get("difficulty") != row["difficulty"] or audit.get("source") != source:
            raise ValueError(f"Row {i} difficulty/source conflicts with ledger")
        if not audit.get("independent_reasoning", "").strip() or not audit.get("option_review", "").strip():
            raise ValueError(f"Row {i} lacks answer or option review")
        signature = audit.get("concept_signature")
        if not signature or signature in signatures:
            raise ValueError(f"Row {i} has a missing or repeated problem signature")
        signatures.add(signature)
    return rows


def chapter_context(db):
    return db.execute(
        select(Exam, Subject, Chapter)
        .join(Subject, Subject.exam_id == Exam.id)
        .join(Chapter, Chapter.subject_id == Subject.id)
        .where(
            Exam.slug == "ssc", Exam.is_active.is_(True), Subject.slug == "reasoning",
            Subject.is_active.is_(True), Chapter.slug == "classification", Chapter.is_active.is_(True),
            Chapter.subcategory_id.is_(None),
        )
    ).one_or_none()


def verify_existing(rows, existing):
    by_stem = {norm(row["question_text"]): row for row in rows}
    actual = {}
    for question in existing:
        stem = norm(question.question_text)
        if stem in actual:
            raise ValueError("Database contains duplicate normalized Classification stems")
        actual[stem] = question
        expected = by_stem.get(stem)
        if expected is None:
            raise ValueError(f"Unexpected existing Classification question prevents safe import: {question.question_text!r}")
        options = {option.option_key: option.option_text for option in question.options}
        keys = [option.option_key for option in question.options if option.is_correct]
        if (
            question.question_text != expected["question_text"] or question.explanation != expected["explanation"]
            or question.difficulty.value != expected["difficulty"] or question.is_pyq is not False
            or question.pyq_year is not None or question.pyq_exam_name is not None
            or question.source != expected["source"] or not question.is_active
            or options != expected["options"] or keys != [expected["correct_option"]]
        ):
            raise ValueError(f"Existing question conflicts with canonical batch: {question.question_text!r}")
    return actual


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="apply after a successful dry-run")
    args = parser.parse_args(argv)
    engine.echo = False
    rows = load_artifacts()
    print("BATCH", len(rows), dict(Counter(row["difficulty"] for row in rows)))
    print("PROVENANCE", {"pdf_derived": sum(row["source"] != ORIGINAL for row in rows), "original": sum(row["source"] == ORIGINAL for row in rows), "pyq": 0})
    with SessionLocal() as db:
        context = chapter_context(db)
        if context is None:
            raise SystemExit("Active SSC → Reasoning → Classification chapter was not found uniquely")
        _, _, chapter = context
        if str(chapter.id) != EXPECTED_CHAPTER_ID:
            raise SystemExit(f"Chapter ID mismatch: expected {EXPECTED_CHAPTER_ID}, found {chapter.id}")
        existing = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        active_normal = sum(q.is_active and not q.is_pyq for q in existing)
        active_pyq = sum(q.is_active and q.is_pyq for q in existing)
        print("CHAPTER", chapter.id, chapter.name)
        print("BEFORE", {"active_normal": active_normal, "active_pyq": active_pyq, "all_records": len(existing)})
        verify_existing(rows, existing)
        if (active_normal, active_pyq) not in {(0, 0), (30, 0)}:
            raise SystemExit("Baseline differs from empty chapter or verified replay; no import performed")
        if active_normal == 0 and existing:
            raise SystemExit("Inactive or non-active chapter records exist; stop for manual review")
        payload = json.dumps({"questions": rows}, ensure_ascii=False).encode("utf-8")
        preview = import_questions(db, payload, "application/json", BATCH.name, True)
        print("DRY_RUN", preview.model_dump())
        if preview.aborted or preview.errors or preview.rejected or preview.duplicates != len(existing) or preview.would_import != 30 - len(existing):
            raise SystemExit("Importer dry-run did not match expected insert/duplicate counts")
        if not args.apply:
            print("NO_DATABASE_CHANGES")
            return
        if active_normal == 30:
            print("IDEMPOTENT_REPLAY: zero additional inserts")
            return
        if active_normal != 0 or active_pyq != 0 or len(existing) != 0 or preview.would_import != 30:
            raise SystemExit("Apply requires confirmed 0 Normal / 0 PYQ / 0 total and exactly 30 inserts")
        result = import_questions(db, payload, "application/json", BATCH.name, False)
        print("IMPORT", result.model_dump())
        if result.aborted or result.errors or result.imported != 30 or result.duplicates:
            raise SystemExit("Actual importer results differed from dry-run")
        after = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        normal = [q for q in after if q.is_active and not q.is_pyq]
        pyq = [q for q in after if q.is_active and q.is_pyq]
        if len(normal) != 30 or pyq or len(after) != 30:
            raise SystemExit(f"Post-import mismatch: active Normal={len(normal)}, PYQ={len(pyq)}, all={len(after)}")
        verify_existing(rows, after)
        print("AFTER", {"active_normal": len(normal), "active_pyq": len(pyq), "all_records": len(after)})
        print("POST_IMPORT_VERIFIED")


if __name__ == "__main__":
    main()
