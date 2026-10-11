"""Build the source-verified Excretory System review batch from page-image decisions."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "data/imports/science"
SOURCE = "brain and nervous system - science.pdf"
CHAPTER = "excretory-system"
CHAPTER_ID = "f5dabc77-d970-46a4-960f-deb6ecb2c8fb"

# (page, stem, A, B, C, D, answer, explanation, difficulty, pyq, year, status, note)
ROWS = [
 (2,"Main excretory substance in mammals is:","Ammonia","Amino acid","Uric acid","Urea","D","","MEDIUM",False,"","NEEDS_REVIEW","Explanation is clipped at the bottom of the source page; excluded from import."),
 (3,"Harmful metabolic wastes from our body are removed by the biological process called:","Defecation","Transportation","Secretion","Excretion","D","The removal of harmful metabolic wastes (like urea, CO₂, and excess salts) from the body is called excretion. Organs like the kidneys, lungs, skin, and liver are involved in excretion. This process helps maintain homeostasis and prevents toxic accumulation in the body. Defecation removes undigested food, secretion releases useful substances, and transportation moves materials but does not remove wastes. Hence, the correct answer is excretion.","MEDIUM",False,"","VERIFIED","Source page image checked: wording, four options/order, marked answer D, complete explanation, and MEDIUM label verified. No PYQ label or exam name visible."),
 (4,"Uric acid is present in:","Soda water","Rancid butter","Sour milk","Human urine","D","As the body breaks down purine-containing compounds, uric acid is produced. It dissolves in the blood and is carried to the kidneys, after which it is excreted in urine.","MEDIUM",False,"","VERIFIED","Page image confirms all options, answer D, complete explanation, and MEDIUM label. No PYQ label or exam name visible."),
 (5,"Excretion means:","Removal of substances present in excess","Formation of those substances that have some role in the body","Removal of such substances that have never been part of the body","All options are correct","A","Excretion is a vital physiological process in living organisms that plays a crucial role in maintaining homeostasis. It involves the elimination of metabolic waste products and harmful substances from the body. This process ensures that the internal environment remains stable and free from the accumulation of toxic or unnecessary compounds. Excretion primarily occurs through various organ systems, such as the","EASY",True,"2017","NEEDS_REVIEW","Explicit PYQ 2017 and EASY labels, options, and marked answer verified. Explanation is visibly clipped mid-sentence."),
 (6,"Humans are ____ organisms.","Ureotelic","Uricotelic","Ammonotelic","Guanotelic","A","Humans are ureotelic organisms. Ureotelic organisms (including mammals like humans) primarily excrete their nitrogenous waste in the form of urea, which is produced in the liver and excreted through urine. Uricotelic organisms (e.g., birds and reptiles) excrete nitrogen as uric acid. Ammonotelic organisms (e.g., aquatic fish) excrete nitrogen as ammonia. Guanotelic organisms primarily excrete nitrogenous waste as guanine. Hence, the correct answer is ureotelic.","MEDIUM",False,"","VERIFIED","Page image confirms wording, options/order, answer A, complete explanation, and MEDIUM label."),
 (7,"The waste product released by the excretory system of fish is mostly:","Ammonia","Uric acid","Urea","None","A","The waste product released by the excretory system of fish is mostly ammonia. Ammonotelic fishes excrete ammonia directly into the water, where it is diluted. Both freshwater and most marine fishes primarily excrete ammonia, although some marine teleosts can","EASY",False,"","NEEDS_REVIEW","Answer A and options verified. Explanation is clipped after “can”; excluded from import."),
 (8,"Metabolic activities that generate nitrogenous waste material in human beings are removed by:","The vascular system","The excretory system","The circulatory system","The respiratory system","B","Nitrogenous wastes in humans mainly include urea, uric acid, and creatinine, which are by-products of protein and nucleic acid metabolism. The excretory system removes metabolic wastes. Kidneys filter blood and produce urine; ureters, bladder, and urethra transport and expel urine. In the kidneys, blood is filtered, nitrogenous wastes are concentrated into urine, and clean blood is returned to circulation.","MEDIUM",False,"","VERIFIED","Page image confirms complete stem/options, answer B, visible complete explanation, and MEDIUM label."),
 (9,"Which body system is responsible for processing and eliminating waste products from the body?","Reproductive system","Lymphatic system","Excretory system","Integumentary system","C","The excretory system, which includes the kidneys, ureters, bladder, and urethra, is responsible for filtering waste products from the blood and eliminating them from the body in the form of urine. The reproductive system is responsible for reproduction. The lymphatic system is involved in immune function. The integumentary system is primarily responsible for protecting the body and regulating temperature. Hence, the correct answer is “Excretory","MEDIUM",False,"","NEEDS_REVIEW","Marked answer C and options verified. Explanation is clipped after “Excretory”; excluded from import."),
 (10,"Nitrogenous wastes are produced due to the breakdown of:","Carbohydrates and lipids","Proteins and nucleic acids","Vitamins and minerals","Fats and glucose","B","Nitrogenous wastes are produced due to the breakdown of proteins and nucleic acids. Proteins are broken down into amino acids; deamination releases nitrogen, forming ammonia, which is subsequently converted into urea. Nucleic acids are broken down into nucleotides containing nitrogenous bases; catabolism of these bases also produces nitrogenous wastes like urea and uric acid.","MEDIUM",False,"","VERIFIED","Page image confirms stem/options and highlighted answer B; full explanation is visible and ends with a complete sentence. MEDIUM label verified."),
 (11,"Guanotelic organisms are those that excrete nitrogenous waste mainly in the form of:","Urea","Ammonia","Guanine","Uric acid","C","Guanotelic organisms convert nitrogenous waste into guanine before excretion. This mode of excretion is typically found in animals living in arid or water-scarce environments because guanine is insoluble in water and requires virtually no water for elimination. Spiders and scorpions are examples. Certain birds and reptiles utilize this pathway to conserve moisture.","MEDIUM",False,"","VERIFIED","Page image confirms four options/order, highlighted answer C, complete explanation, and MEDIUM label."),
 (12,"Main excretory product in birds and reptiles:","Urea","Uric acid","Ammonia","Guanine","B","Birds and reptiles are uricotelic organisms, meaning they primarily excrete uric acid. Uric acid is relatively insoluble in water and is excreted as a thick, semi-solid paste or white powder, requiring minimal water. It is the least toxic of the primary nitrogenous wastes and can be stored inside an egg during embryonic development.","MEDIUM",False,"","VERIFIED","Page image confirms answer B, all options and complete explanation. Exact duplicate of page 21; page 12 retained as first occurrence."),
 (13,"The process by which waste products are removed from the body is commonly known as:","Reproduction","Respiration","Excretion","Suction","C","The process of producing offspring that are biologically or genetically similar to the parent organism is known as reproduction. Respiration is a metabolic process in which cells obtain energy by taking in oxygen and releasing carbon dioxide. Excretion is the process by which metabolic wastes are eliminated from the body. Suction is the removal of air from","MEDIUM",True,"2017","NEEDS_REVIEW","Explicit PYQ 2017 and MEDIUM labels, options, and marked answer C verified. Explanation is clipped mid-sentence."),
 (14,"Which of the following is NOT a waste material removed from blood in the kidney?","Ammonia","Carbon dioxide","Urea","Uric acid","B","The kidneys remove waste products from blood, including urea, uric acid, and ammonia. Carbon dioxide is removed through the lungs. Urea is produced when the body breaks down protein and is removed by the kidneys. Uric acid is produced when the body breaks down purines. Ammonia is produced when the body breaks down proteins. Ammonia is toxic to the body, so it must","EASY",False,"","NEEDS_REVIEW","Options and marked answer B verified. Explanation is clipped before completion; excluded from import."),
 (15,"Which of the following statements about uric acid is correct?","Uric acid is highly soluble in water","Uric acid is the most toxic nitrogenous waste","Uric acid helps in water conservation","Uric acid is excreted mainly by aquatic animals","C","Uric acid is the nitrogenous waste product that requires the least amount of water for excretion, making it a critical adaptation for water conservation in terrestrial animals. Because it is relatively non-toxic and nearly insoluble in water, it can be excreted as a concentrated, semi-solid paste or pellet rather than a liquid.","MEDIUM",False,"","VERIFIED","Page image confirms stem/options, highlighted answer C, full explanation, and MEDIUM label."),
 (16,"Where does the formation of urea take place in our body?","Pancreas","Kidney","Liver","Lungs","C","Urea formation occurs in the liver through the urea cycle (or ornithine cycle). It removes toxic ammonia produced from protein metabolism. The urea is transported to the kidneys for excretion through urine. This helps maintain nitrogen balance in the body. Hence, the correct answer is liver.","MEDIUM",True,"2022","VERIFIED","Explicit PYQ 2022 and MEDIUM labels, all options/order, marked answer C, and complete explanation verified on the page image. No exam name shown."),
 (17,"Which of these is an excretory organ of the human body?","Heart","Skin","Brain","Muscles","B","Skin has a role in excretion by producing sweat. Sweating eliminates excess salts, water, and urea. The heart pumps blood through an artery network; the brain is the central organ of the nervous system; the spinal cord makes up the central nervous system. Hence, the correct answer is skin.","EASY",True,"2020","VERIFIED","Explicit PYQ 2020 and EASY labels, options/order, marked answer B, and complete explanation verified. No exam name shown."),
 (18,"The waste product released by the excretory system of birds and insects is mostly:","Ammonotelic","Uricotelic","Both A and B","None","B","Birds and insects primarily excrete uric acid, which is insoluble in water and helps conserve water. Organisms that excrete uric acid as their main nitrogenous waste are called uricotelic. This adaptation minimizes water loss. Ammonotelic organisms such as fish and amphibians excrete ammonia, which requires more water. Hence, the correct answer is uricotelic.","MEDIUM",False,"","NEEDS_REVIEW","The image marks option B and the explanation identifies uricotelic, but the stem asks for the waste product while its options are organism classifications. Internally inconsistent stem/options; excluded from import pending clarification."),
 (19,"Main excretory substance in mammals is:","Ammonia","Amino acid","Uric acid","Urea","D","","MEDIUM",False,"","DUPLICATE","Exact duplicate of page 2: same stem, four options/order, and marked answer. Page 2 is retained; both source explanations are clipped."),
 (20,"The waste product released by the excretory system of fish is mostly:","Ammonia","Uric acid","Urea","None","A","","EASY",False,"","DUPLICATE","Exact duplicate of page 7: same stem, options/order, and marked answer. Page 7 is retained; both explanations are clipped."),
 (21,"Main excretory product in birds and reptiles:","Urea","Uric acid","Ammonia","Guanine","B","Birds and reptiles are uricotelic organisms, meaning they primarily excrete uric acid. Uric acid is relatively insoluble in water and is excreted as a thick, semi-solid paste or white powder, requiring minimal water. It is the least toxic of the primary nitrogenous wastes and can be stored inside an egg during embryonic development.","MEDIUM",False,"","DUPLICATE","Exact duplicate of page 12: same stem/options/order, marked answer, and explanation. Page 12 is retained."),
]

REVIEW_HEADER = ["source_pdf","source_page","subject_slug","subcategory_slug","chapter_slug","catalog_chapter_id","question_text","option_a","option_b","option_c","option_d","proposed_correct_option","explanation","difficulty","is_pyq","pyq_year","pyq_exam_name","review_status","import_eligible","review_note"]
IMPORT_HEADER = ["subject_slug","subcategory_slug","chapter_slug","question_text","option_a","option_b","option_c","option_d","correct_option","explanation","difficulty","is_pyq","pyq_year","pyq_exam_name","source"]

def main() -> None:
    review_dir = ROOT / "review-datasets" / CHAPTER
    import_dir = ROOT / "by-chapter" / CHAPTER
    review_dir.mkdir(parents=True, exist_ok=True)
    import_dir.mkdir(parents=True, exist_ok=True)
    review_rows = []
    for page, stem, a, b, c, d, answer, explanation, difficulty, pyq, year, status, note in ROWS:
        review_rows.append(dict(zip(REVIEW_HEADER, [SOURCE,str(page),"gk-gs","science",CHAPTER,CHAPTER_ID,stem,a,b,c,d,answer,explanation,difficulty,str(pyq).lower(),year,"",status,str(status=="VERIFIED").lower(),note])))
    def write(path: Path, header: list[str], rows: list[dict[str,str]]) -> None:
        with path.open("w", encoding="utf-8-sig", newline="") as stream:
            writer=csv.DictWriter(stream, fieldnames=header); writer.writeheader(); writer.writerows(rows)
    write(review_dir / f"{CHAPTER}_review.csv", REVIEW_HEADER, review_rows)
    eligible = [r for r in review_rows if r["import_eligible"] == "true"]
    for kind in (False, True):
        batch=[]
        for r in eligible:
            if (r["is_pyq"] == "true") != kind: continue
            batch.append({"subject_slug":"gk-gs","subcategory_slug":"science","chapter_slug":CHAPTER,"question_text":r["question_text"],"option_a":r["option_a"],"option_b":r["option_b"],"option_c":r["option_c"],"option_d":r["option_d"],"correct_option":r["proposed_correct_option"],"explanation":r["explanation"],"difficulty":r["difficulty"],"is_pyq":r["is_pyq"],"pyq_year":r["pyq_year"],"pyq_exam_name":"","source":f"{SOURCE} p. {r['source_page']}"})
        write(import_dir / f"{CHAPTER}_{'pyq' if kind else 'ordinary'}.csv", IMPORT_HEADER, batch)
    # Update only the selected PDF's existing review-queue records; preserve all other records.
    queue_path=ROOT/"SCIENCE_OCR_REVIEW_QUEUE.csv"
    with queue_path.open(encoding="utf-8-sig",newline="") as stream: queue=list(csv.DictReader(stream)); qheader=list(queue[0])
    by_page={str(r["source_page"]):r for r in review_rows}
    for q in queue:
        if q["source_pdf"]==SOURCE and q["source_page"] in by_page:
            r=by_page[q["source_page"]]; q["chapter_slug"]=CHAPTER; q["review_status"]=r["review_status"]; q["review_note"]=r["review_note"]
    write(queue_path,qheader,queue)
    decisions_path=ROOT/"SCIENCE_REVIEW_DECISIONS.csv"
    with decisions_path.open(encoding="utf-8-sig",newline="") as stream: decisions=list(csv.DictReader(stream)); dheader=list(decisions[0])
    existing={(d["source_pdf"],d["source_page"]) for d in decisions}
    for r in review_rows:
        key=(SOURCE,r["source_page"])
        if key not in existing: decisions.append({"source_pdf":SOURCE,"source_page":r["source_page"],"chapter_slug":CHAPTER,"review_status":r["review_status"],"review_note":r["review_note"]})
    write(decisions_path,dheader,decisions)
    report = """# Excretory System Chapter Review

