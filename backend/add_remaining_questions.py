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

# Remaining questions to reach at least 40 per chapter
# Current: FM=38, NPA=34, Basel=33, BT=37
# Need: FM=2, NPA=6, Basel=7, BT=3 = 18 total

# Financial Markets: need 2 more questions
fm_remaining = [
    ("In which year was the Securities and Exchange Board of India (SEBI) established?",
     ["A) 1988", "B) 1992", "C) 1995", "D) 2000", "E) 1990"], "B",
     "SEBI was established in 1988 as a non-statutory body and was given statutory powers in 1992 under the SEBI Act, 1992.", "MEDIUM"),
    ("Which of the following is not a money market instrument?",
     ["A) Treasury Bill", "B) Commercial Paper", "C) Certificate of Deposit", "D) Government Bond", "E) Call Money"], "D",
     "Government Bonds are capital market instruments with long-term maturity, while Treasury Bills, Commercial Paper, Certificate of Deposit, and Call Money are money market instruments with short-term maturity (up to one year).", "MEDIUM"),
]

# NPA: need 6 more questions
npa_remaining = [
    ("The '5/180' NPA classification norm applies to", ["A) Short-term crops", "B) Long-term agriculture", "C) Corporate loans", "D) Personal loans", "E] Consumer loans"], "B",
     "For long-term agriculture, the NPA classification norm is interest or installment remaining unpaid for 2 harvest periods or 180 days, whichever is earlier.", "MEDIUM"),
    ("Which ratio measures the proportion of a bank's NPA to its total capital?",
     ["A) Gross NPA Ratio", "B) Net NPA Ratio", "C) NPA to Capital Ratio", "D) Capital Adequacy Ratio", "E) Provisioning Coverage Ratio"], "C",
     "NPA to Capital Ratio measures the proportion of NPAs relative to the bank's capital, indicating the bank's exposure to credit risk relative its capital base.", "MEDIUM"),
    ("Which of the following would NOT reduce NPAs?", ["A) Strict recovery measures", "B) One-time settlement", "C) Writing off loans without recovery", "D) Better credit appraisal"], "C",
     "Writing off loans without actual recovery does not reduce NPAs; it only removes them from the balance sheet temporarily. The asset still exists and may be reported again.", "MEDIUM"),
    ("The net NPA ratio is calculated by subtracting which from the gross NPA ratio?", ["A) Total provisions", "B) Interest accrued", "C) Capital", "D) Reserves", "E) Interest received"], "A",
     "Net NPA ratio = Gross NPA ratio - Total provisions. It indicates the actual exposure after accounting for provisions.", "MEDIUM"),
    ("Which of the following would improve a bank's NPA situation the most?", ["A) Relaxing CIBIL standards", "B) Strict credit appraisal", "C) Increasing sub-standard assets", "D) Reducing provisioning", "E) Writing off all debts"], "B",
     "Strict credit appraisal at the time of lending helps prevent NPAs from arising. Relaxed standards typically lead to higher NPAs.", "MEDIUM"),
]

# Basel: need 7 more questions
basel_remaining = [
    ("Basel III introduced the concept of global systemically important banks (G-SIBs). Which buffer is applied to G-SIBs over and above the standard capital requirements?",
     ["A) Conservation buffer", "B) Countercyclical capital buffer", "C) G-SIB buffer", "D) Countercyclical buffer"], "C",
     "The G-SIB (Global Systemically Important Banks) buffer is an additional capital requirement on top of the conservation buffer, ranging from 0.5% to 3.5% depending on the bank's systemic importance score.", "MEDIUM"),
    ("Basel III's leverage ratio requirement is expressed as a percentage of which metric?",
     ["A) Tier 1 capital", "B) Tier 2 capital", "C) Total assets", "D) Risk-weighted assets"], "C",
     "The Basel III leverage ratio (3%) is expressed as a percentage of total assets, providing a simple, non-risk-weighted measure to prevent excessive leverage.", "MEDIUM"),
    ("Which of the following statements about Basel III is correct?", ["A) It eliminates all risk-weights for trading book assets", "B) It introduces a non-risk-based leverage ratio", "C) It removes the requirement for liquidity coverage", "D) It reduces the minimum CET1 requirement to 2%"], "B",
     "Basel III introduces a non-risk-based leverage ratio (3% of total assets) as a supplementary measure to the risk-weighted capital requirements.", "MEDIUM"),
    ("The conservation buffer under Basel III was fully implemented by which year?", ["A) 2013", "B) 2015", "C) 2019", "D) 2022", "E) 2025"], "C",
     "The conservation buffer of 2.5% was fully implemented by January 1, 2019, bringing the total minimum CET1 requirement to 7% (4.5% + 2.5% conservation buffer).", "EASY"),
    ("Basel III's countercyclical capital buffer can be activated by which authority?", ["A) International Monetary Fund", "B) National supervisors", "C) Basel Committee", "D) World Bank"], "B",
     "The countercyclical capital buffer can be activated by national supervisors during periods of excessive credit growth to build resilience against systemic risks.", "EASY"),
    ("Which Basel accord first introduced the concept of liquidity risk regulation?", ["A) Basel I", "B) Basel II", "C) Basel III", "D) Basel IV"], "C",
     "Basel III introduced comprehensive liquidity risk regulation including LCR and NSFR, building on the foundation laid by Basel II's three-pillar framework.", "MEDIUM"),
]

