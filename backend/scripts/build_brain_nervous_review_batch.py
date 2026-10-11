"""Build the reviewed Brain & Nervous System Science import-preparation batch.

Source text and answer decisions below were transcribed from the rendered source
pages. The previous Respiratory batch is read only as a source-record index; its
Respiratory-specific decisions are not modified by this script.
"""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "data/imports/science"
CHAPTER = "brain-and-nervous-system"
CHAPTER_ID = "2237850c-bf16-4627-970a-33f548ae8398"
REVIEW_FIELDS = [
    "source_pdf", "source_page", "subject_slug", "subcategory_slug",
    "chapter_slug", "catalog_chapter_id", "question_text", "option_a",
    "option_b", "option_c", "option_d", "proposed_correct_option",
    "explanation", "difficulty", "is_pyq", "pyq_year", "pyq_exam_name",
    "review_status", "import_eligible", "review_note",
]
IMPORT_FIELDS = [
    "subject_slug", "subcategory_slug", "chapter_slug", "question_text",
    "option_a", "option_b", "option_c", "option_d", "correct_option",
    "explanation", "difficulty", "is_pyq", "pyq_year", "pyq_exam_name",
    "source",
]


def item(page: int, question: str, options: tuple[str, str, str, str], answer: str,
         explanation: str, difficulty: str, *, pyq_year: str = "",
         status: str = "VERIFIED", source_pdf: str = "respiratory system - science.pdf",
         note: str = "") -> dict[str, str]:
    pyq = bool(pyq_year)
    if not note:
        note = (
            "Source page image visually checked: complete stem, four options/order, "
            "green correct-answer marking, complete explanation, and visible "
            f"{difficulty} label were verified. "
            + (f"PYQ {pyq_year} is explicitly shown; " if pyq else "No PYQ label is shown; ")
            + "no exam name is visible."
        )
    return {
        "source_pdf": source_pdf,
        "source_page": str(page),
        "subject_slug": "gk-gs",
        "subcategory_slug": "science",
        "chapter_slug": CHAPTER,
        "catalog_chapter_id": CHAPTER_ID,
        "question_text": question,
        "option_a": options[0], "option_b": options[1],
        "option_c": options[2], "option_d": options[3],
        "proposed_correct_option": answer,
        "explanation": explanation,
        "difficulty": difficulty,
        "is_pyq": str(pyq).lower(),
        "pyq_year": pyq_year,
        "pyq_exam_name": "",
        "review_status": status,
        "import_eligible": str(status == "VERIFIED").lower(),
        "review_note": note,
    }


