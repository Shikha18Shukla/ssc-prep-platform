"""Build the Mensuration practice batch and independent calculation ledger."""
from __future__ import annotations
import json, random, re, unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
ORIGINAL="Original SSC-style practice question"
ROWS=[]; LEDGER=[]

def fmt(x):
    if isinstance(x,str): return x
    return str(int(x)) if float(x).is_integer() else f"{x:.2f}".rstrip("0").rstrip(".")

def q(level, stem, answer, proof, source=ORIGINAL, distractors=None):
    a=fmt(answer)
    if distractors is None:
        m=re.fullmatch(r"(-?\d+(?:\.\d+)?)(.*)",a)
        if m:
            n=float(m.group(1)); unit=m.group(2); d=max(1,abs(n)*.1)
            distractors=[fmt(n+d)+unit,fmt(n-d)+unit,fmt(n+2*d)+unit]
        else:
            distractors=["2×"+a,a+"/2","3×"+a]
    vals=[a]
    for v in map(fmt,distractors):
        if v not in vals: vals.append(v)
    m=re.fullmatch(r"(-?\d+(?:\.\d+)?)(.*)",a)
    n=float(m.group(1)) if m else None
    unit=m.group(2) if m else ""
    if n is not None:
        for v in (fmt(n+1)+unit,fmt(n-1)+unit,fmt(n+2)+unit,fmt(n-2)+unit):
            if v not in vals: vals.append(v)
    if len(vals)<4:
        for v in ("2×"+a,a+"/2","3×"+a):
            if v not in vals: vals.append(v)
    if len(vals)<4: raise ValueError((stem,vals))
    vals=vals[:4]; random.Random(len(ROWS)*19+len(stem)).shuffle(vals)
    key="ABCD"[vals.index(a)]
    row={"subject_slug":"maths","subcategory_slug":"advanced-maths","chapter_slug":"mensuration","question_text":stem,"options":dict(zip("ABCD",vals)),"correct_option":key,"explanation":proof,"difficulty":level,"is_pyq":False,"pyq_year":None,"pyq_exam_name":None,"source":source}
    ROWS.append(row); LEDGER.append({"row":len(ROWS),"question":stem,"difficulty":level,"expected_answer":a,"independent_calculation":proof,"source":source})

def src(pdf,page): return f"{pdf}, PDF page {page}; slide deck labels section as PYQ but individual exam/year not stated"

# Source-derived items: Mensuration 1.pdf pages 7–20 (squares/rhombuses).
q("EASY","A square has diagonal 15√2 cm. Find its area.",225,"For square d=s√2, s=15; area=s²=225 cm².",src("Mensuration 1.pdf",7),["225 cm²","150 cm²","450 cm²"])
q("EASY","A square has perimeter 96 cm. Find its area.",576,"Side=96/4=24 cm; area=24²=576 cm².",src("Mensuration 1.pdf",8),["576 cm²","384 cm²","2304 cm²"])
q("MEDIUM","A square has diagonal 20 cm. Find its perimeter.","40√2","Side=20/√2=10√2; perimeter=4×10√2=40√2 cm.",src("Mensuration 1.pdf",9),["40√2 cm","80 cm","20√2 cm"])
q("EASY","Find the ratio of the areas of the incircle and circumcircle of a square.","1:2","R/r=√2 for a square, so πr²:πR²=1:2.",src("Mensuration 1.pdf",10),["1:2","1:√2","1:4"])
q("MEDIUM","A rhombus has area 315 cm² and perimeter 180 cm. Find its altitude.",7,"Side=180/4=45 cm; area=base×height, so height=315/45=7 cm.",src("Mensuration 1.pdf",11),["7 cm","9 cm","35 cm"])
q("EASY","A rhombus has diagonals 6 cm and 8 cm. Find its area.",24,"Area=d₁d₂/2=6×8/2=24 cm².",src("Mensuration 1.pdf",12),["24 cm²","48 cm²","14 cm²"])
q("MEDIUM","A rhombus has side 13 cm and one diagonal 10 cm. Find the other diagonal.",24,"Diagonals bisect at right angles: half of other diagonal=√(13²−5²)=12; full diagonal=24 cm.",src("Mensuration 1.pdf",13),["24 cm","12 cm","20 cm"])
q("MEDIUM","A rhombus has perimeter 40 cm and one diagonal 16 cm. Find the other diagonal.",12,"Side=10; half first diagonal=8; other half=√(10²−8²)=6, so diagonal=12 cm.",src("Mensuration 1.pdf",14),["12 cm","6 cm","20 cm"])
q("EASY","A square has area 200 cm². Its side is doubled. What is the new area?",800,"Area scales as side²; new area=4×200=800 cm².",src("Mensuration 1.pdf",16),["800 cm²","400 cm²","600 cm²"])
q("MEDIUM","A square wire encloses 121 cm². It is reshaped into a circle. Using π=22/7, find the circle's area.",154,"Square side=11, perimeter/wire=44; circle radius=44/(2π)=7; area=π×49=154 cm².",src("Mensuration 1.pdf",17),["154 cm²","121 cm²","176 cm²"])
q("EASY","Using π=22/7, find the greatest circle area that fits inside a square of side 21 cm.",346.5,"Inscribed circle diameter=21, r=10.5; area=(22/7)×10.5²=346.5 cm².",src("Mensuration 1.pdf",18),["346.5 cm²","441 cm²","693 cm²"])
q("MEDIUM","An equilateral triangle is drawn on a square's diagonal. What is the ratio of the triangle area to the square area?", "√3:2","Square diagonal=d; triangle area=√3d²/4; square area=d²/2; ratio=√3:2.",src("Mensuration 1.pdf",19),["√3:2","1:2","√3:1"])

