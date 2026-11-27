import fitz
import os

# Check all the new PDFs
pdf_paths = [
    r'C:\Users\shikh\Downloads\Financial Market 01_Class Notes.pdf',
    r'C:\Users\shikh\Downloads\Financial Market 02_Class Notes.pdf',
    r'C:\Users\shikh\Downloads\Financial Market 03_Class Notes.pdf',
    r'C:\Users\shikh\Downloads\Financial Market 04_Class Notes.pdf',
    r'C:\Users\shikh\Downloads\Financial Market 05_Class Notes.pdf',
    r'C:\Users\shikh\Downloads\Financial Market 07_Class Notes.pdf',
    r'C:\Users\shikh\Downloads\Financial Market 08_Class Notes.pdf',
    r'C:\Users\shikh\Downloads\Financial Market 09_Class Notes.pdf',
    r'C:\Users\shikh\Downloads\Financial Market 10_Class Notes.pdf',
    r'C:\Users\shikh\Downloads\NPA 01_Class Notes.pdf',
    r'C:\Users\shikh\Downloads\NPA 02_Class Notes.pdf',
    r'C:\Users\shikh\Downloads\NPA 03_Class Notes.pdf',
    r'C:\Users\shikh\Downloads\BASEL and RISKS 01_Class Notes.pdf',
    r'C:\Users\shikh\Downloads\BASEL and RISKS 02_Class Notes.pdf',
    r'C:\Users\shikh\Downloads\BASEL and RISKS 03_Class Notes.pdf',
    r'C:\Users\shikh\Downloads\BASEL and RISKS 04_Class Notes.pdf',
    r'C:\Users\shikh\Downloads\Bank Terminologies 01_Class Notes.pdf',
]

for path in pdf_paths:
    if os.path.exists(path):
        doc = fitz.open(path)
        total_text = ''
        for i in range(len(doc)):
            page = doc[i]
            text = page.get_text()
            total_text += text
        doc.close()
        name = os.path.basename(path)
        # Count lines with actual content
        lines = [l for l in total_text.split('\n') if l.strip()]
        print(f'{name}: {len(total_text)} total chars, {len(lines)} non-empty lines')
        if total_text.strip():
            print(f'  Text: {repr(total_text[:200])}')
        else:
            print(f'  No extractable text')
    else:
        name = os.path.basename(path)
        print(f'{name}: NOT FOUND')