import sys
sys.path.insert(0, r'C:\\Users\\shikh\\Desktop\\ssc-prep-platform\\backend')

from alembic import context
from sqlalchemy import create_engine, text

engine = create_engine('postgresql://postgres@127.0.0.1:5432/ssc_prep')

# Run the migration head
context = context.get_context()
context.configure(model=None, url=engine.url)

# Run upgrade
context.run_migrations()

# Or manually run the migration SQL
with engine.begin() as conn:
    # Add section column
    conn.execute(text("ALTER TABLE questions ADD COLUMN section VARCHAR"))
    
    # Now update the section assignments using a CTE with ROW_NUMBER
    # Questions are ordered by id, and we assign sections based on position
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
    conn.execute(text(update_sql))
    conn.commit()
    
    # Verify
    result = conn.execute(text("""
        SELECT section, COUNT(*) FROM questions
        WHERE chapter_id = 'cf6ad0da-7cec-439c-a5f0-ede65dc39f29'
          AND is_active = true
        GROUP BY section
        ORDER BY section
    """)).fetchall()
    print("Section distribution:")
    for row in result:
        print(f"  {row[0]}: {row[1]}")
    
    # Check for NULL
    null_result = conn.execute(text("""
        SELECT COUNT(*) FROM questions
        WHERE chapter_id = 'cf6ad0da-7cec-439c-a5f0-ede65dc39f29'
          AND is_active = true
          AND section IS NULL
    """)).scalar_one()
    print(f"Questions with NULL section: {null_result}")
    
    # Check total
    total = conn.execute(text("""
        SELECT COUNT(*) FROM questions
        WHERE chapter_id = 'cf6ad0da-7cec-439c-a5f0-ede65dc39f29'
          AND is_active = true
    """)).scalar_one()
    print(f"Total active questions: {total}")

print("Migration completed successfully!")