import psycopg2

conn = psycopg2.connect('postgresql://postgres@127.0.0.1:5432/ssc_prep')
cur = conn.cursor()

# Check chapter records
print("Checking chapters table for new banking chapters:")
chapter_ids = {
    'financial-markets': 'a58ffad6-9e93-40bc-b1c1-77e815e3ad4c',
    'non-performing-assets': '414d8f88-db2b-443c-9c54-30482d72888b',
    'basel-norms-and-banking-risks': 'b182d7f6-6571-4a86-9701-8f9be761dd2e',
    'banking-terminologies': '50f681a6-be97-4b3e-b07d-f1f9380d4efd',
}
for ch_slug, ch_id in chapter_ids.items():
    cur.execute('SELECT id, name, subject_id, is_active FROM chapters WHERE id = %s', (ch_id,))
    row = cur.fetchone()
    print(f"  {ch_slug}: id={str(row[0])[:20]}..., name={row[1]}, subject_id={str(row[2])[:20]}..., active={row[3]}")

# Check counts per chapter  
print("\nQuestion counts per chapter:")
for ch_slug, ch_id in chapter_ids.items():
    cur.execute('SELECT COUNT(*), COUNT(*) FILTER (WHERE is_active = true) FROM questions WHERE chapter_id = %s::uuid', (ch_id,))
    total, active = cur.fetchone()
    print(f"  {ch_slug}: total={total}, active={active}")

# Check all active question count
cur.execute('SELECT COUNT(*) FROM questions WHERE is_active = true')
total_active = cur.fetchone()[0]
print(f"\nTotal active questions in database: {total_active}")

# Verify correct answer count per chapter
print("\nVerification - chapters with exactly 1 correct answer per question:")
for ch_slug, ch_id in chapter_ids.items():
    cur.execute('''SELECT COUNT(*) FROM questions q JOIN question_options qo ON q.id = qo.question_id 
                   WHERE q.chapter_id = %s::uuid AND qo.is_correct = TRUE 
                   GROUP BY q.id HAVING COUNT(*) != 1''', (ch_id,))
    bad = cur.fetchall()
    print(f"  {ch_slug}: all have exactly 1 correct answer = {len(bad) == 0}")

conn.close()
print("\nVerification complete!")