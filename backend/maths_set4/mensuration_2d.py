# -*- coding: utf-8 -*-
"""Mensuration 2D - 120 verified questions for the fourth Maths batch."""

from __future__ import annotations

import math
from fractions import Fraction

from .bank import fmt
from .common import build_specs, pair, q, third

SOURCE = "Mensuration 2D class notes (local PDFs)"
PAGES = {
    1: "Mensurations 2D 01 _ Class Notes.pdf, pp. 1-27",
    2: "Mensurations 2D 02  Class Notes.pdf, pp. 1-16",
}


def F(a, b=1):
    return Fraction(a, b)


PI = F(22, 7)


def length(value):
    return f"{fmt(value)} m"


def area(value):
    return f"{fmt(value)} sq m"


def rupees(value):
    return f"₹{fmt(value)}"


def radical_diag(value):
    return f"{fmt(value)}√2 m"


CONTEXTS = ("plot", "field", "park", "garden", "hall")
SETTINGS = ("garden", "playground", "courtyard", "farm", "terrace")


def m2_square_area(r, v):
    presets = [8, 12, 15, 21, 27]
    s = presets[v]
    who, friend = pair(v)
    helper = third(v)
    ctx = CONTEXTS[v]
    answer = area(F(s) * F(s))
    return q(
        "m2_square_area", v,
        f"{who} and {friend} own a square {ctx}. {helper} measures one side as "
        f"{s} m. What is its area?",
        answer,
        [area(F(2 * s)), area(F(3 * s)), area(F(s * s, 2))],
        f"Area of a square = side x side = {s} x {s} = {fmt(F(s * s))} sq m.",
        {"s": s},
    )


def m2_square_perimeter(r, v):
    presets = [9, 14, 18, 23, 31]
    s = presets[v]
    who, friend = pair(v, 1)
    helper = third(v, 3)
    ctx = SETTINGS[v]
    answer = length(F(4 * s))
    return q(
        "m2_square_perimeter", v,
        f"{who} and {friend} want a border around a square {ctx}. {helper} says "
        f"each side is {s} m. What is the total border length?",
        answer,
        [length(F(2 * s)), length(F(3 * s)), length(F(s * s))],
        f"Perimeter of a square = 4 x side = 4 x {s} = {fmt(F(4 * s))} m.",
        {"s": s},
    )


def m2_rectangle_area(r, v):
    presets = [(12, 8), (18, 10), (25, 14), (30, 16), (36, 21)]
    L, W = presets[v]
    who, friend = pair(v, 2)
    helper = third(v, 4)
    ctx = CONTEXTS[v]
    answer = area(F(L) * F(W))
    return q(
        "m2_rectangle_area", v,
        f"{who} and {friend} have a rectangular {ctx} measuring {L} m by {W} m. "
        f"{helper} asks for its area. What is it?",
        answer,
        [area(F(2 * (L + W))), area(F(L + W)), area(F(L * W, 2))],
        f"Area of a rectangle = length x breadth = {L} x {W} = {fmt(F(L * W))} sq m.",
        {"L": L, "W": W},
    )


def m2_rectangle_perimeter(r, v):
    presets = [(15, 9), (22, 12), (28, 17), (34, 19), (42, 25)]
    L, W = presets[v]
    who, friend = pair(v, 3)
    helper = third(v, 5)
    ctx = SETTINGS[v]
    answer = length(F(2 * (L + W)))
    return q(
        "m2_rectangle_perimeter", v,
        f"A rectangular {ctx} owned by {who} is {L} m long and {W} m wide. "
        f"{friend} asks {helper} for the length of its boundary. Find it.",
        answer,
        [length(F(L + W)), length(F(2 * L + W)), length(F(L + 2 * W))],
        f"Perimeter = 2 x (length + breadth) = 2 x ({L} + {W}) = "
        f"{fmt(F(2 * (L + W)))} m.",
        {"L": L, "W": W},
    )


def m2_triangle_area(r, v):
    presets = [(14, 10), (18, 12), (22, 16), (26, 20), (30, 24)]
    base, height = presets[v]
    who, friend = pair(v, 4)
    helper = third(v, 6)
    ctx = CONTEXTS[v]
    answer = area(F(base * height, 2))
    return q(
        "m2_triangle_area", v,
        f"{who} draws a triangular {ctx} for {friend} with base {base} m and "
        f"height {height} m. {helper} asks for its area. What is it?",
        answer,
        [area(F(base * height)), area(F(base * height, 4)), area(F(base + height))],
        f"Area of a triangle = (base x height)/2 = ({base} x {height})/2 = "
        f"{fmt(F(base * height, 2))} sq m.",
        {"b": base, "h": height},
    )


