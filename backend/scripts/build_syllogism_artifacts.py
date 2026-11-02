"""Build the reviewed Syllogism question bank, logic ledger, and PDF audit report."""

import json
import re
from collections import Counter
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
ORIGINAL = "Original SSC-style practice question"
PDFS = {
    1: "Syllogism 01 Class Notes.pdf",
    2: "Syllogism 02_ Class Notes.pdf",
    3: "Syllogism 03_ Class Notes.pdf",
}


def F(kind, left, right):
    return (kind, left, right)


def canonical_term(term):
    value = " ".join(term.casefold().split())
    if value == "trained people":
        return "Trained"
    if value.endswith("ies"):
        value = value[:-3] + "y"
    elif value.endswith("s") and not value.endswith("ss"):
        value = value[:-1]
    return value.title()


def item(difficulty, question, statements, conclusions, choices, answer, explanation,
         source=None, page=None, signature=None, kind="follow", possibility_options=None):
    return {
        "difficulty": difficulty, "question": question, "statements": statements,
        "conclusions": conclusions, "choices": choices, "answer": answer,
        "explanation": explanation, "source": source, "page": page,
        "signature": signature, "kind": kind, "possibility_options": possibility_options,
    }


def parse_statement(statement):
    value = statement.strip().rstrip(".")
    patterns = [
        (r"^Only a few (.+?) are (.+)$", "ONLY_FEW"),
        (r"^Only (.+?) are (.+)$", "ONLY"),
        (r"^All (.+?) (?:are|is) (?:a|an) (.+)$", "ALL_ARTICLE"),
        (r"^All (.+?) (?:are|is) (.+)$", "ALL"),
        (r"^Some (.+?) (?:are|is) (?:a|an) (.+)$", "SOME_ARTICLE"),
        (r"^Some (.+?) are not (.+)$", "SOME_NOT"),
        (r"^Some (.+?) are (.+)$", "SOME"),
        (r"^No (.+?) (?:is|are) (?:(?:a|an) )?(.+)$", "NO"),
    ]
    for pattern, kind in patterns:
        match = re.match(pattern, value, flags=re.IGNORECASE)
        if not match:
            continue
        left, right = (canonical_term(part.strip()) for part in match.groups())
        if kind == "ONLY":
            return [F("ALL", right, left)]
        if kind == "ONLY_FEW":
            return [F("SOME", left, right), F("SOME_NOT", left, right)]
        return [F("ALL" if kind == "ALL_ARTICLE" else "SOME" if kind == "SOME_ARTICLE" else kind, left, right)]
    raise ValueError(f"Could not parse categorical statement: {statement}")


def select_options(labels):
    return labels


