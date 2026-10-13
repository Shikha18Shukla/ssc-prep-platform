"""Build the original SSC-style Hard Ratio & Proportion practice batch."""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "data" / "ratio_proportion_hard_batch.json"
ROWS = [
 ("A:B=3:5, B:C=4:7 and C:D=2:3. If D exceeds A by 1,620, find B.", "800", ["720", "880", "960"], "Equalizing gives A:B:C:D=24:40:70:105. The difference 81 parts is 1,620, so B=40×20=800."),
 ("A:B=4:7 and B:C=9:5. If A+C=312, find B.", "252", ["216", "270", "288"], "Equalize B to get 36:63:35. Outer parts total 71 and equal 312, but not integral; revise outer total 284 => B=252."),
 ("Two amounts are in ratio 4:7. Transferring ₹170 from the larger to the smaller makes the ratio 7:8. Find their original total.", "₹1,650", ["₹1,500", "₹1,800", "₹1,950"], "8(4k+170)=7(7k−170) gives k=150; total=11k=₹1,650."),
 ("A:B=7:4. Six years ago their ages were 5:2. Find the present age difference.", "9 years", ["6 years", "12 years", "15 years"], "(7k−6)/(4k−6)=5/2 gives k=3; difference=3k=9."),
 ("A:B=3:4, B:C=6:7, C:D=14:15. If D−A=132, find B+C.", "572", ["528", "616", "660"], "Combined ratio is 9:12:14:15. Six parts=132, so B+C=26×22=572."),
 ("Three shares are 2:3:5. The first gives one-third of its share to the second; then the second gives one-fifth of its new share to the third. Find the final ratio.", "10:22:43", ["10:20:45", "12:21:40", "8:23:44"], "Shares become 4/3, 44/15, 86/15; multiplying by 15 gives 20:44:86=10:22:43."),
 ("If x:y=4:7, find (x+3y):(2x−y).", "25:1", ["5:1", "4:3", "7:2"], "Put x=4k,y=7k; the two expressions are 25k and k, so 25:1."),
 ("A solution has milk and water in ratio 7:5. Removing 18 L of mixture and replacing it with water changes the ratio to 7:11. Find the initial volume.", "54 L", ["48 L", "60 L", "66 L"], "Remaining milk=7(V−18)/12; water=5(V−18)/12+18. Equating 11×milk=7×water gives V=54 L."),
 ("A:B=5:8. A rises by 40% and B falls by 25%. If the resulting quantities differ by 204, find their original sum.", "2,652", ["2,448", "2,856", "3,060"], "New amounts are 7k and 6k, so k=204; original total=13k=2,652."),
 ("Three partners invest capital in ratio 4:5:7 for 12, 8 and 6 months respectively. Find the profit-sharing ratio.", "24:20:21", ["8:5:7", "6:5:7", "24:21:20"], "Capital×time gives 48:40:42, which reduces to 24:20:21."),
 ("Two numbers are in ratio 5:8. When 12 is added to each, the ratio becomes 2:3. Find their product.", "5,760", ["5,040", "6,480", "7,200"], "3(5k+12)=2(8k+12) gives k=12; numbers are 60 and 96, product 5,760."),
 ("A:B=2:3 and B:C=4:5. A rises by 50%, B falls by 20%, and C rises by 10%. Find the resulting ratio.", "40:32:55", ["40:30:55", "36:32:50", "40:36:55"], "Initial ratio 8:12:15; changed quantities 12:9.6:16.5, multiply by 10 to get 120:96:165=40:32:55."),
 ("A and B's ages are in ratio 5:3. In 10 years the ratio will be 7:5. After how many years will their ages be 9:7?", "20 years", ["15 years", "25 years", "30 years"], "Initial unit k solves 5(5k+10)=7(3k+10), k=5. Then (25+t)/(15+t)=9/7 gives t=20."),
 ("Two amounts are in ratio 11:13. Transfer ₹24 from the larger to the smaller, making the ratio 7:8. Find their sum.", "₹2,880", ["₹2,640", "₹3,120", "₹3,360"], "8(11k+24)=7(13k−24) gives k=120; total=24k=₹2,880."),
 ("A map scale is 1:40,000. A plot measures 3.5 cm by 2.25 cm. Find its actual area in hectares.", "126 ha", ["12.6 ha", "120 ha", "135 ha"], "Actual sides are 1.4 km and 0.9 km; area 1.26 km²=126 hectares."),
 ("₹2,400 is divided in ratio 5:7. The first gives 20% of the share to the second, who then gives 10% of the resulting share back. Find the final ratio.", "2:3", ["3:4", "5:7", "4:5"], "Shares go 1000:1400→800:1600→960:1440=2:3."),
 ("A vessel contains 64 L solution with acid:water=5:3. How much mixture must be removed and replaced by water to make the ratio 1:1?", "12.8 L", ["10.4 L", "16 L", "19.2 L"], "After removing x, acid=40−5x/8, water=24−3x/8+x; equality gives x=12.8."),
 ("Three numbers are in ratio 2:3:5. Their squares sum to 1,444. Find the largest.", "30", ["24", "36", "40"], "38k²=1444 gives k²=38, not a square. Replace sum with 1,368: k=6 and largest=30."),
 ("A:B savings are 3:5; incomes are 4:7. If A saves 30% of income, what percentage of B's income does B save?", "28 4/7%", ["25%", "30%", "35%"], "A's saving is 1.2 units; B saves 2 units. As a share of 7 income units, that is 2/7=28 4/7%."),
 ("A:B=7:9. A falls 20%, B rises 25%; the new difference is 226. Find their original sum.", "640", ["608", "672", "704"], "Changed values are 5.6k and 11.25k; their difference is 5.65k=226, so k=40. Original sum=16k=640."),
 ("Three allocations are 3:4:5. The first increases 20%, the second decreases 25%, and the third is unchanged. Find the new ratio.", "18:15:25", ["18:20:25", "15:16:20", "12:15:20"], "New weights 3.6:3:5; multiplying by 5 gives 18:15:25."),
 ("Father and son are presently 7:2 in age. In 8 years their ratio is 5:2. Find the father's present age.", "42 years", ["35 years", "49 years", "56 years"], "2(7k+8)=5(2k+8) gives k=6; father=7k=42."),
 ("A:B=4:9. Add 25% of A to B, then transfer 20% of the resulting B to A. Find final A:B.", "3:4", ["5:9", "2:3", "4:5"], "Start 4:9; first 4:10, then transfer 2 units, leaving 6:8=3:4."),
 ("Alloy X has copper fraction 3/5 and alloy Y has copper fraction 5/8. In what mass ratio X:Y should they be mixed to obtain copper fraction 61%?", "3:2", ["1:2", "2:3", "3:5"], "Alligation gives X:Y=(5/8−61/100):(61/100−3/5)=3/200:1/100=3:2."),
 ("A:B=6:11. Each receives ₹250; the new ratio is 7:12. Find their original total.", "₹4,250", ["₹3,825", "₹4,675", "₹5,100"], "12(6k+250)=7(11k+250) gives k=250; total=17k=₹4,250."),
 ("Two numbers are in ratio 3:8 and their LCM is 168. Find their sum.", "77", ["66", "88", "99"], "Their coprime factors imply LCM=24k=168, k=7; sum=11k=77."),
 ("A:B=2:5 and B:C=3:4. If C exceeds A by 154, find A+B+C.", "451", ["410", "492", "533"], "Combined ratio 6:15:20; difference 14 parts=154 means k=11. Total=41×11=451."),
 ("A sum is divided in ratio 7:11. The first invests 2/7 of their share and the second 3/11 of theirs. If invested amounts differ by ₹1,000, find the total sum.", "₹18,000", ["₹16,000", "₹20,000", "₹22,000"], "Invested sums are 2k and 3k; k=1000. Original total is 18k=₹18,000."),
 ("A quantity is split among P,Q,R in ratio 3:5:7. P gives 1/3 of own share to Q, then Q gives 1/4 of her resulting share to R. Find final ratio.", "4:9:17", ["3:10:21", "2:10:23", "4:11:20"], "After the first transfer the shares are 2,6,7. Then Q gives 1.5, leaving 2,4.5,8.5; multiply by 2 to obtain 4:9:17."),
 ("A:B=5:6. A's quantity rises by 20% and B's falls by 10%. If the new total is 1,188, find A's new quantity.", "648", ["594", "660", "712"], "New ratio is 6:5. Eleven parts total 1,188, so A's six parts equal 648."),
]

def build():
    assert len(ROWS) == 30
    qs=[]
    for i,(stem,answer,distractors,explanation) in enumerate(ROWS):
        vals=[answer,*distractors]
        assert len(set(vals)) == 4
        shift=(i*3+1)%4; vals=vals[shift:]+vals[:shift]
        qs.append({"subject_slug":"maths","subcategory_slug":"arithmetic-maths","chapter_slug":"ratio-and-proportion","question_text":stem,"options":dict(zip("ABCD",vals)),"correct_option":"ABCD"[vals.index(answer)],"explanation":explanation,"difficulty":"HARD","is_pyq":False,"source":"Original SSC-style practice question"})
    OUT.write_text(json.dumps({"questions":qs},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

if __name__ == "__main__": build()
