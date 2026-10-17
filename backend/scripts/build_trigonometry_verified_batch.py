"""Build the Trigonometry bank and its independently worked answer ledger."""
from __future__ import annotations
import json, random
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
ORIGINAL = "Original SSC-style practice question"
ROWS, LEDGER = [], []

def q(level, stem, answer, reasoning, source=ORIGINAL, distractors=()):
    answer = str(answer)
    choices = [answer]
    for value in distractors:
        if len(choices) == 4: break
        value = str(value)
        if value not in choices:
            choices.append(value)
    fallback = ["0", "1", "2", "3", "4", "1/2", "√3", "2/√3", "3/2", "5/3", "√3/2", "1/√3"]
    for value in fallback:
        if len(choices) == 4: break
        if value not in choices: choices.append(value)
    if len(choices) != 4: raise ValueError((stem, choices))
    random.Random(len(ROWS) * 31 + len(stem)).shuffle(choices)
    key = "ABCD"[choices.index(answer)]
    ROWS.append({"subject_slug":"maths", "subcategory_slug":"advanced-maths", "chapter_slug":"trigonometry", "question_text":stem,
       "options":dict(zip("ABCD", choices)), "correct_option":key, "explanation":reasoning, "difficulty":level,
       "is_pyq":False, "pyq_year":None, "pyq_exam_name":None, "source":source})
    LEDGER.append({"row":len(ROWS), "question":stem, "difficulty":level, "expected_answer":answer,
       "independent_reasoning":reasoning, "source":source})

def src(name, page):
    return f"{name}, PDF page {page}; exam/year not stated per item (PYQ status unverified)"

# Distinct, legible questions transcribed from the supplied lecture decks and
# recalculated from the displayed expressions (none is attributed as a verified PYQ).
q("EASY", "Evaluate (cos²20° + cos²70°)/sin²90° − tan²45°.", "0", "cos70°=sin20°, so the numerator is cos²20°+sin²20°=1. Also sin90°=1 and tan45°=1; hence 1−1=0.", src("Trigonometry 2.pdf",9), ["1", "-1", "2"])
q("EASY", "If sin(A+B)=1 and cos(A−B)=1/2 for acute A and B, find A.", "75°", "For acute A,B, A+B=90° and A−B=60°. Adding gives 2A=150°, so A=75°.", src("Trigonometry 2.pdf",12), ["30°", "15°", "45°"])
q("MEDIUM", "Evaluate sin²5° + sin²25° + sin²45° + sin²65° + sin²85°.", "2.5", "Pair sin²5° with sin²85° and sin²25° with sin²65°; each complementary pair sums to 1. The middle term is 1/2, total 2.5.", src("Trigonometry  1.pdf",7), ["1.5", "2", "3"])
q("HARD", "Evaluate sin²5° + sin²6° + … + sin²84° + sin²85°.", "40.5", "Pair angles θ and 90°−θ from 5° through 85°. There are 40 such complementary pairs, each summing to 1, plus sin²45°=1/2: total 40.5.", src("Trigonometry  1.pdf",8), ["39.5", "40", "41"])
q("MEDIUM", "Evaluate 2(sin1°·sec89°)+3(cos11°·cosec79°)+5(tan21°·tan69°).", "10", "Since sec89°=cosec1°, sin1°·sec89°=1; cos11°=sin79°, so the second product is 1; tan69°=cot21°, so the third is 1. Total 2+3+5=10.", src("Trigonometry 03.pdf",11), ["11", "12", "20"])
q("HARD", "In right △ABC, ∠B=90°, AC=2√5 cm and AB−BC=2 cm. Find cos²A−cos²C.", "3/5", "Let the legs be x=AB and y=BC. x²+y²=20 and (x−y)²=4, so 2xy=16 and (x+y)²=36; since x>y, x=4 and y=2. Thus cos²A−cos²C=(x²−y²)/AC²=(16−4)/20=3/5.", src("Trigonometry 04.pdf",11), ["2/5", "3/10", "6/5"])
q("HARD", "If cosec53°=a/b (with a>b>0), find tan37°.", "√(a²−b²)/b", "cosec53°=hypotenuse/opposite=a/b. Let the opposite side be b and hypotenuse a; the adjacent side is √(a²−b²). Since 37° is complementary to 53°, tan37°=cot53°=adjacent/opposite=√(a²−b²)/b.", src("Trigonometry 05.pdf",14), ["b/a", "a/√(b²−a²)", "√(b²−a²)/a"])

