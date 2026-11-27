"""Direct import of banking questions into PostgreSQL using psycopg2."""
import json
import os
import uuid
from datetime import datetime

import psycopg2

# Chapter mapping: my generated chapter IDs -> database chapter UUIDs
CHAPTER_MAP = {
    "2bc3264e-d1c0-4ec5-ac57-fd445f7f43c5": "6a4df159-35a8-49d7-b764-55162b4cd75d",  # Basics of Banking
    "d751d44d-90e4-4f41-9c8f-2060d186be06": "9c58e44b-e050-4dc6-be37-947a7ae98952",  # RBI
    "5b196e44-4356-4767-8623-cf3e6e45fe37": "a9a0ce3b-9d82-401e-8ed7-c73d0110c646",  # Types of Accounts
    "07f4e0d7-488a-4d85-8383-8efe637ec053": "b4c19be3-102f-49ac-b51b-e2d8658af111",  # Inflation and Monetary Policy
}

# Note: types-of-banks chapter exists in DB but we map basics-of-banking questions to it
# or we can skip. Let me check if we need it.

DB_URL = "postgresql://postgres@127.0.0.1:5432/ssc_prep"


def import_questions():
    """Import questions from the verified batch JSON into the database."""
    
    # Load the batch file
    batch_path = r'C:\Users\shikh\Desktop\ssc-prep-platform\backend\data\imports\general-banking-awareness\verified_batch.json'
    with open(batch_path, 'r', encoding='utf8') as f:
        data = json.load(f)
    
    questions = data['questions']
    chapter_counts = data['chapter_counts']
    
    print(f"Total questions to import: {len(questions)}")
    
    conn = psycopg2.connect(DB_URL)
    conn.autocommit = False
    cur = conn.cursor()
    
    # Track counts
    chapter_stats = {}
    for cid in CHAPTER_MAP.values():
        chapter_stats[cid] = {'total': 0, 'imported': 0}
    
    # First, let's check which chapters exist in the database
    cur.execute("SELECT id, slug, name FROM chapters")
    db_chapters = {row[0]: {'id': row[0], 'slug': row[1], 'name': row[2]} for row in cur.fetchall()}
    print(f"Database chapters: {len(db_chapters)}")
    for cid, info in db_chapters.items():
        print(f"  {info['slug']} ({info['name'][:30]})...")
    
    imported = 0
    skipped = 0
    
    try:
        for i, q in enumerate(questions):
            chapter_id = q.get('chapter_id', '')
            
            # Map the chapter ID to the database chapter UUID
            db_chapter_id = CHAPTER_MAP.get(chapter_id)
            if db_chapter_id is None:
                print(f"WARNING: No chapter mapping for {chapter_id}, skipping question {i}")
                skipped += 1
                continue
            
            # Check if chapter exists in database
            if db_chapter_id not in db_chapters:
                print(f"WARNING: Chapter {db_chapter_id} not found in database, skipping question {i}")
                skipped += 1
                continue
            
            chapter_info = db_chapters[db_chapter_id]
            chapter = chapter_info['slug']
            
            # Ensure exactly 5 options
            opts = q.get('options', [])
            if len(opts) != 5:
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
            question_id = str(uuid.uuid4())
            
            cur.execute("""
                INSERT INTO questions (id, chapter_id, question_text, explanation, difficulty, 
                    is_pyq, pyq_year, pyq_exam_name, source, is_active, created_at, updated_at, image_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                question_id,
                db_chapter_id,
                q.get('question_text', ''),
                q.get('explanation', ''),
                q.get('difficulty', 'MEDIUM'),
                q.get('is_pyq', False),
                q.get('pyq_year'),
                q.get('pyq_exam_name'),
                q.get('source', ''),
                q.get('is_active', True),
                q.get('created_at', datetime.now().isoformat()),
                q.get('updated_at', datetime.now().isoformat()),
                q.get('image_url'),
            ))
            
            # Create the 5 options
            for j, opt_data in enumerate(opts):
                # opt_data is like "A) 1918" or just the text
                # Need to extract just the text part after "A) "
                opt_text = opt_data
                if isinstance(opt_data, dict):
                    opt_text = opt_data.get('option_text', str(opt_data))
                elif ')' in opt_data:
                    opt_text = opt_data.split(')', 1)[1].strip() if ')' in opt_data else opt_data.strip()
                
                is_correct = (j == correct_idx)
                option_key = chr(65 + j)  # A, B, C, D, E
                
                cur.execute("""
                    INSERT INTO question_options (id, question_id, option_key, option_text, display_order, is_correct)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    str(uuid.uuid4()),
                    question_id,
                    option_key,
                    opt_text,
                    j + 1,
                    is_correct,
                ))
            
            chapter_stats[db_chapter_id]['total'] = chapter_stats.get(db_chapter_id, {'total': 0, 'imported': 0})['total'] + 1
            chapter_stats[db_chapter_id]['imported'] = chapter_stats.get(db_chapter_id, {'total': 0, 'imported': 0})['imported'] + 1
            imported += 1
            
            if (i + 1) % 20 == 0:
                conn.commit()
                print(f"Imported {i + 1}/{len(questions)} questions...")
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
        raise
    finally:
        cur.close()
        conn.close()
    
    # Print summary
    print("\n=== Import Summary ===")
    total_imported = 0
    for cid, stats in chapter_stats.items():
        print(f"Chapter {cid}: {stats['imported']} imported out of {stats['total']} total")
        total_imported += stats['imported']
    
    print(f"\nTotal: {total_imported} questions imported")
    
    # Verify by counting in database
    conn2 = psycopg2.connect(DB_URL)
    cur2 = conn2.cursor()
    cur2.execute("SELECT COUNT(*) FROM questions")
    print(f"Total questions in DB: {cur2.fetchone()[0]}")
    cur2.execute("""SELECT c.slug, COUNT(q.id) FROM questions q 
                    JOIN chapters c ON q.chapter_id = c.id 
                    GROUP BY c.slug ORDER BY c.slug""")
    for row in cur2.fetchall():
        print(f"  {row[0]}: {row[1]} questions")
    cur2.close()
    conn2.close()


if __name__ == "__main__":
    import_questions()