"""Validate and import one verified Coding-Decoding source batch."""
import argparse
import json
import sys
import unicodedata
import uuid
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))

from sqlalchemy import select
from app.database.session import SessionLocal, engine
from app.models import Chapter, Question, Subject
from app.services.question_import_service import import_questions

CHAPTER_ID = "ea6abf58-9dc2-4622-b846-3601ac723898"
LEVELS = {"EASY", "MEDIUM", "HARD"}


def norm(text):
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def existing_mismatches(question, row):
    """Return stored fields that disagree with a canonical batch record."""
    stored_options = {option.option_key: option.option_text for option in question.options}
    stored_answer = [option.option_key for option in question.options if option.is_correct]
    stored_difficulty = getattr(question.difficulty, "value", question.difficulty)
    expected = {
        "options": (stored_options, row["options"]),
        "correct_option": (stored_answer, [row["correct_option"]]),
        "explanation": (question.explanation, row["explanation"]),
        "difficulty": (stored_difficulty, row["difficulty"]),
        "is_pyq": (question.is_pyq, row["is_pyq"]),
        "pyq_year": (question.pyq_year, row.get("pyq_year")),
        "pyq_exam_name": (question.pyq_exam_name, row.get("pyq_exam_name")),
        "source": (question.source, row["source"]),
        "is_active": (question.is_active, True),
    }
    return {field: values for field, values in expected.items() if values[0] != values[1]}


def load_and_validate(kind):
    if kind not in {"normal", "normal-additional", "pyq"}:
        raise ValueError("kind must be normal, normal-additional, or pyq")
    prefix = {
        "normal": "coding_decoding_normal",
        "normal-additional": "coding_decoding_normal_additional",
        "pyq": "coding_decoding_pyq",
    }[kind]
    batch_path = BASE / "data" / f"{prefix}_verified_batch.json"
    ledger_path = BASE / "data" / f"{prefix}_answer_ledger.json"
    rows = json.loads(batch_path.read_text(encoding="utf-8"))["questions"]
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    if not rows or len(rows) != len(ledger):
        raise ValueError("Batch and ledger must have the same non-zero record count")
    required = {"subject_slug", "subcategory_slug", "chapter_slug", "question_text", "options", "correct_option", "explanation", "difficulty", "is_pyq", "source"}
    seen = set()
    for i, (row, audit) in enumerate(zip(rows, ledger), 1):
        if required - row.keys():
            raise ValueError(f"Row {i}: missing required fields {required-row.keys()}")
        if (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) != ("reasoning", None, "coding-decoding"):
            raise ValueError(f"Row {i}: wrong catalog association")
        valid_pyq = (row["is_pyq"] is True and isinstance(row.get("pyq_year"), int)
                     and 1950 <= row["pyq_year"] <= 2026 and bool(row.get("pyq_exam_name")))
        valid_normal = (row["is_pyq"] is False and row.get("pyq_year") is None
                        and row.get("pyq_exam_name") is None)
        if row["difficulty"] not in LEVELS or not (valid_pyq if kind == "pyq" else valid_normal):
            raise ValueError(f"Row {i}: invalid difficulty/PYQ metadata")
        if not isinstance(row["options"], dict) or set(row["options"]) != set("ABCD") or len({norm(x) for x in row["options"].values()}) != 4:
            raise ValueError(f"Row {i}: options must be distinct A-D choices")
        key = row["correct_option"]
        if key not in row["options"] or not row["question_text"].strip() or not row["explanation"].strip():
            raise ValueError(f"Row {i}: stem, key or explanation missing")
        if norm(row["question_text"]) in seen:
            raise ValueError(f"Row {i}: duplicate stem")
        seen.add(norm(row["question_text"]))
        if audit != {"row": i, "question": row["question_text"], "difficulty": row["difficulty"], "expected_answer": row["options"][key], "independent_reasoning": row["explanation"], "source": row["source"]}:
            raise ValueError(f"Row {i}: ledger mismatch")
        if kind == "normal" and (not row["source"].startswith("Coding Decoding 0") or "PDF page " not in row["source"]):
            raise ValueError(f"Row {i}: PDF provenance is missing")
        if kind == "normal-additional" and row["source"] != "Original question authored for SSC Prep Platform; not a PYQ.":
            raise ValueError(f"Row {i}: original-question provenance is missing")
        if kind == "pyq" and ("http" not in row["source"] or "secondary" not in row["source"].casefold()):
            raise ValueError(f"Row {i}: source URL and evidence type are required")
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", choices=["normal", "normal-additional", "pyq"], default="normal")
    parser.add_argument("--apply", action="store_true", help="Commit approved inserts; default is dry-run")
    args = parser.parse_args()
    rows = load_and_validate(args.source)
    engine.echo = False
    with SessionLocal() as db:
        chapter = db.get(Chapter, uuid.UUID(CHAPTER_ID))
        if chapter is None or not chapter.is_active or chapter.slug != "coding-decoding":
            raise SystemExit("Target chapter ID verification failed")
        subject = db.get(Subject, chapter.subject_id)
        if subject is None or subject.slug != "reasoning" or chapter.subcategory_id is not None:
            raise SystemExit("Target subject/subcategory verification failed")
        existing = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        candidates = {norm(row["question_text"]): row for row in rows}
        inserts = []
        for q in existing:
            match = candidates.get(norm(q.question_text))
            if match:
                mismatches = existing_mismatches(q, match)
                if mismatches:
                    fields = ", ".join(
                        f"{name} (database={values[0]!r}, batch={values[1]!r})"
                        for name, values in mismatches.items()
                    )
                    raise SystemExit(f"Existing question conflicts with batch: {q.question_text}; {fields}")
            if norm(q.question_text) in candidates:
                candidates.pop(norm(q.question_text))
        inserts = [row for row in rows if norm(row["question_text"]) in candidates]
        print("CHAPTER", chapter.id, chapter.name)
        print("BEFORE", {"total":len(existing),"active":sum(q.is_active for q in existing),"ordinary":sum(q.is_active and not q.is_pyq for q in existing),"PYQ":sum(q.is_active and q.is_pyq for q in existing)})
        print("BATCH", len(rows), "INSERTS", len(inserts), "DIFFICULTY", dict(Counter(row["difficulty"] for row in inserts)))
        data = json.dumps({"questions": inserts}, ensure_ascii=False).encode("utf-8")
        if inserts:
            filename = {
                "normal": "coding_decoding_normal_verified_batch.json",
                "normal-additional": "coding_decoding_normal_additional_verified_batch.json",
                "pyq": "coding_decoding_pyq_verified_batch.json",
            }[args.source]
            preview = import_questions(db, data, "application/json", filename, True)
            print("DRY_RUN", preview.model_dump())
            if preview.aborted or preview.errors or preview.would_import != len(inserts) or preview.duplicates:
                raise SystemExit("Importer dry-run failed; no records imported")
        else:
            print("DRY_RUN_ZERO_NEW_INSERTS")
        if not args.apply or not inserts:
            print("NO_DATABASE_CHANGES")
            return
        result = import_questions(db, data, "application/json", filename, False)
        print("IMPORT", result.model_dump())
        if result.aborted or result.errors or result.imported != len(inserts):
            raise SystemExit("Import result does not match approved dry-run")
        after = db.scalars(select(Question).where(Question.chapter_id == chapter.id)).all()
        print("AFTER", {"total":len(after),"active":sum(q.is_active for q in after),"ordinary":sum(q.is_active and not q.is_pyq for q in after),"PYQ":sum(q.is_active and q.is_pyq for q in after)})

if __name__ == "__main__":
    main()
