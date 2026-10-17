"""Build a reviewed SSC Height and Distance batch with a worked answer ledger.

Source-derived questions are transcribed from two scanned Physics Wallah
Height and Distance lecture decks and independently re-solved. Only legible,
well-posed MCQs with four visible options were retained; concept slides,
recaps, titles/contents and summary pages were excluded, and one slide that
merely repeated an earlier item with a changed length was dropped as a
renumbered clone. Original SSC-style questions fill the remaining
per-difficulty gaps. PYQ status is not asserted for any item.
"""
from __future__ import annotations

import json
import random
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
ORIGINAL = "Original SSC-style practice question"
HD1 = "Height and Distance 01.pdf"
HD2 = "_Height and Distance 02_.pdf"
ROWS = []
LEDGER = []


def src(pdf, page):
    return f"{pdf}, PDF page {page}; exam/year not stated per item (PYQ status unverified)"


def add(level, stem, correct, wrongs, proof, source=ORIGINAL):
    correct = str(correct)
    vals = [correct]
    for w in wrongs:
        w = str(w)
        if w not in vals:
            vals.append(w)
    if len(vals) != 4:
        raise ValueError(f"Expected four distinct options for {stem!r}: {vals}")
    random.Random(len(ROWS) * 37 + len(stem)).shuffle(vals)
    key = "ABCD"[vals.index(correct)]
    ROWS.append({
        "subject_slug": "maths", "subcategory_slug": "advanced-maths",
        "chapter_slug": "height-and-distance", "question_text": stem,
        "options": dict(zip("ABCD", vals)), "correct_option": key,
        "explanation": proof, "difficulty": level, "is_pyq": False,
        "pyq_year": None, "pyq_exam_name": None, "source": source,
    })
    LEDGER.append({
        "row": len(ROWS), "question": stem, "difficulty": level,
        "expected_answer": correct, "independent_reasoning": proof,
        "source": source,
    })


# ─────────────────────────────────────────────────────────────────────────
# SOURCE-DERIVED QUESTIONS (21) — Height and Distance 01 / 02 scanned decks
# ─────────────────────────────────────────────────────────────────────────

# --- Height and Distance 01.pdf (Lecture 1) ---
add("EASY", "The angle of elevation of the sun when the length of the shadow of a tree equals the height of the tree is:",
    "45°", ["60°", "30°", "75°"],
    "Shadow equals height, so tanθ = h/h = 1 and θ = 45°.",
    src(HD1, 8))
add("EASY", "The angle of elevation of the sun when the length of the shadow of a tree is √3 times the height of the tree is:",
    "30°", ["60°", "45°", "75°"],
    "tanθ = 1/√3, so θ = 30°.",
    src(HD1, 9))
add("EASY", "The angle of elevation of the top of a tower from a point 50 m away from its foot is 30°. The height of the tower is:",
    "50/√3 m", ["50√3 m", "75√3 m", "75/√3 m"],
    "h = 50·tan30° = 50/√3 m.",
    src(HD1, 10))
add("EASY", "The length of a string between a kite and a point on the ground is 200 m. If the string makes an angle of 60° with the level ground and there is no slack, the height of the kite is:",
    "173.2 m", ["17.35 m", "123.2 m", "200√3 m"],
    "h = 200·sin60° = 100√3 ≈ 173.2 m.",
    src(HD1, 11))
add("MEDIUM", "The shadow of a tower becomes 60 m longer when the altitude of the sun changes from 45° to 30°. The height of the tower is:",
    "30(√3+1) m", ["20(√3+1) m", "24(√3+1) m", "30(√3−1) m"],
    "Shadows are h and h√3, so h(√3−1) = 60 and h = 60/(√3−1) = 30(√3+1) m.",
    src(HD1, 12))
add("HARD", "The elevation of the top of a tower from a point on the ground is 45°. On travelling 60 m towards the tower, the elevation becomes 60°. The height of the tower is:",
    "30(3+√3) m", ["30 m", "30(3−√3) m", "30√3 m"],
    "h − h/√3 = 60 ⇒ h(√3−1)/√3 = 60 ⇒ h = 60√3/(√3−1) = 30√3(√3+1) = 30(3+√3) m.",
    src(HD1, 13))
add("HARD", "The angles of elevation of a balloon from two consecutive kilometre-stones along a road are 30° and 60°. The height of the balloon above the ground is:",
    "√3/2 km", ["1/2 km", "2/√3 km", "3√3 km"],
    "The two stones are 1 km apart: h√3 − h/√3 = 1 ⇒ 2h/√3 = 1 ⇒ h = √3/2 km.",
    src(HD1, 14))