# Banking Terminologies: need 3 more questions
bt_remaining = [
    ("Base Rate was replaced by MCLR effective April 1, 2016. What was the main reason for this change?",
     ["A) To increase bank profits", "B) To bring transparency in lending rates", "C) To reduce RBI's regulatory burden", "D) To align with international standards"], "B",
     "MCLR was introduced to replace the Base Rate system to determine the minimum lending rate for commercial banks, bringing transparency in lending rates based on marginal cost of funds.", "MEDIUM"),
    ("MCLR is internally determined by each bank but monitored by RBI. The minimum spread between MCLR and Base Rate was?", ["A) 0.5%", "B) 1%", "C) 2%", "D) 3%", "E) No minimum specified"], "B",
     "While MCLR is internally determined by each bank, RBI monitors the framework. The effective spread between MCLR and Base Rate typically ranges around 1% depending on the bank's cost structure.", "MEDIUM"),
    ("The 'Benchmark Prime Lending Rate' (BPLR) was replaced by Base Rate in which year?", ["A) 2008", "B) 2010", "C) 2012", "D) 2014", "E) 2016"], "B",
     "Base Rate was introduced by RBI effective July 1, 2010, replacing the Benchmark Prime Lending Rate (BPLR) system to bring transparency in lending rates.", "EASY"),
]

# Build all remaining questions with chapter assignments
all_remaining = []

fm_cid = chapter_ids['financial-markets']
for q, opts, correct, diff in fm_remaining:
    qid = str(uuid.uuid4())
    all_remaining.append({
        'id': qid,
        'chapter_id': fm_cid,
        'question_text': q,
        'explanation': '',
        'difficulty': diff,
        'is_pyq': False,
        'pyq_year': None,
        'pyq_exam_name': None,
        'source': 'original-practice',
        'is_active': True,
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'image_url': None,
        'options': opts,
        'correct_answer': correct,
    })

np_cid = chapter_ids['non-performing-assets']
for q, opts, correct, diff in npa_remaining:
    qid = str(uuid.uuid4())
    all_remaining.append({
        'id': qid,
        'chapter_id': np_cid,
        'question_text': q,
        'explanation': '',
        'difficulty': diff,
        'is_pyq': False,
        'pyq_year': None,
        'pyq_exam_name': None,
        'source': 'original-practice',
        'is_active': True,
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'image_url': None,
        'options': opts,
        'correct_answer': correct,
    })

bs_cid = chapter_ids['basel-norms-and-banking-risks']
for q, opts, correct, diff in basel_remaining:
    qid = str(uuid.uuid4())
    all_remaining.append({
        'id': qid,
        'chapter_id': bs_cid,
        'question_text': q,
        'explanation': '',
        'difficulty': diff,
        'is_pyq': False,
        'pyq_year': None,
        'pyq_exam_name': None,
        'source': 'original-practice',
        'is_active': True,
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'image_url': None,
        'options': opts,
        'correct_answer': correct,
    })

bt_cid = chapter_ids['banking-terminologies']
for q, opts, correct, diff in bt_remaining:
    qid = str(uuid.uuid4())
    all_remaining.append({
        'id': qid,
        'chapter_id': bt_cid,
        'question_text': q,
        'explanation': '',
        'difficulty': diff,
        'is_pyq': False,
        'pyq_year': None,
        'pyq_exam_name': None,
        'source': 'original-practice',
        'is_active': True,
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'image_url': None,
        'options': opts,
        'correct_answer': correct,
    })

print(f"Total remaining questions to import: {len(all_remaining)}")
print(f"  Financial Markets: {len(fm_remaining)}")
print(f"  NPA: {len(npa_remaining)}")
print(f"  Basel: {len(basel_remaining)}")
print(f"  Banking Terminologies: {len(bt_remaining)}")

imported = 0
for q in all_remaining:
    try:
        qid = q['id']
        cid = q['chapter_id']
        
        cur.execute("""INSERT INTO questions (id, chapter_id, question_text, explanation, difficulty, is_pyq, pyq_year, pyq_exam_name, source, is_active, created_at, updated_at, image_url) 
            VALUES (%s, %s::uuid, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
            qid, cid, q['question_text'], q['explanation'], q['difficulty'],
            q['is_pyq'], q['pyq_year'], q['pyq_exam_name'], q['source'],
            q['is_active'], q['created_at'], q['updated_at'], q['image_url']))
        
        # Insert options
        options = q['options']
        correct_answer = q['correct_answer']
        
        for idx, option_text in enumerate(options):
            option_key = chr(65 + idx)  # A, B, C, D, E
            is_correct = (option_key == correct_answer)
            
            cur.execute("""INSERT INTO question_options (id, question_id, option_key, option_text, display_order, is_correct) 
                VALUES (%s, %s, %s, %s, %s, %s)""", (
                str(uuid.uuid4()),
                qid,
                option_key,
                option_text,
                idx + 1,
                is_correct))
        
        imported += 1
    except Exception as e:
        print(f"Error: {type(e).__name__}: {str(e)[:150]}")
        conn.rollback()

conn.commit()

# Verify counts
print("\n" + "=" * 50)
print("VERIFICATION AFTER ADDITIONAL IMPORT")
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
    
    # Verify correct answer count
    cur.execute('''SELECT COUNT(*) FROM questions q JOIN question_options qo ON q.id = qo.question_id 
                   WHERE q.chapter_id = %s::uuid AND qo.is_correct = TRUE 
                   GROUP BY q.id HAVING COUNT(*) != 1''', (ch_id,))
    bad = cur.fetchall()
    print(f"  All have exactly 1 correct answer: {len(bad) == 0}")

conn.close()
print("\nAdditional import complete!")