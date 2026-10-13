"""Write the authored, original Ratio & Proportion Medium batch."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "data" / "ratio_proportion_medium_batch.json"

# Each item is difficulty, stem, answer, three distractors, explanation.
ROWS = [
    ("MEDIUM", "A:B=3:5 and B:C=10:7. If A+B+C=₹920, how much is B?", "₹400", ["₹280", "₹360", "₹420"], "Equalize B to 10: A:B:C=6:10:7, or 23 parts. Each part is ₹40, so B=₹400."),
    ("MEDIUM", "A 1,080 m cable is cut into two sections in the ratio 2:7. The shorter section is then cut in the ratio 3:5. What is the length of the shortest final piece?", "90 m", ["60 m", "80 m", "120 m"], "The shorter section is 2/9×1,080=240 m. Its shorter piece is 3/8×240=90 m."),
    ("MEDIUM", "A and B hold amounts in the ratio 2:7. If ₹80 is transferred from B to A, their ratio becomes 4:5. What was their original total?", "₹360", ["₹320", "₹400", "₹440"], "Let the amounts be 2k and 7k. 5(2k+80)=4(7k−80) gives k=40, so their original total was 9k=₹360."),
    ("MEDIUM", "A prize of ₹2,400 is divided between P and Q in the ratio 3:5. P gives 20% of her share to Q. What is their final ratio P:Q?", "3:7", ["2:5", "3:5", "5:7"], "Initial shares are ₹900 and ₹1,500. P transfers ₹180, leaving ₹720 and ₹1,680; 720:1,680 simplifies to 3:7."),
    ("MEDIUM", "P:Q=4:7. P's quantity rises by 25% while Q's falls by 20%. What is the new ratio P:Q?", "25:28", ["4:7", "5:7", "5:8"], "The changed quantities are 4×1.25=5 parts and 7×0.8=5.6 parts. 5:5.6=25:28."),
    ("MEDIUM", "The number of boys and girls is in the ratio 5:4. After 8 boys leave, the ratio is 3:4. How many students were there initially?", "36", ["32", "40", "44"], "Let the original counts be 5k and 4k. (5k−8)/(4k)=3/4 gives k=4; total=9k=36."),
    ("MEDIUM", "A parent's and child's present ages are in the ratio 5:3. In 8 years, their ages will be in the ratio 7:5. What is their present combined age?", "32 years", ["24 years", "28 years", "40 years"], "Let present ages be 5k and 3k. 5(5k+8)=7(3k+8) gives k=4; total=8k=32 years."),
    ("MEDIUM", "A father is three times his son's age. Five years ago, the father was four times his son's age. How old is the father now?", "45 years", ["30 years", "40 years", "50 years"], "Let the son's age be x and the father's age be 3x. 3x−5=4(x−5) gives x=15, so the father is 45."),
    ("MEDIUM", "A 3:2 milk-water mixture has 12 litres of water added, making the ratio 3:4. What was the original mixture volume?", "30 L", ["24 L", "36 L", "42 L"], "Let initial amounts be 3k and 2k. 3k/(2k+12)=3/4 gives k=6; original volume=5k=30 L."),
    ("MEDIUM", "A 40 L mixture contains milk and water in the ratio 3:1. Ten litres of mixture are removed and replaced with water. What is the final milk:water ratio?", "9:7", ["3:2", "7:5", "5:4"], "Initially milk=30 L, water=10 L. Removing 10 L removes 7.5 L milk and 2.5 L water; after adding water, amounts are 22.5 L and 17.5 L, or 9:7."),
    ("MEDIUM", "A and B have total monthly incomes of ₹60,000 in the ratio 7:5. Their total monthly expenditure is ₹35,000 in the ratio 4:3. What is their savings ratio A:B?", "3:2", ["2:3", "5:4", "7:5"], "Incomes are ₹35,000 and ₹25,000. Expenditures are ₹20,000 and ₹15,000. Savings are ₹15,000 and ₹10,000, so 3:2."),
    ("MEDIUM", "A:B incomes are in the ratio 4:5. A saves 25% of income and B saves 40%. What is the ratio of their savings?", "1:2", ["4:5", "5:8", "2:5"], "For proportional incomes 4 and 5, savings are 25%×4=1 and 40%×5=2 units."),
    ("MEDIUM", "Three-fifths of A's amount equals two-sevenths of B's amount. Find A:B.", "10:21", ["21:10", "15:14", "6:7"], "3A/5=2B/7 gives 21A=10B, hence A:B=10:21."),
    ("MEDIUM", "Two numbers are in the ratio 4:7. Adding 6 to the smaller and subtracting 3 from the larger makes their ratio 2:3. Find the original larger number.", "84", ["72", "78", "96"], "For 4k and 7k, 3(4k+6)=2(7k−3), so k=12. The larger number is 84."),
    ("MEDIUM", "A:B=5:8. If 12 is added to A and 8 is subtracted from B, the new ratio is 3:4. Find A+B originally.", "234", ["208", "216", "260"], "4(5k+12)=3(8k−8), so k=18. The original sum is 13k=234."),
    ("MEDIUM", "If 3x:5y=9:20 and x+y=49, find x.", "21", ["14", "28", "35"], "3x/(5y)=9/20 gives 60x=45y, so x:y=3:4. Seven parts total 49; x=21."),
    ("MEDIUM", "Three amounts are in the ratio 2:3:5. The largest exceeds the smallest by ₹540. What is the middle amount?", "₹540", ["₹360", "₹450", "₹630"], "The difference is 3 parts=₹540, so one part is ₹180. The middle amount is 3 parts=₹540."),
    ("MEDIUM", "The sides of a triangle are in the ratio 4:5:6. If its perimeter is 180 cm, what is the length of the longest side?", "72 cm", ["60 cm", "66 cm", "78 cm"], "The 15 parts total 180 cm, so one part is 12 cm. The longest side is 6×12=72 cm."),
    ("MEDIUM", "A recipe uses rice and lentils in the ratio 5:2. A cook has 1.2 kg of rice and wants to keep the same ratio. How many grams of lentils are needed?", "480 g", ["400 g", "500 g", "600 g"], "The rice amount is 5 parts, so one part is 1.2/5=0.24 kg. Two parts of lentils are 0.48 kg=480 g."),
    ("MEDIUM", "A map scale is 1:50,000. A road measures 6 cm on the map. If 1 cm is mistakenly measured as 1.2 cm during copying, what length will that road appear to have on the copy?", "7.2 cm", ["5 cm", "6.5 cm", "8 cm"], "The copy enlarges every map length by a factor of 1.2. Thus 6×1.2=7.2 cm."),
    ("MEDIUM", "A and B divide an amount in the ratio 3:5. If A receives ₹240 less than B, what is the total amount?", "₹960", ["₹720", "₹840", "₹1,200"], "The difference is 2 parts=₹240, so one part is ₹120. The total is 8×₹120=₹960."),
    ("MEDIUM", "The present ages of two siblings are in the ratio 4:3. After 6 years their ages will total 54 years. How old is the older sibling now?", "24 years", ["18 years", "21 years", "30 years"], "Their present total is 54−12=42 years, or 7 parts. One part is 6, so the older sibling is 4×6=24."),
    ("MEDIUM", "A container has 54 L of juice and water in the ratio 7:2. How much water must be added to make the ratio 7:5?", "18 L", ["12 L", "21 L", "27 L"], "Each of 9 parts is 6 L, so there are 42 L juice and 12 L water. For 7:5, water must be 30 L; add 18 L."),
    ("MEDIUM", "A sum is divided between X and Y in the ratio 7:9. If X's share is increased by ₹120 and Y's share is reduced by ₹120, the shares become equal. What is the original total?", "₹1,920", ["₹1,600", "₹1,760", "₹2,080"], "The original difference is 240, equal to 2 parts; one part is 120. The total is 16×120=₹1,920."),
    ("MEDIUM", "The ratio of two numbers is 9:13. If their difference is 52, what is their average?", "143", ["117", "130", "156"], "Four parts equal 52, so one part is 13. The numbers are 117 and 169; their average is 143."),
    ("MEDIUM", "A worker's pay for 5 days is in the ratio 3:4 to another worker's pay for 6 days. If the first earns ₹900 per day, what does the second earn per day?", "₹1,000", ["₹750", "₹900", "₹1,200"], "The first five-day pay is ₹4,500, or 3 parts. The second six-day pay is 4 parts=₹6,000, so the second earns ₹1,000 per day."),
    ("MEDIUM", "Three quantities are in the ratio 7:9:12. The first two together equal 128. How much greater is the third quantity than the first?", "40", ["24", "32", "48"], "The first two are 16 parts, so one part is 128/16=8. The third exceeds the first by 5 parts, or 40."),
    ("MEDIUM", "If a:b=3:4 and b:c=6:7, and a+b+c=350, find c.", "140", ["100", "120", "160"], "Make b=12: a:b:c=9:12:14. The 35 parts total 350, so one part is 10 and c=140."),
    ("MEDIUM", "R and S make monthly deposits in the ratio 3:4. In one month, R deposits ₹250 extra, making that month's amounts 4:5. What is S's regular deposit?", "₹5,000", ["₹3,750", "₹4,500", "₹5,500"], "Let regular deposits be 3k and 4k. (3k+250)/(4k)=4/5 gives 15k+1,250=16k, so k=1,250 and S deposits ₹5,000."),
    ("MEDIUM", "The ratio of two positive quantities is 2:3. Their product is 864. What is their sum?", "60", ["48", "66", "72"], "Let the quantities be 2k and 3k. 6k²=864, so k²=144 and k=12; their sum is 5×12=60."),
]


def build():
    assert len(ROWS) == 30, len(ROWS)
    questions = []
    for index, (difficulty, stem, answer, distractors, explanation) in enumerate(ROWS):
        options = [answer, *distractors]
        assert len(set(options)) == 4, (index + 1, options)
        shift = (index * 3 + 1) % 4
        options = options[shift:] + options[:shift]
        questions.append({
            "subject_slug": "maths", "subcategory_slug": "arithmetic-maths",
            "chapter_slug": "ratio-and-proportion", "question_text": stem,
            "options": dict(zip("ABCD", options)),
            "correct_option": "ABCD"[options.index(answer)],
            "explanation": explanation, "difficulty": difficulty,
            "is_pyq": False, "source": "Original SSC-style practice question",
        })
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps({"questions": questions}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    build()
