import os
import json

# Search for any question-related data files
search_terms = [
    'financial-market', 'financial market',
    'non-performing', 'NPA',
    'basel', 'basel norms',
    'banking-terminolog', 'banking terminology',
]

# Look in common project directories
search_dirs = [
    r'C:\Users\shikh\Desktop\ssc-prep-platform',
    r'C:\Users\shikh\Desktop\ssc-prep-platform\backend',
    r'C:\Users\shikh\Desktop\ssc-prep-platform\database',
    r'C:\Users\shikh\Desktop\ssc-prep-platform\data',
    r'C:\Users\shikh\Desktop\ssc-prep-platform\frontend',
    r'C:\Users\shikh\Desktop\ssc-prep-platform\question-bank',
]

print("=== Searching for existing question data ===\n")

for search_dir in search_dirs:
    if not os.path.exists(search_dir):
        continue
    print(f"\nSearching in: {search_dir}")
    for root, dirs, files in os.walk(search_dir):
        # Skip .git and __pycache__
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__']]
        for f in files:
            filepath = os.path.join(root, f)
            # Check if file contains search terms
            try:
                # Only check text/json files
                if f.endswith(('.json', '.jsonl', '.txt', '.md', '.csv', '.py')):
                    # Read first 5KB to check for terms
                    with open(filepath, 'r', errors='ignore') as fh:
                        content = fh.read(5000).lower()
                        for term in search_terms:
                            if term.lower() in content:
                                print(f"  {f}: found '{term}'")
            except:
                pass

# Also check the database directly
print("\n\n=== Checking database for existing chapters ===")
import psycopg2
try:
    conn = psycopg2.connect('postgresql://postgres@127.0.0.1:5432/ssc_prep')
    cur = conn.cursor()
    
    # Check if any of the new chapter IDs exist
    new_chapters = [
        'financial-markets',
        'non-performing-assets', 
        'basel-norms-and-banking-risks',
        'banking-terminologies',
    ]
    
    for chapter_key in new_chapters:
        # Try to find questions with chapter_id containing the key
        # First let's see what chapter IDs exist
        cur.execute("SELECT DISTINCT chapter_id FROM questions LIMIT 20")
        all_chapters = cur.fetchall()
        
        # Check if any match our new chapters
        matching = []
        for (cid,) in all_chapters:
            cid_str = str(cid).lower()
            for key in new_chapters:
                if key in cid_str:
                    matching.append((cid_str, key))
        
        if matching:
            print(f"Found matching chapter IDs for '{chapter_key}':")
            for cid_str, key in matching[:5]:
                # Get counts
                cur.execute('SELECT COUNT(*), COUNT(*) FILTER (WHERE is_active = true) FROM questions WHERE chapter_id = %s', (cid_str,))
                total, active = cur.fetchone()
                print(f"  {cid_str[:20]}...: total={total}, active={active}")
        else:
            print(f"No chapter IDs matching '{chapter_key}' found in database")
    
    # Also just list all distinct chapter_id prefixes
    cur.execute("SELECT DISTINCT chapter_id FROM questions")
    all_cids = cur.fetchall()
    print(f"\nAll chapter IDs in database ({len(all_cids)}):")
    for (cid,) in all_cids:
        print(f"  {str(cid)[:30]}...")
    
    conn.close()
except Exception as e:
    print(f"Database error: {e}")

# Check the verified_batch.json for chapter distribution
print("\n\n=== Checking verified_batch.json chapter distribution ===")
try:
    with open(r'C:\Users\shikh\Desktop\ssc-prep-platform\backend\data\imports\general-banking-awareness\verified_batch.json') as f:
        data = json.load(f)
    print(f"Total questions: {len(data['questions'])}")
    print(f"Chapter counts: {data.get('chapter_counts', 'N/A')}")
    
    # Count by chapter_id prefix
    from collections import Counter
    ch_counts = Counter()
    for q in data['questions']:
        cid = q['chapter_id']
        ch_counts[cid] += 1
    for cid, count in ch_counts.most_common():
        print(f"  {cid[:8]}...: {count}")
except Exception as e:
    print(f"Error: {e}")