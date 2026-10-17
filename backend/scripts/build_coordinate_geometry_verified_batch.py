"""Build the Coordinate Geometry batch and its provenance-aware solution ledger."""
from __future__ import annotations
import json, random, unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
ORIGINAL="Original SSC-style practice question"
ROWS=[]; LEDGER=[]
def src(pdf,page): return f"{pdf}, PDF page {page}; exam/year not stated per item (PYQ status unverified)"
def q(level,stem,answer,proof,source=ORIGINAL,options=()):
    answer=str(answer); vals=[str(x) for x in options]
    if len(vals)!=4 or sum(v==answer for v in vals)!=1 or len(set(vals))!=4:
        raise ValueError(f"Bad options for {stem}: {vals}, answer={answer}")
    random.Random(len(ROWS)*41+len(stem)).shuffle(vals)
    key="ABCD"[vals.index(answer)]
    row={"subject_slug":"maths","subcategory_slug":"advanced-maths","chapter_slug":"coordinate-geometry","question_text":stem,"options":dict(zip("ABCD",vals)),"correct_option":key,"explanation":proof,"difficulty":level,"is_pyq":False,"pyq_year":None,"pyq_exam_name":None,"source":source}
    ROWS.append(row); LEDGER.append({"row":len(ROWS),"question":stem,"difficulty":level,"expected_answer":answer,"independent_reasoning":proof,"source":source})
def add(level, items):
    for stem,ans,proof,opts in items: q(level,stem,ans,proof,ORIGINAL,opts)

# Source questions retained only when the page's data and key yield one answer.
q("EASY","The distance between P(0,b) and Q(a,0) is:","√(a²+b²)","Distance formula gives √((a−0)²+(0−b)²)=√(a²+b²).",src("Coordinate Geometry  01_.pdf",13),["√(a²−b²)","√(a²+b²)","√(a+b)","a+b"])
q("MEDIUM","P divides the segment joining A(5,−2) and B(9,6) internally in the ratio 3:1. Find P.","(8,4)","Section formula gives ((3·9+1·5)/4,(3·6+1·(−2))/4)=(8,4).",src("Coordinate Geometry  01_.pdf",15),["(4,−7)","(7/2,4)","(8,4)","(12,8)"])
q("MEDIUM","P(1,10/3) divides the segment joining A(−3,2) and B(3,4). In what ratio AP:PB does it divide it?","2:1","Using the x-coordinate section formula, 1=(3m−3n)/(m+n), so m=2n. The y-coordinate then is (4m+2n)/(m+n)=10/3, confirming AP:PB=2:1.",src("Coordinate Geometry  01_.pdf",17),["2:3","1:2","2:1","3:1"])
q("HARD","Find the coordinates of the point that divides the segment joining (2,4) and (6,8) externally in the ratio 5:3.","(12,14)","External section formula: ((5·6−3·2)/(5−3),(5·8−3·4)/(5−3))=(12,14).",src("Coordinate Geometry  01_.pdf",18),["(5,6)","(12,14)","(3,8)","(2,7)"])
q("MEDIUM","Find the ratio in which the segment joining A(3,−5) and B(5,4) is divided by the x-axis.","5:4","At the x-axis y=0. For AP:PB=m:n, (4m−5n)/(m+n)=0, hence m:n=5:4.",src("Coordinate Geometry  01_.pdf",19),["4:5","5:4","5:7","6:5"])
q("MEDIUM","Find the slope of the line through P(−4,7) and Q(2,3).","−2/3","Slope=(3−7)/(2−(−4))=−4/6=−2/3.",src("Coordinate Geometry  01_.pdf",21),["−2/3","2/3","−3/2","3/2"])
q("MEDIUM","What angle does the line through (√3,1) and (√15,√5) make with the positive x-axis?","30°","Its slope is (√5−1)/(√15−√3)=1/√3, so the inclination θ satisfies tanθ=1/√3 and θ=30°.",src("Coordinate Geometry  01_.pdf",22),["30°","45°","60°","90°"])
q("MEDIUM","Find the reflection of (7,4) in the point (1,3).","(−5,2)","The reflection point is the opposite endpoint of a segment whose midpoint is (1,3): (x,y)=(2·1−7,2·3−4)=(−5,2).",src("Coordinate Geometry 02_.pdf",23),["(−6,−1)","(−5,2)","(6,−2)","(8,7)"])
q("HARD","Find the perpendicular distance from (−3,4) to the line 3x+4y−5=0.","2/5","Distance=|3(−3)+4(4)−5|/√(3²+4²)=|2|/5=2/5.",src("Coordinate Geometry 02_.pdf",13),["3/5","2/5","1/3","2/3"])
q("HARD","Find the area of the triangle with vertices (3,4), (−4,3), and (8,6).","9/2","Shoelace gives half of |3(3−6)+(−4)(6−4)+8(4−3)|=|-9-8+8|/2=9/2 square units.",src("Coordinate Geometry 02_.pdf",14),["9/4","7/2","9/2","9"])
q("HARD","Find the area of the quadrilateral with consecutive vertices (−4,5), (0,7), (5,−5), and (−4,−2).","121/2","Shoelace: absolute difference of diagonal sums is 121; area=121/2 square units.",src("Coordinate Geometry 02_.pdf",15),["121/2","125/2","121","125"])
q("HARD","For what value of k do the lines 5x+20y=11 and 2x+ky=17 intersect?","k ≠ 8","They are parallel when determinant 5k−40=0, i.e. k=8. They intersect for every other real k.",src("Coordinate Geometry 02_.pdf",16),["k ≠ 8","k ≠ 4","k ≠ 14","k ≠ 2"])
q("HARD","For what value of k do x+3y+7=0 and 4x+ky+19=0 have no solution?","12","No solution requires equal x/y coefficient ratios but unequal constant ratios: 1/4=3/k gives k=12; 7/19≠1/4.",src("Coordinate Geometry 02_.pdf",17),["3","−12","12","8"])
q("HARD","A line ax+by=c, where a,b,c>0, meets the coordinate axes at P and Q. Find the area of triangle OPQ.","c²/(2ab)","The intercepts are c/a and c/b, so the right-triangle area is (1/2)(c/a)(c/b)=c²/(2ab).",src("Coordinate Geometry 02_.pdf",19),["c²/(ab)","c²/(2ab)","c²/(a²b)","c²/(ab²)"])