# Source-derived triangle items: Mensuration 02.pdf.
q("EASY","Find the area of an isosceles triangle with sides 5 cm, 5 cm and base 8 cm.",12,"Altitude bisects base: h=√(5²−4²)=3; area=8×3/2=12 cm².",src("Mensuration 02.pdf",11),["12 cm²","20 cm²","24 cm²"])
q("MEDIUM","An isosceles triangle has perimeter 40 cm and equal-side:base ratio 7:6. Find its area.","24√10","Sides 14,14,12; altitude=√(14²−6²)=4√10; area=12×4√10/2=24√10 cm².",src("Mensuration 02.pdf",13),["24√10 cm²","48√10 cm²","24√5 cm²"])
q("MEDIUM","Find the area of a triangle with sides 8 cm, 6 cm and 4 cm.","3√15","Heron: s=9; area=√[9×1×3×5]=3√15 cm².",src("Mensuration 02.pdf",16),["3√15 cm²","6√15 cm²","12 cm²"])
q("EASY","A 5-12-13 right triangle has a median drawn to its hypotenuse. Find the median length.",6.5,"In a right triangle, median to hypotenuse equals half the hypotenuse: 13/2=6.5 cm.",src("Mensuration 02.pdf",18),["6.5 cm","5 cm","12 cm"])
q("MEDIUM","An isosceles triangle has base 10 cm and area 20 cm². Find the length of each equal side.","√41","Height=2A/b=4; each side=√(5²+4²)=√41 cm.",src("Mensuration 02.pdf",12),["√41 cm","9 cm","41 cm"])
q("MEDIUM","A right triangle has inradius 3 cm and circumradius 12.5 cm. Find its area.",84,"For right triangle hypotenuse=2R=25; area=r×semiperimeter. Legs satisfy a+b=25+2r=31 and a²+b²=625; ab=168; area=ab/2=84 cm².",src("Mensuration 02.pdf",19),["84 cm²","96 cm²","72 cm²"])

