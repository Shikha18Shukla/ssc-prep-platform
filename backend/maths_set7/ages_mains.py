# -*- coding: utf-8 -*-
"""Ages (Mains) - 120 original, HARD, multi-step age questions."""

from __future__ import annotations

from math import gcd

from .bank import fmt
from .common import F, NAMES, build_specs, near_num, q, ratio

SOURCE = "Ages Mains class notes (local PDF)"
PAGES = {
    1: '97c1911e-319b-4bc6-8383-48a92c70a378.pdf, pp. 4-5',
    2: '97c1911e-319b-4bc6-8383-48a92c70a378.pdf, pp. 6-7',
    3: '97c1911e-319b-4bc6-8383-48a92c70a378.pdf, pp. 8-9',
    4: '97c1911e-319b-4bc6-8383-48a92c70a378.pdf, pp. 4-10',
}


def _reduced(x, y):
    g = gcd(abs(int(x)), abs(int(y))) or 1
    return int(x) // g, int(y) // g


def _ratio_options(answer):
    first, second = answer.split(":")
    return [f"{second}:{first}", f"{int(first) + 1}:{second}", f"{first}:{int(second) + 1}"]


def _names(v, offset=0):
    n = len(NAMES)
    base = (3 * v + offset) % n
    return NAMES[base], NAMES[(base + 1) % n], NAMES[(base + 2) % n]


def am_three_shift_pair(r, v):
    # Three-person ratio now + shifted pair ratio + weighted linear condition.
    a, b, c, u, shift, pi, pj, w1, w2, w3, extra, ask_kind = (
        (2, 3, 5, 6, -4, 0, 1, 2, 1, 1, 3, "third"),
        (3, 4, 7, 5, 6, 0, 2, 1, 2, 1, -2, "sum"),
        (4, 5, 9, 4, -5, 1, 2, 1, 1, 2, 4, "first"),
        (5, 7, 11, 3, 8, 0, 1, 3, 1, 1, -5, "gap"),
        (3, 8, 13, 2, -3, 0, 2, 1, 1, 3, 6, "second"),
    )[v]
    names = _names(v)
    ages = [a * u, b * u, c * u]
    ref = [age + shift for age in ages]
    p, qv = _reduced(ref[pi], ref[pj])
    weighted = w1 * ages[0] + w2 * ages[1] + w3 * ages[2] + extra
    coefs = {
        "third": [0, 0, 1], "sum": [1, 1, 1], "first": [1, 0, 0],
        "gap": [0, 1, -1], "second": [0, 1, 0],
    }[ask_kind]
    answer = sum(k * age for k, age in zip(coefs, ages))
    asks = {
        "third": f"{names[2]}'s present age",
        "sum": "the sum of the three present ages",
        "first": f"{names[0]}'s present age",
        "gap": "by how many years the second person is younger than the third",
        "second": f"{names[1]}'s present age",
    }
    when = f"{abs(shift)} years ago" if shift < 0 else f"{shift} years from now"
    text = (
        f"The present ages of {names[0]}, {names[1]} and {names[2]} are in the ratio {a}:{b}:{c}. "
        f"{when.capitalize()}, the ratio of {names[pi]}'s age to {names[pj]}'s age became {p}:{qv}. "
        f"If {w1} times {names[0]}'s present age, plus {w2} times {names[1]}'s present age, plus "
        f"{w3} times {names[2]}'s present age is {weighted}, find {asks[ask_kind]}."
    )
    explanation = (
        f"Let present ages be {a}t, {b}t, {c}t. The shifted pair gives t={u}. "
        f"The weighted condition checks as {w1}*{ages[0]}+{w2}*{ages[1]}+{w3}*{ages[2]}={weighted-extra}, "
        f"and with the extra {extra:+d} it becomes {weighted}. Present ages are {ages}; required value is {answer}."
    )
    return q(
        "am_three_shift_pair", v, text, answer, near_num(answer, 3), explanation,
        {"a": a, "b": b, "c": c, "u": u, "shift": shift, "pi": pi, "pj": pj,
         "w": [w1, w2, w3], "extra": extra, "coefs": coefs},
    )


def am_fraction_sum_diff(r, v):
    # Fraction-of-sum + shifted ratio + gap-fraction condition (3 constraints).
    p, qv, u, shift, fn1, fd1, fn2, fd2, ask_kind = (
        (2, 3, 6, 4, 1, 2, 2, 3, "first"),
        (3, 5, 5, -3, 1, 2, 1, 3, "total"),
        (4, 7, 4, 2, 2, 3, 1, 2, "second"),
        (5, 8, 3, 5, 1, 3, 3, 4, "third"),
        (3, 4, 7, -2, 2, 5, 1, 2, "total"),
    )[v]
    names = _names(v, 1)
    y = p * u + shift
    z = qv * u + shift
    x = F(fn1 * (y + z), fd1)
    gap_yz = z - y
    diff_xy = x - y
    delta = diff_xy - F(fn2 * gap_yz, fd2)
    coefs = {"first": [1, 0, 0], "total": [1, 1, 1], "second": [0, 1, 0], "third": [0, 0, 1]}[ask_kind]
    answer = sum(c * val for c, val in zip(coefs, [x, y, z]))
    when = f"{abs(shift)} years ago" if shift > 0 else f"{abs(shift)} years from now"
    asks = {
        "first": f"{names[0]}'s present age",
        "total": "the sum of the three present ages",
        "second": f"{names[1]}'s present age",
        "third": f"{names[2]}'s present age",
    }
    if delta == 0:
        delta_text = f"is {fn2}/{fd2} of the gap between {names[2]} and {names[1]}"
    elif delta > 0:
        delta_text = f"is {fn2}/{fd2} of the gap between {names[2]} and {names[1]}, plus {fmt(delta)} year{'s' if delta != 1 else ''}"
    else:
        delta_text = f"is {fn2}/{fd2} of the gap between {names[2]} and {names[1]}, minus {fmt(abs(delta))} year{'s' if abs(delta) != 1 else ''}"
    text = (
        f"{names[0]}'s present age is {fn1}/{fd1} of the sum of {names[1]}'s and {names[2]}'s present ages. "
        f"{when.capitalize()}, {names[1]} and {names[2]} were in the ratio {p}:{qv}. "
        f"The excess of {names[0]}'s age over {names[1]}'s age {delta_text}. Find {asks[ask_kind]}."
    )
    explanation = (
        f"Let {names[1]}={p}t{shift:+d}, {names[2]}={qv}t{shift:+d}. Condition 1 gives {names[0]}={fmt(x)} at t={u}. "
        f"Condition 2 checks: ({fmt(x)}-{y})={fmt(diff_xy)} and {fn2}/{fd2}*({z}-{y})+{fmt(delta)}={fmt(diff_xy)}. "
        f"Ages are {fmt(x)}, {y}, {z}; required value {answer}."
    )
    return q(
        "am_fraction_sum_diff", v, text, answer, near_num(answer, 3), explanation,
        {"p": p, "q": qv, "u": u, "shift": shift, "fn1": fn1, "fd1": fd1,
         "fn2": fn2, "fd2": fd2, "delta": fmt(delta), "coefs": coefs},
    )


