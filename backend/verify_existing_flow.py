#!/usr/bin/env python
import sys
sys.path.insert(0, r'C:\Users\shikh\Desktop\ssc-prep-platform\backend')
import psycopg2

conn = psycopg2.connect('postgresql://postgres@127.0.0.1:5432/ssc_prep')
cur = conn.cursor()

# Verify existing Banking chapter still has its questions
cur.execute("""
    SELECT chapter_id, COUNT(*) FROM questions 
    WHERE is_active = true 
    GROUP BY chapter_id 
    ORDER BY chapter_id
""")
chapter_counts = cur.fetchall()
print('Chapter question counts:')
for row in chapter_counts:
    print(f'  Chapter {row[0]}: {row[1]} questions')

# Verify Banking Clerk Current Affairs chapter has 444 questions
cur.execute("""
    SELECT COUNT(*) FROM questions 
    WHERE chapter_id = 'cf6ad0da-7cec-439c-a5f0-ede65dc39f29' 
    AND is_active = true
""")
ca_count = cur.fetchone()[0]
print(f'\\nBanking Clerk Current Affairs chapter questions: {ca_count}')

# Verify the old chapter has 0
cur.execute("""
    SELECT COUNT(*) FROM questions 
    WHERE chapter_id = '4c6d53e5-46b3-4f0a-a71a-e5696e4f70ed' 
    AND is_active = true
""")
old_count = cur.fetchone()[0]
print(f'Old chapter questions: {old_count}')

# Check a sample Banking chapter still works
cur.execute("""
    SELECT c.name, COUNT(q.id) FROM chapter c 
    JOIN questions q ON q.chapter_id = c.id 
    WHERE q.is_active = true 
    GROUP BY c.name 
    LIMIT 3
""")
bank_samples = cur.fetchall()
print('\\nSample Banking chapters:')
for row in bank_samples:
    print(f'  {row[0]}: {row[1]} questions')

print('\\nExisting flow verification complete!')
cur.close()
conn.close()