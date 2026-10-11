"""Create the manually reviewed Disease chapter batch and append shared decisions."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "data/imports/science"
DISEASE_ID = "79eeb111-c0df-4863-aac2-94086844f83b"
GLANDS_ID = "3a7d5736-5a65-434b-8c2c-0f17905bab57"
DISEASE = "disease"
GLANDS = "glands"

# source, page, stem, options, answer, explanation, difficulty, pyq, year, status, note
ROWS = [
 ("Disease.pdf",4,"Which disease listed is caused by ingestion of improperly cooked food rather than insect transmission?",["Kala-azar","Sleeping sickness","Filariasis","Taeniasis"],"D","The disease caused by ingestion of improperly cooked food, rather than insect transmission, is taeniasis. Taeniasis is an intestinal infection caused by tapeworms, typically acquired by eating raw or undercooked beef (Taenia saginata) or pork (Taenia solium), which contains larval cysts. Kala-azar is visceral leishmaniasis spread by infected female sandflies. Sleeping sickness is African trypanosomiasis transmitted by tsetse flies. Filariasis is spread by mosquitoes.","MEDIUM",False,"","NEEDS_REVIEW","Page image confirms question, options/order, marked answer D, and MEDIUM label. The explanation is clipped after the Filariasis option; excluded from import."),
 ("Disease.pdf",5,"Which of the following diseases primarily affects the lymphatic system leading to swelling?",["Psoriasis","Filariasis","Taeniasis","Cholelithiasis"],"B","Filariasis (lymphatic filariasis/elephantiasis) is caused by thread-like parasitic worms transmitted through mosquito bites. The parasites reside in lymphatic vessels and nodes and can cause damage and blockage. This impairs drainage of fluid from tissues, leading to chronic swelling (lymphedema). The source then compares psoriasis and taeniasis; the final cholelithiasis explanation is clipped.","MEDIUM",False,"","NEEDS_REVIEW","Page image confirms answer B and all four options. The explanation is clipped in the final option discussion; excluded from import."),
 ("Disease.pdf",6,"A patient has enlarged spleen, darkened skin, and prolonged fever. Which pathogen is most likely responsible?",["Trypanosoma brucei","Leishmania donovani","Wuchereria bancrofti","Taenia solium"],"B","The clinical presentation of an enlarged spleen (splenomegaly), darkened skin, and prolonged fever is characteristic of visceral leishmaniasis, also known as kala-azar. It is caused by Leishmania donovani and transmitted to humans through the bite of an infected female sandfly. The source explanation continues with the mechanism and symptoms but is clipped mid-sentence.","MEDIUM",False,"","NEEDS_REVIEW","Page image confirms answer B, all options/order, and MEDIUM label. The explanation is clipped mid-sentence; excluded from import."),
 ("Disease.pdf",7,"Which disease is correctly matched with its vector?",["Kala-azar - Tsetse fly","Sleeping sickness - Sand fly","Filariasis - Female Culex mosquito","Taeniasis - Housefly"],"C","Filariasis (specifically lymphatic filariasis) is a parasitic disease caused by microscopic, thread-like worms and is primarily transmitted to humans through the bite of an infected female Culex mosquito. Other mosquitoes, like Anopheles and Aedes, can also serve as vectors in certain regions. Kala-azar is transmitted by the sandfly, not the tsetse fly. Sleeping sickness is transmitted by the tsetse fly, not the sandfly. Taeniasis is acquired through eating infected meat, not by the housefly; houseflies can mechanically transmit diseases such as typhoid, cholera, and dysentery.","MEDIUM",False,"","VERIFIED","Source page image verifies the full stem, four options/order, marked answer C, complete explanation, and MEDIUM label. No PYQ label or exam name is shown."),
 ("Disease.pdf",9,"Which condition would NOT be classified as an acute disease?",["Rapid-onset infection lasting a few days","Chronic metabolic disorder","Short-duration viral fever","Sudden bacterial infection"],"B","Acute diseases have a rapid onset and short duration, often lasting a few days or weeks. Options A, C, and D describe short-duration conditions. A chronic metabolic disorder develops slowly and persists for a long time. The source's concluding answer sentence is clipped.","MEDIUM",False,"","NEEDS_REVIEW","Page image confirms question, all options/order, marked answer B, and MEDIUM label. The concluding explanation is clipped; excluded from import."),
 ("nutrition - science.pdf",2,"Jaundice is caused due to excess accumulation of ______ pigment.",["Hemoglobin","Bilirubin","Melanin","Keratin"],"B","Jaundice is caused by excess accumulation of bilirubin pigment. Bilirubin is a yellow-orange pigment produced during normal breakdown of red blood cells (hemoglobin). When the liver cannot efficiently process or excrete it, it builds up in the blood and tissues, causing yellowing of the skin and eyes. Jaundice is also known as hyperbilirubinemia. Hence, the correct answer is bilirubin.","MEDIUM",False,"","VERIFIED","Source image confirms exact stem, all options/order, answer B, complete explanation, and MEDIUM label. No PYQ label or exam name is shown."),
 ("nutrition - science.pdf",3,"Acquired diseases are:",["Present at birth","Developed during lifetime","Always genetic","Always non-communicable"],"B","Acquired diseases are not present at birth but are acquired during an individual's life. They may be communicable or non-communicable and develop after birth due to external factors such as pathogens, lifestyle choices, or environmental exposures. The source explanation continues with examples but is clipped.","MEDIUM",False,"","NEEDS_REVIEW","Page image confirms stem, four options/order, marked answer B, and MEDIUM label. The examples at the end of the explanation are clipped; excluded from import."),
 ("nutrition - science.pdf",4,"Which microorganism is responsible for causing malaria?",["Plasmodium vivax","Trypanosoma cruzi","Entamoeba histolytica","Giardia lamblia"],"A","Malaria is caused by protozoan parasites of the genus Plasmodium and is transmitted through bites from infected female Anopheles mosquitoes. Plasmodium falciparum is the deadliest species, while Plasmodium vivax is a common cause of malaria. The source continues with distractor explanations but is clipped.","MEDIUM",False,"","NEEDS_REVIEW","Source image confirms all options/order and marked answer A (Plasmodium vivax), but the explanation is clipped in the distractor discussion; excluded from import."),
 ("nutrition - science.pdf",5,"Which of the following diseases is primarily caused by pathogens?",["Hemophilia","Color blindness","Cholera","Down syndrome"],"C","Cholera is an infectious disease caused by the bacterium Vibrio cholerae, a pathogen. Hemophilia and color blindness are hereditary disorders, and Down syndrome is a genetic disorder caused by trisomy 21. Pathogens are microorganisms such as bacteria, viruses, or parasites that cause disease. Hence, the correct answer is cholera.","MEDIUM",False,"","VERIFIED","Source image confirms the complete question, four options/order, marked answer C, full explanation, and MEDIUM label."),
 ("nutrition - science.pdf",6,"Which of the following combinations is correct?",["Down syndrome - Pathogen","Typhoid - Genetic disorder","Influenza - Pathogen-based acquired disease","Hemophilia - Communicable disease"],"C","The source marks option C. Its explanation says Down syndrome is genetic rather than pathogen-caused, typhoid is a communicable bacterial disease rather than genetic, influenza is pathogen-based and acquired, and hemophilia is not communicable. The final hemophilia explanation is clipped.","MEDIUM",False,"","NEEDS_REVIEW","Page image confirms options/order and marked answer C. The explanation is clipped during the final distractor; excluded from import."),
 ("nutrition - science.pdf",7,"Assertion (A): Down syndrome is a congenital disease. Reason (R): It is caused due to chromosomal abnormality (Trisomy 21).",["Both A and R are true, and R is the correct explanation of A","Both A and R are true, but R is not the correct explanation of A","A is true, R is false","A is false, R is true"],"A","The assertion is true because Down syndrome is congenital and present from birth. The reason is true because Down syndrome is caused by a chromosomal abnormality, specifically trisomy 21. The source explanation ends while explaining whether the reason supports the assertion.","MEDIUM",False,"","NEEDS_REVIEW","Image verifies all four assertion-reason options/order and marked answer A. The final explanation is clipped; excluded from import."),
 ("nutrition - science.pdf",8,"Health is not merely the absence of ______ or infirmity.",["Infection","Disease","Weakness","Disability"],"B","The World Health Organization's 1948 Constitution defines health as a state of complete physical, mental, and social well-being, not merely the absence of disease or infirmity. The definition includes a positive, holistic state of well-being. Hence, the correct answer is disease.","MEDIUM",False,"","VERIFIED","Source image resolves the OCR blank and confirms four options/order, answer B, complete explanation, and MEDIUM label."),
 ("nutrition - science.pdf",9,"Acquired diseases can be further classified into ______ and non-communicable diseases.",["Hereditary","Genetic","Communicable","Congenital"],"C","Acquired diseases can be communicable or non-communicable. Acquired diseases develop after birth. Communicable diseases can pass between people or through environmental factors; non-communicable diseases do not spread between people and can develop from lifestyle, genetic, or environmental factors. Hence, the correct answer is communicable.","EASY",False,"","VERIFIED","Page image confirms exact stem, four options/order, marked answer C, complete explanation, and EASY label."),
 ("nutrition - science.pdf",10,"Which of the following is NOT a water-borne disease?",["Typhoid","Mumps","Hepatitis","Cholera"],"B","Mumps (also called parotitis) is a viral infection that affects the salivary glands and spreads through infected saliva. Typhoid spreads through contaminated water and food. Hepatitis is caused by viruses and damages the liver. The source explanation begins its cholera discussion but is clipped.","MEDIUM",True,"2019","NEEDS_REVIEW","Explicit PYQ 2019 and MEDIUM labels, four options/order, and marked answer B are visible. The explanation is clipped during the cholera discussion; excluded from import."),
 ("nutrition - science.pdf",11,"Which of the following is an example of a congenital disease?",["Typhoid","Cholera","Hemophilia","Tuberculosis"],"C","Hemophilia is a congenital disease.","EASY",False,"","VERIFIED","Page image confirms exact question, four options/order, marked answer C, complete explanation sentence, and EASY label."),
 ("nutrition - science.pdf",12,"Which of the following diseases is caused by a parasitic infection?",["Cholera","Influenza","Malaria","Tuberculosis"],"C","Malaria is caused by the Plasmodium parasite and transmitted to humans through bites of infected Anopheles mosquitoes. It affects red blood cells and can cause fever and flu-like illness. The source explanation starts comparing the other options but is clipped.","MEDIUM",False,"","NEEDS_REVIEW","Page image confirms all options/order and marked answer C. The explanation is clipped in the distractor discussion; excluded from import."),
 ("nutrition - science.pdf",13,"Congenital diseases are mainly caused due to:",["Pathogens","Lifestyle factors","Genetic/chromosomal disorders","Nutritional deficiency"],"C","Congenital diseases are primarily caused by genetic or chromosomal disorders. The source lists chromosomal abnormalities and single-gene defects, then discusses other factors, but the final explanation is clipped.","MEDIUM",False,"","NEEDS_REVIEW","Page image confirms all options/order and answer C. The explanation is clipped before its final discussion; excluded from import."),
 ("nutrition - science.pdf",14,"Which of the following is a mode of disease transmission?",["Contaminated food and water","Direct sunlight","Cold weather","Physical exercise"],"A","Contaminated food and water are a mode of indirect, vehicle-borne transmission. Pathogens can reach a healthy person through contaminated water or food. Examples include cholera, typhoid, diarrhea, dysentery, and botulism. The source explanation is clipped after “commonly transmitted through”.","MEDIUM",False,"","NEEDS_REVIEW","Image confirms answer A and all options/order. The explanation is clipped mid-sentence; excluded from import."),
 ("nutrition - science.pdf",15,"DPT vaccination is for protection against:",["Diarrhoea, pertussis, tetanus","Diarrhoea, polio, tetanus","Diphtheria, pertussis, tetanus","Diphtheria, polio, tetanus"],"C","DPT vaccination provides active immunity against diphtheria, pertussis (whooping cough), and tetanus. It is commonly administered to infants and young children in multiple doses. Diphtheria is a bacterial infection affecting the throat and nose; pertussis is a contagious respiratory infection; tetanus causes severe muscle spasms (lockjaw).","MEDIUM",False,"","VERIFIED","Page image confirms stem, options/order, marked answer C, complete explanation, and MEDIUM label."),
 ("nutrition - science.pdf",16,"Typhoid is caused by which kind of pathogens?",["Bacteria","Protozoa","Virus","Fungi"],"A","Typhoid is caused by bacteria. Typhoid fever is caused by Salmonella Typhi and is usually spread through contaminated food or water. The bacteria multiply and spread into the bloodstream. Salmonella Typhi is primarily found in humans and is not known to infect animals. Hence, the correct answer is bacteria.","EASY",False,"","VERIFIED","Page image confirms four options/order, marked answer A, complete explanation, and EASY label."),
 ("nutrition - science.pdf",17,"According to the WHO, health refers to:",["Absence of disease","Physical fitness","Complete physical, mental, and social well-being","Ability to work efficiently"],"C","The World Health Organization defines health as complete physical, mental, and social well-being and not merely the absence of disease or infirmity. This definition, adopted in the 1948 WHO Constitution, emphasizes a holistic concept rather than simply the lack of illness. The concluding answer text is clipped.","EASY",False,"","NEEDS_REVIEW","Page image resolves the OCR option ordering and confirms answer C. The concluding explanation is clipped at the page edge; excluded from import."),
 ("nutrition - science.pdf",18,"Which microorganism is responsible for causing pneumonia?",["Streptococcus pneumoniae","Mycobacterium tuberculosis","Escherichia coli","Salmonella enterica"],"A","Streptococcus pneumoniae (pneumococcus) is a common cause of pneumonia. It is one of the leading causes of bacterial pneumonia in humans. Mycobacterium tuberculosis is associated with tuberculosis, while Escherichia coli and Salmonella enterica are linked to other infections. Hence, the correct answer is Streptococcus pneumoniae.","EASY",False,"","VERIFIED","Page image confirms answer A, all options/order, complete explanation, and EASY label. Earlier it was rejected only as out of Respiratory System scope; its disease mapping is verified here."),
 ("nutrition - science.pdf",19,"Tetanus is a serious disease of the nervous system caused by a toxin-producing:",["Protist","Fungus","Parasite","Bacterium"],"D","Tetanus is caused by Clostridium tetani, commonly found in soil, dust, and animal feces. It is anaerobic and thrives in environments with little or no oxygen. The bacteria can enter through a deep puncture wound. Symptoms include lockjaw, stiff neck, difficulty swallowing, rigid abdominal muscles, and painful muscle spasms lasting for minutes.","MEDIUM",True,"2022","VERIFIED","Explicit MEDIUM and PYQ 2022 labels, four options/order, marked answer D, and complete explanation verified. No exam name is shown."),
 ("nutrition - science.pdf",20,"Bronchitis is defined as:",["Infection of alveoli causing fluid accumulation","Swelling in bronchi and bronchioles","Damage to lung tissues due to pollution","Narrowing of trachea only"],"B","","MEDIUM",False,"","NEEDS_REVIEW","Page image confirms question, four options/order, and marked answer B. The source page has no explanation; excluded from import."),
 ("nutrition - science.pdf",21,"Which of the following statements about Pertussis (Whooping cough) is correct?",["It is caused by Streptococcus species and mainly affects adults","It is caused by Bordetella pertussis and produces loud coughing sounds, especially at night in infants","It is a viral disease affecting only lungs without cough","It causes swelling in bronchi and bronchioles only"],"B","Pertussis (whooping cough) is a bacterial infection caused by Bordetella pertussis. It is characterized by severe coughing spells (paroxysms) that can end with a high-pitched “whoop” sound. It is highly contagious and can be fatal to infants, who often exhibit a worse cough at night.","MEDIUM",False,"","VERIFIED","Source image confirms all four options/order, answer B, complete explanation, and MEDIUM label. Earlier it was rejected only as out of Respiratory System scope; its disease mapping is verified here."),
]

REVIEW_HEADER = ["source_pdf","source_page","subject_slug","subcategory_slug","chapter_slug","catalog_chapter_id","question_text","option_a","option_b","option_c","option_d","proposed_correct_option","explanation","difficulty","is_pyq","pyq_year","pyq_exam_name","review_status","import_eligible","review_note"]
IMPORT_HEADER = ["subject_slug","subcategory_slug","chapter_slug","question_text","option_a","option_b","option_c","option_d","correct_option","explanation","difficulty","is_pyq","pyq_year","pyq_exam_name","source"]

GLANDS_PAGES = [2,3,8,10,11,12,13,14,16,17,18,19,20,21]

def write_csv(path: Path, header: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)

def main() -> None:
    queue_path = ROOT / "SCIENCE_OCR_REVIEW_QUEUE.csv"
    with queue_path.open(encoding="utf-8-sig", newline="") as stream:
        queue = list(csv.DictReader(stream)); queue_header = list(queue[0])
    queue_by_key = {(r["source_pdf"],r["source_page"]):r for r in queue}
    review_rows = []
    for source, page, stem, options, answer, explanation, difficulty, pyq, year, status, note in ROWS:
        if status == "NEEDS_REVIEW":
            # Keep only the OCR-captured partial text for unresolved explanations;
            # never reconstruct the portion clipped from the original page.
            explanation = queue_by_key[(source,str(page))]["explanation_ocr"].strip()
        review_rows.append(dict(zip(REVIEW_HEADER, [source,str(page),"gk-gs","science",DISEASE,DISEASE_ID,stem,*options,answer,explanation,difficulty,str(pyq).lower(),year,"",status,str(status=="VERIFIED").lower(),note])))
    eligible = [r for r in review_rows if r["import_eligible"] == "true"]
    review_dir = ROOT / "review-datasets" / DISEASE
    batch_dir = ROOT / "by-chapter" / DISEASE
    write_csv(review_dir / "disease_review.csv", REVIEW_HEADER, review_rows)
    for pyq in (False, True):
        batch = []
        for r in eligible:
            if (r["is_pyq"] == "true") != pyq:
                continue
            batch.append({"subject_slug":"gk-gs","subcategory_slug":"science","chapter_slug":DISEASE,"question_text":r["question_text"],"option_a":r["option_a"],"option_b":r["option_b"],"option_c":r["option_c"],"option_d":r["option_d"],"correct_option":r["proposed_correct_option"],"explanation":r["explanation"],"difficulty":r["difficulty"],"is_pyq":r["is_pyq"],"pyq_year":r["pyq_year"],"pyq_exam_name":"","source":f"{r['source_pdf']} p. {r['source_page']}"})
        write_csv(batch_dir / f"disease_{'pyq' if pyq else 'ordinary'}.csv", IMPORT_HEADER, batch)

    # Update current queue disposition for this chapter only. Earlier chapter
    # decisions remain in SCIENCE_REVIEW_DECISIONS and their review datasets.
    by_source_page = {(r["source_pdf"],r["source_page"]):r for r in review_rows}
    for q in queue:
        key=(q["source_pdf"],q["source_page"])
        if key in by_source_page:
            r=by_source_page[key]
            q["chapter_slug"]=DISEASE; q["review_status"]=r["review_status"]; q["review_note"]=r["review_note"]
        elif q["source_pdf"]=="Disease.pdf" and int(q["source_page"]) in GLANDS_PAGES:
            q["chapter_slug"]=GLANDS; q["review_status"]="NEEDS_REVIEW"
            q["review_note"]=f"Page image topic mapped to the existing Glands chapter (catalog ID {GLANDS_ID}, slug glands), not Disease. Full Glands chapter review/import preparation remains pending."
        # Disease.pdf p. 15 is intentionally retained as its existing Brain
        # & Nervous System pending record.
    write_csv(queue_path,queue_header,queue)

    decisions_path=ROOT/"SCIENCE_REVIEW_DECISIONS.csv"
    with decisions_path.open(encoding="utf-8-sig",newline="") as stream:
        decisions=list(csv.DictReader(stream)); decision_header=list(decisions[0])
    existing={(r["source_pdf"],r["source_page"],r["chapter_slug"],r["review_status"]) for r in decisions}
    additions=[]
    for r in review_rows:
        key=(r["source_pdf"],r["source_page"],DISEASE,r["review_status"])
        if key not in existing:
            additions.append({"source_pdf":r["source_pdf"],"source_page":r["source_page"],"chapter_slug":DISEASE,"review_status":r["review_status"],"review_note":r["review_note"]})
            existing.add(key)
    for page in GLANDS_PAGES:
        note=f"Question content mapped to existing Glands chapter (catalog ID {GLANDS_ID}, slug glands). This Disease review did not prepare a Glands import batch; question-level Glands validation is pending."
        key=("Disease.pdf",str(page),GLANDS,"NEEDS_REVIEW")
        if key not in existing:
            additions.append({"source_pdf":"Disease.pdf","source_page":str(page),"chapter_slug":GLANDS,"review_status":"NEEDS_REVIEW","review_note":note})
            existing.add(key)
    write_csv(decisions_path,decision_header,decisions+additions)

    report = """# Disease Chapter Review

