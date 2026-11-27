# -*- coding: utf-8 -*-
"""Problems on Age - 120 verified questions for the third Maths batch."""

from __future__ import annotations

from fractions import Fraction

from .bank import fmt, near_ints

SOURCE = "Problems on Age class notes and topic-wise sets (local PDFs)"
PAGES = {
    1: "Problems on Age 01_Class Notes, pp. 1-15",
    2: "Problems on Age 02_Class Notes, pp. 1-17",
    3: "Problems on Age 03_Class Notes, pp. 1-13",
    4: "Problems on Ages, pp. 1-208",
}

NAMES = [
    ("Amit", "Ravi"), ("Sunita", "Kavita"), ("Rahul", "Ankit"),
    ("Pooja", "Neha"), ("Vikas", "Sanjay"), ("Meena", "Reena"),
    ("Arun", "Kiran"), ("Sonia", "Divya"), ("Naveen", "Prakash"),
    ("Lata", "Gita"),
]


def pair(v, offset=0):
    return NAMES[(v + offset) % len(NAMES)]


def q(family, variant, text, answer, distractors, explanation, inputs):
    return {
        "text": text,
        "correct": str(answer),
        "distractors": [str(d) for d in distractors],
        "explanation": explanation,
        "verification_data": {"family": family, "variant": variant, "inputs": inputs},
    }


def age_ratio_present(r, v):
    a, b = pair(v)
    ratio_a, ratio_b, total = r.choice([(2, 3, 50), (3, 4, 70), (4, 5, 90), (5, 7, 96)])
    k = Fraction(total, ratio_a + ratio_b)
    assert k.denominator == 1
    answer = ratio_a * k.numerator
    text = (
        f"The present ages of {a} and {b} are in the ratio {ratio_a}:{ratio_b} "
        f"and their total age is {total} years. How old is {a}?"
    )
    return q(
        "age_ratio_present", v, text, answer, near_ints(answer, r, 6),
        f"Let ages be {ratio_a}k and {ratio_b}k. Then {ratio_a+ratio_b}k = {total}, k = {k.numerator}, so {a}'s age = {answer}.",
        {"A": ratio_a, "B": ratio_b, "Total": total, "Asked": "A", "Age": answer},
    )


def age_after_years_ratio(r, v):
    a, b = pair(v, 1)
    presets = [(20, 30, 10, 3, 4), (18, 28, 8, 13, 18), (24, 36, 12, 3, 4)]
    x, y, n, ra, rb = presets[v % len(presets)]
    assert Fraction(x + n, y + n) == Fraction(ra, rb)
    text = (
        f"{a} is {x} years old and {b} is {y} years old. After {n} years, "
        "what will be the ratio of their ages?"
    )
    answer = f"{ra}:{rb}"
    return q(
        "age_after_years_ratio", v, text, answer,
        [f"{rb}:{ra}", f"{x}:{y}", f"{ra+1}:{rb}"],
        f"After {n} years their ages are {x+n} and {y+n}; ratio = {answer}.",
        {"X": x, "Y": y, "N": n, "Ratio": answer},
    )


def age_before_years_ratio(r, v):
    a, b = pair(v, 2)
    presets = [(20, 30, 5, 3, 5), (25, 40, 10, 1, 2), (18, 27, 3, 5, 8)]
    x, y, n, ra, rb = presets[v % len(presets)]
    assert Fraction(x - n, y - n) == Fraction(ra, rb)
    answer = f"{ra}:{rb}"
    text = (
        f"{a} is {x} and {b} is {y} years old today. What was the ratio of "
        f"their ages {n} years ago?"
    )
    return q(
        "age_before_years_ratio", v, text, answer,
        [f"{rb}:{ra}", f"{x}:{y}", f"{ra}:{rb+1}"],
        f"{n} years ago their ages were {x-n} and {y-n}; ratio = {answer}.",
        {"X": x, "Y": y, "N": n, "Ratio": answer},
    )


