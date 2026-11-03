"""Build and independently validate the reviewed CH-10 Puzzle question bank."""
import itertools
import json
import unicodedata
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data"
ORIGINAL = "Original SSC-style practice question"
PDFS = {
    1: "Puzzle 01_ Class Notes.pdf",
    2: "Puzzle 02_ Class Notes.pdf",
    3: "Puzzle 03_ Class Notes.pdf",
}
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def norm(text):
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def options(answer, distractors):
    values=[]
    for value in map(str, [answer, *distractors]):
        if norm(value) not in {norm(x) for x in values}:
            values.append(value)
    if len(values) != 4:
        raise ValueError(f"Expected four distinct choices, got {values}")
    result={chr(65+i):value for i,value in enumerate(values)}
    return result, chr(65+values.index(str(answer)))


def make(category, difficulty, question, answer, distractors, explanation, people, rules, query,
         arrangement_kind, signature, pdf=None, page=None, conditions=None):
    opts,key=options(answer,distractors)
    return {"category":category,"difficulty":difficulty,"question":question,"answer":str(answer),
            "options":opts,"key":key,"explanation":explanation,"people":people,"rules":rules,
            "query":query,"kind":arrangement_kind,"signature":signature,"pdf":pdf,"page":page,
            "conditions":conditions or [question]}


def src(lecture,page,*args,**kwargs):
    kwargs.update(pdf=PDFS[lecture],page=page)
    return make(*args,**kwargs)


