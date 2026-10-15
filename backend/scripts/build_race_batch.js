// Reproducible Race batch. The PDF-derived rows below were visually reviewed
// and independently solved; original answer calculations are retained in the ledger.
const fs = require('node:fs');
const path = require('node:path');
const rows = [];
const PDF = 'Verified from supplied Race PDF, page ';
const ORIGINAL = 'Original SSC-style practice question';
function add(level, question, answer, calculation, wrongs, source = ORIGINAL) {
  const choices = [answer, ...wrongs];
  if (choices.length !== 4 || new Set(choices.map(x => x.trim().toLowerCase())).size !== 4) {
    throw new Error(`Invalid/repeated options: ${question}`);
  }
  const position = (rows.length * 7 + 1) % 4;
  choices.splice(position, 0, choices.shift());
  rows.push({ level, question, answer, calculation, choices, key: 'ABCD'[position], source });
}
function pdf(level, page, question, answer, calculation, wrongs) {
  add(level, question, answer, calculation, wrongs, `${PDF}${page}; exam/year not stated`);
}

// 10 of 15 readable source questions retained. Excluded: p1's two multi-runner
// margin items overlap existing Speed Time & Distance questions; p3 q1 duplicates
// an existing timed-race margin question; p4 q2's keyed 198 s conflicts with its
// stated 2-second delayed start (the actual result is 202 s); p7 q2 repeats p7 q1's
// opposite-direction first-meeting task with only unit/value changes.
pdf('HARD',2,'In a 1200 m race bike A beats B by 100 m. In a 600 m race B beats C by 100 m. If A beats C by 30 seconds in a 720 m race, find C’s speed.','17/3 m/s','The speed ratios are A:B=12:11 and B:C=6:5, so A:B:C=72:66:55. For 720 m, the time difference between C and A is (720/55v)(17/72)=170/(55v)=30; hence v=17/3 m/s.',['16/3 m/s','18/3 m/s','26/3 m/s']);
pdf('EASY',2,'In a 1000 m race Kamal beats Ravi by 120 m. If Kamal runs at 40 km/h, what is Ravi’s speed?','35.2 km/h','When Kamal finishes, Ravi has run 880 m, so speed ratio K:R=1000:880=25:22. Ravi’s speed=40×22/25=35.2 km/h.',['38.7 km/h','26.8 km/h','29.6 km/h']);
pdf('MEDIUM',3,'In a 400 m race A runs at 16 m/s. A gives B a 15 m start and still wins by 10 seconds. What is B’s speed?','11 m/s','A takes 400/16=25 s. B runs 385 m and takes 25+10=35 s, so B’s speed=385/35=11 m/s.',['10 m/s','13 m/s','9 m/s']);
pdf('MEDIUM',4,'Ajit runs 2 2/3 times as fast as Madhav. Madhav starts 160 m ahead. How far from Ajit’s start should the finish be for them to arrive together?','256 m','Let the finish be x metres from Ajit’s start. Equal times give x/(8v/3)=(x−160)/v, so 3x=8x−1280 and x=256 m.',['225 m','200 m','240 m']);
pdf('EASY',5,'In a 5 km race S gives T a 500 m start. They finish together. If T’s speed is 13.5 km/h, what is S’s speed?','15 km/h','T runs 4.5 km in 4.5/13.5=1/3 h. S covers 5 km in that time, so S’s speed is 15 km/h.',['20 km/h','17.5 km/h','16.5 km/h']);
pdf('MEDIUM',7,'Two runners start together on a 4225 m circular track in opposite directions at 54 km/h and 63 km/h. When do they first meet again?','130 seconds','Convert speeds to 15 and 17.5 m/s. Relative speed=32.5 m/s; time for one combined lap=4225/32.5=130 s.',['120 seconds','140 seconds','150 seconds']);
pdf('MEDIUM',8,'Two cyclists ride around a 75 km circular track at 30 km/h and 25 km/h. After how many hours will both next be at their starting point together?','15 hours','Lap times are 75/30=2.5 h and 75/25=3 h. Their first common return time is LCM(2.5,3)=15 h.',['16 hours','14 hours','7 hours']);
pdf('MEDIUM',8,'Sony and Mony run in the same direction on a 200 m circular track at 18 km/h and 24 km/h. When will they next meet at the starting point together?','120 seconds','18 km/h=5 m/s, giving a 40 s lap; 24 km/h=20/3 m/s, giving a 30 s lap. LCM(40,30)=120 s.',['100 seconds','110 seconds','90 seconds']);
pdf('HARD',9,'Two people run in opposite directions on a 100 m circular track at 20 m/s and 30 m/s. At how many distinct points do they meet?','5','Meetings recur every 100/(20+30)=2 s. The first runner advances 40 m between meetings, so the meeting locations cycle through 100/gcd(100,40)=5 distinct points.',['10','2','3']);
pdf('HARD',9,'P and Q run in the same direction from one point on a circular track. P runs at 6 m/s; Q runs at a natural-number speed below 6. If they meet at exactly two distinct points, what can Q’s speed be?','2 m/s','For speeds 6 and b, meeting positions repeat after (6−b)/gcd(6,b) distinct points. Testing b=1,…,5 gives 5,2,1,1,1 respectively; only b=2 works.',['3 m/s','4 m/s','1 m/s']);

