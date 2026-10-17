"""Build the reviewed Statistics batch and independently checkable calculation ledger."""
from __future__ import annotations

import json
import random
import re
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
LEVELS = ("EASY", "MEDIUM", "HARD")
ORIGINAL = "Original SSC-style practice question"


def fmt(n):
    return str(int(n)) if float(n).is_integer() else f"{n:.2f}".rstrip("0").rstrip(".")


def q(level, stem, answer, proof, source=ORIGINAL, distractors=None):
    answer = fmt(answer) if isinstance(answer, (int, float)) else str(answer)
    if distractors is None:
        n = float(answer)
        delta = 1 if n.is_integer() else 0.5
        distractors = [fmt(n + delta), fmt(n - delta), fmt(n + 2 * delta)]
    values = [answer]
    for candidate in map(str, distractors):
        if candidate not in values:
            values.append(candidate)
    n = float(answer) if re.fullmatch(r"-?\d+(?:\.\d+)?", answer) else None
    delta = 1 if n is not None and n.is_integer() else .5
    for candidate in ([fmt(n+delta), fmt(n-delta), fmt(n+2*delta), fmt(n-2*delta)] if n is not None else []):
        if candidate not in values:
            values.append(candidate)
    if len(values) != 4:
        if len(values) < 4:
            raise ValueError(f"Need four distinct answer choices for {stem!r}: {values}")
        values = values[:4]
    random.Random(len(ROWS) * 19 + len(stem)).shuffle(values)
    key = "ABCD"[values.index(answer)]
    ROWS.append({"subject_slug":"maths", "subcategory_slug":"advanced-maths", "chapter_slug":"statistics",
                 "question_text":stem, "options":dict(zip("ABCD", values)), "correct_option":key,
                 "explanation":proof, "difficulty":level, "is_pyq":False, "pyq_year":None,
                 "pyq_exam_name":None, "source":source})
    LEDGER.append({"row":len(ROWS), "question":stem, "difficulty":level, "expected_answer":answer,
                   "independent_calculation":proof})


ROWS, LEDGER = [], []

# EASY: direct calculations and interpretation.
q("EASY", "Find the arithmetic mean of 18, 24, 31, 37 and 40.", 30, "Sum = 150; mean = 150/5 = 30.")
q("EASY", "The mean of 7 observations is 16. What is their total?", 112, "Total = mean × number of observations = 16 × 7 = 112.")
q("EASY", "The average of 6 numbers is 14. Five are 9, 11, 13, 15 and 18. Find the sixth.", 18, "Required total = 6×14=84; known total=66; missing value=84−66=18.")
q("EASY", "Find the median of 4, 9, 12, 17 and 25.", 12, "The ordered list has five values; the third value is 12.")
q("EASY", "Find the median of 6, 10, 14, 18, 22 and 30.", 16, "For six ordered values, median=(14+18)/2=16.")
q("EASY", "The mean of 5 observations is 12. If one observation 8 is removed, what is the mean of the remaining observations?", 13, "Original total=5×12=60; remaining total=60−8=52; mean=52/4=13.")
q("EASY", "Find the mode of 3, 5, 5, 7, 8, 5, 9 and 7.", 5, "5 occurs three times, more often than any other value.")
q("EASY", "A set of values has frequencies: 2 occurs 3 times, 4 occurs 5 times, and 6 occurs twice. What is the mode?", 4, "The largest frequency is 5, attached to value 4.")
q("EASY", "Find the range of 13, 19, 22, 28 and 35.", 22, "Range = maximum − minimum = 35−13=22.")
q("EASY", "The class interval is 30–40. What is its class mark?", 35, "Class mark=(30+40)/2=35.")
q("EASY", "A frequency table has frequencies 4, 7, 6 and 3. How many observations are there?", 20, "Total frequency=4+7+6+3=20.")
q("EASY", "For values 1, 2 and 3 with frequencies 2, 5 and 3, find the arithmetic mean.", 2.1, "Weighted sum=1×2+2×5+3×3=21; total frequency=10; mean=2.1.", distractors=["1.9","2.2","2.1"])
q("EASY", "The cumulative frequency up to a class is 17, and the preceding cumulative frequency is 11. What is the frequency of that class?", 6, "Class frequency is the difference of successive cumulative frequencies: 17−11=6.")
q("EASY", "A group's marks are 40, 50 and 60, with frequencies 2, 3 and 5. Find the mean mark.", 53, "Weighted total=80+150+300=530; total frequency=10; mean=53.")
q("EASY", "Find the median of 2, 4, 4, 6, 7, 9 and 11.", 6, "The fourth of seven ordered observations is 6.")
q("EASY", "Find the mode of 12, 15, 17, 15, 19, 15 and 20.", 15, "15 appears three times; each other value appears once.")
q("EASY", "A data set has minimum 8 and maximum 41. Find its range.", 33, "Range=41−8=33.")
q("EASY", "What is the class mark of the interval 45–55?", 50, "Midpoint=(45+55)/2=50.")
q("EASY", "The frequencies in five classes are 3, 8, 10, 6 and 3. Find the total frequency.", 30, "3+8+10+6+3=30.")
q("EASY", "For x=2, 4, 6 with frequencies 1, 2, 3, find the mean.", "14/3", "Weighted total=2+8+18=28; N=6; mean=28/6=14/3.", distractors=["4","16/3","5"])
q("EASY", "An observation occurs in class 20–30. Using the exclusive continuous convention, what is the class width?", 10, "Width=upper boundary−lower boundary=30−20=10.")
q("EASY", "The total frequency is 25. If the cumulative frequency before the last class is 19, what is the last class frequency?", 6, "Last frequency=25−19=6.")
q("EASY", "Find the median of 11, 14, 18, 23 and 31.", 18, "The central (third) ordered observation is 18.")
q("EASY", "Find the mean of 12, 16, 20 and 24.", 18, "Sum=72; mean=72/4=18.")
q("EASY", "The mean of 8 values is 21. Their sum is increased by 16 without changing the number of values. By how much does the mean increase?", 2, "Change in mean=change in total/N=16/8=2.")
q("EASY", "The values 1, 2 and 3 have frequencies 5, 2 and 4. Which value is the mode?", 1, "Value 1 occurs 5 times, more than 2 (twice) or 3 (four times).", distractors=["2","3","1"])
q("EASY", "If every observation in a data set is increased by 7, by how much does its mean increase?", 7, "Adding a constant to every observation adds that constant to the mean.")
q("EASY", "If every observation is multiplied by 3, how does the range change?", "3 times", "For a positive scale factor, both maximum and minimum triple, so the range triples.", distractors=["Unchanged","9 times","3 units"])
q("EASY", "A frequency distribution contains 9 observations below 20 and 12 observations from 20 to below 30. What is the cumulative frequency below 30?", 21, "Cumulative count=9+12=21.")
q("EASY", "Find the median of 5, 8, 12, 15, 19, 21, 28 and 32.", 17, "For eight values, median=(15+19)/2=17.")

