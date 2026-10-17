"""Batch shape, calculation-ledger alignment, MCQ and duplicate checks."""
import json
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
BATCH = BASE / "data" / "simplification_verified_batch.json"
LEDGER = BASE / "data" / "simplification_answer_ledger.json"
ORIGINAL = "Original SSC-style practice question"


def norm(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def test_batch_rows_match_independent_answer_ledger_and_mcq_invariants():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    assert len(rows) == len(ledger) == 90
    assert Counter(row["difficulty"] for row in rows) == {"EASY": 30, "MEDIUM": 30, "HARD": 30}
    assert sum(row["source"] == ORIGINAL for row in rows) == 68
    assert sum(row["source"].startswith("Simplification ") for row in rows) == 22
    for i, (row, audit) in enumerate(zip(rows, ledger), start=1):
        assert (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) == ("maths", "advanced-maths", "simplification")
        assert row["is_pyq"] is False and row.get("pyq_year") is None and row.get("pyq_exam_name") is None
        assert row["question_text"].strip() and row["explanation"].strip()
        assert set(row["options"]) == set("ABCD")
        assert all(isinstance(v, str) and v.strip() for v in row["options"].values())
        assert len({norm(v) for v in row["options"].values()}) == 4
        assert row["correct_option"] in row["options"]
        assert row["options"][row["correct_option"]] == audit["expected_answer"]
        assert row["question_text"] == audit["question"]
        assert row["difficulty"] == audit["difficulty"]
        assert audit["row"] == i and audit["independent_reasoning"].strip()
        if row["source"] != ORIGINAL:
            assert ", PDF page " in row["source"] and "exam/year not stated" in row["source"]


def test_stems_are_unique_and_not_near_verbatim_duplicates():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    stems = [norm(row["question_text"]) for row in rows]
    assert len(set(stems)) == 90
    for i, stem in enumerate(stems):
        assert all(SequenceMatcher(None, stem, previous).ratio() < .97 for previous in stems[:i])


def test_independently_recomputed_answer_samples_cover_simplification_cases():
    rows = {r["question_text"]: r for r in json.loads(BATCH.read_text(encoding="utf-8"))["questions"]}
    cases = {
        "Find the value of 1 + 1/(1 + 1/(1 + 1/(1 + 1/(1 + 2/3)))).": "34/21",
        "If x = 1 + 1/(1 + 1/(1 + 1/(1 + 1/2))), then the value of 2x + 7/4 is:": "5",
        "Find the value of 1 − 1/(1 − 1/(1 − 1/(1 − 2/3))).": "1/3",
        "If a, b, c and d are integers such that 1/(a + 1/(b + 1/(c + 1/d))) = 29/154, then a + b + c + d = ?": "14",
        "The value of [ (3 1/5 − 3/5) ÷ 8/5 ] ÷ [ 1 1/7 ÷ { 6/7 − (1/7 ÷ 1/5) } ] is:": "13/64",
        "Simplify: [∛(⁶√(5⁹))]⁴ × [∛(⁶√(5⁹))]⁴": "5⁴",
        "The value of 3/7 ÷ 9/21 + 2 − 4/3 + 1/2 of 12/5 × 25/18 ÷ 5/9 is:": "14/3",
        "What is the value of 90 × 3 ÷ 9 + 4 ÷ 2 × 3 of 4 × 8 ÷ (18 × 2 − 4)?": "36",
        "Find the value of 36 ÷ 8 × 4 + 2 ÷ 4 − 1 + 5 of 3 ÷ (4 × 2 − 3) − 3.": "35/2",
        "The value of 5 ÷ 5 of 5 × 2 + 2 ÷ 2 of 2 × 5 − (5 − 2) ÷ 6 × 2 is:": "19/10",
        "The value of 16 ÷ 4 of 4 × [3 ÷ 4 of {4 × 3 ÷ (3 + 3)}] ÷ (2 ÷ 4 of 8) is:": "6",
        "Find the number of factors of 2³ × 3⁴ × 5⁶.": "140",
        "Find the number of factors of 720.": "30",
        "Find the number of even factors of 2³ × 3⁴ × 5⁶.": "105",
        "The value of 1/(2×3) + 1/(3×4) + 1/(4×5) + ... + 1/(19×20) is:": "9/20",
        "The value of 1/(2×5) + 1/(5×8) + 1/(8×11) + ... + 1/(23×26) is:": "2/13",
        "The value of 1/20 + 1/30 + 1/42 + ... + 1/132 is:": "1/6",
        "The value of 5/(2²×3²) + 7/(3²×4²) + 9/(4²×5²) + ... + 39/(19²×20²) is:": "99/400",
        "Simplify: 1 + 2 + 3 + ... + 99 + 100 + 99 + ... + 2 + 1": "10000",
        "Simplify: √(1 + 2 + 3 + ... + 78 + 79 + 78 + ... + 2 + 1)": "79",
        "Find the number of even factors of 842.": "2",
        "The value of 1/9 + 1/6 + 1/12 + 1/20 + ... + 1/72 is:": "0.5",
        "The value of (3/8 + 5/12) ÷ (7/8 − 3/4) is:": "19/3",
        "The value of [(0.9)² − (0.8)²] ÷ (0.9 − 0.8) is:": "1.7",
        "The value of √0.0004 + ³√0.008 is:": "0.22",
        "Simplify: √12 × √27.": "18",
        "Find the number of prime factors in 12³ (counting repetition).": "9",
        "Simplify: (16/81)^(3/4).": "8/27",
        "Simplify: (√7 + √3)² − 2√21.": "10",
        "Simplify: √(7 + 4√3) + √(7 − 4√3).": "4",
        "Find the value of 12 + 8 ÷ 4.": "14",
        "Find the value of 100 ÷ 4 + 6 × 3.": "43",
        "What is the value of 2/3 + 3/4 − 5/6?": "7/12",
        "Find the value of 20% of 15% of 400.": "12",
    }
    for stem, expected in cases.items():
        row = rows[stem]
        assert row["options"][row["correct_option"]] == expected