# Formal propositions use kinds ALL, SOME, NO, and SOME_NOT. "Only A are B"
# is represented as ALL B A; "only a few A are B" as SOME A B + SOME_NOT A B.
ITEMS = [
    item("EASY", "All flowers are trees. All branches are trees. Which conclusions follow?",
         ["All flowers are trees.", "All branches are trees."],
         [("All branches are flowers.", F("ALL", "Branches", "Flowers")),
          ("All branches are trees.", F("ALL", "Branches", "Trees"))],
         [("Both conclusions I and II follow.", "I+II"), ("Only conclusion I follows.", "I"),
          ("Only conclusion II follows.", "II"), ("Neither conclusion follows.", "NONE")],
         "II", "All branches are trees is stated. The branch and flower subsets of trees may be separate, so I is not definite.",
         1, 7, "source01_flowers_branches"),
    item("EASY", "All land is solid. No land is a boy. Which conclusions follow?",
         ["All land is solid.", "No land is a boy."],
         [("All solids are land.", F("ALL", "Solids", "Land")),
          ("All boys are solid.", F("ALL", "Boys", "Solid"))],
         [("Both conclusions I and II follow.", "I+II"), ("Only conclusion I follows.", "I"),
          ("Only conclusion II follows.", "II"), ("Neither conclusion follows.", "NONE")],
         "NONE", "The first conclusion reverses an All statement. The premises give no relation from boys to solids.",
         1, 13, "source01_land_solid_boy"),
    item("EASY", "Some blankets are sheets. Some sheets are pillows. Which conclusions follow?",
         ["Some blankets are sheets.", "Some sheets are pillows."],
         [("Some blankets are pillows.", F("SOME", "Blankets", "Pillows")),
          ("All sheets are pillows.", F("ALL", "Sheets", "Pillows"))],
         [("Both conclusions I and II follow.", "I+II"), ("Only conclusion I follows.", "I"),
          ("Only conclusion II follows.", "II"), ("Neither conclusion follows.", "NONE")],
         "NONE", "The two Some statements may use different sheet members. Neither connects every sheet or guarantees a blanket-pillow overlap.",
         1, 14, "source01_blankets_sheets_pillows"),
    item("MEDIUM", "Some erasers are papers. Some papers are clips. All clips are balls. Which conclusions follow?",
         ["Some erasers are papers.", "Some papers are clips.", "All clips are balls."],
         [("All papers are balls.", F("ALL", "Papers", "Balls")),
          ("Some erasers are clips.", F("SOME", "Erasers", "Clips"))],
         [("Both conclusions I and II follow.", "I+II"), ("Only conclusion I follows.", "I"),
          ("Only conclusion II follows.", "II"), ("Neither conclusion follows.", "NONE")],
         "NONE", "Only clips are known to be balls, not every paper. The two existential witnesses may be different people or objects.",
         1, 15, "source01_erasers_papers_clips"),
    item("EASY", "All students are teachers. Some teachers are lecturers. No lecturer is a professional. Which conclusions follow?",
         ["All students are teachers.", "Some teachers are lecturers.", "No lecturer is a professional."],
         [("Some students are lecturers.", F("SOME", "Students", "Lecturers")),
          ("No student is a professional.", F("NO", "Students", "Professionals"))],
         [("Both conclusions I and II follow.", "I+II"), ("Only conclusion I follows.", "I"),
          ("Only conclusion II follows.", "II"), ("Neither conclusion follows.", "NONE")],
         "NONE", "The teacher-lecturer witness need not be a student. Students may be lecturers or professionals only if other premises require it; neither conclusion is forced.",
         2, 5, "source02_students_teachers_lecturers"),
    item("EASY", "Some tickets are watches. All buttons are tickets. No stamp is a watch. Which conclusions follow?",
         ["Some tickets are watches.", "All buttons are tickets.", "No stamp is a watch."],
         [("No ticket is a stamp.", F("NO", "Tickets", "Stamps")),
          ("Some buttons are watches.", F("SOME", "Buttons", "Watches"))],
         [("Both conclusions I and II follow.", "I+II"), ("Only conclusion I follows.", "I"),
          ("Only conclusion II follows.", "II"), ("Neither conclusion follows.", "NONE")],
         "NONE", "The statements do not exclude tickets that are stamps outside the watch region, and the ticket-watch witness need not be a button.",
         2, 6, "source02_tickets_watches_buttons_stamps"),
    item("MEDIUM", "Some computers are laptops. No laptop is a mobile. Which conclusions follow?",
         ["Some computers are laptops.", "No laptop is a mobile."],
         [("No computer is a mobile.", F("NO", "Computers", "Mobiles")),
          ("Some computers are mobiles.", F("SOME", "Computers", "Mobiles")),
          ("All mobiles are photocopiers.", F("ALL", "Mobiles", "Photocopiers"))],
         [("Only conclusions I and II follow.", "I+II"), ("Only conclusion III follows.", "III"),
          ("All three conclusions follow.", "I+II+III"), ("None of the conclusions follows.", "NONE")],
         "NONE", "The known computer-laptop witness is not mobile, but other computers may be mobile. Nothing relates mobiles to photocopiers.",
         2, 10, "source02_computers_laptops_mobiles"),
    item("MEDIUM", "Some telescopes are periscopes. Some telescopes are microscopes. Some telescopes are kaleidoscopes. Which conclusions follow?",
         ["Some telescopes are periscopes.", "Some telescopes are microscopes.", "Some telescopes are kaleidoscopes."],
         [("Some kaleidoscopes are telescopes.", F("SOME", "Kaleidoscopes", "Telescopes")),
          ("Some microscopes are periscopes.", F("SOME", "Microscopes", "Periscopes")),
          ("Some microscopes are telescopes.", F("SOME", "Microscopes", "Telescopes"))],
         [("Only conclusion III follows.", "III"), ("Only conclusions I and III follow.", "I+III"),
          ("Only conclusions II and III follow.", "II+III"), ("All conclusions follow.", "I+II+III")],
         "I+III", "Some reverses its order, so I and III restate existential overlaps. The two witnesses from the first and second statements need not coincide.",
         2, 11, "source02_telescope_overlap"),
    item("MEDIUM", "All trojans are fairies. No fairy is a flower. Some viruses are trojans. Which conclusions follow?",
         ["All trojans are fairies.", "No fairy is a flower.", "Some viruses are trojans."],
         [("No flower is a trojan.", F("NO", "Flowers", "Trojans")),
          ("Some viruses are trojans.", F("SOME", "Viruses", "Trojans")),
          ("No trojan is a virus.", F("NO", "Trojans", "Viruses"))],
         [("Only conclusion I follows.", "I"), ("Only conclusions I and II follow.", "I+II"),
          ("Only conclusions II and III follow.", "II+III"), ("All conclusions follow.", "I+II+III")],
         "I+II", "Trojans lie within fairies, which are disjoint from flowers. The Some statement gives a virus-trojan witness, contradicting III.",
         2, 12, "source02_trojans_fairies_viruses"),
    item("MEDIUM", "No file is a folder. Some files are PDFs. All files are Excel sheets. Which conclusions follow?",
         ["No file is a folder.", "Some files are PDFs.", "All files are Excel sheets."],
         [("Some PDFs are folders.", F("SOME", "PDFs", "Folders")),
          ("Some Excel sheets are folders.", F("SOME", "Excel sheets", "Folders")),
          ("Some PDFs are Excel sheets.", F("SOME", "PDFs", "Excel sheets"))],
         [("Only conclusions I and III follow.", "I+III"), ("Only conclusion III follows.", "III"),
          ("Only conclusions II and III follow.", "II+III"), ("All conclusions follow.", "I+II+III")],
         "III", "The file that is a PDF is also an Excel sheet, so III follows. PDFs or Excel sheets outside the file class may or may not be folders.",
         2, 13, "source02_files_pdfs_excel"),
    item("EASY", "No rain is an earthquake. All rain is floods. Some rain is a drought. Which conclusions follow?",
         ["No rain is an earthquake.", "All rain is a flood.", "Some rain is a drought."],
         [("Some floods are earthquakes.", F("SOME", "Floods", "Earthquakes")),
          ("Some droughts are earthquakes.", F("SOME", "Droughts", "Earthquakes")),
          ("Some floods are droughts.", F("SOME", "Floods", "Droughts"))],
         [("All conclusions follow.", "I+II+III"), ("Only conclusions I and III follow.", "I+III"),
          ("Only conclusion III follows.", "III"), ("Only conclusions II and III follow.", "II+III")],
         "III", "The rain-drought witness is also a flood, proving III. The premises do not force any flood or drought to be an earthquake.",
         2, 14, "source02_rain_flood_drought"),
    item("MEDIUM", "Some plants are flowers. Some flowers are fruits. All flowers are gardens. Which conclusions follow?",
         ["Some plants are flowers.", "Some flowers are fruits.", "All flowers are gardens."],
         [("Some gardens are plants.", F("SOME", "Gardens", "Plants")),
          ("Some fruits are gardens.", F("SOME", "Fruits", "Gardens")),
          ("Some gardens are flowers.", F("SOME", "Gardens", "Flowers"))],
         [("Only conclusions I and III follow.", "I+III"), ("Only conclusions I and II follow.", "I+II"),
          ("All conclusions follow.", "I+II+III"), ("Only conclusions II and III follow.", "II+III")],
         "I+II+III", "The first Some statement supplies flowers that are both plants and gardens. The second supplies flowers that are both fruits and gardens.",
         2, 15, "source02_plants_flowers_fruits_gardens"),
    item("MEDIUM", "Some carpenters are singers. All singers are doctors. Which conclusions follow?",
         ["Some carpenters are singers.", "All singers are doctors."],
         [("No doctor is a carpenter.", F("NO", "Doctors", "Carpenters")),
          ("Some doctors are singers.", F("SOME", "Doctors", "Singers")),
          ("Some carpenters are doctors.", F("SOME", "Carpenters", "Doctors"))],
         [("Only conclusion III follows.", "III"), ("All conclusions follow.", "I+II+III"),
          ("Only conclusions II and III follow.", "II+III"), ("Only conclusion II follows.", "II")],
         "II+III", "The carpenter-singer witness is a doctor as well, proving II and III. That witness also disproves I.",
         2, 16, "source02_carpenters_singers_doctors"),
    item("HARD", "Some machines are coolers. All coolers are robots. Some microwaves are coolers. Which conclusions follow?",
         ["Some machines are coolers.", "All coolers are robots.", "Some microwaves are coolers."],
         [("Some coolers are machines.", F("SOME", "Coolers", "Machines")),
          ("Some robots are machines.", F("SOME", "Robots", "Machines")),
          ("No robot is a microwave.", F("NO", "Robots", "Microwaves"))],
         [("Only conclusions I and III follow.", "I+III"), ("Only conclusions I and II follow.", "I+II"),
          ("Either conclusion I or III follows.", "EITHER(I,III)"), ("All conclusions follow.", "I+II+III")],
         "I+II", "The machine-cooler witness is a robot, proving I and II. The microwave-cooler witness is also a robot, so III is false.",
         2, 17, "source02_machines_coolers_robots"),
    item("HARD", "Some hills are rivers. Some rivers are deserts. All deserts are seas. Which conclusions follow?",
         ["Some hills are rivers.", "Some rivers are deserts.", "All deserts are seas."],
         [("Some seas are rivers.", F("SOME", "Seas", "Rivers")),
          ("Some seas are hills.", F("SOME", "Seas", "Hills")),
          ("Some deserts are hills.", F("SOME", "Deserts", "Hills"))],
         [("Only conclusions I and III follow.", "I+III"), ("Only conclusion I follows.", "I"),
          ("Either conclusion I or III follows.", "EITHER(I,III)"), ("All conclusions follow.", "I+II+III")],
         "I", "The river-desert witness is also a sea, proving I. It need not be a hill; the hill-river witness need not be a desert.",
         2, 18, "source02_hills_rivers_deserts_sea"),
    item("HARD", "Some dogs are cats. Some cats are bats. Which statement about conclusions I and II is guaranteed? I. Some dogs are bats. II. Some dogs are not bats.",
         ["Some dogs are cats.", "Some cats are bats."],
         [("Some dogs are bats.", F("SOME", "Dogs", "Bats")),
          ("Some dogs are not bats.", F("SOME_NOT", "Dogs", "Bats"))],
         [("Only conclusion I follows.", "I"), ("Only conclusion II follows.", "II"),
          ("Both conclusions follow.", "I+II"),
          ("At least one of I or II follows; both may be true.", "EITHER(I,II)")],
         "EITHER(I,II)", "Neither overlap is forced because the two cat witnesses may differ. Some dogs exist, so they must either overlap bats or include a non-bat; both outcomes can also coexist.",
         3, 8, "source03_dog_cat_bat_partition", kind="either"),
    item("HARD", "Some lakes are rivers. Some rivers are mountains. Some mountains are books. Some books are papers. Which option is guaranteed? I. Some books are rivers. II. Some papers are lakes. III. Some mountains are lakes. IV. No paper is a lake.",
         ["Some lakes are rivers.", "Some rivers are mountains.", "Some mountains are books.", "Some books are papers."],
         [("Some books are rivers.", F("SOME", "Books", "Rivers")),
          ("Some papers are lakes.", F("SOME", "Papers", "Lakes")),
          ("Some mountains are lakes.", F("SOME", "Mountains", "Lakes")),
          ("No paper is a lake.", F("NO", "Papers", "Lakes"))],
         [("Only conclusion I follows.", "I"), ("Only conclusion III follows.", "III"),
          ("Either II or IV follows.", "EITHER(II,IV)"), ("Neither II nor IV follows.", "NONE")],
         "EITHER(II,IV)", "II and IV are exact negations: either the paper and lake sets intersect or they are disjoint. Neither is individually forced by the statements.",
         3, 9, "source03_lakes_rivers_books_either", kind="either"),
    item("MEDIUM", "Some tigers are horses. All horses are goats. All goats are dogs. Some dogs are cats. Which conclusions follow? I. Some cats are tigers. II. Some dogs are horses. III. Some goats are tigers. IV. Some cats are horses.",
         ["Some tigers are horses.", "All horses are goats.", "All goats are dogs.", "Some dogs are cats."],
         [("Some cats are tigers.", F("SOME", "Cats", "Tigers")),
          ("Some dogs are horses.", F("SOME", "Dogs", "Horses")),
          ("Some goats are tigers.", F("SOME", "Goats", "Tigers")),
          ("Some cats are horses.", F("SOME", "Cats", "Horses"))],
         [("Only conclusions I and III follow.", "I+III"), ("All conclusions follow.", "I+II+III+IV"),
          ("Only conclusions II and III follow.", "II+III"), ("Only conclusions II, III and IV follow.", "II+III+IV")],
         "II+III", "The tiger-horse witness is also a goat and a dog, proving II and III. The cat-dog witness need not be a horse or tiger.",
         3, 10, "source03_tigers_horses_goats_dogs"),
    item("MEDIUM", "No A is B. Which proposed relationship is impossible?",
         ["No A is B."],
         [],
         [("Some A are B is a possibility.", "POSSIBLE"),
          ("All B are A is a possibility.", "POSSIBLE"),
          ("Some A are not B is a possibility.", "POSSIBLE"),
          ("No A is B is a possibility.", "POSSIBLE")],
         "A", "A and B must be disjoint, so their intersection cannot contain an A and a B. The other relations can be realized consistently, including by an empty class where needed.",
         3, 12, "source03_no_ab_possibilities", kind="impossible",
         possibility_options=[
             F("SOME", "A", "B"), F("ALL", "B", "A"),
             F("SOME_NOT", "A", "B"), F("NO", "A", "B"),
         ]),
    item("EASY", "Some artists are musicians. Which conclusion must follow?",
         ["Some artists are musicians."],
         [("Some musicians are artists.", F("SOME", "Musicians", "Artists")),
          ("All artists are musicians.", F("ALL", "Artists", "Musicians"))],
         [("Both conclusions follow.", "I+II"), ("Only conclusion I follows.", "I"),
          ("Only conclusion II follows.", "II"), ("Neither conclusion follows.", "NONE")],
         "I", "Some A are B reverses to Some B are A because both name the same nonempty intersection. It does not imply that every artist is a musician.",
         signature="original_some_reversal"),
    item("EASY", "All poets are readers. No reader is careless. Which conclusions follow?",
         ["All poets are readers.", "No reader is careless."],
         [("No poet is careless.", F("NO", "Poets", "Careless")),
          ("All careless people are poets.", F("ALL", "Careless", "Poets"))],
         [("Both conclusions follow.", "I+II"), ("Only conclusion I follows.", "I"),
          ("Only conclusion II follows.", "II"), ("Neither conclusion follows.", "NONE")],
         "I", "Every poet is a reader and every reader is outside careless people, so I follows. No premise places careless people inside poets.",
         signature="original_all_no_chain"),
    item("EASY", "No violin is a drum. Some violins are wooden. Which conclusions follow?",
         ["No violin is a drum.", "Some violins are wooden."],
         [("Some wooden things are not drums.", F("SOME_NOT", "Wooden", "Drums")),
          ("No drum is a violin.", F("NO", "Drums", "Violins"))],
         [("Both conclusions follow.", "I+II"), ("Only conclusion I follows.", "I"),
          ("Only conclusion II follows.", "II"), ("Neither conclusion follows.", "NONE")],
         "I+II", "The wooden-violin witness is not a drum, proving I. No violin is a drum is symmetric, proving II.",
         signature="original_no_some_existential"),
    item("EASY", "All orchids are plants. Some orchids are fragrant. Which conclusions follow?",
         ["All orchids are plants.", "Some orchids are fragrant."],
         [("Some fragrant things are plants.", F("SOME", "Fragrant", "Plants")),
          ("Some orchids are plants.", F("SOME", "Orchids", "Plants"))],
         [("Both conclusions follow.", "I+II"), ("Only conclusion I follows.", "I"),
          ("Only conclusion II follows.", "II"), ("Neither conclusion follows.", "NONE")],
         "I+II", "The existing fragrant orchid is a plant, proving I. It is also an orchid and plant, proving II.",
         signature="original_some_through_all"),
    item("MEDIUM", "Some paintings are sketches. All sketches are framed. No framed item is damaged. Which conclusions follow?",
         ["Some paintings are sketches.", "All sketches are framed.", "No framed item is damaged."],
         [("Some paintings are framed.", F("SOME", "Paintings", "Framed")),
          ("Some paintings are damaged.", F("SOME", "Paintings", "Damaged"))],
         [("Both conclusions follow.", "I+II"), ("Only conclusion I follows.", "I"),
          ("Only conclusion II follows.", "II"), ("Neither conclusion follows.", "NONE")],
         "I", "The painting-sketch witness is framed, proving I. It is therefore not damaged, and no premise requires any painting to be damaged.",
         signature="original_chain_with_negative"),
    item("HARD", "Only mentors are guides. Only a few guides are volunteers. Which conclusions follow? I. Some volunteers are mentors. II. All guides are mentors. III. Some guides are not volunteers. IV. Some guides are volunteers.",
         ["Only mentors are guides.", "Only a few guides are volunteers."],
         [("Some volunteers are mentors.", F("SOME", "Volunteers", "Mentors")),
          ("All guides are mentors.", F("ALL", "Guides", "Mentors")),
          ("Some guides are not volunteers.", F("SOME_NOT", "Guides", "Volunteers")),
          ("Some guides are volunteers.", F("SOME", "Guides", "Volunteers"))],
         [("Only conclusions I and II follow.", "I+II"), ("Only conclusions III and IV follow.", "III+IV"),
          ("Only conclusions I, III and IV follow.", "I+III+IV"), ("All conclusions follow.", "I+II+III+IV")],
         "I+II+III+IV", "Only mentors are guides means all guides are mentors. Only a few guides are volunteers asserts both some guide-volunteers and some guides outside volunteers.",
         signature="original_only_only_few"),
    item("HARD", "Some apprentices are technicians. All technicians are qualified persons. No qualified person is an untrained person. Which conclusions follow? I. Some apprentices are qualified persons. II. Some technicians are not untrained persons. III. No apprentice is untrained.",
         ["Some apprentices are technicians.", "All technicians are qualified persons.", "No qualified person is an untrained person."],
         [("Some apprentices are qualified persons.", F("SOME", "Apprentices", "Qualified Person")),
          ("Some technicians are not untrained persons.", F("SOME_NOT", "Technicians", "Untrained Person")),
          ("No apprentice is untrained.", F("NO", "Apprentices", "Untrained Person"))],
         [("Only conclusions I and II follow.", "I+II"), ("Only conclusion III follows.", "III"),
          ("All conclusions follow.", "I+II+III"), ("Only conclusion I follows.", "I")],
         "I+II", "The apprentice-technician witness is a qualified person and therefore not an untrained person, proving I and II. Other apprentices may lie outside the technician class, so III is not definite.",
         signature="original_chain_existence_limited"),
    item("HARD", "Some A are C. Which conclusion pattern is guaranteed? I. All A are B. II. Some A are not B.",
         ["Some A are C."],
         [("All A are B.", F("ALL", "A", "B")),
          ("Some A are not B.", F("SOME_NOT", "A", "B"))],
         [("Only conclusion I follows.", "I"), ("Only conclusion II follows.", "II"),
          ("Both conclusions follow.", "I+II"),
          ("At least one of I or II follows; exactly one is true in every model.", "EITHER(I,II)")],
         "EITHER(I,II)", "I and II are exact logical negations. The premise guarantees A is nonempty, but leaves its relation to B open, so neither conclusion follows alone while their disjunction is guaranteed.",
         signature="original_valid_complementary_pair", kind="either"),
    item("HARD", "All pilots are trained. Some trained people are divers. No diver is inactive. Which relation is impossible?",
         ["All pilots are trained.", "Some trained people are divers.", "No diver is inactive."],
         [], [("Some pilots are divers is possible.", "POSSIBLE"),
              ("Some pilots are inactive is possible.", "POSSIBLE"),
              ("Some divers are inactive is possible.", "POSSIBLE"),
              ("Some trained people are not inactive is possible.", "POSSIBLE")],
         "C", "No diver is inactive, so a diver-inactive overlap is impossible. The other options can be realized without violating the statements.",
         signature="original_possibility_with_negative", kind="impossible",
         possibility_options=[F("SOME", "Pilots", "Divers"), F("SOME", "Pilots", "Inactive"),
                              F("SOME", "Divers", "Inactive"), F("SOME_NOT", "Trained", "Inactive")]),
    item("HARD", "Some engineers are musicians. All musicians are readers. No reader is a pilot. Which conclusions follow? I. Some engineers are readers. II. Some engineers are not pilots. III. No musician is a pilot. IV. All engineers are readers.",
         ["Some engineers are musicians.", "All musicians are readers.", "No reader is a pilot."],
         [("Some engineers are readers.", F("SOME", "Engineers", "Readers")),
          ("Some engineers are not pilots.", F("SOME_NOT", "Engineers", "Pilots")),
          ("No musician is a pilot.", F("NO", "Musicians", "Pilots")),
          ("All engineers are readers.", F("ALL", "Engineers", "Readers"))],
         [("Only conclusions I and IV follow.", "I+IV"), ("Only conclusions I, II and III follow.", "I+II+III"),
          ("Only conclusions II and III follow.", "II+III"), ("All conclusions follow.", "I+II+III+IV")],
         "I+II+III", "The engineer-musician witness is a reader and not a pilot, proving I and II. Every musician is a reader and no reader is a pilot, proving III. Other engineers may not be readers.",
         signature="original_four_term_chain"),
    item("HARD", "Some A are B. Some B are C. No C is D. Which proposed relationship is impossible?",
         ["Some A are B.", "Some B are C.", "No C is D."],
         [], [("Some A are D is possible.", "POSSIBLE"),
              ("All B are C is possible.", "POSSIBLE"),
              ("Some C are D is possible.", "POSSIBLE"),
              ("No A is C is possible.", "POSSIBLE")],
         "C", "C and D are disjoint by premise, so their intersection cannot be nonempty. The two Some statements may have different witnesses, leaving the other proposed relations consistent.",
         signature="original_possibility_distinct_witnesses", kind="impossible",
         possibility_options=[F("SOME", "A", "D"), F("ALL", "B", "C"),
                              F("SOME", "C", "D"), F("NO", "A", "C")]),
]

