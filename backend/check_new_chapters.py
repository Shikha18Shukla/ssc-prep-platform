import psycopg2

conn = psycopg2.connect('postgresql://postgres@127.0.0.1:5432/ssc_prep')
cur = conn.cursor()

# Check for new chapter names using LIKE
search_terms = ['financial', 'basel', 'NPA', 'non-performing', 'banking-term']
for term in search_terms:
    cur.execute(f"SELECT DISTINCT chapter_id FROM questions WHERE chapter_id LIKE '%{term}%'")
    matches = cur.fetchall()
    if matches:
        print(f"Found {len(matches)} chapters matching '{term}':")
        for (cid,) in matches:
            print(f"  {str(cid)[:50]}")

# Also check total questions per chapter to see the distribution
cur.execute("SELECT chapter_id, COUNT(*), COUNT(*) FILTER (WHERE is_active = true) FROM questions GROUP BY chapter_id ORDER BY COUNT(*) DESC LIMIT 30")
top_chapters = cur.fetchall()
print(f"\nTop 30 chapters by question count:")
for (cid, total, active) in top_chapters:
    print(f"  {str(cid)[:30]}...: total={total}, active={active}")

conn.close()