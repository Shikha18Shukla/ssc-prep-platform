"""Clock batch structure, provenance, answers and duplicate regression checks."""
import json
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
BATCH=BASE/"data/clock_verified_batch.json"
LEDGER=BASE/"data/clock_answer_ledger.json"
ORIGINAL="Original SSC-style practice question"
def norm(text): return " ".join(unicodedata.normalize("NFKC",text).casefold().split())
def records(): return json.loads(BATCH.read_text(encoding="utf-8"))["questions"],json.loads(LEDGER.read_text(encoding="utf-8"))

def test_batch_schema_metadata_answers_and_ledger():
    rows,ledger=records(); assert len(rows)==len(ledger)>=30
    counts=Counter(r["difficulty"] for r in rows); assert all(counts[x]>=10 for x in ("EASY","MEDIUM","HARD"))
    for i,(r,a) in enumerate(zip(rows,ledger),1):
        assert (r["subject_slug"],r["subcategory_slug"],r["chapter_slug"])==("reasoning",None,"clock-recorded")
        assert r["is_pyq"] is False and r["pyq_year"] is None and r["pyq_exam_name"] is None
        assert r["question_text"].strip() and r["explanation"].strip() and len(r["source"])<=255
        assert set(r["options"])==set("ABCD") and len({norm(v) for v in r["options"].values()})==4
        assert r["correct_option"] in r["options"] and a["expected_answer"]==r["options"][r["correct_option"]]
        assert a["question_id"]==f"clock-{i:03}" and a["question"]==r["question_text"] and a["source"]==r["source"]
        assert a["difficulty"]==r["difficulty"] and a["independent_reasoning"].strip() and a["option_review"].strip()
        if r["source"]==ORIGINAL: assert a["source_type"]=="original" and a["source_pdf"] is None and a["source_page"] is None
        else: assert a["source_type"]=="pdf-derived" and a["source_pdf"] in r["source"] and a["source_page"]>0

def test_no_exact_or_near_duplicates_within_batch_or_reasoning_corpus():
    rows,_=records(); stems=[norm(r["question_text"]) for r in rows]; assert len(set(stems))==len(stems)
    assert len({a["concept_signature"] for a in json.loads(LEDGER.read_text(encoding="utf-8"))})==len(rows)
    for i,s in enumerate(stems): assert all(SequenceMatcher(None,s,p).ratio()<0.97 for p in stems[:i])
    paths=list((BASE/"data").glob("*.json"))+[BASE.parent/"maximum_and_minimum_value_verified_batch.json"]
    for path in paths:
        if not path.exists(): continue
        if path in (BATCH,LEDGER): continue
        value=json.loads(path.read_text(encoding="utf-8")); others=value.get("questions",[]) if isinstance(value,dict) else []
        for other in others if isinstance(others,list) else []:
            if isinstance(other,dict) and isinstance(other.get("question_text"),str):
                candidate=norm(other["question_text"]); assert candidate not in set(stems),path.name
                if other.get("subject_slug")=="reasoning": assert all(SequenceMatcher(None,candidate,s).ratio()<0.97 for s in stems),path.name

def test_selected_calculations():
    rows,_=records(); keyed={r["question_text"]:r["options"][r["correct_option"]] for r in rows}
    assert keyed["How many degrees does the minute hand move in 30 seconds?"]=="3°"
    assert keyed["At 9:15, what is the smaller angle between the hands?"]=="172.5°"
    assert keyed["Between 9 and 10, when do the hands overlap?"]=="9:49 1/11"
    assert keyed["A clock is correct at 8:00 a.m. It gains 5 minutes every 2 hours. What actual time is it when the clock shows 10:30 a.m.?"]=="10:24 a.m."