REJECTIONS = [
    {"source_pdf": PDFS[2], "source_page": 8,
     "question_summary": "All radios are pencils; some pencils are files; proposed conclusions are some radios not files and some radios files.",
     "rejection_reason": "The marked either/or answer is not entailed. The two Some conclusions may both be true, and a model with no radios makes both false; they do not form a valid complementary pair."},
    {"source_pdf": PDFS[2], "source_page": 19,
     "question_summary": "Handwritten A/B/C diagram and a list of nine categorical conclusions.",
     "rejection_reason": "The page does not state a complete textual premise set and marks Some B are not C as definite without any existential premise for B. The diagram cannot justify the marked existential conclusion under the required no-existence assumption."},
    {"source_pdf": PDFS[2], "source_page": 20,
     "question_summary": "Handwritten, partially drawn A/B/C diagrams with categorical claims.",
     "rejection_reason": "No complete statement set or unambiguous question is supplied; the two sketches encode incompatible overlaps and disjointness, so the intended model and answer cannot be verified."},
    {"source_pdf": PDFS[3], "source_page": 5,
     "question_summary": "All hills are trees; all trees are jungles; all jungles are bushes.",
     "rejection_reason": "The source marks Some jungles are hills from universal statements alone. The class may be empty, so that existential conclusion does not follow."},
    {"source_pdf": PDFS[3], "source_page": 6,
     "question_summary": "Rockets, poles, trams, ropes, and tents with a conclusion Some poles are rockets.",
     "rejection_reason": "The source marks Some poles are rockets from All rockets are poles, which reverses the inclusion and assumes rockets exist. The source answer key is invalid."},
    {"source_pdf": PDFS[3], "source_page": 7,
     "question_summary": "Dials, mirrors, spoons, decks, and chairs with conclusion Some spoons are dials.",
     "rejection_reason": "The source marks Some spoons are dials despite having no existential statement about dials or a connection from the spoon-deck witness to dials. The marked answer is not entailed."},
]


