import json, re, unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

BATCH=Path(__file__).resolve().parents[1]/"data"/"race_verified_batch.json"
DATA=BATCH.parent
EXPECTED=["17/3 m/s","35.2 km/h","11 m/s","256 m","15 km/h","130 seconds","15 hours","120 seconds","5","2 m/s","5 m/s","6.25 m/s","53 1/3 seconds","275 m","25 m","4 seconds","30 km/h","3 km","100 m","11 1/9 m","18 km/h","9 m/s","12 km/h","1 1/9 m","5 minutes","50 m","18 km/h","8 m/s","160 m","6 m/s","15 km/h","80 m","8 1/3 m/s","20 seconds","83 1/3 m","270 m","10 seconds","18 km/h","180/29 m/s","114 m","5.4 m/s","250 seconds","50 seconds","87 m","100 seconds","10 m/s","40 seconds","150 seconds","8 8/9 m/s","48.75 m","B by 1 2/3 s","400 seconds","133 1/3 m","32 seconds","1000/129 m/s","5","1:1","9.6 m/s","33 1/3 m","7.5 seconds","They tie","A","150 m","228 m","B by 1 1/9 s","300 seconds","166 2/3 seconds","240 m","6 2/3 seconds","3","116 2/3 s","20/3 m/s","300 seconds","25:16","They tie","200 seconds","342 m","45 seconds","They tie","150 m","190 m","160 seconds","750 seconds","80/13 m/s","500 m","240 m","They tie","A by 25/19 s","1600 m","100 seconds","10/19 m/s"]
def norm(s): return " ".join(unicodedata.normalize("NFKC",s).casefold().split())
def mask(s):
 s=norm(s); s=re.sub(r"\d[\d,]*(?:\.\d+)?%?"," <n> ",s); return " ".join(re.sub(r"[^a-z<> ]"," ",s).split())
def test_schema_sources_distribution_and_independently_checked_answers():
 rows=json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
 assert len(rows)==len(EXPECTED)==91
 assert Counter(r["difficulty"] for r in rows)=={"EASY":30,"MEDIUM":30,"HARD":31}
 pdf=[r for r in rows if r["source"].startswith("Verified from Race ")]
 assert len(pdf)==11 and sum(r["source"]=="Original SSC-style practice question" for r in rows)==80
 for i,r in enumerate(rows):
  assert (r["subject_slug"],r["subcategory_slug"],r["chapter_slug"])==("maths","arithmetic-maths","race")
  assert r["is_pyq"] is False and r.get("pyq_year") is None and r.get("pyq_exam_name") is None
  assert r["question_text"].strip() and r["explanation"].strip()
  assert set(r["options"])==set("ABCD") and len({norm(v) for v in r["options"].values()})==4
  assert r["options"][r["correct_option"]]==EXPECTED[i],r["question_text"]
  assert sum(v==EXPECTED[i] for v in r["options"].values())==1
 assert Counter(r["correct_option"] for r in rows)=={"A":23,"B":23,"C":22,"D":23}
 assert {r["source"].split(", page ")[0] for r in pdf}=={"Verified from Race 01_ Class Notes.pdf","Verified from Race 02_ Class Notes.pdf"}
def test_exact_number_masked_and_lexical_duplicate_review():
 stems=[r["question_text"] for r in json.loads(BATCH.read_text(encoding="utf-8"))["questions"]]
 assert len(set(map(norm,stems)))==91
 for i,s in enumerate(stems):
  for p in stems[:i]:
   assert mask(s)!=mask(p),f"number-masked duplicate: {s!r} / {p!r}"
   assert SequenceMatcher(None,norm(s),norm(p)).ratio()<.92,f"lexical duplicate: {s!r} / {p!r}"

def test_corrected_three_runner_answer_is_independently_supported():
 row=next(r for r in json.loads(BATCH.read_text(encoding="utf-8"))["questions"] if r["question_text"].startswith("Three competitors run a 600 m race"))
 # Use a common start-time origin: A=75 s, B=5+600/9 s, C=-10+600/7.5 s.
 finish={"A":600/8,"B":5+600/9,"C":-10+600/7.5}
 assert finish=={"A":75,"B":71.66666666666667,"C":70}
 assert row["options"][row["correct_option"]]=="A"
 assert "A finishes last" in row["explanation"]

def test_explanations_and_stems_match_the_stated_race_math():
 rows=json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
 chained=rows[0]
 assert chained["options"][chained["correct_option"]]=="17/3 m/s"
 assert "170/v=30" in chained["explanation"] and "v=17/3 m/s" in chained["explanation"]
 headstart=next(r for r in rows if r["question_text"].startswith("A runner gives a competitor a 20 m head start"))
 assert "competitor finish before the runner" in headstart["question_text"]
 assert "finishes 4 s earlier" in headstart["explanation"]
 distance=next(r for r in rows if r["question_text"].startswith("A runner moves at 6 m/s"))
 assert "How far does the runner travel" in distance["question_text"]
 assert distance["options"][distance["correct_option"]]=="270 m"
 staggered=next(r for r in rows if r["question_text"].startswith("A starts a 500 m race 2 seconds before B"))
 assert staggered["options"][staggered["correct_option"]]=="1000/129 m/s"
 assert "A starts 2 s earlier" in staggered["explanation"]
 circular=next(r for r in rows if r["question_text"].startswith("On a 1000 m track A and B"))
 assert "excluding their initial meeting" in circular["question_text"]
 assert "3×250=750 s" in circular["explanation"]
 source_speed=rows[-1]
 assert source_speed["source"]=="Verified from Race 01_ Class Notes.pdf, page 16; exam/year not stated"
 assert source_speed["options"][source_speed["correct_option"]]=="10/19 m/s"

def test_generated_ledger_and_source_review_are_reproducible_and_complete():
 import sys
 sys.path.insert(0,str(BATCH.parent.parent/"scripts"))
 from build_race_artifacts import render
 generated=render()
 for path,content in generated.items(): assert path.read_bytes()==content
 ledger=json.loads((DATA/"race_answer_ledger.json").read_text(encoding="utf-8"))
 review=json.loads((DATA/"race_source_review.json").read_text(encoding="utf-8"))
 assert len(ledger)==91 and [row["question_id"] for row in ledger]==[f"race-{n:03}" for n in range(1,92)]
 assert {row["category"] for row in ledger}=={"Linear Race","Circular Race"}
 assert len(review["pdfs_reviewed"][0]["pages_visually_reviewed"])==19
 assert len(review["pdfs_reviewed"][1]["pages_visually_reviewed"])==16
 assert len(review["accepted_candidates"])==11
 assert any(x["page"]==13 and "correct" in x["reason"] for x in review["rejected_candidates"])
