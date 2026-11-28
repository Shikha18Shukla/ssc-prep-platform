# -*- coding: utf-8 -*-
"""Ages – Data Interpretation — 120 self-contained Prelims-level questions."""

from __future__ import annotations

from .bank import fmt
from .common import F, build_specs, data, near_num, q, ratio

SOURCE = "Ages Data Interpretation class notes (local PDF)"
PAGES = {
    1: '419d6ebd-36ff-4b8a-80e5-178a8bde98d6.pdf, pp. 4-6',
    2: '419d6ebd-36ff-4b8a-80e5-178a8bde98d6.pdf, pp. 7-8',
    3: '419d6ebd-36ff-4b8a-80e5-178a8bde98d6.pdf, pp. 9-11',
    4: '419d6ebd-36ff-4b8a-80e5-178a8bde98d6.pdf, pp. 4-12',
}


def _ratio_options(answer):
    first, second = answer.split(":")
    return [f"{second}:{first}", f"{int(first) + 1}:{second}", f"{first}:{int(second) + 1}"]


def ad_table_lookup(r, v):
    ages, ask = (
        ([32, 27, 5], 0), ([41, 36, 9], 2), ([29, 24, 4], 3),
        ([38, 33, 7], 4), ([45, 40, 12], 1),
    )[v]
    block = data([("father (years)", ages[0]), ("mother (years)", ages[1]), ("child (years)", ages[2])])
    asks = [
        "father's age", "mother's age", "child's age",
        "sum of all three ages", "difference between the father's age and the mother's age",
    ]
    answer = [ages[0], ages[1], ages[2], sum(ages), abs(ages[0] - ages[1])][ask]
    return q(
        "ad_table_lookup", v, f"{block} Find the {asks[ask]}.", answer,
        near_num(answer, 2),
        f"The table gives ages {ages[0]}, {ages[1]} and {ages[2]}; the requested "
        f"value is {answer}.",
        {"ages": ages, "ask": ask},
    )


def ad_table_difference(r, v):
    ages, pair, labels = (
        ([48, 42, 15], [0, 1], ["father", "mother", "child"]),
        ([53, 49, 12], [0, 2], ["father", "mother", "child"]),
        ([36, 31, 8], [1, 2], ["father", "mother", "child"]),
        ([44, 39, 11], [0, 2], ["father", "mother", "child"]),
        ([57, 51, 16], [0, 1], ["father", "mother", "child"]),
    )[v]
    block = data([(f"{labels[0]} (yr)", ages[0]), (f"{labels[1]} (yr)", ages[1]), (f"{labels[2]} (yr)", ages[2])])
    answer = abs(ages[pair[0]] - ages[pair[1]])
    return q(
        "ad_table_difference", v,
        f"{block} Find the difference between the {labels[pair[0]]}'s age and "
        f"the {labels[pair[1]]}'s age.",
        answer, near_num(answer, 2),
        f"Ages are {ages[pair[0]]} and {ages[pair[1]]}; their difference is "
        f"{ages[pair[0]]} - {ages[pair[1]]} = {answer}.",
        {"ages": ages, "pair": pair},
    )


def ad_table_sum(r, v):
    ages = ([22, 18, 6], [35, 31, 10], [41, 37, 13], [28, 24, 7], [50, 46, 19])[v]
    block = data([("person P", ages[0]), ("person Q", ages[1]), ("person R", ages[2])])
    answer = sum(ages)
    return q(
        "ad_table_sum", v, f"{block} Find the sum of the three ages.", answer,
        near_num(answer, 3),
        f"Adding the listed ages: {ages[0]} + {ages[1]} + {ages[2]} = {answer}.",
        {"ages": ages},
    )