ROWS = [
    item(2, "Dendron and axon are parts of the:", ("Excretory system", "Digestive system", "Muscular system", "Nervous system"), "D", "", "EASY", pyq_year="2021", status="NEEDS_REVIEW", note="Source image confirms all four options, answer D, EASY and PYQ 2021. The explanation continues below the captured page and is clipped; excluded from import."),
    item(4, "Which one of the following makes up the Central Nervous System together with the brain?", ("Neuron", "Brain", "Spinal Cord", "More than one of the above"), "D", "The central nervous system includes the brain and the spinal cord and is the site of information processing and control. The brain is protected within the skull. Some of its main functions include processing sensory information, regulating blood pressure and breathing, and releasing hormones. Hence, the correct answer is ‘More than one of the above.’", "EASY"),
    item(5, "In synapse the information is transmitted in the ______ form.", ("Biological", "Chemical", "Electrical", "No option is correct."), "B", "", "MEDIUM", status="NEEDS_REVIEW", note="Source image confirms all four options and answer B. MEDIUM is visible. The explanation is clipped at the bottom of the captured page; no PYQ label is shown. Excluded from import."),
    item(6, "In which part of a neuron is information acquired?", ("Axon", "Dendrite", "Cell body", "Nerve ending"), "B", "The part of a neuron that receives information is called the dendrite, while the part that sends information as an electrical impulse is called the axon. Information is exchanged between neurons by releasing chemicals into the gap between their dendrites and axons. Neurotransmitters are the molecules involved, while neurotransmission serves as the mechanism. Hence, the correct answer is ‘Dendrite.’", "MEDIUM", pyq_year="2021"),
    item(7, "Which body system is responsible for controlling and coordinating body movements?", ("Skeletal system", "Nervous system", "Digestive system", "Cardiovascular system"), "B", "", "EASY", status="NEEDS_REVIEW", note="Source image confirms all four options, answer B, and EASY. The concluding explanation is clipped at the page bottom; no PYQ label is shown. Excluded from import."),
    item(8, "Which body system is responsible for maintaining the body's balance and equilibrium?", ("Nervous system", "Digestive system", "Urinary system", "Muscular system"), "A", "The nervous system, including the brain and various sensory organs, plays a crucial role in maintaining balance and equilibrium by processing sensory information and coordinating movements. The digestive system processes food, the urinary system regulates waste elimination and fluid balance, and the muscular system is primarily responsible for movement and support. Hence, the correct answer is ‘Nervous system.’", "MEDIUM"),
    item(9, "Spinal cord is the part of: I. Central Nervous System II. Peripheral Nervous System", ("Only I", "Only II", "None", "Both"), "A", "The central nervous system includes the brain and spinal cord and is the site of information processing and control. The peripheral nervous system comprises all the nerves of the body associated with the CNS (brain and spinal cord). The medulla of the brain is connected to the spinal cord. Hence, the correct answer is ‘Only I.’", "EASY"),
    item(10, "In how many parts is the human brain divided?", ("2", "3", "4", "5"), "B", "The forebrain is the main thinking part of the brain, responsible for cognitive, emotional, and motor activities. The midbrain, though small, connects the hindbrain with the forebrain and houses neural centres for reflexes and sensory sensations. The hindbrain consists of the medulla oblongata, cerebellum, and pons, regulating vital functions like breathing and heart rate, as well as maintaining posture and equilibrium. Hence, the correct answer is ‘3.’", "HARD", pyq_year="2017"),
    item(11, "Centre for heat, touch, cold, and pressure are in", ("Frontal lobe", "Occipital lobe", "Parietal lobe", "The frontal as well as occipital lobes both"), "C", "The frontal lobe is associated with reasoning, problem-solving, and voluntary movements. The occipital lobe is primarily responsible for vision. The parietal lobe processes sensory input like touch, temperature, and pressure. The frontal and occipital lobes do not collectively process those sensory signals. Hence, the correct answer is ‘Parietal lobe.’", "MEDIUM"),
    item(12, "Dendrites and axons are parts of which cell?", ("Red blood cell", "Neuron", "Nephron", "White blood cell"), "B", "Neurons, also known as nerve cells, send and receive signals from the brain. A neuron has three parts: dendrites, the cell body (soma), and the axon. Dendrites take information to the cell body; the cell body contains the nucleus; the axon takes information away from the cell body. Hence, the correct answer is ‘Neuron.’", "EASY"),
    item(13, "Neuron is the basic unit of _______.", ("Nervous System", "Circulatory System", "Excretory System", "Digestive System"), "A", "A neuron is the basic unit of the nervous system. Signals between the brain and other parts of the body are mediated by neurons. Almost 100 billion neurons are present in the human brain. A neuron comprises a cell body containing the nucleus and elongations known as axons. Hence, the correct answer is ‘Nervous System.’", "MEDIUM"),
    item(14, "The spinal cord originates from", ("Cerebrum", "Medulla", "Pons", "More than one of the above"), "B", "The spinal cord is a long, tubular structure that extends from the medulla oblongata to the lumbar part of the vertebral column. It is part of the central nervous system. It controls reflex actions and transmits sensory impulses from the skin and muscles to the brain. Hence, the correct answer is ‘medulla.’", "EASY"),
    item(15, "Which part of the brain maintains the posture and balance of the human body?", ("Cerebrum", "Pons", "Cerebellum", "Medulla"), "C", "The cerebellum controls posture, balance, and coordination of movements. It processes sensory inputs to maintain body stability, helps in smooth and precise muscle movements, and works with the inner ear and spinal cord for equilibrium. Hence, the correct answer is ‘Cerebellum.’", "MEDIUM"),
    item(16, "Which of the following is NOT a part of the hind-brain?", ("Pons", "Medulla", "Cerebellum", "Hypothalamus"), "D", "The hypothalamus is not a part of the hindbrain. It is a part of the brain that plays a vital role in controlling many bodily functions, including the release of hormones from the pituitary gland. The three main portions of the hindbrain are the pons, cerebellum, and medulla oblongata. Hence, the correct answer is ‘Hypothalamus.’", "MEDIUM", pyq_year="2021"),
    item(17, "The sensation of feeling full is because of a centre associated with hunger, which is in a separate part of the _______.", ("Pituitary gland", "Midbrain", "Forebrain", "Hindbrain"), "C", "", "MEDIUM", pyq_year="2023", status="NEEDS_REVIEW", note="Source image confirms four options, answer C, MEDIUM and PYQ 2023. The explanation continues below the captured page and is clipped; excluded from import."),
    item(18, "Which part of the brain regulates breathing?", ("Cerebellum", "Medulla", "Fore-brain", "Mid-brain"), "B", "The networks of neurons in the brainstem (pons and medulla) are responsible for the automatic and rhythmic act of breathing. This is typically controlled by the medulla oblongata, a region of the hindbrain. The medulla oblongata responds to carbon dioxide and oxygen levels by sending signals to the heart and diaphragm. The medulla is situated in front of the cerebellum in the brain stem. It transports sensory and motor neurons from the forebrain and midbrain.", "MEDIUM", pyq_year="2018"),
    item(19, "Which bone protects the brain?", ("Patella", "Sternum", "Clavicle", "Skull"), "D", "The bone that protects the brain is the skull, also known as the cranium. The skull is a complex structure made up of several bones that are fused together to form a strong, protective enclosure around the brain. It also provides attachment points for the muscles that control facial expression and jaw movement and plays a vital role in maintaining the structural integrity of the head and neck region. So, the correct option is the skull.", "MEDIUM", status="REJECTED", note="Source image was checked. This asks about the skull and maps to the existing Skeleton System chapter, not Brain & Nervous System; excluded from this batch."),
    item(20, "Which of the following is the main thinking part of the human brain?", ("Hind-brain", "Cerebrum", "Mid-brain", "None of the above"), "B", "The main thinking part of the human brain is the cerebrum. The cerebrum is the large outer part of the brain. It controls reading, thinking, learning, speech, emotions, and planned muscle movements like walking. The cerebrum, a major part of the forebrain, is the main thinking part of the brain and has sensory, motor, and association areas. Hence, the correct answer is ‘Cerebrum.’", "MEDIUM"),
    item(21, "Identify the part of the brain that is called the ‘Little Brain.’", ("Diencephalon", "Brainstem", "Cerebrum", "Cerebellum"), "D", "The part of the brain that controls the maintenance of posture, balance, and equilibrium is the cerebellum. The cerebellum is located at the back of the brain, beneath the cerebrum. It plays a crucial role in coordinating and fine-tuning movements, including control of posture, balance, and coordination. It receives sensory information from muscles, joints, and the inner ear, allowing it to make adjustments and corrections to maintain balance and equilibrium.", "MEDIUM", pyq_year="2019"),
    item(22, "Which part of the brain controls the heart?", ("Spinal Cord", "Medulla Oblongata", "Neuron", "None of these"), "B", "", "HARD", status="NEEDS_REVIEW", note="Source image confirms four options, answer B, and HARD. The explanation is clipped at the page bottom; no PYQ label is shown. Excluded from import."),
    item(15, "Hypothalamus is part of which organ of the Human body?", ("Brain", "Heart", "Spinal Cord", "Liver"), "A", "", "MEDIUM", status="NEEDS_REVIEW", source_pdf="Disease.pdf", note="Source image confirms the answer is Brain and the question maps to Brain & Nervous System, but its explanation is clipped below the captured page. No PYQ label is shown; excluded from import."),
]

