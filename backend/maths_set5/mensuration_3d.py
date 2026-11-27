# -*- coding: utf-8 -*-
"""Mensuration – 3D — 120 verified questions for the fifth Maths batch."""

from __future__ import annotations

from fractions import Fraction

from .bank import fmt
from .common import build_specs, pair, q, third

SOURCE = "Mensuration 3D class notes (local PDFs)"
PAGES = {
    1: "Mensurations 3D 01  Class Notes.pdf, pp. 3-7",
    2: "Mensurations 3D 02  Class Notes.pdf, pp. 4-10",
}


def F(a, b=1):
    return Fraction(a, b)


PI = F(22, 7)
CONTEXTS = ("store room", "water tank", "grain bin", "display box", "tool chest")
SETTINGS = ("warehouse", "workshop", "showroom", "laboratory", "packing unit")


def vol(value):
    return f"{fmt(value)} cu m"


def area(value):
    return f"{fmt(value)} sq m"


def length(value):
    return f"{fmt(value)} m"


def m3_cube_volume(r, v):
    s = (6, 9, 12, 15, 18)[v]
    who, friend = pair(v)
    helper = third(v, 3)
    answer = vol(F(s) ** 3)
    return q(
        "m3_cube_volume", v,
        f"{who} and {friend} measure a cubic {CONTEXTS[v]}. {helper} records each "
        f"edge as {s} m. Find its volume.",
        answer,
        [vol(F(3 * s)), vol(F(s) ** 2), vol(F(s) ** 2 * 3)],
        f"Volume of a cube = side^3 = {s}^3 = {s ** 3} cu m.",
        {"s": s},
    )


def m3_cube_tsa(r, v):
    s = (5, 8, 11, 14, 17)[v]
    who, friend = pair(v, 1)
    helper = third(v, 4)
    answer = area(F(6 * s * s))
    return q(
        "m3_cube_tsa", v,
        f"A cubic {SETTINGS[v]} has edge {s} m. {who} asks {friend} and {helper} "
        f"for the total surface area to be painted. Find it.",
        answer,
        [area(F(4 * s * s)), area(F(s * s)), area(F(12 * s * s))],
        f"Total surface area of a cube = 6 x side^2 = 6 x {s}^2 = {6 * s * s} sq m.",
        {"s": s},
    )


def m3_cube_lsa(r, v):
    s = (7, 10, 13, 16, 19)[v]
    who, friend = pair(v, 2)
    helper = third(v, 5)
    answer = area(F(4 * s * s))
    return q(
        "m3_cube_lsa", v,
        f"{who} needs the lateral surface of a cubic {CONTEXTS[v]} with edge "
        f"{s} m. {friend} asks {helper} to calculate it. Find the area.",
        answer,
        [area(F(6 * s * s)), area(F(s * s)), area(F(2 * s * s))],
        f"Lateral surface area of a cube = 4 x side^2 = 4 x {s}^2 = {4 * s * s} sq m.",
        {"s": s},
    )


def m3_cuboid_volume(r, v):
    dims = ((8, 6, 5), (12, 9, 7), (15, 10, 8), (18, 12, 9), (21, 14, 11))[v]
    L, B, H = dims
    who, friend = pair(v, 3)
    helper = third(v, 6)
    answer = vol(F(L * B * H))
    return q(
        "m3_cuboid_volume", v,
        f"A rectangular {SETTINGS[v]} measures {L} m x {B} m x {H} m. {who}, "
        f"{friend} and {helper} need its volume. Find it.",
        answer,
        [vol(F(2 * (L * B + B * H + H * L))), vol(F(L * B)), vol(F(L * B * H, 2))],
        f"Volume of a cuboid = l x b x h = {L} x {B} x {H} = {L * B * H} cu m.",
        {"L": L, "B": B, "H": H},
    )


