import json
import os

# Check the OCR JSONL files structure
files = [
    r'C:\Users\shikh\Desktop\ssc-prep-platform\tmp\pdfs\general-banking-awareness\ocr_basics.jsonl',
    r'C:\Users\shikh\Desktop\ssc-prep-platform\tmp\pdfs\general-banking-awareness\ocr_rbi.jsonl',
    r'C:\Users\shikh\Desktop\ssc-prep-platform\tmp\pdfs\general-banking-awareness\ocr_accounts.jsonl',
    r'C:\Users\shikh\Desktop\ssc-prep-platform\tmp\pdfs\general-banking-awareness\ocr_inflation.jsonl',
]

for fpath in files:
    fname = os.path.basename(fpath)
    print(f"\n=== {fname} ===")
    count = 0
    with open(fpath) as fh:
        for line in fh:
            if count >= 2:
                print(f"  ... ({count} total lines so far)")
                break
            entry = json.loads(line.strip())
            text = entry.get('text', '')
            pdf = entry.get('pdf', '')
            page = entry.get('page', '')
            # Check if text contains actual question content
            has_options = any(c in text for c in ['A)', 'B)', 'C)', 'D)', 'E)'])
            has_question = '?' in text or 'Question' in text
            print(f"  pdf={pdf}, page={page}, text_start={repr(text[:80])}, has_options={has_options}, has_question={has_question}")
            count += 1
    print(f"  Total entries in this file: {count}")