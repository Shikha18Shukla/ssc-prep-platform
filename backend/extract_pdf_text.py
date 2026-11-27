import fitz  # pyMuPDF
import os
import json
import re
from collections import defaultdict

# Chapter mapping from PDF filename keywords to database chapter keys
CHAPTER_MAPPING = {
    'Financial Market': 'financial-markets',
    'NPA': 'non-performing-assets',
    'BASEL and RISKS': 'basel-norms-and-banking-risks',
    'Banking Terminologies': 'banking-terminologies',
    'Bank Terminologies': 'banking-terminologies',
}

# PDFs to process from Downloads
pdf_files = [
    # Financial Market
    r'C:\Users\shikh\Downloads\Financial Market 01_Class Notes.pdf',
    r'C:\Users\shikh\Downloads\Financial Market 02_Class Notes.pdf',
    r'C:\Users\shikh\Downloads\Financial Market 03_Class Notes.pdf',
    r'C:\Users\shikh\Downloads\Financial Market 04_Class Notes.pdf',
    r'C:\Users\shikh\Downloads\Financial Market 05_Class Notes.pdf',
    r'C:\Users\shikh\Downloads\Financial Market 07_Class Notes.pdf',
    r'C:\Users\shikh\Downloads\Financial Market 08_Class Notes.pdf',
    r'C:\Users\shikh\Downloads\Financial Market 09_Class Notes.pdf',
    r'C:\Users\shikh\Downloads\Financial Market 10_Class Notes.pdf',
    # NPA
    r'C:\Users\shikh\Downloads\NPA 01_Class Notes.pdf',
    r'C:\Users\shikh\Downloads\NPA 02_Class Notes.pdf',
    r'C:\Users\shikh\Downloads\NPA 03_Class Notes.pdf',
    # Basel
    r'C:\Users\shikh\Downloads\BASEL and RISKS 01_Class Notes.pdf',
    r'C:\Users\shikh\Downloads\BASEL and RISKS 02_Class Notes.pdf',
    r'C:\Users\shikh\Downloads\BASEL and RISKS 03_Class Notes.pdf',
    r'C:\Users\shikh\Downloads\BASEL and RISKS 04_Class Notes.pdf',
    # Banking Terminologies
    r'C:\Users\shikh\Downloads\Bank Terminologies 01_Class Notes.pdf',
]

# Add any extra found PDFs
extra_dirs = [
    r'C:\Users\shikh\Desktop\ssc-prep-platform\backend\data\imports\general-banking-awareness',
    r'C:\Users\shikh\Desktop\Indian_Constitution_Temporal_QA\raw',
]
for extra_dir in extra_dirs:
    if os.path.exists(extra_dir):
        for f in os.listdir(extra_dir):
            if any(kw in f for kw in ['Financial', 'NPA', 'Basel', 'Bank Terminology']):
                full_path = os.path.join(extra_dir, f)
                if full_path not in pdf_files:
                    pdf_files.append(full_path)

print(f"Total PDFs to process: {len(pdf_files)}")

# ============================================================
# QUESTION EXTRACTION
# ============================================================

def extract_questions_from_pdf(text, chapter_name, filename, page_num):
    """Extract MCQs from PDF text content."""
    questions = []
    
    # Find potential question blocks by looking for numbered questions
    # Pattern: number followed by period/parenthesis, then question text
    question_starts = list(re.finditer(r'(?m)^\s*\d+[\.\)]\s', text))
    
    if len(question_starts) < 2:
        return questions
    
    for i in range(len(question_starts) - 1):
        start_idx = question_starts[i].start()
        end_idx = question_starts[i + 1].start()
        block_text = text[start_idx:end_idx].strip()
        
        if len(block_text) < 30 or len(block_text) > 1000:
            continue
        
        q = parse_question_block(block_text, chapter_name, filename, page_num)
        if q and q['question_text']:
            questions.append(q)
    
    # Process last block
    if question_starts:
        last_start = question_starts[-1].start()
        block_text = text[last_start:].strip()
        if len(block_text) >= 30 and len(block_text) <= 1000:
            q = parse_question_block(block_text, chapter_name, filename, page_num)
            if q and q['question_text']:
                questions.append(q)
    
    return questions