def m3_cuboid_tsa(r, v):
    dims = ((9, 7, 6), (13, 10, 8), (16, 12, 10), (20, 15, 12), (24, 18, 14))[v]
    L, B, H = dims
    who, friend = pair(v, 4)
    helper = third(v, 7)
    answer = area(F(2 * (L * B + B * H + H * L)))
    return q(
        "m3_cuboid_tsa", v,
        f"{who} and {friend} wrap a rectangular {CONTEXTS[v]} of dimensions "
        f"{L} m, {B} m and {H} m. {helper} asks for the total surface area. Find it.",
        answer,
        [area(F(L * B + B * H + H * L)), area(F(2 * H * (L + B))), area(F(L * B * H))],
        f"Total surface area = 2(lb + bh + hl) = 2({L * B} + {B * H} + {H * L}) = "
        f"{2 * (L * B + B * H + H * L)} sq m.",
        {"L": L, "B": B, "H": H},
    )


def m3_cuboid_lsa(r, v):
    dims = ((11, 8, 7), (14, 11, 9), (18, 13, 11), (22, 16, 13), (26, 19, 15))[v]
    L, B, H = dims
    who, friend = pair(v, 5)
    helper = third(v, 8)
    answer = area(F(2 * H * (L + B)))
    return q(
        "m3_cuboid_lsa", v,
        f"A rectangular {SETTINGS[v]} has length {L} m, breadth {B} m and height "
        f"{H} m. {who}, {friend} and {helper} need the area of its four walls. Find it.",
        answer,
        [area(F(2 * (L * B + B * H + H * L))), area(F(H * (L + B))), area(F(2 * L * B))],
        f"Lateral surface area = 2h(l + b) = 2 x {H} x ({L} + {B}) = "
        f"{2 * H * (L + B)} sq m.",
        {"L": L, "B": B, "H": H},
    )


def m3_cylinder_volume(r, v):
    pairs = ((7, 10), (14, 12), (21, 15), (28, 18), (35, 20))[v]
    rad, ht = pairs
    who, friend = pair(v, 6)
    helper = third(v, 9)
    answer = vol(PI * F(rad) ** 2 * F(ht))
    return q(
        "m3_cylinder_volume", v,
        f"{who} and {friend} fill a cylindrical {CONTEXTS[v]} of radius {rad} m "
        f"and height {ht} m. {helper} uses pi = 22/7. Find its volume.",
        answer,
        [vol(PI * F(rad) * F(ht)), vol(F(2) * PI * F(rad) ** 2 * F(ht)), vol(PI * F(rad) ** 2)],
        f"Volume = pi x r^2 x h = (22/7) x {rad}^2 x {ht} = "
        f"{fmt(PI * F(rad) ** 2 * F(ht))} cu m.",
        {"r": rad, "h": ht},
    )


def m3_cylinder_csa(r, v):
    pairs = ((7, 12), (14, 15), (21, 18), (28, 21), (35, 24))[v]
    rad, ht = pairs
    who, friend = pair(v, 7)
    helper = third(v, 10)
    answer = area(F(2) * PI * F(rad) * F(ht))
    return q(
        "m3_cylinder_csa", v,
        f"A cylindrical {SETTINGS[v]} has radius {rad} m and height {ht} m. "
        f"{who}, {friend} and {helper} need only the curved surface area using "
        f"pi = 22/7. Find it.",
        answer,
        [area(PI * F(rad) * F(ht)), area(F(2) * PI * F(rad) * (F(ht) + F(rad))), area(F(2) * PI * F(rad) ** 2)],
        f"Curved surface area = 2 x pi x r x h = 2 x (22/7) x {rad} x {ht} = "
        f"{fmt(F(2) * PI * F(rad) * F(ht))} sq m.",
        {"r": rad, "h": ht},
    )


def m3_cylinder_tsa(r, v):
    pairs = ((7, 14), (14, 17), (21, 20), (28, 23), (35, 26))[v]
    rad, ht = pairs
    who, friend = pair(v, 8)
    helper = third(v, 11)
    answer = area(F(2) * PI * F(rad) * (F(rad) + F(ht)))
    return q(
        "m3_cylinder_tsa", v,
        f"{who} and {friend} paint a closed cylindrical {CONTEXTS[v]} of radius "
        f"{rad} m and height {ht} m. {helper} uses pi = 22/7. Find the total "
        f"surface area.",
        answer,
        [area(F(2) * PI * F(rad) * F(ht)), area(PI * F(rad) ** 2 * F(ht)), area(PI * F(rad) * (F(rad) + F(ht)))],
        f"Total surface area = 2 x pi x r x (r + h) = 2 x (22/7) x {rad} x "
        f"({rad} + {ht}) = {fmt(F(2) * PI * F(rad) * (F(rad) + F(ht)))} sq m.",
        {"r": rad, "h": ht},
    )


