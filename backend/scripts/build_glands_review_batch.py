"""Build the visually reviewed Glands chapter review and importer artifacts."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "data/imports/science"
CHAPTER = "glands"
CHAPTER_ID = "3a7d5736-5a65-434b-8c2c-0f17905bab57"
DISEASE_PAGES = (2, 3, 8, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21)

# Source-stated difficulty/PYQ metadata and page-visible stems, options, answers.
# Pending explanations are loaded verbatim from OCR and are never completed here.
ROWS = [
    ("Disease.pdf", 2, "If the hypothalamus fails to function, which of the following will be most directly affected?", ("Sweat secretion", "Hormonal regulation of the pituitary gland", "Bile secretion", "Salivary enzyme production"), "B", "MEDIUM", False, "", "NEEDS_REVIEW"),
    ("Disease.pdf", 3, "A patient shows immune deficiency due to improper maturation of T-cells. Which gland is most likely malfunctioning?", ("Thyroid", "Thymus", "Pituitary", "Pineal"), "B", "MEDIUM", False, "", "NEEDS_REVIEW"),
    ("Disease.pdf", 8, "If a gland loses its duct but continues secretions, how will its classification change?", ("It becomes exocrine", "It becomes endocrine", "It becomes inactive", "It becomes nervous tissue"), "B", "MEDIUM", False, "", "VERIFIED"),
    ("Disease.pdf", 10, "Which of the following best explains the role of hormones?", ("They act only at the site of secretion", "They regulate body processes through chemical signaling", "They are structural proteins", "They are only involved in digestion"), "B", "MEDIUM", False, "", "NEEDS_REVIEW"),
    ("Disease.pdf", 11, "What is the primary difference between Endocrine Glands and Exocrine Glands?", ("Endocrine glands release substances through ducts, while exocrine glands release hormones directly into the bloodstream.", "Endocrine glands release hormones directly into the bloodstream, while exocrine glands release substances through ducts.", "Both endocrine and exocrine glands release substances directly into the bloodstream.", "Neither endocrine nor exocrine glands release substances directly into the bloodstream."), "B", "MEDIUM", False, "", "NEEDS_REVIEW"),
    ("Disease.pdf", 12, "Which of the following glands secretes the hormone that regulates physical growth in humans?", ("Parathyroid", "Adrenal", "Pituitary", "Thymus"), "C", "MEDIUM", False, "", "NEEDS_REVIEW"),
    ("Disease.pdf", 13, "_____ is not an endocrine gland in humans.", ("Pineal gland", "Pituitary gland", "Liver", "Adrenal gland"), "C", "MEDIUM", True, "2018", "VERIFIED"),
    ("Disease.pdf", 14, "Which of the following hormone is secreted by the brain that helps to regulate sleep-wake cycles?", ("Insulin", "Melatonin", "Aldosterone", "Oxytocin"), "B", "MEDIUM", True, "2021", "NEEDS_REVIEW"),
    ("Disease.pdf", 16, "Which gland in the endocrine system is responsible for regulating metabolism and is located in the front of your neck?", ("Adrenal gland", "Pituitary gland", "Thyroid gland", "Pancreas"), "C", "EASY", False, "", "NEEDS_REVIEW"),
    ("Disease.pdf", 17, "Antidiuretic Hormone (ADH) is also known as:", ("Vasopressin", "Oxytocin", "Melatonin", "Serotonin"), "A", "EASY", False, "", "NEEDS_REVIEW"),
    ("Disease.pdf", 18, "Which gland in the endocrine system is responsible for producing growth hormone?", ("Adrenal gland", "Pituitary gland", "Thyroid gland", "Pancreas"), "B", "MEDIUM", False, "", "NEEDS_REVIEW"),
    ("Disease.pdf", 19, "Which hormone is primarily responsible for the synthesis of breast milk?", ("Oxytocin", "Estrogen", "Prolactin", "Progesterone"), "C", "MEDIUM", False, "", "NEEDS_REVIEW"),
    ("Disease.pdf", 20, "A gland secretes its product into blood and regulates multiple organs simultaneously. Which property is most likely true?", ("It has a duct system", "Its secretion is rapid and short-lived only", "Its secretion acts as a chemical messenger", "It secretes digestive enzymes"), "C", "MEDIUM", False, "", "NEEDS_REVIEW"),
    ("Disease.pdf", 21, "Oxytocin is stored in which portion of the brain?", ("Hypothalamus", "Posterior pituitary gland", "Medulla oblongata", "Anterior pituitary gland"), "B", "MEDIUM", False, "", "NEEDS_REVIEW"),
    ("Glands.pdf", 30, "Along the path of the vas deferens which glands add their secretions in the sperms? I. Prostate II. Seminal vesicles III. Scrotum", ("Only I and III", "Only I and II", "Only II and III", "All I, II and III"), "B", "MEDIUM", False, "", "NEEDS_REVIEW"),
]

REVIEW_HEADER = ["source_pdf", "source_page", "subject_slug", "subcategory_slug", "chapter_slug", "catalog_chapter_id", "question_text", "option_a", "option_b", "option_c", "option_d", "proposed_correct_option", "explanation", "difficulty", "is_pyq", "pyq_year", "pyq_exam_name", "review_status", "import_eligible", "review_note"]
IMPORT_HEADER = ["subject_slug", "subcategory_slug", "chapter_slug", "question_text", "option_a", "option_b", "option_c", "option_d", "correct_option", "explanation", "difficulty", "is_pyq", "pyq_year", "pyq_exam_name", "source"]


def write_csv(path: Path, header: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    queue_path = ROOT / "SCIENCE_OCR_REVIEW_QUEUE.csv"
    with queue_path.open(encoding="utf-8-sig", newline="") as stream:
        queue = list(csv.DictReader(stream))
        queue_header = list(queue[0])
    queue_by_key = {(row["source_pdf"], row["source_page"]): row for row in queue}
    review_rows = []
    for source, page, stem, options, answer, difficulty, is_pyq, year, status in ROWS:
        queued = queue_by_key[(source, str(page))]
        explanation = queued["explanation_ocr"].strip()
        if source == "Disease.pdf" and page == 8:
            explanation = (
                "If a gland loses its duct but continues secretions, its classification "
                "changes from an exocrine gland (which has ducts) to an endocrine gland "
                "(which is ductless). Exocrine glands release their products through a "
                "duct to a surface. Endocrine glands (ductless glands) release their "
                "secretions (hormones) directly into the bloodstream after losing their "
                "connection to the epithelial surface. Hence, the correct answer is "
                "\"It becomes endocrine\"."
            )
        elif source == "Disease.pdf" and page == 13:
            explanation = (
                "Endocrine glands are the glands that secrete hormones. There are eight "
                "major endocrine glands scattered throughout the body: the pituitary, "
                "pineal, thyroid, thymus, pancreas, adrenal glands, ovaries (in females), "
                "and testes (in males). The liver is not an endocrine gland. The liver "
                "acts as an exocrine gland when creating and excreting bile to be stored "
                "in the gallbladder. Hence, the correct answer is \"Liver\"."
            )
        note = (
            "Page image confirms complete stem, options/order, highlighted answer B, complete explanation, and MEDIUM label. No PYQ label or exam name is shown."
            if source == "Disease.pdf" and page == 8
            else "Page image confirms stem, options/order, highlighted answer C, complete explanation, MEDIUM and explicit PYQ 2018 labels. No exam name is shown."
            if source == "Disease.pdf" and page == 13
            else "Visually checked against source image; the explanation is clipped in the source capture. Kept pending and excluded from import."
        )
        review_rows.append(dict(zip(REVIEW_HEADER, [source, str(page), "gk-gs", "science", CHAPTER, CHAPTER_ID, stem, *options, answer, explanation, difficulty, str(is_pyq).lower(), year, "", status, str(status == "VERIFIED").lower(), note])))

    eligible = [row for row in review_rows if row["import_eligible"] == "true"]
    review_dir = ROOT / "review-datasets" / CHAPTER
    batch_dir = ROOT / "by-chapter" / CHAPTER
    write_csv(review_dir / "glands_review.csv", REVIEW_HEADER, review_rows)
    for pyq in (False, True):
        batch = []
        for row in eligible:
            if (row["is_pyq"] == "true") != pyq:
                continue
            batch.append({"subject_slug": "gk-gs", "subcategory_slug": "science", "chapter_slug": CHAPTER, "question_text": row["question_text"], "option_a": row["option_a"], "option_b": row["option_b"], "option_c": row["option_c"], "option_d": row["option_d"], "correct_option": row["proposed_correct_option"], "explanation": row["explanation"], "difficulty": row["difficulty"], "is_pyq": row["is_pyq"], "pyq_year": row["pyq_year"], "pyq_exam_name": "", "source": f"{row['source_pdf']} p. {row['source_page']}"})
        write_csv(batch_dir / f"glands_{'pyq' if pyq else 'ordinary'}.csv", IMPORT_HEADER, batch)

    by_key = {(row["source_pdf"], row["source_page"]): row for row in review_rows}
    for queue_row in queue:
        record = by_key.get((queue_row["source_pdf"], queue_row["source_page"]))
        if not record:
            continue
        queue_row.update({"chapter_slug": CHAPTER, "review_status": record["review_status"], "review_note": record["review_note"], "difficulty_ocr": record["difficulty"], "pyq_label_ocr": "PYQ" if record["is_pyq"] == "true" else "NO_PYQ_LABEL_DETECTED", "pyq_year_ocr": record["pyq_year"], "question_text_ocr": record["question_text"], "option_a_ocr": record["option_a"], "option_b_ocr": record["option_b"], "option_c_ocr": record["option_c"], "option_d_ocr": record["option_d"], "correct_option_ocr": record["proposed_correct_option"], "explanation_ocr": record["explanation"]})
    write_csv(queue_path, queue_header, queue)

    decisions_path = ROOT / "SCIENCE_REVIEW_DECISIONS.csv"
    with decisions_path.open(encoding="utf-8-sig", newline="") as stream:
        decisions = list(csv.DictReader(stream))
        decision_header = list(decisions[0])
    existing = {(row["source_pdf"], row["source_page"]): row for row in decisions}
    for row in review_rows:
        key = row["source_pdf"], row["source_page"]
        decision = {"source_pdf": key[0], "source_page": key[1], "chapter_slug": CHAPTER, "review_status": row["review_status"], "review_note": row["review_note"]}
        if key in existing:
            existing[key].update(decision)
        else:
            decisions.append(decision)
    write_csv(decisions_path, decision_header, decisions)

    report = """# Glands Chapter Review

