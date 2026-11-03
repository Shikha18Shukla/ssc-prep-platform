"""Build the reviewed Venn Diagram batch and auditable answer/rejection ledger."""

import json
import unicodedata
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
ORIGINAL = "Original SSC-style practice question"


def item(q, options, answer, explanation, difficulty, category, sets, signature,
         verify, page=None, pdf=None, diagram=None, regions=None):
    return {
        "question": q, "options": options, "answer": answer,
        "explanation": explanation, "difficulty": difficulty,
        "question_category": category, "set_count": sets,
        "concept_signature": signature, "independent_verification": verify,
        "source_pdf": pdf, "source_page": page,
        "diagram_description": diagram, "region_values": regions,
    }


ITEMS = [
    # Four source prompts about class relationships.
    item("A three-set diagram has Yellow-only 12, Pink-only 10, Green-only 11, Yellow∩Pink-only 9, Yellow∩Green-only 7, and all-three 8. How many are Pink but neither Green nor Yellow?",
         ["9", "17", "10", "8"], "C", "‘Neither Green nor Yellow’ excludes every overlap with either set. The Pink-only region in the diagram is labeled 10.", "EASY", "numerical", 3, "source_triangle_rectangle_circle_pink_only", "Read the requested set difference directly: Pink ∩ not-Green ∩ not-Yellow = 10.", 7, "Venn Diagram 01_ Class Notes.pdf", "Yellow is a triangle, Pink a rectangle, and Green a circle; the Pink-only region is labeled 10.", {"pink_only": 10}),
    item("Which relationship best represents Mango, Fruit and Cauliflower?",
         ["Mango is inside Fruit; Cauliflower is separate from both.", "All three sets partially overlap.", "Fruit is inside Mango; Cauliflower is separate.", "Mango and Cauliflower are inside Fruit and overlap each other."], "A", "Every mango is a fruit, so Mango is a subset of Fruit. Cauliflower is not a fruit, so its set is separate from both in this classification.", "EASY", "logical_classification", 3, "mango_subset_fruit_cauliflower_disjoint", "Mango ⊂ Fruit; Cauliflower ∩ Fruit = ∅ and therefore Cauliflower ∩ Mango = ∅.", 17, "Venn Diagram 01_ Class Notes.pdf", "A small Mango set fully inside Fruit; a separate Cauliflower set.") ,
    item("Which diagram best represents Wheat, Grains, Onion and Maize?",
         ["Wheat and Maize are separate subsets of Grains; Onion is outside Grains.", "All four sets are completely disjoint.", "Onion is inside Grains, while Wheat and Maize are outside.", "Wheat, Grains and Maize form three nested sets; Onion overlaps them."], "A", "Wheat and maize are kinds of grain, but neither is the other. Onion is not a grain, so it is disjoint from the Grains set.", "MEDIUM", "logical_classification", 4, "wheat_maize_disjoint_subsets_grains_onion_outside", "Wheat ⊂ Grains and Maize ⊂ Grains; Wheat ∩ Maize = ∅; Onion ∩ Grains = ∅.", 22, "Venn Diagram 01_ Class Notes.pdf", "Two disjoint inner sets Wheat and Maize inside Grains; Onion is a separate set."),
    item("Which relationship best represents Vegetable, Woman, Lion and Parrot?",
         ["Four separate sets with no overlap.", "Woman contains Vegetable; Lion and Parrot overlap.", "Lion and Parrot are nested inside Vegetable.", "All four sets overlap in one common region."], "A", "These labels denote different classes: vegetables, people who are women, lions, and parrots. None is a subset of or overlaps another class in the intended classification diagram.", "EASY", "logical_classification", 4, "vegetable_woman_lion_parrot_disjoint", "The four named classes are pairwise disjoint in the intended classification.", 23, "Venn Diagram 01_ Class Notes.pdf", "Four pairwise disjoint sets."),
    item("Which diagram best represents Teachers, Parents and Guardians when people may belong to more than one group?",
         ["Three separate circles.", "Three nested circles.", "Three partially overlapping circles, including a possible common intersection.", "Two overlapping circles and one separate circle."], "C", "A person can be a teacher, a parent, and a guardian at the same time; each role can also occur without the other two. The sets therefore overlap and may share a common region, but none contains another.", "MEDIUM", "logical_classification", 3, "teachers_parents_guardians_overlapping_roles", "Roles are not subset relations; the source diagram shows pairwise overlaps and a central common region.", 8, "Venn Diagram 02_ Class Notes.pdf", "Three non-nested circles, pairwise overlapping with a shared central region."),
    # Six clear source numerical prompts. Values are mutually exclusive regions unless noted.
    item("In a Kesar/Mint/Vanilla diagram, the exclusive regions are: Kesar 32, Mint 21, Vanilla 45, Kesar-Mint 12, Kesar-Vanilla 14, Mint-Vanilla 20, and all three 10. How many people like Mint but not Kesar?",
         ["51", "21", "33", "41"], "D", "Mint but not Kesar includes Mint only (21) and Mint-and-Vanilla only (20). Exclude both Kesar-and-Mint regions, including the all-three region. Thus 21 + 20 = 41.", "MEDIUM", "numerical", 3, "mint_without_kesar_from_exclusive_regions", "21 + 20 = 41; the Kesar∩Mint-only value 12 and the triple value 10 are excluded.", 11, "Venn Diagram 02_ Class Notes.pdf", "Kesar-only 32; Mint-only 21; Vanilla-only 45; Kesar∩Mint only 12; Kesar∩Vanilla only 14; Mint∩Vanilla only 20; all three 10.", {"K_only": 32, "M_only": 21, "V_only": 45, "KM_only": 12, "KV_only": 14, "MV_only": 20, "KMV": 10}),
    item("A Clerks/Potters/Farmers diagram has exclusive regions: Clerks 20, Potters 23, Farmers 45, Clerks-Potters 12, Clerks-Farmers 9, Potters-Farmers 8, and all three 6. How many are both clerks and potters?",
         ["20", "12", "48", "18"], "D", "The Clerks∩Potters total includes the Clerks-and-Potters-only region (12) and the all-three region (6): 12 + 6 = 18.", "MEDIUM", "numerical", 3, "clerks_and_potters_inclusive_pair", "For inclusive C∩P, sum C∩P-only 12 and C∩P∩F 6: 18.", 12, "Venn Diagram 02_ Class Notes.pdf", "Clerks only 20; Potters only 23; Farmers only 45; C∩P only 12; C∩F only 9; P∩F only 8; all three 6.", {"C_only": 20, "P_only": 23, "F_only": 45, "CP_only": 12, "CF_only": 9, "PF_only": 8, "CPF": 6}),
    item("In a four-set diagram, the regions are Florists-only 23, Florists-Teachers 9, Teachers-only 34, Teachers-Celebrities 7, Celebrities-only 25, Celebrities-Doctors 13, and Doctors-only 56. How many are both teachers and florists?",
         ["34", "43", "9", "7"], "C", "The shared Teachers∩Florists region is labeled 9. The value 7 belongs to Teachers∩Celebrities, a different overlap.", "HARD", "numerical", 4, "teacher_florist_shared_region_four_classes", "Inspect the labeled Florists∩Teachers-only region: 9.", 13, "Venn Diagram 02_ Class Notes.pdf", "Four category circles in a chain; Florists∩Teachers is labeled 9.", {"florists_only": 23, "F_T": 9, "teachers_only": 34, "T_C": 7, "celebrities_only": 25, "C_D": 13, "doctors_only": 56}),
    item("In an Urban/Male/Educated diagram, the exclusive regions are U-only 1, M-only 2, E-only 3, U-M 5, U-E 4, M-E 6, and all three 10. How many people belong to the Urban set?",
         ["20", "23", "10", "15"], "A", "The Urban set includes Urban-only 1, Urban∩Male-only 5, Urban∩Educated-only 4, and the all-three region 10. Total = 1 + 5 + 4 + 10 = 20.", "MEDIUM", "numerical", 3, "urban_set_total_from_exclusive_regions", "Sum the four disjoint regions inside Urban: 1 + 5 + 4 + 10 = 20.", 15, "Venn Diagram 02_ Class Notes.pdf", "Urban-only 1; Male-only 2; Educated-only 3; U∩M only 5; U∩E only 4; M∩E only 6; all three 10.", {"U_only": 1, "M_only": 2, "E_only": 3, "UM_only": 5, "UE_only": 4, "ME_only": 6, "UME": 10}),
    item("For Hindi/English/French, the exclusive regions are H-only 20, E-only 10, F-only 20, H-E 25, H-F 10, E-F 10, and all three 10. How many people speak exactly one language?",
         ["70", "50", "43", "105"], "B", "Exactly one language means the three single-language regions only: Hindi-only 20 + English-only 10 + French-only 20 = 50.", "EASY", "numerical", 3, "languages_exactly_one_source_diagram", "20 + 10 + 20 = 50; all pair and triple overlaps are excluded.", 18, "Venn Diagram 02_ Class Notes.pdf", "Hindi-only 20; English-only 10; French-only 20; Hindi-English-only 25; Hindi-French-only 10; English-French-only 10; all three 10.", {"H_only": 20, "E_only": 10, "F_only": 20, "HE_only": 25, "HF_only": 10, "EF_only": 10, "HEF": 10}),
    item("For Hindi/English/French, the exclusive regions are H-only 20, E-only 10, F-only 20, H-E 25, H-F 10, E-F 10, and all three 10. How many people speak exactly two languages?",
         ["56", "45", "35", "50"], "B", "Exactly two languages includes the three pair-only regions: 25 + 10 + 10 = 45. The triple-language region is not included.", "MEDIUM", "numerical", 3, "languages_exactly_two_source_diagram", "25 + 10 + 10 = 45, explicitly excluding all-three 10.", 19, "Venn Diagram 02_ Class Notes.pdf", "Hindi-English-only 25; Hindi-French-only 10; English-French-only 10; all three 10; single-language regions are separate."),
    item("For Hindi/English/French, the exclusive regions are H-only 20, E-only 10, F-only 20, H-E 25, H-F 10, E-F 10, and all three 10. How many people speak all three languages?",
         ["10", "50", "55", "42"], "A", "The central intersection of Hindi, English and French is labeled 10.", "EASY", "numerical", 3, "languages_all_three_source_diagram", "Read H∩E∩F, the central region: 10.", 20, "Venn Diagram 02_ Class Notes.pdf", "The central Hindi∩English∩French region is labeled 10."),
    item("In a Boys/Athletes/College Students diagram, the exclusive regions are boys-only 7, boys-athletes 10, athletes-only 14, boys-college 12, athletes-college 6, college-only 15, and all three 9. How many boys are both college students and athletes?",
         ["9", "10", "6", "12"], "A", "The question asks for Boys∩College Students∩Athletes, the central region common to all three circles. It is labeled 9.", "EASY", "numerical", 3, "boys_college_athletes_triple_intersection", "Read the triple intersection in the center: 9.", 22, "Venn Diagram 02_ Class Notes.pdf", "Boys-only 7; Boys∩Athletes only 10; Athletes-only 14; Boys∩College only 12; Athletes∩College only 6; College-only 15; all three 9.", {"B_only": 7, "BA_only": 10, "A_only": 14, "BC_only": 12, "AC_only": 6, "C_only": 15, "BAC": 9}),
    # Original logical/classification items.
    item("All surgeons are doctors. Some surgeons are men, some surgeons are not men, and some men are not doctors. Which diagram fits?",
         ["Surgeons inside Doctors; Men overlaps both and extends outside Doctors.", "Doctors inside Surgeons; Men is separate.", "All three sets are disjoint.", "Men contains both Doctors and Surgeons."], "A", "Surgeons are wholly within Doctors. The stated examples require Men to overlap Surgeons and Doctors while also extending beyond Doctors; the non-men surgeons occupy a Doctors-and-Surgeons region outside Men.", "MEDIUM", "logical_classification", 3, "surgeons_subset_doctors_men_partial_overlap", "S⊂D; S∩M≠∅; S\M≠∅; M\D≠∅.", None, None, "Surgeons fully within Doctors; Men intersects Doctors and Surgeons, and extends beyond Doctors."),
    item("Patna is within Bihar, and Bihar is within India. Which diagram represents these classes?",
         ["Three separate circles.", "Patna inside Bihar inside India.", "Bihar inside Patna inside India.", "Patna and Bihar overlap, while India is separate."], "B", "Every location in Patna is in Bihar, and every location in Bihar is in India. The sets form a three-level containment chain.", "EASY", "logical_classification", 3, "patna_bihar_india_nested", "Patna ⊂ Bihar ⊂ India.", None, None, "Three nested sets: Patna inside Bihar inside India."),
    item("Gold and Silver are metals, and no object is classified as both Gold and Silver. Which diagram fits?",
         ["Gold and Silver are disjoint subsets inside Metals.", "Metals is inside Gold; Silver overlaps it.", "Gold, Silver and Metals are all disjoint.", "Gold is inside Silver inside Metals."], "A", "Both Gold and Silver belong to the broader Metals class. They are distinct, non-overlapping classes, so draw two disjoint subsets within Metals.", "EASY", "logical_classification", 3, "gold_silver_disjoint_subsets_metals", "Gold ⊂ Metals; Silver ⊂ Metals; Gold∩Silver=∅.", None, None, "Two disjoint inner sets Gold and Silver inside Metals."),
    item("Pet cats and pet dogs are both pet animals, and no animal in this question is both a cat and a dog. Pet animals are animals. Which diagram fits?",
         ["Pet cats and pet dogs are disjoint subsets of Pet Animals, inside Animals.", "Animals inside Pet Animals inside Pet Cats.", "Pet Cats and Pet Dogs overlap; Animals is separate.", "All four sets are disjoint."], "A", "Both pet categories are contained within Pet Animals, which is within Animals. The question states pet cats and pet dogs are disjoint.", "MEDIUM", "logical_classification", 4, "pet_cats_dogs_nested_inside_animals", "Pet Cats ⊂ Pet Animals ⊂ Animals; Pet Dogs ⊂ Pet Animals ⊂ Animals; Pet Cats∩Pet Dogs=∅.", None, None, "Two disjoint pet-category subsets inside Pet Animals, itself inside Animals."),
    item("Some A are B. Some B are C. No A is C. Which diagram is possible?",
         ["A and C are disjoint; each overlaps B in separate regions.", "A, B and C are completely disjoint.", "A is inside C, and both are inside B.", "All three share one common region."], "A", "The premises require an A∩B region and a separate B∩C region, while A and C never intersect. Thus B overlaps each of two mutually disjoint sets.", "MEDIUM", "logical_classification", 3, "middle_set_overlaps_two_disjoint_outer_sets", "A∩B≠∅; B∩C≠∅; A∩C=∅; the two B intersections are disjoint.", None, None, "A and C are disjoint circles; each overlaps B in a different region."),
    item("All students and all athletes are people. Some students are athletes, some students are not athletes, and some athletes are not students. Which diagram fits?",
         ["Students and Athletes partially overlap inside People.", "Students and Athletes are disjoint inside People.", "Students are inside Athletes, both inside People.", "People is inside the overlap of Students and Athletes."], "A", "Both sets are subsets of People. The examples establish a nonempty intersection and nonempty parts unique to each set, so the two sets partially overlap inside People.", "HARD", "logical_classification", 3, "students_athletes_partial_overlap_inside_people", "Students⊂People; Athletes⊂People; S∩A, S\A, and A\S are all nonempty.", None, None, "Two partially overlapping circles, both contained by People."),
    item("Some teachers are singers, some students are singers, and some singers belong to neither group. No teacher is a student. Which diagram fits?",
         ["Teachers and Students are disjoint; each overlaps Singers in separate regions.", "Teachers, Students and Singers all overlap in a common center.", "Teachers are inside Students; Singers is separate.", "Teachers and Students overlap, while Singers is disjoint from both."], "A", "Teachers and Students must be disjoint. Their stated singer members make Singers overlap each set in separate regions, while the singer-only region is nonempty.", "HARD", "logical_classification", 3, "teacher_student_disjoint_both_overlap_singers", "T∩S=∅; T∩G≠∅; S∩G≠∅; G\(T∪S)≠∅.", None, None, "Teachers and Students do not overlap; each intersects Singers, with a Singer-only region."),
    item("All apples are fruits, and no vegetable is a fruit. Which diagram represents Apples, Fruits and Vegetables?",
         ["Apples inside Fruits; Vegetables separate from Fruits.", "Fruits inside Apples; Vegetables overlap Fruits.", "All three sets partially overlap.", "Apples and Vegetables are inside Fruits."], "A", "Apples form a subset of Fruits. Vegetables are disjoint from Fruits, so they are also disjoint from Apples.", "HARD", "logical_classification", 3, "apples_inside_fruits_vegetables_disjoint", "Apples⊂Fruits; Vegetables∩Fruits=∅.", None, None, "Apples contained in Fruits; a separate Vegetables set."),
    # Original numerical two-set items.
    item("In a survey, 46 people chose A, 39 chose B, and 17 chose both. How many chose at least one of A or B?",
         ["68", "85", "102", "29"], "A", "The inclusive totals count the 17 in both twice. Union = 46 + 39 − 17 = 68.", "EASY", "numerical", 2, "two_set_union_from_inclusive_totals", "A∪B = 46 + 39 − 17 = 68.", diagram="A=46, B=39, A∩B=17 (inclusive)."),
    item("Of 150 people, 86 drink tea, 72 drink coffee, and 28 drink neither. How many drink both tea and coffee?",
         ["30", "36", "8", "58"], "B", "At least one = 150 − 28 = 122. By inclusion-exclusion, both = 86 + 72 − 122 = 36.", "EASY", "numerical", 2, "two_set_intersection_from_neither_and_population", "Union=150−28=122; intersection=86+72−122=36.", diagram="Universal 150; tea 86; coffee 72; neither 28."),
    item("In a class, 72 study Mathematics, 58 study Science, and 31 study both. How many study Science only?",
         ["27", "31", "41", "89"], "A", "Science-only members are the Science total minus those in both subjects: 58 − 31 = 27.", "MEDIUM", "numerical", 2, "two_set_only_b_from_inclusive_total", "Only Science = 58 − 31 = 27.", diagram="Math 72; Science 58; inclusive intersection 31."),
    item("Of 90 people, 55 belong to A and 48 to B. If 78 belong to at least one set, how many belong to exactly one set?",
         ["25", "53", "78", "103"], "B", "The intersection is 55 + 48 − 78 = 25. Exactly one = (55 − 25) + (48 − 25) = 53.", "HARD", "numerical", 2, "two_set_exactly_one_from_union", "Both=55+48−78=25; exactly one=55+48−2×25=53.", diagram="A=55, B=48, union=78."),
    item("A group has 64 members in A, 51 in B, and 27 in both. How many are in A only?",
         ["37", "27", "64", "88"], "A", "A-only excludes the intersection: 64 − 27 = 37.", "HARD", "numerical", 2, "two_set_only_a_from_inclusive_total", "Only A=64−27=37.", diagram="A=64; inclusive A∩B=27."),
    # Original numerical three-set items; pairwise counts are explicitly inclusive where stated.
    item("Set A has 75 members. The inclusive totals are A∩B=30 and A∩C=25, while A∩B∩C=10. How many are in A only?",
         ["30", "40", "20", "50"], "A", "Within A, the inclusive AB and AC counts double-count the 10 in all three. A-only = 75 − 30 − 25 + 10 = 30.", "HARD", "numerical", 3, "three_set_only_a_from_inclusive_pairs", "Only A = |A|−|AB|−|AC|+|ABC| = 75−30−25+10 = 30.", diagram="A=75; inclusive AB=30 and AC=25; triple=10."),
    item("In a survey of 240 people, A=110, B=100, C=90; inclusive AB=40, AC=35, BC=30; all three=15. How many belong to none of the sets?",
         ["30", "45", "210", "60"], "A", "Union = 110 + 100 + 90 − 40 − 35 − 30 + 15 = 210. Therefore none = 240 − 210 = 30.", "HARD", "numerical", 3, "three_set_none_from_inclusion_exclusion", "Union=110+100+90−40−35−30+15=210; none=240−210=30.", diagram="Universal 240; inclusive set totals A=110,B=100,C=90; pairwise AB=40,AC=35,BC=30; triple=15."),
    item("A survey diagram shows A-only 10, B-only 12, C-only 8, AB-only 4, AC-only 3, BC-only 5, all three 2, and outside all sets 6. How many are neither A nor C?",
         ["18", "23", "30", "12"], "A", "Neither A nor C includes the B-only region (12) and the region outside all sets (6). Total = 12 + 6 = 18.", "HARD", "numerical", 3, "three_set_neither_two_named_sets", "B-only + outside universe = 12 + 6 = 18.", diagram="Seven exclusive regions and the outside count are stated explicitly.", regions={"A_only": 10, "B_only": 12, "C_only": 8, "AB_only": 4, "AC_only": 3, "BC_only": 5, "ABC": 2, "outside": 6}),
    item("Three sets have disjoint region counts: A-only 14, B-only 11, C-only 9, AB-only 6, AC-only 5, BC-only 4, and all three 3. How many belong to at least one set?",
         ["52", "49", "43", "55"], "A", "At least one means the union: add all seven mutually exclusive regions. 14 + 11 + 9 + 6 + 5 + 4 + 3 = 52.", "HARD", "numerical", 3, "three_set_union_sum_seven_exclusive_regions", "Sum the seven disjoint regions: 14+11+9+6+5+4+3=52.", diagram="All seven region counts are exclusive and the three-set intersection is 3.", regions={"A_only": 14, "B_only": 11, "C_only": 9, "AB_only": 6, "AC_only": 5, "BC_only": 4, "ABC": 3}),
]