def ad_table_average(r, v):
    ages = ([24, 30, 18, 20], [32, 28, 36, 24], [15, 21, 27, 18, 19],
            [40, 36, 44, 32], [26, 34, 30, 22, 23])[v]
    block = data([(f"member {i + 1}", age) for i, age in enumerate(ages)])
    answer = F(sum(ages), len(ages))
    return q(
        "ad_table_average", v, f"{block} Find the average age.", answer,
        near_num(answer, 2),
        f"Total = {sum(ages)} over {len(ages)} members, so average = "
        f"{sum(ages)}/{len(ages)} = {fmt(answer)}.",
        {"ages": ages},
    )


def ad_table_future(r, v):
    ages, idx, k, future = (
        ([33, 28, 8], 2, 5, True), ([42, 37, 12], 1, 4, False),
        ([29, 25, 6], 0, 7, True), ([48, 43, 15], 2, 3, False),
        ([36, 31, 9], 1, 6, True),
    )[v]
    labels = ["person A", "person B", "person C"]
    block = data([(labels[0], ages[0]), (labels[1], ages[1]), (labels[2], ages[2])])
    answer = ages[idx] + (k if future else -k)
    return q(
        "ad_table_future", v,
        f"{block} Find the age of {labels[idx]} {'after' if future else 'before'} {k} years.",
        answer, near_num(answer, 2),
        f"{labels[idx]} is {ages[idx]} now; {'adding' if future else 'subtracting'} "
        f"{k} gives {answer}.",
        {"ages": ages, "idx": idx, "k": k, "future": future},
    )


def ad_table_ratio(r, v):
    a, b, order = ((28, 21, 0), (36, 24, 1), (45, 30, 0), (50, 35, 1), (27, 18, 0))[v]
    block = data([("first person", a), ("second person", b)])
    answer = ratio(a, b) if order == 0 else ratio(b, a)
    return q(
        "ad_table_ratio", v,
        f"{block} Find the ratio of "
        f"{'the first person’s age to the second person’s age' if order == 0 else 'the second person’s age to the first person’s age'} "
        f"in lowest terms.",
        answer, _ratio_options(answer),
        f"The ages are {a} and {b}; the required ratio reduces to {answer}.",
        {"a": a, "b": b, "order": order},
    )


def ad_family_caselet(r, v):
    father, mother, child, ask = (
        (38, 34, 8, 0), (45, 41, 13, 1), (31, 27, 5, 2),
        (52, 48, 20, 3), (42, 38, 11, 4),
    )[v]
    block = data([("father age", father), ("mother age", mother), ("child age", child)])
    values = [father, mother, child, father + mother, father + mother + child]
    asks = [
        "the father's age", "the mother's age", "the child's age",
        "the sum of the parents' ages", "the sum of all three ages",
    ]
    answer = values[ask]
    return q(
        "ad_family_caselet", v, f"{block} Find {asks[ask]}.", answer,
        near_num(answer, 3),
        f"Using father={father}, mother={mother}, child={child}, the requested "
        f"value is {answer}.",
        {"father": father, "mother": mother, "child": child, "ask": ask},
    )


def ad_yearwise(r, v):
    vals, mode, idx = (
        ([31, 32, 33], "lookup", 1), ([28, 29, 30], "change", 0),
        ([40, 41, 42], "sum", 0), ([25, 26, 27], "lookup", 2),
        ([36, 39, 43], "change", 0),
    )[v]
    block = data([("2020 age", vals[0]), ("2021 age", vals[1]), ("2022 age", vals[2])])
    if mode == "lookup":
        answer = vals[idx]
        prompt = f"{block} Find the age recorded for {2020 + idx}."
    elif mode == "change":
        answer = abs(vals[1] - vals[0])
        prompt = f"{block} Find the increase in age from 2020 to 2021."
    else:
        answer = vals[0] + vals[1]
        prompt = f"{block} Find the sum of the ages recorded for 2020 and 2021."
    return q(
        "ad_yearwise", v, prompt, answer, near_num(answer, 2),
        f"The listed values are {vals[0]}, {vals[1]} and {vals[2]}, so the "
        f"required value is {answer}.",
        {"vals": vals, "mode": mode, "idx": idx},
    )


