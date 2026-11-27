import subprocess
import os
import re

print("=== Trying Windows Built-in OCR ===\n")

# Try to use comtypes or pywin32 to access Windows Media OCR
try:
    import win32com.client
    print("pywin32/win32com available")
    # Try to create the OCR engine
    try:
        ocr = win32com.client.CreateObject("Microsoft.Windows.Ocr.OcrEngine")
        print("Created OCR engine successfully")
    except Exception as e:
        print(f"Could not create OCR engine: {e}")
except ImportError:
    print("pywin32 not available")

# Try using subprocess to test if we can access OCR DLLs
print("\nChecking for OCR-related DLLs...")
result = subprocess.run(['dir', 'C:\\Windows\\System32\\msocr*.dll', '/b'], capture_output=True, text=True)
print(f"msocr DLLs: {result.stdout[:200] if result.stdout else 'not found'}")

# Check for Windows.Media.Ocr in COM
result2 = subprocess.run(['reg', 'query', 'HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\SideLoading\\Psf', '/v', 'AllowUnsignedApps'], capture_output=True, text=True)
print(f"Registry check: exit code {result2.returncode}")

# Try PIL + pytesseract with reasonable config
print("\n--- Testing pytesseract with different configs ---")
try:
    import pytesseract
    # Test with a simple image check - but we need actual PDF rendering first
    print("pytesseract imported successfully")
    
    # Check if there's a way to use tesseract data without full install
    tessdata_dirs = os.environ.get('TESSDATA_PREFIX', '')
    print(f"TESSDATA_PREFIX: {tessdata_dirs}")
    
except Exception as e:
    print(f"pytesseract error: {e}")

# Check if we can use PyPDF2 or other PDF tools to get more text
print("\n--- Checking PDF text extraction more carefully ---")
import fitz
pdf_path = r'C:\Users\shikh\Downloads\Financial Market 01_Class Notes.pdf'
doc = fitz.open(pdf_path)
for i in range(len(doc)):
    page = doc[i]
    text = page.get_text("dict")  # Get structured text
    # Look for blocks, lines, spans with text
    if 'blocks' in text:
        blocks = text['blocks']
        print(f"Page {i+1} has {len(blocks)} blocks")
        for block in blocks[:3]:  # Show first 3 blocks
            if 'lines' in block:
                for line in block['lines'][:2]:  # Show first 2 lines
                    if 'spans' in line:
                        for span in line['spans'][:1]:  # Show first span
                            text_str = span.get('text', '').strip()
                            if text_str and len(text_str) > 3:
                                print(f"  Span text: '{text_str}' (size: {span.get('size', 0)})")
doc.close()

# Try rendering page as image and checking for text
print("\n--- Rendering PDF page as surface ---")
doc = fitz.open(pdf_path)
page = doc[0]
# Render at high resolution
pix = page.get_pixmap(dpi=300)
# Save the image
pix.save(r'C:\Users\shikh\Desktop\ssc-prep-platform\tmp\fm_page1.jpg')
print(f"Rendered page 1 to image, size: {pix.width}x{pix.height}")
doc.close()