add("EASY",[
("In which quadrant does (−4,7) lie?","II","x<0 and y>0 identify Quadrant II.",["I","II","III","IV"]),
("Which point lies on the y-axis?","(0,−5)","Every point on the y-axis has x-coordinate 0.",["(−5,0)","(0,−5)","(5,5)","(−1,0)"]),
("Find the distance between (1,2) and (4,6).","5","Distance=√((4−1)²+(6−2)²)=√25=5.",["4","5","6","7"]),
("Find the midpoint of (−2,5) and (6,1).","(2,3)","Average corresponding coordinates: ((−2+6)/2,(5+1)/2)=(2,3).",["(4,6)","(2,3)","(−4,2)","(2,4)"]),
("Reflect (3,−8) across the x-axis.","(3,8)","Reflection across the x-axis preserves x and changes the sign of y.",["(−3,−8)","(3,8)","(−3,8)","(8,3)"]),
("Reflect (−6,2) in the origin.","(6,−2)","Origin reflection maps (x,y) to (−x,−y).",["(−6,−2)","(6,2)","(6,−2)","(2,−6)"]),
("What is the slope of the line through (−1,4) and (3,4)?","0","The y-coordinates are equal, so the line is horizontal and its slope is 0.",["0","1","−1","undefined"]),
("What is the slope of the vertical line through (5,−2) and (5,9)?","undefined","The slope denominator Δx is zero for a vertical line.",["0","1","−1","undefined"]),
("What is the y-coordinate of every point on the x-axis?","0","The x-axis is defined by y=0.",["−1","0","1","It varies"]),
("A point has x<0 and y<0. In which quadrant is it?","III","Both coordinates negative define Quadrant III.",["I","II","III","IV"]),
("Translate (2,−3) by the vector (−4,5).","(−2,2)","Add vector components: (2−4,−3+5)=(−2,2).",["(6,−8)","(−2,2)","(−2,−8)","(2,−2)"]),
("What is the absolute value of the abscissa of (−7,0)?","7","The abscissa is the first coordinate, −7; its absolute value is 7.",["−7","0","2","7"]),
("In the point (−4,−6), what is the ordinate?","−6","The ordinate is the second coordinate, which is −6.",["−4","−6","4","6"]),
("Which pair of points lies on the same horizontal line?","(−3,4) and (2,4)","Points on the same horizontal line have equal y-coordinates; only this pair has matching second coordinates.",["(−3,4) and (2,4)","(1,2) and (1,5)","(0,1) and (2,3)","(−2,4) and (3,−2)"]),
("The midpoint of A(1,−2) and B(x,6) is (4,2). Find x.","7","The midpoint x-coordinate gives (1+x)/2=4, hence x=7; the y-coordinate also averages to 2.",["5","6","7","8"]),
("Which quadrant contains (5,−1)?","IV","Positive x and negative y define Quadrant IV.",["I","II","III","IV"]),
("Find the distance from (−3,4) to the origin.","5","Distance from origin is √(x²+y²)=√(9+16)=5.",["4","5","7","25"]),
("A point is 4 units left and 3 units above the origin. What are its coordinates?","(−4,3)","Left means negative x and above means positive y.",["(4,3)","(−4,3)","(−3,4)","(4,−3)"]),
("If P=(a,b), what are the coordinates of its reflection in the y-axis?","(−a,b)","Reflection across the y-axis reverses x and preserves y.",["(a,−b)","(−a,b)","(−a,−b)","(b,a)"]),
("Find the slope of the line through (2,−1) and (6,7).","2","Slope=(7−(−1))/(6−2)=8/4=2.",["1/2","2","−2","4"]),
("A line has slope 3 and passes through (0,−2). What is its y-intercept?","−2","At x=0 the point on the line is (0,−2), so the y-intercept is −2.",["−3","−2","2","3"]),
("Which ordered pair satisfies y=2x+1?","(2,5)","Substitution gives 5=2·2+1; the other listed pairs fail the equation.",["(1,1)","(2,5)","(3,5)","(0,0)"]),
("How many units apart are the parallel lines x=−2 and x=5?","7","Their horizontal separation is |5−(−2)|=7.",["3","5","7","10"]),
("The point (x,−4) lies on the y-axis. Find x.","0","Points on the y-axis have x-coordinate zero.",["−4","0","4","1"]),
("What is the reflection of (−2,−7) across the x-axis?","(−2,7)","An x-axis reflection preserves the abscissa and negates the ordinate.",["(2,−7)","(−2,7)","(2,7)","(7,−2)"]),
("Find the centroid of the triangle with vertices (0,0), (6,0), and (0,9).","(2,3)","The centroid averages vertex coordinates: ((0+6+0)/3,(0+0+9)/3)=(2,3).",["(3,2)","(2,3)","(6,9)","(3,3)"]),
("A point on the x-axis is 6 units from the origin and lies to the left. Find it.","(−6,0)","On x-axis y=0; left of origin means x=−6.",["(6,0)","(−6,0)","(0,−6)","(−3,0)"]),
("For what value of t is (t,2) in Quadrant I?","t>0","Quadrant I requires both coordinates positive; y=2 is positive and so t must be positive.",["t<0","t=0","t>0","any t"]),
("Which non-origin point is equidistant from the x- and y-axes?","(4,−4)","Distances to the axes are |y| and |x|; here both are 4. The origin is excluded by the stem.",["(2,5)","(4,−4)","(−1,3)","(0,0)"]),
])

