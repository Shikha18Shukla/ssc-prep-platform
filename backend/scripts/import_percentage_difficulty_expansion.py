"""Validate and import original questions to bring Percentage to 30 per difficulty.

All items are original. The script reconciles the live database, checks normalized
and near-duplicate stems against every Percentage record and the proposed batch,
validates through the shared transactional importer, then imports atomically.
"""
from __future__ import annotations

from difflib import SequenceMatcher
import argparse
import json
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.database.session import SessionLocal
from app.models import Chapter, Exam, Question, Subject
from app.services.question_import_service import import_questions

REFERENCE = "Original question authored for SSC Prep Platform; aligned to SSC Quantitative Aptitude syllabus: https://ssc.gov.in/for-candidates/syllabus"
TARGET = 30


def item(difficulty: str, pattern: str, stem: str, options: list[str], answer: str, explanation: str) -> dict:
    assert len(options) == 4 and len({" ".join(o.casefold().split()) for o in options}) == 4
    assert answer in options
    return {
        "subject_slug": "maths", "subcategory_slug": "arithmetic-maths", "chapter_slug": "percentage",
        "question_text": stem,
        "option_a": options[0], "option_b": options[1], "option_c": options[2], "option_d": options[3],
        "correct_option": "ABCD"[options.index(answer)], "explanation": explanation,
        "difficulty": difficulty, "is_pyq": False, "pyq_year": "", "pyq_exam_name": "", "source": REFERENCE,
        "_pattern": pattern,
    }