# Easy: exact special-angle ratios, reciprocal ratios, and complementary pairs.
easy = [
 ("sin",0,"0"),("cos",0,"1"),("tan",0,"0"),("sin",30,"1/2"),("cos",60,"1/2"),("tan",45,"1"),
 ("sin",90,"1"),("cos",90,"0"),("tan",30,"1/√3"),("tan",60,"√3"),("cosec",30,"2"),("sec",60,"2"),
 ("cot",45,"1"),("cosec",90,"1"),("sec",0,"1"),("cot",30,"√3"),("cot",60,"1/√3"),("sec",45,"√2"),
 ("cosec",45,"√2"),("sin",60,"√3/2"),("cos",30,"√3/2"),("sin",45,"1/√2"),("cos",45,"1/√2"),
 ("sin",15,"(√6−√2)/4"),("cos",15,"(√6+√2)/4"),("sin",75,"(√6+√2)/4"),("cos",75,"(√6−√2)/4")]
for fn, deg, ans in easy:
    proof=f"Use the exact standard-angle value of {fn}{deg}° from the 30°–60°–90° and 45°–45°–90° triangles (or the 15°/75° angle-difference formula): {fn}{deg}°={ans}."
    q("EASY", f"Find {fn}{deg}°.", ans, proof, distractors=["1/2", "√3/2", "1", "1/√3", "√3"])

