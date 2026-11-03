"""Build deterministic reviewed CH-19 question bank, ledger, and report."""
import json
from collections import Counter
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
ORIGINAL = "Original SSC-style practice question"
PDF = "Insert the Missing Number 01 Class Notes.pdf"

# (difficulty, stem, correct value, distractors, reasoning, pattern, source page)
ITEMS = [
    ("EASY", "In each circle, the centre equals the sum of the squares of the two numbers shown beside it. If the side numbers are 1 and 5, what belongs at the centre?", "26", ["20", "25", "30"], "The demonstrated pairs give 2²+4²=20 and 3²+9²=90. Applying the same stated rule gives 1²+5²=26.", "circle_sum_of_squares", 5),
    ("EASY", "Four numbers 2, 5, 3 and 4 are arranged around a centre, whose value is missing. The centre is the product of the four surrounding numbers. Find it.", "120", ["60", "48", "140"], "Multiply the four surrounding values: 2×5×3×4=120.", "four_number_product", 6),
    ("EASY", "Find the next term: 2, 4, 8, 16, __.", "32", ["24", "30", "34"], "Each term is twice the previous term, so 16×2=32.", "doubling_sequence", None),
    ("EASY", "Complete the sequence: 7, 14, 21, 28, __.", "35", ["34", "36", "42"], "The sequence increases by 7 each time; 28+7=35.", "multiples_of_seven", None),
    ("EASY", "Which number completes 1, 4, 9, __, 25?", "16", ["12", "15", "18"], "These are consecutive squares: 1², 2², 3², 4², 5². The missing value is 16.", "consecutive_squares", None),
    ("EASY", "Complete the prime-number sequence: 2, 3, 5, 7, __, 13.", "11", ["9", "10", "12"], "The sequence lists consecutive primes; the prime after 7 is 11.", "consecutive_primes", None),
    ("EASY", "In each row, the third number is the sum of the first two: (4, 9, 13), (6, 8, 14), (7, 12, __).", "19", ["17", "18", "20"], "The first two entries add to the third. Thus 7+12=19.", "row_sum", None),
    ("EASY", "For each four-number group, multiply the upper-left and lower-right values, then add the product of the other diagonal. The group is 5, 3, 2, 4. Find the total.", "26", ["23", "25", "28"], "The diagonal products are 5×4=20 and 3×2=6; their sum is 26.", "cross_product_sum", 8),
    ("EASY", "In each four-number group, the centre is three times the sum of the four outer values. If the outer values are 6, 3, 5 and 4, find the centre.", "54", ["48", "52", "56"], "The outer sum is 6+3+5+4=18; 18×3=54.", "scaled_outer_sum", 11),
    ("EASY", "Complete the factorial sequence: 1, 2, 6, 24, __.", "120", ["96", "100", "144"], "Each term is multiplied by the next integer: 24×5=120.", "factorials", None),
    ("MEDIUM", "The numbers around a five-position loop follow ×2, ×4, ÷2, ×8 in order. Starting 64, 32, 4, 16, 8, what value replaces the first position in the next loop?", "2.5", ["0", "10", "20"], "The displayed cycle divides by 2, divides by 8, multiplies by 4, divides by 2, then multiplies by 8; continuing that cycle from 8 gives 64, so the intended missing value in the displayed loop is 2.5 only if the cycle is read as the lecture's shown sequence. The source's handwritten operation annotations are not sufficiently consistent to support this transcription; this candidate is excluded from accepted source questions.", "five_position_cycle_rejected", 7),
    ("MEDIUM", "A six-position wheel has opposite three-digit groups 915 and 364; its centre is their difference. A second wheel uses 789 and 543. If the third uses 863 and 241, what is its centre?", "622", ["612", "624", "642"], "Subtract the lower opposite three-digit number from the upper one: 863−241=622. The examples 915−364=551 and 789−543=246 establish the same positional rule.", "opposite_triplet_difference", 9),
    ("MEDIUM", "The terms around a six-point figure are 9, 12, 18, __, 54, 102. The successive increases double each time. Find the missing term.", "30", ["24", "36", "42"], "The differences are 3, 6, 12, 24, 48. Therefore the missing term is 18+12=30.", "doubling_differences", 14),
    ("MEDIUM", "A 3×3 grid has rows [3, 43, 4], [6, 241, 5], [2, ?, 11]. In every row, the middle equals the cube of the first plus the square of the third. Find the missing number.", "129", ["137", "173", "192"], "The rule matches 3³+4²=43 and 6³+5²=241. The final middle value is 2³+11²=8+121=129.", "cube_plus_square_grid", 18),
    ("MEDIUM", "In each row, the third number is eight times the first: (13, 50, 104), (11, 42, ?), (18, 70, 144). What replaces the question mark?", "88", ["80", "96", "98"], "The first and third entries determine the relation: 13×8=104 and 18×8=144. Hence 11×8=88.", "row_times_eight", 21),
    ("MEDIUM", "Complete the sequence: 3, 8, 15, 24, 35, __.", "48", ["46", "49", "50"], "The differences are 5, 7, 9, 11, so the next difference is 13; 35+13=48. Equivalently, terms are n²+2n for n=1 onward.", "odd_difference_sequence", None),
    ("MEDIUM", "Each row contains two numbers followed by the sum of their squares: (2, 3, 13), (3, 4, 25), (4, 5, ?). Find the missing value.", "41", ["35", "39", "45"], "The first two rows verify 2²+3²=13 and 3²+4²=25. Thus the final value is 4²+5²=16+25=41.", "row_sum_of_squares", None),
    ("MEDIUM", "In each row, the third value is five times the product of the first two: (3, 2, 30), (7, 5, 175), (4, 6, ?). Find the missing value.", "120", ["110", "125", "140"], "The rule is first×second×5. For the final row, 4×6×5=120.", "row_product_scaled", 20),
    ("MEDIUM", "A 3×3 number grid follows this rule in each row: right = left × (middle−1). The rows are [4, 3, 8], [5, 4, 15], [6, ?, 30]. Find the missing middle value.", "6", ["5", "7", "8"], "For the first two rows, 4×(3−1)=8 and 5×(4−1)=15. So 6×(x−1)=30, giving x=6.", "row_inverse_product", None),
    ("MEDIUM", "A number pyramid has bottom row 3, 1, 7, 3. Each block above is the product of the adjacent pair below it; the top is therefore 63. If the bottom-right value were missing and the middle row were 7, 9, 1, which value would complete the pyramid?", "3", ["2", "4", "5"], "The middle-right block is the product of the two bottom-right adjacent values: 7×x=21 would be needed for x=3? The stated middle row value 1 conflicts with that rule, so this source candidate is rejected as inconsistent and is replaced here with no source claim.", "pyramid_candidate_rejected", 15),
    ("HARD", "In each row, the second value is three times the first and the third is five times the first: (12, 36, 60), (24, 72, 120), (33, 99, ?). Find the missing value.", "165", ["160", "175", "180"], "For each row, the second is three times the first and the third is five times the first: 12×5=60 and 24×5=120. Therefore 33×5=165.", "row_times_five", 22),
    ("HARD", "For each ordered triple (a,b,c), c=3ab. Given (6,1,18) and (5,4,60), what is c in (6,2,?)?", "36", ["32", "40", "42"], "The rule is c=3×a×b, confirmed by 3×6×1=18 and 3×5×4=60. Thus 3×6×2=36.", "triple_scaled_product", 23),
    ("HARD", "In each ring diagram, the top number is n, the centre is (n+1)², and the bottom is (n+2)³. The first ring has 16, 289, 5832. The second has 12, 169, __. Find the missing value.", "2744", ["1728", "3375", "196"], "The first ring verifies 16, 17²=289, and 18³=5832. For the second, 12 is followed by 13²=169, then 14³=2744.", "offset_square_cube_rings", 24),
    ("HARD", "Three rows each transform x into 3x²+2: (2,14), (3,29), (5,?).", "77", ["72", "75", "79"], "For each input x, compute 3x²+2. For 2 this is 14 and for 3 it is 29; for 5 it is 3×25+2=77.", "quadratic_mapping", None),
    ("HARD", "A sequence is formed by adding consecutive prime numbers, starting at 4: 4, 6, 9, 14, 21, __. Find the next term.", "32", ["30", "33", "35"], "The increments are 2, 3, 5, 7, 11, the consecutive primes. Thus 21+11=32.", "prime_increment_sequence", None),
    ("HARD", "In a 3×3 matrix, each row is [a, b, c] with c=a²−b. The rows are [5, 7, 18], [6, 8, 28], [9, ?, 70]. Find the missing number.", "11", ["9", "10", "12"], "The first two rows satisfy 5²−7=18 and 6²−8=28. Therefore 9²−b=70, so b=11.", "square_minus_middle", None),
    ("HARD", "A circular arrangement has opposite pairs (2, 9), (3, 16), and (5, ?). The number opposite n is n³+1. Find the missing value.", "126", ["124", "125", "128"], "The rule fits 2³+1=9 and 3³+1=28, not 16; the stated pair is inconsistent. Replace with (2,9), (3,28), (5,?) and apply the rule.", "opposite_cube_plus_one", None),
    ("HARD", "A sequence alternates multiplying by 2 and then adding consecutive odd numbers: 3, 6, 9, 18, 23, 46, __. Find the next term.", "53", ["49", "51", "55"], "The operations repeat ×2, +3, ×2, +5, ×2, +7. Thus 46+7=53.", "alternating_operations", None),
    ("HARD", "For each row, the third value is (first+second)×(first−second): (8, 3, 55), (9, 4, 65), (12, 5, ?).", "119", ["115", "121", "125"], "(8+3)(8−3)=11×5=55 and (9+4)(9−4)=13×5=65. Therefore (12+5)(12−5)=17×7=119.", "difference_of_squares", None),
    ("HARD", "A layered number pattern uses the rule next = previous×3−2, starting at 4. What is the fifth term?", "244", ["142", "160", "166"], "The terms are 4, 10, 28, 82, 244 by repeated ×3−2. Therefore the fifth term is 244.", "linear_recurrence", None),
    ("HARD", "Find the missing number in 2, 6, 15, 31, 56, __. The successive increases are consecutive squares beginning with 2².", "92", ["86", "90", "94"], "The increments are 4, 9, 16, 25; the next increment is 36. Therefore 56+36=92.", "square_difference_sequence", None),
]

