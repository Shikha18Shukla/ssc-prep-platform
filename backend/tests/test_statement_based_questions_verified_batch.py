import importlib.util
import json
from collections import Counter
from pathlib import Path

from scripts import import_statement_based_questions_verified_batch as importer

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def test_verified_bank_counts_and_answers():
    rows = importer.load_artifacts()
    ledger = json.loads((DATA / "statement_based_questions_answer_ledger.json").read_text(encoding="utf-8"))
    assert len(rows) == 32
    assert Counter(row["difficulty"] for row in rows) == Counter({"EASY": 11, "MEDIUM": 11, "HARD": 10})
    assert Counter(item["category"] for item in ledger) == Counter({"ASSUMPTION": 8, "CONCLUSION": 8, "ARGUMENT": 8, "ACTION": 8})
    assert Counter(row["correct_option"] for row in rows) == Counter({"A": 8, "B": 8, "C": 8, "D": 8})
    assert all(row["options"][row["correct_option"]] for row in rows)
    assert all(row["explanation"].strip() for row in rows)
    assert all(row["is_pyq"] is False for row in rows)
    assert all(row["options"][row["correct_option"]] == audit["logical_outcome"] for row, audit in zip(rows, ledger))


def test_source_review_covers_every_scanned_page():
    report = json.loads((DATA / "statement_based_questions_source_review.json").read_text(encoding="utf-8"))
    assert report["total_pages_reviewed"] == 41
    assert len(report["page_reviews"]) == 41
    assert Counter(page["status"] for page in report["page_reviews"]) == Counter({"accepted": 21, "rejected": 7, "reference": 13})


def test_builder_is_deterministic(tmp_path):
    builder_path = ROOT / "scripts" / "build_statement_based_questions_artifacts.py"
    spec = importlib.util.spec_from_file_location("statement_artifact_builder", builder_path)
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    builder.DATA = tmp_path
    builder.build()
    first = {path.name: path.read_bytes() for path in tmp_path.iterdir()}
    builder.build()
    second = {path.name: path.read_bytes() for path in tmp_path.iterdir()}
    assert first == second


def test_importer_rejects_artifact_conflicts(monkeypatch):
    rows = json.loads(importer.BATCH.read_text(encoding="utf-8"))
    rows["questions"][0]["correct_option"] = "Z"
    batch_path = ROOT / "tests" / "_temp_statement_batch.json"
    ledger_path = ROOT / "tests" / "_temp_statement_ledger.json"
    try:
        batch_path.write_text(json.dumps(rows), encoding="utf-8")
        ledger_path.write_text(importer.LEDGER.read_text(encoding="utf-8"), encoding="utf-8")
        monkeypatch.setattr(importer, "BATCH", batch_path)
        monkeypatch.setattr(importer, "LEDGER", ledger_path)
        try:
            importer.load_artifacts()
        except ValueError as exc:
            assert "answer or identity mismatch" in str(exc)
        else:
            raise AssertionError("importer accepted conflicting answer metadata")
    finally:
        batch_path.unlink(missing_ok=True)
        ledger_path.unlink(missing_ok=True)
