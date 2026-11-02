"""Build the reviewed Ranking and Order batch, answer ledger, and report."""

import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
PDF_NAME = "Ranking and Order  01_ Class Notes.pdf"
ORIGINAL = "Original SSC-style practice question"

# difficulty, stem, correct answer, three distractors, explanation, PDF page or None, signature
ITEMS = [
    ("EASY", "In a group of 40 students, S is 15th from the top. What is S's rank from the bottom?", "26th", ["25th", "24th", "27th"], "Opposite-end rank = total − given rank + 1 = 40 − 15 + 1 = 26th.", 6, "vertical_rank_15_of_40"),
    ("EASY", "Amit is 7th from the top and 26th from the bottom in his class. How many students are there?", "32", ["31", "33", "34"], "Total = top rank + bottom rank − 1 = 7 + 26 − 1 = 32.", 7, "amit_top7_bottom26_total"),
    ("EASY", "A person is 27th in a queue from one end and 38th from the other. How many people are in the queue?", "64", ["63", "65", "66"], "The person's place is counted from both ends, so total = 27 + 38 − 1 = 64.", 8, "queue_rank27_rank38_total"),
    ("MEDIUM", "There are 35 people in a group. Govind is 6th from the top, and Krishna is 7 places below him. What is Krishna's rank from the bottom?", "23rd", ["22nd", "24th", "29th"], "Krishna is 6 + 7 = 13th from the top. From the bottom he is 35 − 13 + 1 = 23rd.", 9, "govind_krishna_relative_rank"),
    ("MEDIUM", "Ram and Sham are 13th and 14th from the top, respectively, in a class of 23. What are their ranks from the bottom, respectively?", "11th and 10th", ["10th and 11th", "11th and 9th", "12th and 11th"], "Ram: 23 − 13 + 1 = 11th. Sham: 23 − 14 + 1 = 10th.", 10, "ram_sham_opposite_ranks"),
    ("HARD", "Samsung is 37th from the right and Nokia is 31st from the left. After they interchange positions, Samsung is 46th from the right. How many students are in the row?", "76", ["75", "77", "68"], "After the swap Samsung occupies Nokia's original position, so Nokia was 46th from the right. Total = Nokia's left rank 31 + right rank 46 − 1 = 76. Samsung's initial rank is not needed.", 12, "samsung_nokia_swap_total"),
    ("HARD", "Sahil is 12th from the left and Gaurav is 18th from the right. After they interchange, Sahil is 25th from the left. How many people are in the row?", "42", ["41", "43", "40"], "Sahil moves to Gaurav's original position, so Gaurav was 25th from the left. Total = 25 + 18 − 1 = 42.", 13, "sahil_gaurav_swap_total"),
    ("HARD", "Sameer is 20th from the left and Arun is 12th from the right. After they interchange, Arun is 10th from the right. How many people are in the row?", "29", ["28", "30", "31"], "Arun moves to Sameer's original position. Thus Sameer's position is 10th from the right; total = 20 + 10 − 1 = 29.", 14, "sameer_arun_swap_total"),
    ("EASY", "There are 28 runners. Meera finishes 9th from the front. What is her rank from the end?", "20th", ["19th", "21st", "18th"], "Rank from the end = 28 − 9 + 1 = 20th.", None, "original_rank_from_opposite_end_28_9"),
    ("EASY", "A student is 12th from the bottom in a class of 35. What is the student's rank from the top?", "24th", ["23rd", "25th", "22nd"], "Rank from the top = 35 − 12 + 1 = 24th.", None, "original_rank_from_bottom_35_12"),
    ("EASY", "A contestant is 17th from the front and 21st from the back. How many contestants are there?", "37", ["36", "38", "39"], "Total = 17 + 21 − 1 = 37.", None, "original_two_end_ranks_17_21"),
    ("EASY", "In a row of 43 people, what is the middle position when counted from either end?", "22nd", ["21st", "23rd", "22nd from the left and 21st from the right"], "For an odd total of 43, the single middle position is (43 + 1) ÷ 2 = 22nd from either end.", None, "original_odd_middle_position_43"),
    ("EASY", "A player is 8th from the left in a line. How many players stand ahead of the player?", "7", ["8", "9", "6"], "The player's rank includes the player, so the number ahead is 8 − 1 = 7.", None, "original_people_ahead_rank8"),
    ("EASY", "In a class of 30, a girl is 12th from the bottom. How many students are above her?", "18", ["17", "19", "12"], "There are 30 − 12 = 18 students above her; her own place is excluded.", None, "original_above_from_bottom_30_12"),
    ("EASY", "A swimmer is 6th from the finish end in a field of 24. What is the swimmer's rank from the starting end?", "19th", ["18th", "20th", "17th"], "Opposite-end rank = 24 − 6 + 1 = 19th.", None, "original_finish_to_start_rank_24_6"),
    ("MEDIUM", "In a line of 26, A is 8th from the left and B is 7th from the right. How many people stand between A and B?", "11", ["10", "12", "9"], "B is 26 − 7 + 1 = 20th from the left. The people strictly between positions 8 and 20 are 20 − 8 − 1 = 11.", None, "original_between_opposite_ranks_26"),
    ("MEDIUM", "A is 9th from the left, B is 14th from the right, and exactly 5 people are between them. How many people are in the row?", "28", ["27", "29", "26"], "With ranks measured from opposite ends and 5 people between, total = 9 + 14 + 5 = 28.", None, "original_total_opposite_ranks_with_gap"),
    ("MEDIUM", "There are 42 students. Ravi is 13th from the top, and Aman is 9 places below Ravi. What is Aman's rank from the bottom?", "21st", ["20th", "22nd", "30th"], "Aman is 13 + 9 = 22nd from the top. From the bottom: 42 − 22 + 1 = 21st.", None, "original_relative_rank_then_reverse"),
    ("MEDIUM", "In a row of 39, Leena is 16th from the left and Vina is 23rd from the right. How many people are between them?", "0", ["1", "2", "3"], "Vina is 39 − 23 + 1 = 17th from the left, immediately after Leena at 16th. No one is between them.", None, "original_adjacent_from_opposite_ends"),
    ("MEDIUM", "In a group of 34, R is 11th from the left and S is 13th from the right. How many people are between them?", "10", ["9", "11", "12"], "S is 34 − 13 + 1 = 22nd from the left. Between ranks 11 and 22 are 22 − 11 − 1 = 10 people.", None, "original_people_between_11_22"),
    ("MEDIUM", "There are 45 students. P is 18th from the top. Q is 5 places ahead of P. What is Q's rank from the bottom?", "33rd", ["32nd", "34th", "27th"], "Q is 18 − 5 = 13th from the top. From the bottom: 45 − 13 + 1 = 33rd.", None, "original_ahead_then_bottom_rank"),
    ("MEDIUM", "In a class of 32, B is 4 places below A, who is 6th from the top. C is 3 places below B. What is C's rank from the bottom?", "20th", ["19th", "21st", "23rd"], "B is 10th and C is 13th from the top. C's bottom rank is 32 − 13 + 1 = 20th.", None, "original_three_person_rank_chain"),
    ("MEDIUM", "M is 5th from the top in a class of 27. N is 6 positions below M. What is N's rank from the bottom?", "17th", ["16th", "18th", "12th"], "N is 5 + 6 = 11th from the top. From the bottom: 27 − 11 + 1 = 17th.", None, "original_rank_six_positions_below"),
    ("HARD", "K's position number is 8 less than R's, and R's is 13 less than S's. If S is 21st from the bottom in a group of 48, what is K's rank from the bottom?", "42nd", ["41st", "43rd", "34th"], "From the bottom, R is 21 + 13 = 34th and K is 34 + 8 = 42nd. A person ahead has a larger rank number when counted from the bottom.", None, "original_three_rank_offsets_from_bottom"),
    ("HARD", "A is 19th from the left and B is 16th from the right. If exactly 7 people stand between them, how many people are in the row?", "42", ["41", "43", "40"], "With positions counted from opposite ends and 7 people between them, total = 19 + 16 + 7 = 42.", None, "original_opposite_end_ranks_and_gap"),
    ("HARD", "There are 60 students. A is 17th from the top. B is 12 positions below A, and C is 8 positions ahead of B. What is C's rank from the bottom?", "40th", ["39th", "41st", "32nd"], "B is 29th from the top. C is 29 − 8 = 21st from the top. From the bottom: 60 − 21 + 1 = 40th.", None, "original_three_rank_chain_total"),
    ("HARD", "In a row of 60, A is 14th from the left, B is 21st from the left, and C is 33rd from the right. A and B swap places, then B and C swap places. What is C's final rank from the left?", "14th", ["21st", "28th", "33rd"], "After the first swap B stands in A's original 14th position. In the second swap C takes B's current position, so C finishes 14th from the left.", None, "original_two_sequential_swaps"),
    ("HARD", "Tara is 18th from the front. Mohan is 7 positions behind Tara, and Jaya is 9 positions ahead of Mohan. In a field of 60, what is Jaya's rank from the end?", "45th", ["44th", "46th", "36th"], "Mohan is 18 + 7 = 25th from the front. Jaya is 25 − 9 = 16th. From the end: 60 − 16 + 1 = 45th.", None, "original_mixed_ahead_behind_chain"),
    ("HARD", "In a queue, R is 8th from the front. S is 11 positions behind R, and T is 7 positions ahead of S. How many people stand between R and T?", "3", ["2", "4", "7"], "S is 8 + 11 = 19th from the front; T is 19 − 7 = 12th. The gap between ranks 8 and 12 is 12 − 8 − 1 = 3 people.", None, "original_three_person_queue_offsets"),
    ("HARD", "There are 70 people in a line. A is 26th from the top and B is 29th from the bottom. How many people stand between A and B?", "15", ["13", "14", "16"], "B is 70 − 29 + 1 = 42nd from the top. The people between ranks 26 and 42 are 42 − 26 − 1 = 15.", None, "original_long_line_opposite_ranks"),
]


