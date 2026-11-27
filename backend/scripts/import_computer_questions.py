import json
import os
import psycopg2
import uuid
import unicodedata
from datetime import datetime

DB_URL = 'postgresql://postgres@127.0.0.1:5432/ssc_prep'
CLERK_SID = '85084f2e-a07b-4287-a3f1-2c2b08641f4e'
PO_SID = 'f122d7c2-0146-4631-a0ab-4cf8b58b8182'

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
    json_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'computer_questions.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        all_questions = json.load(f)
    
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    total_inserted = 0
    for slug, questions in all_questions.items():
        clerk_ch_id = get_chapter_id(cur, CLERK_SID, slug)
        po_ch_id = get_chapter_id(cur, PO_SID, slug)
        
        clerk_existing = get_existing_texts(cur, clerk_ch_id)
        po_existing = get_existing_texts(cur, po_ch_id)
        
        inserted_clerk = 0
        inserted_po = 0
        
        for q_data in questions:
            q_text = q_data[0]
            norm = normalize_text(q_text)
            
            if norm not in clerk_existing:
                insert_question(cur, clerk_ch_id, q_data)
                clerk_existing.add(norm)
                inserted_clerk += 1
            
            if norm not in po_existing:
                insert_question(cur, po_ch_id, q_data)
                po_existing.add(norm)
                inserted_po += 1
        
        total_inserted += inserted_clerk + inserted_po
        print(f"{slug}: inserted {inserted_clerk} to Clerk, {inserted_po} to PO")
    
    conn.commit()
    print(f"\nTotal inserted: {total_inserted}")
    conn.close()

if __name__ == '__main__':
    main()