def m2_triangle_perimeter(r, v):
    presets = [(9, 12, 15), (7, 24, 25), (10, 24, 26), (8, 15, 17), (20, 21, 29)]
    x, y, z = presets[v]
    who, friend = pair(v, 5)
    helper = third(v, 7)
    ctx = SETTINGS[v]
    answer = length(F(x + y + z))
    return q(
        "m2_triangle_perimeter", v,
        f"A triangular {ctx} has sides {x} m, {y} m and {z} m. {who} asks "
        f"{friend} and {helper} for its perimeter. Find it.",
        answer,
        [length(F(x + y)), length(F(y + z)), length(F(x + z))],
        f"Perimeter = sum of the three sides = {x} + {y} + {z} = "
        f"{fmt(F(x + y + z))} m.",
        {"a": x, "b": y, "c": z},
    )


def m2_circle_area(r, v):
    presets = [7, 14, 21, 28, 35]
    radius = presets[v]
    who, friend = pair(v, 6)
    helper = third(v, 8)
    ctx = CONTEXTS[v]
    answer = area(PI * F(radius) * F(radius))
    return q(
        "m2_circle_area", v,
        f"{who} and {friend} have a circular {ctx} of radius {radius} m. "
        f"{helper} asks for its area using pi = 22/7. Find it.",
        answer,
        [
            area(F(2) * PI * F(radius)),
            area(PI * F(radius) * F(radius) / 2),
            area(F(2) * PI * F(radius) * F(radius)),
        ],
        f"Area = pi x r x r = (22/7) x {radius} x {radius} = "
        f"{fmt(PI * F(radius) * F(radius))} sq m.",
        {"r": radius},
    )


def m2_circle_circumference(r, v):
    presets = [7, 14, 21, 28, 35]
    radius = presets[v]
    who, friend = pair(v, 7)
    helper = third(v, 9)
    ctx = SETTINGS[v]
    answer = length(F(2) * PI * F(radius))
    return q(
        "m2_circle_circumference", v,
        f"A circular {ctx} in {who}'s care has radius {radius} m. {friend} asks "
        f"{helper} for its circumference using pi = 22/7. Find it.",
        answer,
        [
            length(PI * F(radius)),
            length(F(4) * PI * F(radius)),
            length(F(2) * PI * F(radius) + F(2 * radius)),
        ],
        f"Circumference = 2 x pi x r = 2 x (22/7) x {radius} = "
        f"{fmt(F(2) * PI * F(radius))} m.",
        {"r": radius},
    )


def m2_semicircle_area(r, v):
    presets = [7, 14, 21, 28, 35]
    radius = presets[v]
    who, friend = pair(v, 8)
    helper = third(v, 10)
    ctx = CONTEXTS[v]
    answer = area(PI * F(radius) * F(radius) / 2)
    return q(
        "m2_semicircle_area", v,
        f"{who} marks a semicircular {ctx} of radius {radius} m for {friend}. "
        f"{helper} asks for its area using pi = 22/7. Find it.",
        answer,
        [
            area(PI * F(radius) * F(radius)),
            area(PI * F(radius) * F(radius) / 4),
            area(PI * F(radius) * F(radius) / 2 + PI * F(radius)),
        ],
        f"Area of a semicircle = (pi x r x r)/2 = (22/7 x {radius} x {radius})/2 "
        f"= {fmt(PI * F(radius) * F(radius) / 2)} sq m.",
        {"r": radius},
    )


def m2_semicircle_perimeter(r, v):
    presets = [7, 14, 21, 28, 35]
    radius = presets[v]
    who, friend = pair(v, 9)
    helper = third(v, 11)
    ctx = SETTINGS[v]
    answer = length(PI * F(radius) + F(2 * radius))
    return q(
        "m2_semicircle_perimeter", v,
        f"A semicircular {ctx} has radius {radius} m. {who} asks {friend} and "
        f"{helper} for its boundary length using pi = 22/7. Find it.",
        answer,
        [
            length(PI * F(radius)),
            length(F(2) * PI * F(radius)),
            length(PI * F(radius) + F(radius)),
        ],
        f"Perimeter of a semicircle = pi x r + 2r = (22/7) x {radius} + "
        f"2 x {radius} = {fmt(PI * F(radius) + F(2 * radius))} m.",
        {"r": radius},
    )