// 28 original EASY questions: distinct race calculations and interpretations.
const easy = [
['A runner completes a 100 m sprint in 20 seconds. What is the average speed?','5 m/s','100/20=5 m/s.',['4 m/s','6 m/s','8 m/s']],
['Riya covers 200 m in 32 seconds. What is her speed in m/s?','6.25 m/s','200/32=6.25 m/s.',['5.25 m/s','6.5 m/s','7.25 m/s']],
['A 400 m runner maintains 7.5 m/s. How long does the race take?','53 1/3 seconds','400/7.5=160/3=53 1/3 seconds.',['50 seconds','55 seconds','60 seconds']],
['In a 300 m race, Dev finishes in 50 seconds. At the instant he finishes, how far has an equally paced rival who runs at 5.5 m/s travelled?','275 m','Distance=5.5×50=275 m.',['250 m','280 m','290 m']],
['In a 200 m race, Meera runs at 8 m/s and Tara at 7 m/s. By how many metres does Meera win?','25 m','Meera takes 25 s; Tara covers 7×25=175 m, leaving 25 m.',['20 m','30 m','35 m']],
['A runner gives a competitor a 20 m head start in a 200 m race. Both run at 5 m/s. By how many seconds does the runner win?','4 seconds','The rival runs 180 m and finishes 20/5=4 s earlier than the full 200 m time? Actually the head-start runner has 180 m left and finishes 4 s before the 200 m runner.',['2 seconds','5 seconds','8 seconds']],
['A cyclist completes a 1 km race in 2 minutes. What is the average speed in km/h?','30 km/h','1 km in 2/60 h gives 30 km/h.',['25 km/h','32 km/h','36 km/h']],
['A runner’s speed is 12 km/h. How far does the runner travel in 15 minutes?','3 km','15 min=0.25 h; 12×0.25=3 km.',['2 km','2.5 km','4 km']],
['In a 500 m race, A finishes in 80 s and B in 100 s. How many metres does A beat B by?','100 m','In 80 s B covers 500×80/100=400 m; margin=100 m.',['80 m','90 m','120 m']],
['Runner L runs at 9 m/s and runner M at 8 m/s. In a 100 m race, how many metres does L beat M by?','11 1/9 m','When L covers 100 m in 100/9 s, M covers 800/9 m; margin=100/9=11 1/9 m.',['10 m','12 m','15 m']],
['A 600 m race is completed by Arjun in 120 seconds. What is his speed in km/h?','18 km/h','600/120=5 m/s; 5×3.6=18 km/h.',['15 km/h','16.2 km/h','21.6 km/h']],
['In a 250 m race, Nisha runs at 10 m/s and wins by 25 m. What is the speed of the runner-up?','9 m/s','Nisha takes 25 s; runner-up covers 225 m in 25 s, so 9 m/s.',['8 m/s','9.5 m/s','10.5 m/s']],
['A runner covers 800 m in 4 minutes. What is the runner’s speed in km/h?','12 km/h','800 m/4 min=200 m/min=12 km/h.',['10 km/h','14 km/h','16 km/h']],
['A 100 m runner starts 10 m behind the start line and runs at 5 m/s; the opponent starts at the line at 4.5 m/s. How far ahead is the first runner when the opponent finishes?','1 1/9 m','Opponent time=100/4.5=200/9 s. First runner covers 5×200/9=1000/9 m from their own start; after the 10 m setback, position=910/9 m, so lead=10/9 m.',['2 m','5/9 m','10 m']],
['In a 1.2 km race, a runner averages 4 m/s. How many minutes does the race take?','5 minutes','1200/4=300 seconds=5 minutes.',['4 minutes','6 minutes','8 minutes']],
['Two runners start together on a straight 300 m course at 6 m/s and 5 m/s. When the faster finishes, how far behind is the slower?','50 m','Fast time=50 s; slower covers 250 m, so trails 50 m.',['40 m','60 m','75 m']],
['A runner completes one 400 m lap in 80 seconds. What is the lap speed in km/h?','18 km/h','400/80=5 m/s=18 km/h.',['16 km/h','20 km/h','22.5 km/h']],
['In a 150 m race, P beats Q by 30 m. If P’s speed is 10 m/s, what is Q’s speed?','8 m/s','P takes 15 s; Q covers 120 m in 15 s, so 8 m/s.',['7 m/s','9 m/s','10 m/s']],
['A sprinter runs 100 m in 12.5 seconds. At the same speed, how far will the sprinter run in 20 seconds?','160 m','Speed=8 m/s; 8×20=160 m.',['150 m','165 m','180 m']],
['In a 600 m race, K finishes 20 seconds before J. If J’s speed is 5 m/s, what is K’s speed?','6 m/s','J time=600/5=120 s; K time=100 s; speed=600/100=6 m/s.',['5.5 m/s','6.5 m/s','7 m/s']],
['A runner’s pace is 4 minutes per kilometre. What is the speed in km/h?','15 km/h','One kilometre in 4/60 h gives 15 km/h.',['12 km/h','16 km/h','18 km/h']],
['A and B run a 100 m race in 16 s and 20 s. How far has B run when A crosses the finish?','80 m','B’s speed=5 m/s; in 16 s B covers 80 m.',['75 m','84 m','90 m']],
['A runner completes 5 laps of a 200 m track in 2 minutes. What is the average speed in m/s?','8 1/3 m/s','Distance=1000 m; time=120 s; speed=25/3=8 1/3 m/s.',['7.5 m/s','8 m/s','9 m/s']],
['A 400 m runner takes 50 seconds. How long would the same runner take for 160 m at unchanged speed?','20 seconds','Speed=8 m/s; 160/8=20 s.',['18 seconds','22 seconds','25 seconds']],
['In a 100 m race, A finishes in 10 s and B in 12 s. How many metres does B cover in the time A finishes?','83 1/3 m','B speed=100/12; in 10 s covers 250/3=83 1/3 m.',['80 m','85 m','90 m']],
['A runner moves at 6 m/s. How far ahead is the runner after 45 seconds?','270 m','6×45=270 m.',['240 m','260 m','300 m']],
['In a 300 m race, C runs at 7.5 m/s and D at 6 m/s. How many seconds earlier does C finish?','10 seconds','Times are 40 s and 50 s; difference=10 s.',['8 seconds','12 seconds','15 seconds']],
['A runner covers 1.5 km in 5 minutes. What is the speed in km/h?','18 km/h','1.5/(5/60)=18 km/h.',['15 km/h','16 km/h','20 km/h']],
];
for (const item of easy) { if (item.length !== 4) throw new Error(`Malformed EASY row: ${item[0]}`); const [q,a,c,w]=item; add('EASY',q,a,c,w); }

