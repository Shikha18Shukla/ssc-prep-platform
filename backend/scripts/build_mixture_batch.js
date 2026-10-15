// Build the reviewed Mixture bank from the supplied class-notes PDF and original practice items.
const fs = require('node:fs');
const path = require('node:path');

const pdf = [
  ['EASY','A 50-litre mixture contains acid and water in the ratio 4:1. After 3 litres of water are added, what is the new acid-to-water ratio?',['5:2','2:5','3:5','N.O.T.'],'D','The original amounts are 40 L acid and 10 L water. After adding 3 L water, the ratio is 40:13, which is not among the listed ratios.',4],
  ['EASY','A liquid has acid and water in the ratio 1:3. Adding 5 litres of acid changes the ratio to 1:2. What is the amount of the new mixture?',['32 litres','40 litres','42 litres','45 litres'],'D','If the original mixture is x litres, its acid and water amounts are x/4 and 3x/4. The equation (x/4+5):(3x/4)=1:2 gives x=40, so the new amount is 45 litres.',5],
  ['EASY','Alcohol and water are mixed in the ratio 4:3. Adding 5 litres of water changes the ratio to 4:5. How much alcohol was in the original mixture?',['3 litres','4 litres','15 litres','10 litres'],'D','Let the original parts be 4k and 3k. Then 4k:(3k+5)=4:5, so k=2.5 and the alcohol amount is 4k=10 litres.',6],
  ['EASY','A 9-kg dough has sugar and flour in the ratio 2:7. How much sugar must be added to make the sugar-to-flour ratio 2:5?',['750 g','1.2 kg','1 kg','800 g'],'D','The dough contains 2 kg sugar and 7 kg flour. For a 2:5 ratio, sugar must be 14/5=2.8 kg, so 0.8 kg or 800 g is added.',7],
  ['EASY','A 100-g mixture contains 45% glycerine. If 35 g of water is added, what percentage of the new mixture is glycerine by weight?',['33%','33 1/3','40 20/27','45'],'B','There are 45 g glycerine in 135 g of final mixture. The percentage is 45/135 x 100 = 33 1/3.',8],
  ['MEDIUM','An alloy contains 17.5 kg copper and zinc in the ratio 5:2. If 1.25 kg zinc is added, what is the new copper-to-zinc ratio?',['2:1','2:3','3:2','1:2'],'A','The original amounts are 12.5 kg copper and 5 kg zinc. After adding zinc, the ratio is 12.5:6.25=2:1.',9],
  ['MEDIUM','Two equal-capacity vessels contain water and milk in ratios 3:4 and 5:3. What is the water-to-milk ratio after combining their contents?',['15:12','53:59','20:9','59:53'],'D','Scale the first ratio to 24:32 and the second to 35:21. Adding components gives water:milk=59:53.',10],
  ['MEDIUM','Three equal-capacity bottles contain milk and water in ratios 5:7, 7:9 and 2:1. Their contents are poured together. Approximately what percentage of the final mixture is milk?',['50.7%','73.9%','72.7%','60.7%'],'A','Taking 48 units from each bottle gives milk amounts 20, 21 and 32, and water amounts 28, 27 and 16. Milk is 73/144 of the total, about 50.7%.',11],
  ['MEDIUM','Equal quantities are taken from four equal-capacity bottles whose milk-to-water ratios are 1:2, 2:3, 3:2 and 7:8. What is the final milk-to-water ratio?',['13:15','7:9','9:11','11:9'],'C','For equal quantities, the milk fractions sum to 1/3+2/5+3/5+7/15=27/15 and the water fractions to 33/15. The ratio is 9:11.',12],
  ['MEDIUM','Two rum-and-soda solutions have ratios 2:3 and 3:2. They are mixed in the quantity ratio 4:1. What is the resulting rum-to-soda ratio?',['12:17','11:14','15:11','19:12'],'B','Five equal parts of the first and one part of the second give rum:soda=(2x4+3):(3x4+2)=11:14.',13],
  ['MEDIUM','Three glasses hold 3 L, 4 L and 5 L. Their milk-to-water ratios are 2:3, 3:7 and 4:11. What is the milk-to-water ratio after combining them?',['7:32','14:31','12:25','15:31'],'B','The milk amounts are 6/5, 6/5 and 4/3 L; water amounts are 9/5, 14/5 and 11/3 L. Their ratio reduces from 56:124 to 14:31.',14],
  ['MEDIUM','One liquid contains 20% water and another contains 35% water. Ten parts of the first and four parts of the second are mixed. What percentage of the blend is water?',['24 2/7%','37%','46%','12 1/7%'],'A','The water amount is 10(0.20)+4(0.35)=3.4 parts in 14 parts total. Thus water is 3.4/14 x 100=24 2/7%.',15],
  ['HARD','Two alloys contain copper and tin in ratios 1:3 and 2:5. In what quantity ratio should the first and second alloys be mixed to obtain tin:copper = 8:3?',['3:5','4:7','5:3','7:4'],'B','Copper fractions are 1/4 and 2/7; the target copper fraction is 3/11. Alligation gives first:second=(3/11-2/7):(1/4-3/11)=4:7.',16],
  ['HARD','A laboratory has acid-water solutions in ratios 2:5 and 7:3. In what quantity ratio should the first and second solutions be mixed to obtain acid:water = 2:3?',['4:15','9:8','21:8','1:2'],'C','The acid fractions are 2/7 and 7/10; the target is 2/5. Alligation gives first:second=(7/10-2/5):(2/5-2/7)=21:8.',17],
  ['HARD','Two vessels contain petrol and kerosene in ratios 4:3 and 3:5. In what quantity ratio should portions from the first and second vessels be mixed so the resulting amounts of petrol and kerosene are equal?',['9:6','3:2','7:8','7:4'],'D','The petrol fractions differ from one-half by 1/14 above and 1/8 below. The required first:second quantity ratio is 1/8:1/14=7:4.',18],
  ['HARD','Vessel A contains milk and water in ratio 4:3; vessel B has them in ratio 2:3. What quantity ratio A:B gives a blend that is half milk and half water?',['7:5','5:2','3:11','1:2'],'A','Milk fractions are 4/7 and 2/5, and the target is 1/2. Alligation gives A:B=(1/2-2/5):(4/7-1/2)=7:5.',19],
];

