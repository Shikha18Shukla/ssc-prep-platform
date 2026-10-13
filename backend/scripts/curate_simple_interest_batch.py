"""Create the reviewed, original Simple Interest practice batch."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "data" / "simple_interest_verified_batch.json"
REFERENCE = "Original SSC-style practice question; independently calculated; concept reference: NCERT Class VIII Mathematics, Comparing Quantities; scope reference: SSC CGL Quantitative Aptitude syllabus"
SOURCE_REFERENCE = "Source-derived practice question; Simple Interest questions.pdf, page 1 (visible Physics Wallah branding; no exam/year attribution); answer independently recalculated; not a PYQ"

# (difficulty, stem, answer, three distractors, concise solution)
ROWS = [
    ("EASY", "For a fixed principal and duration, the simple interest at 6% per annum is Rs 240. What would the interest be at 9% per annum?", "Rs 360", ["Rs 300", "Rs 400", "Rs 480"], "With principal and time unchanged, interest is proportional to rate: 240x9/6=Rs 360."),
    ("EASY", "A principal of Rs 12,000 earns Rs 2,520 simple interest in 3 years. Find the annual rate.", "7%", ["6%", "7.5%", "8%"], "r = 2,520 x 100/(12,000 x 3) = 7%."),
    ("EASY", "What amount will Rs 18,000 yield at 6% simple interest in 4 years?", "Rs 22,320", ["Rs 21,600", "Rs 22,000", "Rs 23,040"], "Interest = 18,000 x .06 x 4 = 4,320; amount = Rs 22,320."),
    ("EASY", "For a fixed investment, lowering the annual simple-interest rate from 8% to 6% reduces one year's interest by Rs 100. Find the principal.", "Rs 5,000", ["Rs 4,000", "Rs 6,000", "Rs 8,000"], "The rate difference is 2%, so .02P=100 and P=Rs 5,000."),
    ("EASY", "Rs 5,000 earns Rs 1,500 simple interest in 5 years. What is the annual rate?", "6%", ["5%", "7%", "8%"], "r = 1,500 x 100/(5,000 x 5) = 6%."),
    ("EASY", "In how many years will Rs 12,000 earn Rs 2,880 at 8% simple interest per annum?", "3 years", ["2 years", "2.5 years", "4 years"], "t = 2,880 x 100/(12,000 x 8) = 3 years."),
    ("EASY", "A sum amounts to Rs 13,800 in 2 years at 7.5% simple interest. Find the principal.", "Rs 12,000", ["Rs 11,500", "Rs 12,500", "Rs 13,000"], "Amount factor = 1 + .075 x 2 = 1.15; principal = 13,800/1.15 = Rs 12,000."),
    ("EASY", "A sum of Rs 20,000 amounts to Rs 26,000 in 5 years at simple interest. Find the annual rate.", "6%", ["5%", "7%", "8%"], "Interest = Rs 6,000; r = 6,000 x 100/(20,000 x 5) = 6%."),
    ("EASY", "Find the simple interest on Rs 750 at 8% per annum for 2 years.", "Rs 120", ["Rs 80", "Rs 100", "Rs 150"], "SI = 750 x 8 x 2/100 = Rs 120."),
    ("EASY", "At 12.5% simple interest per annum, how long will it take a sum to triple?", "16 years", ["8 years", "12 years", "20 years"], "To triple, interest must equal 2P; t = 200/12.5 = 16 years."),
    ("EASY", "A principal doubles in 12.5 years at simple interest. Find the annual rate.", "8%", ["6%", "7.5%", "10%"], "For doubling, SI=P; r=100/12.5=8%."),
    ("EASY", "For the same principal and rate, what is the ratio of simple interest for 8 months to simple interest for 1 year?", "2:3", ["1:2", "3:2", "2:5"], "At a fixed principal and rate, simple interest is proportional to time; 8 months:12 months=2:3."),
    ("EASY", "At 6.25% simple interest, what percentage of the principal is earned as interest in 4 years?", "25%", ["20%", "24%", "30%"], "Interest/principal x 100 = 6.25 x 4 = 25%."),
    ("EASY", "Rs 12,000 is invested for 2 years at 6% simple interest. If the rate is halved and the term doubled, what is the interest?", "Rs 1,440", ["Rs 1,200", "Rs 1,600", "Rs 1,800"], "Both rate-time products are equal: 6x2=3x4=12, so SI=12,000x.06x2=Rs 1,440."),
    ("EASY", "What simple interest does Rs 9,600 earn at 7.5% per annum in 2 years?", "Rs 1,440", ["Rs 1,200", "Rs 1,400", "Rs 1,500"], "SI = 9,600 x .075 x 2 = Rs 1,440."),
    ("EASY", "Two sums are lent at the same rate and for the same time. If one principal is Rs 8,000 and the other Rs 12,000, what is the ratio of their simple interests?", "2:3", ["3:2", "1:2", "4:5"], "At a common rate and duration, interest is proportional to principal: 8,000:12,000=2:3."),
    ("EASY", "At the same simple-interest rate, Rs 15,000 earns Rs 1,800 in 2 years. How much will Rs 10,000 earn in 3 years?", "Rs 1,800", ["Rs 1,200", "Rs 1,500", "Rs 2,000"], "The first rate is 1,800 x 100/(15,000 x 2)=6%; the second interest is 10,000 x .06 x 3=Rs 1,800."),
    ("EASY", "Rs 10,000 is lent at 5% for 2 years and then at 8% for 3 years, both at simple interest. Find the total amount at the end.", "Rs 13,400", ["Rs 12,900", "Rs 13,000", "Rs 13,500"], "Interest = 10,000(.05 x 2 + .08 x 3)=Rs 3,400; amount=Rs 13,400."),
    ("EASY", "At 10% simple interest, by what percentage does a principal grow in 9 months?", "7.5%", ["5%", "8%", "10%"], "Nine months is 3/4 year, so the interest is 10%x3/4=7.5% of the principal."),
    ("EASY", "For how long must Rs 6,000 be lent at 10% simple interest to earn Rs 900?", "1.5 years", ["1 year", "1.25 years", "2 years"], "t = 900 x 100/(6,000 x 10)=1.5 years."),
    ("EASY", "At 7% simple interest, Rs 10,000 earns what interest in 5 years?", "Rs 3,500", ["Rs 3,000", "Rs 3,250", "Rs 4,000"], "SI=10,000 x .07 x 5=Rs 3,500."),
    ("EASY", "A sum amounts to Rs 9,200 after 3 years at 5% simple interest. What will the amount be after 5 years at the same rate?", "Rs 10,000", ["Rs 9,600", "Rs 9,800", "Rs 10,200"], "The 3-year amount is 1.15P=9,200, so P=8,000 and annual interest is Rs 400. The 5-year amount is 8,000+5x400=Rs 10,000."),
    ("EASY", "What is the total amount on Rs 8,000 at 10% simple interest for 2 years and 3 months?", "Rs 9,800", ["Rs 9,600", "Rs 9,750", "Rs 10,000"], "Time=2.25 years; SI=8,000 x .10 x 2.25=1,800; amount=Rs 9,800."),
    ("EASY", "A principal of Rs 6,000 earns Rs 2,100 simple interest at 7% per annum. Find the time.", "5 years", ["4 years", "4.5 years", "6 years"], "t=2,100 x 100/(6,000 x 7)=5 years."),
    ("EASY", "A sum of Rs 4,000 is invested at 5% simple interest for 3 years. What is the amount per Rs 1,000 of principal?", "Rs 1,150", ["Rs 1,050", "Rs 1,100", "Rs 1,200"], "For Rs 1,000, interest=1,000 x .05 x 3=150; amount=Rs 1,150."),
    ("EASY", "An amount of Rs 15,000 includes Rs 3,000 simple interest earned in 4 years. Find the principal.", "Rs 12,000", ["Rs 10,000", "Rs 11,000", "Rs 13,000"], "Principal=amount-interest=15,000-3,000=Rs 12,000."),
    ("EASY", "At 4% simple interest, what amount will Rs 25,000 become in 3 years?", "Rs 28,000", ["Rs 27,000", "Rs 27,500", "Rs 29,000"], "SI=25,000 x .04 x 3=3,000; amount=Rs 28,000."),
    ("EASY", "A sum earns simple interest equal to 20% of its principal in 4 years. Find the annual rate.", "5%", ["4%", "6%", "8%"], "Rate=20%/4=5% per year."),
    ("EASY", "At simple interest, Rs 18,000 earns Rs 2,700 in 2.5 years. Find the annual rate.", "6%", ["5%", "7%", "8%"], "r=2,700 x 100/(18,000 x 2.5)=6%."),
    ("EASY", "How much simple interest does Rs 40,000 earn at 3.5% per annum in 18 months?", "Rs 2,100", ["Rs 1,800", "Rs 2,000", "Rs 2,400"], "SI=40,000 x .035 x 1.5=Rs 2,100."),

    ("MEDIUM", "A sum amounts to Rs 5,600 in 3 years and Rs 6,400 in 7 years at simple interest. Find its principal.", "Rs 5,000", ["Rs 4,400", "Rs 4,800", "Rs 5,200"], "Annual interest=(6,400-5,600)/4=200; principal=5,600-3x200=Rs 5,000."),
    ("MEDIUM", "Rs 15,000 is invested at 6% simple interest for 5 years. An additional Rs 5,000 is invested at the same rate after 2 years. Find the total interest at the end of year 5.", "Rs 5,400", ["Rs 4,800", "Rs 5,000", "Rs 6,000"], "The first sum earns 15,000x.06x5=4,500; the added sum earns 5,000x.06x3=900. Total interest=Rs 5,400."),
    ("MEDIUM", "At simple interest, the amount after 5 years is 1.4 times the principal. What will the amount be after 8 years as a multiple of principal?", "1.64 times", ["1.56 times", "1.60 times", "1.72 times"], "Five-year interest is 0.4P, so annual interest is 0.08P; after 8 years amount=1.64P."),
    ("MEDIUM", "A lender charges 8% simple interest for the first 2 years and 11% for the next 3 years. Find the interest on Rs 20,000 over the full 5 years.", "Rs 9,800", ["Rs 9,200", "Rs 9,400", "Rs 10,200"], "Interest=20,000(.08x2+.11x3)=Rs 9,800."),
    ("MEDIUM", "Two equal principals are invested at 6% and 9% simple interest for 4 years. By how much do their interests differ if each principal is Rs 15,000?", "Rs 1,800", ["Rs 1,200", "Rs 1,500", "Rs 2,400"], "Difference=15,000 x (9%-6%) x 4=Rs 1,800."),
    ("MEDIUM", "Rs 10,000 earns Rs 2,400 simple interest in 3 years. At the same rate, how much will Rs 15,000 earn in 5 years?", "Rs 6,000", ["Rs 5,000", "Rs 5,500", "Rs 6,500"], "Rate=2,400/(10,000x3)=8%; new SI=15,000x.08x5=Rs 6,000."),
    ("MEDIUM", "A sum of Rs 10,000 is divided between 5% and 8% simple-interest investments. If total annual interest is Rs 680, how much was invested at 8%?", "Rs 6,000", ["Rs 4,000", "Rs 5,000", "Rs 7,000"], "Let x be at 8%; annual interest=0.08x+0.05(10,000-x)=680, so x=Rs 6,000."),
    ("MEDIUM", "A sum amounts to Rs 7,200 in 2 years and Rs 9,000 in 5 years at simple interest. What amount will it reach in 8 years?", "Rs 10,800", ["Rs 10,200", "Rs 10,500", "Rs 11,400"], "Annual interest=(9,000-7,200)/3=600; amount at year 8=9,000+3x600=Rs 10,800."),
    ("MEDIUM", "A person invests Rs 12,000 at 7% simple interest. After how many years will the amount be Rs 16,200?", "5 years", ["4 years", "4.5 years", "6 years"], "Interest=4,200; annual interest=840; time=4,200/840=5 years."),
    ("MEDIUM", "A sum lent at 6% simple interest for 4 years earns the same interest as Rs 18,000 lent at 8% for 3 years. Find the first principal.", "Rs 18,000", ["Rs 15,000", "Rs 16,000", "Rs 20,000"], "Second interest=18,000x.08x3=4,320; first P=4,320/(.06x4)=Rs 18,000."),
    ("MEDIUM", "The simple interest on a sum at 8% for 3 years is Rs 1,600 less than the interest on Rs 10,000 at 10% for 4 years. Find the first principal.", "Rs 10,000", ["Rs 9,000", "Rs 11,000", "Rs 12,000"], "Second SI=4,000; first SI=2,400; P=2,400/(.08x3)=Rs 10,000."),
    ("MEDIUM", "A sum earns Rs 1,260 simple interest in 3 years at 7%. What principal would earn Rs 2,400 in 4 years at the same rate?", "Rs 8,571.43", ["Rs 7,500", "Rs 8,000", "Rs 9,000"], "P=2,400/(.07x4)=Rs 8,571.43."),
    ("MEDIUM", "A principal is invested at 10% simple interest for 2 years, then the amount is reinvested at 5% for 3 more years. What is the final amount on Rs 10,000?", "Rs 13,800", ["Rs 12,800", "Rs 13,500", "Rs 14,000"], "First amount=12,000; next simple interest=12,000x.05x3=1,800; final=Rs 13,800."),
    ("MEDIUM", "At simple interest, a principal P is invested at 8% for 3 years. A second principal 1.5P is invested at 4% for 4 years. What is the ratio of the first interest to the second?", "1:1", ["1:2", "2:3", "3:2"], "The first interest is .24P; the second is 1.5P x .04 x 4=.24P. Thus the ratio is 1:1."),
    ("MEDIUM", "A sum at 12% simple interest yields Rs 2,160 in interest. If the rate were 9% and the time 4 years, what principal would earn that same interest?", "Rs 6,000", ["Rs 5,000", "Rs 6,500", "Rs 7,000"], "P=2,160/(.09x4)=Rs 6,000."),
    ("MEDIUM", "A sum is lent at 5% for 2 years and 7% for the next 3 years at simple interest. If total interest is Rs 4,650, find the principal.", "Rs 15,000", ["Rs 12,000", "Rs 14,000", "Rs 16,000"], "Interest factor=.31; P=4,650/.31=Rs 15,000."),
    ("MEDIUM", "At simple interest, a sum becomes Rs 11,200 after 4 years at 6%. What would Rs 15,000 become in 3 years at the same rate?", "Rs 17,700", ["Rs 16,800", "Rs 17,400", "Rs 18,000"], "First P=11,200/(1+.24)=9,032.26, but not needed; second amount=15,000(1+.18)=Rs17,700."),
    ("MEDIUM", "A person borrows Rs 24,000 at 9% simple interest and repays Rs 30,480. How long was the money borrowed?", "3 years", ["2.5 years", "3.5 years", "4 years"], "Interest=6,480; annual interest=2,160; time=3 years."),
    ("MEDIUM", "The interest on a principal at 10% for 5 years is Rs 1,600 more than the interest on Rs 8,000 at 7.5% for 4 years. Find the principal.", "Rs 8,000", ["Rs 7,000", "Rs 9,000", "Rs 10,000"], "Known SI=2,400; first SI=4,000; P=4,000/(.10x5)=Rs 8,000."),
    ("MEDIUM", "A sum of Rs 8,000 is split so that one part earns 6% and the other 10% simple interest for one year. If total interest is Rs 640, find the amount at 10%.", "Rs 4,000", ["Rs 3,000", "Rs 5,000", "Rs 6,000"], "Let x earn 10%; .10x+.06(8,000-x)=640 gives x=Rs 4,000."),
    ("MEDIUM", "At 8% simple interest, Rs 9,000 earns Rs 1,440 in 2 years. At 12%, how long will Rs 9,000 take to earn Rs 2,160?", "2 years", ["1.5 years", "2.5 years", "3 years"], "At 12%, annual interest=1,080; 2,160/1,080=2 years."),
    ("MEDIUM", "At simple interest, the amounts after 3 and 7 years differ by Rs 1,600. What is the interest earned in 10 years?", "Rs 4,000", ["Rs 3,200", "Rs 4,800", "Rs 5,000"], "Annual interest=1,600/4=400; ten-year interest=Rs 4,000."),
    ("MEDIUM", "Rs 18,000 is invested at simple interest. The rate is 2 percentage points higher for the first 3 years than for the next 2 years. If the combined interest is Rs 7,920, find the lower rate.", "7.6%", ["6.6%", "8.6%", "9.6%"], "Let lower rate=r. 18,000[(r+2)3+r2]/100=7,920; 5r+6=44; r=7.6%."),
    ("MEDIUM", "A sum is lent at 8% simple interest. Its amount after 5 years is Rs 2,400 more than its amount after 2 years. Find the principal.", "Rs 10,000", ["Rs 8,000", "Rs 9,000", "Rs 12,000"], "Difference is 3 years interest; P=2,400/(.08x3)=Rs 10,000."),
    ("MEDIUM", "At simple interest, Rs 6,000 earns Rs 1,440 in 4 years. At the same rate, what principal earns Rs 1,260 in 3 years?", "Rs 7,000", ["Rs 6,500", "Rs 7,500", "Rs 8,000"], "Rate=1,440/(6,000x4)=6%; P=1,260/(.06x3)=Rs 7,000."),
    ("MEDIUM", "A loan is repaid by two payments of Rs 5,500 at the ends of years 1 and 2. At 10% simple interest, what principal do these payments jointly represent at year 2?", "Rs 11,550", ["Rs 10,500", "Rs 11,000", "Rs 12,000"], "At year 2, first payment value=5,500x1.1=6,050; plus 5,500=Rs 11,550."),
    ("MEDIUM", "A sum is invested at 5% simple interest for 2 years and 8% for the following 3 years. If total interest is Rs 3,400, find the principal.", "Rs 10,000", ["Rs 8,000", "Rs 9,000", "Rs 12,000"], "Interest factor=.05x2+.08x3=.34; P=3,400/.34=Rs 10,000."),
    ("MEDIUM", "A person invests Rs 30,000 in two parts at 6% and 9% simple interest for equal durations. If annual interest totals Rs 2,250, how much is invested at 9%?", "Rs 15,000", ["Rs 10,000", "Rs 12,500", "Rs 20,000"], "Let x earn 9%; .09x+.06(30,000-x)=2,250 gives x=Rs 15,000."),
    ("MEDIUM", "At 7% simple interest, a principal earns Rs 2,450 in 5 years. What would the same principal earn at 10% for 3 years?", "Rs 2,100", ["Rs 1,750", "Rs 2,000", "Rs 2,250"], "P=2,450/(.07x5)=7,000; new SI=7,000x.10x3=Rs 2,100."),
    ("MEDIUM", "Two sums earn equal simple interest: the first is lent at 5% for 3 years, and the second at 8% for 2 years. If the first principal is Rs 6,400, find the second principal.", "Rs 6,000", ["Rs 5,000", "Rs 6,400", "Rs 7,500"], "Equal interest gives 6,400x.05x3=P x .08x2; P=6,000."),

    ("HARD", "A sum is invested at 5% for 3 years, 8% for the next 2 years, and 10% for the final 4 years, all at simple interest. If total interest is Rs 14,200, find the principal.", "Rs 20,000", ["Rs 18,000", "Rs 22,000", "Rs 24,000"], "Rate-time sum=5x3+8x2+10x4=71; P=14,200x100/71=Rs 20,000."),
    ("HARD", "A loan of Rs 10,000 is due after 2 years at 10% simple interest. A payment of Rs 4,000 is made at the end of year 1 and earns 10% simple interest until the due date. What balance remains due at year 2?", "Rs 7,600", ["Rs 7,000", "Rs 8,000", "Rs 8,400"], "The debt due at year 2 is 10,000x1.20=Rs 12,000. The year-1 payment is worth 4,000x1.10=Rs 4,400 at year 2, leaving Rs 7,600."),
    ("HARD", "A sum earns Rs 3,600 simple interest in 4 years. If the rate is increased by 3 percentage points for the next 2 years, the total interest over all 6 years is Rs 6,600. Find the principal.", "Rs 50,000", ["Rs 15,000", "Rs 20,000", "Rs 60,000"], "The extra 3% for 2 years adds .06P. Since the total interest rises from Rs 3,600 to Rs 6,600, .06P=3,000 and P=Rs 50,000."),
    ("HARD", "A principal is lent at 8% simple interest for 3 years. If Rs 5,000 more had been invested at 2 percentage points less for the same duration, the interest would be Rs 180 less. Find the original principal.", "Rs 18,000", ["Rs 12,000", "Rs 16,000", "Rs 20,000"], "Original SI=.24P; changed SI=.18(P+5,000). The original exceeds the changed interest by Rs 180, so .24P-.18(P+5,000)=180; .06P=1,080 and P=Rs 18,000."),
    ("HARD", "A sum is divided in the ratio 2:3 and lent at 6% and 10% simple interest respectively for 4 years. If total interest is Rs 6,720, find the original sum.", "Rs 20,000", ["Rs 18,000", "Rs 22,000", "Rs 24,000"], "Weighted rate-time factor=.4x.06x4+.6x.10x4=.336; P=6,720/.336=Rs 20,000."),
    ("HARD", "At simple interest, Rs 12,000 grows to Rs 15,000 in 5 years. At the same rate, how long will Rs 20,000 take to earn Rs 8,000?", "8 years", ["6 years", "10 years", "12 years"], "Rate=3,000/(12,000x5)=5%; time=8,000/(20,000x.05)=8 years."),
    ("HARD", "A sum is lent at 6% simple interest for 4 years. The rate is raised to 9% for the final 2 years. If total interest is Rs 8,400, find the principal.", "Rs 20,000", ["Rs 18,000", "Rs 22,000", "Rs 24,000"], "Interest factor=.06x4+.09x2=.42; P=8,400/.42=Rs 20,000."),
    ("HARD", "Two sums are invested at 7% and 9% simple interest for 5 years. The first sum is Rs 4,000 greater than the second, and their total interest is Rs 10,200. Find the smaller sum.", "Rs 11,000", ["Rs 9,000", "Rs 10,000", "Rs 12,000"], "Let smaller=x; .35(x+4,000)+.45x=10,200; .8x=8,800; x=Rs 11,000."),
    ("HARD", "What is the present value of Rs 13,000 due exactly 3 years from now if the discount rate is 10% simple interest per annum?", "Rs 10,000", ["Rs 9,500", "Rs 10,500", "Rs 11,000"], "Present value=13,000/(1+.10x3)=Rs 10,000."),
    ("HARD", "A sum amounts to Rs 9,600 after 4 years and Rs 12,000 after 10 years at simple interest. What interest will it earn in 15 years?", "Rs 6,000", ["Rs 5,400", "Rs 6,600", "Rs 7,200"], "Annual interest=2,400/6=400; 15-year SI=Rs 6,000."),
    ("HARD", "A sum is lent at 8% for the first 2 years and 12% for the next 3 years at simple interest. If the final amount is Rs 15,200, find the principal.", "Rs 10,000", ["Rs 9,000", "Rs 11,000", "Rs 12,000"], "Interest factor=.08x2+.12x3=.52; 1.52P=15,200; P=Rs 10,000."),
    ("HARD", "At simple interest, the interest for 6 years is 60% of the principal. What percentage of the amount at year 6 is the interest earned in the first 2 years?", "12.5%", ["15%", "20%", "25%"], "Annual rate=60%/6=10%; two-year interest=.20P and year-6 amount=1.60P; .20/1.60 x 100=12.5%."),
    ("HARD", "A sum is divided between 8% and 12% simple-interest accounts for 3 years. The higher-rate part is twice the lower-rate part. If total interest is Rs 8,400, find the total principal.", "Rs 26,250", ["Rs 20,000", "Rs 22,500", "Rs 27,000"], "The weighted rate is (8+2x12)/3=10.6667%; the 3-year interest factor is .32, so P=8,400/.32=Rs 26,250."),
    ("HARD", "A principal earns simple interest at 7% for 2 years and 10% for the next 3 years. Its total interest is Rs 3,900. Find the principal, to the nearest rupee.", "Rs 8,864", ["Rs 8,000", "Rs 9,500", "Rs 10,000"], "The interest factor is .07x2+.10x3=.44; P=3,900/.44=Rs 8,863.64, which rounds to Rs 8,864."),
    ("HARD", "A sum at simple interest becomes 5/4 of itself in 5 years. What fraction of the principal is its interest in the next 7 years at the same rate?", "7/20", ["1/4", "3/10", "2/5"], "Five-year interest=P/4; annual interest=P/20; seven-year interest=7P/20."),
    ("HARD", "Two investments of Rs 18,000 and Rs 24,000 earn simple interest for 3 years. The smaller earns 2 percentage points more than the larger. If total interest is Rs 6,480, find the rate on the larger investment, to the nearest 0.1%.", "4.3%", ["3.8%", "5.0%", "6.0%"], "Let the larger rate be r. Then 3[18,000(r+.02)+24,000r]=6,480, so r=5,400/126,000=.042857..., or 4.3% to the nearest 0.1%."),
    ("HARD", "A sum is lent at simple interest for 8 years. The rate for the first 3 years is 5%, and for the remaining years it is 8%. If total interest is Rs 4,200, find the principal, to the nearest rupee.", "Rs 7,636", ["Rs 7,000", "Rs 8,000", "Rs 8,500"], "The rate-time factor is .05x3+.08x5=.55; P=4,200/.55=Rs 7,636.36, which rounds to Rs 7,636."),
    ("HARD", "A lender charges simple interest at 9% for the first 4 years and 12% thereafter. If the interest for 7 years is Rs 7,200, find the principal.", "Rs 10,000", ["Rs 9,000", "Rs 11,000", "Rs 12,000"], "Rate-time factor=.09x4+.12x3=.72; P=7,200/.72=Rs 10,000."),
    ("HARD", "A sum earns simple interest equal to 40% of its principal in 5 years. What simple interest will Rs 6,000 earn at the same rate in 3 years?", "Rs 1,440", ["Rs 1,200", "Rs 1,600", "Rs 1,800"], "The annual rate is 40%/5=8%; SI=6,000x.08x3=Rs 1,440."),
    ("HARD", "A sum amounts to Rs 18,000 in 5 years at simple interest. If the rate were 3 percentage points higher, the amount would be Rs 20,700. Find the principal.", "Rs 18,000", ["Rs 15,000", "Rs 20,000", "Rs 22,500"], "Difference in interest=15% of P=2,700; P=Rs18,000."),
    ("HARD", "A sum is split into two parts. One is lent at 5% and the other at 8% simple interest for 4 years. If total interest is 26% of the original sum, what is the ratio of the part at 5% to the part at 8%?", "1:1", ["2:1", "1:2", "3:1"], "Weighted annual rate=26%/4=6.5%, the midpoint of 5% and 8%; therefore the two parts are equal."),
    ("HARD", "At 10% simple interest, a sum earns Rs 4,500 in a certain time. At 8% simple interest for 2 years less, it earns Rs 3,300. How long was the original investment?", "24 years", ["18 years", "20 years", "30 years"], "From .10Pt=4,500, Pt=45,000. Also .08P(t-2)=3,300, so 3,600-.16P=3,300 and P=1,875. Hence t=45,000/1,875=24 years."),
    ("HARD", "The simple interest on a sum for 4 years at 6% is equal to the interest on Rs 18,000 for 3 years at 8%. Find the sum.", "Rs 18,000", ["Rs 15,000", "Rs 20,000", "Rs 24,000"], "Known interest=18,000x.08x3=4,320; P=4,320/(.06x4)=Rs18,000."),
    ("HARD", "A sum is invested at simple interest for 2 years at 8%, then for 3 years at 10%. If the final amount is Rs 14,600, find the principal.", "Rs 10,000", ["Rs 9,000", "Rs 11,000", "Rs 12,000"], "Interest factor=.46; amount=1.46P; P=14,600/1.46=Rs10,000."),
    ("HARD", "At simple interest, the interest earned in 3 years is 3/10 of the principal. What is the ratio of the amount after 8 years to the amount after 2 years?", "3:2", ["4:3", "5:4", "2:1"], "Annual rate=10%; amounts are 1.8P and 1.2P; ratio=3:2."),
    ("HARD", "Two sums differ by Rs 1,000 and are lent at 8% and 10% simple interest respectively for 4 years. The larger sum is at the lower rate. If the interest difference is Rs 800, find the smaller sum.", "Rs 14,000", ["Rs 12,000", "Rs 13,000", "Rs 16,000"], "Let larger=x and smaller=x-1,000. Difference=.4(x-1,000)-.32x=800; x=15,000; smaller=Rs14,000."),
    ("HARD", "A sum earns Rs 4,500 at 7.5% simple interest. If the rate had been 2.5 percentage points lower and time 4 years longer, the interest would be unchanged. The original time was 8 years. Find the principal.", "Rs 7,500", ["Rs 6,000", "Rs 8,000", "Rs 9,000"], "For original 7.5%x8=.60P; alternative 5%(8+4)=.60P, so conditions match; P=4,500/.60=Rs7,500."),
    ("HARD", "A sum of Rs 20,000 is split between 6% and 9% simple-interest accounts. After 5 years the combined interest is Rs 7,500. How much is at 9%?", "Rs 10,000", ["Rs 8,000", "Rs 12,000", "Rs 15,000"], "Annual interest total=1,500; .06(20,000-x)+.09x=1,500 gives x=Rs10,000."),
    ("HARD", "A principal at 8% simple interest for 5 years yields Rs 2,400. If Rs 5,000 is added to the principal and the term is reduced by 2 years at 6%, what is the new interest?", "Rs 1,980", ["Rs 1,800", "Rs 2,160", "Rs 2,400"], "Original P=2,400/(.08x5)=6,000; new SI=11,000x.06x3=Rs1,980."),
    ("HARD", "At simple interest, a sum becomes 7/5 of itself in 8 years. How many years will it take to become 13/5 of itself at the same rate?", "32 years", ["24 years", "28 years", "36 years"], "Eight-year interest=2P/5; to reach 13P/5 requires interest 8P/5, four times as much, so 32 years."),
]

def build():
    assert len(ROWS) == 90, f"Expected 90 rows; found {len(ROWS)}"
    out = []
    for i, (difficulty, stem, answer, distractors, explanation) in enumerate(ROWS):
        opts = [answer, *distractors]
        assert len(set(x.strip().casefold() for x in opts)) == 4, (i + 1, "options not distinct")
        shift = (i * 3 + 1) % 4
        opts = opts[shift:] + opts[:shift]
        labels = "ABCD"
        out.append({
            "subject_slug": "maths", "subcategory_slug": "arithmetic-maths",
            "chapter_slug": "simple-interest", "question_text": stem,
            "options": dict(zip(labels, opts)), "correct_option": labels[opts.index(answer)],
            "explanation": explanation, "difficulty": difficulty, "is_pyq": False,
            "source": SOURCE_REFERENCE if stem in {
                "Find the simple interest on Rs 750 at 8% per annum for 2 years.",
            } else REFERENCE,
        })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"questions": out}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(out)} questions to {OUT}")

if __name__ == "__main__":
    build()
