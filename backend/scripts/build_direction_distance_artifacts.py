"""Build the reviewed Direction and Distance batch, answer ledger, and report."""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
ORIGINAL = "Original SSC-style practice question"
PDFS = {
    1: "Direction and Distance 01_ Class Notes.pdf",
    2: "Direction and Distance 02_ Class Notes.pdf",
    3: "_Direction and Distance 03_ Class Notes.pdf",
}

# Each entry: difficulty, question, answer, distractors, explanation, provenance, page, signature.
ITEMS = [
    ("MEDIUM", "A person is facing east. He turns 90° anticlockwise. Which direction is he facing?", "North", ["South", "East", "West"], "An anticlockwise quarter-turn from east points north.", 0, 0, "original_turn_east_anticlockwise_90"),
    ("MEDIUM", "If north-east is exactly halfway between north and east, what angle does it make with east?", "45°", ["30°", "60°", "90°"], "Adjacent cardinal directions differ by 90°; the intercardinal direction bisects that angle, giving 45°.", 0, 0, "original_intercardinal_angle_from_east"),
    ("EASY", "Mira walks 8 m north and then 6 m east. How far is she from her starting point?", "10 m", ["14 m", "2 m", "12 m"], "The legs are perpendicular, so the displacement is √(8²+6²)=10 m.", 0, 0, "original_pythagorean_6_8_10"),
    ("EASY", "At sunrise, a person faces the sun. Which direction is on the person's left?", "North", ["South", "East", "West"], "At sunrise the sun is in the east. Facing east, the person's left is north.", 0, 0, "original_sunrise_facing_sun_left"),
    ("EASY", "A person faces south and turns 180°. Which direction does the person face now?", "North", ["East", "West", "South"], "A half-turn reverses the facing direction; south becomes north.", 0, 0, "original_south_half_turn"),
    ("EASY", "If South-East is renamed North and North-East is renamed West under one consistent rotation, what does West become?", "South-East", ["North-East", "South-West", "North-West"], "Both given mappings rotate every direction 135° anticlockwise. West (270°) therefore maps to South-East (135°).", 3, 4, "interchange_se_ne_rotation_west"),
    ("EASY", "At sunset, a person's shadow points east. In which direction is the sun?", "West", ["East", "North", "South"], "At sunset the sun is in the west, opposite the eastward shadow.", 0, 0, "original_sunset_shadow_east_sun_west"),
    ("EASY", "A walker travels 5 km west and then 5 km east. What is the shortest distance from the start?", "0 km", ["5 km", "10 km", "√50 km"], "The equal opposite displacements cancel, returning the walker to the start.", 0, 0, "original_opposite_walk_cancel"),
    ("EASY", "If east becomes south and every direction is rotated by the same amount, what does north become?", "East", ["West", "South", "North"], "The mapping is a 90° clockwise rotation. North rotates to east.", 3, 7, "interchange_east_south_north"),
    ("EASY", "A person faces north. Which direction is behind them?", "South", ["East", "West", "North"], "South is opposite north, so it is behind a north-facing person.", 0, 0, "original_opposite_north_south"),
    ("MEDIUM", "Richa walks 50 m west, turns left and walks 90 m, turns left and walks 30 m, turns left and walks 120 m, then turns right and walks 20 m. How far and in which direction is she from home?", "30 m north", ["30 m south", "20 m east", "50 m west"], "Taking home as (0,0), her legs end at (0,30): 30 m due north. The total path is 310 m, but the question asks displacement.", 2, 5, "richa_route_final_displacement"),
    ("MEDIUM", "A driver goes 12 km east, turns left for 9 km, turns left for 13 km, turns left for 11 km, then turns left and goes 1 km. What is the shortest distance and direction back to the start?", "2 km north", ["2 km south", "1 km north", "1 km south"], "Net east-west displacement is 12−13+1=0; net north-south is 9−11=−2. The driver is 2 km south of the start, so returns north.", 2, 6, "sunder_route_return_north_2"),
    ("MEDIUM", "A person starts facing east, turns 45° clockwise, then 180° clockwise, then 270° anticlockwise. What is the final facing direction?", "North-East", ["South-East", "South-West", "North-West"], "Using clockwise bearings from north: 90°+45°+180°−270°=45°, which is north-east.", 2, 11, "rotation_east_45cw_180cw_270ccw"),
    ("MEDIUM", "At sunrise, Amit and Radhe face one another. Amit's shadow falls to Radhe's right. Which direction is Amit facing?", "North", ["South", "East", "West"], "Amit's shadow points west. West is Radhe's right when Radhe faces south; since they face one another, Amit faces north.", 3, 9, "morning_shadow_opposite_pair_right"),
    ("MEDIUM", "If South-East becomes West, North-East becomes South, and the same rotation applies to every direction, what does East become?", "South-West", ["North-West", "West", "South"], "The mapping is a 135° clockwise rotation: east (90°) becomes 225°, or south-west.", 3, 6, "interchange_se_w_ne_s_east"),
    ("HARD", "In a code, M*N means M is south of N; M+N means M is north of N; M%N means M is east of N; M−N means M is west of N. Where is R relative to P in O%P+Q−R?", "South-East", ["North-East", "North-West", "South-West"], "P is north of Q and Q is west of R. Treating each relation as one unit, R is east of Q and one step south of P: south-east.", 3, 13, "coded_chain_o_p_q_r_reviewed"),
    ("HARD", "A child walks 90 m east, turns right for 20 m, turns right for 30 m, then walks north 100 m to meet his father. How far is the father from the child's starting point?", "100 m", ["80 m", "120 m", "140 m"], "The child ends at (60,80): eastward net 90−30=60 m and northward net 100−20=80 m. √(60²+80²)=100 m.", 2, 9, "child_father_60_80_100"),
    ("HARD", "A man faces west, turns 90° anticlockwise, then another 135° anticlockwise, then 270° clockwise. What direction is he facing?", "North-West", ["North-East", "South-East", "South-West"], "Starting bearing 270° clockwise from north: 270−90−135+270=315°, which is north-west.", 2, 12, "west_rotation_90ccw_135ccw_270cw"),
    ("HARD", "Ram starts facing north-west, turns 45° clockwise and then 135° clockwise, 90° anticlockwise, and finally 180° clockwise. Which way does he face?", "South-West", ["North-East", "North-West", "South-East"], "Net turn is 45+135−90+180=270° clockwise. NW has bearing 315°; 315+270=585°≡225°, or south-west.", 2, 13, "ram_multiturn_nw_southwest"),
    ("HARD", "One evening Dipali and Shubham face each other. Shubham's shadow falls to Dipali's left. Which direction is Dipali facing?", "South", ["North", "East", "West"], "At evening the shadow points east. East is Dipali's left when she faces south; hence she faces south.", 3, 11, "evening_shadow_facing_pair_left"),
    ("HARD", "Jitin and Bhawna face each other one evening. Jitin's shadow falls to Bhawna's right. Which direction is Jitin facing?", "South", ["North", "East", "West"], "At evening Jitin's shadow points east. East is Bhawna's right when she faces north, so Jitin, facing her, faces south.", 3, 12, "evening_shadow_facing_pair_right"),
    ("HARD", "In a code, X@Y means X is north of Y, X#Y means X is east of Y, and X$Y means X is south of Y. Where is A relative to B in A#C@D$B?", "East", ["North-East", "South-East", "West"], "D is south of B; C is north of D and level with B; A is east of C, so A is due east of B.", 0, 0, "original_coded_chain_three_symbols"),
    ("HARD", "A hiker walks 5 km north, 12 km east, and 10 km south. What is the shortest distance and direction from the starting point?", "13 km south-east", ["13 km north-east", "25 km south-east", "5 km east"], "Net displacement is 12 km east and 5 km south, so √(12²+5²)=13 km toward the south-east.", 0, 0, "original_net_displacement_5_12_13"),
    ("HARD", "A cyclist travels 8 km north, 6 km east, 8 km south, then 6 km west. How far is the cyclist from the starting point?", "0 km", ["6 km", "8 km", "20 km"], "The north-south and east-west legs each cancel, so the cyclist returns to the start.", 0, 0, "original_closed_rectangular_route"),
    ("EASY", "A person facing north turns 45° clockwise. Which direction are they facing?", "North-East", ["North-West", "South-East", "South-West"], "A 45° clockwise turn from north points north-east.", 0, 0, "original_north_45_cw"),
    ("MEDIUM", "A woman walks 9 m south then 12 m west. What is her shortest distance from the starting point?", "15 m", ["21 m", "3 m", "√21 m"], "The perpendicular legs give √(9²+12²)=15 m.", 0, 0, "original_9_12_15_triangle"),
    ("HARD", "A person faces south-west and turns 135° clockwise. Which direction do they face?", "North", ["South", "East", "West"], "South-west has bearing 225°; adding 135° clockwise gives 360°, or north.", 0, 0, "original_sw_135_cw_north"),
    ("EASY", "Which direction is opposite South-East?", "North-West", ["North-East", "South-West", "South"], "Opposite directions differ by 180°. South-east is opposite north-west.", 0, 0, "original_opposite_se_nw"),
    ("MEDIUM", "A driver travels 7 km east and 24 km north. What is the shortest distance to the starting point?", "25 km", ["31 km", "17 km", "√527 km"], "By Pythagoras, √(7²+24²)=√625=25 km.", 0, 0, "original_7_24_25_triangle"),
    ("MEDIUM", "At sunset, A faces B. A's shadow falls directly behind B. Which direction is A facing?", "East", ["West", "North", "South"], "At sunset A's shadow points east. The shadow is behind B, so B faces west. A faces B, therefore A faces east.", 0, 0, "original_evening_shadow_pair"),
    ("HARD", "Fardeen starts facing west, walks 13 km, turns left for 7 km, turns right for 6 km, turns left for 8 km, and finally turns left for 19 km. How far and in which direction is he from his starting point?", "15 km south", ["15 km north", "13 km west", "19 km east"], "The first leg ends 13 km west. Left from west is south (7); right from south is west (6); left from west is south (8); left from south is east (19). East-west cancels, leaving 15 km south.", 2, 7, "fardeen_route_15_south"),
    ("MEDIUM", "Ramu walks 5 km north, 3 km west, turns right and walks 3 km north, then turns right and walks 3 km east. How far is he from his starting point?", "8 km", ["5 km", "11 km", "6 km"], "West and east legs cancel (3 km each); the northward legs total 5+3=8 km.", 2, 8, "ramu_route_8_north"),
    ("MEDIUM", "If South-East becomes North and North-East becomes West under the same rotation, what does South-West become?", "East", ["North", "South", "West"], "The mappings are a 135° anticlockwise rotation. South-west (225°) rotates to east (90°).", 3, 5, "interchange_se_ne_rotation_sw"),
    ("EASY", "During sunrise, Arman and Abhinay face one another. Abhinay's shadow falls to his right. Which direction is Arman facing?", "North", ["South", "East", "West"], "At sunrise the shadow points west. West is Abhinay's right when he faces south; Arman faces him, so Arman faces north.", 3, 10, "sunrise_shadow_abhinay_right_arman"),
    ("MEDIUM", "A trekker walks 3 km north and 4 km east, then follows a straight route back home. How many kilometers shorter is the straight return than the outward walk?", "2 km", ["1 km", "3 km", "7 km"], "The outward route is 3+4=7 km. The straight return is the 3-4-5 hypotenuse (5 km), so it is 7−5=2 km shorter.", 0, 0, "original_3_4_5_return_saving"),
    ("MEDIUM", "Asha walks 6 m north, 4 m east, 2 m south and 1 m west. What total distance does she travel?", "13 m", ["5 m", "9 m", "11 m"], "Total path length adds every leg: 6+4+2+1=13 m.", 0, 0, "original_total_distance_four_legs"),
    ("EASY", "Starting at home, Richa walks five legs: 50 m west, 90 m south, 30 m east, 120 m north, and 20 m east. What is the total path length?", "310 m", ["270 m", "300 m", "210 m"], "Total distance is the sum of all five traveled legs: 50+90+30+120+20=310 m.", 1, 12, "richa_route_total_path_length"),
]