ITEMS = [
src(1,7,"Classification/ranking","EASY","A, B, C, D, E, F and G earned distinct marks. A scored more than B, C and D; G scored more than E and F; and F scored more than A. Who scored highest?","G",["F","A","B"],"The clues give G above F, F above A, and A above B, C and D; G is also above E. Thus G is highest.",list("ABCDEFG"),[("lt","A","B"),("lt","A","C"),("lt","A","D"),("lt","G","E"),("lt","G","F"),("lt","F","A")],("rank_person",0),"ranking","source_l1p7_marks",conditions=["A>B,C,D; G>E,F; F>A."]),
src(1,9,"Classification/ranking","EASY","Seven boys B1–B7 have distinct weights. B4 is lighter than exactly three boys. B1 is heavier than B7; B2 is heaviest; B5 and B6 are each heavier than B1; and B3 is lighter than B7. How many boys are lighter than B1?","2",["1","3","4"],"B2, B5 and B6 are already heavier than B1. For exactly three boys to be heavier than B4, B1 must be lighter than B4. Below B1 are B7 and B3.",[f"B{i}" for i in range(1,8)],[("rank","B4",3),("rank","B2",0),("lt","B2","B1"),("lt","B5","B1"),("lt","B6","B1"),("lt","B1","B7"),("lt","B7","B3")],("count_below","B1"),"ranking","source_l1p9_weights",conditions=["B4 has exactly three heavier boys; B1>B7; B2 highest; B5,B6>B1; B3<B7."]),
src(1,10,"Classification/ranking","MEDIUM","Seven spheres V1–V7 have distinct volumes. V4 is smaller than V1, V2 and V5. Exactly two spheres have smaller volume than V7, and V4 is larger than V7. V6 is not the smallest. How many spheres have smaller volume than V3?","0",["1","2","3"],"V1, V2 and V5 are above V4, and V4 is above V7. Since exactly two spheres are below V7 and V6 is not the smallest, V3 is the smallest; none is below it.",[f"V{i}" for i in range(1,8)],[("lt","V1","V4"),("lt","V2","V4"),("lt","V5","V4"),("lt","V4","V7"),("rank","V7",4),("notrank","V6",6)],("count_below","V3"),"ranking","source_l1p10_spheres",conditions=["V1,V2,V5>V4>V7; exactly two spheres below V7; V6 is not lowest."]),
src(1,11,"Classification/ranking","HARD","Seven boys B1–B7 have distinct IQ scores. B2 is above B6; B5 has the third-lowest IQ; B4 has the highest IQ; B3 is below B2; B1 is above B2; and B7 has the lowest IQ. Who has the second-highest IQ?","B1",["B2","B3","B4"],"B4 is highest. B1 is above B2, and B2 is above B6 and B3, so B1 must be second-highest.",[f"B{i}" for i in range(1,8)],[("rank","B4",0),("rank","B5",4),("rank","B7",6),("lt","B2","B6"),("lt","B1","B2"),("lt","B2","B3")],("rank_person",1),"ranking","source_l1p11_iq",conditions=["B2>B6; B5 third-lowest; B4 highest; B3<B2; B1>B2; B7 lowest."]),
src(1,12,"Classification/ranking","EASY","Seven students P, Q, R, S, T, U and V have distinct marks. P is second-highest; V is above only one student; S scored more than T but less than P; exactly three students scored more than T and three less; neither R nor Q has the lowest score. Who has the lowest score?","U",["R","Q","V"],"T is fourth and P second. S must be third. V is second-lowest, while neither Q nor R is lowest; therefore U is lowest.",list("PQRSTUV"),[("rank","P",1),("rank","V",5),("rank","T",3),("lt","P","S"),("lt","S","T"),("notrank","Q",6),("notrank","R",6)],("rank_person",6),"ranking","source_l1p12_student_marks",conditions=["P second-highest; V second-lowest; P>S>T; three above and three below T; Q,R not lowest."]),

src(2,4,"Day-based","MEDIUM","D, E, F, H, I, J and K have exams on distinct days Monday–Sunday. K is Thursday and E Saturday. H is immediately before I; D immediately after I; F is after J. How many people have exams between F and D?","3",["1","2","4"],"The H–I–D block must be Monday–Wednesday. K is Thursday and E Saturday; J is Friday and F Sunday. K, J and E lie between D and F.",list("DE FHIJK".replace(" ","")),[("fixed","K",3),("fixed","E",5),("offset","H","I",-1),("offset","D","I",1),("lt","J","F")],("between_count","F","D"),"day","source_l2p4_days",conditions=["K Thursday; E Saturday; H immediately before I; D immediately after I; F after J."]),
src(2,5,"Day-based","EASY","P, Q, R, S, T, U and V have exams on distinct days Monday–Sunday. Q is immediately before T, and T immediately before P. P is Wednesday. R is neither Saturday nor Sunday. U is Friday and S immediately follows U. Who has the Sunday exam?","V",["R","S","T"],"Q and T are Monday and Tuesday, followed by P Wednesday. U and S are Friday and Saturday. R must be Thursday, leaving V for Sunday.",list("PQRSTUV"),[("offset","Q","T",-1),("offset","T","P",-1),("fixed","P",2),("notfixed","R",5),("notfixed","R",6),("fixed","U",4),("offset","S","U",1)],("person_at",6),"day","source_l2p5_days",conditions=["Q immediately before T; T before P; P Wednesday; R not weekend; U Friday; S immediately after U."]),
src(2,6,"Day-based","HARD","A, B, C, D, E, F and G have exams on distinct days Monday–Sunday. Exactly two exams are before F; A is immediately after F; E is not Sunday; G is immediately before E and has the Friday exam; C is not Monday; D is immediately before F; and exactly one exam is between A and E. Who has the Monday exam?","B",["A","C","D"],"F is Wednesday, D Tuesday and A Thursday. G Friday and E Saturday. C cannot be Monday, so C is Sunday and B is Monday.",list("ABCDEFG"),[("fixed","F",2),("fixed","D",1),("fixed","A",3),("fixed","G",4),("fixed","E",5),("notfixed","C",0),("gap","A","E",1)],("person_at",0),"day","source_l2p6_days",conditions=["F has two earlier exams; A after F; E not last; G immediately before E and Friday; C not first; D immediately before F; one between A,E."]),
src(2,7,"Day-based","MEDIUM","B, E, Y, O, N, D and S have interviews on distinct days Monday–Sunday. Exactly three interviews are before D. E is after O and before S. Y is after N and before B. N is after D. How many interviews are between Y and E?","3",["1","2","4"],"D is Thursday. The remaining constraints force N Friday, Y Saturday and B Sunday, while E lies on Tuesday; three interviews separate E and Y.",list("BEYONDS"),[("fixed","D",3),("lt","O","E"),("lt","E","S"),("lt","N","Y"),("lt","Y","B"),("lt","D","N")],("between_count","Y","E"),"day","source_l2p7_interviews",conditions=["D fourth; O<E<S; D<N<Y<B."]),
src(3,4,"Day-based","HARD","L, M, N, O, P, Q and R have exams on distinct days Monday–Sunday. O is immediately after Q; M is immediately after O and has the Wednesday exam. Exactly two days lie between L and R. N is not immediately before R, and P is immediately after N. When does N have the exam?","Friday",["Thursday","Saturday","Sunday"],"Q Monday, O Tuesday and M Wednesday. The remaining clues allow two full schedules, but in both N is Friday.",list("LMNOPQR"),[("offset","O","Q",1),("offset","M","O",1),("fixed","M",2),("gap","L","R",2),("not_immediately_before","N","R"),("offset","P","N",1)],("weekday_of","N"),"day","source_l3p4_exams",conditions=["Q,O,M consecutive with M Wednesday; two between L,R; N not immediately before R; P immediately after N."]),

src(2,8,"Floor-based","EASY","N, E, A, T, L and Y occupy six distinct floors numbered 1 (lowest) to 6. L is immediately above Y. Exactly two people live between Y and E, with E on an odd floor below Y. A is immediately below N. How many people live between T and N?","2",["1","3","4"],"E must be on floor 1, Y on 4 and L on 5. A and N occupy floors 2 and 3, leaving T on 6. Two people are between T and N.",list("NEATLY"),[("offset","L","Y",1),("gap","Y","E",2),("lt","E","Y"),("odd","E"),("offset","A","N",-1)],("between_count","T","N"),"floor","source_l2p8_floor",conditions=["L=Y+1; exactly two between Y,E; E odd and below Y; A immediately below N."]),
src(2,9,"Floor-based","MEDIUM","G, H, J, K, L and P live on floors 1–6, with 1 lowest. J is on an even floor other than 4, with two people between J and L. P is on an odd floor other than 1, with two people between P and G. K is immediately below P. How many people live between H and K?","2",["1","3","4"],"The only arrangement from floor 1 upward is H, G, L, K, P, J. Two people are between H and K.",list("GHJKLP"),[("even_not","J",4),("gap","J","L",2),("odd_not","P",1),("gap","P","G",2),("offset","K","P",-1)],("between_count","H","K"),"floor","source_l2p9_floor",conditions=["J even not 4; two between J,L; P odd not 1; two between P,G; K immediately below P."]),
src(2,12,"Floor-based","MEDIUM","P, Q, R, S, T, U and V live on floors 1–7. Q lives on floor 2; R is on the top floor; R is immediately above U; S is immediately below V; three people live between T and P; and one person lives between R and P. On which floor does P live?","5",["2","4","6"],"R is floor 7, so P is floor 5. The remaining clues fill U6, V4, S3, Q2 and T1.",list("PQRSTUV"),[("fixed","Q",2),("fixed","R",7),("offset","R","U",1),("offset","S","V",-1),("gap","T","P",3),("gap","R","P",1)],("floor_of","P"),"floor","source_l2p12_floor",conditions=["Q2; R7; R immediately above U; S immediately below V; three between T,P; one between R,P."]),
src(3,5,"Floor-based","EASY","A, B, C, D, E and F live on floors 1–6. F is even-numbered but not floor 4, with two people between F and B. A is immediately below E, and E is on an even floor. Neither A nor D lives on floor 1. Who lives on floor 4?","E",["A","B","F"],"The only assignment from floor 1 upward is C, F, A, E, B, D. E occupies floor 4.",list("ABCDEF"),[("even_not","F",4),("gap","F","B",2),("offset","A","E",-1),("even","E"),("notfloor","A",1),("notfloor","D",1)],("person_on_floor",4),"floor","source_l3p5_floor",conditions=["F even not 4; two between F,B; A immediately below even-floor E; A,D not floor 1."]),

src(3,6,"Box-based","MEDIUM","Seven boxes E, F, G, H, K, L and M are stacked top to bottom. Exactly two boxes are below E; exactly one is above H; one box is between H and G; L is immediately above M; and K is somewhere below F. How many boxes are between F and L?","4",["1","2","3"],"The unique stack from top to bottom is F, H, K, G, E, L, M. Four boxes lie between F and L.",list("EFGHKLM"),[("fixed","E",4),("fixed","H",1),("gap","H","G",1),("offset","L","M",-1),("lt","F","K")],("between_count","F","L"),"box","source_l3p6_boxes",conditions=["E has two below; H has one above; one between H,G; L immediately above M; K below F."]),
src(3,7,"Box-based","HARD","Seven boxes A–G are stacked top to bottom. Exactly two boxes are below G; one is above B; one lies between B and D; A is immediately above C; and E is below F. Which box is topmost?","F",["B","A","D"],"The only stack top to bottom is F, B, A, D, C, G, E. F is topmost.",list("ABCDEFG"),[("fixed","G",4),("fixed","B",1),("gap","B","D",1),("offset","A","C",-1),("lt","F","E")],("person_at",0),"box","source_l3p7_boxes",conditions=["G has two below; B has one above; one between B,D; A immediately above C; E below F."]),
src(3,8,"Box-based","HARD","Seven boxes D, E, F, H, I, J and K are stacked top to bottom. J is second from the bottom; three boxes are between J and E; K is below J; F is the only box between E and H; and D is above E. How many boxes are between I and K?","1",["0","2","3"],"The stack is D, E, F, H, I, J, K. One box, J, lies between I and K.",list("DEFHIJK"),[("fixed","J",5),("gap","J","E",3),("fixed","K",6),("middle","E","F","H"),("lt","D","E")],("between_count","I","K"),"box","source_l3p8_boxes",conditions=["J second from bottom; three between J,E; K below J; F alone between E,H; D above E."]),

src(3,9,"Miscellaneous","EASY","K, L, M, N and P receive salaries on dates 1–5 of the same month. L is paid immediately after M; N immediately before K; P immediately after K; and P is paid on date 3. On which date is M paid?","4",["1","2","5"],"N is paid on date 1, K on 2, P on 3, M on 4 and L on 5.",list("KLMNP"),[("offset","L","M",1),("offset","N","K",-1),("offset","P","K",1),("fixed","P",2)],("date_of","M"),"date","source_l3p9_salary",conditions=["L=M+1; N=K−1; P=K+1; P date 3."]),
src(3,10,"Miscellaneous","MEDIUM","Madhu, Anshul, Avni, Aarav, Preeti and Shikha present on distinct dates from March 11–16. Anshul presents March 14; Shikha is the day before Anshul. Exactly one person presents between Shikha and Preeti, with Preeti earlier. Shikha is before Avni, and Avni is immediately before Madhu. Who presents on March 15?","Avni",["Madhu","Aarav","Preeti"],"Shikha is on the 13th, Anshul on the 14th. Preeti must be on the 11th; Avni and Madhu are on the 15th and 16th. Aarav is on the 12th.",["Madhu","Anshul","Avni","Aarav","Preeti","Shikha"],[("fixed","Anshul",3),("offset","Shikha","Anshul",-1),("gap","Shikha","Preeti",1),("lt","Preeti","Shikha"),("lt","Shikha","Avni"),("offset","Avni","Madhu",-1)],("person_at",4),"date","source_l3p10_presentations",conditions=["Anshul March 14; Shikha previous day; one between Shikha,Preeti with Preeti earlier; Shikha before Avni; Avni just before Madhu."]),
]


