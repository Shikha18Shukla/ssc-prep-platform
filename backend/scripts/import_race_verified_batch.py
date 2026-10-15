"""Validate, preview and idempotently import the reviewed Race bank."""
import argparse, json, re, sys, unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))
from sqlalchemy import select
from app.database.session import SessionLocal, engine
from app.models import Chapter, Exam, Question, Subject, Subcategory
from app.services.question_import_service import import_questions

BATCH = BASE / "data" / "race_verified_batch.json"
LEVELS = ("EASY", "MEDIUM", "HARD")
TARGET = {level: 30 for level in LEVELS}
PDF_SOURCE = "Verified from supplied Race PDF, page "
ORIGINAL_SOURCE = "Original SSC-style practice question"

def normalized(value): return " ".join(unicodedata.normalize("NFKC", value).casefold().split())
def number_masked(value):
    value = normalized(value)
    value = re.sub(r"\d[\d,]*(?:\.\d+)?%?", " <number> ", value)
    return " ".join(re.sub(r"[^a-z<> ]", " ", value).split())

def _check_stems(stems):
    for index, stem in enumerate(stems):
        for prior in stems[:index]:
            if normalized(stem) == normalized(prior): raise ValueError(f"Exact duplicate: {stem!r}")
            if number_masked(stem) == number_masked(prior): raise ValueError(f"Number-masked duplicate: {stem!r} / {prior!r}")
            if SequenceMatcher(None, normalized(stem), normalized(prior)).ratio() >= .92:
                raise ValueError(f"Near-duplicate wording: {stem!r} / {prior!r}")

def load_batch():
    payload = json.loads(BATCH.read_text(encoding="utf-8")); records = payload.get("questions") if isinstance(payload, dict) else None
    if not isinstance(records, list) or len(records) != 90: raise ValueError("Race batch must contain exactly 90 questions")
    if Counter(row.get("difficulty") for row in records if isinstance(row, dict)) != TARGET: raise ValueError("Race batch must have 30 per difficulty")
    required = {"subject_slug","subcategory_slug","chapter_slug","question_text","options","correct_option","explanation","difficulty","is_pyq","source"}
    pdf_rows = original_rows = 0; stems=[]
    for index,row in enumerate(records,1):
        if not isinstance(row,dict): raise ValueError(f"Row {index} must be an object")
        missing=required-set(row)
        if missing: raise ValueError(f"Row {index} missing {sorted(missing)}")
        if (row["subject_slug"],row["subcategory_slug"],row["chapter_slug"]) != ("maths","arithmetic-maths","race"): raise ValueError(f"Row {index} catalog mismatch")
        if row["difficulty"] not in LEVELS or row["is_pyq"] is not False: raise ValueError(f"Row {index} invalid difficulty/provenance")
        if row.get("pyq_year") is not None or row.get("pyq_exam_name") is not None: raise ValueError(f"Row {index} has PYQ metadata")
        source=row["source"]
        if source==ORIGINAL_SOURCE: original_rows+=1
        elif source.startswith(PDF_SOURCE) and "; exam/year not stated" in source:
            page=re.search(r"page (\d+);",source)
            if not page or int(page.group(1)) not in {2,3,4,5,7,8,9}: raise ValueError(f"Row {index} invalid PDF page")
            pdf_rows+=1
        else: raise ValueError(f"Row {index} unrecognized provenance {source!r}")
        if not row["question_text"].strip() or not row["explanation"].strip(): raise ValueError(f"Row {index} empty question/explanation")
        if len(source)>255: raise ValueError(f"Row {index} source too long")
        options=row["options"]
        if not isinstance(options,dict) or set(options)!=set("ABCD"): raise ValueError(f"Row {index} must have A-D options")
        vals=[options[k] for k in "ABCD"]
        if any(not isinstance(v,str) or not v.strip() for v in vals) or len({normalized(v) for v in vals})!=4: raise ValueError(f"Row {index} invalid options")
        if row["correct_option"] not in options: raise ValueError(f"Row {index} invalid key")
        stems.append(row["question_text"])
    if (pdf_rows,original_rows)!=(10,80): raise ValueError(f"Expected 10 PDF and 80 original, got {pdf_rows}/{original_rows}")
    _check_stems(stems); return records

def chapter_context(db):
    return db.execute(select(Exam,Subject,Subcategory,Chapter).join(Subject,Subject.exam_id==Exam.id).join(Subcategory,Subcategory.subject_id==Subject.id).join(Chapter,Chapter.subcategory_id==Subcategory.id).where(Exam.slug=="ssc",Exam.is_active.is_(True),Subject.slug=="maths",Subject.is_active.is_(True),Subcategory.slug=="arithmetic-maths",Subcategory.is_active.is_(True),Chapter.slug=="race",Chapter.is_active.is_(True))).one_or_none()
