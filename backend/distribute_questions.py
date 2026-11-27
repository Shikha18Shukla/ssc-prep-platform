import sys
sys.path.insert(0, r'C:\\Users\\shikh\\Desktop\\ssc-prep-platform\\backend')
from sqlalchemy import create_engine, func, select, text
from sqlalchemy.orm import Session
from app.models import Question

engine = create_engine('postgresql://postgres@127.0.0.1:5432/ssc_prep')
db = Session(engine)

# Get all 444 Banking Clerk Current Affairs questions ordered by ID for determinism
sql = text('SELECT id, question_text, explanation, source, difficulty FROM questions WHERE chapter_id = :cid AND is_active = true ORDER BY id')
results = db.execute(sql, {'cid': 'cf6ad0da-7cec-439c-a5f0-ede65dc39f29'}).fetchall()

print('Total questions:', len(results))
q_ids = [r[0] for r in results]

# Distribute with exact counts:
# Section 1: 50 questions, Section 2: 100 questions, Section 3: 150 questions, Section 4: 144 questions
# 50 + 100 + 150 + 144 = 444

section_names = ['current_affairs_test_1', 'current_affairs_test_2', 'current_affairs_test_3', 'current_affairs_test_4']
section_counts = [50, 100, 150, 144]

sections = {}
for i, name in enumerate(section_names):
    sections[name] = {
        'count': section_counts[i],
        'question_ids': q_ids[sum(section_counts[:i]):sum(section_counts[:i+1])],
        'start_idx': sum(section_counts[:i]),
        'end_idx': sum(section_counts[:i+1])
    }

# Verify counts
for name, data in sections.items():
    print(f"{name}: {len(data['question_ids'])} questions (expected {data['count']}) - start={data['start_idx']}, end={data['end_idx']}")

# Verify total unique IDs across all sections
all_ids = []
for name, data in sections.items():
    all_ids.extend(data['question_ids'])
unique_ids = set(all_ids)
print()
print('Total unique IDs across sections:', len(unique_ids))
print('Total IDs (with duplicates):', len(all_ids))

# Verify no duplicates across sections
for i, name1 in enumerate(section_names):
    for name2 in section_names[i+1:]:
        set1 = set(sections[name1]['question_ids'])
        set2 = set(sections[name2]['question_ids'])
        overlap = set1 & set2
        if overlap:
            print(f' OVERLAP between {name1} and {name2}: {len(overlap)} questions - IDs: {list(overlap)[:3]}')
        else:
            print(f' NO OVERLAP between {name1} and {name2}')

# Verify all 444 are used
if len(unique_ids) == 444:
    print('SUCCESS: All 444 unique question IDs distributed exactly once')
else:
    print('ERROR: Expected 444 unique IDs, got', len(unique_ids))

# Print first and last question ID in each section for verification
for name, data in sections.items():
    first_id = data['question_ids'][0]
    last_id = data['question_ids'][-1]
    print(f'{name}: first={first_id}, last={last_id}')

db.close()