add("MEDIUM", "A man on the top of a 50 m high tower sees a car moving towards the tower at an angle of depression of 30°. After some time the angle of depression becomes 60°. The distance travelled by the car during this time is:",
    "100√3/3 m", ["50√3 m", "50√3/3 m", "100√3 m"],
    "Distances are 50√3 and 50/√3; difference = 50√3 − 50/√3 = 100/√3 = 100√3/3 m.",
    src(HD1, 15))
add("HARD", "There are two temples on the two banks of a river just opposite to each other. One temple is 54 m high. From the top of this temple, the angles of depression of the top and the foot of the other temple are 30° and 60° respectively. The height of the other temple is:",
    "36 m", ["18 m", "36√3 m", "18√3 m"],
    "River width = 54/√3 = 18√3. Drop to the other temple's top = 18√3·tan30° = 18, so its height = 54 − 18 = 36 m.",
    src(HD1, 16))

# --- _Height and Distance 02_.pdf (Lecture 2) ---
add("MEDIUM", "A vertical pole and a vertical tower stand on the same level ground. The pole is 10 m high. From the top of the pole, the angle of elevation of the top of the tower is 60° and the angle of depression of the foot of the tower is 30°. The height of the tower is:",
    "40 m", ["20 m", "30 m", "50 m"],
    "Horizontal gap = 10/tan30° = 10√3. Rise above the pole = 10√3·tan60° = 30, so the tower = 10 + 30 = 40 m.",
    src(HD2, 6))
add("MEDIUM", "A vertical post 15 ft high is broken at a certain height and its upper part, not completely separated, meets the ground at an angle of 30°. The height at which the post is broken is:",
    "5 ft", ["10 ft", "15√3(2−√3) ft", "5√3 ft"],
    "With broken height h and upper part 15 − h, sin30° = h/(15 − h) = 1/2 ⇒ 2h = 15 − h ⇒ h = 5 ft.",
    src(HD2, 7))
add("MEDIUM", "Two poles of equal height stand opposite to each other on either side of a road 100 m wide. From a point between them on the road, the angles of elevation of their tops are 30° and 60°. The height of each pole is:",
    "25√3 m", ["20√3 m", "28√3 m", "30√3 m"],
    "x·√3 = (100 − x)/√3 ⇒ 3x = 100 − x ⇒ x = 25; height = 25√3 m.",
    src(HD2, 8))
add("HARD", "The angle of elevation of the top of a tower from the bottom of a building is twice that from its top. If the tower is 75 m high and the angle of elevation of the top of the tower from the bottom of the building is 60°, the height of the building is:",
    "50 m", ["25 m", "37.5 m", "60 m"],
    "Horizontal gap = 75/√3 = 25√3; from the building top tan30° = (75 − h)/(25√3) ⇒ 75 − h = 25 ⇒ h = 50 m.",
    src(HD2, 9))
add("MEDIUM", "The angles of elevation of the top of a tower from two points on the ground at distances a and b from its base, in the same straight line with the tower, are complementary. The height of the tower is:",
    "√(ab)", ["a/b", "ab", "a²b²"],
    "For complementary angles (h/a)(h/b) = tanθ·cotθ = 1, so h² = ab and h = √(ab).",
    src(HD2, 10))
add("EASY", "The angles of elevation of the top of a tower from two points at distances 10 m and 5 m from its base, on the same straight line with it, are complementary. The height of the tower is:",
    "√50 m", ["5 m", "15 m", "√75 m"],
    "For complementary angles h = √(10·5) = √50 m.",
    src(HD2, 11))
add("HARD", "An aeroplane flying at a height of 5000 m passes vertically above another aeroplane, when the angles of elevation of the two aeroplanes from the same point on the ground are 60° and 45° respectively. The vertical distance between the aeroplanes at that instant is:",
    "5000(1−1/√3) m", ["5000(√3−1) m", "5000(3−√3) m", "4500 m"],
    "Horizontal distance = 5000/√3; the lower plane is 5000/√3 high (tan45° = 1), so the gap = 5000 − 5000/√3 = 5000(1−1/√3) m.",
    src(HD2, 12))
add("HARD", "The angle of elevation of an aeroplane from a point on the ground is 60°. After 10 seconds of flight the elevation changes to 30°. If the aeroplane is flying at a height of 1500√3 m, the speed of the plane is:",
    "300 m/s", ["200 m/s", "100 m/s", "150 m/s"],
    "Horizontal run = 1500√3·√3 − 1500√3/√3 = 4500 − 1500 = 3000 m in 10 s ⇒ 300 m/s.",
    src(HD2, 13))