def am_replacement_average(r, v):
    # Average replacement with two events and a target future average.
    n, avg, k, leave_age, join_age, extra_leave, ask_kind = (
        (8, 32, 3, 40, 25, 1, "new_avg"),
        (10, 28, 2, 36, 0, 2, "join_age"),
        (12, 35, 4, 0, 29, 1, "leave_age"),
        (9, 30, 5, 45, 27, 1, "total_now"),
        (11, 26, 3, 38, 0, 2, "join_age"),
    )[v]
    names = _names(v, 2)
    total_now = n * avg
    # after k years, extra_leave people leave and join_age person joins (or solve for unknown)
    if ask_kind == "new_avg":
        # extra_leave leaves at leave_age now? use: after k years all age by k, extra_leave leave with current leave_age+k, one joins with join_age
        total_after = total_now + n * k - extra_leave * (leave_age + k) + join_age
        count_after = n - extra_leave + 1
        answer = F(total_after, count_after)
        leave_word = "member" if extra_leave == 1 else "members"
        text = (
            f"A team of {n} members has average present age {avg}. After {k} years, {extra_leave} {leave_word} aged {leave_age} now leave and "
            f"{names[0]} aged {join_age} joins. Find the average age of the team immediately after this change."
        )
        explanation = (
            f"Present total={n}*{avg}={total_now}. After {k} years total becomes {total_now}+{n}*{k}={total_now+n*k}. "
            f"Leaving members take {extra_leave}*({leave_age}+{k})={extra_leave*(leave_age+k)}; joiner adds {join_age}. "
            f"New total={total_after}, count={count_after}, average={fmt(answer)}."
        )
        vd = {"n": n, "avg": avg, "k": k, "leave_age": leave_age, "join_age": join_age, "extra_leave": extra_leave, "ask": ask_kind}
    elif ask_kind == "join_age":
        # find join_age given target average
        target = avg - 1 if v == 1 else avg - 2
        total_after = total_now + n * k - extra_leave * (leave_age + k)
        count_after = n - extra_leave + 1
        answer = target * count_after - total_after
        text = (
            f"A group of {n} people has average present age {avg}. After {k} years, {extra_leave} members whose present ages average {leave_age} leave. "
            f"A new member {names[1]} joins then, and the group's average becomes {target}. Find {names[1]}'s age at joining."
        )
        explanation = (
            f"After {k} years original total={total_now+n*k}. Departing total={extra_leave}*({leave_age}+{k})={extra_leave*(leave_age+k)}. "
            f"Remaining+joiner count={count_after}, target total={target}*{count_after}={target*count_after}. Joiner age={answer}."
        )
        vd = {"n": n, "avg": avg, "k": k, "leave_age": leave_age, "target": target, "extra_leave": extra_leave, "ask": ask_kind}
    elif ask_kind == "leave_age":
        target = avg + 1
        join_age2 = 29
        count_after = n - extra_leave + 1
        total_after_known = target * count_after - join_age2
        # total_after_known = total_now + n*k - extra_leave*(leave_age+k)
        answer = F(total_now + n * k - total_after_known, extra_leave) - k
        text = (
            f"In a batch of {n} trainees, average present age is {avg}. After {k} years, {extra_leave} trainee(s) leave and one trainee aged {join_age2} joins. "
            f"The average then becomes {target}. Find the present average age of the trainee(s) who left."
        )
        explanation = (
            f"Final total={target}*{count_after}={target*count_after}; before joiner={total_after_known}. "
            f"Original after {k} years={total_now+n*k}. Leaving group at that time={total_now+n*k-total_after_known}={total_now+n*k-total_after_known}, "
            f"so present average leaving age={fmt(answer)}."
        )
        vd = {"n": n, "avg": avg, "k": k, "join_age": join_age2, "target": target, "extra_leave": extra_leave, "ask": ask_kind}
    else:  # total_now
        total_after = total_now + n * k - extra_leave * (leave_age + k) + join_age
        count_after = n - extra_leave + 1
        answer = total_now
        text = (
            f"A committee of {n} members has average present age {avg}. After {k} years, {extra_leave} member aged {leave_age} now leaves and {names[2]} aged {join_age} joins. "
            f"If the resulting average is {fmt(F(total_after, count_after))}, find the present total age of the committee."
        )
        explanation = (
            f"Average {avg} over {n} members means present total={n}*{avg}={total_now}. "
            f"Forward check: after {k} years total {total_now+n*k}, minus leaver {leave_age+k}, plus joiner {join_age} gives {total_after} over {count_after}."
        )
        vd = {"n": n, "avg": avg, "k": k, "leave_age": leave_age, "join_age": join_age, "extra_leave": extra_leave, "ask": ask_kind}
    return q("am_replacement_average", v, text, answer, near_num(answer, 2), explanation, vd)


def am_new_birth_average(r, v):
    # Family average with birth/aging and a later event (second birth or departure).
    n, avg0, k1, k2, ask_kind = (
        (5, 30, 3, 2, "avg"),
        (6, 28, 4, 3, "total"),
        (4, 35, 5, 2, "child_age"),
        (7, 26, 2, 4, "avg"),
        (5, 32, 6, 1, "total"),
    )[v]
    names = _names(v, 3)
    # At t=0, n members avg avg0. After k1 years a child is born (age 0 at birth). After another k2 years, another child born.
    # Ask for average/total/age of first child at final time.
    final_years = k1 + k2
    total_orig = n * (avg0 + final_years)
    child1 = k2  # born at k1, so age k2 at final
    child2 = 0
    count = n + 2
    total = total_orig + child1 + child2
    avg_final = F(total, count)
    if ask_kind == "avg":
        answer = avg_final
        ask = f"the average age of the family at the end of {final_years} years"
    elif ask_kind == "total":
        answer = total
        ask = f"the total age of the family at the end of {final_years} years"
    else:
        answer = child1
        ask = f"the age of {names[0]}'s first child at the end of {final_years} years"
    text = (
        f"A family of {n} members has average present age {avg0}. After {k1} year{'s' if k1!=1 else ''}, a child is born in the family. "
        f"After another {k2} year{'s' if k2!=1 else ''}, a second child is born. Assuming no one else joins or leaves, find {ask}."
    )
    explanation = (
        f"After {final_years} years each original member ages by {final_years}: {n}*({avg0}+{final_years})={total_orig}. "
        f"First child born after {k1} years is now {k2}; second newborn is 0. Total={total_orig}+{child1}+0={total}, "
        f"count={count}, average={fmt(avg_final)}. Required value={answer}."
    )
    return q(
        "am_new_birth_average", v, text, answer, near_num(answer, 2), explanation,
        {"n": n, "avg0": avg0, "k1": k1, "k2": k2, "ask": ask_kind},
    )


def am_reciprocal_product(r, v):
    # Reciprocal condition + product/sum condition + future ratio.
    p, qv, u, k, ask_kind = (
        (2, 3, 6, 5, "older"),
        (3, 5, 4, 6, "younger"),
        (4, 7, 3, 4, "sum"),
        (5, 8, 2, 7, "diff"),
        (3, 4, 5, 8, "older"),
    )[v]
    names = _names(v, 4)
    A, B = p * u, qv * u
    # conditions: 1/A+1/B = (p+q)/(p*q*u), A*B=p*q*u^2, after k years ratio (A+k)/(B+k)
    recip = F(p + qv, p * qv * u)
    prod = p * qv * u * u
    fut_p, fut_q = _reduced(A + k, B + k)
    coefs = {"older": [0, 1], "younger": [1, 0], "sum": [1, 1], "diff": [-1, 1]}[ask_kind]
    answer = coefs[0] * A + coefs[1] * B
    asks = {
        "older": f"{names[1]}'s present age",
        "younger": f"{names[0]}'s present age",
        "sum": "the sum of their present ages",
        "diff": "the difference of their present ages",
    }
    text = (
        f"The present ages of {names[0]} and {names[1]} are in the ratio {p}:{qv}. "
        f"The sum of the reciprocals of their present ages is {fmt(recip)}, and the product of their present ages is {prod}. "
        f"After {k} years, their ages will be in the ratio {fut_p}:{fut_q}. Find {asks[ask_kind]}."
    )
    explanation = (
        f"Let ages be {p}t,{qv}t. Reciprocal gives ( {p}+{qv})/({p*qv}t)={fmt(recip)} => t={u}. "
        f"Product check: {p*u}*{qv*u}={prod}. Future ratio ({A}+{k}):({B}+{k})={fut_p}:{fut_q}. "
        f"Ages {A},{B}; required value {answer}."
    )
    return q(
        "am_reciprocal_product", v, text, answer, near_num(answer, 3), explanation,
        {"p": p, "q": qv, "u": u, "k": k, "coefs": coefs},
    )


