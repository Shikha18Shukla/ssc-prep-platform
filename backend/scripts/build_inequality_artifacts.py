"""Build CH-16 artifacts and independently solve strict/non-strict order constraints."""

import json
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
CHAPTER_ID = "6d8b6da5-6635-417c-99e4-0bb7f511520b"
PDF = "Inequality 01_ Class Notes.pdf"
ORIGINAL = "Original SSC-style practice question"

STATUS_OPTIONS = {
    "TRUE": "Definitely follows",
    "FALSE": "Definitely false",
    "UNKNOWN": "Cannot be determined",
    "INCONSISTENT": "Statements are inconsistent",
}
CONCLUSION_OPTIONS = {
    "ONLY_I": "Only conclusion I follows",
    "ONLY_II": "Only conclusion II follows",
    "BOTH": "Both conclusions I and II follow",
    "NEITHER": "Neither conclusion follows",
    "EITHER": "Either conclusion I or II follows",
}
COMMON_FOUR = ["ONLY_I", "ONLY_II", "BOTH", "NEITHER"]


def closure(statements, extra_variables=()):
    """Return strict-aware transitive closure for constraints over a total order.

    Each edge a -> b means a <= b; a strict edge means a < b. A system is
    inconsistent exactly when a strict edge lies on a directed cycle. This is
    sound for arbitrary real or integer values because the input only contains
    order/equality constraints (no arithmetic offsets).
    """
    variables = sorted({x for row in statements for x in (row["left"], row["right"])} | set(extra_variables))
    reach = {a: {b: a == b for b in variables} for a in variables}
    strict = {a: {b: False for b in variables} for a in variables}

    def edge(a, b, is_strict):
        reach[a][b] = True
        strict[a][b] = strict[a][b] or is_strict

    for row in statements:
        a, op, b = row["left"], row["op"], row["right"]
        if op == "<":
            edge(a, b, True)
        elif op == "≤":
            edge(a, b, False)
        elif op == ">":
            edge(b, a, True)
        elif op == "≥":
            edge(b, a, False)
        elif op == "=":
            edge(a, b, False)
            edge(b, a, False)
        else:
            raise ValueError(f"Unsupported inequality operator: {op}")

    for k in variables:
        for i in variables:
            if not reach[i][k]:
                continue
            for j in variables:
                if reach[k][j]:
                    path_is_strict = strict[i][k] or strict[k][j]
                    if not reach[i][j]:
                        reach[i][j] = True
                    if path_is_strict:
                        strict[i][j] = True

    inconsistent = any(strict[v][v] for v in variables)
    return variables, reach, strict, inconsistent


def relation_true(claim, reach, strict):
    a, op, b = claim["left"], claim["op"], claim["right"]
    if op == "<":
        return reach.get(a, {}).get(b, False) and strict.get(a, {}).get(b, False)
    if op == "≤":
        return reach.get(a, {}).get(b, False)
    if op == ">":
        return reach.get(b, {}).get(a, False) and strict.get(b, {}).get(a, False)
    if op == "≥":
        return reach.get(b, {}).get(a, False)
    if op == "=":
        return (reach.get(a, {}).get(b, False) and reach.get(b, {}).get(a, False)
                and not strict.get(a, {}).get(b, False) and not strict.get(b, {}).get(a, False))
    raise ValueError(f"Unsupported claim operator: {op}")


def relation_false(claim, reach, strict):
    """Whether every model satisfies the logical negation of a comparison."""
    a, op, b = claim["left"], claim["op"], claim["right"]
    if op == "<":
        return reach.get(b, {}).get(a, False)  # a >= b
    if op == "≤":
        return reach.get(b, {}).get(a, False) and strict.get(b, {}).get(a, False)  # a > b
    if op == ">":
        return reach.get(a, {}).get(b, False)  # a <= b
    if op == "≥":
        return reach.get(a, {}).get(b, False) and strict.get(a, {}).get(b, False)  # a < b
    if op == "=":
        return (reach.get(a, {}).get(b, False) and strict.get(a, {}).get(b, False)
                or reach.get(b, {}).get(a, False) and strict.get(b, {}).get(a, False))
    raise ValueError(f"Unsupported claim operator: {op}")


