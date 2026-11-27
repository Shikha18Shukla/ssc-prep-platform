import json
import os

files = [
    r'C:\Users\shikh\Desktop\ssc-prep-platform\tmp\pdfs\general-banking-awareness\ocr_basics.jsonl',
    r'C:\Users\shikh\Desktop\ssc-prep-platform\tmp\pdfs\general-banking-awareness\ocr_rbi.jsonl',
    r'C:\Users\shikh\Desktop\ssc-prep-platform\tmp\pdfs\general-banking-awareness\ocr_accounts.jsonl',
    r'C:\Users\shikh\Desktop\ssc-prep-platform\tmp\pdfs\general-banking-awareness\ocr_inflation.jsonl',
]

for f in files:
    print(f'\n=== {os.path.basename(f)} ===')
    count = 0
    with open(f) as fh:
        for line in fh:
            if count >= 3:
                print('  ... (more)')
                break
            entry = json.loads(line.strip())
            q_text = entry.get('question_text', '')[:80]
            opts = entry.get('options', [])
            ans = entry.get('correct_answer', '')
            print(f'  Q: {q_text}...')
            print(f'  Options: {opts}')
            print(f'  Answer: {ans}')
            count += 1