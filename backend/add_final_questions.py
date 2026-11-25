import psycopg2
import uuid
from datetime import datetime

conn = psycopg2.connect('postgresql://postgres@127.0.0.1:5432/ssc_prep')
cur = conn.cursor()

chapter_ids = {
    'financial-markets': 'a58ffad6-9e93-40bc-b1c1-77e815e3ad4c',
    'non-performing-assets': '414d8f88-db2b-443c-9c54-30482d72888b',
    'basel-norms-and-banking-risks': 'b182d7f6-6571-4a86-9701-8f9be761dd2e',
    'banking-terminologies': '50f681a6-be97-4b3e-b07d-f1f9380d4efd',
}

# Add remaining 2 FM questions
fm_questions = [
    ("In which year was the Securities and Exchange Board of India (SEBI) established?", ["A) 1988", "B) 1992", "C) 1995", "D) 2000", "E) 1990"], "B", "MEDIUM"),
    ("Which of the following is not a money market instrument?", ["A) Treasury Bill", "B) Commercial Paper", "C) Certificate of Deposit", "D) Government Bond", "E) Call Money"], "D", "MEDIUM"),
]

for q, opts, correct, diff in fm_questions:
    qid = str(uuid.uuid4())
    cur.execute("INSERT INTO questions (id, chapter_id, question_text, explanation, difficulty, is_pyq, pyq_year, pyq_exam_name, source, is_active, created_at, updated_at, image_url) VALUES (%s, %s::uuid, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (qid, chapter_ids['financial-markets'], q, '', diff, False, None, None, 'original-practice', True, datetime.now(), datetime.now(), None))
    for idx, option_text in enumerate(opts):
        option_key = chr(65 + idx)
        is_correct = (option_key == correct)
        cur.execute("INSERT INTO question_options (id, question_id, option_key, option_text, display_order, is_correct) VALUES (%s, %s, %s, %s, %s, %s)",
            (str(uuid.uuid4()), qid, option_key, option_text, idx+1, is_correct))

# Add remaining 6 NPA questions
npa_questions = [
    ("The '5/180' NPA classification norm applies to", ["A) Short-term crops", "B) Long-term agriculture", "C) Corporate loans", "D) Personal loans", "E) Consumer loans"], "B", "MEDIUM"),
    ("Which ratio measures the proportion of a bank's NPA to its total capital?", ["A) Gross NPA Ratio", "B) Net NPA Ratio", "C) NPA to Capital Ratio", "D) Capital Adequacy Ratio", "E) Provisioning Coverage Ratio"], "C", "MEDIUM"),
    ("Which of the following would NOT reduce NPAs?", ["A) Strict recovery measures", "B) One-time settlement", "C) Writing off loans without recovery", "D) Better credit appraisal"], "C", "MEDIUM"),
    ("The net NPA ratio is calculated by subtracting which from the gross NPA ratio?", ["A) Total provisions", "B) Interest accrued", "C) Capital", "D) Reserves", "E) Interest received"], "A", "MEDIUM"),
    ("Which of the following would improve a bank's NPA situation the most?", ["A) Relaxing CIBIL standards", "B) Strict credit appraisal", "C) Increasing sub-standard assets", "D) Reducing provisioning", "E) Writing off all debts"], "B", "MEDIUM"),
    ("Agricultural loans overdue for 90 days are classified as NPA. For short-term crops, the overdue period is:", ["A) 30 days", "B) 60 days", "C) 90 days", "D) 120 days", "E) 180 days"], "A", "EASY"),
]

for q, opts, correct, diff in npa_questions:
    qid = str(uuid.uuid4())
    cur.execute("INSERT INTO questions (id, chapter_id, question_text, explanation, difficulty, is_pyq, pyq_year, pyq_exam_name, source, is_active, created_at, updated_at, image_url) VALUES (%s, %s::uuid, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (qid, chapter_ids['non-performing-assets'], q, '', diff, False, None, None, 'original-practice', True, datetime.now(), datetime.now(), None))
    for idx, option_text in enumerate(opts):
        option_key = chr(65 + idx)
        is_correct = (option_key == correct)
        cur.execute("INSERT INTO question_options (id, question_id, option_key, option_text, display_order, is_correct) VALUES (%s, %s, %s, %s, %s, %s)",
            (str(uuid.uuid4()), qid, option_key, option_text, idx+1, is_correct))

# Add remaining 7 Basel questions
basel_questions = [
    ("Basel III introduced the concept of global systemically important banks (G-SIBs). Which buffer is applied to G-SIBs over and above the standard capital requirements?", ["A) Conservation buffer", "B) Countercyclical capital buffer", "C) G-SIB buffer", "D) Countercyclical buffer"], "C", "MEDIUM"),
    ("Basel III's leverage ratio requirement is expressed as a percentage of which metric?", ["A) Tier 1 capital", "B) Tier 2 capital", "C) Total assets", "D) Risk-weighted assets"], "C", "MEDIUM"),
    ("Which of the following statements about Basel III is correct?", ["A) It eliminates all risk-weights for trading book assets", "B) It introduces a non-risk-based leverage ratio", "C) It removes the requirement for liquidity coverage", "D) It reduces the minimum CET1 requirement to 2%"], "B", "MEDIUM"),
    ("The conservation buffer under Basel III was fully implemented by which year?", ["A) 2013", "B) 2015", "C) 2019", "D) 2022", "E) 2025"], "C", "EASY"),
    ("Basel III's countercyclical capital buffer can be activated by which authority?", ["A) International Monetary Fund", "B) National supervisors", "C) Basel Committee", "D) World Bank"], "B", "EASY"),
    ("Which Basel accord first introduced the concept of liquidity risk regulation?", ["A) Basel I", "B) Basel II", "C) Basel III", "D) Basel IV"], "C", "MEDIUM"),
    ("Basel III's minimum CET1 requirement of 4.5% plus conservation buffer of 2.5% equals what total minimum?", ["A) 2.5%", "B) 5%", "C) 7%", "D) 8%"], "C", "EASY"),
]

for q, opts, correct, diff in basel_questions:
    qid = str(uuid.uuid4())
    cur.execute("INSERT INTO questions (id, chapter_id, question_text, explanation, difficulty, is_pyq, pyq_year, pyq_exam_name, source, is_active, created_at, updated_at, image_url) VALUES (%s, %s::uuid, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (qid, chapter_ids['basel-norms-and-banking-risks'], q, '', diff, False, None, None, 'original-practice', True, datetime.now(), datetime.now(), None))
    for idx, option_text in enumerate(opts):
        option_key = chr(65 + idx)
        is_correct = (option_key == correct)
        cur.execute("INSERT INTO question_options (id, question_id, option_key, option_text, display_order, is_correct) VALUES (%s, %s, %s, %s, %s, %s)",
            (str(uuid.uuid4()), qid, option_key, option_text, idx+1, is_correct))

# Add remaining 3 BT questions
bt_questions = [
    ("Base Rate was replaced by MCLR effective April 1, 2016. What was the main reason for this change?", ["A) To increase bank profits", "B) To bring transparency in lending rates", "C) To reduce RBI's regulatory burden", "D) To align with international standards"], "B", "MEDIUM"),
    ("MCLR is internally determined by each bank but monitored by RBI. The minimum spread between MCLR and Base Rate was?", ["A) 0.5%", "B) 1%", "C) 2%", "D) 3%", "E) No minimum specified"], "B", "MEDIUM"),
    ("The 'Benchmark Prime Lending Rate' (BPLR) was replaced by Base Rate in which year?", ["A) 2008", "B) 2010", "C) 2012", "D) 2014", "E) 2016"], "B", "EASY"),
]

for q, opts, correct, diff in bt_questions:
    qid = str(uuid.uuid4())
    cur.execute("INSERT INTO questions (id, chapter_id, question_text, explanation, difficulty, is_pyq, pyq_year, pyq_exam_name, source, is_active, created_at, updated_at, image_url) VALUES (%s, %s::uuid, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (qid, chapter_ids['banking-terminologies'], q, '', diff, False, None, None, 'original-practice', True, datetime.now(), datetime.now(), None))
    for idx, option_text in enumerate(opts):
        option_key = chr(65 + idx)
        is_correct = (option_key == correct)
        cur.execute("INSERT INTO question_options (id, question_id, option_key, option_text, display_order, is_correct) VALUES (%s, %s, %s, %s, %s, %s)",
            (str(uuid.uuid4()), qid, option_key, option_text, idx+1, is_correct))

conn.commit()
print("Added 2 + 6 + 7 + 3 = 18 questions successfully!")

# Verify counts
print("\n" + "=" * 50)
print("FINAL VERIFICATION")
print("=" * 50)

for ch_slug, ch_id in chapter_ids.items():
    cur.execute('SELECT COUNT(*), COUNT(*) FILTER (WHERE is_active = true) FROM questions WHERE chapter_id = %s::uuid', (ch_id,))
    total, active = cur.fetchone()
    cur.execute('SELECT COUNT(*) FROM question_options WHERE question_id IN (SELECT id FROM questions WHERE chapter_id = %s::uuid)', (ch_id,))
    opts = cur.fetchone()[0]
    
    print(f"\n{ch_slug}:")
    print(f"  Total questions: {total}")
    print(f"  Active questions: {active}")
    print(f"  Option records: {opts}")
    
    cur.execute('''SELECT COUNT(*) FROM questions q JOIN question_options qo ON q.id = qo.question_id 
                   WHERE q.chapter_id = %s::uuid AND qo.is_correct = TRUE 
                   GROUP BY q.id HAVING COUNT(*) != 1''', (ch_id,))
    bad = cur.fetchall()
    print(f"  All have exactly 1 correct answer: {len(bad) == 0}")

conn.close()
print("\nDone!")