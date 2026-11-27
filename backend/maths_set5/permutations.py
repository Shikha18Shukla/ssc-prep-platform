# -*- coding: utf-8 -*-
"""Permutations — 120 verified questions for the fifth Maths batch."""

from __future__ import annotations

import math
from fractions import Fraction

from .bank import fmt
from .common import build_specs, pair, q, third

SOURCE = "Permutations class notes (local PDFs)"
PAGES = {
    1: "Permuations 01  Class Notes.pdf, pp. 3-4",
    2: "Permuations 01  Class Notes.pdf, pp. 5-15",
}


def F(a, b=1):
    return Fraction(a, b)


def fact(n):
    return math.factorial(n)


def npr(n, r):
    return fact(n) // fact(n - r)


CONTEXTS = ("library shelf", "display rack", "classroom row", "workshop bench", "contest stage")
ITEMS = ("books", "trophies", "files", "tools", "badges")


def p_count_fcp(r, v):
    data = ((3, 4), (4, 5), (5, 6), (6, 7), (7, 8))[v]
    m, n = data
    who, friend = pair(v)
    helper = third(v, 3)
    answer = fmt(m * n)
    return q(
        "p_count_fcp", v,
        f"{who} has {m} choices for a {CONTEXTS[v]} slot and {friend} has {n} "
        f"choices for the next slot. {helper} applies the fundamental counting "
        f"principle. How many ordered pairs are possible?",
        answer,
        [fmt(m + n), fmt(m * n * 2), fmt(m * n + 1)],
        f"For ordered independent choices, multiply: {m} x {n} = {m * n}.",
        {"m": m, "n": n},
    )


