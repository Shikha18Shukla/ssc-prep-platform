# Puzzle deduplication and independent verification — progress

**Day-Based Sets 1–4 are processed.** Set 4 source reconciliation and answer verification are complete; the final group remains underdetermined, so four questions are held.

## Day-Based Set 4 source and solving

The original 13-page PDF was reviewed against extracted text and rendered pages for all Set 4 question groups, including the solution continuation on p. 12. The four groups are Q1–5, Q6–10, Q11–15, and Q16–20. Three groups have exactly one clue-consistent arrangement. Under the literal no-between reading of the Q16–Q20 final clue, that group has three. The publisher’s p. 12 elimination discards two arrangements using an ordering not clearly stated in the clue text; this conflict is documented, not silently resolved.

### Group arrangements and question results

1. **Q1–Q5 (unique):** Sunday Myntra, Monday Snapdeal, Tuesday Flipkart, Wednesday Ajio, Thursday Lifestyle, Friday Meesho, Saturday Faballey. Answers **D, A, B, A, A**; all printed keys match.
2. **Q6–Q10 (unique):** Monday Q(19), Tuesday T(23), Wednesday R(13), Thursday U(17), Friday P(25), Saturday S(11), Sunday V(29). Answers **D, D, E, B, C**; all printed keys match.
3. **Q11–Q15 (unique):** Monday Domino’s, Tuesday Swiggy, Wednesday Uber eats, Thursday Deliveroo, Friday Door dash, Saturday Zomato, Sunday Just eat. Answers **A, C, E, B, A**; all printed keys match.
4. **Q16–Q20 (non-unique):** exhaustive enumeration gives three clue-consistent arrangements:
   - Sunday C-Infosys, Monday B-Microsoft, Tuesday G-HCL, Wednesday A-Oracle, Thursday E-Wipro, Friday D-TCS, Saturday F-Google.
   - Sunday C-Infosys, Monday D-TCS, Tuesday E-Wipro, Wednesday A-Oracle, Thursday G-HCL, Friday B-Microsoft, Saturday F-Google.
   - Sunday C-Infosys, Monday D-TCS, Tuesday G-HCL, Wednesday A-Oracle, Thursday E-Wipro, Friday B-Microsoft, Saturday F-Google.
   **Q19 is verified as option B (E)** because E is Wipro in all three. **Q16, Q17, Q18 and Q20 are held**: the answer or single-option integrity changes across valid arrangements. Printed keys E, D, C and E only fit subsets of the valid solutions; for Q20, the third arrangement yields A/C/D true, which has no listed response.

### All Set 4 question classifications

| Question | Status | Independent result | Printed key | Notes |
|---|---|---|---|---|
| Q1 (p. 2) | verified_import_candidate | D — Lifestyle-Sunday | D | Verified independently |
| Q2 (p. 2) | verified_import_candidate | A — Only I and IV | A | Verified independently |
| Q3 (p. 2) | verified_import_candidate | B — The store which gives immediately before Faballey | B | Verified independently |
| Q4 (p. 2) | verified_import_candidate | A — Saturday | A | Verified independently |
| Q5 (p. 2–3) | verified_import_candidate | A — Three | A | Verified independently |
| Q6 (p. 5) | verified_import_candidate | D — Four | D | Verified independently |
| Q7 (p. 5) | verified_import_candidate | D — Person whose age is 17 | D | Verified independently |
| Q8 (p. 5) | verified_import_candidate | E — More than four | E | Verified independently |
| Q9 (p. 5) | verified_import_candidate | B — Person who celebrated on Friday | B | Verified independently |
| Q10 (p. 5) | verified_import_candidate | C — Person who celebrates on Thursday | C | Verified independently |
| Q11 (p. 8) | verified_import_candidate | A — Domino’s | A | Verified independently |
| Q12 (p. 8) | verified_import_candidate | C — Just eat and Door dash | C | Verified independently |
| Q13 (p. 8) | verified_import_candidate | E — None | E | Verified independently |
| Q14 (p. 8) | verified_import_candidate | B — Just eat | B | Verified independently |
| Q15 (p. 8) | verified_import_candidate | A — Deliveroo | A | Verified independently |
| Q16 (p. 10) | held | Held | E | The three valid arrangements yield either Friday D/TCS (where options A and C both describe that same Friday person) or Friday B/Microsoft (where options B and D are both correct); exactly-one-option integrity and answer stability fail. |
| Q17 (p. 10) | held | Held | D | The odd pair is not stable: FB is the positional-gap outlier in arrangements 1 and 3, while arrangement 2 has a different gap pattern (CG is four apart and FB one apart), so a unique odd pair is not established. |
| Q18 (p. 10) | held | Held | C | The correct response is C in arrangement 1 but E (none of A-D) in arrangements 2 and 3. |
| Q19 (p. 10) | verified_import_candidate | B — E | B | Verified independently |
| Q20 (p. 11) | held | Held | E | The truth set varies: arrangement 1 makes A-D true; arrangement 2 makes only A true; arrangement 3 makes A, C and D true, for which no listed response exists. |