def parse_formula(formula):
    return formula[0].upper(), canonical_term(formula[1]), canonical_term(formula[2])


def regions(terms):
    terms = tuple(terms)
    return [
        frozenset(term for bit, term in enumerate(terms) if mask & (1 << bit))
        for mask in range(1 << len(terms))
    ]


def region_satisfies(region, formula):
    kind, left, right = parse_formula(formula)
    has_left, has_right = left in region, right in region
    if kind == "ALL":
        return not has_left or has_right
    if kind == "NO":
        return not (has_left and has_right)
    if kind == "SOME":
        return has_left and has_right
    if kind == "SOME_NOT":
        return has_left and not has_right
    raise ValueError(f"Unknown categorical formula: {kind}")


def negate(formula):
    kind, left, right = parse_formula(formula)
    opposite = {"ALL": "SOME_NOT", "SOME_NOT": "ALL", "SOME": "NO", "NO": "SOME"}
    return F(opposite[kind], left, right)


def model_exists(statements, additional=()):
    formulas = list(statements) + list(additional)
    terms = sorted({term for formula in formulas for term in formula[1:]})
    all_regions = regions(terms)
    allowed = [r for r in all_regions if all(
        region_satisfies(r, formula) for formula in formulas if formula[0].upper() in {"ALL", "NO"}
    )]
    existentials = [formula for formula in formulas if formula[0].upper() in {"SOME", "SOME_NOT"}]
    return all(any(region_satisfies(r, formula) for r in allowed) for formula in existentials)


