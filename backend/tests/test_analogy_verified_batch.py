"""Structural, provenance, uniqueness, and answer-ledger checks for Analogy."""

import json
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
BATCH = BASE / "data" / "analogy_verified_batch.json"
LEDGER = BASE / "data" / "analogy_answer_ledger.json"
ORIGINAL = "Original SSC-style practice question"


def norm(text):
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def records():
    return json.loads(BATCH.read_text(encoding="utf-8"))["questions"], json.loads(LEDGER.read_text(encoding="utf-8"))


def test_batch_has_30_aligned_valid_normal_questions():
    rows, ledger = records()
    assert len(rows) == len(ledger) == 30
    assert Counter(row["difficulty"] for row in rows) == {"EASY": 10, "MEDIUM": 12, "HARD": 8}
    assert Counter("original" if row["source"] == ORIGINAL else "pdf" for row in rows) == {"pdf": 21, "original": 9}
    for i, (row, audit) in enumerate(zip(rows, ledger), 1):
        assert row["subject_slug"] == "reasoning"
        assert row["subcategory_slug"] is None
        assert row["chapter_slug"] == "analogy"
        assert row["is_pyq"] is False
        assert row["pyq_year"] is None and row["pyq_exam_name"] is None
        assert row["difficulty"] in {"EASY", "MEDIUM", "HARD"}
        assert row["question_text"].strip() and row["explanation"].strip()
        assert len(row["source"]) <= 255
        options = row["options"]
        assert set(options) == set("ABCD")
        assert all(isinstance(v, str) and v.strip() for v in options.values())
        assert len({norm(v) for v in options.values()}) == 4
        assert row["correct_option"] in options
        assert sum(norm(v) == norm(options[row["correct_option"]]) for v in options.values()) == 1
        assert audit["row"] == i and audit["question"] == row["question_text"]
        assert audit["expected_answer"] == options[row["correct_option"]]
        assert audit["correct_option"] == row["correct_option"]
        assert audit["difficulty"] == row["difficulty"] and audit["source"] == row["source"]
        assert audit["independent_reasoning"].strip() and audit["option_review"].strip()
        assert audit["concept_signature"].strip()
        if row["source"] != ORIGINAL:
            assert row["source"].startswith("Analogy 0")
            assert "lecture slide " in row["source"] and "exam/year not stated" in row["source"]


def test_stems_and_underlying_problem_signatures_are_unique():
    rows, ledger = records()
    stems = [norm(row["question_text"]) for row in rows]
    assert len(set(stems)) == 30
    signatures = [audit["concept_signature"] for audit in ledger]
    assert len(set(signatures)) == 30
    for i, stem in enumerate(stems):
        for prior in stems[:i]:
            assert SequenceMatcher(None, stem, prior).ratio() < 0.97

    # Top-level data JSON files are the canonical subject/chapter banks and ledgers;
    # nested imports/ directories contain review scratch data for unrelated subjects.
    for path in (BASE / "data").glob("*.json"):
        if path == BATCH:
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        prior_rows = payload.get("questions", []) if isinstance(payload, dict) else []
        if not isinstance(prior_rows, list):
            continue
        for prior in prior_rows:
            if not isinstance(prior, dict) or not isinstance(prior.get("question_text"), str):
                continue
            candidate = norm(prior["question_text"])
            assert candidate not in set(stems), f"Exact artifact duplicate in {path.name}: {prior['question_text']}"
            # Fuzzy comparison is meaningful for the same reasoning domain; exact
            # stem comparison above still checks every canonical subject batch.
            if prior.get("subject_slug") == "reasoning" or prior.get("chapter_slug") == "analogy":
                assert all(SequenceMatcher(None, candidate, stem).ratio() < 0.97 for stem in stems), f"Near-duplicate artifact stem in {path.name}"


def test_recomputed_numeric_and_letter_answer_checkpoints():
    rows, _ = records()
    keyed = {row["question_text"]: row["options"][row["correct_option"]] for row in rows}
    assert keyed["86 : 298 :: 105 : 317 :: 48 : ?"] == str(48 + 212)
    assert keyed["35 : 21 :: ? : 36 :: 40 : 24"] == str(36 * 5 / 3).removesuffix(".0")
    assert keyed["12 : 132 :: 20 : 380 :: 2 : ?"] == str(2 * (2 - 1))
    assert keyed["4 : 84 :: 11 : ? :: 13 : 2379"] == str(11**3 + 11**2 + 11)
    assert keyed["X : 1332 :: 17 : Y"] == "X=11, Y=4914"
    assert keyed["6 : 32 :: 10 : ? :: 11 : 117"] == str(10**2 - 4)
    assert keyed["3 : 8 :: 6 : ? :: 11 : 1000"] == str((6 - 1) ** 3)
    assert keyed["2 : 10 :: 4 : 68 :: 6 : ?"] == str(6**3 + 6)
    assert keyed["AC : CF :: MO : ?"] == "OR"
    assert keyed["ABCD : BDFH :: CDEF : ?"] == "DFHJ"
