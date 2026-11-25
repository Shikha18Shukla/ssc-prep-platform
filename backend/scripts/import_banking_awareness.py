import json
import os
import psycopg2
import uuid
import unicodedata
from datetime import datetime

DB_URL = 'postgresql://postgres@127.0.0.1:5432/ssc_prep'
PO_SID = '79da4fe3-ee5a-4356-9117-e5bc6f87367a'
CLERK_SID = 'e8252000-a19a-48bd-b386-b363e0fd69d2'

def normalize_text(text):
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())

def get_chapter_id(cur, sid, slug):
    cur.execute("SELECT id FROM chapters WHERE subject_id = %s AND slug = %s", (sid, slug))
    return cur.fetchone()[0]

def get_existing_texts(cur, chapter_id):
    cur.execute("SELECT question_text FROM questions WHERE chapter_id = %s::uuid AND is_active = true", (chapter_id,))
    return set(normalize_text(r[0]) for r in cur.fetchall())

def insert_question(cur, ch_id, q_data):
    q_text, opts, correct, diff, expl = q_data
    qid = str(uuid.uuid4())
    now = datetime.now()
    cur.execute("""
        INSERT INTO questions (id, chapter_id, question_text, explanation, difficulty, is_pyq, pyq_year, pyq_exam_name, source, is_active, created_at, updated_at, image_url)
        VALUES (%s, %s::uuid, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (qid, ch_id, q_text, expl, diff, False, None, None, 'original-practice', True, now, now, None))
    
    for idx, opt_text in enumerate(opts):
        opt_key = chr(65 + idx)
        is_correct = (opt_key == correct)
        cur.execute("""
            INSERT INTO question_options (id, question_id, option_key, option_text, display_order, is_correct)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (str(uuid.uuid4()), qid, opt_key, opt_text, idx + 1, is_correct))
    
    return qid

def main():
    # Load questions from JSON
    json_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'banking_awareness_new_questions.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        all_questions = json.load(f)
    
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    total_inserted = 0
    for slug, questions in all_questions.items():
        po_ch_id = get_chapter_id(cur, PO_SID, slug)
        clerk_ch_id = get_chapter_id(cur, CLERK_SID, slug)
        
        po_existing = get_existing_texts(cur, po_ch_id)
        clerk_existing = get_existing_texts(cur, clerk_ch_id)
        
        inserted_po = 0
        inserted_clerk = 0
        
        for q_data in questions:
            q_text = q_data[0]
            norm = normalize_text(q_text)
            
            # Insert into PO if not exists
            if norm not in po_existing:
                insert_question(cur, po_ch_id, q_data)
                po_existing.add(norm)
                inserted_po += 1
            
            # Insert into Clerk if not exists
            if norm not in clerk_existing:
                insert_question(cur, clerk_ch_id, q_data)
                clerk_existing.add(norm)
                inserted_clerk += 1
        
        total_inserted += inserted_po + inserted_clerk
        print(f"{slug}: inserted {inserted_po} to PO, {inserted_clerk} to Clerk")
    
    conn.commit()
    print(f"\nTotal inserted: {total_inserted}")
    conn.close()

if __name__ == '__main__':
    main()