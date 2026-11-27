import psycopg2

conn = psycopg2.connect('postgresql://postgres@127.0.0.1:5432/ssc_prep')
cur = conn.cursor()

# Check all chapters
cur.execute('SELECT id, name, subject_id FROM chapters')
all_chapters = cur.fetchall()
print(f"Total chapters in database: {len(all_chapters)}")
print()

# Find chapters with 40+ active questions
print("Chapters and their active question counts:")
for cid, sname, subj in all_chapters:
    cur.execute('SELECT COUNT(*), COUNT(*) FILTER (WHERE is_active = true) FROM questions WHERE chapter_id = %s', (cid,))
    total, active = cur.fetchone()
    marker = " OK" if active >= 40 else " LOW"
    print(f"  Chapter {str(cid)[:20]}...: {sname[:50]} - total={total}, active={active}{marker}")

conn.close()
print("\nDone!")