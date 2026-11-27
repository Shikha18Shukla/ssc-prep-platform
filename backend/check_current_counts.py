import psycopg2

conn = psycopg2.connect('postgresql://postgres@127.0.0.1:5432/ssc_prep')
cur = conn.cursor()

# Check current counts per chapter
chapter_ids = {
    'financial-markets': 'a58ffad6-9e93-40bc-b1c1-77e815e3ad4c',
    'non-performing-assets': '414d8f88-db2b-443c-9c54-30482d72888b',
    'basel-norms-and-banking-risks': 'b182d7f6-6571-4a86-9701-8f9be761dd2e',
    'banking-terminologies': '50f681a6-be97-4b3e-b07d-f1f9380d4efd',
}

print("Current active question counts per chapter:")
for ch_slug, ch_id in chapter_ids.items():
    cur.execute('SELECT COUNT(*), COUNT(*) FILTER (WHERE is_active = true) FROM questions WHERE chapter_id = %s::uuid', (ch_id,))
    total, active = cur.fetchone()
    print(f"  {ch_slug}: total={total}, active={active}")

# Also check the 5 original banking chapters
cur.execute('SELECT id, name FROM chapters WHERE subject_id = %s', ('79da4fe3-ee5a-4356-9117-e5bc6f87367a',))
bank_chapters = cur.fetchall()
print("\nOriginal banking chapters:")
for cid, sname in bank_chapters:
    cur.execute('SELECT COUNT(*), COUNT(*) FILTER (WHERE is_active = true) FROM questions WHERE chapter_id = %s', (cid,))
    total, active = cur.fetchone()
    print(f"  {sname}: total={total}, active={active}")

conn.close()