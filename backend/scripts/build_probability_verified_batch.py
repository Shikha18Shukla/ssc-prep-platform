"""Build the reviewed Probability batch and its outcome-count answer ledger."""
from __future__ import annotations

import json
import random
import re
import unicodedata
from collections import Counter
from fractions import Fraction
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
LEVELS = ("EASY", "MEDIUM", "HARD")
ORIGINAL = "Original SSC-style practice question"

# A ledger entry records the equally likely outcomes counted during solution.
# Supplied-PDF questions are transcribed/adapted from the slides; no exam/year
# is printed for an individual item, so they are ordinary questions, not PYQs.
SPECS = {
"EASY": [
 ("Two fair coins are tossed together. What is the probability of getting at most one head?",3,4,"The outcomes are HH, HT, TH, TT; three have at most one head.","Probability 1 PDF, slide 7; exam/year not stated"),
 ("A fair six-sided die is rolled once. What is the probability of an odd result?",3,6,"The odd faces are 1, 3, and 5: 3 of 6.",ORIGINAL),
 ("One number is selected uniformly from 1 to 12. What is the probability that it is a prime?",5,12,"The primes are 2, 3, 5, 7, and 11: 5 of 12.",ORIGINAL),
 ("A fair die is rolled. What is the chance that its score exceeds 4?",2,6,"Only 5 and 6 qualify: 2 of 6.",ORIGINAL),
 ("A standard die is thrown once. Find the probability of rolling a multiple of 3.",2,6,"The qualifying faces are 3 and 6: 2 of 6.",ORIGINAL),
 ("A card is selected at random from a standard 52-card deck. Find the probability it is a heart.",13,52,"There are 13 hearts among 52 cards.",ORIGINAL),
 ("One card is drawn from a 52-card pack. What is the probability of drawing a face card?",12,52,"There are 3 face ranks in each of 4 suits, giving 12 of 52.","Probability 2 PDF, slide 11; exam/year not stated"),
 ("A single card is taken from a shuffled standard deck. What is the probability that it is a red king?",2,52,"The king of hearts and king of diamonds are the 2 red kings among 52.","Probability 2 PDF, slide 12; exam/year not stated"),
 ("A playing card is picked blindly from a full deck. What is the probability of a red card?",26,52,"The 2 red suits contain 26 cards in total.","Probability 2 PDF, slide 10; exam/year not stated"),
 ("An integer from 1 through 15 is chosen at random. What is the probability it is divisible by 3?",5,15,"The qualifying values are 3, 6, 9, 12, and 15: 5 of 15.",ORIGINAL),
 ("One of the integers 1 to 20 is selected. What is the probability it is divisible by 5?",4,20,"The multiples are 5, 10, 15, and 20: 4 of 20.",ORIGINAL),
 ("A letter is chosen uniformly from the word MATHS. What is the probability of choosing its only vowel?",1,5,"MATHS has five letters and only A is a vowel.",ORIGINAL),
 ("A day of the week is selected at random. What is the probability its name begins with S?",2,7,"Saturday and Sunday qualify: 2 of 7 days.",ORIGINAL),
 ("A month is chosen uniformly from a calendar year. What is the probability it has 31 days?",7,12,"Seven of the twelve months have 31 days.",ORIGINAL),
 ("A spinner has 10 equal sectors, of which 4 are blue. What is the probability it stops on blue?",4,10,"Four of ten equally likely sectors are blue.",ORIGINAL),
 ("A pouch contains 5 red, 3 blue, and 2 yellow counters. One is drawn. Find the probability it is blue.",3,10,"There are 3 blue counters out of 10 total.",ORIGINAL),
 ("A decimal digit is selected uniformly from 0 through 9. What is the probability it is less than 4?",4,10,"Digits 0, 1, 2, and 3 qualify: 4 of 10.",ORIGINAL),
 ("A box holds 8 green marbles and 2 white marbles. One marble is drawn. Find the probability of green.",8,10,"Eight of the ten marbles are green.",ORIGINAL),
 ("Two fair coins are tossed. What is the probability of getting exactly one head?",2,4,"HT and TH qualify among HH, HT, TH, TT: 2 of 4.",ORIGINAL),
 ("Three fair coins are tossed. What is the probability that all three show tails?",1,8,"There are 2^3 = 8 equiprobable sequences and only TTT qualifies.",ORIGINAL),
 ("A fair die is rolled. What is the probability that the result is not 6?",5,6,"Five of the six faces are not 6.",ORIGINAL),
 ("Among the 36 ordered outcomes when a pair of dice is rolled, what fraction produces a total score of seven?",6,36,"The six ordered pairs are (1,6), (2,5), (3,4), (4,3), (5,2), and (6,1), out of 36.",ORIGINAL),
 ("A card is drawn from a standard deck. What is the probability it is a diamond?",13,52,"One of four suits is diamonds, so 13 of 52 cards qualify.",ORIGINAL),
 ("An integer from 1 to 12 is selected. Find the probability that it is a perfect square.",3,12,"The square values are 1, 4, and 9: 3 of 12.",ORIGINAL),
 ("A number from 1 to 30 is chosen uniformly. What is the probability it is divisible by 2 or 3?",20,30,"There are 15 multiples of 2, 10 of 3, and 5 of both; 15+10-5=20.",ORIGINAL),
 ("A two-digit integer is selected uniformly from 10 to 99. What is the probability its units digit is zero?",9,90,"The qualifying numbers are 10, 20, ..., 90: 9 of 90.",ORIGINAL),
 ("A carton has 3 defective and 9 working bulbs. If one is selected at random, what is the probability it works?",9,12,"Nine of the twelve bulbs work.",ORIGINAL),
 ("A fair six-sided die is rolled. What is the probability of getting a number less than 3?",2,6,"Only 1 and 2 qualify: 2 of 6.",ORIGINAL),
 ("One card is drawn from a standard deck. What is the probability it is the ace of spades?",1,52,"Exactly one of the 52 cards is the ace of spades.",ORIGINAL),
 ("A jar contains 7 red and 7 blue beads. One bead is drawn. Find the probability of blue.",7,14,"Seven of the fourteen beads are blue.",ORIGINAL),
],
"MEDIUM": [
 ("A coin is tossed three times. What is the probability that heads and tails alternate on every toss?",2,8,"Only HTH and THT alternate; they are 2 of the 8 equally likely sequences.","Probability 1 PDF, slide 9; exam/year not stated"),
 ("A die is rolled twice and the sum is known to be 10. Given this, what is the probability that at least one roll is 5?",1,3,"The ordered outcomes with sum 10 are (4,6), (5,5), (6,4); only one includes a 5.","Probability 1 PDF, slide 15; exam/year not stated"),
 ("Two fair dice are thrown. What is the probability that their sum is 5?",4,36,"The ordered pairs (1,4), (2,3), (3,2), (4,1) are 4 of 36.","Probability 1 PDF, slide 16; exam/year not stated"),
 ("A fair die is rolled twice. Given that the first score is even, what is the probability that the sum is 8?",3,18,"There are 3 qualifying ordered pairs (2,6), (4,4), (6,2) among 18 outcomes with an even first score.",ORIGINAL),
 ("A fair die shows a number greater than 2. What is the conditional probability that the number is even?",2,4,"Given {3,4,5,6}, two of the four possible faces are even.",ORIGINAL),
 ("Two counters are drawn without replacement from 5 red and 4 blue counters. Find the probability both are red.",10,36,"There are C(5,2)=10 red pairs among C(9,2)=36 pairs.",ORIGINAL),
 ("Two cards are drawn without replacement from a standard deck. What is the probability both are hearts?",78,1326,"There are C(13,2)=78 heart pairs among C(52,2)=1326 pairs.",ORIGINAL),
 ("A bag has 4 green and 6 orange balls. Two balls are drawn with replacement. What is the probability both are green?",16,100,"Replacement keeps the green chance at 4/10 each draw; (4/10)^2=16/100.",ORIGINAL),
 ("A box has 4 red and 6 white tokens. Two are drawn without replacement. What is the probability of one of each colour?",48,90,"There are 4×6×2=48 ordered mixed-colour pairs among 10×9=90 ordered pairs.",ORIGINAL),
 ("Two cards are dealt one after another without replacement. Find the probability that at least one is an ace.",198,1326,"Of C(52,2)=1326 pairs, 1326-C(48,2)=198 contain at least one ace.",ORIGINAL),
 ("Three unbiased coins are tossed. What is the probability of getting at most two heads?",7,8,"There are 8 equally likely sequences; only HHH has more than two heads, so 7 qualify.","Probability 1 PDF, slide 10; exam/year not stated"),
 ("Three fair dice are rolled. Find the probability their total is 4.",3,216,"The only ordered triples are permutations of (1,1,2), giving 3 of 6^3=216.",ORIGINAL),
 ("A card is selected from a standard deck. What is the probability it is a face card or a heart?",22,52,"There are 12 face cards and 13 hearts, with 3 overlap cards; 12+13-3=22.",ORIGINAL),
 ("An integer from 1 to 30 is chosen, given that it is even. What is the probability it is also divisible by 3?",5,15,"There are 15 even integers and 5 divisible by 6, so the conditional chance is 5/15.",ORIGINAL),
 ("A bag has 3 red and 3 blue balls. Given that the first ball drawn without replacement is red, what is the probability the second is red?",2,5,"After a red first draw, 2 red remain among 5 balls.",ORIGINAL),
 ("A box contains 3 red and 2 blue balls. Two are drawn without replacement. Find the probability of one red and one blue.",12,20,"There are 3×2×2=12 ordered mixed pairs among 5×4=20.",ORIGINAL),
 ("A box is selected at random: box A has 2 red and 3 blue balls; box B has 4 red and 1 blue. What is the chance of drawing red?",6,10,"Each box has probability 1/2; average the red chances: (2/5+4/5)/2=6/10.",ORIGINAL),
 ("A container has 3 white and 2 black beads. Two beads are drawn without replacement. What is the probability of white first, then black?",6,20,"The ordered chance is (3/5)(2/4)=6/20.",ORIGINAL),
 ("Two fair dice are rolled. Given that the sum is even, what is the probability that both scores are even?",9,18,"An even sum occurs in 18 pairs; 3×3=9 of these have both scores even.",ORIGINAL),
 ("A three-digit number is chosen uniformly from 100 through 999. What is the probability it is divisible by 5?",180,900,"There are 180 multiples of 5 among the 900 three-digit integers.",ORIGINAL),
 ("A raffle has 6 winning and 8 losing tickets. Two tickets are drawn without replacement. What is the probability of at least one winner?",63,91,"Out of C(14,2)=91 pairs, subtract C(8,2)=28 all-losing pairs: 63.",ORIGINAL),
 ("Ten components include 4 faulty and 6 sound parts. Two are selected without replacement. Find the probability exactly one is faulty.",24,45,"Choose one faulty and one sound: 4×6=24; total pairs C(10,2)=45.",ORIGINAL),
 ("Two distinct chips are drawn from 1 to 8. What is the probability their sum is even?",12,28,"An even sum means both odd or both even: C(4,2)+C(4,2)=12 of C(8,2)=28.",ORIGINAL),
 ("A family with three children is selected from equally likely boy/girl outcomes. What is the probability of at least two girls?",4,8,"GGG, GGB, GBG, and BGG qualify: 4 of 8.",ORIGINAL),
 ("A fair coin is tossed four times. Find the probability of exactly one head.",4,16,"Choose the position of the sole head in C(4,1)=4 ways among 2^4=16 outcomes.",ORIGINAL),
 ("A card drawn from a standard deck is known to be a face card. What is the probability it is a king?",4,12,"There are 4 kings among the 12 face cards.",ORIGINAL),
 ("A fair die is rolled. Find the probability the result is divisible by 2 or by 3.",4,6,"The union is {2,3,4,6}: 4 of 6 faces qualify.",ORIGINAL),
 ("A pouch holds 4 red, 3 blue, and 2 green marbles. Two are drawn with replacement. What is the probability they have different colours?",52,81,"Same-colour probability is (16+9+4)/81=29/81; different colours have probability 52/81.",ORIGINAL),
 ("Two fair dice are rolled. What is the probability that the scores are equal?",6,36,"The six doubles are (1,1) through (6,6), among 36 pairs.",ORIGINAL),
 ("A two-digit number is picked uniformly from 10 to 99. What is the probability that its digits sum to 9?",9,90,"The qualifying numbers are 18, 27, 36, 45, 54, 63, 72, 81, and 90: 9 of 90.",ORIGINAL),
],
"HARD": [
 ("Three cards are drawn from a 52-card deck. What is the probability exactly two are aces?",288,22100,"Choose 2 of 4 aces and 1 of 48 others: C(4,2)C(48,1)=288; total C(52,3)=22100.",ORIGINAL),
 ("Three balls are selected from an urn containing 5 red and 4 blue balls. Find the probability at least two are red.",50,84,"Favourable sets are C(5,2)C(4,1)+C(5,3)=40+10=50; total C(9,3)=84.",ORIGINAL),
 ("Four cards are drawn from a standard deck. Find the probability that exactly one is a heart.",13* (39*38*37//6),270725,"Choose 1 of 13 hearts and 3 of 39 non-hearts; divide by C(52,4)=270725.",ORIGINAL),
 ("Three fair dice are rolled. What is the probability that their scores add to 10?",27,216,"There are 27 ordered triples from 1..6 with sum 10 (by direct enumeration), out of 216.",ORIGINAL),
 ("Four fair coins are tossed. Find the probability of exactly two heads and exactly two tails.",6,16,"Choose which 2 of 4 tosses are heads: C(4,2)=6 of 16 sequences.",ORIGINAL),
 ("Two fair dice are rolled. Find the probability their product is divisible by 6.",15,36,"For first-die scores 1 through 6, the numbers of compatible second scores are 1, 2, 3, 2, 1, and 6; 15 of 36 pairs qualify.",ORIGINAL),
 ("A bag has 6 red and 5 blue balls. Three are selected without replacement. What is the probability of exactly two red?",75,165,"Choose 2 red and 1 blue: C(6,2)C(5,1)=75; total C(11,3)=165.",ORIGINAL),
 ("Given that a card from a standard deck is black, what is the probability it is a face card?",6,26,"There are 26 black cards, including 6 black Jacks, Queens, and Kings.",ORIGINAL),
 ("Box A has 3 red and 2 white balls; box B has 1 red and 4 white. A box is chosen at random and a red ball appears. What is the probability box A was chosen?",3,4,"P(A and red)=3/10; P(B and red)=1/10; conditional probability is (3/10)/(4/10)=3/4.",ORIGINAL),
 ("A 5-digit code is formed by choosing five distinct digits from 0..9 in order. What is the probability its first digit is 0?",1,10,"There are 10 equally frequent choices for the first digit; one is 0 (equivalently 9P4/10P5=1/10).",ORIGINAL),
 ("Two cards are drawn without replacement. Given the first is a queen, what is the probability the second is also a queen?",3,51,"After one queen is removed, 3 queens remain among 51 cards.",ORIGINAL),
 ("A committee of 3 is chosen from 5 women and 4 men. Find the probability it contains at least 2 women.",50,84,"Favourable committees: C(5,2)C(4,1)+C(5,3)=40+10=50; all committees C(9,3)=84.",ORIGINAL),
 ("Two numbers are drawn from 1..10 without replacement. What is the probability their product is odd?",10,45,"Both must be odd: C(5,2)=10 favourable pairs of C(10,2)=45.",ORIGINAL),
 ("A fair die is rolled four times. Find the probability of exactly one 6.",500,1296,"Choose the 6 position in 4 ways; remaining rolls have 5 choices each: 4·5^3=500 of 6^4=1296.",ORIGINAL),
 ("A drawer has 4 black and 6 white socks. Three are drawn without replacement. What is the probability all are the same colour?",24,120,"All black or all white: C(4,3)+C(6,3)=4+20=24 of C(10,3)=120.",ORIGINAL),
 ("Two dice are rolled. Given at least one die shows 4, what is the probability the sum is 9?",2,11,"There are 11 ordered pairs with at least one 4; (4,5) and (5,4) sum to 9.",ORIGINAL),
 ("A 52-card deck is dealt 2 cards. Find the probability of one ace and one king.",16,1326,"Choose an ace and king in 4×4=16 ways among C(52,2)=1326 pairs.",ORIGINAL),
 ("A box contains 4 red, 5 blue, and 3 yellow balls. Three are drawn without replacement. What is the probability all three colours appear?",60,220,"Choose one of each: 4×5×3=60; total C(12,3)=220.",ORIGINAL),
 ("Three fair dice are rolled. What is the probability exactly one die shows 6 and the total is 10?",9,216,"The other two scores must sum to 4: (1,3), (2,2), or (3,1). Choose the position of the 6 in 3 ways, giving 9 of 216 triples.",ORIGINAL),
 ("A random integer from 1 to 100 is chosen. What is the probability it is divisible by 4 or 6 but not both?",25,100,"There are 25 multiples of 4, 16 of 6, and 8 of both. Exactly one condition holds in (25-8)+(16-8)=25 of 100 cases.",ORIGINAL),
 ("Two cards are selected from 5 red and 7 black cards. What is the probability both are the same colour?",31,66,"Same colour pairs are C(5,2)+C(7,2)=10+21=31 among C(12,2)=66.",ORIGINAL),
 ("A fair coin is tossed until the first head appears, with at most 4 tosses. Given a head appears, what is the probability it first appears on toss 3?",2,15,"Conditioning excludes TTTT. First head on toss 3 is TTH: probability 1/8; any head by toss 4 has probability 15/16; ratio is 2/15.",ORIGINAL),
 ("A two-digit number is formed from distinct digits selected from 1..9. What is the probability it is divisible by 5?",1,9,"The units digit must be 5; the tens digit then has 8 choices. Of 9×8=72 numbers, 8 qualify.",ORIGINAL),
 ("A bag contains 4 red and 6 blue counters. Three are drawn without replacement. Given at least one is red, what is the probability exactly one is red?",60,100,"Exactly one red: C(4,1)C(6,2)=60. At least one red: C(10,3)-C(6,3)=120-20=100.",ORIGINAL),
 ("Two fair dice are rolled. Given their product is even, what is the probability their sum is 7?",6,27,"Product even excludes the 3×3=9 odd-odd pairs, leaving 27; all 6 sum-7 pairs have an even product.",ORIGINAL),
 ("A card is drawn, replaced, and a second card drawn. What is the probability both cards are aces or both are kings?",32,2704,"There are 4^2 ace pairs and 4^2 king pairs: 32 of 52^2=2704 ordered draws.",ORIGINAL),
 ("A class has 8 girls and 7 boys. Two students are chosen without replacement. Given at least one is a girl, what is the probability both are girls?",28,84,"Both girls: C(8,2)=28. At least one girl: C(15,2)-C(7,2)=105-21=84.",ORIGINAL),
 ("A 3-digit number is selected uniformly from 100..999. What is the probability all its digits are different?",648,900,"There are 9 choices for hundreds, 9 for tens, and 8 for units: 648 of 900 numbers.",ORIGINAL),
 ("A bag contains 5 red and 4 blue balls. Three draws are made without replacement. Given the first draw was red, what is the probability exactly one of the next two is red?",32,56,"After red first, 4 red and 4 blue remain. One red and one blue in two draws has 4·4·2=32 ordered pairs among 8·7=56.",ORIGINAL),
 ("A family is known to have two children and at least one is a girl. Assuming the four ordered boy/girl outcomes are equally likely, what is the probability both are girls?",1,3,"The eligible outcomes are GG, GB, BG; one of these three is GG.",ORIGINAL),
],
}

def norm(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())

def fmt(frac: Fraction) -> str:
    return str(frac.numerator) if frac.denominator == 1 else f"{frac.numerator}/{frac.denominator}"

def build() -> tuple[dict, list]:
    rng = random.Random(20261015)
    questions, ledger = [], []
    for level in LEVELS:
        if len(SPECS[level]) != 30:
            raise ValueError(f"{level} has {len(SPECS[level])} rows, expected 30")
        for index, (stem, favourable, total, working, source) in enumerate(SPECS[level], 1):
            if "Correction" in working:
                raise ValueError(f"Unresolved solution note: {stem}")
            answer = Fraction(favourable, total)
            if not 0 <= answer <= 1:
                raise ValueError(f"Invalid probability for {stem}: {answer}")
            distractors = []
            for candidate in (Fraction(0), Fraction(1), Fraction(1,2), Fraction(1,3), Fraction(2,3), Fraction(1,4), Fraction(3,4), Fraction(1,5), Fraction(2,5), Fraction(3,5), Fraction(4,5), Fraction(1,6), Fraction(5,6), Fraction(1,8), Fraction(3,8), Fraction(5,8), Fraction(7,8), Fraction(1,9), Fraction(2,9), Fraction(4,9), Fraction(5,9), Fraction(1,10), Fraction(3,10), Fraction(7,10), Fraction(9,10), Fraction(1,12), Fraction(5,12), Fraction(7,12), Fraction(11,12)):
                if candidate != answer and candidate not in distractors:
                    distractors.append(candidate)
                if len(distractors) == 3:
                    break
            values = [("ANSWER", answer), *[(f"D{i}", d) for i, d in enumerate(distractors, 1)]]
            rng.shuffle(values)
            correct_key = next("ABCD"[i] for i, pair in enumerate(values) if pair[0] == "ANSWER")
            options = {"ABCD"[i]: fmt(value) for i, (_, value) in enumerate(values)}
            explanation = f"{working} Therefore the probability is {favourable}/{total} = {fmt(answer)}."
            questions.append({
                "subject_slug":"maths", "subcategory_slug":"advanced-maths", "chapter_slug":"probability",
                "question_text":stem, "options":options, "correct_option":correct_key,
                "explanation":explanation, "difficulty":level, "is_pyq":False,
                "pyq_year":None, "pyq_exam_name":None, "source":source,
            })
            ledger.append({
                "row":len(ledger)+1, "difficulty":level, "favourable_outcomes":favourable,
                "total_equally_likely_outcomes":total, "expected_answer":fmt(answer),
                "independent_calculation":working, "question":stem, "source":source,
            })
    norm_stems = [norm(q["question_text"]) for q in questions]
    if len(set(norm_stems)) != 90:
        raise ValueError("Duplicate normalized stems")
    payload = {"questions":questions}
    return payload, ledger

if __name__ == "__main__":
    payload, ledger = build()
    (BASE / "data" / "probability_verified_batch.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    (BASE / "data" / "probability_answer_ledger.json").write_text(json.dumps(ledger, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print("Wrote 90 Probability questions and answer-ledger calculations")
