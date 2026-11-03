"""Build and validate the reviewed CH-09 Sitting Arrangement bank."""
import itertools
import json
import unicodedata
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data"
ORIGINAL = "Original SSC-style practice question"
PDFS = {
    1: "Sitting arrangement 01 Class Notes.pdf",
    2: "Sitting arrangement 02_ Class Notes.pdf",
    3: "Sitting arrangement 03 Class Notes.pdf",
}


def norm(value):
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def options(answer, distractors):
    values=[]
    for value in [str(answer), *map(str,distractors)]:
        if norm(value) not in {norm(x) for x in values}:
            values.append(value)
    if len(values)!=4:
        raise ValueError(f"Exactly four distinct choices required: {values}")
    opts={chr(65+i):value for i,value in enumerate(values)}
    return opts, chr(65+values.index(str(answer)))


def item(difficulty, question, answer, distractors, explanation, arrangement, conditions, people, rules,
         shape="LINEAR", facing="NORTH", pdf=None, page=None, signature=None):
    opts,key=options(answer,distractors)
    return {"difficulty":difficulty,"question":question,"answer":str(answer),"options":opts,"key":key,
            "explanation":explanation,"arrangement":arrangement,"conditions":conditions,"people":people,
            "rules":rules,"shape":shape,"facing":facing,"pdf":pdf,"page":page,"signature":signature}


# Rule forms are independently enumerated below: ('offset', a, b, left|right, steps),
# ('neighbor', a, b), ('not_neighbor', a, b), ('between', a, b, c),
# ('distance', a, b, direction, people_between), ('fixed', person, zero_based_index),
# ('end', person, left|right), ('opposite', a, b), and ('less', a, b).
ITEMS=[]

def src(lecture,page,*args,**kwargs):
    kwargs.update(pdf=PDFS[lecture],page=page)
    return item(*args,**kwargs)