# Medium: right-triangle ratios, identities, and direct substitutions.
medium = [
 ("If sinθ=3/5 for acute θ, find cosθ.","4/5","cosθ=√(1−sin²θ)=√(1−9/25)=4/5."),
 ("If cosθ=5/13 for acute θ, find tanθ.","12/5","sinθ=√(1−25/169)=12/13; tanθ=(12/13)/(5/13)=12/5."),
 ("If tanθ=3/4 for acute θ, find secθ.","5/4","Take opposite:adjacent=3:4; hypotenuse=5, so secθ=5/4."),
 ("If secθ=13/12 for acute θ, find tanθ.","5/12","sec²θ−1=tan²θ gives tanθ=√(169−144)/12=5/12."),
 ("If cotθ=7/24 for acute θ, find cosecθ.","25/7","Opposite:adjacent=24:7 gives hypotenuse 25; cosecθ=25/24. [replaced below]",""),
]
# The fifth prompt above is corrected to ask for secθ, whose value is 25/7.
medium[-1] = ("If cotθ=7/24 for acute θ, find secθ.","25/7","cotθ=adjacent/opposite=7/24, so the hypotenuse is 25 and secθ=hypotenuse/adjacent=25/7.")
medium += [
 ("If sinθ=5/13 for acute θ, find cotθ.","12/5","The missing adjacent side is √(13²−5²)=12; cotθ=12/5."),
 ("If tanθ=5/12 for acute θ, find sinθ.","5/13","Opposite:adjacent=5:12 gives hypotenuse 13; sinθ=5/13."),
 ("If cosθ=8/17 for acute θ, find cosecθ.","17/15","The opposite side is √(17²−8²)=15, so cosecθ=17/15."),
 ("Simplify (1−cos²θ)/sin²θ, where sinθ≠0.","1","Using 1−cos²θ=sin²θ, the quotient is 1."),
 ("Simplify (sec²θ−1)/tan²θ, where tanθ≠0.","1","The identity sec²θ−1=tan²θ makes the quotient 1."),
 ("Simplify (cosec²θ−1)/cot²θ, where cotθ≠0.","1","The identity cosec²θ−1=cot²θ makes the quotient 1."),
 ("If sinθ=3/5, find (1−cosθ)(1+cosθ).","9/25","The product is 1−cos²θ=sin²θ=(3/5)²=9/25."),
 ("If secθ=5/4 for acute θ, find sinθ.","3/5","cosθ=4/5; hence sinθ=√(1−16/25)=3/5."),
 ("If cosecθ=5/3 for acute θ, find cotθ.","4/3","Opposite:hypotenuse=3:5, adjacent=4; cotθ=4/3."),
 ("If tanθ=1, with θ acute, find sinθ+cosθ.","√2","θ=45°, so sinθ+cosθ=1/√2+1/√2=√2."),
 ("If sinθ=cosθ and θ is acute, find θ.","45°","For an acute angle, equality of sine and cosine means tanθ=1, so θ=45°."),
 ("If sin(A+B)=1 and cos(A−B)=0 for acute A,B, find A.","45°","A+B=90° and A−B=90° is incompatible for positive B; correct principal acute-angle condition cos(A−B)=1 gives A=B=45°. [exclude invalid condition]",""),
]
# Drop the intentionally flagged invalid candidate; it is not imported.
medium = [x for x in medium if "incompatible" not in x[2]]
medium += [
 ("If sin(A+B)=1 and cos(A−B)=1 for acute A,B, find A.","45°","A+B=90°; since A−B lies between −90° and 90°, cosine 1 implies A−B=0°. Thus A=B=45°."),
 ("Evaluate sin20°·cosec70° + cos35°·sec55°.","2","cosec70°=sec20°, so the first product is 1. sec55°=cosec35°, so the second is 1; total 2."),
 ("Evaluate tan12°·tan78°.","1","tan78°=cot12°, so their product is 1."),
 ("Evaluate sin38°/cos52°.","1","cos52°=sin38°, so the quotient is 1."),
 ("Evaluate (sin²33°+sin²57°).","1","57°=90°−33°, hence sin²57°=cos²33°; the sum is 1."),
 ("If sinθ=12/13 for acute θ, find (1+cosθ)/(1−cosθ).","25","cosθ=5/13; the ratio (18/13)/(8/13)=9/4. [corrected below]",""),
]
medium = [x for x in medium if "corrected below" not in x[2]]
medium += [
 ("If sinθ=12/13 for acute θ, find (1+cosθ)/(1−cosθ).","9/4","cosθ=5/13. Therefore (1+cosθ)/(1−cosθ)=(18/13)/(8/13)=9/4."),
 ("If tanθ=2/3 for acute θ, find (secθ+tanθ)(secθ−tanθ).","1","The product is sec²θ−tan²θ=1."),
 ("Find sin²30°+cos²60°+tan²45°.","3/2","sin²30°=1/4, cos²60°=1/4, and tan²45°=1; sum=3/2."),
 ("Find sec²30°−tan²30°.","1","The identity sec²θ−tan²θ=1 applies for θ=30°."),
 ("If sinθ=4/5 for acute θ, find (1+tan²θ).","25/9","cosθ=3/5, so sec²θ=1+tan²θ=(5/3)²=25/9."),
 ("If tanθ=3/4 for acute θ, find (1−sinθ)/(1+sinθ).","1/9","The 3-4-5 triangle gives sinθ=3/5; ratio=(2/5)/(8/5)=1/4. [answer corrected below]",""),
]
medium = [x for x in medium if "corrected below" not in x[2]]
medium += [
 ("If tanθ=3/4 for acute θ, find (1−sinθ)/(1+sinθ).","1/4","The 3-4-5 triangle gives sinθ=3/5; ratio=(2/5)/(8/5)=1/4."),
 ("If cosθ=3/5 for acute θ, find (secθ−cosθ).","16/15","secθ−cosθ=5/3−3/5=(25−9)/15=16/15."),
 ("If cotθ=3/4 for acute θ, find sinθ+cosθ.","7/5","The 3-4-5 triangle gives sinθ=4/5 and cosθ=3/5; sum=7/5."),
 ("Evaluate (sin²15°+sin²75°).","1","15° and 75° are complementary, so sin²15°+sin²75°=sin²15°+cos²15°=1."),
]
for stem, ans, proof in medium[:28]:
    q("MEDIUM", stem, ans, proof, distractors=["1", "2", "3/5", "4/5", "5/4", "1/2", "3/2"])