def m2_parallelogram_area(r, v):
    presets = [(18, 12), (24, 15), (30, 16), (36, 21), (42, 25)]
    base, height = presets[v]
    who, friend = pair(v, 10)
    helper = third(v, 12)
    ctx = CONTEXTS[v]
    answer = area(F(base) * F(height))
    return q(
        "m2_parallelogram_area", v,
        f"{who} has a parallelogram-shaped {ctx} with base {base} m and height "
        f"{height} m. {friend} and {helper} need its area. Find it.",
        answer,
        [
            area(F(2 * (base + height))),
            area(F(base * height, 2)),
            area(F(base + height)),
        ],
        f"Area of a parallelogram = base x height = {base} x {height} = "
        f"{fmt(F(base * height))} sq m.",
        {"b": base, "h": height},
    )


def m2_parallelogram_perimeter(r, v):
    presets = [(15, 10), (21, 14), (27, 18), (33, 22), (39, 26)]
    x, y = presets[v]
    who, friend = pair(v, 11)
    helper = third(v, 13)
    ctx = SETTINGS[v]
    answer = length(F(2 * (x + y)))
    return q(
        "m2_parallelogram_perimeter", v,
        f"The adjacent sides of a parallelogram {ctx} are {x} m and {y} m. "
        f"{who} asks {friend} and {helper} for its perimeter. Find it.",
        answer,
        [length(F(x + y)), length(F(x * y)), length(F(3 * x + y))],
        f"Perimeter = 2 x (sum of adjacent sides) = 2 x ({x} + {y}) = "
        f"{fmt(F(2 * (x + y)))} m.",
        {"a": x, "b": y},
    )


def m2_rhombus_area(r, v):
    presets = [(16, 12), (24, 18), (30, 20), (36, 24), (42, 28)]
    d1, d2 = presets[v]
    who, friend = pair(v, 12)
    helper = third(v, 14)
    ctx = CONTEXTS[v]
    answer = area(F(d1 * d2, 2))
    return q(
        "m2_rhombus_area", v,
        f"A rhombus-shaped {ctx} belongs to {who}. Its diagonals are {d1} m and "
        f"{d2} m. {friend} asks {helper} for the area. Find it.",
        answer,
        [area(F(d1 * d2)), area(F(d1 * d2, 4)), area(F(d1 + d2))],
        f"Area of a rhombus = (d1 x d2)/2 = ({d1} x {d2})/2 = "
        f"{fmt(F(d1 * d2, 2))} sq m.",
        {"d1": d1, "d2": d2},
    )


def m2_rhombus_perimeter(r, v):
    presets = [10, 15, 20, 25, 30]
    s = presets[v]
    who, friend = pair(v, 13)
    helper = third(v, 15)
    ctx = SETTINGS[v]
    answer = length(F(4 * s))
    return q(
        "m2_rhombus_perimeter", v,
        f"Each side of a rhombus {ctx} is {s} m. {who} tells {friend} that "
        f"{helper} needs the perimeter. Find it.",
        answer,
        [length(F(s * s)), length(F(2 * s)), length(F(3 * s))],
        f"Perimeter of a rhombus = 4 x side = 4 x {s} = {fmt(F(4 * s))} m.",
        {"s": s},
    )


def m2_trapezium_area(r, v):
    presets = [(12, 8, 6), (16, 10, 9), (20, 14, 12), (24, 18, 15), (30, 20, 18)]
    x, y, h = presets[v]
    who, friend = pair(v, 14)
    helper = third(v, 16)
    ctx = CONTEXTS[v]
    answer = area(F(x + y, 2) * F(h))
    return q(
        "m2_trapezium_area", v,
        f"A trapezium {ctx} has parallel sides {x} m and {y} m and height {h} m. "
        f"{who} and {friend} ask {helper} for its area. Find it.",
        answer,
        [area(F((x + y) * h)), area(F((x + y) * h, 4)), area(F(x + y + h))],
        f"Area = [(sum of parallel sides)/2] x height = [({x} + {y})/2] x {h} "
        f"= {fmt(F(x + y, 2) * F(h))} sq m.",
        {"a": x, "b": y, "h": h},
    )


def m2_trapezium_perimeter(r, v):
    presets = [
        (12, 8, 7, 9), (16, 10, 9, 11), (20, 14, 11, 13),
        (24, 18, 13, 15), (30, 20, 17, 19),
    ]
    x, y, z, w = presets[v]
    who, friend = pair(v, 15)
    helper = third(v, 17)
    ctx = SETTINGS[v]
    answer = length(F(x + y + z + w))
    return q(
        "m2_trapezium_perimeter", v,
        f"The four sides of a trapezium {ctx} are {x} m, {y} m, {z} m and {w} m. "
        f"{who} asks {friend} and {helper} for its perimeter. Find it.",
        answer,
        [length(F(x + y)), length(F(z + w)), length(F(x + y + z))],
        f"Perimeter = {x} + {y} + {z} + {w} = {fmt(F(x + y + z + w))} m.",
        {"a": x, "b": y, "c": z, "d": w},
    )


