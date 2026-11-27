import psycopg2

conn = psycopg2.connect('postgresql://postgres@127.0.0.1:5432/ssc_prep')
cur = conn.cursor()

# Check all chapter IDs
cur.execute("SELECT DISTINCT chapter_id FROM questions")
cids = cur.fetchall()
print(f'Total chapter IDs: {len(cids)}')

# Look for any that might match the new chapter names
new_keys = ['financial', 'non-performing', 'basel', 'banking-terminology']
for (cid,) in cids:
    cid_str = str(cid).lower()
    for key in new_keys:
        if key in cid_str:
            print(f"FOUND: {cid_str[:40]}")

# If no matches, just show first 30
print("\nFirst 30 chapter IDs:")
for (cid,) in cids[:30]:
    print(f"  {str(cid)[:40]}")

conn.close()