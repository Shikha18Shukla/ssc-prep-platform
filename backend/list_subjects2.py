import psycopg2

conn = psycopg2.connect('postgresql://postgres@127.0.0.1:5432/ssc_prep')
cur = conn.cursor()

# Check subjects table schema
cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'subjects' ORDER BY ordinal_position")
cols = cur.fetchall()
print("Subjects table columns:")
for col in cols:
    print(f"  {col[0]}")

# Get all subjects data
cur.execute("SELECT * FROM subjects ORDER BY id")
subjects = cur.fetchall()
print(f"\nTotal subjects: {len(subjects)}")
for row in subjects:
    print(f"  {row}")

conn.close()