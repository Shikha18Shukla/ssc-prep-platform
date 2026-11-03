"""Safely apply and verify the CH-17 visual-option shuffle against live rows."""
from __future__ import annotations

import argparse
import json
import logging
import sys
from collections import Counter
from pathlib import Path

from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))
from app.database.session import SessionLocal, engine
from app.models import Question, QuestionOption

from build_non_verbal_reasoning_artifacts import LETTERS, option_state_field, remap_explanation

CHAPTER_ID = "746c8d03-3645-4454-a875-7cd9109e133a"
BATCH = BASE / "data" / "non_verbal_reasoning_verified_batch.json"
LEDGER = BASE / "data" / "non_verbal_reasoning_answer_ledger.json"
DIFFICULTY_REPORT = BASE / "data" / "non_verbal_reasoning_reconciliation_report.json"
REPORT_JSON = BASE / "data" / "non_verbal_reasoning_answer_position_reconciliation_report.json"
REPORT_MD = BASE / "data" / "non_verbal_reasoning_answer_position_reconciliation_report.md"


def canonical_json(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def assert_unordered_options_preserved(original, shuffled, old_answer, new_answer):
    """Independent validation routine; compares complete visual choice states as multisets."""
    original_values = Counter(canonical_json(x) for x in original)
    shuffled_values = Counter(canonical_json(x) for x in shuffled)
    if len(original) != 4 or original_values != shuffled_values:
        raise ValueError("Original and shuffled option sets differ as unordered multisets")
    if len(shuffled_values) != 4:
        raise ValueError("Options must be four distinct visual states")
    if canonical_json(original[old_answer]) != canonical_json(shuffled[new_answer]):
        raise ValueError("Correct visual state moved incorrectly")


def load_artifacts():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    selected = [x for x in ledger if x.get("record_type") == "selected_question"]
    old = json.loads(DIFFICULTY_REPORT.read_text(encoding="utf-8"))["before"]
    if len(rows) != 33 or len(selected) != 33 or len(old["records"]) != 33:
        raise ValueError("Expected complete 33-question artifacts and prior live snapshot")
    old_by_key = {r["import_key"]: r for r in old["records"]}
    data = []
    for row, audit in zip(rows, selected):
        key = row["image_url"]
        if audit["image_asset"] != key or audit["question_id"] != key.rsplit("/", 1)[-1].replace(".svg", ""):
            raise ValueError(f"Stable import key mismatch at {key}")
        shuffle = audit["option_shuffle_audit"]
        spec = audit["rule_spec"]
        field = option_state_field(spec)
        assert_unordered_options_preserved(shuffle["original_options"], spec[field], shuffle["original_correct_index"], audit["answer_index"])
        if audit["answer_index"] != LETTERS.index(row["correct_option"]):
            raise ValueError(f"Key/index mismatch for {audit['question_id']}")
        if audit["options"] != row["options"] or audit["explanation"] != row["explanation"]:
            raise ValueError(f"Canonical/ledger mismatch for {audit['question_id']}")
        prior = old_by_key.get(key)
        if not prior or prior.get("classification") not in {"exact_match", "same_question_answer_difficulty_mismatch"}:
            raise ValueError(f"No exact-content pre-shuffle live match available for {key}")
        old_fields = prior["fields"]
        old_correct = old_fields["correct_option"]["live"]
        old_explanation = old_fields["explanation"]["live"]
        remapped_explanation = remap_explanation(old_explanation, audit["rule_family"], shuffle["old_to_new_indexes"], row["correct_option"])
        if remapped_explanation != row["explanation"]:
            raise ValueError(f"Explanation contains non-letter content changes for {key}")
        data.append({"row": row, "audit": audit, "prior": prior, "old_correct": old_correct, "old_explanation": old_explanation})
    return data, ledger


def collect_live(db):
    records = db.scalars(select(Question).where(Question.chapter_id == CHAPTER_ID).options(selectinload(Question.options))).all()
    by_key: dict[str, list[Question]] = {}
    for question in records:
        if question.image_url:
            by_key.setdefault(question.image_url, []).append(question)
    return records, by_key


def verify_preconditions(data, live_records, by_key):
    if len(live_records) != 33:
        raise RuntimeError(f"Expected exactly 33 CH-17 rows, found {len(live_records)}")
    findings = []
    for item in data:
        row, audit = item["row"], item["audit"]
        matches = by_key.get(row["image_url"], [])
        if len(matches) != 1:
            raise RuntimeError(f"Stable key is missing or ambiguous: {row['image_url']}")
        question = matches[0]
        rec = audit["database_reconciliation"]
        if str(question.id) != rec["question_uuid"] or question.chapter_id != __import__("uuid").UUID(CHAPTER_ID):
            raise RuntimeError(f"Live UUID/chapter precondition failed for {audit['question_id']}")
        if question.question_text != row["question_text"] or question.image_url != row["image_url"]:
            raise RuntimeError(f"Question text or asset changed for {audit['question_id']}")
        if question.difficulty.value != row["difficulty"] or not question.is_active or question.is_pyq:
            raise RuntimeError(f"Difficulty or status changed for {audit['question_id']}")
        option_map = {o.option_key: o.option_text for o in question.options}
        current_correct = [o.option_key for o in question.options if o.is_correct]
        if option_map != row["options"] or current_correct != [item["old_correct"]]:
            raise RuntimeError(f"Option labels or existing correct key changed for {audit['question_id']}")
        if question.explanation != item["old_explanation"]:
            raise RuntimeError(f"Explanation changed after pre-shuffle snapshot for {audit['question_id']}")
        if len(question.options) != 4 or len({o.option_text for o in question.options}) != 4:
            raise RuntimeError(f"Live options are invalid for {audit['question_id']}")
        findings.append({"question_id": audit["question_id"], "live_id": str(question.id), "old_correct": item["old_correct"],
                         "new_correct": row["correct_option"], "old_explanation": question.explanation, "new_explanation": row["explanation"],
                         "classification": "answer_key_and_letter_reference_update" if item["old_correct"] != row["correct_option"] or question.explanation != row["explanation"] else "unchanged_key_and_explanation"})
    return findings


def write_report(findings, options_updated, explanations_updated):
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    counts = Counter(r["correct_option"] for r in rows)
    body = ["# CH-17 Answer Position Reconciliation", "", f"Chapter ID: `{CHAPTER_ID}`", "",
            "## Outcome", "", f"Balanced distribution: `{dict(counts)}`.", f"Option correctness records updated: **{options_updated}**.",
            f"Explanation answer-letter references updated: **{explanations_updated}** (reasoning text preserved).", "",
            "All visual choices were compared as unordered multisets using complete option-state objects. The correct state at the prior index equals the state at the new key/index for every question. Stable `nvr-###` keys and live question UUIDs were checked; only CH-17 option correctness flags and answer-letter references in explanations were changed.", "",
            "## Per-question mapping", "", "| Import key | Live question UUID | Old key | New key | Correct state preserved |", "|---|---|---:|---:|---|"]
    for row in findings:
        body.append(f"| `{row['question_id']}` | `{row['live_id']}` | {row['old_correct']} | {row['new_correct']} | yes |")
    REPORT_JSON.write_text(json.dumps({"chapter_id": CHAPTER_ID, "answer_distribution": dict(counts), "option_correctness_rows_updated": options_updated,
                                       "explanation_letter_references_updated": explanations_updated, "records": findings}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    REPORT_MD.write_text("\n".join(body)+"\n", encoding="utf-8")


def apply(db, data):
    live_records, by_key = collect_live(db)
    findings = verify_preconditions(data, live_records, by_key)
    updates = 0
    explanation_updates = 0
    for item, finding in zip(data, findings):
        row, audit = item["row"], item["audit"]
        question = by_key[row["image_url"]][0]
        locked = db.scalar(select(Question).where(Question.id == question.id, Question.chapter_id == CHAPTER_ID).with_for_update())
        locked_options = db.scalars(select(QuestionOption).where(QuestionOption.question_id == question.id).order_by(QuestionOption.option_key).with_for_update()).all()
        if locked is None or {x.option_key: x.option_text for x in locked_options} != row["options"]:
            raise RuntimeError(f"Lock/precondition failed for {audit['question_id']}")
        current = {x.option_key: x for x in locked_options}
        for key in LETTERS:
            option = current[key]
            should_be_correct = key == row["correct_option"]
            if option.is_correct == should_be_correct:
                continue
            result = db.execute(update(QuestionOption).where(
                QuestionOption.id == option.id, QuestionOption.question_id == question.id,
                QuestionOption.option_key == key, QuestionOption.option_text == row["options"][key],
                QuestionOption.is_correct.is_(not should_be_correct),
            ).values(is_correct=should_be_correct))
            if result.rowcount != 1:
                raise RuntimeError(f"Option correctness precondition failed for {audit['question_id']}:{key}")
            updates += 1
        if locked.explanation != row["explanation"]:
            if locked.explanation != item["old_explanation"]:
                raise RuntimeError(f"Explanation precondition failed for {audit['question_id']}")
            result = db.execute(update(Question).where(
                Question.id == locked.id, Question.chapter_id == CHAPTER_ID, Question.image_url == row["image_url"],
                Question.question_text == row["question_text"], Question.explanation == item["old_explanation"],
                Question.difficulty == locked.difficulty, Question.is_active.is_(True), Question.is_pyq.is_(False),
            ).values(explanation=row["explanation"]))
            if result.rowcount != 1:
                raise RuntimeError(f"Explanation reference precondition failed for {audit['question_id']}")
            explanation_updates += 1
        db.flush()
    return findings, updates, explanation_updates


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply",action="store_true",help="Apply the preconditioned CH-17 option-key correction")
    args=parser.parse_args(argv)
    logging.getLogger("sqlalchemy.engine").disabled = True
    engine.echo = False
    data, ledger = load_artifacts()
    if not args.apply:
        with SessionLocal() as db:
            live, by_key = collect_live(db)
            findings = verify_preconditions(data, live, by_key)
        print("ANSWER_POSITION_DRY_RUN", {"questions":len(findings),"key_changes":sum(x["old_correct"]!=x["new_correct"] for x in findings),
                                             "explanation_reference_changes":sum(x["old_explanation"]!=x["new_explanation"] for x in findings),
                                             "target_distribution":dict(Counter(r["row"]["correct_option"] for r in data)),"no_database_changes":True})
        return
    with SessionLocal.begin() as db:
        findings, flags_updated, explanations_updated = apply(db, data)
    with SessionLocal.begin() as db:
        live, by_key = collect_live(db)
        for item in data:
            row = item["row"]
            question = by_key[row["image_url"]][0]
            correct = [o.option_key for o in question.options if o.is_correct]
            if correct != [row["correct_option"]] or question.explanation != row["explanation"]:
                raise RuntimeError(f"Post-update verification failed for {row['image_url']}")
            audit = item["audit"]
            audit["database_reconciliation"]["final_classification"] = "exact_match"
            audit["database_reconciliation"]["initial_correct_option"] = item["old_correct"]
            audit["database_reconciliation"]["requested_correct_option"] = row["correct_option"]
            audit["answer_position_reconciliation"] = {"live_question_uuid": str(question.id), "old_correct_option": item["old_correct"],
                                                        "correct_option": row["correct_option"], "validation": "PASS — option multiset and answer state preserved"}
    LEDGER.write_text(json.dumps(ledger, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    write_report(findings, flags_updated, explanations_updated)
    print("ANSWER_POSITION_RECONCILIATION", {"option_correctness_rows_updated": flags_updated,
                                            "explanation_letter_references_updated": explanations_updated,
                                            "answer_distribution": dict(Counter(r["row"]["correct_option"] for r in data)),
                                            "verified_questions": len(data)})


if __name__ == "__main__":
    main()
