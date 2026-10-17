"""Batch shape, calculation-ledger alignment, MCQ and duplicate checks."""
import json
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
BATCH = BASE / "data" / "statistics_verified_batch.json"
LEDGER = BASE / "data" / "statistics_answer_ledger.json"


def norm(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def test_batch_rows_match_independent_answer_ledger_and_mcq_invariants():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    assert len(rows) == len(ledger) == 90
    assert Counter(row["difficulty"] for row in rows) == {"EASY": 30, "MEDIUM": 30, "HARD": 30}
    assert all(row["source"] == "Original SSC-style practice question" for row in rows)
    for i, (row, audit) in enumerate(zip(rows, ledger), start=1):
        assert (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) == ("maths", "advanced-maths", "statistics")
        assert row["is_pyq"] is False and row.get("pyq_year") is None and row.get("pyq_exam_name") is None
        assert row["question_text"].strip() and row["explanation"].strip()
        assert set(row["options"]) == set("ABCD")
        assert all(isinstance(v, str) and v.strip() for v in row["options"].values())
        assert len({norm(v) for v in row["options"].values()}) == 4
        assert row["correct_option"] in row["options"]
        assert row["options"][row["correct_option"]] == audit["expected_answer"]
        assert row["question_text"] == audit["question"]
        assert row["difficulty"] == audit["difficulty"]
        assert audit["row"] == i and audit["independent_calculation"].strip()


def test_stems_are_unique_and_not_near_verbatim_duplicates():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    stems = [norm(row["question_text"]) for row in rows]
    assert len(set(stems)) == 90
    for i, stem in enumerate(stems):
        assert all(SequenceMatcher(None, stem, previous).ratio() < .97 for previous in stems[:i])


def test_independently_recomputed_answer_samples_cover_formulas_and_rounding():
    rows = {r["question_text"]: r for r in json.loads(BATCH.read_text(encoding="utf-8"))["questions"]}
    cases = {
        "Find the arithmetic mean of 18, 24, 31, 37 and 40.": "30",
        "For values 1, 2 and 3 with frequencies 2, 5 and 3, find the arithmetic mean.": "2.1",
        "A grouped distribution has classes 0–10, 10–20, 20–30 with frequencies 5, 9, 6. Estimate its median using continuous class boundaries.": "15.56",
        "A grouped distribution has modal class 30–40; adjacent frequencies are 7 and 5, and modal frequency is 13. Estimate its mode.": "34.29",
        "For the population 1, 2, 3, 4, 5, 6, find the variance.": "2.92",
        "A grouped distribution has classes 0–10, 10–20, 20–30, 30–40 and frequencies 5, 8, 12, 5. Using continuous boundaries, estimate the median.": "21.67",
    }
    for stem, expected in cases.items():
        row = rows[stem]
        assert row["options"][row["correct_option"]] == expected
