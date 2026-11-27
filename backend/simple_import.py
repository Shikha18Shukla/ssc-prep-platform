import psycopg2
import uuid
from datetime import datetime

conn = psycopg2.connect('postgresql://postgres@127.0.0.1:5432/ssc_prep')
cur = conn.cursor()

# Use existing chapter IDs from the database (General/Banking Awareness subject)
chapter_ids = {
    'financial-markets': 'a58ffad6-9e93-40bc-b1c1-77e815e3ad4c',
    'non-performing-assets': '414d8f88-db2b-443c-9c54-30482d72888b',
    'basel-norms-and-banking-risks': 'b182d7f6-6571-4a86-9701-8f9be761dd2e',
    'banking-terminologies': '50f681a6-be97-4b3e-b07d-f1f9380d4efd',
}

# Define all questions as tuples: (question_text, options_list, correct_answer, difficulty)
# Financial Markets: 15 questions
fm_questions = [
    ("In which year was the Securities and Exchange Board of India (SEBI) established?",
     ["A) 1988", "B) 1992", "C) 1995", "D) 2000", "E) 1990"], "B", "MEDIUM"),
    ("Which of the following is not a money market instrument?",
     ["A) Treasury Bill", "B) Commercial Paper", "C) Certificate of Deposit", "D) Government Bond", "E) Call Money"], "D", "MEDIUM"),
    ("The red ink used in a bank's Balance Sheet indicates",
     ["A) Profits", "B) Losses", "C) Capital", "D) Liabilities", "E) Assets"], "B", "EASY"),
    ("Which committee recommended the introduction of New Banking Technology in India?",
     ["A) Khan Committee", "B) Narasimham Committee", "C) Mukherjee Committee", "D) Deshmukh Committee", "E) Selvam Committee"], "B", "MEDIUM"),
    ("The Indian financial system is supervised by which of the following?",
     ["A) SEBI only", "B) RBI only", "C) SEBI and RBI", "D) SEBI, RBI and IRDA", "E) Ministry of Finance"], "C", "MEDIUM"),
    ("Which of the following is the primary objective of the Reserve Bank of India?",
     ["A) Maximize profits", "B) Control inflation", "C) Issue currency and manage foreign exchange", "D) Provide loans to farmers", "E) Regulate stock markets"], "C", "EASY"),
    ("The facility that allows banks to borrow money from other banks on an overnight basis is called",
     ["A) Repo Rate", "B) Reverse Repo Rate", "C) Call Money Rate", "D) Bank Rate", "E) MSF Rate"], "C", "EASY"),
    ("Which of the following instruments is issued by the Government of India to borrow money from the public for a period of 7 to 10 years?",
     ["A) Treasury Bill", "B) State Development Loan", "C) National Savings Certificate", "D) Kisan Vikas Patra", "E) Government Bond"], "B", "MEDIUM"),
    ("The full form of 'AMC' in the context of mutual funds is?",
     ["A) Asset Management Company", "B) Automated Money Counter", "C) Account Management Commission", "D) Asset Monitoring Committee", "E) Aggregate Market Capitalization"], "A", "EASY"),
    ("Which of the following is considered a 'primary market' instrument?",
     ["A) Equity Shares (IPO)", "B) Public Trading of Shares", "C) Secondary Market Trading", "D) Stock Exchange Trading", "E) Option Trading"], "A", "MEDIUM"),
    ("The 'Lender of Last Resort' function is performed by?",
     ["A) Commercial Banks", "B) SEBI", "C) Reserve Bank of India", "D) NABARD", "E) SIDBI"], "C", "MEDIUM"),
    ("Which of the following is not a function of the Securities and Exchange Board of India (SEBI)?",
     ["A) Regulate stock exchanges", "B) Protect investors", "C) Issue government bonds", "D) Regulate mutual funds", "E) Register intermediaries"], "C", "MEDIUM"),
    ("The base rate system in Indian banks was introduced based on recommendations of?",
     ["A) Narasimham I Committee", "B) Narasimham II Committee", "C) Kelkar Committee", "D) Raghuram Rajan Committee", "E) Urjit Patel Committee"], "B", "MEDIUM"),
    ("Which of the following is the primary function of a commercial bank?",
     ["A) Issue currency", "B) Accept deposits and lend", "C) Regulate money supply", "D) Set bank rates", "E) Supervise financial markets"], "B", "EASY"),
    ("SEBI was established in which year?",
     ["A) 1987", "B) 1988", "C) 1989", "D) 1990", "E) 1991"], "B", "EASY"),
]