- Catalog chapter: **Excretory System** (`excretory-system`), ID `f5dabc77-d970-46a4-960f-deb6ecb2c8fb`, confirmed from the existing `gk-gs/science` catalog.
- Source reviewed: `brain and nervous system - science.pdf`, physical PDF pages 2–21 (20 question pages). The title does not describe these questions. The separately named `excretory system - science.pdf` was not used because its reviewed pages concern nutrition/proteins.
- All 20 pages were visually checked against their OCR transcript. A search of the other Science OCR transcripts found no additional confidently mappable Excretory System questions.
- No exam names were visible; none were inferred. Difficulty labels are preserved for internal review and coverage only.

## Disposition by difficulty and question type

| Difficulty | Type | Verified | Needs review | Rejected | Duplicate |
|---|---|---:|---:|---:|---:|
| EASY | Ordinary | 0 | 2 | 0 | 1 |
| EASY | PYQ | 1 | 1 | 0 | 0 |
| MEDIUM | Ordinary | 8 | 3 | 0 | 2 |
| MEDIUM | PYQ | 1 | 1 | 0 | 0 |
| HARD | Ordinary | 0 | 0 | 0 | 0 |
| HARD | PYQ | 0 | 0 | 0 | 0 |

- Verified/import-ready: **10** (8 ordinary, 2 PYQ).
- Needs review: **7** (5 ordinary, 2 PYQ). Six explanations are visibly clipped. Page 18 has an answer/explanation consistent with “uricotelic” but its stem asks for a waste product while its options are organism classifications, so it is pending for inconsistent stem/options.
- Rejected: **0**. Confirmed duplicate source rows: **3** (pp. 19→2, 20→7, 21→12). No candidate was rejected as unrelated.
- The p. 2 and p. 19, p. 7 and p. 20 explanation captures are clipped; their source duplicates are still confirmed from the matching stem/options/answer. Retained candidates remain pending and are not imported.

## Ordinary-question coverage targets

| Difficulty | Verified ordinary | Target | Remaining |
|---|---:|---:|---:|
| EASY | 0 | 25 | 25 |
| MEDIUM | 8 | 25 | 17 |
| HARD | 0 | 25 | 25 |

PYQs are tracked separately and do not count toward ordinary targets. Science users are not asked to select difficulty; these labels are internal quality metadata only.

## Duplicate review

All candidates were compared with the active question bank and previously prepared Science review/import batches. Three exact duplicate pairs occur within this source: p. 19 duplicates p. 2, p. 20 duplicates p. 7, and p. 21 duplicates p. 12. No duplicate against active records or earlier chapter batches was confirmed. Global duplicate report and decisions were extended without replacing prior chapter records.

## Validation

The ordinary and PYQ CSVs contain only fully verified records with complete explanations and importer fields. They are covered by isolated importer dry-run tests that require zero inserted rows. No production import or database modification was performed.
"""
    (review_dir / f"{CHAPTER}_review_report.md").write_text(report, encoding="utf-8")

if __name__ == "__main__": main()