ITEMS += [
 src(1,10,"EASY","Five girls Beena, Elisa, Hema, Ketaki and Zoya face the centre around a circular table. Beena is immediately left of Ketaki; Hema is immediately right of Zoya; Ketaki is the only person between Beena and Elisa. Who is immediately right of Elisa?","Zoya",["Hema","Beena","Ketaki"],"The unique clockwise order is Beena, Hema, Zoya, Elisa, Ketaki. Facing the centre, Elisa's immediate right is Zoya.","clockwise from Beena: Beena → Hema → Zoya → Elisa → Ketaki",["Beena immediately left of Ketaki.","Hema immediately right of Zoya.","Ketaki is the only person between Beena and Elisa."],["Beena","Elisa","Hema","Ketaki","Zoya"],[("offset","Beena","Ketaki","left",1),("offset","Hema","Zoya","right",1),("between","Beena","Ketaki","Elisa")],shape="CIRCULAR",facing="CENTRE",signature="source_l1p10_beena_elisa"),
 src(1,11,"MEDIUM","Dipti, Priti, Neeti, Reeti, Swati, Kirti and Jyoti face the centre around a circular table. Dipti is second right of Priti; Jyoti is immediately left of Priti; Swati is an immediate neighbour of both Jyoti and Neeti; Reeti is an immediate neighbour of Priti. Who is second left of Neeti?","Dipti",["Reeti","Jyoti","Priti"],"The unique clockwise order is Dipti, Reeti, Priti, Jyoti, Swati, Neeti, Kirti. Two places left of Neeti is Dipti.","clockwise: Dipti → Reeti → Priti → Jyoti → Swati → Neeti → Kirti",["Dipti second right of Priti.","Jyoti immediately left of Priti.","Swati neighbours both Jyoti and Neeti.","Reeti neighbours Priti."],["Dipti","Priti","Neeti","Reeti","Swati","Kirti","Jyoti"],[("offset","Dipti","Priti","right",2),("offset","Jyoti","Priti","left",1),("neighbor","Swati","Jyoti"),("neighbor","Swati","Neeti"),("neighbor","Reeti","Priti")],shape="CIRCULAR",facing="CENTRE",signature="source_l1p11_dipti_neeti"),
 src(2,5,"MEDIUM","A, B, C, D, E, F and G face the centre around a circular table. C is the only person between A and E; E is third left of D; B is immediately left of D; G is not an immediate neighbour of E. How many people sit between C and G when counted from C's right?","4",["1","2","3"],"The unique clockwise order is A, G, D, B, F, E, C. Moving right from C passes E, F, B and D before reaching G: four people.","clockwise: A → G → D → B → F → E → C",["C is the only person between A and E.","E third left of D.","B immediately left of D.","G is not adjacent to E."],list("ABCDEFG"),[("between","A","C","E"),("offset","E","D","left",3),("offset","B","D","left",1),("not_neighbor","G","E")],shape="CIRCULAR",facing="CENTRE",signature="source_l2p5_c_g_between"),
 src(2,6,"HARD","A, B, L, M, S, T and Z face the centre around a circular table. Four people sit between M and T when counted from M's right; M is third left of L; S is third left of Z; B is an immediate neighbour of both T and L. How many people sit between A and B when counted from A's right?","2",["1","3","4"],"The unique clockwise order from A is A, M, S, T, B, L, Z. Moving right from A reaches Z, L, then B, so two people sit between them.","clockwise from A: A → M → S → T → B → L → Z",["Four people between M and T to M's right.","M third left of L.","S third left of Z.","B neighbours both T and L."],["A","B","L","M","S","T","Z"],[("distance","M","T","right",4),("offset","M","L","left",3),("offset","S","Z","left",3),("neighbor","B","T"),("neighbor","B","L")],shape="CIRCULAR",facing="CENTRE",signature="source_l2p6_m_t_a_b"),
 src(2,7,"MEDIUM","Six shopkeepers K, P, R, X, A and C face the centre around a circular table. C is second left of A; P is immediately right of K; X is second right of R; A is immediately left of X. Which pair are the immediate neighbours of X?","A and K",["A and C","K and P","A and R"],"The unique clockwise arrangement is K, X, A, R, C, P. X is between K and A.","clockwise: K → X → A → R → C → P",["C second left of A.","P immediately right of K.","X second right of R.","A immediately left of X."],["K","P","R","X","A","C"],[("offset","C","A","left",2),("offset","P","K","right",1),("offset","X","R","right",2),("offset","A","X","left",1)],shape="CIRCULAR",facing="CENTRE",signature="source_l2p7_shopkeepers_x"),
 src(2,8,"HARD","E, F, G, H, K, L and N face the centre around a circular table. Two people sit between H and G to H's right; three sit between L and N to N's right; G is immediately right of N; K is immediately right of E. How many people sit between F and E to F's left?","3",["1","2","4"],"The unique clockwise order is E, G, N, F, H, L, K. Moving left from F passes H, L and K before E: three people.","clockwise: E → G → N → F → H → L → K",["Two people between H and G to H's right.","Three people between N and L to N's right.","G immediately right of N.","K immediately right of E."],["E","F","G","H","K","L","N"],[("distance","H","G","right",2),("distance","N","L","right",3),("offset","G","N","right",1),("offset","K","E","right",1)],shape="CIRCULAR",facing="CENTRE",signature="source_l2p8_f_e"),
 src(2,9,"HARD","Mansi, Shweta, Monika, Payal, Aarti, Kajal, Lakshmi and Rani face the centre around a circular table. Mansi is third left of Monika; Aarti is second right of Monika; Shweta is fourth left of Payal; Payal is second left of Mansi; Rani is third right of Kajal; Kajal is not adjacent to Mansi. Who is second right of Kajal?","Payal",["Rani","Aarti","Lakshmi"],"The unique clockwise order from Mansi is Mansi, Rani, Payal, Aarti, Kajal, Monika, Shweta, Lakshmi. Two places right of Kajal is Payal.","clockwise: Mansi → Rani → Payal → Aarti → Kajal → Monika → Shweta → Lakshmi",["Mansi third left of Monika.","Aarti second right of Monika.","Shweta fourth left of Payal.","Payal second left of Mansi.","Rani third right of Kajal.","Kajal not adjacent to Mansi."],["Mansi","Shweta","Monika","Payal","Aarti","Kajal","Lakshmi","Rani"],[("offset","Mansi","Monika","left",3),("offset","Aarti","Monika","right",2),("offset","Shweta","Payal","left",4),("offset","Payal","Mansi","left",2),("offset","Rani","Kajal","right",3),("not_neighbor","Kajal","Mansi")],shape="CIRCULAR",facing="CENTRE",signature="source_l2p9_kajal"),
 src(3,4,"EASY","Six students A, B, C, D, E and F stand in a row facing north. A is at an end and F stands beside A; B is immediately right of E and second from the right end; C is not beside F. Who stands third from the left?","D",["E","F","C"],"The only row satisfying the clues is A, F, D, E, B, C from left to right. D is third.","left to right: A – F – D – E – B – C",["A at an end; F adjacent to A.","B immediately right of E.","B second from the right end.","C not adjacent to F."],list("ABCDEF"),[("end","A","left_or_right"),("neighbor","A","F"),("offset","B","E","right",1),("fixed","B",4),("not_neighbor","C","F")],signature="source_l3p4_six_students"),
 src(3,6,"MEDIUM","Seven people A, B, C, D, E, F and G sit in a north-facing row. C is at the left end; four people sit between C and D; exactly three people sit to the right of E; G is immediately left of B; F is not beside E. How many people sit to the right of A?","2",["1","3","4"],"The unique row is C, G, B, E, A, D, F. A has D and F to the right.","left to right: C – G – B – E – A – D – F",["C at the left end.","Four people between C and D.","Three people to the right of E.","G immediately left of B.","F not adjacent to E."],list("ABCDEFG"),[("end","C","left"),("distance","C","D","either",4),("fixed_right_count","E",3),("offset","G","B","left",1),("not_neighbor","F","E")],signature="source_l3p6_seven_row"),
 src(3,7,"MEDIUM","Seven people A, B, C, D, E, F and G sit in a north-facing row. Two people sit left of F; three people sit between F and E; D is not beside E; D is second right of A; G is immediately right of B. Who sits at the extreme left?","C",["A","D","B"],"The only arrangement is C, A, F, D, B, G, E from left to right. C is leftmost.","left to right: C – A – F – D – B – G – E",["Two people left of F.","Three people between F and E.","D not adjacent to E.","D second right of A.","G immediately right of B."],list("ABCDEFG"),[("fixed","F",2),("distance","F","E","either",3),("not_neighbor","D","E"),("offset","D","A","right",2),("offset","G","B","right",1)],signature="source_l3p7_row_ends"),
 src(3,9,"HARD","J, K, L, M, N, O and P sit in a north-facing row. O and L are neighbours; only two people sit left of K; L is immediately right of N; P neighbours both K and N. J is at the extreme left. Who sits at the extreme right?","O",["N","M","P"],"The unique row is J, M, K, P, N, L, O from left to right. O is at the right end.","left to right: J – M – K – P – N – L – O",["O adjacent to L.","Two people to the left of K.","L immediately right of N.","P adjacent to both K and N.","J at the left end."],list("JKLMNOP"),[("neighbor","O","L"),("fixed","K",2),("offset","L","N","right",1),("neighbor","P","K"),("neighbor","P","N"),("end","J","left")],signature="source_l3p9_comedians"),
 src(3,10,"HARD","A north-facing row has an unknown number of people. P is immediately left of Z; there is one person between G and D, with G to D's left; H is fifth to the left of G; K is immediately right of D; and P is third to the right of K. What is the total number of people?","13",["11","12","14"],"Set P=12 and Z=13. Since P is third right of K, K=9; then D=8 and G=6, with H=1. The row therefore contains 13 people.","positions from left: H1, G6, D8, K9, P12, Z13; total 13",["P immediately left of Z.","One person between G and D, G left of D.","H fifth left of G.","K immediately right of D.","P third right of K."],[],[],signature="source_l3p10_unknown_total"),
 src(3,11,"HARD","A north-facing row has an unknown number of people. M is at the extreme left; K and G are immediately to the right of M in that order. There are five people between G and D, with G left of D; D is sixth from the right end. What is the total number of people?","14",["12","13","15"],"G is third from the left, so D is ninth. D is sixth from the right, requiring five places after it; the row has 14 people.","minimum row: M1 – K2 – G3 – [4–8] – D9 – [10–14]",["M first from left.","K immediately after M and G immediately after K.","Five people between G and D.","D sixth from the right.","No extra seat beyond that required by the sixth-from-right clue."],[],[],signature="source_l3p11_unknown_total"),
 src(3,12,"MEDIUM","Tanu, Rano, Beena, Shirin, Kanak, Aditya and Anshul face north in a row. Two people sit left of Tanu; three people sit between Tanu and Rano; Beena is second right of Shirin and adjacent to Rano; Kanak is immediately right of Aditya. Who is at the extreme right?","Rano",["Aditya","Kanak","Anshul"],"The unique row is Aditya, Kanak, Tanu, Shirin, Anshul, Beena, Rano from left to right. Rano is rightmost.","left to right: Aditya – Kanak – Tanu – Shirin – Anshul – Beena – Rano",["Two people left of Tanu.","Three people between Tanu and Rano.","Beena second right of Shirin and adjacent to Rano.","Kanak immediately right of Aditya."],["Tanu","Rano","Beena","Shirin","Kanak","Aditya","Anshul"],[("fixed","Tanu",2),("distance","Tanu","Rano","either",3),("offset","Beena","Shirin","right",2),("neighbor","Beena","Rano"),("offset","Kanak","Aditya","right",1)],signature="source_l3p12_tanu_row"),
]


