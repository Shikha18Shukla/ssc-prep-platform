"""Build the reviewed original SSC Average question batch."""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "data" / "average_verified_batch.json"

# Stem, correct numeric answer, concise derivation. Independent verification
# expressions are maintained in backend/tests/test_average_verified_batch.py.
ROWS = [
 ("EASY", "The average of five numbers is 24. Four of them sum to 100. Find the fifth number.", 20, "The total is 5×24=120; the missing number is 120−100=20."),
 ("EASY", "The average of eight numbers is 35. What ninth number must be included to make the average 38?", 62, "The totals must rise from 8×35=280 to 9×38=342, requiring 62."),
 ("EASY", "The average age of six people is 32 years. A 25-year-old joins them. What is the new average age?", 31, "Their total age becomes 6×32+25=217; 217/7=31 years."),
 ("EASY", "The average weight of 30 parcels is 40 kg. A parcel weighing 160 kg is replaced by one weighing 40 kg. Find the new average weight.", 36, "Total weight falls by 120 kg: (30×40−160+40)/30=36 kg."),
 ("EASY", "Find the average of the first 20 positive integers.", 10.5, "The mean of an arithmetic sequence is (first+last)/2=(1+20)/2=10.5."),
 ("EASY", "The average of 12, 17, 19 and x is 18. Find x.", 24, "The four numbers total 72; x=72−12−17−19=24."),
 ("EASY", "Thirty students have an average score of 60 and twenty students have an average score of 75. Find the average score of all 50 students.", 66, "Combined mean=(30×60+20×75)/50=66."),
 ("EASY", "Twelve workers earn an average of ₹500 per day. What must a thirteenth worker earn for the group average to be ₹520?", 760, "Required total is 13×520=6760; the new worker earns 6760−12×500=760."),
 ("EASY", "A student averages 68 marks in five tests. What score in the sixth test will raise the average to 70?", 80, "The required six-test total is 420; the first five total 340, leaving 80."),
 ("EASY", "Find the average of all integers from 18 through 26, inclusive.", 22, "For consecutive terms, mean=(18+26)/2=22."),
 ("EASY", "Find the average of the seven consecutive odd numbers 31, 33, 35, 37, 39, 41 and 43.", 37, "The middle term of seven equally spaced values is their mean: 37."),
 ("EASY", "Two numbers have an average of 56 and differ by 18. Find the larger number.", 65, "Their sum is 112; the larger is (112+18)/2=65."),
 ("EASY", "A shop's average sales over four days are ₹250 per day. On the fifth day it sells ₹320. What is the five-day daily average?", 264, "Total sales are 4×250+320=1320; average=264."),
 ("EASY", "The average of 11, 14, 18, 21 and x is 17. Find x.", 21, "The required total is 85; the four known values total 64, so x=21."),
 ("EASY", "The average weight of 12 players is 64 kg. A 72 kg player is replaced by a 60 kg player. What is the new average weight?", 63, "The total falls by 12 kg, so the mean falls by 12/12=1 kg to 63."),
 ("EASY", "Two groups each contain 30 students. Their average marks are 68 and 76. Find the combined average.", 72, "Equal-sized groups have mean (68+76)/2=72."),
 ("EASY", "The average of four numbers is 32. A fifth number, 42, is added. Find the new average.", 34, "The original total is 128; (128+42)/5=34."),
 ("EASY", "Nine observations have an average of 45. After removing one observation, the remaining average is 43. Find the removed observation.", 61, "The totals are 405 and 8×43=344; the removed value is 61."),
 ("EASY", "Eight boys have an average age of 14 years. Two boys aged 12 and 20 join them. Find the new average age.", 14.4, "The new total is 8×14+12+20=144; 144/10=14.4 years."),
 ("EASY", "Find the average of the multiples of 6 from 6 to 60, inclusive.", 33, "The sequence is arithmetic, so its mean is (6+60)/2=33."),
 ("EASY", "A batter's average after five innings is 36 runs. After scoring 60 in the sixth innings, what is the new average?", 40, "The total becomes 5×36+60=240; 240/6=40."),
 ("EASY", "The average of 20 numbers is 12. If 3 is added to every number, what is the new average?", 15, "Adding the same amount to every observation raises the mean by 3."),
 ("EASY", "A family of four has an average age of 20 years. The father is 44. What is the average age of the other three members?", 12, "The other members' total is 4×20−44=36; their mean is 12."),
 ("EASY", "A factory makes an average of 120 units per day for five days and 150 units on the sixth day. Find the six-day daily average.", 125, "Total production is 600+150=750; 750/6=125."),
 ("EASY", "The average of 15 observations is 28. A further observation of 48 is included. Find the new average.", 29.25, "The new total is 15×28+48=468; 468/16=29.25."),
 ("EASY", "The average of three numbers is 30. Two of them sum to 62. Find the third number.", 28, "The total is 90; the third number is 90−62=28."),
 ("EASY", "Find the average of five consecutive multiples of 4 whose smallest value is 32.", 40, "The values are 32, 36, 40, 44 and 48; their mean is the middle value, 40."),
 ("EASY", "Two kinds of grain are mixed: 2 kg costs ₹100 per kg and 3 kg costs ₹120 per kg. Find the average cost per kg.", 112, "Total cost is 200+360=560 for 5 kg; the mean cost is ₹112/kg."),
 ("EASY", "Six values have an average of 25. If the value 13 is removed, what is the average of the remaining five?", 27.4, "The remaining total is 150−13=137; 137/5=27.4."),
 ("EASY", "A worker's average output over seven days is 52 units. The average for the first six days is 50 units. Find the seventh day's output.", 64, "Seven-day total is 364; the first six total 300, so the last day is 64."),

 ("MEDIUM", "A class of 36 students averages 68 marks. A 92-mark student is replaced by another student, and the class average becomes 67. Find the replacement student's mark.", 56, "The class total falls by 36 marks, so the replacement scored 92−36=56."),
 ("MEDIUM", "The average age of a family of five is 24 years. A newborn joins the family. What is the new average age?", 20, "The total remains 120 years; 120/6=20."),
 ("MEDIUM", "In a group, 24 students average 72 marks and 16 students average 63 marks. Find the combined average.", 68.4, "Combined total=1728+1008=2736; 2736/40=68.4."),
 ("MEDIUM", "A student averages 70 in six tests. What must the seventh-test score be to make the seven-test average 72?", 84, "Required total=504; the first six total 420, leaving 84."),
 ("MEDIUM", "Ten numbers average 50. One number, 59, is removed. Find the average of the remaining numbers.", 49, "Remaining total=500−59=441; 441/9=49."),
 ("MEDIUM", "A group of 32 workers produces an average of 68 units per shift. Including a trainee's output brings the 33-person average to 67 units. How many units did the trainee produce?", 35, "The group total is 32×68=2176; the new total is 33×67=2211; the trainee produced 35 units."),
 ("MEDIUM", "A team of 11 players has an average age of 26 years. A 35-year-old player leaves and a new player joins; the team's average age becomes 25 years. Find the new player's age.", 24, "The total decreases by 11 years, hence new age=35−11=24."),
 ("MEDIUM", "A student scores an average of 78 in 5 papers. If the first four papers total 296 marks, what did the student score in the fifth paper?", 94, "Five-paper total=390; fifth score=390−296=94."),
 ("MEDIUM", "A shop's average daily revenue for 8 days is ₹4,250. If the first 7 days brought in ₹28,700, find the eighth day's revenue.", 5300, "Eight-day total=34,000; eighth day=34,000−28,700=5,300."),
 ("MEDIUM", "Find the mean of the 12 consecutive even integers from 14 through 36.", 25, "There are 12 terms; mean=(14+36)/2=25."),
 ("MEDIUM", "A batter's average after 9 innings is 42. In the tenth innings the batter scores 78. Find the new average.", 45.6, "New total=9×42+78=456; divide by 10 to get 45.6."),
 ("MEDIUM", "A class average is 64 for 40 pupils. The 10 pupils who scored the lowest average 44 leave. Find the average of the remaining pupils to two decimal places.", 70.6666666667, "Original total=2,560; departing total=440; 2,120/30=70 2/3=70.67 to two decimal places."),
 ("MEDIUM", "The average age of 15 employees is 32 years. A 47-year-old employee is replaced by a new employee, and the average falls to 31 years. Find the new employee's age.", 32, "The total falls by 15 years; new employee=47−15=32."),
 ("MEDIUM", "A student has an average of 68 marks in 8 subjects. After a recheck, one mark is raised from 52 to 76. What is the corrected average?", 71, "The total rises by 24 marks; the mean rises by 24/8=3 to 71."),
 ("MEDIUM", "The average of 7 consecutive integers is 46. What is the product of the smallest and largest integers?", 2107, "The middle is 46; endpoints are 43 and 49, whose product is 2,107."),
 ("MEDIUM", "A vehicle travels for equal durations at 40, 50 and 60 km/h. What is its average speed over these three stages?", 50, "For equal time intervals, average speed is the arithmetic mean: (40+50+60)/3=50 km/h."),
 ("MEDIUM", "A worker's average production over 12 days is 84 units. In the first 5 days the average was 78. Find the average for the remaining 7 days to two decimal places.", 88.2857142857, "Total=1,008; first five=390; remaining=618; mean=618/7=88.29 to two decimal places."),
 ("MEDIUM", "The average of 9 measurements is 36. One measurement was recorded as 18 instead of 45. Find the corrected average.", 39, "Correcting the total adds 27; the mean rises by 27/9=3 to 39."),
 ("MEDIUM", "A group of 20 adults averages 42 years. Five adults averaging 52 years join them. Find the new average age.", 44, "Combined mean=(20×42+5×52)/25=44."),
 ("MEDIUM", "A player averages 35 runs over 12 innings. What score in the thirteenth innings gives an overall average of 38?", 74, "Required total=13×38=494; prior total=420; score=74."),
 ("MEDIUM", "The average of six numbers is 24. If one number is doubled, the average becomes 28. Find the original number.", 24, "The total rises by 6×4=24; doubling one value added that value, so it was 24."),
 ("MEDIUM", "A company has 40 employees with an average salary of ₹32,000. Eight employees with an average salary of ₹42,000 leave. Find the average salary of those remaining, in thousands of rupees.", 29.5, "Initial payroll=₹1,280,000; leavers' payroll=₹336,000; remaining mean=₹944,000/32=₹29,500."),
 ("MEDIUM", "The average of the first 15 positive odd integers is what value?", 15, "The first and last odd numbers are 1 and 29; their mean is 15."),
 ("MEDIUM", "A team of 9 has an average score of 72. If the captain's score is excluded, the other 8 average 69. Find the captain's score.", 96, "Team total=648; other players total=552; captain scored 96."),
 ("MEDIUM", "A family of six has an average age of 27 years. The average age of the parents is 48 years. Find the average age of the four children.", 16.5, "Family total=162; parents total=96; children's mean=66/4=16.5."),
 ("MEDIUM", "A retailer's average sales over 10 days are ₹1,800. Sales during the first 9 days average ₹1,720. Find sales on day 10.", 2520, "Ten-day total=18,000; first nine=15,480; last day=2,520."),
 ("MEDIUM", "The mean of 8 numbers is 31. If each of the first 5 numbers is increased by 4 and each of the remaining 3 is decreased by 2, find the new mean.", 32.75, "The sum changes by 5×4−3×2=14; the mean rises by 14/8=1.75 to 32.75."),
 ("MEDIUM", "Two sections contain 25 and 35 students. Their average scores are 72 and 68 respectively. By how many marks does the combined total exceed 4,000?", 180, "Combined total=25×72+35×68=4,180; it exceeds 4,000 by 180."),
 ("MEDIUM", "The mean of 5 consecutive multiples of 7 is 42. Find the largest of the five numbers.", 56, "The middle multiple is 42; the largest is two steps higher: 42+14=56."),
 ("MEDIUM", "A student averages 66 marks after 8 papers. If the average across all 10 papers must be 70, what average is needed across the final two papers?", 86, "The first eight total 528; the ten-paper target is 700. The last two total 172, so their mean must be 86."),

 ("HARD", "In an office of 20 employees, the average age is 35 years. Six employees averaging 25 years transfer out, and four new employees averaging 30 years join. Find the new average age to two decimal places.", 670/18, "Starting sum=700; subtract 150 and add 120 to get 670 across 18 people, or 335/9=37.22 years to two decimal places."),
 ("HARD", "A batter's average after 20 innings is 48. The next three scores are 72, 84 and 96. What score in the 24th innings is needed for an overall average of 52?", 36, "Target total=1,248; after 23 innings the total is 960+72+84+96=1,212; the required score is 36."),
 ("HARD", "A class of 40 students averages 65 marks. The top 5 average 91 and the bottom 5 average 39. Find the average of the remaining 30 students.", 65, "Whole total=2600; top and bottom total=455+195=650; remaining mean=1950/30=65."),
 ("HARD", "The average age of 8 family members is 29 years. A 44-year-old member leaves, twins aged 2 join, and one year passes. Find the new average age to two decimal places.", 67/3, "After departure and the twins' arrival, total age is 232−44+4=192 for 9 people. A year later it is 201; mean=67/3=22.33."),
 ("HARD", "A student averages 72 in 10 tests. The average of the first 6 is 68 and that of the last 5 is 78. What was the score on the sixth test?", 78, "Total=720; first six=408; last five=390. Their overlap is test 6: 408+390−720=78."),
 ("HARD", "A company has 30 workers averaging 36 units of output. Twelve workers averaging 42 units move to another shift; 8 workers averaging 32 units join. Find the new average output of the 26 workers.", 32, "Total=1,080−504+256=832 across 26 workers; new mean=32 units."),
 ("HARD", "The average of 11 numbers is 50. The average of the first 6 is 49 and of the last 6 is 52. Find the sixth number.", 56, "Total=550; sums of overlapping groups are 294 and 312; overlap=294+312−550=56."),
 ("HARD", "A train of 12 coaches averages 54 passengers. Six coaches average 48 passengers and the remaining six average 60. Two coaches, one from each group, are exchanged. If the new first group average is 52, find the difference in passenger counts between the exchanged coaches.", 24, "First group initially totals 288. New total=312, so the incoming coach exceeds outgoing by 24 passengers."),
 ("HARD", "A candidate averages 76 marks in 8 papers. The average of the first 5 papers is 72 and the average of the last 4 papers is 82. Find the mark in the fifth paper.", 80, "All-paper total=608; first five total=360; last four=328; shared fifth paper=360+328−608=80."),
 ("HARD", "The average of 15 numbers is 40. The average of the first 8 is 35 and the average of the last 8 is 46. Find the eighth number.", 48, "Total=600; first sum=280 and last sum=368; shared eighth value=280+368−600=48."),
 ("HARD", "A firm has 50 employees averaging 34 years of age. Ten employees averaging 46 retire; 6 replacements averaging 28 join. What is the new average age to two decimal places?", 1408/46, "Total age=1,700−460+168=1,408 for 46 employees; mean=704/23=30.61 years."),
 ("HARD", "A player averages 40 runs in 15 innings. In innings 16–20 the player scores 80, 0, 70, 0 and 60. What average across innings 21–25 is needed to make the 25-innings average 42?", 48, "Target total=1,050; first 20 innings total 600+210=810. The next five need 240 runs, or an average of 48."),
 ("HARD", "Averages of groups A and B are 72 and 64, and their sizes are in the ratio 3:5. When 8 people move from B to A, both groups have equal size and their combined average remains 67. Find the original size of group A.", 24, "Let sizes be 3k,5k. Equal sizes after move imply 3k+8=5k−8, so k=8 and A=24."),
 ("HARD", "The mean of 9 consecutive integers is 42. A tenth integer is added and the mean becomes 44. Find the added integer.", 62, "Original total=9×42=378; new total=440; added value=62."),
 ("HARD", "A student averages 80 in 6 subjects. The average in the first 3 is 76 and in the last 4 is 83. Find the score in the third subject.", 80, "Total=480; first-three total=228, last-four total=332; shared score=228+332−480=80."),
 ("HARD", "The average weight of 18 boxes is 24 kg. The 6 heaviest average 31 kg, and the 5 lightest average 17 kg. Find the average weight of the remaining 7 boxes.", 23, "Total=432; extreme groups total 186+85=271, leaving 161 kg among 7 boxes; mean=23 kg."),
 ("HARD", "The average of 12 values is 25. The average of the first 7 is 22 and the average of the last 7 is 29. Find the seventh value.", 57, "Total=300; first seven=154 and last seven=203; shared seventh value=154+203−300=57."),
 ("HARD", "A 20-player squad averages 26 years. The 4 oldest average 38 and the 3 youngest average 19. These seven players are replaced by seven averaging 24. Find the squad's new average age.", 23.95, "The departing seven total 4×38+3×19=209; replacements total 168. New squad total=520−209+168=479; mean=23.95."),
 ("HARD", "A candidate's average in 12 tests is 64. The average in the first 7 is 60 and in the last 6 is 70. Find the seventh test score.", 72, "Total=768; first seven and last six each total 420; shared seventh score=420+420−768=72."),
 ("HARD", "A workshop has 16 machines averaging 25 units per hour. Ten machines average 22 units per hour. Find the average output of the remaining six machines.", 30, "Total=400; the ten make 220, leaving 180 for six machines; mean=30."),
 ("HARD", "The average of 25 numbers is 48. The average of the first 13 is 44 and of the last 13 is 53. Find the 13th number.", 61, "Total=1,200; first thirteen=572 and last thirteen=689; shared value=572+689−1,200=61."),
 ("HARD", "A household spends an average of ₹42,000 per month over a year. The first four months average ₹38,000 and the next five average ₹40,000. Find the total spent in the final three months.", 152000, "Annual total=₹504,000; first nine months total ₹352,000; final three months total ₹152,000."),
 ("HARD", "A class averages 68 across 45 pupils. Five absent pupils are included in this average; when they are excluded, the remaining 40 average 66. Find the absent pupils' average marks.", 84, "Original total=3,060; present pupils total=2,640; absent total=420, so their average is 84."),
 ("HARD", "An athlete scores an average of 24 points over 18 games. The first 10 games average 21 points. If the last 10 average 28, how many points were scored in games 9 and 10 combined?", 58, "Total=432; first ten=210 and last ten=280; overlap games 9–10 total 210+280−432=58."),
 ("HARD", "The average of 20 measurements is 35. Two values were entered as 48 and 62 instead of 84 and 26. Find the corrected average.", 35, "Correcting the total changes it by (84+26)−(48+62)=0; mean remains 35."),
 ("HARD", "A group of 30 adults averages 42 years. Six adults averaging 50 leave, and four adults averaging 33 join. Find the new average age.", 39, "Total age=1,260−300+132=1,092 across 28 adults; mean=39."),
 ("HARD", "A student averages 74 marks in 9 papers. The first 5 average 70 and the last 5 average 80. Find the fifth paper's mark.", 84, "Overall total=666; first five=350; last five=400; shared fifth mark=350+400−666=84."),
 ("HARD", "A club has 40 members averaging 29 years. Eight members averaging 24 leave. How many new members averaging 35 must join for the new club average to be 31?", 6, "After departures the total is 1,160−192=968 across 32. Solve (968+35n)/(32+n)=31 to get n=6."),
 ("HARD", "Three examination sections contain 20, 30 and 50 candidates with average marks 62, 68 and 74. Find the combined average mark.", 69.8, "Weighted total=1,240+2,040+3,700=6,980 across 100 candidates; mean=69.8."),
 ("HARD", "A factory's daily outputs during four equal five-day weeks average 42, 48, 54 and 60 units per day. Find the average daily output over all 20 days.", 51, "Each week has equal weight, so mean=(42+48+54+60)/4=51."),
]

def build():
    assert len(ROWS) == 90, f"expected 90 rows, got {len(ROWS)}"
    questions=[]
    for i,(difficulty,stem,answer,explanation) in enumerate(ROWS):
        offsets=(-11,7,-3) if isinstance(answer,int) else (-2.5,1.25,-0.75)
        distractors=[answer+offset for offset in offsets]
        options=[answer,*distractors]
        shift=(i*3+1)%4
        options=options[shift:]+options[:shift]
        display=lambda value: f"{value:.2f}" if isinstance(value, float) else str(value)
        questions.append({
            "subject_slug":"maths","subcategory_slug":"arithmetic-maths",
            "chapter_slug":"average","question_text":stem,
            "options":dict(zip("ABCD",map(display,options))),
            "correct_option":"ABCD"[options.index(answer)],
            "explanation":explanation,"difficulty":difficulty,"is_pyq":False,
            "source":"Original SSC-style practice question",
        })
    OUT.write_text(json.dumps({"questions":questions},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

if __name__ == "__main__": build()
