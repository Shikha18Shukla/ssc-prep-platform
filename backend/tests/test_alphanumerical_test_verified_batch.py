"""Structural and answer-ledger checks for the Alphanumerical Test batch."""

import json
import re
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
BATCH = BASE / "data" / "alphanumerical_test_verified_batch.json"
LEDGER = BASE / "data" / "alphanumerical_test_answer_ledger.json"


def norm(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def contents():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    return rows, ledger


def test_batch_and_ledger_have_30_aligned_valid_normal_records():
    rows, ledger = contents()
    assert len(rows) == len(ledger) == 30
    assert Counter(row["difficulty"] for row in rows) == {
        "EASY": 10,
        "MEDIUM": 12,
        "HARD": 8,
    }
    assert Counter("pdf" if row["source"].startswith("Alphanumerical test") else "original" for row in rows) == {
        "pdf": 25,
        "original": 5,
    }
    for index, (row, audit) in enumerate(zip(rows, ledger), start=1):
        assert row["subject_slug"] == "reasoning"
        assert row["chapter_slug"] == "alphanumerical-test"
        assert row["is_pyq"] is False
        assert row.get("pyq_year") is None
        assert row.get("pyq_exam_name") is None
        assert row["difficulty"] in {"EASY", "MEDIUM", "HARD"}
        assert row["question_text"].strip()
        assert len(row["explanation"].strip()) >= 20
        options = row["options"]
        assert set(options) == set("ABCD")
        assert all(isinstance(value, str) and value.strip() for value in options.values())
        assert len({norm(value) for value in options.values()}) == 4
        assert row["correct_option"] in options
        answer = options[row["correct_option"]]
        assert sum(norm(value) == norm(answer) for value in options.values()) == 1
        assert audit["row"] == index
        assert audit["question"] == row["question_text"]
        assert audit["difficulty"] == row["difficulty"]
        assert audit["source"] == row["source"]
        assert audit["expected_answer"] == answer
        assert audit["independent_reasoning"].strip()
        if row["source"].startswith("Alphanumerical test"):
            assert "PDF page " in row["source"] and "exam/year not stated" in row["source"]
        else:
            assert row["source"] == "Original SSC-style practice question"


def test_batch_stems_are_unique_and_no_existing_alphanumerical_artifact_duplicates():
    rows, _ = contents()
    stems = [norm(row["question_text"]) for row in rows]
    assert len(set(stems)) == 30
    for i, stem in enumerate(stems):
        assert all(SequenceMatcher(None, stem, prior).ratio() < 0.97 for prior in stems[:i])

    for path in (BASE / "data").rglob("*.json"):
        if path == BATCH:
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        prior_rows = payload.get("questions", []) if isinstance(payload, dict) else []
        for prior in prior_rows:
            assert norm(prior.get("question_text", "")) not in set(stems)


def test_independently_recomputed_answer_checkpoints():
    rows, _ = contents()
    answers = {row["question_text"]: row["options"][row["correct_option"]] for row in rows}
    assert answers[rows[0]["question_text"]] == "One"
    assert answers[rows[1]["question_text"]] == "Three"
    assert answers[rows[2]["question_text"]] == "Four"
    assert answers[rows[3]["question_text"]] == "Two"
    assert answers[rows[4]["question_text"]] == "Six"
    assert answers[rows[5]["question_text"]] == "627"
    assert answers[rows[6]["question_text"]] == "7"
    assert answers[rows[7]["question_text"]] == "D"
    assert answers[rows[8]["question_text"]] == "I"
    assert answers[rows[9]["question_text"]] == "652"
    assert answers[rows[10]["question_text"]] == "U"
    assert answers[rows[11]["question_text"]] == "F"
    assert answers[rows[12]["question_text"]] == "K"
    assert answers[rows[13]["question_text"]] == "T"
    assert answers[rows[14]["question_text"]] == "Q"
    assert answers[rows[15]["question_text"]] == "B"
    assert answers[rows[16]["question_text"]] == "4"
    assert answers[rows[17]["question_text"]] == "Two"
    assert answers[rows[18]["question_text"]] == "Three"
    assert answers[rows[19]["question_text"]] == "103"
    assert answers[rows[20]["question_text"]] == "Ten"
    assert answers[rows[21]["question_text"]] == "0"
    assert answers[rows[22]["question_text"]] == "M"
    assert answers[rows[28]["question_text"]] == "None of these"
    assert answers[rows[29]["question_text"]] == "Q"
    assert answers[rows[23]["question_text"]] == "Z42"
    assert answers[rows[24]["question_text"]] == "A64"
    assert answers[rows[25]["question_text"]] == "4-18-9-2"
    assert answers[rows[26]["question_text"]] == "B2, D4, F6, H8"
    assert answers[rows[27]["question_text"]] == "4"


def test_source_metadata_contains_no_claimed_exam_provenance():
    rows, _ = contents()
    for row in rows:
        assert row["is_pyq"] is False
        assert row.get("pyq_year") is None and row.get("pyq_exam_name") is None
        if row["source"].startswith("Alphanumerical test"):
            assert not re.search(r"SSC|CGL|CHSL|exam\s*20\d\d", row["source"], re.I)