def classify_claim(statements, claim):
    _, reach, strict, inconsistent = closure(statements, (claim["left"], claim["right"]))
    if inconsistent:
        return "INCONSISTENT"
    if relation_true(claim, reach, strict):
        return "TRUE"
    if relation_false(claim, reach, strict):
        return "FALSE"
    return "UNKNOWN"


def is_complementary(first, second):
    if (first["left"], first["right"]) != (second["left"], second["right"]):
        return False
    return {first["op"], second["op"]} in ({">", "≤"}, {"<", "≥"})


def conclusion_outcome(statements, conclusions):
    _, reach, strict, inconsistent = closure(
        statements, (x for c in conclusions for x in (c["left"], c["right"]))
    )
    if inconsistent:
        raise ValueError("Cannot evaluate conclusions from inconsistent statements")
    follows = [relation_true(c, reach, strict) for c in conclusions]
    if follows == [False, False] and is_complementary(*conclusions):
        # The pair is exclusive and exhaustive in every total-order assignment.
        return "EITHER"
    if follows == [True, True]:
        return "BOTH"
    if follows[0]:
        return "ONLY_I"
    if follows[1]:
        return "ONLY_II"
    return "NEITHER"


def statement(left, op, right):
    return {"left": left, "op": op, "right": right}


def claim_signature(claim):
    return f"{claim['left']}{claim['op']}{claim['right']}"


def chain(*tokens):
    """Build constraints from alternating variable/operator tokens."""
    if len(tokens) < 3 or len(tokens) % 2 == 0:
        raise ValueError(f"Malformed chain: {tokens}")
    return [statement(tokens[i], tokens[i + 1], tokens[i + 2]) for i in range(0, len(tokens) - 2, 2)]


def make_claim(question, statements, claim, difficulty, topic, signature, explanation,
               source=None, page=None, source_answer=None, source_wording=None, source_mark=None):
    outcome = classify_claim(statements, claim)
    return {
        "question": question,
        "options": {"A": STATUS_OPTIONS["TRUE"], "B": STATUS_OPTIONS["FALSE"],
                    "C": STATUS_OPTIONS["UNKNOWN"], "D": STATUS_OPTIONS["INCONSISTENT"]},
        "answer": {"TRUE": "A", "FALSE": "B", "UNKNOWN": "C", "INCONSISTENT": "D"}[outcome],
        "expected": outcome, "explanation": explanation, "difficulty": difficulty,
        "topic": topic, "signature": signature, "kind": "claim",
        "statements": statements, "claim": claim, "conclusions": None,
        "verification": f"Strict-aware graph closure classifies {claim_signature(claim)} as {outcome}.",
        "source": source, "page": page, "source_answer": source_answer,
        "source_wording": source_wording, "source_mark": source_mark,
    }


def make_conclusions(question, statements, conclusions, expected, difficulty, topic,
                     signature, explanation, source=None, page=None, source_answer=None,
                     source_wording=None, source_mark=None, include_either=False):
    actual = conclusion_outcome(statements, conclusions)
    if actual != expected:
        raise ValueError(f"Answer mismatch for {signature}: expected {expected}, computed {actual}")
    keys = ["ONLY_I", "ONLY_II", "BOTH", "EITHER"] if include_either else COMMON_FOUR
    options = {chr(65 + i): CONCLUSION_OPTIONS[key] for i, key in enumerate(keys)}
    answer = next(k for k, value in options.items() if value == CONCLUSION_OPTIONS[expected])
    return {
        "question": question, "options": options, "answer": answer, "expected": expected,
        "explanation": explanation, "difficulty": difficulty, "topic": topic,
        "signature": signature, "kind": "conclusions", "statements": statements,
        "claim": None, "conclusions": conclusions,
        "verification": f"Strict-aware graph closure evaluates conclusions as {actual}; either-or is accepted only for a complementary pair.",
        "source": source, "page": page, "source_answer": source_answer,
        "source_wording": source_wording, "source_mark": source_mark,
    }


