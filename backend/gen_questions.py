import json
import uuid as uuid_mod
from datetime import datetime

# Existing chapter IDs from the database (linked to General/Banking Awareness subject)
chapter_ids = {
    'financial-markets': 'a58ffad6-9e93-40bc-b1c1-77e815e3ad4c',
    'non-performing-assets': '414d8f88-db2b-443c-9c54-30482d72888b',
    'basel-norms-and-banking-risks': 'b182d7f6-6571-4a86-9701-8f9be761dd2e',
    'banking-terminologies': '50f681a6-be97-4b3e-b07d-f1f9380d4efd',
}

questions_data = []

# Financial Markets questions (15 questions)
fm_questions = [
    {
        'question': "In which year was the Securities and Exchange Board of India (SEBI) established?",
        'options': ['A) 1988', 'B) 1992', 'C) 1995', 'D) 2000', 'E) 1990'],
        'correct': 'B',
        'explanation': "SEBI was established in 1988 as a non-statutory body and was given statutory powers in 1992 under the SEBI Act, 1992.",
        'difficulty': 'MEDIUM',
    },
    {
        'question': "Which of the following is not a money market instrument?",
        'options': ['A) Treasury Bill', 'B) Commercial Paper', 'C) Certificate of Deposit', 'D) Government Bond', 'E) Call Money'],
        'correct': 'D',
        'explanation': "Government Bonds are capital market instruments with long-term maturity, while Treasury Bills, Commercial Paper, Certificate of Deposit, and Call Money are money market instruments with short-term maturity (up to one year).",
        'difficulty': 'MEDIUM',
    },
    {
        'question': "The red ink used in a bank's Balance Sheet indicates",
        'options': ['A) Profits', 'B) Losses', 'C) Capital', 'D) Liabilities', 'E) Assets'],
        'correct': 'B',
        'explanation': "In banking convention, red ink indicates losses or negative figures, while black ink indicates profits or positive figures in financial statements.",
        'difficulty': 'EASY',
    },
    {
        'question': "Which committee recommended the introduction of New Banking Technology in India?",
        'options': ['A) Khan Committee', 'B) Narasimham Committee', 'C) Mukherjee Committee', 'D) Deshmukh Committee', 'E) Selvam Committee'],
        'correct': 'B',
        'explanation': "The Narasimham Committee (1991) recommended the introduction of new banking technology and modernization of the Indian banking system.",
        'difficulty': 'MEDIUM',
    },
    {
        'question': "The Indian financial system is supervised by which of the following?",
        'options': ['A) SEBI only', 'B) RBI only', 'C) SEBI and RBI', 'D) SEBI, RBI and IRDA', 'E) Ministry of Finance'],
        'correct': 'C',
        'explanation': "The Indian financial system is supervised by both SEBI (for securities markets) and RBI (for banking and financial institutions). IRDA supervises insurance.",
        'difficulty': 'MEDIUM',
    },
    {
        'question': "Which of the following is the primary objective of the Reserve Bank of India?",
        'options': ['A) Maximize profits', 'B) Control inflation', 'C) Issue currency and manage foreign exchange', 'D) Provide loans to farmers', 'E) Regulate stock markets'],
        'correct': 'C',
        'explanation': "Under the Reserve Bank of India Act, 1934, the primary objectives of RBI are: issue of bank notes, keeping of reserves, and monetary policy to ensure financial stability.",
        'difficulty': 'EASY',
    },
    {
        'question': "The facility that allows banks to borrow money from other banks on an overnight basis is called",
        'options': ['A) Repo Rate', 'B) Reverse Repo Rate', 'C) Call Money Rate', 'D) Bank Rate', 'E) MSF Rate'],
        'correct': 'C',
        'explanation': "Call money market is the market where banks borrow and lend money on an overnight basis. The rate at which this is done is the call money rate.",
        'difficulty': 'EASY',
    },
    {
        'question': "Which of the following instruments is issued by the Government of India to borrow money from the public for a period of 7 to 10 years?",
        'options': ['A) Treasury Bill', 'B) State Development Loan', 'C) National Savings Certificate', 'D) Kisan Vikas Patra', 'E) Government Bond'],
        'correct': 'B',
        'explanation': "State Development Loans (SDLs) are issued by state governments with maturities typically of 5-10 years, while Treasury Bills have maturities of up to 364 days.",
        'difficulty': 'MEDIUM',
    },
    {
        'question': "The full form of 'AMC' in the context of mutual funds is?",
        'options': ['A) Asset Management Company', 'B) Automated Money Counter', 'C) Account Management Commission', 'D) Asset Monitoring Committee', 'E) Aggregate Market Capitalization'],
        'correct': 'A',
        'explanation': "AMC stands for Asset Management Company, which is the firm that manages the investment portfolio of a mutual fund.",
        'difficulty': 'EASY',
    },
    {
        'question': "Which of the following is considered a 'primary market' instrument?",
        'options': ['A) Equity Shares (IPO)', 'B) Public Trading of Shares', 'C) Secondary Market Trading', 'D) Stock Exchange Trading', 'E) Option Trading'],
        'correct': 'A',
        'explanation': "Primary market involves the issuance of new securities by companies to the public for the first time (IPO). Secondary market involves trading of existing securities.",
        'difficulty': 'MEDIUM',
    },
    {
        'question': "The 'Lender of Last Resort' function is performed by?",
        'options': ['A) Commercial Banks', 'B) SEBI', 'C) Reserve Bank of India', 'D) NABARD', 'E) SIDBI'],
        'correct': 'C',
        'explanation': "The Reserve Bank of India acts as the lender of last resort to commercial banks, providing liquidity support during times of financial stress or crisis.",
        'difficulty': 'MEDIUM',
    },
    {
        'question': "Which of the following is not a function of the Securities and Exchange Board of India (SEBI)?",
        'options': ['A) Regulate stock exchanges', 'B) Protect investors', 'C) Issue government bonds', 'D) Regulate mutual funds', 'E) Register intermediaries'],
        'correct': 'C',
        'explanation': "SEBI does not issue government bonds; that is the role of the Government and RBI. SEBI regulates the securities market, protects investors, and regulates intermediaries.",
        'difficulty': 'MEDIUM',
    },
    {
        'question': "The base rate system in Indian banks was introduced based on recommendations of?",
        'options': ['A) Narasimham I Committee', 'B) Narasimham II Committee', 'C) Kelkar Committee', 'D) Raghuram Rajan Committee', 'E) Urjit Patel Committee'],
        'correct': 'B',
        'explanation': "The base rate system was introduced from July 2010 based on the recommendations of the Narasimham II Committee to bring transparency in lending rates.",
        'difficulty': 'MEDIUM',
    },
    {
        'question': "Which of the following is the primary function of a commercial bank?",
        'options': ['A) Issue currency', 'B) Accept deposits and lend', 'C) Regulate money supply', 'D) Set bank rates', 'E) Supervise financial markets'],
        'correct': 'B',
        'explanation': "The primary function of a commercial bank is to accept deposits from the public and lend money to borrowers, facilitating economic activity.",
        'difficulty': 'EASY',
    },
    {
        'question': "SEBI was established in which year?",
        'options': ['A) 1987', 'B) 1988', 'C) 1989', 'D) 1990', 'E) 1991'],
        'correct': 'B',
        'explanation': "SEBI was established in 1988 to regulate the securities market and protect investors' interests.",
        'difficulty': 'EASY',
    },
]