- Existing catalog chapter: **Disease** (`disease`), ID `79eeb111-c0df-4863-aac2-94086844f83b`, confirmed under `gk-gs/science`. No catalog changes were made.
- `Disease.pdf` pages 2–21 were inspected against page images and OCR. Five pages (4–7, 9) contain Disease questions; fourteen (2, 3, 8, 10–14, 16–21) contain Glands questions and were mapped to existing Glands (`glands`, ID `3a7d5736-5a65-434b-8c2c-0f17905bab57`); page 15 asks about the brain and remains in its previously recorded Brain & Nervous System review.
- All 20 question pages of `nutrition - science.pdf` were inspected; each contains a Disease/health question and was reviewed for this batch.
- Searches of the remaining OCR transcripts found only incidental disease mentions within questions mapped to other chapters (for example stomach acid/bacteria, bacterial cell structure, and Plasmodium reproduction). No other confidently mappable Disease question was added.
- Exam names are not visible in the reviewed source pages and were not inferred.

## Disposition by difficulty and question type

| Difficulty | Type | Verified | Needs review | Rejected | Duplicate |
|---|---|---:|---:|---:|---:|
| EASY | Ordinary | 4 | 1 | 0 | 0 |
| MEDIUM | Ordinary | 6 | 12 | 0 | 0 |
| HARD | Ordinary | 0 | 0 | 0 | 0 |
| EASY | PYQ | 0 | 0 | 0 | 0 |
| MEDIUM | PYQ | 1 | 1 | 0 | 0 |
| HARD | PYQ | 0 | 0 | 0 | 0 |