# NPA: 13 questions
npa_questions = [
    ("An asset is classified as Non-Performing Asset (NPA) if the interest or principal remains overdue for a period of",
     ["A) 30 days", "B) 60 days", "C) 90 days", "D) 120 days", "E) 180 days"], "C", "EASY"),
    ("Which of the following is not a type of NPA?",
     ["A) Sub-standard Asset", "B) Doubtful Asset", "C) Loss Asset", "D) Bad Bank", "E) Standard Asset"], "E", "MEDIUM"),
    ("The act of transferring NPAs from one bank to another is called",
     ["A) Debt Securitization", "B) Asset Securitization", "C) Novation", "D) Assignment", "E) Transfer"], "D", "MEDIUM"),
    ("Under the SARFAESI Act, 2002, banks can recover NPAs without the intervention of",
     ["A) Debt Recovery Tribunal", "B) SARFAESI Act", "C) Consumer Forum", "D) Court"], "A", "MEDIUM"),
    ("Which of the following is the typical provisioning percentage for sub-standard assets?",
     ["A) 25%", "B) 30%", "C) 40%", "D) 15%", "E) 50%"], "B", "MEDIUM"),
    ("Resolution of NPA through one-time settlement is typically done with",
     ["A) Full recovery", "B) 50-70% recovery", "C) 80-90% recovery", "D) 100% recovery", "E) No recovery"], "B", "MEDIUM"),
    ("Credit facilities granted by a bank for agriculture and allied activities that remain overdue for 90 days are classified as NPA under",
     ["A) Agriculture Advance", "B) Priority Sector Lending", "C) NPA Classification", "D) Farm Credit", "E) Rural Credit"], "A", "MEDIUM"),
    ("The NPA ratio (NPAs to Total Advances) of a bank indicates its",
     ["A) Profitability", "B) Liquidity", "C) Asset Quality", "D) Capital Adequacy", "E) Operational Efficiency"], "C", "MEDIUM"),
    ("Which of the following would improve a bank's NPA situation?",
     ["A) Relaxing CIBIL standards", "B) Strict credit appraisal", "C) Increasing sub-standard assets", "D) Reducing provisioning", "E) Writing off all debts"], "B", "MEDIUM"),
    ("Under the 'Pradhan Mantri Mudra Yojana', loans are given in which categories?",
     ["A) Shishu, Kishore and Tarun", "B) Small, Medium and Large", "C) Gold, Silver and Platinum", "D) Primary, Secondary and Tertiary", "E) Micro and Macro"], "A", "EASY"),
    ("The '5/180' NPA classification norm applies to",
     ["A) Short-term crops", "B) Long-term agriculture", "C) Corporate loans", "D) Personal loans", "E] Consumer loans"], "B", "MEDIUM"),
    ("Which ratio measures the proportion of a bank's NPA to its total capital?",
     ["A) Gross NPA Ratio", "B) Net NPA Ratio", "C) NPA to Capital Ratio", "D) Capital Adequacy Ratio", "E) Provisioning Coverage Ratio"], "C", "MEDIUM"),
    ("Which of the following would NOT reduce NPAs?",
     ["A) Strict recovery measures", "B) One-time settlement", "C) Writing off loans without recovery", "D) Better credit appraisal"], "C", "MEDIUM"),
]

