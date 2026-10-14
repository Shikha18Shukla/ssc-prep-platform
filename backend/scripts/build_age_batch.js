// Build the reviewed Age chapter batch from the scanned supplied PDF and
// separately authored SSC-style practice questions.
const fs = require('node:fs');
const path = require('node:path');

const pdfQuestions = [
  ['EASY', 'A mother and her son are aged in the ratio 7:3. Their ages total 60 years. By how many years is the mother older?', ['12 years', '24 years', '18 years', '30 years'], 'B', 'The ten ratio parts total 60, so one part is 6. The age gap is four parts: 4 x 6 = 24 years.', 5],
  ['MEDIUM', 'A woman and a girl are currently in the ratio 4:5, and their ages sum to 81 years. What will their ratio be after 9 years?', ['6:5', '5:4', '5:6', '3:4'], 'C', 'Their current ages are 36 and 45. After 9 years they will be 45 and 54, which reduces to 5:6.', 6],
  ['EASY', 'Chandrika and Gokati currently have ages in the ratio 4:5. Four years from now, their ages will total 80 years. What will their age ratio be then?', ['8:9', '9:11', '5:6', '4:5'], 'B', 'Their present total is 80 - 8 = 72, so their ages are 32 and 40. In four years they are 36 and 44, or 9:11.', 8],
  ['EASY', 'Kamal and Shambhu have ages in the ratio 7:4 and a combined age of 44. What will the ratio of Shambhu’s age to Kamal’s after 8 years?', ['4:7', '15:12', '4:3', '2:3'], 'D', 'Their ages are 28 and 16. After 8 years Shambhu will be 24 and Kamal 36, giving 2:3.', 7],
  ['EASY', 'Arun is as many years younger than Bhushan as he is older than Anil. Bhushan and Anil together are 58. How old is Arun?', ['30 years', '29 years', '40 years', '50 years'], 'B', 'The equal gaps make Arun the midpoint of Bhushan and Anil, so twice Arun’s age is 58. Arun is 29.', 9],
  ['EASY', 'Rakesh is exactly midway in age between Rajesh and Mukesh. Rajesh and Mukesh together are 48 years old. How old is Rakesh?', ['20 years', '24 years', '30 years', '25 years'], 'B', 'If Rakesh is the midpoint, the mean of the two outer ages is Rakesh’s age: 48 / 2 = 24.', 10],
  ['MEDIUM', 'Amar and Anjali’s present ages are in the ratio 2:3. In three years their ratio will be 3:4. What is Amar’s present age?', ['6 years', '9 years', '15 years', 'Cannot be determined'], 'A', 'Let their ages be 2x and 3x. (2x+3)/(3x+3)=3/4 gives x=3, so Amar is 6.', 11],
  ['HARD', 'Six years ago Kamal and Suresh were in the ratio 6:5. Four years from now their ratio will be 11:10. What is Suresh’s present age?', ['20 years', '18 years', '16 years', '24 years'], 'C', 'Let their ages six years ago be 6x and 5x. Four years later, (6x+10)/(5x+10)=11/10, so 60x+100=55x+110, x=2 and Suresh’s present age is 5x+6=16.', 12],
  ['MEDIUM', 'Ten years ago B was ten times C’s age. Today their ages are in the ratio 4:1. How old is B now?', ['10 years', '40 years', '60 years', '80 years'], 'C', 'Let present ages be 4x and x. Ten years ago, 4x-10=10(x-10), so x=15 and B is 60.', 13],
  ['MEDIUM', 'Six years ago A was twice B’s age. Their present ages are in the ratio 4:3. How old is B now?', ['9 years', '6 years', '12 years', '16 years'], 'A', 'Let present ages be 4x and 3x. Six years ago, 4x-6=2(3x-6), giving x=3 and B=9.', 14],
  ['HARD', 'Sneha is one-sixth of her father’s age. In ten years, her father will be twice Vimal’s age. Vimal turned 8 two years ago. How old is Sneha now?', ['24 years', '6 years', '30 years', '5 years'], 'D', 'Vimal is now 10, so the father will be 20 years older in the stated future, at age 40. He is now 30; Sneha is 30/6 = 5.', 15],
  ['MEDIUM', 'Sudha is twice Radha’s age. If Radha’s age is reduced by 6 and Sudha’s is increased by 4, the resulting Sudha age is four times the resulting Radha age. What will their ages be in 2 years?', ['Sudha 30, Radha 14', 'Sudha 26, Radha 12', 'Sudha 34, Radha 20', 'Sudha 30, Radha 16'], 'D', 'Let Radha be R and Sudha 2R. Then 2R+4=4(R-6), so R=14 and Sudha=28. In two years they will be 16 and 30.', 16],
  ['MEDIUM', 'Neeraj is half Suraj’s age. If Neeraj’s age is reduced by 8 while Suraj’s is increased by 5, Suraj will be five times Neeraj’s adjusted age. What were their ages two years ago?', ['30 and 15 years', '28 and 14 years', '26 and 12 years', '28 and 13 years'], 'D', 'Let Neeraj be N and Suraj be 2N. Then 2N+5=5(N-8), so N=15 and Suraj=30. Two years ago they were 13 and 28.', 17],
  ['EASY', 'The average age of 27 students is 22 years. Including their teacher raises the average to 23. How old is the teacher?', ['42 years', '48 years', '50 years', '52 years'], 'C', 'The students total 27 x 22 = 594 years. The new total is 28 x 23 = 644, so the teacher is 50.', 18],
  ['MEDIUM', 'Nineteen group members average 24 years. Adding a faculty member raises the average by 4 months. How old is the faculty member?', ['35 years', '30 years 8 months', '37 years 4 months', '32 years 8 months'], 'B', 'The new total is 20 x 24 years 4 months = 486 years 8 months. The 19 members total 456 years, so the faculty member is 30 years 8 months.', 19],
  ['EASY', 'Five children were born exactly four years apart. Their ages sum to 80 years. How old is the eldest child?', ['18 years', '24 years', '16 years', '28 years'], 'B', 'The middle child is 16, the average age. The eldest is two four-year intervals older: 16+8=24.', 20],
  ['EASY', 'Five years ago a couple averaged 23 years of age. Today the couple and their child average 20. How old is the child today?', ['9 years', '14 years', '4 years', '3 years'], 'C', 'The parents’ current total is 46+10=56. The family total is 3 x 20=60, so the child is 4.', 21],
  ['MEDIUM', 'A couple averaged 27 years four years ago, when their child was born. What is the child’s present age if the current family average is 21?', ['4 years', '3 years', '2 years', '1 year'], 'D', 'The parents’ combined age was 54, and has increased by 8 to 62. The family total is 3 x 21 = 63, so the child is 1.', 22],
  ['MEDIUM', 'A couple married four years ago when their average age was 25. Today the husband, wife, and their son average 20. How old is the son?', ['1 year', '2 years', '2.5 years', '3 years'], 'B', 'At marriage the parents totaled 50. Today they total 58. The family total is 60, so their son is 2.', 23],
  ['EASY', 'Seven children average 12 years. One child aged 6 dies. What is the average age of the remaining six?', ['13 years', '10 years', '11 years', '14 years'], 'A', 'The original total was 84. Removing 6 leaves 78, and 78/6 = 13.', 24],
  ['HARD', 'Five sons have distinct positive integer ages and average 11 years. What is the greatest possible age of the eldest?', ['50 years', '45 years', '55 years', '35 years'], 'B', 'Their total is 55. Minimize the other four distinct positive ages to 1, 2, 3, and 4; the eldest can be 55-10=45.', 25],
  ['EASY', 'Twenty boys average 14 years. A 16-year-old leaves and a new boy joins; the average becomes 13.8. How old is the new boy?', ['14 years', '13 years', '16 years', '12 years'], 'D', 'The group total falls by (14-13.8) x 20 = 4 years. The replacement is 16-4=12.', 26],
  ['MEDIUM', 'A class has 42 boys. Replacing a 10-year-old with a new boy raises the average age by 2 months. How old is the new boy?', ['12 years 2 months', '19 years', '17 years', '10 years 6 months'], 'C', 'A two-month increase in the mean raises the class total by 42 x 2 = 84 months, or 7 years. The new boy is 10+7=17.', 27],
  ['MEDIUM', 'Ten people have an average age that rises by 3 years after two people aged 23 and 25 are replaced. What is the average age of the two newcomers?', ['23 years', '40 years', '37 years', '39 years'], 'D', 'The total rises by 10 x 3 = 30 years. The newcomers total 23+25+30=78, so their average is 39.', 28],
];

