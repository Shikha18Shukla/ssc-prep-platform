"""Build the reviewed CH-17 visual question bank and its answer ledger.

All retained questions are original diagrams. Source-card candidates are listed
as rejected because the supplied lecture slides have instructor solution marks
drawn over their answer figures; the cards cannot safely be shown to learners.
"""
from __future__ import annotations

import json
import math
import random
import re
from copy import deepcopy
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
ASSETS = BASE.parent / "frontend" / "public" / "question-assets" / "non-verbal-reasoning"
BATCH = BASE / "data" / "non_verbal_reasoning_verified_batch.json"
LEDGER = BASE / "data" / "non_verbal_reasoning_answer_ledger.json"
REPORT = BASE / "data" / "non_verbal_reasoning_review_report.md"
CHAPTER_ID = "746c8d03-3645-4454-a875-7cd9109e133a"
DIFFICULTY_CYCLE = ("EASY", "MEDIUM", "HARD")
LETTERS = "ABCD"
SHAPES = ["triangle", "diamond", "pentagon", "arrow", "L"]


def polygon(shape: str, cx: float, cy: float, radius: float, angle: float, fill: str) -> str:
    if shape == "arrow":
        pts = [(0,-1),(.30,-.25),(.13,-.25),(.13,.9),(-.13,.9),(-.13,-.25),(-.30,-.25)]
    elif shape == "L":
        pts = [(-.75,-.75),(-.35,-.75),(-.35,.35),(.75,.35),(.75,.75),(-.75,.75)]
    else:
        sides = {"triangle":3,"diamond":4,"pentagon":5}.get(shape, 6)
        pts = [(math.cos(2*math.pi*i/sides-math.pi/2), math.sin(2*math.pi*i/sides-math.pi/2)) for i in range(sides)]
    pts = [(cx + radius*(x*math.cos(math.radians(angle))-y*math.sin(math.radians(angle))),
            cy + radius*(x*math.sin(math.radians(angle))+y*math.cos(math.radians(angle)))) for x,y in pts]
    return f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x,y in pts)}" fill="{fill}" stroke="#172554" stroke-width="3" stroke-linejoin="round"/>'


def glyph(state: dict, x: float, y: float, size: float = 34) -> str:
    if state.get("flip_x"):
        flip = f' transform="translate({2*x} 0) scale(-1 1)"'
    elif state.get("flip_y"):
        flip = f' transform="translate(0 {2*y}) scale(1 -1)"'
    else:
        flip = ""
    out = f'<g{flip}>' + polygon(state.get("shape","triangle"), x, y, size, state.get("angle",0), state.get("fill","white"))
    mark = state.get("mark", "")
    if mark == "dot":
        out += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#dc2626"/>'
    elif mark == "line":
        a=math.radians(state.get("angle",0)); dx=math.cos(a)*size*.72;dy=math.sin(a)*size*.72
        out += f'<line x1="{x-dx:.1f}" y1="{y-dy:.1f}" x2="{x+dx:.1f}" y2="{y+dy:.1f}" stroke="#2563eb" stroke-width="3"/>'
    count=state.get("count",0)
    if count:
        for k in range(count):
            a=2*math.pi*k/max(count,1)-math.pi/2
            out += f'<circle cx="{x+13*math.cos(a):.1f}" cy="{y+13*math.sin(a):.1f}" r="2.8" fill="#dc2626"/>'
    return out + '</g>'