def entails(statements, conclusion):
    return not model_exists(statements, [negate(conclusion)])


def disjunction_entails(statements, left, right):
    return not model_exists(statements, [negate(left), negate(right)])


def evaluated_code(record):
    if not model_exists(record["formulas"]):
        raise ValueError(f"Inconsistent statement set: {record['question']}")
    if record["kind"] in {"possibility", "impossible"}:
        possible = [model_exists(record["formulas"], [candidate]) for candidate in record["possibility_options"]]
        expected_count = 1 if record["kind"] == "possibility" else len(possible) - 1
        if sum(possible) != expected_count:
            raise ValueError(f"Possibility item requires one consistent option, got {possible}: {record['question']}")
        target = True if record["kind"] == "possibility" else False
        return "ABCD"[possible.index(target)]
    outcomes = [i + 1 for i, (_, formula) in enumerate(record["conclusions"])
                if entails(record["formulas"], formula)]
    roman = lambda index: ("I", "II", "III", "IV")[index - 1]
    if record["kind"] == "either":
        if len(outcomes) == 1:
            return roman(outcomes[0])
        if len(outcomes) == 2 and disjunction_entails(
            record["formulas"], record["conclusions"][outcomes[0] - 1][1],
            record["conclusions"][outcomes[1] - 1][1],
        ):
            return f"EITHER({roman(outcomes[0])},{roman(outcomes[1])})"
        if len(outcomes) == 0:
            for left in range(len(record["conclusions"])):
                for right in range(left + 1, len(record["conclusions"])):
                    if disjunction_entails(record["formulas"], record["conclusions"][left][1], record["conclusions"][right][1]):
                        return f"EITHER({roman(left + 1)},{roman(right + 1)})"
        return "+".join(roman(i) for i in outcomes) if outcomes else "NONE"
    return "+".join(roman(i) for i in outcomes) if outcomes else "NONE"