def m2_composite_rect_square(r, v):
    presets = [
        (18, 12, 6), (24, 15, 9), (30, 18, 12), (36, 20, 15), (42, 24, 18),
    ]
    L, W, s = presets[v]
    who, friend = pair(v, 16)
    helper = third(v, 18)
    ctx = CONTEXTS[v]
    answer = area(F(L * W) + F(s * s))
    return q(
        "m2_composite_rect_square", v,
        f"{who} joins a square of side {s} m to a rectangular {ctx} of {L} m by "
        f"{W} m. {friend} asks {helper} for the combined area. Find it.",
        answer,
        [area(F(L * W)), area(F(s * s)), area(F((L + s) * (W + s)))],
        f"Total area = rectangle + square = ({L} x {W}) + ({s} x {s}) = "
        f"{fmt(F(L * W) + F(s * s))} sq m.",
        {"L": L, "W": W, "s": s},
    )


def m2_composite_circle_square(r, v):
    presets = [(21, 7), (28, 7), (35, 14), (42, 14), (49, 21)]
    s, radius = presets[v]
    who, friend = pair(v, 17)
    helper = third(v, 19)
    ctx = SETTINGS[v]
    answer = area(F(s * s) - PI * F(radius) * F(radius))
    return q(
        "m2_composite_circle_square", v,
        f"A square {ctx} of side {s} m has a circular bed of radius {radius} m "
        f"inside it. {who} asks {friend} and {helper} for the leftover area using "
        f"pi = 22/7. Find it.",
        answer,
        [
            area(F(s * s)),
            area(PI * F(radius) * F(radius)),
            area(F(s * s) + PI * F(radius) * F(radius)),
        ],
        f"Leftover area = square - circle = ({s} x {s}) - [(22/7) x {radius} x "
        f"{radius}] = {fmt(F(s * s) - PI * F(radius) * F(radius))} sq m.",
        {"s": s, "r": radius},
    )


def m2_path_area(r, v):
    presets = [(20, 12, 2), (24, 16, 3), (30, 18, 2), (36, 24, 4), (40, 28, 3)]
    L, W, width = presets[v]
    who, friend = pair(v, 18)
    helper = third(v, 0)
    ctx = CONTEXTS[v]
    answer = area(F((L + 2 * width) * (W + 2 * width)) - F(L * W))
    return q(
        "m2_path_area", v,
        f"A rectangular {ctx} is {L} m by {W} m. {who} builds a path of uniform "
        f"width {width} m all around it outside. {friend} asks {helper} for the "
        f"path area. Find it.",
        answer,
        [
            area(F(2 * width * (L + W))),
            area(F((L + 2 * width) * (W + 2 * width))),
            area(F(width * (L + W))),
        ],
        f"Outer size = ({L} + 2 x {width}) by ({W} + 2 x {width}). Path area = "
        f"outer - inner = {fmt(F((L + 2 * width) * (W + 2 * width)))} - "
        f"{fmt(F(L * W))} = "
        f"{fmt(F((L + 2 * width) * (W + 2 * width)) - F(L * W))} sq m.",
        {"L": L, "W": W, "w": width},
    )


def m2_square_diagonal(r, v):
    presets = [10, 14, 20, 28, 35]
    s = presets[v]
    who, friend = pair(v, 19)
    helper = third(v, 1)
    ctx = SETTINGS[v]
    answer = radical_diag(F(s))
    return q(
        "m2_square_diagonal", v,
        f"{who} has a square {ctx} of side {s} m. {friend} asks {helper} for the "
        f"exact length of its diagonal. What is it?",
        answer,
        [radical_diag(F(2 * s)), length(F(s)), radical_diag(F(s + 1))],
        f"Diagonal of a square = side x sqrt(2) = {s} x sqrt(2) = {s}√2 m.",
        {"s": s},
    )


