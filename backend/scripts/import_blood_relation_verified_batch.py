"""Validate, dry-run, and idempotently import the reviewed Blood Relation Normal bank."""

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

BATCH = BASE / "data" / "blood_relation_verified_batch.json"
LEDGER = BASE / "data" / "blood_relation_answer_ledger.json"
EXPECTED_CHAPTER_ID = "cf83a214-1a3c-4af9-89bf-63b25503a2bf"
LEVELS = {"EASY": 10, "MEDIUM": 12, "HARD": 8}
ORIGINAL = "Original SSC-style practice question"


def norm(text):
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def load_artifacts():
    rows = json.loads(BATCH.read_text(encoding="utf-8")).get("questions")
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    if not isinstance(rows, list) or len(rows) != 30 or not isinstance(ledger, list) or len(ledger) != 30:
        raise ValueError("Blood Relation batch and ledger must each contain 30 rows")
    if Counter(row.get("difficulty") for row in rows) != Counter(LEVELS):
        raise ValueError("Difficulty distribution must be 10 EASY, 12 MEDIUM, 8 HARD")
    stems, signatures = set(), set()
    for index, (row, audit) in enumerate(zip(rows, ledger), 1):
        if (row.get("subject_slug"), row.get("subcategory_slug"), row.get("chapter_slug")) != ("reasoning", None, "blood-relation"):
            raise ValueError(f"Row {index} has incorrect chapter metadata")
        if row.get("is_pyq") is not False or row.get("pyq_year") is not None or row.get("pyq_exam_name") is not None:
            raise ValueError(f"Row {index} is not Normal metadata")
        if not row.get("question_text", "").strip() or not row.get("explanation", "").strip():
            raise ValueError(f"Row {index} lacks a stem or explanation")
        options = row.get("options")
        if not isinstance(options, dict) or set(options) != set("ABCD"):
            raise ValueError(f"Row {index} must have choices A-D")
        if any(not isinstance(value, str) or not value.strip() for value in options.values()) or len({norm(value) for value in options.values()}) != 4:
            raise ValueError(f"Row {index} options must be four distinct nonempty strings")
        if row.get("correct_option") not in options:
            raise ValueError(f"Row {index} has an invalid answer key")
        source = row.get("source")
        if not isinstance(source, str) or not source or len(source) > 255:
            raise ValueError(f"Row {index} has invalid source metadata")
        if source != ORIGINAL and not (source.startswith("Blood relation 0") and "lecture slide " in source and "exam/year not stated" in source):
            raise ValueError(f"Row {index} claims unsupported source provenance")
        stem = norm(row["question_text"])
        if stem in stems:
            raise ValueError(f"Duplicate normalized stem at row {index}")
        stems.add(stem)
        if audit.get("row") != index or audit.get("question") != row["question_text"]:
            raise ValueError(f"Ledger misalignment at row {index}")
        if audit.get("expected_answer") != options[row["correct_option"]] or audit.get("correct_option") != row["correct_option"]:
            raise ValueError(f"Ledger answer mismatch at row {index}")
        if audit.get("difficulty") != row["difficulty"] or audit.get("source") != source:
            raise ValueError(f"Ledger metadata mismatch at row {index}")
        if not audit.get("independent_reasoning", "").strip() or not audit.get("option_review", "").strip():
            raise ValueError(f"Ledger lacks verification notes at row {index}")
        signature = audit.get("concept_signature")
        if not signature or signature in signatures:
            raise ValueError(f"Missing or repeated concept signature at row {index}")
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
            Chapter.slug == "blood-relation", Chapter.is_active.is_(True),
            Chapter.subcategory_id.is_(None),
        )
    ).one_or_none()


def verify_existing(rows, existing):
    expected = {norm(row["question_text"]): row for row in rows}
    seen = set()
    for question in existing:
        stem = norm(question.question_text)
        if stem in seen:
            raise ValueError("Database contains duplicate normalized Blood Relation stems")
        seen.add(stem)
        row = expected.get(stem)
        if row is None:
            raise ValueError(f"Unexpected existing question; refusing to alter it: {question.question_text!r}")
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


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="apply after a successful guarded dry-run")
    args = parser.parse_args(argv)
    engine.echo = False
    rows = load_artifacts()
    print("BATCH", len(rows), dict(Counter(row["difficulty"] for row in rows)))
    print("PROVENANCE", {"pdf_derived": sum(row["source"] != ORIGINAL for row in rows), "original": sum(row["source"] == ORIGINAL for row in rows), "pyq": 0})
    with SessionLocal() as db:
        context = chapter_context(db)
        if context is None:
            raise SystemExit("Active SSC → Reasoning → Blood Relation chapter was not found uniquely")
        _, _, chapter = context
        if str(chapter.id) != EXPECTED_CHAPTER_ID:
            raise SystemExit(f"Chapter ID mismatch: expected {EXPECTED_CHAPTER_ID}, found {chapter.id}")
        existing = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        normal = sum(q.is_active and not q.is_pyq for q in existing)
        pyq = sum(q.is_active and q.is_pyq for q in existing)
        print("CHAPTER", chapter.id, chapter.name)
        print("BEFORE", {"active_normal": normal, "active_pyq": pyq, "all_records": len(existing)})
        verify_existing(rows, existing)
        if (normal, pyq, len(existing)) not in {(0, 0, 0), (30, 0, 30)}:
            raise SystemExit("Baseline differs from empty chapter or exact replay; no import performed")
        payload = json.dumps({"questions": rows}, ensure_ascii=False).encode("utf-8")
        preview = import_questions(db, payload, "application/json", BATCH.name, True)
        print("DRY_RUN", preview.model_dump())
        if preview.aborted or preview.errors or preview.rejected or preview.duplicates != len(existing) or preview.would_import != 30 - len(existing):
            raise SystemExit("Dry-run did not match the guarded insert/replay count")
        if not args.apply:
            print("NO_DATABASE_CHANGES")
            return
        if normal == 30:
            print("IDEMPOTENT_REPLAY: zero additional inserts")
            return
        result = import_questions(db, payload, "application/json", BATCH.name, False)
        print("IMPORT", result.model_dump())
        if result.aborted or result.errors or result.rejected or result.imported != 30 or result.duplicates:
            raise SystemExit("Import result differed from successful dry-run")
        after = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        active_normal = [q for q in after if q.is_active and not q.is_pyq]
        active_pyq = [q for q in after if q.is_active and q.is_pyq]
        if len(after) != 30 or len(active_normal) != 30 or active_pyq:
            raise SystemExit(f"Post-import counts mismatch: Normal={len(active_normal)}, PYQ={len(active_pyq)}, total={len(after)}")
        verify_existing(rows, after)
        distribution = Counter(q.difficulty.value for q in active_normal)
        if distribution != Counter(LEVELS):
            raise SystemExit(f"Post-import difficulty distribution mismatch: {distribution}")
        print("AFTER", {"active_normal": len(active_normal), "active_pyq": len(active_pyq), "all_records": len(after), "difficulty": dict(distribution)})
        print("POST_IMPORT_VERIFIED")


if __name__ == "__main__":
    main()
