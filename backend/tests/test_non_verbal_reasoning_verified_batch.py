"""Focused validation of the generated CH-17 visual bank and answer rules."""
from __future__ import annotations

import importlib.util
import json
import math
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from types import SimpleNamespace

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("nvr_importer",ROOT/"scripts"/"import_non_verbal_reasoning_verified_batch.py")
nvr=importlib.util.module_from_spec(SPEC); sys.modules[SPEC.name]=nvr; SPEC.loader.exec_module(nvr)
BUILD_SPEC=importlib.util.spec_from_file_location("nvr_builder",ROOT/"scripts"/"build_non_verbal_reasoning_artifacts.py")
builder=importlib.util.module_from_spec(BUILD_SPEC); sys.modules[BUILD_SPEC.name]=builder; BUILD_SPEC.loader.exec_module(builder)
sys.path.insert(0,str(ROOT/"scripts"))
POS_SPEC=importlib.util.spec_from_file_location("nvr_answer_reconcile",ROOT/"scripts"/"reconcile_non_verbal_answer_positions.py")
position_reconcile=importlib.util.module_from_spec(POS_SPEC); sys.modules[POS_SPEC.name]=position_reconcile; POS_SPEC.loader.exec_module(position_reconcile)

def bank():
    return json.loads((ROOT/"data"/"non_verbal_reasoning_verified_batch.json").read_text(encoding="utf-8"))["questions"]

def ledger():
    return json.loads((ROOT/"data"/"non_verbal_reasoning_answer_ledger.json").read_text(encoding="utf-8"))

def selected(): return [r for r in ledger() if r["record_type"]=="selected_question"]

def test_batch_schema_difficulties_options_and_assets():
    rows=bank(); audit=selected()
    assert len(rows)==33 and len(audit)==33
    assert Counter(x["difficulty"] for x in rows)=={"EASY":11,"MEDIUM":11,"HARD":11}
    distribution=Counter(x["correct_option"] for x in rows)
    assert distribution=={"A":9,"B":8,"C":8,"D":8}
    assert builder.option_target_indices(33)==builder.option_target_indices(33)
    targets=builder.option_target_indices(33)
    assert Counter("ABCD"[i] for i in targets)==distribution
    assert all(not(targets[i]==targets[i+1]==targets[i+2]) for i in range(31))
    assert all(targets[i:i+4] not in ([0,1,2,3],[1,2,3,0],[2,3,0,1],[3,0,1,2]) for i in range(30))
    assert all(x["chapter_slug"]=="non-verbal-reasoning" and x["is_pyq"] is False for x in rows)
    assert len({x["question_text"].casefold() for x in rows})==len(rows)
    for row in rows:
        assert set(row["options"])==set("ABCD")
        assert len(set(row["options"].values()))==4
        assert row["correct_option"] in row["options"]
        path=ROOT.parent/"frontend"/"public"/row_path(row["image_url"])
        assert path.is_file()
        assert ET.parse(path).getroot().tag.endswith("svg")
    assert len([x for x in ledger() if x["record_type"]=="rejected_source_prompt"])==55
    families=Counter(x["rule_family"] for x in audit)
    assert len(families)==11 and set(families.values())=={3}
    assert all(Counter(x["difficulty"] for x in audit if x["rule_family"]==family)=={"EASY":1,"MEDIUM":1,"HARD":1} for family in families)
    assert all(x["database_reconciliation"]["chapter_id"]=="746c8d03-3645-4454-a875-7cd9109e133a" for x in audit)
    assert all(x["database_reconciliation"]["import_key"]==x["image_asset"] and x["database_reconciliation"]["final_classification"] in {"exact_match","answer_key_reconciliation_pending"} for x in audit)
    prior=json.loads((ROOT/"data"/"non_verbal_reasoning_reconciliation_report.json").read_text(encoding="utf-8"))["before"]
    prior_by_key={x["import_key"]:x for x in prior["records"]}
    by_id={x["question_id"]:x for x in audit}
    for row in rows:
        audit_row=by_id[row["image_url"].rsplit("/",1)[-1].replace(".svg","")]
        prior_row=prior_by_key[row["image_url"]]
        shuffle=audit_row["option_shuffle_audit"]; spec=audit_row["rule_spec"]; field=builder.option_state_field(spec)
        builder.validate_option_shuffle(shuffle["original_options"],spec[field],shuffle["original_correct_index"],shuffle["shuffled_correct_index"])
        position_reconcile.assert_unordered_options_preserved(shuffle["original_options"],spec[field],shuffle["original_correct_index"],audit_row["answer_index"])
        assert row["correct_option"]=="ABCD"[audit_row["answer_index"]]
        assert row["question_text"]==prior_row["fields"]["question_text"]["live"]
        assert row["difficulty"]==prior_row["fields"]["difficulty"]["canonical"]
        assert row["image_url"]==prior_row["import_key"]
        assert Counter(row["options"].values())==Counter(f"Figure {k} (shown in diagram)" for k in "ABCD")
        assert builder.diagram_card(audit_row["rule_family"],spec)==(ROOT.parent/"frontend"/"public"/row_path(row["image_url"])).read_text(encoding="utf-8")
        assert row["explanation"]==audit_row["explanation"]
        old_explanation=prior_row["fields"]["explanation"]["live"]
        assert builder.remap_explanation(old_explanation,audit_row["rule_family"],shuffle["old_to_new_indexes"],row["correct_option"])==row["explanation"]
    assert len(nvr.load_and_validate())==33

