import psycopg2

conn = psycopg2.connect('postgresql://postgres@127.0.0.1:5432/ssc_prep')
cur = conn.cursor()

# Get all chapter IDs
cur.execute("SELECT chapter_id FROM questions ORDER BY chapter_id LIMIT 200")
all_cids = cur.fetchall()

# Terms to search for in chapter_id
search_terms = ['financial', 'basel', 'NPA', 'non-performing', 'banking-term', 'inflation', 'monetary']

print(f"Total chapters sampled: {len(all_cids)}")
print("\nChecking for new chapter keywords:")

found = set()
for (cid,) in all_cids:
    cid_str = str(cid).lower()
    for term in search_terms:
        if term in cid_str:
            found.add(term)
            break

for term in found:
    print(f"  Found '{term}' in some chapter IDs")

# Show all unique chapter_id prefixes (first 20 chars)
print("\nAll chapter ID prefixes (first 20):")
unique_prefixes = set()
for (cid,) in all_cids:
    unique_prefixes.add(str(cid)[:20])

for prefix in sorted(unique_prefixes)[:50]:
    print(f"  {prefix}")

conn.close()