def am_admission_service(r, v):
    # Service/joining with ratio at joining, ratio now, service-gap, and sum condition.
    p, qv, u, rr, ss, t, ask_kind = (
        (2, 3, 5, 5, 6, 4, "A_present"),
        (3, 4, 4, 4, 5, 5, "B_join"),
        (1, 2, 7, 3, 4, 6, "present_sum"),
        (2, 5, 3, 4, 7, 5, "A_join"),
        (3, 5, 4, 6, 8, 5, "present_diff"),
    )[v]
    names = _names(v, 5)
    A_join, B_join = p * u, qv * u
    A_now, B_now = rr * t, ss * t
    gap = (A_now - A_join) - (B_now - B_join)  # service difference A-B
    join_sum = A_join + B_join
    present_sum = A_now + B_now
    coefs = {"A_present": [1, 0, 0, 0], "B_join": [0, 0, 0, 1], "present_sum": [1, 1, 0, 0], "A_join": [0, 0, 1, 0], "present_diff": [1, -1, 0, 0]}[ask_kind]
    answer = coefs[0] * A_now + coefs[1] * B_now + coefs[2] * A_join + coefs[3] * B_join
    asks = {
        "A_present": f"{names[0]}'s present age",
        "B_join": f"{names[1]}'s age at joining",
        "present_sum": "the sum of their present ages",
        "A_join": f"{names[0]}'s age at joining",
        "present_diff": "the difference of their present ages",
    }
    gap_text = f"{names[0]} has {gap} more years of service than {names[1]}" if gap >= 0 else f"{names[1]} has {-gap} more years of service than {names[0]}"
    text = (
        f"{names[0]} and {names[1]} joined a service when their ages were in the ratio {p}:{qv}. "
        f"Their present ages are in the ratio {rr}:{ss}. {gap_text}. "
        f"The sum of their ages at joining was {join_sum}, and the sum of their present ages is {present_sum}. Find {asks[ask_kind]}."
    )
    explanation = (
        f"Joining ages {p}u,{qv}u with sum {join_sum} gives u={u}; present ages {rr}t,{ss}t with sum {present_sum} gives t={t}. "
        f"Service gap ({A_now}-{A_join})-({B_now}-{B_join})={gap}. Required value {answer}."
    )
    return q(
        "am_admission_service", v, text, answer, near_num(answer, 3), explanation,
        {"p": p, "q": qv, "u": u, "r": rr, "s": ss, "t": t, "coefs": coefs},
    )


def am_unequal_gaps_ratio(r, v):
    # Unequal time gaps: past ratio, future ratio, and present sum/condition.
    a, b, u, k, m, ask_kind = (
        (2, 3, 8, 4, 6, "first"),
        (3, 5, 7, 6, 9, "sum"),
        (4, 7, 6, 5, 10, "gap"),
        (5, 9, 5, 4, 8, "second"),
        (3, 4, 9, 5, 7, "future_sum"),
    )[v]
    names = _names(v, 6)
    A, B = a * u + k, b * u + k
    past_p, past_q = _reduced(a * u, b * u)
    fut_p, fut_q = _reduced(A + m, B + m)
    present_sum = A + B
    coefs = {"first": [1, 0], "sum": [1, 1], "gap": [-1, 1], "second": [0, 1], "future_sum": [1, 1]}[ask_kind]
    answer = coefs[0] * A + coefs[1] * B + (2 * m if ask_kind == "future_sum" else 0)
    asks = {
        "first": f"{names[0]}'s present age",
        "sum": "the sum of their present ages",
        "gap": f"how many years {names[1]} is older than {names[0]}",
        "second": f"{names[1]}'s present age",
        "future_sum": f"the sum of their ages after {m} years",
    }
    text = (
        f"{k} years ago, the ages of {names[0]} and {names[1]} were in the ratio {past_p}:{past_q}. "
        f"After {m} years from now, their ages will be in the ratio {fut_p}:{fut_q}. "
        f"The sum of their present ages is {present_sum}. Find {asks[ask_kind]}."
    )
    explanation = (
        f"Let ages {k} years ago be {a}u,{b}u with u={u}, so present ages are {A},{B}. "
        f"Check future: ({A}+{m}):({B}+{m})={fut_p}:{fut_q}. Present sum {A}+{B}={present_sum}. Required value {answer}."
    )
    return q(
        "am_unequal_gaps_ratio", v, text, answer, near_num(answer, 3), explanation,
        {"a": a, "b": b, "u": u, "k": k, "m": m, "coefs": coefs, "ask": ask_kind},
    )


def am_hidden_multiple_family(r, v):
    # Father/mother as linear functions of child + shifted ratio + second shifted condition.
    m1, a1, m2, a2, x, s1, s2, ask_kind = (
        (3, 4, 2, 6, 8, 5, 10, "child"),
        (4, -2, 3, 1, 7, 4, 9, "father"),
        (5, 3, 2, 10, 6, -3, 7, "mother"),
        (2, 6, 4, -4, 9, 6, 12, "sum"),
        (6, -5, 3, 8, 5, 5, 11, "gap"),
    )[v]
    names = _names(v, 7)
    father = m1 * x + a1
    mother = m2 * x + a2
    p1, q1 = _reduced(father + s1, mother + s1)
    p2, q2 = _reduced(father + s2, mother + s2)
    coefs = {"child": [1, 0, 0], "father": [0, 1, 0], "mother": [0, 0, 1], "sum": [0, 1, 1], "gap": [0, 1, -1]}[ask_kind]
    answer = coefs[0] * x + coefs[1] * father + coefs[2] * mother
    when1 = f"{abs(s1)} year{'s' if abs(s1)!=1 else ''} from now" if s1 > 0 else f"{abs(s1)} year{'s' if abs(s1)!=1 else ''} ago"
    when2 = f"{abs(s2)} year{'s' if abs(s2)!=1 else ''} from now" if s2 > 0 else f"{abs(s2)} year{'s' if abs(s2)!=1 else ''} ago"
    verb1 = "will be" if s1 > 0 else "was"
    verb2 = "will be" if s2 > 0 else "was"
    f_rel = f"{m1} times {names[2]}'s age {'plus' if a1>=0 else 'minus'} {abs(a1)}"
    m_rel = f"{m2} times {names[2]}'s age {'plus' if a2>=0 else 'minus'} {abs(a2)}"
    asks = {
        "child": f"{names[2]}'s present age",
        "father": f"{names[0]}'s present age",
        "mother": f"{names[1]}'s present age",
        "sum": "the sum of the parents' present ages",
        "gap": f"how many years {names[0]} is older than {names[1]}",
    }
    text = (
        f"{names[0]}'s present age is {f_rel}, and {names[1]}'s present age is {m_rel}. "
        f"{when1.capitalize()}, the ratio of {names[0]}'s age to {names[1]}'s age {verb1} {p1}:{q1}. "
        f"{when2.capitalize()}, that ratio {verb2} {p2}:{q2}. Find {asks[ask_kind]}."
    )
    explanation = (
        f"Let child=x. Father={m1}x{a1:+d}, Mother={m2}x{a2:+d}. "
        f"Shift {s1:+d} gives ({father+s1}):({mother+s1})={p1}:{q1}; shift {s2:+d} gives ({father+s2}):({mother+s2})={p2}:{q2}. "
        f"Solving gives x={x}, father={father}, mother={mother}; required value {answer}."
    )
    return q(
        "am_hidden_multiple_family", v, text, answer, near_num(answer, 3), explanation,
        {"m1": m1, "a1": a1, "m2": m2, "a2": a2, "x": x, "s1": s1, "s2": s2, "coefs": coefs},
    )


