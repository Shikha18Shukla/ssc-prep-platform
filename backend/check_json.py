import json
import os

path = r'C:\Users\shikh\Desktop\ssc-prep-platform\backend\questions_import.json'
if os.path.exists(path):
    with open(path) as f:
        d = json.load(f)
    print(f'File exists with {len(d["questions"])} questions')
    # Show first question chapter_id
    q = d['questions'][0]
    print(f'First question chapter_id: {q["chapter_id"]}')
    print(f'First question correct_answer: {q["correct_answer"]}')
    print(f'First question difficulty: {q["difficulty"]}')
else:
    print('File not found')