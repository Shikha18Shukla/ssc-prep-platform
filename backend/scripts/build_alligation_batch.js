// Build the reviewed Alligation batch from the supplied scanned lecture and original practice items.
const fs = require('node:fs');
const path = require('node:path');

const pdf = [
  ['EASY','Tea costing Rs 80/kg and Rs 120/kg is blended to make a mixture worth Rs 90/kg. What is the quantity ratio of the cheaper tea to the dearer tea?',['3:1','1:3','2:1','1:2'],'A','By alligation, cheaper:dearer = (120-90):(90-80) = 30:10 = 3:1.',12],
  ['EASY','Rice priced at Rs 3.10/kg and Rs 3.60/kg is mixed to obtain a blend worth Rs 3.25/kg. Find the ratio of the cheaper to the costlier rice.',['7:3','3:7','5:3','7:4'],'A','The cross-differences are 3.60-3.25 = 0.35 and 3.25-3.10 = 0.15. Their ratio is 7:3.',13],
  ['EASY','Two rice grades cost Rs 10.20/kg and Rs 14.40/kg. In what cheaper-to-dearer quantity ratio will their blend cost Rs 12.60/kg?',['4:3','2:5','3:4','3:5'],'C','The cross-differences are 14.40-12.60=1.80 and 12.60-10.20=2.40. Cheaper:dearer = 1.80:2.40 = 3:4.',14],
  ['EASY','A 15% sugar solution and a 40% sugar solution are combined to make a 30% solution. What is the weaker-to-stronger solution ratio?',['2:3','3:2','8:9','9:8'],'A','Alligation gives weaker:stronger = (40-30):(30-15) = 10:15 = 2:3.',15],
  ['MEDIUM','How many kilograms of sugar costing Rs 55/kg must be added to 60 kg costing Rs 48/kg so the blend costs Rs 52.50/kg?',['90 kg','95 kg','102 kg','108 kg'],'D','Alligation gives Rs 55 sugar:Rs 48 sugar = (52.50-48):(55-52.50) = 4.5:2.5 = 9:5. The 60 kg is five parts, so the added amount is 9x12 = 108 kg.',16],
  ['MEDIUM','Two grain varieties cost Rs 15/kg and Rs 21/kg. At what cheaper-to-dearer ratio should they be blended so a Rs 24/kg selling price gives a 20% gain?',['1:5','5:1','2:5','1:4'],'A','A 20% gain at Rs 24/kg means the blend costs Rs 20/kg. Alligation gives cheaper:dearer = (21-20):(20-15) = 1:5.',17],
  ['MEDIUM','Two grain varieties cost Rs 65/kg and Rs 60/kg. At what ratio of the Rs 65 grain to the Rs 60 grain should they be blended if a Rs 68.20/kg selling price gives a 10% gain?',['2:3','3:2','1:2','2:5'],'A','The blend cost is 68.20/1.10 = Rs 62/kg. Alligation for Rs 65 and Rs 60 gives dearer:cheaper = (62-60):(65-62) = 2:3.',18],
  ['MEDIUM','A no-cost water supply is mixed with spirit. At what water-to-spirit ratio can the blend be sold at cost for a 20% gain?',['1:5','5:1','1:4','2:5'],'A','If the blend sells for 100, a 20% gain means its cost is 100/1.2 = 83 1/3. Alligation between water at zero and spirit at 100 gives spirit:water = 5:1, hence water:spirit = 1:5.',19],
  ['MEDIUM','In a group of 65 students, each boy receives 80 paise and each girl 30 paise from a Rs 39 fund. How many girls are there?',['26','30','35','39'],'A','The mean allocation is 3900/65 = 60 paise. Boy:girl counts = (60-30):(80-60) = 30:20 = 3:2. Girls are 2/5 of 65, or 26.',20],
  ['MEDIUM','Rs 1,050 is shared among 1,400 men and women; each man gets Rs 1 and each woman 50 paise. How many women are in the group?',['700','600','750','800'],'A','The average share is 1050/1400 = Rs 0.75. Male:female count = (0.75-0.50):(1.00-0.75) = 1:1, so there are 700 women.',21],
  ['MEDIUM','Girls average 73 marks and boys average 71. If the class average is 71.8, what percentage of the class are girls?',['40%','45%','50%','60%'],'A','Girls:boys = (71.8-71):(73-71.8) = 0.8:1.2 = 2:3. Girls are 2/5 of the class, or 40%.',22],
];