- Existing catalog chapter: **Glands** (`glands`), ID `3a7d5736-5a65-434b-8c2c-0f17905bab57`, under `gk-gs/science`. The existing catalog row was retained; no duplicate chapter was created.
- Visually reviewed all 14 reserved question pages in `Disease.pdf`: pp. 2, 3, 8, 10–14, and 16–21. The page images confirm Glands/endocrine content, difficulty labels, marked answers, options, and visible PYQ metadata. Pages 8 and 13 have complete explanations; the other 12 source captures visibly cut off their explanations and remain pending.
- Searched OCR transcripts for all 21 Science PDFs by endocrine, gland, hormone, pituitary, thyroid, and related question content. No further clearly endocrine/Glands questions were found. `Glands.pdf` p. 30 is an additional accessory-gland question; its answer/options and MEDIUM label are visible, but its explanation is clipped, so it remains pending. The salivary-gland identification question in `cell -science.pdf` p. 20 remains assigned to Digestive System per its completed review. Reproductive and skeletal questions in `Glands.pdf` were not reassigned based on the misleading filename.
- Candidate rows reviewed for this chapter: 15. Verified: **2** (1 ordinary, 1 PYQ). Needs review: **13**. Rejected: **0** in the Glands question candidate set. Confirmed duplicates: **0**. No exam names were visible; none were inferred.

