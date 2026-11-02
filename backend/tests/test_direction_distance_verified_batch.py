"""Artifact, answer, provenance, and duplicate regression checks for Direction and Distance."""

import json
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path
from types import SimpleNamespace

from app.services.test_service import _selection_counts

BASE = Path(__file__).resolve().parents[1]
BATCH = BASE / "data" / "direction_distance_verified_batch.json"
LEDGER = BASE / "data" / "direction_distance_answer_ledger.json"
ORIGINAL = "Original SSC-style practice question"


def norm(text):
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def records():
    return json.loads(BATCH.read_text(encoding="utf-8"))["questions"], json.loads(LEDGER.read_text(encoding="utf-8"))


def test_batch_ledger_options_and_provenance_are_aligned():
    rows, ledger = records()
    assert len(rows) == len(ledger) == 37
    assert Counter(row["difficulty"] for row in rows) == {"EASY": 12, "MEDIUM": 14, "HARD": 11}
    assert Counter("original" if row["source"] == ORIGINAL else "pdf" for row in rows) == {"original": 19, "pdf": 18}
    for i, (row, audit) in enumerate(zip(rows, ledger), 1):
        assert (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) == ("reasoning", None, "direction-and-distance")
        assert row["is_pyq"] is False and row["pyq_year"] is None and row["pyq_exam_name"] is None
        assert row["question_text"].strip() and row["explanation"].strip()
        options = row["options"]
        assert set(options) == set("ABCD") and len({norm(x) for x in options.values()}) == 4
        assert row["correct_option"] in options
        assert audit["question_id"] == f"direction-distance-{i:03}"
        assert audit["question"] == row["question_text"]
        assert audit["expected_answer"] == options[row["correct_option"]]
        assert audit["difficulty"] == row["difficulty"] and audit["source"] == row["source"]
        assert audit["verification_status"].startswith("PASS")
        assert audit["independent_reasoning"].strip() and audit["option_review"].strip()
        if row["source"] == ORIGINAL:
            assert audit["source_type"] == "original" and audit["source_pdf"] is None and audit["source_page"] is None
        else:
            assert audit["source_type"] == "pdf-derived" and isinstance(audit["source_page"], int)
            assert audit["source_pdf"] in row["source"]


def test_question_signatures_and_existing_canonical_batches_are_distinct():
    rows, ledger = records()
    stems = [norm(row["question_text"]) for row in rows]
    assert len(set(stems)) == len(rows)
    signatures = [audit["concept_signature"] for audit in ledger]
    assert all(signatures) and len(set(signatures)) == len(rows)
    for i, stem in enumerate(stems):
        assert all(SequenceMatcher(None, stem, prior).ratio() < 0.97 for prior in stems[:i])
    paths = list((BASE / "data").glob("*.json")) + [BASE.parent / "maximum_and_minimum_value_verified_batch.json"]
    for path in paths:
        if path == BATCH:
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        previous = payload.get("questions", []) if isinstance(payload, dict) else []
        for old in previous if isinstance(previous, list) else []:
            if not isinstance(old, dict) or old.get("subject_slug") != "reasoning":
                continue
            candidate = norm(old.get("question_text", ""))
            assert candidate not in set(stems), f"Exact duplicate in {path.name}: {candidate}"
            assert all(SequenceMatcher(None, candidate, stem).ratio() < 0.97 for stem in stems), f"Near duplicate in {path.name}: {candidate}"


def test_independent_direction_and_distance_checkpoints():
    rows, _ = records()
    keyed = {row["question_text"]: row["options"][row["correct_option"]] for row in rows}
    assert keyed["If South-East is renamed North and North-East is renamed West under one consistent rotation, what does West become?"] == "South-East"
    assert keyed["A driver goes 12 km east, turns left for 9 km, turns left for 13 km, turns left for 11 km, then turns left and goes 1 km. What is the shortest distance and direction back to the start?"] == "2 km north"
    assert keyed["A child walks 90 m east, turns right for 20 m, turns right for 30 m, then walks north 100 m to meet his father. How far is the father from the child's starting point?"] == "100 m"
    assert keyed["In a code, M*N means M is south of N; M+N means M is north of N; M%N means M is east of N; M−N means M is west of N. Where is R relative to P in O%P+Q−R?"] == "South-East"
    assert keyed["Fardeen starts facing west, walks 13 km, turns left for 7 km, turns right for 6 km, turns left for 8 km, and finally turns left for 19 km. How far and in which direction is he from his starting point?"] == "15 km south"
    assert keyed["A trekker walks 3 km north and 4 km east, then follows a straight route back home. How many kilometers shorter is the straight return than the outward walk?"] == "2 km"
    assert keyed["Starting at home, Richa walks five legs: 50 m west, 90 m south, 30 m east, 120 m north, and 20 m east. What is the total path length?"] == "310 m"


def test_all_three_difficulties_meet_reasoning_test_minimum():
    rows, _ = records()
    counts = Counter(row["difficulty"] for row in rows)
    assert all(_selection_counts(counts[level], SimpleNamespace(slug="reasoning")) == [10] for level in ("EASY", "MEDIUM", "HARD"))
    _, ledger = records()
    rejected = ledger[10]["rejected_source_questions"]
    assert len(rejected) == 1
    assert rejected[0]["source_page"] == 12 and "duplicate" in rejected[0]["rejection_reason"].casefold()
