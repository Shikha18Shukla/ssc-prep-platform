"""Artifact, metadata, provenance, answer-ledger, and duplication checks for Series."""

import json
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path
from types import SimpleNamespace

from app.services.test_service import _selection_counts

BASE = Path(__file__).resolve().parents[1]
BATCH = BASE / "data" / "series_verified_batch.json"
LEDGER = BASE / "data" / "series_answer_ledger.json"
ORIGINAL = "Original SSC-style practice question"


def norm(text):
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def records():
    return json.loads(BATCH.read_text(encoding="utf-8"))["questions"], json.loads(LEDGER.read_text(encoding="utf-8"))


def test_batch_has_32_aligned_valid_normal_questions():
    rows, ledger = records()
    assert len(rows) == len(ledger) == 32
    assert Counter(row["difficulty"] for row in rows) == {"EASY": 10, "MEDIUM": 12, "HARD": 10}
    assert Counter("original" if row["source"] == ORIGINAL else "pdf" for row in rows) == {"pdf": 27, "original": 5}
    for i, (row, audit) in enumerate(zip(rows, ledger), 1):
        assert (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) == ("reasoning", None, "series")
        assert row["is_pyq"] is False and row["pyq_year"] is None and row["pyq_exam_name"] is None
        assert row["difficulty"] in {"EASY", "MEDIUM", "HARD"}
        assert row["question_text"].strip() and row["explanation"].strip()
        assert len(row["source"]) <= 255
        options = row["options"]
        assert set(options) == set("ABCD")
        assert all(isinstance(value, str) and value.strip() for value in options.values())
        assert len({norm(value) for value in options.values()}) == 4
        assert row["correct_option"] in options
        assert sum(norm(value) == norm(options[row["correct_option"]]) for value in options.values()) == 1
        assert audit["question_id"] == f"series-{i:03}" and audit["row"] == i
        assert audit["question"] == row["question_text"]
        assert audit["expected_answer"] == options[row["correct_option"]]
        assert audit["correct_option"] == row["correct_option"]
        assert audit["difficulty"] == row["difficulty"] and audit["source"] == row["source"]
        assert audit["independent_reasoning"].strip() and audit["option_review"].strip()
        assert audit["validation_status"].startswith("PASS")
        if row["source"] == ORIGINAL:
            assert audit["source_type"] == "original"
            assert audit["source_pdf"] is None and audit["source_page"] is None
        else:
            assert audit["source_type"] == "pdf-derived"
            assert audit["source_pdf"] in row["source"]
            assert isinstance(audit["source_page"], int) and audit["source_page"] > 0


def test_stems_and_problem_signatures_are_unique_and_reviewed():
    rows, ledger = records()
    stems = [norm(row["question_text"]) for row in rows]
    assert len(set(stems)) == len(rows)
    signatures = [audit["concept_signature"] for audit in ledger]
    assert all(signatures) and len(set(signatures)) == len(rows)
    for i, stem in enumerate(stems):
        for prior in stems[:i]:
            assert SequenceMatcher(None, stem, prior).ratio() < 0.97
    for path in (BASE / "data").glob("*.json"):
        if path == BATCH:
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        prior_rows = payload.get("questions", []) if isinstance(payload, dict) else []
        for prior in prior_rows if isinstance(prior_rows, list) else []:
            if not isinstance(prior, dict) or not isinstance(prior.get("question_text"), str):
                continue
            candidate = norm(prior["question_text"])
            assert candidate not in set(stems), f"Exact duplicate in {path.name}: {prior['question_text']}"
            if prior.get("subject_slug") == "reasoning":
                assert all(SequenceMatcher(None, candidate, stem).ratio() < 0.97 for stem in stems), f"Near duplicate in {path.name}"


def test_independent_answer_checkpoints():
    rows, _ = records()
    keyed = {row["question_text"]: row["options"][row["correct_option"]] for row in rows}
    expected = {
        "What will be the next term in the given series? 2, 13, 79, 475, ?": "2851",
        "What number replaces the question mark? 2, 14, 70, 210, ?": "210",
        "What is the ninth pair in the series? 3+3, 8+4, 15+5, 24+6, 35+7, ...": "99 + 11",
        "In the series 5, 11, 18, (25), 35, (45), 56, decide whether the bracketed numbers are correct.": "The first is incorrect and the second is correct.",
        "Find the wrong number in the series: 0, 4, 18, 48, 96, 180": "96",
        "What is the next alphanumeric term? A1, C4, F9, J16, O25, ?": "U36",
        "What is the next term? 1, 4, 10, 20, 35, 56, ?": "84",
        "What is the next term in the series? 1, 2, 5, 12, 29, ?": "70",
        "Find the next term: 3, 4, 7, 16, 43, ?": "124",
    }
    assert all(keyed[stem] == answer for stem, answer in expected.items())


def test_two_new_hard_items_are_original_and_have_distinct_rules():
    rows, ledger = records()
    additions = rows[30:]
    audits = ledger[30:]
    assert len(additions) == len(audits) == 2
    assert [audit["question_id"] for audit in audits] == ["series-031", "series-032"]
    assert all(row["difficulty"] == "HARD" and row["source"] == ORIGINAL for row in additions)
    assert all(audit["source_type"] == "original" and audit["source_pdf"] is None and audit["source_page"] is None for audit in audits)
    assert {audit["concept_signature"] for audit in audits} == {
        "second_order_recurrence_twice_previous_plus_previous_previous",
        "geometric_progression_in_first_differences_ratio_three",
    }


def test_hard_bank_now_meets_existing_reasoning_test_minimum():
    rows, _ = records()
    hard_count = sum(row["difficulty"] == "HARD" for row in rows)
    assert hard_count == 10
    assert _selection_counts(hard_count, SimpleNamespace(slug="reasoning")) == [10]