const originalQuestions = [
  ['EASY', 'Mira and her brother have a combined age of 52 years, and Mira is 13 years older. How old is her brother?', 19, 'The younger age is (52-13)/2 = 19 years.'],
  ['EASY', 'A father is 28 years older than his daughter. Together they are 56. What is the daughter’s age?', 14, 'Subtract the 28-year gap from the total: 28/2 = 14 years.'],
  ['EASY', 'A mother is three times her child’s age, and she is 24 years older. How old is the child?', 12, 'If the child is x, the mother is 3x; 3x-x=24, so x=12.'],
  ['EASY', 'Eight years ago, Dev was 12. How old is he now?', 20, 'Present age = 12+8 = 20 years.'],
  ['EASY', 'Two cousins have ages in the ratio 4:3 and together are 49. What is the younger cousin’s age?', 21, 'Seven parts equal 49, so a part is 7; the younger cousin is 3 x 7 = 21.'],
  ['EASY', 'The older of two sisters is 8 years older. Their ages total 44. How old is the younger sister?', 18, 'Younger age = (44-8)/2 = 18 years.'],
  ['EASY', 'A brother is 5 years older than his sister, who is 16. How old is he?', 21, '21-16 = 5 years, so the brother is 21.'],
  ['EASY', 'Two brothers together are 47. The younger is 19. Find the older brother’s age.', 28, '47-19 = 28 years.'],
  ['EASY', 'The age ratio of two cousins is 3:2 and the older is 9 years older. How old is the younger?', 18, 'One ratio part is 9 years; the younger is 2 x 9 = 18.'],
  ['EASY', 'Asha is four times Neha’s age. Their ages total 50 years. How old is Neha?', 10, 'Five equal parts total 50, so Neha is one part: 10 years.'],
  ['EASY', 'Three cousins’ ages total 72 years. Two are 24 and 28. How old is the third?', 20, '72-24-28 = 20 years.'],
  ['EASY', 'Three siblings are 14, 16, and 18 years old. What is the middle age?', 16, 'In the ordered ages 14, 16, 18, the middle value is 16.'],
  ['EASY', 'A grandfather is 60 and his grandson is 12. By how many years is the grandfather older?', 48, '60-12 = 48 years.'],
  ['EASY', 'A parent is 42 and a child is 14. How many years older is the parent?', 28, '42-14 = 28 years.'],
  ['EASY', 'A girl is 17 and her brother is 23. What will their age difference be in 10 years?', 6, 'Both ages increase by the same amount, so their difference remains 23-17 = 6.'],
  ['EASY', 'A woman is 36 and her daughter is 12. How old will the woman be when the daughter is 20?', 44, 'The daughter reaches 20 in 8 years; the woman will then be 36+8 = 44.'],
  ['EASY', 'Two friends have a total age of 63 years. One is 27. How old is the other?', 36, '63-27 = 36 years.'],
  ['EASY', 'The present ratio of a father’s age to his son’s is 5:2. If the son is 18, how old is the father?', 45, 'Two parts equal 18, so one part is 9; the father is 5 x 9 = 45.'],
  ['EASY', 'A mother is 32 years older than her son. If the son is 11, how old is the mother?', 43, '32+11 = 43 years.'],
  ['EASY', 'Three years ago, Isha was 15. What is twice her age now?', 36, 'Isha is 18 now; twice 18 is 36.'],
  ['MEDIUM', 'A father is four times his son’s age now. In 12 years he will be twice his son’s age. How old is the son now?', 6, 'Let the son be x. 4x+12=2(x+12), so x=6 years.'],
  ['MEDIUM', 'A mother is 3 times her daughter’s age. In 8 years the mother will be twice the daughter’s age. How old is the daughter now?', 8, 'Let the daughter be x. 3x+8=2(x+8), hence x=8.'],
  ['MEDIUM', 'The present ages of two people are in the ratio 5:3. Six years ago the ratio was 3:1. What is the younger person’s present age?', 9, 'Let ages be 5x and 3x. (5x-6)/(3x-6)=3 gives 5x-6=9x-18, x=3; younger age is 9.'],
  ['MEDIUM', 'A father and son total 54 years. In six years the father will be twice the son’s age. What is the son’s present age?', 16, 'Let son=x and father=54-x. Then 60-x=2(x+6), so x=16.'],
  ['MEDIUM', 'Two years ago, a teacher was five times a student’s age. In 10 years the teacher will be twice the student’s age. How old is the student now?', 6, 'Let current ages be T and S. T-2=5(S-2) and T+10=2(S+10). Solving gives S=6.'],
  ['MEDIUM', 'Three siblings have a total age of 42. The eldest is twice the youngest, and the middle child is 6 years older than the youngest. How old is the youngest?', 9, 'Let youngest=x. x+(x+6)+2x=42, so 4x=36 and x=9.'],
  ['MEDIUM', 'A mother is 24 years older than her child. Six years ago she was four times as old. How old is the child now?', 14, 'Let child=x. x+24-6=4(x-6), so x+18=4x-24 and x=14.'],
  ['MEDIUM', 'A couple’s ages total 68. The husband is 4 years older. How old will the wife be in 7 years?', 39, 'Wife=(68-4)/2=32; in 7 years she will be 39.'],
  ['MEDIUM', 'A parent is 6 times the child’s age. After 15 years, the parent will be three times the child’s age. How old is the child?', 10, 'Let child=x. 6x+15=3(x+15), so 3x=30 and x=10.'],
  ['MEDIUM', 'In a family, two parents average 32 years. Their three children average 12. What is the average age of all five?', 20, 'Parents total 64; children total 36; the combined mean is (64+36)/5=20 years.'],
  ['MEDIUM', 'The average age of 8 players is 21. A 25-year-old leaves and a new player joins; the average falls to 20.5. How old is the new player?', 21, 'The group total falls by 8 x .5 = 4. The replacement is 25-4=21.'],
  ['MEDIUM', 'Four years from now, a pair’s ages will total 70. Their present ages differ by 10 years. What is the younger person’s present age?', 26, 'Their current total is 70-8=62. The younger age is (62-10)/2=26.'],
  ['MEDIUM', 'The mean age of 12 workers is 31. A 43-year-old worker is replaced, reducing the mean to 30.5. What is the new worker’s age?', 37, 'The total falls by 12 x .5=6, so the replacement is 43-6=37.'],
  ['MEDIUM', 'A father is 30 years older than his daughter. In 5 years their combined ages will be 60. How old is the daughter now?', 10, 'Their present total is 50; younger=(50-30)/2=10.'],
  ['MEDIUM', 'Two brothers have a present age ratio of 7:4. In 8 years their ratio will be 3:2. How old is the younger brother now?', 16, 'Let ages be 7x and 4x. (7x+8)/(4x+8)=3/2 gives 14x+16=12x+24, x=4; younger=16.'],
  ['MEDIUM', 'A grandfather’s age is 5 times his grandson’s. Ten years ago he was 9 times as old. What is the grandson’s current age?', 20, 'Let grandson=x. 5x-10=9(x-10), so 80=4x and x=20.'],
  ['MEDIUM', 'A mother and daughter’s ages total 50. In 5 years the mother will be twice her daughter’s age. How old is the daughter now?', 15, 'Let daughter=x and mother=50-x. 55-x=2(x+5), so 45=3x and x=15.'],
  ['MEDIUM', 'The ages of three friends add to 72. The second is 4 years older than the first, and the third is twice the first. Find the first friend’s age.', 17, 'Let the first be x. x+(x+4)+2x=72 gives x=17.'],
  ['MEDIUM', 'A father is 3 times as old as his son. Eight years ago he was 5 times as old. How old is the son now?', 16, 'Let son=x. 3x-8=5(x-8), so 32=2x and x=16.'],
  ['HARD', 'A mother is 4 times her child’s age. Eight years ago she was 8 times the child’s age. In 12 years, how old will the child be?', 26, 'Let child=x. 4x-8=8(x-8), so 56=4x and x=14. In 12 years the child will be 26.'],
  ['HARD', 'A father’s age is 3 times his son’s. In 12 years it will be twice the son’s age. How old will the father be in 20 years?', 56, 'Let son=x. 3x+12=2(x+12), so x=12 and father=36; in 20 years father is 56.'],
  ['HARD', 'A woman is 5 times her daughter’s age. Ten years ago she was 9 times her daughter’s age. What will their ages total in 5 years?', 130, 'Let daughter=x. 5x-10=9(x-10), so x=20 and the woman is 100. Their future total is 130.'],
  ['HARD', 'Three siblings have ages in the ratio 2:3:5 and total 70. How old will the youngest and eldest be together in 6 years?', 61, 'One part is 7; youngest is 14 and eldest 35. Six years later they total 14+6+35+6=61.'],
  ['HARD', 'A father and two children total 88 years. The father is 4 times the older child’s age, and the older child is twice the younger. How old is the younger child?', 8, 'Let younger=x, older=2x and father=8x. Then 11x=88, so x=8.'],
  ['HARD', 'A couple’s present ages total 76. The husband is 4 years older. Their child is 8. What will the average age of all three be in 6 years?', 34, 'Current parent ages are 40 and 36. With the child total 84; in six years total 102, average 34.'],
  ['HARD', 'A group of 6 siblings averages 18 years. The youngest is 8; the other five have distinct integer ages. What is the greatest possible age of the eldest?', 58, 'Total is 108. The five other distinct ages must be at least 9, 10, 11, 12, and the eldest; so eldest=108-(8+9+10+11+12)=58.'],
  ['HARD', 'Three years ago a pair’s ages were in the ratio 5:4. In 9 years they will total 60. How old is the younger person now?', 19, 'Their current total is 60-18=42; three years ago it was 36. Nine ratio parts equal 36, so the younger was 16 and is now 19.'],
  ['HARD', 'A mother and son currently total 54 years. Six years from now the mother will be twice the son’s age. How old is the son now?', 16, 'Let son=x, mother=54-x. Then 60-x=2(x+6), giving x=16.'],
  ['HARD', 'A father is 5 times as old as his son. In 15 years he will be twice as old. How old is the father now?', 25, 'Let son=x. 5x+15=2(x+15), so x=5 and father=25.'],
  ['HARD', 'A three-person family averages 24 years. The parent is 42, and the two children differ by 6 years. How old is the younger child?', 12, 'Family total=72; children total=30. Younger=(30-6)/2=12.'],
  ['HARD', 'The mean age of 10 trainees is 19. A 24-year-old leaves and is replaced, increasing the mean by 1.5 years. What is the new trainee’s age?', 39, 'The total rises by 10 x 1.5=15, so the replacement is 24+15=39.'],
  ['HARD', 'A father and daughter total 64 years. Four years ago the father was 7 times her age. How old will the daughter be in 10 years?', 21, 'Let daughter=x and father=64-x. Then 60-x=7(x-4), so x=11; in 10 years she will be 21.'],
  ['HARD', 'Three ages are consecutive multiples of 5 and sum to 90. What is the eldest age?', 35, 'Let ages be 5n, 5(n+1), 5(n+2). Their sum is 15n+15=90, n=5; eldest is 35.'],
  ['HARD', 'A parent is 4 times a child’s age. In 6 years the parent will be 3 times the child’s age. How old is the parent now?', 48, 'Let child=x. 4x+6=3(x+6), so x=12 and parent=48.'],
  ['HARD', 'Two people currently total 82 years. Five years ago their ages were in the ratio 7:5. How old is the younger person now?', 35, 'Five years ago their total was 82-10=72. The younger was 5/12 x 72=30, so now they are 35.'],
  ['HARD', 'A father and son currently total 68 years. In 8 years the father will be twice the son’s age. How old is the father now?', 48, 'Let son=x and father=68-x. Then 76-x=2(x+8), so x=20 and the father is 48.'],
  ['HARD', 'Seven years ago a father was five times his son’s age. In five years he will be three times his son’s age. How old is the father now?', 67, 'Let the son be S and father F. F-7=5(S-7), F+5=3(S+5). Equating gives S=19 and F=67.'],
  ['HARD', 'A mother is three times her daughter’s age. Eight years ago she was five times as old. How old is the mother now?', 48, 'Let daughter=x. 3x-8=5(x-8), so x=16 and mother=48.'],
  ['HARD', 'A father and son are now in the ratio 5:2. In nine years the ratio will be 2:1. How old is the father now?', 45, 'Let ages be 5x and 2x. 5x+9=2(2x+9), so x=9 and the father is 45.'],
  ['HARD', 'Two sisters are 12 years apart. Six years ago the elder was twice the younger. How old is the elder now?', 30, 'Let younger=y and elder=y+12. y+6=2(y-6), so y=18 and elder=30.'],
  ['HARD', 'Nine staff members average 24 years. Adding a tenth staff member raises the average to 26. How old is the new member?', 44, 'The original total is 216 and the new total is 260; the added member is 44.'],
  ['HARD', 'A team of 15 averages 22 years. Replacing a 17-year-old raises the average by 1.2 years. How old is the new member?', 35, 'The total rises by 15 x 1.2=18 years, so the replacement is 17+18=35.'],
  ['HARD', 'A parent and child currently total 76 years. Eight years ago their ages were in the ratio 4:1. How old is the child now?', 20, 'Eight years ago their total was 60, so one of five ratio parts was 12. The child is now 12+8=20.'],
  ['HARD', 'Three people total 92 years. The eldest is 10 years older than the middle person, who is 5 years older than the youngest. How old is the middle person?', 29, 'Let youngest=x. x+(x+5)+(x+15)=92, so x=24 and the middle person is 29.'],
  ['HARD', 'Two siblings’ ages are in the ratio 5:3 today. Eight years ago they were in the ratio 3:1. How old is the older sibling today?', 20, 'Let current ages be 5x and 3x. (5x-8)/(3x-8)=3 gives x=4, so the older sibling is 20.'],
  ['HARD', 'A mother and two children total 95 years. The mother is twice the older child’s age, and the older child is 5 years older than the younger. How old is the mother?', 50, 'Let younger=x. Older=x+5 and mother=2x+10. Their total is 4x+15=95, so x=20 and mother=50.'],
];

