// Reproducible, audited text-first Data Interpretation practice batch.
const fs = require('node:fs');
const path = require('node:path');

const rows = [];
const PDF = 'Verified from supplied Data Interpretation PDF, page ';
const ORIGINAL = 'Original SSC-style practice question';

function add(level, dataset, prompt, answer, calculation, wrongs, source = ORIGINAL) {
  const values = [answer, ...wrongs];
  if (new Set(values.map(v => v.trim().toLowerCase())).size !== 4) {
    throw new Error(`Options repeat for ${prompt}`);
  }
  const position = (rows.length * 7 + 1) % 4;
  values.splice(position, 0, values.shift());
  rows.push({ level, dataset, prompt, answer, calculation, values, key: 'ABCD'[position], source });
}

const table = (name, data) => `Dataset ${name} (all values are given below):\n${data}`;
function set(dataset, specs) {
  for (const [level, prompt, answer, calculation, wrongs] of specs) {
    add(level, dataset, prompt, answer, calculation, wrongs);
  }
}
function pdf(level, page, dataset, prompt, answer, calculation, wrongs) {
  add(level, dataset, prompt, answer, calculation, wrongs, `${PDF}${page}; exam/year not stated`);
}

// The 15 usable questions from the supplied PDF. Page 8 is excluded because
// its computed percentage (368/530 = 69.43%) is absent from every option.
pdf('MEDIUM',5,table('PDF-5','Company sales by year (units):\nYear | A | B\nP | 350 | 1150\nQ | 550 | 850\nR | 750 | 950\nS | 650 | 350\nT | 450 | 250'),'Let L1 be the absolute difference between the companies’ total sales and L2 be A’s average annual sales. Find L1:L2.','16:11','A totals 2,750 and B totals 3,550, so L1=800. A’s average is 2,750/5=550. Thus 800:550=16:11.',['11:17','11:16','13:12']);
pdf('EASY',6,table('PDF-6','Refrigerator production by company (units):\nA 300; B 210; C 180; D 120; E 60; F 150'),'A’s production is what percent of E’s production?','500%','300/60 × 100 = 500%.',['600%','400%','200%']);
pdf('EASY',7,table('PDF-7','Books sold by two shops (books):\nMonth | S1 | S2\nM1 | 50 | 5\nM2 | 40 | 10\nM3 | 20 | 60\nM4 | 15 | 30\nM5 | 5 | 25'),'Let J1 be the combined total sold by both shops over five months and J2 the absolute difference between their totals. Find J1+J2.','260','S1 sold 130 and S2 sold 130. Therefore J1=260, J2=0, and J1+J2=260.',['160','200','130']);
pdf('MEDIUM',9,table('PDF-9','Toy production by year (units):\nToy | 2016 | 2017 | 2018\nBicycle | 1500 | 2000 | 2500\nTrain | 1600 | 1800 | 2000\nCar | 1800 | 1600 | 2600\nBus | 2000 | 1600 | 3000'),'Find the ratio of cars plus trains produced in 2017 and 2018 to buses produced in all three years.','40:33','Cars and trains in 2017–18 total 1,600+2,600+1,800+2,000=8,000. Buses total 2,000+1,600+3,000=6,600. The ratio simplifies to 40:33.',['30:41','33:40','35:41']);
pdf('HARD',10,table('PDF-10','Articles: cost price and profit (rupees):\nD | 700 | 200\nE | 600 | 150\nF | 400 | 300\nG | 500 | 400\nH | 300 | 250\nI | 800 | 350'),'Which statements are NOT correct? I. Profit on D, E and F is 30.63% of the cost price of G, H and I. II. Total cost price : total profit is 1:2.','Neither I nor II','Profit D+E+F=650 and cost G+H+I=1,600, so I is false (650/1,600=40.625%). Total cost=3,300 and profit=1,650, or 2:1, so II is also false.',['Both I and II','Only II','Only I']);
pdf('EASY',11,table('PDF-11','Annual profit percentage:\nYear | Profit %\n2016 | 45\n2017 | 70\n2018 | 60\n2019 | 40\n2020 | 55'),'What was the average profit percentage over these five years?','54%','(45+70+60+40+55)/5 = 270/5 = 54%.',['55%','44%','48%']);
pdf('MEDIUM',12,table('PDF-12','Teachers in five schools (people):\nSchool | Male | Female\nL | 160 | 180\nM | 180 | 170\nN | 170 | 120\nP | 150 | 110\nQ | 130 | 130'),'Which statement is correct? I. Male teachers at L are 135.44% of female teachers at P. II. Female teachers at M and N together : male teachers at N and P together = 29:32.','Only II','Statement I gives 160/110×100≈145.45%, so it is false. For II, (170+120):(170+150)=290:320=29:32, so only II is true.',['Both I and II','Neither I nor II','Only I']);
pdf('EASY',13,table('PDF-13','Calculators sold by shops L and M (units):\nMonth | L | M\nD | 350 | 305\nE | 340 | 310\nF | 320 | 360\nG | 315 | 330\nH | 305 | 325'),'Let J1 be L’s average monthly sales and J2 the absolute difference between the shops’ five-month totals. Find J2/J1.','0','L totals 1,630, giving J1=1,630/5=326. M also totals 1,630, so J2=0 and J2/J1=0.',['326','125','1']);
pdf('MEDIUM',14,table('PDF-14','Books sold (thousands):\nBranch | 2010 | 2011\nC1 | 67 | 75\nC2 | 79 | 91\nC3 | 85 | 76\nC4 | 66 | 86\nC5 | 83 | 72'),'Find the ratio of C2’s two-year sales to C4’s two-year sales.','85:76','C2 total=79+91=170 and C4 total=66+86=152. Simplifying 170:152 gives 85:76.',['76:85','169:153','153:169']);
pdf('EASY',15,table('PDF-15','Patient temperature by time (°C):\n10:00 a.m. 34.5; 11:00 a.m. 35; 12:00 noon 38; 1:00 p.m. 38.5; 2:00 p.m. 34; 3:00 p.m. 34'),'At what time was the patient’s temperature highest?','1:00 p.m.','The largest listed temperature is 38.5°C, at 1:00 p.m.',['12:00 noon','10:00 a.m.','11:00 a.m.']);
pdf('EASY',16,table('PDF-16','Company income and expenditure (thousand rupees):\nYear | Income | Expenditure\nY1 | 700 | 300\nY2 | 500 | 200\nY3 | 400 | 300\nY4 | 800 | 200\nY5 | 300 | 150'),'In which year were savings lowest?','Y3','Savings are 400, 300, 100, 600 and 150 thousand rupees, respectively. The minimum is 100 in Y3.',['Y4','Y2','Y5']);
pdf('MEDIUM',17,table('PDF-17','Six articles: cost price and profit (rupees):\nArticle | Cost | Profit\nJ | 650 | 150\nK | 550 | 100\nL | 350 | 250\nM | 450 | 350\nN | 250 | 200\nP | 750 | 300'),'Which statement is correct? I. Combined cost of J and K is 100% more than combined profit of L and M. II. Profit of N and P : cost of K and M = 2:1.','Only I','J+K cost=1,200, exactly 100% more than L+M profit=600. N+P profit : K+M cost=500:1,000=1:2, not 2:1. Only I is correct.',['Only II','Both I and II','Neither I nor II']);
pdf('MEDIUM',18,table('PDF-18','Student marks:\nSubject | 2015 | 2016\nMathematics | 40 | 56\nHistory | 45 | 40\nScience | 67 | 68\nHindi | 34 | 90\nCivics | 40 | 60'),'History marks in 2016 are what percent of the student’s total Civics marks across both years?','40%','History 2016=40; Civics total=40+60=100. Thus 40/100×100=40%.',['55%','50%','60%']);
pdf('EASY',19,table('PDF-19','Population (thousands):\nYear | State P | State Q\nA | 150 | 300\nB | 250 | 200\nC | 175 | 125\nD | 100 | 75\nE | 50 | 150'),'What is the absolute difference between the two states’ total populations over all five years?','125','P totals 725 and Q totals 850 thousand. Their absolute difference is 125 thousand.',['150','75','275']);
pdf('MEDIUM',20,table('PDF-20','Income and expenditure (thousand rupees):\nCompany | Expenditure | Income\nA | 45 | 35\nB | 40 | 50\nC | 45 | 40\nD | 30 | 40\nE | 45 | 50'),'Which company had the greatest percentage loss?','A','Only A and C made losses. A lost 10/45×100≈22.22%; C lost 5/45×100≈11.11%. A’s percentage loss is greater.',['E','B','C']);

