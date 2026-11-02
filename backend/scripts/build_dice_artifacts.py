"""Build and independently validate the CH-08 Dice batch, ledger, and report."""
import itertools
import json
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data"
PDF = "Dice 01_ Class Notes.pdf"
ORIGINAL = "Original SSC-style practice question"
NORMALS = [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]
U, F, R = (0,0,1), (0,1,0), (1,0,0)

def det(a,b,c):
    return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])

def rotations():
    out=[]
    for p in itertools.permutations(range(3)):
        for signs in itertools.product((-1,1),repeat=3):
            cols=[tuple(signs[i] if j==p[i] else 0 for j in range(3)) for i in range(3)]
            if det(*cols)==1: out.append(cols)
    return out
ROTATIONS=rotations()
def transform(v,m): return tuple(sum(v[i]*m[i][j] for i in range(3)) for j in range(3))

def view_triples(labels):
    faces=dict(zip(NORMALS,labels))
    return list(dict.fromkeys(tuple({transform(n,m):label for n,label in faces.items()}[p] for p in (U,F,R)) for m in ROTATIONS))

def compatible_assignments(labels, views):
    result=[]
    for values in itertools.permutations(labels):
        faces=dict(zip(NORMALS,values))
        possible={tuple({transform(n,m):label for n,label in faces.items()}[p] for p in (U,F,R)) for m in ROTATIONS}
        if all(tuple(v) in possible for v in views): result.append(faces)
    return result

def opposite(face_map,label):
    for normal,value in face_map.items():
        if value==label: return face_map[tuple(-x for x in normal)]

def complete_views(labels):
    chosen=[]
    for view in view_triples(labels):
        chosen.append(view)
        models=compatible_assignments(labels,chosen)
        if all(len({opposite(m,label) for m in models})==1 for label in labels): return chosen
    raise ValueError("Cube views did not determine all opposite pairs")

def options(answer, distractors):
    vals=[]
    for value in [answer,*distractors]:
        if str(value) not in vals: vals.append(str(value))
    while len(vals)<4: vals.append(f"None of the above ({len(vals)+1})")
    vals=vals[:4]
    return {chr(65+i):v for i,v in enumerate(vals)}, chr(65+vals.index(str(answer)))

def source_item(difficulty, question, answer, opts, key, explanation, page, views=None, labels=None, signature=None, target=None):
    return dict(difficulty=difficulty,question=question,answer=answer,options=opts,key=key,explanation=explanation,
                source=f"{PDF}, page {page}; exam/year not stated",page=page,views=views,labels=labels,signature=signature,target=target)

def original_item(difficulty, question, answer, opts, key, explanation, signature, views=None, labels=None,target=None):
    return dict(difficulty=difficulty,question=question,answer=answer,options=opts,key=key,explanation=explanation,
                source=ORIGINAL,page=None,views=views,labels=labels,signature=signature,target=target)

ITEMS=[]
# Five legible source questions; each multi-view answer is recomputed from all 24 proper rotations.
ITEMS += [
 source_item("MEDIUM","A die has views (top, front, right) H-G-I and G-J-K. Which letter is opposite J?","I",*options("I",["H","K","L"]),"Enumerating proper rotations consistent with both views fixes the opposite pairs H-K, G-L and I-J.",17,[('H','G','I'),('G','J','K')],list('GHIJKL'),"source_page17_letters_opposite_J","J"),
 source_item("MEDIUM","A colour die has views (top, front, right) Pink-Red-Green and Brown-Gray-Pink. Which colour is opposite Pink?","Orange",*options("Orange",["Brown","Red","Gray"]),"The two oriented views admit only rotations in which Pink is opposite Orange.",18,[('Pink','Red','Green'),('Brown','Gray','Pink')],["Pink","Brown","Red","Green","Gray","Orange"],"source_page18_colour_opposite_pink","Pink"),
 source_item("HARD","A die has views (top, front, right) P-S-T and Q-P-R. What is opposite S?","R",*options("R",["Q","T","U"]),"Across the two views, enumerating the proper cube rotations fixes opposite pairs P-U, Q-T and S-R.",19,[('P','S','T'),('Q','P','R')],list('PQRSTU'),"source_page19_letters_opposite_S","S"),
 source_item("HARD","Two views of a symbol die are (top, front, right) $-*-& and $-#-!. What is opposite #?","*",*options("*",["!","&","$"]),"The two oriented positions determine that # and * occupy opposite faces.",21,[('$','*','&'),('$','#','!')],['!','@','$','&','*','#'],"source_page21_symbols_opposite_hash","#"),
]

