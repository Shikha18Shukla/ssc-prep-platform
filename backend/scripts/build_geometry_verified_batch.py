"""Build a reviewed SSC Geometry batch with a calculation/reasoning ledger."""
from __future__ import annotations
import json, random, re, unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
ORIGINAL="Original SSC-style practice question"
ROWS=[]; LEDGER=[]

def q(level,stem,answer,proof,source=ORIGINAL,wrong=()):
    answer=str(answer); vals=[answer]
    for v in wrong:
        v=str(v)
        if v not in vals: vals.append(v)
    if len(vals)<4:
        m=re.fullmatch(r"(-?\d+(?:\.\d+)?)(.*)",answer)
        if m:
            x=float(m.group(1)); u=m.group(2)
            for z in (x+10,x-10,x+20,x-20):
                v=(str(int(z)) if z.is_integer() else str(z))+u
                if v not in vals: vals.append(v)
                if len(vals)==4: break
        else:
            for v in ("2×"+answer,answer+"/2","3×"+answer):
                if v not in vals: vals.append(v)
    if len(vals)!=4: raise ValueError(f"Expected four distinct options for {stem}: {vals}")
    random.Random(len(ROWS)*37+len(stem)).shuffle(vals)
    key="ABCD"[vals.index(answer)]
    ROWS.append({"subject_slug":"maths","subcategory_slug":"advanced-maths","chapter_slug":"geometry","question_text":stem,"options":dict(zip("ABCD",vals)),"correct_option":key,"explanation":proof,"difficulty":level,"is_pyq":False,"pyq_year":None,"pyq_exam_name":None,"source":source})
    LEDGER.append({"row":len(ROWS),"question":stem,"difficulty":level,"expected_answer":answer,"independent_reasoning":proof,"source":source})

def src(pdf,page): return f"{pdf}, PDF page {page}; exam/year not stated per item (PYQ status unverified)"