### Source corrections and page spans

- Removed the embedded running header from the Q6–Q10 directions: The source PDF contains the running header “DAY BASED PUZZLE SET-4 (Eng)” embedded between the T/Q and age clues in the p. 4–5 text extraction. It is a page header, not a puzzle clue; it was removed from the directions.
- Removed the embedded running header from the Q11–Q15 directions; it was extraction contamination, not a clue.
- Restored Q10 option D from the rendered p. 5 source: “Person who celebrates exactly between S and Q”; the old inventory stopped after “S”.
- Checked source spans: Q5 is p. 2–3; Q12–Q15 p. 8; Q20 p. 11. These spans are correct. Questions Q6–Q10 use the p. 4–5 shared directions and p. 5 questions; Q11–Q15 use p. 7–8 directions and p. 8 questions.
- The p. 12 publisher solution eliminates alternatives that satisfy the literal no-between clue and displays only one arrangement. Since the clue does not clearly state the stronger ordering used by that elimination, Q16–Q18 and Q20 remain held. Q19 remains invariant.
- The source spells the Q1 option “Sanpdeal”; it was preserved rather than silently corrected.

### Semantic deduplication and local destination check

Set 4 was compared with the question contexts in Sets 1–3 and with its own 20 appearances. No semantic duplicate was identified. The local PostgreSQL database was queried in a `READ ONLY` transaction at `127.0.0.1:5432/ssc_prep`: Weekdays Based `a6d1bdfc-f147-4c1b-b88d-17e415219f4f` has 0 active / 0 inactive; Designation Based `4ed7e743-a62d-4236-af91-20298410eb2f` has 0 active / 0 inactive. No database overlaps were found. No writes or migrations were performed.

## Day-Based Set 5 source and solving

All 12 physical pages were reviewed visually. The numbered question pages and continuation pages were reconciled; Q9 (p. 5) and Q19 (p. 10) are present in the inventory. Three groups have unique solutions. The foot-fest group has five valid arrangements under the written clues, although the printed solution presents only one.

### Group arrangements

1. **Q1–Q5 (unique):** Monday:B-Red; Tuesday:A-Pink; Wednesday:F-Yellow; Thursday:C-Green; Friday:D-Orange; Saturday:E-Blue. Answers **A, E, B, C, C**; all printed keys match.
2. **Q6–Q10 (non-unique):** five valid clue-consistent schedules remain:
   1. Monday:B-Dosa; Tuesday:D-Chappati; Wednesday:A-Parota; Thursday:C-Idly; Friday:E-Poori; Saturday:F-Rice
   2. Monday:B-Dosa; Tuesday:D-Chappati; Wednesday:A-Parota; Thursday:F-Idly; Friday:E-Poori; Saturday:C-Rice
   3. Monday:B-Dosa; Tuesday:D-Chappati; Wednesday:F-Parota; Thursday:A-Idly; Friday:E-Poori; Saturday:C-Rice
   4. Monday:B-Dosa; Tuesday:D-Chappati; Wednesday:F-Parota; Thursday:C-Idly; Friday:E-Poori; Saturday:A-Rice
   5. Monday:F-Poori; Tuesday:B-Dosa; Wednesday:D-Chappati; Thursday:A-Parota; Friday:C-Idly; Saturday:E-Rice
   The publisher’s p. 6 eliminations do not remove four schedules under the written clues. Q6, Q8, Q9 and Q10 have different answers across valid schedules; Q7’s conditional mapping is under-specified. All five are held.
3. **Q11–Q15 (unique):** Sunday:Pasta; Monday:Biryani; Tuesday:Soup; Wednesday:Burger; Thursday:Dosa; Friday:Meals; Saturday:Pizza. Answers **D, B, C, D, D**; all printed keys match.
4. **Q16–Q20 (unique):** Sunday:Air India; Monday:Jetlite; Tuesday:Spicejet; Wednesday:Vistara; Thursday:Goair; Friday:Air Asia; Saturday:Indigo. Answers **D, C, E, D, C**; all printed keys match.

