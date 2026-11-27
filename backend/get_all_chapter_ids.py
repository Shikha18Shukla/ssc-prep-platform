import psycopg2

conn = psycopg2.connect('postgresql://postgres@127.0.0.1:5432/ssc_prep')
cur = conn.cursor()

# Get all distinct chapter IDs
cur.execute("SELECT DISTINCT chapter_id FROM questions ORDER BY chapter_id")
all_cids = cur.fetchall()

print(f"Total distinct chapter IDs: {len(all_cids)}")

# Check for new chapter keywords
search_terms = ['financial', 'basel', 'NPA', 'non-performing', 'banking-term', 'inflation', 'monetary']
found_terms = set()

for (cid,) in all_cids:
    cid_str = str(cid).lower()
    for term in search_terms:
        if term in cid_str:
            found_terms.add(term)
            break

if found_terms:
    print(f"\nFound these search terms in chapter IDs: {found_terms}")
else:
    print("\nNone of the search terms (financial, basel, NPA, non-performing, banking-term, inflation, monetary) found in any chapter ID")

# Show all chapter IDs
print("\nAll chapter IDs:")
for i, (cid,) in enumerate(all_cids):
    print(f"  {i+1}. {str(cid)[:50]}")

conn.close()