def age_difference(r, v):
    a, b = pair(v, 3)
    ra, rb, diff = r.choice([(2, 5, 18), (3, 7, 20), (4, 9, 25), (5, 8, 18)])
    k = Fraction(diff, rb - ra)
    assert k.denominator == 1
    answer = rb * k.numerator
    text = (
        f"The ages of {a} and {b} are in the ratio {ra}:{rb}. Their age "
        f"difference is {diff} years. How old is the elder one?"
    )
    return q(
        "age_difference", v, text, answer, near_ints(answer, r, 6),
        f"Difference = ({rb}-{ra})k = {diff}, so k = {k.numerator}; elder age = {answer}.",
        {"A": ra, "B": rb, "Diff": diff, "Asked": "elder", "Age": answer},
    )


def age_father_son_sum(r, v):
    father, son = pair(v, 4)
    ra, rb, total = r.choice([(4, 1, 50), (5, 2, 56), (3, 1, 48), (6, 1, 63)])
    k = Fraction(total, ra + rb)
    assert k.denominator == 1
    answer = ra * k.numerator
    text = (
        f"The ages of {father} and his son {son} are in the ratio {ra}:{rb}. "
        f"The sum of their ages is {total}. Find {father}'s present age."
    )
    return q(
        "age_father_son_sum", v, text, answer, near_ints(answer, r, 6),
        f"Let ages be {ra}k and {rb}k; {ra+rb}k = {total}, k = {k.numerator}; father's age = {answer}.",
        {"A": ra, "B": rb, "Total": total, "Asked": "A", "Age": answer},
    )


def age_mother_daughter(r, v):
    mother, daughter = pair(v, 5)
    presets = [(42, 18, 24), (50, 20, 30), (36, 12, 24), (45, 15, 30)]
    m, d, diff = presets[v % len(presets)]
    answer = diff
    text = (
        f"{mother} is {m} years old and her daughter {daughter} is {d} years "
        "old. How many years older is the mother?"
    )
    return q(
        "age_mother_daughter", v, text, answer, near_ints(answer, r, 4),
        f"Age difference stays constant: {m} - {d} = {answer} years.",
        {"M": m, "D": d, "Diff": diff},
    )


def age_brother_sister_future(r, v):
    brother, sister = pair(v, 6)
    presets = [(15, 10, 20), (20, 12, 28), (18, 14, 30), (22, 16, 34), (25, 18, 40)]
    x, y, target = presets[v % len(presets)]
    n = target - x
    answer = x + n
    text = (
        f"{brother} is {x} and {sister} is {y} years old. In how many years "
        f"will {brother} be {target} years old?"
    )
    return q(
        "age_brother_sister_future", v, text, n, near_ints(n, r, 3),
        f"{brother} needs to reach {target}; years required = {target} - {x} = {n}.",
        {"X": x, "Target": target, "N": n},
    )


def age_family_average(r, v):
    presets = [(32, 30, 8, 34), (40, 36, 10, 42), (28, 24, 6, 30)]
    a, b, child, avg = presets[v % len(presets)]
    father, mother = pair(v)
    total = 3 * avg
    answer = total - a - b
    text = (
        f"The average age of {father}, {mother} and their child is {avg} years. "
        f"The parents are {a} and {b} years old. Find the child's age."
    )
    return q(
        "age_family_average", v, text, answer, near_ints(answer, r, 4),
        f"Total age = 3 x {avg} = {total}; child's age = {total} - {a} - {b} = {answer}.",
        {"A": a, "B": b, "Avg": avg, "Child": answer},
    )


def age_father_at_birth(r, v):
    father, son = pair(v, 7)
    presets = [(45, 15), (52, 22), (38, 8), (60, 30), (42, 12)]
    f, s = presets[v % len(presets)]
    answer = f - s
    text = (
        f"{father} is {f} and {son} is {s} years old now. How old was "
        f"{father} when {son} was born?"
    )
    return q(
        "age_father_at_birth", v, text, answer, near_ints(answer, r, 4),
        f"At {son}'s birth, {father}'s age = {f} - {s} = {answer}.",
        {"F": f, "S": s, "Diff": answer},
    )


