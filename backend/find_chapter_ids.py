import psycopg2

conn = psycopg2.connect('postgresql://postgres@127.0.0.1:5432/ssc_prep')
cur = conn.cursor()

# Check for any chapters related to our new topics
search_terms = ['financial', 'market', 'NPA', 'non-performing', 'basel', 'banking-term', 'terminolog']
for term in search_terms:
    # Use LIKE with explicit text cast since chapter_id is uuid
    cur.execute("SELECT DISTINCT chapter_id FROM questions WHERE chapter_id::text LIKE '%{}%'".format(term))
    matches = cur.fetchall()
    if matches:
        print(f'Found {len(matches)} chapters matching "{term}":')
        for (cid,) in matches:
            print(f'  {str(cid)[:50]}')

# Also check total question count
cur.execute('SELECT COUNT(*) FROM questions')
total = cur.fetchone()[0]
print(f'\nTotal questions in database: {total}')

# Check active count
cur.execute('SELECT COUNT(*) FROM questions WHERE is_active = true')
active = cur.fetchone()[0]
print(f'Total active questions: {active}')

# Check the specific chapter IDs we know about
known_chapters = {
    'basics-of-banking': '6a4df159-35a8-49d7-b764-55162b4cd75d',
    'rbi': '9c58e44b-e050-4dc6-be37-947a7ae98952',
    'types-of-accounts': 'a9a0ce3b-9d82-401e-8ed7-c73d0110c646',
    'inflation-and-monetary-policy': 'b4c19be3-102f-49ac-b51b-e2d8658af111',
    'types-of-banks': 'ab45d16e-b077-47cd-8302-9df5e14f2808',
}

print('\nKnown chapter IDs check:')
for name, cid in known_chapters.items():
    cur.execute('SELECT COUNT(*), COUNT(*) FILTER (WHERE is_active = true) FROM questions WHERE chapter_id = %s', (cid,))
    total, active = cur.fetchone()
    print(f'  {name}: total={total}, active={active}')

conn.close()