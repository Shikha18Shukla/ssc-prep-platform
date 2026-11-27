import psycopg2

conn = psycopg2.connect('postgresql://postgres@127.0.0.1:5432/ssc_prep')
cur = conn.cursor()

# Check what subjects exist
cur.execute('SELECT id, name FROM subjects')
subjects = cur.fetchall()
print('All subjects:')
for (sid, sname) in subjects:
    print(f'  {sid}: {sname}')

# Get one subject ID to use
conn.close()