# NPA questions (13 questions)
npa_questions = [
    {
        'question': "An asset is classified as Non-Performing Asset (NPA) if the interest or principal remains overdue for a period of",
        'options': ['A) 30 days', 'B) 60 days', 'C) 90 days', 'D) 120 days', 'E) 180 days'],
        'correct': 'C',
        'explanation': "As per RBI guidelines, an asset becomes an NPA if the interest or principal payment remains overdue for a period of 90 days or more.",
        'difficulty': 'EASY',
    },
    {
        'question': "Which of the following is not a type of NPA?",
        'options': ['A) Sub-standard Asset', 'B) Doubtful Asset', 'C) Loss Asset', 'D) Bad Bank', 'E) Standard Asset'],
        'correct': 'E',
        'explanation': "Standard assets are performing assets that do not disclose any problem. Sub-standard, Doubtful, and Loss are the three categories of NPAs. 'Bad Bank' is a resolution framework, not a classification.",
        'difficulty': 'MEDIUM',
    },
    {
        'question': "The act of transferring NPAs from one bank to another is called",
        'options': ['A) Debt Securitization', 'B) Asset Securitization', 'C) Novation', 'D) Assignment', 'E) Transfer'],
        'correct': 'D',
        'explanation': "Assignment refers to the transfer of NPAs from one bank to another (or to an asset reconstruction company). Securitization involves converting assets into securities.",
        'difficulty': 'MEDIUM',
    },
    {
        'question': "Under the SARFAESI Act, 2002, banks can recover NPAs without the intervention of",
        'options': ['A) Debt Recovery Tribunal', 'B) SARFAESI Act', 'C) Consumer Forum', 'D) Court'],
        'correct': 'A',
        'explanation': "SARFAESI Act allows banks to recover NPAs without approaching DRT. However, certain legal actions may still require court intervention. Consumer Forum has no role in NPA recovery.",
        'difficulty': 'MEDIUM',
    },
    {
        'question': "Which of the following is the typical provisioning percentage for sub-standard assets?",
        'options': ['A) 25%', 'B) 30%', 'C) 40%', 'D) 15%', 'E) 50%'],
        'correct': 'B',
        'explanation': "For sub-standard assets, banks are required to make a provision of at least 25% of the unsecured portion and 100% of the secured portion, typically averaging around 30% in practice.",
        'difficulty': 'MEDIUM',
    },
    {
        'question': "Resolution of NPA through one-time settlement is typically done with",
        'options': ['A) Full recovery', 'B) 50-70% recovery', 'C) 80-90% recovery', 'D) 100% recovery', 'E) No recovery'],
        'correct': 'B',
        'explanation': "One-time settlement (OTS) typically involves recovery of 50-70% of the outstanding amount, depending on the borrower's repayment capacity and collateral value.",
        'difficulty': 'MEDIUM',
    },
    {
        'question': "Credit facilities granted by a bank for agriculture and allied activities that remain overdue for 90 days are classified as NPA under",
        'options': ['A) Agriculture Advance', 'B) Priority Sector Lending', 'C) NPA Classification', 'D) Farm Credit', 'E) Rural Credit'],
        'correct': 'A',
        'explanation': "Agricultural advances that remain overdue for 90 days are classified as NPAs. However, for short-term agricultural loans, the overdue period may be different.",
        'difficulty': 'MEDIUM',
    },
    {
        'question': "The NPA ratio (NPAs to Total Advances) of a bank indicates its",
        'options': ['A) Profitability', 'B) Liquidity', 'C) Asset Quality', 'D) Capital Adequacy', 'E) Operational Efficiency'],
        'correct': 'C',
        'explanation': "The NPA ratio or gross NPA ratio (GNPA / Total Advances) is a key indicator of a bank's asset quality. Higher ratios indicate poorer asset quality.",
        'difficulty': 'MEDIUM',
    },
    {
        'question': "Which of the following would improve a bank's NPA situation?",
        'options': ['A) Relaxing CIBIL standards', 'B) Strict credit appraisal', 'C) Increasing sub-standard assets', 'D) Reducing provisioning', 'E) Writing off all debts'],
        'correct': 'B',
        'explanation': "Strict credit appraisal at the time of lending helps prevent NPAs from arising. Relaxed standards typically lead to higher NPAs.",
        'difficulty': 'MEDIUM',
    },
    {
        'question': "Under the 'Pradhan Mantri Mudra Yojana', loans are given in which categories?",
        'options': ['A) Shishu, Kishore and Tarun', 'B) Small, Medium and Large', 'C) Gold, Silver and Platinum', 'D) Primary, Secondary and Tertiary', 'E) Micro and Macro'],
        'correct': 'A',
        'explanation': "PMMY loans are categorized as Shishu (up to 50000), Kishore (50001 to 5 lakh), and Tarun (5 lakh to 10 lakh) based on the loan amount and stage of business.",
        'difficulty': 'EASY',
    },
    {
        'question': "The '5/180' NPA classification norm applies to",
        'options': ['A) Short-term crops', 'B) Long-term agriculture', 'C) Corporate loans', 'D) Personal loans', 'E] Consumer loans'],
        'correct': 'B',
        'explanation': "For long-term agriculture, the NPA classification norm is interest or installment remaining unpaid for 2 harvest periods or 180 days, whichever is earlier.",
        'difficulty': 'MEDIUM',
    },
    {
        'question': "Which ratio measures the proportion of a bank's NPA to its total capital?",
        'options': ['A) Gross NPA Ratio', 'B) Net NPA Ratio', 'C) NPA to Capital Ratio', 'D) Capital Adequacy Ratio', 'E) Provisioning Coverage Ratio'],
        'correct': 'C',
        'explanation': "NPA to Capital Ratio measures the proportion of NPAs relative to the bank's capital, indicating the bank's exposure to credit risk relative its capital base.",
        'difficulty': 'MEDIUM',
    },
    {
        'question': "Which of the following would NOT reduce NPAs?",
        'options': ['A) Strict recovery measures', 'B) One-time settlement', 'C) Writing off loans without recovery', 'D) Better credit appraisal'],
        'correct': 'C',
        'explanation': "Writing off loans without actual recovery does not reduce NPAs; it only removes them from the balance sheet temporarily. The asset still exists and may be reported again.",
        'difficulty': 'MEDIUM',
    },
]