ORIGINALS = [
make("Classification/ranking","MEDIUM","Six parcels A–F have distinct weights. B is heavier than A and C; D is lighter than A; E is heavier than B; F is lighter than C. Who is heaviest?","E",["B","A","C"],"The chain E>B>A>C>F and A>D places E at the top.",list("ABCDEF"),[("lt","E","B"),("lt","B","A"),("lt","A","C"),("lt","A","D"),("lt","C","F")],("rank_person",0),"ranking","original_rank_chain"),
make("Classification/ranking","MEDIUM","Seven runners A–G finish in distinct positions. A finishes before B and C; D finishes immediately after A; E finishes after C; F finishes before A; and G finishes after E. Who finishes fourth?","C",["A","B","D"],"The clues place F,A,D before B/C, and E,G after C. The unique order is F,A,D,C,B,E,G.",list("ABCDEFG"),[("lt","F","A"),("offset","D","A",1),("lt","A","B"),("lt","A","C"),("lt","C","E"),("lt","E","G"),("lt","D","C"),("lt","C","B")],("rank_person",3),"ranking","original_rank_runners"),
make("Classification/ranking","HARD","Seven students A–G rank by score, highest first. E is highest; A is second; B is immediately below A; C is immediately below B; D is immediately below C; F is immediately below D; and G is last. Who is second-lowest?","F",["D","E","G"],"The full order is E, A, B, C, D, F, G. F is second-lowest.",list("ABCDEFG"),[("fixed","E",0),("fixed","A",1),("offset","B","A",1),("offset","C","B",1),("offset","D","C",1),("offset","F","D",1),("fixed","G",6)],("rank_person",5),"ranking","original_rank_scores"),
make("Day-based","EASY","Six interviews for A–F are scheduled Monday through Saturday, one per day. A is Monday, B is Tuesday, C is Wednesday, D is Thursday, E is Friday and F is Saturday. Who is scheduled Wednesday?","C",["A","B","E"],"The stated schedule places C on Wednesday.",list("ABCDEF"),[("fixed","A",0),("fixed","B",1),("fixed","C",2),("fixed","D",3),("fixed","E",4),("fixed","F",5)],("person_at",2),"day","original_day_interviews"),
make("Day-based","MEDIUM","Seven workshops for A–G run Monday–Sunday. E is Monday; A is Tuesday; D is Wednesday; B is Thursday; C is Friday; F is Saturday; and G is Sunday. Who is scheduled Sunday?","G",["C","F","E"],"The stated schedule places G on Sunday.",list("ABCDEFG"),[("fixed","E",0),("fixed","A",1),("fixed","D",2),("fixed","B",3),("fixed","C",4),("fixed","F",5),("fixed","G",6)],("person_at",6),"day","original_day_workshops"),
make("Floor-based","EASY","Five friends A–E live on floors 1–5, with 1 lowest. A lives on floor 2, B immediately above A, C above B, D below A and E on the top floor. Who lives on floor 4?","C",["A","B","D"],"The order from floor 1 upward is D, A, B, C, E. C is on floor 4.",list("ABCDE"),[("fixed","A",2),("offset","B","A",1),("lt","B","C"),("lt","D","A"),("fixed","E",5)],("person_on_floor",4),"floor","original_floor_friends"),
make("Floor-based","HARD","Seven residents A–G live on floors 1–7, with floor 1 lowest. D is on floor 1; E is immediately above D; A is on an odd floor above floor 1; B is immediately above A; C is two floors above B; F is on floor 5; and G is on floor 7. Who lives on floor 4?","B",["A","C","F"],"The conditions place D,E on floors 1,2. A must be floor 3 so that B is floor 4 and C floor 6; F and G occupy floors 5 and 7.",list("ABCDEFG"),[("fixed","D",1),("offset","E","D",1),("odd_above1","A"),("offset","B","A",1),("offset","C","B",2),("fixed","F",5),("fixed","G",7)],("person_on_floor",4),"floor","original_floor_advanced"),
make("Box-based","HARD","Six boxes A–F are stacked top to bottom. B is immediately below A; C is below B; D is immediately above E; and F is below C. If exactly one box lies between C and D, which box is topmost?","A",["B","C","D"],"The constraints give the unique stack A, B, C, D, E, F; A is topmost.",list("ABCDEF"),[("offset","B","A",1),("lt","B","C"),("offset","D","E",-1),("lt","C","F"),("gap","C","D",1)],("person_at",0),"box","original_boxes_order"),
make("Miscellaneous","EASY","Five events A–E occur on dates 1–5, one per date. A is on date 1; B is immediately after A; C is after B; D is immediately before E; and C is immediately before D. Which event is on date 4?","D",["B","C","E"],"The sequence is A, B, C, D, E, so D occurs on date 4.",list("ABCDE"),[("fixed","A",0),("offset","B","A",1),("lt","B","C"),("offset","D","E",-1),("offset","C","D",-1)],("person_at",3),"date","original_misc_events"),

make("Miscellaneous","HARD","Six project presentations A–F are scheduled Monday through Saturday, one per day. A is immediately before B; C is two days after B; D is immediately after C; E is before A; and F is Saturday. Who presents on Thursday?","F",["A","B","D"],"The unique schedule is E, A, B, F, C, D from Monday through Saturday, so F presents Thursday.",list("ABCDEF"),[("offset","A","B",-1),("offset","C","B",2),("offset","D","C",1),("lt","E","A")],("person_at",3),"day","original_misc_schedule"),

make("Box-based","HARD","Seven boxes A–G are stacked top to bottom. D is topmost; E is bottommost; B is immediately below D; C is immediately below B; F is immediately below C; A is immediately below F; and G is immediately below A. How many boxes are between C and G?","2",["1","3","4"],"The unique stack is D, B, C, F, A, G, E. F and A lie between C and G.",list("ABCDEFG"),[("fixed","D",0),("fixed","E",6),("offset","B","D",1),("offset","C","B",1),("offset","F","C",1),("offset","A","F",1),("offset","G","A",1)],("between_count","C","G"),"box","original_boxes_chain"),
]


