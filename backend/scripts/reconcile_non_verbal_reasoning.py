"""Audit CH-17 canonical rows against live records; optionally reconcile difficulty only."""
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
from app.models import Difficulty, Question, QuestionOption

CHAPTER_ID = "746c8d03-3645-4454-a875-7cd9109e133a"
BATCH = BASE / "data" / "non_verbal_reasoning_verified_batch.json"
LEDGER = BASE / "data" / "non_verbal_reasoning_answer_ledger.json"
JSON_REPORT = BASE / "data" / "non_verbal_reasoning_reconciliation_report.json"
MD_REPORT = BASE / "data" / "non_verbal_reasoning_reconciliation_report.md"


def load_canonical():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    selected = [r for r in json.loads(LEDGER.read_text(encoding="utf-8")) if r.get("record_type") == "selected_question"]
    if len(rows) != 33 or len(selected) != 33:
        raise ValueError("Expected 33 canonical questions and 33 selected ledger entries")
    result = []
    for row, audit in zip(rows, selected):
        if row["image_url"] != audit["image_asset"] or row["question_text"] != audit["question"]:
            raise ValueError(f"Canonical / ledger key mismatch at row {audit.get('row')}")
        result.append({**row, "question_id": audit["question_id"], "ledger": audit})
    return result


def row_options(question):
    return {o.option_key: o.option_text for o in question.options}


def row_answer(question):
    correct = [o.option_key for o in question.options if o.is_correct]
    return correct[0] if len(correct) == 1 else None


def compare(canonical, live):
    """Return field-level comparisons and the required reconciliation class."""
    checks = {
        "question_text": (live.question_text, canonical["question_text"]),
        "options": (row_options(live), canonical["options"]),
        "correct_option": (row_answer(live), canonical["correct_option"]),
        "explanation": (live.explanation, canonical["explanation"]),
        "difficulty": (live.difficulty.value, canonical["difficulty"]),
        "chapter_id": (str(live.chapter_id), CHAPTER_ID),
        "active": (bool(live.is_active), True),
        "is_pyq": (bool(live.is_pyq), False),
    }
    differences = [k for k, (actual, expected) in checks.items() if actual != expected]
    content_fields = {"question_text", "options", "correct_option", "explanation", "chapter_id", "active", "is_pyq"}
    if not differences:
        category = "exact_match"
    elif set(differences) == {"difficulty"}:
        category = "same_question_answer_difficulty_mismatch"
    elif set(differences) & content_fields:
        category = "content_mismatch"
    else:
        category = "content_mismatch"
    return category, checks, differences


def snapshot(db):
    canonical = load_canonical()
    live = db.scalars(select(Question).where(Question.chapter_id == CHAPTER_ID).options(selectinload(Question.options))).all()
    by_asset: dict[str, list[Question]] = {}
    for q in live:
        if q.image_url:
            by_asset.setdefault(q.image_url, []).append(q)
    used: set[str] = set()
    entries = []
    counts = Counter()
    for row in canonical:
        matches = by_asset.get(row.get("image_url", ""), [])
        if len(matches) > 1:
            counts["ambiguous_match"] += 1
            entries.append({"question_id": row["question_id"], "import_key": row["image_url"], "classification": "ambiguous_match", "live_ids": [str(q.id) for q in matches]})
            continue
        if not matches:
            counts["missing_from_database"] += 1
            entries.append({"question_id": row["question_id"], "import_key": row["image_url"], "classification": "missing_from_database"})
            continue
        q = matches[0]
        used.add(str(q.id))
        category, checks, differences = compare(row, q)
        counts[category] += 1
        entries.append({
            "question_id": row["question_id"], "import_key": row["image_url"], "live_id": str(q.id),
            "classification": category, "differences": differences,
            "fields": {name: {"live": actual, "canonical": expected} for name, (actual, expected) in checks.items()},
        })
    extras = [q for q in live if str(q.id) not in used]
    for q in extras:
        counts["unexpected_extra_live_record"] += 1
    return {"chapter_id": CHAPTER_ID, "canonical_count": len(canonical), "live_count": len(live), "counts": dict(counts), "records": entries,
            "unexpected_extras": [{"live_id": str(q.id), "import_key": q.image_url, "question_text": q.question_text} for q in extras]}