# Source-derived: selected legible, independently solvable examples from six decks.
q("MEDIUM","Two parallel chords of a circle have lengths 10 cm and 4 cm, lie on the same side of the centre, and are 3 cm apart. Find the circle's diameter.","2√29 cm","The perpendicular distances x,y from centre satisfy x²=r²−25, y²=r²−4 and y−x=3. Thus (y−x)(y+x)=21, so y+x=7, x=2,y=5; r²=29, diameter=2√29 cm.",src("Geometry 1.pdf",5),["√29 cm","4√29 cm","2√21 cm"])
q("EASY","Two triangles have AB=DB, AC=DC, and BC is common. Which congruence criterion proves △ABC≅△DBC?","SSS","The three corresponding sides are equal: AB=DB, AC=DC, and BC=BC; use SSS.",ORIGINAL,["SAS","ASA","RHS"])
q("MEDIUM","A circle has radius 5 cm. A chord is 6 cm long. Find its distance from the centre.",4,"The perpendicular from the centre bisects the chord; distance=√(5²−3²)=4 cm.",src("Geometry 4.pdf",6),["3 cm","4 cm","5 cm"])
q("EASY","From an external point, two tangents are drawn to the same circle. One tangent segment is 12 cm. Find the other tangent segment.","12 cm","Tangent segments from a common external point have equal lengths.",src("Geometry 4.pdf",11),["6 cm","24 cm","√12 cm"])
q("HARD","Two circles of radii 4 cm and 6 cm have centres 10 cm apart. Find the length of a direct common tangent segment.","4√6 cm","For a direct common tangent, L²=d²−(R−r)²=100−4=96; L=4√6 cm.",ORIGINAL,["8 cm","10 cm","6 cm"])
q("MEDIUM","At the intersection of two straight lines, one angle is 68°. Find the vertically opposite angle.","68°","Vertically opposite angles are equal.",ORIGINAL,["112°","34°","146°"])
q("EASY","Two adjacent angles form a straight line. If one is 73°, find the other.","107°","A linear pair sums to 180°; 180−73=107°.",src("Geometry 2.pdf",6),["73°","117°","97°"])
q("MEDIUM","Two parallel lines are cut by a transversal. If an interior angle on one side is 118°, find the interior angle on the same side of the transversal at the other line.","62°","Co-interior angles between parallel lines are supplementary: 180−118=62°.",src("Geometry 2.pdf",7),["118°","72°","52°"])
q("MEDIUM","Two parallel lines are cut by a transversal. An acute corresponding angle is 54°. Find the obtuse angle at the other intersection.","126°","The matching acute angle is 54°; its adjacent linear-pair angle is 180−54=126°.",src("Geometry 2.pdf",9),["54°","144°","116°"])
q("MEDIUM","In a triangle, an exterior angle is 125° and one remote interior angle is 48°. Find the other remote interior angle.","77°","Exterior-angle theorem: 125=48+x, so x=77°.",ORIGINAL,["67°","83°","55°"])
q("EASY","The interior angles of a triangle include 47° and 68°. Find the third angle.","65°","Triangle angle sum is 180°; 180−47−68=65°.",ORIGINAL,["55°","75°","115°"])
q("MEDIUM","AB is parallel to CD. A zig-zag transversal makes angles 125° and 35° with the parallel directions at the two bends. Find the acute angle between its two segments.","90°","The first segment's acute inclination is 180−125=55°; the second is 35° on the other side. Their included angle is 55+35=90°.",src("Geometry 2.pdf",13),["80°","100°","70°"])
q("EASY","A cyclic quadrilateral has one interior angle of 112°. Find its opposite angle.","68°","Opposite angles of a cyclic quadrilateral are supplementary: 180−112=68°.",src("Geometry 3.pdf",10),["112°","78°","58°"])
q("EASY","A chord of a circle is 10 cm long and is 12 cm from the centre. Find the circle's diameter.","26 cm","The perpendicular bisects the chord; radius=√(12²+5²)=13 cm, so diameter=26 cm.",src("Geometry 5.pdf",28),["13 cm","15 cm","30 cm"])
q("EASY","Two concentric circles have radii 5 cm and 3 cm. A chord of the larger circle is tangent to the smaller circle. Find the chord length.","8 cm","The perpendicular from the common centre to the chord is 3 cm. Half-chord=√(5²−3²)=4 cm, so the chord is 8 cm.",src("Geometry 5.pdf",29),["4 cm","6 cm","10 cm"])
q("EASY","A radius is drawn to the point where a tangent touches a circle. What is the angle between the radius and tangent?","90°","The tangent at a point is perpendicular to the radius through that point.",ORIGINAL,["45°","60°","180°"])
q("MEDIUM","From an external point P, PT is a tangent of length 12 cm, and a secant meets the circle at A then B. If PA=x cm and AB=7 cm, find x.","9 cm","Tangent-secant theorem gives PT²=PA·PB, so 144=x(x+7). Thus x²+7x−144=0=(x−9)(x+16), and the positive length is 9 cm.",src("Geometry 5.pdf",31),["8 cm","12 cm","16 cm"])
q("MEDIUM","O is the circumcentre of △PQR. If ∠QOR=110° and ∠OPR=25°, find ∠PRQ.","60°","OP=OR, so ∠PRO=25°. In isosceles △QOR, ∠ORQ=(180−110)/2=35°. Thus ∠PRQ=25+35=60°.",src("Geometry 6.pdf",28),["65°","50°","55°"])
q("MEDIUM","In △ABC, D and E lie on AB and AC, respectively, and DE∥BC. If AD:DB=2:3, find AE:EC.","2:3","Thales/intercept theorem: parallel DE cuts the two sides proportionally, AD/DB=AE/EC=2/3.",src("Geometry 5.pdf",15),["3:2","2:5","5:2"])
q("MEDIUM","The centroid G of a triangle divides median AD in the ratio AG:GD. Find this ratio.","2:1","The centroid lies two-thirds of the way from each vertex along a median, so AG:GD=2:1.",src("Geometry 5.pdf",11),["1:2","3:1","1:1"])