def ad_average_compare(r, v):
    group_a, group_b, ask = (
        ([20, 24, 28], [30, 34, 38], "A"),
        ([20, 24, 28], [30, 34, 38], "diff"),
        ([32, 36, 40], [26, 30, 34], "B"),
        ([18, 22, 26, 30], [24, 28, 32, 36], "diff"),
        ([42, 46, 50], [38, 42, 46], "A"),
    )[v]
    block = data([("group A ages", group_a), ("group B ages", group_b)])
    avg_a, avg_b = F(sum(group_a), len(group_a)), F(sum(group_b), len(group_b))
    answer = avg_a if ask == "A" else (avg_b if ask == "B" else abs(avg_a - avg_b))
    asks = {
        "A": "the average age of group A",
        "B": "the average age of group B",
        "diff": "the difference between the two group averages",
    }
    return q(
        "ad_average_compare", v, f"{block} Find {asks[ask]}.", answer,
        near_num(answer, 2),
        f"Group A average = {sum(group_a)}/{len(group_a)} = {fmt(avg_a)}; "
        f"group B average = {sum(group_b)}/{len(group_b)} = {fmt(avg_b)}; "
        f"the required value is {answer}.",
        {"a": group_a, "b": group_b, "ask": ask},
    )


def ad_percentage_of_age(r, v):
    ages, idx, percent = (
        ([40, 36, 8], 0, 25), ([50, 45, 12], 1, 20),
        ([60, 54, 15], 2, 40), ([48, 42, 10], 0, 50),
        ([72, 66, 18], 2, 25),
    )[v]
    labels = ["person A", "person B", "person C"]
    block = data([(labels[0], ages[0]), (labels[1], ages[1]), (labels[2], ages[2])])
    answer = F(ages[idx] * percent, 100)
    return q(
        "ad_percentage_of_age", v,
        f"{block} What is {percent}% of {labels[idx]}'s age?", answer,
        near_num(answer, 2),
        f"{percent}% of {ages[idx]} = {percent}x{ages[idx]}/100 = {fmt(answer)}.",
        {"ages": ages, "idx": idx, "percent": percent},
    )


def ad_future_ratio(r, v):
    a, b, k = ((25, 20, 5), (32, 24, 4), (40, 30, 10), (18, 12, 3), (45, 36, 9))[v]
    block = data([("first age", a), ("second age", b), ("years ahead", k)])
    answer = ratio(a + k, b + k)
    return q(
        "ad_future_ratio", v,
        f"{block} Find the ratio of the first age to the second age after {k} years.",
        answer, _ratio_options(answer),
        f"After {k} years the ages are {a + k} and {b + k}; the ratio is {answer}.",
        {"a": a, "b": b, "k": k},
    )


def ad_past_ratio(r, v):
    a, b, k = ((30, 25, 5), (42, 36, 6), (51, 39, 9), (28, 22, 4), (60, 48, 12))[v]
    block = data([("first age", a), ("second age", b), ("years back", k)])
    answer = ratio(a - k, b - k)
    return q(
        "ad_past_ratio", v,
        f"{block} Find the ratio of the first age to the second age {k} years ago.",
        answer, _ratio_options(answer),
        f"{k} years ago the ages were {a - k} and {b - k}; the ratio is {answer}.",
        {"a": a, "b": b, "k": k},
    )


def ad_join_average(r, v):
    n, avg, newcomer, ask = (
        (5, 30, 30, "avg"), (4, 28, 40, "total"), (6, 32, 26, "avg"),
        (8, 35, 44, "avg"), (7, 29, 35, "total"),
    )[v]
    block = data([("members", n), ("current average", avg), ("joining age", newcomer)])
    total = n * avg + newcomer
    count = n + 1
    answer = total if ask == "total" else F(total, count)
    return q(
        "ad_join_average", v,
        f"{block} Find the {'total age of the group' if ask == 'total' else 'average age of the group'} after the new member joins.",
        answer, near_num(answer, 2),
        f"Initial total = {n}x{avg} = {n * avg}; adding {newcomer} gives {total} "
        f"over {count} members, so the average is {fmt(F(total, count))}.",
        {"n": n, "avg": avg, "new": newcomer, "ask": ask},
    )


