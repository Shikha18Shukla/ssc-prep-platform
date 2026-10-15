// Build the reviewed Pipe & Cistern batch from the supplied PDF and original practice items.
const fs = require('node:fs');
const path = require('node:path');

const pdf = [
  ['EASY','Two pipes fill a tank separately in 30 minutes and 20 minutes. How long will they take together?',['15 min','12 min','18 min','9 min'],'B','Their rates are 1/30 + 1/20 = 1/12 tank per minute, so the tank fills in 12 minutes.',5],
  ['EASY','A reservoir is filled by two pipes in 24 minutes and 40 minutes. How long do they take together?',['33 min','45 min','15 min','20 min'],'C','Combined rate = 1/24 + 1/40 = 1/15 tank per minute, so it takes 15 minutes.',6],
  ['EASY','Pipes A and B fill a tank in 5 hours and 10 hours; pipe C empties it in 20 hours. If all start together, when is the tank full?',['6 h','5 h','4 h','10 h'],'C','Net rate = 1/5 + 1/10 - 1/20 = 1/4 tank per hour, so filling takes 4 hours.',7],
  ['EASY','Two inlets fill a tank in 20 and 30 minutes, while an outlet empties it in 60 minutes. Starting empty, how long do all three take to fill it?',['13 min','14 min','15 min','None of the above'],'C','Net rate = 1/20 + 1/30 - 1/60 = 1/15 tank per minute, so it takes 15 minutes.',8],
  ['EASY','An inlet fills a tank in 16 hours. With a bottom leak open, it fills in 24 hours. How long would the leak alone take to empty a full tank?',['41 h','43 h','48 h','50 h'],'C','The leak rate is 1/16 - 1/24 = 1/48 tank per hour, so it empties a full tank in 48 hours.',9],
  ['MEDIUM','Tap A fills a tank in 40 hours and tap B in 50 hours. Both start together, then A is closed; the tank is full after 25 hours total. After how long was A closed?',['12 h','25 h','15 h','20 h'],'D','B supplies 25/50 = 1/2 of the tank in 25 hours. A must supply the other half at 1/40 tank per hour, requiring 20 hours.',10],
  ['HARD','Two inlets fill a tank in 15 and 12 minutes. A waste pipe removes 22 gallons per minute. All three together fill the empty tank in 20 minutes. What is the tank capacity?',['200 gal','210 gal','220 gal','230 gal'],'C','The inlets supply 1/15 + 1/12 = 3/20 tank per minute. Net rate is 1/20, so the waste rate is 1/10 tank per minute. If that is 22 gal/min, capacity is 220 gallons.',11],
  ['HARD','Two pipes fill a tank in 10 and 12 minutes. A vent pipe removes 9 gallons per minute. Together they fill the empty tank in 30 minutes. What is the capacity?',['60 gal','180 gal','120 gal','240 gal'],'A','The inlets supply 1/10 + 1/12 = 11/60 tank per minute. Net rate 1/30 leaves 9/60 = 3/20 tank per minute for the vent. Thus capacity = 9 ÷ (3/20) = 60 gallons.',12],
  ['HARD','Pipes A and B fill a tank in 20 and 24 minutes. Pipe C empties it at 3 gallons per minute. All three together fill it in 15 minutes. Find the capacity.',['180 gal','150 gal','120 gal','60 gal'],'C','A and B supply 1/20 + 1/24 = 11/120 tank per minute. The net is 1/15 = 8/120, so C removes 3/120 tank per minute. At 3 gal/min, capacity is 120 gallons.',13],
  ['HARD','A fills a tank in 3 hours, B in 4 hours, and C empties it in 1 hour. A opens at 3 p.m., B at 4 p.m., and C at 5 p.m. When will the tank be empty?',['7:12 p.m.','7:15 p.m.','7:10 p.m.','7:18 p.m.'],'A','Using 12 units/hour, A adds 4 units from 3–4 and A+B add 7 units from 4–5, leaving 11 units at 5 p.m. Their net rate afterward is 4+3-12=-5 units/hour, so draining takes 11/5 hours = 2 h 12 min. The tank empties at 7:12 p.m.',14],
  ['HARD','A fills a tank in 15 hours, B in 12 hours, and C empties it in 4 hours. They open at 8 a.m., 9 a.m., and 11 a.m., respectively. When will the tank be empty?',['11:40 a.m.','12:40 p.m.','1:40 p.m.','2:40 p.m.'],'D','In 60 units/hour, A adds 4 units in the first hour and A+B add 18 in the next two hours, so 22 units are present at 11 a.m. The combined net rate is 4+5-15=-6 units/hour; emptying takes 22/6 = 3 h 40 min. The time is 2:40 p.m.',15],
  ['MEDIUM','A fills a tank in 4 hours and B in 6 hours. They run alternately for one hour each, starting with A. How long until the tank is full?',['4 1/2 h','4 2/3 h','3 1/2 h','3 1/4 h'],'B','In 12 units, A adds 3 units/hour and B 2. Two hours add 5 units. After two cycles (4 hours), 10/12 is full; A supplies the remaining 2 units in 2/3 hour. Total = 4 2/3 hours.',16],
  ['MEDIUM','A fills a tank in 20 minutes and B empties it in 30 minutes. They operate alternately for one minute each, starting with A. How long until the tank is full?',['121 min','110 min','115 min','120 min'],'C','In 60 units, A adds 3 units/minute and B removes 2. Each two-minute cycle adds 1 unit. After 57 cycles (114 minutes), 57 units are present; A adds the final 3 units in one minute. Total = 115 minutes.',17],
  ['HARD','Pipes P and Q fill a tank in 15 and 45 minutes; R empties it in 30 minutes. P, then Q, then R are opened for one minute each, repeatedly. How long until the tank is full?',['51 5/6 min','18 min','54 min','51 4/9 min'],'A','In 90 units/minute, P adds 6, Q adds 2, and R removes 3 each minute. A three-minute cycle adds 5 units. After 17 cycles (51 minutes), 85 of 90 units are present; P supplies the remaining 5 units in 5/6 minute.',18],
  ['HARD','P fills a tank in 5 hours, Q in 6 hours, and R empties it in 10 hours. P, Q, and R open at 6 a.m., 7 a.m., and 8 a.m. in that order, then repeat hourly. When is the tank full?',['4:30 p.m.','3:30 p.m.','4:00 p.m.','3:00 p.m.'],'C','In 30 units/hour, P adds 6, Q adds 5, and R removes 3. Each three-hour cycle adds 8 units; after three cycles (9 hours), 24/30 is full. P then supplies the remaining 6 units in one hour. Starting at 6 a.m., the tank is full at 4 p.m.',19],
];

