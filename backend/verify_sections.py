#!/usr/bin/env python
import psycopg2

conn = psycopg2.connect('postgresql://postgres@127.0.0.1:5432/ssc_prep')
conn.autocommit = True
cur = conn.cursor()

# Check if section column exists
cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name='questions' AND column_name='section'")
if cur.fetchone():
    print("Section column already exists")
else:
    cur.execute("ALTER TABLE questions ADD COLUMN section VARCHAR")
    print("Added section column")

# Update section assignments using ROW_NUMBER over ORDER BY id
update_sql = """
    UPDATE questions
    SET section = sub.section
    FROM (
        SELECT id,
            CASE
                WHEN ROW_NUMBER() OVER (ORDER BY id) > 0 AND ROW_NUMBER() OVER (ORDER BY id) <= 50 THEN 'current_affairs_test_1'
                WHEN ROW_NUMBER() OVER (ORDER BY id) > 50 AND ROW_NUMBER() OVER (ORDER BY id) <= 150 THEN 'current_affairs_test_2'
                WHEN ROW_NUMBER() OVER (ORDER BY id) > 150 AND ROW_NUMBER() OVER (ORDER BY id) <= 300 THEN 'current_affairs_test_3'
                ELSE 'current_affairs_test_4'
            END as section
        FROM questions
        WHERE chapter_id = 'cf6ad0da-7cec-439c-a5f0-ede65dc39f29'
          AND is_active = true
    ) sub
    WHERE questions.id = sub.id
"""
cur.execute(update_sql)
print("Updated section assignments")

# Verify
cur.execute("""
    SELECT section, COUNT(*) FROM questions
    WHERE chapter_id = 'cf6ad0da-7cec-439c-a5f0-ede65dc39f29'
      AND is_active = true
    GROUP BY section
    ORDER BY section
""")
result = cur.fetchall()
print("Section distribution:")
for row in result:
    print("  " + str(row[0]) + ": " + str(row[1]))

# Check for NULL
cur.execute("""
    SELECT COUNT(*) FROM questions
    WHERE chapter_id = 'cf6ad0da-7cec-439c-a5f0-ede65dc39f29'
      AND is_active = true
      AND section IS NULL
""")
null_result = cur.fetchone()[0]
print("Questions with NULL section: " + str(null_result))

# Check total
cur.execute("""
    SELECT COUNT(*) FROM questions
    WHERE chapter_id = 'cf6ad0da-7cec-439c-a5f0-ede65dc39f29'
      AND is_active = true
""")
total = cur.fetchone()[0]
print("Total active questions: " + str(total))

# Verify counts
sections = {}
for row in result:
    sections[row[0]] = row[1]

s1 = sections.get('current_affairs_test_1', 0)
s2 = sections.get('current_affairs_test_2', 0)
s3 = sections.get('current_affairs_test_3', 0)
s4 = sections.get('current_affairs_test_4', 0)

print("\nSection 1 (current_affairs_test_1): " + str(s1) + " (expected 50)")
print("Section 2 (current_affairs_test_2): " + str(s2) + " (expected 100)")
print("Section 3 (current_affairs_test_3): " + str(s3) + " (expected 150)")
print("Section 4 (current_affairs_test_4): " + str(s4) + " (expected 144)")
print("Total: " + str(s1+s2+s3+s4) + " (expected 444)")

if s1 == 50 and s2 == 100 and s3 == 150 and s4 == 144 and (s1+s2+s3+s4) == 444:
    print("\nAll section counts are correct!")
else:
    print("Section counts mismatch!")

cur.close()
conn.close()