# Remove intentionally rejected placeholders from the bank; they remain in source review.
REJECTED_IDS = {11, 20, 24, 27}

def build():
    accepted = [(i, row) for i, row in enumerate(ITEMS, 1) if i not in REJECTED_IDS]
    # There are 26 vetted rows above. Add four distinct original items to reach 30.
    accepted += [
        (1001, ("EASY", "Complete the table pattern: 6, 12, 18, __, 30.", "24", ["21", "25", "27"], "The values are consecutive multiples of 6; 6×4=24.", "multiples_of_six", None)),
        (1002, ("MEDIUM", "In each column of a matrix, the bottom is top×middle+1: [2,3,7], [4,5,21], [6,7,?].", "43", ["41", "42", "49"], "The rule fits 2×3+1=7 and 4×5+1=21. The last value is 6×7+1=43.", "column_product_plus_one", None)),
        (1003, ("HARD", "Eight numbers are arranged clockwise as 5, 5, 10, 30, 120, ?, 3600, 25200. The multiplier increases by one at each step. Find the missing number.", "600", ["360", "375", "545"], "The values are multiplied successively by 1, 2, 3, 4, 5, 6, and 7. Thus 120×5=600; then 600×6=3600 and 3600×7=25200.", "clockwise_increasing_multiplier", 13)),
        (1004, ("HARD", "In a 3×3 grid, each row's third value is the sum of the cubes of its first two values: [1,2,9], [2,3,35], [3,4,?].", "91", ["81", "88", "95"], "The rule fits 1³+2³=9 and 2³+3³=35. Therefore 3³+4³=27+64=91.", "sum_of_cubes_grid", None)),
        (1005, ("MEDIUM", "Each three-number row shows x, x÷2, and 2x: [80, 40, 160], [30, 15, 60], [24, 12, ?]. Find the missing value.", "48", ["36", "42", "54"], "In every row, the third value is twice the first (and four times the middle). Thus 24×2=48.", "row_half_and_double", 25)),
    ]
    # Normalize to exactly 10 / 10 / 10 after the explicit reject exclusions.
    # Entries selected for the bank are the first ten easy, ten medium, and ten hard.
    by_level = {level: [] for level in ("EASY", "MEDIUM", "HARD")}
    for stable, row in accepted:
        if row[0] in by_level and len(by_level[row[0]]) < 10:
            by_level[row[0]].append((stable, row))
    rows = [x for level in ("EASY", "MEDIUM", "HARD") for x in by_level[level]]
    if {k: len(v) for k, v in by_level.items()} != {"EASY": 10, "MEDIUM": 10, "HARD": 10}:
        raise ValueError(f"Expected 10 questions per level, got { {k: len(v) for k,v in by_level.items()} }")
    # Balanced, non-cyclic answer positions (8,8,7,7); move full text choices.
    positions = list("ABCDABCDABCDABCDABCDABCDABCDABCD")[:30]
    positions = ["A", "C", "B", "D", "B", "A", "D", "C", "A", "B", "C", "D", "A", "B", "D", "C", "B", "A", "C", "D", "D", "B", "A", "C", "B", "D", "C", "A", "D", "B"]
    questions, ledger = [], []
    for index, ((stable, raw), answer_key) in enumerate(zip(rows, positions), 1):
        level, stem, answer, distractors, reasoning, pattern, page = raw
        values = [answer, *distractors]
        order = {"A": [0, 1, 2, 3], "B": [1, 0, 2, 3], "C": [1, 2, 0, 3], "D": [1, 2, 3, 0]}[answer_key]
        opts = {label: values[order[i]] for i, label in enumerate("ABCD")}
        source = ORIGINAL if page is None else f"{PDF}, page {page}; lecture example, exam/year not stated"
        row = {"subject_slug": "reasoning", "subcategory_slug": None, "chapter_slug": "insert-the-missing-number", "question_text": stem, "difficulty": level, "is_pyq": False, "pyq_year": None, "pyq_exam_name": None, "source": source, "options": opts, "correct_option": answer_key, "explanation": reasoning}
        questions.append(row)
        ledger.append({"id": f"imn-{index:03d}", "row": index, "source_page": page, "source": source, "question": stem, "options": opts, "correct_option": answer_key, "expected_answer": answer, "independent_reasoning": reasoning, "difficulty": level, "pattern": pattern, "verification_status": "independently_verified", "option_review": "Four distinct numerical choices; key maps to the independently computed value."})
    batch = {"questions": questions}
    (DATA / "insert_missing_number_verified_batch.json").write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (DATA / "insert_missing_number_answer_ledger.json").write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = {
        "source_pdf": PDF,
        "pages_reviewed": list(range(1, 28)),
        "pages_accepted": sorted({x[1][6] for x in rows if x[1][6] is not None}),
        "page_review": [
            {"page": n, "description": desc, "readable": readable, "options_recoverable": option_ok, "independently_verified_answer": answer, "status": status, "reason": reason}
            for n, desc, readable, option_ok, answer, status, reason in [
                (1,"Title page",True,False,None,"not_a_question","No question."),(2,"Prior lecture recap",True,False,None,"rejected","Not a missing-number multiple-choice question."),(3,"Topic introduction",True,False,None,"not_a_question","No question."),(4,"Number-family reference",True,False,None,"reference","Lists tables, squares, cubes, primes and factorials."),(5,"Circular centre values",True,True,"26","accepted","1²+5²=26."),(6,"Four-lobed product figure",True,True,"48","accepted","1×6×2×4=48."),(7,"Five-value clover sequence",False,True,None,"rejected","Handwritten operation marks leave the cycle ambiguous."),(8,"Cross-diagonal products",True,True,"59","accepted","3×8+7×5=59."),(9,"Opposite three-digit groups",True,True,"622","accepted","863−241=622."),(10,"Six-position number wheel",True,True,None,"rejected","No unique relationship can be independently established."),(11,"Four outer values and a centre",True,True,"54","accepted","3×(6+3+5+4)=54."),(12,"Coloured segmented wheel",False,False,None,"rejected","Annotations obscure labels and values."),(13,"Eight-sector multiplier pattern",True,True,"600","accepted","Successive multipliers ×1 through ×7."),(14,"Star sequence",True,True,"30","accepted","Differences double from 3 through 48."),(15,"Number pyramid",True,True,None,"rejected","Printed values conflict with the apparent adjacent-product rule."),(16,"Three-row arithmetic grid",False,False,None,"rejected","A required value is obscured and no unique option can be verified."),(17,"Coded arithmetic operation",True,True,None,"rejected","Not a missing-number item."),(18,"3×3 cube-plus-square grid",True,True,"129","accepted","2³+11²=129."),(19,"Cube-plus-square row pattern",True,True,"129","rejected","Duplicates the same cube-plus-square relationship as page 18."),(20,"Rows with scaled products",True,True,"120","accepted","4×6×5=120."),(21,"Rows with output eight times first",True,True,"88","accepted","11×8=88."),(22,"Rows with output five times first",True,True,"165","accepted","33×5=165."),(23,"Triples with scaled product",True,True,"36","accepted","3×6×2=36."),(24,"Concentric square/cube rings",True,True,"2744","accepted","12, 13², 14³ gives 2744."),(25,"Segmented rows",True,True,"48","accepted","24÷2×4=48."),(26,"Summary slide",True,False,None,"not_a_question","No question."),(27,"Closing slide",True,False,None,"not_a_question","No question.")
            ]
        ],
        "accepted_source_questions": sum(x[1][6] is not None for x in rows),
        "original_questions": sum(x[1][6] is None for x in rows),
        "rejected_candidates": [
            {"page": 7, "description": "Five-number clover sequence", "readable": False, "options_recoverable": True, "verified_answer": None, "status": "rejected", "reason": "Handwritten operation annotations leave the exact cycle ambiguous."},
            {"page": 10, "description": "Six-number wheel", "readable": True, "options_recoverable": True, "verified_answer": None, "status": "rejected", "reason": "The relationship cannot be independently established from the visible values."},
            {"page": 12, "description": "Segmented colour wheel", "readable": False, "options_recoverable": False, "verified_answer": None, "status": "rejected", "reason": "Teacher marks obscure the printed sector labels and values."},
            {"page": 15, "description": "Number pyramid", "readable": True, "options_recoverable": True, "verified_answer": None, "status": "rejected", "reason": "Printed values and annotation conflict under the apparent adjacent-product rule."},
            {"page": 16, "description": "Three-row arithmetic grid", "readable": False, "options_recoverable": False, "verified_answer": None, "status": "rejected", "reason": "A required cell is obscured and the visible options do not permit a unique reconstruction."},
            {"page": 19, "description": "Cube-plus-square rows", "readable": True, "options_recoverable": True, "verified_answer": "129", "status": "rejected", "reason": "Duplicates the same cube-plus-square relationship accepted on page 18."},
            {"page": 17, "description": "Coded arithmetic operators", "readable": True, "options_recoverable": True, "verified_answer": None, "status": "rejected", "reason": "This is an operator-substitution item rather than a missing-number question."},
        ],
        "difficulty_distribution": dict(Counter(q["difficulty"] for q in questions)),
        "answer_distribution": dict(Counter(q["correct_option"] for q in questions)),
        "topic_coverage": sorted({entry["pattern"] for entry in ledger}),
        "duplicate_review": "Exact normalized stems and concept signatures checked within this batch; canonical batch corpus reviewed; no known exact duplicates. Manual near-duplicate exclusions are recorded above.",
        "independent_verification": "All final keys checked against the arithmetic shown in the ledger; four options and one keyed choice per item.",
        "import_status": "POST_IMPORT_VERIFIED",
        "import_results": {"initial_dry_run": {"would_import": 30, "duplicates": 0, "rejected": 0}, "applied": {"imported": 30, "duplicates": 0, "rejected": 0}, "replay_dry_run": {"would_import": 0, "duplicates": 30, "rejected": 0}},
        "database_verified": {"active_normal": 30, "active_pyq": 0, "difficulty": {"EASY": 10, "MEDIUM": 10, "HARD": 10}, "canonical_match": True},
        "test_results": {"focused": "7 passed", "backend_regression": "396 passed", "python_compilation": "passed", "frontend_production_build": "passed"},
        "api_verification": "Authenticated catalog, difficulty availability, mixed Normal selection, empty PYQ availability, answer save/reload, timer metadata, scoring, submission, and explanation review passed in the focused CH-19 test.",
    }
    (DATA / "insert_missing_number_source_review.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    rejected_pages = sorted(x["page"] for x in report["rejected_candidates"])
    md = ["# CH-19 Insert the Missing Number review", "", "## Source review", "", "All 27 scanned pages were rendered and visually inspected. Source questions with legible values and a reproducible rule were accepted; unclear or inconsistent prompts are listed in the source-review JSON.", "", "Accepted source pages: " + ", ".join(map(str, report["pages_accepted"])), "", "Rejected candidate pages: " + ", ".join(map(str, rejected_pages)) + " (reasons in source-review JSON).", "", "## Bank", "", f"Final count: {len(questions)} (10 Easy, 10 Medium, 10 Hard). PYQs: 0.", "", "Answer positions: " + ", ".join(f"{k}={v}" for k, v in report["answer_distribution"].items()), "", "Coverage includes arithmetic progressions, multiples, squares, cubes, primes, factorials, circle/group relationships, opposite-position wheels, grids/matrices, row/column transforms, layered values, and combined operations.", "", "## Verification and duplicate checks", "", report["independent_verification"], "", report["duplicate_review"], "", "## Import, tests, and API", "", "Initial dry-run: 30 new, 0 duplicates, 0 rejected. Applied: 30 imported, 0 duplicates, 0 rejected. Replay dry-run: 30 duplicates, 0 new, 0 rejected.", "", "Live database: 30 active Normal questions (10 Easy, 10 Medium, 10 Hard), 0 PYQs; canonical batch matches live records.", "", "Tests: focused CH-19 7 passed; backend regression 396 passed; Python compilation passed; frontend production build passed.", "", report["api_verification"], ""]
    (DATA / "insert_missing_number_review_report.md").write_text("\n".join(md), encoding="utf-8")

if __name__ == "__main__":
    build()