def age_grandparent(r, v):
    presets = [(60, 30, 10, 2), (70, 35, 5, 2), (64, 16, 4, 4)]
    g, p, n, target = presets[v % len(presets)]
    grandparent, parent = pair(v + 1)
    answer = f"{g+n}:{p+n}"
    text = (
        f"{grandparent} is {g} and {parent} is {p} years old. What will be "
        f"the ratio of their ages after {n} years?"
    )
    return q(
        "age_grandparent", v, text, answer,
        [f"{p+n}:{g+n}", f"{g}:{p}", f"{g+n+1}:{p+n}"],
        f"Ages become {g+n} and {p+n}; ratio = {answer}.",
        {"G": g, "P": p, "N": n, "Ratio": answer},
    )


def age_husband_wife(r, v):
    h, w = pair(v, 8)
    ra, rb, diff = r.choice([(5, 4, 8), (7, 6, 6), (9, 7, 10), (4, 3, 9)])
    k = Fraction(diff, ra - rb)
    assert k.denominator == 1
    answer = rb * k.numerator
    text = (
        f"The ages of {h} and {w} are in the ratio {ra}:{rb}. If {h} is "
        f"{diff} years older, how old is {w}?"
    )
    return q(
        "age_husband_wife", v, text, answer, near_ints(answer, r, 5),
        f"Difference = ({ra}-{rb})k = {diff}, k = {k.numerator}; {w}'s age = {answer}.",
        {"A": ra, "B": rb, "Diff": diff, "Asked": "B", "Age": answer},
    )


def age_three_people(r, v):
    a, b, c = ["A", "B", "C"]
    ra, rb, rc, total = r.choice([(1, 2, 3, 60), (2, 3, 4, 72), (3, 4, 5, 96)])
    k = Fraction(total, ra + rb + rc)
    assert k.denominator == 1
    answer = rc * k.numerator
    first, second = pair(v)
    third = pair(v + 5)[1]
    text = (
        f"{first}, {second} and {third} have ages in the ratio {ra}:{rb}:{rc}. Their total "
        f"age is {total} years. What is the age of the oldest?"
    )
    return q(
        "age_three_people", v, text, answer, near_ints(answer, r, 7),
        f"Sum of ratio parts = {ra+rb+rc}; k = {k.numerator}; oldest = {answer}.",
        {"A": ra, "B": rb, "C": rc, "Total": total, "Asked": "C", "Age": answer},
    )


def age_double_after(r, v):
    a, b = pair(v, 9)
    presets = [(14, 4, 6, 2), (22, 7, 8, 2), (30, 10, 10, 2), (40, 16, 8, 2), (26, 11, 4, 2)]
    x, y, n, target = presets[v % len(presets)]
    assert x + n == target * (y + n)
    answer = n
    text = (
        f"{a} is {x} and {b} is {y} years old. After how many years will "
        f"{a} be {target} times as old as {b}?"
    )
    return q(
        "age_double_after", v, text, answer, near_ints(answer, r, 3),
        f"After {n} years, ages are {x+n} and {y+n}; {x+n} = {target} x {y+n}.",
        {"X": x, "Y": y, "Target": target, "N": n},
    )


def age_half_before(r, v):
    a, b = pair(v, 1)
    presets = [(30, 20, 10, 2), (40, 25, 10, 2), (50, 30, 10, 2),
               (36, 24, 12, 2), (44, 28, 12, 2)]
    x, y, n, target = presets[v % len(presets)]
    assert x - n == target * (y - n)
    answer = n
    text = (
        f"{a} is {x} and {b} is {y} years old. How many years ago was "
        f"{a} {target} times as old as {b}?"
    )
    return q(
        "age_half_before", v, text, answer, near_ints(answer, r, 3),
        f"{n} years ago the ages were {x-n} and {y-n}; the required multiple is {target}.",
        {"X": x, "Y": y, "Target": target, "N": n},
    )


