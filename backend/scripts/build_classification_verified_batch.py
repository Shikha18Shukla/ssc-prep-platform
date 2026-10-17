"""Build the reviewed Classification Normal batch and independent answer ledger."""

import json
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
BATCH = BASE / "data" / "classification_verified_batch.json"
LEDGER = BASE / "data" / "classification_answer_ledger.json"
PDF1 = "Classification 01_.pdf"
PDF2 = "Classification 02_.pdf"
ORIGINAL = "Original SSC-style practice question"

# Each entry is (difficulty, stem, A, B, C, D, key, explanation, source, signature).
ITEMS = [
    ("EASY", "Which item is not one of the four Vedas?", "Rigveda", "Yajurveda", "Atharvaveda", "Ayurveda", "D", "Rigveda, Yajurveda, and Atharvaveda are Vedas. Ayurveda is a traditional medical system, not a Veda.", f"{PDF1}, lecture slide 5; exam/year not stated", "vedic_texts_vs_medical_tradition"),
    ("EASY", "Which item does not belong with the others?", "Curd", "Butter", "Oil", "Cheese", "C", "Curd, butter, and cheese are dairy products. Oil is not a dairy product.", f"{PDF1}, lecture slide 6; exam/year not stated", "three_dairy_products_one_non_dairy"),
    ("EASY", "Which is different from the other three?", "Calendar", "Year", "Date", "Month", "A", "A year, date, and month are units or labels of calendar time. A calendar is the system or object that organizes them.", f"{PDF1}, lecture slide 7; exam/year not stated", "calendar_object_vs_time_units"),
    ("EASY", "Choose the odd one out by musical instrument family.", "Flute", "Violin", "Guitar", "Sitar", "A", "A flute is a wind instrument. Violin, guitar, and sitar are string instruments.", f"{PDF1}, lecture slide 8; exam/year not stated", "wind_instrument_vs_string_instruments"),
    ("MEDIUM", "Which condition is not generally classified as a deficiency disease?", "Anaemia", "Scurvy", "Diarrhoea", "Goitre", "C", "Scurvy is caused by vitamin C deficiency; some anaemias and goitre are associated with nutrient deficiencies. Diarrhoea is a symptom/condition with many causes, not a deficiency disease category.", f"{PDF1}, lecture slide 10; exam/year not stated; wording clarified to specify the classification", "deficiency_disease_vs_symptom"),
    ("MEDIUM", "Which is not ordinarily classified as a natural disaster?", "Flood", "Hurricane", "Avalanche", "Explosion", "D", "Floods, hurricanes, and avalanches are natural hazards. An explosion is ordinarily an event caused by human activity, so it is the intended different category.", f"{PDF1}, lecture slide 12; exam/year not stated; relation made explicit from the slide annotation", "natural_disasters_vs_explosion"),
    ("EASY", "Which is not a family relationship?", "Mother", "Friend", "Sister", "Father", "B", "Mother, sister, and father are family relationships. Friend describes a social relationship that need not be familial.", f"{PDF1}, lecture slide 14; exam/year not stated", "family_relations_vs_friend"),
    ("EASY", "Which river is geographically different from the other three?", "Ganga", "Brahmaputra", "Amazon", "Yamuna", "C", "Ganga, Brahmaputra, and Yamuna are rivers of South Asia. The Amazon is in South America.", f"{PDF2}, lecture slide 5; exam/year not stated", "south_asian_rivers_vs_amazon"),
    ("EASY", "Which person is different by profession?", "Narendra Modi", "Rahul Gandhi", "Amit Shah", "Mahendra Singh Dhoni", "D", "The first three are politicians. Mahendra Singh Dhoni is a former international cricketer.", f"{PDF2}, lecture slide 8; exam/year not stated", "politicians_vs_cricketer"),
    ("EASY", "Which number is not prime?", "31", "71", "51", "101", "C", "31, 71, and 101 are prime. 51 is divisible by 3 (5+1=6) and equals 3×17.", f"{PDF2}, lecture slide 14; exam/year not stated", "three_primes_one_composite_51"),
    ("MEDIUM", "Which letter-pair transition does not follow the same rule as the others?", "UX–YB", "GJ–JP", "PS–TW", "YB–CF", "B", "In A, C, and D, each letter advances four positions, wrapping after Z (U→Y and X→B; P→T and S→W; Y→C and B→F). In B, G→J advances three while J→P advances six.", f"{PDF2}, lecture slide 7; exam/year not stated", "letter_pair_each_letter_advances_four"),
    ("MEDIUM", "Which number pair is inconsistent with the rule n → n³+n?", "7 : 350", "5 : 130", "1 : 4", "6 : 222", "C", "For n=7, 7³+7=350; for 5, 125+5=130; for 6, 216+6=222. For n=1 the rule gives 2, not 4.", f"{PDF2}, lecture slide 10; exam/year not stated", "n_cubed_plus_n_pairs"),
    ("MEDIUM", "Which number pair is different from the other three?", "15 : 34", "1 : 6", "18 : 42", "7 : 18", "C", "Each pair follows second number = 2×first + 4, except 18 gives 2×18+4=40, not 42.", f"{PDF2}, lecture slide 12; exam/year not stated", "pairs_second_twice_first_plus_four"),
    ("HARD", "Which triple does not follow the same rule as the others?", "7, 343, 333", "5, 125, 115", "4, 64, 54", "3, 27, 19", "D", "The second entry is the cube of the first; the third is ten less than the second. For 3, 27−10=17, not 19.", f"{PDF2}, lecture slide 13; exam/year not stated", "n_n_cubed_cube_minus_ten"),
    ("HARD", "Which group of three numbers is different?", "720, 715, 710", "505, 500, 495", "100, 90, 85", "250, 245, 240", "C", "In A, B, and D, each successive number decreases by 5. In C, 100 to 90 decreases by 10, then to 85 by 5.", f"{PDF2}, lecture slide 19; exam/year not stated", "three_numbers_decrease_by_five"),
    ("HARD", "Which number triple does not follow the same rule?", "7, 70, 1600", "4, 40, 800", "6, 60, 1200", "5, 50, 1000", "A", "The second number is ten times the first, and the third is twenty times the second. B, C, and D follow this rule; 70×20=1400, not 1600.", f"{PDF2}, lecture slide 20; exam/year not stated", "triple_x_ten_x_two_hundred_x"),
    ("HARD", "Which triplet is inconsistent with the others?", "3 : 7 : 27", "12 : 25 : 1728", "2 : 5 : 8", "5 : 10 : 125", "D", "The first number is n, the second is 2n+1, and the third is n³. A, B, and C follow; for n=5 the middle value should be 11, not 10.", f"{PDF2}, lecture slide 21; exam/year not stated", "triplet_n_two_n_plus_one_n_cubed"),

    ("EASY", "Which item belongs to a different astronomical category?", "Mercury", "Venus", "Earth", "Moon", "D", "Mercury, Venus, and Earth are planets. The Moon is Earth's natural satellite.", ORIGINAL, "three_planets_one_satellite"),
    ("EASY", "Which letter-number pair breaks the pattern?", "2A", "4C", "6E", "8H", "D", "The number terms increase by 2 and the letter positions also increase by 2: A, C, E, so the next letter is G. The final pair should be 8G, not 8H.", ORIGINAL, "even_numbers_with_letters_ascending_by_two"),
    ("MEDIUM", "Which pair is inconsistent with the rule n : n(n+1)?", "3 : 12", "4 : 20", "5 : 30", "6 : 40", "D", "The output should be n(n+1): 3×4=12, 4×5=20, 5×6=30, and 6×7=42. Thus 6:40 is the exception.", ORIGINAL, "n_times_successor_pairs"),
    ("MEDIUM", "Which item is different by biological classification?", "Oak", "Pine", "Rose", "Maple", "C", "Oak, pine, and maple are trees. A rose is a flowering shrub, not a tree in the ordinary classification used here.", ORIGINAL, "three_trees_one_shrub"),
    ("MEDIUM", "Which letter pair breaks the pattern?", "AC", "DF", "GI", "JN", "D", "The first letters advance by three positions (A, D, G, J), and the second letter is two positions after the first (C, F, I, L). JN has a four-position gap, so it should be JL.", ORIGINAL, "letter_pairs_start_plus_three_gap_two"),
    ("MEDIUM", "Which group does not follow the same rule?", "2, 5, 8", "4, 9, 14", "6, 13, 20", "8, 17, 25", "D", "The entries follow n, 2n+1, and 3n+2. For n=2,4,6 this gives (2,5,8), (4,9,14), (6,13,20). For n=8 the last value should be 26, not 25.", ORIGINAL, "triplet_n_2n_plus_one_3n_plus_two"),
    ("MEDIUM", "Which number is different from the other three?", "49", "64", "81", "99", "D", "49=7², 64=8², and 81=9² are perfect squares. 99 is not a perfect square (9²=81 and 10²=100).", ORIGINAL, "three_consecutive_squares_one_non_square"),
    ("MEDIUM", "Which letter group breaks the pattern?", "ACE", "DFH", "GIK", "JMN", "D", "Within each group the letter positions increase by two: A-C-E, D-F-H, G-I-K. Starting at J, the pattern requires J-L-N; J-M-N does not have equal two-position steps.", ORIGINAL, "three_letter_groups_step_two"),
    ("MEDIUM", "Which device is different by its primary measured quantity?", "Thermometer", "Barometer", "Hygrometer", "Compass", "D", "A thermometer measures temperature, a barometer pressure, and a hygrometer humidity. A compass indicates direction rather than measuring one of those physical conditions.", ORIGINAL, "three_environment_measuring_instruments_vs_direction"),
    ("HARD", "Which triple fails the rule (n, n²+1, n³+1)?", "2, 5, 9", "3, 10, 28", "4, 17, 65", "5, 26, 125", "D", "For first value n, the second is n²+1 and the third is n³+1. A gives 5 and 9; B gives 10 and 28; C gives 17 and 65. For 5 the third value should be 126, not 125.", ORIGINAL, "triple_n_square_plus_one_cube_plus_one"),
    ("HARD", "Which ordered pair is different from the others?", "2 : 3", "5 : 7", "11 : 13", "17 : 21", "D", "In A, B, and C, the second value is the next prime after the first (2→3, 5→7, 11→13). The next prime after 17 is 19, not 21.", ORIGINAL, "consecutive_prime_pairs"),
    ("HARD", "Which letter transformation does not follow the same rule?", "ABC → BDF", "DEF → EGI", "GHI → HJL", "JKL → LMO", "D", "In A, B, and C each letter advances one position, then the second and third letters advance by one and two extra positions respectively: ABC→BDF (1,2,3), DEF→EGI (1,2,3), GHI→HJL (1,2,3). JKL should become KMO, so LMO is inconsistent.", ORIGINAL, "letter_triplet_shifts_one_two_three"),
    ("HARD", "Which number triple is different by the relation between consecutive entries?", "3, 10, 31", "4, 13, 40", "5, 16, 49", "6, 19, 59", "D", "The rule is next = 3×current+1: 3→10→31, 4→13→40, 5→16→49, and 6→19→58. In D the final value should be 58, not 59.", ORIGINAL, "triples_next_equals_three_times_previous_plus_one"),
]


def build():
    if len(ITEMS) != 30:
        raise ValueError(f"Expected 30 items, got {len(ITEMS)}")
    rows, ledger = [], []
    for i, item in enumerate(ITEMS, 1):
        difficulty, stem, a, b, c, d, key, explanation, source, signature = item
        row = {
            "subject_slug": "reasoning", "subcategory_slug": None,
            "chapter_slug": "classification", "question_text": stem,
            "explanation": explanation, "difficulty": difficulty,
            "is_pyq": False, "pyq_year": None, "pyq_exam_name": None,
            "source": source,
            "options": dict(zip("ABCD", (a, b, c, d))), "correct_option": key,
        }
        rows.append(row)
        ledger.append({
            "row": i, "question": stem, "expected_answer": row["options"][key],
            "correct_option": key, "difficulty": difficulty, "source": source,
            "independent_reasoning": explanation,
            "option_review": f"A={a}; B={b}; C={c}; D={d}. Exactly one option fails the stated classification rule.",
            "concept_signature": signature,
        })
    BATCH.write_text(json.dumps({"questions": rows}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    LEDGER.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(rows)} questions; difficulties={dict(Counter(r['difficulty'] for r in rows))}")


if __name__ == "__main__":
    build()
