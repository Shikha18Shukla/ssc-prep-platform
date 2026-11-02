"""Validate, dry-run, and safely import the reviewed Direction and Distance Normal bank."""

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

BATCH = BASE / "data" / "direction_distance_verified_batch.json"
LEDGER = BASE / "data" / "direction_distance_answer_ledger.json"
EXPECTED_CHAPTER_ID = "4efb2826-617c-4925-b389-4f3047b42dd2"
LEVELS = {"EASY": 12, "MEDIUM": 14, "HARD": 11}
ORIGINAL = "Original SSC-style practice question"


def norm(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def load_artifacts():
    rows = json.loads(BATCH.read_text(encoding="utf-8")).get("questions")
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    if not isinstance(rows, list) or len(rows) != 37 or not isinstance(ledger, list) or len(ledger) != len(rows):
        raise ValueError("Direction and Distance batch and ledger must align and contain exactly 37 records")
    if Counter(row.get("difficulty") for row in rows) != Counter(LEVELS):
        raise ValueError("Difficulty distribution must be 12 EASY, 14 MEDIUM, 11 HARD")
    stems, signatures = set(), set()
    for i, (row, audit) in enumerate(zip(rows, ledger), 1):
        if (row.get("subject_slug"), row.get("subcategory_slug"), row.get("chapter_slug")) != ("reasoning", None, "direction-and-distance"):
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
        if key not in options or len([v for v in options.values() if norm(v) == norm(options[key])]) != 1:
            raise ValueError(f"Row {i} does not have one uniquely keyed choice")
        source = row.get("source")
        valid_pdf = isinstance(source, str) and any(source.startswith(name + ", page ") for name in ("Direction and Distance 01_ Class Notes.pdf", "Direction and Distance 02_ Class Notes.pdf", "_Direction and Distance 03_ Class Notes.pdf")) and source.endswith("; exam/year not stated")
        if source != ORIGINAL and not valid_pdf:
            raise ValueError(f"Row {i} has unsupported provenance")
        if len(source) > 255:
            raise ValueError(f"Row {i} provenance exceeds the database field length")
        stem = norm(row["question_text"])
        if stem in stems:
            raise ValueError(f"Repeated stem in row {i}")
        stems.add(stem)
        if audit.get("question_id") != f"direction-distance-{i:03}" or audit.get("row") != i or audit.get("question") != row["question_text"]:
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
            Subject.is_active.is_(True), Chapter.slug == "direction-and-distance", Chapter.is_active.is_(True),
            Chapter.subcategory_id.is_(None),
        )
    ).one_or_none()


def verify_existing(rows, existing):
    expected = {norm(row["question_text"]): row for row in rows}
    actual = {}
    for question in existing:
        stem = norm(question.question_text)
        if stem in actual or stem not in expected:
            raise ValueError("Unexpected or duplicate existing Direction and Distance question prevents safe import")
        actual[stem] = question
        row = expected[stem]
        options = {o.option_key: o.option_text for o in question.options}
        keys = [o.option_key for o in question.options if o.is_correct]
        if (question.question_text != row["question_text"] or question.explanation != row["explanation"]
                or question.difficulty.value != row["difficulty"] or question.is_pyq is not False
                or question.pyq_year is not None or question.pyq_exam_name is not None
                or question.source != row["source"] or not question.is_active
                or options != row["options"] or keys != [row["correct_option"]]):
            raise ValueError("Existing Direction and Distance question conflicts with canonical batch")
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
            raise SystemExit("Active SSC → Reasoning → Direction and Distance chapter was not found uniquely")
        _, _, chapter = context
        if str(chapter.id) != EXPECTED_CHAPTER_ID:
            raise SystemExit(f"Chapter ID mismatch: expected reference {EXPECTED_CHAPTER_ID}, found {chapter.id}")
        existing = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        normal = sum(q.is_active and not q.is_pyq for q in existing)
        pyq = sum(q.is_active and q.is_pyq for q in existing)
        print("CHAPTER", chapter.id, chapter.name)
        print("BEFORE", {"active_normal": normal, "active_pyq": pyq, "all_records": len(existing)})
        verify_existing(rows, existing)
        if (normal, pyq, len(existing)) not in {(0, 0, 0), (34, 0, 34), (expected_count, 0, expected_count)}:
            raise SystemExit("Baseline must be the verified empty chapter, the prior exact 34-question import, or the completed batch")
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
        if (normal, pyq, len(existing)) not in {(0, 0, 0), (34, 0, 34)} or preview.duplicates != len(existing) or preview.would_import != expected_count - len(existing):
            raise SystemExit("Apply requires an exact known baseline and only the missing canonical questions")
        result = import_questions(db, payload, "application/json", BATCH.name, False)
        print("IMPORT", result.model_dump())
        if result.aborted or result.errors or result.rejected or result.imported != expected_count - len(existing) or result.duplicates != len(existing):
            raise SystemExit("Actual importer results differed from the expected missing inserts and existing duplicates")
        after = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        active_normal = [q for q in after if q.is_active and not q.is_pyq]
        active_pyq = [q for q in after if q.is_active and q.is_pyq]
        if len(active_normal) != expected_count or active_pyq or len(after) != expected_count:
            raise SystemExit("Post-import active Normal/PYQ/total counts do not match the batch")
        verify_existing(rows, after)
        counts = Counter(q.difficulty.value for q in active_normal)
        if counts != Counter(LEVELS):
            raise SystemExit(f"Post-import difficulty counts do not match: {dict(counts)}")
        replay = import_questions(db, payload, "application/json", BATCH.name, True)
        print("REPLAY_DRY_RUN", replay.model_dump())
        if replay.aborted or replay.errors or replay.rejected or replay.would_import or replay.duplicates != expected_count:
            raise SystemExit("Post-import replay was not idempotent")
        print("AFTER", {"active_normal": len(active_normal), "active_pyq": 0, "all_records": len(after), "difficulty": dict(counts)})
        print("POST_IMPORT_VERIFIED")


if __name__ == "__main__":
    main()


