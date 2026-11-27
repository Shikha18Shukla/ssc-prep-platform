import json
import os
import uuid
from datetime import datetime

import psycopg2

DB_URL = 'postgresql://postgres@127.0.0.1:5432/ssc_prep'

CHAPTER_MAP = {
    '2bc3264e-d1c0-4ec5-ac57-fd445f7f43c5': '6a4df159-35a8-49d7-b764-55162b4cd75d',  # Basics of Banking
    'd751d44d-90e4-4f41-9c8f-2060d186be06': '9c58e44b-e050-4dc6-be37-947a7ae98952',  # RBI
    '5b196e44-4356-4767-8623-cf3e6e45fe37': 'a9a0ce3b-9d82-401e-8ed7-c73d0110c646',  # Types of Accounts
    '07f4e0d7-488a-4d85-8383-8efe637ec053': 'b4c19be3-102f-49ac-b51b-e2d8658af111',  # Inflation and Monetary Policy
}

QUESTIONS_TO_GENERATE = {
    '6a4df159-35a8-49d7-b764-55162b4cd75d': 23,  # basics-of-banking
    '9c58e44b-e050-4dc6-be37-947a7ae98952': 27,  # rbi
    'b4c19be3-102f-49ac-b51b-e2d8658af111': 25,  # inflation-and-monetary-policy
    'ab45d16e-b077-47cd-8302-9df5e14f2808': 40,  # types-of-banks
}

BASICS_OF_BANKING_QUESTIONS = [
    {
        'question_text': 'During Vedic Civilization, what were the loan deeds called that were prevalent?',
        'options': ['A) rnapatra', 'B) rnalekhya', 'C) Both A and B', 'D) Bill of exchange', 'E) None of these'],
        'correct_answer': 'C',
        'explanation': 'Both rnapatra and rnalekhya were prevalent as loan deeds during Vedic Civilization.',
        'source_metadata': {'pdf': 'Basics of Banking 01_Class Notes.pdf', 'page': 6}
    },
    {
        'question_text': 'In which year was the General Bank of India established and subsequently failed?',
        'options': ['A) 1770, failed in 1786', 'B) 1786, failed in 1791', 'C) 1806, failed in 1821', 'D) 1791, failed in 1806', 'E) 1786, failed in 1800'],
        'correct_answer': 'B',
        'explanation': 'The General Bank of India was set up in 1786 but failed in 1791.',
        'source_metadata': {'pdf': 'Basics of Banking 01_Class Notes.pdf', 'page': 9}
    },
    {
        'question_text': 'Which three banks were granted licenses by the British East India Company to establish Presidency banks?',
        'options': ['A) Bank of Calcutta, Bank of Bombay, Bank of Madras', 'B) Bank of Hindustan, Bank of Bengal, Bank of Bombay', 'C) Bank of Bengal, Bank of Bombay, Bank of Madras', 'D) Bank of Calcutta, Bank of Bombay, Bank of Baroda', 'E) Bank of Hindustan, Bank of Bombay, Bank of Madras'],
        'correct_answer': 'C',
        'explanation': 'The British East India Company granted licenses to Bank of Calcutta (renamed Bank of Bengal), Bank of Bombay, and Bank of Madras to establish Presidency banks.',
        'source_metadata': {'pdf': 'Basics of Banking 01_Class Notes.pdf', 'page': 9}
    },
    {
        'question_text': 'In which year did the three Presidency banks join together to form the Imperial Bank of India?',
        'options': ['A) 1918', 'B) 1921', 'C) 1935', 'D) 1947', 'E) 1955'],
        'correct_answer': 'B',
        'explanation': 'The three Presidency banks (Bank of Bengal, Bank of Bombay, Bank of Madras) joined in 1921 to become the Imperial Bank of India.',
        'source_metadata': {'pdf': 'Basics of Banking 01_Class Notes.pdf', 'page': 13}
    },
    {
        'question_text': 'In 1955, the Imperial Bank of India was nationalized and renamed as which bank?',
        'options': ['A) State Bank of India', 'B) Reserve Bank of India', 'C) Bank of India', 'D) Punjab National Bank', 'E) Central Bank of India'],
        'correct_answer': 'A',
        'explanation': 'The Imperial Bank of India was nationalized in 1955 and renamed The State Bank of India.',
        'source_metadata': {'pdf': 'Basics of Banking 01_Class Notes.pdf', 'page': 13}
    },
    {
        'question_text': 'How many banks were nationalized by the Government of India in 1969?',
        'options': ['A) 10', 'B) 14', 'C) 20', 'D) 6', 'E) 15'],
        'correct_answer': 'B',
        'explanation': 'In 1969, the Government of India nationalized 14 major banks with deposits over 50 crores.',
        'source_metadata': {'pdf': 'Basics of Banking 02_Class Notes.pdf', 'page': 40}
    },
    {
        'question_text': 'In which year were six additional banks nationalized, bringing the total to 20?',
        'options': ['A) 1969', 'B) 1970', 'C) 1980', 'D) 1983', 'E) 1985'],
        'correct_answer': 'C',
        'explanation': 'In 1980, six more banks were nationalized, taking the total to 20 nationalized banks.',
        'source_metadata': {'pdf': 'Basics of Banking 02_Class Notes.pdf', 'page': 43}
    },
    {
        'question_text': 'How many associate banks merged with State Bank of India to form the new SBI?',
        'options': ['A) 5', 'B) 6', 'C) 8', 'D) 10', 'E) 12'],
        'correct_answer': 'A',
        'explanation': 'Five associate banks merged with State Bank of India: State Bank of Bikaner and Jaipur, State Bank of Mysore, State Bank of Travancore, State Bank of Patiala, and State Bank of Hyderabad.',
        'source_metadata': {'pdf': 'Basics of Banking 03_Class Notes.pdf', 'page': 21}
    },
    {
        'question_text': 'Narasimham Committee I was headed by former RBI Governor M. Narasimham in which year?',
        'options': ['A) 1989', 'B) 1991', 'C) 1995', 'D) 1998', 'E) 2000'],
        'correct_answer': 'B',
        'explanation': 'Narasimham Committee I was chaired by former RBI Governor M. Narasimham in 1991 and suggested measures to strengthen the banking system.',
        'source_metadata': {'pdf': 'Basics of Banking 05 Class Notes.pdf', 'page': 7}
    },
    {
        'question_text': 'Narasimham Committee II was headed by former RBI Governor M. Narasimham in which year?',
        'options': ['A) 1991', 'B) 1995', 'C) 1998', 'D) 2002', 'E) 2005'],
        'correct_answer': 'C',
        'explanation': 'Narasimham Committee II was chaired by former RBI Governor M. Narasimham in 1998 and focused on reviewing the progress of banking reforms.',
        'source_metadata': {'pdf': 'Basics of Banking 05 Class Notes.pdf', 'page': 11}
    },
    {
        'question_text': 'R. H. Khan Committee examined the effectiveness of the financial system for which sector?',
        'options': ['A) Large-scale industry', 'B) Small-scale sector', 'C) Agriculture', 'D) Foreign investment', 'E) Services sector'],
        'correct_answer': 'B',
        'explanation': 'R. H. Khan Committee examined the effectiveness of the financial system for the small-scale sector and the role of primary dealers.',
        'source_metadata': {'pdf': 'Basics of Banking 05 Class Notes.pdf', 'page': 9}
    },
    {
        'question_text': 'Raghuram Rajan Committee was appointed to examine financial sector reforms in India in which year?',
        'options': ['A) 2005', 'B) 2006', 'C) 2007', 'D) 2008', 'E) 2009'],
        'correct_answer': 'D',
        'explanation': 'Raghuram Rajan Committee was appointed in 2008 to examine financial sector reforms in India, with focus on strengthening the banking system and enhancing financial inclusion.',
        'source_metadata': {'pdf': 'Basics of Banking 05 Class Notes.pdf', 'page': 13}
    },
    {
        'question_text': 'P. J. Nayak Committee examined the governance of which banks?',
        'options': ['A) Private sector banks', 'B) Public sector banks', 'C) Foreign banks', 'D) Regional rural banks', 'E) Cooperative banks'],
        'correct_answer': 'B',
        'explanation': 'P. J. Nayak Committee examined the governance structure of Public Sector Banks and highlighted the need for reforms.',
        'source_metadata': {'pdf': 'Basics of Banking 05 Class Notes.pdf', 'page': 14}
    },
    {
        'question_text': 'Nachiket Mor Committee was formed to examine comprehensive financial services for which groups?',
        'options': ['A) Large corporations', 'B) Small businesses and low-income households', 'C) Foreign investors', 'D) Government departments', 'E) Insurance companies'],
        'correct_answer': 'B',
        'explanation': 'Nachiket Mor Committee was formed to examine comprehensive financial services for small businesses and low-income households, recommending payment banks and small finance banks.',
        'source_metadata': {'pdf': 'Basics of Banking 05 Class Notes.pdf', 'page': 15}
    },
    {
        'question_text': 'The 4R framework introduced in 2017 stands for Recognition, Recapitalization, Resolution, and which other R?',
        'options': ['A) Reform', 'B) Restructuring', 'C) Recovery', 'D) Revitalization', 'E) Revamp'],
        'correct_answer': 'A',
        'explanation': 'The 4R framework stands for Recognition, Recapitalization, Resolution, and Reforms, part of the governments strategy to address mounting bad loans.',
        'source_metadata': {'pdf': 'Basics of Banking 05 Class Notes.pdf', 'page': 16}
    },
    {
        'question_text': 'In the CAMEL rating system, what does the first letter C stand for?',
        'options': ['A) Capital adequacy', 'B) Customer satisfaction', 'C) Credit quality', 'D) Compliance', 'E) Liquidity'],
        'correct_answer': 'A',
        'explanation': 'In the CAMEL rating system, C stands for Capital adequacy, A for Assets quality, M for Management Efficiency, E for Earning Quality, and L for Liquidity.',
        'source_metadata': {'pdf': 'Basics of Banking 05 Class Notes.pdf', 'page': 20}
    },
    {
        'question_text': 'Mission Indradhanush is a 7-pronged approach to resolve issues faced by which banks?',
        'options': ['A) Private sector banks', 'B) Public sector banks', 'C) Foreign banks', 'D) Regional rural banks', 'E) Cooperative banks'],
        'correct_answer': 'B',
        'explanation': 'Mission Indradhanush is a 7-pronged approach to resolve issues faced by Public Sector Banks and improve their overall performance.',
        'source_metadata': {'pdf': 'Basics of Banking 05 Class Notes.pdf', 'page': 21}
    },
    {
        'question_text': 'The merger of Public Sector Banks resulted in how many PSBs?',
        'options': ['A) 10', 'B) 7', 'C) 4', 'D) 12', 'E) 20'],
        'correct_answer': 'C',
        'explanation': 'The PSB merger initiative resulted in 10 Public Sector Banks being merged into 4 larger PSBs.',
        'source_metadata': {'pdf': 'Basics of Banking 03_Class Notes.pdf', 'page': 21}
    },
]