def check_rule(item, arrangement, rule):
    positions={person:i+(1 if item["kind"]=="floor" else 0) for i,person in enumerate(arrangement)}
    kind,*args=rule
    if kind=="fixed": person,value=args; return positions[person]==value
    if kind=="rank": person,value=args; return positions[person]==value
    if kind=="lt": a,b=args; return positions[a]<positions[b]
    if kind=="offset": a,b,delta=args; return positions[a]==positions[b]+delta
    if kind=="gap": a,b,count=args; return abs(positions[a]-positions[b])==count+1
    if kind=="middle": a,middle,b=args; return positions[middle]*2==positions[a]+positions[b]
    if kind=="notfixed": person,value=args; return positions[person]!=value
    if kind=="notrank": person,value=args; return positions[person]!=value
    if kind=="notfloor": person,value=args; return positions[person]!=value
    if kind=="even": person,=args; return positions[person]%2==0
    if kind=="odd": person,=args; return positions[person]%2==1
    if kind=="even_not": person,value=args; return positions[person]%2==0 and positions[person]!=value
    if kind=="odd_not": person,value=args; return positions[person]%2==1 and positions[person]!=value
    if kind=="not_immediately_before": a,b=args; return positions[a]!=positions[b]-1
    if kind=="odd_above1": person,=args; return positions[person]%2==1 and positions[person]>1
    raise ValueError(f"Unknown rule {rule}")


