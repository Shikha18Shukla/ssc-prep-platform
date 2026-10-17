"""Batch shape, calculation-ledger alignment, MCQ and duplicate checks."""
import json
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
BATCH = BASE / "data" / "algebra_verified_batch.json"
LEDGER = BASE / "data" / "algebra_answer_ledger.json"
ORIGINAL = "Original SSC-style practice question"


def norm(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def test_batch_rows_match_independent_answer_ledger_and_mcq_invariants():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    assert len(rows) == len(ledger) == 90
    assert Counter(row["difficulty"] for row in rows) == {"EASY": 30, "MEDIUM": 30, "HARD": 30}
    assert sum(row["source"] == ORIGINAL for row in rows) == 41
    assert sum(row["source"].startswith(("Algebra ", "_Algebra ")) for row in rows) == 49
    for i, (row, audit) in enumerate(zip(rows, ledger), start=1):
        assert (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) == ("maths", "advanced-maths", "algebra")
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


def test_independently_recomputed_answer_samples_cover_algebra_identities():
    rows = {r["question_text"]: r for r in json.loads(BATCH.read_text(encoding="utf-8"))["questions"]}
    cases = {
        "If x² + 3x + 1 = 0, then the value of x⁶ + 1/x⁶ is:": "322",
        "If √x − 1/√x = √6, then x² + 1/x² is equal to:": "62",
        "If x + 1/x = 5, find the value of x⁵ + 1/x⁵.": "2525",
        "If x + 1/x = 3, then the value of x⁷ + 1/x⁷ is:": "843",
        "If a + b + c = 16 and a² + b² + c² = 90, find ab + bc + ca.": "83",
        "If a = 25, b = 15, c = −10, then the value of (a³ + b³ + c³ − 3abc)/((a − b)² + (b − c)² + (c − a)²) is:": "15",
        "If a + b + c = 6, a² + b² + c² = 14 and a³ + b³ + c³ = 36, then the value of abc is:": "6",
        "If x + y + z = 7, x² + y² + z² = 85 and x³ + y³ + z³ = 913, then the value of ∛(xyz) is:": "4",
        "If x − 1/x = √5, find x³ − 1/x³.": "8√5",
        "If x + 1/x = 6, find (x − 1/x)².": "32",
    }
    for stem, expected in cases.items():
        row = rows[stem]
        assert row["options"][row["correct_option"]] == expected
