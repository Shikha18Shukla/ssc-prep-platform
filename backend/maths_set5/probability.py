# -*- coding: utf-8 -*-
"""Probability — 120 verified questions for the fifth Maths batch."""

from __future__ import annotations

import math
from fractions import Fraction

from .bank import fmt
from .common import build_specs, pair, q, third

SOURCE = "Probability class notes (local PDFs)"
PAGES = {
    1: "Probability 01  Class Notes.pdf, pp. 4-17",
    2: "7e88503c-399d-41ec-81d4-e2a199287a4e.pdf, pp. 4-12",
}


def F(a, b=1):
    return Fraction(a, b)


def near_fracs(value: Fraction):
    return [fmt(value / 2), fmt(value * 2), fmt(value + F(1, 6))]


def prob_basic_coin(r, v):
    coins = (1, 2, 3, 4, 5)[v]
    who, friend = pair(v)
    helper = third(v, 3)
    answer = F(1, 2)
    return q(
        "prob_basic_coin", v,
        f"{who} tosses {coins} fair coin(s) once; {friend} asks {helper} for the "
        f"probability of getting a head on a single toss. Find it.",
        answer,
        near_fracs(answer),
        f"A fair coin has one head among two equally likely outcomes, so the "
        f"probability is 1/2.",
        {"coins": coins},
    )


def prob_die_face(r, v):
    faces = (2, 3, 4, 5, 6)[v]
    who, friend = pair(v, 1)
    helper = third(v, 4)
    answer = F(1, 6)
    return q(
        "prob_die_face", v,
        f"{who} rolls a fair six-sided die and asks {friend} and {helper} for the "
        f"probability that the upper face is exactly {faces}. Find it.",
        answer,
        near_fracs(answer),
        f"One favourable face out of six equally likely faces gives 1/6.",
        {"face": faces},
    )


def prob_die_even(r, v):
    sides = (5, 6, 7, 8, 9)[v]
    favourable = sides // 2
    who, friend = pair(v, 2)
    helper = third(v, 5)
    answer = F(favourable, sides)
    return q(
        "prob_die_even", v,
        f"A fair die has {sides} equally likely faces numbered 1 to {sides}. "
        f"{who}, {friend} and {helper} need the probability of an even-numbered face. "
        f"Find it.",
        answer,
        near_fracs(answer),
        f"There are {favourable} even faces among {sides} faces, so the probability "
        f"is {fmt(answer)}.",
        {"n": sides, "f": favourable},
    )


def prob_two_dice_sum(r, v):
    targets = (7, 8, 9, 10, 11)[v]
    counts = {7: 6, 8: 5, 9: 4, 10: 3, 11: 2}
    favourable = counts[targets]
    who, friend = pair(v, 3)
    helper = third(v, 6)
    answer = F(favourable, 36)
    return q(
        "prob_two_dice_sum", v,
        f"{who} and {friend} roll two fair dice and {helper} records the sum. What "
        f"is the probability that the sum is {targets}?",
        answer,
        near_fracs(answer),
        f"There are 36 ordered outcomes. A sum of {targets} occurs in {favourable} "
        f"ways, so the probability is {fmt(answer)}.",
        {"sum": targets},
    )


def prob_doublet(r, v):
    sides = (6, 6, 8, 10, 12)[v]
    who, friend = pair(v, 4)
    helper = third(v, 7)
    answer = F(sides, sides * sides)
    return q(
        "prob_doublet", v,
        f"{who}, {friend} and {helper} roll two fair dice numbered 1 to {sides}. "
        f"What is the probability of a doublet?",
        answer,
        near_fracs(answer),
        f"There are {sides} doublets among {sides}^2 ordered outcomes, giving "
        f"{fmt(answer)}.",
        {"n": sides},
    )


def prob_card_suit(r, v):
    suits = ("spades", "hearts", "diamonds", "clubs", "red suits")[v]
    favourable = 13 if v < 4 else 26
    who, friend = pair(v, 5)
    helper = third(v, 8)
    answer = F(favourable, 52)
    return q(
        "prob_card_suit", v,
        f"A well-shuffled standard deck has 52 cards. {who}, {friend} and {helper} "
        f"draw one card. What is the probability that it belongs to {suits}?",
        answer,
        near_fracs(answer),
        f"There are {favourable} favourable cards out of 52, so the probability is "
        f"{fmt(answer)}.",
        {"f": favourable},
    )