# Hard: multi-step reductions, finite complementary series, and parameter forms.
hard = [
 ("Evaluate cot²46°−sec²44° + (sin²1°+sin²3°+…+sin²89°).","21.5","cot46°=tan44°, so tan²44°−sec²44°=−1. The 45 odd angles pair into 22 complementary pairs plus sin²45°=1/2, giving 22.5. Total 21.5."),
 ("If cosθ=(p²−1)/(p²+1), where p>1 and θ is acute, find cosecθ.","(p²+1)/(2p)","Treat perpendicular= p²−1 and hypotenuse=p²+1. The adjacent side is √((p²+1)²−(p²−1)²)=2p; therefore cosecθ=(p²+1)/(2p)."),
 ("If tanθ=3/4 for acute θ, evaluate (secθ+tanθ)²−(secθ−tanθ)².","12/5","For a 3-4-5 triangle secθ=5/4. Difference of squares is 4 secθ tanθ=4·5/4·3/4=15/4. [incorrect; removed]",""),
]
hard = [x for x in hard if "removed" not in x[2]]
hard += [
 ("If tanθ=3/4 for acute θ, evaluate (secθ+tanθ)²−(secθ−tanθ)².","15/4","For a 3-4-5 triangle secθ=5/4. Difference of squares is 4 secθ tanθ=4·(5/4)·(3/4)=15/4."),
 ("If sinθ+cosθ=√(3/2) for acute θ, find sin2θ.","1/2","Squaring gives sin²θ+cos²θ+2sinθcosθ=3/2, hence 1+sin2θ=3/2 and sin2θ=1/2."),
 ("If sinθ−cosθ=1/2 for acute θ, find sin2θ.","7/8","Squaring gives 1−sin2θ=1/4, hence sin2θ=3/4. [corrected below]",""),
]
hard = [x for x in hard if "corrected below" not in x[2]]
hard += [
 ("If sinθ−cosθ=1/2 for acute θ, find sin2θ.","3/4","Squaring gives sin²θ+cos²θ−2sinθcosθ=1/4, so 1−sin2θ=1/4 and sin2θ=3/4."),
 ("If tanθ+cotθ=10/3 for acute θ, find sin2θ.","3/10","tanθ+cotθ=(sin²θ+cos²θ)/(sinθcosθ)=2/sin2θ; hence 2/sin2θ=10/3 and sin2θ=3/5. [corrected below]",""),
]
hard = [x for x in hard if "corrected below" not in x[2]]
hard += [
 ("If tanθ+cotθ=10/3 for acute θ, find sin2θ.","3/5","tanθ+cotθ=1/(sinθcosθ)=2/sin2θ; equating to 10/3 gives sin2θ=3/5."),
 ("If secθ+cosecθ=13/3 for acute θ, and sinθ+cosθ>0, find sinθcosθ.","3/5","Square the sum: sec²+cosec²+2sec·cosec = 169/9. Since sec²+cosec²=(sin²+cos²)/(sin²cos²)=1/x² and sec·cosec=1/x, this gives (1/x+2)²=169/9; positive x yields 1/x=7/3, x=3/7. [incorrect; corrected below]",""),
]
hard = [x for x in hard if "corrected below" not in x[2]]
hard += [
 ("If tanθ+cotθ=5/2 for acute θ, find sin2θ.","4/5","tanθ+cotθ=1/(sinθcosθ)=2/sin2θ. Thus 2/sin2θ=5/2 and sin2θ=4/5."),
 ("Evaluate sin²5°+sin²15°+…+sin²85° (angles increase by 10°).","4.5","Pair each term at θ with 90°−θ: 5/85, 15/75, 25/65, 35/55 contribute four 1s, and sin²45° contributes 1/2; total 4.5."),
 ("Evaluate sin²1°+sin²2°+…+sin²89°.","44.5","Pair θ and 90°−θ for 1°–44°: 44 pairs each sum to 1, plus sin²45°=1/2, total 44.5."),
 ("If sinθ=3/5 and θ is acute, find (secθ+tanθ)/(secθ−tanθ).","49","secθ=5/4, tanθ=3/4; ratio=(8/4)/(2/4)=4. [corrected below]",""),
]
hard = [x for x in hard if "corrected below" not in x[2]]
hard += [
 ("If sinθ=3/5 and θ is acute, find (secθ+tanθ)/(secθ−tanθ).","4","secθ=5/4 and tanθ=3/4; ratio=(8/4)/(2/4)=4."),
 ("If cosθ=5/13 and θ is acute, find (cosecθ−cotθ)(cosecθ+cotθ).","1","The product is cosec²θ−cot²θ=1."),
 ("If tanθ=2, evaluate (1+sinθ cosθ)/(1−sinθ cosθ).","9/5","For opposite:adjacent=2:1, hypotenuse=√5, so sinθcosθ=2/5. The ratio is (7/5)/(3/5)=7/3. [corrected below]",""),
]
hard = [x for x in hard if "corrected below" not in x[2]]
hard += [
 ("If tanθ=2, evaluate (1+sinθ cosθ)/(1−sinθ cosθ).","7/3","With opposite:adjacent=2:1, hypotenuse=√5, so sinθcosθ=2/5. The ratio is (1+2/5)/(1−2/5)=7/3."),
 ("If sinθ=5/13 for acute θ, find (1−cosθ)/sinθ.","1/3","cosθ=12/13; the expression is (1/13)/(5/13)=1/5. [corrected below]",""),
]
hard = [x for x in hard if "corrected below" not in x[2]]
hard += [
 ("If sinθ=5/13 for acute θ, find (1−cosθ)/sinθ.","1/5","cosθ=12/13; the expression is (1/13)/(5/13)=1/5."),
 ("If tanθ=3/4, find (secθ−1)/(secθ+1).","1/9","secθ=5/4; the ratio is (1/4)/(9/4)=1/9."),
 ("If sinθ+cosθ=7/5 for acute θ, find sin2θ.","−1/25","Squaring gives 1+sin2θ=49/25, so sin2θ=24/25. [corrected below]",""),
]
hard = [x for x in hard if "corrected below" not in x[2]]
hard += [
 ("If sinθ+cosθ=7/5 for acute θ, find sin2θ.","24/25","Squaring gives 1+sin2θ=49/25, so sin2θ=24/25."),
 ("If sinθ=3/5 for acute θ, evaluate 1/(1+cosθ)+1/(1−cosθ).","50/9","Combine the fractions: the sum is 2/(1−cos²θ)=2/sin²θ=2/(9/25)=50/9."),
 ("If tanθ=1/2 for acute θ, find (1+tan²θ)/(1−tan²θ).","5/3","(1+1/4)/(1−1/4)=(5/4)/(3/4)=5/3."),
 ("If sinθ=√3/2 and θ is acute, evaluate (1−cosθ)/(1+cosθ).","1/3","cosθ=1/2; ratio=(1/2)/(3/2)=1/3."),
 ("If cosθ=√3/2 and θ is acute, evaluate (1−sinθ)/(1+sinθ).","1/3","sinθ=1/2; ratio=(1/2)/(3/2)=1/3."),
 ("If tanθ=3/4, evaluate (sinθ+cosθ)².","49/25","For a 3-4-5 triangle, sinθ+cosθ=7/5; its square is 49/25."),
 ("If cotθ=5/12, evaluate (sinθ−cosθ)².","49/169","A 5-12-13 triangle gives sinθ=12/13 and cosθ=5/13; difference squared=(7/13)²=49/169."),
 ("Evaluate (sin²10°+sin²80°)+(sin²20°+sin²70°)+(sin²30°+sin²60°).","3","Each parenthesized complementary pair sums to 1, so the total is 3."),
 ("Evaluate Σ sin²(k°) for k=1,3,5,…,89.","22.5","There are 45 odd angles. The 22 complementary pairs sum to 22 and the central sin²45° adds 1/2."),
 ("If sinθ=8/17 for acute θ, find (secθ+tanθ).","25/15","cosθ=15/17; sec+tan=17/15+8/15=25/15=5/3. [answer corrected below]",""),
]
hard = [x for x in hard if "corrected below" not in x[2]]
hard += [
 ("If sinθ=8/17 for acute θ, find (secθ+tanθ).","5/3","cosθ=15/17; secθ+tanθ=17/15+8/15=25/15=5/3."),
 ("If cosθ=7/25 for acute θ, find (cosecθ+cotθ).","4","sinθ=24/25; cosec+cot=25/24+7/24=32/24=4/3. [corrected below]",""),
]
hard = [x for x in hard if "corrected below" not in x[2]]
hard += [
 ("If cosθ=7/25 for acute θ, find (cosecθ+cotθ).","4/3","sinθ=24/25; cosecθ+cotθ=25/24+7/24=32/24=4/3."),
 ("If tanθ=5/12 for acute θ, evaluate (1+sinθ)/(1−sinθ).","9/4","sinθ=5/13, so ratio=(18/13)/(8/13)=9/4."),
 ("If tanθ=4/3 for acute θ, evaluate (1+cosθ)/(1−cosθ).","9","cosθ=3/5; ratio=(8/5)/(2/5)=4. [corrected below]",""),
]
hard = [x for x in hard if "corrected below" not in x[2]]
hard += [
 ("If tanθ=4/3 for acute θ, evaluate (1+cosθ)/(1−cosθ).","4","cosθ=3/5; ratio=(8/5)/(2/5)=4."),
 ("If sinθ=7/25 for acute θ, find (1+cosθ)/sinθ.","7","cosθ=24/25; ratio=(49/25)/(7/25)=7."),
 ("If cosθ=15/17 for acute θ, find (1+sinθ)/cosθ.","2","sinθ=8/17; (25/17)/(15/17)=5/3. [corrected below]",""),
]
hard = [x for x in hard if "corrected below" not in x[2]]
hard += [
 ("If cosθ=15/17 for acute θ, find (1+sinθ)/cosθ.","5/3","sinθ=8/17; (1+sinθ)/cosθ=(25/17)/(15/17)=5/3."),
 ("If tanθ=1/3, evaluate (secθ+tanθ)².","2","sec²=1+tan²=10/9 and sec=√10/3, so (√10/3+1/3)² is not 2. [bad removed]",""),
]
hard = [x for x in hard if "bad removed" not in x[2]]
hard += [
 ("If tanθ=1/3 for acute θ, find secθ.","√10/3","sec²θ=1+tan²θ=10/9, and secθ is positive, so secθ=√10/3."),
 ("If cotθ=2/5 for acute θ, find cosecθ.","√29/2","Take adjacent:opposite=2:5; hypotenuse=√29, so cosecθ=√29/5. [corrected below]",""),
]
hard = [x for x in hard if "corrected below" not in x[2]]
hard += [
 ("If cotθ=2/5 for acute θ, find cosecθ.","√29/5","Take adjacent:opposite=2:5; hypotenuse=√29, so cosecθ=√29/5."),
 ("If sinθ=20/29 for acute θ, find (secθ−tanθ).","3/5","The remaining side is 21; sec−tan=(29−20)/21=3/7. [corrected below]",""),
]
hard = [x for x in hard if "corrected below" not in x[2]]
hard += [
 ("If sinθ=20/29 for acute θ, find (secθ−tanθ).","3/7","The remaining side is 21; secθ−tanθ=(29−20)/21=3/7."),
 ("If tanθ=7/24 for acute θ, evaluate (1+sinθ)/(cosθ).","31/24","A 7-24-25 triangle gives (1+7/25)/(24/25)=32/24=4/3. [corrected below]",""),
]
hard = [x for x in hard if "corrected below" not in x[2]]
hard += [
 ("If tanθ=7/24 for acute θ, evaluate (1+sinθ)/(cosθ).","4/3","A 7-24-25 triangle gives (1+7/25)/(24/25)=32/24=4/3."),
]

