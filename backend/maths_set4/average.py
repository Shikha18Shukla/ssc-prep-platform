# -*- coding: utf-8 -*-
"""Average - 120 original verified questions for the fourth Maths batch."""

from __future__ import annotations

from fractions import Fraction

from .bank import fmt, fmt_dec
from .common import build_specs, pair, q, ratio_str, third

F = Fraction

SOURCE = "Average topic-wise mains sets (local PDFs)"
PAGES = {
    1: "Mains_Topic_wise_Average_Set_-1_(Mains).pdf, pp. 1-8",
    2: "Mains_Topic_wise_Average_Set_-2_(Mains).pdf, pp. 1-8",
    3: "Mains_Topic_wise_Average_Set_-3_(Mains).pdf, pp. 1-8",
    4: "Mains_Topic_wise_Average_Set_-4_(Mains).pdf, pp. 1-8",
}


AV_BASIC = (
    ((68, 72, 75, 81, 84), "went through five quiz scorecards", "What is their mean score?"),
    ((54, 61, 68, 72, 80), "jotted down five practice-test marks", "Find the average mark."),
    ((90, 94, 97, 101, 108), "checked five mock-exam scores", "What was the average of the five scores?"),
    ((42, 48, 59, 60, 71), "tallied five weekly assessment marks", "Determine the arithmetic mean of these marks."),
    ((77, 81, 88, 92, 97), "compared five section-wise scores", "What is the average score across the five entries?"),
)


def av_basic(rng, variant):
    v = variant % 5
    values, scene, ask = AV_BASIC[v]
    name_a, name_b = pair(variant, 0)
    total = sum(values)
    n = len(values)
    mean = F(total, n)
    text = f"{name_a} and {name_b} {scene}: {', '.join(str(x) for x in values)}. {ask}"
    alts = []
    for cand in (F(total, n - 1), F(total - values[0], n), F(total - values[1], n), F(total, n + 1)):
        label = fmt(cand)
        if label != fmt(mean) and label not in alts:
            alts.append(label)
        if len(alts) == 3:
            break
    return q(
        "av_basic", variant, text, mean, alts,
        f"Sum = {total} and there are {n} figures, so the average is {total}/{n} = {fmt(mean)}.",
        {"values": list(values)},
    )


AV_TWO_GROUPS = (
    (10, 70, 15, 80, "led two batches of students", "Find the combined average of both batches."),
    (8, 65, 12, 75, "compared two practice batches", "What is the average for all the students together?"),
    (20, 58, 30, 68, "reviewed two sections of a class", "Find the overall average of the two sections."),
    (14, 82, 21, 92, "coached two batches for a contest", "What is the mean of the entire group?"),
    (9, 55, 6, 70, "looked after two tutorial groups", "Determine the average of all students in the two groups."),
)


def av_two_groups(rng, variant):
    v = variant % 5
    n1, m1, n2, m2, scene, ask = AV_TWO_GROUPS[v]
    name_a, name_b = pair(variant, 1)
    total = n1 * m1 + n2 * m2
    combined = F(total, n1 + n2)
    text = (
        f"{name_a} and {name_b} {scene}. {name_a}'s group has {n1} students with average {m1}, "
        f"while {name_b}'s group has {n2} students with average {m2}. {ask}"
    )
    alts = []
    for cand in (F(m1 + m2, 2), F(total, n1 + n2 - 1), F(total, n1 + n2 + 1), F(n1 * m1 + n2 * m2 + n1, n1 + n2)):
        label = fmt(cand)
        if label != fmt(combined) and label not in alts:
            alts.append(label)
        if len(alts) == 3:
            break
    return q(
        "av_two_groups", variant, text, combined, alts,
        f"Combined total = {n1} x {m1} + {n2} x {m2} = {total}; students = {n1 + n2}; "
        f"average = {total}/{n1 + n2} = {fmt(combined)}.",
        {"N1": n1, "A1": m1, "N2": n2, "A2": m2},
    )


AV_REPLACEMENT = (
    (10, 72, 60, 90, "kept a log of ten readings", "What is the new average?"),
    (8, 65, 50, 82, "recorded eight measurements", "Find the average after the replacement."),
    (12, 58, 64, 88, "reviewed twelve observations", "What does the average become?"),
    (15, 80, 95, 65, "checked fifteen entries", "Determine the revised average."),
    (20, 66, 54, 94, "maintained twenty data rows", "What is the average of the updated rows?"),
)