def prob_card_face(r, v):
    counts = (12, 4, 16, 20, 26)[v]
    who, friend = pair(v, 6)
    helper = third(v, 9)
    answer = F(counts, 52)
    return q(
        "prob_card_face", v,
        f"From a standard 52-card deck, {who}, {friend} and {helper} draw one card. "
        f"What is the probability that it is one of {counts} specified cards?",
        answer,
        near_fracs(answer),
        f"The specified set has {counts} cards among 52, so the probability is "
        f"{fmt(answer)}.",
        {"f": counts},
    )


def prob_balls_bag(r, v):
    data = ((4, 6, "blue"), (5, 7, "red"), (6, 8, "green"), (7, 9, "yellow"), (8, 10, "white"))[v]
    a, b, colour = data
    who, friend = pair(v, 7)
    helper = third(v, 10)
    answer = F(a, a + b)
    return q(
        "prob_balls_bag", v,
        f"A bag holds {a} {colour} balls and {b} other balls. {who}, {friend} and "
        f"{helper} draw one ball at random. What is the probability that it is {colour}?",
        answer,
        near_fracs(answer),
        f"Favourable balls = {a}; total balls = {a + b}; probability = {fmt(answer)}.",
        {"a": a, "b": b},
    )


def prob_two_same_without(r, v):
    data = ((4, 5), (5, 6), (6, 7), (7, 8), (8, 9))[v]
    a, b = data
    who, friend = pair(v, 8)
    helper = third(v, 11)
    total = a + b
    answer = F(a * (a - 1) + b * (b - 1), total * (total - 1))
    return q(
        "prob_two_same_without", v,
        f"A bag has {a} red and {b} blue balls. {who}, {friend} and {helper} draw two "
        f"balls without replacement. What is the probability that both have the same colour?",
        answer,
        near_fracs(answer),
        f"Favourable ordered pairs = {a}x{a - 1} + {b}x{b - 1}; total ordered pairs "
        f"= {total}x{total - 1}; probability = {fmt(answer)}.",
        {"a": a, "b": b},
    )


def prob_two_different_without(r, v):
    data = ((4, 5), (5, 6), (6, 7), (7, 8), (8, 9))[v]
    a, b = data
    who, friend = pair(v, 9)
    helper = third(v, 12)
    total = a + b
    answer = F(2 * a * b, total * (total - 1))
    return q(
        "prob_two_different_without", v,
        f"A box has {a} red pens and {b} blue pens. {who}, {friend} and {helper} pick "
        f"two pens without replacement. What is the probability that the colours differ?",
        answer,
        near_fracs(answer),
        f"Ordered favourable pairs = 2x{a}x{b}; total ordered pairs = {total}x"
        f"{total - 1}; probability = {fmt(answer)}.",
        {"a": a, "b": b},
    )


def prob_complement(r, v):
    data = ((4, 6), (5, 7), (6, 8), (7, 9), (8, 10))[v]
    a, b = data
    who, friend = pair(v, 10)
    helper = third(v, 13)
    total = a + b
    answer = 1 - F(a, total)
    return q(
        "prob_complement", v,
        f"A bag has {a} green and {b} non-green balls. {who}, {friend} and {helper} "
        f"draw one ball. What is the probability that it is not green?",
        answer,
        near_fracs(F(b, total)),
        f"Use the complement: 1 - P(green) = 1 - {fmt(F(a, total))} = {fmt(answer)}.",
        {"a": a, "b": b},
    )


def prob_independent_both(r, v):
    data = ((2, 3), (3, 4), (4, 5), (5, 6), (6, 7))[v]
    a, b = data
    who, friend = pair(v, 11)
    helper = third(v, 14)
    answer = F(1, a * b)
    return q(
        "prob_independent_both", v,
        f"{who} has a 1-in-{a} chance of solving a problem and {friend} has a "
        f"1-in-{b} chance, independently. {helper} asks for the probability that both "
        f"solve it. Find it.",
        answer,
        near_fracs(answer),
        f"For independent events, multiply probabilities: 1/{a} x 1/{b} = {fmt(answer)}.",
        {"a": a, "b": b},
    )


def prob_independent_at_least_one(r, v):
    data = ((2, 3), (3, 4), (4, 5), (5, 6), (6, 7))[v]
    a, b = data
    who, friend = pair(v, 12)
    helper = third(v, 15)
    answer = 1 - F(a - 1, a) * F(b - 1, b)
    return q(
        "prob_independent_at_least_one", v,
        f"{who} solves a problem with probability 1/{a} and {friend} solves it with "
        f"probability 1/{b}, independently. {helper} asks for the probability that at "
        f"least one solves it. Find it.",
        answer,
        near_fracs(1 - answer),
        f"Use the complement: 1 - (1 - 1/{a})(1 - 1/{b}) = {fmt(answer)}.",
        {"a": a, "b": b},
    )