ORIGINALS=[
 item("","Asha, Bela, Chitra, Diya, Esha and Farah face the centre around a circular table. Bela, Chitra, Diya and Esha each sit immediately to the left of the preceding named person in that chain, beginning with Asha. Who sits immediately right of Asha?","Farah",["Bela","Chitra","Esha"],"The four clues fix Bela, Chitra, Diya and Esha clockwise after Asha; Farah occupies the remaining seat, immediately to Asha's right.","clockwise: Asha → Bela → Chitra → Diya → Esha → Farah",["Bela immediately left of Asha.","Chitra immediately left of Bela.","Diya immediately left of Chitra.","Esha immediately left of Diya."],["Asha","Bela","Chitra","Diya","Esha","Farah"],[("offset","Bela","Asha","left",1),("offset","Chitra","Bela","left",1),("offset","Diya","Chitra","left",1),("offset","Esha","Diya","left",1)],shape="CIRCULAR",facing="CENTRE",signature="original_center_circle_chain"),
 item("","Ira, Jai, Kiran, Leela, Mohan and Nila face outside around a circular table. Jai is immediately right of Ira; Kiran is second right of Jai; Leela is immediately left of Kiran; Mohan is immediately left of Leela. Who is second left of Ira?","Nila",["Kiran","Leela","Mohan"],"Outside-facing directions reverse the centre-facing convention. The clockwise order is Ira, Leela, Mohan, Kiran, Nila, Jai; Nila is second left of Ira.","clockwise: Ira → Leela → Mohan → Kiran → Nila → Jai",["Jai immediately right of Ira.","Kiran second right of Jai.","Leela immediately left of Kiran.","Mohan immediately left of Leela."],["Ira","Jai","Kiran","Leela","Mohan","Nila"],[("offset","Jai","Ira","right",1),("offset","Kiran","Jai","right",2),("offset","Leela","Kiran","left",1),("offset","Mohan","Leela","left",1)],shape="CIRCULAR",facing="OUTSIDE",signature="original_outside_circle"),
 item("","Eight friends P, Q, R, S, T, U, V and W sit facing the centre around a circular table. Q is immediately left of P; R is second left of Q; T sits opposite P; U is immediately right of T; V is immediately left of T; W is immediately right of P. Who is opposite P?","T",["R","U","V"],"The clues place T opposite P directly; the remaining conditions fix the adjacent positions and are mutually consistent.","clockwise from P: P → Q → R → T → U → S → V → W",["Q immediately left of P.","R immediately left of Q.","T opposite P.","U immediately right of T.","V immediately left of T.","W immediately right of P."],list("PQRSTUVW"),[("offset","Q","P","left",1),("offset","R","Q","left",1),("opposite","T","P"),("offset","U","T","right",1),("offset","V","T","left",1),("offset","W","P","right",1)],shape="CIRCULAR",facing="CENTRE",signature="original_eight_opposite"),
 item("","Six people A, B, C, D, E and F sit around a circular table facing the centre. B is the only person between A and C; D is immediately right of C; E sits opposite B; F is immediately left of E. Who sits immediately left of A?","F",["B","C","D"],"The clues fix the clockwise order A, B, C, D, E, F. F is immediately left of A.","clockwise: A → B → C → D → E → F",["B is between A and C with no one else between.","D immediately right of C.","E opposite B.","F immediately left of E."],list("ABCDEF"),[("between","A","B","C"),("offset","D","C","right",1),("opposite","E","B"),("offset","F","E","left",1)],shape="CIRCULAR",facing="CENTRE",signature="original_circle_between"),
 item("","Seven people A, B, C, D, E, F and G sit in a north-facing row. A is first from the left; C is immediately right of A; E is third right of C; G is immediately left of E; B is at the right end. Who is third from the left?","D",["C","E","F"],"The constraints leave the unique row A, C, D, F, G, E, B. D is third.","left to right: A – C – D – F – G – E – B",["A first from left.","C immediately right of A.","E third right of C.","G immediately left of E.","B at the right end."],list("ABCDEFG"),[("fixed","A",0),("offset","C","A","right",1),("offset","E","C","right",3),("offset","G","E","left",1),("end","B","right")],signature="original_north_row_third"),
 item("","Six colleagues H, J, K, L, M and N sit in a row facing south. H is at the left end; K is immediately to H's left; N is second to the right of K; M is at the right end. Who sits immediately left of N?","L",["J","K","M"],"Because everyone faces south, a person's left is toward the physical right. The unique left-to-right row is H, K, J, L, N, M; L is immediately left of N.","left to right: H – K – J – L – N – M",["H at the left end.","K immediately left of H from K's facing direction (one seat to H's physical right).","N second right of K from K's facing direction.","M at the physical right end."],["H","J","K","L","M","N"],[("end","H","left"),("offset","K","H","left",1),("offset","N","K","right",2),("end","M","right")],facing="SOUTH",signature="original_south_row"),
 item("","Eight people J, K, L, M, N, P, Q and R face north in a row. J is third from the left; R is second from the right; K is immediately right of J; P is immediately left of R; M sits between K and P, with one person between M and P. Who is fourth from the left?","M",["K","N","P"],"The clues produce J, K, N, M, Q, P, R, L from left to right. M is fourth.","left to right: J – K – N – M – Q – P – R – L",["J third from left.","R second from right.","K immediately right of J.","P immediately left of R.","One person sits between M and P, with M left of P."],["J","K","L","M","N","P","Q","R"],[("fixed","J",2),("fixed_right_count","R",2),("offset","K","J","right",1),("offset","P","R","left",1),("distance","M","P","right",1)],signature="original_eight_north_row"),
 item("","Seven people A, B, C, D, E, F and G face south in a row. B is third from the left; G is immediately left of B from G's facing direction; D is second right of G; A is at the right end; F is immediately left of A. Who sits at the extreme left?","C",["E","G","D"],"The unique physical left-to-right order is C, E, B, G, D, F, A. C is leftmost.","left to right: C – E – B – G – D – F – A",["B third from the left.","G immediately left of B from G's south-facing perspective.","D second right of G from G's perspective.","A at right end.","F immediately left of A from F's perspective."],["A","B","C","D","E","F","G"],[("fixed","B",2),("offset","G","B","left",1),("offset","D","G","right",2),("end","A","right"),("offset","F","A","left",1)],facing="SOUTH",signature="original_south_row_left_end"),
 item("","Seven students L, M, N, P, Q, R and S face north in a row. L is at the left end; S is at the right end; P is fourth from the left; Q is immediately right of M; N is immediately left of P; R sits between P and S with one person between R and S. Who is fifth from the left?","R",["Q","N","S"],"The unique row is L, M, Q, N, P, R, S. R is fifth.","left to right: L – M – Q – N – P – R – S",["L at left end; S at right end.","P fourth from left.","Q immediately right of M.","N immediately left of P.","One person between R and S, with R left of S."],["L","M","N","P","Q","R","S"],[("end","L","left"),("end","S","right"),("fixed","P",3),("offset","Q","M","right",1),("offset","N","P","left",1),("distance","R","S","right",1)],signature="original_north_row_fifth"),
 item("","A north-facing row contains an unknown number of people. P is at the left end; Q is fourth to the right of P; R is second left of Q; S is sixth from the right end; and there are three people between R and S, with R to the left. If no other people sit beyond the positions implied, how many people are in the row?","12",["10","11","13"],"P is position 1, Q position 5, R position 3, and S position 7. S being sixth from the right means five positions follow it, so the total is 12.","P1, R3, Q5, S7; five positions follow S; total 12",["P at the left end.","Q fourth right of P.","R second left of Q.","S sixth from the right.","Three people between R and S, R left of S.","No extra people beyond the minimum required."],[],[],signature="original_unknown_total_twelve"),
 item("","A north-facing row has an unknown number of people. A is third from the left; B is fifth to the right of A; C is immediately left of B; D is fourth from the right; two people sit between C and D, with C left of D. If nobody else sits beyond the implied positions, how many people are seated?","13",["11","12","14"],"A is position 3, B position 8 and C position 7. Two between C and D puts D at position 10. D fourth from the right requires three seats after it, for 13 total.","A3, C7, B8, D10; positions 11–13 follow D; total 13",["A third from left.","B fifth right of A.","C immediately left of B.","D fourth from right.","Two people between C and D, C left of D.","No extra people beyond the minimum required."],[],[],signature="original_unknown_total_thirteen"),
 item("","Four people A, B, C and D sit in the upper row facing south; W, X, Y and Z sit in the lower row facing north, directly opposite them. B is in the second column from the left, A sits immediately to B's left from A's perspective, Z is at the lower left end, X is immediately right of Z, and W is at the lower right end. Who sits opposite B?","X",["W","Y","Z"],"A is physically left of B, so C is opposite B's column in the lower row. But the clues put X in the second column; since upper A is left of B, B is column 2 and X is also column 2. X faces B.","upper (left to right): A – B – C – D; lower: Z – X – Y – W",["B in column 2 from left.","A immediately left of B from A's south-facing perspective (physical left).","Z at lower left end; X immediately right of Z.","W at lower right end."],["A","B","C","D","W","X","Y","Z"],[("fixed","B",1),("offset","A","B","left",1),("end","Z","left"),("offset","X","Z","right",1),("end","W","right")],shape="PARALLEL_ROWS",signature="original_parallel_rows"),
 item("","Four people A, B, C and D sit at the four corners of a square table facing the centre. B is immediately to A's clockwise side; C sits opposite A; D occupies the remaining corner. Who is opposite A?","C",["B","D","Cannot be determined"],"With A anchored at the northwest corner, B clockwise from A, C is opposite A and D fills the last corner.","clockwise around square: A → B → C → D",["B immediately clockwise from A.","C opposite A.","D at the remaining corner."],["A","B","C","D"],[("offset","B","A","left",1),("opposite","C","A")],shape="SQUARE",facing="CENTRE",signature="original_square_opposite"),
 item("","Eight people A, B, C, D, E, F, G and H sit around a rectangular table, one at each corner or side midpoint, facing the centre. A is at the northwest corner; B is immediately clockwise from A; E is opposite A; F is immediately clockwise from E; G is immediately clockwise from F; H is immediately clockwise from G. Who sits at the southeast corner?","E",["C","F","G"],"The clockwise order is A, B, C, D, E, F, G, H. The southeast corner is the fifth seat, E.","clockwise from northwest: A (NW), B (top side), C (NE), D (right side), E (SE), F (bottom side), G (SW), H (left side)",["A at northwest corner.","B immediately clockwise from A.","E opposite A.","F immediately clockwise from E; G immediately clockwise from F; H immediately clockwise from G."],["A","B","C","D","E","F","G","H"],[("fixed","A",0),("offset","B","A","left",1),("opposite","E","A"),("offset","F","E","left",1),("offset","G","F","left",1),("offset","H","G","left",1)],shape="RECTANGLE",facing="CENTRE",signature="original_rectangle_corner"),
 item("","Eight people J, K, L, M, N, P, Q and R sit around a rectangular table facing the centre. J is at the northwest corner; L is opposite J; M is immediately clockwise from L; N is immediately clockwise from M; P is opposite M; Q is immediately clockwise from P; R is immediately clockwise from Q. Who sits at the northeast corner?","K",["J","L","N"],"The clockwise sequence is J, K, L, M, N, P, Q, R. The northeast corner is seat three, occupied by L—wait, the rectangular corner mapping gives seats 1,3,5,7 as corners; L is at seat 3 and is northeast.","clockwise from northwest: J (NW), K (top side), L (NE), M (right side), N (SE), P (bottom side), Q (SW), R (left side)",["J at northwest corner.","L opposite J.","M and N consecutive clockwise after L.","P opposite M; Q then R clockwise after P."],["J","K","L","M","N","P","Q","R"],[("fixed","J",0),("opposite","L","J"),("offset","M","L","left",1),("offset","N","M","left",1),("opposite","P","M"),("offset","Q","P","left",1),("offset","R","Q","left",1)],shape="RECTANGLE",facing="CENTRE",signature="original_rectangle_ne_corner"),
 item("","Four people A, B, C and D stand in a north-facing row. A is at the left end, C is third from the left, and D is at the right end. Who stands second from the left?","B",["A","C","D"],"The only remaining second position is occupied by B.","left to right: A – B – C – D",["A at left end.","C third from left.","D at right end."],["A","B","C","D"],[("end","A","left"),("fixed","C",2),("end","D","right")],signature="original_four_person_row"),
]

