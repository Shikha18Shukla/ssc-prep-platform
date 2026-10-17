"""Build the reviewed Blood Relation Normal batch and independent answer ledger."""

import json
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
BATCH = BASE / "data" / "blood_relation_verified_batch.json"
LEDGER = BASE / "data" / "blood_relation_answer_ledger.json"
PDF2 = "Blood relation 02_.pdf"
PDF3 = "Blood relation 03_.pdf"
ORIGINAL = "Original SSC-style practice question"

# (difficulty, stem, A, B, C, D, key, explanation, source, concept signature)
ITEMS = [
    ("MEDIUM", "A joint family has a father, a mother, three married sons, and one unmarried daughter. Two sons each have two daughters; the third has one son. How many female members are in the family?", "2", "3", "6", "9", "D", "Count the mother (1), unmarried daughter (1), wives of the three married sons (3), and four granddaughters (4): 1+1+3+4=9. The grandson and male family members do not add to the female count.", f"{PDF2}, lecture slide 5; exam/year not stated; wording clarified from bilingual slide", "joint_family_female_member_count"),
    ("MEDIUM", "F is the brother of G. G is the husband of H. H is the daughter of I, and I is the wife of J. How is F related to J?", "Daughter's husband's brother", "Brother", "Father", "Daughter's husband's father", "A", "I is J's wife and H is I's daughter, so H is J's daughter. G is H's husband and F is G's brother. Thus F is the brother of J's daughter's husband.", f"{PDF2}, lecture slide 8; exam/year not stated", "daughter_husbands_brother"),
    ("EASY", "Himmat is the husband of Kavita. Sharda is the daughter of Ravi and Ketaki, and Kavita and Sharda are full sisters. How is Ravi related to Himmat?", "Brother", "Father", "Uncle", "Father-in-law", "D", "Ravi is Sharda's father. Since Kavita and Sharda are full sisters, Ravi is also Kavita's father. Himmat is Kavita's husband, so Ravi is Himmat's father-in-law.", f"{PDF2}, lecture slide 10; exam/year not stated; full-sibling relation stated explicitly", "wifes_father_father_in_law"),
    ("MEDIUM", "H is the husband of G. J is H's son. L is J's son. L and M are full siblings. N is M's mother and is married to J. How is N related to H?", "Daughter-in-law", "Daughter", "Sister", "Mother", "A", "N is married to J, who is H's son. Therefore N is H's daughter-in-law. The full-sibling statement also makes N L's mother, consistent with the slide's family chain.", f"{PDF2}, lecture slide 11; exam/year not stated; marriage and full-sibling links stated to remove ambiguity", "sons_wife_is_daughter_in_law"),
    ("MEDIUM", "Kartik is the paternal grandfather of Deepak. Nirupama is Deepak's mother, and Ankit is both Nirupama's husband and Deepak's father. How is Kartik related to Ankit?", "Brother", "Son", "Uncle", "Father", "D", "Ankit is Deepak's father. Kartik is Deepak's paternal grandfather, so Kartik is the father of Ankit.", f"{PDF2}, lecture slide 12; exam/year not stated; Ankit's parentage of Deepak made explicit", "paternal_grandfather_is_father_of_father"),
    ("EASY", "Karishma introduces Reshma and says, ‘She is my father-in-law's daughter's daughter.’ How is Reshma related to Karishma?", "Sister", "Cousin", "Sister-in-law", "Niece", "D", "Karishma's father-in-law's daughter is her husband's sister. That daughter's daughter is Karishma's niece.", f"{PDF2}, lecture slide 13; exam/year not stated", "father_in_laws_daughter_daughter_is_niece"),
    ("HARD", "The symbols mean: A+B: A is the son of B; A−B: A is the sister of B; A×B: A is the wife of B; A÷B: A is the father of B. Assume the stated parents are spouses. How is Q related to D in Q÷E+R−C×D?", "Sister's husband", "Wife's sister's husband", "Son", "Husband", "B", "Q is E's father and R is E's other parent, so Q and R are spouses. R is C's sister, and C is D's wife. Therefore Q is the husband of D's wife's sister.", f"{PDF3}, lecture slide 4; exam/year not stated; co-parent spouse assumption made explicit", "coded_wifes_sister_husband"),
    ("MEDIUM", "The symbols mean: A+B: A is the sister of B; A−B: A is the brother of B; A×B: A is the wife of B; A÷B: A is the father of B. Assume sibling links denote full siblings. How is F related to Y in F−H×L÷O+Y?", "Father's father", "Mother's brother", "Mother's father", "Father's brother", "B", "F is H's brother; H is L's wife. L is O's father, and O is Y's sister, so O and Y share parents. H is their mother; F is their mother's brother.", f"{PDF3}, lecture slide 6; exam/year not stated; full-sibling relation stated", "coded_mothers_brother"),
    ("EASY", "The symbols mean: A%B: A is the daughter of B; A$B: A is the son of B; A*B: A is the sister of B. How is H related to J in H%I$J$K*L?", "Grandson", "Uncle", "Granddaughter", "Son", "C", "H is the daughter of I, and I is the son of J. Thus H is J's granddaughter.", f"{PDF3}, lecture slide 7; exam/year not stated", "coded_granddaughter_from_daughter_son"),
    ("MEDIUM", "The symbols mean: A+B: A is the father of B; A−B: A is the sister of B; A×B: A is the brother of B; A÷B: A is the daughter of B. Assume sibling links denote full siblings. How is S related to U in R+S×T−V÷U?", "Husband", "Son", "Brother", "Daughter", "B", "R is S's father. S is T's brother, T is V's sister, and V is U's daughter. Under the stated full-sibling convention, S is also U's child; since S is identified as a brother, S is U's son.", f"{PDF3}, lecture slide 8; exam/year not stated; full-sibling relation stated", "coded_child_is_son"),
    ("HARD", "The symbols mean: A+B: A is the sister of B; A@B: A is the brother of B; A#B: A is the wife of B; A÷B: A is the father of B. Assume stated sibling links denote full siblings. How is W related to U in W@E+R÷H#U?", "Wife's father", "Wife's brother", "Wife's father's brother", "Wife's father's father", "C", "W is E's brother and E is R's sister, so W is R's brother. R is H's father; H is U's wife. Therefore W is the brother of U's wife's father.", f"{PDF3}, lecture slide 9; exam/year not stated; full-sibling relation stated", "coded_wifes_fathers_brother"),
    ("MEDIUM", "The symbols mean: A$B: A is the son of B; A+B: A is the brother of B; A@B: A is the wife of B; A÷B: A is the father of B. Assume sibling links denote full siblings. How is E related to N in E$F÷G+M@N?", "Father", "Brother", "Wife's brother", "Wife's father", "C", "E is F's son and F is G's father, so E and G are siblings. G is M's brother, so E is M's brother. M is N's wife; hence E is N's wife's brother.", f"{PDF3}, lecture slide 11; exam/year not stated; sibling links clarified", "coded_wifes_brother"),
    ("HARD", "The symbols mean: A+B: A is the daughter of B; A−B: A is the brother of B; A×B: A is the wife of B; A÷B: A is the father of B. Assume O and P are full siblings. How is M related to Q in M÷N×O−P+Q?", "Son's wife's father", "Wife's father", "Wife's brother", "Son's wife's brother", "A", "M is N's father; N is O's wife. O is P's brother, and P is Q's daughter, so O is Q's son. Therefore M is the father of Q's son's wife.", f"{PDF3}, lecture slide 12; exam/year not stated; full-sibling link stated", "coded_sons_wifes_father"),
    ("HARD", "The symbols mean: A+B: B is the father of A; A#B: B is the sister of A; A@B: B is the brother of A. Assume the sibling links denote full siblings. How is E related to A in A@B#C+D+E?", "Grandfather", "Father", "Uncle", "Son", "A", "B is A's brother and C is B's sister, so A, B, and C are siblings. D is C's father and E is D's father. E is two generations above A, so E is A's grandfather.", f"{PDF3}, lecture slide 17; exam/year not stated; full-sibling relation stated", "coded_grandfather"),

    ("EASY", "Rita is the sister of Mohan. Mohan is the father of Kiran. How is Rita related to Kiran?", "Paternal aunt", "Maternal aunt", "Sister", "Grandmother", "A", "Rita is the sister of Kiran's father, so she is Kiran's paternal aunt.", ORIGINAL, "father_sister_is_paternal_aunt"),
    ("EASY", "Asha is the daughter of Neha. Neha is the daughter of Lata. How is Lata related to Asha?", "Mother", "Paternal grandmother", "Maternal grandmother", "Aunt", "C", "Neha is Asha's mother, and Lata is Neha's mother. Lata is Asha's maternal grandmother.", ORIGINAL, "mothers_mother_is_maternal_grandmother"),
    ("EASY", "Pointing to a boy, Meena says, ‘He is the son of my father's only son.’ Meena has one brother, and her father has no other sons. How is the boy related to Meena?", "Brother", "Nephew", "Cousin", "Uncle", "B", "Meena's father's only son is her brother. The boy is her brother's son, so he is her nephew.", ORIGINAL, "brothers_son_is_nephew"),
    ("EASY", "P is the father of Q. Q and R are full siblings. How is P related to R?", "Uncle", "Father", "Brother", "Grandfather", "B", "P is Q's father, and R is Q's full sibling. Therefore P is also R's father.", ORIGINAL, "father_of_full_sibling_is_father"),
    ("EASY", "Asha is the daughter of Ravi. Ravi is the son of Mohan. How is Mohan related to Asha?", "Maternal grandfather", "Paternal grandfather", "Uncle", "Father", "B", "Ravi is Asha's father. Mohan is Ravi's father, so Mohan is Asha's paternal grandfather.", ORIGINAL, "fathers_father_is_paternal_grandfather"),
    ("EASY", "Tara is the daughter of Arjun and Meera. Rohit is Tara's son. How is Arjun related to Rohit?", "Paternal grandfather", "Maternal grandfather", "Uncle", "Father", "B", "Arjun is Tara's father, and Tara is Rohit's mother. Arjun is Rohit's maternal grandfather.", ORIGINAL, "mothers_father_is_maternal_grandfather"),
    ("EASY", "Kamal is the brother of Leela. Leela is the mother of Nitin. How is Kamal related to Nitin?", "Paternal uncle", "Maternal uncle", "Brother", "Grandfather", "B", "Kamal is the brother of Nitin's mother, so he is Nitin's maternal uncle.", ORIGINAL, "mothers_brother_is_maternal_uncle"),
    ("MEDIUM", "Ravi and Sita are full siblings. Ravi is the father of Arjun, and Sita is the mother of Beena. How are Arjun and Beena related?", "Brother and sister", "First cousins", "Uncle and niece", "Father and daughter", "B", "Arjun is the child of Ravi and Beena is the child of Ravi's full sister Sita. Children of siblings are first cousins.", ORIGINAL, "children_of_full_siblings_are_first_cousins"),
    ("MEDIUM", "Neha is the mother of Pooja. Pooja is married to Karan. How is Neha related to Karan?", "Sister-in-law", "Mother-in-law", "Aunt", "Daughter-in-law", "B", "Neha is the mother of Karan's wife, so Neha is his mother-in-law.", ORIGINAL, "wifes_mother_is_mother_in_law"),
    ("MEDIUM", "A woman’s brother has a daughter, and that daughter has a son, R. How is R related to the woman?", "Nephew", "Cousin", "Great-nephew", "Grandson", "C", "The woman's brother's daughter is her niece. That niece's son is her great-nephew (also called a grandnephew).", ORIGINAL, "nieces_son_is_great_nephew"),
    ("MEDIUM", "J is married to K. L is K's sister. L is the mother of M. How is L related to J?", "Sister-in-law", "Mother-in-law", "Daughter", "Cousin", "A", "L is the sister of J's spouse K, so L is J's sister-in-law.", ORIGINAL, "spouses_sister_is_sister_in_law"),
    ("MEDIUM", "N is the sister of M. M is the father of P and is married to L, P's mother. How is N related to P?", "Maternal aunt", "Paternal aunt", "Sister", "Grandmother", "B", "M is P's father and N is M's sister. Thus N is P's paternal aunt.", ORIGINAL, "fathers_sister_is_paternal_aunt_from_spouse_chain"),
    ("HARD", "P is the brother of Q. Q is the father of R. R is the mother of S. How is P related to S?", "Mother's maternal uncle", "Mother's father's brother", "Father's paternal uncle", "Mother's father", "B", "P is the brother of S's maternal grandfather Q. Q is R's father, and R is S's mother. So P is the brother of S's mother's father.", ORIGINAL, "mothers_fathers_brother"),
    ("HARD", "E is the mother of A. A is the father of B. B and C are full siblings. C is the father of D. How is E related to D?", "Paternal grandmother", "Maternal great-grandmother", "Paternal great-grandmother", "Paternal great-aunt", "C", "A is C's father because B and C are full siblings. E is A's mother, C is D's father, so E is D's paternal great-grandmother.", ORIGINAL, "paternal_great_grandmother_chain"),
    ("HARD", "The symbols mean: A+B: A is the father of B; A−B: A is the mother of B; A×B: A is the sister of B. How is P related to S in P×R−B+S?", "Father's maternal aunt", "Mother's paternal aunt", "Father's sister", "Mother's aunt", "A", "P is R's sister, R is B's mother, and B is S's father. Therefore P is the sister of S's father's mother: S's father's maternal aunt.", ORIGINAL, "coded_fathers_maternal_aunt"),
    ("HARD", "A is the brother of B. B is the mother of C. C is the father of D. E is the sister of A. Assume A and B, and A and E, are full siblings. How is E related to D?", "Father's maternal aunt", "Father's paternal aunt", "Mother's paternal aunt", "Grandmother", "A", "E is A's sister and A and B are full siblings, so E is also B's sister. B is C's mother, and C is D's father. Thus E is the sister of D's paternal grandmother: D's father's maternal aunt.", ORIGINAL, "fathers_maternal_grandmothers_sister"),
]


def build():
    if len(ITEMS) != 30:
        raise ValueError(f"Expected 30 questions, found {len(ITEMS)}")
    rows, ledger = [], []
    for index, item in enumerate(ITEMS, 1):
        difficulty, stem, a, b, c, d, key, explanation, source, signature = item
        options = dict(zip("ABCD", (a, b, c, d)))
        row = {
            "subject_slug": "reasoning", "subcategory_slug": None,
            "chapter_slug": "blood-relation", "question_text": stem,
            "explanation": explanation, "difficulty": difficulty,
            "is_pyq": False, "pyq_year": None, "pyq_exam_name": None,
            "source": source, "options": options, "correct_option": key,
        }
        rows.append(row)
        ledger.append({
            "row": index, "question": stem, "expected_answer": options[key],
            "correct_option": key, "difficulty": difficulty, "source": source,
            "independent_reasoning": explanation,
            "option_review": f"A={a}; B={b}; C={c}; D={d}. Only the keyed option matches the stated relations.",
            "concept_signature": signature,
        })
    BATCH.write_text(json.dumps({"questions": rows}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    LEDGER.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Wrote", len(rows), "questions", dict(Counter(row["difficulty"] for row in rows)))


if __name__ == "__main__":
    build()
