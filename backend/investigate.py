import psycopg2

conn = psycopg2.connect('postgresql://postgres@127.0.0.1:5432/ssc_prep')
cur = conn.cursor()

# 1. Get all chapters with subject_id
cur.execute('SELECT id, name, subject_id, is_active FROM chapters ORDER BY id')
all_chapters = cur.fetchall()
print(f"Total chapters: {len(all_chapters)}")
print("\nAll chapters:")
for cid, sname, subj, is_active in all_chapters:
    print(f"  ID: {str(cid)[:20]}... | Name: {sname[:50]} | Subject: {str(subj)[:20]}... | Active: {is_active}")

# 2. Get question counts per chapter
print("\n\nQuestion counts per chapter:")
for cid, sname, subj, is_active in all_chapters:
    cur.execute('SELECT COUNT(*), COUNT(*) FILTER (WHERE is_active = true) FROM questions WHERE chapter_id = %s', (cid,))
    total, active = cur.fetchone()
    print(f"  {str(cid)[:20]}... {sname[:50]}: total={total}, active={active}")

# 3. Check the 9 Banking Awareness chapters specifically
banking_subject = '79da4fe3-ee5a-4356-9117-e5bc6f87367a'
cur.execute('SELECT id, name, subject_id FROM chapters WHERE subject_id = %s', (banking_subject,))
banking_chapters = cur.fetchall()
print(f"\n\nBanking Awareness chapters (subject_id={banking_subject}):")
for cid, sname, subj in banking_chapters:
    cur.execute('SELECT COUNT(*), COUNT(*) FILTER (WHERE is_active = true) FROM questions WHERE chapter_id = %s', (cid,))
    total, active = cur.fetchone()
    print(f"  {sname}: total={total}, active={active}")

# 4. Check all question chapter_ids
print("\n\nQuestion chapter_id distribution:")
cur.execute('SELECT chapter_id, COUNT(*) FROM questions GROUP BY chapter_id ORDER BY COUNT(*) DESC')
q_dist = cur.fetchall()
for cid, count in q_dist:
    # Get chapter name
    cur.execute('SELECT name FROM chapters WHERE id = %s', (cid,))
    cname = cur.fetchone()[0]
    print(f"  {cname[:50]}: {count} questions")

conn.close()