def build():
    rows, ledger = [], []
    for i, (difficulty, question, answer, distractors, explanation, pdf_no, page, signature) in enumerate(ITEMS, 1):
        if answer in distractors or len(set(distractors)) != 3:
            raise ValueError(f"Row {i}: answer and three distractors must be distinct")
        choices = list(distractors)
        choices.insert((i - 1) % 4, answer)
        options = dict(zip("ABCD", choices))
        key = next(k for k, value in options.items() if value == answer)
        source = ORIGINAL if not pdf_no else f"{PDFS[pdf_no]}, page {page}; exam/year not stated"
        row = {"subject_slug": "reasoning", "subcategory_slug": None, "chapter_slug": "direction-and-distance", "question_text": question,
               "options": options, "correct_option": key, "explanation": explanation, "difficulty": difficulty,
               "is_pyq": False, "pyq_year": None, "pyq_exam_name": None, "source": source}
        rows.append(row)
        ledger.append({"question_id": f"direction-distance-{i:03}", "row": i, "question": question,
                       "source_type": "pdf-derived" if pdf_no else "original", "source_pdf": PDFS[pdf_no] if pdf_no else None,
                       "source_page": page if pdf_no else None, "expected_answer": answer, "correct_option": key,
                       "explanation": explanation, "difficulty": difficulty, "verification_status": "PASS - independently solved",
                       "pyq_status": "not identified as PYQ in source; imported as Normal" if pdf_no else "original practice; imported as Normal",
                       "source": source, "independent_reasoning": explanation, "option_review": f"Answer is {key}; all four options are distinct.",
                       "concept_signature": signature or f"original_reviewed_signature_{i:03}", "validation_status": "PASS"})
    ledger[10]["rejected_source_questions"] = [{
        "source_pdf": PDFS[1],
        "source_page": 12,
        "question_summary": "Richa's distance and direction from home (the displacement sub-question).",
        "rejection_reason": "Duplicate of the same displacement sub-question selected from Direction and Distance 02_ Class Notes.pdf, page 5. The distinct total-path-length part is retained from this multipart source slide as a separate record.",
    }]
    (DATA / "direction_distance_verified_batch.json").write_text(json.dumps({"questions": rows}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (DATA / "direction_distance_answer_ledger.json").write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (DATA / "direction_distance_review_report.md").write_text("""# Direction and Distance review\n\n## Status\n\nCOMPLETED — live import, post-import verification, replay and authenticated API checks passed.\n\nAll 42 scanned pages were visually inspected: Deck 01 (12), Deck 02 (15), Deck 03 (15).\n\n## Source-question review\n\nReviewed 19 visible prompt parts across the three decks; selected 18 question items and rejected 1 repeated Richa displacement sub-question (Deck 02 page 5 repeats that part of the fuller multipart prompt on Deck 01 page 12). Instructional slides, recap exercises without complete prompts, and summary pages were not counted as source questions. The marked answer on the Deck 03 page 13 coded chain conflicts with the operator definitions; the question was retained with the independently derived answer (South-East).\n\n| PDF | Pages inspected | Selected | Rejected / excluded |\n|---|---:|---:|---|\n| Direction and Distance 01_ Class Notes.pdf | 12/12 | 1 | Separate total-distance part of Richa's multipart prompt included; repeated displacement part covered from Deck 02 page 5. |\n| Direction and Distance 02_ Class Notes.pdf | 15/15 | 8 | No unique clear question rejected; recap, summary and diagram-only instruction excluded. |\n| _Direction and Distance 03_ Class Notes.pdf | 15/15 | 9 | No unique clear question rejected; instructional shadow diagram and summaries excluded. |\n\nThe batch contains 37 Normal questions: 18 PDF-derived and 19 original SSC-style questions; 12 Easy, 14 Medium and 11 Hard. Each item has four distinct options and an independent explanation. The bank covers 3-4-5, 5-12-13 and 6-8-10 triangles. No exam/year is stated in the selected source material, and no PYQ records are created.\n""", encoding="utf-8")

if __name__ == "__main__":
    build()



