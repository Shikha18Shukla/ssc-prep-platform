"""Regression checks for the verified Inequality Sets 1–4 import batch."""

import json
import re
import unicodedata
from collections import Counter
from pathlib import Path


IMPORT_FILE = (
    Path(__file__).parents[1]
    / "data/imports/reasoning/inequality/inequality_sets_01_04_verified.json"
)
LEDGER_FILE = (
    Path(__file__).parents[1]
    / "data/imports/reasoning/inequality/inequality_sets_01_04_answer_ledger.json"
)


def _normalized(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def test_verified_sets_01_04_batch_is_source_traceable_and_matches_audit_ledger():
    records = json.loads(IMPORT_FILE.read_text(encoding="utf-8"))["questions"]
    ledger = json.loads(LEDGER_FILE.read_text(encoding="utf-8"))["questions"]

    assert len(ledger) == 80
    assert Counter(row["disposition"] for row in ledger) == {
        "eligible": 65,
        "held": 15,
    }
    assert Counter(row["set_number"] for row in ledger) == {
        1: 20,
        2: 20,
        3: 20,
        4: 20,
    }
    assert len(records) == 65
    assert len({_normalized(row["question_text"]) for row in records}) == len(records)

    ledger_by_question = {
        _normalized(row["normalized_question"]): row
        for row in ledger
        if row["disposition"] == "eligible"
    }
    assert len(ledger_by_question) == len(records)

    for record in records:
        audit = ledger_by_question[_normalized(record["question_text"])]
        assert record["exam_slug"] == "banking-clerk"
        assert record["subject_slug"] == "reasoning"
        assert record["subcategory_slug"] is None
        assert record["chapter_slug"] == "inequality"
        assert set(record["options"]) == set("ABCDE")
        assert record["correct_option"] in record["options"]
        assert record["correct_option"] == audit["independent_outcome"]
        assert record["correct_option"] == audit["printed_answer"]
        assert record["explanation"].strip()
        assert record["difficulty"] in {"EASY", "MEDIUM", "HARD"}
        assert record["is_pyq"] is False
        assert len(record["source"]) <= 255
        match = re.fullmatch(
            r"INEQUALITY SET-(\d) \(Eng\)\.pdf; Set (\d); physical page (\d+)",
            record["source"],
        )
        assert match
        assert int(match.group(1)) == audit["set_number"]
        assert int(match.group(2)) == audit["set_number"]
        assert int(match.group(3)) == audit["physical_page"]