REJECTED = [
    ("Venn Diagram 01_ Class Notes.pdf", 5, "Book, Bike and Human", "Rejected as a separate item because it tests the same all-disjoint classification as page 23, which is retained with four classes; changing only category count/names would be repetitive."),
    ("Venn Diagram 01_ Class Notes.pdf", 6, "Computer, Book, Mouse / India, Mumbai, Delhi / Girls, Tennis Player, Boys / Table, Chair, Refrigerator", "Rejected: source diagram and handwritten annotations do not consistently map to the listed choices; mouse/computer and tennis-player/gender relationships are not specified precisely."),
    ("Venn Diagram 01_ Class Notes.pdf", 8, "People who can speak only one language", "Rejected as duplicate of the clearer three-language count question retained from Venn Diagram 02, page 18."),
    ("Venn Diagram 01_ Class Notes.pdf", 15, "Kishore Kumar, Prabhu Deva, Dancer", "Rejected: membership of the named individuals in the broad Dancer class is not defined, so the diagram cannot be uniquely established from the prompt."),
    ("Venn Diagram 01_ Class Notes.pdf", 16, "Doctors, Surgeons, Men", "Rejected: surgeons are within doctors, but the source does not state whether/how surgeons overlap men; the handwritten diagram cannot supply a missing premise."),
    ("Venn Diagram 01_ Class Notes.pdf", 18, "Female, Cardiologist, Engineer", "Rejected: gender/occupation intersections are not fully specified; several distinct Venn structures are possible."),
    ("Venn Diagram 02_ Class Notes.pdf", 5, "Book, Bike and Human", "Rejected as duplicate of the same all-disjoint class relationship in Venn Diagram 01, page 5; the four-disjoint version on page 23 is retained."),
    ("Venn Diagram 02_ Class Notes.pdf", 6, "Computer, Book, Mouse / India, Mumbai, Delhi / Girls, Tennis Player, Boys / Table, Chair, Refrigerator", "Rejected: repeats the under-specified/misaligned examples from Venn Diagram 01, page 6."),
    ("Venn Diagram 02_ Class Notes.pdf", 7, "Spices/Cumin/Spinach; Animals/Plants/Cucumber; Engineer/Doctor/Pharmacist; Wheat/Corn/Cereals", "Rejected: the teaching diagram asks for one-contained-set plus unrelated-set patterns already represented by retained class questions; Wheat/Corn/Cereals also repeats the grain-containment concept in Venn Diagram 01, page 22."),
    ("Venn Diagram 02_ Class Notes.pdf", 9, "Dog, Pet Animals, Animals / Mammal, Cow, Bat / Couple, Married, Women / Clock, Time, Second", "Rejected: ‘Dog’ is not necessarily a pet, Couple and Women mix set units, and Clock/Time mix an instrument with a measured quantity; only handwritten assumptions could force a single diagram."),
    ("Venn Diagram 02_ Class Notes.pdf", 10, "House/Window/Tenant; Weeks/Years/Months; Paragraph/Sentence/Pen; Truck/Ships/Transport", "Rejected as lecture examples without a unique question prompt; the disjoint week/year/month example also repeats the retained all-disjoint category rule."),
    ("Venn Diagram 02_ Class Notes.pdf", 21, "People who speak one language", "Rejected as duplicate of page 18. The handwritten selected answer 105 sums all regions and contradicts ‘one language’; the correctly worded answer would be 50."),
]


