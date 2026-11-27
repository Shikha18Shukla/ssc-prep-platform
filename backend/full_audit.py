import psycopg2

conn = psycopg2.connect('postgresql://postgres@127.0.0.1:5432/ssc_prep')
cur = conn.cursor()

print('=' * 70)
print('FINAL DATABASE AUDIT - ALL FIVE BANKING CHAPTERS')
print('=' * 70)

# Check all five banking chapters
# Using the chapter IDs that have questions
chapters = [
    ('basics-of-banking', '6a4df159-35a8-49d7-b764-55162b4cd75d'),
    ('rbi', '9c58e44b-e050-4dc6-be37-947a7ae98952'),
    ('types-of-accounts', 'a9a0ce3b-9d82-401e-8ed7-c73d0110c646'),
    ('inflation-and-monetary-policy', 'b4c19be3-102f-49ac-b51b-e2d8658af111'),
    ('types-of-banks', 'ab45d16e-b077-47cd-8302-9df5e14f2808'),
]

print()
for slug, cid in chapters:
    cur.execute('SELECT COUNT(*), COUNT(*) FILTER (WHERE is_active = true) FROM questions WHERE chapter_id = %s', (cid,))
    total, active = cur.fetchone()
    cur.execute('SELECT COUNT(*) FROM question_options WHERE question_id IN (SELECT id FROM questions WHERE chapter_id = %s)', (cid,))
    opts = cur.fetchone()[0]
    cur.execute('''SELECT q.id::text, SUM(CASE WHEN qo.is_correct = TRUE THEN 1 ELSE 0 END) as correct_count
                   FROM questions q 
                   JOIN question_options qo ON q.id = qo.question_id
                   WHERE q.chapter_id = %s
                   GROUP BY q.id
                   HAVING SUM(CASE WHEN qo.is_correct = TRUE THEN 1 ELSE 0 END) != 1''', (cid,))
    bad_correct = cur.fetchall()
    cur.execute('SELECT COUNT(*) FROM questions WHERE chapter_id = %s AND (question_text IS NULL OR question_text = \'\')', (cid,))
    empty_text = cur.fetchone()[0]
    cur.execute('SELECT COUNT(*) FROM questions WHERE chapter_id = %s AND (explanation IS NULL OR explanation = \'\')', (cid,))
    empty_explain = cur.fetchone()[0]
    
    print(f'{slug} (ID: {cid[:8]}...):')
    print(f'  Total questions: {total}')
    print(f'  Active questions: {active}')
    print(f'  Active >= 40: {active >= 40}')
    print(f'  Option records: {opts}')
    print(f'  All have exactly 1 correct answer: {len(bad_correct) == 0}')
    print(f'  Questions with empty question text: {empty_text}')
    print(f'  Questions with empty explanation: {empty_explain}')

# Total count
cur.execute('SELECT COUNT(*) FROM questions WHERE chapter_id IN (%s,%s,%s,%s,%s)' % tuple(cid for _, cid in chapters))
total_all = cur.fetchone()[0]
print(f'\\nTotal questions across 5 chapters: {total_all}')

conn.close()