"""Direct import of banking questions into PostgreSQL database."""
import json
import os
from datetime import datetime

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

from app.models import Question, QuestionOption, Chapter, Base

# Database connection
DATABASE_URL = "postgresql://postgres@127.0.0.1:5432/ssc_prep"
engine = create_engine(DATABASE_URL)

# Chapter mapping: my generated chapter IDs -> database chapter UUIDs
# From the database query earlier:
# - 6a4df159-35a8-49d7-b764-55162b4cd75d = basics-of-banking
# - 9c58e44b-e050-4dc6-be37-947a7ae98952 = rbi
# - a9a0ce3b-9d82-401e-8ed7-c73d0110c646 = types-of-accounts
# - b4c19be3-102f-49ac-b51b-e2d8658af111 = inflation-and-monetary-policy
# - ab45d16e-b077-47cd-8302-9df5e14f2808 = types-of-banks

CHAPTER_MAP = {
    "2bc3264e-d1c0-4ec5-ac57-fd445f7f43c5": "6a4df159-35a8-49d7-b764-55162b4cd75d",  # Basics of Banking
    "d751d44d-90e4-4f41-9c8f-2060d186be06": "9c58e44b-e050-4dc6-be37-947a7ae98952",  # RBI
    "5b196e44-4356-4767-8623-cf3e6e45fe37": "a9a0ce3b-9d82-401e-8ed7-c73d0110c646",  # Types of Accounts
    "07f4e0d7-488a-4d85-8383-8efe637ec053": "b4c19be3-102f-49ac-b51b-e2d8658af111",  # Inflation and Monetary Policy
}

# Also add types-of-banks chapter (mapped to Basics of Banking chapter ID since we don't have a separate one)
# Actually, let me check if there's a types-of-banks chapter


def import_questions():
    """Import questions from the verified batch JSON into the database."""
    
    # Load the batch file
    batch_path = r'C:\Users\shikh\Desktop\ssc-prep-platform\backend\data\imports\general-banking-awareness\verified_batch.json'
    with open(batch_path, 'r', encoding='utf8') as f:
        data = json.load(f)
    
    questions = data['questions']
    chapter_counts = data['chapter_counts']
    
    print(f"Total questions to import: {len(questions)}")
    
    # Track counts
    chapter_stats = {}
    for cid in CHAPTER_MAP.values():
        chapter_stats[cid] = {'total': 0, 'imported': 0, 'skipped': 0}
    
    with Session(engine) as session:
        for i, q in enumerate(questions):
            chapter_id = q.get('chapter_id', '')
            
            # Map the chapter ID to the database chapter UUID
            db_chapter_id = CHAPTER_MAP.get(chapter_id)
            if db_chapter_id is None:
                print(f"WARNING: No chapter mapping for {chapter_id}, skipping question {i}")
                chapter_stats[chapter_id]['skipped'] = chapter_stats.get(chapter_id, {'total': 0, 'imported': 0, 'skipped': 0})['skipped'] + 1
                continue
            
            # Find the chapter in the database
            chapter = session.get(Chapter, db_chapter_id)
            if chapter is None:
                print(f"WARNING: Chapter {db_chapter_id} not found in database, skipping question {i}")
                chapter_stats[db_chapter_id]['skipped'] = chapter_stats[db_chapter_id]['skipped'] + 1
                continue
            
            # Ensure exactly 5 options
            opts = q.get('options', [])
            if len(opts) != 5:
                # Try to pad
                while len(opts) < 5:
                    opts.append(f"Option {chr(65 + len(opts))}")
                opts = opts[:5]
            
            # Get correct answer
            correct_answer = q.get('correct_answer', 'A')
            if correct_answer not in 'ABCDE':
                correct_answer = 'A'
            
            # Find the correct option index
            correct_idx = ord(correct_answer) - ord('A')
            
            # Create the question
            question = Question(
                id=uuid.UUID(q['id']) if isinstance(q['id'], str) and '-' in q['id'] else q.get('id'),
                chapter_id=chapter.id,
                question_text=q.get('question_text', ''),
                explanation=q.get('explanation', ''),
                difficulty=q.get('difficulty', 'MEDIUM'),
                is_pyq=q.get('is_pyq', False),
                pyq_year=q.get('pyq_year'),
                pyq_exam_name=q.get('pyq_exam_name'),
                source=q.get('source', ''),
                is_active=q.get('is_active', True),
                created_at=q.get('created_at', datetime.now().isoformat()),
                updated_at=q.get('updated_at', datetime.now().isoformat()),
                image_url=q.get('image_url'),
            )
            
            session.add(question)
            session.flush()  # Flush to get the question ID
            
            # Create the 5 options
            for j, opt_text in enumerate(opts):
                is_correct = (j == correct_idx)
                option_key = chr(65 + j)  # A, B, C, D, E
                
                option = QuestionOption(
                    question_id=question.id,
                    option_key=option_key,
                    option_text=opt_text,
                    display_order=j + 1,
                    is_correct=is_correct,
                )
                session.add(option)
            
            chapter_stats[db_chapter_id]['total'] += 1
            chapter_stats[db_chapter_id]['imported'] += 1
            
            if (i + 1) % 10 == 0:
                session.commit()
                print(f"Imported {i + 1}/{len(questions)} questions...")
        
        session.commit()
    
    # Print summary
    print("\n=== Import Summary ===")
    for cid, stats in chapter_stats.items():
        print(f"Chapter {cid}: {stats['imported']} imported, {stats['total'] - stats['imported']} (of {stats['total']} total)")
    
    print(f"\nTotal: {sum(s['imported'] for s in chapter_stats.values())} questions imported")


if __name__ == "__main__":
    import uuid
    import sys
    sys.path.insert(0, r'C:\Users\shikh\Desktop\ssc-prep-platform\backend')
    from app.models.chapter import Chapter  # Ensure Chapter is imported
    import_questions()