# Original foundational geometry.
easy=[
 ("Two complementary angles are in the ratio 2:3. Find the smaller angle.",36,"Let angles be 2x,3x; 5x=90, x=18; smaller=36°.","°"),
 ("Two supplementary angles are equal. Find each angle.",90,"Equal angles sum to 180°, so each is 90°.","°"),
 ("A triangle has angles 90° and 35°. Find the third angle.",55,"180−90−35=55°.","°"),
 ("An isosceles triangle has vertex angle 40°. Find each base angle.",70,"Base angles equal; each=(180−40)/2=70°.","°"),
 ("An equilateral triangle has side 9 cm. Find its perimeter.",27,"Perimeter=3×9=27 cm."," cm"),
 ("In a triangle, the two opposite interior angles to an exterior angle are 52° and 61°. Find the exterior angle.",113,"Exterior angle equals sum of remote interior angles=52+61=113°.","°"),
 ("A triangle has side lengths 5 cm, 7 cm, and x cm. Which is the least possible integer x?",3,"Triangle inequality requires x>|7−5|=2, so least integer x=3 (also x<12)."," cm"),
 ("A right triangle has legs 6 cm and 8 cm. Find the hypotenuse.",10,"Pythagoras: c=√(6²+8²)=10 cm."," cm"),
 ("A right triangle has hypotenuse 13 cm and one leg 5 cm. Find the other leg.",12,"Other leg=√(13²−5²)=12 cm."," cm"),
 ("A linear pair has angle measures (3x+10)° and (2x+20)°. Find x.",30,"3x+10+2x+20=180; 5x=150; x=30.",""),
 ("Two vertically opposite angles measure (4x−5)° and (3x+15)°. Find x.",20,"Set equal: 4x−5=3x+15; x=20.",""),
 ("Two parallel lines are cut by a transversal. A corresponding angle is 72°. Find its alternate interior angle.",72,"Corresponding and alternate interior angles are equal for parallel lines.","°"),
 ("The sum of interior angles of a quadrilateral is what?",360,"A quadrilateral can be divided into two triangles; total=2×180=360°.","°"),
 ("Find each interior angle of a regular hexagon.",120,"Interior angle=(n−2)180/n=4×180/6=120°.","°"),
 ("Find the sum of the interior angles of a decagon.",1440,"Sum=(n−2)180=8×180=1440°.","°"),
 ("Find each exterior angle of a regular 15-sided polygon.",24,"Exterior angles sum to 360°; each=360/15=24°.","°"),
 ("A polygon has interior-angle sum 1260°. How many sides does it have?",9,"(n−2)180=1260 gives n−2=7, n=9.",""),
 ("A rectangle has length 12 cm and width 5 cm. Find its diagonal.",13,"Diagonal=√(12²+5²)=13 cm."," cm"),
 ("A square has diagonal 10√2 cm. Find its side.",10,"For a square d=s√2; s=10 cm."," cm"),
 ("A rhombus has diagonals 10 cm and 24 cm. Find its side length.",13,"Diagonals bisect perpendicularly; side=√(5²+12²)=13 cm."," cm"),
 ("A parallelogram has adjacent angles x° and (2x−30)°. Find x.",70,"Adjacent angles sum 180: x+2x−30=180; x=70.","°"),
 ("A rhombus has diagonals 16 cm and 30 cm. Find its area.",240,"Area of a rhombus is half the product of its diagonals: (16×30)/2=240 cm²."," cm²"),
 ("An isosceles trapezoid has one base angle 72°. Find the other angle on the same leg.",108,"Consecutive interior angles between parallel bases are supplementary: 108°.","°"),
 ("A circle has radius 7 cm. Find its diameter.",14,"Diameter=2r=14 cm."," cm"),
 ("A central angle subtending a minor arc is 104°. Find the measure of that arc.",104,"The measure of a minor arc equals its central angle.","°"),
 ("An inscribed angle intercepts an arc of 130°. Find the inscribed angle.",65,"An inscribed angle equals half its intercepted arc: 130/2=65°.","°"),
 ("An inscribed angle subtends a diameter. Find the angle.",90,"Angle in a semicircle is a right angle.","°"),
 ("A chord is 16 cm long. What is the length of the radius drawn to its midpoint if the centre-to-chord distance is 6 cm?",10,"The centre, chord midpoint, and endpoint form a right triangle: r=√(8²+6²)=10 cm."," cm"),
 ("A tangent and a chord meet at a point on a circle. The intercepted minor arc is 84°. Find the acute angle between them.",42,"Tangent-chord angle equals half the intercepted arc: 84/2=42°.","°"),
 ("A cyclic quadrilateral has three angles 85°, 95°, and 110°. Find the fourth angle.",70,"Quadrilateral angles sum 360°; fourth=360−290=70°.","°")]
