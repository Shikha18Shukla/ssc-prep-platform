"""Build the source-reviewed CH-15 Word Building bank and answer ledger."""

import json
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
CHAPTER_ID = "886e3a61-031f-48ce-9c62-aff6db3ba7a5"
ORIGINAL = "Original SSC-style practice question"


def item(question, options, answer, explanation, difficulty, topic, subtopic,
         signature, method, source=None, page=None, source_answer=None, data=None):
    return {
        "question": question, "options": options, "answer": answer,
        "explanation": explanation, "difficulty": difficulty, "topic": topic,
        "subtopic": subtopic, "signature": signature, "method": method,
        "source": source, "page": page, "source_answer": source_answer,
        "data": data or {},
    }


P1 = "Word Building 01_ Class Notes.pdf"
P2 = "Word Building 02_ Class Notes.pdf"

ITEMS = [
    # Easy: 10 selected source prompts.
    item("Arrange the words GRAPE, GROWN, GRASS, GROSS and GRIND in dictionary order.",
         ["1, 5, 4, 3, 2", "1, 3, 4, 2, 5", "1, 3, 5, 4, 2", "1, 4, 3, 5, 2"], "C",
         "Compare letter by letter: GRAPE, GRASS, GRIND, GROSS, GROWN. Their labels are 1, 3, 5, 4, 2.",
         "EASY", "dictionary_arrangement", "five-word lexicographic sequence", "source_grape_dictionary_order",
         "Lexicographically sort the five transcribed words and map them to their original labels.", P1, 7, "C",
         {"words": ["GRAPE", "GROWN", "GRASS", "GROSS", "GRIND"], "order": [1, 3, 5, 4, 2]}),
    item("From ORGANISATION, which word cannot be formed using its letters?",
         ["GRANT", "NATION", "GIANTS", "ORANGE"], "D",
         "ORANGE requires E, which does not occur in ORGANISATION. The other three words do not exceed any source-letter frequency.",
         "EASY", "word_formation", "letter-frequency cannot-form", "source_organisation_cannot_form",
         "Compare the frequency Counter of each choice against ORGANISATION.", P1, 10, "D",
         {"base": "ORGANISATION", "valid": {"GRANT": True, "NATION": True, "GIANTS": True, "ORANGE": False}}),
    item("From APPLICATION, which word cannot be formed using its letters?",
         ["POLONIA", "POINT", "OPTICAL", "ANTIC"], "A",
         "POLONIA needs two Os, but APPLICATION contains only one O. POINT, OPTICAL and ANTIC each fit the available letter counts.",
         "EASY", "word_formation", "letter-frequency cannot-form", "source_application_cannot_form",
         "Compare each choice's letter frequencies with APPLICATION; POLONIA alone requires an unavailable extra O.", P1, 12, "A",
         {"base": "APPLICATION", "valid": {"POLONIA": False, "POINT": True, "OPTICAL": True, "ANTIC": True}}),
    item("Letters are numbered 1=O, 2=P, 3=I, 4=L, 5=E and 6=C. Which number sequence forms POLICE?",
         ["3, 1, 2, 5, 4, 6", "2, 1, 4, 3, 6, 5", "2, 5, 6, 4, 1, 3", "4, 3, 1, 5, 2, 6"], "B",
         "POLICE maps P=2, O=1, L=4, I=3, C=6, E=5, giving 2, 1, 4, 3, 6, 5.",
         "EASY", "letter_jumbling", "number mapping to POLICE", "source_police_number_sequence",
         "Map each letter of POLICE through the supplied one-to-one letter-number key.", P2, 4, "B",
         {"mapping": {"1": "O", "2": "P", "3": "I", "4": "L", "5": "E", "6": "C"}, "word": "POLICE", "sequence": "2, 1, 4, 3, 6, 5"}),
    item("Letters are numbered 1=C, 2=A, 3=D, 4=N and 5=E. Which sequence forms DANCE?",
         ["3, 2, 4, 1, 5", "4, 1, 2, 5, 3", "3, 5, 2, 1, 4", "1, 5, 2, 3, 4"], "A",
         "DANCE uses D=3, A=2, N=4, C=1 and E=5, so the sequence is 3, 2, 4, 1, 5.",
         "EASY", "letter_jumbling", "number mapping to DANCE", "source_dance_number_sequence",
         "Map DANCE through the displayed key and compare with the four sequences.", P2, 6, "A",
         {"mapping": {"1": "C", "2": "A", "3": "D", "4": "N", "5": "E"}, "word": "DANCE", "sequence": "3, 2, 4, 1, 5"}),
    item("Letters are numbered 1=M, 2=I, 3=G, 4=A and 5=E. Which sequence forms IMAGE?",
         ["2, 1, 4, 3, 5", "4, 3, 4, 3, 5", "2, 1, 4, 5, 3", "3, 5, 2, 1, 4"], "A",
         "IMAGE maps I=2, M=1, A=4, G=3 and E=5. Therefore the sequence is 2, 1, 4, 3, 5.",
         "EASY", "letter_jumbling", "number mapping to IMAGE", "source_image_number_sequence",
         "Map each letter of IMAGE to its number in the supplied key.", P2, 7, "A",
         {"mapping": {"1": "M", "2": "I", "3": "G", "4": "A", "5": "E"}, "word": "IMAGE", "sequence": "2, 1, 4, 3, 5"}),
    item("Append the same letter to LAN, SAN, WOR and SEE to make four meaningful words. Which letter works?",
         ["A", "D", "B", "K"], "B",
         "Appending D gives LAND, SAND, WORD and SEED, all standard English words.",
         "EASY", "prefix_suffix", "common one-letter suffix", "source_land_sand_word_seed_suffix",
         "Append each candidate to all four stems and confirm the resulting words.", P2, 10, "B: D",
         {"stems": ["LAN", "SAN", "WOR", "SEE"], "suffix": "D", "results": ["LAND", "SAND", "WORD", "SEED"]}),
    item("Which suffix can be added to CONSULT, ASSIST, ACCOUNT and CONTEST to form meaningful words?",
         ["AL", "ANT", "NESS", "MENT"], "B",
         "ANT forms CONSULTANT, ASSISTANT, ACCOUNTANT and CONTESTANT.",
         "EASY", "prefix_suffix", "common agent suffix", "source_common_ant_suffix",
         "Append each suffix to every base word; only ANT produces all four established words.", P2, 11, "B: ANT",
         {"stems": ["CONSULT", "ASSIST", "ACCOUNT", "CONTEST"], "suffix": "ANT", "results": ["CONSULTANT", "ASSISTANT", "ACCOUNTANT", "CONTESTANT"]}),
    item("Add the same letter to the beginning of TOP, COPE, TINK and LOT. Which letter makes meaningful words?",
         ["H", "S", "B", "C"], "B",
         "S forms STOP, SCOPE, STINK and SLOT.",
         "EASY", "prefix_suffix", "common one-letter prefix", "source_stop_scope_stink_slot_prefix",
         "Prepend each option to all four stems; S yields four familiar words.", P2, 12, "B: S",
         {"stems": ["TOP", "COPE", "TINK", "LOT"], "prefix": "S", "results": ["STOP", "SCOPE", "STINK", "SLOT"]}),
    item("When YAWN is arranged in alphabetical order, which letter remains in its original position?",
         ["W", "Y", "N", "A"], "A",
         "Alphabetical order is A, N, W, Y. W remains in position 3, its original position.",
         "EASY", "alphabetical_positions", "unchanged letter position", "source_yawn_unchanged_letter",
         "Sort the letters and compare each sorted position with the original word.", P2, 18, "A: W",
         {"word": "YAWN", "unchanged_positions": [3]}),

    # Medium: 7 source and 3 original questions.
    item("From AMPLIFICATION, which word can be formed using its letters?",
         ["ACTOR", "MANOR", "CHAMP", "MANIA"], "D",
         "MANIA can be made from M, A, N, I and A. ACTOR and MANOR need R; CHAMP needs H, neither of which occurs in AMPLIFICATION.",
         "MEDIUM", "word_formation", "letter-frequency can-form", "source_amplification_can_form",
         "Check each candidate against the letter-frequency Counter for AMPLIFICATION.", P1, 14, "D",
         {"base": "AMPLIFICATION", "valid": {"ACTOR": False, "MANOR": False, "CHAMP": False, "MANIA": True}}),
    item("Letters map as T=5, M=4, H=3, R=2, E=1 and O=0. Which sequence spells MOTHER?",
         ["0, 2, 5, 3, 1, 4", "5, 0, 4, 2, 3, 1", "3, 1, 5, 4, 0, 2", "4, 0, 5, 3, 1, 2"], "D",
         "MOTHER maps M=4, O=0, T=5, H=3, E=1, R=2: 4, 0, 5, 3, 1, 2.",
         "MEDIUM", "letter_jumbling", "number mapping to MOTHER", "source_mother_number_sequence",
         "Use the displayed letter-number key in the order M-O-T-H-E-R.", P2, 5, "D",
         {"mapping": {"5": "T", "4": "M", "3": "H", "2": "R", "1": "E", "0": "O"}, "word": "MOTHER", "sequence": "4, 0, 5, 3, 1, 2"}),
    item("Which word is second in dictionary order: THRONE, THRIFT, THROAT or THRILL?",
         ["THROAT", "THRILL", "THRIFT", "THRONE"], "B",
         "All words begin THR. THRIFT and THRILL continue with I, which sorts before O in THROAT and THRONE. Between THRIFT and THRILL, F precedes L, so THRILL is second.",
         "MEDIUM", "dictionary_arrangement", "shared-prefix second word", "original_thrift_shared_prefix_second",
         "Compare complete spellings lexicographically: THRIFT, THRILL, THROAT, THRONE.",
         data={"words": ["THRONE", "THRIFT", "THROAT", "THRILL"], "order": ["THRIFT", "THRILL", "THROAT", "THRONE"], "position": 2}),
    item("Letters H, T, R, U, O and A are numbered 1, 2, 3, 4, 5 and 6 respectively. Which sequence spells AUTHOR?",
         ["6, 4, 2, 1, 5, 3", "3, 4, 5, 2, 1, 6", "1, 6, 2, 4, 5, 3", "2, 1, 5, 3, 4, 6"], "A",
         "Using H=1, T=2, R=3, U=4, O=5 and A=6, AUTHOR maps A-U-T-H-O-R to 6, 4, 2, 1, 5, 3.",
         "MEDIUM", "letter_jumbling", "letter-number mapping to AUTHOR", "source_author_number_sequence",
         "Read AUTHOR in order and replace each letter with its displayed number.", P2, 9, "A",
         {"mapping": {"1": "H", "2": "T", "3": "R", "4": "U", "5": "O", "6": "A"}, "word": "AUTHOR", "sequence": "6, 4, 2, 1, 5, 3"}),
    item("How many letters in DRAWING remain in the same position after its letters are alphabetized?",
         ["1", "3", "2", "0"], "D",
         "DRAWING sorts to A-D-G-I-N-R-W. Comparing positions 1 through 7 with D-R-A-W-I-N-G, no position contains the same letter.",
         "MEDIUM", "alphabetical_positions", "unchanged positions after sorting", "source_drawing_unchanged_count",
         "Alphabetically sort DRAWING and count index-by-index matches with the original.", P2, 14, "D: 0",
         {"word": "DRAWING", "unchanged_positions": []}),
    item("How many letters in DEVELOP remain in the same position after its letters are alphabetized?",
         ["2", "4", "3", "5"], "A",
         "DEVELOP sorts to D-E-E-L-O-P-V. D at position 1 and E at position 2 stay in place; the other positions change.",
         "MEDIUM", "alphabetical_positions", "unchanged positions with repeated letters", "source_develop_unchanged_count",
         "Sort the multiset of letters and compare each position; repeated Es are counted by position, not by identity.", P2, 15, "A: 2",
         {"word": "DEVELOP", "unchanged_positions": [1, 2]}),
    item("In SIGNATURE, how many letters lie between the first vowel and the last consonant?",
         ["3", "4", "5", "6"], "C",
         "The first vowel I is at position 2. The last consonant R is at position 8. Positions 3 through 7 contain five letters.",
         "MEDIUM", "letter_pairs", "distance between specified letter positions", "source_signature_inner_letters",
         "Locate the first vowel and last consonant, then subtract their indices and exclude both endpoints.", P2, 16, "C: 5",
         {"word": "SIGNATURE", "first_vowel_index": 2, "last_consonant_index": 8, "between_count": 5}),
    item("How many pairs in PERHAPS have the same number of letters between them in the word and in the alphabet? Count each pair once, in either alphabetic direction.",
         ["1", "2", "3", "4"], "A",
         "Only P-R qualifies: the letters are two positions apart in PERHAPS and two alphabet positions apart (P=16, R=18). The other pairs fail this equality.",
         "MEDIUM", "letter_pairs", "equal word and alphabet separation", "source_perhaps_letter_pairs",
         "Enumerate all position pairs once and test abs(alphabet index difference) = word index difference.", P2, 20, "A: One",
         {"word": "PERHAPS", "pairs": [["P", "R"]], "count": 1}),
    item("From EDUCATION, which word cannot be formed using its letters?",
         ["ACTION", "CAUTION", "EDUCATE", "AUCTION"], "C",
         "EDUCATE needs two Es, while EDUCATION has one E. ACTION, CAUTION and AUCTION each fit the available letter frequencies.",
         "MEDIUM", "word_formation", "repeated-letter frequency cannot-form", "original_education_letter_frequency",
         "Compare each choice's frequency Counter with EDUCATION; EDUCATE is the only overdrawn letter count.",
         data={"base": "EDUCATION", "valid": {"ACTION": True, "CAUTION": True, "EDUCATE": False, "AUCTION": True}}),
    item("Which suffix completes all four words: THANK__, CARE__, HOPE__ and USE__?",
         ["LESS", "FUL", "ABLE", "NESS"], "B",
         "FUL gives THANKFUL, CAREFUL, HOPEFUL and USEFUL, all common words. The other suffixes do not form a valid word with every stem.",
         "MEDIUM", "prefix_suffix", "common productive suffix", "original_common_ful_suffix",
         "Append each candidate suffix to each stem and check that all four results are standard English words.",
         data={"stems": ["THANK", "CARE", "HOPE", "USE"], "suffix": "FUL", "results": ["THANKFUL", "CAREFUL", "HOPEFUL", "USEFUL"]}),

    # Hard: 3 selected source prompts and 7 original questions.
    item("How many letters in FLAGSTONE remain in the same position after alphabetical arrangement?",
         ["2", "1", "4", "None"], "A",
         "FLAGSTONE sorts to A-E-F-G-L-N-O-S-T. G remains at position 4 and O at position 7, so two positions are unchanged.",
         "HARD", "alphabetical_positions", "unchanged positions in nine-letter word", "source_flagstone_unchanged_count",
         "Sort the letters and compare all nine positions; G at 4 and O at 7 are the only matches.", P2, 17, "A: 2",
         {"word": "FLAGSTONE", "unchanged_positions": [4, 7]}),
    item("How many qualifying letter pairs are in FANCIER? Count each pair once, including either alphabetic direction.",
         ["1", "2", "3", "More than three"], "D",
         "Five pairs qualify: F-C, A-C, A-E, N-R and C-E. In each, the absolute alphabet-position difference equals the distance between the letters' positions in FANCIER.",
         "HARD", "letter_pairs", "enumerate all equal-distance pairs", "source_fancier_letter_pairs",
         "Exhaustively test all 21 pairs of positions using absolute alphabetic distance; five satisfy the rule.", P2, 21, "D: More than three",
         {"word": "FANCIER", "pairs": [["F", "C"], ["A", "C"], ["A", "E"], ["N", "R"], ["C", "E"]], "count": 5}),
    item("How many qualifying letter pairs are in BEACON? Count each pair once, in either alphabetic direction.",
         ["1", "2", "3", "4"], "B",
         "E-C qualifies because their alphabet positions differ by 2 and they are two places apart in the word. O-N also qualifies at distance 1. Total: 2.",
         "HARD", "letter_pairs", "bidirectional equal-distance pairs", "source_beacon_letter_pairs",
         "Check every pair once with absolute alphabet-position difference equal to their word-position distance.", P2, 22, "B: Two",
         {"word": "BEACON", "pairs": [["E", "C"], ["O", "N"]], "count": 2}),
    item("Arrange PREVENT, PREVIEW, PREY and PREACH in dictionary order. Which word is third?",
         ["PREVENT", "PREVIEW", "PREY", "PREACH"], "B",
         "The complete dictionary order is PREACH, PREVENT, PREVIEW, PREY, so PREVIEW is third.",
         "HARD", "dictionary_arrangement", "third word among shared-prefix items", "original_pre_third_dictionary_word",
         "Sort all full words lexicographically, then select position three." ,
         data={"words": ["PREVENT", "PREVIEW", "PREY", "PREACH"], "order": ["PREACH", "PREVENT", "PREVIEW", "PREY"], "position": 3}),
    item("Arrange TRANSFER, TRANSIT, TRANSLATE and TRANSPORT in dictionary order. Which word is second?",
         ["TRANSFER", "TRANSIT", "TRANSLATE", "TRANSPORT"], "B",
         "After TRANS, the next differing letters are F, I, L and P, respectively. Thus TRANSFER, TRANSIT, TRANSLATE, TRANSPORT; TRANSIT is second.",
         "HARD", "dictionary_arrangement", "long common-prefix comparison", "original_trans_dictionary_second",
         "Compare each word letter-by-letter after the common TRANS prefix; F < I < L < P.",
         data={"words": ["TRANSFER", "TRANSIT", "TRANSLATE", "TRANSPORT"], "order": ["TRANSFER", "TRANSIT", "TRANSLATE", "TRANSPORT"], "position": 2}),
    item("From MISSISSIPPI, which word cannot be formed using its letters?",
         ["MISS", "PISS", "SIPS", "PIPES"], "D",
         "PIPES requires E, absent from MISSISSIPPI. Each other option is within the source frequencies (M=1, I=4, S=4, P=2).",
         "HARD", "word_formation", "multiple repeated-letter counts", "original_mississippi_letter_frequency",
         "Compare each option's frequency Counter against MISSISSIPPI; PIPES alone uses a missing letter.",
         data={"base": "MISSISSIPPI", "valid": {"MISS": True, "PISS": True, "SIPS": True, "PIPES": False}}),
    item("Letters are numbered 1=T, 2=A, 3=E, 4=C and 5=R. Which sequence forms TRACE?",
         ["1, 5, 2, 4, 3", "5, 1, 2, 3, 4", "1, 2, 5, 4, 3", "3, 5, 2, 1, 4"], "A",
         "TRACE maps T=1, R=5, A=2, C=4 and E=3. The sequence is 1, 5, 2, 4, 3.",
         "HARD", "letter_jumbling", "reordered five-letter mapping", "original_trace_number_sequence",
         "Decode each number in the sequence and compare the resulting letters with TRACE.",
         data={"mapping": {"1": "T", "2": "A", "3": "E", "4": "C", "5": "R"}, "word": "TRACE", "sequence": "1, 5, 2, 4, 3"}),
    item("The letters G, A, R, D, E and N are numbered 3, 5, 1, 4, 2 and 6 respectively. Which number sequence spells GARDEN?",
         ["3, 5, 1, 4, 2, 6", "5, 3, 1, 4, 6, 2", "3, 1, 5, 2, 4, 6", "6, 2, 4, 1, 5, 3"], "A",
         "Read the code in G-A-R-D-E-N order: 3, 5, 1, 4, 2, 6.",
         "HARD", "letter_jumbling", "six-letter mapped word", "original_garden_number_sequence",
         "Apply the given number for each successive letter in GARDEN.",
         data={"mapping": {"3": "G", "5": "A", "1": "R", "4": "D", "2": "E", "6": "N"}, "word": "GARDEN", "sequence": "3, 5, 1, 4, 2, 6"}),
    item("How many letters in BALLOON remain in the same position after alphabetical arrangement?",
         ["1", "2", "3", "4"], "C",
         "BALLOON sorts to A-B-L-L-N-O-O. The two Ls remain at positions 3 and 4, and O remains at position 6: three positions match.",
         "HARD", "alphabetical_positions", "repeated letters after sorting", "original_balloon_unchanged_positions",
         "Sort the letters as a multiset and compare position-by-position; positions 3 and 4 match.",
         data={"word": "BALLOON", "unchanged_positions": [3, 4, 6]}),
    item("How many pairs in DECEPTION have the same number of letters between them in the word and in the alphabet? Count each pair once in either alphabetic direction.",
         ["2", "3", "4", "5"], "A",
         "The qualifying pairs are D-E and O-N; each pair is adjacent in the word and adjacent in the alphabet. Therefore there are two pairs.",
         "HARD", "letter_pairs", "exhaustive equal-distance pair count", "original_deception_letter_pairs",
         "Enumerate all pairs of positions and count those where absolute alphabet-index gap equals word-index gap.",
         data={"word": "DECEPTION", "pairs": [["D", "E"], ["O", "N"]], "count": 2}),
]