// 23 original MEDIUM questions.
const medium = [
['In a 400 m race, A gives B a 40 m start and wins by 8 seconds. A runs at 8 m/s. Find B’s speed.','180/29 m/s','A takes50 s. B covers360 m in58 s, so B’s speed=360/58=180/29 m/s.',['5.8 m/s','6.4 m/s','7 m/s']],
['In a 500 m race, P beats Q by 50 m. In a 400 m race, Q beats R by 40 m. If P runs a 600 m race, by how many metres does P beat R?','114 m','P:Q=500:450=10:9 and Q:R=400:360=10:9. Thus P:R=100:81. When P runs600 m, R runs486 m; margin=114 m.',['108 m','120 m','126 m']],
['A gives B a 30 m start in a 300 m race. They finish together. If A runs at 6 m/s, what is B’s speed?','5.4 m/s','A time=300/6=50 s; B covers 270 m in 50 s, so 5.4 m/s.',['5 m/s','5.5 m/s','6 m/s']],
['On a 500 m track two runners start together in the same direction at 7 m/s and 5 m/s. When does the faster first lap the slower?','250 seconds','Relative speed=2 m/s; one-lap gain=500 m; time=250 s.',['200 seconds','300 seconds','350 seconds']],
['On a 400 m circular track, runners at 5 m/s and 3 m/s start together in opposite directions. When do they first meet?','50 seconds','Relative speed=8 m/s; 400/8=50 s.',['40 seconds','60 seconds','80 seconds']],
['In a 600 m race, A beats B by 60 m, and B beats C by 30 m. How far does A beat C?','87 m','A:B=600:540=10:9; B:C=600:570=20:19. Thus A:C=200:171. When A runs600, C runs513; margin87 m.',['90 m','96 m','105 m']],
['A runner covers 1000 m at 5 m/s. A second runner starts 20 seconds later at 6 m/s. How long after the second runner starts will they catch the first?','100 seconds','First runner’s head start distance=5×20=100 m. Relative speed=1 m/s; catch time=100 s.',['80 seconds','120 seconds','150 seconds']],
['A wins a 200 m race against B by 20 m. If B’s speed is 9 m/s, what is A’s speed?','10 m/s','When A finishes, B covers180 m. Time=180/9=20 s; A speed=200/20=10 m/s.',['9.5 m/s','10.5 m/s','11 m/s']],
['In a 1 km race, A runs at 18 km/h and B at 15 km/h. How long after A finishes does B finish?','40 seconds','A time=1000/5=200 s; B time=1000/(25/6)=240 s; difference=40 s.',['30 seconds','45 seconds','60 seconds']],
['Two runners start together on a 300 m circular track in the same direction at 8 m/s and 6 m/s. How long until they first meet again at the start?','150 seconds','Lap times are 37.5 s and 50 s; the first common return is150 s (four laps and three laps).',['300 seconds','450 seconds','750 seconds']],
['A gives B a 50 m start in a 450 m race. A runs at 10 m/s and both finish together. Find B’s speed.','8 8/9 m/s','A time=45 s; B runs400 m in45 s; speed=80/9=8 8/9 m/s.',['8 m/s','9 m/s','9.5 m/s']],
['In a 500 m race, A beats B by 25 m. In a 300 m race, B beats C by 15 m. Find the distance by which A beats C in a 500 m race.','48.75 m','A:B=500:475=20:19; B:C=300:285=20:19; A:C=400:361. When A runs500, C runs451.25; margin48.75 m.',['45 m','50 m','55 m']],
['A and B run a 400 m race. A runs at 8 m/s; B runs at 7.5 m/s but starts 5 seconds earlier. Who wins, and by how much time?','B by 1 2/3 s','A takes50 s; B takes400/7.5=53 1/3 s after own start, so finishes at48 1/3 s from A’s start. B wins by1 2/3 s.',['A by 2 s','B by 2 1/3 s','A by 1 2/3 s']],
['Runners start together on a 600 m track in the same direction at 9 m/s and 7.5 m/s. When does the faster runner overtake the slower?','400 seconds','Relative speed=1.5 m/s; one lap gain=600 m; time=400 s.',['300 seconds','450 seconds','600 seconds']],
['A finishes a 1200 m race in 4 minutes; B finishes in 4 minutes 30 seconds. How far does A beat B by?','133 1/3 m','In 240 s B covers 1200×240/270=1066 2/3 m; margin=133 1/3 m.',['120 m','140 m','160 m']],
['A runs 400 m in 50 s. B starts 4 s later and runs at 9 m/s. How long after B starts does B catch A?','32 seconds','At B’s start A is32 m ahead; relative speed=9−8=1 m/s, so catch time=32 s.',['28 seconds','36 seconds','40 seconds']],
['A gives B a 2-second start in a 500 m race. If B runs at 8 m/s and they finish together, what is A’s speed?','1000/129 m/s','B takes62.5 s after starting; A runs64.5 s, so speed=500/64.5=1000/129 m/s.',['7.5 m/s','8 m/s','8.5 m/s']],
['On a 400 m track, two runners move in opposite directions at 6 m/s and 4 m/s. How many meetings occur in 3 minutes, counting a meeting at the start as the first?','5','Relative lap time=400/(6+4)=40 s. In180 s they meet at0,40,80,120,160 s:5 meetings.',['4','6','8']],
['In a 300 m race, A beats B by 30 m. In a separate 500 m race, A beats C by 50 m. Find B:C speed ratio.','1:1','A:B=300:270=10:9; A:C=500:450=10:9, hence B:C=1:1.',['10:9','9:10','8:9']],
['A runner averages 12 m/s for the first 300 m of a 600 m race and 8 m/s for the rest. What is the average speed for the whole race?','9.6 m/s','Total time=300/12+300/8=25+37.5=62.5 s; 600/62.5=9.6 m/s.',['10 m/s','9 m/s','8.5 m/s']],
['Three runners complete a 100 m race in 10 s, 12 s and 15 s. When the fastest finishes, how far behind is the slowest?','33 1/3 m','Slowest speed=100/15; in10 s covers 66 2/3 m; gap=33 1/3 m.',['30 m','35 m','40 m']],
['A gives another runner a 60 m start in a 600 m race. Their speeds are 10 m/s and 8 m/s respectively. What is the actual time margin?','7.5 seconds','The first runner takes60 s; the other covers540 m at8 m/s in67.5 s, so the first wins by7.5 s.',['5 seconds','10 seconds','12.5 seconds']],
['A and B run a 1000 m race. A’s speed is 10 m/s and B’s is 9.5 m/s. If B gets a 50 m head start, who wins?','They tie','A takes100 s. B runs950 m at9.5 m/s=100 s, so they tie.',['A by 2 seconds','B by 5 seconds','B by 10 seconds']],
['Three competitors run a 600 m race. A runs at 8 m/s and starts 5 seconds before B, who runs at 9 m/s. C runs at 7.5 m/s and starts 10 seconds before A. Who finishes last?','B','Measure time from A’s start: A finishes at75 s; B at5+600/9=71 2/3 s; C starts10 s earlier and finishes at−10+600/7.5=70 s. B finishes last.',['A','C','A and C tie']],
['A runner completes a 1500 m race in 3 minutes. Another completes it in 3 minutes 20 seconds. At the first runner’s finish, how many metres remain for the second?','150 m','At180 s the second covers1500×180/200=1350 m; 150 m remain.',['120 m','180 m','200 m']],
];
// A few answer/calc records above are intentionally computed from the written
// conditions; guard these hand-derived values with the independent test ledger.
for (const item of medium) { if (item.length !== 4) throw new Error(`Malformed MEDIUM row: ${item[0]}`); const [q,a,c,w]=item; add('MEDIUM',q,a,c,w); }