const originals = [
  ['EASY','Pipe A fills a tank in 12 minutes and pipe B in 18 minutes. How long do they take working together?','7.2 min','Combined rate = 1/12 + 1/18 = 5/36 tank per minute. Time = 36/5 = 7.2 minutes.'],
  ['EASY','One inlet fills a cistern in 8 hours and another in 12 hours. How long will both take together?','4.8 h','Combined rate = 1/8 + 1/12 = 5/24 tank per hour. Time = 24/5 = 4.8 hours.'],
  ['EASY','A pipe fills a tank in 15 minutes and a second pipe fills it in 30 minutes. Find their joint filling time.','10 min','Their combined rate is 1/15 + 1/30 = 1/10 tank per minute, so they take 10 minutes.'],
  ['EASY','An inlet fills a tank in 20 hours. A leak would empty a full tank in 60 hours. How long does the inlet take to fill the tank with the leak present?','30 h','Net rate = 1/20 - 1/60 = 1/30 tank per hour, so filling takes 30 hours.'],
  ['EASY','A 960-litre tank is empty. A pipe supplies water at 48 litres per minute. How many minutes are needed to fill it?','20 min','Time = 960/48 = 20 minutes.'],
  ['EASY','One pipe fills 1/4 of a tank in 10 minutes, and another fills 1/6 in 10 minutes. How long do both take to fill the tank?','24 min','Their rates are 1/40 and 1/60 tank per minute, totaling 1/24 tank per minute.'],
  ['EASY','Two pipes fill a tank in 24 and 36 minutes. What is their combined filling time?','14.4 min','Combined rate = 1/24 + 1/36 = 5/72 tank per minute; time = 72/5 = 14.4 minutes.'],
  ['EASY','Three inlets fill a tank separately in 6, 8, and 12 hours. How long do they take together?','2.6667 h','Their rate is 1/6 + 1/8 + 1/12 = 3/8 tank per hour. Time = 8/3 hours, about 2.6667 hours.'],
  ['EASY','An inlet supplies 10 litres per minute while an outlet drains 2 litres per minute. How long will they take to fill an empty 240-litre tank together?','30 min','Net inflow is 10-2 = 8 litres per minute. Time = 240/8 = 30 minutes.'],
  ['EASY','A pipe supplies 200 litres per hour to an empty 1,200-litre tank. How long will filling take?','6 h','Time = 1,200/200 = 6 hours.'],
  ['EASY','Two outlets can empty a full tank in 8 hours and 12 hours. How long do they take together to empty it?','4.8 h','Combined emptying rate = 1/8 + 1/12 = 5/24 tank per hour; time = 24/5 = 4.8 hours.'],
  ['EASY','A pipe fills one-third of a tank in 5 hours. At the same constant rate, how long does it take to fill the whole tank?','15 h','Three times the one-third fill time is 3 x 5 = 15 hours.'],
  ['EASY','Pipe A fills a tank in 10 hours and pipe B in 15 hours. What is their joint filling time?','6 h','Their rates sum to 1/10 + 1/15 = 1/6 tank per hour, so they take 6 hours.'],
  ['EASY','Two pipes fill a reservoir in 18 minutes and 27 minutes. How long will they take together?','10.8 min','Combined rate = 1/18 + 1/27 = 5/54 tank per minute. Time = 54/5 = 10.8 minutes.'],
  ['EASY','A 180-litre tank is empty. An inlet flows at 12 litres per minute. How long will it take to fill the tank?','15 min','Time = 180/12 = 15 minutes.'],
  ['EASY','A pipe fills 5/6 of a tank in 50 minutes. How long will it take to fill the remaining 1/6 at the same rate?','10 min','The remaining one-sixth is one-fifth of the amount filled in 50 minutes, so it takes 50/5 = 10 minutes.'],
  ['EASY','A pipe fills a 1,200-litre cistern in 40 minutes. What is its flow rate?','30 L/min','Rate = 1,200/40 = 30 litres per minute.'],
  ['EASY','Pipe A fills a tank in 7 hours and pipe B in 14 hours. How long do they take together?','4.6667 h','Combined rate = 1/7 + 1/14 = 3/14 tank per hour. Time = 14/3, about 4.6667 hours.'],
  ['EASY','An outlet empties 600 litres of water in 20 minutes. What is its constant drainage rate?','30 L/min','Rate = 600/20 = 30 litres per minute.'],
  ['EASY','A 1,000-litre tank is filled by a pipe flowing at 25 litres per minute. How long does filling take?','40 min','Time = 1,000/25 = 40 minutes.'],
  ['EASY','Two pipes fill a tank in 16 hours and 48 hours. How long do they take working together?','12 h','Combined rate = 1/16 + 1/48 = 1/12 tank per hour.'],
  ['EASY','Three identical inlets together fill a tank in 8 hours. How long would one inlet take alone?','24 h','Each identical inlet supplies one-third of the combined rate, so one takes 3 x 8 = 24 hours.'],
  ['EASY','A pipe fills a tank in 45 minutes. What fraction of the tank does it fill in 15 minutes?','0.3333 tank','In 15 of its 45 minutes, it fills 15/45 = 1/3 of the tank, about 0.3333.'],
  ['EASY','Two inlets fill 1/6 and 1/12 of a tank per hour. How many hours do they need to fill the tank together?','4 h','Combined rate = 1/6 + 1/12 = 1/4 tank per hour.'],
  ['EASY','A pump raises the water level by 5 litres per minute in a 30-litre empty tank. How long until the tank is full?','6 min','Time = 30/5 = 6 minutes.'],

  ['MEDIUM','Two inlets fill a tank in 12 and 18 minutes, while a leak empties it in 36 minutes. How long will all three take to fill the empty tank?','9 min','Net rate = 1/12 + 1/18 - 1/36 = 1/9 tank per minute.'],
  ['MEDIUM','Pipes fill a tank in 20 and 30 minutes; an outlet empties it in 45 minutes. If all start together, how long to fill the tank?','16.3636 min','Net rate = 1/20 + 1/30 - 1/45 = 11/180 tank per minute. Time = 180/11, about 16.3636 minutes.'],
  ['MEDIUM','An inlet alone fills a tank in 10 hours, but with a leak open it takes 15 hours. How long would the leak alone take to empty a full tank?','30 h','Leak rate = 1/10 - 1/15 = 1/30 tank per hour.'],
  ['MEDIUM','Two inlets fill a tank in 8 and 12 hours, and a drain empties it in 24 hours. How long do they take together with the drain open?','6 h','Net rate = 1/8 + 1/12 - 1/24 = 1/6 tank per hour.'],
  ['MEDIUM','A fills a tank in 6 hours and B in 9 hours. Both run for 2 hours, then A is closed. How long after opening do they finish filling it?','6 h','In 2 hours they fill 2(1/6+1/9)=5/9. The remaining 4/9 takes 4 hours with B at 1/9 per hour; total time is 6 hours.'],
  ['MEDIUM','Starting with A, two pipes alternate one minute each. A fills a tank in 12 minutes and B empties it in 18 minutes. If the tank starts empty, how long until it is full?','72 min','Each A-B two-minute cycle adds 1/12-1/18=1/36 tank. It takes 36 cycles, or 72 minutes, to fill it.'],
  ['MEDIUM','A tank is 3/8 full. An inlet that fills the whole tank in 20 minutes is opened. How long to fill the rest?','12.5 min','The remaining 5/8 takes (5/8) x 20 = 12.5 minutes.'],
  ['MEDIUM','Two pipes fill a tank in 16 and 24 hours. How long do they need to fill 5/6 of it together?','8 h','Their combined rate is 1/16 + 1/24 = 5/48 tank per hour. Time for 5/6 is (5/6)/(5/48)=8 hours.'],
  ['MEDIUM','A tank is half full. An inlet fills it in 25 minutes and an outlet empties it in 50 minutes. How long until the tank is full with both open?','25 min','Net rate = 1/25-1/50=1/50 tank per minute. Filling the remaining half takes 25 minutes.'],
  ['MEDIUM','A 1,800-litre tank is one-quarter full. An inlet adds 600 litres per hour while an outlet drains 150 litres per hour. How long to fill it?','3 h','The remaining volume is 1,350 L and net inflow is 450 L/hour, so time = 3 hours.'],
  ['MEDIUM','Two inlets fill a tank in 6 and 4 hours, while a drain empties it in 12 hours. How long do all three take together?','3 h','Net rate = 1/6+1/4-1/12=1/3 tank per hour.'],
  ['MEDIUM','A fills a tank in 15 minutes. It runs alone for 5 minutes, then B, which fills a tank in 20 minutes, runs alone. What is the total filling time?','18.3333 min','A fills 1/3 in 5 minutes, leaving 2/3. B takes (2/3)x20=13 1/3 minutes. Total = 18 1/3 minutes.'],
  ['MEDIUM','An inlet fills a tank in 10 hours. A second inlet fills one-quarter of the tank in 2 hours. How long do both take together?','4.4444 h','The second rate is 1/8 per hour. Combined rate = 1/10+1/8=9/40; time = 40/9, about 4.4444 hours.'],
  ['MEDIUM','Pipe A fills 3/5 of a tank in 6 hours. Pipe B fills 1/4 in 3 hours. How long do they take together?','5.4545 h','Rates are 1/10 and 1/12 tank/hour. Combined rate 11/60 gives time 60/11, about 5.4545 hours.'],
  ['MEDIUM','Two outlets empty a full tank in 8 and 12 hours. If the tank is 3/4 full, how long will they take to empty it together?','3.6 h','Combined drainage rate = 1/8+1/12=5/24. Time = (3/4)/(5/24)=18/5=3.6 hours.'],
  ['MEDIUM','A 900-litre tank is one-third full. An inlet supplies 30 L/min and an outlet drains 12 L/min. How long to fill the rest?','33.3333 min','The remaining 600 L fills at 18 L/min, requiring 33 1/3 minutes.'],
  ['MEDIUM','A fills a tank in 14 minutes and B in 21 minutes. They work together for 6 minutes, after which B is closed. How long after opening A is the tank full?','10 min','Together they fill (1/14+1/21)x6=5/7. The remaining 2/7 takes 4 minutes with A. Total time is 10 minutes.'],
  ['MEDIUM','A and B fill a tank in 8 and 12 hours. What is the ratio of A’s filling rate to B’s?','3:2','Rates are 1/8 and 1/12; their ratio is 12:8 = 3:2.'],
  ['MEDIUM','Two inlets fill a tank in 20 and 30 minutes, and an outlet empties it in 60 minutes. How much of the tank is filled in 4 minutes when all are open?','0.2667 tank','Net rate = 1/20+1/30-1/60=1/15 tank per minute. In 4 minutes this is 4/15, about 0.2667.'],
  ['MEDIUM','A 1,200-litre tank starts empty. Inlet A supplies 5 L/min, inlet B 7 L/min, and an outlet drains 2 L/min. How much is in the tank after 30 minutes?','300 L','Net inflow = 5+7-2 = 10 L/min. After 30 minutes, 300 L is present.'],
  ['MEDIUM','A 900-litre tank already contains 360 litres. An inlet supplies 50 L/hour and an outlet drains 20 L/hour. How long until full?','18 h','The tank needs 900-360=540 more litres. Net inflow is 50-20=30 L/hour, so filling takes 540/30=18 hours.'],
  ['MEDIUM','A fills a tank in 8 hours and B in 12 hours. They run together for 3 hours, then B is closed. How long in total to fill the tank?','6 h','Together they fill 3(1/8+1/12)=5/8. The remaining 3/8 takes 3 hours with A, for 6 hours total.'],
  ['MEDIUM','An empty tank has capacity 1,000 litres. Inlet A supplies 40 L/hour and an outlet removes 15 L/hour. How long do they take together to fill it?','40 h','Net rate = 25 L/hour, so time = 1,000/25 = 40 hours.'],
  ['MEDIUM','A 720-litre tank is empty. Two pipes supply 5 and 7 litres per minute while an outlet removes 2 litres per minute. How long to fill it?','72 min','Net rate is 10 L/min; 720/10 = 72 minutes.'],
  ['MEDIUM','A pipe fills 2/5 of a tank in 8 minutes. At the same rate, how long will it take to fill the remaining 3/5?','12 min','The rate is 1/20 tank per minute. The remaining 3/5 takes (3/5) x 20 = 12 minutes.'],
  ['MEDIUM','Two inlets fill a tank in 5 and 10 hours. They run together for 2 hours. What fraction of the tank remains empty?','0.4 tank','Their combined rate is 1/5+1/10=3/10 per hour. In 2 hours they fill 3/5, leaving 2/5 = 0.4 tank.'],

  ['HARD','An inlet fills a tank in 9 hours, another in 12 hours, and an outlet empties it in 18 hours. How long do all three take together?','7.2 h','Net rate = 1/9+1/12-1/18=5/36 tank/hour. Time = 36/5 = 7.2 hours.'],
  ['HARD','A tank is 2/7 full. An inlet fills it in 14 minutes and a leak empties it in 35 minutes. How long until full with both open?','16.6667 min','Net rate = 1/14-1/35=3/70. The remaining 5/7 takes (5/7)/(3/70)=50/3 minutes.'],
  ['HARD','Pipe A fills a tank in 10 hours. Pipe B, which fills it in 15 hours, is opened 2 hours after A. How long from A’s start until the tank is full?','6.8 h','A first fills 1/5 in 2 hours. The remaining 4/5 is filled at 1/10+1/15=1/6 per hour, taking 4.8 hours. Total = 6.8 hours.'],
  ['HARD','A 1,200-litre tank is one-quarter full. Two inlets supply 14 and 10 L/min while an outlet drains 6 L/min. How long until it is full?','50 min','The remaining 900 L fills at net 14+10-6=18 L/min, so time = 50 minutes.'],
  ['HARD','A fills a tank in 5 hours and B in 7.5 hours. They alternate one hour each, starting with A. When will the tank be full?','6 h','A adds 1/5 and B adds 1/7.5=2/15 per hour. Each two-hour cycle adds 1/3 tank; three cycles fill it in 6 hours.'],
  ['HARD','A tank is 5/8 full. An inlet fills it in 12 hours and an outlet empties it in 30 hours. How long until full with both open?','7.5 h','Net rate = 1/12-1/30=1/20. The remaining 3/8 takes 7.5 hours.'],
  ['HARD','Pipes P, Q, and R fill a tank in 16, 24, and 48 minutes. P and Q run together for 6 minutes, then R is also opened. How long in total to fill the tank?','9 min','P+Q fill 6(1/16+1/24)=5/8. All three then fill at 1/16+1/24+1/48=1/8 per minute; the remaining 3/8 takes 3 minutes.'],
  ['HARD','A fills a tank in 15 hours and B in 20 hours. A runs alone for 3 hours, then both run. How long from the start until the tank is full?','9.8571 h','A fills 1/5 in 3 hours. The remaining 4/5 takes (4/5)/(7/60)=48/7 hours. Total = 3+48/7 = 69/7, about 9.8571 hours.'],
  ['HARD','Pipe A fills a tank in 18 hours and outlet B empties it in 24 hours. A runs 2 hours, then B runs 1 hour; this cycle repeats. How long to fill the tank?','40.75 h','Each 3-hour cycle adds 2/18-1/24=5/72. After 13 cycles (39 hours), 65/72 is filled. A then supplies the remaining 7/72 in 7/4 hours, for 40.75 hours total.'],
  ['MEDIUM','Two inlets fill a tank in 12 and 18 hours, and an outlet empties it in 36 hours. All run for 4 hours, then the outlet is closed. How long in total to fill the tank?','8 h','All three have net rate 1/12+1/18-1/36=1/9 and fill 4/9 in 4 hours. The remaining 5/9 at inlet rate 5/36 takes 4 more hours.'],
  ['HARD','An inlet fills a tank in 20 minutes and a leak empties it in 60 minutes. If both remain open, how long will an empty tank take to fill?','30 min','Net rate = 1/20-1/60=1/30 tank per minute.'],
  ['HARD','A fills a tank in 24 minutes and B in 36 minutes. Both run for 6 minutes, then A is closed and B continues. What is the total filling time?','27 min','Together they fill 6(1/24+1/36)=5/12. The remaining 7/12 takes 21 minutes with B; total = 27 minutes.'],
  ['HARD','A tank is 3/4 full. An inlet fills it in 18 hours and an outlet empties it in 12 hours. If both remain open, how long until it is empty?','27 h','Net rate is 1/18-1/12=-1/36 tank per hour. From 3/4 full, emptying takes (3/4)x36=27 hours.'],
  ['HARD','Two inlets fill a tank in 16 and 24 minutes, while an outlet empties it in 32 minutes. How long do all three take together?','13.7143 min','Net rate = 1/16+1/24-1/32=7/96 tank/minute, so time = 96/7 = 13.7143 minutes.'],
  ['HARD','A fills a tank in 10 hours, B in 15 hours, and C empties it in 30 hours. A starts at 8 a.m., B at 9 a.m., and C at 10 a.m. When will the tank be full?','5:20 p.m.','By 10 a.m., A has supplied 1/10 and A+B another 1/6, totaling 4/15. Net rate thereafter is 1/10 tank/hour. The remaining 11/15 takes 7 h 20 min, so it is full at 5:20 p.m.'],
  ['HARD','Two inlets fill a tank in 15 and 20 minutes, and an outlet empties it in 24 minutes. If all start together, how long to fill it?','13.3333 min','Net rate = 1/15+1/20-1/24=3/40 tank/minute. Time = 40/3 = 13.3333 minutes.'],
  ['HARD','A tank is empty. Inlets fill it in 12 and 18 minutes. An outlet drains 19 litres per minute. With all three open, the tank fills in 30 minutes. What is its capacity?','180 L','The inlets supply 1/12+1/18=5/36 tank/minute. Net rate is 1/30, so the outlet rate is 5/36-1/30=19/180 tank/minute. If that is 19 L/min, capacity is 180 L.'],
  ['HARD','A tank is full. Inlet A fills it in 18 hours and outlet B empties it in 12 hours. Both are opened together. How long until the tank is empty?','36 h','Net rate = 1/18-1/12=-1/36 tank per hour, so a full tank drains in 36 hours.'],
  ['HARD','A 60%-full tank has an inlet that fills it in 24 minutes and an outlet that empties it in 40 minutes. How long until it is full with both open?','24 min','Net rate = 1/24-1/40=1/60 tank/minute. The remaining 40% takes 0.4x60 = 24 minutes.'],
  ['HARD','A 2,000-litre tank is 30% full. Two inlets supply 40 and 25 L/min, while a leak drains 10 L/min. How long until full?','25.4545 min','The remaining 1,400 L fills at net 40+25-10=55 L/min. Time = 1,400/55 = 25.4545 minutes.'],
  ['HARD','A fills a tank in 10 hours and B in 15 hours. Both start together; A is closed after x hours, while B continues. The tank fills in 12 hours. Find x.','2 h','B supplies 12/15=4/5 of the tank. A supplies the remaining 1/5 at 1/10 per hour, so x=2 hours.'],
  ['HARD','A tank is half full. Inlet A fills a tank in 8 hours and outlet B empties it in 6 hours. They alternate one hour each, starting with A. How long until the tank is empty?','24 h','Each two-hour cycle changes the level by 1/8-1/6=-1/24 tank. Starting at 1/2, it takes 12 cycles (24 hours) to empty the tank.'],
  ['HARD','A fills a tank in 5 hours, B in 10 hours, and C empties it in 20 hours. A and B run for 2 hours; then C is also opened. How long from the start until full?','3.6 h','A+B fill 2(1/5+1/10)=3/5. All three then have net rate 1/5+1/10-1/20=1/4. The remaining 2/5 takes 1.6 hours. Total = 3.6 hours.'],
  ['HARD','Pipes A and B fill a tank in 12 and 16 hours. C empties it in 24 hours but is opened only after A and B have run for 3 hours. How long from the start until full?','8.4 h','A+B fill 3(1/12+1/16)=7/16. The remaining 9/16 fills at net rate 1/12+1/16-1/24=5/48, taking 27/5=5.4 hours. Total = 8.4 hours.'],
];