def av_replacement(rng, variant):
    v = variant % 5
    n, avg, old, new, scene, ask = AV_REPLACEMENT[v]
    name_a, name_b = pair(variant, 2)
    change = F(new - old, n)
    answer = F(avg) + change
    text = (
        f"{name_a} and {name_b} {scene} whose average is {avg}. "
        f"A reading of {old} is replaced by {new}. {ask}"
    )
    alts = []
    for cand in (F(avg) + F(new - old, n - 1), F(avg) - change, F(avg) + F(new - old, n + 1), F(n * avg + new, n + 1)):
        label = fmt(cand)
        if label != fmt(answer) and label not in alts:
            alts.append(label)
        if len(alts) == 3:
            break
    return q(
        "av_replacement", variant, text, answer, alts,
        f"The replacement adds {new - old} to the total of {n} readings, so the average rises by "
        f"{new - old}/{n}; new average = {avg} + {fmt(change)} = {fmt(answer)}.",
        {"N": n, "Avg": avg, "Old": old, "New": new},
    )


AV_ADDED_MEMBER = (
    (9, 68, 88, "had nine values with average 68", "What is the average once the new value is included?"),
    (11, 74, 98, "tracked eleven readings with average 74", "Find the average after the extra reading."),
    (15, 56, 88, "collected fifteen figures with average 56", "What is the mean of all sixteen figures?"),
    (7, 82, 74, "worked with seven numbers averaging 82", "Determine the new average after adding the number."),
    (12, 63, 102, "noted twelve entries averaging 63", "What is the revised average of the entries?"),
)


def av_added_member(rng, variant):
    v = variant % 5
    n, avg, added, scene, ask = AV_ADDED_MEMBER[v]
    name_a, name_b = pair(variant, 3)
    name_c = third(variant)
    total = n * avg + added
    answer = F(total, n + 1)
    text = (
        f"{name_a} and {name_b} {scene}. {name_c} adds one more value of {added} to the list. {ask}"
    )
    alts = []
    for cand in (F(total, n), F(total, n + 2), F((n - 1) * avg + added, n), F(avg) + F(added, n)):
        label = fmt(cand)
        if label != fmt(answer) and label not in alts:
            alts.append(label)
        if len(alts) == 3:
            break
    return q(
        "av_added_member", variant, text, answer, alts,
        f"Old total = {n} x {avg} = {n * avg}; new total = {n * avg} + {added} = {total}; "
        f"dividing by {n + 1} members gives {total}/{n + 1} = {fmt(answer)}.",
        {"N": n, "Avg": avg, "Added": added},
    )


AV_REMOVED_MEMBER = (
    (10, 72, 90, "kept ten figures averaging 72", "What is the average of the remaining figures?"),
    (8, 65, 51, "listed eight readings averaging 65", "Find the mean after that reading is removed."),
    (12, 58, 36, "stored twelve values averaging 58", "What is the average of the leftover values?"),
    (15, 80, 108, "recorded fifteen marks averaging 80", "Determine the remaining average."),
    (20, 70, 51, "held twenty data points averaging 70", "What is the mean of the other points?"),
)


def av_removed_member(rng, variant):
    v = variant % 5
    n, avg, removed, scene, ask = AV_REMOVED_MEMBER[v]
    name_a, name_b = pair(variant, 0)
    total = n * avg - removed
    answer = F(total, n - 1)
    text = (
        f"{name_a} and {name_b} {scene}. The value {removed} is now removed from the list. {ask}"
    )
    alts = []
    for cand in (F(total, n), F(total, n - 2), F(n * avg + removed, n - 1), F(avg) - F(removed, n)):
        label = fmt(cand)
        if label != fmt(answer) and label not in alts:
            alts.append(label)
        if len(alts) == 3:
            break
    return q(
        "av_removed_member", variant, text, answer, alts,
        f"Original total = {n} x {avg} = {n * avg}; after removing {removed}, the total is {total} "
        f"for {n - 1} figures, so the average is {total}/{n - 1} = {fmt(answer)}.",
        {"N": n, "Avg": avg, "Removed": removed},
    )


AV_MISSING_VALUE = (
    (5, 72, (64, 70, 75, 77), "looked at five scores averaging 72", "What is the missing score?"),
    (6, 68, (60, 62, 66, 68, 70), "had six readings averaging 68", "Find the reading that is not shown."),
    (4, 85, (78, 80, 92), "saw four marks averaging 85", "Which mark was left out?"),
    (8, 55, (45, 48, 52, 58, 62, 65, 70), "examined eight figures averaging 55", "What is the eighth figure?"),
    (7, 90, (84, 86, 88, 90, 92, 94), "checked seven values averaging 90", "Determine the missing value."),
)


def av_missing_value(rng, variant):
    v = variant % 5
    n, avg, known, scene, ask = AV_MISSING_VALUE[v]
    name_a, name_b = pair(variant, 1)
    shown = sum(known)
    answer = n * avg - shown
    text = (
        f"{name_a} and {name_b} {scene}. The figures they can see are "
        f"{', '.join(str(x) for x in known)}. {ask}"
    )
    alts = []
    for cand in (answer + 2, answer - 3, n * avg - sum(known[:-1]), n * avg - sum(known[1:])):
        label = fmt(cand)
        if label != fmt(answer) and label not in alts:
            alts.append(label)
        if len(alts) == 3:
            break
    return q(
        "av_missing_value", variant, text, answer, alts,
        f"All {n} figures total {n} x {avg} = {n * avg}; the {n - 1} known figures total {shown}; "
        f"hence the missing figure is {n * avg} - {shown} = {answer}.",
        {"N": n, "Avg": avg, "Known": list(known)},
    )


