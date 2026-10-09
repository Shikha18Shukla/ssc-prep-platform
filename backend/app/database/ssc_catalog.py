"""SSC chapter catalog transcribed from the supplied chapter screenshots.

Each chapter's list position becomes its display order within that category.
The source's CH labels are not used as global IDs or encoded in slugs.
Names ending in an ellipsis are visibly truncated in the source and need
manual confirmation; their hidden wording is intentionally not inferred.
"""

from collections.abc import Iterator


# A category name of None means the chapters are directly under the subject.
SSC_CATALOG: dict[str, list[tuple[str | None, list[str]]]] = {
    "gk-gs": [
        (
            "Science",
            [
                "Cell",
                "Digestive System",
                "Circulatory System",
                "Respiratory System",
                "Brain & Nervous System",
                "Excretory System",
                "Nutrition",
                "Disease",
                "Glands",
                "Skeleton System",
                "Reproduction",
                "Plant Kingdom",
                "Animal Kingdom",
                "Tissues",
                "Matter & Atom",
                "Metals & Non Metals",
                "Acid Base & Salt",
                "Carbon & Its Compound",
                "Periodic Table",
                "Chemical Reaction",
                "Chemistry in Every Day Life",
                "Motion & Force",
                "Gravitation Work Energy",
                "Optics & Human Eye",
                "Sound",
                "Electricity",
                "Magnetic Effect & Heating",
                "Physics Revision",
            ],
        ),
        (
            "Computer",
            [
                "Basics",
                "Generations",
                "Types Of Computers",
                "Computer Memory",
                "Computer Threats, Security",
                "Ms Office",
                "Input Output Devices",
                "Computer Terminology",
                "Storage Devices",
            ],
        ),
        (
            "Static GK",
            [
                "Neighbouring Countries of I...",
                "Major Ramsar Site",
                "Major Awards",
                "Classical Dance",
                "Folk Dance",
                "Biosphere Reserve of India",
                "National Park of India",
                "International Organisation",
                "Important Days",
                "World Heritage Sites of India",
                "Major Festivals & Fares of In...",
                "Major Tribes",
                "Census Report",
                "Forest Report",
                "Tiger Reserve",
            ],
        ),
        (
            "Geography",
            [
                "Introduction",
                "Himalayas",
                "Plains of India",
                "Plateau",
                "Islands",
                "Physical Geography",
                "Mapping (World Geography)",
            ],
        ),
        (
            "Economics",
            [
                "Introduction",
                "Money",
                "Banking",
                "National Income",
                "Economic Planning",
                "Planning Commission, NDC, Nit...",
                "Inflation, Deflation",
                "Fiscal Policy, Deficit",
                "FDI, FPI, BOP",
                "IMF, WTO, WB",
                "International Economic Organi...",
                "National Economic Organisation",
                "Market Structure",
                "Monetary Policy",
                "Poverty & Unemployment",
                "Factors of Production",
                "Law of Demand and Supply",
            ],
        ),
        (
            "Polity",
            [
                "Constitution",
                "Preamble",
                "Union and it's Territories",
                "Citizenship",
                "Fundamental Rights",
                "Directive Principle of State Poli...",
                "Fundamental Duties",
                "President",
                "Emergency Powers",
                "Vice President/Prime Minister",
                "Attorney/Advocate General",
                "State",
                "Loksabha/Rajya Sabha",
                "State Legislature",
                "Constitutional Bodies",
                "Non Constitutional Bodies",
                "Supreme /High court",
                "Parts, Schedules, Sources",
                "Making of the Constitution",
                "Historical Background",
            ],
        ),
        (
            "History",
            [
                "Introduction",
                "Stone Age",
                "Indus Valley Civilization",
                "Vedic Culture",
                "Mahajanapadas",
                "Jainism",
                "Buddhism",
                "Magadh Empire",
                "Mauryan Empire",
                "Post Mauryan Empire",
                "Gupta Era",
                "Post Gupta Era",
                "Southern Empire",
                "Arab and Turkey Invasion",
                "Delhi Sultanate",
                "Vijaynagar & Bahmani Empire",
                "Mughal Empire",
                "Maratha Empire",
                "Post Mughal Empire",
                "European Companies",
                "Expansion of British Power",
                "Governor-General & Viceroy",
                "The Revolt of 1857",
                "National Movement",
                "Indian Independence Movement",
            ],
        ),
    ],
    "maths": [
        (
            "Arithmetic Maths",
            [
                "Percentage",
                "Profit & Loss",
                "Discount",
                "Simple Interest",
                "Compound Interest",
                "Ratio & Proportion",
                "Partnership",
                "Average",
                "Age",
                "Mixture",
                "Alligation",
                "Time & Work",
                "Pipe & Cistern",
                "Speed Time & Distance",
                "Train",
                "Boat & Stream",
                "Data Interpretation",
                "Race",
            ],
        ),
        (
            "Advanced Maths",
            [
                "Geometry",
                "Coordinate Geometry",
                "Mensuration",
                "Statistics",
                "Probability",
                "Number System",
                "Simplification",
                "HCF & LCM",
                "Algebra",
                "Quadratic Equations",
                "Trigonometry",
                "Maximum & Minimum Value",
                "Height & Distance",
            ],
        ),
    ],
    "english": [
        (
            None,
            [
                "Introduction",
                "Parts of Speech",
                "Basics",
                "Noun",
                "Pronoun",
                "Adjective",
                "Article",
                "Verb Basics",
                "Subject and Verb Agreement",
                "Tense",
                "Voice",
                "Conjunction",
                "Narration",
                "Adverb",
                "Question Tag",
                "Preposition",
                "Para Jumble",
                "Cloze Test",
                "Mixed Errors",
                "Sentence Improvement",
                "Reading Comprehension",
                "Vocabulary",
            ],
        ),
    ],
    "reasoning": [
        (
            None,
            [
                "Coding Decoding",
                "Alphanumerical Test",
                "Analogy",
                "Classification",
                "Mathematical Operations",
                "Series",
                "Syllogism",
                "Dice",
                "Sitting Arrangement",
                "Puzzle",
                "Venn Diagram",
                "Direction and Distance",
                "Ranking and Order",
                "Blood Relation",
                "Word Building",
                "Inequality",
                "Non-Verbal Reasoning",
                "Statement Based Questions",
                "Insert the Missing Number",
                "Decision Making",
                "Calendar (Recorded)",
                "Clock (Recorded)",
            ],
        ),
    ],
}


EXCLUDED_SOURCE_CARDS = [
    ("gk-gs/computer", "Brain Storming Session - 1"),
    ("gk-gs/computer", "Brain Storming Session -2"),
    ("gk-gs/computer", "Brain Storming Session -3"),
    ("gk-gs/economics", "Doubt Session"),
    ("gk-gs/polity", "Practice Set - 01"),
    ("gk-gs/polity", "Practice Set - 02"),
    ("english", "Practice Set"),
]


def iter_catalog_chapters() -> Iterator[tuple[str, str | None, str, int]]:
    """Yield (subject slug, subcategory slug, name, display order)."""
    for subject_slug, groups in SSC_CATALOG.items():
        for category_name, chapter_names in groups:
            category_slug = slugify(category_name) if category_name else None
            for order, chapter_name in enumerate(chapter_names, start=1):
                yield subject_slug, category_slug, chapter_name, order


def slugify(name: str) -> str:
    """Generate a stable topic slug without adding a category prefix."""
    import re
    import unicodedata

    normalized = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    normalized = normalized.replace("&", " and ")
    return re.sub(r"[^a-z0-9]+", "-", normalized.lower()).strip("-")