# MEDIUM: combined, weighted and frequency-based multi-step calculations.
q("MEDIUM", "The mean of 12 numbers is 18. If 24 is replaced by 36, what is the new mean?", 19, "The total rises by 12; mean rises by 12/12=1, giving 19.")
q("MEDIUM", "A class of 20 students has mean score 64 and another class of 30 has mean 70. Find the combined mean.", 67.6, "Combined total=20×64+30×70=3380; N=50; mean=67.6.")
q("MEDIUM", "A worker earns ₹500 per day for 12 days and ₹650 per day for 8 days. What is the average daily earning over all 20 days?", 560, "Total=12×500+8×650=11200; divide by 20 to obtain 560.")
q("MEDIUM", "The mean of 9 observations is 14. The mean of the first 5 is 12. Find the mean of the remaining 4.", 16.5, "All total=126; first-five total=60; remaining total=66; 66/4=16.5.")
q("MEDIUM", "Find the median of 3, 7, 8, 12, 14, 19, 23, 26 and 31.", 14, "There are nine values; the fifth is 14.")
q("MEDIUM", "In a distribution, values 10, 20, 30 and 40 have frequencies 3, 5, f and 2. If the total frequency is 16, find f.", 6, "f=16−(3+5+2)=6.")
q("MEDIUM", "For values 10, 20 and 30 with frequencies 4, 5 and 1, respectively, find the mean.", 17, "Weighted sum=40+100+30=170; total frequency=10; mean=17.")
q("MEDIUM", "The grouped classes 0–10, 10–20, 20–30 have frequencies 2, 5, 3. Using class marks, find the estimated mean.", 16, "Midpoints 5,15,25; weighted sum=10+75+75=160; N=10; mean=16.")
q("MEDIUM", "For classes 10–20, 20–30, 30–40 the frequencies are 4, 9, 7. What is the median class?", "20–30", "N=20, so N/2=10; cumulative frequencies are 4,13,20, placing the 10th value in 20–30.", distractors=["10–20","30–40","0–10"])
q("MEDIUM", "A grouped distribution has classes 0–10, 10–20, 20–30 with frequencies 5, 9, 6. Estimate its median using continuous class boundaries.", 15.56, "Median class 10–20; L=10, cf=5, f=9, h=10, N=20; median=10+((10−5)/9)×10=15.56.", distractors=["16.67","17.5","15.56"])
q("MEDIUM", "A data set has mean 25 and median 27. Using the empirical relation, estimate its mode.", 31, "Mode≈3×median−2×mean=81−50=31.")
q("MEDIUM", "For observations 4, 7, 10, 13, 16, find the population variance.", 18, "Mean=10; squared deviations sum=36+9+0+9+36=90; population variance=90/5=18.")
q("MEDIUM", "For the population 2, 4, 6, 8, find the standard deviation.", "√5", "Mean=5; squared deviations sum=9+1+1+9=20; population variance=20/4=5; SD=√5.", distractors=["2","√6","√3"])
q("MEDIUM", "Set A has minimum 12 and maximum 48; set B has minimum 5 and maximum 39. Which has the larger range, and by how much?", "Set A by 2", "Range A=36; range B=34; A's range is larger by 2.", distractors=["Set B by 2","Set A by 4","Set B by 4"])
q("MEDIUM", "Five consecutive even integers have mean 28. What is the largest integer?", 32, "For an arithmetic sequence the mean is its middle term, 28; the largest is 28+4=32.")
q("MEDIUM", "The mean of 10 values is 22. One value was recorded as 34 instead of 24. Find the corrected mean.", 21, "Corrected total=220−34+24=210; corrected mean=210/10=21.")
q("MEDIUM", "A discrete distribution has x=1,2,3,4 and frequencies 2,4,3,1. Find the median.", 2, "N=10; the 5th and 6th ordered observations are both 2, so median=2.")
q("MEDIUM", "In a grouped table, cumulative frequencies at the end of successive classes are 7, 18, 26 and 30. Find the frequency of the third class.", 8, "Third-class frequency=26−18=8.")
q("MEDIUM", "For classes 0–10, 10–20, 20–30 with frequencies 3, 8, 5, what is the estimated mean using class marks?", 16.25, "Weighted total=5×3+15×8+25×5=260; N=16; mean=16.25.")
q("MEDIUM", "The mean of 15 observations is 20. If six observations with mean 17 are removed, find the mean of the remaining observations.", 22, "Original total=300; removed total=102; remaining total=198; 198/9=22.")
q("MEDIUM", "A frequency table has classes 0–5, 5–10, 10–15 with frequencies 6, 9, 5. Find the cumulative frequency through the second class.", 15, "6+9=15.")
q("MEDIUM", "If each value x is transformed to 2x+3, and the original mean is 11, what is the new mean?", 25, "Mean transforms linearly: 2×11+3=25.")
q("MEDIUM", "A data set of 8 values has mean 15. Seven values sum to 101. What is the eighth value?", 19, "Total=8×15=120; missing value=120−101=19.")
q("MEDIUM", "For values 5, 10, 15, 20 with frequencies 1, 2, 4, 3, find the mode.", 15, "Largest frequency is 4, corresponding to value 15.")
q("MEDIUM", "For the population 1, 3, 5, 7, find the variance.", 5, "Mean=4; squared deviations sum=9+1+1+9=20; variance=20/4=5.")
q("MEDIUM", "The average of 40 readings is 52. One reading 72 is replaced by 32. Find the new average.", 51, "Total decreases by 40; mean decreases by 40/40=1; new mean=51.")
q("MEDIUM", "A grouped table has total frequency 30. Between which two ordered observations does its median lie?", "15th and 16th", "For an even total N=30, the median is the average of observations N/2=15 and N/2+1=16.", distractors=["14th and 15th","16th and 17th","15th alone"])
q("MEDIUM", "A survey records 12, 15, 18, 21, 24 with frequencies 2, 3, 4, 3, 2. Find the mean.", 18, "Symmetry about 18 gives mean 18; directly weighted total=252 over N=14.")
q("MEDIUM", "A grouped distribution has modal class 20–30, previous frequency 6, modal frequency 12 and next frequency 8. Using the grouped mode formula, estimate the mode.", 26, "L=20, h=10, f1=12, f0=6, f2=8; mode=20+((12−6)/(24−6−8))×10=26.")
q("MEDIUM", "For the ordered observations 2, 4, 6, 8, 10, 12, 14, 16, find the interquartile range using the median-of-halves convention.", 8, "Lower-half median Q1=(4+6)/2=5; upper-half median Q3=(12+14)/2=13; IQR=13−5=8.")