add("HARD", "At the foot of a mountain the elevation of its summit is 45°. After ascending 3 km towards the mountain up a slope of 30° inclination, the elevation is found to be 60°. The height of the mountain is:",
    "(3/2)(√3+1) km", ["3(√3+1) km", "(3/2)(√3−1) km", "3√3 km"],
    "Ascending 3 km at 30°: horizontal 3√3/2, vertical 3/2. Then h − 3/2 = √3(h − 3√3/2) ⇒ h(√3−1) = 3 ⇒ h = (3/2)(√3+1) km.",
    src(HD2, 14))
add("HARD", "A tower standing on a horizontal plane subtends a certain angle at a point 160 m from its foot. On advancing 100 m towards it, the tower subtends an angle twice as before. The height of the tower is:",
    "80 m", ["100 m", "160 m", "200 m"],
    "tanθ = h/160, tan2θ = h/60. Using tan2θ = 2tanθ/(1−tan²θ): (8/3)t = 2t/(1−t²) ⇒ t² = 1/4 ⇒ h = 160/2 = 80 m.",
    src(HD2, 16))
add("HARD", "A round balloon of radius r subtends an angle α at the eye of an observer, while the angle of elevation of its centre is β. The height of its centre above the horizontal is:",
    "r sinβ·cosec(α/2)", ["r cosβ·cosec(α/2)", "r cosβ·sinβ", "r² sin(β/2)·cos(α/2)"],
    "Distance to the centre = r·cosec(α/2); the centre's height = that distance × sinβ = r·sinβ·cosec(α/2).",
    src(HD2, 17))
add("HARD", "From a point P, the tangent of the angle of elevation of a tower is 3/4. On walking 560 m towards the tower, the tangent of the angle of elevation becomes 4/3. The height of the tower is:",
    "960 m", ["720 m", "840 m", "1000 m"],
    "Base distances are 4h/3 and 3h/4; 4h/3 − 3h/4 = 560 ⇒ 7h/12 = 560 ⇒ h = 960 m.",
    src(HD2, 18))

# ─────────────────────────────────────────────────────────────────────────
# ORIGINAL SSC-STYLE QUESTIONS (69) filling the remaining per-level gaps
# ─────────────────────────────────────────────────────────────────────────

