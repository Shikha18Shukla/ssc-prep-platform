import sys
import os
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import Session

# Add the current directory to sys.path to import app
sys.path.append(os.getcwd())

from app.models.subject import Subject
from app.models.chapter import Chapter
from app.models.question import Question

# Database connection
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/ssc_prep"
engine = create_engine(DATABASE_URL)

def query_counts():
    with Session(engine) as session:
        # Find the GS subject (Science belongs to GS subcategory usually, or is it its own subject?)
        # Let's find chapters that are likely science chapters.
        # From the prompt, we know there are 28 Science chapters.
        
        science_chapters = session.execute(
            select(Chapter)
            .join(Subject)
            .filter(Subject.slug == "general-studies")
            .order_by(Chapter.display_order)
        ).scalars().all()
        
        if not science_chapters:
            # Maybe slug is different
            science_chapters = session.execute(
                select(Chapter).order_by(Chapter.display_order)
            ).scalars().all()

        print("| Science Chapter | Ordinary | PYQ | Needed |")
        print("|---|---:|---:|---:|")
        
        total_ordinary = 0
        total_pyq = 0
        total_needed = 0
        
        for chapter in science_chapters:
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
            
            print(f"| {chapter.name} | {ordinary_count} | {pyq_count} | {needed} |")
            
            total_ordinary += ordinary_count
            total_pyq += pyq_count
            total_needed += needed
            
        print(f"| **TOTAL** | **{total_ordinary}** | **{total_pyq}** | **{total_needed}** |")

if __name__ == "__main__":
    query_counts()
