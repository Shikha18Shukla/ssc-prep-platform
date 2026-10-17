"""Batch shape, calculation-ledger alignment, MCQ and duplicate checks."""
import json
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
BATCH = BASE / "data" / "hcf_lcm_verified_batch.json"
LEDGER = BASE / "data" / "hcf_lcm_answer_ledger.json"
ORIGINAL = "Original SSC-style practice question"


def norm(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def test_batch_rows_match_independent_answer_ledger_and_mcq_invariants():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    assert len(rows) == len(ledger) == 90
    assert Counter(row["difficulty"] for row in rows) == {"EASY": 30, "MEDIUM": 30, "HARD": 30}
    assert sum(row["source"] == ORIGINAL for row in rows) == 71
    assert sum(row["source"].startswith("HCF and LCM ") for row in rows) == 19
    for i, (row, audit) in enumerate(zip(rows, ledger), start=1):
        assert (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) == ("maths", "advanced-maths", "hcf-and-lcm")
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


def test_independently_recomputed_answer_samples_cover_hcf_lcm_cases():
    rows = {r["question_text"]: r for r in json.loads(BATCH.read_text(encoding="utf-8"))["questions"]}
    cases = {
        "Find the HCF of 35 and 30.": "5",
        "Find the HCF of 240, 280 and 560.": "40",
        "The LCM of two numbers is 45 times their HCF. If one of the numbers is 125 and the sum of the HCF and the LCM is 1150, the other number is:": "225",
        "Find the LCM of 15, 24, 32 and 45.": "1440",
        "Find the LCM of 48, 50, 98, 54 and 72.": "2⁴ × 3³ × 5² × 7²",
        "What is the HCF of 7/16, 21/32 and 49/8?": "7/32",
        "Find the difference between the LCM and the HCF of 4/7, 5/14 and 9/35.": "25.7",
        "Find the least number which is divisible by 2, 3, 4, 5 and 6, leaves a remainder 1 in each case, and is completely divisible by 7.": "301",
        "Find the least number which when divided by 5, 6, 7 and 8 leaves a remainder 3 in each case, but when divided by 9 leaves no remainder.": "1683",
        "Six bells ring after 2, 4, 6, 8, 10 and 12 seconds respectively. How many times will they ring simultaneously in 30 minutes?": "16",
        "Find the largest number that divides 2053 and 967, leaving remainders 5 and 7 respectively.": "64",
        "Find the least number of square tiles required to pave a floor 15 m 17 cm long and 9 m 2 cm broad.": "814",
        "Find the greatest number that divides 1305, 4665 and 6905, leaving the same remainder in each case.": "1120",
        "Reduce the fraction 161/207 to its lowest terms.": "7/9",
        "The HCF of two numbers is 24 and their LCM is 720. If one of the numbers lies between 100 and 150, find it.": "120",
        "Find the greatest number which on dividing 1657 and 2037 leaves remainders 6 and 5 respectively.": "127",
    }
    for stem, expected in cases.items():
        row = rows[stem]
        assert row["options"][row["correct_option"]] == expected
