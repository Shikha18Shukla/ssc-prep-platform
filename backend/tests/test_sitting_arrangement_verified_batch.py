"""Focused CH-09 Sitting Arrangement artifact and availability regressions."""
import json
import unicodedata
from collections import Counter
from pathlib import Path
from types import SimpleNamespace

from app.services.test_service import _selection_counts
from scripts.import_sitting_arrangement_verified_batch import load_artifacts

BASE = Path(__file__).resolve().parents[1]
BATCH = BASE / "data" / "sitting_arrangement_verified_batch.json"
LEDGER = BASE / "data" / "sitting_arrangement_answer_ledger.json"
ORIGINAL = "Original SSC-style practice question"


def norm(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def test_batch_ledger_provenance_and_normal_metadata_align():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    assert len(rows) == len(ledger) == 30
    assert Counter(row["difficulty"] for row in rows) == {"EASY": 10, "MEDIUM": 10, "HARD": 10}
    assert Counter(audit["source_type"] for audit in ledger) == {"pdf-derived": 14, "original": 16}
    assert len({norm(row["question_text"]) for row in rows}) == 30
    for i, (row, audit) in enumerate(zip(rows, ledger), 1):
        assert (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) == ("reasoning", None, "sitting-arrangement")
        assert row["is_pyq"] is False and row["pyq_year"] is None and row["pyq_exam_name"] is None
        assert set(row["options"]) == set("ABCD")
        assert len({norm(value) for value in row["options"].values()}) == 4
        assert row["correct_option"] in row["options"]
        assert audit["question_id"] == f"sitting-arrangement-{i:03}" and audit["row"] == i
        assert audit["expected_answer"] == row["options"][row["correct_option"]]
        assert audit["options"] == row["options"]
        assert audit["is_pyq"] is False
        assert audit["verified_arrangement"]
        assert audit["source"] == row["source"] and audit["concept_signature"]
        assert audit["independent_reasoning"] and audit["option_review"]
        if row["source"] == ORIGINAL:
            assert audit["source_type"] == "original" and audit["source_pdf"] is None and audit["source_page"] is None
        else:
            assert audit["source_type"] == "pdf-derived"
            assert audit["source_pdf"] in {"Sitting arrangement 01 Class Notes.pdf", "Sitting arrangement 02_ Class Notes.pdf", "Sitting arrangement 03 Class Notes.pdf"}
            assert isinstance(audit["source_page"], int)
    assert len(ledger[0]["rejected_source_questions"]) == 3


def test_importer_schema_validator_and_reasoning_selection_counts():
    assert len(load_artifacts()) == 30
    reasoning = SimpleNamespace(slug="reasoning")
    assert _selection_counts(30, reasoning) == [10, 15, 20, 25]
    assert _selection_counts(10, reasoning) == [10]


def test_seating_arrangements_were_unique_and_rejected_prompts_are_logged():
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    source = [row for row in ledger if row["source_type"] == "pdf-derived"]
    assert len(source) == 14
    assert all(row["verification_status"].startswith("PASS") for row in ledger)
    assert len({row["concept_signature"] for row in ledger}) == 30
    review = json.loads((BASE / "data" / "sitting_arrangement_source_review.json").read_text(encoding="utf-8"))
    assert review["reviewed_pages"] == 41 and review["selected"] == 14 and review["rejected"] == 3
    assert len(review["rejections"]) == 3
    report = (BASE / "data" / "sitting_arrangement_review_report.md").read_text(encoding="utf-8")
    assert "Replay: 30 duplicates recognized" in report
    assert "Authenticated API" in report