# Basel questions (13 questions) - all difficulty EASY or MEDIUM (no HIGH)
basel_questions = [
    {
        'question': "Basel III norms were issued by the Basel Committee on Banking Supervision in",
        'options': ['A) 2004', 'B) 2008', 'C) 2010', 'D) 2013', 'E) 2015'],
        'correct': 'D',
        'explanation': "Basel III framework was finalized in November 2010 and began implementation from 2013, with full implementation by 2019.",
        'difficulty': 'EASY',
    },
    {
        'question': "Basel III primarily aims to strengthen which three aspects of banking regulation?",
        'options': ['A) Capital, Liquidity, and Leverage', 'B) Capital, Profitability, and Liquidity', 'C) Leverage, Solvency, and Profitability', 'D) Capital, Risk Management, and Auditing', 'E) Liquidity, Solvency, and Capital'],
        'correct': 'A',
        'difficulty': 'MEDIUM',
    },
    {
        'question': "Common Equity Tier 1 (CET1) capital primarily consists of?",
        'options': ['A) Hybrid instruments', 'B) Subordinated debt', 'C) Common shares and retained earnings', 'D) Preferred shares', 'E) Bonds'],
        'correct': 'C',
        'difficulty': 'MEDIUM',
    },
    {
        'question': "The minimum Common Equity Tier 1 capital ratio under Basel III is?",
        'options': ['A) 2%', 'B) 4.5%', 'C) 6%', 'D) 8%', 'E) 10%'],
        'correct': 'B',
        'difficulty': 'MEDIUM',
    },
    {
        'question': "Liquidity Coverage Ratio (LCR) under Basel III requires banks to maintain adequate liquid assets to withstand",
        'options': ['A) 30 days of stressed liquidity scenario', 'B) 90 days of stress', 'C) 1 year of stress', 'D) 1 month of normal operations', 'E) 6 months of stress'],
        'correct': 'A',
        'difficulty': 'MEDIUM',
    },
    {
        'question': "Net Stable Funding Ratio (NSFR) requires a minimum ratio of stable funding to required stable funding of at least",
        'options': ['A) 90%', 'B) 100%', 'C) 110%', 'D) 125%', 'E) 150%'],
        'correct': 'B',
        'difficulty': 'MEDIUM',
    },
    {
        'question': "Basel III introduced a leverage ratio to restrict the",
        'options': ['A) Total risk-weighted assets', 'B) Amount of lending', 'C) Overall exposure of the bank', 'D) Capital adequacy ratio', 'E) Loan-to-deposit ratio'],
        'correct': 'C',
        'difficulty': 'MEDIUM',
    },
    {
        'question': "Risk-weighted assets (RWA) in Basel III are calculated based on?",
        'options': ['A) Total assets of the bank', 'B) Credit risk only', 'C) Risk profiles of counterparties and assets', 'D) Market risk only', 'E) Operational risk only'],
        'correct': 'C',
        'difficulty': 'MEDIUM',
    },
    {
        'question': "The countercyclical capital buffer under Basel III is designed to",
        'options': ['A) Protect against housing bubbles only', 'B) Be activated during systemic stress', 'C) Replace the conservation buffer', 'D) Apply only to foreign banks', 'E) Limit dividend payments permanently'],
        'correct': 'B',
        'difficulty': 'MEDIUM',
    },
    {
        'question': "Which of the following is NOT a Basel III capital instrument?",
        'options': ['A) Common Equity Tier 1', 'B) Additional Tier 1', 'C) Tier 2', 'D) Tier 3', 'E) All are Basel III instruments'],
        'correct': 'D',
        'difficulty': 'MEDIUM',
    },
    {
        'question': "The output floor under Basel III limits the benefit of risk-weight reductions, requiring banks to hold at least",
        'options': ['A) 50% of standardized RWA', 'B) 65% of standardized RWA', 'C) 72.5% of standardized RWA', 'D) 75% of standardized RWA', 'E) 80% of standardized RWA'],
        'correct': 'C',
        'difficulty': 'MEDIUM',
    },
    {
        'question': "Basel II norms were issued in which year?",
        'options': ['A) 1999', 'B) 2004', 'C) 2010', 'D) 2013', 'E) 2015'],
        'correct': 'B',
        'difficulty': 'EASY',
    },
    {
        'question': "Which of the following Basel Accords introduced the concept of Capital Adequacy Ratio (CAR)?",
        'options': ['A) Basel I', 'B) Basel II', 'C) Basel III', 'D) Basel IV', 'E) None of the above'],
        'correct': 'A',
        'difficulty': 'EASY',
    },
]