for s,a,p,u in easy[:22]:q("EASY",s,str(a)+u,p)

# Medium: linked properties and theorem applications.
medium=[
 ("In △ABC, AB=AC and ∠A=44°. Find each base angle.",68,"Base angles equal; each=(180−44)/2=68°.","°"),
 ("The angles of a triangle are in ratio 2:3:4. Find the largest angle.",80,"Nine parts=180°, one=20°; largest=4×20=80°.","°"),
 ("A right triangle has one acute angle 32°. Find the other acute angle.",58,"Acute angles in a right triangle sum to 90°; 90−32=58°.","°"),
 ("In △ABC, ∠A=50° and ∠B=70°. The bisectors of A and B meet at I. Find ∠AIB.",120,"Incenter angle=90°+C/2; C=60°, so ∠AIB=120°.","°"),
 ("In △ABC, AD bisects ∠A. If AB=10, AC=15, and BD=8, find DC.",12,"Angle-bisector theorem BD/DC=AB/AC=2/3; DC=12."," cm"),
 ("In △ABC, DE∥BC, with AD=6, DB=4, and AE=9. Find EC.",6,"Intercept theorem AD/DB=AE/EC; 6/4=9/EC gives EC=6."," cm"),
 ("Triangles ABC and DEF are similar with side scale AB:DE=3:5. If area of ABC is 54 cm², find area DEF.",150,"Areas scale as square of side ratio: 54×(5/3)²=150 cm²."," cm²"),
 ("Two similar triangles have corresponding sides 8 cm and 12 cm. If the smaller perimeter is 30 cm, find the larger perimeter.",45,"Perimeters scale as corresponding sides: 30×12/8=45 cm."," cm"),
 ("A 1.5 m pole casts a 2 m shadow. At the same time, a tree casts a 12 m shadow. Find the tree's height.",9,"Similar triangles: height/shadow=1.5/2; tree height=12×0.75=9 m."," m"),
 ("A 10 m ladder reaches 8 m up a wall. How far is its foot from the wall?",6,"By Pythagoras, horizontal distance=√(10²−8²)=6 m."," m"),
 ("The diagonal of a rectangle is 25 cm and one side is 7 cm. Find the other side.",24,"√(25²−7²)=24 cm."," cm"),
 ("A square's side is increased from 8 cm to 12 cm. By how much does the square of its diagonal increase?",160,"For side s, diagonal squared is 2s²; change=2(12²−8²)=160 cm²."," cm²"),
 ("A parallelogram has one angle 118°. Find its adjacent angle.",62,"Adjacent angles in a parallelogram are supplementary; 180−118=62°.","°"),
 ("A rhombus has one interior angle 64°. Find its smallest angle.",64,"Opposite angles equal 64°; adjacent angles are 116°, so smallest=64°.","°"),
 ("A quadrilateral has angles 75°, 92°, and 108°. Find its fourth angle.",85,"Fourth=360−(75+92+108)=85°.","°"),
 ("A regular polygon has exterior angle 30°. Find its number of sides.",12,"n=360/30=12.",""),
 ("A regular octagon has how many diagonals?",20,"Diagonals=n(n−3)/2=8×5/2=20.",""),
 ("A regular pentagon has interior angle sum what?",540,"Sum=(5−2)×180=540°.","°"),
 ("A cyclic quadrilateral has opposite angles (3x+10)° and (5x−6)°. Find x.",22,"Opposite angles sum 180: 8x+4=180; x=22.",""),
 ("In a circle, equal chords subtend central angles (5x−10)° and (3x+30)°. Find x.",20,"Equal chords subtend equal angles: 5x−10=3x+30; x=20.",""),
 ("A chord of a circle of radius 10 cm is 12 cm long. Find its distance from the centre.",8,"Half-chord=6; distance=√(10²−6²)=8 cm."," cm"),
 ("Two chords intersect inside a circle. One chord's segments are 3 cm and 12 cm; the other's are 4 cm and x cm. Find x.",9,"Intersecting chords: 3×12=4x; x=9 cm."," cm"),
 ("From external point P, secants PAB and PCD have PA=4, AB=5, PC=3. Find CD.",9,"PA·PB=PC·PD; 4×9=3×(3+CD); CD=9."," cm"),
 ("A circle's radius is 13 cm and a chord is 5 cm from the centre. Find chord length.",24,"Half chord=√(13²−5²)=12; full length=24 cm."," cm"),
 ("A triangle has sides 7 cm, 24 cm, 25 cm. Find its inradius.",3,"It is right; area=7×24/2=84, semiperimeter=28; r=A/s=3 cm."," cm"),
 ("A right triangle has legs 9 cm and 12 cm. Find its circumradius.",7.5,"For a right triangle, circumradius is half the hypotenuse; hypotenuse=15, R=7.5 cm."," cm"),
 ("In a triangle, the median to a side divides the triangle into two areas. If total area is 72 cm², find each part's area.",36,"A median bisects the opposite side; the two triangles have equal altitudes and bases, hence each area=36 cm²."," cm²"),
 ("The medians of a triangle meet at G. If median AD=18 cm, find GD.",6,"Centroid divides a median in ratio AG:GD=2:1; GD=18/3=6 cm."," cm"),
 ("A triangle has sides 13 cm and 14 cm with included angle 60°. Find the square of the third side.",183,"Cosine rule c²=13²+14²−2×13×14×cos60=169+196−182=183 cm²."," cm²"),
 ("Two isosceles triangles are similar. Their corresponding sides are 6 cm and 9 cm. If the smaller area is 32 cm², find the larger area.",72,"Area scale=(9/6)²=9/4; larger area=32×9/4=72 cm²."," cm²")]