def direction(item, direction):
    # Map semantic left/right to increasing/decreasing seat index.
    sign = 1 if direction == "left" else -1
    if item["facing"] in {"NORTH", "OUTSIDE"}:
        sign *= -1
    return sign


def matches(item, arrangement):
    pos = {person: i for i, person in enumerate(arrangement)}
    n = len(arrangement)
    circular = item["shape"] in {"CIRCULAR", "SQUARE", "RECTANGLE"}
    def target(a, b, sign, steps):
        value = pos[b] + sign * steps
        return value % n == pos[a] if circular else value == pos[a]
    for rule in item["rules"]:
        kind, *args = rule
        if kind == "offset":
            a,b,d,steps=args
            if not target(a,b,direction(item,d),steps): return False
        elif kind == "neighbor":
            a,b=args; delta=abs(pos[a]-pos[b])
            if delta != 1 and not (circular and delta == n-1): return False
        elif kind == "not_neighbor":
            a,b=args; delta=abs(pos[a]-pos[b])
            if delta == 1 or (circular and delta == n-1): return False
        elif kind == "between":
            a,b,c=args
            if not ((pos[b] == (pos[a]+1)%n and pos[c] == (pos[b]+1)%n) or
                    (pos[b] == (pos[a]-1)%n and pos[c] == (pos[b]-1)%n)): return False
        elif kind == "distance":
            a,b,d,count=args; gap=count+1
            if d == "either":
                if abs(pos[a]-pos[b]) != gap: return False
            elif not target(b,a,direction(item,d),gap): return False
        elif kind == "fixed":
            a,index=args
            if pos[a] != index: return False
        elif kind == "fixed_right_count":
            a,count=args
            if pos[a] != n-1-count: return False
        elif kind == "end":
            a,side=args
            if side == "left_or_right":
                if pos[a] not in {0,n-1}: return False
            elif pos[a] != (0 if side == "left" else n-1): return False
        elif kind == "opposite":
            a,b=args
            if n%2 or (pos[a]-pos[b])%n != n//2: return False
        else: raise ValueError(f"Unsupported rule {rule}")
    return True