function normalized(value) { return String(value).trim(); }
function gcd(a,b) { return b ? gcd(b,a%b) : Math.abs(a); }
function ratioKey(value) {
  const parts=value.split(':').map(Number); const g=parts.reduce((a,b)=>gcd(a,b));
  return parts.map(n=>n/g).join(':');
}
function placeCorrect(values,index) {
  const unique=[];
  for (const value of values) if (!unique.some(v => v.toLowerCase()===value.toLowerCase())) unique.push(value);
  if (unique.length!==4) throw new Error(`Expected four distinct options for ${values[0]}, got ${unique.join('|')}`);
  const answer=unique.shift(); const spot=index%4; unique.splice(spot,0,answer);
  return {options:Object.fromEntries('ABCD'.split('').map((k,i)=>[k,unique[i]])),correct_option:'ABCD'[spot]};
}
function optionsFor(answer,index) {
  if (/^\d+(?::\d+)+$/.test(answer)) {
    const p=answer.split(':').map(Number), candidates=[answer];
    const variants=[p.slice().reverse(),[p[0]+1,p[1]],[p[0],p[1]+1],[p[0]+2,p[1]],[p[0],p[1]+2],[Math.max(1,p[0]-1),p[1]],[p[0],Math.max(1,p[1]-1)]];
    for (const v of variants) if (ratioKey(v.join(':'))!==ratioKey(answer)) candidates.push(v.join(':'));
    const selected=[]; for(const value of candidates) if(!selected.some(v=>ratioKey(v)===ratioKey(value))) selected.push(value);
    return placeCorrect(selected.slice(0,4),index);
  }
  const m=answer.match(/^([\d,]+(?:\.\d+)?)(.*)$/);
  if(!m) throw new Error(`Unsupported answer format: ${answer}`);
  const value=Number(m[1].replace(/,/g,'')), suffix=m[2];
  const step=Math.max(value>=10?1:0.1,Math.abs(value)*0.1);
  const decimals=Math.max((m[1].split('.')[1]||'').length,Number.isInteger(step)?0:1);
  let nums=[];
  for(let k=0;nums.length<4&&k<20;k++) {
    const n=value+(k===0?0:(k%2?1:-1)*Math.ceil(k/2)*step);
    const rounded=Number(n.toFixed(decimals));
    if(rounded>=0&&!nums.includes(rounded)) nums.push(rounded);
  }
  return placeCorrect(nums.map(n=>`${n}${suffix}`),index);
}
function row(level,stem,options,correct,explanation,source) {
  return {subject_slug:'maths',subcategory_slug:'arithmetic-maths',chapter_slug:'pipe-and-cistern',question_text:stem,options,correct_option:correct,explanation,difficulty:level,is_pyq:false,pyq_year:null,pyq_exam_name:null,source};
}
const rows=pdf.map(([level,stem,choices,key,explanation,page])=>row(level,stem,Object.fromEntries('ABCD'.split('').map((k,i)=>[k,choices[i]])),key,explanation,`Verified from supplied Pipe and Cistern PDF, page ${page}; exam/year not stated`));
for(let i=0;i<originals.length;i++) {
  const [level,stem,answer,explanation]=originals[i];
  const generated=optionsFor(normalized(answer),i);
  rows.push(row(level,stem,generated.options,generated.correct_option,explanation,'Original SSC-style practice question'));
}
const counts=Object.fromEntries(['EASY','MEDIUM','HARD'].map(level=>[level,rows.filter(r=>r.difficulty===level).length]));
if(rows.length!==90 || JSON.stringify(counts)!==JSON.stringify({EASY:30,MEDIUM:30,HARD:30})) throw new Error(`Unexpected batch shape: ${rows.length} ${JSON.stringify(counts)}`);
const out=path.join(__dirname,'..','data','pipe_and_cistern_verified_batch.json');
fs.writeFileSync(out,JSON.stringify({questions:rows},null,2)+'\n','utf8');
console.log(`Wrote ${rows.length} rows to ${out}`);
console.log('DIFFICULTY',counts);
console.log('PROVENANCE',{verified_pdf:pdf.length,original:originals.length});