def ad_leave_average(r, v):
    n, avg, leaving, ask = (
        (6, 32, 42, "avg"), (8, 30, 50, "total"), (5, 36, 40, "avg"),
        (9, 28, 44, "avg"), (7, 34, 52, "total"),
    )[v]
    block = data([("members", n), ("current average", avg), ("departing age", leaving)])
    total = n * avg - leaving
    count = n - 1
    answer = total if ask == "total" else F(total, count)
    return q(
        "ad_leave_average", v,
        f"{block} Find the {'total age of the group' if ask == 'total' else 'average age of the group'} after the member leaves.",
        answer, near_num(answer, 2),
        f"Initial total = {n}x{avg} = {n * avg}; subtracting {leaving} leaves "
        f"{total} across {count} members, so the average is {fmt(F(total, count))}.",
        {"n": n, "avg": avg, "leaving": leaving, "ask": ask},
    )


def ad_bar_pairs(r, v):
    pairs, mode, idx = (
        ([[28, 24], [29, 25], [30, 26]], "sum_at", 1),
        ([[35, 31], [36, 32], [37, 33]], "diff_at", 0),
        ([[41, 38], [42, 39], [43, 40]], "total_first", 0),
        ([[22, 18], [23, 19], [24, 20]], "sum_at", 2),
        ([[50, 45], [51, 46], [52, 47]], "diff_at", 1),
    )[v]
    rows = []
    for i, pair in enumerate(pairs):
        rows.append((f"year {2020 + i} A", pair[0]))
        rows.append((f"year {2020 + i} B", pair[1]))
    block = data(rows)
    if mode == "sum_at":
        answer = pairs[idx][0] + pairs[idx][1]
        prompt = f"{block} Find the sum of A's and B's ages in {2020 + idx}."
    elif mode == "diff_at":
        answer = pairs[idx][0] - pairs[idx][1]
        prompt = f"{block} Find by how many years A is older than B in {2020 + idx}."
    else:
        answer = sum(pair[0] for pair in pairs)
        prompt = f"{block} Find the total of A's ages over the three years."
    return q(
        "ad_bar_pairs", v, prompt, answer, near_num(answer, 2),
        f"The listed pair values are {pairs}; the requested value is {answer}.",
        {"pairs": pairs, "mode": mode, "idx": idx},
    )


def ad_two_groups_combined(r, v):
    n1, avg1, n2, avg2, ask = (
        (4, 25, 6, 35, "avg"), (5, 30, 5, 40, "total"),
        (3, 20, 7, 30, "avg"), (6, 28, 4, 38, "avg"),
        (8, 33, 2, 43, "total"),
    )[v]
    block = data([("group A members", n1), ("group A average", avg1),
                  ("group B members", n2), ("group B average", avg2)])
    total = n1 * avg1 + n2 * avg2
    count = n1 + n2
    answer = total if ask == "total" else F(total, count)
    return q(
        "ad_two_groups_combined", v,
        f"{block} Find the {'combined total age' if ask == 'total' else 'combined average age'}.",
        answer, near_num(answer, 2),
        f"Totals are {n1}x{avg1} = {n1 * avg1} and {n2}x{avg2} = {n2 * avg2}; "
        f"combined total = {total} over {count} people, giving average "
        f"{fmt(F(total, count))}.",
        {"n1": n1, "a1": avg1, "n2": n2, "a2": avg2, "ask": ask},
    )