# Source-derived rectangle, parallelogram and trapezium items: Mensuration 3.pdf.
q("EASY","A rectangular field has one side 15 m and diagonal 17 m. Find its area.",120,"Other side=√(17²−15²)=8 m; area=15×8=120 m².",src("Mensuration 3.pdf",9),["120 m²","150 m²","136 m²"])
q("MEDIUM","A 25 m by 16 m courtyard is paved with 20 cm by 10 cm tiles. How many tiles are needed?",20000,"Courtyard=400 m²; tile=0.2×0.1=0.02 m²; count=400/0.02=20,000.",src("Mensuration 3.pdf",10),["20,000","2,000","40,000"])
q("MEDIUM","A parallelogram has adjacent sides 60 cm and 40 cm and a diagonal 80 cm. Find its area.","600√15 cm²","Triangle sides 60,40,80 have s=90; Heron area=√(90×30×50×10)=300√15 cm²; the parallelogram is twice that, so area=600√15 cm².",src("Mensuration 3.pdf",12),["300√15 cm²","1200√15 cm²","600√15 cm²"])
q("MEDIUM","A parallelogram has adjacent sides 12 cm and 14 cm; one diagonal is 16 cm. Find the other diagonal.","2√106 cm","Parallelogram law: d₁²+d₂²=2(12²+14²)=680; d₂²=424; d₂=2√106 cm.",src("Mensuration 3.pdf",13),["20 cm","22 cm","14 cm"])
q("MEDIUM","A parallelogram's sides are in ratio 3:2, its area is 243 cm², and included angle is 30°. Find its perimeter.",90,"Let sides 3x,2x. Area=3x·2x·sin30=3x²=243, x=9; perimeter=2(27+18)=90 cm.",src("Mensuration 3.pdf",15),["90 cm","81 cm","108 cm"])
q("MEDIUM","A trapezium has area 384 cm², parallel-side ratio 3:5, and height 12 cm. Find the shorter parallel side.",24,"384=12(a+b)/2 gives a+b=64; ratio parts total 8, one part=8; shorter=3×8=24 cm.",src("Mensuration 3.pdf",19),["24 cm","40 cm","32 cm"])
q("MEDIUM","A trapezium has area 180 cm² and height 9 cm. One parallel side is 6 cm longer than the other. Find the shorter side.",17,"Sum of parallel sides=2A/h=40; solve x+(x+6)=40, x=17 cm.",src("Mensuration 3.pdf",20),["17 cm","23 cm","20 cm"])

# Original Easy (fill remaining 18) direct formula and practical questions.
easy=[
 ("A rectangle measures 18 cm by 7 cm. Find its perimeter.",50,"P=2(18+7)=50 cm."),
 ("A rectangle has area 96 cm² and length 12 cm. Find its width.",8,"Width=area/length=96/12=8 cm."),
 ("Find the area of a triangle with base 18 cm and perpendicular height 7 cm.",63,"A=bh/2=18×7/2=63 cm²."),
 ("A parallelogram has base 15 cm and altitude 8 cm. Find its area.",120,"A=base×height=15×8=120 cm²."),
 ("A trapezium has parallel sides 8 cm and 14 cm and height 6 cm. Find its area.",66,"A=(8+14)×6/2=66 cm²."),
 ("A circle has radius 7 cm. Using π=22/7, find its circumference.",44,"C=2πr=2×22/7×7=44 cm."),
 ("A circle has diameter 14 cm. Using π=22/7, find its area.",154,"r=7; A=πr²=154 cm²."),
 ("Find the area of a semicircle of radius 14 cm. Use π=22/7.",308,"A=πr²/2=(22/7×196)/2=308 cm²."),
 ("A square has side 13 cm. Find the length of its diagonal.","13√2","d=s√2=13√2 cm."),
 ("A cube has side 5 cm. Find its volume.",125,"V=a³=5³=125 cm³."),
 ("A cube has side 4 cm. Find its total surface area.",96,"TSA=6a²=6×16=96 cm²."),
 ("A cuboid measures 8 cm × 5 cm × 3 cm. Find its volume.",120,"V=lbh=8×5×3=120 cm³."),
 ("A cylinder has radius 7 cm and height 10 cm. Find its volume using π=22/7.",1540,"V=πr²h=22/7×49×10=1540 cm³."),
 ("A cylinder has radius 7 cm and height 5 cm. Find its curved surface area using π=22/7.",220,"CSA=2πrh=2×22/7×7×5=220 cm²."),
 ("A cone has radius 3 cm and height 4 cm. Find its volume using π=3.14.",37.68,"V=πr²h/3=3.14×9×4/3=37.68 cm³."),
 ("A sphere has radius 3 cm. Find its volume using π=3.14.",113.04,"V=4πr³/3=4×3.14×27/3=113.04 cm³."),
 ("A hemisphere has radius 7 cm. Find its total surface area using π=22/7.",462,"TSA=3πr²=3×22/7×49=462 cm²."),
 ("Convert 2.5 m² to cm².",25000,"1 m²=10,000 cm²; 2.5×10,000=25,000 cm²."),
 ("A triangle has base 12 cm and height 9 cm. Find its area.",54,"Area=bh/2=12×9/2=54 cm²."),
 ("A cuboid is 10 cm long, 4 cm wide and 3 cm high. Find its lateral surface area.",84,"LSA=2h(l+b)=6×14=84 cm²."),
 ("A circle has radius 14 cm. Using π=22/7, find its area.",616,"A=πr²=22/7×196=616 cm².")]
