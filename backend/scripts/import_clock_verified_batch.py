"""Validate and safely import the reviewed Clock Normal bank."""
import argparse
import json
import sys
import unicodedata
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))
from sqlalchemy import select
from app.database.session import SessionLocal, engine
from app.models import Chapter, Exam, Question, Subject
from app.services.question_import_service import import_questions

BATCH = BASE / "data" / "clock_verified_batch.json"
LEDGER = BASE / "data" / "clock_answer_ledger.json"
EXPECTED_CHAPTER_ID = "43e38225-b6f7-4fd0-a35b-cf2a75a86f7d"
ORIGINAL = "Original SSC-style practice question"

def norm(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())

def verify_existing(rows, existing):
    expected={norm(row["question_text"]):row for row in rows}; seen=set()
    for q in existing:
        stem=norm(q.question_text)
        if stem in seen or stem not in expected: raise ValueError("Unexpected or duplicate existing Clock question")
        seen.add(stem); row=expected[stem]
        options={o.option_key:o.option_text for o in q.options}; correct=[o.option_key for o in q.options if o.is_correct]
        if (q.question_text!=row["question_text"] or q.explanation!=row["explanation"] or q.difficulty.value!=row["difficulty"] or q.is_pyq is not False or q.pyq_year is not None or q.pyq_exam_name is not None or q.source!=row["source"] or not q.is_active or options!=row["options"] or correct!=[row["correct_option"]]):
            raise ValueError("Existing Clock question conflicts with the canonical batch")

def load_artifacts():
    rows = json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    audits = json.loads(LEDGER.read_text(encoding="utf-8"))
    if len(rows) != len(audits) or len(rows) < 30:
        raise ValueError("Clock batch and ledger must align and contain at least 30 records")
    counts = Counter(row["difficulty"] for row in rows)
    if any(counts[level] < 10 for level in ("EASY", "MEDIUM", "HARD")):
        raise ValueError(f"Each difficulty requires at least 10 questions: {counts}")
    stems, signatures = set(), set()
    for i, (row, audit) in enumerate(zip(rows, audits), 1):
        if (row.get("subject_slug"), row.get("subcategory_slug"), row.get("chapter_slug")) != ("reasoning", None, "clock-recorded"):
            raise ValueError(f"Row {i}: incorrect catalog metadata")
        if row.get("is_pyq") is not False or row.get("pyq_year") is not None or row.get("pyq_exam_name") is not None:
            raise ValueError(f"Row {i}: invalid Normal/PYQ metadata")
        if row.get("difficulty") not in {"EASY", "MEDIUM", "HARD"} or not row.get("question_text", "").strip() or not row.get("explanation", "").strip():
            raise ValueError(f"Row {i}: missing stem/explanation or invalid difficulty")
        opts = row.get("options", {})
        if set(opts) != set("ABCD") or len({norm(v) for v in opts.values()}) != 4 or row.get("correct_option") not in opts:
            raise ValueError(f"Row {i}: invalid four-option answer set")
        if len(row["source"]) > 255:
            raise ValueError(f"Row {i}: provenance too long")
        stem = norm(row["question_text"])
        if stem in stems: raise ValueError(f"Repeated stem at row {i}")
        stems.add(stem)
        if audit.get("question_id") != f"clock-{i:03}" or audit.get("question") != row["question_text"] or audit.get("expected_answer") != opts[row["correct_option"]] or audit.get("source") != row["source"] or audit.get("difficulty") != row["difficulty"]:
            raise ValueError(f"Row {i}: ledger mismatch")
        sig = audit.get("concept_signature")
        if not sig or sig in signatures or not audit.get("independent_reasoning") or not audit.get("option_review"):
            raise ValueError(f"Row {i}: missing/repeated reasoning signature or audit")
        signatures.add(sig)
        if row["source"] == ORIGINAL:
            if audit.get("source_type") != "original" or audit.get("source_pdf") is not None or audit.get("source_page") is not None: raise ValueError(f"Row {i}: invalid original provenance")
        elif audit.get("source_type") != "pdf-derived" or audit.get("source_pdf") not in row["source"] or not isinstance(audit.get("source_page"), int):
            raise ValueError(f"Row {i}: incomplete PDF provenance")
    return rows

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("--apply",action="store_true"); args=parser.parse_args(argv)
    engine.echo=False; rows=load_artifacts(); print("BATCH",len(rows),dict(Counter(r["difficulty"] for r in rows)))
    with SessionLocal() as db:
        context=db.execute(select(Exam,Subject,Chapter).join(Subject,Subject.exam_id==Exam.id).join(Chapter,Chapter.subject_id==Subject.id).where(Exam.slug=="ssc",Exam.is_active.is_(True),Subject.slug=="reasoning",Subject.is_active.is_(True),Chapter.slug=="clock-recorded",Chapter.is_active.is_(True),Chapter.subcategory_id.is_(None))).one_or_none()
        if context is None: raise SystemExit("Active SSC → Reasoning → Clock (Recorded) chapter not found uniquely")
        _,_,chapter=context
        if str(chapter.id)!=EXPECTED_CHAPTER_ID: raise SystemExit(f"Clock chapter ID mismatch: {chapter.id}")
        existing=db.scalars(select(Question).where(Question.chapter_id==chapter.id)).all()
        normal=sum(q.is_active and not q.is_pyq for q in existing); pyq=sum(q.is_active and q.is_pyq for q in existing)
        print("CHAPTER",chapter.id,chapter.name); print("BEFORE",{"active_normal":normal,"active_pyq":pyq,"all_records":len(existing)})
        verify_existing(rows,existing)
        if (normal,pyq,len(existing)) not in {(0,0,0),(len(rows),0,len(rows))}: raise SystemExit("Clock baseline must be empty or the exact completed canonical bank")
        payload=json.dumps({"questions":rows},ensure_ascii=False).encode()
        preview=import_questions(db,payload,"application/json",BATCH.name,True); print("DRY_RUN",preview.model_dump())
        if preview.aborted or preview.errors or preview.rejected or preview.duplicates!=len(existing) or preview.would_import!=len(rows)-len(existing): raise SystemExit("Dry-run failed safety guards")
        if not args.apply: print("NO_DATABASE_CHANGES"); return
        if normal==len(rows): print("IDEMPOTENT_REPLAY: zero additional inserts"); return
        if normal or pyq or existing: raise SystemExit("Apply requires the exact verified empty Clock baseline")
        result=import_questions(db,payload,"application/json",BATCH.name,False); print("IMPORT",result.model_dump())
        if result.aborted or result.errors or result.rejected or result.duplicates or result.imported!=len(rows): raise SystemExit("Import results differ from expected clean insert")
        after=db.scalars(select(Question).where(Question.chapter_id==chapter.id)).all()
        if len(after)!=len(rows) or sum(q.is_active and not q.is_pyq for q in after)!=len(rows) or any(q.is_pyq for q in after): raise SystemExit("Post-import counts mismatch")
        verify_existing(rows,after)
        replay=import_questions(db,payload,"application/json",BATCH.name,True); print("REPLAY_DRY_RUN",replay.model_dump())
        if replay.aborted or replay.errors or replay.rejected or replay.would_import or replay.duplicates!=len(rows): raise SystemExit("Replay is not idempotent")
        print("AFTER",{"active_normal":len(rows),"active_pyq":0,"all_records":len(after)}); print("POST_IMPORT_VERIFIED")

if __name__=="__main__": main()
