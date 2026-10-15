import json, re, unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

BATCH=Path(__file__).resolve().parents[1]/"data"/"race_verified_batch.json"
EXPECTED=["17/3 m/s","35.2 km/h","11 m/s","256 m","15 km/h","130 seconds","15 hours","120 seconds","5","2 m/s","5 m/s","6.25 m/s","53 1/3 seconds","275 m","25 m","4 seconds","30 km/h","3 km","100 m","11 1/9 m","18 km/h","9 m/s","12 km/h","1 1/9 m","5 minutes","50 m","18 km/h","8 m/s","160 m","6 m/s","15 km/h","80 m","8 1/3 m/s","20 seconds","83 1/3 m","270 m","10 seconds","18 km/h","180/29 m/s","114 m","5.4 m/s","250 seconds","50 seconds","87 m","100 seconds","10 m/s","40 seconds","150 seconds","8 8/9 m/s","48.75 m","B by 1 2/3 s","400 seconds","133 1/3 m","32 seconds","1000/129 m/s","5","1:1","9.6 m/s","33 1/3 m","7.5 seconds","They tie","B","150 m","228 m","B by 1 1/9 s","300 seconds","166 2/3 seconds","240 m","6 2/3 seconds","3","116 2/3 s","20/3 m/s","300 seconds","25:16","They tie","200 seconds","342 m","45 seconds","They tie","150 m","190 m","160 seconds","750 seconds","80/13 m/s","500 m","240 m","They tie","A by 25/19 s","1600 m","100 seconds"]
def norm(s): return " ".join(unicodedata.normalize("NFKC",s).casefold().split())
def mask(s):
 s=norm(s); s=re.sub(r"\d[\d,]*(?:\.\d+)?%?"," <n> ",s); return " ".join(re.sub(r"[^a-z<> ]"," ",s).split())
def test_schema_sources_distribution_and_independently_checked_answers():
 rows=json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
 assert len(rows)==len(EXPECTED)==90
 assert Counter(r["difficulty"] for r in rows)=={"EASY":30,"MEDIUM":30,"HARD":30}
 pdf=[r for r in rows if r["source"].startswith("Verified from supplied Race PDF")]
 assert len(pdf)==10 and sum(r["source"]=="Original SSC-style practice question" for r in rows)==80
 for i,r in enumerate(rows):
  assert (r["subject_slug"],r["subcategory_slug"],r["chapter_slug"])==("maths","arithmetic-maths","race")
  assert r["is_pyq"] is False and r.get("pyq_year") is None and r.get("pyq_exam_name") is None
  assert r["question_text"].strip() and r["explanation"].strip()
  assert set(r["options"])==set("ABCD") and len({norm(v) for v in r["options"].values()})==4
  assert r["options"][r["correct_option"]]==EXPECTED[i],r["question_text"]
  assert sum(v==EXPECTED[i] for v in r["options"].values())==1
def test_exact_number_masked_and_lexical_duplicate_review():
 stems=[r["question_text"] for r in json.loads(BATCH.read_text(encoding="utf-8"))["questions"]]
 assert len(set(map(norm,stems)))==90
 for i,s in enumerate(stems):
  for p in stems[:i]:
   assert mask(s)!=mask(p),f"number-masked duplicate: {s!r} / {p!r}"
   assert SequenceMatcher(None,norm(s),norm(p)).ratio()<.92,f"lexical duplicate: {s!r} / {p!r}"