# Banking Terminologies questions (15 questions)
bt_questions = [
    {
        'question': "CRR (Cash Reserve Ratio) refers to the percentage of bank deposits that banks must maintain with",
        'options': ['A) SEBI', 'B) RBI', 'C) NABARD', 'D) Commercial Banks', 'E) Government'],
        'correct': 'B',
        'difficulty': 'EASY',
    },
    {
        'question': "SLR (Statutory Liquidity Ratio) refers to the percentage of bank deposits that banks must maintain in",
        'options': ['A) Cash with RBI', 'B) Gold or approved securities', 'C) Foreign currency', 'D) Corporate bonds', 'E) Government bonds only'],
        'correct': 'B',
        'difficulty': 'EASY',
    },
    {
        'question': "The difference between CRR and SLR is that CRR is maintained with",
        'options': ['A) Commercial Banks', 'B) RBI', 'C) Government', 'D) SEBI', 'E) NABARD'],
        'correct': 'B',
        'difficulty': 'EASY',
    },
    {
        'question': "Repo Rate is the rate at which RBI lends money to banks against",
        'options': ['A) Government Securities', 'B) Corporate Bonds', 'C) Foreign Exchange', 'D) Gold', 'E) Shares'],
        'correct': 'A',
        'difficulty': 'EASY',
    },
    {
        'question': "Reverse Repo Rate is the rate at which RBI borrows money from banks against",
        'options': ['A) Government Securities', 'B) Corporate Bonds', 'C) Foreign Exchange', 'D) Gold', 'E) Shares'],
        'correct': 'A',
        'difficulty': 'EASY',
    },
    {
        'question': "Marginal Standing Facility (MSF) rate is pegged at",
        'options': ['A) Repo Rate', 'B) Reverse Repo Rate', 'C) 1% above Repo Rate', 'D) 2% above Repo Rate', 'E) Bank Rate'],
        'correct': 'C',
        'difficulty': 'MEDIUM',
    },
    {
        'question': "Bank Rate is the rate at which RBI rediscounts bills of exchange with",
        'options': ['A) Commercial Banks', 'B) Cooperative Banks', 'C) State Governments', 'D) Financial Institutions', 'E) All of the above'],
        'correct': 'E',
        'difficulty': 'MEDIUM',
    },
    {
        'question': "Open Market Operations (OMO) refer to",
        'options': ['A) Trading in stock markets', 'B) RBI buying/selling government securities', 'C) Banking ombudsman actions', 'D) Bank marketing activities', 'E) Online money transfers'],
        'correct': 'B',
        'difficulty': 'EASY',
    },
    {
        'question': "The 'Marginal Cost of Funds based Lending Rate' (MCLR) was introduced in",
        'options': ['A) 2010', 'B) 2012', 'C) 2016', 'D) 2018', 'E) 2020'],
        'correct': 'C',
        'difficulty': 'MEDIUM',
    },
    {
        'question': "MCLR is determined by the",
        'options': ['A) Government of India', 'B) Finance Ministry', 'C) Individual Banks', 'D) Reserve Bank of India', 'E) Indian Banks Association'],
        'correct': 'C',
        'difficulty': 'MEDIUM',
    },
    {
        'question': "Base Rate was the lending rate system introduced by RBI in",
        'options': ['A) 2003', 'B) 2007', 'C) 2010', 'D) 2014', 'E) 2018'],
        'correct': 'C',
        'difficulty': 'EASY',
    },
    {
        'question': "The 'Prime Lending Rate' (PLR) is the rate charged by banks to their",
        'options': ['A) Best customers', 'B) Small customers', 'C) All customers equally', 'D) Corporate customers', 'E) Priority sector customers'],
        'correct': 'A',
        'difficulty': 'EASY',
    },
    {
        'question': "Call Money Market is a market for",
        'options': ['A) Long-term loans', 'B) Overnight borrowing/lending', 'C) Government securities', 'D) Corporate bonds', 'E) Foreign exchange'],
        'correct': 'B',
        'difficulty': 'EASY',
    },
    {
        'question': "Certificate of Deposit (CD) is a money market instrument issued by",
        'options': ['A) RBI', 'B) Commercial Banks', 'C) Government', 'D) SEBI', 'E) NABARD'],
        'correct': 'B',
        'difficulty': 'EASY',
    },
    {
        'question': "The 'Placement' in banking refers to",
        'options': ['A) Placement of NPAs', 'B) Raising capital by issuing shares', 'C) Investment of funds', 'D) Distribution of dividends', 'E) Allocation of loans'],
        'correct': 'B',
        'difficulty': 'EASY',
    },
]