def parse_question_block(text, chapter_name, filename, page_num):
    """Parse a text block into a question dict."""
    try:
        # Remove leading number like "1." "2." etc
        cleaned = re.sub(r'^\s*\d+[\.\)]\s*', '', text, count=1)
        
        # Try to find options by looking for A) B) C) D) E) pattern in original text
        option_matches = re.findall(r'[A-E]\)\s+(.+?)(?:\n|$)', text)
        
        if len(option_matches) < 5:
            # Not enough options found with the simple pattern
            return None
        
        # We have at least 5 options, take the first 5
        options_texts = option_matches[:5]
        
        options = {}
        for i, opt_text in enumerate(options_texts):
            key = chr(65 + i)  # A, B, C, D, E
            options[key] = opt_text.strip()
        
        if len(options) != 5:
            return None
        
        # Extract question text - remove the options from the text
        # Get the question text by removing option patterns
        question_text = re.sub(r'[A-E]\)\s+.+?(\n|$)', '', text, flags=re.DOTALL)
        question_text = re.sub(r'^\s*\d+[\.\)]\s*', '', question_text).strip()
        
        if len(question_text) < 20 or len(question_text) > 500:
            return None
        
        # Determine correct answer
        correct_answer = None
        ans_match = re.search(r'Ans\.?\s*:\s*([A-E])', text, re.IGNORECASE)
        if ans_match:
            correct_answer = ans_match.group(1)
        else:
            # No explicit answer marker - mark for review
            correct_answer = 'A'
        
        # Build explanation
        explanation = ''
        expl_match = re.search(r'Explanation[:\s]+(.+?)(?:\n|$)', text, re.IGNORECASE)
        if expl_match:
            explanation = expl_match.group(1).strip()
        
        return {
            'question_text': question_text,
            'options': options,
            'correct_answer': correct_answer,
            'explanation': explanation,
            'chapter': chapter_name,
            'source_filename': filename,
            'page': page_num,
            'needs_review': correct_answer not in 'ABCDE',
        }
        
    except Exception as e:
        print(f"    Error: {e}")
        return None


# ============================================================
# PROCESS ALL PDFs
# ============================================================

all_questions = defaultdict(list)  # chapter_name -> [question_data]

for pdf_path in pdf_files:
    filename = os.path.basename(pdf_path)
    
    # Determine chapter from filename
    chapter_name = None
    for kw, ch_key in CHAPTER_MAPPING.items():
        if kw in filename:
            chapter_name = ch_key
            break
    
    if chapter_name is None:
        print(f"WARNING: Could not determine chapter for {filename}")
        continue
    
    print(f"\nProcessing: {filename} (chapter: {chapter_name})")
    
    try:
        doc = fitz.open(pdf_path)
        num_pages = len(doc)
        print(f"  Pages: {num_pages}")
        
        for page_num in range(num_pages):
            page = doc[page_num]
            text = page.get_text()
            
            # Extract questions from this page
            questions = extract_questions_from_pdf(text, chapter_name, filename, page_num + 1)
            
            for q in questions:
                all_questions[chapter_name].append(q)
        
        doc.close()
        print(f"  -> Extracted {len(questions)} questions from this PDF")
        
    except Exception as e:
        print(f"  ERROR processing {filename}: {e}")
        import traceback
        traceback.print_exc()

# ============================================================
# SUMMARY AND SAVE
# ============================================================

print("\n" + "=" * 60)
print("EXTRACTION SUMMARY")
print("=" * 60)
for chapter, questions in sorted(all_questions.items()):
    print(f"{chapter}: {len(questions)} questions extracted")

# Save extracted questions
output = {}
for chapter, questions in sorted(all_questions.items()):
    output[chapter] = [q.copy() for q in questions]
    # Remove internal fields before saving
    for q in output[chapter]:
        q.pop('needs_review', None)

with open('extracted_questions.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f"\nQuestions saved to extracted_questions.json")
print(f"Total chapters with questions: {len(all_questions)}")