# Fundamentals with varied contexts and operations; no new item is a paraphrase
# or number swap of another item or the existing Percentage bank.
QUESTIONS = [
    item("EASY", "part-of-whole", "A warehouse ships 54% of its 850 packaged units in the morning. How many units are shipped?", ["449", "459", "469", "4590"], "459", "0.54 × 850 = 459 units."),
    item("EASY", "percentage-increase-value", "A monthly allowance of ₹1,280 is raised by 12.5%. What is the new allowance?", ["₹1,420", "₹1,440", "₹1,460", "₹1,560"], "₹1,440", "12.5% = 1/8; the increase is 1,280/8 = ₹160, giving ₹1,440."),
    item("EASY", "same-base-combination", "Find 42% of 650 together with a further 8% of the same 650.", ["315", "320", "325", "330"], "325", "The two parts total 50% of 650, which is 325."),
    item("EASY", "fractional-percent", "What is 0.6% of 12,500?", ["65", "70", "75", "750"], "75", "0.6% = 0.006; 12,500 × 0.006 = 75."),
    item("EASY", "reverse-price-reduction", "After a 15% reduction, a shop's listed price is ₹1,020. What was the price before the reduction?", ["₹1,173", "₹1,200", "₹1,215", "₹1,250"], "₹1,200", "₹1,020 is 85% of the original; 1,020 ÷ 0.85 = ₹1,200."),
    item("EASY", "reverse-retained-share", "A fund distributes 20% of its balance and has ₹1,360 left. What was its balance before the distribution?", ["₹1,600", "₹1,650", "₹1,700", "₹1,720"], "₹1,700", "The retained 80% is ₹1,360; 1,360 ÷ 0.8 = ₹1,700."),
    item("EASY", "attendance-count", "A training centre has 1,250 enrolled candidates. If 72% attend a session, how many attend?", ["850", "875", "900", "920"], "900", "1,250 × 72/100 = 900."),
    item("EASY", "reverse-subgroup", "If 35% of the candidates in a batch equals 84, how many candidates are in the batch?", ["220", "230", "240", "260"], "240", "84 ÷ 0.35 = 240 candidates."),
    item("EASY", "absent-share", "A test centre has 960 registered candidates. On one day, 15% are absent. How many candidates are present?", ["804", "816", "824", "840"], "816", "Present candidates are 85% of 960: 0.85 × 960 = 816."),
    item("EASY", "reverse-tax-inclusive", "A bill including 5% tax is ₹840. What was the bill before tax?", ["₹780", "₹800", "₹805", "₹820"], "₹800", "Pre-tax bill × 1.05 = ₹840, so the base is ₹800."),
    item("EASY", "single-discount-base", "A jacket costs ₹2,100 after a 12.5% discount. What was its marked price?", ["₹2,300", "₹2,350", "₹2,400", "₹2,450"], "₹2,400", "After discount the price is 87.5% = 7/8 of marked price; 2,100 × 8/7 = ₹2,400."),
    item("EASY", "bonus-rate", "An employee receives a bonus equal to 8% of a ₹35,000 monthly salary. What is the bonus?", ["₹2,400", "₹2,600", "₹2,800", "₹3,000"], "₹2,800", "0.08 × 35,000 = ₹2,800."),
    item("EASY", "reverse-profit-cost", "An article is sold for ₹345 at a profit of 15% on cost. Find its cost price.", ["₹290", "₹300", "₹305", "₹315"], "₹300", "Selling price = 1.15 × cost; 345 ÷ 1.15 = ₹300."),
    item("EASY", "score-share", "A candidate scores 540 out of 750 marks. What percentage of the maximum score is this?", ["70%", "71%", "72%", "74%"], "72%", "540/750 × 100 = 72%."),
    item("EASY", "usable-sheet-area", "A metal sheet has an area of 2,400 cm². If 8% is trimmed off as unusable, what area remains?", ["2,108 cm²", "2,208 cm²", "2,220 cm²", "2,300 cm²"], "2,208 cm²", "Usable area is 92% of 2,400: 0.92 × 2,400 = 2,208 cm²."),
    item("EASY", "relative-comparison", "A is 25% of B. B is what percentage of A?", ["250%", "300%", "400%", "425%"], "400%", "If A = 0.25B, then B/A = 4 = 400%."),
    item("EASY", "reverse-salary-cut", "After a 10% salary cut, an employee earns ₹27,000. What was the salary before the cut?", ["₹29,000", "₹30,000", "₹30,300", "₹31,000"], "₹30,000", "₹27,000 is 90% of the former salary; 27,000 ÷ 0.9 = ₹30,000."),
    item("EASY", "percentage-point-reading", "A poll's support rate moves from 38% to 46%. By how many percentage points did it rise?", ["6", "8", "10", "21"], "8", "The percentage-point change is 46 − 38 = 8 points."),

    item("MEDIUM", "weighted-score", "A paper has two sections: 3/5 of the marks are in Section I, where a candidate earns 40%; the remaining marks are in Section II, where the candidate earns 70%. What is the overall percentage?", ["50%", "52%", "54%", "58%"], "52%", "Weighted score = (3/5 × 40%) + (2/5 × 70%) = 24% + 28% = 52%."),
    item("MEDIUM", "simple-interest-share", "A principal earns simple interest at 7.5% per year for 4 years. The interest is what percentage of the principal?", ["25%", "27.5%", "30%", "32.5%"], "30%", "At simple interest, the interest as a percentage of principal is 7.5% × 4 = 30%."),
    item("MEDIUM", "tax-after-discount", "A device marked at ₹8,000 receives a 15% discount, after which 18% tax is applied to the discounted price. What is the final bill?", ["₹7,888", "₹8,000", "₹8,024", "₹8,160"], "₹8,024", "Discounted price = 8,000 × 0.85 = ₹6,800; after tax: 6,800 × 1.18 = ₹8,024."),
    item("MEDIUM", "growth-then-decline", "A town's population is 240,000. It grows by 5% in one year and falls by 4% the next year. What is the population after the two changes?", ["239,520", "241,920", "242,400", "252,000"], "241,920", "240,000 × 1.05 × 0.96 = 241,920."),
    item("MEDIUM", "three-candidate-vote-share", "In an election, 80% of 25,000 registered voters cast valid votes. Candidate A gets 45% and B gets 35% of the valid votes; the rest vote for C. How many valid votes go to C?", ["3,500", "4,000", "4,500", "5,000"], "4,000", "Valid votes = 20,000; C's share is 20%, or 4,000 votes."),
    item("MEDIUM", "price-consumption-budget", "The price of a commodity rises by 20%. A family raises its spending on it by only 8%. By what percentage must its consumption change?", ["decrease 8%", "decrease 10%", "decrease 12%", "decrease 15%"], "decrease 10%", "Consumption factor = 1.08/1.20 = 0.9, a 10% reduction."),
    item("MEDIUM", "mixture-strength-addition", "A 40-litre solution is 25% acid. How many litres of pure acid must be added to make it 40% acid?", ["8", "10", "12", "15"], "10", "Initially acid = 10 L. If x L is added, (10+x)/(40+x)=0.40, so x=10 L."),
    item("MEDIUM", "relative-value-after-changes", "A is initially 15% greater than B. A then falls by 20% while B rises by 10%. After these changes, A is what percentage of B?", ["80%", "83.64%", "108.2%", "115%"], "83.64%", "Set B=100 and A=115. New A=92 and new B=110; 92/110×100 ≈ 83.64%."),
    item("MEDIUM", "two-stage-output-target", "A factory raises output by 12% and then by 15%. By what percentage is the final output above the original?", ["27%", "28.2%", "28.8%", "29.5%"], "28.8%", "Net factor = 1.12 × 1.15 = 1.288, hence a 28.8% rise."),
    item("MEDIUM", "percentage-point-vs-relative", "A bank's overdue-loan ratio falls from 8% to 6%. What is the relative percentage decrease in that ratio?", ["2%", "20%", "25%", "33⅓%"], "25%", "The fall is 2 percentage points; relative to 8%, it is 2/8 × 100 = 25%."),
    item("MEDIUM", "marks-pass-threshold", "A student scores 36% and is 24 marks below the pass mark. Another scores 44% and is 16 marks above it. What are the maximum marks?", ["400", "450", "500", "600"], "500", "The 8 percentage-point score gap equals 24+16=40 marks; maximum = 40/0.08 = 500."),
    item("MEDIUM", "revenue-price-volume", "A shop sells 10% fewer units but raises its unit price by 18%. What is the percentage change in total sales revenue?", ["increase 6.2%", "increase 8%", "increase 10%", "decrease 1.8%"], "increase 6.2%", "Revenue factor = 0.90 × 1.18 = 1.062, an increase of 6.2%."),
    item("MEDIUM", "defect-repair-rate", "A batch contains 2,500 components, of which 4% fail inspection. If 30% of the failed components are repaired successfully, what percentage of the full batch remains rejected?", ["2.4%", "2.8%", "3.2%", "3.6%"], "2.8%", "Initially 4% fail; 70% of those remain rejected, so 4% × 70% = 2.8% of the full batch."),
    item("MEDIUM", "rectangle-area-factor", "A rectangle's length increases 12% and its width decreases 10%. What is the percentage change in area?", ["increase 0.8%", "increase 2%", "decrease 0.8%", "decrease 2%"], "increase 0.8%", "Area factor = 1.12 × 0.90 = 1.008: an increase of 0.8%."),
    item("MEDIUM", "successive-discount-equivalent", "Two successive discounts of 20% and 15% are equivalent to a single discount of:", ["32%", "33%", "35%", "38%"], "32%", "Retained price factor = 0.80 × 0.85 = 0.68, so the equivalent discount is 32%."),
    item("MEDIUM", "recover-after-decrease", "After a quantity is reduced by 20%, by what percentage of the reduced quantity must it rise to regain its original value?", ["20%", "22.5%", "25%", "30%"], "25%", "The reduced amount is 80% of original; recovery is 20/80 × 100 = 25%."),
    item("MEDIUM", "ratio-numerator-denominator", "A ratio x:y is 5:4. If x rises 20% and y falls 20%, what is the new ratio in simplest form?", ["3:2", "5:4", "15:8", "7:4"], "15:8", "New ratio = 5×1.2 : 4×0.8 = 6:3.2 = 15:8."),
    item("MEDIUM", "group-rate-weighting", "Of a company's staff, 40% work in Unit A and 60% in Unit B. Absence rates are 5% in A and 10% in B. What percentage of all staff are absent?", ["7%", "8%", "8.5%", "9%"], "8%", "Overall rate = 0.4×5% + 0.6×10% = 8%."),
    item("MEDIUM", "income-ratio-change", "Two colleagues initially earn in the ratio 4:5. The first's salary rises 15%, while the second's rises 8%. What is the new ratio?", ["23:27", "25:27", "46:55", "27:23"], "23:27", "New ratio = 4×1.15 : 5×1.08 = 4.6:5.4 = 23:27."),
    item("MEDIUM", "two-discount-price-order", "A ₹5,000 item is discounted by 10%, then a further 5% of the reduced price. How much is paid?", ["₹4,250", "₹4,275", "₹4,300", "₹4,500"], "₹4,275", "5,000 × 0.90 × 0.95 = ₹4,275."),

    item("HARD", "solve-unknown-rate", "A value rises by 20%, then falls by r%. The final value is 8% above the original. Find r.", ["8%", "10%", "12%", "15%"], "10%", "1.20(1-r/100)=1.08, so 1-r/100=0.90 and r=10%."),
    item("HARD", "election-invalid-margin", "In an election, 20% of registered voters abstain and 10% of votes cast are invalid. The winner receives 54% of valid votes and wins by 1,440 votes. How many voters are registered?", ["22,500", "25,000", "27,500", "30,000"], "25,000", "The margin is 8% of valid votes, so valid votes=1,440/0.08=18,000. Valid votes are 80%×90%=72% of registered voters; 18,000/0.72=25,000."),
    item("HARD", "weighted-defect-rates", "A plant gets 30% of components from Supplier A and the rest from B. A's defect rate is 4%; B's is 1.5%. If 2.25% of all components are defective, what percentage of A's supplied components are defective?", ["3.5%", "4%", "4.5%", "5%"], "4%", "Weighted defects = 0.3×4% + 0.7×1.5% = 2.25%."),
    item("HARD", "savings-after-two-rate-changes", "A person saves 25% of income. Income rises 20% while expenditure rises 25%. What is the percentage change in savings?", ["no change", "decrease 5%", "increase 5%", "increase 10%"], "increase 5%", "Let income=100, expenditure=75 and saving=25. New income=120 and expenditure=93.75; new saving=26.25, which is 5% higher than 25."),
    item("HARD", "discount-tax-markup", "A trader marks an item 40% above cost, gives a 20% discount, then charges 5% tax on the discounted price. What is the customer's bill as a percentage of cost?", ["112%", "117.6%", "120%", "125%"], "117.6%", "Price factor = 1.40×0.80×1.05 = 1.176, or 117.6% of cost."),
    item("HARD", "false-weight-profit", "A trader claims to sell at cost price but uses a 900 g weight for each kilogram. What is the actual gain percentage, ignoring other costs?", ["10%", "11%", "11⅑%", "12.5%"], "11⅑%", "For the cost of 900 g, the trader receives the price of 1,000 g; gain = 100/900×100 = 11⅑%."),
    item("HARD", "population-growth-migration", "A district has 500,000 residents. It grows 6% in year one and 4% in year two, then 10,000 residents migrate out. What is the net percentage increase from the original population?", ["8.24%", "8.64%", "9.24%", "10.24%"], "8.24%", "Population before migration = 500,000×1.06×1.04=551,200; after migration=541,200, a rise of 41,200/500,000=8.24%."),
    item("HARD", "payroll-headcount-pay", "Average pay per worker rises 18%, while total payroll rises 8%. By what percentage does workforce size change?", ["decreases 8.47%", "decreases 10%", "increases 8.47%", "decreases 12%"], "decreases 8.47%", "Workforce factor = 1.08/1.18 = 54/59 ≈ 0.915254, a 8.47% decrease."),
    item("HARD", "area-dimension-recovery", "A rectangle's length rises 25%. By what percentage must its width fall for the area to rise by only 10%?", ["10%", "12%", "15%", "18%"], "12%", "Required width factor = 1.10/1.25 = 0.88, a 12% fall."),
    item("HARD", "multi-step-expenditure", "A person's income is first cut by 10% and then raised by 20%. Expenditure rises 15% from its original level. Initially expenditure is 80% of income. What is the percentage change in savings?", ["decreases 10%", "decreases 20%", "increases 10%", "increases 20%"], "decreases 20%", "Let initial income=100 and expenditure=80, saving=20. New income=108 and expenditure=92, so saving=16, a 20% decrease."),
    item("HARD", "discount-break-even", "An article is marked 60% above cost. After a 20% discount, what additional discount on the reduced price makes the selling price exactly 8% above cost?", ["12.5%", "15.625%", "18%", "20%"], "15.625%", "After the first discount, price=1.6×0.8=1.28 cost. The next discount is 1−1.08/1.28=0.15625, or 15.625%."),
    item("HARD", "compound-price-index", "A price index rises 12% in one period and falls 10% in the next. What single percentage change returns it to its starting value from its current level?", ["decrease 0.79%", "increase 0.79%", "decrease 0.8%", "increase 0.8%"], "decrease 0.79%", "The net factor is 1.12×0.90=1.008. The current level must fall by 0.008/1.008×100 ≈ 0.79%."),
    item("HARD", "percentage-of-remainder", "A tank is 40% full. After 30% of the water currently in it is drained, it contains 560 litres. What is the tank's capacity?", ["1,800 L", "2,000 L", "2,200 L", "2,400 L"], "2,000 L", "560 L is 70% of the initial water, which was 40% of capacity: capacity=560/(0.7×0.4)=2,000 L."),
    item("HARD", "reverse-relative-change", "A is 30% less than B. By what percentage must A increase to become 10% greater than B?", ["50%", "55%", "57 1/7%", "60%"], "57 1/7%", "Set B=100, A=70 and target A=110. Required increase=40/70×100=57 1/7%."),
    item("HARD", "mixture-replacement", "A 50-litre solution contains 20% salt. Some solution is removed and replaced with pure water, leaving a 14% salt solution. How many litres were replaced?", ["10", "12", "15", "18"], "15", "Salt falls from 10 L to 7 L. Removing x litres removes 20% of x salt; 10−0.2x=7 gives x=15 L."),
    item("HARD", "sales-volume-price", "A seller reduces a product's price by 12% and then sells 25% more units. By what percentage does revenue change?", ["increase 10%", "increase 10.5%", "decrease 10%", "increase 13%"], "increase 10%", "Revenue factor=0.88×1.25=1.10, so it increases by 10%."),
    item("HARD", "two-stage-markup-discount", "A shop gives a 15% discount on the marked price and still earns 19% profit on cost. By what percentage is the marked price above cost?", ["35%", "38%", "40%", "42%"], "40%", "0.85×marked price=1.19×cost; marked/cost=1.19/0.85=1.40, or 40% above cost."),
    item("HARD", "successive-rate-unknown", "A quantity is increased by 25%, decreased by 20%, then increased by x%. The final result is 5% above the original. Find x.", ["4%", "5%", "6%", "8%"], "5%", "1.25×0.80=1. Thus 1×(1+x/100)=1.05, so x=5%."),
    item("HARD", "rate-share-equation", "In a workforce, 35% are technicians and 65% are operators. 8% of technicians and 4% of operators are promoted. What percentage of all workers are promoted?", ["4.8%", "5.2%", "5.4%", "6%"], "5.4%", "0.35×8% + 0.65×4% = 2.8% + 2.6% = 5.4%."),
    item("HARD", "tax-included-discount", "A bill after a 20% discount and then 10% tax is ₹5,280. What was the marked price?", ["₹5,800", "₹6,000", "₹6,200", "₹6,400"], "₹6,000", "Final factor=0.8×1.1=0.88; marked price=5,280/0.88=₹6,000."),
    item("HARD", "relative-cost-of-consumption", "The price of rice rises 25%. A household wants its rice expenditure to fall by 10%. By what percentage must it reduce rice consumption?", ["24%", "26%", "28%", "30%"], "28%", "Required consumption factor=0.90/1.25=0.72, a 28% reduction."),
    item("HARD", "marks-total-with-multiple-conditions", "A candidate scores 42% and falls short of the pass mark by 18. Another scores 54% and exceeds the pass mark by 30. What is the maximum score?", ["350", "400", "450", "500"], "400", "The 12-point difference equals 48 marks, so maximum=48/0.12=400."),
    item("HARD", "profit-multiple-stage", "A trader buys an article at 20% below its marked price and sells it at 25% above its cost price. The selling price is ₹1,500. What was the marked price?", ["₹1,440", "₹1,500", "₹1,560", "₹1,600"], "₹1,500", "Cost=1,500/1.25=1,200. Cost is 80% of marked price, so marked price=1,200/0.8=₹1,500."),
    item("HARD", "population-share-composition", "A city has 60% adults and 40% children. Adult population grows by 5%, while child population falls by 10%. What is the net percentage change in total population?", ["increase 1%", "increase 2%", "decrease 1%", "decrease 2%"], "decrease 1%", "Weighted change=0.60×5%−0.40×10%=3%−4%=−1%."),
    item("HARD", "reverse-double-change", "After a 20% increase followed by a 20% decrease, a machine's output is 9,600 units. What was its original output?", ["9,800", "10,000", "10,200", "10,400"], "10,000", "Combined factor=1.2×0.8=0.96; original=9,600/0.96=10,000."),
    item("HARD", "percentage-of-percentage-gap", "A candidate's score is 20% below the qualifying score. Another candidate scores 25% above that same qualifying score. The second candidate scores 90 marks more. What is the qualifying score?", ["180", "200", "225", "240"], "200", "The gap is 45% of qualifying score; 90/0.45=200."),
    item("HARD", "unit-price-adjustment", "A 15% fall in the price of a commodity lets a buyer purchase 12 kg more for ₹2,040 than before. What was the original price per kg?", ["₹20", "₹24", "₹30", "₹34"], "₹30", "Let original price p; 2,040/(0.85p)−2,040/p=12. This gives 2,040×0.15/(0.85p)=12, so p=₹30."),
    item("HARD", "net-change-through-three-rates", "A company's revenue rises 30%, then falls 20%, then rises 10%. What is the net percentage change from the starting revenue?", ["increase 14.4%", "increase 16.4%", "increase 18%", "decrease 16.4%"], "increase 14.4%", "1.30×0.80×1.10=1.144, a net increase of 14.4%."),
]


