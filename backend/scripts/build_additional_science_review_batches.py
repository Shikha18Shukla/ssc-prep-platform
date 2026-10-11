"""Record visual reviews for additional Science PDF page candidates.

This script prepares review records and importer CSVs only. It never imports
questions into an application database.
"""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "data/imports/science"
CATALOG_IDS = {
    "chemical-reaction": "b19ea070-a111-409b-9975-f203fea66276",
    "motion-and-force": "029386c9-bbf0-45d3-813e-bf0d52fdf091",
    "skeleton-system": "4e271000-7906-4bc3-965b-4e6d2692d137",
    "optics-and-human-eye": "a7bd204b-eb86-43eb-9c2d-f72e7e1dce30",
    "metals-and-non-metals": "0f365ed8-5137-4d4c-9b21-ce76b6dbc842",
    "periodic-table": "47a79886-a191-4b02-b044-446ca513d507",
    "gravitation-work-energy": "2e7ec7ef-13e8-4adf-a35a-9c6f4f6fe05c",
    "plant-kingdom": "c328f94b-f3f5-419f-a2f1-899e760e7240",
    "magnetic-effect-and-heating": "b21dfc94-3eaf-4e83-9882-192cf418b2c4",
    "matter-and-atom": "1f372c5a-abf6-45b0-9975-10092037915f",
    "cell": "24be0c8f-9b9f-47cc-95db-01b766b8016a",
    "nutrition": "d581e071-f539-4716-97e4-2e73e6b5c625",
    "reproduction": "c8514f3d-1208-4b1e-81a8-0f053f6b3a55",
    "chemistry-in-every-day-life": "da188972-c61c-4249-bdfd-0784761ced7b",
    "electricity": "24ba6660-d222-4a7b-b4e3-dce738a85260",
    "sound": "d12ea943-a2eb-4ba5-b71b-6b8865b7cb9a",
}

IMPORT_COLUMNS = [
    "subject_slug", "subcategory_slug", "chapter_slug", "question_text",
    "option_a", "option_b", "option_c", "option_d", "correct_option",
    "explanation", "difficulty", "is_pyq", "pyq_year", "pyq_exam_name", "source",
]
REVIEW_COLUMNS = [
    "source_pdf", "source_page", "subject_slug", "subcategory_slug", "chapter_slug",
    "catalog_chapter_id", "question_text", "option_a", "option_b", "option_c",
    "option_d", "proposed_correct_option", "explanation", "difficulty", "is_pyq",
    "pyq_year", "pyq_exam_name", "review_status", "import_eligible", "review_note",
]
DECISION_COLUMNS = ["source_pdf", "source_page", "chapter_slug", "review_status", "review_note"]