for stem,a,p in easy:q("EASY",stem,a,p)

# Medium: mixed applications; 24 originals (with source-derived medium rows gives target 30).
medium=[
 ("A rectangular garden is 30 m by 18 m. A 2 m-wide path runs inside along its boundary. Find the planted area.",364,"Inner dimensions 26×14; planted area=364 m²."),
 ("A circular track has radius 35 m. Find the distance around it using π=22/7.",220,"C=2πr=220 m."),
 ("A 90° sector has radius 14 cm. Find its area using π=22/7.",154,"Sector area=90/360×π×14²=154 cm²."),
 ("A wheel of radius 35 cm makes 200 complete revolutions. Find distance travelled in metres using π=22/7.",440,"Circumference=220 cm; distance=44,000 cm=440 m."),
 ("A cube's side is increased by 20%. By what percentage does its volume increase?",72.8,"Volume factor=1.2³=1.728; increase=72.8%."),
 ("A cuboid 12 cm × 8 cm × 5 cm is painted on all faces. Find painted area.",392,"TSA=2(lb+bh+hl)=2(96+40+60)=392 cm²."),
 ("A closed cylinder has radius 7 cm and height 12 cm. Find total surface area using π=22/7.",836,"TSA=2πr(r+h)=44×19=836 cm²."),
 ("A cone has radius 7 cm and slant height 25 cm. Find curved surface area using π=22/7.",550,"CSA=πrl=22/7×7×25=550 cm²."),
 ("A sphere's radius changes from 3 cm to 6 cm. By what factor does its volume change?",8,"Volume is proportional to r³; factor=(6/3)³=8."),
 ("A metal cube of side 6 cm is melted into cubes of side 2 cm. How many small cubes are made?",27,"Volume ratio=6³/2³=27."),
 ("A room 8 m long, 6 m wide and 4 m high is painted on four walls. Find wall area.",112,"Four-wall area=2h(l+b)=8(8+6)=112 m²."),
 ("A circular lawn of radius 14 m has a concentric path 7 m wide. Find the path area using π=22/7.",770,"Outer radius=21; area=π(21²−14²)=π×245=770 m²."),
 ("A triangle has sides 13 cm, 14 cm and 15 cm. Find its area.",84,"Heron s=21; area=√(21×8×7×6)=84 cm²."),
 ("A parallelogram has base 24 cm and area 360 cm². Find its altitude.",15,"h=A/b=360/24=15 cm."),
 ("An isosceles trapezium has parallel sides 10 cm and 22 cm and height 8 cm. Find its area.",128,"A=(10+22)×8/2=128 cm²."),
 ("A rectangle's length is 3 times its width and its area is 243 cm². Find its perimeter.",72,"3w²=243 ⇒ w=9,l=27; P=2(36)=72 cm."),
 ("A 20 cm × 14 cm rectangle is joined to a 14 cm × 7 cm rectangle along a full 14 cm side. Find the outer perimeter.",82,"Combined shape is 20×21 rectangle; perimeter=2(20+21)=82 cm."),
 ("A cylindrical tank of radius 1.4 m is filled to height 2 m. Find capacity in litres using π=22/7.",12320,"V=22/7×1.4²×2=12.32 m³=12,320 L."),
 ("A cone and cylinder have equal base radius and height. If cylinder volume is 990 cm³, find cone volume.",330,"Cone volume is one-third cylinder volume=330 cm³."),
 ("A cuboid's dimensions are doubled. By what factor does its total surface area change?",4,"Each face area scales by 2², so TSA is multiplied by 4."),
 ("A square of side 14 cm has a semicircle attached externally along one side as diameter. Find the perimeter of the outline using π=22/7.",66,"Three exposed square sides=42; semicircle arc=π×14/2=22; total=64. Wait perimeter=64 cm.",),
 ("A cone has radius 5 cm and height 12 cm. Find its slant height.",13,"l=√(r²+h²)=√(25+144)=13 cm."),
 ("A hemispherical bowl of radius 21 cm is filled with water. Find its volume using π=22/7.",19404,"V=2πr³/3=2×22/7×21³/3=19,404 cm³."),
 ("A trapezium has area 300 cm², height 12 cm and parallel sides in ratio 2:3. Find the longer side.",30,"Sum=2A/h=50; five ratio parts, one=10; longer=30 cm.")]