def am_group_avg_exit_entry(r, v):
    # Multi-event average: exit + entry + later age shift.
    n, avg, leave_n, leave_avg, join_n, join_avg, k, ask_kind = (
        (10, 40, 2, 32, 1, 25, 3, "avg_after_k"),
        (12, 35, 3, 28, 2, 40, 2, "total_after_k"),
        (9, 44, 1, 38, 2, 50, 4, "count_after"),
        (15, 30, 4, 24, 3, 36, 2, "avg_after_k"),
        (8, 27, 2, 20, 1, 35, 5, "total_after_k"),
    )[v]
    names = _names(v, 8)
    total0 = n * avg
    after_event_total = total0 - leave_n * leave_avg + join_n * join_avg
    count_after = n - leave_n + join_n
    total_after_k = after_event_total + count_after * k
    avg_after_k = F(total_after_k, count_after)
    if ask_kind == "avg_after_k":
        answer = avg_after_k
        ask = f"the average age of the group {k} years after the change"
    elif ask_kind == "total_after_k":
        answer = total_after_k
        ask = f"the total age of the group {k} years after the change"
    else:
        answer = count_after
        ask = "the number of people in the group after the change"
    leave_people = "person" if leave_n == 1 else "people"
    join_people = "person" if join_n == 1 else "people"
    text = (
        f"A group of {n} people has average age {avg}. Then {leave_n} {leave_people} whose average age is {leave_avg} leave, "
        f"and {join_n} new {join_people} whose average age is {join_avg} join. Find {ask}."
    )
    explanation = (
        f"Initial total={n}*{avg}={total0}. After exit/entry: {total0}-{leave_n}*{leave_avg}+{join_n}*{join_avg}={after_event_total}, "
        f"count={count_after}. After {k} years add {count_after}*{k}={count_after*k}: total={total_after_k}, average={fmt(avg_after_k)}. "
        f"Required value {answer}."
    )
    return q(
        "am_group_avg_exit_entry", v, text, answer, near_num(answer, 2), explanation,
        {"n": n, "avg": avg, "leave_n": leave_n, "leave_avg": leave_avg, "join_n": join_n, "join_avg": join_avg, "k": k, "ask": ask_kind},
    )


def am_future_different_pair(r, v):
    # Two ratios at different times plus third-person relation and later ratio.
    a, b, u, k, m, e, base, ask_kind = (
        (3, 4, 6, 4, 6, 5, "A", "C"),
        (2, 5, 5, 3, 5, -4, "B", "A"),
        (4, 7, 4, 5, 8, 6, "A", "sum"),
        (5, 8, 3, 6, 4, -3, "B", "gap"),
        (3, 5, 7, 2, 9, 7, "A", "B"),
    )[v]
    names = _names(v, 9)
    A, B = a * u, b * u
    C = (A if base == "A" else B) + e
    past_p, past_q = _reduced(A - k, B - k)
    fut_p, fut_q = _reduced((B if ask_kind != 'A' else A) + m, C + m) if ask_kind in ('C','sum','gap','B') else _reduced(A+m, C+m)
    # choose pair for future ratio consistently: A:C
    fut_p, fut_q = _reduced(A + m, C + m)
    coefs = {"A": [1, 0, 0], "B": [0, 1, 0], "C": [0, 0, 1], "sum": [1, 1, 1], "gap": [0, 1, -1]}[ask_kind]
    answer = coefs[0] * A + coefs[1] * B + coefs[2] * C
    asks = {"A": f"{names[0]}'s present age", "B": f"{names[1]}'s present age", "C": f"{names[2]}'s present age", "sum": "the sum of the three present ages", "gap": f"by how many years {names[1]} is older than {names[2]}"}
    rel = f"{abs(e)} years {'older' if e>0 else 'younger'} than {names[0] if base=='A' else names[1]}"
    text = (
        f"The present ages of {names[0]} and {names[1]} are in the ratio {a}:{b}. "
        f"{k} years ago, their ages were in the ratio {past_p}:{past_q}. "
        f"{names[2]} is presently {rel}. After {m} years, the ratio of {names[0]}'s age to {names[2]}'s age will be {fut_p}:{fut_q}. "
        f"Find {asks[ask_kind]}."
    )
    explanation = (
        f"From present ratio and {k}-years-ago ratio, {a}u:{b}u with u={u} gives A={A}, B={B}. "
        f"{names[2]}={C} from relation to {base}. Future A:C check ({A+m}):({C+m})={fut_p}:{fut_q}. Required value {answer}."
    )
    return q(
        "am_future_different_pair", v, text, answer, near_num(answer, 3), explanation,
        {"a": a, "b": b, "u": u, "k": k, "m": m, "e": e, "base": base, "coefs": coefs},
    )


def am_percentage_ages(r, v):
    # Percentage relation + two time shifts + sum condition.
    p, u, k1, k2, anchor, ask_kind = (
        (60, 25, 5, 8, "A_of_B", "B"),
        (40, 30, 6, 4, "A_of_B", "A"),
        (50, 36, 6, 9, "B_of_A", "sum"),
        (25, 40, 5, 10, "B_of_A", "diff"),
        (75, 28, 4, 7, "A_of_B", "A"),
    )[v]
    names = _names(v, 10)
    if anchor == "A_of_B":
        A, B = F(p * u, 100), F(u)
    else:
        A, B = F(u), F(p * u, 100)
    # two conditions: k1 years ago ratio/percentage and k2 years hence ratio
    past_p, past_q = _reduced(A - k1, B - k1)
    fut_p, fut_q = _reduced(A + k2, B + k2)
    coefs = {"A": [1, 0], "B": [0, 1], "sum": [1, 1], "diff": [1, -1]}[ask_kind]
    answer = coefs[0] * A + coefs[1] * B
    asks = {"A": f"{names[0]}'s present age", "B": f"{names[1]}'s present age", "sum": "the sum of their present ages", "diff": "the difference of their present ages"}
    present = f"{names[0]}'s present age is {p}% of {names[1]}'s present age" if anchor == "A_of_B" else f"{names[1]}'s present age is {p}% of {names[0]}'s present age"
    text = (
        f"{present}. {k1} years ago, the ratio of their ages was {past_p}:{past_q}. "
        f"After {k2} years, the ratio of their ages will be {fut_p}:{fut_q}. Find {asks[ask_kind]}."
    )
    explanation = (
        f"From percentage, let base be {u} giving ages {fmt(A)},{fmt(B)}. "
        f"Past check ({fmt(A-k1)}):({fmt(B-k1)})={past_p}:{past_q}; future check ({fmt(A+k2)}):({fmt(B+k2)})={fut_p}:{fut_q}. "
        f"Required value {answer}."
    )
    return q(
        "am_percentage_ages", v, text, answer, near_num(answer, 3), explanation,
        {"p": p, "u": u, "k1": k1, "k2": k2, "anchor": anchor, "coefs": coefs},
    )


