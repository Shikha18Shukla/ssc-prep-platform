"""Safely dry-run or apply the verified CH-17 visual question bank."""
from __future__ import annotations

import argparse
import json
import sys
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE))
from sqlalchemy import select
from app.database.session import SessionLocal,engine
from app.models import Chapter,Exam,Question,Subject
from app.services.question_import_service import import_questions

BATCH=BASE/"data"/"non_verbal_reasoning_verified_batch.json"
LEDGER=BASE/"data"/"non_verbal_reasoning_answer_ledger.json"
CHAPTER_ID="746c8d03-3645-4454-a875-7cd9109e133a"
LEVELS=Counter({"EASY":11,"MEDIUM":11,"HARD":11})
LETTERS=set("ABCD")

def norm(s): return " ".join(unicodedata.normalize("NFKC",s).casefold().split())

def load_and_validate():
    rows=json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    ledger=json.loads(LEDGER.read_text(encoding="utf-8"))
    selected=[x for x in ledger if x.get("record_type")=="selected_question"]
    if len(rows)!=33 or len(selected)!=33 or Counter(x["difficulty"] for x in rows)!=LEVELS:
        raise ValueError("Expected 33 aligned questions and 11 at each difficulty")
    if (len([x for x in ledger if x.get("record_type")=="rejected_source_prompt"])!=55):
        raise ValueError("Expected source-candidate rejections to remain documented")
    stems=set(); signatures=set(); asset_root=BASE.parent/"frontend"/"public"
    for i,(row,audit) in enumerate(zip(rows,selected),1):
        if (row.get("subject_slug"),row.get("subcategory_slug"),row.get("chapter_slug"))!=("reasoning",None,"non-verbal-reasoning"):
            raise ValueError(f"Row {i}: incorrect catalog metadata")
        if row.get("is_pyq") is not False or row.get("pyq_year") is not None or row.get("pyq_exam_name") is not None:
            raise ValueError(f"Row {i}: must be Normal, not PYQ")
        if row.get("difficulty") not in LEVELS or not row.get("question_text","").strip() or not row.get("explanation","").strip():
            raise ValueError(f"Row {i}: missing stem/explanation or invalid difficulty")
        opts=row.get("options")
        if not isinstance(opts,dict) or set(opts)!=LETTERS or len({norm(v) for v in opts.values()})!=4:
            raise ValueError(f"Row {i}: requires four distinct options A-D")
        key=row.get("correct_option")
        if key not in opts or audit.get("expected_answer")!=opts[key] or audit.get("correct_option")!=key:
            raise ValueError(f"Row {i}: answer and ledger disagree")
        if audit.get("difficulty")!=row["difficulty"] or audit.get("question")!=row["question_text"] or not audit.get("verification_method"):
            raise ValueError(f"Row {i}: incomplete or mismatched answer ledger")
        stem=norm(row["question_text"])
        if stem in stems: raise ValueError(f"Row {i}: duplicate question stem")
        stems.add(stem)
        sig=audit.get("concept_signature")
        if not sig or sig in signatures: raise ValueError(f"Row {i}: duplicate/missing concept signature")
        signatures.add(sig)
        image=row.get("image_url",""); parsed=urlsplit(image)
        if not image.startswith("/question-assets/non-verbal-reasoning/") or parsed.scheme or parsed.netloc or ".." in parsed.path.split("/"):
            raise ValueError(f"Row {i}: unsafe image URL")
        disk=asset_root/parsed.path.lstrip("/")
        if not disk.is_file(): raise ValueError(f"Row {i}: image asset missing: {disk}")
        root=ET.parse(disk).getroot()
        if not root.tag.endswith("svg"): raise ValueError(f"Row {i}: asset is not SVG")
        if audit.get("image_asset")!=image or audit.get("is_pyq") is not False:
            raise ValueError(f"Row {i}: image or PYQ metadata mismatches ledger")
    return rows

def context(db):
    return db.execute(select(Exam,Subject,Chapter).join(Subject,Subject.exam_id==Exam.id).join(Chapter,Chapter.subject_id==Subject.id).where(
        Exam.slug=="ssc",Exam.is_active.is_(True),Subject.slug=="reasoning",Subject.is_active.is_(True),
        Chapter.slug=="non-verbal-reasoning",Chapter.is_active.is_(True),Chapter.subcategory_id.is_(None))).one_or_none()

def existing_record_conflicts(row,q):
    options={o.option_key:o.option_text for o in q.options}; correct=[o.option_key for o in q.options if o.is_correct]
    differences=[]
    if q.question_text!=row["question_text"]: differences.append("question_text")
    if options!=row["options"]: differences.append("options")
    if correct!=[row["correct_option"]]: differences.append("correct_option")
    if q.explanation!=row["explanation"]: differences.append("explanation")
    if q.image_url!=row["image_url"]: differences.append("image_url")
    if q.difficulty.value!=row["difficulty"]: differences.append("difficulty")
    if not q.is_active: differences.append("active")
    if q.is_pyq: differences.append("is_pyq")
    category="same_question_answer_difficulty_mismatch" if differences==["difficulty"] else ("content_or_status_conflict" if differences else "exact_match")
    return category,differences

