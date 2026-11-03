"""Guarded dry-run-first importer for the reviewed CH-18 question bank."""
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

BATCH = BASE / "data" / "statement_based_questions_verified_batch.json"
LEDGER = BASE / "data" / "statement_based_questions_answer_ledger.json"
CHAPTER_ID = "74a2c484-5c88-406f-9406-cf4d3d3f5607"
LEVELS = {"EASY": 11, "MEDIUM": 11, "HARD": 10}
ORIGINAL = "Original SSC-style practice question"


def norm(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def load_artifacts():
    rows = json.loads(BATCH.read_text(encoding="utf-8")).get("questions")
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    if not isinstance(rows, list) or len(rows) != 32 or not isinstance(ledger, list) or len(ledger) != 32:
        raise ValueError("CH-18 batch and ledger must each contain exactly 32 records")
    if Counter(row.get("difficulty") for row in rows) != Counter(LEVELS):
        raise ValueError("Difficulty distribution must be 11 EASY, 11 MEDIUM, 10 HARD")
    seen, signatures = set(), set()
    for index, (row, audit) in enumerate(zip(rows, ledger), 1):
        if (row.get("subject_slug"), row.get("subcategory_slug"), row.get("chapter_slug")) != ("reasoning", None, "statement-based-questions"):
            raise ValueError(f"Row {index} chapter metadata mismatch")
        if row.get("is_pyq") is not False or row.get("pyq_year") is not None or row.get("pyq_exam_name") is not None:
            raise ValueError(f"Row {index} must be Normal, not PYQ")
        if row.get("difficulty") not in LEVELS or not row.get("question_text", "").strip() or not row.get("explanation", "").strip():
            raise ValueError(f"Row {index} missing stem/explanation or has invalid difficulty")
        options = row.get("options")
        if not isinstance(options, dict) or set(options) != set("ABCD") or any(not isinstance(v, str) or not v.strip() for v in options.values()) or len({norm(v) for v in options.values()}) != 4:
            raise ValueError(f"Row {index} must have four distinct non-empty options")
        if row.get("correct_option") not in options or audit.get("row") != index or audit.get("id") != f"sbq-{index:03d}":
            raise ValueError(f"Row {index} answer or identity mismatch")
        if audit.get("question") != row["question_text"] or audit.get("options") != options or audit.get("correct_option") != row["correct_option"]:
            raise ValueError(f"Ledger mismatch at row {index}")
        if audit.get("difficulty") != row["difficulty"] or audit.get("independent_reasoning") != row["explanation"] or audit.get("verification_status") != "independently_verified":
            raise ValueError(f"Ledger verification mismatch at row {index}")
        if len(row["source"]) > 255 or (row["source"] != ORIGINAL and ("page " not in row["source"] or "exam/year not stated" not in row["source"])):
            raise ValueError(f"Unsupported provenance at row {index}")
        stem = norm(row["question_text"])
        if stem in seen:
            raise ValueError(f"Duplicate question stem at row {index}")
        seen.add(stem)
        signature = (audit.get("category"), norm(audit.get("statement", "")))
        if signature in signatures:
            raise ValueError(f"Repeated statement scenario at row {index}")
        signatures.add(signature)
    if Counter(row["correct_option"] for row in rows) != Counter({"A": 8, "B": 8, "C": 8, "D": 8}):
        raise ValueError("Correct-answer positions must be balanced at eight each")
    if Counter(item.get("category") for item in ledger) != Counter({"ASSUMPTION": 8, "CONCLUSION": 8, "ARGUMENT": 8, "ACTION": 8}):
        raise ValueError("Each question category must contain eight questions")
    return rows


def chapter_context(db):
    return db.execute(select(Exam, Subject, Chapter).join(Subject, Subject.exam_id == Exam.id).join(Chapter, Chapter.subject_id == Subject.id).where(
        Exam.slug == "ssc", Exam.is_active.is_(True), Subject.slug == "reasoning", Subject.is_active.is_(True),
        Chapter.slug == "statement-based-questions", Chapter.is_active.is_(True), Chapter.subcategory_id.is_(None),
    )).one_or_none()


def verify_existing(rows, existing):
    expected = {norm(row["question_text"]): row for row in rows}
    seen = set()
    for question in existing:
        stem = norm(question.question_text)
        if stem in seen:
            raise ValueError("Database contains duplicate normalized CH-18 stems")
        seen.add(stem)
        row = expected.get(stem)
        if row is None:
            raise ValueError(f"Unexpected CH-18 record; refusing to alter it: {question.question_text!r}")
        option_map = {option.option_key: option.option_text for option in question.options}
        correct = [option.option_key for option in question.options if option.is_correct]
        if (question.question_text != row["question_text"] or question.explanation != row["explanation"]
                or question.difficulty.value != row["difficulty"] or question.is_pyq is not False or not question.is_active
                or question.source != row["source"] or option_map != row["options"] or correct != [row["correct_option"]]):
            raise ValueError(f"Existing record conflicts with canonical CH-18: {question.question_text!r}")


def duplicate_scan(rows, questions):
    candidates = {norm(row["question_text"]): row["question_text"] for row in rows}
    collisions, near = [], []
    for question in questions:
        candidate = norm(question.question_text)
        if candidate in candidates:
            collisions.append((question.id, candidates[candidate]))
            continue
        for stem in candidates.values():
            score = SequenceMatcher(None, candidate, norm(stem)).ratio()
            if score >= 0.92:
                near.append((question.id, round(score, 3), stem))
    if collisions or near:
        raise ValueError(f"Duplicate scan conflict: exact={collisions[:5]}, near={near[:5]}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="apply only after all guarded dry-run checks")
    args = parser.parse_args(argv)
    engine.echo = False
    rows = load_artifacts()
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    print("BATCH", len(rows), dict(Counter(row["difficulty"] for row in rows)))
    print("CATEGORIES", dict(Counter(item["category"] for item in ledger)))
    print("ANSWER_POSITIONS", dict(Counter(row["correct_option"] for row in rows)))
    print("PROVENANCE", {"source_derived": sum(row["source"] != ORIGINAL for row in rows), "original": sum(row["source"] == ORIGINAL for row in rows), "pyq": 0})
    with SessionLocal() as db:
        context = chapter_context(db)
        if context is None:
            raise SystemExit("Active SSC → Reasoning → Statement Based Questions chapter was not found uniquely")
        _, _, chapter = context
        if str(chapter.id) != CHAPTER_ID:
            raise SystemExit(f"CH-18 ID mismatch: expected {CHAPTER_ID}, found {chapter.id}")
        existing = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        normal = sum(q.is_active and not q.is_pyq for q in existing)
        pyq = sum(q.is_active and q.is_pyq for q in existing)
        print("CHAPTER", chapter.id, chapter.name, "BEFORE", {"normal": normal, "pyq": pyq, "records": len(existing)})
        if (normal, pyq, len(existing)) not in {(0, 0, 0), (32, 0, 32)}:
            raise SystemExit("CH-18 baseline differs from empty chapter or exact replay; refusing import")
        verify_existing(rows, existing)
        all_reasoning = db.scalars(select(Question).join(Chapter, Question.chapter_id == Chapter.id).join(Subject, Chapter.subject_id == Subject.id).join(Exam, Subject.exam_id == Exam.id).where(
            Exam.slug == "ssc", Subject.slug == "reasoning", Question.is_active.is_(True), Question.is_pyq.is_(False)
        )).all()
        duplicate_scan(rows, [q for q in all_reasoning if q.chapter_id != chapter.id])
        result = import_questions(db, json.dumps({"questions": rows}, ensure_ascii=False).encode(), "application/json", BATCH.name, True)
        print("DRY_RUN", result.model_dump())
        if result.aborted or result.errors or result.rejected or result.duplicates != len(existing) or result.would_import != 32 - len(existing):
            raise SystemExit("Dry-run did not match guarded insert/replay count")
        if not args.apply:
            print("NO_DATABASE_CHANGES")
            return
        if normal == 32:
            print("IDEMPOTENT_REPLAY: zero additional inserts")
            return
        applied = import_questions(db, json.dumps({"questions": rows}, ensure_ascii=False).encode(), "application/json", BATCH.name, False)
        print("IMPORT", applied.model_dump())
        if applied.aborted or applied.errors or applied.rejected or applied.imported != 32 or applied.duplicates:
            db.rollback()
            raise SystemExit("Import result differed from successful guarded dry-run")
        after = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        verify_existing(rows, after)
        counts = Counter(q.difficulty.value for q in after if q.is_active and not q.is_pyq)
        if len(after) != 32 or counts != Counter(LEVELS) or any(q.is_pyq for q in after):
            db.rollback()
            raise SystemExit(f"Post-import verification failed: records={len(after)}, levels={counts}")
        db.commit()
        print("AFTER", {"active_normal": 32, "active_pyq": 0, "difficulty": dict(counts)})
        print("POST_IMPORT_VERIFIED")


if __name__ == "__main__":
    main()