def am_simultaneous_linear(r, v):
    # Two linear equations with time shifts - classic hard algebra.
    A, B, c1, d1, c2, d2, s1, s2, s3, ask_kind = (
        (17, 9, 2, 3, 5, -4, 3, 4, 2, "A"),
        (23, 11, 3, 2, 4, -5, 2, 3, 1, "B"),
        (14, 20, 5, 2, 3, -1, 1, 2, 0, "sum"),
        (31, 13, 4, 3, 7, -2, 4, 1, 3, "diff"),
        (19, 27, 2, 5, 6, -1, 2, 3, 1, "A"),
    )[v]
    names = _names(v, 11)
    # eq1: c1*(A-s1)+d1*(B-s2)=e1
    e1 = c1 * (A - s1) + d1 * (B - s2)
    # eq2: c2*A + d2*(B+s3)=e2 (d2 may be negative)
    e2 = c2 * A + d2 * (B + s3)
    coefs = {"A": [1, 0], "B": [0, 1], "sum": [1, 1], "diff": [1, -1]}[ask_kind]
    answer = coefs[0] * A + coefs[1] * B
    asks = {"A": f"{names[0]}'s present age", "B": f"{names[1]}'s present age", "sum": "the sum of their present ages", "diff": "the difference of their present ages"}
    s1_txt = f"{s1} year{'s' if s1!=1 else ''} ago" if s1 else "now"
    s2_txt = f"{s2} year{'s' if s2!=1 else ''} ago" if s2 else "now"
    s3_txt = f"{s3} year{'s' if s3!=1 else ''} from now" if s3 else "present age"
    if s3:
        second_term = f"{'minus' if d2<0 else 'plus'} {abs(d2)} times {names[1]}'s age {s3_txt}"
    else:
        second_term = f"{'minus' if d2<0 else 'plus'} {abs(d2)} times {names[1]}'s {s3_txt}"
    text = (
        f"{c1} times {names[0]}'s age {s1_txt} plus {d1} times {names[1]}'s age {s2_txt} is {e1}. "
        f"Also, {c2} times {names[0]}'s present age {second_term} is {e2}. "
        f"Find {asks[ask_kind]}."
    )
    det = c1 * d2 - c2 * d1
    rhs1 = e1 + c1 * s1 + d1 * s2
    rhs2 = e2 - d2 * s3
    explanation = (
        f"Let present ages be x,y. Eq1: {c1}x+{d1}y={rhs1}. Eq2: {c2}x+{d2}y={rhs2}. "
        f"Solving gives x={A}, y={B}. Required value {answer}."
    )
    return q(
        "am_simultaneous_linear", v, text, answer, near_num(answer, 3), explanation,
        {"c1": c1, "d1": d1, "c2": c2, "d2": d2, "rhs1": rhs1, "rhs2": rhs2, "coefs": coefs},
    )


def am_three_time_chain(r, v):
    # Three people: past ratio A:B, present gap for C, future ratio involving C, plus sum.
    a, b, u, k, gap, m, ask_kind = (
        (2, 3, 6, 4, 5, 7, "A"),
        (3, 5, 5, 3, -4, 6, "C"),
        (4, 7, 4, 5, 9, 8, "sum"),
        (5, 8, 3, 6, -6, 4, "gapBC"),
        (3, 4, 8, 2, 7, 9, "future_C"),
    )[v]
    names = _names(v, 12)
    A, B = a * u + k, b * u + k
    C = B + gap
    past_p, past_q = _reduced(a * u, b * u)
    fut_p, fut_q = _reduced(A + m, C + m)
    total = A + B + C
    if ask_kind == "A":
        answer = A
    elif ask_kind == "C":
        answer = C
    elif ask_kind == "sum":
        answer = total
    elif ask_kind == "gapBC":
        answer = B - C
    else:
        answer = C + m
    asks = {"A": f"{names[0]}'s present age", "C": f"{names[2]}'s present age", "sum": "the sum of the three present ages", "gapBC": f"by how many years {names[1]} is older than {names[2]}", "future_C": f"{names[2]}'s age after {m} years"}
    rel = f"{abs(gap)} years {'older' if gap>0 else 'younger'} than {names[1]}"
    text = (
        f"{k} years ago, the ages of {names[0]} and {names[1]} were in the ratio {past_p}:{past_q}. "
        f"At present, {names[2]} is {rel}. After {m} years, the ratio of {names[0]}'s age to {names[2]}'s age will be {fut_p}:{fut_q}. "
        f"The sum of their present ages is {total}. Find {asks[ask_kind]}."
    )
    explanation = (
        f"Past ages {a}u,{b}u with u={u} give present A={A}, B={B}; C=B{gap:+d}={C}. "
        f"Future A:C ({A+m}):({C+m})={fut_p}:{fut_q}. Sum {total}. Required value {answer}."
    )
    return q(
        "am_three_time_chain", v, text, answer, near_num(answer, 3), explanation,
        {"a": a, "b": b, "u": u, "k": k, "gap": gap, "m": m, "ask": ask_kind},
    )


def am_average_subset(r, v):
    # Subset averages with removal/replacement and a future average condition.
    n, avg, t, old_avg, s, young_avg, k, ask_kind = (
        (7, 32, 2, 45, 2, 20, 3, "middle"),
        (9, 34, 3, 46, 2, 22, 4, "middle_future"),
        (8, 36, 2, 50, 3, 24, 0, "extremes_total"),
        (10, 29, 3, 40, 2, 18, 0, "avg_remaining"),
        (11, 31, 3, 44, 4, 21, 2, "total_future"),
    )[v]
    names = _names(v, 13)
    total = n * avg
    middle = total - t * old_avg - s * young_avg
    rem_count = n - t - s
    if ask_kind == "middle":
        answer = middle
    elif ask_kind == "middle_future":
        answer = middle + rem_count * k
    elif ask_kind == "extremes_total":
        answer = t * old_avg + s * young_avg
    elif ask_kind == "avg_remaining":
        answer = F(middle, rem_count)
    else:
        answer = total + n * k
    asks = {
        "middle": f"the total present age of the remaining {rem_count} member(s)",
        "middle_future": f"the total age of the remaining {rem_count} member(s) after {k} years",
        "extremes_total": "the combined present age of the oldest and youngest selected members",
        "avg_remaining": f"the average present age of the remaining {rem_count} member(s)",
        "total_future": f"the total age of the whole group after {k} years",
    }
    text = (
        f"A group of {n} people has average present age {avg}. The average age of the {t} oldest members is {old_avg}, "
        f"and the average age of the {s} youngest members is {young_avg}. "
        f"If the whole group ages by {k} years, find {asks[ask_kind]}."
    )
    explanation = (
        f"Total={n}*{avg}={total}. Oldest subtotal={t}*{old_avg}={t*old_avg}, youngest subtotal={s}*{young_avg}={s*young_avg}. "
        f"Remaining {rem_count} members total {middle}. After {k} years whole total {total+n*k}, remaining total {middle+rem_count*k}. "
        f"Required value {answer}."
    )
    return q(
        "am_average_subset", v, text, answer, near_num(answer, 2), explanation,
        {"n": n, "avg": avg, "t": t, "old": old_avg, "s": s, "young": young_avg, "k": k, "rem_count": rem_count, "ask": ask_kind},
    )


