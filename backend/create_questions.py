import psycopg2
import json
import uuid
from datetime import datetime

conn = psycopg2.connect('postgresql://postgres@127.0.0.1:5432/ssc_prep')
cur = conn.cursor()

# First, let's check the existing schema and chapter structure
print("=== Database Schema Check ===\n")

# Check questions table structure
cur.execute("""SELECT column_name, data_type 
               FROM information_schema.columns 
               WHERE table_name = 'questions' 
               ORDER BY ordinal_position""")
columns = cur.fetchall()
print("questions table columns:")
for col in columns:
    print(f"  {col[0]}: {col[1]}")

# Check question_options table structure
cur.execute("""SELECT column_name, data_type 
               FROM information_schema.columns 
               WHERE table_name = 'question_options' 
               ORDER BY ordinal_position""")
columns = cur.fetchall()
print("\nquestion_options table columns:")
for col in columns:
    print(f"  {col[0]}: {col[1]}")

# Check existing chapter IDs that are in use
cur.execute("SELECT DISTINCT chapter_id FROM questions ORDER BY chapter_id LIMIT 30")
chapters = cur.fetchall()
print(f"\nExisting chapter IDs ({len(chapters)}):")
for (cid,) in chapters:
    print(f"  {str(cid)[:50]}")

# Check what chapters have questions and counts
cur.execute("""
    SELECT chapter_id, COUNT(*) as total, 
           COUNT(*) FILTER (WHERE is_active = true) as active
    FROM questions 
    GROUP BY chapter_id 
    ORDER BY active DESC
""")
chapter_counts = cur.fetchall()
print(f"\nChapter question counts (top 30):")
for (cid, total, active) in chapter_counts[:30]:
    print(f"  {str(cid)[:30]}...: total={total}, active={active}")

conn.close()
print("\n=== Schema check complete ===")