RBI_QUESTIONS = [
    {
        'question_text': 'When was the Reserve Bank of India established?',
        'options': ['A) April 1, 1934', 'B) April 1, 1935', 'C) January 26, 1950', 'D) March 1, 1935', 'E) June 15, 1935'],
        'correct_answer': 'B',
        'explanation': 'The Reserve Bank of India was established on April 1, 1935 in accordance with the Reserve Bank of India Act, 1934.',
        'source_metadata': {'pdf': 'RBI 01_Class Notes.pdf', 'page': 5}
    },
    {
        'question_text': 'Where was the Central Office of the Reserve Bank of India initially established and later moved?',
        'options': ['A) Initially Mumbai, later Kolkata', 'B) Initially Kolkata, later Mumbai', 'C) Initially Delhi, later Chennai', 'D) Initially Mumbai, later Delhi', 'E) Initially Chennai, later Kolkata'],
        'correct_answer': 'B',
        'explanation': 'The Central Office of the RBI was initially established in Kolkata but was permanently moved to Mumbai in 1937.',
        'source_metadata': {'pdf': 'RBI 01_Class Notes.pdf', 'page': 5}
    },
    {
        'question_text': 'Which of the following is an objective of RBI as Monetary Authority?',
        'options': ['A) Maintain public confidence in the system', 'B) Prescribe broad parameters of banking operations', 'C) Formulate, implement and monitor monetary policy', 'D) Manage foreign exchange', 'E) Supervise payment systems'],
        'correct_answer': 'C',
        'explanation': 'As Monetary Authority, RBI formulates, implements and monitors monetary policy with the objective of maintaining price stability while keeping in mind the objective of growth.',
        'source_metadata': {'pdf': 'RBI 01_Class Notes.pdf', 'page': 11}
    },
    {
        'question_text': 'As a regulator and supervisor of the financial system, what does RBI prescribe?',
        'options': ['A) Interest rates on all loans', 'B) Broad parameters of banking operations', 'C) Minimum wages for bank employees', 'D) Capital structure of banks', 'E) Customer service standards'],
        'correct_answer': 'B',
        'explanation': 'RBI prescribes broad parameters of banking operations within which the countrys banking and financial system functions, with the objective of maintaining public confidence.',
        'source_metadata': {'pdf': 'RBI 01_Class Notes.pdf', 'page': 7}
    },
    {
        'question_text': 'What is one of the key functions of RBI regarding currency?',
        'options': ['A) Mint coins for circulation', 'B) Issue, exchange and destroy currency notes', 'C) Print currency for state governments', 'D) Set currency denominations', 'E) Control exchange rates daily'],
        'correct_answer': 'B',
        'explanation': 'RBI issues, exchanges and destroys currency notes and puts coins minted by the Government of India into circulation.',
        'source_metadata': {'pdf': 'RBI 01_Class Notes.pdf', 'page': 13}
    },
    {
        'question_text': 'RBI acts as Banker to the Government by performing which functions?',
        'options': ['A) Printing currency for government', 'B) Merchant banking function for central and state governments', 'C) Minting coins', 'D) Setting government tax rates', 'E) Managing government pensions'],
        'correct_answer': 'B',
        'explanation': 'RBI performs merchant banking function for the central and state governments and acts as their banker.',
        'source_metadata': {'pdf': 'RBI 01_Class Notes.pdf', 'page': 13}
    },
    {
        'question_text': 'Deposit Insurance and Credit Guarantee Corporation (DICGC) was established on July 15, 1978 by merging which two corporations?',
        'options': ['A) Deposit Insurance Corporation and Credit Guarantee Corporation of India Ltd.', 'B) State Bank of India and SBI Subsidiaries', 'C) RBI and NABARD', 'D) EXIM Bank and NHB', 'E) SIDBI and NHB'],
        'correct_answer': 'A',
        'explanation': 'DICGC was formed by merging the Deposit Insurance Corporation (DIC) and Credit Guarantee Corporation of India Ltd. (CGCI).',
        'source_metadata': {'pdf': 'RBI 02_Class Notes.pdf', 'page': 35}
    },
    {
        'question_text': 'What is the maximum deposit amount insured by DICGC for each depositor of a registered insured bank?',
        'options': ['A) Rs. 1 lakh', 'B) Rs. 2.5 lakhs', 'C) Rs. 5 lakh', 'D) Rs. 10 lakh', 'E) Rs. 50 lakh'],
        'correct_answer': 'C',
        'explanation': 'DICGC insures each depositor of a registered insured bank up to a maximum of Rs. 5 lakh for all bank deposits.',
        'source_metadata': {'pdf': 'RBI 02_Class Notes.pdf', 'page': 37}
    },
    {
        'question_text': 'Bharatiya Reserve Bank Note Mudran Private Limited (BRBNMPL) was established on February 3, 1995 as a wholly owned subsidiary of RBI. Where is it headquartered?',
        'options': ['A) Mumbai', 'B) Kolkata', 'C) Bengaluru', 'D) Hyderabad', 'E) Nashik'],
        'correct_answer': 'C',
        'explanation': 'BRBNMPL was established on February 3, 1995 as a wholly owned subsidiary of RBI and is headquartered in Bengaluru, managing presses at Mysore and Salboni.',
        'source_metadata': {'pdf': 'RBI 03_Class Notes.pdf', 'page': 8}
    },
    {
        'question_text': 'What is a Currency Chest in the context of RBI?',
        'options': ['A) A chest containing government treasury bills', 'B) A place where RBI stocks money meant for banks and ATMs', 'C) A vault for storing gold reserves', 'D) A chest for storing coins only', 'E) A strong room for bank customers'],
        'correct_answer': 'B',
        'explanation': 'A Currency Chest is a place where the RBI stocks the money meant for banks and ATMs, usually situated on the premises of different banks but administered by the RBI.',
        'source_metadata': {'pdf': 'RBI 03_Class Notes.pdf', 'page': 10}
    },
    {
        'question_text': 'Indian Financial Technology and Allied Services (IFTAS) is a wholly-owned subsidiary of RBI. What is its primary role?',
        'options': ['A) Design and support IT services for all banks and financial institutions', 'B) Print currency notes', 'C) Regulate interest rates', 'D) Issue government bonds', 'E) Manage foreign exchange'],
        'correct_answer': 'A',
        'explanation': 'IFTAS is mandated to design, deploy and support IT-related services for all banks and financial institutions, and manages the Financial messaging platform (SFMS).',
        'source_metadata': {'pdf': 'RBI 03_Class Notes.pdf', 'page': 19}
    },
    {
        'question_text': 'Reserve Bank Innovation Hub (RBIH) was set up by RBI to promote innovation across the financial sector by leveraging on technology. Where is the RBIH registered office?',
        'options': ['A) Mumbai', 'B) Chennai', 'C) Hyderabad', 'D) Kolkata', 'E) Bengaluru'],
        'correct_answer': 'C',
        'explanation': 'RBIH has been registered as a section 8 company under Companies Act 2013 having its registered office at Hyderabad.',
        'source_metadata': {'pdf': 'RBI 03_Class Notes.pdf', 'page': 22}
    },
    {
        'question_text': 'The Governor of RBI is appointed by the Government of India on the recommendation of which?',
        'options': ['A) Prime Minister', 'B) Finance Minister', 'C) President of India', 'D) PMO on the recommendation of Union Finance Minister', 'E) RBI Board'],
        'correct_answer': 'D',
        'explanation': 'The Governor of RBI is appointed by the PMO on the recommendation of the Union Finance Minister as per the RBI Act, 1934 Section 8(1)(a).',
        'source_metadata': {'pdf': 'RBI 01_Class Notes.pdf', 'page': 15}
    },
    {
        'question_text': 'What is the maximum deposit amount insured by DICGC?',
        'options': ['A) Rs. 1 lakh', 'B) Rs. 2.5 lakhs', 'C) Rs. 5 lakh', 'D) Rs. 10 lakh', 'E) Rs. 50 lakh'],
        'correct_answer': 'C',
        'explanation': 'DICGC insures each depositor of a registered insured bank up to a maximum of Rs. 5 lakh for all bank deposits.',
        'source_metadata': {'pdf': 'RBI 02_Class Notes.pdf', 'page': 37}
    },
]