# EASY originals (25) — varied contexts and unknowns so no two stems collide.
easy = [
    ("A ladder 10 m long leans against a vertical wall, making an angle of 60° with the ground. Find the height on the wall reached by the ladder.",
     "5√3 m", ["5 m", "10√3 m", "10/√3 m"],
     "h = 10·sin60° = 5√3 m."),
    ("A ladder 13 m long has its foot 5 m away from a vertical wall. Find the height on the wall reached by the top of the ladder.",
     "12 m", ["8 m", "11 m", "12√2 m"],
     "h = √(13² − 5²) = 12 m."),
    ("A tower 15 m high casts a shadow 5√3 m long on level ground. Find the elevation of the sun.",
     "60°", ["30°", "45°", "75°"],
     "tanθ = 15/(5√3) = √3 ⇒ θ = 60°."),
    ("A kite is flying at a height of 60 m. If the string makes an angle of 30° with the ground, find the length of the string.",
     "120 m", ["60√3 m", "30√3 m", "90 m"],
     "L = 60/sin30° = 120 m."),
    ("From a point 30 m away from the foot of a tree on level ground, the angle of elevation of the top of the tree is 30°. Find the height of the tree.",
     "10√3 m", ["30√3 m", "15 m", "30 m"],
     "h = 30·tan30° = 10√3 m."),
    ("The angle of elevation of the top of a building from a point 20 m from its foot on the ground is 45°. Find the height of the building.",
     "20 m", ["20√3 m", "20/√3 m", "40 m"],
     "h = 20·tan45° = 20 m."),
    ("A flagstaff stands vertically on the ground. From a point 10 m away, the angle of elevation of its top is 60°. Find the height of the flagstaff.",
     "10√3 m", ["10/√3 m", "20 m", "10 m"],
     "h = 10·tan60° = 10√3 m."),
    ("A boy 1.5 m tall stands on level ground when the sun's elevation is 45°. Find the length of his shadow.",
     "1.5 m", ["3 m", "1.5√3 m", "0.75 m"],
     "Shadow = 1.5/tan45° = 1.5 m."),
    ("A guy wire runs from the top of an 18 m pole to a peg on the ground 6√3 m from its foot. Find the angle the wire makes with the ground.",
     "60°", ["30°", "45°", "75°"],
     "tanθ = 18/(6√3) = √3 ⇒ θ = 60°."),
    ("A vertical pole 5 m high stands on level ground. From a point on the ground, the angle of elevation of its top is 45°. Find the distance of the point from the foot of the pole.",
     "5 m", ["5√3 m", "5/√3 m", "10 m"],
     "d = 5/tan45° = 5 m."),
    ("From the top of a 30 m lighthouse, the angle of depression of a boat on the sea is 30°. Find the distance of the boat from the foot of the lighthouse.",
     "30√3 m", ["30/√3 m", "60 m", "15√3 m"],
     "d = 30/tan30° = 30√3 m."),
    ("A rope tied to the top of a 9 m pole is pegged to the ground so that the rope makes 45° with the ground. Find the distance of the peg from the foot of the pole.",
     "9 m", ["9√3 m", "9/√3 m", "18 m"],
     "d = 9/tan45° = 9 m."),
    ("A tower is 40 m high. Find the angle of elevation of its top from a point on the ground 40 m from its foot.",
     "45°", ["30°", "60°", "75°"],
     "tanθ = 40/40 = 1 ⇒ θ = 45°."),
    ("From the top of a 25 m tall building, the angle of depression of a car on the road is 45°. Find the distance of the car from the base of the building.",
     "25 m", ["25√3 m", "25/√3 m", "50 m"],
     "d = 25/tan45° = 25 m."),
    ("A ladder 20 m long reaches a window 10√3 m above the ground. Find the angle the ladder makes with the ground.",
     "60°", ["30°", "45°", "75°"],
     "sinθ = 10√3/20 = √3/2 ⇒ θ = 60°."),
    ("A kite string 80 m long makes an angle of 30° with the ground. Find the height of the kite above the ground.",
     "40 m", ["40√3 m", "80√3 m", "20 m"],
     "h = 80·sin30° = 40 m."),
    ("From a point 100 m from the foot of a tower on level ground, the angle of elevation of its top is 60°. Find the height of the tower.",
     "100√3 m", ["100/√3 m", "200 m", "50√3 m"],
     "h = 100·tan60° = 100√3 m."),
    ("A man 1.8 m tall casts a shadow 1.8√3 m long. Find the altitude of the sun.",
     "30°", ["45°", "60°", "75°"],
     "tanθ = 1.8/(1.8√3) = 1/√3 ⇒ θ = 30°."),
    ("The elevation of the top of a cliff from a point 60 m away from its base is 30°. Find the height of the cliff.",
     "20√3 m", ["60√3 m", "30 m", "10√3 m"],
     "h = 60·tan30° = 60/√3 = 20√3 m."),
    ("An 8 m ladder rests against a wall making an angle of 45° with the ground. Find the height on the wall reached by the ladder.",
     "4√2 m", ["8√2 m", "4 m", "2√2 m"],
     "h = 8·sin45° = 4√2 m."),
    ("A tower stands on level ground. From a point 30√3 m from its foot, the angle of elevation of its top is 30°. Find the height of the tower.",
     "30 m", ["30√3 m", "90 m", "15 m"],
     "h = 30√3·tan30° = 30 m."),
    ("From the top of a 12 m high pole, the angle of depression of a point on the ground is 60°. Find the distance of the point from the foot of the pole.",
     "4√3 m", ["12√3 m", "6 m", "8√3 m"],
     "d = 12/tan60° = 12/√3 = 4√3 m."),
    ("The string of a kite is 150 m long and makes an angle of 60° with the ground. Find the height of the kite.",
     "75√3 m", ["75 m", "150√3 m", "50√3 m"],
     "h = 150·sin60° = 75√3 m."),
    ("From a point on the ground, the angle of elevation of the top of a hill is 45°, and the hill is 500 m high. Find the distance of the point from the base of the hill.",
     "500 m", ["500√3 m", "500/√3 m", "250 m"],
     "d = 500/tan45° = 500 m."),
    ("A vertical mast 24 m high stands on level ground. Its shadow is 8√3 m long. Find the elevation of the sun.",
     "60°", ["30°", "45°", "75°"],
     "tanθ = 24/(8√3) = √3 ⇒ θ = 60°."),
]
for stem, ans, wrongs, proof in easy:
    add("EASY", stem, ans, wrongs, proof)

