// Build the reviewed Partnership batch from the supplied scanned PDF and original practice items.
const fs = require('node:fs');
const path = require('node:path');

const pdf = [
  ['EASY','Three partners invest Rs 8,000, Rs 6,000 and Rs 4,000 for the same period. If their total profit is Rs 15,453, what is the first partner’s share?',['Rs 7,475','Rs 3,964','Rs 5,854','Rs 6,868'],'D','Their capital ratio is 4:3:2, totaling 9 parts. One part is Rs 1,717, so the first partner receives 4 x 1,717 = Rs 6,868.',5],
  ['EASY','X and Y invest Rs 17,100 and Rs 24,300 for one year. X receives Rs 3,800 profit. What is their total profit?',['Rs 9,200','Rs 9,600','Rs 8,400','Rs 8,800'],'A','The capital ratio is 19:27. If X’s 19 parts equal Rs 3,800, one part is Rs 200; 46 parts equal Rs 9,200.',6],
  ['EASY','Surbhi invests Rs 6,000 for 5 months and Urba invests Rs 5,000 for 6 months. What is their profit ratio?',['36:25','6:5','5:6','1:1'],'D','Profit follows capital x time: 6,000 x 5 : 5,000 x 6 = 30,000:30,000 = 1:1.',7],
  ['MEDIUM','A, B and C invest capital in the ratio 2:3:5 for periods in the ratio 4:5:6. What is the resulting profit ratio?',['08:15:20','05:15:30','08:15:30','07:15:30'],'C','Multiply each capital share by its time: 2x4 : 3x5 : 5x6 = 8:15:30. The matching option is C.',8],
  ['MEDIUM','A, B and C invest in the ratio 8:5:3. Their profit ratio is 4:15:6. What is the ratio of their investment periods?',['1:6:5','2:3:4','1:6:4','2:6:3'],'C','Time is proportional to profit/capital: 4/8 : 15/5 : 6/3 = 1/2:3:2 = 1:6:4.',9],
  ['MEDIUM','S, T and U invest Rs 4,200, Rs 6,300 and Rs 8,400. S leaves after 3 months, T after 6 months, while U stays for 12 months. If profit totals Rs 6,000, what is U’s share?',['Rs 4,200','Rs 3,200','Rs 4,000','Rs 3,600'],'C','Capital-time weights are 4,200x3 : 6,300x6 : 8,400x12 = 1:3:8. U receives 8/12 of Rs 6,000 = Rs 4,000.',10],
  ['EASY','Umar and Avinash invest Rs 10,000 and Rs 15,000. Avinash withdraws his capital after 8 months; the first year’s profit is divided between them. What is the profit ratio?',['3:2','2:3','1:1','1:2'],'C','Their capital-time values are 10,000x12 and 15,000x8, both Rs 120,000; the ratio is 1:1.',11],
  ['EASY','Tarun and Tapan invest Rs 13,000 and Rs 19,500. Tapan withdraws after 8 months; profit is divided after 12 months. What is their profit ratio?',['1:2','3:2','1:1','2:3'],'C','The capital-time values are 13,000x12 and 19,500x8, both 156,000. Their profit ratio is 1:1.',12],
  ['HARD','A invests Rs 76,000. B joins later with Rs 57,000. At year end, profit is split 2:1 in A’s favor. How many months after the start did B join?',['4 months','6 months','3 months','5 months'],'A','Let B invest for t months. 76,000x12 : 57,000t = 2:1, giving 16/t=2 and t=8 months. B joined after 12-8=4 months.',13],
  ['MEDIUM','Ramdas invests Rs 90,000 for a year. Shyamdas joins later with Rs 30,000. If year-end profit is shared 4:1, after how many months did Shyamdas join?',['4 months','3 months','1 month','6 months'],'B','The capital-time ratio 90,000x12 : 30,000xt must be 4:1. Thus 36:t=4:1, so t=9 months; he joined after 3 months.',14],
  ['HARD','B invests one-fifth of a partnership’s total capital for 10 months and receives one-third of the annual profit. For how many months did A invest the remaining capital?',['4 months','6 months','5 months','3 months'],'C','B:A capital ratio is 1:4. Their profit ratio is 1:2, so 1x10 : 4xt = 1:2; 10/(4t)=1/2 and t=5 months.',15],
  ['HARD','A invests one-sixth of the capital for one-sixth of the term; B invests one-third for one-third of the term; C invests the balance throughout. What share of Rs 13,800 does B receive?',['Rs 1,200','Rs 2,400','Rs 3,000','Rs 3,600'],'B','Weights are A 1/36, B 1/9, and C 1/2, or 1:4:18. B receives 4/23 x Rs 13,800 = Rs 2,400.',16],
  ['HARD','A starts with Rs 25 lakh and adds Rs 10 lakh after a year. B starts with Rs 35 lakh and removes Rs 10 lakh after two years. C invests Rs 30 lakh for all three years. What is the profit ratio at year three?',['19:19:18','20:19:18','20:20:19','10:10:9'],'A','Capital-time totals are A 25x1+35x2=95, B 35x2+25x1=95, C 30x3=90. The ratio 95:95:90 reduces to 19:19:18.',17],
  ['MEDIUM','A and B start with Rs 5,000 and Rs 2,500. A halves his capital after 4 months; B halves his after 8 months. If annual profit is Rs 1,950, what is A’s share?',['Rs 1,200','Rs 1,250','Rs 1,150','Rs 1,100'],'A','A’s capital-time is 5,000x4+2,500x8=40,000; B’s is 2,500x8+1,250x4=25,000. A receives 8/13 x 1,950 = Rs 1,200.',18],
  ['HARD','A, B and C invest Rs 2,400, Rs 3,300 and Rs 4,800. A receives one-eighth of total profit as salary, then the remainder is shared by capital. If A receives Rs 390 in all, find total profit.',['Rs 900','Rs 1,200','Rs 1,385','Rs 1,800'],'B','A’s capital fraction of the remaining 7/8 profit is 8/35. His total fraction is 1/8+(7/8)(8/35)=13/40. Thus total profit is 390x40/13=Rs 1,200.',19],
  ['HARD','A and B each begin with Rs 70,000. After 10 months A adds Rs 40,000; two months later B removes Rs 20,000; two months later C joins with Rs 40,000. At the end of 24 months C receives Rs 7,500. What is A’s share?',['Rs 25,500','Rs 20,625','Rs 42,000','Rs 27,000'],'C','Capital-time values are A 70,000x10+110,000x14=2,240,000; B 70,000x12+50,000x12=1,440,000; C 40,000x10=400,000. Their ratio is 28:18:5. A receives 28/5 x Rs 7,500 = Rs 42,000.',20],
  ['EASY','A, B and C invest Rs 13,750, Rs 16,250 and Rs 18,750 for equal periods. If B receives Rs 5,200 profit, what is the difference between C’s and A’s shares?',['Rs 1,600','Rs 1,500','Rs 1,200','Rs 1,800'],'A','Capital ratio is 11:13:15. One part is 5,200/13=400; C minus A is (15-11)x400=Rs 1,600.',21],
  ['EASY','A invests seven times as much as B for the same duration. If the annual profit is Rs 2,75,000, what is A’s share?',['Rs 2,40,625','Rs 2,45,625','Rs 2,42,365','Rs 2,41,225'],'A','A receives 7/8 of the profit: 7/8 x Rs 2,75,000 = Rs 2,40,625.',22],
  ['MEDIUM','Ramesh invests Rs 40,000 at the start. Kevin joins six months later with Rs 20,000. If the year’s profit is Rs 10,000, how much does Kevin receive?',['Rs 2,000','Rs 3,000','Rs 4,000','Rs 2,500'],'A','Their capital-time values are 40,000x12 and 20,000x6, a ratio of 4:1. Kevin receives Rs 2,000.',23],
  ['MEDIUM','Three partners share profit in the ratio 8:7:5 and invest for 7, 8 and 14 months, respectively. What is their capital ratio?',['49:64:20','20:49:64','20:64:49','64:49:20'],'D','Capital is proportional to profit/time: 8/7:7/8:5/14. Multiplying by 56 gives 64:49:20.',24],
  ['MEDIUM','Partners share profit 9:8:11 after investing their capitals for 4, 6 and 18 months. What was the ratio of their capitals?',['81:48:22','27:48:22','81:16:66','27:16:66'],'A','Capital is profit/time: 9/4:8/6:11/18. Multiplying by 36 gives 81:48:22.',25],
  ['HARD','Capitals are in ratio 2:3:5 and durations in ratio 4:2:3. C’s profit exceeds A’s by Rs 1,47,000. Find B’s profit.',['Rs 1,26,000','Rs 1,68,000','Rs 1,05,000','Rs 1,89,000'],'A','Profit weights are 8:6:15. C-A is 7 parts = Rs 1,47,000, so one part is Rs 21,000 and B gets 6 parts = Rs 1,26,000.',26],
];