add("MEDIUM",[
("Find the point that divides (−4,3) and (8,−5) internally in the ratio 1:2.","(0,1/3)","Section formula gives ((1·8+2·(−4))/3,(1·(−5)+2·3)/3)=(0,1/3).",["(0,1/3)","(4,−1/3)","(−4,1)","(2,1/3)"]),
("The midpoint of A(−3,5) and B(x,y) is (2,−1). Find B.","(7,−7)","From (−3+x)/2=2, x=7; from (5+y)/2=−1, y=−7.",["(1,−3)","(7,−7)","(−7,7)","(4,−6)"]),
("Find the ratio in which P(2,1) divides the segment joining A(−1,−2) and B(5,4).","1:1","P is the midpoint: coordinates average to ((−1+5)/2,(−2+4)/2)=(2,1), so the ratio is 1:1.",["1:2","2:1","1:1","3:2"]),
("A point divides A(1,−3) and B(7,9) in ratio 2:1 internally. Find its y-coordinate.","5","y=(2·9+1·(−3))/3=15/3=5.",["3","4","5","6"]),
("Find the slope of the line through (−2,5) and (4,−7).","−2","Slope=(−7−5)/(4−(−2))=−12/6=−2.",["2","−2","−1/2","1/2"]),
("A line through (3,−2) is parallel to the line through (−1,4) and (2,10). Find its slope.","2","The reference slope is (10−4)/(2−(−1))=6/3=2; parallel lines have equal slopes.",["−2","1/2","2","3"]),
("Find the equation of the line with slope −3 passing through (2,5).","y=−3x+11","Point-slope form: y−5=−3(x−2), hence y=−3x+11.",["y=3x−1","y=−3x+11","y=−3x+5","y=−x+7"]),
("Find the x-intercept of 2x+3y=12.","6","Set y=0, obtaining 2x=12 and x=6.",["3","4","6","12"]),
("Find the y-intercept of 5x−2y=8.","−4","Set x=0; −2y=8, so y=−4.",["−8","−4","2","4"]),
("Are (1,2), (3,6), and (5,10) collinear?","Yes","Each point satisfies y=2x, so all three lie on the same line.",["Yes","No","Only first two","Cannot determine"]),
("Find the intersection point of x+y=7 and x−y=1.","(4,3)","Adding the equations gives 2x=8, so x=4; then y=3.",["(3,4)","(4,3)","(5,2)","(4,−3)"]),
("The distance between (x,1) and (2,5) is 5. If x>2, find x.","5","(x−2)²+16=25 gives (x−2)²=9; x>2 selects x=5.",["−1","1","5","7"]),
("Find the point where y=2x+1 meets the x-axis.","(−1/2,0)","Set y=0: 2x+1=0, so x=−1/2.",["(1/2,0)","(−1/2,0)","(0,1)","(0,−1)"]),
("A line through (1,3) and (5,11) meets the y-axis at what value?","1","Slope=2, so y−3=2(x−1), or y=2x+1; y-intercept=1.",["−1","0","1","2"]),
("Find the distance from (−2,7) to the line y=3.","4","The horizontal line has constant y=3; perpendicular distance is |7−3|=4.",["2","3","4","5"]),
("The midpoint of A and B is (3,−2). If A=(−1,4), find B.","(7,−8)","Coordinate sums must be twice the midpoint: B=(6−(−1),−4−4)=(7,−8).",["(5,−6)","(7,−8)","(−7,8)","(6,−4)"]),
("Find the slope of a line perpendicular to y=(1/4)x−6.","−4","Perpendicular nonvertical slopes multiply to −1; reciprocal of 1/4 with opposite sign is −4.",["4","−4","1/4","−1/4"]),
("For which value of k are (2,1), (5,7), and (8,k) collinear?","13","First two give slope 6/3=2. From (5,7), moving to x=8 raises y by 2·3=6; k=13.",["11","12","13","14"]),
("A line has intercepts 4 on x-axis and 6 on y-axis. Find its equation in intercept form.","x/4+y/6=1","Intercept form is x/a+y/b=1, with a=4 and b=6.",["x/6+y/4=1","x/4+y/6=1","4x+6y=1","x+y=10"]),
("A triangle has vertices (−2,0), (4,0), and (1,h). Its area is 12. If h>0, find h.","4","The base length is 6; 6h/2=12 gives h=4.",["2","3","4","6"]),
("Find the point that divides (−3,2) and (9,8) externally in ratio 2:1.","(21,14)","External formula yields ((2·9−1·(−3))/(2−1),(2·8−1·2)/(2−1))=(21,14).",["(5,6)","(15,10)","(21,14)","(−21,−14)"]),
("A line passes through (−2,3) and is parallel to 4x−2y=7. Find its y-intercept.","7","The given line has slope 2. Through (−2,3): y−3=2(x+2), so y=2x+7 and its y-intercept is 7.",["−1","3","5","7"]),
("Three consecutive vertices of an axis-parallel rectangle are (−1,2), (5,2), and (5,−3). Find the fourth vertex.","(−1,−3)","The first pair defines the top horizontal side and the second pair the right vertical side; the missing corner combines x=−1 with y=−3.",["(−1,−3)","(5,−3)","(−1,2)","(5,2)"]),
("A point (a,−6) is 10 units from (2,−6). Find the possible values of a.","−8 or 12","Equal y-coordinates make distance |a−2|=10, giving a=−8 or 12.",["−8 or 12","−6 or 10","−12 or 8","−10 or 6"]),
])