### Set 5 question classifications

| Question | Status | Answer or hold reason | Printed key |
|---|---|---|---|
| Q1 (p. 2) | verified_import_candidate | A — The one who bought immediately before E | A |
| Q2 (p. 2) | verified_import_candidate | E — Monday-E | E |
| Q3 (p. 2) | verified_import_candidate | B — Two | B |
| Q4 (p. 2) | verified_import_candidate | C — Yellow | C |
| Q5 (p. 2) | verified_import_candidate | C — A-Pink | C |
| Q6 (p. 4) | held | The exhaustive clue check leaves five different valid arrangements; the person ordering Idly changes (C, F, A, C, C), so no single listed answer is established. | B |
| Q7 (p. 4-5) | held | The conditional “If E orders on Monday, C orders on 7, and so on in the same logic” does not define a mapping for the other people or explain what “7” means for a Monday-Saturday event; the printed key cannot be independently derived. | D |
| Q8 (p. 5) | held | Thursday contains Idly in four valid arrangements but Parota in the fifth, so the answer is not invariant. | A |
| Q9 (p. 5) | held | Poori is Friday in four valid arrangements and Monday in the fifth, so the day is not invariant. | C |
| Q10 (p. 5) | held | The number between B and C is two in three valid arrangements and four in two; both options B and D occur. | B |
| Q11 (p. 6-7) | verified_import_candidate | D — Sunday | D |
| Q12 (p. 7) | verified_import_candidate | B — Only II | B |
| Q13 (p. 7) | verified_import_candidate | C — The dish which is celebrated exactly between Pasta and Dosa days | C |
| Q14 (p. 7) | verified_import_candidate | D — Five | D |
| Q15 (p. 7) | verified_import_candidate | D — Same as the dishes celebrated after the dosa day | D |
| Q16 (p. 9-10) | verified_import_candidate | D — Four | D |
| Q17 (p. 9) | verified_import_candidate | C — Goair | C |
| Q18 (p. 9-10) | verified_import_candidate | E — More than four | E |
| Q19 (p. 10) | verified_import_candidate | D — Tuesday | D |
| Q20 (p. 10) | verified_import_candidate | C — Indigo | C |

### Set 5 source corrections

- Recovered the full Q3 option A from p. 2: “As many persons bought the dress between A and E”; the prior extraction stopped at “A”.
- Corrected line-wrap artifacts `bef ore` → `before` in Q1–Q5 directions and `followi ng` → `following` in Q16–Q20 directions. Normalized the Q19 `re lated` line wrap to “related”.
- Corrected physical spans and source identifiers: Q7 p. 4–5 (options continue on p. 5); Q11 p. 6–7 (option E continues on p. 7); Q16 and Q18 p. 9–10 (options continue on p. 10). Q9 remains p. 5 and Q19 p. 10.
- No question wording or answer was silently rewritten.

### Set 5 duplicate and database check

Compared Set 5 against Sets 1–4, within Set 5, and both destination chapters. No semantic duplicates were identified. A read-only transaction confirmed local `ssc_prep` at `127.0.0.1:5432`; Weekdays Based has 0 active / 0 inactive and Designation Based has 0 active / 0 inactive. No writes or migrations occurred.

## Day-Based Set 6 source and solving

All 12 physical pages were visually reviewed. The four puzzle groups were exhaustively enumerated; each has one solution and all 20 questions have one independently verified correct option. Q2 and Q5, Q6, Q10, and Q15 were specifically source-checked.

### Group arrangements

1. **Q1-Q5 (unique):** Monday:B-Botany; Tuesday:F-English; Wednesday:D-Zoology; Thursday:C-Chemistry; Friday:A-Tamil; Saturday:G-Maths; Sunday:E-Physics. Answers **D, B, E, A, C**; all printed keys match.
2. **Q6-Q10 (unique):** Monday:F-3 wickets; Tuesday:M-7 wickets; Wednesday:D-6 wickets; Thursday:N-5 wickets; Friday:O-8 wickets; Saturday:E-9 wickets. Answers **C, B, C, D, D**; all printed keys match.
3. **Q11-Q15 (unique):** Sunday:A; Monday:C; Tuesday:E; Wednesday:B; Thursday:F; Friday:G; Saturday:D. Answers **C, A, D, E, C**; all printed keys match.
4. **Q16-Q20 (unique):** Wednesday:C-Coorg; Thursday:F-Ooty; Friday:B-Leh; Saturday:D-Goa; Sunday:G-Hampi; Monday:A-Shimla; Tuesday:E-Agra. Answers **C, E, A, C, C**; all printed keys match.