// Independently recalculated numeric or ratio answers for original items.
const originals = [
  ['EASY','Twelve litres of a milk-water mixture have ratio 3:1. Eight litres of another have ratio 1:3. What is the final milk-to-water ratio?','11:9','The milk amounts are 9 and 2 L, and the water amounts are 3 and 6 L. Thus the ratio is 11:9.'],
  ['EASY','A 25-L fruit drink is prepared with concentrate and water in the ratio 2:3. How many litres of water are used?','15 L','The ratio has five parts, so one part is 5 L. Water is three parts, or 15 L.'],
  ['EASY','A 30-kg sugar-flour dough has sugar:flour=1:4. How much sugar does it contain?','6 kg','The ratio has five parts, so one part is 6 kg. Sugar is one part, or 6 kg.'],
  ['EASY','A 40-L drink contains juice and water in ratio 3:5. How much pure juice must be added to make equal amounts of juice and water?','10 L','The drink has 15 L juice and 25 L water. Adding 10 L juice makes both amounts 25 L.'],
  ['EASY','A grocer blends 20 kg of rice costing Rs 20/kg with 30 kg costing Rs 30/kg. What is the average cost per kilogram?','Rs 26/kg','The total cost is 20x20+30x30=Rs 1,300 for 50 kg, or Rs 26/kg.'],
  ['EASY','A 12-L solution is 25% syrup and an 8-L solution is 50% syrup. What is the syrup percentage after mixing?','35%','The syrup amounts are 3 L and 4 L. Seven litres in 20 L is 35%.'],
  ['EASY','A 32-kg brass ingot has copper:zinc=5:3. How many kilograms of zinc does it contain?','12 kg','There are 8 ratio parts, so each part is 4 kg. Zinc is 3 parts, or 12 kg.'],
  ['EASY','Five kilograms of a solution is 40% salt; another 15 kg solution is 20% salt. Find the salt percentage of the blend.','25%','Salt totals 2+3=5 kg in 20 kg mixture, which is 25%.'],
  ['EASY','A 20-L mixture is 30% flavouring. If 5 L of water evaporate, what percentage of the remaining mixture is flavouring?','40%','The flavouring remains 6 L while total volume falls to 15 L. Thus the new concentration is 6/15=40%.'],
  ['EASY','A 16-L milk-water mixture has ratio 3:5. How much milk must be added to make milk and water equal?','4 L','It contains 6 L milk and 10 L water. Add 4 L milk to equalize them.'],
  ['EASY','Four kilograms of tea costing Rs 300/kg are blended with 6 kg costing Rs 450/kg. Find the blend cost per kilogram.','Rs 390/kg','Total cost is Rs 1,200+2,700=3,900 for 10 kg, giving Rs 390/kg.'],
  ['EASY','Eight litres of alcohol solution is 30% alcohol. How much water should be added to reduce it to 20%?','4 L','Alcohol remains 2.4 L. At 20%, the total volume must be 12 L, so add 4 L water.'],
  ['EASY','How many kilograms of a 35% concentrate must be mixed with 10 kg of a 15% concentrate to obtain a 25% blend?','10 kg','The target lies midway between 15% and 35%, so equal quantities are required: 10 kg.'],
  ['EASY','A 35-kg alloy has copper:tin=3:4. After adding 5 kg tin, what is the new copper-to-tin ratio?','3:5','Copper is 15 kg and tin 20 kg; after addition tin is 25 kg, giving 3:5.'],
  ['EASY','A 24-kg milk-water mixture has milk:water=5:3. How many kilograms of milk does it contain?','15 kg','Eight ratio parts equal 24 kg, so one part is 3 kg and milk is 5x3=15 kg.'],
  ['EASY','Equal volumes of two drinks with water:milk ratios 2:3 and 3:2 are combined. What is the final water-to-milk ratio?','1:1','The water fractions are 2/5 and 3/5, whose equal-weight average is 1/2; milk is also 1/2.'],
  ['EASY','How much sugar is present in 25 L of a 12% sugar solution?','3 L','Twelve percent of 25 L is 3 L of sugar.'],
  ['EASY','Five litres of 60% acid solution are mixed with 15 litres of 20% acid solution. What is the final acid percentage?','30%','The acid totals 3+3=6 L in 20 L, so the concentration is 30%.'],
  ['EASY','Thirty kilograms of grain costing Rs 80/kg are mixed with 20 kg costing Rs 110/kg. Find the mean cost per kilogram.','Rs 92/kg','The total cost is Rs 2,400+2,200=4,600 for 50 kg, or Rs 92/kg.'],
  ['EASY','A 40-L milk-water mixture is 3:5. If 8 litres are poured out, how many litres of milk remain?','12 L','The mixture contains 15 L milk. The 8-L portion contains 3 L milk, leaving 12 L milk.'],
  ['EASY','Six kilograms of nuts at Rs 120/kg are mixed with 4 kg at Rs 180/kg. What is the average price per kilogram?','Rs 144/kg','The total cost is Rs 720+720=1,440 for 10 kg, or Rs 144/kg.'],
  ['EASY','Twenty litres of a 30% concentrate are diluted by removing 5 litres of the mixture and replacing it with water. What is the new concentration?','22.5%','The initial concentrate is 6 L. Removing 5 L removes 1.5 L concentrate, leaving 4.5 L in 20 L, or 22.5%.'],
  ['EASY','A vessel holds 12 L of pure milk. How much water must be added for milk:water to become 3:1?','4 L','One quarter of the final 16 L is water, so add 4 L.'],
  ['EASY','Fifteen litres of 40% salt solution are combined with 5 litres of 10% salt solution. What is the final salt percentage?','32.5%','Salt totals 6+0.5=6.5 L-equivalent in 20 L, which is 32.5%.'],
  ['EASY','Six litres of acid-water solution have ratio 2:1; nine litres of another solution have ratio 1:2. What is the combined acid-to-water ratio?','7:8','Acid totals 4+3=7 L and water totals 2+6=8 L.'],

  ['MEDIUM','A trader blends 20% and 50% acid solutions to obtain a 32% solution. What is the required quantity ratio, weaker solution:stronger solution?','3:2','By alligation, weaker:stronger=(50-32):(32-20)=18:12=3:2.'],
  ['MEDIUM','Coffee at Rs 240/kg is mixed with coffee at Rs 360/kg to obtain a blend worth Rs 300/kg. What quantity ratio gives this price?','1:1','The target price is halfway between Rs 240 and Rs 360, so equal quantities are needed.'],
  ['MEDIUM','A 60-L vessel is full of milk. Twelve litres are removed and replaced with water. What is the final milk-to-water ratio?','4:1','After removal, 48 L milk remains and 12 L water is added, giving 4:1.'],
  ['MEDIUM','An 80-L mixture has milk:water=7:3. Twenty litres are withdrawn and replaced with water. What is the new milk-to-water ratio?','21:19','The withdrawn amount contains 14 L milk and 6 L water. Remaining amounts are 42 L milk and 18 L water; add 20 L water to get 42:38=21:19.'],
  ['MEDIUM','Twenty-five kilograms of 12% solution are blended with 35 kg of 32% solution. What is the final concentration?','23.6667%','Solute totals 3+11.2=14.2 kg in 60 kg, so concentration is 23 2/3%.'],
  ['MEDIUM','How many kilograms each of 30% and 50% acid solutions make 40 kg of a 42% blend? Give the amount of the 50% solution.','24 kg','Alligation gives weaker:stronger=(50-42):(42-30)=2:3. Three fifths of 40 kg is 24 kg.'],
  ['MEDIUM','Fifteen litres of 40% acid solution are mixed with a 10% solution to make a 25% solution. How many litres of the weaker solution are needed?','15 L','Solve (6+0.1x)/(15+x)=0.25; this gives 0.15x=2.25 and x=15 L.'],
  ['MEDIUM','A 35-kg alloy contains copper and zinc in ratio 3:4. How much zinc must be added to make copper:zinc=3:5?','5 kg','The alloy has 15 kg copper and 20 kg zinc. The target requires 25 kg zinc, so add 5 kg.'],
  ['MEDIUM','A 50-L alcohol solution is 30% alcohol. Ten litres are removed and replaced with pure alcohol. What is the new alcohol percentage?','44%','The initial 15 L alcohol loses 3 L when 10 L mixture is removed, then gains 10 L. Thus 22/50=44%.'],
  ['MEDIUM','A 100-kg blend is made from 20 kg of 10% solution, 30 kg of 40% solution and 50 kg of 60% solution. Find its concentration.','44%','Solute totals 2+12+30=44 kg in 100 kg, giving 44%.'],
  ['MEDIUM','Thirty litres of milk-water mixture are 2:1, and 15 litres of another are 1:2. What is the final milk-to-water ratio?','5:4','The first contributes 20 L milk and 10 L water; the second contributes 5 L each. The total ratio is 25:20=5:4.'],
  ['MEDIUM','Coffee at Rs 350/kg is mixed with coffee at Rs 500/kg to average Rs 410/kg. If 15 kg of the cheaper coffee is used, how much of the dearer coffee is needed?','10 kg','Alligation gives cheaper:dearer=(500-410):(410-350)=3:2. Thus 15 kg corresponds to 10 kg dearer coffee.'],
  ['MEDIUM','How much water must be added to 40 L of a 45% solution to reduce its concentration to 30%?','20 L','There are 18 L solute. At 30%, the final volume must be 60 L, requiring 20 L water.'],
  ['MEDIUM','A 25-kg mixture is 12% salt. How much pure salt must be added to make it 20% salt?','2.5 kg','Solve (3+x)/(25+x)=0.20, giving 0.8x=2 and x=2.5 kg.'],
  ['MEDIUM','Eight litres of a 75% solution are combined with 12 litres of a 25% solution. What is the final concentration?','45%','The solute amounts are 6 and 3 L. Nine litres in 20 L is 45%.'],
  ['MEDIUM','A 48-kg blend uses two rice varieties costing Rs 120/kg and Rs 180/kg. The mean price is Rs 150/kg. How much of the dearer variety is used?','24 kg','The target is midway between the prices, so half of 48 kg, or 24 kg, is the dearer variety.'],
  ['MEDIUM','One hundred litres of 40% solution have 25 L removed and replaced with 20% solution. What is the new concentration?','35%','Solute falls from 40 L to 30 L after removal, then rises by 5 L to 35 L in 100 L.'],
  ['MEDIUM','A 36-L vessel contains pure milk. Nine litres are removed and replaced with water; the same operation is repeated once. What is the final milk:water ratio?','9:7','After two rounds milk is 36(27/36)^2=20.25 L; water is 15.75 L. The ratio is 9:7.'],
  ['MEDIUM','Equal amounts of three solutions containing 20%, 40% and 70% solute are combined. What is the final concentration?','43.3333%','For equal amounts, concentration is the mean: (20+40+70)/3=43 1/3%.'],
  ['MEDIUM','A 60-kg salt-sand mixture has salt:sand=5:7. How much salt must be added to make the ratio 3:4?','1.25 kg','There are 25 kg salt and 35 kg sand. At 3:4, salt must be 26.25 kg, so add 1.25 kg.'],
  ['MEDIUM','A 40-L milk-water mixture is 3:5. How much pure milk must be added to make the ratio 3:4?','3.75 L','There are 15 L milk and 25 L water. Solve (15+x):25=3:4 to get x=3.75 L.'],
  ['MEDIUM','Solutions of 24% and 44% concentration are blended in volume ratio 5:3. What is the resulting concentration?','31.5%','The weighted concentration is (24x5+44x3)/8=31.5%.'],
  ['MEDIUM','A 25-L mixture is 32% concentrate. Some is removed and replaced with a 12% solution. If the final concentration is 28%, how many litres were replaced?','5 L','Solute after replacement is 0.32(25-x)+0.12x. Setting this to 0.28x25 gives x=5 L.'],

  ['HARD','An 80-L mixture is 60% concentrate. Ten litres are replaced with water, and this operation is repeated. What is the final concentration?','45.9375%','Each operation leaves 7/8 of the concentrate. Final concentrate is 48(7/8)^2=36.75 L in 80 L, or 45.9375%.'],
  ['HARD','A 100-L solution is 50% acid. First 20 L are replaced with water; then 10 L of the new mixture are also replaced with water. Find the final acid percentage.','36%','After the first exchange acid is 40 L. The second removes 4 L acid, leaving 36 L in 100 L.'],
  ['HARD','A 100-L solution contains 48% acid. Replace 25 L with a 20% acid solution, then replace 20 L of the new mixture with water. What is the final concentration?','32.8%','After the first exchange acid is 36+5=41 L. The next removal leaves 41x80/100=32.8 L acid in 100 L.'],
  ['HARD','A blend contains 20 kg of 70% copper alloy, 30 kg of 40% copper alloy, and some pure copper. How much pure copper is needed for a 60% copper blend?','10 kg','Copper is initially 14+12=26 kg. Solve (26+x)/(50+x)=0.60 to get x=10 kg.'],
  ['HARD','Two coffees cost Rs 220/kg and Rs 340/kg. Their blend averages Rs 300/kg, and the dearer coffee exceeds the cheaper by 20 kg. Find the total blend weight.','60 kg','Alligation gives cheaper:dearer=(340-300):(300-220)=1:2. Their difference is one part, or 20 kg; total is three parts=60 kg.'],
  ['HARD','Three solutions are mixed in quantity ratio 3:2:1. The first is 40% solute and the second is 70%. What concentration must the third solution have for the blend to be 50%?','40%','The first two contribute 3(40)+2(70)=260 concentration-parts. For six total parts at 50%, the third must contribute 300-260=40, so it is 40%.'],
  ['HARD','A 60-L milk-water mixture has ratio 5:3. Twelve litres are removed and replaced with pure milk. What is the final milk-to-water ratio?','7:3','Initially milk=37.5 L and water=22.5 L. Removing 12 L removes 7.5 and 4.5 L; after adding milk, amounts are 42 and 18 L, or 7:3.'],
  ['HARD','A 40-L liquid is 40% solute. It is mixed with a 70% solution. How many litres of the stronger solution are needed for a 52% blend?','26.6667 L','Solve (16+0.70x)/(40+x)=0.52; this gives 0.18x=4.8 and x=80/3, about 26.6667 L.'],
  ['HARD','A 60-L solution is 50% concentrate. Replace 15 L with a 20% solution, then repeat the same exchange. What is the final concentration?','36.875%','After one exchange concentrate is 30-7.5+3=25.5 L. After the second it is 25.5-6.375+3=22.125 L, which is 36.875% of 60 L.'],
  ['HARD','A mixture has 30 L of 20% solution, 45 L of 50% solution and 15 L of 80% solution. What is its overall concentration?','45%','Solute totals 6+22.5+12=40.5 L in 90 L, giving 45%.'],
  ['HARD','A 75-L solution is 24% solute. Replace 15 L with a 60% solution. What is the new concentration?','31.2%','Initially solute is 18 L. The exchange removes 3.6 L and adds 9 L, leaving 23.4 L in 75 L, or 31.2%.'],
  ['HARD','An 80-L milk-water mixture has ratio 3:5. Remove 16 L of the mixture, then add pure milk until the ratio becomes 2:3. How much milk is added?','2.6667 L','After removal, milk=24 L and water=40 L. Solve (24+x):40=2:3, giving x=8/3, about 2.6667 L.'],
  ['HARD','Twenty-four litres of 25% solution are mixed with a 55% solution to obtain 40%. If 12 L of the blend are then removed, how much solute remains?','14.4 L','The alligation equation gives 24 L of the stronger solution. The blend has 19.2 L solute in 48 L; after removing one-quarter, 14.4 L remains.'],
  ['HARD','Solutions are mixed in quantity ratio 1:2:2. Their concentrations are 20%, 50% and x%. If the blend is 42%, find x.','45%','(20+2x50+2x)/5=42, so 120+2x=210 and x=45%.'],
  ['HARD','Two alloys contain tin:copper in ratios 2:3 and 1:4. In what ratio should the first and second alloys be combined to obtain tin:copper=1:2?','2:1','Tin fractions are 2/5 and 1/5; the target is 1/3. Alligation yields first:second=(1/3-1/5):(2/5-1/3)=2:1.'],
  ['HARD','A 120-L mixture is 35% alcohol. Replace 30 L with an x% alcohol solution, then replace 20 L of the new mixture with water. If the final concentration is 30%, find x.','39%','After the first exchange alcohol is 31.5+0.3x L. The second leaves 5/6 of it; setting that to 36 L gives x=39%.'],
  ['HARD','A tank has 25 L of 60% concentrate and 15 L of 20% concentrate. How much water must be added to reduce the final concentration to 35%?','11.4286 L','The solute is 15+3=18 L in 40 L. Solve 18/(40+x)=0.35, giving x=80/7, about 11.4286 L.'],
  ['HARD','Twenty litres of a 25% solution and 30 litres of a 40% solution are mixed with x litres of a 70% solution. If the final concentration is 50%, find x.','40 L','Solute equation: 5+12+0.7x=0.5(50+x). Thus 0.2x=8 and x=40 L.'],
  ['HARD','A 60-kg alloy has copper:zinc=7:5. How much zinc must be added to make copper:zinc=7:8?','15 kg','Copper is 35 kg and zinc 25 kg. The target requires 40 kg zinc, so add 15 kg.'],
  ['HARD','A 50-L solution is 40% acid. Ten litres are removed and replaced with water. How much pure acid must then be added to restore a 40% concentration?','6.6667 L','After replacement, 16 L acid remains. Solve (16+x)/(50+x)=0.40, yielding x=20/3, about 6.6667 L.'],
  ['HARD','A 60-L blend contains 25% solute. How much 50% solution must be added to make the blend 45%?','240 L','Solve (15+0.5x)/(60+x)=0.45; then 0.05x=12 and x=240 L.'],
  ['HARD','A mixture contains 20 kg of 30% solution and 30 kg of 50% solution. How many kilograms of water must evaporate for the concentration to become 50%?','8 kg','Solute remains 6+15=21 kg. At 50%, the total mass must be 42 kg; evaporate 50-42=8 kg water.'],
  ['HARD','A 100-L solution is 80% milk. Replace 20 L with water, then remove 10 L of the new mixture and replace it with pure milk. What is the final milk percentage?','67.6%','After the first exchange milk is 64 L. The next removal leaves 57.6 L milk; adding 10 L gives 67.6 L in 100 L.'],
  ['HARD','One hundred litres of 50% solution are repeatedly replaced with a 20% solution: first 20 L, then 10 L. What is the final solute percentage?','41.6%','First solute amount becomes 50-10+4=44 L. Next it becomes 44-4.4+2=41.6 L in 100 L, hence 41.6%.'],
  ['HARD','An alloy blend contains 40 kg of 25% copper alloy and 60 kg of 55% copper alloy. How much pure tin must be added to reduce copper to 40%?','7.5 kg','Copper is 10+33=43 kg. At 40%, total mass must be 43/0.4=107.5 kg, so add 7.5 kg tin.'],
  ['HARD','A 40-L solution is 25% acid. It is mixed with some 55% acid solution, then 10 L of water is added. If the final concentration is 35%, how much 55% solution was used?','37.5 L','If x litres of the stronger solution are used, (10+0.55x)/(50+x)=0.35. Solving 0.2x=7.5 gives x=37.5 L.'],
];

