"""Add section column to questions table for Current Affairs practice tests.

Revision ID: 0011_current_affairs_sections
Revises: 0010_banking_catalog
"""
from typing import Sequence, Union
import uuid

from alembic import op
import sqlalchemy as sa

revision: str = "0011_current_affairs_sections"
down_revision: Union[str, None] = "0010_banking_catalog"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add section column to questions table
    op.add_column("questions", sa.Column("section", sa.String, nullable=True))

    # Update all 444 Banking Clerk Current Affairs questions with section assignments
    # Section distribution: 50, 100, 150, 144
    # Questions are ordered by ID (deterministic)
    update_cases = [
        # (section_value, start_index, end_index)
        ("current_affairs_test_1", 0, 50),      # first 50 questions
        ("current_affairs_test_2", 50, 150),    # next 100 questions
        ("current_affairs_test_3", 150, 300),   # next 150 questions
        ("current_affairs_test_4", 300, 444),   # remaining 144 questions
    ]

    bind = op.get_bind()

    for section_name, start_idx, end_idx in update_cases:
        # Build CASE statement to set section based on question ID order position
        # We need to identify questions by their position in the ordered result set
        # Since we can't easily get the position, we'll update by ID range using a temp approach
        # 
        # Alternative: use a WHERE clause that matches the right IDs
        # Since questions are ordered by id, we can use position-based filtering
        # But UUIDs don't have natural ordering, so let's use a different approach:
        # We'll set the section for all CA questions, and the application will handle
        # the ordering. Since the assignment is deterministic based on the order questions
        # were fetched (ORDER BY id), we need a way to track position.
        #
        # Actually, the simplest approach: assign section based on the question's position
        # in the ordered list. Since we can't store position easily without a separate table,
        # let's just set the section column and rely on the application to query the right
        # questions. The section assignment itself is deterministic.
        #
        # Wait - I need a way to identify which questions get which section. 
        # Let me use a different approach: create a temporary ranking and update.
        
        # Actually, the most reliable approach: use ROW_NUMBER() over ORDER BY id
        # and update accordingly. But PostgreSQL doesn't support UPDATE with window 
        # functions directly in Alembic this way.
        
        # Let me use a simpler approach: since we know the exact count per section,
        # we can use the question IDs' order. But UUIDs are random, so we need another way.
        
        # Best approach: Create a ranking using a CTE and update from that.
        # However, Alembic raw SQL might be tricky. Let me use a different strategy.
        pass

    # Actually, let me take a simpler approach: assign section based on a 
    # deterministic hash/order of the question IDs. Since we already determined
    # the distribution offline, we need to persist it.
    #
    # The cleanest way: use a CTE with ROW_NUMBER and UPDATE.
    
    # For each section, we'll update questions whose ID appears in the first N,
    # next M, etc. based on ORDER BY id.
    # Since PostgreSQL's ORDER BY on UUID is arbitrary but consistent, we can use
    # the fact that the questions were already ordered by id when we distributed them.
    
    # Let me use a raw SQL approach with a CTE
    for section_name, start_idx, end_idx in update_cases:
        # Create a CTE that numbers questions by ORDER BY id, then update section
        # for the right range
        sql = text(f"""
            UPDATE questions
            SET section = '{section_name}'
            FROM (
                SELECT id, ROW_NUMBER() OVER (ORDER BY id) as rn
                FROM questions
                WHERE chapter_id = 'cf6ad0da-7cec-439c-a5f0-ede65dc39f29'
                  AND is_active = true
            ) sub
            WHERE questions.id = sub.id
              AND sub.rn > {start_idx}
              AND sub.rn <= {end_idx}
        """)
        bind.execute(sql)

    bind.commit()

    # Verify the update
    count = bind.execute(text("""
        SELECT section, COUNT(*) FROM questions
        WHERE chapter_id = 'cf6ad0da-7cec-439c-a5f0-ede65dc39f29'
          AND is_active = true
        GROUP BY section
    """)).fetchall()
    print("Section distribution after migration:")
    for row in count:
        print(f"  {row[0]}: {row[1]}")

    # Verify no NULL sections remain
    null_count = bind.execute(text("""
        SELECT COUNT(*) FROM questions
        WHERE chapter_id = 'cf6ad0da-7cec-439c-a5f0-ede65dc39f29'
          AND is_active = true
          AND section IS NULL
    """)).scalar_one()
    print(f"Questions with NULL section: {null_count}")


def downgrade() -> None:
    # Remove the section column and reset section assignments
    op.drop_column("questions", "section")