# This is a page-image transcription/review. No exam name is visible on these
# pages. Explanation notes explicitly distinguish source text from review text.
ROWS = [
    {
        "source_pdf": "chemical reactions.pdf", "source_page": "2", "chapter_slug": "chemical-reaction",
        "question_text": "Select the correct balanced equation option for the reaction Fe + H2O -> Fe3O4 + H2.",
        "options": ["3Fe + 4H2O -> Fe3O4 + 2H2", "2Fe + 4H2O -> Fe3O4 + 4H2", "3Fe + 4H2O -> Fe3O4 + 4H2", "4Fe + 4H2O -> Fe3O4 + 4H2"],
        "answer": "C", "explanation": "The balanced equation is 3Fe + 4H2O -> Fe3O4 + 4H2: both sides contain 3 iron atoms, 4 oxygen atoms, and 8 hydrogen atoms.",
        "difficulty": "MEDIUM", "is_pyq": False, "year": "",
        "note": "The page image confirms the stem, four options/order, marked answer 3, and MEDIUM label. No PYQ label or exam name is visible. The source explanation is clipped; this concise atom-count explanation was written during review and is not attributed to the PDF.",
    },
    {
        "source_pdf": "chemistry in every day life.pdf", "source_page": "2", "chapter_slug": "motion-and-force",
        "question_text": "Velocity is a vector quantity because it depends upon:",
        "options": ["Magnitude only", "Direction only", "Both magnitude and direction", "Neither magnitude nor direction"],
        "answer": "C", "explanation": "Velocity is displacement per unit time. Since displacement has both magnitude and direction, velocity is also a vector and depends on both.",
        "difficulty": "MEDIUM", "is_pyq": False, "year": "",
        "note": "The page image confirms the full stem/options, marked answer 3, MEDIUM label, and a complete explanation. Mapped by question content to Motion & Force; the PDF title is misleading. No PYQ label or exam name is visible.",
    },
    {
        "source_pdf": "Glands.pdf", "source_page": "2", "chapter_slug": "skeleton-system",
        "question_text": "The total number of bones in the body of an adult human is _____.",
        "options": ["205", "206", "216", "636"],
        "answer": "B", "explanation": "The standard adult human skeleton has 206 bones. Small sesamoid bones can vary, but 206 is the accepted count used for this question.",
        "difficulty": "MEDIUM", "is_pyq": True, "year": "2017",
        "note": "The page image confirms stem/options, marked answer 2, MEDIUM and explicit PYQ 2017 labels, plus the explanation. No exam name is shown. Mapped by content to Skeleton System; the PDF title is misleading.",
    },
    {
        "source_pdf": "gravitational work and energy.pdf", "source_page": "2", "chapter_slug": "optics-and-human-eye",
        "question_text": "The incident ray and the reflected ray, together with the normal at the point of incidence, all lie in _____.",
        "options": ["The same plane", "Diagonally opposite planes", "Vertically opposite planes", "Different planes"],
        "answer": "A", "explanation": "The law of reflection states that the incident ray, the reflected ray, and the normal at the point of incidence lie in the same plane.",
        "difficulty": "MEDIUM", "is_pyq": True, "year": "2021",
        "note": "The page image confirms the reflection-law stem, four options/order, marked answer 1, MEDIUM and explicit PYQ 2021 labels. The page explanation supports the same-plane answer. No exam name is visible. Mapped by content to Optics & Human Eye; the PDF title is misleading.",
    },
    {
        "source_pdf": "matter and atoms.pdf", "source_page": "2", "chapter_slug": "metals-and-non-metals",
        "question_text": "Which is the only non-metallic element that is in liquid state at room temperature?",
        "options": ["Francium", "Helium", "Bromine", "Mercury"],
        "answer": "C", "explanation": "Bromine is a non-metal and is liquid at ordinary room temperature. Mercury is also liquid, but it is a metal.",
        "difficulty": "MEDIUM", "is_pyq": False, "year": "",
        "note": "The page image confirms the full stem/options, marked answer 3, MEDIUM label, and explanation including Bromine's melting/boiling points. No PYQ label or exam name is visible. Mapped by content to Metals & Non Metals; the PDF title is misleading.",
    },
    {
        "source_pdf": "metal and non metals.pdf", "source_page": "2", "chapter_slug": "periodic-table",
        "question_text": "Who introduced the term 'triads' in the classification of elements?",
        "options": ["Dmitri Mendeleev", "Johann Dobereiner", "A. E. B. de Chancourtois", "John Newlands"],
        "answer": "B", "explanation": "Johann Dobereiner introduced triads: groups of three elements with similar properties in which the middle atomic mass was approximately the mean of the other two.",
        "difficulty": "MEDIUM", "is_pyq": False, "year": "",
        "note": "The page image confirms the stem/options, marked answer 2, MEDIUM label, and a complete explanation. No PYQ label or exam name is visible. Mapped by content to Periodic Table; the PDF title is misleading.",
    },
    {
        "source_pdf": "motion and force.pdf", "source_page": "2", "chapter_slug": "gravitation-work-energy",
        "question_text": "The gravitational force between two objects of masses m1 and m2 is directly proportional to _____.",
        "options": ["m2 - m1", "m1 - m2", "m1 / m2", "m1 x m2"],
        "answer": "D", "explanation": "Newton's law of universal gravitation gives F = G(m1 x m2)/r^2, so force is directly proportional to the product of the two masses when distance is fixed.",
        "difficulty": "MEDIUM", "is_pyq": False, "year": "",
        "note": "The page image confirms the formula stem, four options/order, marked answer 4, MEDIUM label, and the product-of-masses explanation. No PYQ label or exam name is visible. Mapped by content to Gravitation Work Energy; the PDF title is misleading.",
    },
    {
        "source_pdf": "periodic table.pdf", "source_page": "2", "chapter_slug": "chemical-reaction",
        "question_text": "What type of reaction takes place when calcium oxide reacts vigorously with water to produce slaked lime?",
        "options": ["Decomposition reaction", "Double displacement reaction", "Combination reaction", "Displacement reaction"],
        "answer": "C", "explanation": "Calcium oxide and water combine to form the single product calcium hydroxide: CaO + H2O -> Ca(OH)2. This is a combination reaction.",
        "difficulty": "MEDIUM", "is_pyq": False, "year": "",
        "note": "The page image confirms the stem/options, marked answer 3, MEDIUM label, and the combination-reaction explanation. No PYQ label or exam name is visible. Mapped by content to Chemical Reaction; the PDF title is misleading.",
    },
    {
        "source_pdf": "reproduction.pdf", "source_page": "2", "chapter_slug": "plant-kingdom",
        "question_text": "The plants which can live in soil but are dependent on water for sexual reproduction are known as?",
        "options": ["Thallophyta", "Pteridophytes", "Bryophytes", "Algae"],
        "answer": "C", "explanation": "Bryophytes can live on land, but their motile male gametes need water to reach the egg for fertilisation.",
        "difficulty": "EASY", "is_pyq": False, "year": "",
        "note": "The page image confirms the question/options, marked answer 3, EASY label, and complete explanation. No PYQ label or exam name is visible. Mapped to Plant Kingdom by the plant group being tested, not from the PDF title.",
    },
    {
        "source_pdf": "sound.pdf", "source_page": "2", "chapter_slug": "magnetic-effect-and-heating",
        "question_text": "How does the magnetic field strength around a current-carrying conductor change as distance from the conductor increases?",
        "options": ["It decreases", "It is unaffected", "It increases", "It remains constant"],
        "answer": "A", "explanation": "For a long straight current-carrying conductor, magnetic field strength decreases with distance from the conductor (B is proportional to 1/r).",
        "difficulty": "HARD", "is_pyq": True, "year": "2022",
        "note": "The page image confirms the distance-dependent magnetic-field stem, four options/order, marked answer 1, HARD and explicit PYQ 2022 labels. No exam name is shown. Mapped by content to Magnetic Effect & Heating; the PDF title is misleading.",
    },
    {
        "source_pdf": "Tissues.pdf", "source_page": "2", "chapter_slug": "matter-and-atom",
        "question_text": "What is the primary characteristic that distinguishes a gas from other states of matter?",
        "options": ["Ability to maintain a fixed shape", "Fixed volume", "Compressibility", "Rigidity"],
        "answer": "C", "explanation": "Gas particles are far apart, so gases can be compressed. Gases also lack a fixed shape and fixed volume.",
        "difficulty": "MEDIUM", "is_pyq": False, "year": "",
        "note": "The page image confirms the full stem/options, marked answer 3, MEDIUM label, and complete explanation. No PYQ label or exam name is visible. Mapped by content to Matter & Atom; the PDF title is misleading.",
    },
    {
        "source_pdf": "cell -science.pdf", "source_page": "25", "chapter_slug": "cell",
        "question_text": "What is the outermost layer found in the cell envelope of a bacterial cell called?",
        "options": ["Glycocalyx", "Cell membrane", "Plasma membrane", "Cytoplasm"],
        "answer": "A", "explanation": "The glycocalyx is the outer surface covering found outside the cell wall in many bacteria; it commonly consists of a capsule or slime layer.",
        "difficulty": "EASY", "is_pyq": True, "year": "2022",
        "note": "The page image confirms all options, the green correct marker on option 1, EASY and explicit PYQ 2022 labels, and an explanation naming Glycocalyx. No exam name is visible. The question maps to Cell by content.",
    },
    {
        "source_pdf": "excretory system - science.pdf", "source_page": "4", "chapter_slug": "nutrition",
        "question_text": "Kwashiorkor is caused by which deficiency?",
        "options": ["Iron", "Protein", "Calcium", "Vitamin A"],
        "answer": "B", "explanation": "Kwashiorkor is severe protein-energy malnutrition caused primarily by inadequate protein intake; the source explanation identifies protein deficiency.",
        "difficulty": "EASY", "is_pyq": True, "year": "2022",
        "note": "The page image confirms the full stem/options, green correct marker on option 2, EASY and explicit PYQ 2022 labels, and the source explanation. No exam name is visible. Mapped to Nutrition by content; the PDF title is misleading.",
    },
    {
        "source_pdf": "Glands.pdf", "source_page": "14", "chapter_slug": "reproduction",
        "question_text": "What is the type of asexual reproduction in Amoeba?",
        "options": ["Spore formation", "Binary fission", "Vegetative propagation", "Budding"],
        "answer": "B", "explanation": "Amoeba reproduces asexually by binary fission: its parent cell divides into two daughter cells.",
        "difficulty": "MEDIUM", "is_pyq": True, "year": "2018",
        "note": "The page image confirms all options, green correct marker on option 2, MEDIUM and explicit PYQ 2018 labels, and a source explanation supporting binary fission. No exam name is visible. Mapped to Reproduction by content; the PDF title is misleading.",
    },
    {
        "source_pdf": "chemical reactions.pdf", "source_page": "6", "chapter_slug": "chemistry-in-every-day-life",
        "question_text": "Which substance is commonly used in the saponification process to produce soap?",
        "options": ["Sodium bicarbonate", "Sodium chloride", "Sodium hydroxide", "Sodium carbonate"],
        "answer": "C", "explanation": "Saponification reacts fats or oils with a strong alkali. Sodium hydroxide is commonly used to make solid soap.",
        "difficulty": "MEDIUM", "is_pyq": False, "year": "",
        "note": "Source page image confirms the full stem/options, green correct marker on option 3 (sodium hydroxide), MEDIUM label, and the explanation that sodium hydroxide is used to make solid soap through saponification. Compared with PDF page 9: although the wording and option sets differ, both ask the same sodium-hydroxide/soap-manufacture fact, and both explanations state that NaOH is used in soap production through saponification. Page 6 is a semantic duplicate; retain page 9, the explicit PYQ 2022 record. Audit correction 2026-10-10: supersedes the earlier central-ledger VERIFIED decision; see SCIENCE_DUPLICATE_REVIEW.md for the full comparison and preserved prior note.",
        "status": "DUPLICATE", "import_eligible": False,
    },
    {
        "source_pdf": "chemical reactions.pdf", "source_page": "9", "chapter_slug": "chemistry-in-every-day-life",
        "question_text": "Sodium hydroxide is used in which application?",
        "options": ["As an antacid", "In alkaline batteries", "In manufacturing of soap", "As a cleansing agent"],
        "answer": "C", "explanation": "Sodium hydroxide is used to manufacture soap through saponification. It is too caustic for use as an antacid.",
        "difficulty": "EASY", "is_pyq": True, "year": "2022",
        "note": "The page image confirms the stem/options, green correct marker on option 3, EASY and explicit PYQ 2022 labels, and the source explanation. No exam name is visible. Mapped to Chemistry in Every Day Life by application; the PDF title is not used as chapter evidence.",
    },
    {
        "source_pdf": "sound.pdf", "source_page": "7", "chapter_slug": "electricity",
        "question_text": "A modern electrical generator works on which principle?",
        "options": ["Magnetic induction", "Electromagnetic induction", "Electrical induction", "Electrical energy"],
        "answer": "B", "explanation": "A modern generator operates by electromagnetic induction: changing magnetic flux induces an electromotive force.",
        "difficulty": "MEDIUM", "is_pyq": True, "year": "2021",
        "note": "The page image confirms all options, green correct marker on option 2, MEDIUM and explicit PYQ 2021 labels, and an explanation naming electromagnetic induction. No exam name is visible. Mapped to Electricity by content; the PDF title is misleading.",
    },
    {
        "source_pdf": "sound.pdf", "source_page": "12", "chapter_slug": "electricity",
        "question_text": "What is the SI unit of electric charge?",
        "options": ["Coulomb", "Watt", "Newton", "Joule"],
        "answer": "A", "explanation": "Electric charge is measured in coulombs (C) in the SI system.",
        "difficulty": "EASY", "is_pyq": True, "year": "2022",
        "note": "The page image confirms all options, green correct marker on option 1, EASY and explicit PYQ 2022 labels. The visible source solution identifies Coulomb; this concise explanation was written during review. No exam name is visible. Mapped to Electricity by content; the PDF title is misleading.",
    },
    {
        "source_pdf": "sound.pdf", "source_page": "18", "chapter_slug": "electricity",
        "question_text": "A 18 V battery drives a current of 3 A through a bulb. What is the bulb's resistance?",
        "options": ["6 Ω", "2 Ω", "4 Ω", "3 Ω"],
        "answer": "A", "explanation": "By Ohm's law, R = V/I = 18/3 = 6 Ω.",
        "difficulty": "EASY", "is_pyq": True, "year": "2023",
        "note": "The page image confirms all options, green correct marker on option 1, EASY and explicit PYQ 2023 labels, and the source solution using Ohm's law. No exam name is visible. Mapped to Electricity by content; the PDF title is misleading.",
    },
    {
        "source_pdf": "optics and human eye.pdf", "source_page": "2", "chapter_slug": "sound",
        "question_text": "What property of sound waves makes them require a material medium for propagation?",
        "options": ["Echo nature", "Longitudinal nature", "Electromagnetic nature", "Mechanical nature"],
        "answer": "B", "explanation": "Sound is a mechanical wave and needs a material medium. Longitudinal describes the vibration direction, not the reason a medium is required.",
        "difficulty": "MEDIUM", "is_pyq": False, "year": "",
        "note": "The page image marks option 2 (Longitudinal nature), but the question asks why sound requires a medium; that property is mechanical nature, option 4. The source answer/explanation is internally inconsistent. Mapped to Sound by content, but retained as NEEDS_REVIEW and excluded from import until corrected against the source owner.",
        "status": "NEEDS_REVIEW", "import_eligible": False,
    },
]