AV_WEIGHTED = (
    (((2, 70), (3, 80), (5, 90)), "weighed three components of a test", "Find the weighted average mark."),
    (((2, 60), (3, 75), (5, 85)), "combined three weighted papers", "What is the weighted mean?"),
    (((4, 65), (3, 72), (3, 88)), "merged three graded tasks", "Determine the weighted average score."),
    (((2, 80), (3, 90), (5, 96)), "calculated a final grade from three parts", "What is the final weighted mark?"),
    (((3, 55), (2, 65), (5, 75)), "combined three assessment weights", "Find the weighted average."),
)


def av_weighted(rng, variant):
    v = variant % 5
    pairs, scene, ask = AV_WEIGHTED[v]
    name_a, name_b = pair(variant, 2)
    name_c = third(variant)
    pairs = [tuple(x) for x in pairs]
    weight_total = sum(w for w, _ in pairs)
    scored_total = sum(w * m for w, m in pairs)
    answer = F(scored_total, weight_total)
    detail = ", ".join(f"{w} weight and {m} marks" for w, m in pairs)
    text = f"{name_a}, {name_c} and {name_b} {scene}: {detail}. {ask}"
    plain = F(sum(m for _, m in pairs), len(pairs))
    alts = []
    for cand in (plain, answer + 2, answer - 2, F(scored_total, weight_total - 1)):
        label = fmt(cand)
        if label != fmt(answer) and label not in alts:
            alts.append(label)
        if len(alts) == 3:
            break
    return q(
        "av_weighted", variant, text, answer, alts,
        f"Weighted sum = {scored_total} and total weight = {weight_total}, so the weighted average "
        f"is {scored_total}/{weight_total} = {fmt(answer)}.",
        {"Pairs": [[w, m] for w, m in pairs]},
    )


AV_AGE_FAMILY = (
    (4, 32, 5, "noted the ages of a family", "What will the average age be after {y} years?"),
    (5, 28, 3, "recorded five family ages", "Find the average age after {y} years."),
    (3, 41, 7, "discussed three relatives' ages", "What is the average age {y} years from now?"),
    (6, 35, 4, "listed six members of a household", "Determine the average age after {y} years."),
    (2, 54, 10, "compared two family members' ages", "What will their average age be in {y} years?"),
)


def av_age_family(rng, variant):
    v = variant % 5
    n, avg, years, scene, ask = AV_AGE_FAMILY[v]
    name_a, name_b = pair(variant, 3)
    answer = F(avg) + years
    text = (
        f"{name_a} and {name_b} {scene}: the average age of the {n} members is {avg} years. "
        f"{ask.format(y=years)}"
    )
    alts = []
    for cand in (F(avg) + F(years, 2), F(avg) + 2 * years, F(avg) + years - 1, F(avg) + years + 2):
        label = fmt(cand)
        if label != fmt(answer) and label not in alts:
            alts.append(label)
        if len(alts) == 3:
            break
    return q(
        "av_age_family", variant, text, answer, alts,
        f"Every member gains {years} years, so the average also rises by {years}: "
        f"{avg} + {years} = {fmt(answer)}.",
        {"N": n, "Avg": avg, "Years": years},
    )


AV_MARKS = (
    ((60, 70, 77, 86, 92), 3, "listed five subject marks", "What is the average of the best {k} marks?"),
    ((58, 65, 72, 88, 98), 3, "noted five test scores", "Find the mean of the highest {k} scores."),
    ((63, 74, 79, 90, 98), 3, "compared five paper marks", "What is the average of the top {k} papers?"),
    ((55, 68, 76, 83, 87), 3, "reviewed five exam marks", "Determine the mean of the best {k} marks."),
    ((62, 70, 85, 94, 100), 3, "tallied five unit-test scores", "What is the average of the three highest scores?"),
)


def av_marks(rng, variant):
    v = variant % 5
    marks, top, scene, ask = AV_MARKS[v]
    name_a, name_b = pair(variant, 0)
    best = sorted(marks, reverse=True)[:top]
    answer = F(sum(best), top)
    text = (
        f"{name_a} and {name_b} {scene}: {', '.join(str(x) for x in marks)}. "
        f"{ask.format(k=top)}"
    )
    all_mean = F(sum(marks), len(marks))
    low = sorted(marks)[:top]
    alts = []
    for cand in (all_mean, F(sum(low), top), F(sum(best[:top - 1]), top - 1), answer + 1):
        label = fmt(cand)
        if label != fmt(answer) and label not in alts:
            alts.append(label)
        if len(alts) == 3:
            break
    return q(
        "av_marks", variant, text, answer, alts,
        f"The best {top} marks are {', '.join(str(x) for x in best)}, summing to {sum(best)}; "
        f"their average is {sum(best)}/{top} = {fmt(answer)}.",
        {"Marks": list(marks), "Top": top},
    )