## Verified counts and ordinary coverage

| Difficulty | Verified ordinary | Target | Remaining |
|---|---:|---:|---:|
| EASY | 0 | 25 | 25 |
| MEDIUM | 1 | 25 | 24 |
| HARD | 0 | 25 | 25 |

The one verified PYQ is MEDIUM, year 2018 (`Disease.pdf` p. 13). PYQs are tracked separately and do not count toward ordinary targets. Difficulty is internal classification metadata; Science users do not get a difficulty-selection step.

## Duplicate audit

Compared the 15 Glands candidates with all 44 active question records and 249 non-Glands prior review/import rows. No exact stem or high-similarity match at 0.80 or above was found. The highest active-record stem similarity was 0.650 and concerned unrelated Disease wording. Similar endocrine concepts (for example hormone roles and endocrine/exocrine classification) are distinct questions with different stems and options. No Glands source pair was confirmed as a duplicate.

## Import readiness and validation

Only the two fully verified, source-complete, nonduplicate questions are in the separate importer files (1 ordinary, 1 PYQ). The 13 pending records are excluded. Dry-run validation is in-memory only and does not import these questions into production. Disease's previously approved 11-question production import remains complete and unchanged.

## Source limitations

The source captures for Disease.pdf pp. 2, 3, 10–12, 14, and 16–21 and Glands.pdf p. 30 cut off explanation text. Their visible stem, options, selected answer, difficulty, and any shown PYQ year were transcribed without supplying missing explanation text. They remain `NEEDS_REVIEW`.

## Next recommended chapter

Review **Reproduction** next. The scan of `Glands.pdf` contains a larger set of reproductive-system questions, and a content-led review of those pages plus `reproduction.pdf` can establish the correct mappings without relying on either filename.
"""
    (review_dir / "glands_review_report.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