### Set 6 question classifications

| Question | Status | Independently derived answer | Printed key |
|---|---|---|---|
| Q1 (p. 2) | verified_import_candidate | D — The one which taught immediately before English | D |
| Q2 (p. 2) | verified_import_candidate | B — The one goes on Saturday | B |
| Q3 (p. 2) | verified_import_candidate | E — None | E |
| Q4 (p. 2) | verified_import_candidate | A — Zoology | A |
| Q5 (p. 2-3) | verified_import_candidate | C — The one who goes to Zoology tuition goes two days after B | C |
| Q6 (p. 4) | verified_import_candidate | C — O | C |
| Q7 (p. 4) | verified_import_candidate | B — Monday | B |
| Q8 (p. 4) | verified_import_candidate | C — 15 | C |
| Q9 (p. 4-5) | verified_import_candidate | D — Saturday | D |
| Q10 (p. 5) | verified_import_candidate | D — The one who plays on Monday | D |
| Q11 (p. 6) | verified_import_candidate | C — Tuesday | C |
| Q12 (p. 6) | verified_import_candidate | A — D | A |
| Q13 (p. 6) | verified_import_candidate | D — F | D |
| Q14 (p. 6-7) | verified_import_candidate | E — DA | E |
| Q15 (p. 7) | verified_import_candidate | C — Only III | C |
| Q16 (p. 9) | verified_import_candidate | C — A | C |
| Q17 (p. 9) | verified_import_candidate | E — Two | E |
| Q18 (p. 9) | verified_import_candidate | A — The person who attends the wedding on Sunday | A |
| Q19 (p. 9) | verified_import_candidate | C — The one who likes Coorg attends the wedding immediately before F | C |
| Q20 (p. 9) | verified_import_candidate | C — G – Shimla | C |

### Set 6 source corrections and page spans

- Normalized extraction line wraps in the tuition directions (`day s`, `day o n`, `go es`) and shopping directions (`Su nday`, spacing at sentence boundaries).
- Removed the running page header mistakenly inserted inside Q16-Q20 directions; normalized `We dnesday` to “Wednesday” and line-wrapped “the”.
- Normalized the cricket clue wrap `odd- numbered` to “odd-numbered”.
- Corrected spans/stable IDs after source review: Q6 is p. 4 (all options there), Q9 is pp. 4-5, and Q14 is pp. 6-7. Q5 remains pp. 2-3.
- Other question spans checked: Q1-Q4 p. 2; Q7-Q8 p. 4; Q10 p. 5; Q11-Q13 p. 6; Q15 p. 7; Q16-Q20 p. 9.
- No question answer or substantive wording was changed.

### Set 6 duplicates and destination check

Set 6 was compared with Sets 1-5, within itself, and against the local destination chapters. No semantic duplicates were identified. A read-only query confirmed local `ssc_prep` at `127.0.0.1:5432`; Weekdays Based has 0 active / 0 inactive and Designation Based has 0 active / 0 inactive. No database writes or migrations were performed.

## Designation-Based Phase 2 verification (Sets 2-4)

All 36 pages across the three PDFs were inspected through the saved rendered composites and page extracts. Question wording, options, shared clues, and printed keys were checked. The 12 shared-clue groups were exhaustively enumerated over every assignment of people to designation slots; the sports group also enumerated all person and sport permutations. Each group has exactly one valid arrangement.

### Puzzle-group arrangements

1. **Set 2 Q1-Q5:** Reporter B → Resident Editor E → Photo Editor C → Sub Editor F → News Editor A → Assignment Editor G → Publisher D. Answers D, C, A, E, B.

2. **Set 2 Q6-Q10:** Coordinator L → Analyst K → Client Strategist N → Associate M → Traffic Manager H → Planner I → Trainee J. Answers C, E, A, D, A.

3. **Set 2 Q11-Q15:** CEO U → GM Q → DGM V → AGM P → Manager S → Assistant Manager T → Clerk R. Answers D, E, D, B, B.

4. **Set 2 Q16-Q20:** CEO B → Director F → Manager C → Assistant Manager G → HR Manager A → Customer Representative H → Chef E → Staff D. Answers D, C, B, D, C.

5. **Set 3 Q1-Q5:** Board of Director I → CEO N → COO O → President J → Vice President K → General Manager M → Supervisor H → Worker L. Answers D, C, B, D, E.

6. **Set 3 Q6-Q10:** Field Marshal I → General G → Lieutenant General B → Major General F → Brigadier D → Colonel E → Lieutenant Colonel H → Major C → Captain A. Answers C, B, E, A, D.