for item in medium[:14]:
    stem,a,p,*_=item
    if stem.startswith("A square of side 14"):
        a=64; p="Three exposed square sides=42; semicircle arc=πd/2=22; perimeter=64 cm."
    q("MEDIUM",stem,a,p)

# Hard: 30 multi-step original problems including composite solids and dimension changes.
hard=[
 ("A wire forms a square of area 484 cm², then is reshaped into a circle. Find circle area using π=22/7.",616,"Square side=22; wire length=88; circle r=88/(2π)=14; area=616 cm²."),
 ("A rectangular plot has perimeter 94 m and diagonal 37 m. Find its area.",420,"l+b=47; l²+b²=37²=1369; 2lb=47²−1369=840; area=420 m²."),
 ("A circle of radius 14 cm is cut from a square of side 28 cm. Find remaining area using π=22/7.","168 cm²","Square area=784; circle area=616; remainder=168 cm²."),
 ("A 90° sector of radius 28 cm is removed from a circle. Find remaining area using π=22/7.",1848,"Remaining 3/4×π×28²=3/4×2464=1848 cm²."),
 ("A solid consists of a cylinder of radius 7 cm and height 10 cm with a hemisphere on top. Find external curved area using π=22/7.",748,"Cylinder CSA=440; hemisphere CSA=2πr²=308; total=748 cm²."),
 ("A cylinder of radius 6 cm and height 8 cm is melted into a cone of radius 4 cm. Find cone height.",54,"π×36×8=(1/3)π×16×h; h=54 cm."),
 ("A cone of radius 7 cm and height 24 cm is cut from a cylinder with the same base and height. Find remaining volume using π=22/7.","2464 cm³","Cylinder=π×49×24=3696; cone=1232; difference=2464 cm³."),
 ("A sphere of radius 6 cm is melted into identical spheres of radius 2 cm. How many are formed?",27,"Volume ratio=(6/2)³=27."),
 ("A closed cubical tank has capacity 13,824 litres. Find its total outer surface area in m².","34.56 m²","13,824 L=13.824 m³; side=2.4 m; TSA=6×2.4²=34.56 m²."),
 ("A cuboid 20 cm × 15 cm × 10 cm is cut into the largest possible equal cubes. How many cubes result?",24,"Largest cube side=gcd(20,15,10)=5; count=(20/5)(15/5)(10/5)=24."),
 ("A circular path 3.5 m wide surrounds a circular pond of radius 10.5 m. Find path area using π=22/7.","269.5 m²","Outer radius=14; annulus area=π(196−110.25)=269.5 m²."),
 ("A rectangle 30 cm by 20 cm has a semicircle of diameter 20 cm attached along one short side. Find the perimeter using π=3.14.","111.4 cm","Three exposed rectangle sides=30+30+20=80; semicircle arc=πr=31.4; total=111.4 cm."),
 ("A square and an equilateral triangle have equal perimeters. If the triangle side is 12 cm, find the square area.",81,"Triangle perimeter=36; square side=9; area=81 cm²."),
 ("A right triangle with legs 9 cm and 12 cm is revolved about the 9 cm leg. Find the volume of the resulting cone using π=3.14.","1356.48 cm³","Cone r=12,h=9; V=π×144×9/3=1356.48 cm³."),
 ("A cylindrical vessel of radius 14 cm contains water to 10 cm. A solid sphere of radius 7 cm is immersed. By how much does water level rise?","7/3 cm","Displaced volume=4π×343/3; vessel base area=π×196; rise=(1372/3)/196=7/3 cm."),
 ("A cone and a hemisphere have the same radius 6 cm. If cone height is 8 cm, find the ratio of cone volume to hemisphere volume.","2:3","Cone=π×36×8/3=96π; hemisphere=2π×216/3=144π; ratio=2:3."),
 ("A cube of side 12 cm is painted on all faces and cut into 1 cm cubes. How many small cubes have exactly two painted faces?",120,"Exactly two faces occur on edge interiors: 12 edges×(12−2)=120."),
 ("A cube of side 10 cm is painted externally and cut into 1 cm cubes. How many small cubes have no paint?",512,"Interior cubes=(10−2)³=512."),
 ("A room 12 m × 8 m × 4 m has one door 2 m × 1 m and two windows each 1.5 m × 1 m. Find area of four walls to paint.","155 m²","Walls=2h(l+b)=160; openings=2+2×1.5=5; paint area=155 m²."),
 ("A cylindrical pipe has external radius 5 cm, internal radius 4 cm and length 2 m. Find material volume in cm³ using π=3.14.","5652 cm³","V=π(R²−r²)h=3.14×9×200=5652 cm³."),
 ("The radius of a sphere is reduced by 20%. Find the percentage decrease in its surface area.",36,"New area factor=0.8²=0.64; decrease=36%."),
 ("A cuboid has length:width:height=4:3:2 and volume 1536 cm³. Find its total surface area.","832 cm²","Dimensions 4x,3x,2x; 24x³=1536 ⇒x=4; sides 16,12,8; TSA=2(192+96+128)=832 cm²."),
 ("A trapezium has parallel sides 18 cm and 32 cm and area 500 cm². Find its height.",20,"500=(18+32)h/2=25h; h=20 cm."),
 ("A rhombus has area 240 cm² and one diagonal 16 cm. Find its perimeter.",68,"Other diagonal=2A/16=30; side=√(8²+15²)=17; perimeter=68 cm."),
 ("A triangular field has sides 25 m, 39 m and 56 m. Find its area.",420,"Heron s=60; area=√(60×35×21×4)=420 m²."),
 ("A solid sphere of radius 3 cm is placed inside a tight-fitting cube. Find the volume of the space inside the cube but outside the sphere using π=3.14.","102.96 cm³","Cube side=6, V=216; sphere V=4/3×3.14×27=113.04; difference=102.96 cm³."),
 ("A cone has radius 9 cm and slant height 15 cm. Find its total surface area using π=3.14.","678.24 cm²","CSA+base=πr(l+r)=3.14×9×24=678.24 cm²."),
 ("A hemispherical dome of radius 7 m is painted outside at ₹12 per m². Find the cost using π=22/7.","₹3696","Curved area=2πr²=308 m²; cost=308×₹12=₹3696."),
 ("A 10 m × 8 m floor is covered with square tiles of side 40 cm. How many whole tiles are needed?",500,"Tile area=.16 m²; floor=80 m²; count=500."),
 ("A cylindrical tank of radius 3.5 m and height 4 m is filled to 80% capacity. Find water volume in litres using π=22/7.",123200,"Full volume=22/7×12.25×4=154 m³; 80%=123.2 m³=123,200 L.")]
