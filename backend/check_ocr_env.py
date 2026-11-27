import subprocess
import os
import re

print("=== OCR Environment Check ===\n")

# 1. Check tesseract location
result = subprocess.run(['where', 'tesseract'], capture_output=True, text=True)
print(f"1. tesseract location: {result.stdout.strip() if result.stdout else 'NOT FOUND'}")

# 2. Check pip packages for OCR
result3 = subprocess.run(['pip', 'list'], capture_output=True, text=True)
packages = result3.stdout.lower().split('\n')
ocr_pkgs = [p.split('==')[0].strip() for p in packages if 'ocr' in p.lower()]
print(f"2. OCR packages in pip: {ocr_pkgs if ocr_pkgs else 'none'}")

# 3. Check environment variables
tesseract_path = os.environ.get('TESSDATA_PREFIX', 'not set')
print(f"3. TESSDATA_PREFIX: {tesseract_path}")

# 4. Check pytesseract
try:
    import pytesseract
    print(f"4. pytesseract available: YES")
    try:
        version = pytesseract.get_tesseract_version()
        print(f"   tesseract version: {version}")
    except Exception as e:
        print(f"   tesseract version: ERROR - {str(e)[:200]}")
except ImportError:
    print(f"4. pytesseract available: NO")

# 5. List all installed packages related to OCR/image
result4 = subprocess.run(['pip', 'list'], capture_output=True, text=True)
all_pkgs = result4.stdout.lower().split('\n')
image_pkgs = [p.split('==')[0].strip() for p in all_pkgs if any(kw in p for kw in ['easy', 'paddle', 'onnx', 'rapid', 'tesser', 'ocr', 'image'])]
print(f"5. Image/OCR-related packages: {image_pkgs if image_pkgs else 'none'}")

# 6. Try Windows built-in OCR check
print(f"6. Windows Media Ocr: requires admin rights / not available in user space")

print("\n=== End of Check ===")