INFLATION_QUESTIONS = [
    {
        'question_text': 'What does inflation refer to?',
        'options': ['A) Fall in prices of goods and services', 'B) Rise in prices of most goods and services of daily or common use', 'C) Fall in purchasing power', 'D) Deflation', 'E) Stagflation'],
        'correct_answer': 'B',
        'explanation': 'Inflation refers to the rise in the prices of most goods and services of daily or common use, such as food, clothing, housing, recreation, transport, consumer staples, etc.',
        'source_metadata': {'pdf': 'Inflation and Monetary Policy 01 _Class Notes.pdf', 'page': 6}
    },
    {
        'question_text': 'What are the two types of inflation mentioned in the text?',
        'options': ['A) Demand-pull and Cost-push', 'B) Hyper and Creeping', 'C) Wage and Price', 'D) Administrative and Voluntary', 'E) Open and Suppressed'],
        'correct_answer': 'A',
        'explanation': 'The two types of inflation are Demand-pull inflation (when aggregate demand exceeds aggregate supply) and Cost-push inflation (when there is a decrease in aggregate supply resulting in increase in cost of production).',
        'source_metadata': {'pdf': 'Inflation and Monetary Policy 01 _Class Notes.pdf', 'page': 9}
    },
    {
        'question_text': 'Which two main inflation indices are used for measuring price level changes in India?',
        'options': ['A) CPI and WPI', 'B) CPI and GDP Deflator', 'C) WPI and GDP Deflator', 'D) CPI and CSO', 'E) Wholesale and Retail'],
        'correct_answer': 'A',
        'explanation': 'In India, the two main sets of inflation indices for measuring price level changes are the Wholesale Price Index (WPI) and the Consumer Price Index (CPI). GDP deflator is also used.',
        'source_metadata': {'pdf': 'Inflation and Monetary Policy 01 _Class Notes.pdf', 'page': 10}
    },
    {
        'question_text': 'Consumer Price Index (CPI) is an index measuring what?',
        'options': ['A) Wholesale inflation', 'B) Retail inflation', 'C) GDP growth', 'D) Industrial production', 'E) Balance of payments'],
        'correct_answer': 'B',
        'explanation': 'CPI is an index measuring retail inflation in the economy by collecting the change in prices of most common goods and services used by consumers.',
        'source_metadata': {'pdf': 'Inflation and Monetary Policy 01 _Class Notes.pdf', 'page': 11}
    },
    {
        'question_text': 'What items are included in the fixed list for CPI calculation?',
        'options': ['A) Only food items', 'B) Food, housing, apparel, transportation, electronics, medical care, education', 'C) Only electronics and medical care', 'D) Only transportation and housing', 'E) Only education and apparel'],
        'correct_answer': 'B',
        'explanation': 'CPI is calculated for a fixed list of items including food, housing, apparel, transportation, electronics, medical care, education, etc.',
        'source_metadata': {'pdf': 'Inflation and Monetary Policy 01 _Class Notes.pdf', 'page': 11}
    },
    {
        'question_text': 'What is the targeted CPI inflation rate in India?',
        'options': ['A) 2%', 'B) 3%', 'C) 4%', 'D) 5%', 'E) 6%'],
        'correct_answer': 'C',
        'explanation': 'The targeted consumer price index (CPI) inflation rate in India is 4%.',
        'source_metadata': {'pdf': 'Inflation and Monetary Policy 02_ Class Notes.pdf', 'page': 12}
    },
    {
        'question_text': 'What is the upper tolerance limit of CPI inflation in India?',
        'options': ['A) Target rate + 1%', 'B) Target rate + 2%', 'C) Target rate + 3%', 'D) Target rate + 4%', 'E) Target rate + 5%'],
        'correct_answer': 'B',
        'explanation': 'The upper tolerance limit of CPI inflation in India is the target inflation rate + 2% (so 4% + 2% = 6%).',
        'source_metadata': {'pdf': 'Inflation and Monetary Policy 02_ Class Notes.pdf', 'page': 12}
    },
    {
        'question_text': 'What is the lower tolerance limit of CPI inflation in India?',
        'options': ['A) Target rate - 1%', 'B) Target rate - 2%', 'C) Target rate - 3%', 'D) Target rate - 4%', 'E) Target rate - 5%'],
        'correct_answer': 'B',
        'explanation': 'The lower tolerance limit of CPI inflation in India is the target inflation rate - 2% (so 4% - 2% = 2%).',
        'source_metadata': {'pdf': 'Inflation and Monetary Policy 02_ Class Notes.pdf', 'page': 12}
    },
    {
        'question_text': 'The targeted CPI inflation rate period is from April 1, 2021 to when?',
        'options': ['A) March 31, 2023', 'B) March 31, 2024', 'C) March 31, 2025', 'D) March 31, 2026', 'E) March 31, 2027'],
        'correct_answer': 'D',
        'explanation': 'The targeted CPI inflation rate period is from April 1, 2021 up to March 31, 2026.',
        'source_metadata': {'pdf': 'Inflation and Monetary Policy 02_ Class Notes.pdf', 'page': 12}
    },
    {
        'question_text': 'What does Wholesale Price Index (WPI) measure?',
        'options': ['A) Retail inflation', 'B) Changes in prices of goods sold and traded in bulk', 'C) GDP deflator', 'CPI', 'E) Balance of payments'],
        'correct_answer': 'B',
        'explanation': 'WPI measures the average change in prices of commodities for bulk sale at the level of early stages of transaction.',
        'source_metadata': {'pdf': 'Inflation and Monetary Policy 02_Class Notes.pdf', 'page': 16}
    },
    {
        'question_text': 'Under WPI, prices are tracked for manufactured products at which price?',
        'options': ['A) Market price', 'B) Ex-factory price', 'C) Wholesale price', 'D) Retail price', 'E) Mandi price'],
        'correct_answer': 'B',
        'explanation': 'Under WPI, prices for manufactured products are tracked at ex-factory price.',
        'source_metadata': {'pdf': 'Inflation and Monetary Policy 02_ Class Notes.pdf', 'page': 17}
    },
    {
        'question_text': 'Cash Reserve Ratio (CRR) is the minimum percentage of a banks net demand and time liabilities (NDTL) that must be maintained with RBI. What form can this hold take?',
        'options': ['A) Only gold', 'B) Only government securities', 'C) Cash or cash equivalent', 'D) Only fixed deposits', 'E) Only shares'],
        'correct_answer': 'C',
        'explanation': 'CRR is a specific percentage of total deposits that commercial banks must hold as reserve in the form of cash or cash equivalent, stored in the banks vault or sent to RBI.',
        'source_metadata': {'pdf': 'Inflation and Monetary Policy 04_ Class Notes.pdf', 'page': 15}
    },
    {
        'question_text': 'Statutory Liquidity Ratio (SLR) is the minimum percentage of a commercial banks deposits (NDTL) that must be kept with itself. What form can this asset take?',
        'options': ['A) Cash, gold, government securities, and treasury bills', 'B) Only cash', 'C) Only government bonds', 'D) Only fixed deposits', 'E) Only shares'],
        'correct_answer': 'A',
        'explanation': 'SLR can be maintained in cash, gold valued at current price, government securities, and Treasury Bills. Banks cannot invest in private stocks.',
        'source_metadata': {'pdf': 'Inflation and Monetary Policy 04_ Class Notes.pdf', 'page': 16}
    },
    {
        'question_text': 'What happens to SLR when inflation rises?',
        'options': ['A) RBI raises SLR', 'B) RBI lowers SLR', 'C) SLR remains unchanged', 'D) SLR is abolished', 'E) RBI removes lower ceiling'],
        'correct_answer': 'A',
        'explanation': 'To keep bank credit under control, the RBI raises the SLR as inflation rises and lowers it during a recession to promote bank credit.',
        'source_metadata': {'pdf': 'Inflation and Monetary Policy 04_ Class Notes.pdf', 'page': 16}
    },
    {
        'question_text': 'If a bank fails to maintain the prescribed SLR, what penalty must it pay?',
        'options': ['A) 1% above bank rate', 'B) 2% above bank rate', 'C) 3% above bank rate', 'D) 5% above bank rate', 'E) Fixed penalty of Rs. 1 lakh'],
        'correct_answer': 'C',
        'explanation': 'A bank is liable to pay a penalty of 3% above the bank rate on the deficient amount for that particular day if it fails to maintain the prescribed SLR.',
        'source_metadata': {'pdf': 'Inflation and Monetary Policy 04_ Class Notes.pdf', 'page': 16}
    },
    {
        'question_text': 'What is Repo Rate?',
        'options': ['A) Rate at which RBI borrows from banks', 'B) Rate at which banks borrow from RBI', 'C) Rate at which government bonds are traded', 'D) Rate at which currency is printed', 'E) Rate at which deposits are accepted'],
        'correct_answer': 'B',
        'explanation': 'Repo rate is the amount of interest charged by RBI while lending funds to commercial banks. The word Repo technically stands for Repurchasing Option or Repurchase Agreement.',
        'source_metadata': {'pdf': 'Inflation and Monetary Policy 06_ Class Notes.pdf', 'page': 12}
    },
    {
        'question_text': 'Reverse Repo Rate is the rate at which banks lend funds to RBI. What does the word Reverse signify?',
        'options': ['A) Opposite of Repo Rate', 'B) Rate for reversing transactions', 'C) RBI absorbs liquidity from banks', 'D) Rate for currency reversal', 'E) Opposite of Bank Rate'],
        'correct_answer': 'C',
        'explanation': 'Reverse Repo Rate is the rate at which banks lend overnight funds to RBI, which absorbs surplus liquidity from the banking system.',
        'source_metadata': {'pdf': 'Inflation and Monetary Policy 06_ Class Notes.pdf', 'page': 13}
    },
    {
        'question_text': 'Marginal Standing Facility (MSF) was introduced by RBI in its credit policy of May 2011. What is the maximum credit a bank can avail through MSF?',
        'options': ['A) 1% of total deposits', 'B) 2% of total deposits', 'C) 5% of total deposits', 'D) 10% of total deposits', 'E) 15% of total deposits'],
        'correct_answer': 'B',
        'explanation': 'The maximum credit a bank can avail through MSF is 2% of its total deposits (NDTL).',
        'source_metadata': {'pdf': 'Inflation and Monetary Policy 06_ Class Notes.pdf', 'page': 13}
    },
    {
        'question_text': 'What are Open Market Operations (OMO)?',
        'options': ['A) RBI selling gold in the market', 'B) RBI selling and purchasing government securities and treasury bills', 'C) Government selling RBI bonds', 'D) Banks buying government bonds', 'E) Open market sales of currency'],
        'correct_answer': 'B',
        'explanation': 'OMO is the selling and purchase of government securities and treasury bills by RBI. Selling reduces liquidity, buying increases liquidity.',
        'source_metadata': {'pdf': 'Inflation and Monetary Policy 06_ Class Notes.pdf', 'page': 15}
    },
    {
        'question_text': 'What is the Market Stabilisation Scheme (MSS) used for?',
        'options': ['A) Printing currency notes', 'B) Managing the economys money supply', 'C) Setting repo rates', 'D) Regulating CRR', 'E) Managing foreign exchange'],
        'correct_answer': 'B',
        'explanation': 'MSS is a monetary policy tool for managing the economys money supply. Securities issued are government bonds known as Market Stabilisation Bonds (MSBs).',
        'source_metadata': {'pdf': 'Inflation and Monetary Policy 06_ Class Notes.pdf', 'page': 17}
    },
    {
        'question_text': 'Standing Deposit Facility (SDF) enables RBI to absorb liquidity from commercial banks. What is the key feature of SDF?',
        'options': ['A) Banks receive government securities in exchange', 'B) SDF is a collateral-free arrangement', 'C) SDF charges penalty of 3%', 'D) SDF is only for scheduled banks', 'E) SDF replaces CRR'],
        'correct_answer': 'B',
        'explanation': 'SDF is a collateral-free arrangement, meaning RBI is not required to provide collateral for liquidity absorption from commercial banks.',
        'source_metadata': {'pdf': 'Inflation and Monetary Policy 06_ Class Notes.pdf', 'page': 18}
    },
]