// Original EASY sets (24 questions in eight compact, fully embedded datasets).
set(table('E-01','Fruit sales (kg):\nStall | Apples | Pears | Plums\nA | 24 | 18 | 12\nB | 30 | 15 | 15\nC | 21 | 24 | 15'),[
 ['EASY','How many kilograms of apples did all three stalls sell?','75 kg','24+30+21=75 kg.',['69 kg','78 kg','81 kg']],
 ['EASY','What is the ratio of pears sold by C to pears sold by A?','4:3','24:18 simplifies to4:3.',['3:4','4:5','3:5']],
 ['EASY','How many kilograms of fruit did stall B sell in total?','60 kg','30+15+15=60 kg.',['55 kg','45 kg','65 kg']],
]);
set(table('E-02','Quarterly sales (thousand units):\nProduct | Q1 | Q2 | Q3 | Q4\nP | 20 | 24 | 28 | 32\nQ | 18 | 20 | 22 | 26\nR | 25 | 20 | 30 | 25'),[
 ['EASY','What were product P’s total sales for the year?','104 thousand','20+24+28+32=104 thousand.',['96 thousand','100 thousand','108 thousand']],
 ['EASY','By how many thousand units did Q4 sales of P exceed Q1 sales of Q?','14 thousand','32−18=14 thousand.',['12 thousand','10 thousand','16 thousand']],
 ['EASY','What is the average quarterly sale of R?','25 thousand','(25+20+30+25)/4=25 thousand.',['24 thousand','26 thousand','30 thousand']],
]);
set(table('E-03','Students choosing activities (students):\nSchool | Music | Art | Drama\nL | 35 | 25 | 20\nM | 30 | 32 | 18\nN | 28 | 22 | 30'),[
 ['EASY','How many students at school M chose Art?','32','The table gives 32 students.',['30','28','35']],
 ['EASY','How many more students at L chose Music than Drama?','15','35−20=15 students.',['10','12','18']],
 ['EASY','How many students chose Drama across all three schools?','68','20+18+30=68 students.',['66','70','72']],
]);
set(table('E-04','Household budget shares (percent of monthly budget):\nFood 30%; Housing 25%; Transport 15%; Education 10%; Other 20%. Monthly budget = Rs 40,000.'),[
 ['EASY','How much is spent on food?','Rs 12,000','30% of Rs40,000 = Rs12,000.',['Rs 10,000','Rs 8,000','Rs 14,000']],
 ['EASY','What is the difference between housing and transport spending?','Rs 4,000','(25−15)% of Rs40,000=Rs4,000.',['Rs 3,000','Rs 5,000','Rs 6,000']],
 ['EASY','What percentage of the budget is spent on education and transport together?','25%','10%+15%=25%.',['20%','30%','35%']],
]);
set(table('E-05','Books borrowed (books):\nClass | January | February\n5A | 42 | 38\n5B | 35 | 45\n5C | 48 | 40'),[
 ['EASY','How many books did class 5A borrow over both months?','80','42+38=80 books.',['78','82','84']],
 ['EASY','Which class borrowed the most books in February?','5B','February values are 38,45,40; the maximum is45.',['5A','5C','They tied']],
 ['EASY','How many books did all classes borrow in January?','125','42+35+48=125.',['120','128','130']],
]);
set(table('E-06','Rainfall (mm):\nMonth | June | July | August | September\nTown A | 120 | 160 | 140 | 100\nTown B | 90 | 150 | 180 | 120'),[
 ['EASY','How much rainfall did Town A receive in July?','160 mm','Read the July value for Town A:160 mm.',['140 mm','150 mm','180 mm']],
 ['EASY','What was Town B’s total rainfall over these four months?','540 mm','90+150+180+120=540 mm.',['520 mm','550 mm','560 mm']],
 ['EASY','By how many millimetres did Town B’s August rainfall exceed Town A’s August rainfall?','40 mm','180−140=40 mm.',['20 mm','30 mm','60 mm']],
]);
set(table('E-07','Bags collected for recycling (bags):\nGroup | Paper | Plastic\nA | 36 | 24\nB | 28 | 32\nC | 40 | 20\nD | 26 | 34'),[
 ['EASY','How many paper bags did the four groups collect?','130','36+28+40+26=130.',['120','128','136']],
 ['EASY','What is the ratio of plastic bags collected by A to those collected by D?','12:17','24:34 simplifies to12:17.',['17:12','3:4','2:3']],
 ['EASY','How many bags did group C collect in total?','60','40+20=60 bags.',['56','64','58']],
]);
set(table('E-08','Marks in a quiz (points):\nStudent | Round 1 | Round 2 | Round 3\nAsha | 18 | 20 | 22\nBala | 20 | 16 | 24\nCharu | 15 | 21 | 18'),[
 ['EASY','What is Asha’s total score?','60','18+20+22=60 points.',['58','62','64']],
 ['EASY','What is the difference between Bala’s highest and lowest round scores?','8','24−16=8 points.',['6','10','12']],
 ['MEDIUM','How many points did Charu score in Rounds 1 and 3 combined?','33','15+18=33 points.',['30','36','39']],
]);

