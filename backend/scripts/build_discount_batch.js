// Rebuild the reviewed Discount JSON from the maintained Profit & Loss seed
// questions plus explicitly checked PDF and original practice records.
const fs = require('node:fs');
const path = require('node:path');
const seed = require('../data/profit_loss_verified_batch.json').questions;
const rows = seed.filter(q => /discount|marked price|marked at/i.test(q.question_text)
  && !/sold without discount/i.test(q.question_text))
  .map(q => ({ ...q, chapter_slug: 'discount',
    source: 'Original SSC-style practice question; adapted from reviewed Profit & Loss bank' }));
if (rows.length !== 33) throw new Error(`expected 33 discount-specific source rows; found ${rows.length}`);

const pdfRows = [
  ['An article marked at Rs 3,600 is sold for Rs 3,132. What discount percentage was allowed?',13,'%','Discount = 3,600 - 3,132 = Rs 468; 468/3,600 x 100 = 13%.',5,'EASY'],
  ['A marked price is reduced successively by 5%, 10% and 20%. What single discount is equivalent?',31.6,'%','Net factor = .95 x .90 x .80 = .684; equivalent discount = 31.6%.',6,'MEDIUM'],
  ['A coffee maker marked at Rs 2,000 receives successive discounts of 30%, 20% and 10%. Find its selling price.',1008,'Rs','2,000 x .70 x .80 x .90 = Rs 1,008.',7,'MEDIUM'],
  ['An article marked at Rs 1,800 is discounted by 10% and then 20%. What is the final price?',1296,'Rs','1,800 x .90 x .80 = Rs 1,296.',8,'EASY'],
  ['On a Rs 50,000 bill, compare a single 20% discount with successive discounts of 16% and 4%. What is the difference in the amounts discounted?',320,'Rs','Successive rate = 1 - .84 x .96 = 19.36%; difference = .64% of 50,000 = Rs 320.',13,'MEDIUM'],
  ['A notebook costs a shopkeeper Rs 85. After allowing a 15% discount, the shopkeeper earns 20% on cost. What was its marked price?',120,'Rs','Selling price = 85 x 1.20 = Rs 102; mark = 102/.85 = Rs 120.',18,'MEDIUM'],
  ['A trader gives an 18% discount on the marked price and earns 6.6% on cost. By what percentage is the mark above cost?',30,'%','Let cost=100. Then .82 MP=106.6, so MP=130, or 30% above cost.',20,'HARD'],
  ['For the larger of these offers, buy 3 and get 4 free or buy 5 and get 6 free, what is its equivalent discount rate?',57.14,'%','First offer: 4/7 = 57.14%; second: 6/11 = 54.55%; the first is larger.',23,'MEDIUM'],
  ['A bottle has an MRP of Rs 20. Under a buy 2, get 1 free offer, what is the effective discount percentage?',33.33,'%','Pay Rs 40 for goods listed at Rs 60; discount = 20/60 x 100 = 33.33%.',24,'EASY'],
  ['A buyer gets 3 bananas free on buying 12 and then receives a further 25% bill discount. What is the equivalent discount?',40,'%','Free quantity gives 20% off; successive reduction = 1 - .80 x .75 = 40%.',25,'MEDIUM'],
];
function rounded(x) { return Math.round((x + Number.EPSILON) * 100) / 100; }
function display(x) { return Number.isInteger(x) ? String(x) : String(rounded(x)); }
function generated(stem, answer, unit, explanation, difficulty, source, ix) {
  const value = rounded(answer);
  const step = unit === 'ratio' ? 1 : Math.max(unit === '%' ? 1 : 2, rounded(Math.abs(value) * (unit === '%' ? .08 : .06)));
  const vals = [...new Set([value, rounded(value + step), rounded(value - step), rounded(value + step * 2)])];
  while (vals.length < 4) vals.push(rounded(value + step * (vals.length + 1)));
  const correct = ix % 4;
  const at = vals.indexOf(value); [vals[correct], vals[at]] = [vals[at], vals[correct]];
  const options = Object.fromEntries('ABCD'.split('').map((key, i) => [key,
    unit === '%' ? `${display(vals[i])}%` : unit === 'ratio' ? `${Math.round(vals[i])}:10` : `${display(vals[i])} Rs`]));
  return { subject_slug:'maths', subcategory_slug:'arithmetic-maths', chapter_slug:'discount', question_text:stem,
    options, correct_option:'ABCD'[correct], explanation, difficulty, is_pyq:false, pyq_year:null, pyq_exam_name:null, source };
}
let n=0;
for (const [stem,a,u,e,page,d] of pdfRows) rows.push(generated(stem,a,u,e,d,`Verified from supplied Discount PDF, page ${page}; exam/year not stated`,n++));