add("HARD",[
("Find k if the distance between (k,−4) and (3,8) is 13 and k<3.","−2","(k−3)²+12²=13² gives (k−3)²=25; k=−2 or 8, and k<3 selects −2.",["−8","−2","2","8"]),
("Find the circumcentre of the triangle with vertices (0,0), (6,0), and (0,8).","(3,4)","The triangle is right-angled at the origin, so its circumcentre is the midpoint of its hypotenuse from (6,0) to (0,8): (3,4).",["(3,4)","(6,8)","(0,4)","(3,0)"]),
("Find the value of t for which (1,2), (4,6), and (t,10) are collinear.","7","Slope between the first points is 4/3. Collinearity requires (10−6)/(t−4)=4/3, giving t=7.",["6","7","8","10"]),
("Find the perpendicular distance from (2,−1) to 6x−8y+3=0.","23/10","Distance=|12+8+3|/√(36+64)=23/10.",["17/10","2","23/10","23/5"]),
("The lines 2x+y=10 and x−y=2 intersect at P. Find the distance from P to (1,−1).","3√2","Solving gives P=(4,2). The distance to (1,−1) is √((4−1)²+(2+1)²)=√18=3√2.",["3","3√2","6","9"]),
("Two lines 3x+ky=5 and 6x+4y=9 are parallel and distinct. Find k.","2","Parallelism requires 3/6=k/4=1/2, so k=2. Their constants are not in the same ratio (5/9≠1/2), so they are distinct.",["1","2","3","4"]),
("Find the equation of the line through the intersection of x+y=5 and 2x−y=1, with slope 3.","y=3x−3","Solving gives intersection (2,3). Point-slope form y−3=3(x−2), hence y=3x−3.",["y=3x+3","y=3x−3","y=−3x+9","y=3x−7"]),
("A triangle has vertices (0,0), (p,0), and (0,q), with area 30 and p:q=5:3. If p,q>0, find p+q.","16","pq/2=30 gives pq=60. With p:q=5:3, let p=5u,q=3u;15u²=60 so u=2 and p+q=16.",["12","14","16","20"]),
("Find the point on the x-axis equidistant from A(−2,3) and B(4,3).","(1,0)","Let P=(x,0). Equate squared distances: (x+2)²+9=(x−4)²+9; simplifying gives 12x=12, so x=1.",["(−1,0)","(0,1)","(1,0)","(2,0)"]),
("A line cuts positive intercepts a and b and has equation x/a+y/b=1. If its intercept triangle has area 24 and a:b=3:4, find a+b.","14","ab/2=24 gives ab=48. Set a=3u,b=4u;12u²=48 so u=2 and a+b=14.",["10","12","14","16"]),
("Find the area of the triangle with vertices (a,0), (0,b), and (−a,0), where a,b>0.","ab","The base on the x-axis has length 2a and height b; area=(2a·b)/2=ab.",["ab/2","ab","2ab","a+b"]),
("Find the value of m if the line through (−1,4) and (m,−2) is perpendicular to 2x+3y=7.","−5","The given line slope is −2/3, so a perpendicular line has slope 3/2. Thus (−2−4)/(m+1)=−6/(m+1)=3/2, giving m=−5.",["−5","−3","5","8"]),
("The points A(0,0), B(6,0), and C(3,k) form a right angle at C. If k>0, find k.","3","At C, vectors CA=(−3,−k), CB=(3,−k). Perpendicularity gives CA·CB=−9+k²=0; k=3 since k>0.",["1","2","3","6"]),
("A line through (2,−3) has x-intercept 5. Find its slope.","1","Slope between (2,−3) and (5,0) is (0+3)/(5−2)=1.",["−1","1/2","1","3"]),
("A point P divides A(−4,1) and B(8,7) internally so that AP:PB=2:1. Find the distance OP.","√41","P=((2·8+1·(−4))/3,(2·7+1)/3)=(4,5), so OP=√(4²+5²)=√41.",["5","√41","√89","9"]),
("Find the area of the quadrilateral with vertices (0,0), (6,0), (5,4), and (1,3) in this order.","35/2","Shoelace diagonal sums differ by |39−4|=35; area=35/2.",["15","17","35/2","20"]),
("Find the distance between the parallel lines 3x−4y+8=0 and 6x−8y−5=0.","21/10","Divide the second equation by 2: 3x−4y−5/2=0. Distance=|8−(−5/2)|/√(9+16)=21/10.",["3/2","2","21/10","21/5"]),
("Find the equation of the line through (−2,5) and perpendicular to 3x−2y=8.","2x+3y−11=0","Given slope is 3/2; perpendicular slope=−2/3. Through point: y−5=−2/3(x+2), which rearranges to 2x+3y−11=0.",["2x−3y+19=0","2x+3y−11=0","3x+2y−4=0","2x+3y+11=0"]),
("For what value of k are (k,1), (2,3), and (6,11) collinear?","1","Slope from (2,3) to (6,11) is 2, so line is y=2x−1. Setting y=1 gives x=1.",["−1","1","2","4"]),
("Find the equation of the perpendicular bisector of the segment joining (−2,1) and (4,5).","3x+2y−9=0","The midpoint is (1,3); segment slope is 2/3, so the perpendicular slope is −3/2. Through (1,3): y−3=−3(x−1)/2, or 3x+2y−9=0.",["3x+2y−9=0","2x+3y−9=0","3x−2y+3=0","2x−3y+7=0"]),
("A line through (1,−2) is perpendicular to the line joining (−3,4) and (5,0). Find its y-intercept.","−4","The joining line slope is (0−4)/(5+3)=−1/2; a perpendicular line has slope 2. Through (1,−2): y=2x−4, so its y-intercept is −4.",["−4","−2","2","4"]),
("Find the area of the triangle formed by x=0, y=0, and 2x+5y=20.","20","Intercepts are (10,0) and (0,4); area=10·4/2=20.",["10","20","40","100"]),
("A point P=(x,y) is equidistant from A(−1,2), B(5,2), and C(2,5). Find P.","(2,2)","Equidistance from A and B places P on their perpendicular bisector x=2. Equating distances to A and C gives 9+(y−2)²=(y−5)², so 6y=12 and y=2.",["(2,2)","(1,3)","(3,2)","(2,4)"]),
])