def age_sum_after(r, v):
    presets = [(25, 18, 7, 57), (32, 24, 5, 66), (40, 30, 10, 90), (28, 20, 6, 60)]
    x, y, n, total = presets[v % len(presets)]
    first, second = pair(v + 2)
    answer = x + y + 2 * n
    assert answer == total
    text = (
        f"{first} and {second} are {x} and {y} years old. What will be the sum of their "
        f"ages after {n} years?"
    )
    return q(
        "age_sum_after", v, text, answer, near_ints(answer, r, 6),
        f"Each gains {n} years, so sum = {x}+{y}+2 x {n} = {answer}.",
        {"X": x, "Y": y, "N": n, "Sum": answer},
    )


def age_diff_after(r, v):
    a, b = pair(v, 2)
    presets = [(35, 22, 12), (48, 30, 20), (29, 17, 8), (60, 45, 15), (41, 26, 9)]
    x, y, n = presets[v % len(presets)]
    answer = x - y
    text = (
        f"{a} is {x} and {b} is {y} years old. What will be the difference "
        f"in their ages after {n} years?"
    )
    return q(
        "age_diff_after", v, text, answer, near_ints(answer, r, 4),
        f"Age difference never changes: {x} - {y} = {answer}.",
        {"X": x, "Y": y, "N": n, "Diff": answer},
    )


def age_ratio_change(r, v):
    import math
    presets = [(30, 20, 10, 40, 30), (24, 16, 8, 32, 24), (45, 30, 15, 60, 45),
               (18, 12, 6, 28, 22), (50, 35, 10, 65, 50)]
    x, y, n, nx, ny = presets[v % len(presets)]
    g = math.gcd(nx, ny)
    answer = f"{nx // g}:{ny // g}"
    first, second = pair(v, 8)
    text = (
        f"The present ages of {first} and {second} are in the ratio {x}:{y}. "
        f"After {n} years they will be {nx} and {ny}. What is the new ratio?"
    )
    return q(
        "age_ratio_change", v, text, answer,
        [f"{ny}:{nx}", f"{x}:{y}", f"{nx+1}:{ny}"],
        f"New ages are {nx} and {ny}; ratio = {answer}.",
        {"NX": nx, "NY": ny, "Ratio": answer},
    )


def age_average_family_future(r, v):
    presets = [(30, 28, 8, 6, 28), (40, 35, 15, 10, 40), (25, 23, 6, 4, 22),
               (36, 30, 12, 9, 35), (45, 39, 15, 12, 45)]
    a, b, c, n, avg = presets[v % len(presets)]
    father, mother = pair(v + 3)
    answer = (a + b + c + 3 * n) // 3
    assert answer == avg
    text = (
        f"A family of three — {father}, {mother} and a child — has present ages "
        f"{a}, {b} and {c}. What will their "
        f"average age be after {n} years?"
    )
    return q(
        "age_average_family_future", v, text, answer, near_ints(answer, r, 4),
        f"Each gains {n} years, so average rises by {n}: ({a}+{b}+{c})/3 + {n} = {answer}.",
        {"A": a, "B": b, "C": c, "N": n, "Avg": answer},
    )


def age_son_from_father_future(r, v):
    father, son = pair(v, 3)
    presets = [(40, 10, 10, 20), (50, 15, 10, 25), (36, 6, 12, 18), (60, 20, 5, 25)]
    f, s, n, target = presets[v % len(presets)]
    answer = s + n
    assert answer == target
    text = (
        f"{father} is {f} and {son} is {s} years old. How old will {son} be "
        f"when {father} is {f + n}?"
    )
    return q(
        "age_son_from_father_future", v, text, answer, near_ints(answer, r, 4),
        f"After {n} years {father} is {f+n}; {son}'s age = {s}+{n} = {answer}.",
        {"F": f, "S": s, "N": n, "TargetSon": answer},
    )