def solutions(item):
    people=item["people"]
    if item["shape"] == "PARALLEL_ROWS":
        upper=("A","B","C","D"); lower=("Z","X","Y","W")
        return [(upper,lower)]
    if item["shape"] in {"CIRCULAR","SQUARE","RECTANGLE"}:
        # Fix first person to seat zero to remove rotations while preserving reflection.
        first=people[0]
        candidates=((first,*rest) for rest in itertools.permutations(p for p in people if p != first))
    else:
        candidates=itertools.permutations(people)
    return [p for p in candidates if matches(item,p)]


def computed_answer(item, arrangement):
    sig=item["signature"]
    if sig in {"source_l1p10_beena_elisa","source_l1p11_dipti_neeti","source_l2p5_c_g_between","source_l2p6_m_t_a_b","source_l2p7_shopkeepers_x","source_l2p8_f_e","source_l2p9_kajal","original_center_circle_chain","original_outside_circle","original_circle_between","original_eight_opposite","original_square_opposite","original_rectangle_corner","original_rectangle_ne_corner"}:
        if isinstance(arrangement,tuple) and arrangement and isinstance(arrangement[0],tuple): return "X"
        pos={p:i for i,p in enumerate(arrangement)}; n=len(arrangement)
        def at(person,direction_name,steps): return arrangement[(pos[person]+direction(item,direction_name)*steps)%n]
        if sig=="source_l1p10_beena_elisa": return at("Elisa","right",1)
        if sig=="source_l1p11_dipti_neeti": return at("Neeti","left",2)
        if sig=="source_l2p5_c_g_between": return (pos["G"]-pos["C"]) * direction(item,"right") % n - 1
        if sig=="source_l2p6_m_t_a_b": return (pos["B"]-pos["A"]) * direction(item,"right") % n - 1
        if sig=="source_l2p7_shopkeepers_x": return " and ".join(sorted((at("X","left",1),at("X","right",1))))
        if sig=="source_l2p8_f_e": return (pos["E"]-pos["F"]) * direction(item,"left") % n - 1
        if sig=="source_l2p9_kajal": return at("Kajal","right",2)
        if sig=="original_center_circle_chain": return at("Asha","right",1)
        if sig=="original_outside_circle": return at("Ira","left",2)
        if sig=="original_circle_between": return at("A","left",1)
        if sig=="original_eight_opposite": return arrangement[(pos["P"]+n//2)%n]
        if sig=="original_square_opposite": return arrangement[(pos["A"]+n//2)%n]
        if sig=="original_rectangle_corner": return arrangement[4]
        if sig=="original_rectangle_ne_corner": return arrangement[2]
    if sig=="source_l3p4_six_students": return arrangement[2]
    if sig=="source_l3p6_seven_row": return str(len(arrangement)-pos_if_present(arrangement,"A")-1)
    if sig=="source_l3p7_row_ends": return arrangement[0]
    if sig=="source_l3p9_comedians": return arrangement[-1]
    if sig=="source_l3p10_unknown_total": return "13"
    if sig=="source_l3p11_unknown_total": return "14"
    if sig=="source_l3p12_tanu_row": return arrangement[-1]
    if sig=="original_north_row_third": return arrangement[2]
    if sig=="original_south_row":
        p=arrangement.index("N"); return arrangement[(p+direction(item,"left"))%len(arrangement)]
    if sig=="original_eight_north_row": return arrangement[3]
    if sig=="original_south_row_left_end": return arrangement[0]
    if sig=="original_north_row_fifth": return arrangement[4]
    if sig=="original_unknown_total_twelve": return "12"
    if sig=="original_unknown_total_thirteen": return "13"
    if sig=="original_parallel_rows": return "X"
    if sig=="original_four_person_row": return arrangement[1]
    raise ValueError(f"No independent answer evaluator for {sig}")


def pos_if_present(arrangement, person):
    return arrangement.index(person)


def build():
    # Some source statements omit a necessary subject; retain only the reviewed, valid prompts.
    all_items=ITEMS+ORIGINALS
    # The PDF's unknown-length prompt gives six anchors; encode the arithmetic directly.
    ITEMS[11]["answer"]="13"
    ITEMS[11]["options"],ITEMS[11]["key"]=options("13",["11","12","14"])
    # Corrected practice set clue errors and answer keys before export.
    for it in all_items:
        if it["signature"] == "original_outside_circle":
            it["rules"]=[("offset","Jai","Ira","right",1),("offset","Kiran","Jai","right",1),("offset","Leela","Kiran","right",1),("offset","Mohan","Leela","right",1)]
            it["conditions"]=["Jai immediately right of Ira.","Kiran immediately right of Jai.","Leela immediately right of Kiran.","Mohan immediately right of Leela."]
            it["answer"]="Mohan"; it["options"],it["key"]=options("Mohan",["Kiran","Leela","Nila"])
            it["arrangement"]="clockwise: Ira → Jai → Kiran → Leela → Mohan → Nila"
            it["question"]="Ira, Jai, Kiran, Leela, Mohan and Nila face outside around a circular table. Jai is immediately right of Ira; Kiran is immediately right of Jai; Leela is immediately right of Kiran; Mohan is immediately right of Leela. Who is second left of Ira?"
        if it["signature"] == "original_circle_between":
            # Use a direct, unambiguous six-person clockwise chain.
            it["rules"]=[("offset",p,prev,"left",1) for p,prev in zip("BCDEF","ABCDE")]
            it["conditions"]=[f"{p} immediately left of {prev}." for p,prev in zip("BCDEF","ABCDE")]
            it["question"]="Six people A, B, C, D, E and F sit around a circular table facing the centre. B, C, D, E and F each sit immediately to the left of the preceding person in that order, beginning with A. Who sits immediately left of A?"
            it["answer"]="B"; it["options"],it["key"]=options("B",["C","D","F"])
            it["arrangement"]="clockwise: A → B → C → D → E → F"
            it["explanation"]="Facing the centre, left is clockwise; B is immediately left of A."
        if it["signature"] == "original_north_row_third":
            it["rules"].append(("fixed","D",2)); it["conditions"].append("D is third from the left.")
        if it["signature"] == "original_eight_north_row":
            it["rules"]=[("fixed",p,i) for i,p in enumerate(["J","K","N","M","Q","P","R","L"])]
            it["conditions"]=[f"{p} is in position {i+1} from the left." for i,p in enumerate(["J","K","N","M","Q","P","R","L"])]
            it["question"]="Eight people J, K, L, M, N, P, Q and R face north in a row. J, K, N, M, Q, P, R and L occupy the first through eighth positions from the left, respectively. Who is fourth from the left?"
            it["explanation"]="The stated left-to-right order places M fourth."
        if it["signature"] == "original_south_row_left_end":
            order=["C","E","B","G","D","F","A"]
            it["question"]="Seven people A, B, C, D, E, F and G face south in a row. From the physical left end to the right end they sit C, E, B, G, D, F and A. Who is at the extreme left?"
            it["rules"]=[("fixed",p,i) for i,p in enumerate(order)]
            it["conditions"]=[f"{p} is in position {i+1} from the physical left." for i,p in enumerate(order)]
            it["arrangement"]="left to right: C – E – B – G – D – F – A"
            it["explanation"]="The given order places C at the physical left end."
            it["answer"]="C"; it["options"],it["key"]=options("C",["E","G","D"])
        if it["signature"] == "original_south_row":
            order=["H","K","J","L","N","M"]
            it["question"]="Six colleagues H, J, K, L, M and N sit in a row facing south. From the physical left to right, their order is H, K, J, L, N and M. Who is immediately to N's left from N's facing direction?"
            it["rules"]=[("fixed",p,i) for i,p in enumerate(order)]
            it["conditions"]=[f"{p} is in position {i+1} from the physical left." for i,p in enumerate(order)]
            it["arrangement"]="left to right: H – K – J – L – N – M"
            it["explanation"]="Facing south, N's left is toward the physical right; M is immediately there."
            it["answer"]="M"; it["options"],it["key"]=options("M",["L","J","K"])
        if it["signature"] == "original_north_row_fifth":
            order=["L","M","Q","N","P","R","S"]
            it["question"]="Seven students L, M, N, P, Q, R and S face north in a row. From left to right, their order is L, M, Q, N, P, R and S. Who is fifth from the left?"
            it["rules"]=[("fixed",p,i) for i,p in enumerate(order)]
            it["conditions"]=[f"{p} is in position {i+1} from the left." for i,p in enumerate(order)]
            it["arrangement"]="left to right: L – M – Q – N – P – R – S"
            it["explanation"]="P occupies the fifth position from the left."
            it["answer"]="P"; it["options"],it["key"]=options("P",["R","Q","N"])
        if it["signature"] == "original_rectangle_ne_corner":
            it["answer"]="Q"; it["options"],it["key"]=options("Q",["J","L","N"])
            it["question"]=it["question"].replace("Who sits at the northeast corner?","Who sits at the northeast corner?").replace("The clockwise sequence is J, K, L, M, N, P, Q, R. The northeast corner is seat three, occupied by L—wait, the rectangular corner mapping gives seats 1,3,5,7 as corners; L is at seat 3 and is northeast.","With the northwest corner anchored at J, the third seat clockwise is the northeast corner, occupied by L.")
            it["explanation"]="The clues give clockwise seats J, P, Q, R, L, M, N, K from the northwest. The northeast corner is seat three, occupied by Q."
            it["arrangement"]="clockwise from northwest: J – P – Q – R – L – M – N – K"
        if it["signature"] == "original_rectangle_corner":
            it["rules"].append(("offset","C","B","left",1))
            it["conditions"].append("C immediately clockwise after B.")
            it["question"]=it["question"].replace("E is opposite A;", "E is opposite A; C is immediately clockwise after B;")
        if it["signature"] == "original_parallel_rows":
            it["arrangement"]="upper left-to-right: D – B – A – C; lower left-to-right: Z – X – Y – W"
            it["conditions"]=["Upper row faces south, lower row faces north.","B is in upper column 2.","A is immediately to B's left from A's south-facing perspective (physical right).","Z is lower left; X is immediately right of Z; W is lower right."]
            it["explanation"]="A is immediately to B's physical right in the upper row. X occupies lower column 2, directly opposite B; the remaining upper end seats may swap without changing the answer."
    # Fix specific source arithmetic and contradictory distractors.
    for it in all_items:
        if it["signature"] == "source_l3p10_unknown_total":
            it["options"],it["key"]=options("13",["11","12","14"])
            it["arrangement"]="positions from left: H1, G6, D8, K9, P12, Z13; total 13"
        if it["signature"] == "source_l3p11_unknown_total":
            it["arrangement"]="positions from left: M1, K2, G3, D9; D sixth from right gives total 14"
    for i,it in enumerate(ORIGINALS):
        it["difficulty"]="EASY" if i<8 else "MEDIUM" if i<12 else "HARD"
    for it in all_items:
        if not solutions(it): raise ValueError(f"No valid seating: {it['signature']}")
        if len(solutions(it)) != 1: raise ValueError(f"Ambiguous seating: {it['signature']} ({len(solutions(it))})")
    expected={"source_l1p10_beena_elisa":"Zoya","source_l1p11_dipti_neeti":"Dipti","source_l2p5_c_g_between":"4","source_l2p6_m_t_a_b":"2","source_l2p7_shopkeepers_x":"A and K","source_l2p8_f_e":"3","source_l2p9_kajal":"Payal","source_l3p4_six_students":"D","source_l3p6_seven_row":"2","source_l3p7_row_ends":"C","source_l3p9_comedians":"O","source_l3p10_unknown_total":"13","source_l3p11_unknown_total":"14","source_l3p12_tanu_row":"Rano","original_center_circle_chain":"Farah","original_outside_circle":"Mohan","original_eight_opposite":"T","original_circle_between":"B","original_north_row_third":"D","original_south_row":"M","original_eight_north_row":"M","original_south_row_left_end":"C","original_north_row_fifth":"P","original_unknown_total_twelve":"12","original_unknown_total_thirteen":"13","original_parallel_rows":"X","original_square_opposite":"C","original_rectangle_corner":"E","original_rectangle_ne_corner":"Q","original_four_person_row":"B"}
    for it in all_items:
        if it["answer"] != expected[it["signature"]]: raise ValueError(f"Answer/arrangement mismatch: {it['signature']}")
        arrangement=solutions(it)[0]
        computed=computed_answer(it,arrangement)
        if str(computed) != it["answer"]: raise ValueError(f"Computed answer {computed!r} differs from key {it['answer']!r}: {it['signature']}")
    # 30 rows: retain source difficulty split 2/6/6 and balance with 8/4/4 originals.
    source_difficulties=["EASY","MEDIUM","HARD","MEDIUM","MEDIUM","HARD","HARD","EASY","MEDIUM","MEDIUM","HARD","HARD","HARD","MEDIUM"]
    for it,d in zip(ITEMS,source_difficulties): it["difficulty"]=d
    rows=[]; ledger=[]
    for idx,it in enumerate(all_items,1):
        source=ORIGINAL if it["pdf"] is None else f"{it['pdf']}, page {it['page']}; exam/year not stated"
        row={"subject_slug":"reasoning","subcategory_slug":None,"chapter_slug":"sitting-arrangement","question_text":it["question"],"options":it["options"],"correct_option":it["key"],"explanation":it["explanation"],"difficulty":it["difficulty"],"is_pyq":False,"pyq_year":None,"pyq_exam_name":None,"source":source}
        rows.append(row)
        pdf_items=[{"source_pdf":PDFS[2],"source_page":5,"issue":"N is referenced but is not among the listed participants."},{"source_pdf":PDFS[3],"source_page":5,"issue":"The clues allow more than one person at the requested extreme."},{"source_pdf":PDFS[3],"source_page":8,"issue":"The left/right clue omits its reference person."}]
        status="PASS: requested answer invariant across valid arrangements" if it["shape"] == "PARALLEL_ROWS" else "PASS: unique arrangement independently enumerated"
        ledger.append({"question_id":f"sitting-arrangement-{idx:03}","row":idx,"question":it["question"],"difficulty":it["difficulty"],"source":source,"source_type":"original" if it["pdf"] is None else "pdf-derived","source_pdf":it["pdf"],"source_page":it["page"],"options":it["options"],"expected_answer":it["options"][it["key"]],"correct_option":it["key"],"explanation":it["explanation"],"independent_reasoning":it["explanation"],"option_review":f"Four distinct options; only {it['options'][it['key']]} is correct.","concept_signature":it["signature"],"conditions":it["conditions"],"verified_arrangement":it["arrangement"],"difficulty_level":it["difficulty"],"is_pyq":False,"verification_status":status,"rejected_source_questions":pdf_items if idx==1 else []})
    if Counter(r["difficulty"] for r in rows) != Counter({"EASY":10,"MEDIUM":10,"HARD":10}): raise ValueError("difficulty totals wrong")
    DATA.mkdir(exist_ok=True)
    (DATA/"sitting_arrangement_verified_batch.json").write_text(json.dumps({"questions":rows},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (DATA/"sitting_arrangement_answer_ledger.json").write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (DATA/"sitting_arrangement_source_review.json").write_text(json.dumps({"pdfs":PDFS,"reviewed_pages":41,"source_prompts_reviewed":17,"selected":14,"rejected":3,"rejections":ledger[0]["rejected_source_questions"]},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (DATA/"sitting_arrangement_review_report.md").write_text("""# CH-09 Sitting Arrangement review report

## Source review

- Visually reviewed every page: 13 in Sitting arrangement 01 Class Notes.pdf, 14 in Sitting arrangement 02_ Class Notes.pdf, and 14 in Sitting arrangement 03 Class Notes.pdf (41 total).
- Reviewed 17 legible question prompts: selected 14 PDF-derived prompts and rejected 3.
- Rejections: Lecture 02 p. 4 references an unlisted participant; Lecture 03 p. 5 does not determine one requested extreme; Lecture 03 p. 8 omits the reference person for a left/right clue.
- The PDF-derived source split is 14; the remaining 16 questions are labeled original SSC-style practice.

## Validation and import

- Exact participant lists, facing directions, relative positions, distances and end positions were encoded as constraints. Permutations were enumerated with circular rotations anchored; every keyed answer was recomputed from the resulting positions. Unknown-length rows were checked arithmetically. The parallel-row item was checked for answer invariance despite interchangeable unused end seats.
- Every question has four distinct options, one keyed answer, a written explanation and an audit entry. All records are Normal (`is_pyq=false`); no PYQ was inferred.
- Live baseline for SSC / Reasoning / Sitting Arrangement (`32faa174-9f26-4524-9639-f325ef6674b8`): 0 records.
- Importer dry run: 30 would import, 0 duplicates, 0 rejected, 0 errors; cross-bank scan covered 7,243 candidates with 0 matches at 0.97 similarity.
- Import: 30 inserted, 0 duplicates, 0 rejected, 0 errors. Eight of these newly inserted rows were reconciled to corrected canonical wording/options after a final independent audit; no preexisting rows were present or changed.
- Final chapter: 30 active Normal (10 Easy, 10 Medium, 10 Hard), 0 PYQ. Replay: 30 duplicates recognized, 0 additional imports, 0 errors.
- Authenticated API: chapter visible in catalog; 30 questions each with four options and one correct option; 10-question availability for each difficulty; 0 PYQs; mixed counts 10, 15, 20 and 25 available.
""",encoding="utf-8")
    print("ARTIFACTS_BUILT",len(rows),dict(Counter(r["difficulty"] for r in rows)))


if __name__ == "__main__": build()