def m3_cone_volume(r, v):
    pairs = ((7, 12), (14, 18), (21, 24), (28, 27), (35, 30))[v]
    rad, ht = pairs
    who, friend = pair(v, 9)
    helper = third(v, 12)
    answer = vol(PI * F(rad) ** 2 * F(ht) / F(3))
    return q(
        "m3_cone_volume", v,
        f"A conical {SETTINGS[v]} has radius {rad} m and height {ht} m. {who}, "
        f"{friend} and {helper} use pi = 22/7. Find its volume.",
        answer,
        [vol(PI * F(rad) ** 2 * F(ht)), vol(PI * F(rad) * F(ht) / F(3)), vol(F(PI * F(rad) ** 2 * F(ht), 6))],
        f"Volume of a cone = (1/3) x pi x r^2 x h = (1/3) x (22/7) x {rad}^2 x {ht} = "
        f"{fmt(PI * F(rad) ** 2 * F(ht) / F(3))} cu m.",
        {"r": rad, "h": ht},
    )


def m3_cone_csa(r, v):
    triples = ((7, 24, 25), (14, 48, 50), (21, 20, 29), (28, 45, 53), (35, 12, 37))[v]
    rad, ht, slant = triples
    who, friend = pair(v, 10)
    helper = third(v, 13)
    answer = area(PI * F(rad) * F(slant))
    return q(
        "m3_cone_csa", v,
        f"A conical {CONTEXTS[v]} has radius {rad} m, height {ht} m and slant "
        f"height {slant} m. {who}, {friend} and {helper} need the curved area using "
        f"pi = 22/7. Find it.",
        answer,
        [area(PI * F(rad) * F(ht)), area(F(2) * PI * F(rad) * F(slant)), area(PI * F(rad) ** 2)],
        f"Curved surface area = pi x r x l = (22/7) x {rad} x {slant} = "
        f"{fmt(PI * F(rad) * F(slant))} sq m.",
        {"r": rad, "l": slant},
    )


def m3_cone_tsa(r, v):
    triples = ((7, 24, 25), (14, 48, 50), (21, 20, 29), (28, 45, 53), (35, 12, 37))[v]
    rad, ht, slant = triples
    who, friend = pair(v, 11)
    helper = third(v, 14)
    answer = area(PI * F(rad) * (F(rad) + F(slant)))
    return q(
        "m3_cone_tsa", v,
        f"{who} and {friend} cover a conical {SETTINGS[v]} with radius {rad} m and "
        f"slant height {slant} m. {helper} uses pi = 22/7. Find the total surface area.",
        answer,
        [area(PI * F(rad) * F(slant)), area(F(2) * PI * F(rad) * (F(rad) + F(slant))), area(PI * F(rad) ** 2)],
        f"Total surface area = pi x r x (r + l) = (22/7) x {rad} x ({rad} + {slant}) = "
        f"{fmt(PI * F(rad) * (F(rad) + F(slant)))} sq m.",
        {"r": rad, "l": slant},
    )


def m3_sphere_volume(r, v):
    radii = (7, 14, 21, 28, 35)[v]
    who, friend = pair(v, 12)
    helper = third(v, 15)
    answer = vol(F(4, 3) * PI * F(radii) ** 3)
    return q(
        "m3_sphere_volume", v,
        f"A spherical {CONTEXTS[v]} has radius {radii} m. {who}, {friend} and "
        f"{helper} use pi = 22/7. Find its volume.",
        answer,
        [vol(F(4) * PI * F(radii) ** 2), vol(F(4, 3) * PI * F(radii) ** 2), vol(F(2, 3) * PI * F(radii) ** 3)],
        f"Volume of a sphere = (4/3) x pi x r^3 = (4/3) x (22/7) x {radii}^3 = "
        f"{fmt(F(4, 3) * PI * F(radii) ** 3)} cu m.",
        {"r": radii},
    )


