import psycopg2

conn = psycopg2.connect('postgresql://postgres@127.0.0.1:5432/ssc_prep')
cur = conn.cursor()

# Check chapters table
cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'chapters' ORDER BY ordinal_position")
cols = cur.fetchall()
print('chapters table columns:')
for col in cols:
    print(f'  {col[0]}: {col[1]}')

# Check if chapters table has data
cur.execute('SELECT COUNT(*) FROM chapters')
count = cur.fetchone()[0]
print(f'\nChapters table has {count} rows')

if count > 0:
    cur.execute('SELECT * FROM chapters LIMIT 5')
    rows = cur.fetchall()
    for row in rows:
        print(f'  {row}')

conn.close()