def am_ratio_change_find_time(r, v):
    # Present ratio+sum, past/future ratio, and ask for time/age with verification.
    p, qv, total, rr, ss, direction, ask_kind = (
        (2, 5, 49, 1, 2, "future", "years"),
        (2, 5, 49, 1, 4, "past", "years"),
        (3, 7, 60, 1, 2, "future", "age"),
        (5, 4, 72, 6, 5, "future", "sum_after"),
        (3, 5, 64, 1, 2, "past", "age_at_reference"),
    )[v]
    names = _names(v, 14)
    A = F(p * total, p + qv)
    B = F(qv * total, p + qv)
    if direction == "future":
        k = F(ss * A - rr * B, rr - ss)
    else:
        k = F(ss * A - rr * B, ss - rr)
    if ask_kind == "years":
        answer = k
    elif ask_kind == "age":
        answer = A + k if direction == "future" else A - k
    elif ask_kind == "sum_after":
        answer = A + B + 2 * k
    else:
        answer = A - k
    asks = {
        "years": f"the number of years {'from now' if direction=='future' else 'ago'} when the ratio becomes {rr}:{ss}",
        "age": f"{names[0]}'s age at that time",
        "sum_after": "the sum of their ages at that time",
        "age_at_reference": f"{names[0]}'s age at that earlier time",
    }
    text = (
        f"The present ages of {names[0]} and {names[1]} are in the ratio {p}:{qv} and their sum is {total}. "
        f"The ratio of their ages {'after some years' if direction=='future' else 'some years ago'} becomes {rr}:{ss}. "
        f"If {names[1]} is currently {fmt(B)} years old, find {asks[ask_kind]}."
    )
    explanation = (
        f"Present ages are {fmt(A)} and {fmt(B)}. Solving ({fmt(A)}{'+' if direction=='future' else '-'}k)/({fmt(B)}{'+' if direction=='future' else '-'}k)={rr}/{ss} gives k={fmt(k)}. "
        f"Required value {answer}."
    )
    return q(
        "am_ratio_change_find_time", v, text, answer, near_num(answer, 2), explanation,
        {"p": p, "q": qv, "total": total, "r": rr, "s": ss, "direction": direction, "ask": ask_kind},
    )


def am_two_future_conditions(r, v):
    # Two future ratios and a present gap/sum constraint.
    a, b, m, c2, d2, n, mode, u, ask_kind = (
        (2, 3, 5, 2, 3, 7, "AC", 19, "B"),
        (3, 4, 4, 2, 3, 6, "BC", 17, "C"),
        (4, 5, 6, 3, 5, 8, "AC", 22, "sum"),
        (2, 5, 3, 4, 5, 5, "BC", 17, "B"),
        (5, 6, 5, 2, 3, 7, "AC", 25, "gap"),
    )[v]
    names = _names(v, 15)
    A = F(u)
    B = F(b * (A + m), a) - m
    C_base = A if mode == "AC" else B
    C = F(d2 * (C_base + n), c2) - n
    gap = C - C_base
    coefs = {"B": [0, 1, 0], "C": [0, 0, 1], "sum": [1, 1, 1], "gap": [0, -1, 1]}[ask_kind]
    answer = coefs[0] * A + coefs[1] * B + coefs[2] * C
    asks = {"B": f"{names[1]}'s present age", "C": f"{names[2]}'s present age", "sum": "the sum of the three present ages", "gap": f"by how many years {names[2]} is older than {names[1]}"}
    text = (
        f"After {m} years, the ratio of {names[0]}'s age to {names[1]}'s age will be {a}:{b}. "
        f"After {n} years, the ratio of {names[0] if mode=='AC' else names[1]}'s age to {names[2]}'s age will be {c2}:{d2}. "
        f"Presently, {names[2]} is {fmt(gap)} years older than {names[0] if mode=='AC' else names[1]}. "
        f"If {names[0]}'s present age is {fmt(A)}, find {asks[ask_kind]}."
    )
    explanation = (
        f"Using A={fmt(A)} in future ratio 1 gives B={fmt(B)}. Using {mode} future ratio gives C={fmt(C)}. "
        f"Gap C-base={fmt(gap)} matches. Required value {answer}."
    )
    return q(
        "am_two_future_conditions", v, text, answer, near_num(answer, 3), explanation,
        {"a": a, "b": b, "m": m, "c2": c2, "d2": d2, "n": n, "mode": mode, "u": u, "coefs": coefs},
    )


def am_joining_service_two(r, v):
    # Two people joining service at different times with present ratio and service-sum constraint.
    gap, p, qv, lag, x, ask_kind = (
        (12, 5, 3, 4, 10, "service_A"),
        (9, 4, 3, 6, 15, "join_B"),
        (10, 3, 2, 3, 12, "total_service"),
        (15, 7, 4, 5, 12, "A_present"),
        (8, 5, 3, 2, 7, "join_A"),
    )[v]
    names = _names(v, 16)
    A = F(gap * p, p - qv)
    B = F(gap * qv, p - qv)
    joinA = x
    joinB = x + lag - gap
    servA = A - joinA
    servB = B - joinB
    join_sum = joinA + joinB
    coefs = {"service_A": [0, 0, 1, 0, 0], "join_B": [0, 1, 0, 0, 0], "total_service": [0, 0, 1, 1, 0], "A_present": [0, 0, 0, 0, 1], "join_A": [1, 0, 0, 0, 0]}[ask_kind]
    answer = coefs[0] * joinA + coefs[1] * joinB + coefs[2] * servA + coefs[3] * servB + coefs[4] * A
    asks = {
        "service_A": f"the number of years {names[0]} has served",
        "join_B": f"{names[1]}'s age at joining",
        "total_service": "the sum of their years of service",
        "A_present": f"{names[0]}'s present age",
        "join_A": f"{names[0]}'s age at joining",
    }
    text = (
        f"{names[0]} is {gap} years older than {names[1]}, and their present ages are in the ratio {p}:{qv}. "
        f"{names[1]} joined service {lag} years after {names[0]}. The sum of their ages at the time of joining was {fmt(join_sum)}. "
        f"Find {asks[ask_kind]}."
    )
    explanation = (
        f"From age gap and ratio, A={fmt(A)}, B={fmt(B)}. If {names[0]} joined at {joinA}, {names[1]} joined at {joinB}; sum {fmt(join_sum)} matches. "
        f"Service years are {fmt(servA)} and {fmt(servB)}. Required value {answer}."
    )
    return q(
        "am_joining_service_two", v, text, answer, near_num(answer, 3), explanation,
        {"gap": gap, "p": p, "q": qv, "lag": lag, "x": x, "coefs": coefs},
    )


