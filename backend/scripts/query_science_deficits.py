import sys
import os
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import Session

# Add the current directory to sys.path to import app
sys.path.append(os.getcwd())

from app.models.subject import Subject
from app.models.chapter import Chapter
from app.models.subcategory import Subcategory
from app.models.question import Question

# Database connection
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/ssc_prep"
engine = create_engine(DATABASE_URL)

SCIENCE_CHAPTER_NAMES = [
    "Cell", "Digestive System", "Circulatory System", "Respiratory System",
    "Brain & Nervous System", "Excretory System", "Nutrition", "Disease",
    "Glands", "Skeleton System", "Reproduction", "Plant Kingdom",
    "Animal Kingdom", "Tissues", "Matter & Atom", "Metals & Non Metals",
    "Acid Base & Salt", "Carbon & Its Compound", "Periodic Table",
    "Chemical Reaction", "Chemistry in Every Day Life", "Motion & Force",
    "Gravitation Work Energy", "Optics & Human Eye", "Sound", "Electricity",
    "Magnetic Effect & Heating", "Physics Revision"
]

def query_science_counts():
    with Session(engine) as session:
        # Find Science chapters explicitly
        science_chapters = session.execute(
            select(Chapter)
            .filter(Chapter.name.in_(SCIENCE_CHAPTER_NAMES))
            .order_by(Chapter.display_order)
        ).scalars().all()
        
        # Also find by subcategory if any subcategory is 'Biology', 'Physics', 'Chemistry'
        science_subcategories = session.execute(
            select(Subcategory)
            .filter(Subcategory.name.in_(["Biology", "Physics", "Chemistry"]))
        ).scalars().all()
        
        if science_subcategories:
            sub_ids = [s.id for s in science_subcategories]
            extra_chapters = session.execute(
                select(Chapter)
                .filter(Chapter.subcategory_id.in_(sub_ids))
                .filter(~Chapter.name.in_(SCIENCE_CHAPTER_NAMES))
            ).scalars().all()
            science_chapters.extend(extra_chapters)

        # deduplicate by name just in case
        seen = set()
        unique_chapters = []
        for c in science_chapters:
            if c.name not in seen:
                unique_chapters.append(c)
                seen.add(c.name)

        print("| Science Chapter | ID | Ordinary | PYQ | Needed |")
        print("|---|---|---:|---:|---:|")
        
        total_ordinary = 0
        total_pyq = 0
        total_needed = 0
        
        for chapter in unique_chapters:
            # Ordinary active questions
            ordinary_count = session.query(func.count(Question.id)).filter(
                Question.chapter_id == chapter.id,
                Question.is_active == True,
                Question.is_pyq == False
            ).scalar()
            
            # PYQ active questions
            pyq_count = session.query(func.count(Question.id)).filter(
                Question.chapter_id == chapter.id,
                Question.is_active == True,
                Question.is_pyq == True
            ).scalar()
            
            needed = max(0, 10 - ordinary_count)
            
            print(f"| {chapter.name} | {chapter.id} | {ordinary_count} | {pyq_count} | {needed} |")
            
            total_ordinary += ordinary_count
            total_pyq += pyq_count
            total_needed += needed
            
        print(f"| **TOTAL** | | **{total_ordinary}** | **{total_pyq}** | **{total_needed}** |")

if __name__ == "__main__":
    query_science_counts()