# Build the questions list
all_questions = []

fm_cid = chapter_ids['financial-markets']
for i, q in enumerate(fm_questions):
    qid = str(uuid_mod.uuid4())
    all_questions.append({
        'id': qid,
        'chapter_id': fm_cid,
        'question_text': q['question'],
        'explanation': q['explanation'],
        'difficulty': q['difficulty'],
        'is_pyq': False,
        'pyq_year': None,
        'pyq_exam_name': None,
        'source': 'original-practice',
        'is_active': True,
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'image_url': None,
        'options': q['options'],
        'correct_answer': q['correct'],
    })

np_cid = chapter_ids['non-performing-assets']
for i, q in enumerate(npa_questions):
    qid = str(uuid_mod.uuid4())
    all_questions.append({
        'id': qid,
        'chapter_id': np_cid,
        'question_text': q['question'],
        'explanation': q['explanation'],
        'difficulty': q['difficulty'],
        'is_pyq': False,
        'pyq_year': None,
        'pyq_exam_name': None,
        'source': 'original-practice',
        'is_active': True,
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'image_url': None,
        'options': q['options'],
        'correct_answer': q['correct'],
    })

bs_cid = chapter_ids['basel-norms-and-banking-risks']
for i, q in enumerate(basel_questions):
    qid = str(uuid_mod.uuid4())
    all_questions.append({
        'id': qid,
        'chapter_id': bs_cid,
        'question_text': q['question'],
        'explanation': q['explanation'],
        'difficulty': q['difficulty'],
        'is_pyq': False,
        'pyq_year': None,
        'pyq_exam_name': None,
        'source': 'original-practice',
        'is_active': True,
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'image_url': None,
        'options': q['options'],
        'correct_answer': q['correct'],
    })

bt_cid = chapter_ids['banking-terminologies']
for i, q in enumerate(bt_questions):
    qid = str(uuid_mod.uuid4())
    all_questions.append({
        'id': qid,
        'chapter_id': bt_cid,
        'question_text': q['question'],
        'explanation': q['explanation'],
        'difficulty': q['difficulty'],
        'is_pyq': False,
        'pyq_year': None,
        'pyq_exam_name': None,
        'source': 'original-practice',
        'is_active': True,
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'image_url': None,
        'options': q['options'],
        'correct_answer': q['correct'],
    })

output = {
    'total_questions': len(all_questions),
    'questions': all_questions,
}

with open('questions_import.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"Generated questions_import.json with {len(all_questions)} questions")
for ch_slug, ch_id in chapter_ids.items():
    count = sum(1 for q in all_questions if q['chapter_id'] == ch_id)
    print(f"  {ch_slug}: {count}")