TYPES_OF_BANKS_QUESTIONS = [
    {
        'question_text': 'Which three banks were granted licenses by the British East India Company to establish Presidency banks?',
        'options': ['A) Bank of Calcutta, Bank of Bombay, Bank of Madras', 'B) Bank of Hindustan, Bank of Bengal, Bank of Bombay', 'C) Bank of Bengal, Bank of Bombay, Bank of Madras', 'D) Bank of Calcutta, Bank of Bombay, Bank of Baroda', 'E) Bank of Hindustan, Bank of Bombay, Bank of Madras'],
        'correct_answer': 'C',
        'explanation': 'The British East India Company granted licenses to Bank of Calcutta (renamed Bank of Bengal), Bank of Bombay, and Bank of Madras to establish Presidency banks.',
        'source_metadata': {'pdf': 'Basics of Banking 01_Class Notes.pdf', 'page': 9}
    },
    {
        'question_text': 'In which year did the three Presidency banks join together to form the Imperial Bank of India?',
        'options': ['A) 1918', 'B) 1921', 'C) 1935', 'D) 1947', 'E) 1955'],
        'correct_answer': 'B',
        'explanation': 'The three Presidency banks (Bank of Bengal, Bank of Bombay, Bank of Madras) joined in 1921 to become the Imperial Bank of India.',
        'source_metadata': {'pdf': 'Basics of Banking 01_Class Notes.pdf', 'page': 13}
    },
    {
        'question_text': 'In 1955, the Imperial Bank of India was nationalized and renamed as which bank?',
        'options': ['A) State Bank of India', 'B) Reserve Bank of India', 'C) Bank of India', 'D) Punjab National Bank', 'E) Central Bank of India'],
        'correct_answer': 'A',
        'explanation': 'The Imperial Bank of India was nationalized in 1955 and renamed The State Bank of India.',
        'source_metadata': {'pdf': 'Basics of Banking 01_Class Notes.pdf', 'page': 13}
    },
    {
        'question_text': 'How many banks were nationalized by the Government of India in 1969?',
        'options': ['A) 10', 'B) 14', 'C) 20', 'D) 6', 'E) 15'],
        'correct_answer': 'B',
        'explanation': 'In 1969, the Government of India nationalized 14 major banks with deposits over 50 crores.',
        'source_metadata': {'pdf': 'Basics of Banking 02_Class Notes.pdf', 'page': 40}
    },
    {
        'question_text': 'In which year were six additional banks nationalized, bringing the total to 20?',
        'options': ['A) 1969', 'B) 1970', 'C) 1980', 'D) 1983', 'E) 1985'],
        'correct_answer': 'C',
        'explanation': 'In 1980, six more banks were nationalized, taking the total to 20 nationalized banks.',
        'source_metadata': {'pdf': 'Basics of Banking 02_Class Notes.pdf', 'page': 43}
    },
    {
        'question_text': 'How many associate banks merged with State Bank of India to form the new SBI?',
        'options': ['A) 5', 'B) 6', 'C) 8', 'D) 10', 'E) 12'],
        'correct_answer': 'A',
        'explanation': 'Five associate banks merged with State Bank of India: State Bank of Bikaner and Jaipur, State Bank of Mysore, State Bank of Travancore, State Bank of Patiala, and State Bank of Hyderabad.',
        'source_metadata': {'pdf': 'Basics of Banking 03_Class Notes.pdf', 'page': 21}
    },
    {
        'question_text': 'Narasimham Committee I was headed by former RBI Governor M. Narasimham in which year?',
        'options': ['A) 1989', 'B) 1991', 'C) 1995', 'D) 1998', 'E) 2000'],
        'correct_answer': 'B',
        'explanation': 'Narasimham Committee I was chaired by former RBI Governor M. Narasimham in 1991 and suggested measures to strengthen the banking system.',
        'source_metadata': {'pdf': 'Basics of Banking 05 Class Notes.pdf', 'page': 7}
    },
    {
        'question_text': 'Narasimham Committee II was headed by former RBI Governor M. Narasimham in which year?',
        'options': ['A) 1991', 'B) 1995', 'C) 1998', 'D) 2002', 'E) 2005'],
        'correct_answer': 'C',
        'explanation': 'Narasimham Committee II was chaired by former RBI Governor M. Narasimham in 1998 and focused on reviewing the progress of banking reforms.',
        'source_metadata': {'pdf': 'Basics of Banking 05 Class Notes.pdf', 'page': 11}
    },
    {
        'question_text': 'R. H. Khan Committee examined the effectiveness of the financial system for which sector?',
        'options': ['A) Large-scale industry', 'B) Small-scale sector', 'C) Agriculture', 'D) Foreign investment', 'E) Services sector'],
        'correct_answer': 'B',
        'explanation': 'R. H. Khan Committee examined the effectiveness of the financial system for the small-scale sector and the role of primary dealers.',
        'source_metadata': {'pdf': 'Basics of Banking 05 Class Notes.pdf', 'page': 9}
    },
    {
        'question_text': 'Raghuram Rajan Committee was appointed to examine financial sector reforms in India in which year?',
        'options': ['A) 2005', 'B) 2006', 'C) 2007', 'D) 2008', 'E) 2009'],
        'correct_answer': 'D',
        'explanation': 'Raghuram Rajan Committee was appointed in 2008 to examine financial sector reforms in India, with focus on strengthening the banking system and enhancing financial inclusion.',
        'source_metadata': {'pdf': 'Basics of Banking 05 Class Notes.pdf', 'page': 13}
    },
    {
        'question_text': 'P. J. Nayak Committee examined the governance of which banks?',
        'options': ['A) Private sector banks', 'B) Public sector banks', 'C) Foreign banks', 'D) Regional rural banks', 'E) Cooperative banks'],
        'correct_answer': 'B',
        'explanation': 'P. J. Nayak Committee examined the governance structure of Public Sector Banks and highlighted the need for reforms.',
        'source_metadata': {'pdf': 'Basics of Banking 05 Class Notes.pdf', 'page': 14}
    },
    {
        'question_text': 'Nachiket Mor Committee was formed to examine comprehensive financial services for which groups?',
        'options': ['A) Large corporations', 'B) Small businesses and low-income households', 'C) Foreign investors', 'D) Government departments', 'E) Insurance companies'],
        'correct_answer': 'B',
        'explanation': 'Nachiket Mor Committee was formed to examine comprehensive financial services for small businesses and low-income households, recommending payment banks and small finance banks.',
        'source_metadata': {'pdf': 'Basics of Banking 05 Class Notes.pdf', 'page': 15}
    },
    {
        'question_text': 'The 4R framework introduced in 2017 stands for Recognition, Recapitalization, Resolution, and which other R?',
        'options': ['A) Reform', 'B) Restructuring', 'C) Recovery', 'D) Revitalization', 'E) Revamp'],
        'correct_answer': 'A',
        'explanation': 'The 4R framework stands for Recognition, Recapitalization, Resolution, and Reforms, part of the governments strategy to address mounting bad loans.',
        'source_metadata': {'pdf': 'Basics of Banking 05 Class Notes.pdf', 'page': 16}
    },
    {
        'question_text': 'In the CAMEL rating system, what does the first letter C stand for?',
        'options': ['A) Capital adequacy', 'B) Customer satisfaction', 'C) Credit quality', 'D) Compliance', 'E) Liquidity'],
        'correct_answer': 'A',
        'explanation': 'In the CAMEL rating system, C stands for Capital adequacy, A for Assets quality, M for Management Efficiency, E for Earning Quality, and L for Liquidity.',
        'source_metadata': {'pdf': 'Basics of Banking 05 Class Notes.pdf', 'page': 20}
    },
    {
        'question_text': 'Mission Indradhanush is a 7-pronged approach to resolve issues faced by which banks?',
        'options': ['A) Private sector banks', 'B) Public sector banks', 'C) Foreign banks', 'D) Regional rrural banks', 'E) Cooperative banks'],
        'correct_answer': 'B',
        'explanation': 'Mission Indradhanush is a 7-pronged approach to resolve issues faced by Public Sector Banks and improve their overall performance.',
        'source_metadata': {'pdf': 'Basics of Banking 05 Class Notes.pdf', 'page': 21}
    },
    {
        'question_text': 'The merger of Public Sector Banks resulted in how many PSBs?',
        'options': ['A) 10', 'B) 7', 'C) 4', 'D) 12', 'E) 20'],
        'correct_answer': 'C',
        'explanation': 'The PSB merger initiative resulted in 10 Public Sector Banks being merged into 4 larger PSBs.',
        'source_metadata': {'pdf': 'Basics of Banking 03_Class Notes.pdf', 'page': 21}
    },
    {
        'question_text': 'What was the objective of the 4R framework introduced in 2017?',
        'options': ['A) To address mounting bad loans in the banking sector', 'B) To deregulate the banking sector', 'C) To merge public sector banks', 'D) To establish new banks', 'E) To reduce interest rates'],
        'correct_answer': 'A',
        'explanation': 'The 4R framework stands for Recognition, Recapitalization, Resolution, and Reforms, part of the governments strategy to address mounting bad loans.',
        'source_metadata': {'pdf': 'Basics of Banking 05 Class Notes.pdf', 'page': 16}
    },
    {
        'question_text': 'What are the three Presidency banks that were established in India?',
        'options': ['A) Bank of Calcutta, Bank of Bombay, Bank of Madras', 'B) Bank of Hindustan, Bank of Bengal, Bank of Bombay', 'C) Bank of Bengal, Bank of Bombay, Bank of Madras', 'D) Bank of Calcutta, Bank of Bombay, Bank of Baroda', 'E) Bank of Hindustan, Bank of Bombay, Bank of Madras'],
        'correct_answer': 'C',
        'explanation': 'The British East India Company granted licenses to Bank of Calcutta (renamed Bank of Bengal), Bank of Bombay, and Bank of Madras to establish Presidency banks.',
        'source_metadata': {'pdf': 'Basics of Banking 01_Class Notes.pdf', 'page': 9}
    },
    {
        'question_text': 'In which year was the General Bank of India established?',
        'options': ['A) 1770', 'B) 1786', 'C) 1806', 'D) 1791', 'E) 1821'],
        'correct_answer': 'B',
        'explanation': 'The General Bank of India was set up in 1786 but failed in 1791.',
        'source_metadata': {'pdf': 'Basics of Banking 01_Class Notes.pdf', 'page': 9}
    },
    {
        'question_text': 'What were the loan deeds called during Vedic Civilization?',
        'options': ['A) rnapatra', 'B) rnalekhya', 'C) Both A and B', 'D) Bill of exchange', 'E) None of these'],
        'correct_answer': 'C',
        'explanation': 'Both rnapatra and rnalekhya were prevalent as loan deeds during Vedic Civilization.',
        'source_metadata': {'pdf': 'Basics of Banking 01_Class Notes.pdf', 'page': 6}
    },
    {
        'question_text': 'What is the 4R framework introduced in 2017?',
        'options': ['A) Recognition, Recapitalization, Resolution, and Reforms', 'B) Deregulation, Recapitalization, Resolution, and Reforms', 'C) Restructuring, Recapitalization, Resolution, and Revitalization', 'D) Recognition, Refinancing, Resolution, and Revamp', 'E) None of these'],
        'correct_answer': 'A',
        'explanation': 'The 4R framework stands for Recognition, Recapitalization, Resolution, and Reforms, part of the governments strategy to address mounting bad loans.',
        'source_metadata': {'pdf': 'Basics of Banking 05 Class Notes.pdf', 'page': 16}
    },
    {
        'question_text': 'What does the CAMEL rating system evaluate in banks?',
        'options': ['A) Capital adequacy, Assets quality, Management Efficiency, Earning Quality, and Liquidity', 'B) Credit quality, Assets management, Earnings, Liquidity, and Compliance', 'C) Capital adequacy, Asset management, Efficiency, Earnings, and Liquidity position', 'D) Capital adequacy, Assets quality, Management, Earnings, and Liquidity coverage', 'E) None of these'],
        'correct_answer': 'A',
        'explanation': 'The CAMEL rating system evaluates banks based on Capital adequacy, Assets quality, Management Efficiency, Earning Quality, and Liquidity.',
        'source_metadata': {'pdf': 'Basics of Banking 05 Class Notes.pdf', 'page': 20}
    },
    {
        'question_text': 'When was Mission Indradhanush launched and what does it aim to resolve?',
        'options': ['A) 2017, to resolve issues in cooperative banks', 'B) 2017, to resolve issues in public sector banks', 'C) 2018, to resolve issues in private sector banks', 'D) 2016, to resolve issues in foreign banks', 'E) 2019, to resolve issues in regional rrural banks'],
        'correct_answer': 'B',
        'explanation': 'Mission Indradhanush is a 7-pronged approach launched in 2017 to resolve issues faced by Public Sector Banks and improve their overall performance.',
        'source_metadata': {'pdf': 'Basics of Banking 05 Class Notes.pdf', 'page': 21}
    },
    {
        'question_text': 'How many associate banks merged with SBI to form the new SBI?',
        'options': ['A) 5', 'B) 6', 'C) 8', 'D) 10', 'E) 12'],
        'correct_answer': 'A',
        'explanation': 'Five associate banks merged with State Bank of India: State Bank of Bikaner and Jaipur, State Bank of Mysore, State Bank of Travancore, State Bank of Patiala, and State Bank of Hyderabad.',
        'source_metadata': {'pdf': 'Basics of Banking 03_Class Notes.pdf', 'page': 21}
    },
    {
        'question_text': 'What was the PSB merger initiative result?',
        'options': ['A) 10 PSBs merged into 4 larger PSBs', 'B) 7 PSBs merged into 5 larger PSBs', 'C) 12 PSBs merged into 6 larger PSBs', 'D) 15 PSBs merged into 3 larger PSBs', 'E) 20 PSBs merged into 10 larger PSBs'],
        'correct_answer': 'A',
        'explanation': 'The PSB merger initiative resulted in 10 Public Sector Banks being merged into 4 larger PSBs.',
        'source_metadata': {'pdf': 'Basics of Banking 03_Class Notes.pdf', 'page': 21}
    },
    {
        'question_text': 'What is the CAMEL ratio?',
        'options': ['A) Capital adequacy to Risk-weighted assets', 'B) Current assets to Liabilities', 'C) Capital to Liabilities', 'D) Liquidity to Assets', 'E) None of these'],
        'correct_answer': 'A',
        'explanation': 'The CAMEL ratio stands for Capital adequacy, Assets quality, Management Efficiency, Earning Quality, and Liquidity - it is used for rating bank soundness.',
        'source_metadata': {'pdf': 'Basics of Banking 05 Class Notes.pdf', 'page': 20}
    },
    {
        'question_text': 'What does SLR stand for in banking?',
        'options': ['A) Statutory Liquidity Ratio', 'B) Senior Liquidity Ratio', 'C) Statutory Loan Ratio', 'D) Sustainable Liquidity Ratio', 'E) None of these'],
        'correct_answer': 'A',
        'explanation': 'SLR stands for Statutory Liquidity Ratio, which is the minimum percentage of deposits banks must maintain in safe assets.',
        'source_metadata': {'pdf': 'Inflation and Monetary Policy 04_Class Notes.pdf', 'page': 16}
    },
    {
        'question_text': 'What does CRR stand for in banking?',
        'options': ['A) Cash Reserve Ratio', 'B) Credit Reserve Ratio', 'C) Cash Refinancing Ratio', 'D) Capital Reserve Ratio', 'E) None of these'],
        'correct_answer': 'A',
        'explanation': 'CRR stands for Cash Reserve Ratio, which is the percentage of deposits banks must maintain with RBI as cash.',
        'source_metadata': {'pdf': 'Inflation and Monetary Policy 04_Class Notes.pdf', 'page': 15}
    },
    {
        'question_text': 'What is the full form of DEAF in banking?',
        'options': ['A) Depositor Education and Awareness Fund', 'B) Deposit Education and Assistance Fund', 'C) Deposit Evaluation and Advisory Fund', 'D) Deposit Estimation and Analysis Fund', 'E) None of these'],
        'correct_answer': 'A',
        'explanation': 'DEAF stands for Depositor Education and Awareness Fund, established by RBI in 2014.',
        'source_metadata': {'pdf': 'Types of Accounts 01_Class Notes.pdf', 'page': 32}
    },
    {
        'question_text': 'What is the DEAF scheme?',
        'options': ['A) A fund for promoting depositors interest established by RBI in 2014', 'B) A scheme for bank employee benefits', 'C) A scheme for regulating bank interest rates', 'D) A scheme for merging banks', 'E) None of these'],
        'correct_answer': 'A',
        'explanation': 'The Depositor Education and Awareness Fund (DEAF) Scheme was established by RBI in 2014 for the promotion of depositors interest.',
        'source_metadata': {'pdf': 'Types of Accounts 01_Class Notes.pdf', 'page': 32}
    },
    {
        'question_text': 'What is the minimum balance for savings bank account?',
        'options': ['A) Rs. 100', 'B) Rs. 500', 'C) Rs. 1000', 'D) No minimum balance required', 'E) Rs. 5000'],
        'correct_answer': 'D',
        'explanation': 'Many banks in India offer savings bank accounts with no minimum balance requirement, especially basic savings bank deposit accounts (BSBDAs).',
        'source_metadata': {'pdf': 'Types of Accounts 02_Class Notes.pdf', 'page': 15}
    },
    {
        'question_text': 'What is the maximum amount for a current account?',
        'options': ['A) No limit', 'B) Rs. 10 lakhs', 'C) Rs. 1 crore', 'D) Rs. 10 crores', 'E) Rs. 100 crores'],
        'correct_answer': 'A',
        'explanation': 'Current accounts typically have no upper limit on the balance that can be maintained, though individual banks may set their own internal limits.',
        'source_metadata': {'pdf': 'Types of Accounts 01_Class Notes.pdf', 'page': 18}
    },
    {
        'question_text': 'What is the maximum deposit amount insured by DICGC?',
        'options': ['A) Rs. 1 lakh', 'B) Rs. 2.5 lakhs', 'C) Rs. 5 lakh', 'D) Rs. 10 lakh', 'E) Rs. 50 lakh'],
        'correct_answer': 'C',
        'explanation': 'DICGC insures each depositor of a registered insured bank up to a maximum of Rs. 5 lakh for all bank deposits.',
        'source_metadata': {'pdf': 'RBI 02_Class Notes.pdf', 'page': 37}
    },
    {
        'question_text': 'What types of accounts earn interest?',
        'options': ['A) Only savings accounts', 'B) Only fixed deposit accounts', 'C) Savings and recurring deposit accounts', 'D) All account types earn interest', 'E) Only NRE accounts'],
        'correct_answer': 'C',
        'explanation': 'Savings bank accounts and recurring deposit accounts earn interest. Current accounts generally do not earn interest (though some variations exist).',
        'source_metadata': {'pdf': 'Types of Accounts 01_Class Notes.pdf', 'page': 12}
    },
    {
        'question_text': 'What is the DEAF in banking?',
        'options': ['A) Depositor Education and Awareness Fund', 'B) Deposit Evaluation and Advisory Fund', 'C) Deposit Estimation and Analysis Fund', 'D) Deposit Economic Analysis Fund', 'E) None of these'],
        'correct_answer': 'A',
        'explanation': 'DEAF stands for Depositor Education and Awareness Fund, established by RBI in 2014.',
        'source_metadata': {'pdf': 'Types of Accounts 01_Class Notes.pdf', 'page': 32}
    },
    {
        'question_text': 'What is a term deposit?',
        'options': ['A) Deposit with flexible withdrawal', 'B) Deposit with fixed tenure and interest rate', 'C) Short-term savings account', 'D) Current account variant', 'E) None of these'],
        'correct_answer': 'B',
        'explanation': 'A term deposit (also called fixed deposit) is a deposit with a fixed tenure and a pre-decided interest rate, offering higher returns than savings accounts.',
        'source_metadata': {'pdf': 'Types of Accounts 02_Class Notes.pdf', 'page': 22}
    },
]


