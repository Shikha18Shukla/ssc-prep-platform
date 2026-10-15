// Build the reviewed Train batch. The four retained PDF items have fixed choices;
// original options are generated deterministically around independently solved keys.
const fs = require('node:fs');
const path = require('node:path');

const pdf = [
  ['HARD','Two trains of equal length run on parallel tracks. They cross in opposite directions at 65 km/h and 85 km/h in 6 seconds. Find the length of each train.',['100 m','115 m','125 m','150 m'],'C','Their combined length is (65+85)×5/18×6=250 m. Equal lengths are 125 m each.',18],
  ['HARD','Trains of lengths 100 m and 95 m take 27 s to cross in the same direction and 9 s in opposite directions. Find their speeds.',['44 and 22 km/h','52 and 26 km/h','36 and 18 km/h','40 and 20 km/h'],'B','The relative speeds are 195/27=65/9 m/s and 195/9=65/3 m/s. Solving sum and difference gives 130/9 and 65/9 m/s, or 52 and 26 km/h.',21],
  ['HARD','Two trains moving in opposite directions pass a person in 30 s and 18 s. They cross each other in 25 s. What is the ratio of their speeds?',['7:5','5:7','3:2','2:3'],'A','If speeds are u and v, train lengths are 30u and 18v. Then 30u+18v=25(u+v), so 5u=7v and u:v=7:5.',22],
  ['EASY','A passenger counts 31 telegraph posts in 60 seconds while riding a train. Adjacent posts are 60 m apart. What is the train speed in km/h?',['90 km/h','108 km/h','120 km/h','96 km/h'],'B','Thirty intervals cover 30×60=1,800 m in 60 s, giving 30 m/s=108 km/h.',24],
];

