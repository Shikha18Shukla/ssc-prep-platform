"""Structure, provenance, independent calculations, and duplicate checks."""
import json, unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
BATCH=BASE/"data"/"coordinate_geometry_verified_batch.json"
LEDGER=BASE/"data"/"coordinate_geometry_answer_ledger.json"
def norm(s): return " ".join(unicodedata.normalize("NFKC",s).casefold().split())
def test_rows_align_with_ledger_and_mcq_invariants():
    rows=json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    ledger=json.loads(LEDGER.read_text(encoding="utf-8"))
    assert len(rows)==len(ledger)==90
    assert Counter(r["difficulty"] for r in rows)=={"EASY":30,"MEDIUM":30,"HARD":30}
    assert sum(r["source"]=="Original SSC-style practice question" for r in rows)==76
    assert sum(r["source"].startswith("Coordinate Geometry ") for r in rows)==14
    for i,(r,a) in enumerate(zip(rows,ledger),1):
        assert (r["subject_slug"],r["subcategory_slug"],r["chapter_slug"])==("maths","advanced-maths","coordinate-geometry")
        assert r["is_pyq"] is False and r.get("pyq_year") is None and r.get("pyq_exam_name") is None
        assert r["question_text"].strip() and r["explanation"].strip()
        assert set(r["options"])==set("ABCD") and len({norm(v) for v in r["options"].values()})==4
        assert r["correct_option"] in r["options"] and r["options"][r["correct_option"]]==a["expected_answer"]
        assert (a["row"],a["question"],a["difficulty"])==(i,r["question_text"],r["difficulty"])
        assert a["independent_reasoning"].strip() and a["source"]==r["source"]
        if r["source"]!="Original SSC-style practice question":
            assert ", PDF page " in r["source"] and "exam/year not stated" in r["source"]
def test_stems_have_no_exact_or_near_verbatim_duplicates():
    rows=json.loads(BATCH.read_text(encoding="utf-8"))["questions"]
    stems=[norm(r["question_text"]) for r in rows]
    assert len(set(stems))==90
    for i,s in enumerate(stems): assert all(SequenceMatcher(None,s,p).ratio()<.97 for p in stems[:i])
def test_independent_coordinate_calculations():
    rows={r["question_text"]:r for r in json.loads(BATCH.read_text(encoding="utf-8"))["questions"]}
    expected={
      "The distance between P(0,b) and Q(a,0) is:":"√(a²+b²)",
      "Find the reflection of (7,4) in the point (1,3).":"(−5,2)",
      "Find the perpendicular distance from (−3,4) to the line 3x+4y−5=0.":"2/5",
      "Find the area of the triangle with vertices (3,4), (−4,3), and (8,6).":"9/2",
      "Find the area of the quadrilateral with consecutive vertices (−4,5), (0,7), (5,−5), and (−4,−2).":"121/2",
      "For what value of k do x+3y+7=0 and 4x+ky+19=0 have no solution?":"12",
      "The lines 2x+y=10 and x−y=2 intersect at P. Find the distance from P to (1,−1).":"3√2",
      "Find the point on the x-axis equidistant from A(−2,3) and B(4,3).":"(1,0)",
      "A point P=(x,y) is equidistant from A(−1,2), B(5,2), and C(2,5). Find P.":"(2,2)",
    }
    for stem,answer in expected.items():
      r=rows[stem]; assert r["options"][r["correct_option"]]==answer