def am_fraction_two_conditions(r, v):
    # Two fraction conditions among three ages plus total and a future ratio check.
    k, m, t, mode, ask_kind = (
        (2, 3, 5, "sum", "A"),
        (3, 2, 6, "sum", "B"),
        (4, 3, 4, "diff", "C"),
        (2, 5, 3, "diff", "total"),
        (3, 4, 5, "sum", "ratio"),
    )[v]
    names = _names(v, 17)
    if mode == "sum":
        A, B, C = (m + 1) * t, (k + 1) * t, (k * m - 1) * t
    else:
        A, B, C = (m - 1) * t, (k - 1) * t, (k * m - 1) * t
    total = A + B + C
    fut_p, fut_q = _reduced(A + 5, B + 5)
    if ask_kind == "ratio":
        answer = ratio(A, B)
        distractors = _ratio_options(answer)
    else:
        coefs = {"A": [1, 0, 0], "B": [0, 1, 0], "C": [0, 0, 1], "total": [1, 1, 1]}[ask_kind]
        answer = coefs[0] * A + coefs[1] * B + coefs[2] * C
        distractors = near_num(answer, 3)
    if mode == "sum":
        rel1 = f"{names[0]}'s age is 1/{k} of the sum of {names[1]}'s and {names[2]}'s ages"
        rel2 = f"{names[1]}'s age is 1/{m} of the sum of {names[0]}'s and {names[2]}'s ages"
    else:
        rel1 = f"{names[0]}'s age is 1/{k} of the excess of {names[2]}'s age over {names[1]}'s age"
        rel2 = f"{names[1]}'s age is 1/{m} of the excess of {names[2]}'s age over {names[0]}'s age"
    asks = {"A": f"{names[0]}'s age", "B": f"{names[1]}'s age", "C": f"{names[2]}'s age", "total": "the total of the three ages", "ratio": f"the ratio {names[0]}:{names[1]}"}
    text = (
        f"{rel1.capitalize()}, and {rel2}. The sum of the three ages is {total}. "
        f"After 5 years, the ratio of {names[0]}'s age to {names[1]}'s age will be {fut_p}:{fut_q}. Find {asks[ask_kind]}."
    )
    explanation = (
        f"Translate both fraction conditions and total={total} to get A={A}, B={B}, C={C}. "
        f"Future check ({A+5}):({B+5})={fut_p}:{fut_q}. Required value {answer}."
    )
    return q(
        "am_fraction_two_conditions", v, text, answer, distractors, explanation,
        {"k": k, "m": m, "t": t, "mode": mode, "ask": ask_kind},
    )


def am_percentage_change_average(r, v):
    # Average changes with aging, exits/entries, and reverse unknown count.
    n, avg, k, t, x_avg, mode, ask_kind = (
        (10, 30, 2, 2, 25, "leave", "count"),
        (8, 34, 3, 2, 40, "join", "total"),
        (12, 28, 1, 3, 22, "leave", "avg"),
        (9, 31, 4, 3, 47, "join", "remaining"),
        (15, 26, 2, 4, 31, "leave", "count"),
    )[v]
    names = _names(v, 18)
    aged = n * (avg + k)
    if mode == "leave":
        total_after = aged - t * x_avg
        count_after = n - t
    else:
        total_after = aged + t * x_avg
        count_after = n + t
    new_avg = F(total_after, count_after)
    if ask_kind == "count":
        answer = t
    elif ask_kind == "remaining":
        answer = count_after
    elif ask_kind == "total":
        answer = total_after
    else:
        answer = new_avg
    event = f"{t} members whose average age is {x_avg} leave" if mode == "leave" else f"{t} new members whose average age is {x_avg} join"
    asks = {"count": "the number of members who left/joined", "remaining": "the number of members after the change", "total": "the total age after the change", "avg": "the new average age"}
    text = (
        f"A group of {n} people has average present age {avg}. After {k} year{'s' if k!=1 else ''}, {event}. "
        f"As a result, the average age becomes {fmt(new_avg)}. Find {asks[ask_kind]}."
    )
    explanation = (
        f"After {k} years original total={n}*({avg}+{k})={aged}. Event gives total {total_after} over {count_after} members, "
        f"average {fmt(new_avg)}. Required value {answer}."
    )
    return q(
        "am_percentage_change_average", v, text, answer, near_num(answer, 2), explanation,
        {"n": n, "avg": avg, "k": k, "t": t, "x_avg": x_avg, "mode": mode, "ask": ask_kind},
    )


def am_reciprocal_sum_diff(r, v):
    # Sum/diff/product/reciprocal conditions leading to quadratic-like but integer solution.
    s, diff, k, ask_kind = (
        (52, 14, 6, "elder"),
        (60, 8, 5, "younger"),
        (48, 12, 4, "sum_after"),
        (70, 10, 3, "product"),
        (44, 6, 8, "ratio_future"),
    )[v]
    names = _names(v, 19)
    elder = F(s + diff, 2)
    younger = F(s - diff, 2)
    product = elder * younger
    fut_p, fut_q = _reduced(elder + k, younger + k)
    if ask_kind == "elder":
        answer = elder
        distractors = near_num(answer, 2)
    elif ask_kind == "younger":
        answer = younger
        distractors = near_num(answer, 2)
    elif ask_kind == "sum_after":
        answer = elder + younger + 2 * k
        distractors = near_num(answer, 2)
    elif ask_kind == "product":
        answer = product
        distractors = near_num(answer, 4)
    else:
        answer = f"{fut_p}:{fut_q}"
        distractors = _ratio_options(answer)
    asks = {"elder": f"{names[1]}'s present age", "younger": f"{names[0]}'s present age", "sum_after": f"the sum of their ages after {k} years", "product": "the product of their present ages", "ratio_future": f"the ratio of their ages after {k} years"}
    if ask_kind in ("elder", "younger", "product"):
        text = (
            f"The sum of the present ages of {names[0]} and {names[1]} is {s}, and the difference of their ages is {diff}. "
            f"The product of their present ages is {fmt(product)}. Find {asks[ask_kind]}."
        )
    else:
        text = (
            f"The sum of the present ages of {names[0]} and {names[1]} is {s}, and the difference of their ages is {diff}. "
            f"The product of their present ages is {fmt(product)}. After {k} years, find {asks[ask_kind]}."
        )
    explanation = (
        f"From sum/diff: elder=( {s}+{diff})/2={fmt(elder)}, younger=( {s}-{diff})/2={fmt(younger)}. "
        f"Product check {fmt(elder)}*{fmt(younger)}={fmt(product)}. After {k} years ages {fmt(elder+k)},{fmt(younger+k)}. Required value {answer}."
    )
    return q(
        "am_reciprocal_sum_diff", v, text, answer, distractors, explanation,
        {"s": s, "d": diff, "k": k, "ask": ask_kind},
    )


def am_exam_eligibility(r, v):
    # Eligibility/cutoff with ratio history, future eligibility, and minimum wait.
    p, qv, u, k, limit, extra_years, ask_kind = (
        (2, 1, 9, 4, 25, 3, "years"),
        (3, 2, 7, 3, 30, 2, "years"),
        (4, 3, 6, 5, 27, 4, "age"),
        (5, 3, 5, 4, 28, 1, "age"),
        (3, 1, 8, 6, 21, 2, "years"),
    )[v]
    names = _names(v, 20)
    A, B = p * u + k, qv * u + k  # present ages
    elder, younger = max(A, B), min(A, B)
    # extra condition: after extra_years, elder will be limit+extra_years? use as check
    fut_elder = elder + extra_years
    target_age = limit
    years_wait = max(0, target_age - younger)
    if ask_kind == "years":
        answer = years_wait
        ask = f"how many more years {names[1] if B<=A else names[0]} must wait to become eligible"
    else:
        answer = younger
        ask = f"the present age of the younger candidate"
    text = (
        f"{k} years ago, the ages of {names[0]} and {names[1]} were in the ratio {p}:{qv}. "
        f"After {extra_years} year{'s' if extra_years!=1 else ''} from now, the elder candidate will be {fmt(fut_elder)} years old. "
        f"The minimum eligibility age for an exam is {limit} years. Find {ask}."
    )
    explanation = (
        f"Past ages {p*u},{qv*u} give present ages {A},{B}. Elder is {elder}; after {extra_years} years {fut_elder} matches. "
        f"Younger is {younger}, so wait for limit {limit} is {years_wait}. Required value {answer}."
    )
    return q(
        "am_exam_eligibility", v, text, answer, near_num(answer, 2), explanation,
        {"p": p, "q": qv, "u": u, "k": k, "limit": limit, "extra_years": extra_years, "ask": ask_kind},
    )