def m3_sphere_surface(r, v):
    radii = (7, 14, 21, 28, 35)[v]
    who, friend = pair(v, 13)
    helper = third(v, 16)
    answer = area(F(4) * PI * F(radii) ** 2)
    return q(
        "m3_sphere_surface", v,
        f"{who} and {friend} polish a spherical {SETTINGS[v]} of radius {radii} m. "
        f"{helper} uses pi = 22/7. Find the surface area.",
        answer,
        [area(F(2) * PI * F(radii) ** 2), area(F(4) * PI * F(radii)), area(F(4, 3) * PI * F(radii) ** 2)],
        f"Surface area = 4 x pi x r^2 = 4 x (22/7) x {radii}^2 = "
        f"{fmt(F(4) * PI * F(radii) ** 2)} sq m.",
        {"r": radii},
    )


def m3_hemisphere_volume(r, v):
    radii = (7, 14, 21, 28, 35)[v]
    who, friend = pair(v, 14)
    helper = third(v, 17)
    answer = vol(F(2, 3) * PI * F(radii) ** 3)
    return q(
        "m3_hemisphere_volume", v,
        f"A hemispherical {CONTEXTS[v]} has radius {radii} m. {who}, {friend} and "
        f"{helper} use pi = 22/7. Find its volume.",
        answer,
        [vol(F(4, 3) * PI * F(radii) ** 3), vol(F(2, 3) * PI * F(radii) ** 2), vol(F(1, 3) * PI * F(radii) ** 3)],
        f"Volume of a hemisphere = (2/3) x pi x r^3 = (2/3) x (22/7) x {radii}^3 = "
        f"{fmt(F(2, 3) * PI * F(radii) ** 3)} cu m.",
        {"r": radii},
    )


def m3_hemisphere_csa(r, v):
    radii = (7, 14, 21, 28, 35)[v]
    who, friend = pair(v, 15)
    helper = third(v, 18)
    answer = area(F(2) * PI * F(radii) ** 2)
    return q(
        "m3_hemisphere_csa", v,
        f"The curved shell of a hemispherical {SETTINGS[v]} has radius {radii} m. "
        f"{who}, {friend} and {helper} use pi = 22/7. Find the curved surface area.",
        answer,
        [area(F(3) * PI * F(radii) ** 2), area(F(4) * PI * F(radii) ** 2), area(PI * F(radii) ** 2)],
        f"Curved surface area of a hemisphere = 2 x pi x r^2 = 2 x (22/7) x {radii}^2 = "
        f"{fmt(F(2) * PI * F(radii) ** 2)} sq m.",
        {"r": radii},
    )


def m3_hemisphere_tsa(r, v):
    radii = (7, 14, 21, 28, 35)[v]
    who, friend = pair(v, 16)
    helper = third(v, 19)
    answer = area(F(3) * PI * F(radii) ** 2)
    return q(
        "m3_hemisphere_tsa", v,
        f"{who} and {friend} close a hemispherical {CONTEXTS[v]} of radius {radii} m, "
        f"including its circular base. {helper} uses pi = 22/7. Find the total surface area.",
        answer,
        [area(F(2) * PI * F(radii) ** 2), area(F(4) * PI * F(radii) ** 2), area(F(3) * PI * F(radii))],
        f"Total surface area of a hemisphere = 3 x pi x r^2 = 3 x (22/7) x {radii}^2 = "
        f"{fmt(F(3) * PI * F(radii) ** 2)} sq m.",
        {"r": radii},
    )


def m3_melt_cylinder_cones(r, v):
    data = ((14, 9), (21, 12), (28, 15), (35, 18), (42, 21))[v]
    ht, cone_ht = data
    who, friend = pair(v, 17)
    helper = third(v, 20)
    answer = fmt(F(3 * ht, cone_ht))
    return q(
        "m3_melt_cylinder_cones", v,
        f"{who} melts a solid cylinder of radius {7 + v} m and height {ht} m and "
        f"recasts it into cones of the same radius and height {cone_ht} m. {friend} "
        f"asks {helper} how many cones are formed. Find the number.",
        answer,
        [fmt(F(ht, cone_ht)), fmt(F(3 * ht, 2 * cone_ht)), fmt(F(ht, 3 * cone_ht))],
        f"Volumes cancel pi and r^2. Number of cones = cylinder volume / cone volume = "
        f"3 x cylinder height / cone height = 3 x {ht} / {cone_ht} = {fmt(F(3 * ht, cone_ht))}.",
        {"h": ht, "H": cone_ht},
    )


