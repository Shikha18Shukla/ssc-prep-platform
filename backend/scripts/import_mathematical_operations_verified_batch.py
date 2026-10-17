"""Guarded dry-run/import for the reviewed Mathematical Operations Normal bank."""

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

BATCH = BASE / "data" / "mathematical_operations_verified_batch.json"
LEDGER = BASE / "data" / "mathematical_operations_answer_ledger.json"
EXPECTED_CHAPTER_ID = "a9a0ce3b-9d82-401e-8ed7-c73d0110c646"
LEVELS = {"EASY": 10, "MEDIUM": 12, "HARD": 8}


def norm(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def load_artifacts():
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    rows = batch.get("questions") if isinstance(batch, dict) else None
    if not isinstance(rows, list) or len(rows) != 30 or not isinstance(ledger, list) or len(ledger) != 30:
        raise ValueError("Batch and answer ledger must each contain exactly 30 records")
    if Counter(row.get("difficulty") for row in rows) != Counter(LEVELS):
        raise ValueError("Expected difficulty distribution is 10 EASY, 12 MEDIUM, 8 HARD")
    stems, signatures = set(), set()
    for i, (row, audit) in enumerate(zip(rows, ledger), 1):
        if (row.get("subject_slug"), row.get("subcategory_slug"), row.get("chapter_slug")) != ("reasoning", None, "mathematical-operations"):
            raise ValueError(f"Row {i} has incorrect catalog metadata")
        if row.get("is_pyq") is not False or row.get("pyq_year") is not None or row.get("pyq_exam_name") is not None:
            raise ValueError(f"Row {i} is not Normal metadata")
        if not isinstance(row.get("question_text"), str) or not row["question_text"].strip() or not isinstance(row.get("explanation"), str) or not row["explanation"].strip():
            raise ValueError(f"Row {i} is missing its question or explanation")
        if row.get("difficulty") not in LEVELS:
            raise ValueError(f"Row {i} has an invalid difficulty")
        if not isinstance(row.get("options"), dict) or set(row["options"]) != set("ABCD"):
            raise ValueError(f"Row {i} must have exactly options A-D")
        options = row["options"]
        if any(not isinstance(value, str) or not value.strip() for value in options.values()) or len({norm(value) for value in options.values()}) != 4:
            raise ValueError(f"Row {i} must have four distinct nonempty options")
        key = row.get("correct_option")
        if key not in options:
            raise ValueError(f"Row {i} has an invalid correct option")
        source = row.get("source")
        if not isinstance(source, str) or len(source) > 255 or not source.endswith("; exam/year not stated"):
            raise ValueError(f"Row {i} has unsupported or invalid provenance")
        if not (source.startswith("Mathematical Operations 01 _.pdf, page ") or source.startswith("Mathematical Operations 02_.pdf, page ")):
            raise ValueError(f"Row {i} references an unknown PDF")
        stem = norm(row["question_text"])
        if stem in stems:
            raise ValueError(f"Duplicate normalized stem at row {i}")
        stems.add(stem)
        if audit.get("row") != i or audit.get("question") != row["question_text"]:
            raise ValueError(f"Ledger does not align at row {i}")
        if audit.get("expected_answer") != options[key] or audit.get("correct_option") != key:
            raise ValueError(f"Ledger answer mismatch at row {i}")
        if audit.get("difficulty") != row["difficulty"] or audit.get("source") != source or audit.get("source_type") != "pdf-derived":
            raise ValueError(f"Ledger metadata mismatch at row {i}")
        if not audit.get("independent_reasoning", "").strip() or not audit.get("option_review", "").strip():
            raise ValueError(f"Ledger verification is incomplete at row {i}")
        signature = audit.get("concept_signature")
        if not signature or signature in signatures:
            raise ValueError(f"Missing or repeated concept signature at row {i}")
        signatures.add(signature)
    return rows


def chapter_context(db):
    return db.execute(
        select(Exam, Subject, Chapter)
        .join(Subject, Subject.exam_id == Exam.id)
        .join(Chapter, Chapter.subject_id == Subject.id)
        .where(
            Exam.slug == "ssc", Exam.is_active.is_(True),
            Subject.slug == "reasoning", Subject.is_active.is_(True),
            Chapter.slug == "mathematical-operations", Chapter.is_active.is_(True),
            Chapter.subcategory_id.is_(None),
        )
    ).one_or_none()


def verify_existing(rows, existing):
    expected = {norm(row["question_text"]): row for row in rows}
    actual = {}
    for question in existing:
        stem = norm(question.question_text)
        if stem in actual:
            raise ValueError("Database contains duplicate normalized Mathematical Operations stems")
        row = expected.get(stem)
        if row is None:
            raise ValueError(f"Unexpected database record; refusing to alter it: {question.question_text!r}")
        actual[stem] = question
        options = {option.option_key: option.option_text for option in question.options}
        keys = [option.option_key for option in question.options if option.is_correct]
        if (
            question.question_text != row["question_text"] or question.explanation != row["explanation"]
            or question.difficulty.value != row["difficulty"] or question.is_pyq is not False
            or question.pyq_year is not None or question.pyq_exam_name is not None
            or question.source != row["source"] or not question.is_active
            or options != row["options"] or keys != [row["correct_option"]]
        ):
            raise ValueError(f"Existing record conflicts with canonical batch: {question.question_text!r}")
    return actual


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="import only after the guarded dry-run succeeds")
    args = parser.parse_args(argv)
    engine.echo = False
    rows = load_artifacts()
    payload = json.dumps({"questions": rows}, ensure_ascii=False).encode("utf-8")
    print("BATCH", len(rows), dict(Counter(row["difficulty"] for row in rows)))
    print("PROVENANCE", {"pdf_1": sum("01 _.pdf" in row["source"] for row in rows), "pdf_2": sum("02_.pdf" in row["source"] for row in rows), "original": 0, "pyq": 0})
    with SessionLocal() as db:
        context = chapter_context(db)
        if context is None:
            raise SystemExit("Active SSC → Reasoning → Mathematical Operations chapter was not found uniquely")
        _, _, chapter = context
        if str(chapter.id) != EXPECTED_CHAPTER_ID:
            raise SystemExit(f"Chapter ID mismatch: expected {EXPECTED_CHAPTER_ID}, found {chapter.id}")
        existing = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        normal = [q for q in existing if q.is_active and not q.is_pyq]
        pyq = [q for q in existing if q.is_active and q.is_pyq]
        print("CHAPTER", chapter.id, chapter.name)
        print("BEFORE", {"active_normal": len(normal), "active_pyq": len(pyq), "all_records": len(existing)})
        matched = verify_existing(rows, existing)
        if len(existing) == 0:
            if normal or pyq:
                raise SystemExit("Unexpected empty-chapter count state")
        elif len(existing) == 30:
            if len(normal) != 30 or pyq or Counter(q.difficulty.value for q in normal) != Counter(LEVELS):
                raise SystemExit("Existing records do not form an exact canonical replay")
        else:
            raise SystemExit("Baseline differs from empty chapter or exact replay; no database changes performed")
        preview = import_questions(db, payload, "application/json", BATCH.name, True)
        print("DRY_RUN", preview.model_dump())
        expected_inserts = 30 - len(matched)
        if preview.aborted or preview.errors or preview.rejected or preview.duplicates != len(matched) or preview.would_import != expected_inserts:
            raise SystemExit("Dry-run did not match the guarded insert or replay count")
        if not args.apply:
            print("NO_DATABASE_CHANGES")
            return
        if len(existing) == 30:
            print("IDEMPOTENT_REPLAY: zero additional inserts")
            return
        if len(existing) != 0 or preview.would_import != 30:
            raise SystemExit("Apply requires confirmed 0 Normal / 0 PYQ / 0 total and exactly 30 inserts")
        result = import_questions(db, payload, "application/json", BATCH.name, False)
        print("IMPORT", result.model_dump())
        if result.aborted or result.errors or result.rejected or result.duplicates or result.imported != 30:
            raise SystemExit("Import results differed from the successful dry-run")
        after = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        normal_after = [q for q in after if q.is_active and not q.is_pyq]
        pyq_after = [q for q in after if q.is_active and q.is_pyq]
        if len(after) != 30 or len(normal_after) != 30 or pyq_after:
            raise SystemExit(f"Post-import count mismatch: active Normal={len(normal_after)}, PYQ={len(pyq_after)}, all={len(after)}")
        verify_existing(rows, after)
        distribution = Counter(q.difficulty.value for q in normal_after)
        if distribution != Counter(LEVELS):
            raise SystemExit(f"Post-import difficulty mismatch: {distribution}")
        replay = import_questions(db, payload, "application/json", BATCH.name, True)
        print("REPLAY_DRY_RUN", replay.model_dump())
        if replay.aborted or replay.errors or replay.rejected or replay.duplicates != 30 or replay.would_import != 0:
            raise SystemExit("Replay dry-run was not idempotent")
        print("AFTER", {"active_normal": len(normal_after), "active_pyq": len(pyq_after), "all_records": len(after), "difficulty": dict(distribution)})
        print("POST_IMPORT_VERIFIED")


if __name__ == "__main__":
    main()