def _write_csv(path: Path, columns: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def _review_row(item: dict) -> dict:
    return {
        "source_pdf": item["source_pdf"],
        "source_page": item["source_page"],
        "subject_slug": "gk-gs",
        "subcategory_slug": "science",
        "chapter_slug": item["chapter_slug"],
        "catalog_chapter_id": CATALOG_IDS[item["chapter_slug"]],
        "question_text": item["question_text"],
        **{f"option_{key.lower()}": text for key, text in zip("ABCD", item["options"], strict=True)},
        "proposed_correct_option": item["answer"],
        "explanation": item["explanation"],
        "difficulty": item["difficulty"],
        "is_pyq": str(item["is_pyq"]).lower(),
        "pyq_year": item["year"],
        "pyq_exam_name": "",
        "review_status": item.get("status", "VERIFIED"),
        "import_eligible": str(item.get("import_eligible", True)).lower(),
        "review_note": item["note"],
    }


def main() -> int:
    queue_path = ROOT / "SCIENCE_OCR_REVIEW_QUEUE.csv"
    decisions_path = ROOT / "SCIENCE_REVIEW_DECISIONS.csv"
    with queue_path.open(encoding="utf-8-sig", newline="") as stream:
        queue = list(csv.DictReader(stream))
        queue_columns = list(queue[0])

    by_source = {(row["source_pdf"], row["source_page"]): row for row in queue}
    decisions: list[dict] = []
    by_chapter: dict[str, list[dict]] = {}
    review_rows = []
    for item in ROWS:
        key = (item["source_pdf"], item["source_page"])
        if key not in by_source:
            raise ValueError(f"Source page is absent from OCR queue: {key}")
        status = item.get("status", "VERIFIED")
        source_row = by_source[key]
        source_row["chapter_slug"] = item["chapter_slug"]
        source_row["review_status"] = status
        source_row["review_note"] = item["note"]
        decisions.append({
            "source_pdf": item["source_pdf"],
            "source_page": item["source_page"],
            "chapter_slug": item["chapter_slug"],
            "review_status": status,
            "review_note": item["note"],
        })
        review_rows.append(_review_row(item))
        if status == "VERIFIED" and item.get("import_eligible", True):
            by_chapter.setdefault(item["chapter_slug"], []).append(item)

    _write_csv(queue_path, queue_columns, queue)
    with decisions_path.open(encoding="utf-8-sig", newline="") as stream:
        old_decisions = list(csv.DictReader(stream))
    old_keys = {(r["source_pdf"], r["source_page"]) for r in old_decisions}
    new_decisions = [r for r in decisions if (r["source_pdf"], r["source_page"]) not in old_keys]
    _write_csv(decisions_path, DECISION_COLUMNS, old_decisions + new_decisions)

    _write_csv(ROOT / "review-datasets/source-page-supplement/source-page-supplement_review.csv", REVIEW_COLUMNS, review_rows)
    batch_history = []
    batch_root = ROOT / "by-chapter/source-page-supplement"
    expected_batch_paths: set[Path] = set()
    for chapter, items in sorted(by_chapter.items()):
        ordinary = []
        pyq = []
        for item in items:
            row = {
                "subject_slug": "gk-gs", "subcategory_slug": "science", "chapter_slug": chapter,
                "question_text": item["question_text"],
                **{f"option_{key.lower()}": text for key, text in zip("ABCD", item["options"], strict=True)},
                "correct_option": item["answer"], "explanation": item["explanation"],
                "difficulty": item["difficulty"], "is_pyq": str(item["is_pyq"]).lower(),
                "pyq_year": item["year"], "pyq_exam_name": "",
                "source": f"{item['source_pdf']}, PDF page {item['source_page']}",
            }
            (pyq if item["is_pyq"] else ordinary).append(row)
        for suffix, rows in (("ordinary", ordinary), ("pyq", pyq)):
            batch_path = batch_root / chapter / f"{chapter}_{suffix}.csv"
            if rows:
                _write_csv(batch_path, IMPORT_COLUMNS, rows)
                expected_batch_paths.add(batch_path)
        batch_history.append({
            "chapter_slug": chapter,
            "ordinary_rows": len(ordinary),
            "pyq_rows": len(pyq),
            "status": "prepared_not_imported",
        })
    for stale_path in batch_root.rglob("*.csv"):
        if stale_path not in expected_batch_paths:
            stale_path.unlink()
    for empty_dir in sorted(
        (path for path in batch_root.rglob("*") if path.is_dir()),
        key=lambda path: len(path.parts),
        reverse=True,
    ):
        if not any(empty_dir.iterdir()):
            empty_dir.rmdir()

    (ROOT / "review-datasets/source-page-supplement/source-page-supplement_review_report.md").write_text(
        "# Additional Science PDF Page Review\n\n"
        "Page images were rendered from the original PDFs and checked for each listed stem, option order, marked answer, difficulty, PYQ label/year, and explanation. Chapter mapping follows question content, not source filename.\n\n"
        f"- Visually reviewed: {len(ROWS)} records.\n"
        f"- Verified and prepared for dry-run: {sum(len(v) for v in by_chapter.values())} records across {len(by_chapter)} chapters.\n"
        f"- Confirmed semantic duplicate: {sum(item.get('status') == 'DUPLICATE' for item in ROWS)} record; excluded from importer batches.\n"
        f"- Pending review: {sum(item.get('status') == 'NEEDS_REVIEW' for item in ROWS)} Sound record; the source answer marker conflicts with the correct scientific explanation and it remains excluded.\n"
        "- Candidate similarity comparison and manual disposition are documented in SCIENCE_DUPLICATE_REVIEW.md.\n"
        "- No exam name was inferred. The source's explicit PYQ labels and years are retained only where visible.\n"
        "- New rows are prepared only; this script does not import them. User approval is required before any new batch is imported.\n\n"
        "## Prepared batches\n\n| Chapter | Ordinary | PYQ | Status |\n|---|---:|---:|---|\n"
        + "\n".join(f"| {r['chapter_slug']} | {r['ordinary_rows']} | {r['pyq_rows']} | {r['status']} |" for r in batch_history)
        + "\n",
        encoding="utf-8",
    )
    print(f"Prepared {sum(len(v) for v in by_chapter.values())} rows across {len(by_chapter)} chapter batches; imported 0.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