# HARD: multiple linked statistics, missing frequencies, comparisons and grouped measures.
q("HARD", "A data set has 20 observations with mean 18. The mean of the first 8 is 15 and of the next 7 is 20. Find the mean of the final 5.", 20, "Total=360; first 8 sum=120; next 7 sum=140; final sum=100; final mean=20.", distractors=["21","19","20"])
q("HARD", "The mean of 12 values is 25. Replacing x by 31 raises the mean to 26. Find x.", 19, "Total rises by 12; replacement adds 31−x=12, hence x=19.")
q("HARD", "A group of 18 observations has mean 40, and a second group has mean 45. If the combined mean is 42.5, how many observations are in the second group?", 18, "Let the second-group size be x: (18×40+45x)/(18+x)=42.5; 720+45x=765+42.5x; x=18.")
q("HARD", "A frequency distribution has values 1, 2, 3, 4 with frequencies 3, 5, f, 2. If the mean is 2.5, find f.", 8, "(3+10+3f+8)/(10+f)=2.5; 21+3f=25+2.5f; f=8.")
q("HARD", "The values 10, 20, 30, 40 have frequencies 3, f, 5, 2. If the mean is 25, find f.", 2, "(30+20f+150+80)/(10+f)=25; 260+20f=250+25f; f=2.")
q("HARD", "In a grouped distribution, classes 0–10, 10–20, 20–30, 30–40 have frequencies 5, 9, 12, 4. Estimate the median.", 20.83, "N=30; cumulative frequency before the median class 20–30 is 14; L=20, f=12, h=10; median=20+((15−14)/12)×10=20.83.", distractors=["21.11","22.5","20.83"])
q("HARD", "For classes 0–10, 10–20, 20–30, frequencies are 4, 9, 7. Estimate the median by interpolation.", 16.67, "N=20; median class 10–20; L=10, cf=4,f=9,h=10; median=10+(10−4)/9×10=16.67.")
q("HARD", "A grouped distribution has modal class 30–40; adjacent frequencies are 7 and 5, and modal frequency is 13. Estimate its mode.", 34.29, "Mode=30+((13−7)/(2×13−7−5))×10=30+6/14×10=34.29.", distractors=["35.71","36","34.29"])
q("HARD", "For a grouped distribution, modal class is 40–50 with previous, modal and next frequencies 8, 14 and 10. Find the estimated mode.", 46, "Mode=40+((14−8)/(28−8−10))×10=40+6/10×10=46.", distractors=["44","45","46"])
q("HARD", "A data set has mean 32 and median 35. Using the empirical relation, estimate the mode.", 41, "Mode≈3×35−2×32=105−64=41.")
q("HARD", "For the population 2, 4, 6, 8, 10, calculate the standard deviation.", 2.83, "Mean=6; squared deviations total=40; population variance=8; SD=√8≈2.83.", distractors=["2.83","3.16","4"])
q("HARD", "For the population 1, 2, 3, 4, 5, 6, find the variance.", 2.92, "Mean=3.5; squared deviations sum=17.5; divide by 6 gives 35/12≈2.92.", distractors=["2.92","3.5","17.5"])
q("HARD", "Set A consists of 4, 6, 8, 10, 12. Set B consists of 2, 6, 8, 10, 14. Which set has the larger population variance and by how much?", "Set B by 8", "Both means are 8. A squared-deviation sum=40, variance=8; B sum=80, variance=16; difference=8. The larger set is B.", distractors=["Set A by 8","Set B by 4","Set A by 4"])
q("HARD", "The mean of 25 values is 16. If one value is omitted, the mean of the remaining 24 is 15.5. Find the omitted value.", 28, "Original total=400; remaining total=24×15.5=372; omitted value=28.")
q("HARD", "The mean of 40 observations is 50. Two observations 35 and 65 were mistakenly recorded as 53 and 56. Find the corrected mean.", 49.775, "Incorrect total=2000; subtract erroneous 53+56 and add 35+65 gives 1991; corrected mean=1991/40=49.775.")
q("HARD", "Values 10, 20, 30, 40 have frequencies 2, 3, x, 1. If the median of all observations is 25, find x.", 4, "For median 25 the middle values are 20 and 30. Five observations are at or below 20, so the total is 10; x=10−2−3−1=4.")
q("HARD", "A grouped table has classes 0–10, 10–20, 20–30 with frequencies 4, f, 6. Its estimated mean is 16. Find f.", 10, "(5×4+15f+25×6)/(10+f)=16; 170+15f=160+16f; f=10.")
q("HARD", "A population has mean 20 and standard deviation 4. If every value is transformed to 3x−5, what is the new population variance?", 144, "Variance scales by the square of the multiplier; 3²×4²=144.")
q("HARD", "A grouped distribution has classes 0–10, 10–20, 20–30, 30–40 and frequencies 3, 7, 12, 8. Estimate the mean.", 23.33, "Midpoints 5,15,25,35; weighted sum=15+105+300+280=700; N=30; mean=23.33.", distractors=["22.5","24","23.33"])
q("HARD", "The mean of 10 values is 12 and their population variance is 9. If each value is increased by 5, what are the new mean and variance?", "17; 9", "A shift by 5 raises mean to 17 and leaves variance unchanged at 9.", distractors=["17; 14","12; 9","17; 4"])
q("HARD", "The mean of 8 observations is 14. If one observation 6 is replaced by 22 and another 18 by 10, what is the new mean?", 15, "The net total change=(22−6)+(10−18)=8; mean increases by 8/8=1 to 15.")
q("HARD", "In a grouped table, classes 0–10, 10–20, 20–30 have frequencies 6, f, 10. If the median class is 10–20 and the total number is 30, find f.", 14, "f=30−6−10=14; N/2=15, and cumulative before/mid class is 6 then 20, confirming median class.")
q("HARD", "A distribution has total frequency 40. Its first three class frequencies are 8, 11 and 9. Find the fourth frequency.", 12, "Remaining frequency=40−(8+11+9)=12.")
q("HARD", "For observations 3, 5, 7, 9, 11, find the sum of squared deviations from their mean.", 40, "Mean=7; squared deviations 16+4+0+4+16 sum to 40.")
q("HARD", "The mean of 16 observations is 24. The mean of 6 of them is 20 and of another 5 is 26. Find the mean of the remaining 5.", 26.8, "Total=384; known subtotals=120+130=250; remainder=134; mean=134/5=26.8.", distractors=["26","27.2","26.8"])
q("HARD", "For x=1,2,3,4 with frequencies 2, 4, 6, 8, find the median.", 3, "N=20; 10th and 11th values are both 3, so median=3.")
q("HARD", "A grouped distribution has classes 0–10, 10–20, 20–30, 30–40 and frequencies 5, 8, 12, 5. Using continuous boundaries, estimate the median.", 21.67, "N=30; median class 20–30, L=20, cf=13, f=12, h=10; median=20+(15−13)/12×10=21.67.", distractors=["21.25","22.5","21.67"])
q("HARD", "The mode of a moderately skewed distribution is 24 and its mean is 20. Using the empirical relation, find the median.", 21.33, "Mode≈3Median−2Mean; 24=3Median−40, so Median=64/3≈21.33.", distractors=["22","24","21.33"])
q("HARD", "Two groups have sizes 15 and 25, with means 32 and 40. Find their combined mean.", 37, "Weighted mean=(15×32+25×40)/40=(480+1000)/40=37.")
q("HARD", "Two equally sized groups each contain 4 values. Their means are 10 and 14, and each group's population variance is 1. What is the population variance of all 8 values combined?", 5, "Combined mean=12. Each group contributes within-group squared deviation 4×1=4 and between-group deviation 4×(2²)=16; combined squared deviations=40; variance=40/8=5.")