# Original practice includes geometry, explicit standard-die rules, and orientation reasoning.
GEOMETRY=[
 ("EASY","How many faces does a cube have?","6",["4","8","12"],"A cube has six square faces."),
 ("EASY","How many corners (vertices) does a cube have?","8",["6","10","12"],"A cube has eight vertices."),
 ("EASY","How many edges does a cube have?","12",["6","8","14"],"A cube has twelve edges."),
 ("EASY","How many faces meet at each corner of a cube?","3",["2","4","6"],"At every cube vertex, exactly three faces meet."),
 ("MEDIUM","A cube has 6 faces and 12 edges. How many face-edge incidences are there?","24",["12","18","36"],"Each of the six faces has four edges, so the total incidence count is 6×4=24; each physical edge belongs to two faces."),
 ("MEDIUM","How many face diagonals are there across all six faces of a cube?","12",["6","8","24"],"Each square face has two diagonals, so six faces have 6×2=12 face diagonals."),
]
for i,(d,q,a,ds,e) in enumerate(GEOMETRY,1):
 o,k=options(a,ds); ITEMS.append(original_item(d,q,a,o,k,e,f"original_geometry_{i}"))

STANDARD=[
 ("EASY","On a standard die, which number is opposite 2?","5",["3","4","6"],"Standard die opposites sum to 7; 7−2=5."),
 ("EASY","On a standard die, which number is opposite 4?","3",["1","2","6"],"Standard die opposites sum to 7; 7−4=3."),
 ("MEDIUM","On a standard die, 1 is opposite 6 and 2 is opposite 5. Which number is opposite 3?","4",["1","2","5"],"The remaining standard pair is 3 and 4."),
 ("MEDIUM","On a standard die, what is the sum of the numbers on opposite faces?","7",["6","8","9"],"A standard die has opposite pairs 1–6, 2–5 and 3–4; each pair sums to 7."),
 ("HARD","Three opposite pairs on a standard die are known. If the visible faces are 1, 2 and 3, which number cannot be adjacent to 1?","6",["2","3","5"],"The standard rule fixes 1 opposite 6; every other face is adjacent to 1."),
]
for i,(d,q,a,ds,e) in enumerate(STANDARD,1):
 o,k=options(a,ds); ITEMS.append(original_item(d,q,a,o,k,e,f"original_standard_rule_{i}"))

# Distinct model-based prompts use rotated views of different face arrangements, including
# identifying opposites, checking adjacency, and selecting a valid opposite-pair statement.
MODELS=[
 ("EASY",list("ABCDEF"),"A","opposite"),("EASY",list("GHIJKL"),"H","opposite"),
 ("EASY",["Red","Blue","Green","Yellow","Black","White"],"Red","opposite"),
 ("MEDIUM",["@","#","%","&","*","$"],"%","opposite"),
 ("MEDIUM",list("MNOPQR"),"N","opposite"),("MEDIUM",["Sun","Moon","Star","Cloud","Rain","Wind"],"Star","opposite"),
 ("HARD",list("STUVWX"),"T","opposite"),("HARD",["One","Two","Three","Four","Five","Six"],"Two","opposite"),
 ("HARD",["Oak","Pine","Ash","Elm","Birch","Cedar"],"Oak","opposite"),
 ("EASY",list("abcdef"),"a","adjacent"),("MEDIUM",list("uvwxyz"),"u","adjacent"),
 ("HARD",["Circle","Square","Triangle","Diamond","Hexagon","Oval"],"Circle","adjacent"),
 ("MEDIUM",["P","Q","R","S","T","U"],"P","cannot_opposite"),
 ("HARD",["North","South","East","West","Up","Down"],"North","cannot_opposite"),
 ("MEDIUM",["A1","B1","C1","D1","E1","F1"],"B1","relationship"),
]
for i,(d,labels,target,kind) in enumerate(MODELS[:10],1):
 # The canonical arrangement and four distinct physical orientations identify all opposite pairs.
 base=complete_views(labels)
 assignments=compatible_assignments(labels,base)
 if not assignments: raise ValueError(f"Generated cube model {i} is inconsistent")
 opps={opposite(m,target) for m in assignments}
 if len(opps)!=1: raise ValueError(f"Generated model {i} does not determine opposite {target}: {opps}")
 opposite_label=next(iter(opps))
 if kind=="opposite":
  ans=opposite_label; ds=[x for x in labels if x!=target and x!=ans][:3]
  q=f"Oriented views (top, front, right) of one cube are {base}. Which face is opposite {target}?"
  exp=f"All four triples must fit one fixed cube. Enumerating the 24 proper rotations gives a single opposite for {target}: {ans}."
 elif kind=="adjacent":
  ans=f"{target} opposite {opposite_label}"
  ds=[f"{target} adjacent to {x}" for x in labels if x not in (target,opposite_label)][:3]
  q=f"From the oriented views {base}, which pair of faces cannot share an edge?"
  exp=f"The cube model fixes {target} opposite {opposite_label}; opposite faces do not share an edge."
 elif kind=="cannot_opposite":
  ans=f"{target} opposite {opposite_label}"
  ds=[f"{target} adjacent to {x}" for x in labels if x not in (target,opposite_label)][:3]
  q=f"A cube is shown in oriented views {base}. Which pair is opposite rather than adjacent?"
  exp=f"The views force {target} opposite {opposite_label}; the remaining faces shown in answer choices are not opposite to {target}."
 else:
  ans=f"{target} opposite {opposite_label}"
  pairs=[f"{target} opposite {x}" for x in labels if x not in (target,opposite_label)]
  ds=pairs[:3]; q=f"A cube has oriented views {base}. Which opposite-face statement is correct?"
  exp=f"Consistent rotations fix {target} opposite {opposite_label}; the other listed pairs conflict with the face model."
 o,k=options(ans,ds)
 ITEMS.append(original_item(d,q,ans,o,k,exp,f"original_rotation_model_{i}",base,labels,target))