# Basel: 13 questions - all MEDIUM or EASY difficulty
basel_questions = [
    ("Basel III norms were issued by the Basel Committee on Banking Supervision in",
     ["A) 2004", "B) 2008", "C) 2010", "D) 2013", "E) 2015"], "D", "EASY"),
    ("Basel III primarily aims to strengthen which three aspects of banking regulation?",
     ["A) Capital, Liquidity, and Leverage", "B) Capital, Profitability, and Liquidity", "C) Leverage, Solvency, and Profitability", "D) Capital, Risk Management, and Auditing", "E) Liquidity, Solvency, and Capital"], "A", "MEDIUM"),
    ("Common Equity Tier 1 (CET1) capital primarily consists of?",
     ["A) Hybrid instruments", "B) Subordinated debt", "C) Common shares and retained earnings", "D) Preferred shares", "E] Bonds"], "C", "MEDIUM"),
    ("The minimum Common Equity Tier 1 capital ratio under Basel III is?",
     ["A) 2%", "B) 4.5%", "C) 6%", "D) 8%", "E] 10%"], "B", "MEDIUM"),
    ("Liquidity Coverage Ratio (LCR) under Basel III requires banks to maintain adequate liquid assets to withstand",
     ["A) 30 days of stressed liquidity scenario", "B) 90 days of stress", "C) 1 year of stress", "D) 1 month of normal operations", "E] 6 months of stress"], "A", "MEDIUM"),
    ("Net Stable Funding Ratio (NSFR) requires a minimum ratio of stable funding to required stable funding of at least",
     ["A) 90%", "B) 100%", "C) 110%", "D) 125%", "E] 150%"], "B", "MEDIUM"),
    ("Basel III introduced a leverage ratio to restrict the",
     ["A) Total risk-weighted assets", "B) Amount of lending", "C) Overall exposure of the bank", "D) Capital adequacy ratio", "E] Loan-to-deposit ratio"], "C", "MEDIUM"),
    ("Risk-weighted assets (RWA) in Basel III are calculated based on?",
     ["A) Total assets of the bank", "B) Credit risk only", "C) Risk profiles of counterparties and assets", "D) Market risk only", "E] Operational risk only"], "C", "MEDIUM"),
    ("The countercyclical capital buffer under Basel III is designed to",
     ["A) Protect against housing bubbles only", "B) Be activated during systemic stress", "C) Replace the conservation buffer", "D) Apply only to foreign banks", "E] Limit dividend payments permanently"], "B", "MEDIUM"),
    ("Which of the following is NOT a Basel III capital instrument?",
     ["A) Common Equity Tier 1", "B) Additional Tier 1", "C) Tier 2", "D) Tier 3", "E] All are Basel III instruments"], "D", "MEDIUM"),
    ("The output floor under Basel III limits the benefit of risk-weight reductions, requiring banks to hold at least",
     ["A) 50% of standardized RWA", "B) 65% of standardized RWA", "C) 72.5% of standardized RWA", "D) 75% of standardized RWA", "E] 80% of standardized RWA"], "C", "MEDIUM"),
    ("Basel II norms were issued in which year?",
     ["A) 1999", "B) 2004", "C) 2010", "D) 2013", "E] 2015"], "B", "EASY"),
    ("Which of the following Basel Accords introduced the concept of Capital Adequacy Ratio (CAR)?",
     ["A) Basel I", "B) Basel II", "C) Basel III", "D) Basel IV", "E] None of the above"], "A", "EASY"),
]