def m3_melt_cube_cuboid(r, v):
    data = ((12, 8, 6), (18, 9, 8), (24, 12, 9), (30, 15, 12), (36, 18, 16))[v]
    side, breadth, ht = data
    length = F(side ** 3, breadth * ht)
    who, friend = pair(v, 18)
    helper = third(v, 21)
    answer = fmt(length)
    return q(
        "m3_melt_cube_cuboid", v,
        f"A cube of side {side} m is melted and recast into a cuboid of breadth "
        f"{breadth} m and height {ht} m. {who}, {friend} and {helper} need its length. "
        f"Find it.",
        answer,
        [fmt(length * 2), fmt(length / 2), fmt(F(side ** 2, breadth))],
        f"Volumes are equal, so length = side^3 / (breadth x height) = {side}^3 / "
        f"({breadth} x {ht}) = {fmt(length)} m.",
        {"s": side, "b": breadth, "h": ht},
    )


def m3_combined_cylinder_cone(r, v):
    data = ((7, 10, 12), (14, 14, 18), (21, 16, 21), (28, 18, 24), (35, 20, 27))[v]
    rad, cyl_h, cone_h = data
    who, friend = pair(v, 19)
    helper = third(v, 22)
    volume = PI * F(rad) ** 2 * (F(cyl_h) + F(cone_h, 3))
    answer = vol(volume)
    return q(
        "m3_combined_cylinder_cone", v,
        f"A {SETTINGS[v]} is a cylinder of radius {rad} m and height {cyl_h} m "
        f"surmounted by a cone of height {cone_h} m. {who}, {friend} and {helper} "
        f"use pi = 22/7. Find the total volume.",
        answer,
        [vol(PI * F(rad) ** 2 * F(cyl_h)), vol(F(4, 3) * PI * F(rad) ** 2 * F(cyl_h)), vol(PI * F(rad) ** 2 * (F(cyl_h) + F(cone_h)))],
        f"Total volume = pi r^2 h + (1/3) pi r^2 H = pi r^2 (h + H/3) = "
        f"{fmt(volume)} cu m.",
        {"r": rad, "h": cyl_h, "H": cone_h},
    )


def m3_capacity_litres(r, v):
    dims = ((50, 40, 30), (80, 50, 40), (100, 60, 45), (120, 75, 50), (150, 80, 60))[v]
    L, B, H = dims
    who, friend = pair(v, 20)
    helper = third(v, 23)
    litres = F(L * B * H, 1000)
    answer = f"{fmt(litres)} litres"
    return q(
        "m3_capacity_litres", v,
        f"A rectangular {CONTEXTS[v]} is {L} cm by {B} cm by {H} cm. {who}, {friend} "
        f"and {helper} need its capacity in litres. Find it.",
        answer,
        [f"{fmt(litres * 10)} litres", f"{fmt(litres / 10)} litres", f"{fmt(L * B * H)} litres"],
        f"Volume = {L} x {B} x {H} = {L * B * H} cubic cm. Since 1000 cubic cm = "
        f"1 litre, capacity = {fmt(litres)} litres.",
        {"L": L, "B": B, "H": H},
    )


def m3_water_rise(r, v):
    data = ((7, 14), (14, 21), (21, 28), (28, 35), (35, 42))[v]
    side, tank_r = data
    who, friend = pair(v, 21)
    helper = third(v, 24)
    rise = F(side ** 3) / (PI * F(tank_r) ** 2)
    answer = length(rise)
    return q(
        "m3_water_rise", v,
        f"A cube of side {side} m is fully immersed in a cylindrical {SETTINGS[v]} "
        f"of radius {tank_r} m. {who}, {friend} and {helper} use pi = 22/7. By how "
        f"much does the water level rise?",
        answer,
        [length(rise * 2), length(rise / 2), length(F(side ** 2) / (PI * F(tank_r)))],
        f"Displaced volume = cube volume = {side}^3. Rise = displaced volume / "
        f"(pi x tank radius^2) = {fmt(rise)} m.",
        {"s": side, "R": tank_r},
    )


