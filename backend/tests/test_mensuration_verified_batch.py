"""Batch shape, calculation-ledger alignment, MCQ and duplicate checks."""
import json
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
BATCH = BASE / "data" / "mensuration_verified_batch.json"
LEDGER = BASE / "data" / "mensuration_answer_ledger.json"


def norm(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def test_batch_rows_match_independent_answer_ledger_and_mcq_invariants():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    assert len(rows) == len(ledger) == 90
    assert Counter(row["difficulty"] for row in rows) == {"EASY": 30, "MEDIUM": 30, "HARD": 30}
    assert sum(row["source"] == "Original SSC-style practice question" for row in rows) == 65
    assert sum(row["source"].startswith("Mensuration ") for row in rows) == 25
    for i, (row, audit) in enumerate(zip(rows, ledger), start=1):
        assert (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) == ("maths", "advanced-maths", "mensuration")
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
        "A square has diagonal 15√2 cm. Find its area.": "225",
        "A rhombus has side 13 cm and one diagonal 10 cm. Find the other diagonal.": "24",
        "A rectangular field has one side 15 m and diagonal 17 m. Find its area.": "120",
        "A parallelogram has adjacent sides 60 cm and 40 cm and a diagonal 80 cm. Find its area.": "600√15 cm²",
        "A parallelogram has adjacent sides 12 cm and 14 cm; one diagonal is 16 cm. Find the other diagonal.": "2√106 cm",
        "A 90° sector has radius 14 cm. Find its area using π=22/7.": "154",
        "A cylinder of radius 6 cm and height 8 cm is melted into a cone of radius 4 cm. Find cone height.": "54",
        "A room 12 m × 8 m × 4 m has one door 2 m × 1 m and two windows each 1.5 m × 1 m. Find area of four walls to paint.": "155 m²",
        "A hemispherical dome of radius 7 m is painted outside at ₹12 per m². Find the cost using π=22/7.": "₹3696",
    }
    for stem, expected in cases.items():
        row = rows[stem]
        assert row["options"][row["correct_option"]] == expected