- Verified/import-ready: **11** (10 ordinary, 1 PYQ).
- Needs review: **14** (13 ordinary, 1 PYQ). Pending rows have clipped explanations or, for Nutrition p. 20, no source explanation.
- Rejected: **0**. Confirmed duplicates: **0**. Similar/related questions were compared by full stem, options, and answer rather than marked duplicate from keyword similarity alone.

## Ordinary-question coverage targets

| Difficulty | Verified ordinary | Target | Remaining |
|---|---:|---:|---:|
| EASY | 4 | 25 | 21 |
| MEDIUM | 6 | 25 | 19 |
| HARD | 0 | 25 | 25 |

PYQs are tracked separately and do not count toward the ordinary targets. Difficulty labels are internal review metadata; Science users are not asked to choose a difficulty.

## Import readiness and source traceability

Only fully verified, nonduplicate Disease records with complete source explanations are included in the ordinary/PYQ CSVs. Each row preserves source filename and physical PDF page. The PYQ CSV contains the one verified source-labeled item (Nutrition p. 19, PYQ 2022); no exam name is shown.

## Validation

Isolated importer dry-run tests validate all 11 eligible rows, assert zero inserted rows, and confirm the test database remains empty. Production database access was read-only; no production import or modification was performed.
"""
    (review_dir/"disease_review_report.md").write_text(report,encoding="utf-8")

if __name__ == "__main__":
    main()