for s,a,p,u in medium[:19]:q("MEDIUM",s,str(a)+u,p)

# Hard: multi-step theorem chains and nontrivial reasoning.
hard=[
 ("In △ABC, AB=AC and ∠A=36°. The bisector of ∠B meets AC at D. Find ∠BDC.",72,"Base angles B=C=72°. In △BCD, ∠CBD=36° and ∠BCD=72°, so ∠BDC=180−36−72=72°.","°"),
 ("In △ABC, AD is an angle bisector, AB=12 cm, AC=18 cm, BC=20 cm. Find BD.",8,"BD/DC=12/18=2/3 and BD+DC=20; BD=8 cm."," cm"),
 ("A line parallel to one side of a triangle cuts the other two sides in ratios 3:2 from the corresponding vertices. If the smaller triangle area is 81 cm², find the whole triangle area.",225,"Side scale small:whole=3:(3+2)=3/5; area scale=9/25; whole=81×25/9=225 cm²."," cm²"),
 ("Two similar triangles have area ratio 25:49. A corresponding side of the smaller triangle is 15 cm. Find the corresponding side of the larger triangle.",21,"Side ratio=√25:√49=5:7; larger side=15×7/5=21 cm."," cm"),
 ("A right triangle has altitude from the right angle to its hypotenuse, splitting the hypotenuse into 9 cm and 16 cm segments. Find the altitude.",12,"Altitude is geometric mean: h²=9×16, so h=12 cm."," cm"),
 ("In a right triangle, the hypotenuse is 25 cm and one leg is 15 cm. Find the radius of its incircle.",5,"Other leg=20; for right triangle r=(a+b−c)/2=(15+20−25)/2=5 cm."," cm"),
 ("The sides of a triangle are 13 cm, 14 cm, and 15 cm. Find its inradius.",4,"Heron area: s=21, A=√(21×8×7×6)=84; r=A/s=4 cm."," cm"),
 ("A triangle has sides 10 cm, 17 cm, and 21 cm. Find the length of the median to the 21 cm side.","√337/2","Median formula m²=(2a²+2b²−c²)/4=(200+578−441)/4=337/4; m=√337/2 cm."," cm"),
 ("In triangle ABC, AB=10 cm, AC=14 cm, and BC=16 cm. Find the length of the angle bisector from A.","10√7/3","Angle-bisector length²=bc[1−a²/(b+c)²]=10×14[1−256/576]=700/9; length=10√7/3 cm."," cm"),
 ("In an isosceles triangle with equal sides 13 cm and base 10 cm, find the radius of the incircle.","10/3","Height=12; area=60; semiperimeter=18; inradius=A/s=60/18=10/3 cm."," cm"),
 ("A regular polygon has each interior angle 165°. Find the number of sides.",24,"Exterior angle=180−165=15°; n=360/15=24.",""),
 ("The interior-angle sum of a polygon is four times its exterior-angle sum. How many sides does it have?",10,"(n−2)180=4×360=1440; n−2=8, n=10.",""),
 ("A convex polygon has 54 diagonals. Find its number of sides.",12,"n(n−3)/2=54 ⇒ n²−3n−108=0 ⇒(n−12)(n+9)=0; n=12.",""),
 ("In a cyclic quadrilateral, one angle is twice its opposite angle. Find the larger of the two opposite angles.",120,"Let angles x and 2x. x+2x=180 ⇒ larger=120°.","°"),
 ("A cyclic quadrilateral has consecutive angles (2x+10)°, (3x−5)°, and (x+20)°. Find the fourth angle.",35,"Opposite first and third sum 180: (2x+10)+(x+20)=180 ⇒x=50. The second angle is 145°; its opposite is 35°.","°"),
 ("Two chords AB and CD intersect at P inside a circle. If AP=4, PB=9, CP=6, find PD.",6,"AP×PB=CP×PD; 36=6PD; PD=6."," cm"),
 ("From point P, a tangent PT and a secant PAB are drawn. If PA=5 cm and AB=7 cm, find PT.","√60 cm","PT²=PA·PB=5×12=60; PT=√60 cm."," cm"),
 ("A chord of a circle of radius 17 cm is 8 cm from the centre. Find the chord length.",30,"Half-chord=√(17²−8²)=15; chord=30 cm."," cm"),
 ("Two parallel chords of lengths 16 cm and 30 cm lie on opposite sides of a circle's centre. Their distances from the centre are 15 cm and 8 cm. Find the circle's radius.",17,"For chord 16, half=8 and distance=15; r²=8²+15²=289, so r=17 cm. For chord30 half=15, d=8 also gives17."," cm"),
 ("A circle has radius 10 cm. A chord subtends a central angle of 120°. Find the chord length.","10√3 cm","Chord=2R sin(θ/2)=20 sin60=10√3 cm."," cm"),
 ("An inscribed angle intercepts a major arc of 250°. Find the measure of that inscribed angle.",125,"An inscribed angle equals half its intercepted arc: 250/2=125°.","°"),
 ("Two tangents from P touch a circle at A and B. If ∠AOB=136°, find ∠APB.",44,"OA⊥PA and OB⊥PB; quadrilateral OAPB has two right angles, so ∠APB=180−136=44°.","°"),
 ("A circle is inscribed in a triangle with side lengths 13, 14, and 15 cm. Find the total length of the three tangent segments from each vertex to its two contact points.",42,"At each vertex the two tangent segments are equal; their combined total across vertices equals the triangle perimeter 42 cm."," cm"),
 ("A triangle has sides 7 cm, 15 cm, and 20 cm. Find the radius of its circumcircle.","25/2","Heron s=21; area=√(21×14×6×1)=42. Circumradius abc/(4A)=7×15×20/168=25/2 cm."," cm"),
 ("In △ABC, medians AD and BE meet at G. If area △ABC is 90 cm², find area △ABG.",30,"The centroid partitions the triangle into six equal-area small triangles; ABG comprises two, so area=90/3=30 cm²."," cm²"),
 ("In triangle ABC, D is midpoint of BC. If AB²+AC²=250 cm² and BC=10 cm, find AD.",10,"Apollonius: AB²+AC²=2(AD²+BD²). 250=2(AD²+25); AD²=100; AD=10 cm."," cm"),
 ("A triangle has sides 5 cm, 12 cm, and 13 cm. Find the distance from the right-angle vertex to the midpoint of the hypotenuse.",6.5,"In a right triangle, median to hypotenuse equals half the hypotenuse, 13/2=6.5 cm."," cm"),
 ("The sides of a triangle are 9 cm, 10 cm, and 17 cm. Find the median to the side of length 17 cm.","√73/2","Median²=(2×9²+2×10²−17²)/4=(162+200−289)/4=73/4; median=√73/2 cm."," cm"),
 ("A point lies inside an equilateral triangle of side 6 cm. Its perpendicular distances from the three sides are 1 cm, 2 cm, and h cm. Find h.","3√3−3 cm","Area total=√3/4×36=9√3. Also area=1/2×6×(1+2+h)=3(3+h); h=3√3−3 cm."," cm"),
 ("In △ABC, AB=AC=10 cm and BC=12 cm. The incircle touches BC at D. Find BD.",6,"In an isosceles triangle the incenter lies on the perpendicular bisector of BC; tangency point D is its midpoint, so BD=6 cm."," cm")]