const originals = [
['EASY','A commuter train covers 156 km in 2 hours 30 minutes without stopping. What is its average speed?','62.4 km/h','Convert 2 h 30 min to 2.5 h. Average speed=156/2.5=62.4 km/h.'],
['EASY','A train travels at 16 m/s for 75 seconds. How far does it go?','1200 m','Distance=speed×time=16×75=1,200 m.'],
['EASY','At 90 km/h, how many metres does a train cover in 20 seconds?','500 m','90 km/h=25 m/s. In 20 seconds it covers 25×20=500 m.'],
['EASY','A train covers 315 km at a constant 70 km/h. How long is the journey?','4.5 h','Time=distance/speed=315/70=4.5 hours.'],
['EASY','An express train runs 84 km in 1 hour 12 minutes. Find its average speed.','70 km/h','1 hour 12 minutes=1.2 hours; 84/1.2=70 km/h.'],
["EASY","A passenger train has 12 coaches, each 16 m long, with a 2 m gap between consecutive coaches. At 72 km/h, how long does it take to pass a signal?","10.7 s","Train length including the 11 gaps is 12×16+11×2=214 m. At 72 km/h=20 m/s, the pass takes 214/20=10.7 s."],
["EASY","A train travels at 72 km/h from the kilometer marker 84 to the kilometer marker 89. How many seconds does the trip take?","250 s","The markers are 5 km apart. At 72 km/h, the train covers 1.2 km per minute; 5/1.2=25/6 minutes=250 seconds."],
['EASY','A 240 m train runs at 72 km/h. How many seconds does it take to pass a stationary person?','12 s','72 km/h=20 m/s, so time=240/20=12 s.'],
['EASY','A train travelling at 18 m/s passes a 90 m platform in 20 seconds. What is the train length?','270 m','Total distance=18×20=360 m. Subtract the platform: 360−90=270 m.'],
["EASY","A 72 km route takes how many minutes less at 72 km/h than at 60 km/h?","12 min","At 60 km/h the trip takes 72/60=1.2 h; at 72 km/h it takes 1 h. The difference is 0.2 h=12 min."],
['EASY','Two trains move toward each other at 48 km/h and 66 km/h. What is their relative speed in m/s?','31.6667 m/s','Opposite-direction speeds add: 114×5/18=31.6667 m/s.'],
['EASY','Two trains travel in the same direction at 88 km/h and 61 km/h. Find their relative speed.','27 km/h','Same-direction relative speed is the difference: 88−61=27 km/h.'],
['EASY','A 360 m train travels at 90 km/h. How long does it take to pass a pole?','14.4 s','90 km/h=25 m/s; 360/25=14.4 s.'],
['EASY','An express travels 180 km between terminals, taking 2 hours 45 minutes including a 15-minute stop. What is its average speed while moving?','72 km/h','Moving time is 2.5 hours. Average running speed=180/2.5=72 km/h.'],
['EASY','A local train covers 198 km at 66 km/h. Find its travel time.','3 h','Time=198/66=3 hours.'],
['EASY','A train covers 1,050 m in 70 seconds. What is its speed in m/s?','15 m/s','Speed=1,050/70=15 m/s.'],
["EASY","A 540 m tunnel is crossed at 54 km/h. For 12 seconds, the whole train is inside the tunnel. Find the train length.","360 m","At 54 km/h the train travels 15 m/s. While it is fully inside, it travels 15×12=180 m; train length=540−180=360 m."],
['EASY','A train passes a lamp post in 9 seconds at 20 m/s. Find its length.','180 m','Train length=speed×time=20×9=180 m.'],
['EASY','A train is 275 m long and moves at 55 km/h. How long will it take to cross a person standing beside the track?','18 s','55 km/h=275/18 m/s; time=275÷(275/18)=18 s.'],
["EASY","A train travels at 72 km/h for 25 minutes and then at 60 km/h for 35 minutes, without stopping. How far does it travel in total?","65 km","The first part is 72×25/60=30 km; the second is 60×35/60=35 km. Total distance=65 km."],
['EASY','A train runs at 12.5 m/s. Express this speed in km/h.','45 km/h','12.5×18/5=45 km/h.'],
['EASY','A 225 m train crosses a bridge in 30 seconds at 45 km/h. What is the bridge length?','150 m','45 km/h=12.5 m/s. Total distance=375 m; bridge=375−225=150 m.'],
['EASY','A train covers 144 km in 96 minutes. Find its speed in km/h.','90 km/h','96 minutes=1.6 hours; 144/1.6=90 km/h.'],
['EASY','A 300 m train passes a trackside marker at 25 m/s. How long does the pass take?','12 s','Time=300/25=12 s.'],
['EASY','Two trains have speeds 72 km/h and 54 km/h and move toward each other. Find their relative speed in km/h.','126 km/h','For opposite directions, add the speeds: 72+54=126 km/h.'],
['EASY','A train travels 42 km in 36 minutes. What is its average speed?','70 km/h','36 minutes=0.6 h; 42/0.6=70 km/h.'],
['EASY','A 150 m train crosses a 250 m platform at 20 m/s. Find the time to clear it.','20 s','Total distance=150+250=400 m; 400/20=20 s.'],
['EASY','At 48 km/h, how far does a train travel in 25 seconds?','333.3333 m','48 km/h=40/3 m/s; distance=(40/3)×25=1,000/3 m.'],
['EASY','A train of length 192 m passes a pole in 12 seconds. What is its speed in km/h?','57.6 km/h','Speed=192/12=16 m/s; 16×18/5=57.6 km/h.'],

['MEDIUM','A 240 m train crosses a 360 m platform in 30 seconds. Find its speed in km/h.','72 km/h','Total distance=600 m; speed=20 m/s=72 km/h.'],
["MEDIUM","Two trains start 90 km apart and travel toward each other. After 30 minutes, they are still 15 km apart. If the first train travels at 72 km/h, find the speed of the second.","78 km/h","In 30 minutes the trains close 90\u221215=75 km, so their combined speed is 75/0.5=150 km/h. The second speed is 150\u221272=78 km/h."],
["MEDIUM","A train takes 30 seconds from its front entering a 600 m tunnel until its rear exits. It remains completely inside the tunnel for 10 seconds. Find its speed in km/h.","108 km/h","Let train length be L and speed v. The full-crossing interval gives L+600=30v; the interval when the whole train is inside gives 600\u2212L=10v. Adding, 1,200=40v, so v=30 m/s=108 km/h."],
['MEDIUM','A 180 m train overtakes a 120 m train moving at 36 km/h. The pass takes 30 seconds. Find the faster train speed.','72 km/h','Relative speed=300/30=10 m/s=36 km/h. Faster speed=36+36=72 km/h.'],
['MEDIUM','Two trains 150 m and 210 m long approach each other at 54 km/h and 72 km/h. How long to cross completely?','10.2857 s','Combined length=360 m. Relative speed=126×5/18=35 m/s; time=360/35=10.2857 s.'],
['MEDIUM','A train leaves a station at 60 km/h. Another leaves the same station 30 minutes later at 90 km/h. How long after the second departure will it catch the first?','1 h','The first gains 30 km. Closing speed=90−60=30 km/h, so catch-up time=1 h.'],
['MEDIUM','Two stations are 330 km apart. Trains leave simultaneously toward each other at 80 km/h and 70 km/h. When do they meet?','2.2 h','Combined speed=150 km/h; meeting time=330/150=2.2 h.'],
['MEDIUM','A 250 m train clears a 350 m platform in 30 seconds. How long does it take to pass a signal post at that speed?','12.5 s','Speed=(250+350)/30=20 m/s. Pole time=250/20=12.5 s.'],
['MEDIUM','A train at 72 km/h takes 18 seconds to pass a pole. How long to cross a 180 m platform?','27 s','Train length=20×18=360 m. Total crossing distance=540 m; time=540/20=27 s.'],
['MEDIUM','A 300 m train passes a cyclist moving in the same direction at 12 km/h in 18 seconds. Find the train speed.','72 km/h','Relative speed=300/18=16.6667 m/s=60 km/h. Add cyclist speed: train=72 km/h.'],
['MEDIUM','A train running at 90 km/h passes a person walking at 6 km/h in the same direction in 12 seconds. Find the train length.','280 m','Relative speed=84 km/h=70/3 m/s. Length=(70/3)×12=280 m.'],
['MEDIUM','A 400 m train passes a 200 m train moving in the same direction at 45 km/h in 48 seconds. Find the faster train speed.','90 km/h','Relative speed=600/48=12.5 m/s=45 km/h; faster speed=45+45=90 km/h.'],
['MEDIUM','A train covers the first 120 km of a trip at 60 km/h and the next 120 km at 80 km/h. Find its average speed for the whole trip.','68.5714 km/h','Total time=2+1.5=3.5 h; average speed=240/3.5=68.5714 km/h.'],
['MEDIUM','A train travels 210 km at 70 km/h, stops for 20 minutes, then travels 140 km at 70 km/h. Find its overall average speed including the stop.','65.625 km/h','Moving time=3+2=5 h; total time=5 h 20 min=16/3 h. Average=350÷(16/3)=65.625 km/h.'],
["MEDIUM","A 300 m train passes a pole in 20 seconds, and a 360 m train passes a pole in 18 seconds. How much faster is the second train?","5 m/s","Their speeds are 300/20=15 m/s and 360/18=20 m/s. The second is 20−15=5 m/s faster."],
['MEDIUM','A train passes a 240 m platform in 24 seconds at 54 km/h. How long is the train?','120 m','Speed=15 m/s; total distance=360 m. Train length=360−240=120 m.'],
['MEDIUM','Two trains are 210 km apart and travel toward each other at 65 km/h and 75 km/h. How far does the faster train travel before they meet?','112.5 km','Meeting time=210/(65+75)=1.5 h. Faster train covers 75×1.5=112.5 km.'],
['MEDIUM','A 240 m train overtakes a 160 m train moving at 48 km/h in 32 seconds. Find the speed of the faster train.','93 km/h','Relative speed=400/32=12.5 m/s=45 km/h. Faster speed=48+45=93 km/h.'],
["MEDIUM","A train is to average 72 km/h over a 240 km journey. It covers the first 120 km at 60 km/h. What speed must it maintain for the second half?","90 km/h","The target total time is 240/72=10/3 hours. The first half takes 120/60=2 hours, leaving 4/3 hours for 120 km. Required speed=120\u00f7(4/3)=90 km/h."],
['MEDIUM','Two trains of equal length cross in the same direction in 40 seconds and in opposite directions in 8 seconds. The faster train travels at 72 km/h. Find the slower speed.','48 km/h','For equal lengths, relative-speed ratio (opposite/same) is 40/8=5. Let speeds be u,v: (u+v)/(u−v)=5, so u=1.5v. Thus v=48 km/h.'],
['MEDIUM','A train at 108 km/h passes a pole in 10 seconds. How long does it take to pass a 250 m platform?','18.3333 s','Speed=30 m/s; train length=300 m. Total distance=550 m; time=550/30=18.3333 s.'],
['MEDIUM','A train passes a 90 m platform in 15 seconds at 36 km/h. What is the train length?','60 m','36 km/h=10 m/s; total distance=150 m. Subtract 90 m to get 60 m.'],
['MEDIUM','A train moving at 72 km/h overtakes a jogger running at 9 km/h in the same direction in 20 seconds. Find the train length.','350 m','Relative speed=63 km/h=17.5 m/s; length=17.5×20=350 m.'],
['MEDIUM','Two trains start 280 km apart and travel in the same direction at 82 km/h and 62 km/h. How long until the faster one catches the slower one?','14 h','Closing speed=20 km/h; catch-up time=280/20=14 h.'],
["MEDIUM","A train clears 80 m, 120 m, and 160 m platforms in 18 s, 20 s, and 22 s, respectively. Find the train length.","280 m","Increasing platform length by 40 m adds 2 s, so speed=20 m/s. On the 80 m platform, total distance is 20×18=360 m; train length=360−80=280 m."],
["MEDIUM","A train covers one-third of a 180 km route at 60 km/h and the remaining two-thirds at 90 km/h. How many minutes does the full trip take?","140 min","The first 60 km takes 1 h. The remaining 120 km takes 120/90=4/3 h=80 min. Total=140 min."],
['MEDIUM','A train travels at 80 km/h for 45 minutes, waits 15 minutes, then travels at 60 km/h for 1 hour. Find average speed for the whole period.','60 km/h','Distance=60+60=120 km; total elapsed time=2 h; average=60 km/h.'],
['MEDIUM','Two trains leave stations 360 km apart at 8 a.m. and travel toward each other at 45 km/h and 75 km/h. At what time do they meet?','11 a.m.','Their combined speed is 120 km/h; they meet after 360/120=3 hours, at 11 a.m.'],
['MEDIUM','Two trains leave stations 540 km apart at the same time and travel toward each other. If one travels at 63 km/h and they meet after 4 hours, find the other speed.','72 km/h','In 4 hours they close 540 km, so their combined speed is 135 km/h. The unknown speed is 135−63=72 km/h.'],
['MEDIUM','Two stations are 450 km apart. A train leaves one at 7 a.m. at 60 km/h; another leaves the other station at 8 a.m. at 90 km/h toward it. How long after 8 a.m. will they meet?','2.6 h','By 8 a.m. the first train has covered 60 km, leaving 390 km. Their closing speed is 150 km/h, so the remaining time is 390/150=2.6 hours.'],

["HARD","A 360 m train travels at 72 km/h through a 600 m station platform. For how many seconds is the entire train on the platform, from its rear entering until its front leaves?","12 s","From rear entry to front exit, the train advances platform length minus train length: 600−360=240 m. At 72 km/h=20 m/s, the interval is 240/20=12 s."],
["HARD","A 240 m train passes one cyclist moving in the same direction in 20 seconds and another cyclist moving in the opposite direction in 12 seconds. The two cyclists travel at the same speed. Find the train speed.","57.6 km/h","Relative speed with the first cyclist is 240/20=12 m/s, so the train is 12 m/s faster than the cyclist. With the second cyclist it is 240/12=20 m/s, the sum. Train speed is (12+20)/2=16 m/s=57.6 km/h."],
['HARD','Two trains, 300 m and 200 m long, overtake in 40 seconds in the same direction and cross in 10 seconds in opposite directions. Find the faster train speed.','112.5 km/h','Combined length=500 m. Difference speed=500/40=12.5 m/s; sum speed=500/10=50 m/s. Faster speed=(50+12.5)/2=31.25 m/s=112.5 km/h.'],
['HARD','Two trains start 420 km apart and move toward each other. One travels at 15 m/s and the other at 20 m/s. How long until they meet?','3 h 20 min','Combined speed=35 m/s. Time=420,000/35=12,000 s=3 h 20 min.'],
["HARD","A 390 m train takes 45 seconds from its front reaching the first pole until its rear clears the 18th pole. If adjacent poles are 30 m apart, find the train speed.","20 m/s","From front reaching pole 1 to rear clearing pole 18, the front travels 390+17×30=900 m. Speed=900/45=20 m/s."],
['HARD','A 360 m train passes a person walking at 6 km/h in the same direction in 24 seconds. Find the train speed.','60 km/h','Relative speed=360/24=15 m/s. Add 6 km/h (5/3 m/s): train speed=50/3 m/s=60 km/h.'],
['HARD','A train travels 180 km at 60 km/h, stops 20 minutes, then covers 240 km. What speed is needed on the second leg for a 5-hour total journey?','144 km/h','First leg takes 3 h and stop takes 1/3 h; remaining time=5−10/3=5/3 h. Speed=240÷(5/3)=144 km/h.'],
["HARD","A 300 m train passes a pole in 20 seconds, and a 180 m train passes a pole in 12 seconds. If they move in opposite directions, how long will they take to cross each other?","16 s","Their speeds are 300/20=15 m/s and 180/12=15 m/s. Opposite-direction relative speed=30 m/s; combined length=480 m. Crossing time=480/30=16 s."],
["HARD","A train covers a 120 km route each way. Its return speed is 25% higher than its outward speed. If total round-trip travel time is 3 hours 36 minutes, find its outward speed.","60 km/h","Let the outward speed be v. The return speed is 1.25v. Thus 120/v+120/(1.25v)=216/v=3.6 h, giving v=60 km/h."],
["HARD","A train's length and a platform's length are in the ratio 3:2. At 72 km/h, the train clears the platform in 25 seconds. Find the train length.","300 m","The train travels (72\u00d75/18)\u00d725=500 m while clearing the platform. This is 5 ratio parts, so one part is 100 m; train length is 3\u00d7100=300 m."],
['HARD','Two trains leave the same point in opposite directions at 54 km/h and 72 km/h. After 40 minutes, how far apart are they?','84 km','Combined speed=126 km/h; 40 min=2/3 h; separation=126×2/3=84 km.'],
['HARD','A 280 m train passes a bridge in 24 seconds. At the same speed, it passes a 160 m tunnel in 20 seconds. Find the train speed.','30 m/s','The bridge is 120 m longer than the tunnel; this extra distance takes 4 s. Speed=30 m/s.'],
["HARD","A 240 km train trip arrives 20 minutes late when it averages 72 km/h and 20 minutes early when it averages 90 km/h. What is the scheduled travel time?","3 h","At 72 km/h the travel time is 240/72=3 h 20 min, so the schedule is 3 h. At 90 km/h it is 240/90=2 h 40 min, also 20 minutes before that schedule."],
['HARD','A 220 m train overtakes a 180 m train travelling at 45 km/h in 32 seconds. How long to cross that train in the opposite direction if the faster train runs at 90 km/h?','10.6667 s','The first relative speed is 400/32=12.5 m/s=45 km/h; hence the other train moves at 45 km/h. Opposite relative speed=135 km/h=37.5 m/s; time=400/37.5=10.6667 s.'],
["HARD","Two trains each cover the same 180 km route. The faster train travels 15 km/h faster and takes one hour less. Find the slower train's speed.","45 km/h","Let the slower speed be v. The time difference is 180/v\u2212180/(v+15)=1. Solving 180\u00d715=v(v+15) gives v=45 km/h; the faster speed is 60 km/h."],
['HARD','A 400 m train moving at 90 km/h overtakes a 240 m train in 32 seconds. Find the slower train speed.','18 km/h','Combined length=640 m; relative speed=640/32=20 m/s=72 km/h. Slower speed=90−72=18 km/h.'],
['HARD','A train travels 150 km at 50 km/h, then 180 km at 60 km/h, then 120 km at 80 km/h. Find its average speed.','60 km/h','Total distance=450 km. Time=3+3+1.5=7.5 h; average=450/7.5=60 km/h.'],
['HARD','A train passes a pole in 8 seconds and a 240 m bridge in 20 seconds. It crosses another train of length 180 m in 10 seconds in the opposite direction. Find the other speed.','50.4 km/h','Speed=240/12=20 m/s, length=160 m. Relative speed=(160+180)/10=34 m/s; other=14 m/s=50.4 km/h.'],
['HARD','A train covers 300 km. It travels the first half at 60 km/h and the second half at 100 km/h. How long is the whole trip?','4 h','The halves are 150 km each: times 2.5 h and 1.5 h, total 4 h.'],
['HARD','Two trains start from stations 510 km apart and travel toward each other at 68 km/h and 82 km/h. How far from the first station do they meet?','231.2 km','Meeting time=510/150=3.4 h. Distance from first station=68×3.4=231.2 km.'],
['HARD','An express covers 300 km at 75 km/h but is delayed 40 minutes en route. What is its average speed from departure to arrival?','64.2857 km/h','Running time=4 h; elapsed time=4 h 40 min=14/3 h. Average speed=300÷(14/3)=450/7=64.2857 km/h.'],
["HARD","A train passes a person walking toward it at 6 km/h in 12 seconds and a jogger moving in the same direction at 9 km/h in 20 seconds. Find the train speed.","31.5 km/h","Let the train speed be v m/s and length L. The opposite-direction pass gives L=12(v+5/3); the same-direction pass gives L=20(v\u22122.5). Equating gives v=8.75 m/s=31.5 km/h."],
['HARD','Two trains 240 m and 160 m long cross in opposite directions in 8 seconds. Their speeds differ by 18 km/h. Find the faster train speed.','99 km/h','Sum speed=400/8=50 m/s=180 km/h. Difference=18 km/h; faster speed=(180+18)/2=99 km/h.'],
["HARD","Two trains start 360 km apart and travel toward each other. The first travels at 72 km/h for its first hour, then at 108 km/h; the second travels at 72 km/h throughout. How long until they meet?","2.2 h","In the first hour they cover 72+72=144 km, leaving 216 km. Their later closing speed is 108+72=180 km/h, requiring 1.2 hours. Total time=2.2 hours."],
["HARD","A train is 395 m long and is made of identical 20 m coaches with 5 m gaps between consecutive coaches. How many coaches does it have?","16 coaches","For n coaches, total length=20n+5(n\u22121)=25n\u22125. Setting this to 395 gives 25n=400, so n=16."],
['HARD','A train completes a 240 km trip at 80 km/h but makes a 30-minute stop. What average speed does it maintain over the full elapsed time?','68.5714 km/h','Running time=3 h; elapsed time=3.5 h. Average=240/3.5=68.5714 km/h.'],
["HARD","A 240 m train passes a pole in 20 seconds, and a 360 m train passes a pole in 24 seconds. If they move in the same direction, how long does the faster train take to overtake the slower one?","200 s","Their speeds are 240/20=12 m/s and 360/24=15 m/s. Relative speed=3 m/s; distance to pass=240+360=600 m. Time=600/3=200 s."],
];

