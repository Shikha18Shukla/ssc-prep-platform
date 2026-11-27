import psycopg2
import json
import uuid as uuid_mod
from datetime import datetime
import psycopg2.extras

# Load questions from JSON file
with open('questions_import.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

questions = data['questions']
print(f"Loaded {len(questions)} questions from JSON file")

# Chapter ID mapping (UUIDs as strings)
chapter_id_strings = {
    'financial-markets': '222c866b-71a3-4277-95e5-1af657ed49a9',
    'non-performing-assets': 'a05cdb4d-ba5c-455b-9e4c-4d4a277e8ed8',
    'basel-norms-and-banking-risks': '22631dcb-cdad-4315-91e4-1fb00e92a116',
    'banking-terminologies': 'b5e1404a-99b4-46a5-bd95-ff7c4cdb1144',
}

# Build mapping: UUID string -> chapter slug
slug_from_id = {
    cid: slug for slug, cid in chapter_id_strings.items()
}

conn = psycopg2.connect('postgresql://postgres@127.0.0.1:5432/ssc_prep')
psycopg2.extras.register_uuid(conn)
cur = conn.cursor()

imported = 0
skipped = 0

for q in questions:
    try:
        # Parse dates
        created_at = datetime.fromisoformat(q['created_at']) if isinstance(q['created_at'], str) else q['created_at']
        updated_at = datetime.fromisoformat(q['updated_at']) if isinstance(q['updated_at'], str) else q['updated_at']
        
        chapter_id_str = q['chapter_id']
        
        # Insert question - use ::uuid cast for the chapter_id parameter
        qid = q['id']
        cid_str = chapter_id_str  # Keep as string, will be cast in SQL
        
        cur.execute("""
            INSERT INTO questions (id, chapter_id, question_text, explanation, difficulty, is_pyq, pyq_year, pyq_exam_name, source, is_active, created_at, updated_at, image_url)
            VALUES (%s, %s::uuid, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            qid, chapter_id_str, q['question_text'], q['explanation'], q['difficulty'],
            q['is_pyq'], q['pyq_year'], q['pyq_exam_name'], q['source'],
            q['is_active'], created_at, updated_at, q['image_url']
        ))
        
        # Insert options
        options = q['options']
        correct_answer = q['correct_answer']
        
        for idx, option_text in enumerate(options):
            option_key = chr(65 + idx)  # A, B, C, D, E
            is_correct = (option_key == correct_answer)
            
            cur.execute("""
                INSERT INTO question_options (id, question_id, option_key, option_text, display_order, is_correct)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                str(uuid.uuid4()),
                qid,
                option_key,
                option_text,
                idx + 1,
                is_correct,
            ))
        
        imported += 1
        if imported % 10 == 0:
            print(f"Imported {imported} questions...")
    except Exception as e:
        print(f"Error importing question (chapter_id={q.get('chapter_id', 'N/A')}): {type(e).__name__}: {str(e)[:200]}")
        skipped += 1
        conn.rollback()

conn.commit()

# Verify counts per chapter
print("\n" + "=" * 70)
print("IMPORT VERIFICATION")
print("=" * 70)

# Get chapter names from slug mapping
for ch_slug, cid_str in chapter_id_strings.items():
    # Use the UUID string directly in the query with ::uuid cast
    cur.execute('SELECT COUNT(*), COUNT(*) FILTER (WHERE is_active = true) FROM questions WHERE chapter_id = %s::uuid', (cid_str,))
    total, active = cur.fetchone()
    # Also get options count
    cur.execute('SELECT COUNT(*) FROM question_options WHERE question_id IN (SELECT id FROM questions WHERE chapter_id = %s::uuid)', (cid_str,))
    opts = cur.fetchone()[0]
    # Check correct answer count
    cur.execute('''SELECT COUNT(*) FROM questions q JOIN question_options qo ON q.id = qo.question_id WHERE q.chapter_id = %s::uuid AND qo.is_correct = TRUE GROUP BY q.id HAVING COUNT(*) != 1''', (cid_str,))
    bad = cur.fetchall()
    
    print(f"\n{ch_slug}:")
    print(f"  Total questions: {total}")
    print(f"  Active questions: {active}")
    print(f"  Option records: {opts}")
    print(f"  All have exactly 1 correct answer: {len(bad) == 0}")

# Total active count
cur.execute('SELECT COUNT(*) FROM questions WHERE is_active = true')
total_active = cur.fetchone()[0]
print(f"\nTotal active questions in database: {total_active}")

conn.close()
print(f"\nImport complete: {imported} imported, {skipped} skipped")
print("=" * 70)