def verify_existing(rows,existing):
    by_stem={norm(r["question_text"]):r for r in rows}; seen=set(); conflicts=[]
    for q in existing:
        key=norm(q.question_text)
        if key not in by_stem or key in seen:
            conflicts.append({"live_id":str(q.id),"question_text":q.question_text,"classification":"unexpected_or_duplicate_live_record"})
            continue
        seen.add(key); row=by_stem[key]
        category,differences=existing_record_conflicts(row,q)
        if differences:
            conflicts.append({"live_id":str(q.id),"import_key":row["image_url"],"classification":category,"fields":differences,
                              "live_difficulty":q.difficulty.value,"canonical_difficulty":row["difficulty"]})
    missing=set(by_stem)-seen
    if missing and existing:
        conflicts.extend({"question_text":by_stem[key]["question_text"],"classification":"canonical_question_missing_from_live"} for key in sorted(missing))
    if conflicts:
        print("EXISTING_RECORD_CONFLICTS",json.dumps(conflicts,ensure_ascii=False))
        raise ValueError(f"Existing CH-17 records contain {len(conflicts)} conflict(s); none were skipped or overwritten")
    return seen

def duplicate_scan(db,chapter_id,rows):
    prior=db.scalars(select(Question.question_text).join(Chapter,Chapter.id==Question.chapter_id).join(Subject,Subject.id==Chapter.subject_id).where(Subject.slug=="reasoning",Question.chapter_id!=chapter_id)).all()
    stems=[norm(r["question_text"]) for r in rows]; matches=[]
    for old in prior:
        n=norm(old)
        for candidate in stems:
            if SequenceMatcher(None,n,candidate).ratio()>=.94: matches.append((old,candidate))
    if matches: raise ValueError(f"Cross-chapter exact/near stem duplicate review required: {matches[:3]!r}")
    return len(prior)

def canonical_batch_scan(rows):
    from difflib import SequenceMatcher
    candidates=[norm(r["question_text"]) for r in rows]; matches=[]; files=0
    # Canonical chapter banks use the existing backend/data/*_verified_batch.json convention.
    for path in BASE.joinpath("data").glob("*verified_batch.json"):
        if path==BATCH: continue
        try: parsed=json.loads(path.read_text(encoding="utf-8-sig"))
        except (OSError,json.JSONDecodeError): continue
        items=parsed.get("questions",[]) if isinstance(parsed,dict) else parsed
        if not isinstance(items,list): continue
        files+=1
        for prior_row in items:
            if not isinstance(prior_row,dict) or not isinstance(prior_row.get("question_text"),str): continue
            old=norm(prior_row["question_text"])
            for new in candidates:
                matcher=SequenceMatcher(None,old,new,autojunk=True)
                if matcher.quick_ratio()<.94: continue
                ratio=matcher.ratio()
                if ratio>=.94: matches.append((path.name,prior_row["question_text"],new,round(ratio,3)))
    if matches: raise ValueError(f"Canonical question batch exact/near duplicate review required: {matches[:5]!r}")
    return files

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("--apply",action="store_true"); args=parser.parse_args(argv)
    engine.echo=False; rows=load_and_validate(); print("BATCH",len(rows),dict(Counter(r["difficulty"] for r in rows)),"ASSETS",len(rows))
    print("CANONICAL_BATCH_FILES_SCANNED",canonical_batch_scan(rows))
    with SessionLocal() as db:
        found=context(db)
        if not found: raise SystemExit("Active SSC → Reasoning → Non-Verbal Reasoning chapter not found uniquely")
        _,_,chapter=found
        if str(chapter.id)!=CHAPTER_ID: raise SystemExit(f"Chapter ID mismatch: {chapter.id}")
        existing=db.scalars(select(Question).where(Question.chapter_id==chapter.id)).all()
        print("CHAPTER",chapter.id,"BASELINE",len(existing)); verify_existing(rows,existing)
        if len(existing) not in (0,33): raise SystemExit("Safe baseline must be empty or exact completed 33-question batch")
        scanned=duplicate_scan(db,chapter.id,rows); print("REASONING_RECORDS_SCANNED",scanned)
        payload=json.dumps({"questions":rows},ensure_ascii=False).encode()
        preview=import_questions(db,payload,"application/json",BATCH.name,True)
        print("DRY_RUN",preview.model_dump())
        if preview.aborted or preview.errors or preview.rejected or preview.duplicates!=len(existing) or preview.would_import!=33-len(existing):
            raise SystemExit("Importer dry-run did not match exact baseline")
        if not args.apply: print("NO_DATABASE_CHANGES"); return
        if len(existing)==33: print("IDEMPOTENT_REPLAY: zero inserts"); return
        if len(existing)!=0: raise SystemExit("Apply requires verified empty baseline")
        result=import_questions(db,payload,"application/json",BATCH.name,False); print("IMPORT",result.model_dump())
        if result.aborted or result.errors or result.rejected or result.imported!=33: raise SystemExit("Import result mismatch")
        after=db.scalars(select(Question).where(Question.chapter_id==chapter.id)).all(); verify_existing(rows,after)
        replay=import_questions(db,payload,"application/json",BATCH.name,True); print("REPLAY_DRY_RUN",replay.model_dump())
        if replay.aborted or replay.errors or replay.rejected or replay.would_import or replay.duplicates!=33: raise SystemExit("Replay is not idempotent")
        print("POST_IMPORT_VERIFIED",len(after))

if __name__=="__main__": main()
