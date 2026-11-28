# Banking Maths Set 9 - Frontend UI Verification

## Source change

Only `frontend/src/pages/BankingPage.tsx` was changed: 19 lines added after the
existing `"pipe-and-cistern-mains"` mapping, supplying the seven missing
frontend chapter-key mappings for Set 9. No Set 1-8 mapping was edited. The only
tracked diff in the repository is this file (`git diff --stat`: 1 file changed,
19 insertions).

## Fresh-client check

The production build passed (`npm run build`: `tsc -b && vite build`, 57 modules
transformed). The browser check used a fresh document at
`http://localhost:5173/banking` with cache bypass to avoid the stale-bundle
issue seen in Set 8. Authentication used a short-lived token signed with the
backend's real JWT settings for one active local user. The token was served
temporarily from `frontend/public/set9_ui_token.txt`, read by the page, and the
file was deleted immediately afterward. No token is recorded in this report or
any repository file.

## Banking Clerk / Math & Quant

All seven target chapters displayed **`120 questions · 4 parts`**:

- Pipe and Cistern - Data Interpretation
- Trains (Mains)
- Trains - Data Interpretation
- Boats and Streams (Mains)
- Boats and Streams - Data Interpretation
- Probability (Mains)
- Probability - Data Interpretation

## Banking PO / Math & Quant

The same seven chapters displayed **`120 questions · 4 parts`** under the
`Banking PO` exam.

## Result

Both exams show the expected counts and four parts for all seven Set 9 chapters.
The temporary token file is absent, the browser tab was closed, and the Git
status was rechecked after the UI check.