const originals = [
  ['EASY','Two friends contribute Rs 18,000 and Rs 12,000 for the same 12-month venture. If the venture earns Rs 25,000, how much goes to the first friend?',15000,'The investment ratio is 3:2, so the first friend receives 3/5 x Rs 25,000 = Rs 15,000.'],
  ['EASY','Aarav and Bela put Rs 12,000 and Rs 18,000 into a shop for one year. From Rs 15,000 profit, what is Bela’s portion?',9000,'The capitals are in ratio 2:3; Bela receives 3/5 of Rs 15,000 = Rs 9,000.'],
  ['EASY','Nisha places Rs 24,000 in a venture for 10 months. Dev contributes Rs 40,000; how many months give them equal profit weights?',6,'Set 24,000x10 = 40,000xm. Solving gives m=6 months.'],
  ['EASY','Three equal-duration partners contribute in the ratio 2:5:3. If the distributable profit is Rs 50,000, what does the second partner receive?',25000,'The ratio totals 10 parts. The second partner receives 5/10 x Rs 50,000 = Rs 25,000.'],
  ['EASY','Capital is shared 7:5 between Iqbal and Jai, who invest for equal periods. If profit is Rs 48,000, what is Jai’s share?',20000,'Jai owns 5 of 12 profit parts: 5/12 x Rs 48,000 = Rs 20,000.'],
  ['EASY','Mina invests Rs 20,000 for a full year; Om invests Rs 30,000 for eight months. What is their profit ratio?','1:1','Both capital-time products are Rs 240,000, so the ratio is 1:1.'],
  ['EASY','Ravi, Sita and Tanu share a year’s venture in capital proportions 3:4:5. If the profit is Rs 48,000, what is Sita’s share?',16000,'The total is 12 parts; Sita receives 4/12 x Rs 48,000 = Rs 16,000.'],
  ['EASY','A contributes one-quarter of the capital and B provides the rest. What amount of a Rs 12,000 profit belongs to A?',3000,'A’s quarter of Rs 12,000 is Rs 3,000.'],
  ['EASY','Leena and Mohan invest Rs 15,000 and Rs 25,000 for the same period. How much of their Rs 24,000 profit goes to Leena?',9000,'Their ratio is 3:5; Leena receives 3/8 x Rs 24,000 = Rs 9,000.'],
  ['EASY','A partnership divides Rs 18,000 between its founders in the ratio 2:1. What is the larger share?',12000,'The larger share is 2/3 of Rs 18,000 = Rs 12,000.'],
  ['EASY','A firm earns Rs 60,000. Two partners’ agreed capital ratio is 3:2. Find the first partner’s share.',36000,'Three of five parts equal 3/5 x Rs 60,000 = Rs 36,000.'],
  ['EASY','Pia and Quinn invest in ratio 5:7 for equal periods. How much of a Rs 30,000 profit is Quinn’s?',17500,'Quinn’s share is 7/12 x Rs 30,000 = Rs 17,500.'],
  ['EASY','Asha puts Rs 18,000 in for six months while Bilal puts Rs 9,000 in for a year. If profit is Rs 14,000, how much does Bilal receive?',7000,'Both have equal capital-time weight (Rs 108,000), so Bilal receives half: Rs 7,000.'],
  ['EASY','Two partners’ yearly capital-time contributions are Rs 144,000 apiece. What does each receive from a Rs 6,400 profit?',3200,'Equal capital-time values mean equal profit shares; each receives Rs 3,200.'],
  ['EASY','With equal investment periods, Kunal and Lata contribute in the ratio 4:7. What is Kunal’s share of Rs 22,000?',8000,'Kunal receives 4/11 x Rs 22,000 = Rs 8,000.'],
  ['EASY','A, B and C invest for the same length of time in ratio 2:3:4. If total profit is Rs 54,000, how much does A receive?',12000,'A has 2/9 of the capital and profit: Rs 54,000 x 2/9 = Rs 12,000.'],
  ['EASY','A invests Rs 40,000 for a year, while B invests Rs 40,000 for nine months. What portion of a Rs 42,000 profit belongs to A?',24000,'The weights are 40,000x12 : 40,000x9 = 4:3. A gets 4/7 of Rs 42,000 = Rs 24,000.'],
  ['EASY','Three partners receive profit in ratio 3:2:1. If the middle partner gets Rs 2,400, what is the whole profit?',7200,'Two parts equal Rs 2,400, so one part is Rs 1,200; six parts total Rs 7,200.'],
  ['EASY','A and B invest Rs 40,000 and Rs 60,000 for one year. What does A earn from a Rs 25,000 profit?',10000,'A owns 2/5 of the capital, so A receives Rs 10,000.'],
  ['EASY','A small firm has Rs 100,000 capital; Noor supplies Rs 20,000 for the full year. If profit is Rs 15,000, what is Noor’s share?',3000,'Noor contributes one-fifth of the capital-time, so the share is Rs 3,000.'],
  ['EASY','Asha invests Rs 24,000 for a year. Bina invests Rs 36,000 for eight months. Their total profit is Rs 14,000. What does each partner receive?',7000,'Both weights are Rs 288,000, so they divide profit equally: Rs 7,000 apiece.'],
  ['EASY','A, B and C invest Rs 10,000, Rs 15,000 and Rs 25,000 for equal periods. If B receives Rs 4,500, find the total profit.',15000,'B’s 15 of 50 capital parts equal Rs 4,500; total profit is Rs 4,500x50/15 = Rs 15,000.'],
  ['EASY','One partner contributes two-fifths of a firm’s capital for the entire year. What does that partner receive from Rs 10,000 profit?',4000,'The share is 2/5 x Rs 10,000 = Rs 4,000.'],

  ['MEDIUM','A invests Rs 12,000 from the opening day. B joins four months later with Rs 18,000. At the end of 12 months, what is their profit ratio?','1:1','A’s weight is 12,000x12; B’s is 18,000x8. Both equal Rs 144,000, so the ratio is 1:1.'],
  ['MEDIUM','Farah funds Rs 40,000 for all 12 months; Gopal joins after four months with Rs 30,000. If total profit is Rs 42,000, what is Farah’s share?',28000,'Weights are 480,000 and 240,000, or 2:1. Farah receives two-thirds of Rs 42,000 = Rs 28,000.'],
  ['MEDIUM','Jai and Kiran begin with capital in ratio 3:4. Jai withdraws after eight months while Kiran stays the full year. Find the profit ratio.','1:2','Their weights are 3x8 : 4x12 = 24:48 = 1:2.'],
  ['MEDIUM','Asha’s capital is Rs 50,000 for eight months. Bela invests Rs 70,000; what duration gives a profit ratio of 10:21?',12,'Solve 50,000x8 : 70,000xt = 10:21. This gives t=12 months.'],
  ['MEDIUM','Three partners invest Rs 20,000, Rs 30,000 and Rs 40,000. The first and third stay 12 months; the second leaves after eight. What is the profit ratio?','1:1:2','Weights are 240,000:240,000:480,000, reducing to 1:1:2.'],
  ['MEDIUM','A partner starts with Rs 36,000 and adds Rs 24,000 after six months. What is that partner’s capital-time total for the first year?',576000,'The first amount contributes 36,000x12=432,000; the added capital contributes 24,000x6=144,000; total Rs 576,000.'],
  ['MEDIUM','M and N each begin with Rs 30,000. After four months M withdraws one-third of the capital; N leaves the full amount. What is M:N profit ratio after 12 months?','7:9','M’s weight is 30,000x4+20,000x8=280,000; N’s is 360,000, giving 7:9.'],
  ['MEDIUM','A working partner earns a fixed Rs 3,000 management allowance from Rs 27,000 profit. The remaining amount is split 2:1. What is the working partner’s total receipt if they hold the two-part share?',19000,'After the allowance, Rs 24,000 remains; the partner gets 2/3 of it, Rs 16,000. Adding Rs 3,000 gives Rs 19,000.'],
  ['MEDIUM','A invests Rs 48,000 for 12 months and B invests Rs 60,000 for part of the year. If profits are equal, for how many months was B’s capital committed?',9,'Set 48,000x12=60,000xt. Thus t=9 months.'],
  ['MEDIUM','A joins a venture with Rs 25,000 after three months. The original partner had Rs 40,000 from the start. What is their year-end profit ratio?','32:15','The weights are 40,000x12 and 25,000x9, or 480:225 = 32:15.'],
  ['MEDIUM','A and B contribute equal capital. After six months, A removes half; B keeps the full amount to year end. Find A:B profit ratio.','3:4','A has 6+3=9 capital-month units while B has 12; ratio 3:4.'],
  ['MEDIUM','A partnership earns Rs 72,000. A and B’s capital-time weights are 5:7. What is the difference between their profit shares?',12000,'The difference is 2/12 of Rs 72,000 = Rs 12,000.'],
  ['MEDIUM','R and S invest in the ratio 4:5. R stays 12 months; S stays 8 months. What is the profit ratio?','6:5','Multiply capital by duration: 4x12:5x8 = 48:40 = 6:5.'],
  ['MEDIUM','A joins a business after two months with Rs 24,000. B started with Rs 18,000 and stayed all year. What is A’s share of Rs 19,000 profit?',10000,'A’s weight is 24,000x10=240,000; B’s is 18,000x12=216,000, ratio 10:9. A receives 10/19x19,000 = Rs 10,000.'],
  ['MEDIUM','K and L invest Rs 32,000 and Rs 48,000. After four months K doubles the capital; L leaves the original amount unchanged. Find the annual profit ratio.','10:9','K’s weight is 32,000x4+64,000x8=640,000; L’s is 48,000x12=576,000; ratio 10:9.'],
  ['MEDIUM','After a Rs 4,000 allowance, the partners split Rs 36,000 in ratio 5:4. What is the larger share of that remainder?',20000,'Five of nine parts of Rs 36,000 equal Rs 20,000.'],
  ['MEDIUM','Three equal capital investments remain for 12, 9 and 6 months. If the first partner receives Rs 8,000, how much does the second receive?',6000,'The profit ratio follows duration, 12:9:6; the second share is 9/12 x Rs 8,000 = Rs 6,000.'],
  ['MEDIUM','P and Q invest in capital ratio 7:5 for equal periods. P later gives one-quarter of P’s capital share to a new R for the final four months of a year. What is the final profit ratio?','77:60:7','For the first eight months P:Q weights are 7:5; in the final four months P retains 21/4 units and R receives 7/4. Totals: P 77, Q 60, R 7.'],
  ['MEDIUM','A contributes Rs 60,000 for 12 months. B contributes Rs 45,000 and joins after four months. If total profit is Rs 30,000, what is B’s share?',10000,'Weights are 720,000 and 360,000, so B receives one-third of the profit: Rs 10,000.'],
  ['MEDIUM','A partner puts Rs 50,000 in for a full year. A second partner joins with Rs 75,000 after four months. If the second partner earns Rs 15,000, what is the total profit?',30000,'Weights are 600,000 and 600,000, so the shares are equal; total profit is Rs 30,000.'],
  ['MEDIUM','A and B share profit in ratio 3:2 after capital-time weights are 9:6. If A receives Rs 18,000, what is B’s share?',12000,'The weights reduce to 3:2. B receives 2/3 of A’s share, Rs 12,000.'],
  ['MEDIUM','A invests Rs 24,000 for 12 months. B invests Rs 36,000 but exits after eight months. What amount of profit does A receive from a total of Rs 18,000?',9000,'Both capital-time weights are 288,000, so A receives half: Rs 9,000.'],

  ['HARD','A invests Rs 60,000 for 12 months. B joins after three months with Rs 80,000, then withdraws Rs 20,000 after another five months. Find their profit ratio at year end.','9:8','A has 720,000 weight. B has 80,000x5+60,000x4=640,000; ratio 9:8.'],
  ['HARD','A and B begin with Rs 50,000 and Rs 70,000. After six months A adds Rs 30,000; after eight months B removes Rs 20,000. What is the profit ratio after one year?','39:38','A:50,000x6+80,000x6=780,000. B:70,000x8+50,000x4=760,000. Ratio 39:38.'],
  ['HARD','Three partners’ starting capitals are 2:3:4. After four months the first doubles its stake; after six months the third withdraws half. What is the year-end profit ratio?','10:9:9','Capital-months: A 2x4+4x8=40; B 3x12=36; C 4x6+2x6=36. Ratio 10:9:9.'],
  ['HARD','A working partner receives Rs 5,000 salary from annual profit. The remainder is divided 3:2, and the worker takes the larger share. If the worker receives Rs 32,000 altogether, find total profit.',50000,'The worker receives Rs 5,000 plus 3/5 of the remainder. Thus Rs 27,000 is 3/5 of the remainder; the remainder is Rs 45,000 and total profit is Rs 50,000.'],
  ['HARD','A invests Rs 90,000 for a year. B joins with Rs 60,000 after three months. C joins after six months with Rs 1,20,000. If total profit is Rs 52,000, find C’s share.',16000,'Weights are 1,080,000:540,000:720,000 = 6:3:4; C receives 4/13xRs 52,000 = Rs 16,000.'],
  ['HARD','A, B and C invest in the ratio 5:4:3. After four months A withdraws 40% of the stake; B adds half of B’s stake after six months; C stays unchanged. Find the annual profit ratio.','11:15:9','Using capital-months: A 5x4+3x8=44; B 4x6+6x6=60; C 3x12=36. Ratio 11:15:9.'],
  ['HARD','A and B start with Rs 80,000 and Rs 60,000. A removes Rs 20,000 after four months; B adds Rs 30,000 after eight months. What is B’s share-to-total-profit ratio?','21:41','A weight is 80,000x4+60,000x8=800,000. B weight is 60,000x8+90,000x4=840,000. B’s fraction is 840/1,640 = 21/41.'],
  ['HARD','Two partners receive profits in ratio 7:5. The first invested Rs 84,000 for 10 months; the second invested Rs 60,000 for how many months?',10,'Set 84,000x10 : 60,000xt = 7:5. Solving gives t=10 months.'],
  ['HARD','Three partners invest in ratio 4:5:6. The first stays 12 months, the second joins after two months, and the third leaves after eight months. Find their profit ratio.','24:25:24','Weights are 4x12:5x10:6x8 = 48:50:48, reducing to 24:25:24.'],
  ['HARD','A working partner takes Rs 6,000 salary from Rs 66,000 total profit. The rest is shared 5:4, and the working partner is the four-part partner. What does that partner receive altogether?',32666.67,'After salary Rs 60,000 remains. Four-ninths is Rs 26,666.67; including salary gives Rs 32,666.67.'],
  ['HARD','A starts with Rs 1,00,000; B joins after four months with Rs 1,50,000. C joins after six months with Rs 2,00,000. If profit is Rs 96,000, find B’s share.',32000,'Weights are A 1,200,000; B 1,200,000; C 1,200,000. Each gets Rs 32,000.'],
  ['HARD','A and B invest in ratio 3:5. A stays all year; B withdraws one-fifth of capital after five months. What is the profit ratio?','36:53','Weights: A 36 units; B 5x5+4x7=53 units. Ratio 36:53.'],
  ['HARD','A and B invest Rs 1,20,000 and Rs 90,000. A withdraws half after six months; B adds Rs 30,000 after four months. What is B’s share of Rs 39,000 profit?',21450,'A weight: 120,000x6+60,000x6=1,080,000. B:90,000x4+120,000x8=1,320,000. Ratio 9:11; B receives Rs 21,450.'],
  ['HARD','A contributes Rs 75,000 for the full year. B contributes Rs 1,00,000, joins after three months and withdraws one-quarter after nine months. Find the profit ratio.','12:11','A weight is 900,000. B weight is 100,000x6+75,000x3=825,000; ratio 24:22 =12:11.'],
  ['HARD','A, B and C put Rs 40,000, Rs 50,000 and Rs 60,000 into a venture. After six months A doubles the stake; after three months B leaves; C stays all year. What is the profit ratio?','8:5:8','Weights: A 40,000x6+80,000x6=720,000; B 50,000x9=450,000; C 60,000x12=720,000. Ratio 8:5:8.'],
  ['HARD','A and B share profit 3:2. A’s capital is Rs 72,000 for 10 months. If B invests Rs 1,20,000, how long was B’s capital in the firm?',4,'Set 72,000x10 : 120,000xt = 3:2; this gives t=4 months.'],
  ['HARD','A invests Rs 54,000 for 12 months. B joins with Rs 72,000 after three months. C invests Rs 90,000 for the final six months. If B receives Rs 24,000, find the total profit.',68000,'Weights are 648,000:648,000:540,000 = 6:6:5. B has 6/17 of the total; total profit is Rs 68,000.'],
  ['HARD','A and B invest equally at first. After four months A doubles the contribution; after eight months B doubles theirs. What is their profit ratio at year end?','5:4','A’s capital-time units are 4+2x8=20; B’s are 8+2x4=16. Ratio 5:4.'],
  ['HARD','A starts with Rs 1,50,000. B joins after four months with Rs 1,20,000. C joins at month six with Rs 90,000. Express C’s profit share as a ratio of total profit.','9:55','Weights are 1,800,000, 960,000 and 540,000, totaling 3,300,000. C’s share to total is 540:3,300 = 9:55.'],
  ['HARD','A and B contribute capital in ratio 5:4. A keeps the stake for 12 months; B increases capital by 50% after four months. What is the profit ratio?','15:16','Weights: A 5x12=60; B 4x4+6x8=64. Ratio 15:16.'],
  ['HARD','A and B share profit 4:3. A invested Rs 96,000 for 10 months. B invested Rs 80,000; how many months did B invest?',9,'Set 96,000x10 : 80,000xt =4:3, giving t=9 months.'],
  ['HARD','A puts Rs 40,000 for 12 months, B puts Rs 60,000 for eight months, and C puts Rs 80,000 for six months. From Rs 57,000 profit, what does C get?',19000,'Each capital-time product is Rs 480,000, so C receives one-third = Rs 19,000.'],
  ['HARD','A and B begin with Rs 50,000 and Rs 80,000. At month six A adds Rs 20,000; at month nine B removes Rs 30,000. Find their profit ratio.','24:29','A weight 50,000x6+70,000x6=720,000; B 80,000x9+50,000x3=870,000. Ratio 24:29.'],
];