P1 = chain("T", ">", "M", "≥", "N", "=", "O", ">", "P", "≥", "Q")
P1_TEXT = "T > M ≥ N = O > P ≥ Q"
P1_CLAIMS = [
    ("M", "≥", "P", "easy", "Marked true; handwritten note also states M > P."),
    ("O", ">", "M", "easy", "Marked false."),
    ("Q", "=", "M", "easy", "Marked false."),
    ("T", ">", "O", "easy", "Marked true."),
    ("M", ">", "Q", "easy", "Marked true."),
    ("O", "≥", "Q", "easy", "Handwritten mark is unclear; note appears to assert O > Q."),
    ("N", "=", "Q", "easy", "Marked false."),
    ("T", ">", "Q", "easy", "Marked true."),
    ("P", "<", "T", "easy", "Marked true."),
    ("M", "≥", "Q", "easy", "Marked true."),
    ("N", ">", "O", "medium", "Marked false."),
    ("M", ">", "N", "medium", "Marked false/uncertain; independently this is undetermined."),
    ("T", "=", "M", "medium", "Marked false."),
    ("N", "=", "P", "medium", "Marked false."),
    ("O", "=", "N", "medium", "Marked true."),
]

ITEMS = []
for idx, (a, op, b, difficulty, mark) in enumerate(P1_CLAIMS, 1):
    claim = statement(a, op, b)
    sig = f"source_chain_claim_{idx:02}_{a}_{op}_{b}"
    outcome = classify_claim(P1, claim)
    explanation = {
        "TRUE": f"The chain {P1_TEXT} entails {a} {op} {b}; the strict and non-strict links are preserved in the transitive comparison.",
        "FALSE": f"The chain {P1_TEXT} entails the opposite comparison, so {a} {op} {b} cannot hold.",
        "UNKNOWN": f"The chain establishes only {a} ≥ {b}; equality and strict inequality are both possible, so {a} > {b} is not definite." if (a, op, b) == ("M", ">", "N") else f"The chain {P1_TEXT} does not determine a single truth value for {a} {op} {b}.",
        "INCONSISTENT": "The statements are inconsistent.",
    }[outcome]
    ITEMS.append(make_claim(
        f"Given {P1_TEXT}, what is the status of the claim {a} {op} {b}?",
        P1, claim, difficulty.upper(), "direct_relation", sig, explanation,
        PDF, 5, mark, f"Conclusion {idx}: {a} {op} {b}", mark,
    ))