AV_CONSECUTIVE = (
    (7, 12, "listed consecutive integers", "What is their average?"),
    (9, 20, "wrote down consecutive whole numbers", "Find the mean of the list."),
    (5, 31, "considered consecutive integers", "What is the average of the five numbers?"),
    (11, 45, "counted consecutive numbers", "Determine their arithmetic mean."),
    (13, 11, "noted a run of consecutive integers", "What is the mean of the run?"),
)


def av_consecutive(rng, variant):
    v = variant % 5
    count, first, scene, ask = AV_CONSECUTIVE[v]
    name_a, name_b = pair(variant, 1)
    answer = F(2 * first + count - 1, 2)
    text = (
        f"{name_a} and {name_b} {scene}: take {count} consecutive integers starting from {first}. {ask}"
    )
    alts = []
    for cand in (F(2 * first + count, 2), answer + 1, answer - 1, F(first + count, 2)):
        label = fmt(cand)
        if label != fmt(answer) and label not in alts:
            alts.append(label)
        if len(alts) == 3:
            break
    return q(
        "av_consecutive", variant, text, answer, alts,
        f"The first term is {first} and the last is {first + count - 1}; for consecutive integers "
        f"the mean is (first + last)/2 = ({first} + {first + count - 1})/2 = {fmt(answer)}.",
        {"Count": count, "First": first},
    )


AV_RATIO_SPLIT = (
    (2, 3, 70, 85, "compared two classes", "What is the average of all the students?"),
    (3, 5, 64, 80, "looked at two tutorial sections", "Find the combined average."),
    (4, 1, 72, 92, "reviewed two groups", "What is the overall mean?"),
    (5, 7, 55, 67, "merged two batches", "Determine the mean of the whole batch."),
    (1, 4, 82, 97, "checked two sections of a class", "What is their common average?"),
)


def av_ratio_split(rng, variant):
    v = variant % 5
    r1, r2, m1, m2, scene, ask = AV_RATIO_SPLIT[v]
    name_a, name_b = pair(variant, 2)
    weighted = r1 * m1 + r2 * m2
    answer = F(weighted, r1 + r2)
    text = (
        f"{name_a} and {name_b} {scene}: their student numbers are in the ratio {r1}:{r2} and their "
        f"average marks are {m1} and {m2} respectively. {ask}"
    )
    alts = []
    for cand in (F(m1 + m2, 2), F(weighted, r1 + r2 - 1), F(weighted, r1 + r2 + 1), F(m1 + m2, 2) + 1):
        label = fmt(cand)
        if label != fmt(answer) and label not in alts:
            alts.append(label)
        if len(alts) == 3:
            break
    return q(
        "av_ratio_split", variant, text, answer, alts,
        f"Taking the group sizes as {r1}k and {r2}k, the total is k({weighted}) and the headcount "
        f"is k({r1 + r2}); the average is {weighted}/{r1 + r2} = {fmt(answer)}.",
        {"R1": r1, "R2": r2, "A1": m1, "A2": m2},
    )


AV_CHANGE_ONE = (
    (8, 70, 58, 82, "tracked eight observations", "By how much does the average increase?"),
    (12, 64, 70, 94, "kept twelve figures", "What is the rise in the average?"),
    (10, 75, 50, 90, "checked ten readings", "By how much does the mean go up?"),
    (6, 68, 56, 86, "listed six values", "Find the increase in the average."),
    (8, 70, 42, 98, "noted eight entries", "How much higher is the new average?"),
)


def av_change_one(rng, variant):
    v = variant % 5
    n, avg, old, new, scene, ask = AV_CHANGE_ONE[v]
    name_a, name_b = pair(variant, 3)
    answer = F(new - old, n)
    text = (
        f"{name_a} and {name_b} {scene} whose average is {avg}. One entry is changed from {old} "
        f"to {new}. {ask}"
    )
    alts = []
    for cand in (F(new - old, n - 1), F(new - old, n + 1), answer + 2, F(new - old, n) - 1):
        label = fmt(cand)
        if label != fmt(answer) and label not in alts:
            alts.append(label)
        if len(alts) == 3:
            break
    return q(
        "av_change_one", variant, text, answer, alts,
        f"The total grows by {new - old}, which is shared by {n} entries, so the average increases "
        f"by {new - old}/{n} = {fmt(answer)}.",
        {"N": n, "Avg": avg, "Old": old, "New": new},
    )


AV_GROUP_SIZES = (
    (72, 78, 67, "compared two sections", "What is the ratio of the size of {A}'s group to {B}'s group?"),
    (68, 76, 61, "looked at two teams", "Find the ratio of the numbers in {A}'s group and {B}'s group."),
    (75, 84, 71, "reviewed two batches", "What is the ratio of {A}'s batch size to {B}'s batch size?"),
    (82, 92, 73, "studied two classes", "Determine the ratio of the two group sizes ({A} : {B})."),
    (70, 80, 67, "merged two groups of students", "Find the ratio of students in {A}'s group to {B}'s group."),
)


