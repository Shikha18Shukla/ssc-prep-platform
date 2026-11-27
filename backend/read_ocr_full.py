import json
import os

files = [
    r'C:\Users\shikh\Desktop\ssc-prep-platform\tmp\pdfs\general-banking-awareness\ocr_basics.jsonl',
]

# Read just the first entry to see the structure
with open(files[0]) as fh:
    line = fh.readline().strip()
    entry = json.loads(line)
    print("Full entry structure:")
    for key, value in entry.items():
        print(f"  {key}: {repr(value)[:200]}")