def render_report(before, after, updated):
    lines = ["# CH-17 Canonical / Live Reconciliation", "", f"Chapter ID: `{CHAPTER_ID}`", "",
             "## Result", "", f"Difficulty-only updates applied: **{updated}**.",
             f"Final classifications: `{json.dumps(after['counts'], sort_keys=True)}`.",
             f"Canonical/live row counts: {after['canonical_count']} / {after['live_count']}.", "",
             "The stable import key is the local image path (`nvr-001.svg` … `nvr-033.svg`), paired with the ledger `question_id`. Matching also requires exact question text, four options, correct option, explanation, CH-17 chapter, active status, and Normal status. No fuzzy similarity authorized a write.", "",
             "## Root cause", "",
             "The live rows were created at 2026-11-03 16:29 local time; the canonical batch and ledger were rewritten at 16:38. The current builder assigns the intended balanced per-family levels in round-robin order (one Easy, Medium, Hard item per family). The rewrite changed 22 difficulty labels while leaving the question content unchanged. The answer ledger records the final intended levels; content/answer verification is separate from difficulty assignment.", "",
             "## Per-question comparison", "",
             "| Key | Live question UUID | Initial class | Initial difficulty | Canonical difficulty | Content/options/answer/explanation | Final class |", "|---|---|---|---|---|---|---|"]
    after_by_key = {r.get("import_key"): r for r in after["records"]}
    for old in before["records"]:
        final = after_by_key.get(old.get("import_key"), {})
        fields = old.get("fields", {})
        live_diff = fields.get("difficulty", {}).get("live", "—")
        can_diff = fields.get("difficulty", {}).get("canonical", "—")
        non_diff = set(old.get("differences", [])) - {"difficulty"}
        content_status = "exact" if not non_diff else ", ".join(sorted(non_diff))
        lines.append(f"| `{old.get('question_id','?')}` | `{old.get('live_id','—')}` | {old['classification']} | {live_diff} | {can_diff} | {content_status} | {final.get('classification','—')} |")
    lines += ["", "## Rejected source material / scope", "", "The 55 marked source candidates remain rejected. They were not promoted to source-derived questions. The 33 retained questions remain designated Original.", ""]
    JSON_REPORT.write_text(json.dumps({"before": before, "after": after, "difficulty_updates": updated}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    MD_REPORT.write_text("\n".join(lines), encoding="utf-8")


def apply_difficulty_only(db, before):
    rows = load_canonical()
    if before["canonical_count"] != 33 or before["live_count"] != 33:
        raise RuntimeError("Reconciliation requires exactly 33 canonical and 33 live CH-17 rows")
    cats = Counter(e["classification"] for e in before["records"])
    if set(cats) - {"exact_match", "same_question_answer_difficulty_mismatch"}:
        raise RuntimeError(f"Unsafe reconciliation classes present: {dict(cats)}")
    if cats["same_question_answer_difficulty_mismatch"] != 22:
        raise RuntimeError(f"Expected exactly 22 difficulty-only mismatches; found {cats['same_question_answer_difficulty_mismatch']}")
    canonical_by_key = {r["image_url"]: r for r in rows}
    update_ids = []
    for entry in before["records"]:
        if entry["classification"] != "same_question_answer_difficulty_mismatch":
            continue
        qid = entry["live_id"]
        q = db.scalar(select(Question).where(Question.id == qid, Question.chapter_id == CHAPTER_ID).options(selectinload(Question.options)).with_for_update())
        if q is None:
            raise RuntimeError(f"Precondition failed: row disappeared: {qid}")
        canonical = canonical_by_key[entry["import_key"]]
        category, _, _ = compare(canonical, q)
        if category != "same_question_answer_difficulty_mismatch":
            raise RuntimeError(f"Precondition failed: row changed while reconciling: {qid} ({category})")
        locked_options = db.scalars(select(QuestionOption).where(QuestionOption.question_id == q.id).order_by(QuestionOption.option_key).with_for_update()).all()
        locked_option_map = {o.option_key: o.option_text for o in locked_options}
        locked_correct = [o.option_key for o in locked_options if o.is_correct]
        if locked_option_map != canonical["options"] or locked_correct != [canonical["correct_option"]]:
            raise RuntimeError(f"Precondition failed: options or answer changed while reconciling: {qid}")
        expected_old = entry["fields"]["difficulty"]["live"]
        result = db.execute(update(Question).where(
            Question.id == q.id, Question.chapter_id == CHAPTER_ID, Question.image_url == canonical["image_url"],
            Question.question_text == canonical["question_text"], Question.explanation == canonical["explanation"],
            Question.difficulty == Difficulty[expected_old], Question.is_active.is_(True), Question.is_pyq.is_(False),
        ).values(difficulty=Difficulty[canonical["difficulty"]]))
        if result.rowcount != 1:
            raise RuntimeError(f"Conditional update precondition failed for {qid}")
        update_ids.append(qid)
    return len(update_ids)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply-verified-difficulty-reconciliation", action="store_true", help="Conditionally update only the 22 verified difficulty labels")
    args = parser.parse_args(argv)
    engine.echo = False
    logging.getLogger("sqlalchemy.engine").disabled = True
    if args.apply_verified_difficulty_reconciliation:
        with SessionLocal.begin() as db:
            before = snapshot(db)
            changed = apply_difficulty_only(db, before)
        with SessionLocal.begin() as db:
            after = snapshot(db)
        render_report(before, after, changed)
        print("RECONCILIATION_APPLIED", changed, "FINAL", after["counts"])
        if after["counts"] != {"exact_match": 33}:
            raise SystemExit("Post-update canonical/live verification failed")
    else:
        with SessionLocal() as db:
            before = snapshot(db)
        render_report(before, before, 0)
        print("RECONCILIATION_DRY_RUN", before["counts"], "REPORT", MD_REPORT.name)


if __name__ == "__main__":
    main()