def m2_rect_diagonal(r, v):
    presets = [(12, 5), (15, 8), (24, 7), (20, 15), (21, 20)]
    L, W = presets[v]
    who, friend = pair(v, 0)
    helper = third(v, 2)
    ctx = CONTEXTS[v]
    total = F(L * L + W * W)
    diagonal = F(math.isqrt(int(total)))
    answer = length(diagonal)
    return q(
        "m2_rect_diagonal", v,
        f"A rectangular {ctx} is {L} m long and {W} m wide. {who} asks {friend} "
        f"and {helper} for the diagonal length. Find it.",
        answer,
        [length(F(L + W)), length(F(2 * L)), length(F(2 * W))],
        f"Diagonal^2 = {L}^2 + {W}^2 = {fmt(total)}; diagonal = "
        f"{fmt(diagonal)} m.",
        {"L": L, "W": W},
    )


def m2_tiles_cost(r, v):
    presets = [
        (12, 9, 30, 8), (15, 12, 50, 10), (18, 12, 60, 12),
        (20, 15, 50, 15), (24, 18, 60, 20),
    ]
    L, W, tile, rate = presets[v]
    who, friend = pair(v, 1)
    helper = third(v, 3)
    ctx = SETTINGS[v]
    tiles = F(L * W * 10000, tile * tile)
    total = tiles * F(rate)
    answer = rupees(total)
    return q(
        "m2_tiles_cost", v,
        f"{who} tiles a {ctx} floor measuring {L} m by {W} m with square tiles "
        f"of side {tile} cm. Each tile costs ₹{rate}. {friend} asks {helper} for "
        f"the total cost. Find it.",
        answer,
        [rupees(tiles), rupees(F(L * W) * F(rate)), rupees(tiles * F(2 * rate))],
        f"Floor area = {L} x {W} = {L * W} sq m = {L * W * 10000} sq cm; one "
        f"tile = {tile} x {tile} = {tile * tile} sq cm; tiles = {fmt(tiles)}; "
        f"cost = {fmt(tiles)} x {rate} = ₹{fmt(total)}.",
        {"L": L, "W": W, "tile_cm": tile, "rate": rate},
    )


def m2_fencing_cost(r, v):
    presets = [(18, 12, 5), (24, 16, 7), (30, 20, 9), (36, 24, 11), (42, 28, 13)]
    L, W, rate = presets[v]
    who, friend = pair(v, 2)
    helper = third(v, 4)
    ctx = CONTEXTS[v]
    perimeter = F(2 * (L + W))
    total = perimeter * F(rate)
    answer = rupees(total)
    return q(
        "m2_fencing_cost", v,
        f"{who} fences a rectangular {ctx} of {L} m by {W} m at ₹{rate} per "
        f"metre. {friend} asks {helper} for the total cost. Find it.",
        answer,
        [rupees(perimeter), rupees(F(L + W) * F(rate)), rupees(F(L * W))],
        f"Perimeter = 2 x ({L} + {W}) = {fmt(perimeter)} m; cost = "
        f"{fmt(perimeter)} x {rate} = ₹{fmt(total)}.",
        {"L": L, "W": W, "rate": rate},
    )


def m2_compare(r, v):
    presets = [
        (20, 18, 15), (25, 22, 18), (30, 26, 22), (35, 30, 26), (40, 34, 30),
    ]
    s, L, W = presets[v]
    who, friend = pair(v, 3)
    helper = third(v, 5)
    ctx = SETTINGS[v]
    square = F(s * s)
    rectangle = F(L * W)
    difference = square - rectangle
    answer = area(difference)
    return q(
        "m2_compare", v,
        f"{who} has a square {ctx} of side {s} m and {friend} has a rectangular "
        f"one of {L} m by {W} m. {helper} asks how much larger the square's area "
        f"is. Find it.",
        answer,
        [area(square), area(rectangle), area(square + rectangle)],
        f"Square area = {s} x {s} = {fmt(square)} sq m; rectangle area = {L} x "
        f"{W} = {fmt(rectangle)} sq m; difference = {fmt(difference)} sq m.",
        {"s": s, "L": L, "W": W},
    )


FAMILIES = (
    m2_square_area,
    m2_square_perimeter,
    m2_rectangle_area,
    m2_rectangle_perimeter,
    m2_triangle_area,
    m2_triangle_perimeter,
    m2_circle_area,
    m2_circle_circumference,
    m2_semicircle_area,
    m2_semicircle_perimeter,
    m2_parallelogram_area,
    m2_parallelogram_perimeter,
    m2_rhombus_area,
    m2_rhombus_perimeter,
    m2_trapezium_area,
    m2_trapezium_perimeter,
    m2_composite_rect_square,
    m2_composite_circle_square,
    m2_path_area,
    m2_square_diagonal,
    m2_rect_diagonal,
    m2_tiles_cost,
    m2_fencing_cost,
    m2_compare,
)


def build_mensuration_2d():
    return build_specs(FAMILIES)