// Independently checked original Alligation practice questions: [difficulty, stem, answer, explanation].
const originals = [
  ['EASY','A grocer combines 12 kg of lentils at Rs 18/kg with 8 kg at Rs 27/kg. What is the mean price per kilogram?','Rs 21.60/kg','The total cost is 12x18 + 8x27 = Rs 432 for 20 kg; 432/20 = Rs 21.60/kg.'],
  ['EASY','For a catering order, 15 kg of rice costing Rs 24/kg is joined by 10 kg priced at Rs 33/kg. Find the average cost of one kilogram.','Rs 27.60/kg','The combined cost is 15x24 + 10x33 = Rs 690 for 25 kg, so the mean is Rs 27.60/kg.'],
  ['EASY','The shop mixes 40 kg of coffee worth Rs 45/kg with 20 kg worth Rs 60/kg. Compute the new lot’s cost per kilogram.','Rs 50/kg','The total cost is Rs 1,800 + Rs 1,200 = Rs 3,000 for 60 kg. The unit cost is Rs 50/kg.'],
  ['EASY','An oil merchant pours 8 L of oil at Rs 52/L and 12 L at Rs 68/L into one tank. What is the mean price per litre?','Rs 61.60/L','The cost is 8x52 + 12x68 = Rs 1,232 for 20 L, giving Rs 61.60/L.'],
  ['EASY','A 3:5 mass blend uses tea grades priced Rs 80/kg and Rs 104/kg, respectively. Determine its mean price per kilogram.','Rs 95/kg','The weighted mean is (3x80 + 5x104)/8 = Rs 760/8 = Rs 95/kg.'],
  ['EASY','Eighteen kilograms of apples at Rs 70/kg are packed with 12 kg at Rs 95/kg. What is the average price of the packed lot?','Rs 80/kg','Total cost is 18x70 + 12x95 = Rs 2,400 for 30 kg, so the mean is Rs 80/kg.'],
  ['EASY','To obtain flour costing Rs 31/kg from lots priced Rs 25/kg and Rs 40/kg, how many kilograms of the cheaper flour should be used per 2 kg of dearer flour?','3 kg','Cheaper:dearer = (40-31):(31-25) = 9:6 = 3:2; 2 kg of dearer flour pairs with 3 kg of cheaper flour.'],
  ['EASY','A grain dealer wants a Rs 48/kg blend from wheat at Rs 42/kg and Rs 57/kg. State the lower-priced to higher-priced quantity ratio.','3:2','Alligation gives cheaper:dearer = (57-48):(48-42) = 9:6 = 3:2.'],
  ['EASY','Two saline solutions contain salt at 20% and 50%. What weaker-to-stronger quantity ratio produces a 32% solution?','3:2','The cross-differences are 50-32=18 and 32-20=12, so weaker:stronger = 18:12 = 3:2.'],
  ['EASY','Sugar syrups of 12% and 32% concentration are combined to make 20% syrup. Find the weaker-to-stronger volume ratio.','3:2','Alligation gives (32-20):(20-12) = 12:8 = 3:2.'],
  ['EASY','Milk costing Rs 50/L and Rs 70/L is blended to obtain milk worth Rs 58/L. How many parts of the cheaper milk are used per part of dearer milk?','3:2','Cheaper:dearer = (70-58):(58-50) = 12:8 = 3:2.'],
  ['EASY','A grocer combines rice grades costing Rs 90/kg and Rs 114/kg in equal quantities. What is the resulting price per kilogram?','Rs 102/kg','Equal quantities average the prices: (90+114)/2 = Rs 102/kg.'],
  ['EASY','How should oils at Rs 34/L and Rs 46/L be blended to obtain a Rs 40/L mixture? Give cheaper:dearer.','1:1','Rs 40 is midway between Rs 34 and Rs 46, so the cross-differences are both 6 and the ratio is 1:1.'],
  ['EASY','In what amount ratio should 40% concentrate be combined with 10% concentrate to make a 25% blend?','1:1','The target is midway between 10% and 40%, so the weaker:stronger amounts are equal. The order asked is stronger:weaker, still 1:1.'],
  ['EASY','Acid solutions at 25% and 70% are mixed to get 40% acid. What is the weaker-to-stronger amount ratio?','2:1','By alligation, weaker:stronger = (70-40):(40-25) = 30:15 = 2:1.'],
  ['EASY','A 15-L drink is 20% fruit concentrate. It is poured into 25 L of a 40% drink. What is the final concentrate percentage?','32.5%','Concentrate totals 15x0.20 + 25x0.40 = 13 L in 40 L, or 32.5%.'],
  ['EASY','Thirty kilograms of grain at Rs 24/kg is combined with 20 kg at Rs 39/kg. Find the mean cost per kilogram.','Rs 30/kg','Total cost is Rs 720 + Rs 780 = Rs 1,500 for 50 kg, giving Rs 30/kg.'],
  ['EASY','Nine kilograms of coffee at Rs 48/kg are mixed with 6 kg at Rs 78/kg. What is the blend’s unit cost?','Rs 60/kg','The total is Rs 432 + Rs 468 = Rs 900 for 15 kg, so the mean is Rs 60/kg.'],
  ['EASY','Twenty kilograms of rice at Rs 30/kg are blended with 30 kg at Rs 45/kg. Calculate the average price.','Rs 39/kg','Total cost is 20x30 + 30x45 = Rs 1,950 for 50 kg, giving Rs 39/kg.'],
  ['EASY','A tea seller needs 5 kg of a Rs 92/kg blend. The available teas cost Rs 80/kg and Rs 110/kg. How much of the Rs 110 tea is required?','2 kg','Cheaper:dearer = (110-92):(92-80) = 18:12 = 3:2. The dearer tea is 2/5 of the 5-kg blend, or 2 kg.'],
  ['EASY','A 20-L container holds 25% syrup. If 5 L of water evaporate, what is the syrup percentage in the remaining liquid?','33.3333%','Syrup remains 5 L, while total volume becomes 15 L. Thus 5/15 = 1/3, or 33.3333%.'],
  ['EASY','A 20-kg mix contains 30% salt. How many kilograms of pure salt must be added to raise the concentration to 40%?','3.3333 kg','There are 6 kg salt. Solve (6+x)/(20+x)=0.40: 6+x=8+0.4x, so x=10/3 kg, approximately 3.3333 kg.'],
  ['EASY','A 40-L beverage is 25% juice. How much pure juice should be poured in to make the new drink 40% juice?','10 L','There are 10 L juice. Solve (10+x)/(40+x)=0.40, giving x=10 L.'],
  ['EASY','Eighteen litres of 25% acid solution are diluted with water until they are 20% acid. What volume of water is added?','4.5 L','The acid remains 4.5 L. At 20%, total volume must be 4.5/0.20=22.5 L; add 4.5 L.'],
  ['EASY','Ten kilograms of 16% salt solution are joined with 15 kg of 24% solution. Find the salt percentage in the combined batch.','20.8%','Salt mass is 1.6+3.6=5.2 kg in 25 kg, so concentration is 20.8%.'],
  ['EASY','A fruit seller combines 14 kg of oranges at Rs 36/kg with 21 kg at Rs 50/kg. What is the mean price?','Rs 44.40/kg','Total cost is Rs 504+Rs 1,050=Rs 1,554 for 35 kg; the mean is Rs 44.40/kg.'],

  ['MEDIUM','A Rs 54/kg blend is made from grades costing Rs 42/kg and Rs 60/kg. What quantity ratio of cheaper to dearer grade is required?','1:2','The cross-differences are 60-54=6 and 54-42=12. Cheaper:dearer = 6:12 = 1:2.'],
  ['MEDIUM','A 36-kg mixture is prepared from grain at Rs 50/kg and Rs 70/kg, with a mean cost of Rs 62/kg. How many kilograms of the dearer grain are used?','21.6 kg','Cheaper:dearer = (70-62):(62-50)=8:12=2:3. The dearer share is 3/5 of 36=21.6 kg.'],
  ['MEDIUM','A 45-L tank is filled using 20% and 50% saline solutions to obtain a 32% blend. How many litres of the stronger solution are needed?','18 L','Weaker:stronger=(50-32):(32-20)=18:12=3:2. The stronger portion is 2/5 of 45 L = 18 L.'],
  ['MEDIUM','A shop combines 20% and 80% syrup. If the final concentration is 44%, what is the weaker-to-stronger volume ratio?','3:2','The differences are 80-44=36 and 44-20=24; 36:24 reduces to 3:2.'],
  ['MEDIUM','A 40-kg blend costs Rs 50/kg. One component costs Rs 40/kg and the other Rs 65/kg. How many kilograms of the dearer component are in the blend?','16 kg','Cheaper:dearer=(65-50):(50-40)=15:10=3:2. Dearer is 2/5 of 40, or 16 kg.'],
  ['MEDIUM','Rice at Rs 50/kg and Rs 80/kg is mixed, then sold for Rs 72/kg at a 20% gain. What cheaper-to-dearer purchase ratio was used?','2:1','The blend cost is 72/1.20=Rs 60/kg. Alligation gives cheaper:dearer=(80-60):(60-50)=20:10=2:1.'],
  ['MEDIUM','Twelve litres of a 20% solution are mixed with 18 litres of a 50% solution. What is the final concentration?','38%','Solute totals 2.4+9=11.4 L in 30 L, which is 38%.'],
  ['MEDIUM','A 30-kg blend of two grades at Rs 48/kg and Rs 72/kg averages Rs 58/kg. How many kilograms are from the Rs 72 grade?','12.5 kg','Cheaper:dearer=(72-58):(58-48)=14:10=7:5. The dearer share is 5/12 of 30=12.5 kg.'],
  ['MEDIUM','A dairy combines 24 L of 25% cream with 16 L of 55% cream. Determine the final fat percentage.','37%','Fat totals 6+8.8=14.8 L in 40 L, so the final percentage is 37%.'],
  ['MEDIUM','A merchant has 8 kg of spice costing Rs 42/kg and wants a Rs 54/kg blend using spice at Rs 66/kg. How much of the dearer spice must be added?','8 kg','Alligation requires cheaper:dearer=(66-54):(54-42)=1:1. Add 8 kg.'],
  ['MEDIUM','A 30-L acid blend is made from 30% and 60% solutions and has strength 42%. Find the amount of 60% solution.','12 L','Weaker:stronger=(60-42):(42-30)=18:12=3:2. Stronger is 2/5 of 30 L = 12 L.'],
  ['MEDIUM','A vendor buys 20 kg of pulses at Rs 36/kg and 30 kg at Rs 54/kg. At what price per kilogram must the mixture be sold for a 25% gain?','Rs 58.50/kg','Mean cost=(20x36+30x54)/50=Rs 46.80/kg. With 25% gain, selling price=46.8x1.25=Rs 58.50/kg.'],
  ['MEDIUM','A 25-kg alloy contains copper and zinc in the ratio 2:3. It is mixed with 15 kg of another alloy that is 60% copper. What percentage of the combined 40 kg is copper?','47.5%','The first alloy has 10 kg copper; the second has 9 kg. Copper totals 19 kg in 40 kg, or 47.5%.'],
  ['MEDIUM','A solution containing 35% alcohol is blended with pure alcohol to obtain 52% alcohol. What ratio of the weaker solution to pure alcohol is needed?','48:17','By alligation, weaker:pure=(100-52):(52-35)=48:17.'],
  ['MEDIUM','A 12-kg blend at Rs 90/kg is extended with a grade at Rs 66/kg until its mean cost is Rs 78/kg. How much of the cheaper grade is added?','12 kg','The target is midway between Rs 66 and Rs 90, so equal masses are needed; add 12 kg.'],
  ['MEDIUM','A 40-L juice base is 15% concentrate. How much 45% concentrate must be added to reach 30%?','40 L','Solve (6+0.45x)/(40+x)=0.30. Then 0.15x=6, so x=40 L.'],
  ['MEDIUM','A grocer mixes 18 kg of coffee at Rs 120/kg with 12 kg at Rs 150/kg. Find the selling price per kilogram for a 20% profit.','Rs 158.40/kg','Mean cost=(18x120+12x150)/30=Rs 132/kg. A 20% profit requires Rs 132x1.2=Rs 158.40/kg.'],
  ['MEDIUM','A 25-L drink is 40% fruit juice. How much water must be added to reduce the juice concentration to 25%?','15 L','Juice remains 10 L. For a 25% drink, total volume must be 40 L, so add 15 L water.'],
  ['MEDIUM','Two grades of flour cost Rs 32/kg and Rs 56/kg. If 30 kg of the cheaper grade is used, what quantity of dearer grade gives a Rs 41/kg blend?','18 kg','Cheaper:dearer=(56-41):(41-32)=15:9=5:3. If 30 kg is five parts, dearer quantity is three parts, or 18 kg.'],
  ['MEDIUM','A 50-L batch is 28% acid. It is blended with 20% acid solution to obtain 25% acid. How many litres of the 20% solution are used?','30 L','Alligation gives 20%:28%=(28-25):(25-20)=3:5. If the 28% portion is 50 L (five parts), the 20% amount is 30 L.'],
  ['MEDIUM','A milk vendor combines 10 L of 30% water milk with 15 L of 10% water milk. What percentage of the final mixture is water?','18%','Water totals 3+1.5=4.5 L in 25 L, or 18%.'],
  ['MEDIUM','A 60-kg grain blend costs Rs 48/kg and uses grades at Rs 40/kg and Rs 60/kg. What amount of the Rs 40 grade is present?','36 kg','Cheaper:dearer=(60-48):(48-40)=12:8=3:2. The cheaper share is 3/5 of 60=36 kg.'],
  ['MEDIUM','A class has girls averaging 84 and boys averaging 72. The overall mean is 79. What percentage of students are girls?','58.3333%','Girls:boys=(79-72):(84-79)=7:5. Girls are 7/12 of the class, or approximately 58.3333%.'],

  ['HARD','A blender combines 12 kg of coffee at Rs 80/kg, 18 kg at Rs 110/kg and 10 kg at Rs 140/kg. Find the mean cost per kilogram.','Rs 108.50/kg','Total cost is 960+1,980+1,400=Rs 4,340 for 40 kg, so the mean is Rs 108.50/kg.'],
  ['HARD','A 50-kg mix contains grades at Rs 30/kg, Rs 45/kg and Rs 70/kg in the ratio 2:3:5. What is its mean cost?','Rs 54.50/kg','The weighted mean is (2x30+3x45+5x70)/10 = 545/10 = Rs 54.50/kg.'],
  ['HARD','A 40-L solution is made from 10%, 30% and 70% liquids in the ratio 1:2:1. What is the final concentration?','35%','The weighted mean is (10+60+70)/4 = 35%.'],
  ['HARD','A 60-kg blend costs Rs 54/kg and is made from grades at Rs 42/kg, Rs 60/kg and Rs 72/kg. If the Rs 72 grade contributes 10 kg, how much Rs 42 grade is used?','26.6667 kg','Let x be the Rs 42 quantity and y the Rs 60 quantity. x+y=50 and 42x+60y+720=3,240. Substitution gives x=26 2/3 kg.'],
  ['HARD','A 100-L drink contains 30% juice. Some 60% concentrate is added until the blend is 42% juice. How many litres are added?','66.6667 L','Solve (30+0.60x)/(100+x)=0.42. Then 0.18x=12, so x=66 2/3 L.'],
  ['HARD','A trader mixes two grains at Rs 40/kg and Rs 70/kg. The blend is sold at Rs 66/kg for a 20% profit. What is the cheaper-to-dearer quantity ratio?','1:1','The mean cost is 66/1.2=Rs 55/kg. Alligation gives cheaper:dearer=(70-55):(55-40)=1:1.'],
  ['HARD','Three tea grades cost Rs 60/kg, Rs 84/kg and Rs 120/kg. Equal quantities of the first two are used. How much of the Rs 120 grade is needed per 10 kg of each cheaper grade to make a Rs 90/kg blend?','12 kg','The first two 10-kg lots cost 600+840=1,440. Solve (1,440+120x)/(20+x)=90; 30x=360, so x=12 kg.'],
  ['HARD','A 40-kg alloy at Rs 180/kg is made from metals costing Rs 150/kg and Rs 210/kg. What quantity of the dearer metal is present?','20 kg','The target is midway between Rs 150 and Rs 210, so the amounts are equal: 20 kg each.'],
  ['HARD','A 30-L alcohol solution is 40% alcohol. How much pure alcohol should be added to make it 65%?','21.4286 L','Solve (12+x)/(30+x)=0.65. Then 0.35x=7.5, so x=150/7 = 21.4286 L.'],
  ['HARD','A seller mixes 20 kg of rice at Rs 48/kg with 30 kg at Rs 72/kg. At what price must the mix be sold to gain 25% after 5% of the total mass is spoiled without recovery?','Rs 82.11/kg','Cost is Rs 3,120. Saleable mass is 47.5 kg. To gain 25%, revenue must be Rs 3,900, so price=3,900/47.5=Rs 82.1053/kg, or Rs 82.11/kg.'],
  ['HARD','A batch uses 25 kg of 20% solution and 15 kg of 60% solution. How much water must evaporate so the remaining mixture is 40% solute?','5 kg','Solute mass is 5+9=14 kg. At 40%, total mass must be 14/0.40=35 kg, so evaporate 40-35=5 kg water.'],
  ['HARD','A 50-kg alloy contains copper and tin in the ratio 3:2. It is blended with a 40% copper alloy to obtain 45% copper. How much of the second alloy is used?','150 kg','The first alloy is 60% copper. Alligation quantities first:second=(45-40):(60-45)=5:15=1:3. For 50 kg first alloy, use 150 kg second alloy.'],
  ['HARD','A shop blends tea costing Rs 90/kg and Rs 150/kg. The Rs 150 tea is one-third of the blend. What is the blend’s mean price?','Rs 110/kg','The weighted mean is (2/3)x90 + (1/3)x150 = Rs 110/kg.'],
  ['HARD','A 48-L mixture contains milk and water in the ratio 5:3. How much water should be added so that milk is 50% of the final mixture?','12 L','Milk is 30 L. For milk to be half, final volume must be 60 L, so add 12 L water.'],
  ['HARD','A 75-kg grain blend at Rs 52/kg contains grades at Rs 40/kg and Rs 64/kg. How many kilograms of the Rs 64 grade are used?','37.5 kg','Cheaper:dearer=(64-52):(52-40)=1:1, so 37.5 kg is dearer.'],
  ['HARD','A 30-L mixture is 20% salt. It is brought to a final volume of 50 L using 50% salt solution and pure water. How many litres of the 50% solution are needed for a final 30% salt concentration?','18 L','The final salt amount is 15 L. The original solution contributes 6 L, so the 50% solution must contribute 9 L, requiring 18 L; the remaining 2 L is water.'],
  ['HARD','A dairy mixes 20 L at 25% fat and 30 L at 45% fat. How much of a 60% cream is needed to raise the blend to 42%?','13.8889 L','Initial fat=5+13.5=18.5 L. Solve (18.5+0.60x)/(50+x)=0.42; 0.18x=2.5, so x=13.8889 L.'],
  ['HARD','A 100-kg blend contains grades at Rs 35/kg and Rs 55/kg, with the dearer grade twice the cheaper quantity. It is sold for Rs 54/kg. What is the profit percentage?','11.72%','The ratio is 1:2, so mean cost=(35+2x55)/3=Rs 48.3333/kg. Profit percentage=(54-48.3333)/48.3333 x100=11.724%, or 11.72%.'],
  ['HARD','A 40-kg blend costs Rs 63/kg and contains components at Rs 45/kg, Rs 60/kg and Rs 90/kg. If the first two components are equal in mass, how much of each is used?','14.4 kg','Let each of the Rs 45 and Rs 60 components be x, leaving 40-2x kg at Rs 90. Then 45x+60x+90(40-2x)=2,520; solving gives x=14.4 kg.'],
  ['HARD','A 60-L drink is 35% juice. After two identical replacements with water, the final concentration is 22.4%. What volume is removed each time?','12 L','After each replacement, the juice fraction is multiplied by 1-x/60. Solve 0.35(1-x/60)^2=0.224; therefore 1-x/60=0.8 and x=12 L.'],
  ['HARD','A 25-kg spice mixture costing Rs 72/kg is blended with spice at Rs 96/kg. How much of the second spice must be added to make the mean cost Rs 84/kg?','25 kg','The target is midway between Rs 72 and Rs 96, so equal quantities are needed: add 25 kg.'],
  ['HARD','A 90-L container has a 20% acid solution. How many litres of 50% solution must be added, with water making up the rest, to obtain 30% acid in a final 150 L?','54 L','Let x be 50% solution. The rest added is water. Acid balance: 18+0.5x=45, so x=54 L; the remaining 6 L is water.'],
  ['HARD','A mixture of 20% and 50% solutions has 36 L total and 32.5% concentration. How many litres of the stronger solution are present?','15 L','The weaker:stronger ratio is (50-32.5):(32.5-20)=17.5:12.5=7:5. The stronger share is 5/12 of 36=15 L.'],
  ['HARD','A merchant blends 40 kg at Rs 80/kg, 30 kg at Rs 100/kg and x kg at Rs 140/kg. If the overall mean is Rs 105/kg, find x.','32.8571 kg','Known cost is 3,200+3,000=6,200. Solve (6,200+140x)/(70+x)=105; 35x=1,150, so x=32.8571 kg.'],
  ['HARD','A tank contains 80 L of 25% brine. It is mixed with 40 L of 55% brine, then 20 L of the mixture is removed and replaced by pure water. What is the final salt percentage?','29.1667%','Initial salt=20+22=42 L in 120 L. Removing 20 L removes 7 L salt; 35 L salt remains in 120 L after water is added, or 29.1667%.'],
  ['HARD','A 100-kg blend of two grains costs Rs 58/kg. One grade costs Rs 46/kg and the other Rs 66/kg. If 10 kg of the dearer grain is replaced with the cheaper grade, what is the new mean cost?','Rs 56/kg','The original dearer share is 60 kg by alligation. Replacing 10 kg dearer with cheaper reduces cost by Rs 200; new mean=(5,800-200)/100=Rs 56/kg.'],
  ['HARD','A 40-L solution contains 30% acid. First 10 L is removed and replaced with water; then 10 L of this new mixture is removed and replaced with 50% acid. What is the final acid percentage?','29.375%','After first exchange, acid is 9 L in 40 L (22.5%). The next removal takes 2.25 L acid; adding 5 L acid gives 11.75 L in 40 L = 29.375%.'],
  ['HARD','A 70-kg blend is made from components priced Rs 50/kg, Rs 80/kg and Rs 110/kg in the ratio 2:3:2. What is its average price?','Rs 80/kg','The ratio total is 7 parts. Weighted mean=(2x50+3x80+2x110)/7=Rs 80/kg.'],
  ['HARD','A 50-L solution is 40% alcohol. Some 70% alcohol is added, then 10 L water, producing a 50% final solution. How much 70% alcohol was added?','50 L','Let x be added. (20+0.70x)/(60+x)=0.50, so 0.20x=10 and x=50 L.'],
  ['HARD','A jeweller mixes 20 g of 80% gold alloy with 30 g of 60% gold alloy. How many grams of pure gold must be added to make the final alloy 75% gold?','14 g','Gold starts at 16+18=34 g. Solve (34+x)/(50+x)=0.75; 0.25x=3.5, so x=14 g.'],
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
  const m=answer.match(/^(Rs )?([\d,]+(?:\.\d+)?)(.*)$/);
  if(!m) throw new Error(`Unsupported answer format: ${answer}`);
  const value=Number(m[2].replace(/,/g,'')), prefix=m[1]||'', suffix=m[3];
  const step=Math.max(value>=10?1:0.1,Math.abs(value)*0.1);
  const decimals=Math.max((m[2].split('.')[1]||'').length, Number.isInteger(step)?0:1);
  const nums=[value,value+step,value-step,value+2*step].filter((n,i,a)=>n>=0&&a.indexOf(n)===i);
  while(nums.length<4) nums.push(value+(nums.length+1)*step);
  const choices=nums.slice(0,4).map(n=>`${prefix}${Number(n.toFixed(decimals))}${suffix}`);
  return placeCorrect(choices,index);
}
function row(level,stem,options,correct,explanation,source) {
  return {subject_slug:'maths',subcategory_slug:'arithmetic-maths',chapter_slug:'alligation',question_text:stem,options,correct_option:correct,explanation,difficulty:level,is_pyq:false,pyq_year:null,pyq_exam_name:null,source};
}
const rows=pdf.map(([level,stem,choices,key,explanation,page])=>row(level,stem,Object.fromEntries('ABCD'.split('').map((k,i)=>[k,choices[i]])),key,explanation,`Verified from supplied Alligation PDF, page ${page}; exam/year not stated`));
for(let i=0;i<originals.length;i++) {
  const [level,stem,answer,explanation]=originals[i];
  const generated=optionsFor(normalized(answer),i);
  rows.push(row(level,stem,generated.options,generated.correct_option,explanation,'Original SSC-style practice question'));
}
const counts=Object.fromEntries(['EASY','MEDIUM','HARD'].map(level=>[level,rows.filter(r=>r.difficulty===level).length]));
if(rows.length!==90 || JSON.stringify(counts)!==JSON.stringify({EASY:30,MEDIUM:30,HARD:30})) throw new Error(`Unexpected batch shape: ${rows.length} ${JSON.stringify(counts)}`);
const out=path.join(__dirname,'..','data','alligation_verified_batch.json');
fs.writeFileSync(out,JSON.stringify({questions:rows},null,2)+'\n','utf8');
console.log(`Wrote ${rows.length} rows to ${out}`);
console.log('DIFFICULTY',counts);
console.log('PROVENANCE',{verified_pdf:pdf.length,original:originals.length});
