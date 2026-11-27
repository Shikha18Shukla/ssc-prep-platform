import os

# Check for tessdata directory
tessdata_paths = [
    r'C:\Program Files\Tesseract-OCR\tessdata',
    r'C:\Users\shikh\AppData\Local\Tesseract-OCR\tessdata',
    r'C:\Users\shikh\AppData\Roaming\Tesseract-OCR\tessdata',
    r'C:\Program Files (x86)\Tesseract-OCR\tessdata',
]

for path in tessdata_paths:
    if os.path.exists(path):
        files = os.listdir(path)
        traineddata = [f for f in files if f.endswith('.traineddata')]
        print(f"Found tessdata at: {path}")
        print(f"  traineddata files: {traineddata[:5]}...")
    else:
        print(f"Tessdata not found at: {path}")

# Also check common locations
for drive in ['C:', 'D:']:
    tess = os.path.join(drive, 'Program Files', 'Tesseract-OCR', 'tessdata')
    if os.path.exists(tess):
        files = os.listdir(tess)
        tdd = [f for f in files if f.endswith('.traineddata')]
        print(f"Found on {drive}: {tdd[:5]}...")

# Check environment
print(f"\nTESSDATA_PREFIX env: {os.environ.get('TESSDATA_PREFIX', 'not set')}")

# Check if tesseract data is embedded somewhere
print("\nChecking for any OCR-related files in Python install...")
python_dir = os.path.dirname(os.__file__)
print(f"Python dir: {python_dir[:50]}...")