def normalized(s):
    return " ".join(unicodedata.normalize("NFKC", s).casefold().split())

def number_mask(s):
    s=normalized(s)
    return " ".join(re.sub(r"[^a-z<> ]", " ", re.sub(r"\d[\d,]*(?:\.\d+)?%?", " <n> ", s)).split())

def main():
    if len(ROWS) != 90 or Counter(x["difficulty"] for x in ROWS) != {"EASY":30,"MEDIUM":30,"HARD":30}:
        raise SystemExit(f"bad batch size/levels {len(ROWS)} {Counter(x['difficulty'] for x in ROWS)}")
    for i, row in enumerate(ROWS):
        if len(row["options"]) != 4 or len(set(row["options"].values())) != 4 or row["options"][row["correct_option"]] != LEDGER[i]["expected_answer"]:
            raise SystemExit(f"bad options/key at row {i+1}")
        for other in ROWS[:i]:
            if normalized(row["question_text"]) == normalized(other["question_text"]):
                raise SystemExit(f"duplicate stems at row {i+1}: {row['question_text']}")
            if SequenceMatcher(None, normalized(row["question_text"]), normalized(other["question_text"])).ratio() >= .97:
                raise SystemExit(f"near-identical stems at row {i+1}: {row['question_text']}")
    (BASE / "data" / "statistics_verified_batch.json").write_text(json.dumps({"questions":ROWS},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (BASE / "data" / "statistics_answer_ledger.json").write_text(json.dumps(LEDGER,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("Wrote",len(ROWS),"Statistics questions; counts",dict(Counter(x["difficulty"] for x in ROWS)))

if __name__ == "__main__": main()
