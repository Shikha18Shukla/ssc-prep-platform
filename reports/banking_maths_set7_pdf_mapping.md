# Banking Maths Set 7 - PDF content mapping

All six attached PDFs were extracted with the Set 6 PyMuPDF/OCR approach:
PyMuPDF text layer first, then `rapidocr_onnxruntime` at 150 dpi for every
image-only page. **All 77 pages were image-only and were OCR’d.** Printed
questions and answer keys were treated as untrusted reference data and were
never copied into the bank.

Artifacts:

- `tmp/set7_extract_pdfs.py`
- `tmp/set7_pdf_text/*.json`
- `tmp/set7_pdf_text/inventory.json`
- `tmp/set7_page_map.py`
- `tmp/set7_page_map.txt`
- `tmp/set7_page_text.txt`

## Content-based chapter assignment

Chapter assignment was derived from slide titles and extracted topic text, not
from the UUID filenames.

| PDF file | Pages | Assigned chapter | Evidence from extracted pages |
| --- | ---: | --- | --- |
| `36c4c768-3fbf-4ae7-8b96-debff3f16eec.pdf` | 13 | Mixture and Alligation (Mains) | p1 “MIXTURE and Alligation Mains”; p3 “Mixture and Alligation Mains”; p4–p12 “MIXTURE ADVANCED” |
| `66052d90-202e-454e-96d2-3f7291856dba.pdf` | 13 | Mixture and Alligation – Data Interpretation | p1 “Mixture & Alligation Data Interpretation”; p3 “Mixture & Alligation Mains Data Interpretation”; p4–p12 container-based DI tables/caselets |
| `97c1911e-319b-4bc6-8383-48a92c70a378.pdf` | 11 | Ages (Mains) | p1 “Ages Mains”; p3 “Rules on Ages (MAINS)”; p4–p10 “Mains Problems Based on Ages” |
| `419d6ebd-36ff-4b8a-80e5-178a8bde98d6.pdf` | 13 | Ages – Data Interpretation | p1 “AGES Data Interpretation”; p3 “Ages Data Interpretation”; p4–p12 quantity comparison, blank-filling, table/average age DI |
| `cc2c97f4-4d95-4e6e-964f-d9318068eb13.pdf` | 14 | Partnership (Mains) | p1 “PARTNERSHIP MAINS”; p3 “Partnership Mains”; p4–p13 advanced capital/time, salary, ratio-amendment and caselet problems |
| `9f8905f3-85dc-44f0-bda1-42d5c96a3304.pdf` | 13 | Partnership – Data Interpretation | p1 “PARTNERSHIP DI”; p3 “Partnership Data Interpretation”; p4–p12 multi-business tables and caselets |

## Page-by-page topic record

Every PDF follows the same deck pattern: p1 title slide, p2 recap of the
previous lecture, p3 topics to be covered, p4 onward worked examples/caselets,
final page “THANK-YOU”. The content-bearing page ranges are recorded below.

### Mixture and Alligation (Mains) — 36c4…, pp. 4–12

- p4: three equal-size soda drums; multi-vessel concentration comparison.
- p5: ammonium sulphate/phosphate fertiliser mixing; component-ratio algebra.
- p6: two separated vessels X and Y; mixture strengths and transfer condition.
- p7: milk-and-water containers A and B; concentration comparison.
- p8: milk containers with 74% and 60% concentration; replacement/readdition.
- p9: item K made from chemicals A and B in a 7:5 ratio; cost/quality condition.
- p10–p12: worked calculations and average-marks mixture applications.
- Difficulty indicators: slide title “Mains”, topic heading “MIXTURE ADVANCED”,
  multi-step transfer/replacement/weighted-average examples.

### Mixture and Alligation – Data Interpretation — 66052…, pp. 4–12

- p4–p8: five containers P, Q, R, S and T with milk/alcohol quantities; table DI.
- p9: total mixture of container P increased by 28.56%; ratio-change question.
- p10: alcohol in container Q increased by 20%; component-quantity question.
- p11–p12: symbolic quantity expressions and milk-decrease condition for container T.
- Difficulty indicators: the source deck is labelled “Mains DI”, but the user
  requires these normal DI chapters to stay Prelims-level. The PDF is used only
  for topic scope; shipped questions are direct table/caselet interpretation.

### Ages (Mains) — 97c19…, pp. 4–10

- p4–p5: ages before 10 years, D is 16 years older than A, sum conditions;
  simultaneous equations.
- p6: five-member family (Aman, wife, son, two daughters); average-age relations.
- p7–p8: ratio of A:B = 3:p and a future age difference; quadratic in p.
- p9: Ritesh/Vikesh ratio 9:7 with percentage and future-ratio conditions.
- p10: age of A after q years and age of B after (p−2) years; ratio conditions.
- Difficulty indicators: “Mains Problems Based on Ages”, algebraic quadratics,
  multi-person family averages and shifted reference times.

### Ages – Data Interpretation — 419d…, pp. 4–12

- p4–p6: quantity-I vs quantity-II comparison format.
- p7–p8: P is 12.5% older than Q; future/past ratio answer options.
- p9: two blanks in a statement; half of a sum/cross-condition.
- p10–p11: information sufficiency and ratio-option selection.
- p12: average age of A, B, C and D = 38; average of B and C after 2 years.
- Difficulty indicators: source is titled “Ages Mains DI”, but shipped chapter
  is Prelims-level: direct lookup, difference, sum, average, percentage and
  simple ratio questions from inline data.

### Partnership (Mains) — cc2c…, pp. 4–13

- p4–p5: M and N initial investments; algebraic statement validation.
- p6–p8: P, Q and R capital/time caselet with direction questions.
- p9–p10: P, Q and R profit-percentage caselet.
- p11–p12: P, Q and R reinvestment/withdrawal caselet.
- p13: A, B and C direction caselet.
- Difficulty indicators: “PARTNERSHIP MAINS”, statement-option algebra,
  caselets with salary/commission, successive ratio changes and time weighting.

### Partnership – Data Interpretation — 9f89…, pp. 4–12

- p4–p6: three partners in five businesses A–E; initial-capital ratio table.
- p7: business A with a six-month joining condition.
- p8: business B with a late-joining partner after x years.
- p9–p10: worked calculations and salary/total-profit condition.
- p11: business D; partner withdrawal after five years.
- p12: business E; sequential joining after two and five years.
- Difficulty indicators: source is labelled “DI MAINS”, but shipped chapter is
  Prelims-level: totals, simple ratios, one-share amounts, differences,
  percentages, averages and missing-table entries from inline data.

## Formulas/patterns recorded for bank construction

- Mixture: concentration = solute/volume; weighted solute balance; replacement
  retains the current concentration; evaporation removes solvent only;
  alligation ratio = (target − cheaper) : (dearer − target); component transfer
  between vessels; three-component and two-stage restrictions.
- Ages: present/past/future ages as linear variables; ratio shifts at unequal
  time gaps; family averages with entry/exit/birth; percentage-of-age and
  reciprocal/product conditions; quadratic conditions in a ratio parameter.
- Partnership: profit share proportional to capital × time; salary/commission
  deducted before division; guaranteed minimum and deficiency adjustment;
  admission/retirement ratio amendment; capital changes at mid-period; reverse
  problems from one partner's share.
- DI: all data is embedded inline in every question; no question depends on an
  external table, chart, graph, image or passage.
