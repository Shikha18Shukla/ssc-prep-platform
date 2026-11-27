import psycopg2

conn = psycopg2.connect('postgresql://postgres@127.0.0.1:5432/ssc_prep')
cur = conn.cursor()

# Check difficulty enum
cur.execute('SELECT DISTINCT difficulty FROM questions')
difficulties = cur.fetchall()
print('Difficulty values in questions table:')
for d in difficulties:
    print(f'  {d[0]}')

# Check chapters table - find banking-related chapters
cur.execute('SELECT id, name, subject_id FROM chapters WHERE subject_id = %s', ('79da4fe3-ee5a-4356-9117-e5bc6f87367a',))
bank_chapters = cur.fetchall()
print(f'\nBanking awareness chapters: {len(bank_chapters)}')
for row in bank_chapters:
    print(f'  ID: {row[0]}, Name: {row[1]}')

# Get one chapter ID
if bank_chapters:
    test_cid = bank_chapters[0][0]
    cur.execute('SELECT COUNT(*), COUNT(*) FILTER (WHERE is_active=true) FROM questions WHERE chapter_id = %s', (test_cid,))
    total, active = cur.fetchone()
    print(f'\nChapter {test_cid[:20]}...: total={total}, active={active}')

conn.close()