function normalized(s){return s.normalize('NFKC').toLowerCase().replace(/\s+/g,' ').trim();}
function numericOptions(answer,index){
  const m=answer.match(/^(-?[\d,]+(?:\.\d+)?)(.*)$/);
  if(!m) throw new Error(`unsupported answer: ${answer}`);
  const target=Number(m[1].replace(/,/g,'')), suffix=m[2], decimals=(m[1].split('.')[1]||'').length;
  const step=Math.max(target>=10?1:0.1,Math.abs(target)*0.1), values=[target];
  for(let k=1;values.length<4;k++){const n=Number((target+(k%2?1:-1)*Math.ceil(k/2)*step).toFixed(decimals));if(n>=0&&!values.includes(n))values.push(n);}
  const opts=values.map(v=>`${v}${suffix}`);const correct=opts.shift();opts.splice(index%3,0,correct);
  return {options:Object.fromEntries('ABCD'.split('').map((key,i)=>[key,opts[i]])),correct_option:'ABCD'[opts.indexOf(correct)]};
}
function row(level,stem,options,correct,explanation,source){return {subject_slug:'maths',subcategory_slug:'arithmetic-maths',chapter_slug:'train',question_text:stem,options,correct_option:correct,explanation,difficulty:level,is_pyq:false,pyq_year:null,pyq_exam_name:null,source};}
const rows=pdf.map(([level,stem,options,key,explanation,page])=>row(level,stem,Object.fromEntries('ABCD'.split('').map((k,i)=>[k,options[i]])),key,explanation,`Verified from supplied Train PDF, page ${page}; exam/year not stated`));
let ordinal=0;
for(const [level,stem,answer,explanation] of originals){const g=numericOptions(answer,ordinal++);rows.push(row(level,stem,g.options,g.correct_option,explanation,'Original SSC-style practice question'));}
const counts=Object.fromEntries(['EASY','MEDIUM','HARD'].map(level=>[level,rows.filter(r=>r.difficulty===level).length]));
if(rows.length!==90||JSON.stringify(counts)!==JSON.stringify({EASY:30,MEDIUM:30,HARD:30}))throw new Error(`Wrong batch shape ${rows.length} ${JSON.stringify(counts)}`);
const out=path.join(__dirname,'..','data','train_verified_batch.json');fs.writeFileSync(out,JSON.stringify({questions:rows},null,2)+'\n','utf8');
console.log('WROTE',rows.length,out,'DIFFICULTY',counts,'PROVENANCE',{pdf:pdf.length,original:originals.length});