function optionsFor(answer, index) {
  const ratio = /^\d+(?::\d+)+$/.test(String(answer));
  let vals;
  if (ratio) {
    const parts = String(answer).split(':').map(Number);
    vals = [parts.join(':'), ...parts.map((value, part) => parts.map((n, i) => n + (i === part ? 1 : 0)).join(':'))];
    while (vals.length < 4) {
      const candidate = parts.map((n, i) => n + (i === parts.length - 1 ? vals.length - 1 : 0)).join(':');
      if (!vals.includes(candidate)) vals.push(candidate);
      else vals.push(parts.map((n, i) => n + (i === 0 ? vals.length : 0)).join(':'));
    }
  } else {
    const n = Number(answer);
    const step = Math.max(1, Math.round(Math.abs(n) * 0.1));
    vals = [...new Set([n, n+step, n-step, n+2*step, n-2*step].filter(x => x > 0))].slice(0,4);
    while (vals.length < 4) vals.push(n + (vals.length+1)*step);
  }
  const correctAt = index % 4;
  const correctVal = String(vals.shift());
  vals.splice(correctAt, 0, correctVal);
  const unit = /capital-time total/i.test(originals[index][1]) ? 'Rs-months' : /how many months|how long|what duration|for how many months/i.test(originals[index][1]) ? 'months' : 'Rs';
  const options = Object.fromEntries('ABCD'.split('').map((key, i) => [key, ratio ? vals[i] : `${Number.isInteger(Number(vals[i])) ? Number(vals[i]) : Number(Number(vals[i]).toFixed(2))} ${unit}`]));
  return {options, correct_option:'ABCD'[correctAt]};
}
function row(difficulty, question_text, options, correct_option, explanation, source) {
  return {subject_slug:'maths',subcategory_slug:'arithmetic-maths',chapter_slug:'partnership',question_text,options,correct_option,explanation,difficulty,is_pyq:false,pyq_year:null,pyq_exam_name:null,source};
}
const rows = pdf.map(([d,stem,opts,key,explanation,page]) => row(d,stem,Object.fromEntries('ABCD'.split('').map((k,i)=>[k,opts[i]])),key,explanation,`Verified from supplied Partnership PDF, page ${page}; exam/year not stated`));
for (let i=0;i<originals.length;i++) {
  const [d,stem,answer,explanation]=originals[i]; const choice=optionsFor(answer,i);
  rows.push(row(d,stem,choice.options,choice.correct_option,explanation,'Original SSC-style practice question'));
}
const counts = Object.fromEntries(['EASY','MEDIUM','HARD'].map(level=>[level,rows.filter(r=>r.difficulty===level).length]));
if (rows.length!==90 || JSON.stringify(counts)!==JSON.stringify({EASY:30,MEDIUM:30,HARD:30})) throw new Error(`Expected 90 balanced items; got ${JSON.stringify(counts)} (${rows.length})`);
fs.writeFileSync(path.join(__dirname,'..','data','partnership_verified_batch.json'),`${JSON.stringify({questions:rows},null,2)}\n`,'utf8');
console.log(`Wrote ${rows.length}: PDF ${pdf.length}, original ${originals.length}, ${JSON.stringify(counts)}`);