def row_path(url): return url.lstrip("/")

def test_rotation_count_and_alternation_rules_are_exact():
    for audit in selected():
        spec=audit["rule_spec"]; fam=audit["rule_family"]
        if fam=="rotation":
            seq=spec["sequence"]; step=seq[1]["angle"]-seq[0]["angle"]
            assert seq[2]["angle"]-seq[1]["angle"]==step
            assert spec["options"][audit["answer_index"]]["angle"]==seq[2]["angle"]+step
        elif fam=="count":
            vals=[x["count"] for x in spec["sequence"]]
            assert vals[1]-vals[0]==vals[2]-vals[1]
            assert spec["options"][audit["answer_index"]]["count"]==vals[2]+(vals[1]-vals[0])
        elif fam=="alternate":
            states=spec["sequence"]
            assert states[0]["fill"]==states[2]["fill"] and states[0]["mark"]==states[2]["mark"]
            answer=spec["options"][audit["answer_index"]]
            assert answer["fill"]!=states[-1]["fill"]
            assert answer["mark"]!=states[-1]["mark"]

def test_matrix_reflection_fold_analogy_and_classification_rules():
    for audit in selected():
        s=audit["rule_spec"]; fam=audit["rule_family"]
        if fam=="matrix":
            a,b,c,_=s["matrix"]; answer=s["options"][audit["answer_index"]]
            assert b["angle"]-a["angle"]==c["angle"]-a["angle"]
            assert answer["angle"]-c["angle"]==b["angle"]-a["angle"]
            assert answer["mark"]==b["mark"] and answer["fill"]==c["fill"]
        elif fam=="reflection":
            answer=s["options"][audit["answer_index"]]
            assert answer["flip_x"] != answer["flip_y"]
            assert answer["mark"]==s["original"]["mark"]
        elif fam=="fold":
            points=s["options"][audit["answer_index"]]
            assert len(points)==4
            xs=sorted(round(p[0],2) for p in points)
            assert xs[0]<44 and xs[1]<44 and xs[2]>44 and xs[3]>44
        elif fam=="analogy":
            delta=s["b"]["angle"]-s["a"]["angle"]
            answer=s["options"][audit["answer_index"]]
            assert answer["angle"]-s["c"]["angle"]==delta
            assert answer["fill"]==s["c"]["fill"] and answer["mark"]==s["c"]["mark"]
        elif fam=="classify":
            opts=s["options"]
            key=audit["answer_index"]; other=[x for i,x in enumerate(opts) if i!=key]
            assert len({x["mark"] for x in other})==1 and len({x["fill"] for x in other})==1
            assert opts[key]["mark"]!=other[0]["mark"] or opts[key]["fill"]!=other[0]["fill"]

def test_embedded_counting_and_dot_answers():
    for audit in selected():
        s=audit["rule_spec"]; fam=audit["rule_family"]
        if fam=="embed":
            target=s["target_segments"]
            key=audit["answer_index"]
            assert all(seg in s["options"][key] for seg in target)
            assert all(not all(seg in option for seg in target) for i,option in enumerate(s["options"]) if i!=key)
        elif fam=="countfig":
            n=s["levels"]
            assert s["answer_count"]==n+1  # n internal horizontal segments plus the base form apex triangles.
            assert len(set(s["option_counts"]))==4 and s["option_counts"][audit["answer_index"]]==s["answer_count"]
            asset=ROOT.parent/"frontend"/"public"/"question-assets"/"non-verbal-reasoning"/f"nvr-{audit['row']:03}.svg"
            assert asset.read_text(encoding="utf-8").count('stroke="#2563eb"')==n
        elif fam=="dots":
            mode=s["mode"]; x,y=s["positions"][audit["answer_index"]]
            if mode==0: assert x*x+y*y<65**2 and not (-30<x<30 and -30<y<30)
            elif mode==1:
                assert x*x+y*y<65**2 and x < -52*(1-y/35)
            else: assert math.hypot(x+32,y)<55 and math.hypot(x-32,y)<55

def test_importer_reports_difficulty_and_answer_conflicts_without_hiding_them():
    row=bank()[0]
    def live(difficulty="MEDIUM", text=None, correct=None, option_text=None):
        return SimpleNamespace(
            question_text=text or row["question_text"], image_url=row["image_url"],
            difficulty=SimpleNamespace(value=difficulty), explanation=row["explanation"],
            is_active=True, is_pyq=False,
            options=[SimpleNamespace(option_key=k,option_text=option_text if k=="B" and option_text else v,is_correct=k==(correct or row["correct_option"])) for k,v in row["options"].items()],
        )
    category,fields=nvr.existing_record_conflicts(row,live())
    assert category=="same_question_answer_difficulty_mismatch" and fields==["difficulty"]
    category,fields=nvr.existing_record_conflicts(row,live("EASY",text="Changed wording"))
    assert category=="content_or_status_conflict" and "question_text" in fields
    different_key=next(k for k in "ABCD" if k!=row["correct_option"])
    category,fields=nvr.existing_record_conflicts(row,live("EASY",correct=different_key))
    assert category=="content_or_status_conflict" and "correct_option" in fields
    category,fields=nvr.existing_record_conflicts(row,live("EASY",option_text="Detached choice"))
    assert category=="content_or_status_conflict" and "options" in fields