def av_group_sizes(rng, variant):
    v = variant % 5
    combined, high, low, scene, ask = AV_GROUP_SIZES[v]
    name_a, name_b = pair(variant, 0)
    upper = combined - low
    lower = high - combined
    ratio = ratio_str(upper, lower)
    text = (
        f"{name_a} and {name_b} {scene}. {name_a}'s group averages {high} and {name_b}'s group "
        f"averages {low}; together they average {combined}. {ask.format(A=name_a, B=name_b)}"
    )
    alts = []
    for cand in (ratio_str(lower, upper), ratio_str(upper + 1, lower), ratio_str(upper, lower + 1), ratio_str(upper + 2, lower)):
        if cand != ratio and cand not in alts:
            alts.append(cand)
        if len(alts) == 3:
            break
    return q(
        "av_group_sizes", variant, text, ratio, alts,
        f"If the counts are x and y, x({high} - {combined}) = y({combined} - {low}), so x:y = "
        f"{upper}:{lower}, i.e. {ratio}.",
        {"A1": high, "A2": low, "Combined": combined},
    )


AV_TOTAL_FROM_AVERAGE = (
    (12, 68, "shared twelve equal parcels", "What is the total of all the parcels?"),
    (15, 74, "packed fifteen boxes", "Find the total weight of the boxes."),
    (20, 56, "handled twenty consignments", "What is the combined value of the consignments?"),
    (8, 92, "counted eight sacks", "Determine the total amount in the sacks."),
    (25, 63, "sorted twenty-five packets", "What is the overall total?"),
)


def av_total_from_average(rng, variant):
    v = variant % 5
    n, avg, scene, ask = AV_TOTAL_FROM_AVERAGE[v]
    name_a, name_b = pair(variant, 1)
    answer = n * avg
    text = (
        f"{name_a} and {name_b} {scene}: the average per unit is {avg}. {ask}"
    )
    alts = []
    for cand in (n * (avg + 1), n * (avg - 1), (n + 1) * avg, (n - 1) * avg):
        label = fmt(cand)
        if label != fmt(answer) and label not in alts:
            alts.append(label)
        if len(alts) == 3:
            break
    return q(
        "av_total_from_average", variant, text, answer, alts,
        f"Total = number of units x average = {n} x {avg} = {answer}.",
        {"N": n, "Avg": avg},
    )


AV_CORRECTION = (
    (10, 72, 62, 82, "checked ten entries", "What is the correct average?"),
    (8, 65, 50, 74, "reviewed eight readings", "Find the accurate mean."),
    (12, 58, 88, 64, "audited twelve figures", "What should the average have been?"),
    (15, 80, 70, 100, "verified fifteen scores", "Determine the corrected average."),
    (20, 66, 86, 66, "rechecked twenty values", "What is the right average now?"),
)


def av_correction(rng, variant):
    v = variant % 5
    n, avg, wrong, right, scene, ask = AV_CORRECTION[v]
    name_a, name_b = pair(variant, 2)
    correction = right - wrong
    answer = F(n * avg + correction, n)
    text = (
        f"{name_a} and {name_b} {scene} and got an average of {avg} for {n} entries, but "
        f"the value {wrong} was written instead of {right}. {ask}"
    )
    alts = []
    for cand in (F(avg) + F(correction, n - 1), F(avg) - F(correction, n), F(avg) - F(correction, 2 * n), F(n * avg + 2 * correction, n)):
        label = fmt(cand)
        if label != fmt(answer) and label not in alts:
            alts.append(label)
        if len(alts) == 3:
            break
    return q(
        "av_correction", variant, text, answer, alts,
        f"The total must change by {right} - {wrong} = {correction}; corrected average = "
        f"{avg} + ({correction})/{n} = {fmt(answer)}.",
        {"N": n, "Avg": avg, "Wrong": wrong, "Right": right},
    )


AV_BATTING = (
    ((58, 72, 45, 90, 65), 1, "followed a cricket innings log", "What is the batting average?"),
    ((44, 66, 81, 39, 70, 60), 1, "kept a scorecard of six matches", "Find the batting average."),
    ((102, 48, 75, 63, 92), 1, "reviewed five match scores", "What is the player's average?"),
    ((35, 58, 44, 71, 62), 2, "noted five innings with two not-outs", "Determine the batting average."),
    ((80, 50, 70, 65, 75), 1, "checked five innings of a batter", "What is the runs-per-dismissal average?"),
)