for s,a,p,u in hard[:29]:q("HARD",s,str(a)+u,p)

def norm(s):return " ".join(unicodedata.normalize("NFKC",s).casefold().split())
def main():
    counts=Counter(r["difficulty"] for r in ROWS)
    if len(ROWS)!=90 or counts!={"EASY":30,"MEDIUM":30,"HARD":30}:raise SystemExit(f"bad batch count {len(ROWS)} {counts}")
    for i,r in enumerate(ROWS):
        if len(set(norm(v) for v in r["options"].values()))!=4 or r["options"][r["correct_option"]]!=LEDGER[i]["expected_answer"]:raise SystemExit(f"MCQ invariant failure row {i+1}")
        for other in ROWS[:i]:
            if norm(other["question_text"])==norm(r["question_text"]) or SequenceMatcher(None,norm(other["question_text"]),norm(r["question_text"])).ratio()>=.93:raise SystemExit(f"near duplicate: {r['question_text']}")
    (BASE/"data/geometry_verified_batch.json").write_text(json.dumps({"questions":ROWS},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (BASE/"data/geometry_answer_ledger.json").write_text(json.dumps(LEDGER,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("WROTE",len(ROWS),dict(counts),"source",sum(r["source"]!=ORIGINAL for r in ROWS),"original",sum(r["source"]==ORIGINAL for r in ROWS))
if __name__=="__main__":main()