# Reject near-verbatim stems; semantic coverage was manually balanced across
# coordinate signs, distance, section, slope/line, area, and reflection tasks.
def norm(s): return " ".join(unicodedata.normalize("NFKC",s).casefold().split())
def main():
    if len(ROWS)!=90 or Counter(r["difficulty"] for r in ROWS)!={"EASY":30,"MEDIUM":30,"HARD":30}:
        raise ValueError(f"bad bank size/distribution: {len(ROWS)} {Counter(r['difficulty'] for r in ROWS)}")
    stems=[norm(r["question_text"]) for r in ROWS]
    for i,s in enumerate(stems):
        for p in stems[:i]:
            if s==p or SequenceMatcher(None,s,p).ratio()>=.97: raise ValueError(f"duplicate stem: {s} / {p}")
    (BASE/"data/coordinate_geometry_verified_batch.json").write_text(json.dumps({"questions":ROWS},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (BASE/"data/coordinate_geometry_answer_ledger.json").write_text(json.dumps(LEDGER,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("WROTE",len(ROWS),dict(Counter(r["difficulty"] for r in ROWS)),"source",sum(r["source"]!=ORIGINAL for r in ROWS),"original",sum(r["source"]==ORIGINAL for r in ROWS))
if __name__=="__main__": main()