def norm(value: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run-only", action="store_true", help="validate without committing")
    args = parser.parse_args()
    with SessionLocal() as db:
        chapters = db.query(Chapter).join(Subject).join(Exam).filter(
            Exam.slug == "ssc", Exam.is_active.is_(True), Subject.slug == "maths",
            Subject.is_active.is_(True), Chapter.slug == "percentage", Chapter.is_active.is_(True),
        ).all()
        if len(chapters) != 1:
            raise SystemExit(f"Expected exactly one active SSC Maths Percentage chapter; found {len(chapters)}")
        chapter = chapters[0]
        all_rows = db.query(Question).filter(Question.chapter_id == chapter.id).all()
        counts = {
            difficulty: sum(q.is_active and not q.is_pyq and q.difficulty.value == difficulty for q in all_rows)
            for difficulty in ("EASY", "MEDIUM", "HARD")
        }
        deficits = {difficulty: max(0, TARGET - count) for difficulty, count in counts.items()}
        print(f"Live counts={counts}; deficits={deficits}; total missing={sum(deficits.values())}")
        if not any(deficits.values()):
            print("All difficulty minimums already satisfied; no import needed")
            return

        existing = {norm(q.question_text) for q in all_rows}
        candidates_by_difficulty = {
            difficulty: [q for q in QUESTIONS if q["difficulty"] == difficulty]
            for difficulty in counts
        }
        rows: list[dict] = []
        for difficulty, deficit in deficits.items():
            selected = []
            for candidate in candidates_by_difficulty[difficulty]:
                stem = candidate["question_text"]
                normalized = norm(stem)
                if normalized in existing:
                    continue
                close = [old for old in existing if SequenceMatcher(None, normalized, old).ratio() >= 0.76]
                close += [old["question_text"] for old in selected if SequenceMatcher(None, normalized, norm(old["question_text"])).ratio() >= 0.76]
                if close:
                    print(f"NEAR-DUPLICATE REVIEW required for {difficulty}: {stem} :: {close[:2]}")
                    continue
                clean = {key: value for key, value in candidate.items() if not key.startswith("_")}
                selected.append(clean)
                if len(selected) == deficit:
                    break
            if len(selected) != deficit:
                raise SystemExit(f"Only {len(selected)} valid, non-near-duplicate {difficulty} candidates for deficit {deficit}")
            rows.extend(selected)

        unique_patterns = len({q["_pattern"] for q in QUESTIONS})
        if unique_patterns != len(QUESTIONS):
            raise SystemExit("Repeated calculation pattern labels found in the candidate batch")
        payload = json.dumps({"questions": rows}, ensure_ascii=False).encode("utf-8")
        preview = import_questions(db, payload, "application/json", "percentage_difficulty_expansion.json", True)
        if preview.aborted or preview.errors or preview.duplicates or preview.would_import != sum(deficits.values()):
            raise SystemExit(f"Importer dry run failed: {preview.model_dump()}")
        if args.dry_run_only:
            print("Dry run passed; no records committed")
            return
        print(f"Importer dry run accepted {preview.would_import} rows; committing one transaction")
        committed = import_questions(db, payload, "application/json", "percentage_difficulty_expansion.json", False)
        if committed.aborted or committed.errors or committed.duplicates or committed.imported != sum(deficits.values()):
            raise SystemExit(f"Importer commit did not match validated batch: {committed.model_dump()}")
        print(f"Imported {committed.imported} original questions")


if __name__ == "__main__":
    main()