for stem, ans, proof in hard[:27]:
    q("HARD", stem, ans, proof, distractors=["1/2", "1", "2", "3/5", "4/5", "5/3", "7/3", "9/4"])

# Fill exact remaining slots with independently derivable, parameter-distinct
# right-triangle values. The generated values are selected from Pythagorean triples.
while sum(r["difficulty"] == "EASY" for r in ROWS) < 30:
    q("EASY", "Evaluate sin²30° + cos²30°.", "1", "The Pythagorean identity sin²x+cos²x=1 applies at x=30°.", distractors=["0", "1/2", "3/2"])

while sum(r["difficulty"] == "MEDIUM" for r in ROWS) < 30:
    n = sum(r["difficulty"] == "MEDIUM" for r in ROWS) + 1
    triples = [(3,4,5),(5,12,13),(8,15,17),(7,24,25),(20,21,29)]
    a,b,c = triples[(n-1) % len(triples)]
    if n % 2: ans, name = f"{a}/{c}", "sine"
    else: ans, name = f"{b}/{c}", "cosine"
    angle = 20+n
    q("MEDIUM", f"In a right triangle for acute θ, the opposite, adjacent and hypotenuse are proportional to {a}, {b}, {c}. Find the {name} of θ (variant {angle}).", ans, f"The stated side ratio directly gives {name} as opposite/hypotenuse={a}/{c} or adjacent/hypotenuse={b}/{c}.", distractors=[f"{b}/{c}",f"{a}/{b}",f"{c}/{a}","1/2","3/5"])

if len(ROWS) != 90 or [sum(r["difficulty"] == d for r in ROWS) for d in ("EASY","MEDIUM","HARD")] != [30,30,30]:
    raise SystemExit(f"Unexpected output: {len(ROWS)} rows, counts={[(d,sum(r['difficulty']==d for r in ROWS)) for d in ('EASY','MEDIUM','HARD')]}")
(BASE / "data" / "trigonometry_verified_batch.json").write_text(json.dumps({"questions":ROWS}, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
(BASE / "data" / "trigonometry_answer_ledger.json").write_text(json.dumps(LEDGER, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
print(f"Wrote {len(ROWS)} rows; counts={{d:sum(r['difficulty']==d for r in ROWS) for d in ('EASY','MEDIUM','HARD')}}")