function normalized(value) { return String(value).trim(); }
function optionsFor(answer, index) {
  const ratio = /^\d+(?::\d+)+$/.test(answer);
  if (ratio) {
    const parts = answer.split(':').map(Number);
    const choices = [answer];
    for (let i=0; i<parts.length && choices.length<4; i++) {
      const changed = [...parts]; changed[i]++;
      const candidate = changed.join(':');
      if (!choices.includes(candidate)) choices.push(candidate);
    }
    while (choices.length<4) choices.push(parts.map((n,i)=>n+(i===0?choices.length:0)).join(':'));
    return placeCorrect(choices, index);
  }
  const match = answer.match(/^(Rs )?(-?[\d.]+)(.*)$/);
  if (!match) throw new Error(`Unsupported answer format: ${answer}`);
  const value = Number(match[2]); const prefix = match[1] || ''; const suffix = match[3];
  const step = Math.max(Math.abs(value)*0.1, value >= 10 ? 1 : 0.1);
  let values = [value, value+step, value-step, value+2*step].filter((n,i,a)=>n>=0 && a.indexOf(n)===i);
  while (values.length<4) values.push(value+(values.length+1)*step);
  const vals = values.slice(0,4).map(n => `${prefix}${Number(n.toFixed(4))}${suffix}`);
  return placeCorrect(vals, index);
}
function placeCorrect(values,index) {
  const correct = values.shift(); const spot = index%4; values.splice(spot,0,correct);
  return {options:Object.fromEntries('ABCD'.split('').map((k,i)=>[k,values[i]])),correct_option:'ABCD'[spot]};
}
function row(level,stem,options,correct,explanation,source) {
  return {subject_slug:'maths',subcategory_slug:'arithmetic-maths',chapter_slug:'mixture',question_text:stem,options,correct_option:correct,explanation,difficulty:level,is_pyq:false,pyq_year:null,pyq_exam_name:null,source};
}
const rows = pdf.map(([d,stem,opts,key,explanation,page])=>row(d,stem,Object.fromEntries('ABCD'.split('').map((k,i)=>[k,opts[i]])),key,explanation,`Verified from supplied Mixture PDF, page ${page}; exam/year not stated`));
for (let i=0;i<originals.length;i++) {
  const [level,stem,answer,explanation]=originals[i];
  const generated=optionsFor(normalized(answer),i);
  rows.push(row(level,stem,generated.options,generated.correct_option,explanation,'Original SSC-style practice question'));
}
const counts=Object.fromEntries(['EASY','MEDIUM','HARD'].map(level=>[level,rows.filter(r=>r.difficulty===level).length]));
const pdfCounts=Object.fromEntries(['EASY','MEDIUM','HARD'].map(level=>[level,pdf.filter(r=>r[0]===level).length]));
if (rows.length!==90 || JSON.stringify(counts)!==JSON.stringify({EASY:30,MEDIUM:30,HARD:30})) throw new Error(`Expected 90 balanced items: ${JSON.stringify(counts)}`);
fs.writeFileSync(path.join(__dirname,'..','data','mixture_verified_batch.json'),`${JSON.stringify({questions:rows},null,2)}\n`,'utf8');
console.log(`Wrote ${rows.length}: PDF ${pdf.length} ${JSON.stringify(pdfCounts)}, original ${originals.length}, ${JSON.stringify(counts)}`);