// Original MEDIUM sets (24 questions).
set(table('M-01','Monthly output (thousand units):\nFactory | Jan | Feb | Mar | Apr\nA | 32 | 40 | 36 | 44\nB | 28 | 35 | 42 | 45\nC | 40 | 38 | 46 | 36'),[
 ['MEDIUM','By what percent did A’s output rise from January to April?','37.5%','(44−32)/32×100=37.5%.',['25%','30%','40%']],
 ['MEDIUM','What is the ratio of B’s four-month output to C’s?','15:16','B=150, C=160 thousand; ratio 150:160=15:16.',['16:15','3:4','4:5']],
 ['MEDIUM','What was the average monthly output of all three factories in March?','41.33 thousand','(36+42+46)/3=124/3=41.33 thousand.',['40 thousand','42 thousand','43.33 thousand']],
]);
set(table('M-02','Travel bookings (people):\nRoute | Mon | Tue | Wed\nNorth | 240 | 300 | 360\nSouth | 180 | 270 | 330\nEast | 200 | 250 | 350\nWest | 160 | 220 | 280'),[
 ['MEDIUM','North bookings on Tuesday were what percent of all Tuesday bookings?','28.85%','Tuesday total=1,040; 300/1,040×100≈28.85%.',['27.5%','30%','32.5%']],
 ['MEDIUM','What is the difference between total North and total West bookings?','240','North=900; West=660; difference=240.',['220','260','280']],
 ['MEDIUM','South bookings increased by what percent from Monday to Wednesday?','83.33%','Increase=150; 150/180×100=83.33%.',['75%','80%','85%']],
]);
set(table('M-03','Library holdings (books):\nSection | Fiction | Science | History\nA | 420 | 280 | 300\nB | 360 | 340 | 250\nC | 480 | 320 | 350'),[
 ['HARD','What percent of all listed books are Science books?','30.32%','Science=940; grand total=3,100; 940/3,100×100≈30.32%.',['28%','32%','35%']],
 ['MEDIUM','Find the ratio of Section C holdings to Section B holdings.','23:19','C=1,150, B=950; 1,150:950=23:19.',['19:23','6:5','5:4']],
 ['MEDIUM','How many more Fiction than History books are listed altogether?','360','Fiction=1,260; History=900; difference=360.',['320','340','400']],
]);
set(table('M-04','Online orders (orders):\nDay | Electronics | Clothing | Home\nMon | 125 | 180 | 95\nTue | 150 | 160 | 110\nWed | 175 | 210 | 105\nThu | 200 | 190 | 130'),[
 ['MEDIUM','Electronics orders on Thursday were what percent more than Monday?','60%','Increase=75; 75/125×100=60%.',['50%','55%','65%']],
 ['MEDIUM','What is the ratio of Clothing orders to Home orders over all four days?','740:440','Clothing=740, Home=440; ratio is 37:22 (equivalently 740:440).',['37:20','22:37','3:2']],
 ['HARD','What was the average total number of orders per day?','457.5','Daily totals 400,420,490,520 sum=1,830; average=457.5.',['450','460','465']],
]);
set(table('M-05','Crop yield (tonnes):\nFarm | Wheat | Rice | Maize\nP | 48 | 36 | 24\nQ | 42 | 45 | 33\nR | 55 | 40 | 25\nS | 35 | 50 | 30'),[
 ['MEDIUM','What percent of the total yield came from Farm R?','25.92%','R=120; total=463; 120/463×100≈25.92%.',['20.5%','24%','27.5%']],
 ['MEDIUM','Find the ratio of total rice yield to total maize yield.','171:112','Rice=171, maize=112.',['3:2','19:14','112:171']],
 ['MEDIUM','How many tonnes did Farms P and S produce together?','223','P=108; S=115; combined=223.',['218','225','230']],
]);
set(table('M-06','Monthly electricity use (kWh):\nHouse | May | June | July\nA | 240 | 300 | 360\nB | 320 | 280 | 400\nC | 200 | 260 | 340'),[
 ['MEDIUM','House A’s July use was what percent of the three houses’ July total?','32.73%','July total=1,100; 360/1,100×100≈32.73%.',['30%','33%','36%']],
 ['MEDIUM','What is the difference between House B’s total and House C’s total use?','200 kWh','B=1,000; C=800; difference=200 kWh.',['180 kWh','220 kWh','240 kWh']],
 ['MEDIUM','By what percent did House A use increase from May to July?','50%','(360−240)/240×100=50%.',['40%','45%','60%']],
]);
set(table('M-07','Tournament points (points):\nTeam | League | Cup | Friendly\nFalcons | 38 | 24 | 18\nTigers | 32 | 30 | 20\nWolves | 40 | 18 | 26\nEagles | 28 | 34 | 22'),[
 ['MEDIUM','What is the average Friendly score across the four teams?','21.5','(18+20+26+22)/4=86/4=21.5.',['20.5','21','22']],
 ['MEDIUM','League points of Falcons and Wolves together are what percent of all League points?','56.52%','78/(38+32+40+28)×100=78/138×100≈56.52%.',['50%','54%','60%']],
 ['MEDIUM','What is the ratio of Tigers’ total points to Eagles’ total points?','82:84','Tigers=82, Eagles=84; simplifies 41:42.',['42:41','4:5','5:4']],
]);
set(table('M-08','Water supplied (thousand litres):\nZone | Morning | Afternoon | Evening\n1 | 18 | 12 | 15\n2 | 20 | 14 | 16\n3 | 16 | 18 | 14\n4 | 22 | 10 | 20\n5 | 14 | 16 | 18'),[
 ['MEDIUM','What percent of Zone 3’s daily supply was delivered in the afternoon?','37.5%','Zone3 total=48; 18/48×100=37.5%.',['35%','40%','42.5%']],
 ['MEDIUM','Find the ratio of total morning supply to total evening supply.','90:83','Morning=90; evening=83.',['83:90','10:9','9:8']],
 ['MEDIUM','Which zone received the greatest total daily supply?','Zone 4','Totals:45,50,48,52,48; greatest is 52 in Zone4.',['Zone 2','Zone 3','Zone 5']],
]);