# MEDIUM originals (24)
medium = [
    ("The angle of elevation of the top of a tower from a point on the ground is 30°. On walking 40 m towards the tower, the angle of elevation becomes 60°. Find the height of the tower.",
     "20√3 m", ["40√3 m", "20 m", "40/√3 m"],
     "h√3 − h/√3 = 40 ⇒ 2h/√3 = 40 ⇒ h = 20√3 m."),
    ("Two observers stand on opposite sides of a tower, 60 m apart. They find the angle of elevation of the top of the tower to be 30° and 60°. Find the height of the tower.",
     "15√3 m", ["30√3 m", "20√3 m", "12√3 m"],
     "h(cot30° + cot60°) = 60 ⇒ h(4/√3) = 60 ⇒ h = 15√3 m."),
    ("The angles of elevation of the top of a tower from two points 25 m and 16 m from its base, on the same side in a straight line with it, are complementary. Find the height of the tower.",
     "20 m", ["25 m", "16 m", "41 m"],
     "For complementary angles h = √(25·16) = 20 m."),
    ("A flagstaff 5 m tall stands on the top of a tower. From a point on the ground, the angle of elevation of the top of the flagstaff is 60° and that of the top of the tower is 45°. Find the height of the tower.",
     "5(√3+1)/2 m", ["5(√3−1)/2 m", "5√3 m", "10 m"],
     "Distance = H; (H+5)/H = √3 ⇒ H(√3−1) = 5 ⇒ H = 5/(√3−1) = 5(√3+1)/2 m."),
    ("A man on the top of a 60 m tower observes two cars on the same side of the tower at angles of depression 30° and 45°. Find the distance between the cars.",
     "60(√3−1) m", ["60(√3+1) m", "60√3 m", "30(√3−1) m"],
     "Distances are 60√3 and 60; gap = 60√3 − 60 = 60(√3−1) m."),
    ("The shadow of a tower is 36 m longer when the sun's altitude is 30° than when it is 60°. Find the height of the tower.",
     "18√3 m", ["36√3 m", "18 m", "12√3 m"],
     "h√3 − h/√3 = 36 ⇒ 2h/√3 = 36 ⇒ h = 18√3 m."),
    ("A kite is flying at a height of 75 m. A boy first sees it at an elevation of 30° and after some time at 60°. Find the horizontal distance the kite moved.",
     "50√3 m", ["25√3 m", "75√3 m", "100√3 m"],
     "75√3 − 75/√3 = 75√3 − 25√3 = 50√3 m."),
    ("From the top of a 45 m lighthouse, the angles of depression of two ships on opposite sides are 30° and 45°. Find the distance between the ships.",
     "45(√3+1) m", ["45(√3−1) m", "45√3 m", "90 m"],
     "Distances are 45√3 and 45; total = 45√3 + 45 = 45(√3+1) m."),
    ("A bridge is 10 m above the water surface. The angle of depression of a boat on the water from a point on the bridge is 30°. Find the horizontal distance of the boat from the point directly below the bridge.",
     "10√3 m", ["10/√3 m", "20 m", "10 m"],
     "d = 10/tan30° = 10√3 m."),
    ("From a point on the ground, the tangent of the angle of elevation of the top of a 25 m tower is 5/12. Find the horizontal distance of the point from the foot of the tower.",
     "60 m", ["25 m", "12 m", "48 m"],
     "d = 25 ÷ (5/12) = 60 m."),
    ("A man 1.6 m tall stands 28.4 m from a tower and finds the angle of elevation of its top to be 45°. Find the height of the tower.",
     "30 m", ["28.4 m", "26.8 m", "31.6 m"],
     "Height above the eye = 28.4·tan45° = 28.4; tower = 28.4 + 1.6 = 30 m."),
    ("The angle of elevation of a cloud from a point 60 m above a lake is 30° and the angle of depression of its reflection in the lake is 60°. Find the height of the cloud above the lake.",
     "120 m", ["90 m", "150 m", "180 m"],
     "(H−60)/d = tan30°, (H+60)/d = tan60° ⇒ (H+60)/(H−60) = 3 ⇒ H = 120 m."),
    ("A statue 2 m tall stands on the top of a pedestal. From a point on the ground, the angle of elevation of the top of the statue is 60° and that of the top of the pedestal is 45°. Find the height of the pedestal.",
     "(√3+1) m", ["(√3−1) m", "2√3 m", "2 m"],
     "Distance = H; (H+2)/H = √3 ⇒ H(√3−1) = 2 ⇒ H = 2/(√3−1) = √3+1 m."),
    ("From the top of a 120 m high cliff, the angles of depression of two boats on the sea on the same side are 30° and 60°. Find the distance between the boats.",
     "80√3 m", ["40√3 m", "120(√3−1) m", "60√3 m"],
     "Distances are 120√3 and 40√3; gap = 120√3 − 40√3 = 80√3 m."),
    ("A mast stands on the top of a cliff. From a point 30 m from the base of the cliff, the angle of elevation of the top of the mast is 60° and that of its base is 30°. Find the height of the mast.",
     "20√3 m", ["10√3 m", "30√3 m", "20 m"],
     "Cliff = 30·tan30° = 10√3; mast top = 30·tan60° = 30√3; mast = 20√3 m."),
    ("The angle of elevation of the top of a tower from a point A due south of it is 30°, and from a point B due east of it is 45°. If AB = 100 m, find the height of the tower.",
     "50 m", ["100 m", "50√3 m", "100/√3 m"],
     "OA = h√3 and OB = h with OA ⊥ OB; 3h² + h² = 100² ⇒ h = 50 m."),
    ("Two poles of heights 6 m and 11 m stand on level ground. If the distance between their feet is 12 m, find the distance between their tops.",
     "13 m", ["12 m", "17 m", "5 m"],
     "√(12² + 5²) = 13 m."),
    ("A person walks 20 m away from a tower and finds that the angle of elevation of its top falls from 60° to 30°. Find the height of the tower.",
     "10√3 m", ["20√3 m", "10 m", "20/√3 m"],
     "h(cot30° − cot60°) = 20 ⇒ 2h/√3 = 20 ⇒ h = 10√3 m."),
    ("A ladder 25 m long reaches a window 20 m above the ground on one side of a street. Keeping its foot fixed, the ladder is turned to the other side to reach a window 7 m high. Find the width of the street.",
     "39 m", ["35 m", "32 m", "45 m"],
     "√(25² − 20²) = 15 and √(25² − 7²) = 24; width = 15 + 24 = 39 m."),
    ("The angle of elevation of the top of a building from the foot of a tower is 30°, and that of the top of the tower from the foot of the building is 60°. If the tower is 50 m high, find the height of the building.",
     "50/3 m", ["25 m", "50√3/3 m", "25/3 m"],
     "Gap = 50/√3; building = (50/√3)·tan30° = 50/3 m."),
    ("From the top of a 100 m tower, a man observes two cars on the ground on opposite sides at angles of depression 30° and 45°. Find the distance between the cars.",
     "100(√3+1) m", ["100(√3−1) m", "100√3 m", "200 m"],
     "Distances are 100√3 and 100; total = 100√3 + 100 = 100(√3+1) m."),
    ("A flagpole 12 m high is fixed on the top of a tower. From a point on the ground, the angle of elevation of the top of the flagpole is 60° and that of the top of the tower is 30°. Find the height of the tower.",
     "6 m", ["12 m", "4 m", "18 m"],
     "Distance = H√3; (H+12)/(H√3) = √3 ⇒ H + 12 = 3H ⇒ H = 6 m."),
    ("The angle of elevation of the top of a tower from the top and the bottom of a 10 m high building are 30° and 45° respectively. Find the height of the tower.",
     "5(3+√3) m", ["10(3+√3) m", "5(3−√3) m", "15 m"],
     "Distance = H; (H−10)/H = 1/√3 ⇒ H(1−1/√3) = 10 ⇒ H = 5(3+√3) m."),
    ("The angles of depression of the top and the bottom of an 8 m tall building from the top of a multi-storeyed building are 30° and 45°. Find the height of the multi-storeyed building.",
     "4(3+√3) m", ["8(3+√3) m", "4(3−√3) m", "12 m"],
     "Distance = H; (H−8)/H = 1/√3 ⇒ H(1−1/√3) = 8 ⇒ H = 4(3+√3) m."),
]
for stem, ans, wrongs, proof in medium:
    add("MEDIUM", stem, ans, wrongs, proof)

