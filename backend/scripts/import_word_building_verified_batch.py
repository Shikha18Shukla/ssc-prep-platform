"""Validate, dry-run and safely import the CH-15 Word Building Normal bank."""

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

BATCH = BASE / "data" / "word_building_verified_batch.json"
LEDGER = BASE / "data" / "word_building_answer_ledger.json"
EXPECTED_CHAPTER_ID = "886e3a61-031f-48ce-9c62-aff6db3ba7a5"
EXPECTED_COUNTS = Counter({"EASY": 10, "MEDIUM": 10, "HARD": 10})
ORIGINAL = "Original SSC-style practice question"


def norm(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def load_artifacts():
    rows = json.loads(BATCH.read_text(encoding="utf-8")).get("questions")
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    if not isinstance(rows, list) or len(rows) != 30 or not isinstance(ledger, list) or len(ledger) != len(rows):
        raise ValueError("Word Building batch and ledger must align and contain 30 questions")
    if Counter(row.get("difficulty") for row in rows) != EXPECTED_COUNTS:
        raise ValueError("Difficulty counts must be 10 EASY, 10 MEDIUM and 10 HARD")
    stems, signatures = set(), set()
    for i, (row, audit) in enumerate(zip(rows, ledger), 1):
        if (row.get("subject_slug"), row.get("subcategory_slug"), row.get("chapter_slug")) != ("reasoning", None, "word-building"):
            raise ValueError(f"Row {i} has incorrect catalog metadata")
        if audit.get("chapter_id") != EXPECTED_CHAPTER_ID:
            raise ValueError(f"Ledger row {i} is not assigned to the discovered CH-15 chapter ID")
        if row.get("is_pyq") is not False or row.get("pyq_year") is not None or row.get("pyq_exam_name") is not None:
            raise ValueError(f"Row {i} is not valid Normal-question metadata")
        if row.get("difficulty") not in EXPECTED_COUNTS:
            raise ValueError(f"Row {i} has invalid difficulty")
        if not row.get("question_text", "").strip() or not row.get("explanation", "").strip():
            raise ValueError(f"Row {i} is missing its stem or explanation")
        options = row.get("options")
        if not isinstance(options, dict) or set(options) != set("ABCD"):
            raise ValueError(f"Row {i} must have exactly options A-D")
        if any(not isinstance(v, str) or not v.strip() for v in options.values()) or len({norm(v) for v in options.values()}) != 4:
            raise ValueError(f"Row {i} options must be four distinct nonempty strings")
        key = row.get("correct_option")
        if key not in options or sum(norm(v) == norm(options[key]) for v in options.values()) != 1:
            raise ValueError(f"Row {i} does not have exactly one keyed correct option")
        source = row.get("source")
        valid_pdf = isinstance(source, str) and source.startswith("Word Building 0") and source.endswith("; exam/year not stated")
        if source != ORIGINAL and not valid_pdf:
            raise ValueError(f"Row {i} has unsupported source metadata")
        if len(source) > 255:
            raise ValueError(f"Row {i} source exceeds the database field limit")
        stem = norm(row["question_text"])
        if stem in stems:
            raise ValueError(f"Repeated question stem at row {i}")
        stems.add(stem)
        if audit.get("question_id") != f"word-building-{i:03}" or audit.get("row") != i or audit.get("question") != row["question_text"]:
            raise ValueError(f"Row {i} does not align with its answer ledger entry")
        if audit.get("expected_answer") != options[key] or audit.get("correct_option") != key:
            raise ValueError(f"Row {i} answer conflicts with the answer ledger")
        if audit.get("difficulty") != row["difficulty"] or audit.get("source") != source:
            raise ValueError(f"Row {i} difficulty/source conflicts with the answer ledger")
        if not audit.get("independent_verification", "").strip() or not audit.get("validation_status", "").startswith("PASS"):
            raise ValueError(f"Row {i} lacks independent answer verification")
        signature = audit.get("concept_signature")
        if not signature or signature in signatures:
            raise ValueError(f"Row {i} has a missing or duplicated concept signature")
        signatures.add(signature)
        if source == ORIGINAL:
            if audit.get("source_type") != "original" or audit.get("source_pdf") is not None or audit.get("source_page") is not None:
                raise ValueError(f"Original row {i} has fabricated PDF provenance")
        elif audit.get("source_type") != "pdf-derived" or audit.get("source_pdf") not in source or not isinstance(audit.get("source_page"), int):
            raise ValueError(f"PDF-derived row {i} has incomplete provenance")
    return rows


def chapter_context(db):
    return db.execute(
        select(Exam, Subject, Chapter)
        .join(Subject, Subject.exam_id == Exam.id)
        .join(Chapter, Chapter.subject_id == Subject.id)
        .where(
            Exam.slug == "ssc", Exam.is_active.is_(True), Subject.slug == "reasoning",
            Subject.is_active.is_(True), Chapter.slug == "word-building", Chapter.is_active.is_(True),
            Chapter.subcategory_id.is_(None),
        )
    ).one_or_none()


def verify_existing(rows, existing):
    expected = {norm(row["question_text"]): row for row in rows}
    found = {}
    for question in existing:
        stem = norm(question.question_text)
        if stem in found or stem not in expected:
            raise ValueError("Unexpected or duplicate CH-15 record prevents safe import")
        found[stem] = question
        row = expected[stem]
        option_map = {o.option_key: o.option_text for o in question.options}
        correct_keys = [o.option_key for o in question.options if o.is_correct]
        if (question.question_text != row["question_text"] or question.explanation != row["explanation"]
                or question.difficulty.value != row["difficulty"] or question.is_pyq is not False
                or question.pyq_year is not None or question.pyq_exam_name is not None
                or question.source != row["source"] or not question.is_active
                or option_map != row["options"] or correct_keys != [row["correct_option"]]):
            raise ValueError("Existing CH-15 question conflicts with the canonical batch")
    return found


def check_canonical_duplicates(rows):
    paths = list((BASE / "data").glob("*.json")) + list(BASE.glob("*_verified_batch.json"))
    exact, near, scanned = [], [], 0
    candidates = [norm(row["question_text"]) for row in rows]
    for path in paths:
        if path.resolve() == BATCH.resolve():
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        prior_rows = payload.get("questions", []) if isinstance(payload, dict) else []
        for prior in prior_rows if isinstance(prior_rows, list) else []:
            if not isinstance(prior, dict) or prior.get("subject_slug") != "reasoning":
                continue
            text = prior.get("question_text")
            if not isinstance(text, str) or not text.strip():
                continue
            scanned += 1
            normalized = norm(text)
            for candidate in candidates:
                ratio = SequenceMatcher(None, normalized, candidate).ratio()
                if ratio == 1:
                    exact.append((path.name, text))
                elif ratio >= 0.94:
                    near.append((path.name, text, round(ratio, 3)))
    if exact or near:
        raise ValueError(f"Canonical Reasoning duplicate review required: exact={exact[:3]!r}; near={near[:3]!r}")
    return scanned


def check_reasoning_duplicates(db, chapter_id, rows):
    existing = db.scalars(
        select(Question.question_text)
        .join(Chapter, Chapter.id == Question.chapter_id)
        .join(Subject, Subject.id == Chapter.subject_id)
        .where(Subject.slug == "reasoning", Question.chapter_id != chapter_id)
    ).all()
    exact, near = [], []
    for text in existing:
        prior = norm(text)
        for row in rows:
            ratio = SequenceMatcher(None, prior, norm(row["question_text"])).ratio()
            if ratio == 1:
                exact.append(text)
            elif ratio >= 0.94:
                near.append((text, row["question_text"], round(ratio, 3)))
    if exact or near:
        raise ValueError(f"Cross-chapter Reasoning duplicate review required: exact={exact[:3]!r}; near={near[:3]!r}")
    return len(existing)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="write only after the chapter, baseline and dry-run guards pass")
    args = parser.parse_args(argv)
    engine.echo = False
    rows = load_artifacts()
    print("BATCH", len(rows), dict(Counter(row["difficulty"] for row in rows)))
    canonical_count = check_canonical_duplicates(rows)
    print("CANONICAL_REASONING_QUESTIONS_SCANNED", canonical_count)
    with SessionLocal() as db:
        context = chapter_context(db)
        if context is None:
            raise SystemExit("Active SSC → Reasoning → Word Building chapter was not found uniquely")
        _, _, chapter = context
        if str(chapter.id) != EXPECTED_CHAPTER_ID:
            raise SystemExit(f"CH-15 ID mismatch: expected discovered ID {EXPECTED_CHAPTER_ID}, got {chapter.id}")
        existing = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        normal = sum(q.is_active and not q.is_pyq for q in existing)
        pyq = sum(q.is_active and q.is_pyq for q in existing)
        print("CHAPTER", chapter.id, chapter.name)
        print("BEFORE", {"active_normal": normal, "active_pyq": pyq, "all_records": len(existing)})
        verify_existing(rows, existing)
        reasoning_count = check_reasoning_duplicates(db, chapter.id, rows)
        print("CROSS_CHAPTER_REASONING_RECORDS_SCANNED", reasoning_count)
        if (normal, pyq, len(existing)) not in {(0, 0, 0), (30, 0, 30)}:
            raise SystemExit("Baseline must be empty CH-15 or the exact completed 30-question Normal batch")
        payload = json.dumps({"questions": rows}, ensure_ascii=False).encode("utf-8")
        preview = import_questions(db, payload, "application/json", BATCH.name, True)
        print("DRY_RUN", preview.model_dump())
        if preview.aborted or preview.errors or preview.rejected or preview.duplicates != len(existing) or preview.would_import != 30 - len(existing):
            raise SystemExit("Importer dry-run did not match the verified baseline")
        if not args.apply:
            print("NO_DATABASE_CHANGES")
            return
        if normal == 30:
            print("IDEMPOTENT_REPLAY: zero additional inserts")
            return
        if normal or pyq or existing or preview.duplicates or preview.would_import != 30:
            raise SystemExit("Apply requires the exact verified empty CH-15 baseline and 30 clean rows")
        result = import_questions(db, payload, "application/json", BATCH.name, False)
        print("IMPORT", result.model_dump())
        if result.aborted or result.errors or result.rejected or result.imported != 30 or result.duplicates:
            raise SystemExit("Actual importer results differed from 30 clean inserts")
        after = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        active_normal = [q for q in after if q.is_active and not q.is_pyq]
        active_pyq = [q for q in after if q.is_active and q.is_pyq]
        counts = Counter(q.difficulty.value for q in active_normal)
        if len(active_normal) != 30 or active_pyq or len(after) != 30 or counts != EXPECTED_COUNTS:
            raise SystemExit(f"Post-import counts differ from bank: {dict(counts)}")
        verify_existing(rows, after)
        replay = import_questions(db, payload, "application/json", BATCH.name, True)
        print("REPLAY_DRY_RUN", replay.model_dump())
        if replay.aborted or replay.errors or replay.rejected or replay.would_import or replay.duplicates != 30:
            raise SystemExit("Post-import replay was not idempotent")
        print("AFTER", {"active_normal": 30, "active_pyq": 0, "all_records": 30, "difficulty": dict(counts)})
        print("POST_IMPORT_VERIFIED")


if __name__ == "__main__":
    main()