# The repeated Respiratory source page is retained in the review dataset to
# preserve the source-level duplicate disposition; p. 4 is the fuller record.
ROWS.insert(1, item(3, "Which one of the following makes up the Central Nervous System together with the brain?", ("Neuron", "Brain", "Spinal Cord", "More than one of the above"), "D", "", "EASY", status="DUPLICATE", note="Confirmed exact duplicate of respiratory system - science.pdf p. 4 by matching stem, option order, and answer. Page 3 has no complete explanation capture; p. 4 is retained."))


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    review_dir = ROOT / "review-datasets" / CHAPTER
    import_dir = ROOT / "by-chapter" / CHAPTER
    review = review_dir / f"{CHAPTER}_review.csv"
    report = review_dir / f"{CHAPTER}_review_report.md"
    write_csv(review, REVIEW_FIELDS, ROWS)
    eligible = [row for row in ROWS if row["import_eligible"] == "true"]
    ordinary = [row for row in eligible if row["is_pyq"] == "false"]
    pyq = [row for row in eligible if row["is_pyq"] == "true"]

    def importer_row(row: dict[str, str]) -> dict[str, str]:
        return {
            "subject_slug": row["subject_slug"], "subcategory_slug": row["subcategory_slug"],
            "chapter_slug": row["chapter_slug"], "question_text": row["question_text"],
            "option_a": row["option_a"], "option_b": row["option_b"],
            "option_c": row["option_c"], "option_d": row["option_d"],
            "correct_option": row["proposed_correct_option"], "explanation": row["explanation"],
            "difficulty": row["difficulty"], "is_pyq": row["is_pyq"],
            "pyq_year": row["pyq_year"], "pyq_exam_name": row["pyq_exam_name"],
            "source": f"{row['source_pdf']} p. {row['source_page']}",
        }

    write_csv(import_dir / f"{CHAPTER}_ordinary.csv", IMPORT_FIELDS, [importer_row(r) for r in ordinary])
    write_csv(import_dir / f"{CHAPTER}_pyq.csv", IMPORT_FIELDS, [importer_row(r) for r in pyq])

    status_labels = {"VERIFIED": "Verified", "NEEDS_REVIEW": "Needs review", "REJECTED": "Rejected", "DUPLICATE": "Duplicate"}
    counts = {}
    for status in status_labels:
        for level in ("EASY", "MEDIUM", "HARD"):
            for kind, pred in (("Ordinary", lambda row: row["is_pyq"] == "false"), ("PYQ", lambda row: row["is_pyq"] == "true")):
                counts[(status, level, kind)] = sum(row["review_status"] == status and row["difficulty"] == level and pred(row) for row in ROWS)
    summary = [
        f"| {level} | {kind} | "
        + " | ".join(str(counts[(status, level, kind)]) for status in status_labels)
        + " |"
        for level in ("EASY", "MEDIUM", "HARD")
        for kind in ("Ordinary", "PYQ")
    ]
    gaps = {level: max(0, 25 - sum(row["difficulty"] == level and row["is_pyq"] == "false" for row in eligible)) for level in ("EASY", "MEDIUM", "HARD")}
    report.write_text("\n".join([
        "# Brain & Nervous System Chapter Review", "",
        f"- Catalog chapter: **Brain & Nervous System** (`{CHAPTER}`), ID `{CHAPTER_ID}`; confirmed through a read-only query beneath `gk-gs/science`.",
        "- Source pages: `respiratory system - science.pdf` pp. 2–22 (all 21 question pages); `Disease.pdf` p. 15 checked as an additional candidate. `brain and nervous system - science.pdf` pp. 2–21 were also visually sampled; its 20 question pages contain excretory-system content and add no Brain & Nervous System questions.",
        "- The Respiratory PDF pages with Brain & Nervous System content are pp. 2–18 and 20–22. Page 3 duplicates p. 4; p. 19 is a Skeleton System question.",
        "- The additional `Disease.pdf` p. 15 question asks which organ contains the hypothalamus; its answer is Brain, but the explanation is clipped, so it remains pending.",
        "", "## Disposition counts", "", "| Difficulty | Type | Verified | Needs review | Rejected | Duplicate |", "|---|---|---:|---:|---:|---:|", *summary,
        "", f"- Verified/import-ready records: {len(eligible)} ({len(ordinary)} ordinary, {len(pyq)} PYQ).",
        f"- Needs review: {sum(r['review_status'] == 'NEEDS_REVIEW' for r in ROWS)}; rejected as outside chapter: {sum(r['review_status'] == 'REJECTED' for r in ROWS)}; confirmed duplicate records: {sum(r['review_status'] == 'DUPLICATE' for r in ROWS)}.",
        "- Confirmed duplicate retained only once: Respiratory PDF p. 3 is duplicate of p. 4.",
        "", "## Ordinary target gaps", "", "| Difficulty | Verified ordinary | Target | Remaining |", "|---|---:|---:|---:|",
        *[f"| {level} | {25-gaps[level]} | 25 | {gaps[level]} |" for level in ("EASY", "MEDIUM", "HARD")],
        "", "PYQs are tracked separately and do not count toward ordinary targets. No exam names were visible; none were inferred.",
        "", "## Duplicate audit", "",
        "Compared 20 distinct Brain candidates (19 from the Respiratory PDF and the additional Disease p. 15 candidate) with 33 active question-bank rows and all 99 prior chapter-review rows (85 had nonempty stems). No active-question or prior-batch duplicate was confirmed. The nearest text-similarity lead was Respiratory PDF p. 16 vs. a Circulatory System valve question (0.815); visual/content comparison shows unrelated subjects and different answer choices. Similar concept mentions were not counted as duplicates.",
        "", "## Review limits", "",
        "Pages with clipped explanations (Respiratory PDF pp. 2, 5, 7, 17, 22 and Disease p. 15) remain NEEDS_REVIEW and are excluded from both importer CSVs. Page text, option order, highlighted answers, explanation completeness, visible difficulty, and PYQ labels/years were checked against rendered source pages. The PDF titled `brain and nervous system - science.pdf` was not treated as topic evidence.",
        "", "## Validation", "",
        "Importer dry-run validation is covered by `tests/test_science_import_candidates.py`; it uses the isolated test database, asserts all 14 eligible rows are accepted and imported count is zero, and checks the test database remains empty. No production import was run.",
    ]) + "\n", encoding="utf-8")
    print(f"Wrote {review}; eligible ordinary={len(ordinary)}, PYQ={len(pyq)}")


if __name__ == "__main__":
    main()
