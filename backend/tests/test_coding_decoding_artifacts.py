import json
import runpy
from types import SimpleNamespace
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "import_coding_decoding_batch.py"
DATA = Path(__file__).resolve().parents[1] / "data"


@pytest.fixture(scope="module")
def import_tools():
    return runpy.run_path(str(SCRIPT))


def test_normal_batch_and_ledger_have_valid_distinct_records(import_tools):
    rows = import_tools["load_and_validate"]("normal")
    ledger = json.loads((DATA / "coding_decoding_normal_answer_ledger.json").read_text(encoding="utf-8"))
    assert len(rows) == len(ledger) == 24
    assert len({row["question_text"].casefold() for row in rows}) == 24
    assert all(row["is_pyq"] is False for row in rows)


def test_pyq_batch_and_ledger_have_valid_distinct_records(import_tools):
    rows = import_tools["load_and_validate"]("pyq")
    assert len(rows) == 4
    assert len({row["question_text"].casefold() for row in rows}) == 4
    assert all(row["is_pyq"] is True and row["pyq_year"] in {2022, 2023} for row in rows)


def test_explosion_explanation_matches_position_permutation(import_tools):
    rows = import_tools["load_and_validate"]("pyq")
    row = next(q for q in rows if "EXPLOSION" in q["question_text"])
    assert row["options"][row["correct_option"]] == "SIONOEXPL"
    assert "positions 6–9, then position 5, then positions 1–4" in row["explanation"]
    assert "final four letters are reversed" not in row["explanation"]


def test_identical_existing_pyq_is_idempotent_but_content_mismatch_is_reported(import_tools):
    rows = import_tools["load_and_validate"]("pyq")
    row = rows[0]
    stored = SimpleNamespace(
        options=[SimpleNamespace(option_key=key, option_text=value, is_correct=key == row["correct_option"])
                 for key, value in row["options"].items()],
        explanation=row["explanation"], difficulty=row["difficulty"], is_pyq=True,
        pyq_year=row["pyq_year"], pyq_exam_name=row["pyq_exam_name"], source=row["source"], is_active=True,
    )
    assert import_tools["existing_mismatches"](stored, row) == {}
    stored.explanation = "different explanation"
    assert set(import_tools["existing_mismatches"](stored, row)) == {"explanation"}


def test_additional_normal_batch_is_30_valid_novel_records(import_tools):
    rows = import_tools["load_and_validate"]("normal-additional")
    assert len(rows) == 30
    assert {level: sum(row["difficulty"] == level for row in rows)
            for level in ("EASY", "MEDIUM", "HARD")} == {"EASY": 10, "MEDIUM": 12, "HARD": 8}
    assert all(row["is_pyq"] is False for row in rows)
    normalize = import_tools["norm"]
    new_stems = {normalize(row["question_text"]) for row in rows}
    old_rows = import_tools["load_and_validate"]("normal") + import_tools["load_and_validate"]("pyq")
    old_stems = {normalize(row["question_text"]) for row in old_rows}
    assert len(new_stems) == 30
    assert new_stems.isdisjoint(old_stems)
    assert [row["options"][row["correct_option"]] for row in rows] == [
        "FQI", "YVW", "NEDRAG", "OBN", "PLENI", "2143", "26074", "IMTN", "33", "Z",
        "PCEOKT", "DOCSG", "14", "FNQE", "ANTPL", "396", "FJRSG", "ABERZ", "24", "DFH",
        "$D#@", "NCUI", "GMZOK", "DMGA", "11", "EV", "RMAETK", "TFDK", "381", "141216",
    ]
    for row in rows:
        assert set(row["options"]) == set("ABCD")
        assert len({normalize(value) for value in row["options"].values()}) == 4
        assert row["correct_option"] in row["options"]
        assert row["options"][row["correct_option"]].strip()
        assert row["explanation"].strip()
