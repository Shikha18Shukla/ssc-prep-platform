"""Build the reviewed original Compound Interest practice batch.

All questions below are original SSC-style practice items. The supplied scanned
PDF was consulted for topic coverage only; no PYQ provenance is claimed.
"""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "data" / "compound_interest_verified_batch.json"
REFERENCE = "Original SSC-style practice; independently calculated; concepts checked against NCERT Class VIII Mathematics, Chapter 8: Comparing Quantities (ncert.nic.in/textbook.php?hemh1=8-14)"

# (difficulty, stem, answer, three distractors, explanation)
ROWS = [
    ("EASY", "At 10% per annum compounded annually, what is the compound interest on Rs 8,000 after 2 years?", "Rs 1,680", ["Rs 1,600", "Rs 1,620", "Rs 1,800"], "Amount = 8,000 x 1.1^2 = Rs 9,680; interest = Rs 1,680."),
    ("EASY", "A sum of Rs 12,500 is invested at 8% compound interest for 2 years. Find the amount.", "Rs 14,580", ["Rs 14,500", "Rs 14,400", "Rs 15,000"], "12,500 x (1.08)^2 = Rs 14,580."),
    ("EASY", "What principal amounts to Rs 9,261 in 3 years at 5% compound interest per annum?", "Rs 8,000", ["Rs 7,800", "Rs 8,250", "Rs 8,500"], "9,261/(1.05)^3 = 9,261/1.157625 = Rs 8,000."),
    ("EASY", "A principal becomes Rs 14,400 in 2 years at 20% annual compound interest. What was the principal?", "Rs 10,000", ["Rs 9,600", "Rs 11,000", "Rs 12,000"], "Principal = 14,400/(1.2)^2 = Rs 10,000."),
    ("EASY", "At what annual rate will Rs 6,000 become Rs 7,260 in 2 years, compounded annually?", "10%", ["8%", "9%", "12%"], "7,260/6,000 = 1.21 = (1.1)^2, so the rate is 10%."),
    ("EASY", "A deposit is Rs 6,050 at the end of year 2 under 10% annual compound interest. What was its value at the end of year 1?", "Rs 5,500", ["Rs 5,000", "Rs 5,250", "Rs 6,000"], "Reverse one year of 10% growth: 6,050/1.1 = Rs 5,500."),
    ("EASY", "The compound interest on Rs 20,000 for 1 year at 7.5% per annum is:", "Rs 1,500", ["Rs 1,250", "Rs 1,450", "Rs 1,575"], "For one annual period, interest = 20,000 x 0.075 = Rs 1,500."),
    ("EASY", "At 10% annual compound interest, what is the amount on Rs 4,000 after 3 years?", "Rs 5,324", ["Rs 5,200", "Rs 5,280", "Rs 5,400"], "4,000 x 1.1^3 = Rs 5,324."),
    ("EASY", "The amount on a sum at 10% compounded annually is Rs 12,100 after 2 years. Find the compound interest.", "Rs 2,100", ["Rs 1,900", "Rs 2,000", "Rs 2,200"], "Principal = 12,100/1.21 = Rs 10,000; CI = Rs 2,100."),
    ("EASY", "A machine worth Rs 80,000 depreciates by 10% each year. What is its value after 2 years?", "Rs 64,800", ["Rs 64,000", "Rs 66,000", "Rs 68,000"], "Value = 80,000 x 0.9^2 = Rs 64,800."),
    ("EASY", "A town has 40,000 people and grows by 5% yearly. What is its population after 2 years?", "44,100", ["44,000", "42,000", "45,000"], "40,000 x 1.05^2 = 44,100."),
    ("EASY", "For Rs 10,000 at 10% p.a., how much greater is the compound interest for 2 years than the simple interest?", "Rs 100", ["Rs 0", "Rs 50", "Rs 200"], "Two-year CI = Rs 2,100; SI = Rs 2,000; difference = Rs 100."),
    ("EASY", "Find the compound interest on Rs 16,000 for 2 years at 12.5% per annum, compounded annually.", "Rs 4,250", ["Rs 4,000", "Rs 4,125", "Rs 4,500"], "16,000 x (9/8)^2 - 16,000 = Rs 4,250."),
    ("EASY", "A sum doubles in 2 years under annual compound interest. What is the amount after 4 years as a multiple of the principal?", "4 times", ["3 times", "5 times", "8 times"], "Two-year growth factor is 2; repeating the same two-year period gives factor 2^2 = 4."),
    ("EASY", "Rs 10,000 earns 10% compound interest for 2 years, compounded half-yearly. Find the amount.", "Rs 12,155.06", ["Rs 12,100", "Rs 12,200", "Rs 12,210"], "Four half-years at 5%: 10,000 x 1.05^4 = Rs 12,155.0625."),
    ("EASY", "At 10% p.a. compounded annually, the amount on Rs 2,000 after 2 years is:", "Rs 2,420", ["Rs 2,400", "Rs 2,440", "Rs 2,500"], "2,000 x 1.1^2 = Rs 2,420."),
    ("EASY", "On a principal of Rs 8,000 at 10% annual compounding, how much of the second year's interest is interest on the first year's interest?", "Rs 80", ["Rs 40", "Rs 100", "Rs 800"], "The first-year interest is Rs 800; the second-year interest on that credited interest is 10% of Rs 800 = Rs 80."),
    ("EASY", "A sum of Rs 8,000 is invested at 25% p.a. compounded annually for 2 years. Find the compound interest.", "Rs 4,500", ["Rs 4,000", "Rs 4,250", "Rs 5,000"], "8,000 x 1.25^2 - 8,000 = Rs 4,500."),
    ("EASY", "A deposit of Rs 15,000 earns 4% compound interest annually. What is its amount after 3 years?", "Rs 16,872.96", ["Rs 16,800", "Rs 16,920", "Rs 17,000"], "15,000 x 1.04^3 = Rs 16,872.96."),
    ("EASY", "Rs 25,000 is invested at 6% p.a., compounded half-yearly. What is the amount after 1 year?", "Rs 26,522.50", ["Rs 26,500", "Rs 26,560", "Rs 26,625"], "Two periods at 3%: 25,000 x 1.03^2 = Rs 26,522.50."),
    ("EASY", "A sum of Rs 4,000 becomes Rs 4,840 in 2 years at annual compound interest. Find the rate.", "10%", ["8%", "9%", "12%"], "4,840/4,000 = 1.21; the annual factor is 1.1."),
    ("EASY", "Rs 2,500 is invested at 20% compound interest annually for 2 years. How much of the total interest represents interest on interest?", "Rs 100", ["Rs 50", "Rs 200", "Rs 500"], "Total CI is Rs 1,100; SI is Rs 1,000. The extra Rs 100 is interest on the first year's interest."),
    ("EASY", "A sum of Rs 10,000 is compounded quarterly at 8% p.a. What is the amount after 6 months?", "Rs 10,404", ["Rs 10,400", "Rs 10,408", "Rs 10,800"], "Two quarters at 2% each: 10,000 x 1.02^2 = Rs 10,404."),
    ("EASY", "An asset worth Rs 6,40,000 falls by 20% in value, then rises by 20% of its reduced value. What is its final value?", "Rs 6,14,400", ["Rs 6,40,000", "Rs 6,00,000", "Rs 6,20,000"], "6,40,000 x 0.8 x 1.2 = Rs 6,14,400; the equal percentages do not cancel."),
    ("EASY", "An investment of Rs 3,200 grows at 25% compound interest annually. Find its value after 3 years.", "Rs 6,250", ["Rs 5,800", "Rs 6,000", "Rs 6,400"], "3,200 x 1.25^3 = Rs 6,250."),
    ("EASY", "A Rs 10,000 deposit earns 10% compound interest annually. In which year does the interest for that single year first exceed Rs 1,000?", "Year 2", ["Year 1", "Year 3", "Year 4"], "Year-1 interest is Rs 1,000; year-2 interest is 10% of Rs 11,000, or Rs 1,100."),
    ("EASY", "A principal of Rs 7,500 is invested at 4% compound interest for 2 years. Find the interest.", "Rs 612", ["Rs 600", "Rs 606", "Rs 624"], "7,500 x (1.0816 - 1) = Rs 612."),
    ("EASY", "A population of 20,000 rises by 10% in one year and by 5% in the next. Find the population after two years.", "23,100", ["23,000", "23,050", "23,200"], "20,000 x 1.10 x 1.05 = 23,100."),
    ("EASY", "At 10% annual compounding, how many years does Rs 1,000 take to reach Rs 1,331?", "3 years", ["2 years", "4 years", "5 years"], "1.1^3 = 1.331, so the time is 3 years."),
    ("EASY", "At 10% annual compounding, a fund is Rs 12,100 after 2 years. What was the balance one year earlier?", "Rs 11,000", ["Rs 10,000", "Rs 10,500", "Rs 11,500"], "One year earlier balance is 12,100/1.1 = Rs 11,000."),

    ("MEDIUM", "A bank credits 8% for the first year and 10% for the second year. What is the amount on Rs 25,000 after both years?", "Rs 29,700", ["Rs 29,500", "Rs 29,650", "Rs 30,000"], "25,000 x 1.08 x 1.10 = Rs 29,700."),
    ("MEDIUM", "Find the difference between CI and SI on Rs 24,000 for 2 years at 12.5% p.a.", "Rs 375", ["Rs 300", "Rs 350", "Rs 400"], "For two years the difference is P(r/100)^2 = 24,000 x 1/64 = Rs 375."),
    ("MEDIUM", "At 10% p.a., a sum earns Rs 2,310 compound interest in 2 years. Find the principal.", "Rs 11,000", ["Rs 10,500", "Rs 12,000", "Rs 12,100"], "Two-year CI is 21% of P; P = 2,310/0.21 = Rs 11,000."),
    ("MEDIUM", "A sum is Rs 13,310 after 3 years at 10% annual compound interest. What was it after 1 year?", "Rs 11,000", ["Rs 10,000", "Rs 11,100", "Rs 12,100"], "Amount after year 1 = 13,310/(1.1)^2 = Rs 11,000."),
    ("MEDIUM", "An investor places Rs 20,000 at 10% p.a. for 1 year, then reinvests the proceeds for 1 year at 12%. Find the final amount.", "Rs 24,640", ["Rs 24,400", "Rs 24,600", "Rs 24,800"], "20,000 x 1.10 x 1.12 = Rs 24,640."),
    ("MEDIUM", "A sum becomes Rs 9,680 in 2 years at 10% p.a. compounded annually. How much compound interest does it earn in the third year?", "Rs 968", ["Rs 950", "Rs 1,000", "Rs 1,100"], "Third-year interest is 10% of Rs 9,680 = Rs 968."),
    ("MEDIUM", "A machine costing Rs 2,50,000 depreciates 15% in year one and 12% in year two. What is its value after two years?", "Rs 1,87,000", ["Rs 1,85,000", "Rs 1,87,500", "Rs 1,90,000"], "2,50,000 x 0.85 x 0.88 = Rs 1,87,000."),
    ("MEDIUM", "A sum is compounded half-yearly at 10% p.a. If the principal is Rs 16,000, what is the amount after 18 months?", "Rs 18,522", ["Rs 18,480", "Rs 18,500", "Rs 18,600"], "Three half-years at 5%: 16,000 x 1.05^3 = Rs 18,522."),
    ("MEDIUM", "At 8% p.a., compounded quarterly, find the amount on Rs 20,000 after 9 months.", "Rs 21,224.16", ["Rs 21,200", "Rs 21,216", "Rs 21,280"], "Three quarters at 2%: 20,000 x 1.02^3 = Rs 21,224.16."),
    ("MEDIUM", "An amount is Rs 14,400 after 2 years at 20% compounded annually. What was the amount at the end of year one?", "Rs 12,000", ["Rs 10,000", "Rs 11,500", "Rs 12,500"], "Reverse the second year's 20% growth: 14,400/1.2 = Rs 12,000."),
    ("MEDIUM", "A sum grows by 10% in year one, 20% in year two, then falls by 10% in year three. What is the net percentage change?", "18.8% increase", ["20% increase", "18% increase", "21.6% increase"], "Net factor = 1.1 x 1.2 x 0.9 = 1.188, an 18.8% increase."),
    ("MEDIUM", "For Rs 10,000 at 10% annual compound interest over 3 years, approximately what percentage of the total compound interest is interest on interest?", "9.37%", ["8.00%", "10.00%", "12.50%"], "Total CI is 0.331P=Rs 3,310. Interest-on-interest is CI minus the Rs 3,000 simple interest=Rs 310; 310/3,310 x 100 is about 9.37%."),
    ("MEDIUM", "A sum amounts to Rs 14,400 in 2 years and Rs 17,280 in 3 years under annual compounding. Find the rate.", "20%", ["15%", "18%", "25%"], "The third-year factor is 17,280/14,400 = 1.20, hence 20%."),
    ("MEDIUM", "At 10% compound interest, the difference between the amounts at the end of year 3 and year 2 is Rs 1,452. Find the principal.", "Rs 12,000", ["Rs 10,000", "Rs 11,000", "Rs 13,200"], "The third-year interest is 0.1 x P x 1.1^2 = 0.121P; P = Rs 12,000."),
    ("MEDIUM", "A sum of Rs 32,000 is invested at 6.25% p.a. compounded annually. Find its amount after 2 years.", "Rs 36,125", ["Rs 36,000", "Rs 36,100", "Rs 36,250"], "Rate = 1/16; amount = 32,000 x (17/16)^2 = Rs 36,125."),
    ("MEDIUM", "A city's population is 1,60,000. It rises by 12.5% and then falls by 8%. What is the resulting population?", "1,65,600", ["1,60,000", "1,62,000", "1,64,000"], "1,60,000 x 1.125 x 0.92 = 1,65,600."),
    ("MEDIUM", "A sum of Rs 40,000 is compounded half-yearly at 12% p.a. for one year. Find the compound interest.", "Rs 4,944", ["Rs 4,800", "Rs 4,900", "Rs 5,000"], "Two periods at 6%: amount = 40,000 x 1.06^2 = 44,944; CI = Rs 4,944."),
    ("MEDIUM", "An investment is compounded annually at 10%. By what percentage is the interest credited in year 3 greater than the interest credited in year 1?", "21%", ["10%", "20%", "30%"], "Year-1 interest is 0.1P; year-3 interest is 0.1P x 1.1^2; the latter is 21% greater."),
    ("MEDIUM", "A deposit of Rs 50,000 grows at 8% for 2 years, then at 5% for the next year. What is the maturity value?", "Rs 61,236", ["Rs 60,000", "Rs 61,000", "Rs 62,000"], "50,000 x 1.08^2 x 1.05 = Rs 61,236."),
    ("MEDIUM", "For a principal of Rs 10,000 at 10% p.a. for 2 years, how much greater is the amount with half-yearly compounding than with annual compounding?", "Rs 55.06", ["Rs 20", "Rs 30", "Rs 50"], "Annual amount is Rs 12,100; half-yearly amount is 10,000 x 1.05^4 = Rs 12,155.06; difference Rs 55.06."),
    ("MEDIUM", "A sum of Rs 10,000 is compounded quarterly at 12% p.a. for 6 months. Find the interest.", "Rs 609", ["Rs 600", "Rs 606", "Rs 612"], "Two quarters at 3%: 10,000 x (1.03^2 - 1) = Rs 609."),
    ("MEDIUM", "The CI on a sum for 2 years at 10% is Rs 2,100. What would the SI on the same sum, rate and period be?", "Rs 2,000", ["Rs 1,900", "Rs 2,050", "Rs 2,100"], "CI of Rs 2,100 implies P = 2,100/0.21 = Rs 10,000; SI = 20% of P = Rs 2,000."),
    ("MEDIUM", "A sum becomes 1.44 times itself in 2 years with annual compounding. Find the annual rate.", "20%", ["18%", "22%", "24%"], "√1.44 = 1.2, so the annual rate is 20%."),
    ("MEDIUM", "A laptop loses 20% of its value in the first year and 10% of its reduced value in the second. If bought for Rs 75,000, find its value after 2 years.", "Rs 54,000", ["Rs 52,500", "Rs 55,000", "Rs 60,000"], "75,000 x 0.8 x 0.9 = Rs 54,000."),
    ("MEDIUM", "At 10% p.a. compounded annually, the interest earned in the second year is Rs 1,210. Find the initial principal.", "Rs 11,000", ["Rs 10,000", "Rs 12,100", "Rs 12,000"], "Second-year interest = 0.1 x 1.1P = 0.11P; P = Rs 11,000."),
    ("MEDIUM", "Rs 24,200 is due after 2 years at 10% annual compound interest. What is its present value?", "Rs 20,000", ["Rs 18,000", "Rs 19,000", "Rs 22,000"], "Present value = 24,200/1.21 = Rs 20,000."),
    ("MEDIUM", "The compound interest on Rs 25,000 for 2 years is Rs 5,250. Find the annual rate.", "10%", ["8%", "9%", "12%"], "The amount factor is 1 + 5,250/25,000 = 1.21 = 1.1^2."),
    ("MEDIUM", "An investment of Rs 80,000 earns 5% in year one and 7.5% in year two. Find the total interest.", "Rs 10,300", ["Rs 10,000", "Rs 10,200", "Rs 10,500"], "80,000 x 1.05 x 1.075 = Rs 90,300; interest = Rs 10,300."),
    ("MEDIUM", "At 25% p.a., by how much does the 3-year compound interest exceed 3-year simple interest, expressed as a percentage of principal?", "20.3125%", ["18.75%", "25%", "31.25%"], "Three-year CI factor is 1.25^3 - 1 = 0.953125; SI is 0.75P; excess is 0.203125P."),
    ("MEDIUM", "A sum becomes Rs 12,100 in 2 years at 10% compound interest. If Rs 2,100 is withdrawn at that time and the balance is reinvested at 10% for one more year, what is the final amount?", "Rs 11,000", ["Rs 10,000", "Rs 10,500", "Rs 12,100"], "Initial principal is Rs 10,000; balance after withdrawal is Rs 10,000, which becomes Rs 11,000 after one year."),

    ("HARD", "An investor deposits Rs 30,000 at 10% for year 1, 20% for year 2, and 25% for year 3. What is the compound interest over the full term?", "Rs 19,500", ["Rs 18,000", "Rs 19,000", "Rs 20,000"], "30,000 x 1.10 x 1.20 x 1.25 = 49,500; interest = Rs 19,500."),
    ("HARD", "The difference between CI and SI on a sum for 3 years at 20% p.a. is Rs 15,360. Find the principal.", "Rs 1,20,000", ["Rs 1,00,000", "Rs 1,10,000", "Rs 1,25,000"], "Three-year CI factor excess over SI is 1.2^3 - 1 - 0.6 = 0.128; P=15,360/0.128=Rs 1,20,000."),
    ("HARD", "A sum at annual compound interest amounts to Rs 13,310 in 3 years and Rs 14,641 in 4 years. Find the principal.", "Rs 10,000", ["Rs 9,000", "Rs 11,000", "Rs 12,100"], "Year-4 factor = 14,641/13,310 = 1.1; initial principal = 13,310/1.1^3 = Rs 10,000."),
    ("HARD", "A loan of Rs 50,000 is repaid in two equal annual instalments at 10% compound interest, first payment at year-end. Find each instalment.", "Rs 28,809.52", ["Rs 27,500", "Rs 30,000", "Rs 31,000"], "50,000 = X/1.1 + X/1.21; X = 50,000/(1/1.1+1/1.21) = Rs 28,809.52."),
    ("HARD", "A sum is invested at 20% p.a. compounded annually. The interest earned in year 3 exceeds that in year 2 by Rs 1,200. Find the principal.", "Rs 25,000", ["Rs 20,000", "Rs 24,000", "Rs 30,000"], "Difference = 20% of year-2 interest = 0.2 x 0.2 x 1.2P = 0.048P; P=Rs 25,000."),
    ("HARD", "A principal becomes Rs 13,824 in 3 years when the annual rate is 20%. What would it become in 2 years at 10% on the same principal?", "Rs 9,680", ["Rs 9,000", "Rs 10,000", "Rs 10,500"], "P=13,824/1.728=8,000; alternate amount=8,000 x 1.21=Rs 9,680."),
    ("HARD", "A sum is compounded half-yearly at 16% p.a. for 1.5 years. If its final amount is Rs 15,746.40, find the principal.", "Rs 12,500", ["Rs 10,000", "Rs 12,000", "Rs 13,000"], "Three half-years at 8%: 12,500 x 1.08^3 = Rs 15,746.40."),
    ("HARD", "A sum earns Rs 2,000 interest in year 1 and Rs 2,420 in year 2 under annual compounding. What is the interest in year 4?", "Rs 3,542.82", ["Rs 2,904", "Rs 3,000", "Rs 3,200"], "Year-to-year interest ratio is 2,420/2,000=1.21, so r=21%; year-4 interest=2,000 x 1.21^3=Rs 3,542.82."),
    ("HARD", "A machine depreciates 10% in year 1, 20% in year 2, and appreciates 25% in year 3. If its initial value is Rs 2,00,000, find its final value.", "Rs 1,80,000", ["Rs 1,75,000", "Rs 1,85,000", "Rs 1,90,000"], "2,00,000 x 0.9 x 0.8 x 1.25 = Rs 1,80,000."),
    ("HARD", "The difference between CI and SI for 2 years at 20% p.a. is Rs 800. Find the principal and the 2-year amount.", "P = Rs 20,000; amount = Rs 28,800", ["P = Rs 10,000; amount = Rs 14,400", "P = Rs 20,000; amount = Rs 28,000", "P = Rs 40,000; amount = Rs 57,600"], "Difference=0.04P=800, so P=20,000; amount=20,000 x 1.44=28,800."),
    ("HARD", "An amount grows at 10% p.a. compounded annually. The interest credited in the third year is Rs 1,452. Find the amount at the end of year 4.", "Rs 17,569.20", ["Rs 16,000", "Rs 18,000", "Rs 20,000"], "Year-3 interest=0.1P(1.1)^2=1,452 gives P=12,000; year-4 amount=12,000 x 1.1^4=Rs 17,569.20."),
    ("HARD", "At annual compound interest, a sum becomes 1.331 times itself in 3 years. What is the percentage increase in its amount from year 2 to year 4?", "21%", ["10%", "20%", "33.1%"], "1.331=1.1^3; amount in year 4 relative to year 2 is 1.1^2=1.21, a 21% increase."),
    ("HARD", "Rs 24,000 is invested at 20% p.a. compounded annually for 1 year and 3 months. Find the amount, assuming simple interest for the remaining fraction of a year.", "Rs 30,240", ["Rs 30,000", "Rs 30,800", "Rs 31,200"], "After one year the amount is Rs 28,800; simple interest for 3 months at 20% on that amount is Rs 1,440, giving Rs 30,240."),
    ("HARD", "A sum is invested for 2 years. The rate is 10% for the first year; the second-year rate is such that the final amount is 1.265 times principal. Find the second-year rate.", "15%", ["12%", "14%", "16%"], "1.1 x (1+r)=1.265; 1+r=1.15, so r=15%."),
    ("HARD", "A sum at 10% compound interest becomes Rs 13,310 in 3 years. If Rs 3,310 is withdrawn then, what is the amount of the remaining balance after another 2 years at 10%?", "Rs 12,100", ["Rs 11,000", "Rs 12,000", "Rs 13,310"], "Balance after withdrawal=10,000; after 2 years=10,000 x 1.21=Rs 12,100."),
    ("HARD", "An amount P is split equally between two accounts earning 10% and 20% compound interest for 2 years. If the combined maturity value is Rs 13,250, find P.", "Rs 10,000", ["Rs 9,000", "Rs 11,000", "Rs 12,000"], "Combined factor is (1.1^2+1.2^2)/2=1.325; P=13,250/1.325=Rs 10,000."),
    ("HARD", "An investment grows by 10% in each of the first two years and 21% in the third year. What is its total percentage growth?", "46.41%", ["41%", "44.1%", "45%"], "Combined factor=1.1 x 1.1 x 1.21=1.4641; total growth=46.41%."),
    ("HARD", "At a fixed annual compound rate, the difference between the amount at the end of year 4 and year 3 is Rs 2,662. Find the principal if the rate is 10%.", "Rs 20,000", ["Rs 18,000", "Rs 22,000", "Rs 24,000"], "Difference=P x 1.1^3 x 0.1=0.1331P; P=2,662/0.1331=Rs 20,000."),
    ("HARD", "A sum of Rs 80,000 is compounded half-yearly at 10% p.a. for 2 years. How much greater is its amount than with annual compounding?", "Rs 440.50", ["Rs 100", "Rs 200", "Rs 500"], "Half-yearly factor 1.05^4=1.21550625; annual factor 1.1^2=1.21; difference=Rs 440.50."),
    ("HARD", "A sum is compounded annually at 10%. The compound interest for 3 years is Rs 3,310. Find the interest earned in year 2.", "Rs 1,100", ["Rs 1,000", "Rs 1,210", "Rs 1,331"], "CI=0.331P=3,310 gives P=10,000. Year-2 interest=1,000 x 1.1=Rs 1,100."),
    ("HARD", "A sum is compounded annually at 10% for 2 years and then at 5% for 1 year. If the final amount is Rs 12,705, find the initial principal.", "Rs 10,000", ["Rs 9,000", "Rs 11,000", "Rs 12,000"], "Combined factor=1.1^2 x 1.05=1.2705; P=12,705/1.2705=Rs 10,000."),
    ("HARD", "A sum doubles in 4 years under annual compounding. What is the ratio of the compound interest earned in year 4 to that earned in year 1?", "2^(3/4) : 1", ["2 : 1", "√2 : 1", "4 : 1"], "The annual growth factor x satisfies x^4=2. The ratio of year-4 to year-1 interest is x^3=2^(3/4)."),
    ("HARD", "A city grows at 10% annually for 2 years, then its population falls 10% the next year. If it began with 1,00,000 people, what is the final population?", "1,08,900", ["1,08,000", "1,09,000", "1,10,000"], "1,00,000 x 1.1^2 x 0.9 = 1,08,900."),
    ("HARD", "A borrower repays a Rs 1,00,000 loan in two equal annual instalments. At 10% compound interest, what total interest is paid?", "Rs 15,238.10", ["Rs 12,000", "Rs 18,000", "Rs 21,000"], "Installment X=100,000/(1/1.1+1/1.21)=Rs 57,619.05; total paid=115,238.10; interest=Rs 15,238.10."),
    ("HARD", "A sum earns 10% compound interest annually. Its amount at the end of year 3 exceeds its amount at the end of year 1 by Rs 2,310. Find the principal.", "Rs 10,000", ["Rs 9,000", "Rs 11,000", "Rs 12,100"], "P(1.1^3-1.1)=0.231P=2,310, so P=Rs 10,000."),
    ("HARD", "A sum of Rs 50,000 is invested at 8% p.a. compounded half-yearly. What is the amount after 2 years, to the nearest rupee?", "Rs 58,493", ["Rs 58,000", "Rs 58,400", "Rs 59,000"], "Four half-years at 4%: 50,000 x 1.04^4=Rs 58,492.93."),
    ("HARD", "A sum at 20% annual compound interest is Rs 14,400 after 2 years. What is the compound interest earned during the next 2 years?", "Rs 6,336", ["Rs 5,760", "Rs 6,000", "Rs 7,200"], "Next two-year interest=14,400 x (1.44-1)=Rs 6,336."),
    ("HARD", "Two equal sums are invested at 10% and 20% compound interest respectively for 3 years. Their amounts differ by Rs 15,880. Find each original sum.", "Rs 40,000", ["Rs 16,000", "Rs 20,000", "Rs 25,000"], "Difference per rupee=(1.2^3-1.1^3)=0.397; P=15,880/0.397=Rs 40,000."),
    ("HARD", "An amount is compounded quarterly at 12% p.a. If the principal is Rs 64,000, what is the amount after 1 year?", "Rs 72,070.72", ["Rs 71,680", "Rs 72,000", "Rs 72,500"], "Four quarters at 3%: 64,000 x 1.03^4=Rs 72,070.72."),
    ("HARD", "The compound interest on a sum for 2 years at 10% exceeds the simple interest by Rs 250. What would the compound interest be at the same rate for 3 years?", "Rs 8,275", ["Rs 7,500", "Rs 8,000", "Rs 8,500"], "0.01P=250 gives P=25,000; three-year CI=25,000 x (1.331-1)=Rs 8,275."),
]

def build():
    assert len(ROWS) == 90, f"Expected 90 rows, got {len(ROWS)}"
    output = []
    for i, (difficulty, stem, answer, wrong, explanation) in enumerate(ROWS):
        assert len(set([answer, *wrong])) == 4, (i, "duplicate option")
        # Rotate option order to avoid a positional answer pattern.
        options = [answer, *wrong]
        shift = (i * 3 + 1) % 4
        options = options[shift:] + options[:shift]
        labels = "ABCD"
        correct = labels[options.index(answer)]
        output.append({
            "subject_slug": "maths", "subcategory_slug": "arithmetic-maths",
            "chapter_slug": "compound-interest", "question_text": stem,
            "options": dict(zip(labels, options)), "correct_option": correct,
            "explanation": explanation, "difficulty": difficulty,
            "is_pyq": False, "source": REFERENCE,
        })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"questions": output}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(output)} questions to {OUT}")

if __name__ == "__main__":
    build()
