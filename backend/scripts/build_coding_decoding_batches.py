"""Build the reviewed Coding-Decoding batches and independent answer ledgers."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PREFIX = "Coding Decoding"
ORIGINAL = "Original SSC-style practice question"

# Question, answer, concise independent proof, PDF number/page, difficulty,
# and three distractors. Ambiguous scan questions are intentionally omitted.
SCANNED = [
    ("In any code language, INDIA is written as 914491. How will POLICE be written in that language?", "161512935", "Replace each letter by its A1Z26 position and concatenate: P=16, O=15, L=12, I=9, C=3, E=5.", 1, 10, "MEDIUM", ["161512935", "15654835", "161545545", "16171717"]),
    ("If MANGO is written as 50 in a code language, how is GOA written in that language?", "23", "The code is the sum of alphabet positions: G+O+A=7+15+1=23.", 2, 7, "EASY", ["23", "33", "32", "27"]),
    ("If PILOT is written as 144 in a symbolic language, how will TRAIN be written in the same language?", "124", "The code is twice the sum of alphabet positions. TRAIN gives 2×(20+18+1+9+14)=124.", 2, 8, "EASY", ["133", "124", "132", "125"]),
    ("If MACHINE is coded as 19-7-9-14-15-20-11, how will DANGER be coded?", "10-7-20-13-11-24", "Each alphabet position is increased by 6: DANGER positions 4,1,14,7,5,18 become 10,7,20,13,11,24.", 2, 9, "MEDIUM", ["10-7-20-13-11-24", "11-7-16-20-11-24", "13-7-20-9-11-25", "13-7-20-10-11-25"]),
    ("In a certain code language, MORE is coded as 14-12-9-22 and KNOW as 16-13-12-4. How will SAID be coded?", "8-26-18-23", "Each letter is replaced by its reverse alphabet position (27 minus its A1Z26 position). SAID maps to 8-26-18-23.", 2, 10, "MEDIUM", ["7-26-18-22", "8-26-18-23", "8-26-17-23", "7-25-18-23"]),
    ("If GO is written as 32 in a code language, how is COME written in that language?", "72", "Add reverse alphabet positions: C=24, O=12, M=14, E=22; total 72. GO gives 20+12=32.", 2, 11, "MEDIUM", ["72", "88", "89", "76"]),
    ("If DISPUR is written as DISRUP in a certain code, how will SHIMLA be written in that code?", "SHIALM", "The 4th and 6th letters are interchanged. SHIMLA becomes SHIALM.", 2, 14, "EASY", ["SHIALM", "SHKBLM", "MAORUP", "KLMOST"]),
    ("If COLOUR is coded as DNMNVP, how will DEMAND be coded?", "EDNZOB", "The position shifts are +1,−1,+1,−1,+1,−2. Applying them to DEMAND yields EDNZOB.", 2, 15, "HARD", ["EDNBMB", "EDNZOC", "EDNZOB", "EDLBMC"]),
    ("In a certain code, NAIL is written as 2637 and LANE as 3278. How is E written in that code?", "8", "N, A and L are common to both words; their digits are 2, 3 and 7. The remaining digit in LANE is 8, so E=8.", 2, 19, "MEDIUM", ["2", "3", "8", "7"]),
    ("In a certain code, DRAW is written as 7932 and WEAR as 4729. How is E written in that code?", "4", "The words share W, A and R, and the codes share 7, 9 and 2. The remaining digit 4 represents E.", 2, 20, "MEDIUM", ["7", "4", "9", "2"]),
    ("In a certain code language, NEAR is written as 4968 and REAP as 9865. How will P be written in that code language?", "5", "R, E and A are shared; their codes are the three digits common to 4968 and 9865 (9, 8, 6). The remaining digit for P is 5.", 2, 21, "MEDIUM", ["6", "8", "9", "5"]),
    ("In a code language, 'She will come' is 'vu de ja', 'Come and eat' is 'te vu ma', and 'all will eat' is 'ma nu ja'. What is the code for 'all'?", "nu", "'Will' and 'eat' are shared by the first/third and second/third statements, giving ja and ma; the remaining code in the third statement, nu, is 'all'.", 2, 23, "HARD", ["nu", "ja", "ma", "te"]),
    ("In a code language, 639 means 'water is drink', 316 means 'juice is drink', and 219 means 'water or juice'. What is the code for 'or'?", "2", "Digits 3 and 6 are the shared codes for 'is' and 'drink'. In the third statement, 9 is water and 1 is juice, leaving 2 for 'or'.", 2, 24, "HARD", ["1", "2", "9", "3"]),
    ("If 'light' is called 'morning', 'morning' is called 'dark', 'dark' is called 'night', 'night' is called 'sunshine', and 'sunshine' is called 'dusk', when do we sleep?", "Sunshine", "We sleep at night; the code calls night 'sunshine'.", 3, 6, "EASY", ["Night", "Light", "Dusk", "Sunshine"]),
    ("If a train is called a bus, a bus is called a tractor, a tractor is called a car, a car is called a scooter, a scooter is called a cycle, and a cycle is called a moped, which is used to plough a field?", "Car", "A tractor is used to plough a field. In the substitution, a tractor is called a car.", 3, 7, "EASY", ["Train", "Bus", "Tractor", "Car"]),
    ("If air is called green, green is called blue, blue is called sky, sky is called yellow, yellow is called water, and water is called pink, what is the colour of the sky?", "Sky", "The real colour is blue; blue is called sky.", 3, 8, "EASY", ["Blue", "Sky", "Yellow", "Water"]),
    ("If honey is called chocolate, chocolate is called sugar, sugar is called joy, and joy is called freedom, which is made from cocoa beans?", "Sugar", "Cocoa beans make chocolate; chocolate is called sugar in this code.", 3, 9, "EASY", ["Chocolate", "Sugar", "Honey", "Joy"]),
    ("In a coding language TEAR is called 7%9# and PERY is called &%#8. How is ARTERY called?", "9#7%#8", "TEAR gives T=7,E=%,A=9,R=#; PERY confirms P=&,Y=8. Substitute ARTERY letter by letter.", 3, 12, "MEDIUM", ["9#7%#8", "9#%7#8", "9%7#%8", "9%7%#8"]),
    ("In a certain code, 13479 is written as AQFJL and 5268 as DMPN. How is 396824 written?", "QLPNMF", "Use the digit-to-letter mapping in the examples: 3=Q,9=L,6=P,8=N,2=M,4=F, yielding QLPNMF.", 3, 13, "MEDIUM", ["QLNPMF", "QLPNMF", "QLPMNF", "QLPNME"]),
    ("A code table maps W=5, P=6, J=9, Q=1, E=2, T=3, I=@, A=4, U=©, F=8, D=%, B=★, V=7, M=#, H=$. For MBUVWE, apply these rules: (i) if the first letter is a consonant and the fourth is a vowel, code both as the fourth letter; (ii) if the second is a vowel and last is a consonant, code both as 8; (iii) if the first and last are consonants, interchange their codes. What is the code?", "#★©752", "For MBUVWE, the fourth letter V is a consonant, the second B is a consonant, and the last E is a vowel. None of the three conditions applies; substitute the table directly: #★©752.", 3, 15, "HARD", ["#★#52", "7★©#52", "#★©752", "#★★7528"]),
    ("Using this matrix, encode PAST: rows 0–4 are A R S N C / N C A R S / S N C A R / R S N C A / C A R S N; rows 5–9 are O E L P T / T O E L P / P T O E L / L P T O E / E L P T O. Use the row number followed by column number.", "86,12,31,76", "Locate each letter: P at row 8 column 6, A at row 1 column 2, S at row 3 column 1, T at row 7 column 6.", 3, 19, "HARD", ["75,21,14,65", "86,12,31,76", "58,41,12,67", "88,77,41,67"]),
    ("Using the stated two-block letter matrix (rows 0–4: A R S N C / N C A R S / S N C A R / R S N C A / C A R S N; rows 5–9: O E L P T / T O E L P / P T O E L / L P T O E / E L P T O), encode RATE as row number followed by column number.", "13,12,98,67", "R is at (1,3), A at (1,2), T at (9,8), and E at (6,7).", 3, 20, "HARD", ["13,12,98,67", "42,23,56,76", "30,14,95,89", "24,43,89,95"]),
    ("Using the stated two-block letter matrix (rows 0–4: A R S N C / N C A R S / S N C A R / R S N C A / C A R S N; rows 5–9: O E L P T / T O E L P / P T O E L / L P T O E / E L P T O), encode POET as row number followed by column number.", "69,88,67,65", "P is at (6,9), O at (8,8), E at (6,7), and T at (6,5).", 3, 21, "HARD", ["69,88,67,65", "75,55,65,67", "77,88,98,89", "21,67,76,78"]),
    ("Using the stated two-block letter matrix (rows 0–4: A R S N C / N C A R S / S N C A R / R S N C A / C A R S N; rows 5–9: O E L P T / T O E L P / P T O E L / L P T O E / E L P T O), encode NEST as row number followed by column number.", "21,67,14,59", "N is at (2,1), E at (6,7), S at (1,4), and T at (5,9).", 3, 22, "HARD", ["32,56,20,89", "10,65,41,76", "32,76,34,98", "21,67,14,59"]),
]

def make_row(stem, answer, explanation, difficulty, options, source, pyq=False, exam=None, year=None):
    if len(set(options)) != 4 or answer not in options:
        raise ValueError(f"Invalid options for {stem}")
    return {
        "subject_slug": "reasoning", "subcategory_slug": None,
        "chapter_slug": "coding-decoding", "question_text": stem,
        "options": dict(zip("ABCD", options)),
        "correct_option": "ABCD"[options.index(answer)],
        "explanation": explanation, "difficulty": difficulty,
        "is_pyq": pyq, "pyq_year": year, "pyq_exam_name": exam,
        "source": source,
    }

def main():
    normal = []
    ledger = []
    for stem, answer, proof, pdf, page, level, wrong in SCANNED:
        src = f"{SOURCE_PREFIX} 0{pdf}_.pdf, PDF page {page}; source question; exam/year not stated"
        opts = list(wrong)
        row = make_row(stem, answer, proof, level, opts, src)
        normal.append(row)
        ledger.append({"row":len(normal),"question":stem,"difficulty":level,"expected_answer":answer,"independent_reasoning":proof,"source":src})
    stems = [" ".join(row["question_text"].casefold().split()) for row in normal]
    if len(stems) != len(set(stems)):
        raise ValueError("Duplicate normal-question stem")
    if len(normal) != len(ledger):
        raise ValueError("Batch/ledger length mismatch")
    (ROOT/"data"/"coding_decoding_normal_verified_batch.json").write_text(json.dumps({"questions":normal},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (ROOT/"data"/"coding_decoding_normal_answer_ledger.json").write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"Wrote {len(normal)} scanned normal questions")

if __name__ == "__main__":
    main()
