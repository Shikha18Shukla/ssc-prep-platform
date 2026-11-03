"""Validate, dry-run, and safely import the reviewed Sitting Arrangement Normal bank."""

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

BATCH = BASE / "data" / "sitting_arrangement_verified_batch.json"
LEDGER = BASE / "data" / "sitting_arrangement_answer_ledger.json"
EXPECTED_CHAPTER_ID = "32faa174-9f26-4524-9639-f325ef6674b8"
LEVELS = {"EASY": 10, "MEDIUM": 10, "HARD": 10}
ORIGINAL = "Original SSC-style practice question"


def norm(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def load_artifacts():
    rows = json.loads(BATCH.read_text(encoding="utf-8")).get("questions")
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    if not isinstance(rows, list) or len(rows) != 30 or not isinstance(ledger, list) or len(ledger) != len(rows):
        raise ValueError("Sitting Arrangement batch and ledger must align and contain exactly 30 records")
    if Counter(row.get("difficulty") for row in rows) != Counter(LEVELS):
        raise ValueError("Difficulty distribution must be 10 EASY, 10 MEDIUM, 10 HARD")
    stems, signatures = set(), set()
    for i, (row, audit) in enumerate(zip(rows, ledger), 1):
        if (row.get("subject_slug"), row.get("subcategory_slug"), row.get("chapter_slug")) != ("reasoning", None, "sitting-arrangement"):
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
        valid_pdf = isinstance(source, str) and source.startswith("Sitting arrangement 0") and source.endswith("; exam/year not stated")
        if source != ORIGINAL and not valid_pdf:
            raise ValueError(f"Row {i} has unsupported provenance")
        if len(source) > 255:
            raise ValueError(f"Row {i} provenance exceeds the database field length")
        stem = norm(row["question_text"])
        if stem in stems:
            raise ValueError(f"Repeated stem in row {i}")
        stems.add(stem)
        if audit.get("question_id") != f"sitting-arrangement-{i:03}" or audit.get("row") != i or audit.get("question") != row["question_text"]:
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
            Subject.is_active.is_(True), Chapter.slug == "sitting-arrangement", Chapter.is_active.is_(True),
            Chapter.subcategory_id.is_(None),
        )
    ).one_or_none()


def verify_existing(rows, existing):
    expected = {norm(row["question_text"]): row for row in rows}
    actual = {}
    for question in existing:
        stem = norm(question.question_text)
        if stem in actual or stem not in expected:
            raise ValueError("Unexpected or duplicate existing Sitting Arrangement question prevents safe import")
        actual[stem] = question
        row = expected[stem]
        options = {o.option_key: o.option_text for o in question.options}
        keys = [o.option_key for o in question.options if o.is_correct]
        if (question.question_text != row["question_text"] or question.explanation != row["explanation"]
                or question.difficulty.value != row["difficulty"] or question.is_pyq is not False
                or question.pyq_year is not None or question.pyq_exam_name is not None
                or question.source != row["source"] or not question.is_active
                or options != row["options"] or keys != [row["correct_option"]]):
            raise ValueError("Existing Sitting Arrangement question conflicts with canonical batch")
    return actual