def ad_age_multiples(r, v):
    a, k, ask = ((12, 3, 0), (15, 2, 1), (9, 4, 2), (18, 2, 0), (14, 3, 1))[v]
    block = data([("first age", a), ("multiplier", k)])
    values = [k * a, a + k * a, k * a - a]
    asks = ["the second age", "the sum of the two ages", "the difference of the two ages"]
    answer = values[ask]
    return q(
        "ad_age_multiples", v, f"{block} The second age is {k} times the first. Find {asks[ask]}.",
        answer, near_num(answer, 3),
        f"Second age = {k}x{a} = {k * a}; the requested value is {answer}.",
        {"a": a, "k": k, "ask": ask},
    )


def ad_fraction_age(r, v):
    a, k, ask = ((36, 3, 0), (48, 4, 1), (60, 5, 2), (42, 6, 0), (72, 8, 1))[v]
    block = data([("first age", a), ("denominator", k)])
    values = [F(a, k), a + F(a, k), a - F(a, k)]
    asks = ["the second age", "the sum of the two ages", "the difference of the two ages"]
    answer = values[ask]
    return q(
        "ad_fraction_age", v,
        f"{block} The second age is 1/{k} of the first age. Find {asks[ask]}.",
        answer, near_num(answer, 2),
        f"Second age = {a}/{k} = {fmt(F(a, k))}; the requested value is {answer}.",
        {"a": a, "k": k, "ask": ask},
    )


def ad_ratio_missing(r, v):
    p, qv, first, ask = (
        (2, 3, 24, 0), (3, 4, 27, 1), (4, 5, 32, 0),
        (5, 7, 25, 1), (3, 5, 18, 0),
    )[v]
    block = data([("ratio first:second", f"{p}:{qv}"), ("first age", first)])
    second = F(first * qv, p)
    answer = second if ask == 0 else first + second
    return q(
        "ad_ratio_missing", v,
        f"{block} Find {'the second age' if ask == 0 else 'the sum of the two ages'}.",
        answer, near_num(answer, 2),
        f"Second age = {first}x{qv}/{p} = {fmt(second)}; the requested value is {answer}.",
        {"p": p, "q": qv, "first": first, "ask": ask},
    )


def ad_older_count(r, v):
    ages, threshold, mode = (
        ([12, 18, 25, 31], 20, "older"), ([14, 19, 22, 27], 18, "older"),
        ([9, 15, 21, 26], 20, "younger"), ([30, 35, 40, 45], 37, "older"),
        ([11, 17, 23, 29, 33], 24, "younger"),
    )[v]
    block = data([("ages", ages), ("cutoff age", threshold)])
    answer = sum(1 for age in ages if age > threshold) if mode == "older" else sum(1 for age in ages if age < threshold)
    return q(
        "ad_older_count", v,
        f"{block} How many listed ages are {'greater than' if mode == 'older' else 'less than'} {threshold}?",
        answer, near_num(answer, 1),
        f"Comparing each listed age with {threshold}, {answer} values satisfy the condition.",
        {"ages": ages, "threshold": threshold, "mode": mode},
    )