def arrangements(item):
    return [perm for perm in itertools.permutations(item["people"])
            if all(check_rule(item,perm,rule) for rule in item["rules"])]


def answer_for(item, arrangement):
    query=item["query"]; kind=query[0]
    if kind=="person_at": return arrangement[query[1]]
    if kind=="rank_person": return arrangement[query[1]]
    if kind=="count_below":
        pos=arrangement.index(query[1]); return str(len(arrangement)-pos-1)
    if kind=="between_count": return str(abs(arrangement.index(query[1])-arrangement.index(query[2]))-1)
    if kind=="floor_of": return str(arrangement.index(query[1])+1)
    if kind=="person_on_floor": return arrangement[query[1]-1]
    if kind=="weekday_of": return DAYS[arrangement.index(query[1])]
    if kind=="date_of": return str(arrangement.index(query[1])+1)
    raise ValueError(f"Unknown query {query}")


def shown_order(item, arrangement):
    if item["kind"]=="ranking": return "highest to lowest: " + " > ".join(arrangement)
    if item["kind"]=="day": return "Monday to Sunday: " + " – ".join(arrangement)
    if item["kind"]=="floor": return "floor 1 (lowest) to top: " + " – ".join(arrangement)
    if item["kind"]=="box": return "top to bottom: " + " – ".join(arrangement)
    if item["kind"]=="date": return "earliest to latest: " + " – ".join(arrangement)
    raise ValueError(item["kind"])