def av_batting(rng, variant):
    v = variant % 5
    runs, not_out, scene, ask = AV_BATTING[v]
    name_a, name_b = pair(variant, 3)
    name_c = third(variant)
    innings = len(runs)
    dismissals = innings - not_out
    total = sum(runs)
    answer_dec = fmt_dec(float(F(total, dismissals)), 2)
    text = (
        f"{name_a}, {name_c} and {name_b} {scene}: the scores were "
        f"{', '.join(str(x) for x in runs)}, with {not_out} not-out innings. {ask}"
    )
    alts = []
    for cand in (F(total, innings), F(total, dismissals + 1), F(total, dismissals - 1), F(total, innings + 1)):
        label = fmt_dec(float(cand), 2)
        if label != answer_dec and label not in alts:
            alts.append(label)
        if len(alts) == 3:
            break
    return q(
        "av_batting", variant, text, answer_dec, alts,
        f"Total runs = {total}; dismissals = {innings} - {not_out} = {dismissals}; "
        f"batting average = {total}/{dismissals} = {answer_dec}.",
        {"Runs": list(runs), "NotOut": not_out},
    )


AV_TEMPERATURE = (
    ((19, 24, 26, 22, 24), "noted five daily temperatures", "What was the average temperature?"),
    ((18, 23, 26, 20, 24, 21), "logged six daily readings", "Find the mean temperature."),
    ((24, 29, 31, 24), "recorded four afternoon temperatures", "What is the average of the readings?"),
    ((16, 21, 23, 18, 20, 17, 18), "tracked seven morning temperatures", "Determine the mean temperature."),
    ((22, 28, 26, 24), "compared four evening readings", "What is the average temperature?"),
)


def av_temperature(rng, variant):
    v = variant % 5
    temps, scene, ask = AV_TEMPERATURE[v]
    name_a, name_b = pair(variant, 0)
    total = sum(temps)
    answer_dec = fmt_dec(float(F(total, len(temps))), 2)
    text = (
        f"{name_a} and {name_b} {scene} in degrees Celsius: {', '.join(str(x) for x in temps)}. {ask}"
    )
    alts = []
    for cand in (F(total, len(temps) - 1), F(total, len(temps) + 1), F(sum(temps[:-1]), len(temps) - 1), F(total + 1, len(temps))):
        label = fmt_dec(float(cand), 2)
        if label != answer_dec and label not in alts:
            alts.append(label)
        if len(alts) == 3:
            break
    return q(
        "av_temperature", variant, text, answer_dec, alts,
        f"The temperatures total {total} over {len(temps)} days, so the mean is "
        f"{total}/{len(temps)} = {answer_dec} degrees.",
        {"Temps": list(temps)},
    )


AV_EXPENDITURE = (
    (4, 35, 120, "shared a house", "What is the average total cost per person?"),
    (5, 42, 180, "split household expenses", "Find the average expense per head."),
    (3, 50, 90, "planned a shared trip", "What is the mean spending per person?"),
    (6, 28, 240, "pooled their daily costs", "Determine the average total per member."),
    (2, 60, 100, "divided a joint bill", "What is the average outlay per person?"),
)


def av_expenditure(rng, variant):
    v = variant % 5
    n, avg, rent, scene, ask = AV_EXPENDITURE[v]
    name_a, name_b = pair(variant, 1)
    share = F(rent, n)
    answer = F(avg) + share
    text = (
        f"{name_a} and {name_b} {scene}: the average of the other costs for {n} people is {avg} "
        f"and a fixed cost of {rent} is split equally among them. {ask}"
    )
    alts = []
    for cand in (F(avg) + F(rent, n + 1), F(avg) + F(rent, n - 1), F(avg) + rent, F(avg) + F(rent, 2 * n)):
        label = fmt(cand)
        if label != fmt(answer) and label not in alts:
            alts.append(label)
        if len(alts) == 3:
            break
    return q(
        "av_expenditure", variant, text, answer, alts,
        f"Each person bears {rent}/{n} = {fmt(share)} of the fixed cost; adding the average of "
        f"{avg} gives {avg} + {fmt(share)} = {fmt(answer)}.",
        {"N": n, "Avg": avg, "Rent": rent},
    )


AV_THREE_GROUPS = (
    (10, 70, 15, 80, 25, 88, "ran three practice groups", "Find the average of all the students."),
    (10, 60, 10, 70, 20, 85, "compared three sections", "What is the combined average?"),
    (12, 55, 18, 65, 30, 75, "reviewed three batches", "Determine the overall mean."),
    (8, 80, 12, 90, 20, 95, "merged three teams", "What is the average of the whole set?"),
    (20, 50, 30, 60, 50, 68, "pooled three classes", "Find the mean of the combined class."),
)