7. **Set 3 Q11-Q15:** Dean Adhi → Administrator Maya → Surgeon Sara → Specialist Doctor Jai → General Doctor Giri → Chief Nurse Akila → Nurse Riya → Physician Assistant Nitin → Medical Intern Hira. Answers C, D, B, D, A.

8. **Set 3 Q16-Q20:** DCP I → SP G → ASP F → DSP L → PI E → API K → SI H → ASI J. Answers D, C, A, B, E.

9. **Set 4 Q1-Q5:** General Manager M (Cricket) → Chief Manager O (Hockey) → Branch Manager L (Football) → Assistant Manager Q (Basketball) → PO P (Badminton) → Clerk N (Tennis). Answers A, E, A, D, D.

10. **Set 4 Q6-Q10:** General C → Brigadier E → Colonel H → Major F → Captain A → Lieutenant G → Subedar D → Hawaldar B. Answers B, A, D, E, C.

11. **Set 4 Q11-Q15:** Director M → Hotel Manager R → Assistant Manager L → HR Manager P → Customer Representative Q → Chef O → Staff N. Answers D, E, A, A, D.

12. **Set 4 Q16-Q20:** Chairman Q → President T → General Manager O → Assistant Manager S → Branch Manager P → Probationary Officer U → Clerk R. Answers C, D, D, B, C.


### Question classifications and printed-key comparison

| PDF | Per-question answer (option letter) | Classification | Printed-key comparison |
|---|---|---|---|

| DESIGNATION BASED PUZZLE SET-2 (Eng).pdf | Q1 D, Q2 C, Q3 A, Q4 E, Q5 B, Q6 C, Q7 E, Q8 A, Q9 D, Q10 A, Q11 D, Q12 E, Q13 D, Q14 B, Q15 B, Q16 D, Q17 C, Q18 B, Q19 D, Q20 C | 20 verified_import_candidate | All 20 match |

| DESIGNATION BASED PUZZLE SET-3 (Eng).pdf | Q1 D, Q2 C, Q3 B, Q4 D, Q5 E, Q6 C, Q7 B, Q8 E, Q9 A, Q10 D, Q11 C, Q12 D, Q13 B, Q14 D, Q15 A, Q16 D, Q17 C, Q18 A, Q19 B, Q20 E | 20 verified_import_candidate | All 20 match |

| DESIGNATION BASED PUZZLE SET-4 (Eng).pdf | Q1 A, Q2 E, Q3 A, Q4 D, Q5 D, Q6 B, Q7 A, Q8 D, Q9 E, Q10 C, Q11 D, Q12 E, Q13 A, Q14 A, Q15 D, Q16 C, Q17 D, Q18 D, Q19 B, Q20 C | 20 verified_import_candidate | All 20 match |


All 60 Designation-Based questions have exactly five options, one independently verified answer, and an explanation in the answer ledger. **Printed-key disagreements: none. Held questions: none. Duplicates within/across these PDFs: none. Existing destination database overlaps: none.**

### Source corrections

- Corrected OCR line-wrap and running-header artifacts in shared directions, including the Set 4 Q16-Q20 header inserted into the T/R clue and split words such as “President” and “More.”
- Recovered the full Set 2 Q3 option C from the rendered source: “Only two persons are holding the position between A and G.”
- Corrected question/options physical page spans: Set 2 Q7 pp. 4-5 and Q19 pp. 9-10; Set 3 Q7 pp. 4-5 and Q18 pp. 9-10; Set 4 Q9 p. 5 (not p. 6) and Q15 pp. 7-8.
- Set 2 Q6-Q10 publisher case 2 is invalid because J occupies Associate despite the explicit clue that J does not; exhaustive enumeration leaves the unique arrangement reported above.

### Destination check

A read-only transaction confirmed `ssc_prep` at `127.0.0.1:5432` and target chapter `4ed7e743-a62d-4236-af91-20298410eb2f` has 0 active / 0 inactive questions. No question records or schema were changed.

## Overall Phase 2 progress across all nine PDFs

- Groups: **36 identified; 36 solved/reviewed; 0 remaining.**
- Question appearances: **180 of 180 classified.**
- Verified import candidates: **166**; duplicates: **0**; held: **14**; not started: **0**. The 14 held questions are from previously audited Day-Based material; no Designation question is held.
- Completed source files: Day-Based Sets 1-6 and Designation-Based Sets 2-4.
- This Designation audit made no database writes or migrations. The Weekdays Based chapter is outside scope and was not modified.