def ad_median_range(r, v):
    ages, mode = (
        ([18, 24, 30, 36, 42], "median"), ([20, 26, 32, 38], "range"),
        ([15, 21, 27, 33, 39], "median"), ([25, 30, 35, 40, 45], "range"),
        ([12, 18, 24, 30, 36, 42], "median"),
    )[v]
    n = len(ages)
    median = ages[n // 2] if n % 2 else F(ages[n // 2 - 1] + ages[n // 2], 2)
    answer = median if mode == "median" else ages[-1] - ages[0]
    return q(
        "ad_median_range", v,
        f"{data([('ages in order', ages)])} Find the {mode} of the listed ages.",
        answer, near_num(answer, 2),
        f"With ages {ages}, the median is {fmt(median)} and the range is "
        f"{ages[-1] - ages[0]}; the requested value is {answer}.",
        {"ages": ages, "mode": mode},
    )


def ad_two_year_growth(r, v):
    vals, ask = (
        ([30, 31, 33], 0), ([25, 27, 30], 2), ([40, 41, 44], 1),
        ([22, 25, 29], 3), ([50, 52, 55], 0),
    )[v]
    block = data([("year 1 age", vals[0]), ("year 2 age", vals[1]), ("year 3 age", vals[2])])
    values = [vals[1] - vals[0], vals[2] - vals[1], vals[2] - vals[0], F(sum(vals), 3)]
    asks = [
        "the increase from year 1 to year 2", "the increase from year 2 to year 3",
        "the increase from year 1 to year 3", "the average of the three recorded ages",
    ]
    answer = values[ask]
    return q(
        "ad_two_year_growth", v, f"{block} Find {asks[ask]}.", answer,
        near_num(answer, 2),
        f"Using the three values {vals[0]}, {vals[1]} and {vals[2]}, the "
        f"requested value is {answer}.",
        {"vals": vals, "ask": ask},
    )


def ad_caselet_future_sum(r, v):
    ages, k, ask = (
        ([38, 34, 10], 5, "sum"), ([45, 41, 14], 3, "avg"),
        ([31, 27, 6], 4, "sum"), ([52, 48, 20], 2, "avg"),
        ([42, 38, 11], 6, "sum"),
    )[v]
    block = data([("father", ages[0]), ("mother", ages[1]), ("child", ages[2]),
                  ("years ahead", k)])
    total = sum(ages) + k * len(ages)
    answer = total if ask == "sum" else F(total, len(ages))
    return q(
        "ad_caselet_future_sum", v,
        f"{block} Find the {'sum' if ask == 'sum' else 'average'} of the three ages after {k} years.",
        answer, near_num(answer, 2),
        f"Present total = {sum(ages)}; after {k} years each of the {len(ages)} "
        f"people gains {k} years, so total = {total} and average = "
        f"{fmt(F(total, len(ages)))}.",
        {"ages": ages, "k": k, "ask": ask},
    )


def ad_average_after_birth(r, v):
    parents, child, k, ask = (
        ([32, 30], 5, 3, "avg"), ([38, 35], 8, 2, "total"),
        ([41, 37], 11, 4, "child"), ([29, 27], 4, 5, "avg"),
        ([45, 42], 15, 3, "total"),
    )[v]
    block = data([("parent 1", parents[0]), ("parent 2", parents[1]),
                  ("child", child), ("years ahead", k)])
    total = parents[0] + parents[1] + child + 3 * k
    if ask == "total":
        answer = total
    elif ask == "child":
        answer = child + k
    else:
        answer = F(total, 3)
    return q(
        "ad_average_after_birth", v,
        f"{block} Find the {'total family age' if ask == 'total' else ('child’s age' if ask == 'child' else 'average family age')} after {k} years.",
        answer, near_num(answer, 2),
        f"Present family total = {parents[0]}+{parents[1]}+{child} = "
        f"{parents[0] + parents[1] + child}; after {k} years all three gain "
        f"{k} years, so total = {total} and average = {fmt(F(total, 3))}.",
        {"p1": parents[0], "p2": parents[1], "child": child, "k": k, "ask": ask},
    )


FAMILIES = [
    ad_table_lookup, ad_table_difference, ad_table_sum, ad_table_average,
    ad_table_future, ad_table_ratio, ad_family_caselet, ad_yearwise,
    ad_average_compare, ad_percentage_of_age, ad_future_ratio, ad_past_ratio,
    ad_join_average, ad_leave_average, ad_bar_pairs, ad_two_groups_combined,
    ad_age_multiples, ad_fraction_age, ad_ratio_missing, ad_older_count,
    ad_median_range, ad_two_year_growth, ad_caselet_future_sum,
    ad_average_after_birth,
]


def build_ages_di():
    return build_specs(FAMILIES, mains=False)