def m3_hollow_cylinder(r, v):
    data = ((7, 5, 14), (14, 10, 21), (21, 14, 28), (28, 20, 35), (35, 25, 42))[v]
    outer, inner, ht = data
    who, friend = pair(v, 22)
    helper = third(v, 25)
    volume = PI * F(ht) * (F(outer) ** 2 - F(inner) ** 2)
    answer = vol(volume)
    return q(
        "m3_hollow_cylinder", v,
        f"A hollow cylindrical {CONTEXTS[v]} has outer radius {outer} m, inner "
        f"radius {inner} m and height {ht} m. {who}, {friend} and {helper} use "
        f"pi = 22/7. Find the material volume.",
        answer,
        [vol(PI * F(ht) * (F(outer) ** 2 + F(inner) ** 2)), vol(PI * F(ht) * F(outer - inner) ** 2), vol(F(2) * PI * F(ht) * (F(outer) + F(inner)))],
        f"Material volume = pi x h x (R^2 - r^2) = (22/7) x {ht} x "
        f"({outer}^2 - {inner}^2) = {fmt(volume)} cu m.",
        {"R": outer, "r": inner, "h": ht},
    )


def m3_volume_ratio(r, v):
    data = ((7, 12), (14, 18), (21, 24), (28, 30), (35, 36))[v]
    rad, ht = data
    who, friend = pair(v, 23)
    helper = third(v, 26)
    ratio = F(1, 3)
    answer = "1:3"
    return q(
        "m3_volume_ratio", v,
        f"A cone and a cylinder have the same radius {rad} m and the same height "
        f"{ht} m. {who}, {friend} and {helper} ask for the ratio of the cone's volume "
        f"to the cylinder's volume. Find it.",
        answer,
        ["3:1", "1:2", "2:3"],
        f"Cone volume is (1/3) pi r^2 h and cylinder volume is pi r^2 h, so the "
        f"ratio is {fmt(ratio)} = 1:3.",
        {"r": rad, "h": ht},
    )


def m3_paint_cost(r, v):
    dims = ((10, 8, 6, 5), (14, 10, 8, 6), (18, 12, 10, 7), (22, 16, 12, 8), (26, 20, 15, 9))[v]
    L, B, H, rate = dims
    who, friend = pair(v, 24)
    helper = third(v, 27)
    tsa = F(2 * (L * B + B * H + H * L))
    cost = tsa * F(rate)
    answer = f"₹{fmt(cost)}"
    return q(
        "m3_paint_cost", v,
        f"{who} and {friend} paint a closed cuboidal {SETTINGS[v]} of dimensions "
        f"{L} m x {B} m x {H} m. {helper} charges ₹{rate} per sq m. Find the total cost.",
        answer,
        [f"₹{fmt(tsa)}", f"₹{fmt(cost * 2)}", f"₹{fmt(cost / 2)}"],
        f"Total surface area = 2(lb + bh + hl) = {fmt(tsa)} sq m. Cost = area x rate "
        f"= {fmt(tsa)} x {rate} = ₹{fmt(cost)}.",
        {"L": L, "B": B, "H": H, "rate": rate},
    )


FAMILIES = (
    m3_cube_volume,
    m3_cube_tsa,
    m3_cube_lsa,
    m3_cuboid_volume,
    m3_cuboid_tsa,
    m3_cuboid_lsa,
    m3_cylinder_volume,
    m3_cylinder_csa,
    m3_cylinder_tsa,
    m3_cone_volume,
    m3_cone_csa,
    m3_cone_tsa,
    m3_sphere_volume,
    m3_sphere_surface,
    m3_hemisphere_volume,
    m3_hemisphere_csa,
    m3_hemisphere_tsa,
    m3_melt_cylinder_cones,
    m3_melt_cube_cuboid,
    m3_combined_cylinder_cone,
    m3_capacity_litres,
    m3_water_rise,
    m3_hollow_cylinder,
    m3_paint_cost,
)


def build_mensuration_3d():
    return build_specs(FAMILIES)