function scalarOptions(answer, index) {
  const candidates = [answer + 2, answer - 2, answer + 4, answer - 4, answer + 6, answer - 6, answer * 2, Math.max(1, answer / 2)]
    .filter(value => Number.isInteger(value) && value > 0 && value !== answer);
  const distractors = [];
  for (let offset = 0; distractors.length < 3 && offset < candidates.length; offset++) {
    const value = candidates[(index + offset) % candidates.length];
    if (!distractors.includes(value)) distractors.push(value);
  }
  const values = [...distractors];
  const correctIndex = index % 4;
  values.splice(correctIndex, 0, answer);
  return { options: Object.fromEntries('ABCD'.split('').map((key, i) => [key, `${values[i]} years`])), correct_option: 'ABCD'[correctIndex] };
}

function record(difficulty, question_text, options, correct_option, explanation, source) {
  return {
    subject_slug: 'maths', subcategory_slug: 'arithmetic-maths', chapter_slug: 'age',
    question_text, options, correct_option, explanation, difficulty, is_pyq: false,
    pyq_year: null, pyq_exam_name: null, source,
  };
}

const rows = pdfQuestions.map(([difficulty, question_text, options, correct_option, explanation, page]) =>
  record(difficulty, question_text, Object.fromEntries('ABCD'.split('').map((key, i) => [key, options[i]])), correct_option,
    explanation, `Verified from supplied Age PDF, page ${page}; exam/year not stated`));
for (let i = 0; i < originalQuestions.length; i++) {
  const [difficulty, question_text, answer, explanation] = originalQuestions[i];
  const picked = scalarOptions(answer, i);
  rows.push(record(difficulty, question_text, picked.options, picked.correct_option, explanation,
    'Original SSC-style practice question'));
}

const target = { EASY: 30, MEDIUM: 30, HARD: 30 };
const counts = Object.fromEntries(Object.keys(target).map(level => [level, rows.filter(row => row.difficulty === level).length]));
if (rows.length !== 90 || JSON.stringify(counts) !== JSON.stringify(target)) {
  throw new Error(`Age bank must have 30 per difficulty; got ${JSON.stringify(counts)} from ${rows.length} rows`);
}
const output = path.join(__dirname, '..', 'data', 'age_verified_batch.json');
fs.writeFileSync(output, `${JSON.stringify({ questions: rows }, null, 2)}\n`, 'utf8');
console.log(`Wrote ${rows.length} Age questions (${JSON.stringify(counts)}); PDF ${pdfQuestions.length}, original ${originalQuestions.length}`);
