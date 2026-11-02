"""Formal-logic, provenance, option, and duplicate checks for CH-07 Syllogism."""

import copy
import json
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path
from types import SimpleNamespace

from app.services.test_service import _selection_counts
from scripts import build_syllogism_artifacts as logic

BASE = Path(__file__).resolve().parents[1]
BATCH = BASE / "data" / "syllogism_verified_batch.json"
LEDGER = BASE / "data" / "syllogism_answer_ledger.json"
ORIGINAL = "Original SSC-style practice question"


def norm(text):
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def records():
    return (
        json.loads(BATCH.read_text(encoding="utf-8"))["questions"],
        json.loads(LEDGER.read_text(encoding="utf-8")),
    )


def test_batch_ledger_distribution_provenance_and_rejections_align():
    rows, ledger = records()
    assert len(rows) == len(ledger) == 30
    assert Counter(row["difficulty"] for row in rows) == {"EASY": 10, "MEDIUM": 10, "HARD": 10}
    assert Counter("original" if row["source"] == ORIGINAL else "pdf" for row in rows) == {"pdf": 19, "original": 11}
    rejected = ledger[0]["rejected_source_questions"]
    assert len(rejected) == 6
    assert Counter(item["source_pdf"] for item in rejected) == {
        "Syllogism 02_ Class Notes.pdf": 3,
        "Syllogism 03_ Class Notes.pdf": 3,
    }
    assert {item["source_page"] for item in rejected} >= {5, 6, 7, 8, 19, 20}
    for index, (row, audit) in enumerate(zip(rows, ledger), 1):
        assert (row["subject_slug"], row["subcategory_slug"], row["chapter_slug"]) == ("reasoning", None, "syllogism")
        assert row["is_pyq"] is False and row["pyq_year"] is None and row["pyq_exam_name"] is None
        assert audit["question_id"] == f"syllogism-{index:03}" and audit["row"] == index
        assert audit["question"] == row["question_text"] and audit["options"] == row["options"]
        assert audit["expected_answer"] == row["options"][row["correct_option"]]
        assert audit["source"] == row["source"] and audit["difficulty"] == row["difficulty"]
        assert audit["statements"] and audit["verification_status"].startswith("PASS")
        if row["source"] == ORIGINAL:
            assert audit["source_type"] == "original" and audit["source_pdf"] is None and audit["source_page"] is None
        else:
            assert audit["source_type"] == "pdf-derived"
            assert audit["source_pdf"] in row["source"] and isinstance(audit["source_page"], int)


def test_options_are_unique_and_each_question_has_one_checked_answer():
    rows, ledger = records()
    for row, audit in zip(rows, ledger):
        options = row["options"]
        assert set(options) == set("ABCD")
        assert len({norm(text) for text in options.values()}) == 4
        assert row["correct_option"] in options
        assert options[row["correct_option"]] == audit["expected_answer"]
        assert audit["option_review"].startswith("Four distinct options")


def test_all_answers_recompute_from_set_constraints_and_options():
    rows, ledger = records()
    for number, record in enumerate(copy.deepcopy(logic.ITEMS), 1):
        record["formulas"] = [
            formula for statement in record["statements"]
            for formula in logic.parse_statement(statement)
        ]
        actual = logic.evaluated_code(record)
        assert actual == record["answer"], (number, actual, record["answer"])
        row = rows[number - 1]
        if record["kind"] in {"possibility", "impossible"}:
            assert row["correct_option"] == actual
            calculated = [
                logic.model_exists(record["formulas"], [formula])
                for formula in record["possibility_options"]
            ]
            assert calculated == ledger[number - 1]["possible_options"]
        else:
            expected_key = next(
                chr(65 + offset) for offset, (_, code) in enumerate(record["choices"])
                if code == actual
            )
            assert row["correct_option"] == expected_key


def test_empty_classes_only_a_few_and_complementary_conclusions():
    all_ab = logic.F("ALL", "A", "B")
    some_ab = logic.F("SOME", "A", "B")
    no_ab = logic.F("NO", "A", "B")
    some_not_ab = logic.F("SOME_NOT", "A", "B")
    assert not logic.entails([all_ab], some_ab)
    assert logic.entails([all_ab], logic.F("ALL", "A", "B"))
    assert not logic.model_exists([no_ab], [some_ab])
    assert logic.disjunction_entails([], no_ab, some_ab)
    assert not logic.disjunction_entails([some_ab], no_ab, some_not_ab)
    # Some A are B and Some A are not B can both hold, so the first pair is not exclusive.
    both_model = [some_ab, some_not_ab]
    assert logic.model_exists(both_model)
    only_few = [formula for statement in ["Only a few guides are volunteers."] for formula in logic.parse_statement(statement)]
    assert logic.entails(only_few, logic.F("SOME", "Guides", "Volunteers"))
    assert logic.entails(only_few, logic.F("SOME_NOT", "Guides", "Volunteers"))
    only = logic.parse_statement("Only mentors are guides.")
    assert only == [logic.F("ALL", "Guide", "Mentor")]


def test_batch_has_no_stem_or_signature_duplicates_and_no_canonical_near_duplicates():
    rows, ledger = records()
    stems = [norm(row["question_text"]) for row in rows]
    assert len(set(stems)) == len(stems)
    signatures = [audit["concept_signature"] for audit in ledger]
    assert len(set(signatures)) == len(signatures)
    for path in BASE.joinpath("data").glob("*_verified_batch.json"):
        if path == BATCH:
            continue
        try:
            old_rows = json.loads(path.read_text(encoding="utf-8")).get("questions", [])
        except (OSError, json.JSONDecodeError):
            continue
        for old in old_rows if isinstance(old_rows, list) else []:
            if not isinstance(old, dict) or old.get("subject_slug") != "reasoning":
                continue
            candidate = norm(old.get("question_text", ""))
            if not candidate:
                continue
            assert candidate not in set(stems), f"Exact duplicate in {path.name}: {candidate}"
            for stem in stems:
                if abs(len(candidate) - len(stem)) <= 0.03 * max(len(candidate), len(stem)):
                    assert SequenceMatcher(None, candidate, stem, autojunk=False).ratio() < 0.97, f"Near duplicate in {path.name}"


def test_each_difficulty_and_mixed_practice_support_platform_counts():
    rows, _ = records()
    counts = Counter(row["difficulty"] for row in rows)
    assert all(_selection_counts(counts[level], SimpleNamespace(slug="reasoning")) == [10]
               for level in ("EASY", "MEDIUM", "HARD"))
    assert _selection_counts(30, SimpleNamespace(slug="reasoning")) == [10, 15, 20, 25]


def test_review_report_documents_all_pages_method_and_completed_live_verification():
    report = (BASE / "data" / "syllogism_review_report.md").read_text(encoding="utf-8")
    for phrase in ("18/18", "22/22", "14/14", "54/54", "25", "19", "6",
                   "Universal statements do not imply existence", "Either/or", "COMPLETED",
                   "4,053 active question stems", "0 PYQ", "10, 15, 20, and 25"):
        assert phrase.casefold() in report.casefold()