# HARD originals (20)
hard = [
    ("A tree is broken by the wind so that its top touches the ground 8 m from the foot, making an angle of 30° with the ground. Find the original height of the tree.",
     "8√3 m", ["16 m", "8/√3 m", "16/√3 m"],
     "Upper part = 8/cos30° = 16/√3 and broken height = (16/√3)·sin30° = 8/√3; total = 24/√3 = 8√3 m."),
    ("A man in a boat rowing away from a 150 m high lighthouse takes 2 minutes to change the angle of elevation of its top from 60° to 45°. Find the speed of the boat.",
     "5(3−√3)/12 m/s", ["5(3+√3)/12 m/s", "5(3−√3)/6 m/s", "15(3−√3) m/s"],
     "150 − 50√3 = 50(3−√3) m in 120 s ⇒ speed = 5(3−√3)/12 m/s."),
    ("An aeroplane flying at 240 m/s is observed from a point on the ground at an angle of elevation of 60°. After 15 seconds the elevation becomes 30°. Find the height of the aeroplane.",
     "1800√3 m", ["1200√3 m", "3600√3 m", "1800 m"],
     "Run = 240×15 = 3600 = h(cot30° − cot60°) = 2h/√3 ⇒ h = 1800√3 m."),
    ("A person on the bank of a river observes the angle of elevation of a tree on the opposite bank as 60°. On retreating 40 m from the bank, the angle becomes 30°. Find the height of the tree.",
     "20√3 m", ["40√3 m", "20 m", "40/√3 m"],
     "w√3 = (w+40)/√3 ⇒ 3w = w+40 ⇒ w = 20, h = 20√3 m."),
    ("A car approaches a 60 m tower. Its angles of depression from the top change from 30° to 45° in 10 seconds. Find the speed of the car.",
     "6(√3−1) m/s", ["6(√3+1) m/s", "3(√3−1) m/s", "60(√3−1) m/s"],
     "60√3 − 60 = 60(√3−1) m in 10 s ⇒ 6(√3−1) m/s."),
    ("A tower stands on level ground. The elevation of its top is measured from two stations on the same side in line with the tower, and the two angles are found to be complementary. If the stations are 12 m and 27 m from the base, how tall is the tower?",
     "18 m", ["12 m", "27 m", "39 m"],
     "For complementary angles h = √(12·27) = √324 = 18 m."),
    ("A boat is observed from the top of a 150 m cliff. The angle of depression changes from 30° to 45° in 30 seconds as the boat moves towards the cliff. Find its speed.",
     "5(√3−1) m/s", ["5(√3+1) m/s", "15(√3−1) m/s", "5√3 m/s"],
     "150√3 − 150 = 150(√3−1) m in 30 s ⇒ 5(√3−1) m/s."),
    ("A man on the top of a tower observes a car approaching the tower at a uniform speed. If the angle of depression changes from 30° to 45° in 12 minutes, how much longer will the car take to reach the foot of the tower?",
     "6(√3+1) minutes", ["6(√3−1) minutes", "12(√3+1) minutes", "4 minutes"],
     "The car covers h(√3−1) in 12 min; the remaining h needs 12/(√3−1) = 6(√3+1) min."),
    ("From the top of a 60 m high building, the angles of depression of the top and the bottom of a vertical lamp post are 30° and 60°. Find the height of the lamp post.",
     "40 m", ["20 m", "30 m", "45 m"],
     "Gap = 60/√3 = 20√3; drop to the post's top = 20√3·tan30° = 20; post = 60 − 20 = 40 m."),
    ("The angle of elevation of the top of a tower from a point A on the ground is 60°. From a point B, 40 m vertically above A, the angle of elevation is 30°. Find the height of the tower.",
     "60 m", ["80 m", "120 m", "40 m"],
     "d = H/√3; (H−40)/d = tan30° ⇒ (H−40)√3/H = 1/√3 ⇒ 3(H−40) = H ⇒ H = 60 m."),
    ("Two poles of equal height stand on either side of a road 80 m wide. From a point between them on the road, the angles of elevation of their tops are 60° and 30°. Find the height of the poles.",
     "20√3 m", ["40√3 m", "40 m", "80/√3 m"],
     "d₁√3 = d₂/√3 and d₁ + d₂ = 80 ⇒ d₁ = 20, d₂ = 60, h = 20√3 m."),
    ("A highway leads to the foot of a tower. A car is seen from the top of the tower at an angle of depression of 30°. Six seconds later the angle of depression is 60°. How much longer will the car take to reach the foot of the tower?",
     "3 seconds", ["2 seconds", "6 seconds", "4.5 seconds"],
     "The car covers 2h/√3 in 6 s; the remaining h/√3 needs 3 s."),
    ("A man on the deck of a ship 10 m above water level observes the angle of elevation of the top of a hill as 60° and the angle of depression of its base as 30°. Find the height of the hill.",
     "40 m", ["30 m", "20 m", "50 m"],
     "Gap = 10/tan30° = 10√3; rise above the deck = 10√3·√3 = 30; hill = 10 + 30 = 40 m."),
    ("From the top of a 90 m high cliff, the angles of depression of two ships on the same side are 30° and 45°. Find the distance between the ships.",
     "90(√3−1) m", ["90√3 m", "90(√3+1) m", "45(√3−1) m"],
     "Distances are 90√3 and 90; gap = 90√3 − 90 = 90(√3−1) m."),
    ("An observer 1.5 m tall is 28.5 m away from a chimney. The angle of elevation of the top of the chimney from his eye is 45°. Find the height of the chimney.",
     "30 m", ["28.5 m", "27 m", "31.5 m"],
     "Height above the eye = 28.5·tan45° = 28.5; chimney = 28.5 + 1.5 = 30 m."),
    ("A transmission tower is fixed on the top of a 20 m high building. From a point on the ground, the angles of elevation of the top and the bottom of the tower are 60° and 45°. Find the height of the transmission tower.",
     "20(√3−1) m", ["20(√3+1) m", "20√3 m", "20 m"],
     "Gap = 20; tower top = 20·tan60° = 20√3; tower = 20√3 − 20 = 20(√3−1) m."),
    ("From the top of a 7 m high building, the angle of elevation of the top of a cable tower is 60° and the angle of depression of its foot is 45°. Find the height of the cable tower.",
     "7(1+√3) m", ["7(√3−1) m", "14 m", "7√3 m"],
     "Gap = 7; tower top = 7 + 7√3 = 7(1+√3) m."),
    ("The angles of elevation of the top of a rock from the top and the foot of a 20 m high building are 45° and 60°. Find the height of the rock.",
     "10(3+√3) m", ["20(3+√3) m", "10(3−√3) m", "30 m"],
     "d = R/√3; (R−20)/d = tan45° ⇒ R(1−1/√3) = 20 ⇒ R = 10(3+√3) m."),
    ("From the top of a 60 m high building, the angle of elevation of the top of a tower is 30° and the angle of depression of its base is 45°. Find the height of the tower.",
     "60+20√3 m", ["60+60√3 m", "80 m", "40√3 m"],
     "Gap = 60; rise = 60·tan30° = 20√3; tower = 60 + 20√3 m."),
    ("A tower is 100 m high and a flag is hoisted on its top. From a point 100 m from the foot of the tower, the angle of elevation of the top of the flag is 60°. Find the height of the flag.",
     "100(√3−1) m", ["100(√3+1) m", "100√3 m", "50 m"],
     "Flag top = 100·tan60° = 100√3; flag = 100√3 − 100 = 100(√3−1) m."),
]
for stem, ans, wrongs, proof in hard:
    add("HARD", stem, ans, wrongs, proof)