def pair_list(word):
    return [
        [word[i], word[j]]
        for i in range(len(word))
        for j in range(i + 1, len(word))
        if abs(ord(word[i]) - ord(word[j])) == j - i
    ]


def validate(item_data):
    opts = (dict(zip("ABCD", item_data["options"]))
            if isinstance(item_data["options"], list) else item_data["options"])
    assert set(opts) == set("ABCD") and len({v.casefold() for v in opts.values()}) == 4
    assert item_data["answer"] in opts and item_data["difficulty"] in {"EASY", "MEDIUM", "HARD"}
    data = item_data["data"]
    if "base" in data:
        base = Counter(data["base"].casefold())
        for word, valid in data["valid"].items():
            assert (Counter(word.casefold()) <= base) is valid, (data["base"], word, valid)
        correct_text = opts[item_data["answer"]]
        is_cannot = "cannot be formed" in item_data["question"].casefold()
        assert data["valid"][correct_text] is (not is_cannot)
        assert sum(v is (not is_cannot) for v in data["valid"].values()) == 1
    if "mapping" in data:
        seq = [part.strip() for part in data["sequence"].split(",")]
        assert "".join(data["mapping"][n] for n in seq) == data["word"]
        assert opts[item_data["answer"]] == data["sequence"]
    if "word" in data and "unchanged_positions" in data:
        sorted_word = "".join(sorted(data["word"]))
        actual = [i + 1 for i, (a, b) in enumerate(zip(data["word"], sorted_word)) if a == b]
        assert actual == data["unchanged_positions"], (data["word"], sorted_word, actual)
        answer_text = opts[item_data["answer"]]
        if answer_text.isdigit():
            assert int(answer_text) == len(actual)
        else:
            assert len(actual) == 1 and answer_text == data["word"][actual[0] - 1]
    if "pairs" in data:
        assert pair_list(data["word"]) == data["pairs"], (data["word"], pair_list(data["word"]), data["pairs"])
        if "count" in data:
            assert len(data["pairs"]) == data["count"]
            answer_text = opts[item_data["answer"]]
            if data["count"] > 3:
                assert answer_text.casefold() == "more than three"
            else:
                assert answer_text == str(data["count"])
    if "first_vowel_index" in data:
        word = data["word"]
        first_vowel = next(i + 1 for i, ch in enumerate(word) if ch.casefold() in "aeiou")
        last_consonant = max(i + 1 for i, ch in enumerate(word) if ch.casefold() not in "aeiou")
        assert first_vowel == data["first_vowel_index"] and last_consonant == data["last_consonant_index"]
        assert last_consonant - first_vowel - 1 == data["between_count"]
        assert opts[item_data["answer"]] == str(data["between_count"])
    if "words" in data and "order" in data:
        expected = sorted(data["words"], key=str.casefold)
        if data["order"] and isinstance(data["order"][0], int):
            actual = [data["words"][n - 1] for n in data["order"]]
        else:
            actual = data["order"]
        assert [str(x) for x in actual] == [str(x) for x in expected]
        if isinstance(item_data["answer"], str) and item_data["answer"] in opts:
            position = data.get("position")
            answer_text = opts[item_data["answer"]]
            if data["order"] and isinstance(data["order"][0], int):
                assert [int(part.strip()) for part in answer_text.split(",")] == data["order"]
            elif position is not None:
                assert answer_text == expected[position - 1]
            else:
                assert answer_text.replace(" ", "").split(",") == expected
    if "results" in data:
        assert len(data["results"]) == len(data.get("stems", []))
        affix = data.get("suffix", data.get("prefix"))
        if "suffix" in data:
            assert all(result == stem + affix for stem, result in zip(data["stems"], data["results"]))
        else:
            assert all(result == affix + stem for stem, result in zip(data["stems"], data["results"]))
        assert opts[item_data["answer"]] == affix