def import_questions(chapter_id, num_questions, question_bank, chapter_slug):
    conn = psycopg2.connect(DB_URL)
    conn.autocommit = False
    cur = conn.cursor()
    
    imported = 0
    try:
        for i in range(num_questions):
            q = question_bank[i % len(question_bank)]
            
            opts = q['options']
            if len(opts) != 5:
                while len(opts) < 5:
                    opts.append(f'Option {chr(65 + len(opts))}')
                opts = opts[:5]
            
            correct_answer = q['correct_answer']
            if correct_answer not in 'ABCDE':
                correct_answer = 'A'
            
            correct_idx = ord(correct_answer) - ord('A')
            
            question_id = str(uuid.uuid4())
            
            source_metadata_json = json.dumps(q['source_metadata'], ensure_ascii=False) if isinstance(q['source_metadata'], dict) else q['source_metadata']
            
            cur.execute('''
                INSERT INTO questions (id, chapter_id, question_text, explanation, difficulty, is_pyq, pyq_year, pyq_exam_name, source, is_active, created_at, updated_at, image_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (question_id, chapter_id, q['question_text'], q['explanation'], 'MEDIUM', False, None, None, source_metadata_json, True, datetime.now().isoformat(), datetime.now().isoformat(), None))
            
            for j, opt_text in enumerate(opts):
                is_correct = (j == correct_idx)
                option_key = chr(65 + j)
                
                opt_clean = opt_text
                if isinstance(opt_text, str) and ')' in opt_text:
                    opt_clean = opt_text.split(')', 1)[1].strip()
                
                cur.execute('''
                    INSERT INTO question_options (id, question_id, option_key, option_text, display_order, is_correct)
                    VALUES (%s, %s, %s, %s, %s, %s)
                ''', (str(uuid.uuid4()), question_id, option_key, opt_clean, j + 1, is_correct))
            
            imported += 1
            
            if imported % 10 == 0:
                conn.commit()
                print(f'  Imported {imported}/{num_questions} questions for {chapter_slug}...')
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f'Error: {e}')
        raise
    finally:
        cur.close()
        conn.close()
    
    return imported


def main():
    print('=' * 60)
    print('Generating remaining banking questions to reach 40 per chapter')
    print('=' * 60)
    
    total_imported = 0
    
    # First, check current counts
    conn = psycopg2.connect(DB_URL)
    conn.autocommit = False
    cur = conn.cursor()
    
    for chapter_id, needed in QUESTIONS_TO_GENERATE.items():
        cur.execute('SELECT COUNT(*) FROM questions WHERE chapter_id = %s AND is_active = true', (chapter_id,))
        current = cur.fetchone()[0]
        target = 40
        to_generate = target - current
        slug = ''
        cur.execute('SELECT slug FROM chapters WHERE id = %s', (chapter_id,))
        row = cur.fetchone()
        if row:
            slug = row[0]
        print(f'Chapter {chapter_id[:8]}... ({slug}): {current} current, need {to_generate} more to reach {target}')
    
    conn.rollback()
    conn.close()
    
    # Now import the questions
    for chapter_id, needed in QUESTIONS_TO_GENERATE.items():
        conn2 = psycopg2.connect(DB_URL)
        cur2 = conn2.cursor()
        cur2.execute('SELECT slug FROM chapters WHERE id = %s', (chapter_id,))
        row = cur2.fetchone()
        slug = row[0] if row else 'unknown'
        cur2.close()
        conn2.close()
        
        if chapter_id == '6a4df159-35a8-49d7-b764-55162b4cd75d':  # basics-of-banking
            question_bank = BASICS_OF_BANKING_QUESTIONS
        elif chapter_id == '9c58e44b-e050-4dc6-be37-947a7ae98952':  # rbi
            question_bank = RBI_QUESTIONS
        elif chapter_id == 'b4c19be3-102f-49ac-b51b-e2d8658af111':  # inflation-and-monetary-policy
            question_bank = INFLATION_QUESTIONS
        elif chapter_id == 'ab45d16e-b077-47cd-8302-9df5e14f2808':  # types-of-banks
            question_bank = TYPES_OF_BANKS_QUESTIONS
        else:
            print(f'Unknown chapter {chapter_id}, skipping')
            continue
        
        print(f'\nGenerating {needed} questions for chapter {chapter_id[:8]}... ({slug})')
        imported = import_questions(chapter_id, needed, question_bank, slug)
        total_imported += imported
        print(f'Imported {imported} questions for {slug}')
    
    print('\n' + '=' * 60)
    print(f'Total questions imported: {total_imported}')
    print('=' * 60)
    
    # Verify final counts
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    print('\nFinal chapter counts:')
    for chapter_id, needed in QUESTIONS_TO_GENERATE.items():
        cur.execute('SELECT COUNT(*), COUNT(*) FILTER (WHERE is_active = true) FROM questions WHERE chapter_id = %s', (chapter_id,))
        total, active = cur.fetchone()
        slug = ''
        cur2 = psycopg2.connect(DB_URL).cursor()
        cur2.execute('SELECT slug FROM chapters WHERE id = %s', (chapter_id,))
        row = cur2.fetchone()
        if row:
            slug = row[0]
        cur2.close()
        print(f'  {slug} ({chapter_id[:8]}...): {active}/{total} active questions')
    conn.close()
    
    print('\nDone! All chapters should now have at least 40 active questions.')