# Source exercises on pages 6–11. Source-marked choices are retained in the ledger;
# all answer outcomes below are independently recomputed.
ITEMS.extend([
    make_conclusions(
        "Given 1 < 4 ≤ 7 ≤ 3 = 5, assess conclusions I: 4 ≥ 5 and II: 1 < 5.",
        chain("1", "<", "4", "≤", "7", "≤", "3", "=", "5"),
        [statement("4", "≥", "5"), statement("1", "<", "5")], "ONLY_II", "MEDIUM",
        "statement_conclusion", "source_p6_conclusion_only_ii",
        "The chain gives 4 ≤ 5, so 4 ≥ 5 is not entailed. It also gives 1 < 4 ≤ 5, hence 1 < 5 follows.",
        PDF, 6, "B: Only conclusion II is logical.", "1 < 4 ≤ 7 ≤ 3 = 5; I: 4 ≥ 5; II: 1 < 5", "B checked"),
    make_conclusions(
        "Given A ≥ B > C = D and C ≥ P ≥ E < T, assess I: A > E and II: A > T.",
        chain("A", "≥", "B", ">", "C", "=", "D") + chain("C", "≥", "P", "≥", "E") + [statement("E", "<", "T")],
        [statement("A", ">", "E"), statement("A", ">", "T")], "ONLY_I", "MEDIUM",
        "statement_conclusion", "source_p7_handwritten_chain_only_i",
        "A > B > C = D and C ≥ P ≥ E establish A > E. T is only known to exceed E; its relation to A is undetermined, so A > T does not follow.",
        PDF, 7, "Handwritten I checked, II crossed.", "A ≥ B > C = D; C ≥ P ≥ E < T; I: A > E; II: A > T", "I ✓, II ✗"),
    make_conclusions(
        "Given S < C ≤ R = E > A ≥ M, assess I: S < E and II: R > M.",
        chain("S", "<", "C", "≤", "R", "=", "E", ">", "A", "≥", "M"),
        [statement("S", "<", "E"), statement("R", ">", "M")], "BOTH", "MEDIUM",
        "statement_conclusion", "source_p8_both_conclusions",
        "S < C ≤ R = E entails S < E. Also R = E > A ≥ M entails R > M. Both conclusions follow.",
        PDF, 8, "E: Both conclusions are logical.", "S < C ≤ R = E > A ≥ M; I: S < E; II: R > M", "E checked"),
    make_conclusions(
        "Given B ≥ L = K < T = J, assess I: J ≥ B and II: J > L.",
        chain("B", "≥", "L", "=", "K", "<", "T", "=", "J"),
        [statement("J", "≥", "B"), statement("J", ">", "L")], "ONLY_II", "MEDIUM",
        "statement_conclusion", "source_p9_unknown_and_strict_chain",
        "J = T > K = L proves J > L. B ≥ L does not establish whether J ≥ B, so conclusion I is undetermined.",
        PDF, 9, "B: Only conclusion II is correct.", "B ≥ L = K < T = J; I: J ≥ B; II: J > L", "II ✓; I crossed/uncertain"),
    make_conclusions(
        "Given A ≤ M < Y; G < L > A ≥ D > I = N, assess I: G > N and II: L > N.",
        chain("A", "≤", "M", "<", "Y") + chain("G", "<", "L", ">", "A", "≥", "D", ">", "I", "=", "N"),
        [statement("G", ">", "N"), statement("L", ">", "N")], "ONLY_II", "HARD",
        "statement_conclusion", "source_p10_only_ii_disconnected_branch",
        "L > A ≥ D > I = N establishes L > N. G < L alone does not compare G with N, so conclusion I is unknown.",
        PDF, 10, "B: Only conclusion II is logical.", "A ≤ M < Y; G < L > A ≥ D > I = N; I: G > N; II: L > N", "II checked; I crossed"),
    make_conclusions(
        "Given C < R = E ≤ D; D = O < W ≤ N > U ≥ T, assess I: C < W and II: W ≥ T.",
        chain("C", "<", "R", "=", "E", "≤", "D") + chain("D", "=", "O", "<", "W", "≤", "N", ">", "U", "≥", "T"),
        [statement("C", "<", "W"), statement("W", "≥", "T")], "ONLY_I", "HARD",
        "statement_conclusion", "source_p11_equality_and_separate_branch",
        "C < R = E ≤ D = O < W proves C < W. Although N > U ≥ T, W ≤ N does not determine W versus T; II is not entailed.",
        PDF, 11, "A: Only conclusion I is logical.", "C < R = E ≤ D; D = O < W ≤ N > U ≥ T; I: C < W; II: W ≥ T", "I checked; II crossed"),
])