def prob_conditional_without(r, v):
    data = ((5, 4), (6, 5), (7, 6), (8, 7), (9, 8))[v]
    red, blue = data
    who, friend = pair(v, 13)
    helper = third(v, 16)
    answer = F(red - 1, red + blue - 1)
    return q(
        "prob_conditional_without", v,
        f"A bag has {red} red and {blue} blue balls. {who} draws a red ball and does "
        f"not replace it. {friend} then draws one ball; {helper} asks for the "
        f"probability that it is red. Find it.",
        answer,
        near_fracs(answer),
        f"After removing one red ball, {red - 1} red balls remain among "
        f"{red + blue - 1} total balls, so the probability is {fmt(answer)}.",
        {"r": red, "b": blue},
    )


def prob_conditional_table(r, v):
    data = ((10, 6, 4), (12, 7, 5), (15, 9, 6), (18, 10, 8), (20, 12, 8))[v]
    total, a, both = data
    who, friend = pair(v, 14)
    helper = third(v, 17)
    answer = F(both, a)
    return q(
        "prob_conditional_table", v,
        f"In a group of {total} people, {a} are eligible and {both} of those eligible "
        f"are chosen. {who}, {friend} and {helper} pick an eligible person at random. "
        f"What is the probability that the person was chosen?",
        answer,
        near_fracs(answer),
        f"Restrict the sample space to the {a} eligible people; {both} were chosen, "
        f"so the conditional probability is {fmt(answer)}.",
        {"t": total, "a": a, "b": both},
    )


def prob_committee_count(r, v):
    data = ((6, 4, 3), (7, 5, 4), (8, 5, 4), (9, 6, 5), (10, 7, 5))[v]
    men, women, k = data
    who, friend = pair(v, 15)
    helper = third(v, 18)
    favourable = math.comb(men, k)
    total = math.comb(men + women, k)
    answer = F(favourable, total)
    return q(
        "prob_committee_count", v,
        f"A committee of {k} is chosen from {men} men and {women} women. {who}, "
        f"{friend} and {helper} ask for the probability that all members are men. "
        f"Find it.",
        answer,
        near_fracs(answer),
        f"Favourable committees = C({men}, {k}); total = C({men + women}, {k}); "
        f"probability = {fmt(answer)}.",
        {"m": men, "w": women, "k": k},
    )


def prob_coin_exact_heads(r, v):
    tosses, heads = ((3, 1), (4, 2), (5, 2), (5, 3), (6, 3))[v]
    favourable = math.comb(tosses, heads)
    answer = F(favourable, 2 ** tosses)
    who, friend = pair(v, 16)
    helper = third(v, 19)
    return q(
        "prob_coin_exact_heads", v,
        f"{who} tosses a fair coin {tosses} times. {friend} and {helper} ask for the "
        f"probability of getting exactly {heads} heads. Find it.",
        answer,
        near_fracs(answer),
        f"Favourable sequences = C({tosses}, {heads}) = {favourable}; total sequences "
        f"= 2^{tosses}; probability = {fmt(answer)}.",
        {"n": tosses, "k": heads},
    )


def prob_coin_at_least_head(r, v):
    tosses = (2, 3, 4, 5, 6)[v]
    answer = 1 - F(1, 2 ** tosses)
    who, friend = pair(v, 17)
    helper = third(v, 20)
    return q(
        "prob_coin_at_least_head", v,
        f"{who}, {friend} and {helper} toss a fair coin {tosses} times. What is the "
        f"probability of getting at least one head?",
        answer,
        near_fracs(answer),
        f"Complement of no heads is 1 - 1/2^{tosses} = {fmt(answer)}.",
        {"n": tosses},
    )


def prob_die_multiple(r, v):
    sides, multiple = ((6, 2), (6, 3), (10, 2), (12, 3), (20, 4))[v]
    favourable = sides // multiple
    who, friend = pair(v, 18)
    helper = third(v, 21)
    answer = F(favourable, sides)
    return q(
        "prob_die_multiple", v,
        f"A fair die has faces 1 to {sides}. {who}, {friend} and {helper} ask for the "
        f"probability of a face divisible by {multiple}. Find it.",
        answer,
        near_fracs(answer),
        f"There are {favourable} multiples of {multiple} among {sides} faces, so "
        f"the probability is {fmt(answer)}.",
        {"n": sides, "m": multiple},
    )