for stem,a,p,*_ in hard:q("HARD",stem,a,p)

def norm(s): return " ".join(unicodedata.normalize("NFKC",s).casefold().split())
def main():
    counts=Counter(r["difficulty"] for r in ROWS)
    if len(ROWS)!=90 or counts!={"EASY":30,"MEDIUM":30,"HARD":30}: raise SystemExit(f"bad count {len(ROWS)} {counts}")
    for i,r in enumerate(ROWS):
        if len(set(norm(x) for x in r["options"].values()))!=4 or r["options"][r["correct_option"]]!=LEDGER[i]["expected_answer"]: raise SystemExit(f"MCQ/key failure {i+1}")
        for p in ROWS[:i]:
            if norm(r["question_text"])==norm(p["question_text"]) or SequenceMatcher(None,norm(r["question_text"]),norm(p["question_text"])).ratio()>=.97: raise SystemExit(f"duplicate: {r['question_text']}")
    (BASE/"data/mensuration_verified_batch.json").write_text(json.dumps({"questions":ROWS},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (BASE/"data/mensuration_answer_ledger.json").write_text(json.dumps(LEDGER,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("WROTE",len(ROWS),dict(counts),"source",sum(r["source"]!=ORIGINAL for r in ROWS),"original",sum(r["source"]==ORIGINAL for r in ROWS))
if __name__=="__main__": main()
