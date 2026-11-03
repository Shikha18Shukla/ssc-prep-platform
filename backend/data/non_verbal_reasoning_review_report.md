# CH-17 Non-Verbal Reasoning — Source Review and Bank

## Source review

Visually reviewed 106 pages: Lecture 02 (27), Lecture 03 (30), Lecture 04 (26), Lecture 06 (13), Lecture 07 (10). Lectures 01 and 05 were not supplied. Lecture 07 pages 2–8 are worked examples rather than complete MCQs; they were reviewed as counting reference material.

The source ledger records 55 complete prompt candidates rejected because instructor solution annotations are drawn over question/answer figures, making the cards unsuitable for direct learner display. By lecture: Lecture 02: 18 (mirror/paper reflection 1, folding/cutting 9, embedded figures 8); Lecture 03: 19 (analogy 7, classification 4, figure completion 8); Lecture 04: 17 (series 7, matrix 6, dot situation 4); Lecture 06: 1 triangle-count prompt. Lecture 07 pages 2–8 provide worked counting examples but no complete MCQ prompt. No answer ticks were adopted as answer keys. No source-derived questions were retained.

## Bank

33 original visual questions; difficulty distribution: {'EASY': 11, 'MEDIUM': 11, 'HARD': 11}. Correct-answer distribution: {'B': 8, 'D': 8, 'A': 9, 'C': 8}. Topic distribution: {'Figural series · rotation': 3, 'Figural series · progressive count': 3, 'Figural series · alternating attributes': 3, 'Figure matrix · rotation, mark and shading': 3, 'Reflection · mirror/water image': 3, 'Paper folding · one fold and two punches': 3, 'Figural analogy · rotation': 3, 'Figural classification · internal feature': 3, 'Embedded figure · segment containment': 3, 'Counting figures · triangles': 3, 'Dot situation · geometric region': 3}. All are Normal (`is_pyq=false`) with four distinct labeled options, one keyed correct answer, explanation, and local SVG. Correct choices are deterministically shuffled while retaining their complete visual state.

## Visual verification and limitations

Generated 33 SVG assets under `frontend/public/question-assets/non-verbal-reasoning/`. The builder creates each image alongside its question record. Rotation, progressive counts, alternating attributes, matrices, mirror/water reflections, fold/unfold positions, analogy, unique classification, embedded segment networks, triangle enumeration, and dot regions are defined by deterministic state rules. The option shuffle is deterministic and independently checked as an unordered four-choice multiset; the original correct visual state is confirmed at the new answer index. Source-derived items are not included because the supplied question cards display instructor solution annotations over the visual choices.

## Answer-position audit

Deterministic correct-key distribution: {'B': 8, 'D': 8, 'A': 9, 'C': 8}. Original option states and answer indexes are retained in the selected-question ledger for unordered set comparison. Each figure is moved as a complete state in its original diagram; the SVG is regenerated from the shuffled state specification.

## Source limitation

All 55 annotated source candidates remain rejected pending complete clean visual reconstruction and independent solve. Lectures 01 and 05 were not supplied. The bank contains original questions only.

## Live answer-key reconciliation

The balanced option order was applied to all diagrams with stable `nvr-###` IDs. A transaction rechecked each live UUID, exact stem, difficulty, image path, option labels, current correct key, explanation, chapter, and active Normal status before updating. Twenty-three questions moved to a new answer key, changing 46 `QuestionOption.is_correct` records. Twenty-five database explanation strings received answer-letter-reference-only edits; their reasoning was preserved. No wording, difficulty, asset, or unrelated chapter changed. All 33 database rows now match the canonical keys and explanations; two importer dry-runs reported 33 duplicates and zero inserts.

The answer-position comparison and per-question key map are in `non_verbal_reasoning_answer_position_reconciliation_report.md` and `.json`.

## Final verification

The focused CH-17 suite passes (5 tests); backend question-bank, test-session, and catalog regressions pass (102 tests). Python compilation and the frontend production build pass. Authenticated API checks report Easy 11, Medium 11, Hard 11, PYQ 0, and mixed Normal 33. The 10-question Hard session passed timer, save/reload, submit, score, and answer/explanation review checks. SVG static serving returned HTTP 200. The builder produced identical batch, ledger, report, and SVG SHA-256 hashes on two consecutive builds. Browser UI automation was not performed.