def am_time_triple_ratio(r, v):
    # Three-person chained ratios with a sum and a shifted ratio.
    a, b, c, d, t, k, ask_kind = (
        (2, 3, 3, 5, 6, 4, "B"),
        (3, 4, 2, 3, 5, 5, "C"),
        (4, 5, 5, 6, 3, 3, "total"),
        (5, 7, 4, 5, 4, 6, "A"),
        (3, 5, 2, 3, 6, 2, "future_total"),
    )[v]
    names = _names(v, 21)
    A, B, C = a * t, b * t, F(d * b * t, c)
    fut_p, fut_q = _reduced(A + k, C + k)
    if ask_kind == "A":
        answer = A
    elif ask_kind == "B":
        answer = B
    elif ask_kind == "C":
        answer = C
    elif ask_kind == "total":
        answer = A + B + C
    else:
        answer = A + B + C + 3 * k
    asks = {"A": f"{names[0]}'s present age", "B": f"{names[1]}'s present age", "C": f"{names[2]}'s present age", "total": "the sum of their present ages", "future_total": f"the sum of their ages after {k} years"}
    text = (
        f"The present ages of {names[0]} and {names[1]} are in the ratio {a}:{b}, and the present ages of {names[1]} and {names[2]} are in the ratio {c}:{d}. "
        f"The sum of {names[0]}'s and {names[2]}'s present ages is {fmt(A+C)}. After {k} years, the ratio of {names[0]}'s age to {names[2]}'s age will be {fut_p}:{fut_q}. "
        f"Find {asks[ask_kind]}."
    )
    explanation = (
        f"Let A={a}t,B={b}t, then C={d}/{c}*{b}t={fmt(C)}. A+C={fmt(A+C)} gives t={t}. "
        f"Ages {fmt(A)},{fmt(B)},{fmt(C)}. Future A:C ({fmt(A+k)}):({fmt(C+k)})={fut_p}:{fut_q}. Required value {answer}."
    )
    return q(
        "am_time_triple_ratio", v, text, answer, near_num(answer, 3), explanation,
        {"a": a, "b": b, "c": c, "d": d, "t": t, "k": k, "ask": ask_kind},
    )


def am_future_family_average(r, v):
    # Family average over time with birth and leaving, ask future average/total.
    n, avg, k, born, leave_age, ask_kind = (
        (6, 28, 3, 1, 40, "avg"),
        (8, 30, 2, 0, 36, "total"),
        (5, 34, 4, 2, 45, "count"),
        (9, 26, 5, 1, 38, "avg"),
        (7, 32, 3, 1, 37, "total"),
    )[v]
    names = _names(v, 22)
    # at k years: original n age by k, 'born' newborns (age 0) added, one person of present leave_age leaves (so leave_age+k)
    leaving = 1 if leave_age > 0 else 0
    total_after = n * (avg + k) - leaving * (leave_age + k) + 0 * born
    count_after = n + born - leaving
    avg_after = F(total_after, count_after)
    if ask_kind == "avg":
        answer = avg_after
        ask = f"the average age of the family after {k} years"
    elif ask_kind == "total":
        answer = total_after
        ask = f"the total age of the family after {k} years"
    else:
        answer = count_after
        ask = f"the number of family members after {k} years"
    born_text = f", {born} child{'ren are' if born!=1 else ' is'} born during this period" if born else ""
    leave_text = f", and one member who is {leave_age} years old now leaves at the end of {k} years" if leaving else ""
    text = (
        f"A family of {n} members has average present age {avg}. After {k} years{born_text}{leave_text}. "
        f"Find {ask}."
    )
    explanation = (
        f"Original after {k} years: {n}*({avg}+{k})={n*(avg+k)}. "
        f"Leaving member at that time: {leaving*(leave_age+k)}. Newborns contribute 0. "
        f"Total={total_after}, count={count_after}, average={fmt(avg_after)}. Required value {answer}."
    )
    return q(
        "am_future_family_average", v, text, answer, near_num(answer, 2), explanation,
        {"n": n, "avg": avg, "k": k, "born": born, "leave_age": leave_age, "leaving": leaving, "ask": ask_kind},
    )


def am_linear_combo_ratio(r, v):
    # Past ratio + weighted linear combo + future ratio condition.
    p, qv, u, ca, cb, k, m, ask_kind = (
        (2, 3, 7, 3, 4, 5, 6, "A"),
        (4, 5, 6, 2, 3, 4, 8, "B"),
        (3, 7, 5, 5, 2, 6, 4, "sum"),
        (5, 8, 4, 4, 3, 3, 7, "diff"),
        (2, 5, 8, 1, 2, 7, 5, "older"),
    )[v]
    names = _names(v, 23)
    A_past, B_past = p * u, qv * u
    A, B = A_past + k, B_past + k
    weighted = ca * A_past + cb * B_past
    fut_p, fut_q = _reduced(A + m, B + m)
    coefs = {"A": [1, 0], "B": [0, 1], "sum": [1, 1], "diff": [-1, 1], "older": [0, 1]}[ask_kind]
    answer = coefs[0] * A + coefs[1] * B
    asks = {"A": f"{names[0]}'s present age", "B": f"{names[1]}'s present age", "sum": "the sum of their present ages", "diff": "the difference of their present ages", "older": "the present age of the elder person"}
    text = (
        f"{k} years ago, the ages of {names[0]} and {names[1]} were in the ratio {p}:{qv}. "
        f"At that time, {ca} times {names[0]}'s age plus {cb} times {names[1]}'s age was {weighted}. "
        f"After {m} years from now, their ages will be in the ratio {fut_p}:{fut_q}. Find {asks[ask_kind]}."
    )
    explanation = (
        f"Past ages {p}u,{qv}u. Weighted condition {ca}*{p}u+{cb}*{qv}u={weighted} gives u={u}. "
        f"Present ages {A},{B}. Future ({A+m}):({B+m})={fut_p}:{fut_q}. Required value {answer}."
    )
    return q(
        "am_linear_combo_ratio", v, text, answer, near_num(answer, 3), explanation,
        {"p": p, "q": qv, "u": u, "ca": ca, "cb": cb, "k": k, "m": m, "coefs": coefs},
    )


FAMILIES = [
    am_three_shift_pair, am_fraction_sum_diff, am_replacement_average,
    am_new_birth_average, am_reciprocal_product, am_admission_service,
    am_unequal_gaps_ratio, am_hidden_multiple_family, am_group_avg_exit_entry,
    am_future_different_pair, am_percentage_ages, am_simultaneous_linear,
    am_three_time_chain, am_average_subset, am_ratio_change_find_time,
    am_two_future_conditions, am_joining_service_two, am_fraction_two_conditions,
    am_percentage_change_average, am_reciprocal_sum_diff, am_exam_eligibility,
    am_time_triple_ratio, am_future_family_average, am_linear_combo_ratio,
]


def build_ages_mains():
    return build_specs(FAMILIES, mains=True)