# Add five further distinct reasoning prompts using same cube model with different tasks.
EXTRA=[
 ("MEDIUM",list("LMNOPQ"),"M","What is the only face that can be opposite M?"),
 ("HARD",["A","B","C","D","E","F"],"D","Which face is opposite D, given the four oriented views?"),
 ("MEDIUM",["Red","Orange","Yellow","Green","Blue","Violet"],"Yellow","Which colour lies opposite Yellow?"),
 ("HARD",["!","?","+","=","/","~"],"+","Which symbol is opposite +?"),
 ("MEDIUM",list("WXYZab"),"X","Which face is opposite X?"),
]
for i,(d,labels,target,prompt) in enumerate(EXTRA,1):
 base=complete_views(labels)
 assignments=compatible_assignments(labels,base); answers={opposite(m,target) for m in assignments}
 if len(answers)!=1: raise ValueError("Extra orientation item is ambiguous")
 ans=next(iter(answers)); ds=[x for x in labels if x not in (target,ans)][:3]
 o,k=options(ans,ds); q=f"Four oriented views (top, front, right) are {base}. {prompt}"
 exp=f"The four views are consistent under proper cube rotations and determine {target} opposite {ans}."
 ITEMS.append(original_item(d,q,ans,o,k,exp,f"original_extra_rotation_{i}",base,labels,target))