# Nine original questions complete the bank and exercise remaining answer patterns.
ITEMS.extend([
    make_conclusions(
        "Statements: A > B and C > D. Conclusions I: A > C; II: D > A. Which conclusion set follows?",
        [statement("A", ">", "B"), statement("C", ">", "D")],
        [statement("A", ">", "C"), statement("D", ">", "A")], "NEITHER", "MEDIUM",
        "statement_conclusion", "original_disconnected_neither",
        "The two chains are disconnected. Assignments can reverse either proposed cross-chain comparison, so neither conclusion is definitely true.",
        source=None),
    make_conclusions(
        "Statements: X ≥ Y > Z = W. Conclusions I: X > W; II: Y > Z. Which conclusion set follows?",
        chain("X", "≥", "Y", ">", "Z", "=", "W"),
        [statement("X", ">", "W"), statement("Y", ">", "Z")], "BOTH", "HARD",
        "multi_variable_chain", "original_strict_chain_both",
        "X ≥ Y > Z = W makes X > W by transitivity, and Y > Z is a stated strict link. Both follow.",
        source=None),
    make_conclusions(
        "Statements: P > Q ≥ R. Conclusions I: P > R; II: R ≥ P. Which conclusion set follows?",
        chain("P", ">", "Q", "≥", "R"),
        [statement("P", ">", "R"), statement("R", "≥", "P")], "ONLY_I", "HARD",
        "statement_conclusion", "original_strict_vs_nonstrict_only_i",
        "P > Q ≥ R entails P > R. The reverse R ≥ P contradicts this strict ordering, so only I follows.",
        source=None),
    make_conclusions(
        "Statements: A ≥ B > C. Conclusions I: C ≥ A; II: A > C. Which conclusion set follows?",
        chain("A", "≥", "B", ">", "C"),
        [statement("C", "≥", "A"), statement("A", ">", "C")], "ONLY_II", "HARD",
        "statement_conclusion", "original_reverse_contradiction_only_ii",
        "A ≥ B > C entails A > C. C ≥ A is impossible under that strict transitive relation; only II follows.",
        source=None),
    make_conclusions(
        "With no relation given between X and Y, conclusions I: X > Y and II: X ≤ Y form an exhaustive, mutually exclusive pair. What follows?",
        [], [statement("X", ">", "Y"), statement("X", "≤", "Y")], "EITHER", "HARD",
        "either_or_conclusions", "original_complementary_gt_le_either",
        "For any ordered values exactly one of X > Y or X ≤ Y is true. Neither is individually entailed without premises, but the complementary pair is exhaustive and exclusive.",
        source=None, include_either=True),
    make_conclusions(
        "In this coded system, @ means >, # means ≥ and $ means =. Statements: A @ B, B # C, C $ D. Conclusions I: A > D; II: B ≥ D. Which conclusion set follows?",
        [statement("A", ">", "B"), statement("B", "≥", "C"), statement("C", "=", "D")],
        [statement("A", ">", "D"), statement("B", "≥", "D")], "BOTH", "HARD",
        "coded_inequality", "original_coded_gt_ge_eq_both",
        "Decode the symbols: A > B ≥ C = D. Transitivity gives A > D and B ≥ D; both conclusions follow.",
        source=None),
    make_conclusions(
        "In this coded system, ! means <, ~ means ≤ and = means equality. Statements: P ! Q, Q ~ R, R = S. Conclusions I: P < S; II: R > Q. Which conclusion set follows?",
        [statement("P", "<", "Q"), statement("Q", "≤", "R"), statement("R", "=", "S")],
        [statement("P", "<", "S"), statement("R", ">", "Q")], "ONLY_I", "HARD",
        "coded_inequality", "original_coded_lt_le_equal_only_i",
        "Decode as P < Q ≤ R = S, so P < S follows. Q ≤ R permits equality; therefore R > Q is not guaranteed.",
        source=None),
    make_claim(
        "Statements: A > B and C = D. What is the status of the relationship A > C?",
        [statement("A", ">", "B"), statement("C", "=", "D")], statement("A", ">", "C"),
        "HARD", "known_unknown_relationship", "original_disconnected_claim_unknown",
        "A and B form one component, while C = D forms another. Values can satisfy the statements with A > C or A ≤ C, so the relationship cannot be determined.",
        source=None),
    make_conclusions(
        "Statements: L ≥ M > N = O; O > P ≥ Q. Conclusions I: L > P; II: M > Q. Which conclusion set follows?",
        chain("L", "≥", "M", ">", "N", "=", "O", ">", "P", "≥", "Q"),
        [statement("L", ">", "P"), statement("M", ">", "Q")], "BOTH", "HARD",
        "multi_variable_chain", "original_long_chain_strict_links_both",
        "M > N = O > P ≥ Q entails M > P ≥ Q and hence M > Q. Since L ≥ M > P, L > P also follows.",
        source=None),
])


