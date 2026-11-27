#!/usr/bin/env python
import sys
sys.path.insert(0, r'C:\\Users\\shikh\\Desktop\\ssc-prep-platform\\backend')
import psycopg2
from sqlalchemy import text, create_engine

engine = create_engine('postgresql://postgres@127.0.0.1:5432/ssc_prep')

# Step 1: Add section column using raw psycopg2
conn = psycopg2.connect('postgresql://postgres@127.0.0.1:5432/ssc_prep')
conn.autocommit = True
cur = conn.cursor()

# Add section column
cur.execute("ALTER TABLE questions ADD COLUMN section VARCHAR")
print("1. Added section column to questions table")

# Step 2: Update section assignments using ROW_NUMBER over ORDER BY id
# We need to do this in a single transaction
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
conn.commit()
print("2. Updated section assignments")

# Step 3: Verify
cur.execute("""
    SELECT section, COUNT(*) FROM questions
    WHERE chapter_id = 'cf6ad0da-7cec-439c-a5f0-ede65dc39f29'
      AND is_active = true
    GROUP BY section
    ORDER BY section
""")
result = cur.fetchall()
print("3. Section distribution:")
for row in result:
    print(f"   {row[0]}: {row[1]}")

# Check for NULL
cur.execute("""
    SELECT COUNT(*) FROM questions
    WHERE chapter_id = 'cf6ad0da-7cec-439c-a5f0-ede65dc39f29'
      AND is_active = true
      AND section IS NULL
""")
null_result = cur.fetchone()[0]
print(f"4. Questions with NULL section: {null_result}")

# Check total
cur.execute("""
    SELECT COUNT(*) FROM questions
    WHERE chapter_id = 'cf6ad0da-7cec-439c-a5f0-ede65dc39f29'
      AND is_active = true
""")
total = cur.fetchone()[0]
print(f"5. Total active questions: {total}")

cur.close()
conn.close()

print("\\nMigration applied successfully!")