def norm(s):
    return " ".join(unicodedata.normalize("NFKC", s).casefold().split())


def main():
    counts = Counter(r["difficulty"] for r in ROWS)
    if len(ROWS) != 90 or counts != {"EASY": 30, "MEDIUM": 30, "HARD": 30}:
        raise SystemExit(f"bad batch count {len(ROWS)} {counts}")
    for i, r in enumerate(ROWS):
        if len(set(norm(v) for v in r["options"].values())) != 4:
            raise SystemExit(f"option collision row {i+1}: {r['options']}")
        if r["options"][r["correct_option"]] != LEDGER[i]["expected_answer"]:
            raise SystemExit(f"key/ledger mismatch row {i+1}")
    collisions = []
    for i, r in enumerate(ROWS):
        for other in ROWS[:i]:
            a, b = norm(other["question_text"]), norm(r["question_text"])
            ratio = SequenceMatcher(None, a, b).ratio()
            if a == b or ratio >= .95:
                collisions.append((round(ratio, 4), other["question_text"], r["question_text"]))
    if collisions:
        for ratio, a, b in collisions:
            print(f"COLLISION {ratio}\n  A: {a}\n  B: {b}")
        raise SystemExit(f"{len(collisions)} near duplicate pair(s)")
    (BASE / "data/height_distance_verified_batch.json").write_text(
        json.dumps({"questions": ROWS}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (BASE / "data/height_distance_answer_ledger.json").write_text(
        json.dumps(LEDGER, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("WROTE", len(ROWS), dict(counts),
          "source", sum(r["source"] != ORIGINAL for r in ROWS),
          "original", sum(r["source"] == ORIGINAL for r in ROWS))


if __name__ == "__main__":
    main()
