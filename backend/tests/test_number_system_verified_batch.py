"""Batch shape, independently worked solutions, provenance, and MCQ checks."""
import json
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
BATCH = BASE / "data" / "number_system_verified_batch.json"
LEDGER = BASE / "data" / "number_system_answer_ledger.json"


def norm(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def test_rows_align_with_ledger_and_have_one_keyed_answer_and_four_options():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    assert len(rows) == len(ledger) == 90
    assert Counter(row["difficulty"] for row in rows) == {"EASY": 30, "MEDIUM": 30, "HARD": 30}
    assert sum(row["source"] == "Original SSC-style practice question" for row in rows) == 71
    assert sum(row["source"].startswith("Number System ") for row in rows) == 19
    for i, (row, audit) in enumerate(zip(rows, ledger), start=1):
        assert (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) == ("maths", "advanced-maths", "number-system")
        assert row["is_pyq"] is False and row.get("pyq_year") is None and row.get("pyq_exam_name") is None
        assert row["question_text"].strip() and row["explanation"].strip()
        assert set(row["options"]) == set("ABCD")
        assert all(isinstance(value, str) and value.strip() for value in row["options"].values())
        assert len({norm(value) for value in row["options"].values()}) == 4
        assert row["correct_option"] in row["options"]
        assert sum(norm(value) == norm(row["options"][row["correct_option"]]) for value in row["options"].values()) == 1
        assert row["options"][row["correct_option"]] == audit["expected_answer"]
        assert row["question_text"] == audit["question"] and row["difficulty"] == audit["difficulty"]
        assert audit["row"] == i and audit["independent_reasoning"].strip()
        if row["source"] != "Original SSC-style practice question":
            assert ", PDF page " in row["source"] and "exam/year not stated" in row["source"]


def test_stems_are_unique_and_not_near_verbatim_duplicates():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    stems = [norm(row["question_text"]) for row in rows]
    assert len(set(stems)) == 90
    for i, stem in enumerate(stems):
        assert all(SequenceMatcher(None, stem, previous).ratio() < .97 for previous in stems[:i])


def test_selected_trigonometric_calculations_are_independently_recomputed():
    rows = {row["question_text"]: row for row in json.loads(BATCH.read_text(encoding="utf-8"))["questions"]}
    expected = {
        "Evaluate 1/(4·5) + 1/(5·6) + … + 1/(11·12).": "1/6",
        "Evaluate 1/(3·7)+1/(7·11)+…+1/(31·35).": "8/105",
        "Evaluate 5/(2²·3²)+7/(3²·4²)+9/(4²·5²)+…+39/(19²·20²).": "99/400",
        "Evaluate (1−1/2²)(1−1/3²)…(1−1/90²).": "91/180",
        "How many trailing zeroes are in 100!?": "24",
        "Find the least positive integer whose square is divisible by 2⁶·3⁴·5³.": "1800",
    }
    for stem, answer in expected.items():
        row = rows[stem]
        assert row["options"][row["correct_option"]] == answer

