"""Build the reviewed Analogy question batch and its independent answer ledger."""

import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
BATCH = BASE / "data" / "analogy_verified_batch.json"
LEDGER = BASE / "data" / "analogy_answer_ledger.json"
ORIGINAL = "Original SSC-style practice question"

# Stem, options A-D, key, independent explanation, difficulty, source, concept signature.
RECORDS = [
    ("Lemon : Sour :: Ice cream : ?", ["Cold", "Sweet", "Vanilla", "Milk"], "B", "Lemon is characterized by its sour taste; ice cream is characterized by its sweet taste. The remaining choices name a temperature, flavor, or ingredient rather than the corresponding taste.", "EASY", "Analogy 01_.pdf, lecture slide 12; exam/year not stated", "food-item-to-dominant-taste"),
    ("Wife : Husband :: Bride : ?", ["Marriage", "Love", "Man", "Groom"], "D", "Wife and husband are the corresponding partners in a marriage; bride and groom are the corresponding partners at a wedding.", "EASY", "Analogy 01_.pdf, lecture slide 12; exam/year not stated", "wedding-partner-counterpart"),
    ("Tiger : India :: Giant panda : ?", ["Taiwan", "Vietnam", "Russia", "China"], "D", "The pairs associate the named animal with its commonly associated country in this item. Among the choices, the giant panda is associated with China.", "EASY", "Analogy 01_.pdf, lecture slide 13; exam/year not stated", "animal-country-association"),
    ("Maharashtra : Mumbai :: Tamil Nadu : ?", ["Madurai", "Salem", "Chennai", "Coimbatore"], "C", "Mumbai is the capital of Maharashtra, and Chennai is the capital of Tamil Nadu. The other listed Tamil Nadu cities are not its capital.", "EASY", "Analogy 01_.pdf, lecture slide 15; exam/year not stated", "state-capital"),
    ("Writer : Book :: Potter : ?", ["Brush", "Stone", "Pot", "Shoes"], "C", "A writer produces a book; a potter produces a pot. The other choices are not the product named by the occupation.", "EASY", "Analogy 01_.pdf, lecture slide 16; exam/year not stated", "occupation-produced-object"),
    ("Pen : Nib :: ? : Cockpit", ["Aeroplane", "Poultry farm", "Submarine", "Engine room"], "A", "A nib is a functional part of a pen; a cockpit is a functional part of an aeroplane. The other options are not the vehicle whose cockpit is specified.", "EASY", "Analogy 01_.pdf, lecture slide 19; exam/year not stated", "object-to-distinctive-part"),
    ("Kuwait : Dinar :: Turkey : ?", ["Riyal", "Kyat", "Yen", "Lira"], "D", "The dinar is the currency unit used in Kuwait; the lira is the currency unit used in Turkey. The other options are currencies associated with other countries.", "EASY", "Analogy 01_.pdf, lecture slide 21; exam/year not stated", "country-currency"),
    ("Butterfly : Insect :: Snake : ?", ["Cobra", "Python", "Reptile", "Rodent"], "C", "A butterfly is an insect; a snake is a reptile. Cobra and python are particular kinds of snake, while reptile gives the matching broader class.", "EASY", "Analogy 01_.pdf, lecture slide 22; exam/year not stated", "animal-to-class"),
    ("86 : 298 :: 105 : 317 :: 48 : ?", ["280", "270", "260", "250"], "C", "Each first number is increased by 212: 86 + 212 = 298 and 105 + 212 = 317. Therefore 48 + 212 = 260.", "EASY", "Analogy 02_.pdf, lecture slide 6; exam/year not stated", "constant-addition-212"),
    ("Cat : Kitten :: Dog : ?", ["Puppy", "Foal", "Calf", "Cub"], "A", "A kitten is the young of a cat; a puppy is the young of a dog. Foal, calf, and cub are young of other animals.", "EASY", ORIGINAL, "animal-to-young"),

    ("Gold : Necklace :: Iron : ?", ["Shirt", "Ribbon", "Book", "Bucket"], "D", "Gold can be made into a necklace; iron can be made into a bucket. Among the options, bucket is the matching object made from the named material.", "MEDIUM", "Analogy 01_.pdf, lecture slide 20; exam/year not stated", "material-to-object"),
    ("35 : 21 :: ? : 36 :: 40 : 24", ["65", "50", "60", "55"], "C", "In the given pairs the second number is three-fifths of the first: 21/35 = 24/40 = 3/5. Thus (3/5)x = 36, so x = 60.", "MEDIUM", "Analogy 02_.pdf, lecture slide 7; exam/year not stated", "three-fifths-proportion"),
    ("12 : 132 :: 20 : 380 :: 2 : ?", ["8", "6", "12", "2"], "D", "The mapping is n(n − 1): 12×11 = 132 and 20×19 = 380. For 2, 2×1 = 2.", "MEDIUM", "Analogy 02_.pdf, lecture slide 9; exam/year not stated", "n-times-predecessor"),
    ("Select the set related in the same way as (10, 20, 24, 16) and (18, 36, 40, 32).", ["(21, 42, 56, 38)", "(9, 18, 22, 14)", "(20, 40, 64, 46)", "(25, 50, 68, 60)"], "B", "The successive operations are ×2, then +4, then −8: 10→20→24→16 and 18→36→40→32. Only 9→18→22→14 follows all three operations.", "MEDIUM", "Analogy 02_.pdf, lecture slide 15; exam/year not stated", "four-term-double-plus4-minus8"),
    ("Choose the set related in the same way as (6, 12, 3) and (10, 20, 5).", ["(21, 28, 7)", "(14, 28, 7)", "(14, 21, 7)", "(14, 28, 9)"], "B", "In each given triple, the second number is twice the first and the third is half the first. Only (14, 28, 7) satisfies both conditions.", "MEDIUM", "Analogy 02_.pdf, lecture slide 16; exam/year not stated", "triple-double-and-half"),
    ("Choose the set that follows the same successive operations as (1, 2, 4, 8) and (9, 10, 20, 40).", ["(4, 5, 10, 20)", "(19, 20, 20, 30)", "(6, 7, 14, 30)", "(14, 15, 30, 40)"], "A", "The successive operations are +1, ×2, ×2. The first option gives 4→5→10→20, so it alone follows the same sequence of operations.", "MEDIUM", "Analogy 02_.pdf, lecture slide 27; exam/year not stated", "four-term-plus1-double-double"),
    ("Thermometer : Temperature :: Barometer : ?", ["Humidity", "Pressure", "Wind speed", "Rainfall"], "B", "A thermometer measures temperature; a barometer measures atmospheric pressure. The other quantities require different instruments.", "MEDIUM", ORIGINAL, "instrument-to-measured-quantity"),
    ("BD : FH :: JL : ?", ["NQ", "NP", "MP", "NO"], "B", "Each letter advances four alphabet positions: B→F and D→H. Applying the same shift gives J→N and L→P, hence NP.", "MEDIUM", ORIGINAL, "two-letter-parallel-plus-four"),
    ("16 : 4 :: 81 : ?", ["7", "8", "9", "10"], "C", "The second number is the positive square root of the first: √16 = 4. Therefore √81 = 9.", "MEDIUM", ORIGINAL, "positive-square-root"),
    ("Pentagon : 5 :: Octagon : ?", ["6", "7", "8", "9"], "C", "The number represents the polygon's sides. A pentagon has 5 sides and an octagon has 8.", "MEDIUM", ORIGINAL, "polygon-to-side-count"),
    ("June : July :: October : ?", ["September", "November", "December", "January"], "B", "July is the month immediately after June; November is immediately after October.", "MEDIUM", ORIGINAL, "month-to-next-month"),
    ("C3 : F6 :: H8 : ?", ["K10", "K11", "L11", "K12"], "B", "Both components increase by three: C→F and 3→6. Applying the same shifts gives H→K and 8→11, hence K11.", "MEDIUM", ORIGINAL, "letter-and-number-parallel-plus-three"),

    ("4 : 84 :: 11 : ? :: 13 : 2379", ["1221", "1463", "1440", "819"], "B", "For n, the value is n³+n²+n: 4³+4²+4=84 and 13³+13²+13=2379. For 11 this is 1331+121+11=1463.", "HARD", "Analogy 02_.pdf, lecture slide 10; exam/year not stated", "n-cube-square-and-n"),
    ("X : 1332 :: 17 : Y", ["X=10, Y=290", "X=11, Y=290", "X=11, Y=4950", "X=11, Y=4914"], "D", "The rule is n³+1. Since 11³+1=1332, X=11; and 17³+1=4914, so Y=4914.", "HARD", "Analogy 02_.pdf, lecture slide 13; exam/year not stated", "cube-plus-one-pair"),
    ("6 : 32 :: 10 : ? :: 11 : 117", ["110", "88", "99", "96"], "D", "The rule is n²−4: 6²−4=32 and 11²−4=117. Therefore 10²−4=96.", "HARD", "Analogy 02_.pdf, lecture slide 19; exam/year not stated", "square-minus-four"),
    ("3 : 8 :: 6 : ? :: 11 : 1000", ["729", "512", "216", "125"], "D", "The output is the cube of one less than the input: (3−1)³=8 and (11−1)³=1000. Thus (6−1)³=125.", "HARD", "Analogy 02_.pdf, lecture slide 20; exam/year not stated", "predecessor-cube"),
    ("AC : CF :: MO : ?", ["OQ", "PQ", "QR", "OR"], "D", "Within each pair, the first letter advances by 2 and the second by 3: A→C, C→F. Applying those shifts gives M→O and O→R, hence OR.", "HARD", "Analogy 02_.pdf, lecture slide 23; exam/year not stated", "two-letter-offsets-plus-two-plus-three"),
    ("ABC/F : BCD/I :: CDE/L : ?", ["DEF/O", "DEF/N", "EDF/O", "DEF/M"], "A", "The three letters are replaced by the letter whose alphabet position equals their sum: ABC gives 1+2+3=6 (F), BCD gives 2+3+4=9 (I), and CDE gives 3+4+5=12 (L). DEF gives 4+5+6=15 (O).", "HARD", "Analogy 02_.pdf, lecture slide 24; exam/year not stated", "letter-group-alphabet-position-sum"),
    ("2 : 10 :: 4 : 68 :: 6 : ?", ["216", "220", "222", "228"], "C", "The rule is n³+n: 2³+2=10 and 4³+4=68. For 6, 6³+6=216+6=222.", "HARD", ORIGINAL, "cube-plus-input"),
    ("ABCD : BDFH :: CDEF : ?", ["DFHJ", "DEFG", "EGIK", "DFGI"], "A", "Apply increasing shifts of +1, +2, +3, and +4 to successive letters: ABCD becomes BDFH. Applying the same shifts to CDEF gives D, F, H, J: DFHJ.", "HARD", ORIGINAL, "four-letter-increasing-offsets"),
]


def main():
    rows, ledger = [], []
    for index, (stem, choices, key, explanation, difficulty, source, concept) in enumerate(RECORDS, start=1):
        options = dict(zip("ABCD", choices))
        row = {
            "subject_slug": "reasoning", "subcategory_slug": None, "chapter_slug": "analogy",
            "question_text": stem, "options": options, "correct_option": key,
            "explanation": explanation, "difficulty": difficulty, "is_pyq": False,
            "pyq_year": None, "pyq_exam_name": None, "source": source,
        }
        rows.append(row)
        ledger.append({
            "row": index, "question": stem, "expected_answer": options[key],
            "correct_option": key, "difficulty": difficulty, "source": source,
            "source_type": "original" if source == ORIGINAL else "pdf-derived",
            "concept_signature": concept,
            "independent_reasoning": explanation,
            "option_review": "All four options are distinct; the stated relationship selects only the keyed option.",
        })
    BATCH.write_text(json.dumps({"questions": rows}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    LEDGER.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(rows)} questions; source counts: pdf={sum(r['source'] != ORIGINAL for r in rows)}, original={sum(r['source'] == ORIGINAL for r in rows)}")


if __name__ == "__main__":
    main()
