"""Focused CH-08 artifact, cube-orientation, and availability regressions."""
import json
import unicodedata
from collections import Counter
from pathlib import Path
from types import SimpleNamespace

from app.services.test_service import _selection_counts
from scripts.import_dice_verified_batch import load_artifacts

BASE = Path(__file__).resolve().parents[1]
BATCH = BASE / "data" / "dice_verified_batch.json"
LEDGER = BASE / "data" / "dice_answer_ledger.json"
ORIGINAL = "Original SSC-style practice question"


def norm(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def test_batch_ledger_provenance_and_normal_metadata_align():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    assert len(rows) == len(ledger) == 30
    assert Counter(row["difficulty"] for row in rows) == {"EASY": 10, "MEDIUM": 10, "HARD": 10}
    assert Counter(audit["source_type"] for audit in ledger) == {"pdf-derived": 4, "original": 26}
    assert len({norm(row["question_text"]) for row in rows}) == 30
    for i, (row, audit) in enumerate(zip(rows, ledger), 1):
        assert (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) == ("reasoning", None, "dice")
        assert row["is_pyq"] is False and row["pyq_year"] is None and row["pyq_exam_name"] is None
        assert set(row["options"]) == set("ABCD")
        assert len({norm(value) for value in row["options"].values()}) == 4
        assert row["correct_option"] in row["options"]
        assert audit["question_id"] == f"dice-{i:03}" and audit["row"] == i
        assert audit["expected_answer"] == row["options"][row["correct_option"]]
        assert audit["source"] == row["source"] and audit["concept_signature"]
        assert audit["independent_reasoning"] and audit["option_review"]
        if row["source"] == ORIGINAL:
            assert audit["source_type"] == "original" and audit["source_pdf"] is None and audit["source_page"] is None
        else:
            assert audit["source_type"] == "pdf-derived"
            assert audit["source_pdf"] == "Dice 01_ Class Notes.pdf"
            assert audit["source_page"] in {17, 18, 19, 21}
    assert len(ledger[0]["rejected_source_questions"]) == 4


def test_importer_schema_validator_and_reasoning_selection_counts():
    assert len(load_artifacts()) == 30
    reasoning = SimpleNamespace(slug="reasoning")
    assert _selection_counts(30, reasoning) == [10, 15, 20, 25]
    assert _selection_counts(10, reasoning) == [10]


def test_multi_view_source_items_are_complete_and_rotation_checked_by_builder():
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    source = [row for row in ledger if row["source_type"] == "pdf-derived"]
    assert {row["source_page"] for row in source} == {17, 18, 19, 21}
    assert all(len(row["face_configurations"]) >= 2 for row in source)
    assert all(row["verification_status"].startswith("PASS") for row in source)
    answers = {row["source_page"]: row["verified_opposite_faces"][row["target_face"]] for row in source}
    assert answers == {17: "I", 18: "Orange", 19: "R", 21: "*"}
    for row in ledger:
        if row["face_configurations"]:
            assert row["target_face"] in row["verified_opposite_faces"]
            assert row["verified_opposite_faces"][row["target_face"]]