const easy = [
['A jacket marked at Rs 800 receives 15% off. Find the amount paid.',680,'Rs','800 x .85 = Rs 680.'],
['A lamp marked Rs 1,250 sells for Rs 1,000. Find its discount rate.',20,'%','250/1,250 x 100 = 20%.'],
['A shop reduces a Rs 640 list price by Rs 96. What discount percentage is that?',15,'%','96/640 x 100 = 15%.'],
['A chair sells for Rs 765 after a 15% discount. Find its marked price.',900,'Rs','765/.85 = Rs 900.'],
['A bag marked Rs 2,500 is sold at 12% off. Find the selling price.',2200,'Rs','2,500 x .88 = Rs 2,200.'],
['A book marked Rs 480 is sold for Rs 408. Find the discount percentage.',15,'%','72/480 x 100 = 15%.'],
['A retailer deducts Rs 400 from a marked price of Rs 3,200. Find the discount rate.',12.5,'%','400/3,200 x 100 = 12.5%.'],
['A buyer saves Rs 225 on an item marked Rs 1,500. Find the percentage saved.',15,'%','225/1,500 x 100 = 15%.'],
['A 25% discount brings a table price to Rs 1,350. What was the mark?',1800,'Rs','1,350/.75 = Rs 1,800.'],
['A watch marked at Rs 2,400 is sold for Rs 2,040. Find the discount rate.',15,'%','360/2,400 x 100 = 15%.'],
['A kettle marked Rs 960 gets a 12.5% discount. Find the reduction amount.',120,'Rs','960 x .125 = Rs 120.'],
['A suitcase marked Rs 3,500 is offered at 8% off. Find the discount amount.',280,'Rs','3,500 x .08 = Rs 280.'],
['A toy marked Rs 1,800 sells for Rs 1,530. What discount rate was used?',15,'%','270/1,800 x 100 = 15%.'],
['A customer pays Rs 612 for an item marked Rs 680. Find the discount rate.',10,'%','68/680 x 100 = 10%.'],
['A dress marked Rs 2,400 is offered at 20% off. Find the sale price.',1920,'Rs','2,400 x .80 = Rs 1,920.'],
['A shop gives Rs 720 off an item marked Rs 3,600. Find the rate.',20,'%','720/3,600 x 100 = 20%.'],
['A customer pays Rs 540 after a 10% discount. Find the marked price.',600,'Rs','540/.90 = Rs 600.'],
['An appliance marked Rs 900 receives a 30% discount. What is paid?',630,'Rs','900 x .70 = Rs 630.'],
['A mixer listed at Rs 1,600 sells for Rs 1,360. Find the discount rate.',15,'%','240/1,600 x 100 = 15%.'],
['A shop sells a Rs 2,250 item for Rs 2,025. What percent was deducted?',10,'%','225/2,250 x 100 = 10%.'],
['A desk marked Rs 480 is sold at 25% off. Find its selling price.',360,'Rs','480 x .75 = Rs 360.'],
['Shoes listed at Rs 1,760 receive a 6.25% reduction. Find the amount due.',1650,'Rs','1,760 x .9375 = Rs 1,650.'],
];
const medium = [
['A marked price of Rs 4,000 is reduced by 10%, then by 5%. Find the bill.',3420,'Rs','4,000 x .90 x .95 = Rs 3,420.'],
['Successive discounts of 20% and 15% are offered. Find their equivalent single rate.',32,'%','1 - .80 x .85 = 32%.'],
['An article sells for Rs 2,448 after discounts of 15% and 20%. Find its marked price.',3600,'Rs','Combined factor=.85 x .80=.68; 2,448/.68=Rs 3,600.'],
['A Rs 5,000 item gets 10% off, then a Rs 350 coupon. Find the total discount rate.',17,'%','Paid=5,000 x .90 -350=4,150; reduction=850/5,000=17%.'],
['A shop lowers its discount on a Rs 3,000 item from 20% to 12%. By what percent do receipts rise?',10,'%','Receipts rise from 2,400 to 2,640; increase=240/2,400=10%.'],
['Offer A gives 25% off Rs 4,800; offer B gives 15% then 12% off. How much cheaper is the lower offer?',9.6,'Rs','A=3,600; B=4,800 x .85 x .88=3,590.40; B is Rs 9.60 lower.'],
['A seller receives Rs 3,528 after allowing 16% off. Find the marked price.',4200,'Rs','3,528/.84=Rs 4,200.'],
['A printer marked Rs 6,400 is discounted by 12.5%, then a Rs 200 voucher is used. Find the final bill.',5400,'Rs','6,400 x .875 -200=Rs 5,400.'],
['Two successive discounts of 10% and 20% equal one discount of what rate?',28,'%','1 - .90 x .80 = 28%.'],
['A coat costs Rs 1,530 after a 15% reduction. Find its list price.',1800,'Rs','1,530/.85=Rs 1,800.'],
];
const hard = [
['A retailer marks a product 40% above cost, then discounts it by 10% and 5%. Find profit percent.',19.7,'%','1.40 x .90 x .95=1.197 of cost; profit=19.7%.'],
['A mark is 25% above cost. After 10% off, the seller earns Rs 300. Find cost.',2400,'Rs','SP=1.25 x .90 CP=1.125 CP; .125 CP=300; CP=Rs 2,400.'],
['Goods are marked 60% above cost, discounted 20%, and delivery costs 4% of cost. Find net profit percent.',24,'%','Revenue factor=1.60 x .80=1.28; less .04 expense gives 24%.'],
['A marked price is first discounted 20%, then 10%. Find the equivalent single discount.',28,'%','Net factor=.80 x .90=.72; discount=28%.'],
['After 25% off, an extra discount x% makes the total discount 40%. Find x.',20,'%',' .75(1-x)=.60, so x=20%.'],
['An article is marked 50% above cost, discounted 20%, then a Rs 120 coupon is used. The final profit is 5%. Find cost.',800,'Rs','1.50C x .80 -120=1.05C; .15C=120; C=Rs 800.'],
['A shop gives 30% off, then a 5% loyalty reduction on the sale price. Find the single discount.',33.5,'%','1 - .70 x .95=33.5%.'],
['A retailer marks an item 80% above cost and allows 25% off. Find profit percentage.',35,'%','1.80 x .75=1.35; profit=35%.'],
['Two stores sell an item at the same final price. A gives 20% off; B gives 10% then 12%. Find marked-price ratio A:B.',11,'ratio','Equal SP gives .80 MP_A=.88 MP_B, so MP_A:MP_B=.88:.80=11:10.'],
['A price rises 20%, then is discounted 20%. Find the net percentage change from the original.',4,'%','1.20 x .80=.96, a 4% decrease.'],
['An item sells for Rs 2,700 after a 10% discount and Rs 300 coupon. Find its marked price.',3333.33,'Rs','(2,700+300)/.90=Rs 3,333.33.'],
['A seller gives 15% off and still earns 19% profit. By what percent is the mark above cost?',40,'%','1.19 CP=.85 MP; MP/CP=1.40, 40% above cost.'],
['Discounts of 12.5% and 20% are followed by a third discount to make the total 40%. Find the third rate.',14.29,'%','First factor=.875 x .80=.70; required final factor=.60/.70=6/7; third discount=14.2857%.'],
['An item is marked 30% above cost, discounted 10%, then a Rs 60 coupon leaves 8% profit. Find cost.',666.67,'Rs','1.30C x .90 -60=1.08C; .09C=60; C=Rs 666.67.'],
['A Rs 6,000 item gets 25% off and the reduced price is then increased 10%. Find the final price.',4950,'Rs','6,000 x .75 x 1.10=Rs 4,950.'],
];
for(const [arr,d] of [[easy,'EASY'],[medium,'MEDIUM'],[hard,'HARD']]) for(const [s,a,u,e] of arr) rows.push(generated(s,a,u,e,d,'Original SSC-style practice question',n++));
const counts=Object.fromEntries(['EASY','MEDIUM','HARD'].map(d=>[d,rows.filter(q=>q.difficulty===d).length]));
if(rows.length!==90 || Object.values(counts).some(c=>c!==30)) throw Error(`invalid bank: ${rows.length} ${JSON.stringify(counts)}`);
fs.writeFileSync(path.join(__dirname, '../data/discount_verified_batch.json'),JSON.stringify({questions:rows},null,2)+'\n');
console.log('Wrote 90 questions',JSON.stringify(counts),'PDF',rows.filter(q=>q.source.startsWith('Verified from')).length,
  'original',rows.filter(q=>q.source.startsWith('Original SSC-style practice question')).length);