def age_cousin(r, v):
    a, b = pair(v, 4)
    presets = [(18, 24, 6), (22, 30, 8), (14, 21, 7), (27, 36, 9), (31, 40, 9)]
    x, y, diff = presets[v % len(presets)]
    answer = diff
    text = (
        f"{a} is {x} years old and cousin {b} is {y} years old. What is the "
        "difference in their ages?"
    )
    return q(
        "age_cousin", v, text, answer, near_ints(answer, r, 4),
        f"Difference = {y} - {x} = {answer} years.",
        {"X": x, "Y": y, "Diff": answer},
    )


def age_teacher_student(r, v):
    teacher, student = pair(v, 5)
    presets = [(36, 12, 24), (44, 16, 28), (30, 10, 20), (50, 25, 25), (42, 14, 28)]
    t, s, diff = presets[v % len(presets)]
    answer = diff
    text = (
        f"{teacher}, a teacher, is {t} years old and {student}, a student, is {s} "
        "years old. How many years older is the teacher?"
    )
    return q(
        "age_teacher_student", v, text, answer, near_ints(answer, r, 4),
        f"The constant difference is {t} - {s} = {answer} years.",
        {"T": t, "S": s, "Diff": answer},
    )


def age_friend_ratio(r, v):
    a, b = pair(v, 6)
    ra, rb, total = r.choice([(4, 5, 45), (5, 6, 66), (3, 8, 55), (7, 9, 80)])
    k = Fraction(total, ra + rb)
    assert k.denominator == 1
    answer = rb * k.numerator
    text = (
        f"The ratio of the ages of two friends {a} and {b} is {ra}:{rb}. "
        f"Their combined age is {total}. How old is the older friend?"
    )
    return q(
        "age_friend_ratio", v, text, answer, near_ints(answer, r, 6),
        f"k = {total}/({ra}+{rb}) = {k.numerator}; older age = {answer}.",
        {"A": ra, "B": rb, "Total": total, "Asked": "B", "Age": answer},
    )


def age_product(r, v):
    presets = [(6, 12, 72), (8, 14, 112), (9, 15, 135), (10, 18, 180), (12, 20, 240)]
    x, y, product = presets[v % len(presets)]
    answer = product
    first, second = pair(v, 9)
    text = (
        f"The siblings {first} and {second} are {x} and {y} years old. What is "
        "the product of their present ages?"
    )
    return q(
        "age_product", v, text, answer, near_ints(answer, r, 10),
        f"Product = {x} x {y} = {answer}.",
        {"X": x, "Y": y, "Product": answer},
    )


def age_compare(r, v):
    a, b = pair(v, 7)
    presets = [(20, 28), (35, 29), (44, 44), (17, 23), (52, 48)]
    x, y = presets[v % len(presets)]
    answer = "First person" if x > y else "Second person" if y > x else "Both are equal"
    options = ["First person", "Second person", "Both are equal", "Cannot be determined"]
    return {
        "text": f"{a} is {x} years old and {b} is {y} years old. Who is older?",
        "correct": answer,
        "distractors": [o for o in options if o != answer],
        "explanation": f"Comparing {x} and {y}: {answer}.",
        "verification_data": {
            "family": "age_compare", "variant": v,
            "inputs": {"X": x, "Y": y, "Answer": answer},
        },
    }


FAMILIES = [
    age_ratio_present, age_after_years_ratio, age_before_years_ratio,
    age_difference, age_father_son_sum, age_mother_daughter,
    age_brother_sister_future, age_family_average, age_father_at_birth,
    age_grandparent, age_husband_wife, age_three_people, age_double_after,
    age_half_before, age_sum_after, age_diff_after, age_ratio_change,
    age_average_family_future, age_son_from_father_future, age_cousin,
    age_teacher_student, age_friend_ratio, age_product, age_compare,
]


def build_problems_on_age():
    spec = []
    for index, fn in enumerate(FAMILIES):
        part = 1 if index < 3 else 2 if index < 7 else 3 if index < 13 else 4
        difficulty = "EASY" if index < 7 else "MEDIUM" if index < 19 else "HARD"
        for variant in range(5):
            spec.append((part, difficulty, lambda r, f=fn, v=variant: f(r, v), (index % 4) + 1))
    return spec
