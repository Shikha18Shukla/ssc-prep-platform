import psycopg2

conn = psycopg2.connect('postgresql://postgres@127.0.0.1:5432/ssc_prep')
cur = conn.cursor()

# Check all five banking chapters
banking_slugs = ['basics-of-banking', 'rbi', 'types-of-banks', 'types-of-accounts', 'inflation-and-monetary-policy']

print("=" * 70)
print("CHAPTER VERIFICATION")
print("=" * 70)

for slug in banking_slugs:
    cur.execute('SELECT id, slug, name FROM chapters WHERE slug = %s', (slug,))
    row = cur.fetchone()
    if row:
        chapter_id = row[0]
        cur.execute('SELECT COUNT(*), COUNT(*) FILTER (WHERE is_active = true) FROM questions WHERE chapter_id = %s', (chapter_id,))
        total, active = cur.fetchone()
        cur.execute('SELECT COUNT(*) FROM question_options WHERE question_id IN (SELECT id FROM questions WHERE chapter_id = %s)', (chapter_id,))
        opts = cur.fetchone()[0]
        print(f"\n{slug}:")
        print(f"  Chapter ID: {chapter_id[:8]}...")
        print(f"  Total questions: {total}")
        print(f"  Active questions: {active}")
        print(f"  Option records: {opts}")
        # Check if exactly 5 opts per question
        cur.execute('''SELECT COUNT(DISTINCT qo.question_id) as q_count, COUNT(qo.id) as opt_count 
                       FROM question_options qo 
                       JOIN questions q ON qo.question_id = q.id 
                       WHERE q.chapter_id = %s 
                       GROUP BY qo.question_id 
                       HAVING COUNT(qo.id) != 5''', (chapter_id,))
        bad = cur.fetchall()
        print(f"  Questions with != 5 options: {len(bad)}")
    else:
        print(f"\n{slug}: NOT FOUND in database!")

# Also check types-of-banks specifically since it was newly created
cur.execute('SELECT id, slug, name FROM chapters WHERE slug = %s', ('types-of-banks',))
row = cur.fetchone()
if row:
    print(f"\ntypes-of-banks: Found (ID: {row[0][:8]}...)")

conn.close()