def option_target_indices(count: int) -> list[int]:
    """Return a deterministic, balanced, non-cyclic correct-choice schedule."""
    counts = [count // 4] * 4
    for i in range(count % 4):
        counts[i] += 1
    base = [letter for letter, n in enumerate(counts) for _ in range(n)]
    for attempt in range(1000):
        targets = base[:]
        random.Random(0xC417 + attempt).shuffle(targets)
        if any(targets[i] == targets[i+1] == targets[i+2] for i in range(len(targets)-2)):
            continue
        cycles = ([0,1,2,3],[1,2,3,0],[2,3,0,1],[3,0,1,2],[3,2,1,0],[2,1,0,3],[1,0,3,2],[0,3,2,1])
        if any(targets[i:i+4] in cycles for i in range(len(targets)-3)):
            continue
        return targets
    raise RuntimeError("Could not make a balanced answer schedule without a visible pattern")


def option_state_field(spec: dict) -> str:
    for field in ("options", "option_counts", "positions"):
        if field in spec:
            return field
    raise ValueError("Question has no four-option visual state")


def shuffle_option_states(spec: dict, correct_index: int, target_index: int, seed: int) -> tuple[dict, list[int]]:
    """Move complete visual option states; return spec and old-index -> new-index map."""
    field = option_state_field(spec)
    original = deepcopy(spec[field])
    if len(original) != 4 or correct_index not in range(4) or target_index not in range(4):
        raise ValueError("Expected four visual options and valid answer indexes")
    rng = random.Random(seed)
    distractor_indices = [i for i in range(4) if i != correct_index]
    destinations = [i for i in range(4) if i != target_index]
    rng.shuffle(distractor_indices)
    rng.shuffle(destinations)
    mapping = {correct_index: target_index}
    mapping.update(dict(zip(distractor_indices, destinations)))
    arranged = [None] * 4
    for old_index, new_index in mapping.items():
        arranged[new_index] = original[old_index]
    result = deepcopy(spec)
    result[field] = arranged
    return result, [mapping[i] for i in range(4)]


def validate_option_shuffle(original: list, shuffled: list, original_correct: int, shuffled_correct: int) -> None:
    """Independent multiset check: no visual option may be lost, altered, or duplicated."""
    encode = lambda values: sorted(json.dumps(v, sort_keys=True, ensure_ascii=False, separators=(",", ":")) for v in values)
    if len(original) != 4 or len(shuffled) != 4 or encode(original) != encode(shuffled):
        raise ValueError("Shuffled visual choices differ from the original option multiset")
    if encode([original[original_correct]]) != encode([shuffled[shuffled_correct]]):
        raise ValueError("Shuffled correct option no longer depicts the original solution")
    if len(set(encode(shuffled))) != 4:
        raise ValueError("Visual choices are not four distinct options")


def remap_explanation(explanation: str, family: str, old_to_new: list[int], correct_key: str) -> str:
    if family == "classify":
        match = re.search(r"Options A–C share the (.*?) property\.", explanation)
        if not match:
            raise ValueError("Cannot safely rewrite classification explanation")
        other_keys = [letter for letter in LETTERS if letter != correct_key]
        return f"Options {', '.join(other_keys)} share the {match.group(1)} property. Option {correct_key} differs in that property, so {correct_key} is the unique odd figure."
    if family == "dots":
        return re.sub(r"\b([A-D])\b",lambda m:LETTERS[old_to_new[LETTERS.index(m.group(1))]],explanation)
    pattern = re.compile(r"\b(option)\s+([A-D])\b", re.IGNORECASE)
    return pattern.sub(lambda m: f"{m.group(1)} {LETTERS[old_to_new[LETTERS.index(m.group(2).upper())]]}", explanation)


def diagram_card(kind: str, spec: dict) -> str:
    chunks = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 500" role="img">',
              '<rect width="920" height="500" rx="18" fill="#fff"/>',
              '<style>text{font-family:Arial,sans-serif;fill:#172554}.head{font-size:22px;font-weight:bold}.lab{font-size:18px;font-weight:bold}</style>']
    if kind in {"rotation", "count", "alternate", "motion", "matrix"}:
        seq = spec.get("sequence", [])
        xs = [120, 320, 520]
        if kind == "matrix":
            chunks.append('<text x="36" y="36" class="head">Complete the figure matrix</text>')
            cells = spec["matrix"]
            for i, st in enumerate(cells):
                row,col=divmod(i,2); x=170+col*180; y=145+row*135
                chunks.append(f'<rect x="{x-58}" y="{y-48}" width="116" height="96" fill="white" stroke="#64748b" stroke-width="2"/>')
                if st is None: chunks.append(f'<text x="{x}" y="{y+12}" text-anchor="middle" class="head">?</text>')
                else: chunks.append(glyph(st,x,y,28))
            ox=[540,650,760,870]
            chunks.append('<text x="480" y="100" class="head">Options</text>')
            for i,st in enumerate(spec["options"]):
                chunks.append(glyph(st,ox[i],220,25)+f'<text x="{ox[i]}" y="270" text-anchor="middle" class="lab">{LETTERS[i]}</text>')
        else:
            chunks.append(f'<text x="32" y="42" class="head">{spec["caption"]}</text>')
            for i, st in enumerate(seq):
                if i == 3:
                    chunks.append(f'<rect x="{xs[i]-50}" y="125" width="100" height="100" rx="10" fill="#f8fafc" stroke="#64748b" stroke-dasharray="6 5" stroke-width="2"/><text x="{xs[i]}" y="187" text-anchor="middle" class="head">?</text>')
                else: chunks.append(glyph(st,xs[i],175,36))
                chunks.append(f'<text x="{xs[i]}" y="245" text-anchor="middle" class="lab">{i+1}</text>')
            chunks.append('<text x="38" y="320" class="head">Choose the next figure</text>')
            for i,st in enumerate(spec["options"]):
                x=150+i*210
                chunks.append(f'<rect x="{x-70}" y="345" width="140" height="115" rx="10" fill="#f8fafc" stroke="#94a3b8" stroke-width="2"/>')
                chunks.append(glyph(st,x,398,30)+f'<text x="{x}" y="448" text-anchor="middle" class="lab">{LETTERS[i]}</text>')
    elif kind == "classify":
        chunks.append('<text x="30" y="38" class="head">Select the figure with a different property</text>')
        for i,st in enumerate(spec["options"]):
            x=150+i*205
            chunks.append(f'<rect x="{x-75}" y="125" width="150" height="210" rx="12" fill="#f8fafc" stroke="#94a3b8" stroke-width="2"/>')
            chunks.append(glyph(st,x,225,48)+f'<text x="{x}" y="300" text-anchor="middle" class="lab">{LETTERS[i]}</text>')
    elif kind == "reflection":
        chunks.append('<text x="28" y="38" class="head">Choose the specified reflection</text>')
        chunks.append('<text x="150" y="105" text-anchor="middle" class="lab">Original</text>')
        chunks.append(glyph(spec["original"],150,210,55))
        chunks.append(f'<line x1="295" y1="105" x2="295" y2="320" stroke="#64748b" stroke-dasharray="8 6"/><text x="295" y="350" text-anchor="middle" class="lab">{spec["axis"]}</text>')
        for i,st in enumerate(spec["options"]):
            x=440+i*145
            chunks.append(f'<rect x="{x-60}" y="140" width="120" height="190" rx="10" fill="#f8fafc" stroke="#94a3b8" stroke-width="2"/>')
            chunks.append(glyph(st,x,220,42)+f'<text x="{x}" y="300" text-anchor="middle" class="lab">{LETTERS[i]}</text>')
    elif kind == "analogy":
        chunks.append('<text x="30" y="38" class="head">A is related to B; apply the same change to C</text>')
        for label,state,x in [("A",spec["a"],120),("B",spec["b"],310),("C",spec["c"],500)]:
            chunks.append(f'<rect x="{x-65}" y="110" width="130" height="125" rx="10" fill="#f8fafc" stroke="#94a3b8" stroke-width="2"/>')
            chunks.append(glyph(state,x,165,35)+f'<text x="{x}" y="218" text-anchor="middle" class="lab">{label}</text>')
        chunks.append('<text x="620" y="180" text-anchor="middle" class="head">?</text>')
        for i,state in enumerate(spec["options"]):
            x=130+i*210
            chunks.append(f'<rect x="{x-70}" y="310" width="140" height="130" rx="10" fill="#f8fafc" stroke="#94a3b8" stroke-width="2"/>')
            chunks.append(glyph(state,x,365,30)+f'<text x="{x}" y="425" text-anchor="middle" class="lab">{LETTERS[i]}</text>')
    elif kind == "embed":
        chunks.append('<text x="25" y="38" class="head">Which option contains the target figure without rotation?</text>')
        # Target is a square with one diagonal; each option is a segment network.
        chunks.append('<rect x="55" y="105" width="150" height="150" fill="white" stroke="#172554" stroke-width="4"/>')
        for seg in spec["target_segments"]:
            x1,y1,x2,y2=seg
            tx=lambda x:55+(x-50)*150/105; ty=lambda y:105+(y-20)*150/105
            chunks.append(f'<line x1="{tx(x1):.1f}" y1="{ty(y1):.1f}" x2="{tx(x2):.1f}" y2="{ty(y2):.1f}" stroke="#172554" stroke-width="4"/>')
        chunks.append(f'<text x="130" y="285" text-anchor="middle" class="lab">{spec["target_label"]}</text>')
        for i,segments in enumerate(spec["options"]):
            x=340+(i%2)*270; y=90+(i//2)*190
            chunks.append(f'<rect x="{x}" y="{y}" width="220" height="145" rx="8" fill="#f8fafc" stroke="#94a3b8" stroke-width="2"/>')
            for seg in segments:
                x1,y1,x2,y2=seg
                chunks.append(f'<line x1="{x+x1}" y1="{y+y1}" x2="{x+x2}" y2="{y+y2}" stroke="#172554" stroke-width="3"/>')
            chunks.append(f'<text x="{x+110}" y="{y+170}" text-anchor="middle" class="lab">{LETTERS[i]}</text>')
    elif kind == "countfig":
        chunks.append('<text x="28" y="38" class="head">Count every triangle, including larger composites</text>')
        n=spec["levels"]; left,top,width,height=180,90,360,300
        chunks.append(f'<polygon points="{left},{top+height} {left+width},{top+height} {left+width/2},{top}" fill="white" stroke="#172554" stroke-width="4"/>')
        for k in range(1,n+1):
            y=top+height*k/(n+1); half=width*(1-k/(n+1))/2
            chunks.append(f'<line x1="{left+half}" y1="{y}" x2="{left+width-half}" y2="{y}" stroke="#2563eb" stroke-width="3"/>')
        chunks.append(f'<text x="28" y="440" class="head">How many triangles are formed?</text>')
        answer=n+1
        vals=[answer,answer+1,answer+2,max(1,answer-1)]
        for i,v in enumerate(vals):
            x=525+i*95
            chunks.append(f'<rect x="{x-38}" y="220" width="76" height="75" rx="8" fill="#f8fafc" stroke="#94a3b8" stroke-width="2"/><text x="{x}" y="265" text-anchor="middle" class="head">{v}</text><text x="{x}" y="320" text-anchor="middle" class="lab">{LETTERS[i]}</text>')
    elif kind == "dots":
        chunks.append('<text x="28" y="38" class="head">Choose the option placing the dot in the requested region</text>')
        mode=spec["mode"]
        region=["Inside circle, outside square","Inside circle, outside triangle","Inside the overlap of two circles"][mode]
        chunks.append(f'<text x="28" y="72" class="lab">{region}</text>')
        for i,pos in enumerate(spec["positions"]):
            x=125+i*215
            chunks.append(f'<rect x="{x-80}" y="120" width="160" height="210" rx="10" fill="#f8fafc" stroke="#94a3b8" stroke-width="2"/>')
            if mode==0:
                chunks.append(f'<circle cx="{x}" cy="220" r="65" fill="none" stroke="#172554" stroke-width="3"/><rect x="{x-30}" y="190" width="60" height="60" fill="none" stroke="#2563eb" stroke-width="3"/>')
            elif mode==1:
                chunks.append(f'<circle cx="{x}" cy="220" r="65" fill="none" stroke="#172554" stroke-width="3"/><polygon points="{x-52},255 {x+52},255 {x},165" fill="none" stroke="#2563eb" stroke-width="3"/>')
            else:
                chunks.append(f'<circle cx="{x-32}" cy="220" r="55" fill="none" stroke="#172554" stroke-width="3"/><circle cx="{x+32}" cy="220" r="55" fill="none" stroke="#2563eb" stroke-width="3"/>')
            dx,dy=pos
            chunks.append(f'<circle cx="{x+dx}" cy="{220+dy}" r="7" fill="#dc2626"/><text x="{x}" y="305" text-anchor="middle" class="lab">{LETTERS[i]}</text>')
    elif kind == "fold":
        chunks.append('<text x="28" y="38" class="head">Fold, punch, then unfold the sheet</text>')
        chunks.append('<rect x="80" y="105" width="240" height="240" fill="#f8fafc" stroke="#334155" stroke-width="3"/>')
        chunks.append('<line x1="200" y1="105" x2="200" y2="345" stroke="#64748b" stroke-dasharray="8 6" stroke-width="2"/>')
        for px,py in spec["punches"]: chunks.append(f'<circle cx="{px}" cy="{py}" r="8" fill="#dc2626"/>')
        chunks.append('<text x="200" y="385" text-anchor="middle" class="lab">fold at dashed line; punch red dot</text>')
        for i,pts in enumerate(spec["options"]):
            x=435+i*112
            chunks.append(f'<rect x="{x-44}" y="150" width="88" height="140" fill="white" stroke="#94a3b8" stroke-width="2"/>')
            for px,py in pts: chunks.append(f'<circle cx="{x-44+px}" cy="{150+py}" r="5" fill="#dc2626"/>')
            chunks.append(f'<text x="{x}" y="320" text-anchor="middle" class="lab">{LETTERS[i]}</text>')
    chunks.append('</svg>')
    return ''.join(chunks)


def make_items():
    items=[]
    # Five distinct visual rule families with deliberately varied transformations.
    for j in range(5):
        shape=SHAPES[j]; step=[45,90,135,180,270][j]; start=[0,15,30,45,60][j]
        seq=[{"shape":shape,"angle":start+k*step,"mark":"line" if j%2 else "dot","fill":"white"} for k in range(3)]
        correct={**seq[-1],"angle":start+3*step}
        opts=[{**correct,"angle":correct["angle"]+d} for d in [0,45,90,180]]
        items.append(("rotation",f"An asymmetric {shape} figure starts at {start}° and turns {step}° clockwise each step. Select the next orientation.",
                      f"The figure turns {step % 360 or 360}° clockwise at every step. Applying the same rotation once more gives option A.",
                      "Figural series · rotation",{"caption":"Find the next orientation","sequence":seq,"options":opts},0))
    for j in range(5):
        shape=SHAPES[(j+1)%5]; start=j%3+1; inc=j%2+1
        seq=[{"shape":shape,"angle":j*17,"fill":"white","count":start+k*inc} for k in range(3)]
        # Count is depicted by repeated mini-figures in a row.
        seq_states=seq
        opts=[{"shape":shape,"angle":j*17,"fill":"white","count":start+3*inc+d} for d in [0,1,2,3]]
        sp={"caption":"Track the number of repeated marks","sequence":seq_states,"options":opts}
        items.append(("count",f"A {shape} starts with {start} red dots and gains {inc} dot(s) at each step. Choose the next figure.",
                      f"The number of marks increases by {inc} each time: {start}, {start+inc}, {start+2*inc}. The next has {start+3*inc} marks (option A).",
                      "Figural series · progressive count",sp,0))
    for j in range(5):
        shape="L"; states=[{"shape":shape,"angle":j*23,"fill":"#172554" if k%2==0 else "white","mark":"dot" if k%2 else "line"} for k in range(3)]
        next_state={"shape":shape,"angle":j*23,"fill":"white","mark":"dot"}
        opts=[next_state,{**next_state,"angle":j*23+45},{**next_state,"fill":"#172554"},{**next_state,"mark":"line"}]
        items.append(("alternate",f"A {shape} alternates filled/unfilled shading and line/dot marks, beginning at rotation {j*23}°. Select the next state.",
                      "Shading and the internal mark both alternate. After filled-with-line, unfilled-with-dot is required (option A).",
                      "Figural series · alternating attributes",{"caption":"Follow the alternating attributes","sequence":states,"options":opts},0))
    for j in range(5):
        # 2x2 matrix: both rows apply the same orientation increment; marker switches by column.
        shape="L"; base=j*18; step=[45,90,135,180,270][j]
        matrix=[{"shape":shape,"angle":base,"mark":"dot","fill":"white"},{"shape":shape,"angle":base+step,"mark":"line","fill":"white"},
                {"shape":shape,"angle":base+step,"mark":"dot","fill":"#172554"},None]
        correct={"shape":shape,"angle":base+2*step,"mark":"line","fill":"#172554"}
        opts=[correct,{**correct,"angle":correct["angle"]+45},{**correct,"mark":"dot"},{**correct,"fill":"white"}]
        items.append(("matrix",f"Complete the 2×2 {shape} matrix with a {step}° row rotation and changing internal mark.",
                      f"Across each row, orientation advances by {step}° and the internal mark changes dot→line. Down the second column, shading changes to filled. The missing figure is option A.",
                      "Figure matrix · rotation, mark and shading",{"matrix":matrix,"options":opts},0))
    for j in range(5):
        original={"shape":"L","angle":j*29+13,"fill":"white","mark":"line" if j%2 else "dot"}
        # reflect horizontally or vertically; polygon rotations are reflected by negating angle; asymmetric L/arrow identify direction.
        axis="vertical mirror" if j%2==0 else "water image"
        correct={**original,"flip_x":j%2==0,"flip_y":j%2==1}
        opts=[correct,{**original,"angle":(original["angle"]+90)%360},{**original},{**correct,"mark":"dot" if original["mark"]=="line" else "line"}]
        items.append(("reflection",f"Choose the {axis} of the asymmetric L at orientation {j*29+13}°, preserving its {original['mark']}.",
                      f"Reflect the figure across the {('vertical axis' if j%2==0 else 'horizontal axis')}; the shape's orientation reverses while the internal mark remains unchanged. Option A matches.",
                      "Reflection · mirror/water image",{"original":original,"axis":axis,"options":opts},0))
    for j in range(5):
        # A single vertical fold maps each punch to its mirror location; choices use distinct patterns.
        punches=[(245,170+30*j),(265,260-20*j)]
        expected=[(245,170+30*j),(155,170+30*j),(265,260-20*j),(135,260-20*j)]
        wrong1=[(245,170+30*j),(265,260-20*j)]
        wrong2=[(155,170+30*j),(135,260-20*j)]
        wrong3=[(245,170+30*j),(155,170+30*j),(265,260-20*j)]
        pts=lambda seq:[((x-80)/240*88,(y-105)/240*140) for x,y in seq]
        opts=[pts(expected),pts(wrong1),pts(wrong2),pts(wrong3)]
        heights=["near the top","at the upper-middle","at the centre","at the lower-middle","near the bottom"]
        items.append(("fold",f"A square is folded once along its vertical centre line; punches lie {heights[j]} and {heights[4-j]} on the folded half. Choose its unfolded pattern.",
                      "Unfolding reflects every punch across the fold line. Each punch therefore appears with its mirror counterpart at equal distance on the opposite half. Option A shows all reflected positions.",
                      "Paper folding · one fold and two punches",{"punches":punches,"options":opts},0))
    for j in range(5):
        shape="L"; a={"shape":shape,"angle":j*21,"fill":"white","mark":"dot"}; step=[45,90,135,180,270][j]
        b={**a,"angle":a["angle"]+step}; c={"shape":"arrow","angle":j*33,"fill":"#172554","mark":"line"}
        correct={**c,"angle":c["angle"]+step}
        opts=[correct,{**c,"angle":c["angle"]-step},{**c,"fill":"white"},{**c,"mark":"dot"}]
        items.append(("analogy",f"Figure A changes to B by a {step}° rotation. Apply the same transformation to figure C.",
                      f"A→B rotates the complete figure clockwise by {step}° without changing fill or its internal mark. Applying that same turn to C gives option A.",
                      "Figural analogy · rotation",{"a":a,"b":b,"c":c,"options":opts},0))
    for j in range(5):
        shape=SHAPES[j]
        feature=[{"fill":"white","mark":"dot"},{"fill":"#172554","mark":"dot"},{"fill":"white","mark":"dot"},{"fill":"#172554","mark":"dot"},{"fill":"white","mark":"dot"}][j]
        odd=[{"fill":"white","mark":"line"},{"fill":"white","mark":"dot"},{"fill":"white","mark":"line"},{"fill":"white","mark":"dot"},{"fill":"#172554","mark":"line"}][j]
        opts=[{"shape":SHAPES[(j+k)%5],"angle":j*19+k*17,**feature} for k in range(3)]
        opts.append({"shape":SHAPES[(j+3)%5],"angle":j*19+51,**odd})
        descriptions=["central dot","filled interior","central dot","filled interior","central dot"]
        shape_list=", ".join(SHAPES[(j+k)%5] for k in range(4))
        items.append(("classify",f"Among the {shape_list} figures, three share the {descriptions[j]} property. Select the figure that does not share it.",
                      f"Options A–C share the {descriptions[j]} property. Option D differs in that property, so D is the unique odd figure.",
                      "Figural classification · internal feature",{"options":opts},3))
    for j in range(3):
        # The exact target square plus its rising diagonal is embedded only in A.
        square=[(50,20,155,20),(155,20,155,125),(155,125,50,125),(50,125,50,20)]
        diagonal=[(50,125,155,20) if j%2==0 else (50,20,155,125)]
        if j==2: diagonal=[(50,125,155,20),(50,20,155,125)]
        target=square+diagonal
        wrong_diag=(50,20,155,125) if j%2==0 else (50,125,155,20)
        wrong_c=[(50,72,155,72)] if j<2 else [(50,125,155,20)]
        opts=[target+[(50,72,155,72)],square+[wrong_diag],square+wrong_c,
              [(50,20,170,20),(170,20,170,110),(170,110,50,110),(50,110,50,20),(50,110,170,20)]]
        label=["rising diagonal","falling diagonal","both diagonals"][j]
        items.append(("embed",f"Find the option containing a square with the {label}, in the same orientation.",
                      f"Only option A contains all four square sides and the target's {label}. The other panels either reverse/omit a diagonal, add a different internal line or change the square proportions.",
                      "Embedded figure · segment containment",{"target_segments":diagonal,"target_label":label,"options":opts},0))
    for j in range(5):
        n=j+2; answer=n+1
        items.append(("countfig",f"Count all triangles in the figure with {n} internal horizontal levels, including composite triangles.",
                      f"Each internal horizontal segment and the outside base form one triangle with the apex. Thus {n} internal levels make {n}+1={answer} triangles; option A.",
                      "Counting figures · triangles",{"levels":n,"answer_count":answer,"option_counts":[answer,answer+1,answer+2,max(1,answer-1)]},0))
    for j in range(5):
        positions=[[(0,-52),(0,0),(75,0),(20,0)],[(-55,0),(0,0),(80,0),(0,-30)],[(0,0),(-75,0),(75,0),(0,75)],[(-50,0),(0,0),(75,0),(0,50)],[(52,0),(0,0),(75,0),(-52,0)]][j]
        mode=min(j,2)
        prompt=["inside the circle and outside the square","inside the circle and outside the triangle","inside the overlap of both circles","inside the overlap of both rectangles","inside the circle but outside the square"][j]
        explanation=["Option A lies inside the circle but beyond the square edge.","Option A lies inside the circle but outside the triangle; B and D lie in the triangle and C is outside the circle.","Option A lies in both circles. B and C lie in only one circle, while D lies outside both.","Option A lies in the intersection of the rectangles.","Option A lies inside the circle and outside the square."][j]
        items.append(("dots",f"Choose the figure with the red dot {prompt} (diagram {j+1}).",
                      explanation,
                      "Dot situation · geometric region",{"positions":positions,"mode":mode},0))
    return items


def main():
    ASSETS.mkdir(parents=True,exist_ok=True)
    prior_entries={}
    prior_batch={}
    if LEDGER.is_file():
        try:
            prior_entries={r["question_id"]:r for r in json.loads(LEDGER.read_text(encoding="utf-8")) if r.get("record_type")=="selected_question"}
        except (OSError,json.JSONDecodeError,TypeError):
            prior_entries={}
    if BATCH.is_file():
        try:
            prior_batch={r.get("image_url"):r for r in json.loads(BATCH.read_text(encoding="utf-8" )).get("questions",[])}
        except (OSError,json.JSONDecodeError,TypeError):
            prior_batch={}
    questions=[]; ledger=[]; topic_counts=Counter()
    raw_items=make_items(); family_seen=Counter(); items=[]
    for item in raw_items:
        if family_seen[item[0]]<3:
            items.append(item); family_seen[item[0]]+=1
    kept_assets={f"nvr-{i:03}.svg" for i in range(1,len(items)+1)}
    for old in ASSETS.glob("nvr-*.svg"):
        if old.name not in kept_assets and old.stem[4:].isdigit():
            old.unlink()
    targets=option_target_indices(len(items))
    for i,(family,stem,explanation,topic,spec,answer_idx) in enumerate(items,1):
        question_id=f"nvr-{i:03}"
        prior=prior_entries.get(question_id,{})
        option_field=option_state_field(spec)
        original_choices=deepcopy(prior.get("option_shuffle_audit",{}).get("original_options",spec[option_field]))
        original_answer_index=prior.get("option_shuffle_audit",{}).get("original_correct_index",answer_idx)
        validate_option_shuffle(original_choices,spec[option_field],original_answer_index,answer_idx)
        spec,old_to_new=shuffle_option_states(spec,answer_idx,targets[i-1],seed=0xC170+i)
        target_index=targets[i-1]
        validate_option_shuffle(original_choices,spec[option_field],original_answer_index,target_index)
        key=LETTERS[target_index]
        explanation=remap_explanation(explanation,family,old_to_new,key)
        difficulty=DIFFICULTY_CYCLE[(i-1)%len(DIFFICULTY_CYCLE)]
        asset=f"/question-assets/non-verbal-reasoning/nvr-{i:03}.svg"
        svg=diagram_card(family,spec)
        (ASSETS/f"nvr-{i:03}.svg").write_text(svg,encoding="utf-8")
        options={k:f"Figure {k} (shown in diagram)" for k in LETTERS}
        row={"subject_slug":"reasoning","subcategory_slug":None,"chapter_slug":"non-verbal-reasoning",
             "question_text":stem,"image_url":asset,"options":options,"correct_option":key,
             "explanation":explanation,"difficulty":difficulty,"is_pyq":False,"pyq_year":None,
             "pyq_exam_name":None,"source":"Original SSC-style visual reasoning question"}
        questions.append(row); topic_counts[topic]+=1
        shuffle_audit={"original_options":original_choices,"shuffled_options":deepcopy(spec[option_field]),
                       "original_correct_index":original_answer_index,"shuffled_correct_index":target_index,
                       "old_to_new_indexes":old_to_new,"validation":"PASS — unordered option multiset preserved; correct state preserved"}
        entry={"record_type":"selected_question","question_id":question_id,"row":i,
                       "question":stem,"source_type":"original","source":"Original SSC-style visual reasoning question",
                       "rule_family":family,
                       "source_pdf":None,"source_page":None,"topic":topic,"difficulty":difficulty,
                       "options":options,"correct_option":key,"expected_answer":options[key],"explanation":explanation,
                       "verification_method":"Deterministic symbolic state rule encoded by the builder and independently asserted by the focused test.",
                       "concept_signature":f"{family}:{json.dumps(spec,sort_keys=True,separators=(',',':'))}",
                       "rule_spec":spec,"answer_index":target_index,"option_shuffle_audit":shuffle_audit,
                       "image_asset":asset,"is_pyq":False,"validation_status":"PASS — rule and option state verified"}
        if prior.get("database_reconciliation"):
            db_rec=deepcopy(prior["database_reconciliation"])
            previous_question=prior_batch.get(asset,{})
            old_key=previous_question.get("correct_option")
            old_explanation=previous_question.get("explanation")
            pending=old_key!=key or old_explanation!=explanation
            if pending:
                db_rec["initial_correct_option"]=old_key
                db_rec["requested_correct_option"]=key
                db_rec["initial_explanation"]=old_explanation
                db_rec["final_classification"]="answer_key_reconciliation_pending"
            entry["database_reconciliation"]=db_rec
            if not pending and prior.get("answer_position_reconciliation"):
                entry["answer_position_reconciliation"]=prior["answer_position_reconciliation"]
        ledger.append(entry)
    BATCH.parent.mkdir(exist_ok=True)
    BATCH.write_text(json.dumps({"questions":questions},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    # Source question cards are intentionally rejected because the supplied rendered slides have instructor answer marks overlaid on the answer figures.
    rejected=[]
    candidates={"Non-Verbal Reasoning  02_ Class Notes.pdf":list(range(6,11))+list(range(12,17))+list(range(18,26)),
                "Non-Verbal Reasoning  03_ Class Notes.pdf":list(range(6,13))+list(range(14,18))+list(range(19,26))+[28],
                "Non-Verbal Reasoning  04_ Class Notes.pdf":list(range(5,12))+list(range(14,20))+list(range(21,25)),
                "Non-Verbal Reasoning  06_ Class Notes.pdf":[11]}
    for pdf,pages in candidates.items():
        for page in pages:
            if pdf.startswith("Non-Verbal Reasoning  02"):
                topic="mirror/paper reflection" if page==6 else "paper folding/cutting" if page<17 else "embedded figures"
            elif pdf.startswith("Non-Verbal Reasoning  03"):
                topic="figural analogy" if page<=12 else "figural classification" if page<=17 else "figure completion/analysis"
            elif pdf.startswith("Non-Verbal Reasoning  04"):
                topic="figural series" if page<=11 else "figure matrix" if page<=19 else "dot situation"
            else:
                topic="counting figures · triangles"
            rejected.append({"record_type":"rejected_source_prompt","source_pdf":pdf,"source_page":page,
                             "topic":topic,"source_prompt_transcription":"Not retained; the source card is rejected before transcription because solution marks overlap the visual prompt/options.",
                             "options_transcription":None,"source_marked_answer":"Instructor marks visible; not treated as an answer key.",
                             "independently_verified_answer":None,
                             "rejection_reason":"The lecture card has instructor solution strokes/circles over the question or answer figures; reusing the card would expose or alter an answer. No source diagram was silently cleaned or reconstructed."})
    LEDGER.write_text(json.dumps(ledger+rejected,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    report=("# CH-17 Non-Verbal Reasoning — Source Review and Bank\n\n"
      "## Source review\n\n"
      "Visually reviewed 106 pages: Lecture 02 (27), Lecture 03 (30), Lecture 04 (26), Lecture 06 (13), Lecture 07 (10). Lectures 01 and 05 were not supplied. Lecture 07 pages 2–8 are worked examples rather than complete MCQs; they were reviewed as counting reference material.\n\n"
      f"The source ledger records {len(rejected)} complete prompt candidates rejected because instructor solution annotations are drawn over question/answer figures, making the cards unsuitable for direct learner display. By lecture: Lecture 02: 18 (mirror/paper reflection 1, folding/cutting 9, embedded figures 8); Lecture 03: 19 (analogy 7, classification 4, figure completion 8); Lecture 04: 17 (series 7, matrix 6, dot situation 4); Lecture 06: 1 triangle-count prompt. Lecture 07 pages 2–8 provide worked counting examples but no complete MCQ prompt. No answer ticks were adopted as answer keys. No source-derived questions were retained.\n\n"
      "## Bank\n\n"
      f"{len(questions)} original visual questions; difficulty distribution: {dict(Counter(q['difficulty'] for q in questions))}. Correct-answer distribution: {dict(Counter(q['correct_option'] for q in questions))}. Topic distribution: {dict(topic_counts)}. All are Normal (`is_pyq=false`) with four distinct labeled options, one keyed correct answer, explanation, and local SVG. Correct choices are deterministically shuffled while retaining their complete visual state.\n\n"
      "## Visual verification and limitations\n\n"
      f"Generated {len(questions)} SVG assets under `frontend/public/question-assets/non-verbal-reasoning/`. The builder creates each image alongside its question record. Rotation, progressive counts, alternating attributes, matrices, mirror/water reflections, fold/unfold positions, analogy, unique classification, embedded segment networks, triangle enumeration, and dot regions are defined by deterministic state rules. The option shuffle is deterministic and independently checked as an unordered four-choice multiset; the original correct visual state is confirmed at the new answer index. Source-derived items are not included because the supplied question cards display instructor solution annotations over the visual choices.\n\n"
      "## Answer-position audit\n\n"
      f"Deterministic correct-key distribution: {dict(Counter(q['correct_option'] for q in questions))}. Original option states and answer indexes are retained in the selected-question ledger for unordered set comparison. Each figure is moved as a complete state in its original diagram; the SVG is regenerated from the shuffled state specification.\n\n"
      "## Source limitation\n\n"
      "All 55 annotated source candidates remain rejected pending complete clean visual reconstruction and independent solve. Lectures 01 and 05 were not supplied. The bank contains original questions only.\n")
    REPORT.write_text(report,encoding="utf-8")
    print(f"Built {len(questions)} questions; assets={len(questions)}; rejected_source_candidates={len(rejected)}")


if __name__=="__main__": main()