// Original HARD sets (27 questions).
set(table('H-01','Export revenue (million dollars):\nFirm | 2022 | 2023 | 2024\nA | 24 | 30 | 36\nB | 20 | 28 | 32\nC | 18 | 24 | 30\nD | 28 | 26 | 34'),[
 ['HARD','By what percent did combined revenue rise from 2022 to 2024?','46.67%','2022=90; 2024=132; rise 42/90×100=46.67%.',['45%','50%','55%']],
 ['HARD','Firm B’s three-year revenue is what percent of the four firms’ total revenue?','24.24%','B=80; grand total=330; 80/330×100≈24.24%.',['22.5%','25.64%','28%']],
 ['HARD','What is the ratio of Firm A’s 2023–24 revenue to Firm C’s three-year revenue?','11:12','A=66; C=72; ratio=11:12.',['12:11','5:6','7:8']],
]);
set(table('H-02','Vehicle registrations (vehicles):\nRegion | Cars | Motorcycles | Buses\nNorth | 840 | 1260 | 300\nSouth | 720 | 1440 | 360\nEast | 960 | 1080 | 240\nWest | 680 | 1220 | 400'),[
 ['HARD','Motorcycles are what percent of all registrations?','52.63%','Motorcycles=5,000; total=9,500; share≈52.63%.',['45%','48%','55%']],
 ['HARD','If East car registrations rise 12.5%, how many will there be?','1,080','960×1.125=1,080.',['1,060','1,100','1,120']],
 ['HARD','Find the ratio of South and West bus registrations together to North and East car registrations together.','19:45','Buses=760; cars=1,800; ratio=19:45.',['9:19','45:19','2:5']],
]);
set(table('H-03','Department salaries (thousand rupees):\nDepartment | Junior | Senior | Manager\nP | 28 | 42 | 70\nQ | 32 | 48 | 80\nR | 30 | 45 | 75\nS | 36 | 54 | 90'),[
 ['HARD','The workforce proportions of P, Q, R and S are 10:8:12:10. What is the weighted mean salary across the departments?','Rs 45,530','Department means are P=40.6, Q=46.4, R=43.5, S=52.2 thousand. Weighted mean=(10×40.6+8×46.4+12×43.5+10×52.2)/40=45.53 thousand.',['Rs 44,500','Rs 46,465','Rs 48,000']],
 ['HARD','Across all four departments, manager pay is what percent more than junior pay?','150%','Manager total=315; junior total=126; difference/126×100=150%.',['125%','145%','175%']],
 ['HARD','For Department Q, senior salaries are what percent of its combined junior and manager salaries?','42.86%','48/(32+80)×100=42.86%.',['40%','45%','48%']],
]);
set(table('H-04','Production and defects (units):\nPlant | Produced | Defective\nA | 2400 | 48\nB | 3000 | 45\nC | 1800 | 54\nD | 2800 | 56'),[
 ['HARD','Which plant has the lowest defect rate?','B','Rates: A2%, B1.5%, C3%, D2%; minimum B.',['A','C','D']],
 ['HARD','What is the overall defect rate?','2.03%','Defects=203; output=10,000; rate=2.03%.',['1.8%','2.2%','2.5%']],
 ['HARD','If Plant C reduces defects by one-third with unchanged output, how many fewer defects will it have?','18','One-third of 54=18.',['16','20','24']],
]);
set(table('H-05','Exam results (students):\nSchool | Appeared | Passed\nA | 480 | 360\nB | 520 | 390\nC | 450 | 360\nD | 550 | 385'),[
 ['HARD','Which school has the highest pass percentage?','C','Rates: A75%, B75%, C80%, D70%; C highest.',['A','B','D']],
 ['HARD','What percent of all appeared students passed?','74.75%','Passed=1,495; appeared=2,000; 74.75%.',['72.5%','76%','78%']],
 ['HARD','How many additional passes would D need to match School C’s pass rate?','55','At80% of550=440; 440−385=55.',['45','50','60']],
]);
set(table('H-06','Warehouse inventory (crates):\nWarehouse | Start | Received | Dispatched\nA | 620 | 180 | 250\nB | 540 | 260 | 310\nC | 700 | 150 | 420\nD | 480 | 320 | 270'),[
 ['HARD','What is the ratio of total closing stock in A and C to that in B and D?','49:51','Closing A550,C430=980; B490,D530=1,020; ratio49:51.',['51:49','7:6','5:4']],
 ['HARD','Closing stock across all warehouses is what percent of total starting stock?','85.47%','Closing=2,000; start=2,340; 85.47%.',['82.5%','87.5%','90%']],
 ['HARD','If 15% of Warehouse B closing stock is damaged, how many usable crates remain?','416.5','B closing=490; usable=85%×490=416.5.',['410','420','425']],
]);
set(table('H-07','Monthly spending (rupees):\nCategory | January | February | March\nRent | 12000 | 12000 | 12000\nFood | 8000 | 9000 | 7500\nTravel | 3000 | 4500 | 3500\nUtilities | 2500 | 2000 | 3000'),[
 ['HARD','Food was what percent of total three-month spending?','31.01%','Food=24,500; all=79,000; 24,500/79,000×100≈31.01%.',['28%','33%','35%']],
 ['HARD','By what percent did total spending change from January to February?','7.84%','Jan=25,500; Feb=27,500; rise 2,000/25,500=7.84%.',['6.5%','8.5%','10%']],
 ['HARD','In March, rent and food together were what percent of total spending?','75%','19,500/26,000×100=75%.',['70%','72.5%','77.5%']],
]);
set(table('H-08','Passenger counts (thousands):\nStation | 06–09 | 09–12 | 12–15 | 15–18\nP | 18 | 26 | 34 | 22\nQ | 24 | 30 | 28 | 18\nR | 20 | 24 | 36 | 20\nS | 16 | 22 | 30 | 32'),[
 ['HARD','What share of all passengers travelled during 12–15?','32%','12–15=128; total=400; share=32%.',['30%','34%','36%']],
 ['HARD','Station S’s peak-period count (15–18) is what percent greater than its 06–09 count?','100%','(32−16)/16×100=100%.',['80%','90%','110%']],
 ['HARD','Find the ratio of Q’s total to P’s total passengers.','1:1','Q=100 and P=100, ratio 1:1.',['5:4','4:5','6:5']],
]);
set(table('H-09','Crop procurement (tonnes):\nDistrict | Wheat | Rice | Pulses\nA | 150 | 120 | 60\nB | 180 | 90 | 80\nC | 120 | 160 | 70\nD | 210 | 130 | 90'),[
 ['HARD','Rice is what percent of total procurement?','34.25%','Rice=500; total=1,460; 500/1,460×100≈34.25%.',['30%','40%','45%']],
 ['HARD','District C’s pulses are what percent of its wheat and rice combined?','25%','70/(120+160)×100=25%.',['20%','28%','30%']],
 ['HARD','What is the ratio of total wheat and pulses procurement to rice procurement?','48:25','Wheat=660, pulses=300, rice=500; 960:500=48:25.',['25:48','19:10','2:1']],
]);

if (rows.length !== 90) throw new Error(`Expected 90 rows; found ${rows.length}`);
const questions = rows.map(row => ({
  subject_slug: 'maths', subcategory_slug: 'arithmetic-maths', chapter_slug: 'data-interpretation',
  question_text: `${row.dataset}\nQuestion: ${row.prompt}`,
  options: Object.fromEntries(row.values.map((value, index) => ['ABCD'[index], value])),
  correct_option: row.key, explanation: row.calculation, difficulty: row.level,
  is_pyq: false, pyq_year: null, pyq_exam_name: null,
  source: row.source || 'Original SSC-style practice question',
}));
const output = path.join(__dirname, '..', 'data', 'data_interpretation_verified_batch.json');
fs.writeFileSync(output, JSON.stringify({ questions }, null, 2) + '\n');
fs.writeFileSync(path.join(__dirname, '..', 'data', 'data_interpretation_answer_ledger.json'),
  JSON.stringify(rows.map((row, index) => ({ row: index + 1, difficulty: row.level, source: row.source || 'Original', dataset: row.dataset, question: row.prompt, expected_answer: row.answer, calculation: row.calculation })), null, 2) + '\n');
console.log(`Wrote ${questions.length} questions to ${output}`);
