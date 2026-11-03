"""Focused CH-10 Puzzle artifact and availability regressions."""
import json
import unicodedata
from collections import Counter
from pathlib import Path
from types import SimpleNamespace

from app.services.test_service import _selection_counts
from scripts.import_puzzle_verified_batch import load_artifacts

BASE = Path(__file__).resolve().parents[1]
BATCH = BASE / "data" / "puzzle_verified_batch.json"
LEDGER = BASE / "data" / "puzzle_answer_ledger.json"
ORIGINAL = "Original SSC-style practice question"


def norm(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def test_batch_ledger_and_normal_metadata_align():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    assert len(rows) == len(ledger) == 30
    assert Counter(row["difficulty"] for row in rows) == {"EASY": 10, "MEDIUM": 10, "HARD": 10}
    assert Counter(audit["source_type"] for audit in ledger) == {"pdf-derived": 19, "original": 11}
    assert Counter(audit["puzzle_category"] for audit in ledger) == {"Classification/ranking": 8, "Day-based": 7, "Floor-based": 6, "Box-based": 5, "Miscellaneous": 4}
    assert len({norm(row["question_text"]) for row in rows}) == 30
    for i, (row, audit) in enumerate(zip(rows, ledger), 1):
        assert (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) == ("reasoning", None, "puzzle")
        assert row["is_pyq"] is False and row["pyq_year"] is None and row["pyq_exam_name"] is None
        assert set(row["options"]) == set("ABCD")
        assert len({norm(value) for value in row["options"].values()}) == 4
        assert row["correct_option"] in row["options"]
        assert audit["question_id"] == f"puzzle-{i:03}" and audit["row"] == i
        assert audit["expected_answer"] == row["options"][row["correct_option"]]
        assert audit["options"] == row["options"]
        assert audit["is_pyq"] is False and audit["puzzle_category"]
        assert audit["verified_order"] and audit["solution_count"] >= 1
        assert audit["source"] == row["source"] and audit["concept_signature"]
        assert audit["verification_status"].startswith("PASS")
        if row["source"] == ORIGINAL:
            assert audit["source_type"] == "original" and audit["source_pdf"] is None and audit["source_page"] is None
        else:
            assert audit["source_type"] == "pdf-derived"
            assert audit["source_pdf"] in {"Puzzle 01_ Class Notes.pdf", "Puzzle 02_ Class Notes.pdf", "Puzzle 03_ Class Notes.pdf"}
            assert isinstance(audit["source_page"], int)
    assert len(ledger[0]["rejected_source_questions"]) == 4


def test_importer_schema_validator_and_reasoning_selection_counts():
    assert len(load_artifacts()) == 30
    reasoning = SimpleNamespace(slug="reasoning")
    assert _selection_counts(30, reasoning) == [10, 15, 20, 25]
    assert _selection_counts(10, reasoning) == [10]


def test_source_review_and_constraint_audit_are_complete():
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    source = [row for row in ledger if row["source_type"] == "pdf-derived"]
    assert len(source) == 19
    assert all(row["verification_status"].startswith("PASS") for row in ledger)
    assert len({row["concept_signature"] for row in ledger}) == 30
    report = (BASE / "data" / "puzzle_review_report.md").read_text(encoding="utf-8")
    assert "14 in Puzzle 01_ Class Notes.pdf" in report
    assert "14 in Puzzle 02_ Class Notes.pdf" in report
    assert "12 in Puzzle 03_ Class Notes.pdf" in report
    assert "selected 19 and rejected 4" in report
