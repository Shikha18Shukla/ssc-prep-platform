import os

# First, let's explore the PDFs the user mentioned
pdf_dirs = [
    r'C:\Users\shikh\Desktop\ssc-prep-platform\backend\data\imports\general-banking-awareness',
    r'C:\Users\shikh\Desktop\Indian_Constitution_Temporal_QA\raw',
    r'C:\Users\shikh\Desktop\Indian_Constitution_Temporal_QA\raw\sources',
    r'C:\Users\shikh\Desktop\Indian_Constitution_Temporal_QA\raw\constitution',
]

# Also check the downloads folder mentioned
downloads = r'C:\Users\shikh\Downloads'

# Check what's in the downloads folder
downloads_pdfs = []
if os.path.exists(downloads):
    for f in os.listdir(downloads):
        if f.endswith('.pdf'):
            downloads_pdfs.append(f)
    print(f"PDFs in Downloads: {downloads_pdfs}")
else:
    print("Downloads folder not found")

# Check the Indian Constitution directory
for d in pdf_dirs:
    if os.path.exists(d):
        print(f"\n{d}:")
        pdf_count = 0
        for root, dirs, files in os.walk(d):
            for f in files:
                if f.endswith('.pdf'):
                    pdf_count += 1
                    full_path = os.path.join(root, f)
                    print(f"  {f} ({os.path.getsize(full_path)} bytes)")
        print(f"  Total PDFs in this dir: {pdf_count}")
    else:
        print(f"\n{d}: NOT FOUND")