# Banking Terminologies: 15 questions - no apostrophes in option texts
bt_questions = [
    ("CRR (Cash Reserve Ratio) refers to the percentage of bank deposits that banks must maintain with",
     ["A) SEBI", "B) RBI", "C) NABARD", "D) Commercial Banks", "E) Government"], "B", "EASY"),
    ("SLR (Statutory Liquidity Ratio) refers to the percentage of bank deposits that banks must maintain in",
     ["A) Cash with RBI", "B) Gold or approved securities", "C) Foreign currency", "D) Corporate bonds", "E] Government bonds only"], "B", "EASY"),
    ("The difference between CRR and SLR is that CRR is maintained with",
     ["A) Commercial Banks", "B) RBI", "C) Government", "D) SEBI", "E) NABARD"], "B", "EASY"),
    ("Repo Rate is the rate at which RBI lends money to banks against",
     ["A) Government Securities", "B) Corporate Bonds", "C) Foreign Exchange", "D) Gold", "E] Shares"], "A", "EASY"),
    ("Reverse Repo Rate is the rate at which RBI borrows money from banks against",
     ["A) Government Securities", "B) Corporate Bonds", "C) Foreign Exchange", "D) Gold", "E] Shares"], "A", "EASY"),
    ("Marginal Standing Facility (MSF) rate is pegged at",
     ["A) Repo Rate", "B) Reverse Repo Rate", "C) 1% above Repo Rate", "D) 2% above Repo Rate", "E] Bank Rate"], "C", "MEDIUM"),
    ("Bank Rate is the rate at which RBI rediscounts bills of exchange with",
     ["A) Commercial Banks", "B) Cooperative Banks", "C) State Governments", "D) Financial Institutions", "E] All of the above"], "E", "MEDIUM"),
    ("Open Market Operations (OMO) refer to",
     ["A) Trading in stock markets", "B) RBI buying/selling government securities", "C) Banking ombudsman actions", "D) Bank marketing activities", "E] Online money transfers"], "B", "EASY"),
    ("The 'Marginal Cost of Funds based Lending Rate' (MCLR) was introduced in",
     ["A) 2010", "B) 2012", "C) 2016", "D) 2018", "E] 2020"], "C", "MEDIUM"),
    ("MCLR is determined by the",
     ["A) Government of India", "B) Finance Ministry", "C) Individual Banks", "D) Reserve Bank of India", "E] Indian Banks Association"], "C", "MEDIUM"),
    ("Base Rate was the lending rate system introduced by RBI in",
     ["A) 2003", "B) 2007", "C) 2010", "D) 2014", "E] 2018"], "C", "EASY"),
    ("The 'Prime Lending Rate' (PLR) is the rate charged by banks to their",
     ["A) Best customers", "B) Small customers", "C) All customers equally", "D) Corporate customers", "E] Priority sector customers"], "A", "EASY"),
    ("Call Money Market is a market for",
     ["A) Long-term loans", "B) Overnight borrowing/lending", "C) Government securities", "D) Corporate bonds", "E] Foreign exchange"], "B", "EASY"),
    ("Certificate of Deposit (CD) is a money market instrument issued by",
     ["A) RBI", "B) Commercial Banks", "C) Government", "D) SEBI", "E] NABARD"], "B", "EASY"),
    ("The 'Placement' in banking refers to",
     ["A) Placement of NPAs", "B) Raising capital by issuing shares", "C) Investment of funds", "D) Distribution of dividends", "E] Allocation of loans"], "B", "EASY"),
]

# Build all questions with chapter assignments
all_questions = []

fm_cid = chapter_ids['financial-markets']
for q, opts, correct, diff in fm_questions:
    qid = str(uuid.uuid4())
    all_questions.append({
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
for q, opts, correct, diff in npa_questions:
    qid = str(uuid.uuid4())
    all_questions.append({
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
for q, opts, correct, diff in basel_questions:
    qid = str(uuid.uuid4())
    all_questions.append({
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
for q, opts, correct, diff in bt_questions:
    qid = str(uuid.uuid4())
    all_questions.append({
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

print(f"Total questions to import: {len(all_questions)}")

imported = 0
for q in all_questions:
    try:
        qid = q['id']
        cid = q['chapter_id']
        
        cur.execute("""
            INSERT INTO questions (id, chapter_id, question_text, explanation, difficulty, is_pyq, pyq_year, pyq_exam_name, source, is_active, created_at, updated_at, image_url)
            VALUES (%s, %s::uuid, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            qid, cid, q['question_text'], q['explanation'], q['difficulty'],
            q['is_pyq'], q['pyq_year'], q['pyq_exam_name'], q['source'],
            q['is_active'], q['created_at'], q['updated_at'], q['image_url']
        ))
        
        # Insert options
        options = q['options']
        correct_answer = q['correct_answer']
        
        for idx, option_text in enumerate(options):
            option_key = chr(65 + idx)  # A, B, C, D, E
            is_correct = (option_key == correct_answer)
            
            cur.execute("""
                INSERT INTO question_options (id, question_id, option_key, option_text, display_order, is_correct)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                str(uuid.uuid4()),
                qid,
                option_key,
                option_text,
                idx + 1,
                is_correct,
            ))
        
        imported += 1
    except Exception as e:
        print(f"Error: {type(e).__name__}: {str(e)[:150]}")
        conn.rollback()

conn.commit()

# Verify counts
print("\n" + "=" * 50)
print("VERIFICATION")
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

cur.execute('SELECT COUNT(*) FROM questions WHERE is_active = true')
total_active = cur.fetchone()[0]
print(f"\nTotal active questions in database: {total_active}")

conn.close()
print("\nImport complete!")