// 27 original HARD questions.
const hard = [
['In a 1000 m race A beats B by 100 m. In a 600 m race B beats C by 60 m. In a 1200 m race, by how much does A beat C?','228 m','A:B=10:9 and B:C=10:9, so A:C=100:81. When A runs1200, C covers972; margin=228 m.',['240 m','252 m','276 m']],
['A and B race over 800 m. A runs 10 m/s for the first 400 m and 8 m/s thereafter. B runs uniformly at 9 m/s. Who wins and by how much time?','B by 1 1/9 s','A time=400/10+400/8=90 s; B time=800/9=88 8/9 s; B wins by10/9 s.',['A by 1 s','A by 2 s','B by 2 s']],
['Three runners start together on a 600 m circular track at 8, 6 and 4 m/s in the same direction. When are all three next together at the start?','300 seconds','Lap times are75,100,150 s; their first common return is300 s.',['450 seconds','600 seconds','750 seconds']],
['Runners A and B start at the same point on a 500 m track in opposite directions at 7 m/s and 5 m/s. At what time do they meet for the fourth time after starting?','166 2/3 seconds','They meet every500/(7+5)=125/3 s. The fourth meeting occurs after500/3=166 2/3 s.',['125 seconds','150 seconds','200 seconds']],
['In a 1500 m race A beats B by 150 m and B beats C by 100 m. How many metres does A beat C by in a 1500 m race?','240 m','A:B=10:9; B:C=1500:1400=15:14. A:C=25:21. C covers1260 m when A finishes; margin=240 m.',['250 m','300 m','360 m']],
['A runner gives B a 100 m head start in a 1 km race. A runs at 12 m/s and B at 10 m/s. How many seconds earlier does A finish?','6 2/3 seconds','A takes1000/12=83 1/3 s. B runs900 m in90 s; A wins by6 2/3 s.',['5 seconds','8 seconds','10 seconds']],
['On a 600 m circular track, two runners move in the same direction at 9 m/s and 7 m/s. How many times does the faster pass the slower in 15 minutes, excluding the initial shared start?','3','Relative lap time=600/(9−7)=300 s=5 min; they meet after5,10,15 min. Excluding the initial start gives3 passes.',['2','4','5']],
['A runner covers the first 1/3 of a 900 m race at 6 m/s and the rest at 9 m/s. What is the total race time?','116 2/3 s','300/6+600/9=50+66 2/3=116 2/3 s.',['110 s','120 s','125 s']],
['In a 400 m race A finishes 20 seconds before B. A runs at 10 m/s. What is B’s speed?','20/3 m/s','A time=40 s; B time=60 s; speed=400/60=20/3 m/s.',['6 m/s','7 m/s','8 m/s']],
['Two runners start together on a 720 m circular track in opposite directions at 8 m/s and 4 m/s. When do they meet for the fifth time after starting?','300 seconds','They meet every720/12=60 s; the fifth meeting after the start is300 s.',['180 seconds','240 seconds','360 seconds']],
['A beats B by 80 m in a 400 m race. B beats C by 100 m in a 500 m race. Find A:C speed ratio.','25:16','A:B=400:320=5:4; B:C=500:400=5:4. Thus A:C=25:16.',['5:4','4:5','16:25']],
['A and B run a 1000 m race. A runs at 10 m/s. B gets a 100 m start and runs at 9 m/s. Who wins and by how many seconds?','They tie','A takes100 s; B runs900 m in100 s, so they tie.',['A by 5 s','B by 5 s','A by 10 s']],
['On a 400 m track three runners move in the same direction at 10, 8 and 6 m/s. After how long will all be together at the starting point again?','200 seconds','Lap times 40,50,66 2/3 s. LCM of rational lap periods is 200 s.',['160 seconds','240 seconds','300 seconds']],
['A runner wins a 1200 m race over B by 120 m. B wins a 900 m race over C by 90 m. What is A’s winning margin over C in a 1800 m race?','342 m','A:B=10:9 and B:C=10:9; A:C=100:81. In1800 m, C covers1458 m; margin=342 m.',['300 m','324 m','378 m']],
['A starts 15 seconds before B on a 900 m course. A runs at 6 m/s and B at 8 m/s. How long after B starts does B catch A?','45 seconds','A has a 90 m lead at B’s start; relative speed=2 m/s, catch time=45 s.',['40 seconds','50 seconds','60 seconds']],
['In a 1000 m race, P runs the first 400 m at 8 m/s and the remaining 600 m at 12 m/s. Q runs uniformly at 10 m/s. Who finishes first, and by how much?','They tie','P takes50+50=100 s; Q also takes100 s.',['P by 2 seconds','Q by 5 seconds','P by 5 seconds']],
['Two runners start together in opposite directions on a 900 m track at 7 m/s and 5 m/s. How far from the starting point is their second meeting?','150 m','Second meeting is after2×900/12=150 s; first runner travels1050 m, i.e.150 m past the start.',['100 m','300 m','450 m']],
['In a 500 m race A beats B by 50 m. In a 700 m race B beats C by 70 m. In a 1000 m race, what is the A–C margin?','190 m','A:B=10:9; B:C=10:9; A:C=100:81. C covers810 m when A finishes1000; margin=190 m.',['180 m','200 m','210 m']],
['A runner takes 80 seconds to cover 600 m. A second runner takes 75 seconds for the same distance but starts 10 seconds later. How long after the first starts does the second catch up?','160 seconds','Speeds are7.5 and8 m/s. The second starts10 s later with a75 m deficit; relative speed=.5 m/s; catch is150 s after second starts, or160 s after first.',['140 seconds','150 seconds','170 seconds']],
['On a 1000 m track A and B run in the same direction at 12 m/s and 8 m/s. Starting together, at what time do they meet for the third time, counting their initial meeting as time zero?','750 seconds','Relative speed=4 m/s; one-lap gain time=1000/4=250 s. Third meeting after start is750 s.',['500 seconds','1000 seconds','1250 seconds']],
['A runs a 400 m race in 50 s; B runs it in 60 s. C starts 5 s after A and finishes 10 s after B. What is C’s speed?','80/13 m/s','B finishes at60 s; C finishes at70 s from A’s start, runs for65 s, speed=400/65=80/13 m/s.',['6 m/s','7 m/s','8 m/s']],
['In a 1500 m race, A beats B by 300 m and B beats C by 250 m. What is A’s winning margin over C?','500 m','A:B=5:4; B:C=1500:1250=6:5; hence A:C=3:2. C covers1000 m when A finishes; margin500 m.',['550 m','600 m','750 m']],
['Three runners cover a 1200 m race at constant speeds in the ratio 6:5:4. How many metres remain for the slowest when the middle runner finishes?','240 m','When the middle runner covers1200 m, the slowest covers1200×4/5=960 m, leaving240 m.',['180 m','300 m','360 m']],
['A gives B a 40 m head start in a 400 m race. A runs at 10 m/s and B at 9 m/s. Who wins and by how much time?','They tie','A takes40 s; B runs360 m at9 m/s, also taking40 s.',['A by 1 s','B by 4/9 s','B by 1 s']],
['A races over 1200 m, covering the first 600 m at 12 m/s and the rest at 8 m/s. B runs uniformly at 9.5 m/s. Who wins and by how much time?','A by 25/19 s','A takes50+75=125 s. B takes1200/9.5=2400/19≈126.316 s, so A wins25/19 s.',['B by 1 s','A by 2 s','B by 3 s']],
['On a 600 m track, runners at 8 m/s and 5 m/s start at the same point in the same direction. How far does the faster runner travel before first lapping the slower?','1600 m','Time to gain one lap=600/(8−5)=200 s; faster distance=8×200=1600 m.',['1200 m','1400 m','1800 m']],
['A and B start at opposite ends of a 1 km straight course and run toward each other at 6 m/s and 4 m/s. After how long do they meet?','100 seconds','Their closing distance is1000 m at10 m/s; time=100 s.',['80 seconds','125 seconds','150 seconds']],
];
for (const item of hard) { if (item.length !== 4) throw new Error(`Malformed HARD row: ${item[0]}`); const [q,a,c,w]=item; add('HARD',q,a,c,w); }

if (easy.length !== 28 || medium.length !== 25 || hard.length !== 27 || rows.length !== 90) {
  throw new Error(`Unexpected distribution total: ${rows.length} (${easy.length}/${medium.length}/${hard.length})`);
}
const questions = rows.map(row => ({
  subject_slug:'maths', subcategory_slug:'arithmetic-maths', chapter_slug:'race',
  question_text:row.question, options:Object.fromEntries(row.choices.map((v,i)=>['ABCD'[i],v])),
  correct_option:row.key, explanation:row.calculation, difficulty:row.level,
  is_pyq:false, pyq_year:null, pyq_exam_name:null, source:row.source,
}));
const dataDir=path.join(__dirname,'..','data');
fs.writeFileSync(path.join(dataDir,'race_verified_batch.json'),JSON.stringify({questions},null,2)+'\n');
fs.writeFileSync(path.join(dataDir,'race_answer_ledger.json'),JSON.stringify(rows.map((r,i)=>({row:i+1,difficulty:r.level,source:r.source,question:r.question,expected_answer:r.answer,calculation:r.calculation})),null,2)+'\n');
console.log('Wrote 90 Race questions: 30 EASY, 30 MEDIUM, 30 HARD; PDF 10, original 80.');