def av_three_groups(rng, variant):
    v = variant % 5
    n1, m1, n2, m2, n3, m3, scene, ask = AV_THREE_GROUPS[v]
    name_a, name_b = pair(variant, 2)
    name_c = third(variant)
    total = n1 * m1 + n2 * m2 + n3 * m3
    headcount = n1 + n2 + n3
    answer = F(total, headcount)
    text = (
        f"{name_a}, {name_c} and {name_b} {scene}: their size-and-average pairs are "
        f"({n1}, {m1}), ({n2}, {m2}) and ({n3}, {m3}). {ask}"
    )
    alts = []
    for cand in (F(m1 + m2 + m3, 3), F(total, headcount - 1), answer + 2, answer - 2):
        label = fmt(cand)
        if label != fmt(answer) and label not in alts:
            alts.append(label)
        if len(alts) == 3:
            break
    return q(
        "av_three_groups", variant, text, answer, alts,
        f"Weighted total = {n1} x {m1} + {n2} x {m2} + {n3} x {m3} = {total}; total size = "
        f"{headcount}; average = {total}/{headcount} = {fmt(answer)}.",
        {"N1": n1, "A1": m1, "N2": n2, "A2": m2, "N3": n3, "A3": m3},
    )


AV_FIND_COUNT = (
    (70, 90, 75, "watched a running average change", "How many values were there before the addition?"),
    (64, 94, 74, "checked a changing set of readings", "Find the original number of readings."),
    (55, 95, 63, "tracked a list after one addition", "What was the initial count?"),
    (70, 94, 74, "noted an average after adding a value", "How many entries were in the list originally?"),
    (45, 80, 50, "reviewed a changed collection", "Determine the original number of values."),
)


def av_find_count(rng, variant):
    v = variant % 5
    avg, added, new_avg, scene, ask = AV_FIND_COUNT[v]
    name_a, name_b = pair(variant, 3)
    answer = F(added - new_avg, new_avg - avg)
    text = (
        f"{name_a} and {name_b} {scene}: the average was {avg} before the value {added} was "
        f"added, and it became {new_avg} afterwards. {ask}"
    )
    alts = []
    for cand in (F(added - new_avg, new_avg - avg + 1), F(added - new_avg + 1, new_avg - avg), F(added - new_avg, new_avg - avg - 1), answer + 1):
        label = fmt(cand)
        if label != fmt(answer) and label not in alts:
            alts.append(label)
        if len(alts) == 3:
            break
    return q(
        "av_find_count", variant, text, answer, alts,
        f"With n original values, (n x {avg} + {added})/(n + 1) = {new_avg}, so "
        f"n = ({added} - {new_avg})/({new_avg} - {avg}) = {fmt(answer)}.",
        {"Avg": avg, "Added": added, "NewAvg": new_avg},
    )


AV_FIND_NEW_VALUE = (
    (5, 70, 72, "had five readings so far", "What must the sixth reading be to reach an average of {t}?"),
    (8, 65, 68, "collected eight scores", "Find the next score needed for an average of {t}."),
    (10, 80, 81, "recorded ten values", "What value is required next to make the average {t}?"),
    (6, 55, 60, "noted six entries", "Determine the seventh entry needed for an average of {t}."),
    (12, 90, 91, "checked twelve marks", "What mark is needed next to lift the average to {t}?"),
)


def av_find_new_value(rng, variant):
    v = variant % 5
    n, avg, target, scene, ask = AV_FIND_NEW_VALUE[v]
    name_a, name_b = pair(variant, 0)
    answer = F((n + 1) * target - n * avg)
    text = (
        f"{name_a} and {name_b} {scene}, and the current average is {avg}. "
        f"{ask.format(t=target)}"
    )
    alts = []
    for cand in (target + F((n - 1) * (target - avg)), answer + 1, answer - 1, target + F(n * (target - avg), 2)):
        label = fmt(cand)
        if label != fmt(answer) and label not in alts:
            alts.append(label)
        if len(alts) == 3:
            break
    return q(
        "av_find_new_value", variant, text, answer, alts,
        f"After {n + 1} values the total must be {n + 1} x {target} = {(n + 1) * target}; "
        f"the existing total is {n} x {avg} = {n * avg}; the next value is "
        f"{(n + 1) * target} - {n * avg} = {answer}.",
        {"N": n, "Avg": avg, "Target": target},
    )


AV_PERCENTAGE_MARKS = (
    ((70, 78, 84, 90, 83), 100, "added up five test marks", "What is the overall percentage?"),
    ((64, 72, 80, 89, 75), 100, "totalled five paper scores", "Find the percentage of marks obtained."),
    ((36, 42, 45, 35, 42), 50, "checked five marks out of fifty", "What percentage did they score?"),
    ((88, 92, 79, 85, 91), 100, "reviewed five unit-test marks", "Determine the aggregate percentage."),
    ((55, 61, 68, 72, 74), 100, "compiled five subject scores", "What is the average percentage?"),
)


