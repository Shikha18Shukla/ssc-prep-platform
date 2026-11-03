# CH-20 Decision Making review

## Source review

Visually reviewed all 46 scanned pages: Decision Making 01 Class Notes.pdf (26 pages) and Decision Making 02 _ Class Notes.pdf (20 pages). Page-by-page decisions are in `decision_making_source_review.json`.

Accepted source-derived questions: 26; original questions: 8; rejected source candidates: 4.

Rejected source questions: Decision Making 01 Class Notes.pdf p.14: The supplied choice jumps directly to contempt without describing the conduct, applicable procedure, warning, or severity; no proportionate single action can be verified.; Decision Making 01 Class Notes.pdf p.18: The relationship alone does not establish the colleague's conduct or justify arrest; source options encourage guilt by association and arbitrary punishment.; Decision Making 01 Class Notes.pdf p.19: Options do not provide a clearly safe, proportionate response; direct confrontation, gathering a crowd, or leaving the women without support all carry unresolved risks.; Decision Making 01 Class Notes.pdf p.20: ‘Ethical facilities’ and the alleged deprivation are undefined, leaving the responsible procedure and appropriate remedy unclear.

## Question bank

Total: 34 active Normal questions; 0 PYQs.

Categories: SITUATIONAL=16, ELIGIBILITY=18

Difficulty: EASY=11, MEDIUM=12, HARD=11

Correct-answer positions: D=8, A=9, C=8, B=9

## Independent verification

All 16 candidate cases are independently evaluated by evaluate_candidate using per-question criteria, exact reference dates, calendar-age calculation, completed calendar months, and exact-failure referral exceptions. Boundary and exception tests are in test_decision_making_verified_batch.py.

Every selected action was re-evaluated against the stated context for safety, rights, proportionality, procedure, and escalation. Four underspecified or unsafe source situations were rejected.

Exact and high-similarity screening is applied by the guarded importer against live active Reasoning questions and canonical batches; the source cases were manually compared for duplicate scenarios and decision logic.

## Import and application verification

Live database import: 34 imported, 0 rejected, 0 duplicates. Final active Normal=34, PYQ=0; difficulty counts Easy=11, Medium=12, Hard=11. Replay dry-run: 34 duplicates, 0 inserts. Other chapter IDs remained unchanged.

Authenticated live API: chapter appears under Reasoning; Easy/Medium/Hard availability is 11/12/11 for a 10-question request; PYQ availability is 0. Mixed Normal pool reports 34. Returned questions include four options and explanations. TestClient exam-session flow passed save/reload, submission, scoring, and answer/explanation review.

Verification: CH-20 focused tests 9 passed; targeted backend regression 111 passed; full backend suite 409 passed in 630.46s. Python compilation, git diff --check, and frontend production build (Vite 5.4.21) passed. No browser UI verification was performed.