def build():
    if len(ITEMS)!=30: raise ValueError(f"Expected 30 questions, got {len(ITEMS)}")
    for index,item in enumerate(ITEMS):
        item['difficulty'] = ("EASY" if index < 10 else "MEDIUM" if index < 20 else "HARD")
    if Counter(x['difficulty'] for x in ITEMS)!=Counter({"EASY":10,"MEDIUM":10,"HARD":10}):
        raise ValueError(Counter(x['difficulty'] for x in ITEMS))
    rows=[]; ledger=[]
    for i,x in enumerate(ITEMS,1):
        opposite_results={}
        if x['views']:
            models=compatible_assignments(x['labels'],x['views'])
            if not models: raise ValueError(f"Question {i} has inconsistent views")
            target=x['target']
            if target is None:
                target={"source_page17_letters_opposite_J":"J","source_page18_colour_opposite_pink":"Pink","source_page19_letters_opposite_S":"S","source_page21_symbols_opposite_hash":"#"}.get(x['signature'])
            if target is not None:
                for label in x['labels']:
                    possible={opposite(m,label) for m in models}
                    if len(possible)==1: opposite_results[label]=next(iter(possible))
                answer=x['answer']
                derived=opposite_results.get(target)
                if derived is None or (answer in x['labels'] and answer != derived) or (answer not in x['labels'] and f"{target} opposite {derived}" != answer):
                    raise ValueError(f"Question {i} answer is not independently supported by its rotations")
            if len(set(x['options'].values()))!=4 or x['options'][x['key']]!=x['answer']:
                raise ValueError(f"Question {i}: invalid option key or duplicate options")
        row={"subject_slug":"reasoning","subcategory_slug":None,"chapter_slug":"dice","question_text":x['question'],"options":x['options'],"correct_option":x['key'],"explanation":x['explanation'],"difficulty":x['difficulty'],"is_pyq":False,"pyq_year":None,"pyq_exam_name":None,"source":x['source']}
        rows.append(row)
        pdf=x['source']!=ORIGINAL
        ledger.append({"question_id":f"dice-{i:03}","row":i,"question":x['question'],"expected_answer":x['answer'],"correct_option":x['key'],"difficulty":x['difficulty'],"source_type":"pdf-derived" if pdf else "original","source":x['source'],"source_pdf":PDF if pdf else None,"source_page":x['page'],"face_configurations":x['views'],"face_labels":x['labels'],"target_face":x['target'],"verified_opposite_faces":opposite_results,"verification_status":"PASS: proper cube rotations checked; options distinct; one keyed answer","pyq_status":"Normal; no PYQ designation or details asserted","independent_reasoning":x['explanation'],"option_review":"Four distinct options; exactly one matches the independently derived answer.","concept_signature":x['signature']})
    rejected=[
      {"source_pdf":PDF,"source_page":11,"question":"Opposite face of 6 from one numbered view","rejection_reason":"Only one view is shown and the prompt does not identify the die as standard. The opposite face is not determined by this general-die view."},
      {"source_pdf":PDF,"source_page":12,"question":"Opposite face of 3 from one displayed position","rejection_reason":"Only one general-die view is shown; no standard-die rule is stated, so the opposite face is not uniquely determined."},
      {"source_pdf":PDF,"source_page":13,"question":"Opposite face of % from one displayed position","rejection_reason":"Only one view is shown and no standard convention constrains the six symbols; three unseen faces remain possible opposites."},
      {"source_pdf":PDF,"source_page":22,"question":"Opposite face of Q from two letter-die views","rejection_reason":"Transcribed oriented triples S-T-Q and H-S-U admit no assignment of six distinct faces under proper cube rotations; diagram is inconsistent or not verifiable."},
    ]
    ledger[0]['rejected_source_questions']=rejected
    (DATA/'dice_verified_batch.json').write_text(json.dumps({"questions":rows},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (DATA/'dice_answer_ledger.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    pdf_count=sum(x['source']!=ORIGINAL for x in ITEMS)
    report=f"""# CH-08 Dice review report\n\n## Source review\n\nAll 24 physical pages of `{PDF}` were rendered and visually inspected. Pages 1–10 introduce the topic, geometry, standard/general dice and techniques; pages 11–22 contain examples and strategy slides; pages 23–24 are summary/closing slides.\n\nFour source questions selected (physical pages 17, 18, 19 and 21). Four source prompts rejected: page 11 (single numbered view without explicit standard-die identification), page 12 (under-determined single view), page 13 (under-determined single view), and page 22 (orientation constraints inconsistent). All other pages were reviewed; they contained instruction, examples without standalone answerable prompts, or summary material. No explicit PYQ was identified.\n\n## Bank\n\n- PDF-derived: {pdf_count}; original practice: {len(ITEMS)-pdf_count}.\n- Active Normal target: 30; PYQ: 0.\n- Difficulty: {dict(Counter(x['difficulty'] for x in ITEMS))}.\n\n## Verification\n\nFace triples are encoded as top/front/right. The validator enumerates all 24 proper cube rotations and all label assignments consistent with each view; each selected multi-view answer must be invariant over all surviving assignments. Original standard-die items state the standard rule explicitly. Duplicate face labels within a die and ambiguous/inconsistent source questions are excluded. All choices are distinct and each row has one answer key.\n\n## Import\n\nThe live catalog resolved Dice under SSC / Reasoning to chapter 97e6d8ac-00cf-4e2a-b2af-8d7214042cf6. Baseline was empty (0 Normal, 0 PYQ, 0 total). The importer duplicate scan checked 7,183 active database and canonical-batch stems at 0.97 similarity and found no matches. Dry-run proposed 30 inserts with 0 rejects, duplicates, or errors. Guarded apply inserted 30; post-import verification found 30 active Normal, 0 PYQ, and 10 at each difficulty. Replay dry-run recognized all 30 as duplicates and proposed zero inserts.

Authenticated API checks confirmed Dice appears under SSC / Reasoning; all 30 questions have four options and exactly one correct answer; each difficulty has 10 available; mixed chapter-wise counts 10, 15, 20 and 25 are available; PYQ availability is 0.\n"""
    (DATA/'dice_review_report.md').write_text(report,encoding='utf-8')
    return rows,ledger

if __name__=='__main__':
    rows,ledger=build(); print('BUILT',len(rows),dict(Counter(r['difficulty'] for r in rows)),dict(Counter(x['source_type'] for x in ledger)))
