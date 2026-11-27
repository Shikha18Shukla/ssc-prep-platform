import psycopg2

conn = psycopg2.connect('postgresql://postgres@127.0.0.1:5432/ssc_prep')
cur = conn.cursor()

# Check the original 5 banking chapters and their IDs
print("Original Banking Awareness chapters:")
cur.execute("SELECT id, name, subject_id FROM chapters WHERE subject_id = %s ORDER BY id", 
            ('79da4fe3-ee5a-4356-9117-e5bc6f87367a',))
original_chapters = cur.fetchall()
for cid, sname, subj in original_chapters:
    cur.execute("SELECT COUNT(*), COUNT(*) FILTER (WHERE is_active = true) FROM questions WHERE chapter_id = %s", (str(cid),))
    total, active = cur.fetchone()
    print(f"  {sname}: chapter_id={str(cid)[:20]}..., total={total}, active={active}")

# Check the 4 new chapters
print("\nNew Banking Awareness chapters (imported):")
new_chapter_ids = {
    'financial-markets': 'a58ffad6-9e93-40bc-b1c1-77e815e3ad4c',
    'non-performing-assets': '414d8f88-db2b-443c-9c54-30482d72888b',
    'basel-norms-and-banking-risks': 'b182d7f6-6571-4a86-9701-8f9be761dd2e',
    'banking-terminologies': '50f681a6-be97-4b3e-b07d-f1f9380d4efd',
}
for slug, cid in new_chapter_ids.items():
    cur.execute("SELECT COUNT(*), COUNT(*) FILTER (WHERE is_active = true) FROM questions WHERE chapter_id = %s", (cid,))
    total, active = cur.fetchone()
    # Get chapter name
    cur.execute("SELECT name FROM chapters WHERE id = %s", (cid,))
    cname = cur.fetchone()[0]
    print(f"  {slug}: {cname}, chapter_id={str(cid)[:20]}..., total={total}, active={active}")

# Check all chapters with questions
print("\n\nAll chapters with questions (active > 0):")
cur.execute("SELECT c.id, c.name, COUNT(q.id) as question_count FROM chapters c LEFT JOIN questions q ON c.id = q.chapter_id AND q.is_active = true GROUP BY c.id, c.name ORDER BY question_count DESC")
ch_with_questions = cur.fetchall()
for cid, cname, qcount in ch_with_questions:
    if qcount > 0:
        print(f"  {cname[:50]}: chapter_id={str(cid)[:20]}..., questions={qcount}")

conn.close()