def p_distinct_arrangements(r, v):
    counts = (4, 5, 6, 7, 8)[v]
    who, friend = pair(v, 1)
    helper = third(v, 4)
    answer = fmt(fact(counts))
    return q(
        "p_distinct_arrangements", v,
        f"{who}, {friend} and {helper} arrange {counts} distinct {ITEMS[v]} in a "
        f"line on a {CONTEXTS[v]}. How many arrangements are possible?",
        answer,
        [fmt(fact(counts - 1)), fmt(counts * counts), fmt(fact(counts) // 2)],
        f"Arranging {counts} distinct objects in a line gives {counts}! = {fact(counts)}.",
        {"n": counts},
    )


def p_repeated_letters(r, v):
    words = ("LEVEL", "SUCCESS", "BANANA", "BOOKKEEPER", "MISSISSIPPI")
    word = words[v]
    total = len(word)
    denom = (4, 12, 12, 24, 1152)[v]
    answer = fmt(F(fact(total), denom))
    who, friend = pair(v, 2)
    return q(
        "p_repeated_letters", v,
        f"How many distinct letter arrangements can {who} and {friend} make from "
        f"the word {word}?",
        answer,
        [fmt(fact(total)), fmt(F(fact(total), denom * 2)), fmt(F(fact(total), denom // 2 if denom > 1 else 1))],
        f"There are {total} letters with repeated groups. Distinct arrangements = "
        f"{total}! / ({denom}) = {answer}.",
        {"word": word, "n": total, "denom": denom},
    )


def p_word_all_distinct(r, v):
    words = ("PLANK", "QUARTZ", "WINTER", "GOLDEN", "STREAM")[v]
    n = len(words)
    who, friend = pair(v, 3)
    helper = third(v, 5)
    answer = fmt(fact(n))
    return q(
        "p_word_all_distinct", v,
        f"{who}, {friend} and {helper} rearrange every letter of the word {words}. "
        f"How many different words can they form?",
        answer,
        [fmt(fact(n - 1)), fmt(n * n), fmt(fact(n) // n)],
        f"The word {words} has {n} distinct letters, so the number of arrangements "
        f"is {n}! = {fact(n)}.",
        {"word": words, "n": n},
    )


def p_word_repeated(r, v):
    words = ("BALLOON", "CHEMIST", "DIAMOND", "ELEPHANT", "FELLOWSHIP")
    word = words[v]
    n = len(word)
    denom = (4, 1, 2, 2, 2)[v]
    who, friend = pair(v, 4)
    answer = fmt(F(fact(n), denom))
    return q(
        "p_word_repeated", v,
        f"How many distinct arrangements of the letters of {word} are possible? "
        f"{who} and {friend} are checking the repeated letters carefully.",
        answer,
        [fmt(fact(n)), fmt(F(fact(n), 2 * denom)), fmt(F(fact(n - 1), denom))],
        f"There are {n} letters; the repeat factor is {denom}. Distinct arrangements "
        f"= {n}! / {denom} = {answer}.",
        {"word": word, "n": n, "denom": denom},
    )


def p_together_pair(r, v):
    counts = (5, 6, 7, 8, 9)[v]
    who, friend = pair(v, 5)
    helper = third(v, 7)
    answer = fmt(2 * fact(counts - 1))
    return q(
        "p_together_pair", v,
        f"{who}, {friend} and {helper} plus {counts - 2} others are seated in a "
        f"straight row. {who} and {friend} must sit together. How many seating "
        f"arrangements are possible?",
        answer,
        [fmt(fact(counts)), fmt(fact(counts - 1)), fmt(2 * fact(counts))],
        f"Treat the pair as one block: {counts - 1}! arrangements of the block and "
        f"others, times 2 internal orders = {answer}.",
        {"n": counts},
    )


def p_not_together(r, v):
    counts = (5, 6, 7, 8, 9)[v]
    who, friend = pair(v, 6)
    helper = third(v, 8)
    answer = fmt(fact(counts) - 2 * fact(counts - 1))
    return q(
        "p_not_together", v,
        f"{who}, {friend} and {helper} plus {counts - 3} others stand in a row. "
        f"{who} and {friend} must not stand together. How many arrangements are possible?",
        answer,
        [fmt(fact(counts)), fmt(2 * fact(counts - 1)), fmt(fact(counts) - fact(counts - 1))],
        f"Total arrangements {counts}! minus arrangements with the pair together "
        f"2 x {counts - 1}! gives {answer}.",
        {"n": counts},
    )


def p_ends_restriction(r, v):
    counts = (6, 7, 8, 9, 10)[v]
    who, friend = pair(v, 7)
    helper = third(v, 9)
    answer = fmt(2 * fact(counts - 2))
    return q(
        "p_ends_restriction", v,
        f"{counts} people including {who}, {friend} and {helper} line up for a "
        f"photograph. {who} and {friend} must occupy the two ends. How many line-ups "
        f"are possible?",
        answer,
        [fmt(fact(counts)), fmt(fact(counts - 2)), fmt(2 * fact(counts - 1))],
        f"The two ends can be filled by {who} and {friend} in 2 ways; the remaining "
        f"{counts - 2} people can be arranged in {counts - 2}! ways, giving {answer}.",
        {"n": counts},
    )


def p_fixed_position(r, v):
    counts = (5, 6, 7, 8, 9)[v]
    who, friend = pair(v, 8)
    helper = third(v, 10)
    answer = fmt(fact(counts - 2))
    return q(
        "p_fixed_position", v,
        f"{who}, {friend}, {helper} and {counts - 3} others are arranged in a row. "
        f"{who} must be first and {friend} must be last. How many arrangements are possible?",
        answer,
        [fmt(fact(counts)), fmt(fact(counts - 2)), fmt(2 * fact(counts - 2))],
        f"Fix the first and last positions. The remaining {counts - 2} people can "
        f"be arranged in {counts - 2}! = {answer} ways.",
        {"n": counts},
    )


def p_circular_distinct(r, v):
    counts = (5, 6, 7, 8, 9)[v]
    who, friend = pair(v, 9)
    helper = third(v, 11)
    answer = fmt(fact(counts - 1))
    return q(
        "p_circular_distinct", v,
        f"{who}, {friend}, {helper} and {counts - 3} others sit around a circular "
        f"table. How many distinct seatings are possible?",
        answer,
        [fmt(fact(counts)), fmt(fact(counts - 2)), fmt(fact(counts) // counts)],
        f"Circular arrangements of {counts} distinct people = ({counts} - 1)! = "
        f"{answer}; rotations are considered identical.",
        {"n": counts},
    )


def p_circular_pair_together(r, v):
    counts = (6, 7, 8, 9, 10)[v]
    who, friend = pair(v, 10)
    helper = third(v, 12)
    answer = fmt(2 * fact(counts - 2))
    return q(
        "p_circular_pair_together", v,
        f"{who}, {friend}, {helper} and {counts - 3} others sit around a circular "
        f"table. {who} and {friend} must sit together. How many seatings are possible?",
        answer,
        [fmt(fact(counts - 1)), fmt(fact(counts - 2)), fmt(2 * fact(counts - 1))],
        f"Treat the pair as one block. Around a circle, {counts - 1} units give "
        f"{counts - 2}! arrangements, and the pair has 2 internal orders: {answer}.",
        {"n": counts},
    )


def p_arrange_selected(r, v):
    data = ((7, 3), (8, 4), (9, 4), (10, 5), (11, 5))[v]
    n, rsel = data
    who, friend = pair(v, 11)
    helper = third(v, 13)
    answer = fmt(npr(n, rsel))
    return q(
        "p_arrange_selected", v,
        f"From {n} distinct {ITEMS[v]}, {who}, {friend} and {helper} choose {rsel} "
        f"and arrange them in an order. How many ordered arrangements are possible?",
        answer,
        [fmt(math.comb(n, rsel)), fmt(npr(n, rsel - 1)), fmt(npr(n, rsel) // 2)],
        f"Ordered selection of {rsel} from {n} is nPr = {n}P{rsel} = {answer}.",
        {"n": n, "r": rsel},
    )


def p_three_digit_no_repeat(r, v):
    digits = ("12345", "23456", "34567", "45678", "56789")[v]
    who, friend = pair(v, 12)
    helper = third(v, 14)
    answer = fmt(npr(len(digits), 3))
    return q(
        "p_three_digit_no_repeat", v,
        f"Using only the digits {digits}, {who}, {friend} and {helper} form three-digit "
        f"numbers without repetition. How many numbers can be formed?",
        answer,
        [fmt(math.comb(len(digits), 3)), fmt(npr(len(digits), 2)), fmt(npr(len(digits), 3) // 2)],
        f"Three positions filled from {len(digits)} distinct digits without repetition: "
        f"{len(digits)}P3 = {answer}.",
        {"d": digits, "r": 3},
    )


def p_even_numbers(r, v):
    digit_sets = ("123456", "234567", "345678", "456789", "123478")[v]
    who, friend = pair(v, 13)
    helper = third(v, 15)
    evens = sum(1 for ch in digit_sets if int(ch) % 2 == 0)
    rest = len(digit_sets) - 1
    answer = fmt(evens * npr(rest, 3))
    return q(
        "p_even_numbers", v,
        f"{who}, {friend} and {helper} form four-digit numbers from the digits "
        f"{digit_sets} without repetition. How many are even?",
        answer,
        [fmt(npr(len(digit_sets), 4) // 2), fmt(evens * npr(rest, 2)), fmt(evens * npr(rest, 3) // 2)],
        f"The units place must be even: {evens} choices. The other three places use "
        f"the remaining {rest} digits in {rest}P3 = {npr(rest, 3)} orders, so {answer}.",
        {"d": digit_sets, "even": evens},
    )


def p_odd_numbers(r, v):
    digit_sets = ("12345", "23456", "34567", "45678", "56789")[v]
    who, friend = pair(v, 14)
    helper = third(v, 16)
    odds = sum(1 for ch in digit_sets if int(ch) % 2 == 1)
    rest = len(digit_sets) - 1
    answer = fmt(odds * npr(rest, 3))
    return q(
        "p_odd_numbers", v,
        f"Using each digit at most once, {who}, {friend} and {helper} make four-digit "
        f"numbers from {digit_sets}. How many are odd?",
        answer,
        [fmt(npr(len(digit_sets), 4) // 2), fmt(odds * npr(rest, 2)), fmt(odds * npr(rest, 3) // 2)],
        f"The last digit must be odd: {odds} choices. The first three positions can "
        f"be filled from the remaining {rest} digits in {rest}P3 = {npr(rest, 3)} ways, giving {answer}.",
        {"d": digit_sets, "odd": odds},
    )


def p_divisible_by_five(r, v):
    digit_sets = ("12345", "23456", "34567", "45678", "56789")[v]
    who, friend = pair(v, 15)
    helper = third(v, 17)
    fives = sum(1 for ch in digit_sets if ch in "05")
    rest = len(digit_sets) - 1
    answer = fmt(fives * npr(rest, 3))
    return q(
        "p_divisible_by_five", v,
        f"{who}, {friend} and {helper} form four-digit numbers from {digit_sets} "
        f"without repeating a digit. How many are divisible by 5?",
        answer,
        [fmt(npr(len(digit_sets), 4) // 5), fmt(fives * npr(rest, 2)), fmt(fives * npr(rest, 3) // 2)],
        f"A number divisible by 5 ends in 0 or 5. Here there are {fives} such choices, "
        f"and the remaining three places can be filled in {rest}P3 = {npr(rest, 3)} ways: {answer}.",
        {"d": digit_sets, "fives": fives},
    )


def p_vowels_together(r, v):
    words = ("QUEUE", "GROUP", "AUDIO", "OILER", "HOUSE")[v]
    vowel_counts = (4, 2, 4, 3, 3)[v]
    cons_counts = len(words) - vowel_counts
    denom = (4 if v == 0 else 1)
    answer = fmt(F(fact(cons_counts + 1) * fact(vowel_counts), denom))
    who, friend = pair(v, 16)
    return q(
        "p_vowels_together", v,
        f"How many arrangements of the letters of {word_or(words, v)} keep all vowels "
        f"together? {who} and {friend} are checking the vowel block.",
        answer,
        [fmt(fact(len(words))), fmt(fact(cons_counts + 1)), fmt(F(fact(cons_counts + 1) * fact(vowel_counts), 2 * denom))],
        f"Treat the {vowel_counts} vowels as one block. There are {cons_counts + 1} "
        f"objects to arrange and {vowel_counts}! internal vowel orders, adjusted for "
        f"repeats, giving {answer}.",
        {"word": words, "v": vowel_counts, "c": cons_counts, "denom": denom},
    )


def word_or(word, variant):
    return word


def p_vowels_not_together(r, v):
    words = ("PLANE", "QUICK", "STORM", "BREAD", "CLOUD")[v]
    vowel_counts = (2, 2, 1, 2, 2)[v]
    cons_counts = len(words) - vowel_counts
    denom = 1
    total = fact(len(words))
    together = fact(cons_counts + 1) * fact(vowel_counts)
    if vowel_counts == 1:
        together = 0
    answer_num = total - together
    who, friend = pair(v, 17)
    helper = third(v, 19)
    return q(
        "p_vowels_not_together", v,
        f"{who}, {friend} and {helper} rearrange the distinct letters of {words}. "
        f"How many arrangements have no two vowels adjacent?",
        answer_num if answer_num >= 0 else 0,
        [fmt(together), fmt(total), fmt(max(total - together // 2, 0))],
        f"Total arrangements are {len(words)}! = {total}. Arrangements with vowels "
        f"together are {together}. The difference is {answer_num}.",
        {"word": words, "n": len(words), "together": together},
    )


def p_consonants_together(r, v):
    word = ("CANOPY", "MEADOW", "SILENT", "FLOWER", "VIOLIN")[v]
    vowels = "AEIOU"
    cons = [ch for ch in word if ch not in vowels]
    vowel_list = [ch for ch in word if ch in vowels]
    from collections import Counter
    cons_repeat = 1
    for count in Counter(cons).values():
        cons_repeat *= fact(count)
    vowel_repeat = 1
    for count in Counter(vowel_list).values():
        vowel_repeat *= fact(count)
    cons_counts, vowel_counts = len(cons), len(vowel_list)
    together = F(fact(vowel_counts + 1) * fact(cons_counts), cons_repeat * vowel_repeat)
    answer = fmt(together)
    who, friend = pair(v, 18)
    return q(
        "p_consonants_together", v,
        f"How many distinct arrangements of the letters of {word} keep all "
        f"consonants together? {who} and {friend} are counting the consonant block.",
        answer,
        [fmt(fact(len(word))), fmt(fact(vowel_counts + 1)), fmt(together / 2)],
        f"Treat the {cons_counts} consonants as one block, giving {vowel_counts + 1} "
        f"objects and {cons_counts}! internal orders, divided by the repeat factors "
        f"{cons_repeat} and {vowel_repeat}: {answer}.",
        {"word": word, "c": cons_counts, "v": vowel_counts},
    )


def p_pair_never_adjacent(r, v):
    counts = (7, 8, 9, 10, 11)[v]
    who, friend = pair(v, 19)
    helper = third(v, 20)
    total = fact(counts)
    adjacent = 2 * fact(counts - 1)
    answer = fmt(total - adjacent)
    return q(
        "p_pair_never_adjacent", v,
        f"{who}, {friend}, {helper} and {counts - 3} others stand in a row. In how "
        f"many ways can they stand so that {who} and {friend} are not adjacent?",
        answer,
        [fmt(total), fmt(adjacent), fmt(total - fact(counts - 1))],
        f"Subtract arrangements with the pair adjacent (2 x {counts - 1}!) from all "
        f"{counts}! arrangements: {answer}.",
        {"n": counts},
    )


def p_circular_pair_not_together(r, v):
    counts = (6, 7, 8, 9, 10)[v]
    who, friend = pair(v, 19)
    helper = third(v, 21)
    total = fact(counts - 1)
    adjacent = 2 * fact(counts - 2)
    answer = fmt(total - adjacent)
    return q(
        "p_circular_pair_not_together", v,
        f"{who}, {friend}, {helper} and {counts - 3} others sit around a circular "
        f"table. {who} and {friend} must not sit together. How many seatings are possible?",
        answer,
        [fmt(total), fmt(adjacent), fmt(total - fact(counts - 2))],
        f"Total circular seatings are ({counts} - 1)! = {total}. Treating the pair as "
        f"a block gives 2 x ({counts} - 2)! = {adjacent} forbidden seatings, so the "
        f"answer is {answer}.",
        {"n": counts},
    )


def p_rank_word(r, v):
    words = ("BIRD", "CARD", "DARK", "EARTH", "FAITH")[v]
    letters = sorted(words)
    total_letters = len(letters)
    rank = 1
    for pos, ch in enumerate(words):
        smaller = sum(1 for c in letters if c < ch)
        remaining = total_letters - pos - 1
        rank += smaller * math.factorial(remaining)
        letters.remove(ch)
    who, friend = pair(v, 20)
    helper = third(v, 21)
    answer = fmt(rank)
    return q(
        "p_rank_word", v,
        f"{who}, {friend} and {helper} list all alphabetical arrangements of the "
        f"distinct letters of {words}. What is the dictionary rank of {words}?",
        answer,
        [fmt(rank - 1), fmt(rank + 1), fmt(rank // 2)],
        f"Counting arrangements that begin with a smaller available letter at each "
        f"position gives dictionary rank {rank}.",
        {"word": words, "rank": rank},
    )


def p_committee_chair(r, v):
    data = ((8, 4), (9, 5), (10, 5), (11, 6), (12, 6))[v]
    n, k = data
    who, friend = pair(v, 21)
    helper = third(v, 22)
    answer = fmt(math.comb(n, k) * k)
    return q(
        "p_committee_chair", v,
        f"A group has {n} members including {who}, {friend} and {helper}. {who} "
        f"selects a committee of {k} and then chooses one of them as chair. How many "
        f"committee-and-chair outcomes are possible?",
        answer,
        [fmt(math.comb(n, k)), fmt(npr(n, k)), fmt(math.comb(n, k) * (k - 1))],
        f"Choose the committee in {math.comb(n, k)} ways and its chair in {k} ways: "
        f"{answer}.",
        {"n": n, "k": k},
    )


def p_password_pattern(r, v):
    data = ((4, 6), (5, 6), (4, 8), (5, 8), (6, 6))[v]
    letters_n, digits_n = data
    who, friend = pair(v, 22)
    helper = third(v, 23)
    answer = fmt(26 ** letters_n * 10 ** digits_n)
    return q(
        "p_password_pattern", v,
        f"{who} designs a code with {letters_n} lowercase letters followed by "
        f"{digits_n} digits. Repetition is allowed. {friend} asks {helper} how many "
        f"codes are possible. Find the count.",
        answer,
        [fmt(26 * letters_n + 10 * digits_n), fmt(26 ** letters_n * 9 ** digits_n), fmt(26 ** (letters_n - 1) * 10 ** digits_n)],
        f"Each letter position has 26 choices and each digit position has 10 choices. "
        f"Total codes = 26^{letters_n} x 10^{digits_n} = {answer}.",
        {"L": letters_n, "D": digits_n},
    )


FAMILIES = (
    p_count_fcp,
    p_distinct_arrangements,
    p_repeated_letters,
    p_word_all_distinct,
    p_word_repeated,
    p_together_pair,
    p_not_together,
    p_ends_restriction,
    p_fixed_position,
    p_circular_distinct,
    p_circular_pair_together,
    p_arrange_selected,
    p_three_digit_no_repeat,
    p_even_numbers,
    p_odd_numbers,
    p_divisible_by_five,
    p_vowels_together,
    p_vowels_not_together,
    p_consonants_together,
    p_pair_never_adjacent,
    p_circular_pair_not_together,
    p_rank_word,
    p_committee_chair,
    p_password_pattern,
)


def build_permutations():
    return build_specs(FAMILIES)