def duplicate_scan(db, rows, chapter_id):
    proposed = [(norm(r["question_text"]), r["question_text"]) for r in rows]
    candidates = []
    for q in db.scalars(select(Question).where(Question.is_active.is_(True), Question.chapter_id != chapter_id)):
        candidates.append((norm(q.question_text), q.question_text, f"database:{q.chapter_id}"))
    for path in (BASE / "data").glob("*_verified_batch.json"):
        if path == BATCH:
            continue
        try:
            other = json.loads(path.read_text(encoding="utf-8")).get("questions", [])
        except (OSError, ValueError):
            continue
        for row in other:
            if isinstance(row, dict) and isinstance(row.get("question_text"), str):
                candidates.append((norm(row["question_text"]), row["question_text"], f"canonical:{path.name}"))
    matches = []
    for stem, raw in proposed:
        for other, other_raw, origin in candidates:
            # SequenceMatcher cannot reach the threshold when the maximum possible
            # overlap allowed by the two lengths is already below it.
            if 2 * min(len(stem), len(other)) / (len(stem) + len(other)) < 0.97:
                continue
            ratio = SequenceMatcher(None, stem, other, autojunk=False).ratio()
            if ratio >= 0.97:
                matches.append({"proposed": raw, "match": other_raw, "origin": origin, "similarity": round(ratio, 3)})
    return len(candidates), matches


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="apply only after all dry-run guards pass")
    args = parser.parse_args(argv)
    engine.echo = False
    rows = load_artifacts()
    print("BATCH", len(rows), dict(Counter(row["difficulty"] for row in rows)))
    with SessionLocal() as db:
        context = chapter_context(db)
        if context is None:
            raise SystemExit("Active SSC → Reasoning → Sitting Arrangement chapter was not found uniquely")
        _, _, chapter = context
        if str(chapter.id) != EXPECTED_CHAPTER_ID:
            raise SystemExit(f"Chapter ID mismatch: expected reference {EXPECTED_CHAPTER_ID}, found {chapter.id}")
        existing = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        normal = sum(q.is_active and not q.is_pyq for q in existing)
        pyq = sum(q.is_active and q.is_pyq for q in existing)
        print("CHAPTER", chapter.id, chapter.name)
        print("BEFORE", {"active_normal": normal, "active_pyq": pyq, "all_records": len(existing)})
        verify_existing(rows, existing)
        if (normal, pyq, len(existing)) not in {(0, 0, 0), (30, 0, 30)}:
            raise SystemExit("Baseline must be the verified empty Sitting Arrangement chapter or exact completed 30-question bank")
        scanned, matches = duplicate_scan(db, rows, chapter.id)
        print("DUPLICATE_SCAN", {"candidates": scanned, "threshold": 0.97, "match_count": len(matches), "matches": matches[:10]})
        if matches:
            raise SystemExit("Review the Sitting Arrangement duplicate matches before importing")
        payload = json.dumps({"questions": rows}, ensure_ascii=False).encode("utf-8")
        preview = import_questions(db, payload, "application/json", BATCH.name, True)
        print("DRY_RUN", preview.model_dump())
        if preview.aborted or preview.errors or preview.rejected or preview.duplicates != len(existing) or preview.would_import != 30 - len(existing):
            raise SystemExit("Importer dry-run did not match expected insert/duplicate counts")
        if not args.apply:
            print("NO_DATABASE_CHANGES")
            return
        if normal == 30:
            print("IDEMPOTENT_REPLAY: zero additional inserts")
            return
        if normal or pyq or len(existing) or preview.duplicates or preview.would_import != 30:
            raise SystemExit("Apply requires the exact verified empty Sitting Arrangement baseline and 30 clean inserts")
        result = import_questions(db, payload, "application/json", BATCH.name, False)
        print("IMPORT", result.model_dump())
        if result.aborted or result.errors or result.rejected or result.imported != 30 or result.duplicates:
            raise SystemExit("Actual importer results differed from the expected 30 inserts")
        after = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        active_normal = [q for q in after if q.is_active and not q.is_pyq]
        active_pyq = [q for q in after if q.is_active and q.is_pyq]
        if len(active_normal) != 30 or active_pyq or len(after) != 30:
            raise SystemExit("Post-import active Normal/PYQ/total counts do not match the batch")
        verify_existing(rows, after)
        counts = Counter(q.difficulty.value for q in active_normal)
        if counts != Counter(LEVELS):
            raise SystemExit(f"Post-import difficulty counts do not match: {dict(counts)}")
        replay = import_questions(db, payload, "application/json", BATCH.name, True)
        print("REPLAY_DRY_RUN", replay.model_dump())
        if replay.aborted or replay.errors or replay.rejected or replay.would_import or replay.duplicates != 30:
            raise SystemExit("Post-import replay was not idempotent")
        print("AFTER", {"active_normal": len(active_normal), "active_pyq": 0, "all_records": len(after), "difficulty": dict(counts)})
        print("POST_IMPORT_VERIFIED")


if __name__ == "__main__":
    main()