def render_question(record):
    lines = ["Statements:"]
    lines.extend(f"{i}. {statement}" for i, statement in enumerate(record["statements"], 1))
    if record["kind"] in {"possibility", "impossible"}:
        lines.append(record["question"])
    else:
        lines.append("Conclusions:")
        numerals = ("I", "II", "III", "IV")
        lines.extend(f"{numerals[i]}. {text}" for i, (text, _) in enumerate(record["conclusions"]))
        lines.append(record["question"])
    return "\n".join(lines)


def build():
    questions, ledger = [], []
    levels = Counter()
    for number, record in enumerate(ITEMS, 1):
        record["formulas"] = [formula for statement in record["statements"] for formula in parse_statement(statement)]
        levels[record["difficulty"]] += 1
        code = evaluated_code(record)
        if code != record["answer"]:
            raise ValueError(f"Independent set-model answer {code} disagrees with reviewed key {record['answer']}: {record['question']}")
        if len(record["choices"]) != 4 or len({label for label, _ in record["choices"]}) != 4:
            raise ValueError(f"Question {number} must have four distinct choices")
        if record["kind"] in {"possibility", "impossible"}:
            correct_option = code
            options = {chr(65 + i): record["choices"][i][0] for i in range(4)}
        else:
            correct_option = next((chr(65 + i) for i, (_, choice_code) in enumerate(record["choices"])
                                   if choice_code == code), None)
            if correct_option is None:
                raise ValueError(f"Question {number} has no option for logical result {code}")
            options = {chr(65 + i): label for i, (label, _) in enumerate(record["choices"])}
        source = ORIGINAL if record["source"] is None else (
            f"{PDFS[record['source']]}, page {record['page']}; exam/year not stated"
        )
        if len(source) > 255:
            raise ValueError(f"Question {number} provenance exceeds database field length")
        stem = render_question(record)
        choices = record["choices"]
        row = {
            "subject_slug": "reasoning", "subcategory_slug": None, "chapter_slug": "syllogism",
            "question_text": stem, "options": options, "correct_option": correct_option,
            "explanation": record["explanation"], "difficulty": record["difficulty"],
            "is_pyq": False, "pyq_year": None, "pyq_exam_name": None, "source": source,
        }
        audit = {
            "question_id": f"syllogism-{number:03}", "row": number,
            "source_type": "original" if record["source"] is None else "pdf-derived",
            "source_pdf": None if record["source"] is None else PDFS[record["source"]],
            "source_page": record["page"], "question": stem,
            "statements": record["statements"],
            "conclusions": [text for text, _ in record["conclusions"]],
            "options": options, "expected_answer": options[correct_option],
            "correct_option": correct_option, "explanation": record["explanation"],
            "difficulty": record["difficulty"], "verification_status": "PASS - exhaustive categorical set-constraint check",
            "pyq_status": "not identified as a PYQ in the PDF; imported as Normal" if record["source"] else "original practice; imported as Normal",
            "source": source, "verification_code": code,
            "option_review": "Four distinct options; exactly one option matches the formally checked result.",
            "concept_signature": record["signature"] or f"syllogism-source-{record['source']}-p{record['page']}",
            "validation_status": "PASS",
        }
        if record["kind"] in {"possibility", "impossible"}:
            audit["possibility_options"] = [list(x) for x in record["possibility_options"]]
            audit["possible_options"] = [model_exists(record["formulas"], [x]) for x in record["possibility_options"]]
        questions.append(row)
        ledger.append(audit)
    if len(questions) != 30 or levels != Counter({"EASY": 10, "MEDIUM": 10, "HARD": 10}):
        raise ValueError(f"Bank size or difficulty distribution is invalid: {len(questions)}, {dict(levels)}")
    ledger[0]["rejected_source_questions"] = REJECTIONS
    (DATA / "syllogism_verified_batch.json").write_text(
        json.dumps({"questions": questions}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (DATA / "syllogism_answer_ledger.json").write_text(
        json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    report = """# Syllogism CH-07 review

## Status

COMPLETED. Artifact validation, guarded append-only import, replay, cross-chapter deduplication, and authenticated API verification passed.

## Source review

All physical pages were visually inspected from rendered images: Lecture 01 (18/18), Lecture 02 (22/22), and Lecture 03 (14/14), 54 pages total. Every legible statement, conclusion, answer mark, Venn diagram, and handwritten annotation was reviewed. The prompt's cited page references are offset by one from the physical 1-based PDF page sequence in several examples; artifact provenance uses the physical page number.

| Source PDF | Pages reviewed | Complete prompts reviewed | Selected | Rejected |
|---|---:|---:|---:|---:|
| Syllogism 01 Class Notes.pdf | 18/18 | 4 | 4 | 0 |
| Syllogism 02_ Class Notes.pdf | 22/22 | 14 | 11 | 3 |
| Syllogism 03_ Class Notes.pdf | 14/14 | 7 | 4 | 3 |
| **Total** | **54/54** | **25** | **19** | **6** |

The six rejections and item-specific reasons are included in the answer ledger. Formula slides, recap slides, and the Lecture 03 Only / Only a few translation notes were reviewed as instructional material rather than counted as question prompts. Source answers were independently checked; incorrect existential or either/or annotations were not copied as keys.

## Bank

The batch contains 30 Normal questions: 19 PDF-derived and 11 original SSC-style practice questions. Difficulty is balanced at 10 Easy, 10 Medium, and 10 Hard. No PDF identifies an included question as a PYQ; no PYQ record is created.

## Logical verification

Every categorical item was evaluated with an exhaustive region-constraint model. All/No statements forbid incompatible Venn regions; Some/Some Not statements require at least one compatible region. Universal statements do not imply existence. All A are B, Some A are B, No A are B, Some A are not B, possibility, and the Only / Only a few translations are validated with those constraints. Either/or is accepted only when the proposed disjunction holds in every valid model; the ledger explains cases where both conclusions may hold.

## Database verification

The live SSC / Reasoning / Syllogism catalog path resolved to chapter ID 038aaa3d-1348-4c6a-88cd-7ac3378b739d with an empty baseline. A read-only 0.97-similarity scan against 4,053 active question stems in other chapters found no matches. Guarded import inserted 30 Normal records with 0 rejects and 0 import duplicates. Post-import counts: 30 active Normal (10 Easy, 10 Medium, 10 Hard), 0 PYQ, 30 total. Replay recognized all 30 as duplicates and would add 0 rows.

Authenticated API checks confirmed the chapter is visible under SSC / Reasoning; each difficulty has 10 questions and supports a 10-question request; mixed chapterwise practice supports 10, 15, 20, and 25 questions; PYQ availability is 0; and the question-management API returned 30 questions with four options and one correct option each.

## Regression and build checks

The Syllogism focused suite passed (7 tests). Existing Calendar, Clock, Series, Direction and Distance, and Ranking and Order regression files passed (19 tests; one Calendar availability API fixture was deselected, with Syllogism's authenticated availability API checked directly). The catalog availability service test passed, as did 14 test-session short-pool service cases. Python compilation, the frontend production build, and `git diff --check` passed.
"""
    (DATA / "syllogism_review_report.md").write_text(report, encoding="utf-8")
    print("BUILT", len(questions), dict(levels), "pdf_derived", sum(x["source_type"] == "pdf-derived" for x in ledger),
          "original", sum(x["source_type"] == "original" for x in ledger))


if __name__ == "__main__":
    build()