def counts(rows):
    out=Counter()
    for q in rows: out[(q.difficulty.value,"PYQ" if q.is_pyq else "ordinary","active" if q.is_active else "inactive")]+=1
    return out
def print_counts(label,c):
    print(label)
    for lev in LEVELS: print(lev,{f"{state}_{kind}":c[(lev,kind,state)] for state in ("active","inactive") for kind in ("ordinary","PYQ")})
def options_and_answer(q):
    opts={o.option_key:o.option_text for o in q.options}; return opts,next((o.option_key for o in q.options if o.is_correct),None)
def plan_missing(records,existing):
    bykey={normalized(r["question_text"]):r for r in records}; known={}; active=Counter()
    for q in existing:
        key=normalized(q.question_text)
        if key in known: raise ValueError(f"Existing Race exact duplicate: {q.question_text!r}")
        known[key]=q; expected=bykey.get(key)
        if expected:
            opts,answer=options_and_answer(q)
            if (opts!=expected["options"] or answer!=expected["correct_option"] or q.difficulty.value!=expected["difficulty"] or q.is_pyq or not q.is_active): raise ValueError(f"Existing exact match conflicts: {q.question_text!r}")
        if q.is_active and not q.is_pyq: active[q.difficulty.value]+=1
    for row in records:
        for q in existing:
            if normalized(row["question_text"])==normalized(q.question_text): continue
            if number_masked(row["question_text"])==number_masked(q.question_text): raise ValueError(f"Number-masked duplicate against existing: {row['question_text']!r}")
            if SequenceMatcher(None,normalized(row["question_text"]),normalized(q.question_text)).ratio()>=.92: raise ValueError(f"Near duplicate against existing: {row['question_text']!r}")
    deficits={lev:30-active[lev] for lev in LEVELS}
    if any(n<0 for n in deficits.values()): raise ValueError("Existing active ordinary counts exceed targets; preserving rows")
    selected=[]
    for row in records:
        key=normalized(row["question_text"]); lev=row["difficulty"]
        if key in known or deficits[lev]==0: continue
        selected.append(row); known[key]=True; deficits[lev]-=1
    if any(deficits.values()): raise ValueError(f"Batch cannot fill deficits: {deficits}")
    return selected

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument("--dry-run",action="store_true"); args=parser.parse_args(argv)
    engine.echo=False; records=load_batch(); print("BATCH",len(records),dict(Counter(r["difficulty"] for r in records))); print("PROVENANCE",{"verified_pdf":sum(r["source"].startswith(PDF_SOURCE) for r in records),"original":sum(r["source"]==ORIGINAL_SOURCE for r in records)})
    with SessionLocal() as db:
        context=chapter_context(db)
        if context is None: raise SystemExit("Active SSC -> Maths -> Arithmetic Maths -> Race chapter not found uniquely")
        _,_,category,chapter=context; existing=db.scalars(select(Question).where(Question.chapter_id==chapter.id)).all(); before=counts(existing)
        print("CHAPTER",chapter.id,chapter.name,chapter.slug); print("SUBCATEGORY",category.id,category.name,category.slug); print_counts("BEFORE",before)
        try: selected=plan_missing(records,existing)
        except ValueError as exc: raise SystemExit(str(exc)) from exc
        print("PLANNED_INSERTS",len(selected),dict(Counter(r["difficulty"] for r in selected)))
        if not selected: print("NOOP: active ordinary targets met; zero inserts"); return
        preview=import_questions(db,json.dumps({"questions":selected},ensure_ascii=False).encode(),"application/json",BATCH.name,True); print("DRY_RUN",preview.model_dump())
        if preview.aborted or preview.errors or preview.would_import!=len(selected) or preview.duplicates: raise SystemExit("Importer dry-run did not approve every planned insert")
        if args.dry_run: print("NO_DATABASE_CHANGES"); return
        result=import_questions(db,json.dumps({"questions":selected},ensure_ascii=False).encode(),"application/json",BATCH.name,False); print("IMPORT",result.model_dump())
        if result.aborted or result.errors or result.imported!=len(selected): raise SystemExit("Import did not match dry run")
        afterrows=db.scalars(select(Question).where(Question.chapter_id==chapter.id)).all(); after=counts(afterrows); print_counts("AFTER",after)
        if any(after[(lev,"ordinary","active")]!=30 for lev in LEVELS): raise SystemExit("Post-import ordinary counts differ from target")
        print("POST_IMPORT_COUNTS_VERIFIED",len(afterrows))
if __name__=="__main__": main()
