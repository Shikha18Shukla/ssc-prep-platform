#!/usr/bin/env python
import sys
sys.path.insert(0, r'C:\Users\shikh\Desktop\ssc-prep-platform\backend')
import psycopg2

conn = psycopg2.connect('postgresql://postgres@127.0.0.1:5432/ssc_prep')
cur = conn.cursor()

# Test 1: Verify section-filtered question counts
sections = ['current_affairs_test_1', 'current_affairs_test_2', 'current_affairs_test_3', 'current_affairs_test_4']
for section in sections:
    cur.execute(
        "SELECT COUNT(*) FROM questions WHERE chapter_id = %s AND is_active = true AND section = %s",
        ('cf6ad0da-7cec-439c-a5f0-ede65dc39f29', section)
    )
    count = cur.fetchone()[0]
    print(f'Section {section}: {count} questions')

# Test 2: Verify total
cur.execute(
    "SELECT COUNT(*) FROM questions WHERE chapter_id = %s AND is_active = true",
    ('cf6ad0da-7cec-439c-a5f0-ede65dc39f29',)
)
total = cur.fetchone()[0]
print(f'\\nTotal: {total} questions')

# Test 3: Verify no section overlap
for i, s1 in enumerate(sections):
    for s2 in sections[i+1:]:
        cur.execute(
            "SELECT COUNT(*) FROM questions WHERE section = %s AND section = %s AND is_active = true",
            (s1, s2)
        )
        overlap = cur.fetchone()[0]
        print(f'Overlap {s1} & {s2}: {overlap}')

# Test 4: Verify all sections have correct counts
s1 = db_count = 0  # We'll use the first method's results
print()
print('Verification:')
expected = {'current_affairs_test_1': 50, 'current_affairs_test_2': 100, 'current_affairs_test_3': 150, 'current_affairs_test_4': 144}
for section, expected_count in expected.items():
    cur.execute(
        "SELECT COUNT(*) FROM questions WHERE chapter_id = %s AND is_active = true AND section = %s",
        ('cf6ad0da-7cec-439c-a5f0-ede65dc39f29', section)
    )
    actual = cur.fetchone()[0]
    status = 'OK' if actual == expected_count else 'FAIL'
    print(f'  {section}: {actual} (expected {expected_count}) [{status}]')

cur.close()
conn.close()