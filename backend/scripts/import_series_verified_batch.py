"""Validate, dry-run, and safely import the reviewed Series Normal bank."""

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

BATCH = BASE / "data" / "series_verified_batch.json"
LEDGER = BASE / "data" / "series_answer_ledger.json"
EXPECTED_CHAPTER_ID = "782b2b35-1c76-47e6-9e26-73ed87f6b6bb"
LEVELS = {"EASY": 10, "MEDIUM": 12, "HARD": 10}
APPEND_BASELINE = 30
ORIGINAL = "Original SSC-style practice question"


def norm(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def load_artifacts():
    rows = json.loads(BATCH.read_text(encoding="utf-8")).get("questions")
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    if not isinstance(rows, list) or len(rows) != 32 or not isinstance(ledger, list) or len(ledger) != len(rows):
        raise ValueError("Series batch and ledger must align and contain exactly 32 records")
    if Counter(row.get("difficulty") for row in rows) != Counter(LEVELS):
        raise ValueError("Difficulty distribution must be 10 EASY, 12 MEDIUM, 10 HARD")
    stems, signatures = set(), set()
    for i, (row, audit) in enumerate(zip(rows, ledger), 1):
        if (row.get("subject_slug"), row.get("subcategory_slug"), row.get("chapter_slug")) != ("reasoning", None, "series"):
            raise ValueError(f"Row {i} has incorrect catalog metadata")
        if row.get("is_pyq") is not False or row.get("pyq_year") is not None or row.get("pyq_exam_name") is not None:
            raise ValueError(f"Row {i} is not valid Normal metadata")
        if not row.get("question_text", "").strip() or not row.get("explanation", "").strip():
            raise ValueError(f"Row {i} is missing its stem or explanation")
        if row.get("difficulty") not in LEVELS:
            raise ValueError(f"Row {i} has an invalid difficulty")
        options = row.get("options")
        if not isinstance(options, dict) or set(options) != set("ABCD"):
            raise ValueError(f"Row {i} must have exactly options A-D")
        if any(not isinstance(v, str) or not v.strip() for v in options.values()) or len({norm(v) for v in options.values()}) != 4:
            raise ValueError(f"Row {i} options must be four distinct nonempty strings")
        key = row.get("correct_option")
        if key not in options or sum(norm(v) == norm(options[key]) for v in options.values()) != 1:
            raise ValueError(f"Row {i} does not have one uniquely keyed choice")
        source = row.get("source")
        valid_pdf = any(source.startswith(f"Series 0{n}_ Class Notes.pdf, page ") and source.endswith("; exam/year not stated") for n in (1, 2, 3)) if isinstance(source, str) else False
        if source != ORIGINAL and not valid_pdf:
            raise ValueError(f"Row {i} has unsupported provenance")
        stem = norm(row["question_text"])
        if stem in stems:
            raise ValueError(f"Repeated stem in row {i}")
        stems.add(stem)
        if audit.get("question_id") != f"series-{i:03}" or audit.get("row") != i or audit.get("question") != row["question_text"]:
            raise ValueError(f"Row {i} does not align with stable ledger identifiers")
        if audit.get("expected_answer") != options[key] or audit.get("correct_option") != key:
            raise ValueError(f"Row {i} answer conflicts with ledger")
        if audit.get("difficulty") != row["difficulty"] or audit.get("source") != source:
            raise ValueError(f"Row {i} difficulty/source conflicts with ledger")
        if not audit.get("independent_reasoning", "").strip() or not audit.get("option_review", "").strip():
            raise ValueError(f"Row {i} lacks answer or option review")
        signature = audit.get("concept_signature")
        if not signature or signature in signatures:
            raise ValueError(f"Row {i} has a missing or repeated concept signature")
        signatures.add(signature)
        if source == ORIGINAL:
            if audit.get("source_type") != "original" or audit.get("source_pdf") is not None or audit.get("source_page") is not None:
                raise ValueError(f"Row {i} has fabricated provenance for an original question")
        elif audit.get("source_type") != "pdf-derived" or audit.get("source_pdf") not in source or not isinstance(audit.get("source_page"), int):
            raise ValueError(f"Row {i} PDF ledger provenance is incomplete")
    return rows


def chapter_context(db):
    return db.execute(
        select(Exam, Subject, Chapter)
        .join(Subject, Subject.exam_id == Exam.id)
        .join(Chapter, Chapter.subject_id == Subject.id)
        .where(
            Exam.slug == "ssc", Exam.is_active.is_(True), Subject.slug == "reasoning",
            Subject.is_active.is_(True), Chapter.slug == "series", Chapter.is_active.is_(True),
            Chapter.subcategory_id.is_(None),
        )
    ).one_or_none()


def verify_existing(rows, existing):
    expected = {norm(row["question_text"]): row for row in rows}
    actual = {}
    for question in existing:
        stem = norm(question.question_text)
        if stem in actual or stem not in expected:
            raise ValueError("Unexpected or duplicate existing Series question prevents safe import")
        actual[stem] = question
        row = expected[stem]
        options = {o.option_key: o.option_text for o in question.options}
        keys = [o.option_key for o in question.options if o.is_correct]
        if (question.question_text != row["question_text"] or question.explanation != row["explanation"]
                or question.difficulty.value != row["difficulty"] or question.is_pyq is not False
                or question.pyq_year is not None or question.pyq_exam_name is not None
                or question.source != row["source"] or not question.is_active
                or options != row["options"] or keys != [row["correct_option"]]):
            raise ValueError("Existing Series question conflicts with canonical batch")
    return actual


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="apply only after all dry-run guards pass")
    args = parser.parse_args(argv)
    engine.echo = False
    rows = load_artifacts()
    expected_count = len(rows)
    print("BATCH", expected_count, dict(Counter(row["difficulty"] for row in rows)))
    with SessionLocal() as db:
        context = chapter_context(db)
        if context is None:
            raise SystemExit("Active SSC → Reasoning → Series chapter was not found uniquely")
        _, _, chapter = context
        if str(chapter.id) != EXPECTED_CHAPTER_ID:
            raise SystemExit(f"Chapter ID mismatch: expected reference {EXPECTED_CHAPTER_ID}, found {chapter.id}")
        existing = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        normal = sum(q.is_active and not q.is_pyq for q in existing)
        pyq = sum(q.is_active and q.is_pyq for q in existing)
        print("CHAPTER", chapter.id, chapter.name)
        print("BEFORE", {"active_normal": normal, "active_pyq": pyq, "all_records": len(existing)})
        verify_existing(rows, existing)
        if (normal, pyq, len(existing)) not in {
            (APPEND_BASELINE, 0, APPEND_BASELINE),
            (expected_count, 0, expected_count),
        }:
            raise SystemExit("Baseline must be the previously verified 30-question Series bank or the exact completed 32-question bank")
        payload = json.dumps({"questions": rows}, ensure_ascii=False).encode("utf-8")
        preview = import_questions(db, payload, "application/json", BATCH.name, True)
        print("DRY_RUN", preview.model_dump())
        if preview.aborted or preview.errors or preview.rejected or preview.duplicates != len(existing) or preview.would_import != expected_count - len(existing):
            raise SystemExit("Importer dry-run did not match expected insert/duplicate counts")
        if not args.apply:
            print("NO_DATABASE_CHANGES")
            return
        if normal == expected_count:
            print("IDEMPOTENT_REPLAY: zero additional inserts")
            return
        if normal != APPEND_BASELINE or pyq or len(existing) != APPEND_BASELINE or preview.duplicates != APPEND_BASELINE or preview.would_import != expected_count - APPEND_BASELINE:
            raise SystemExit("Apply requires the exact verified 30-question baseline and exactly two new questions")
        result = import_questions(db, payload, "application/json", BATCH.name, False)
        print("IMPORT", result.model_dump())
        if result.aborted or result.errors or result.rejected or result.imported != expected_count - APPEND_BASELINE or result.duplicates != APPEND_BASELINE:
            raise SystemExit("Actual importer results differed from the expected 30 duplicates and two inserts")
        after = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        active_normal = [q for q in after if q.is_active and not q.is_pyq]
        active_pyq = [q for q in after if q.is_active and q.is_pyq]
        if len(active_normal) != expected_count or active_pyq or len(after) != expected_count:
            raise SystemExit("Post-import active Normal/PYQ/total counts do not match the batch")
        verify_existing(rows, after)
        replay = import_questions(db, payload, "application/json", BATCH.name, True)
        print("REPLAY_DRY_RUN", replay.model_dump())
        if replay.aborted or replay.errors or replay.rejected or replay.would_import or replay.duplicates != expected_count:
            raise SystemExit("Post-import replay was not idempotent")
        print("AFTER", {"active_normal": len(active_normal), "active_pyq": 0, "all_records": len(after)})
        print("POST_IMPORT_VERIFIED")


if __name__ == "__main__":
    main()
