# -*- coding: utf-8 -*-
"""Combinations — 120 verified questions for the fifth Maths batch."""

from __future__ import annotations

import math
from fractions import Fraction

from .bank import fmt
from .common import build_specs, pair, q, third

SOURCE = "Combinations class notes (local PDFs)"
PAGES = {
    1: "Combinations 01  Class Notes.pdf, pp. 3-4",
    2: "Combinations 01  Class Notes.pdf, pp. 5-11",
}


def F(a, b=1):
    Fraction(a, b)
    return Fraction(a, b)


CONTEXTS = ("committee", "project team", "selection panel", "sports squad", "review board")


def c_basic(r, v):
    data = ((7, 3), (8, 4), (9, 4), (10, 5), (11, 5))[v]
    n, k = data
    who, friend = pair(v)
    helper = third(v, 3)
    answer = fmt(math.comb(n, k))
    return q(
        "c_basic", v,
        f"From {n} candidates, {who}, {friend} and {helper} choose {k} for a "
        f"{CONTEXTS[v]}. How many selections are possible?",
        answer,
        [fmt(n * k), fmt(math.factorial(n) // math.factorial(n - k)), fmt(math.comb(n, k - 1))],
        f"Order does not matter, so use nCr: C({n}, {k}) = {answer}.",
        {"n": n, "k": k},
    )


def c_exactly_groups(r, v):
    data = ((5, 4, 2, 2), (6, 5, 3, 2), (7, 6, 3, 3), (8, 7, 4, 3), (9, 8, 4, 4))[v]
    men, women, msel, wsel = data
    who, friend = pair(v, 1)
    helper = third(v, 4)
    answer = fmt(math.comb(men, msel) * math.comb(women, wsel))
    return q(
        "c_exactly_groups", v,
        f"A {CONTEXTS[v]} is formed from {men} men and {women} women. {who}, "
        f"{friend} and {helper} require exactly {msel} men and {wsel} women. How many "
        f"committees are possible?",
        answer,
        [fmt(math.comb(men + women, msel + wsel)), fmt(math.comb(men, msel)), fmt(math.comb(women, wsel))],
        f"Choose men and women independently: C({men}, {msel}) x C({women}, {wsel}) "
        f"= {answer}.",
        {"a": men, "b": women, "r": msel, "s": wsel},
    )


def c_at_least_one(r, v):
    data = ((5, 4, 2, 1), (6, 5, 3, 1), (7, 5, 3, 2), (8, 6, 4, 2), (9, 7, 4, 3))[v]
    group_a, group_b, total, min_a = data
    answer = sum(math.comb(group_a, a) * math.comb(group_b, total - a) for a in range(min_a, min(group_a, total) + 1))
    who, friend = pair(v, 2)
    helper = third(v, 5)
    return q(
        "c_at_least_one", v,
        f"A {CONTEXTS[v]} of {total} people is chosen from {group_a} managers and "
        f"{group_b} engineers. {who}, {friend} and {helper} require at least "
        f"{min_a} managers. How many committees are possible?",
        answer,
        [fmt(math.comb(group_a + group_b, total)), fmt(math.comb(group_a, min_a)), fmt(math.comb(group_b, total - min_a))],
        f"Sum the valid cases for {min_a} or more managers from the first group: "
        f"{answer}.",
        {"a": group_a, "b": group_b, "n": total, "m": min_a},
    )


def c_at_most_one(r, v):
    data = ((4, 6, 3), (5, 7, 4), (6, 8, 4), (7, 9, 5), (8, 10, 5))[v]
    special, others, total = data
    answer = math.comb(others, total) + math.comb(special, 1) * math.comb(others, total - 1)
    who, friend = pair(v, 3)
    helper = third(v, 6)
    return q(
        "c_at_most_one", v,
        f"{who}, {friend} and {helper} choose a {CONTEXTS[v]} of {total} from "
        f"{special} special members and {others} other members, with at most one "
        f"special member. How many selections are possible?",
        answer,
        [fmt(math.comb(special + others, total)), fmt(math.comb(others, total)), fmt(math.comb(special, 1) * math.comb(others, total - 1) * 2)],
        f"Case 1 chooses no special member; case 2 chooses exactly one. Total = "
        f"{answer}.",
        {"s": special, "o": others, "n": total},
    )


def c_particular_included(r, v):
    data = ((9, 4), (10, 5), (11, 5), (12, 6), (13, 6))[v]
    n, k = data
    who, friend = pair(v, 4)
    helper = third(v, 7)
    answer = fmt(math.comb(n - 1, k - 1))
    return q(
        "c_particular_included", v,
        f"{who} must be on a {CONTEXTS[v]} of {k} chosen from {n} people. {friend} "
        f"and {helper} fix that condition. How many committees are possible?",
        answer,
        [fmt(math.comb(n, k)), fmt(math.comb(n - 1, k)), fmt(math.comb(n - 2, k - 1))],
        f"Include {who} first, then choose the remaining {k - 1} from {n - 1}: "
        f"C({n - 1}, {k - 1}) = {answer}.",
        {"n": n, "k": k},
    )


def c_particular_excluded(r, v):
    data = ((9, 4), (10, 5), (11, 5), (12, 6), (13, 6))[v]
    n, k = data
    who, friend = pair(v, 5)
    helper = third(v, 8)
    answer = fmt(math.comb(n - 1, k))
    return q(
        "c_particular_excluded", v,
        f"{who} is not eligible for a {CONTEXTS[v]} of {k} chosen from {n} people. "
        f"{friend} and {helper} apply that restriction. How many committees are possible?",
        answer,
        [fmt(math.comb(n, k)), fmt(math.comb(n - 1, k - 1)), fmt(math.comb(n - 2, k))],
        f"Remove {who} from consideration, then choose {k} from {n - 1}: "
        f"C({n - 1}, {k}) = {answer}.",
        {"n": n, "k": k},
    )


def c_include_exclude(r, v):
    data = ((10, 4), (11, 5), (12, 5), (13, 6), (14, 6))[v]
    n, k = data
    who, friend = pair(v, 6)
    helper = third(v, 9)
    answer = fmt(math.comb(n - 2, k - 1))
    return q(
        "c_include_exclude", v,
        f"A {CONTEXTS[v]} of {k} is chosen from {n} people. {who} must be included "
        f"and {friend} must be excluded. {helper} confirms the conditions. How many "
        f"committees are possible?",
        answer,
        [fmt(math.comb(n - 1, k - 1)), fmt(math.comb(n - 1, k)), fmt(math.comb(n - 2, k - 2))],
        f"Include {who} and remove {friend}, leaving {n - 2} people from whom "
        f"{k - 1} are chosen: {answer}.",
        {"n": n, "k": k},
    )


def c_team_from_groups(r, v):
    data = ((4, 5, 3, 2), (5, 6, 3, 3), (6, 7, 4, 3), (7, 8, 4, 4), (8, 9, 5, 4))[v]
    a, b, ra, rb = data
    who, friend = pair(v, 7)
    helper = third(v, 10)
    answer = fmt(math.comb(a, ra) * math.comb(b, rb))
    return q(
        "c_team_from_groups", v,
        f"A {CONTEXTS[v]} draws {ra} from a group of {a} and {rb} from a group of "
        f"{b}. {who}, {friend} and {helper} count the possible teams. How many are there?",
        answer,
        [fmt(math.comb(a + b, ra + rb)), fmt(math.comb(a, ra)), fmt(math.comb(b, rb))],
        f"The two groups are chosen independently: C({a}, {ra}) x C({b}, {rb}) = "
        f"{answer}.",
        {"a": a, "b": b, "r": ra, "s": rb},
    )


def c_cards(r, v):
    data = ((4, 2, 3), (5, 2, 4), (5, 3, 3), (6, 2, 5), (6, 3, 4))[v]
    reds, blacks, total = data
    who, friend = pair(v, 8)
    helper = third(v, 11)
    answer = sum(math.comb(reds, r) * math.comb(blacks, total - r) for r in range(2, min(reds, total) + 1))
    return q(
        "c_cards", v,
        f"From {reds} red cards and {blacks} black cards, {who}, {friend} and "
        f"{helper} choose {total} cards with at least two red cards. How many "
        f"selections are possible?",
        answer,
        [fmt(math.comb(reds + blacks, total)), fmt(math.comb(reds, 2)), fmt(math.comb(blacks, total - 2))],
        f"Add cases with 2 or more red cards: {answer}.",
        {"r": reds, "b": blacks, "n": total},
    )


def c_relation_pr_comb(r, v):
    data = ((6, 3), (7, 3), (8, 4), (9, 4), (10, 5))[v]
    n, k = data
    who, friend = pair(v, 9)
    helper = third(v, 12)
    answer = fmt(math.factorial(k))
    return q(
        "c_relation_pr_comb", v,
        f"{who} knows that P({n}, {k}) = C({n}, {k}) x k!. {friend} asks {helper} "
        f"for the value of k!. Find it.",
        answer,
        [fmt(n - k), fmt(math.factorial(n)), fmt(math.factorial(k - 1))],
        f"Here k = {k}, so k! = {answer}.",
        {"k": k},
    )


def c_select_then_arrange(r, v):
    data = ((7, 3), (8, 4), (9, 4), (10, 5), (11, 5))[v]
    n, k = data
    who, friend = pair(v, 10)
    helper = third(v, 13)
    answer = fmt(math.comb(n, k) * math.factorial(k))
    return q(
        "c_select_then_arrange", v,
        f"{who}, {friend} and {helper} choose {k} of {n} {CONTEXTS[v]} members and "
        f"then assign them to {k} distinct slots. How many outcomes are possible?",
        answer,
        [fmt(math.comb(n, k)), fmt(n * k), fmt(math.factorial(n))],
        f"Choose the group in C({n}, {k}) ways and assign slots in {k}! ways: "
        f"{answer}.",
        {"n": n, "k": k},
    )


def c_assign_roles(r, v):
    data = ((8, 3), (9, 3), (10, 4), (11, 4), (12, 5))[v]
    n, roles = data
    who, friend = pair(v, 11)
    helper = third(v, 14)
    answer = fmt(math.comb(n, roles) * math.factorial(roles))
    return q(
        "c_assign_roles", v,
        f"A {CONTEXTS[v]} of {roles} people is chosen from {n} candidates and each "
        f"gets a different role. {who}, {friend} and {helper} count the outcomes. "
        f"Find the count.",
        answer,
        [fmt(math.comb(n, roles)), fmt(n * roles), fmt(math.comb(n, roles) * math.factorial(roles - 1))],
        f"Select {roles} people, then permute the {roles} roles: C({n}, {roles}) x "
        f"{roles}! = {answer}.",
        {"n": n, "k": roles},
    )


def c_complement(r, v):
    data = ((10, 4, 3), (11, 5, 4), (12, 5, 4), (13, 6, 5), (14, 6, 5))[v]
    n, k, blocked = data
    who, friend = pair(v, 13)
    helper = third(v, 16)
    answer = fmt(math.comb(n - blocked, k))
    return q(
        "c_complement", v,
        f"A {CONTEXTS[v]} of {k} is chosen from {n} people, but {blocked} people "
        f"decline to serve. {who}, {friend} and {helper} count valid committees. "
        f"How many are possible?",
        answer,
        [fmt(math.comb(n, k)), fmt(math.comb(n - blocked, k - 1)), fmt(math.comb(blocked, 1) * math.comb(n - blocked, k - 1))],
        f"Only {n - blocked} people are available, so C({n - blocked}, {k}) = "
        f"{answer}.",
        {"n": n, "k": k, "b": blocked},
    )


def c_question_selection(r, v):
    data = ((6, 5, 3, 2), (7, 6, 4, 2), (8, 6, 4, 3), (9, 7, 5, 3), (10, 8, 5, 4))[v]
    a, b, ra, rb = data
    who, friend = pair(v, 12)
    helper = third(v, 15)
    answer = fmt(math.comb(a, ra) * math.comb(b, rb))
    return q(
        "c_question_selection", v,
        f"A test paper has {a} easy and {b} hard questions. {who}, {friend} and "
        f"{helper} must select {ra} easy and {rb} hard questions. How many papers "
        f"can be formed?",
        answer,
        [fmt(math.comb(a + b, ra + rb)), fmt(math.comb(a, ra)), fmt(math.comb(b, rb))],
        f"Select easy and hard questions separately: C({a}, {ra}) x C({b}, {rb}) "
        f"= {answer}.",
        {"a": a, "b": b, "r": ra, "s": rb},
    )


def c_diag_handshake(r, v):
    counts = (5, 6, 7, 8, 9)[v]
    who, friend = pair(v, 13)
    helper = third(v, 16)
    answer = fmt(math.comb(counts, 2))
    return q(
        "c_diag_handshake", v,
        f"{who}, {friend}, {helper} and {counts - 3} others meet at a {CONTEXTS[v]}. "
        f"If every pair exchanges one handshake, how many handshakes occur?",
        answer,
        [fmt(counts * (counts - 1)), fmt(math.comb(counts, 2) // 2), fmt(counts * 2)],
        f"Each handshake is a pair, so C({counts}, 2) = {answer}.",
        {"n": counts},
    )


def c_diag_polygon(r, v):
    sides = (5, 6, 7, 8, 9)[v]
    who, friend = pair(v, 14)
    helper = third(v, 17)
    answer = fmt(math.comb(sides, 2) - sides)
    return q(
        "c_diag_polygon", v,
        f"{who}, {friend} and {helper} draw a polygon with {sides} sides. How many "
        f"diagonals does it have?",
        answer,
        [fmt(math.comb(sides, 2)), fmt(sides * (sides - 2)), fmt(math.comb(sides - 1, 2))],
        f"All vertex pairs give C({sides}, 2) segments; subtract the {sides} sides "
        f"to get {answer} diagonals.",
        {"n": sides},
    )


def c_at_most_from_group(r, v):
    data = ((4, 6, 3, 1), (5, 7, 4, 2), (6, 8, 4, 2), (7, 9, 5, 3), (8, 10, 5, 3))[v]
    a, b, total, max_a = data
    answer = sum(math.comb(a, r) * math.comb(b, total - r) for r in range(0, min(a, max_a) + 1))
    who, friend = pair(v, 15)
    helper = third(v, 18)
    return q(
        "c_at_most_from_group", v,
        f"A {CONTEXTS[v]} of {total} is chosen from {a} senior and {b} junior "
        f"members, with at most {max_a} seniors. {who}, {friend} and {helper} count "
        f"the committees. How many are possible?",
        answer,
        [fmt(math.comb(a + b, total)), fmt(math.comb(a, max_a)), fmt(math.comb(b, total))],
        f"Sum cases with 0 through {max_a} seniors: {answer}.",
        {"a": a, "b": b, "n": total, "m": max_a},
    )


def c_multi_step_sum(r, v):
    data = ((4, 5, 6, 3), (5, 6, 7, 4), (6, 7, 8, 4), (7, 8, 9, 5), (8, 9, 10, 5))[v]
    a, b, c, total = data
    answer = sum(
        math.comb(a, i) * math.comb(b, j) * math.comb(c, total - i - j)
        for i in range(a + 1)
        for j in range(b + 1)
        if 0 <= total - i - j <= c
    )
    who, friend = pair(v, 16)
    helper = third(v, 19)
    return q(
        "c_multi_step_sum", v,
        f"A {CONTEXTS[v]} of {total} is chosen from {a} traders, {b} accountants "
        f"and {c} engineers. {who}, {friend} and {helper} allow any mix. How many "
        f"committees are possible?",
        answer,
        [fmt(math.comb(a + b + c, total)), fmt(math.comb(a + b, total)), fmt(math.comb(b + c, total))],
        f"All committee members come from {a + b + c} distinct people, so the "
        f"answer is C({a + b + c}, {total}) = {answer}.",
        {"a": a, "b": b, "c": c, "n": total},
    )


def c_exactly_two_special(r, v):
    data = ((5, 7, 3), (6, 8, 4), (7, 9, 4), (8, 10, 5), (9, 11, 5))[v]
    special, others, total = data
    answer = fmt(math.comb(special, 2) * math.comb(others, total - 2))
    who, friend = pair(v, 17)
    helper = third(v, 20)
    return q(
        "c_exactly_two_special", v,
        f"From {special} special members and {others} other members, {who}, "
        f"{friend} and {helper} choose a {CONTEXTS[v]} of {total} with exactly two "
        f"special members. How many committees are possible?",
        answer,
        [fmt(math.comb(special + others, total)), fmt(math.comb(special, 2)), fmt(math.comb(others, total - 2))],
        f"Choose the two special members and the remaining {total - 2} others: "
        f"{answer}.",
        {"s": special, "o": others, "n": total},
    )


def c_no_adjacent_seats(r, v):
    counts = (5, 6, 7, 8, 9)[v]
    who, friend = pair(v, 18)
    helper = third(v, 21)
    answer = fmt(math.comb(counts - 1, 2))
    return q(
        "c_no_adjacent_seats", v,
        f"There are {counts} seats in a row. {who}, {friend} and {helper} choose two "
        f"seats that are not adjacent. How many choices are possible?",
        answer,
        [fmt(math.comb(counts, 2)), fmt(counts - 1), fmt(math.comb(counts, 2) - counts)],
        f"Total pairs C({counts}, 2) minus the {counts - 1} adjacent pairs gives "
        f"C({counts - 1}, 2) = {answer}.",
        {"n": counts},
    )


def c_distribute_identical(r, v):
    data = ((7, 3), (8, 3), (9, 4), (10, 4), (11, 5))[v]
    n, groups = data
    answer = fmt(math.comb(n - 1, groups - 1))
    who, friend = pair(v, 19)
    helper = third(v, 22)
    return q(
        "c_distribute_identical", v,
        f"{who} has {n} identical tokens to split into {groups} non-empty bundles "
        f"for {friend}, {helper} and the others. How many splits are possible?",
        answer,
        [fmt(math.comb(n, groups)), fmt(math.comb(n - 1, groups)), fmt(math.comb(n + groups - 1, groups - 1))],
        f"Stars and bars gives C(n - 1, groups - 1) = C({n - 1}, {groups - 1}) = "
        f"{answer}.",
        {"n": n, "g": groups},
    )


def c_pair_grouping(r, v):
    pairs = (3, 4, 5, 6, 7)[v]
    total = 2 * pairs
    answer = fmt(math.factorial(total) // (2 ** pairs * math.factorial(pairs)))
    who, friend = pair(v, 20)
    helper = third(v, 23)
    return q(
        "c_pair_grouping", v,
        f"{who}, {friend}, {helper} and the others split {total} people into "
        f"{pairs} unnamed pairs for a {CONTEXTS[v]}. How many pairings are possible?",
        answer,
        [fmt(math.factorial(total)), fmt(math.comb(total, 2) ** pairs), fmt(answer * 2)],
        f"Divide {total}! by 2 for each internal pair order and by {pairs}! for the "
        f"unnamed pairs: {answer}.",
        {"p": pairs},
    )


FAMILIES = (
    c_basic,
    c_exactly_groups,
    c_at_least_one,
    c_at_most_one,
    c_particular_included,
    c_particular_excluded,
    c_include_exclude,
    c_team_from_groups,
    c_cards,
    c_relation_pr_comb,
    c_select_then_arrange,
    c_assign_roles,
    c_complement,
    c_question_selection,
    c_diag_handshake,
    c_diag_polygon,
    c_at_most_from_group,
    c_multi_step_sum,
    c_exactly_two_special,
    c_no_adjacent_seats,
    c_distribute_identical,
    c_pair_grouping,
)

# Fill the remaining two slots with additional mixed-application patterns.
def c_letter_selection(r, v):
    data = ((5, 3), (6, 4), (7, 4), (8, 5), (9, 5))[v]
    n, k = data
    who, friend = pair(v, 21)
    helper = third(v, 24)
    answer = fmt(math.comb(n, k) + math.comb(n, k - 1))
    return q(
        "c_letter_selection", v,
        f"A {CONTEXTS[v]} may choose {k} from {n} blue files or {k - 1} from those "
        f"same files plus one red file. {who}, {friend} and {helper} count the "
        f"selections. How many are possible?",
        answer,
        [fmt(math.comb(n, k)), fmt(math.comb(n + 1, k)), fmt(math.comb(n, k - 1))],
        f"Add the two disjoint cases: C({n}, {k}) + C({n}, {k - 1}) = {answer}.",
        {"n": n, "k": k},
    )


def c_multi_committee(r, v):
    data = ((4, 4, 2, 2), (5, 5, 2, 3), (6, 5, 3, 2), (6, 6, 3, 3), (7, 6, 3, 4))[v]
    a, b, ra, rb = data
    who, friend = pair(v, 22)
    helper = third(v, 25)
    answer = fmt(math.comb(a, ra) * math.comb(b, rb))
    return q(
        "c_multi_committee", v,
        f"A {CONTEXTS[v]} needs {ra} members from one pool of {a} and {rb} from "
        f"another of {b}. {who}, {friend} and {helper} count all possible teams. "
        f"How many are there?",
        answer,
        [fmt(math.comb(a + b, ra + rb)), fmt(math.comb(a, ra)), fmt(math.comb(b, rb) * 2)],
        f"Choose from each pool independently: C({a}, {ra}) x C({b}, {rb}) = "
        f"{answer}.",
        {"a": a, "b": b, "r": ra, "s": rb},
    )


FAMILIES = FAMILIES + (c_letter_selection, c_multi_committee)


def build_combinations():
    return build_specs(FAMILIES)
