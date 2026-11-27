import json
import os

path = r'C:\Users\shikh\Desktop\ssc-prep-platform\backend\questions_import.json'
if os.path.exists(path):
    with open(path) as f:
        d = json.load(f)
    print(f'Total questions: {len(d["questions"])}')
    if d['questions']:
        q = d['questions'][0]
        print(f'Keys: {list(q.keys())}')
        print(f'correct_answer: {q.get("correct_answer")}')
        print(f'explanation: {q.get("explanation", "")[:50]}')
else:
    print('File not found')