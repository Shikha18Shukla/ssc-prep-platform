"""Validate, dry-run, and safely import the reviewed Syllogism Normal question bank."""

import argparse
import json
import sys
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))

from sqlalchemy import select

from app.database.session import SessionLocal, engine
from app.models import Chapter, Exam, Question, Subject
from app.services.question_import_service import import_questions

BATCH = BASE / "data" / "syllogism_verified_batch.json"
LEDGER = BASE / "data" / "syllogism_answer_ledger.json"
EXPECTED_CHAPTER_ID = "038aaa3d-1348-4c6a-88cd-7ac3378b739d"
LEVELS = {"EASY": 10, "MEDIUM": 10, "HARD": 10}
ORIGINAL = "Original SSC-style practice question"


def norm(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def load_artifacts():
    rows = json.loads(BATCH.read_text(encoding="utf-8")).get("questions")
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    if not isinstance(rows, list) or len(rows) != 30 or not isinstance(ledger, list) or len(ledger) != len(rows):
        raise ValueError("Syllogism batch and ledger must align and contain exactly 30 questions")
    if Counter(row.get("difficulty") for row in rows) != Counter(LEVELS):
        raise ValueError("Syllogism difficulty distribution must be 10 EASY, 10 MEDIUM, 10 HARD")
    seen, signatures = set(), set()
    for index, (row, audit) in enumerate(zip(rows, ledger), 1):
        if (row.get("subject_slug"), row.get("subcategory_slug"), row.get("chapter_slug")) != ("reasoning", None, "syllogism"):
            raise ValueError(f"Question {index} has incorrect catalog metadata")
        if row.get("is_pyq") is not False or row.get("pyq_year") is not None or row.get("pyq_exam_name") is not None:
            raise ValueError(f"Question {index} has incorrect Normal/PYQ metadata")
        if not row.get("question_text", "").strip() or not row.get("explanation", "").strip():
            raise ValueError(f"Question {index} lacks a stem or explanation")
        options = row.get("options")
        if not isinstance(options, dict) or set(options) != set("ABCD"):
            raise ValueError(f"Question {index} must have options A-D")
        if any(not isinstance(value, str) or not value.strip() for value in options.values()) or len({norm(v) for v in options.values()}) != 4:
            raise ValueError(f"Question {index} must have four distinct nonempty options")
        key = row.get("correct_option")
        if key not in options:
            raise ValueError(f"Question {index} has an invalid correct-option key")
        source = row.get("source")
        valid_pdf = isinstance(source, str) and any(
            source.startswith(f"{filename}, page ") and source.endswith("; exam/year not stated")
            for filename in ("Syllogism 01 Class Notes.pdf", "Syllogism 02_ Class Notes.pdf", "Syllogism 03_ Class Notes.pdf")
        )
        if source != ORIGINAL and not valid_pdf:
            raise ValueError(f"Question {index} has invalid provenance")
        if len(source) > 255:
            raise ValueError(f"Question {index} source exceeds the database field limit")
        stem = norm(row["question_text"])
        if stem in seen:
            raise ValueError(f"Question {index} duplicates another stem in this batch")
        seen.add(stem)
        if audit.get("question_id") != f"syllogism-{index:03}" or audit.get("row") != index or audit.get("question") != row["question_text"]:
            raise ValueError(f"Question {index} does not align with its audit record")
        if audit.get("options") != options or audit.get("expected_answer") != options[key] or audit.get("correct_option") != key:
            raise ValueError(f"Question {index} answer key or choices conflict with the audit record")
        if audit.get("difficulty") != row["difficulty"] or audit.get("source") != source:
            raise ValueError(f"Question {index} difficulty/provenance conflicts with the audit record")
        if not audit.get("statements") or not audit.get("verification_status", "").startswith("PASS"):
            raise ValueError(f"Question {index} lacks statement/logic verification evidence")
        signature = audit.get("concept_signature")
        if not signature or signature in signatures:
            raise ValueError(f"Question {index} has a missing or repeated concept signature")
        signatures.add(signature)
    return rows, ledger


def chapter_context(db):
    return db.execute(
        select(Exam, Subject, Chapter)
        .join(Subject, Subject.exam_id == Exam.id)
        .join(Chapter, Chapter.subject_id == Subject.id)
        .where(
            Exam.slug == "ssc", Exam.is_active.is_(True),
            Subject.slug == "reasoning", Subject.is_active.is_(True),
            Chapter.slug == "syllogism", Chapter.is_active.is_(True),
            Chapter.subcategory_id.is_(None),
        )
    ).one_or_none()


def verify_existing(rows, existing):
    expected = {norm(row["question_text"]): row for row in rows}
    actual = {}
    for question in existing:
        stem = norm(question.question_text)
        if stem in actual or stem not in expected:
            raise ValueError("Unexpected or repeated existing Syllogism question blocks a safe import")
        actual[stem] = question
        row = expected[stem]
        options = {option.option_key: option.option_text for option in question.options}
        correct = [option.option_key for option in question.options if option.is_correct]
        if (question.question_text != row["question_text"] or question.explanation != row["explanation"]
                or question.difficulty.value != row["difficulty"] or question.is_pyq is not False
                or question.pyq_year is not None or question.pyq_exam_name is not None
                or question.source != row["source"] or not question.is_active
                or options != row["options"] or correct != [row["correct_option"]]):
            raise ValueError("Existing Syllogism record conflicts with the canonical reviewed batch")
    return actual


def cross_chapter_duplicates(db, chapter_id, rows, threshold=0.97):
    existing = db.scalars(select(Question.question_text).where(
        Question.is_active.is_(True), Question.chapter_id != chapter_id
    )).all()
    normalized = [(norm(text), text) for text in existing]
    matches = []
    for row in rows:
        stem = norm(row["question_text"])
        for other, raw in normalized:
            if stem == other:
                matches.append((row["question_text"], raw, 1.0))
            elif abs(len(stem) - len(other)) <= 0.03 * max(len(stem), len(other)):
                ratio = SequenceMatcher(None, stem, other, autojunk=False).ratio()
                if ratio >= threshold:
                    matches.append((row["question_text"], raw, ratio))
    return len(existing), matches


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="apply after all batch, catalog, duplicate, and dry-run guards pass")
    args = parser.parse_args(argv)
    engine.echo = False
    rows, ledger = load_artifacts()
    print("BATCH", len(rows), dict(Counter(row["difficulty"] for row in rows)))
    print("PROVENANCE", dict(Counter(audit["source_type"] for audit in ledger)))
    with SessionLocal() as db:
        context = chapter_context(db)
        if context is None:
            raise SystemExit("Active SSC → Reasoning → Syllogism chapter was not found uniquely")
        _, _, chapter = context
        if str(chapter.id) != EXPECTED_CHAPTER_ID:
            raise SystemExit(f"Chapter ID mismatch: expected {EXPECTED_CHAPTER_ID}, found {chapter.id}")
        existing = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        active_normal = sum(q.is_active and not q.is_pyq for q in existing)
        active_pyq = sum(q.is_active and q.is_pyq for q in existing)
        print("CHAPTER", chapter.id, chapter.name)
        print("BEFORE", {"active_normal": active_normal, "active_pyq": active_pyq, "all_records": len(existing)})
        verify_existing(rows, existing)
        if (active_normal, active_pyq, len(existing)) not in {(0, 0, 0), (30, 0, 30)}:
            raise SystemExit("Baseline must be empty or the exact completed 30-question Syllogism batch")
        compared, matches = cross_chapter_duplicates(db, chapter.id, rows)
        print("CROSS_CHAPTER_SCAN", {"active_stems": compared, "threshold": 0.97, "matches": matches[:10], "match_count": len(matches)})
        if matches:
            raise SystemExit("Review the cross-chapter near-duplicate matches before importing")
        payload = json.dumps({"questions": rows}, ensure_ascii=False).encode("utf-8")
        preview = import_questions(db, payload, "application/json", BATCH.name, True)
        print("DRY_RUN", preview.model_dump())
        expected_duplicates = len(existing)
        if preview.aborted or preview.errors or preview.rejected or preview.duplicates != expected_duplicates or preview.would_import != 30 - expected_duplicates:
            raise SystemExit("Importer dry-run did not match expected insert/duplicate counts")
        if not args.apply:
            print("NO_DATABASE_CHANGES")
            return
        if active_normal == 30:
            print("IDEMPOTENT_REPLAY: zero additional inserts")
            return
        if existing or preview.duplicates or preview.would_import != 30:
            raise SystemExit("Apply requires the verified empty Syllogism baseline and 30 clean inserts")
        result = import_questions(db, payload, "application/json", BATCH.name, False)
        print("IMPORT", result.model_dump())
        if result.aborted or result.errors or result.rejected or result.imported != 30 or result.duplicates:
            raise SystemExit("Actual import did not produce exactly 30 clean inserts")
        after = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        active_normal_rows = [q for q in after if q.is_active and not q.is_pyq]
        active_pyq_rows = [q for q in after if q.is_active and q.is_pyq]
        counts = Counter(q.difficulty.value for q in active_normal_rows)
        if len(active_normal_rows) != 30 or active_pyq_rows or len(after) != 30 or counts != Counter(LEVELS):
            raise SystemExit(f"Post-import counts do not match requirements: {dict(counts)}, total={len(after)}")
        verify_existing(rows, after)
        replay = import_questions(db, payload, "application/json", BATCH.name, True)
        print("REPLAY_DRY_RUN", replay.model_dump())
        if replay.aborted or replay.errors or replay.rejected or replay.would_import or replay.duplicates != 30:
            raise SystemExit("Post-import replay did not recognize all 30 records as existing")
        print("AFTER", {"active_normal": 30, "active_pyq": 0, "all_records": 30, "difficulty": dict(counts)})
        print("POST_IMPORT_VERIFIED")


if __name__ == "__main__":
    main()