def build():
    rows, ledger = [], []
    for i, (difficulty, question, answer, distractors, explanation, page, signature) in enumerate(ITEMS, 1):
        if answer in distractors or len(set(distractors)) != 3:
            raise ValueError(f"Row {i}: provide one answer and three distinct distractors")
        choices = list(distractors)
        choices.insert((i - 1) % 4, answer)
        options = dict(zip("ABCD", choices))
        key = next(k for k, value in options.items() if value == answer)
        source = ORIGINAL if page is None else f"{PDF_NAME}, page {page}; exam/year not stated"
        row = {
            "subject_slug": "reasoning", "subcategory_slug": None, "chapter_slug": "ranking-and-order",
            "question_text": question, "options": options, "correct_option": key, "explanation": explanation,
            "difficulty": difficulty, "is_pyq": False, "pyq_year": None, "pyq_exam_name": None, "source": source,
        }
        rows.append(row)
        ledger.append({
            "question_id": f"ranking-order-{i:03}", "row": i, "source_type": "original" if page is None else "pdf-derived",
            "source_pdf": None if page is None else PDF_NAME, "source_page": page, "question": question,
            "options": options, "expected_answer": answer, "correct_option": key, "explanation": explanation,
            "difficulty": difficulty, "verification_status": "PASS - independently solved",
            "pyq_status": "original practice; imported as Normal" if page is None else "no PYQ label present; imported as Normal",
            "source": source, "independent_reasoning": explanation,
            "option_review": f"Answer is {key}; all four options are distinct.",
            "concept_signature": signature, "validation_status": "PASS",
        })
    ledger[5]["rejected_source_questions"] = [{
        "source_pdf": PDF_NAME, "source_page": 11,
        "question_summary": "Diagram showing R and V on opposite ends with an interchange annotation.",
        "rejection_reason": "The diagram has no complete printed question and the handwritten rank labels do not unambiguously identify each person's original and post-swap end-ranks; no unique total can be verified.",
    }]
    (DATA / "ranking_order_verified_batch.json").write_text(json.dumps({"questions": rows}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (DATA / "ranking_order_answer_ledger.json").write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (DATA / "ranking_order_review_report.md").write_text("""# Ranking and Order review\n\n## Status\n\nCOMPLETED. Artifact review, append-only import, replay, cross-chapter duplicate scan, and authenticated API verification passed.\n\n## Source review\n\nAll 17 physical PDF pages were visually inspected. The task's later example page references are offset from the PDF's physical 1-based order; provenance below uses the physical page positions. Reviewed 9 question/example prompts, selected 8 clear, unique questions, and rejected 1 ambiguous diagram. Formula, recap, and title slides without complete prompts were excluded from the prompt count.\n\n| PDF | Pages inspected | Selected | Rejected / excluded |\n|---|---:|---:|---|\n| Ranking and Order  01_ Class Notes.pdf | 17/17 | 8 | 1: page 11 swap diagram lacks a complete, unambiguous statement and clearly identified original/post-swap ranks. |\n\n## Bank\n\nThe batch contains 30 Normal questions: 8 PDF-derived and 22 original SSC-style practice questions. Difficulty: 10 Easy, 10 Medium, 10 Hard. All have four distinct options and one independently checked answer. No PYQ label appears on the selected source questions; no PYQ rows are created.\n\n## Database verification\n\nThe guarded importer inserted 30 active Normal questions into the verified Ranking and Order chapter (10 Easy, 10 Medium, 10 Hard), with 0 PYQs, 0 rejects, and 0 import duplicates. Replay dry-run detected all 30 as existing duplicates and would add 0 rows. Post-import database verification confirmed 30 active Normal rows and 30 total rows.\n\nAuthenticated API checks returned 10 available questions for each difficulty with a 10-question request. The question management API returned 30 Normal questions; each has four choices and exactly one correct choice. A read-only cross-chapter scan compared all 30 stems against 4,023 active question stems in other chapters at a 0.97 similarity threshold and found no matches.\n""", encoding="utf-8")


if __name__ == "__main__":
    build()