def verify_item(item):
    _, _, _, inconsistent = closure(item["statements"])
    if inconsistent:
        raise ValueError(f"Contradictory statement set in {item['signature']}")
    if item["kind"] == "claim":
        computed = classify_claim(item["statements"], item["claim"])
    else:
        computed = conclusion_outcome(item["statements"], item["conclusions"])
    if computed != item["expected"]:
        raise ValueError(f"Independent verification failed for {item['signature']}: {computed} != {item['expected']}")
    return computed


def build():
    if len(ITEMS) != 30:
        raise ValueError(f"Expected 30 questions, got {len(ITEMS)}")
    levels = Counter(item["difficulty"] for item in ITEMS)
    if levels != {"EASY": 10, "MEDIUM": 10, "HARD": 10}:
        raise ValueError(f"Difficulty distribution mismatch: {dict(levels)}")
    signatures = [item["signature"] for item in ITEMS]
    if len(set(signatures)) != len(signatures):
        raise ValueError("Repeated concept signature")

    rows, ledger = [], []
    for idx, item in enumerate(ITEMS, 1):
        computed = verify_item(item)
        opts = item["options"]
        if set(opts) != set("ABCD") or len({v.casefold().strip() for v in opts.values()}) != 4:
            raise ValueError(f"Question {idx} must have exactly four distinct A-D options")
        answer = item["answer"]
        if answer not in opts:
            raise ValueError(f"Question {idx} has invalid correct-option key")
        if not item["question"].strip() or not item["explanation"].strip():
            raise ValueError(f"Question {idx} is missing text or explanation")
        source = ORIGINAL if item["source"] is None else f"{item['source']}, page {item['page']}; exam/year not stated"
        rows.append({
            "subject_slug": "reasoning", "subcategory_slug": None, "chapter_slug": "inequality",
            "question_text": item["question"], "options": opts, "correct_option": answer,
            "explanation": item["explanation"], "difficulty": item["difficulty"],
            "is_pyq": False, "pyq_year": None, "pyq_exam_name": None, "source": source,
        })
        ledger.append({
            "record_type": "selected_question",
            "question_id": f"inequality-{idx:03}", "row": idx, "chapter_id": CHAPTER_ID,
            "question": item["question"], "topic": item["topic"], "difficulty": item["difficulty"],
            "source_type": "original" if item["source"] is None else "pdf-derived",
            "source_pdf": item["source"], "source_page": item["page"], "source": source,
            "source_answer": item["source_answer"], "source_wording": item["source_wording"],
            "source_mark_review": item["source_mark"], "statements": item["statements"],
            "conclusions": item["conclusions"] or ([item["claim"]] if item["claim"] else []),
            "claim": item["claim"], "expected_outcome": item["expected"],
            "correct_option": answer, "correct_answer": opts[answer],
            "options": opts,
            "explanation": item["explanation"], "independent_verification": item["verification"],
            "concept_signature": item["signature"], "is_pyq": False,
            "validation_status": f"PASS - strict-aware graph closure returned {computed}",
        })

    # The two page-4 chains are teaching examples, not complete assessment items.
    # Preserve their review disposition rather than silently treating them as exercises.
    ledger.extend([
        {
            "record_type": "rejected_source_prompt", "source_pdf": PDF, "source_page": 4,
            "source_wording": "A > B ≥ C = D",
            "rejection_reason": "Instructional illustration only; no task, answer choices, or source answer is specified.",
        },
        {
            "record_type": "rejected_source_prompt", "source_pdf": PDF, "source_page": 4,
            "source_wording": "A > B < C",
            "rejection_reason": "Instructional illustration only; no task, answer choices, or source answer is specified.",
        },
    ])

    (BASE / "data" / "inequality_verified_batch.json").write_text(
        json.dumps({"questions": rows}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (BASE / "data" / "inequality_answer_ledger.json").write_text(
        json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("BUILT", len(rows), dict(levels), "PDF-derived", sum(i["source"] is not None for i in ITEMS),
          "original", sum(i["source"] is None for i in ITEMS), "topics", dict(Counter(i["topic"] for i in ITEMS)))


if __name__ == "__main__":
    build()