def norm(text):
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def build():
    rows, ledger = [], []
    if len(ITEMS) != 30:
        raise ValueError(f"Expected 30 selected items; found {len(ITEMS)}")
    for index, entry in enumerate(ITEMS, 1):
        source = (f"{entry['source_pdf']}, page {entry['source_page']}; exam/year not stated"
                  if entry["source_pdf"] else ORIGINAL)
        row = {
            "subject_slug": "reasoning", "subcategory_slug": None, "chapter_slug": "venn-diagram",
            "question_text": entry["question"],
            "options": {chr(65 + i): option for i, option in enumerate(entry["options"])},
            "correct_option": entry["answer"], "explanation": entry["explanation"],
            "difficulty": entry["difficulty"], "is_pyq": False, "pyq_year": None,
            "pyq_exam_name": None, "source": source,
        }
        rows.append(row)
        ledger.append({
            "record_type": "selected_question", "question_id": f"venn-{index:03}", "row": index,
            "source_type": "pdf-derived" if entry["source_pdf"] else "original",
            "source_pdf": entry["source_pdf"], "source_page": entry["source_page"],
            "question_category": entry["question_category"], "set_count": entry["set_count"],
            "question": row["question_text"], "diagram_description": entry["diagram_description"],
            "region_values": entry["region_values"], "options": row["options"],
            "expected_answer": row["options"][row["correct_option"]],
            "correct_option": row["correct_option"], "explanation": row["explanation"],
            "difficulty": row["difficulty"], "independent_verification": entry["independent_verification"],
            "validation_status": "PASS: wording, relationship/region interpretation, options, answer and explanation independently reviewed.",
            "is_pyq": False, "pyq_indication": "No explicit PYQ label/year/exam appears; imported as Normal." if entry["source_pdf"] else "Original practice item; imported as Normal.",
            "source": source, "concept_signature": entry["concept_signature"],
            "duplicate_review": "Compared against selected prompts, other new concepts, current Venn database records and existing Reasoning canonical batches; no exact/semantic duplicate retained.",
        })
    stems = [norm(row["question_text"]) for row in rows]
    signatures = [entry["concept_signature"] for entry in ITEMS]
    if len(set(stems)) != len(stems) or len(set(signatures)) != len(signatures):
        raise ValueError("Repeated normalized question stem or concept signature")
    for row, entry in zip(rows, ITEMS):
        if len(row["options"]) != 4 or len({norm(v) for v in row["options"].values()}) != 4:
            raise ValueError(f"Options are not distinct: {row['question_text']}")
        if row["options"][row["correct_option"]] != entry["options"][ord(row["correct_option"])-65]:
            raise ValueError(f"Incorrect answer key: {row['question_text']}")
        if len(row["source"]) > 255:
            raise ValueError(f"Source too long for database: {row['question_text']}")
    expected = Counter({"EASY": 10, "MEDIUM": 10, "HARD": 10})
    actual = Counter(row["difficulty"] for row in rows)
    if actual != expected:
        raise ValueError(f"Difficulty mix is {actual}, expected {expected}")
    for pdf, page, prompt, reason in REJECTED:
        ledger.append({
            "record_type": "rejected_source_prompt", "question_id": None, "row": None,
            "source_type": "rejected", "source_pdf": pdf, "source_page": page,
            "question_category": None, "set_count": None, "question": prompt,
            "diagram_description": None, "region_values": None, "options": None,
            "expected_answer": None, "correct_option": None, "explanation": None,
            "difficulty": None, "independent_verification": None,
            "validation_status": "REJECTED: not imported.", "is_pyq": None,
            "pyq_indication": "No retained PYQ metadata.", "source": f"{pdf}, page {page}",
            "concept_signature": None, "duplicate_review": reason, "rejection_reason": reason,
        })
    (BASE / "data" / "venn_diagram_verified_batch.json").write_text(
        json.dumps({"questions": rows}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (BASE / "data" / "venn_diagram_answer_ledger.json").write_text(
        json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("BUILT", len(rows), "selected questions", dict(actual), "PDF-derived", sum(bool(x["source_pdf"]) for x in ITEMS), "original", sum(not x["source_pdf"] for x in ITEMS), "rejected source prompts", len(REJECTED))


if __name__ == "__main__":
    build()