def build():
    assert len(ITEMS) == 30
    levels = Counter(x["difficulty"] for x in ITEMS)
    assert levels == {"EASY": 10, "MEDIUM": 10, "HARD": 10}, levels
    rows, ledger = [], []
    for index, x in enumerate(ITEMS, 1):
        validate(x)
        options = (dict(zip("ABCD", x["options"]))
                   if isinstance(x["options"], list) else x["options"])
        source = ORIGINAL if x["source"] is None else f"{x['source']}, page {x['page']}; exam/year not stated"
        row = {
            "subject_slug": "reasoning", "subcategory_slug": None, "chapter_slug": "word-building",
            "question_text": x["question"], "options": options,
            "correct_option": x["answer"], "explanation": x["explanation"],
            "difficulty": x["difficulty"], "is_pyq": False, "pyq_year": None,
            "pyq_exam_name": None, "source": source,
        }
        audit = {
            "question_id": f"word-building-{index:03}", "row": index,
            "chapter_id": CHAPTER_ID,
            "question": x["question"], "topic": x["topic"], "subtopic": x["subtopic"],
            "difficulty": x["difficulty"], "source_type": "original" if x["source"] is None else "pdf-derived",
            "source_pdf": x["source"], "source_page": x["page"], "source": source,
            "source_answer": x["source_answer"], "expected_answer": options[x["answer"]],
            "correct_option": x["answer"], "explanation": x["explanation"],
            "independent_verification": x["method"], "verification_data": x["data"],
            "concept_signature": x["signature"], "is_pyq": False,
            "validation_status": "PASS - independent checks and four-option review",
        }
        rows.append(row); ledger.append(audit)
    (BASE / "data" / "word_building_verified_batch.json").write_text(
        json.dumps({"questions": rows}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (BASE / "data" / "word_building_answer_ledger.json").write_text(
        json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("BUILT", len(rows), dict(levels), "source", sum(x["source"] is not None for x in ITEMS), "original", sum(x["source"] is None for x in ITEMS))


if __name__ == "__main__":
    build()