def prob_card_ace_king(r, v):
    counts = (4, 8, 12, 16, 20)[v]
    who, friend = pair(v, 19)
    helper = third(v, 22)
    answer = F(counts, 52)
    return q(
        "prob_card_ace_king", v,
        f"From a standard 52-card deck, {who}, {friend} and {helper} draw one card. "
        f"What is the probability that it belongs to a specified set of {counts} cards?",
        answer,
        near_fracs(answer),
        f"Favourable cards = {counts}; total cards = 52; probability = {fmt(answer)}.",
        {"f": counts},
    )


def prob_two_dice_product_even(r, v):
    who, friend = pair(v, 20)
    helper = third(v, 23)
    answer = F(3, 4)
    return q(
        "prob_two_dice_product_even", v,
        f"{who}, {friend} and {helper} roll two fair dice. What is the probability "
        f"that the product of the two upper faces is even?",
        answer,
        near_fracs(answer),
        f"The product is odd only when both faces are odd: probability 1/4. Hence "
        f"P(even product) = 1 - 1/4 = 3/4.",
        {"n": 6},
    )


def prob_bag_transfer(r, v):
    data = ((3, 4, 2), (4, 5, 3), (5, 6, 3), (6, 7, 4), (7, 8, 5))[v]
    red, blue, moved = data
    who, friend = pair(v, 21)
    helper = third(v, 24)
    answer = F(red, red + blue)
    return q(
        "prob_bag_transfer", v,
        f"A bag has {red} red and {blue} blue balls. {who}, {friend} and {helper} "
        f"note the probability of drawing red. Then {moved} balls are set aside "
        f"without anyone seeing their colours. What was the original probability?",
        answer,
        near_fracs(answer),
        f"The original probability depends only on the initial composition: "
        f"{red}/({red} + {blue}) = {fmt(answer)}.",
        {"r": red, "b": blue, "m": moved},
    )


def prob_combination_or(r, v):
    data = ((5, 4, 2), (6, 5, 3), (7, 5, 3), (8, 6, 4), (9, 7, 4))[v]
    a, b, k = data
    who, friend = pair(v, 22)
    helper = third(v, 25)
    total = math.comb(a + b, k)
    favourable = total - math.comb(a, k) - math.comb(b, k)
    answer = F(favourable, total)
    return q(
        "prob_combination_or", v,
        f"A group of {k} is chosen from {a} architects and {b} bankers. {who}, "
        f"{friend} and {helper} ask for the probability that the group contains at "
        f"least one from each profession. Find it.",
        answer,
        near_fracs(answer),
        f"Favourable = total committees minus all-architect and all-banker "
        f"committees = {favourable}; total = {total}; probability = {fmt(answer)}.",
        {"a": a, "b": b, "k": k},
    )


def prob_die_less_than(r, v):
    limits = (3, 4, 5, 6, 7)[v]
    sides = max(6, limits)
    favourable = min(limits - 1, sides)
    who, friend = pair(v, 23)
    helper = third(v, 26)
    answer = F(favourable, sides)
    return q(
        "prob_die_less_than", v,
        f"A fair die has faces 1 to {sides}. {who}, {friend} and {helper} ask for the "
        f"probability that the face is less than {limits}. Find it.",
        answer,
        near_fracs(answer),
        f"The favourable faces are 1 through {favourable}, so the probability is "
        f"{fmt(answer)}.",
        {"n": sides, "limit": limits},
    )


FAMILIES = (
    prob_basic_coin,
    prob_die_face,
    prob_die_even,
    prob_two_dice_sum,
    prob_doublet,
    prob_card_suit,
    prob_card_face,
    prob_balls_bag,
    prob_two_same_without,
    prob_two_different_without,
    prob_complement,
    prob_independent_both,
    prob_independent_at_least_one,
    prob_conditional_without,
    prob_conditional_table,
    prob_committee_count,
    prob_coin_exact_heads,
    prob_coin_at_least_head,
    prob_die_multiple,
    prob_card_ace_king,
    prob_two_dice_product_even,
    prob_bag_transfer,
    prob_combination_or,
    prob_die_less_than,
)


def build_probability():
    return build_specs(FAMILIES)