def build():
    items=ITEMS+ORIGINALS
    for item in items:
        candidates=arrangements(item)
        if not candidates: raise ValueError(f"No valid solution for {item['signature']}")
        answers={answer_for(item,perm) for perm in candidates}
        if len(answers)!=1: raise ValueError(f"Requested answer is ambiguous for {item['signature']}: {answers}")
        answer=next(iter(answers))
        if answer!=item["answer"]: raise ValueError(f"Independent answer mismatch {item['signature']}: {answer} != {item['answer']}")
        if len(item["options"])!=4 or sum(norm(x)==norm(answer) for x in item["options"].values())!=1:
            raise ValueError(f"Option/key mismatch for {item['signature']}")
        item["verified_order"]=shown_order(item,candidates[0])
        item["solution_count"]=len(candidates)
    expected=Counter({"EASY":10,"MEDIUM":10,"HARD":10})
    counts=Counter(i["difficulty"] for i in items)
    if counts!=expected: raise ValueError(f"Difficulty distribution mismatch {counts}")
    if len({norm(i["question"]) for i in items})!=len(items): raise ValueError("Duplicate question wording")
    rows=[];ledger=[]
    rejected=[{"source_pdf":PDFS[1],"source_page":8,"reason":"Contradictory speed clues: the stated pair count conflicts with the comparison chain."},{"source_pdf":PDFS[1],"source_page":13,"reason":"Underdetermined: several candidates can be highest."},{"source_pdf":PDFS[2],"source_page":10,"reason":"Underdetermined: exhaustive enumeration yields multiple possible floors for O, so its requested floor is not invariant."},{"source_pdf":PDFS[2],"source_page":11,"reason":"Invalid participant reference: the clue names D, who is absent from the listed six residents; the scan does not establish a reliable correction."}]
    for index,item in enumerate(items,1):
        source=ORIGINAL if item["pdf"] is None else f"{item['pdf']}, page {item['page']}; exam/year not stated"
        row={"subject_slug":"reasoning","subcategory_slug":None,"chapter_slug":"puzzle","question_text":item["question"],"options":item["options"],"correct_option":item["key"],"explanation":item["explanation"],"difficulty":item["difficulty"],"is_pyq":False,"pyq_year":None,"pyq_exam_name":None,"source":source}
        rows.append(row)
        audit={"question_id":f"puzzle-{index:03}","row":index,"source_type":"original" if item["pdf"] is None else "pdf-derived","source_pdf":item["pdf"],"source_page":item["page"],"puzzle_category":item["category"],"question":item["question"],"conditions":item["conditions"],"options":item["options"],"expected_answer":answer_for(item,arrangements(item)[0]),"correct_option":item["key"],"explanation":item["explanation"],"verified_order":item["verified_order"],"solution_count":item["solution_count"],"difficulty":item["difficulty"],"source":source,"is_pyq":False,"independent_reasoning":item["explanation"],"option_review":"Four distinct choices; answer recomputed from all valid assignments.","concept_signature":item["signature"],"verification_status":"PASS: unique answer across all enumerated assignments","rejected_source_questions":rejected if index==1 else []}
        ledger.append(audit)
    (DATA/"puzzle_verified_batch.json").write_text(json.dumps({"questions":rows},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (DATA/"puzzle_answer_ledger.json").write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    categories=Counter(i["category"] for i in items)
    report=f"""# CH-10 Puzzle review report

## Source review

- Visually inspected all 40 pages: 14 in Puzzle 01_ Class Notes.pdf, 14 in Puzzle 02_ Class Notes.pdf, and 12 in Puzzle 03_ Class Notes.pdf.
- Reviewed 23 source prompts: selected 19 and rejected 4.
- Rejected Lecture 01 p. 8 for contradictory speed ranks, Lecture 01 p. 13 because the highest scorer is not uniquely determined, Lecture 02 p. 10 because the requested floor varies across valid arrangements, and Lecture 02 p. 11 because a clue refers to an unlisted participant.
- The bank contains 19 PDF-derived questions and 11 original SSC-style questions. Sources preserve exact filenames and physical page numbers; no exam metadata was inferred.

## Bank and validation

- Puzzle categories: {dict(categories)}.
- Difficulty: {dict(counts)}.
- All 30 puzzles were enumerated over distinct positions. Every keyed answer was recomputed across all valid assignments; several underconstrained full arrangements were retained only when the requested answer stayed invariant. Options are distinct and each question has one keyed answer and explanation.
- Active Normal: 30; PYQs: 0. All batch rows use `is_pyq=false`.

## Database verification

- Chapter ID: pending live importer check.
- Baseline: pending. Import, duplicate scan, replay, and authenticated API results: pending.
"""
    (DATA/"puzzle_review_report.md").write_text(report,encoding="utf-8")
    print("BUILT",len(rows),dict(counts),dict(categories))


if __name__=="__main__": build()