def av_percentage_marks(rng, variant):
    v = variant % 5
    marks, maximum, scene, ask = AV_PERCENTAGE_MARKS[v]
    name_a, name_b = pair(variant, 1)
    total = sum(marks)
    full_total = maximum * len(marks)
    answer_dec = fmt_dec(float(F(100 * total, full_total)), 2)
    text = (
        f"{name_a} and {name_b} {scene}: the marks are {', '.join(str(x) for x in marks)}, "
        f"each out of {maximum}. {ask}"
    )
    alts = []
    for cand in (F(total, len(marks)), F(100 * total, full_total - maximum), F(100 * total, full_total + maximum), F(100 * total, full_total) + 5):
        label = fmt_dec(float(cand), 2)
        if label != answer_dec and label not in alts:
            alts.append(label)
        if len(alts) == 3:
            break
    return q(
        "av_percentage_marks", variant, text, answer_dec, alts,
        f"Marks obtained total {total} out of {len(marks)} x {maximum} = {full_total}; "
        f"percentage = 100 x {total}/{full_total} = {answer_dec}%.",
        {"Marks": list(marks), "Max": maximum},
    )


AV_MIXED_SERIES = (
    ((4, 7, 9, 12, 13), 2, 3, "studied a short series", "If each term is multiplied by {s} and then raised by {h}, what is the new average?"),
    ((10, 14, 18, 22), 3, 5, "examined four numbers", "After multiplying every term by {s} and adding {h}, what is the mean?"),
    ((5, 8, 11, 14, 17, 20), 1, 4, "listed six terms", "What is the average after adding {h} to each term (scale {s})?"),
    ((2, 6, 10, 14), 4, 1, "worked on a number list", "Each term is scaled by {s} and increased by {h}; find the new mean."),
    ((15, 20, 25, 30, 35), 2, 10, "reviewed five values", "What is the mean after scaling by {s} and adding {h}?"),
)


def av_mixed_series(rng, variant):
    v = variant % 5
    values, scale, shift, scene, ask = AV_MIXED_SERIES[v]
    name_a, name_b = pair(variant, 2)
    base_mean = F(sum(values), len(values))
    answer = scale * base_mean + shift
    text = (
        f"{name_a} and {name_b} {scene}: {', '.join(str(x) for x in values)}. "
        f"{ask.format(s=scale, h=shift)}"
    )
    alts = []
    for cand in (base_mean, scale * base_mean, base_mean + shift, scale * base_mean - shift, answer + 2, answer - 2):
        label = fmt(cand)
        if label != fmt(answer) and label not in alts:
            alts.append(label)
        if len(alts) == 3:
            break
    return q(
        "av_mixed_series", variant, text, answer, alts,
        f"Original mean = {sum(values)}/{len(values)} = {fmt(base_mean)}; scaling by {scale} and "
        f"adding {shift} gives {scale} x {fmt(base_mean)} + {shift} = {fmt(answer)}.",
        {"Values": list(values), "Scale": scale, "Shift": shift},
    )


AV_COMPARE = (
    (12, 75, 10, 80, "compared two sales teams", "How much greater is {A}'s total than {B}'s total?"),
    (15, 64, 12, 70, "checked two work groups", "By how much does {A}'s total exceed {B}'s total?"),
    (8, 88, 10, 70, "reviewed two counters", "What is the difference between the two totals ({A} minus {B})?"),
    (20, 55, 16, 60, "studied two shifts", "How much larger is {A}'s total compared with {B}'s?"),
    (9, 98, 12, 68, "looked at two batches of work", "Find the excess of {A}'s total over {B}'s total."),
)


def av_compare(rng, variant):
    v = variant % 5
    n1, m1, n2, m2, scene, ask = AV_COMPARE[v]
    name_a, name_b = pair(variant, 3)
    total1 = n1 * m1
    total2 = n2 * m2
    answer = abs(total1 - total2)
    text = (
        f"{name_a} and {name_b} {scene}: {name_a} handled {n1} cases averaging {m1}, while "
        f"{name_b} handled {n2} cases averaging {m2}. {ask.format(A=name_a, B=name_b)}"
    )
    alts = []
    for cand in (total1 + total2, answer + 10, answer - 10, answer + 5):
        label = fmt(cand)
        if label != fmt(answer) and label not in alts:
            alts.append(label)
        if len(alts) == 3:
            break
    return q(
        "av_compare", variant, text, answer, alts,
        f"{name_a}'s total = {n1} x {m1} = {total1}; {name_b}'s total = {n2} x {m2} = {total2}; "
        f"the difference is {total1} - {total2} = {answer}.",
        {"N1": n1, "A1": m1, "N2": n2, "A2": m2},
    )


FAMILIES = [
    av_basic,
    av_two_groups,
    av_replacement,
    av_added_member,
    av_removed_member,
    av_missing_value,
    av_weighted,
    av_age_family,
    av_marks,
    av_consecutive,
    av_ratio_split,
    av_change_one,
    av_group_sizes,
    av_total_from_average,
    av_correction,
    av_batting,
    av_temperature,
    av_expenditure,
    av_three_groups,
    av_find_count,
    av_find_new_value,
    av_percentage_marks,
    av_mixed_series,
    av_compare,
]


def build_average() -> list[tuple[int, str, object, int]]:
    """Return part, difficulty, generator, page-set number for 120 items."""
    return build_specs(FAMILIES)
