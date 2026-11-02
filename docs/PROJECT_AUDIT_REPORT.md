# SSC Prep Platform — Project, Database and Git Audit

Audit date: 2026-11-02 (Asia/Calcutta)

## Follow-up verification — 2026-11-02

This update supersedes the earlier environment/database blockers below for the final Calendar/Series/Clock checks. The repository-local interpreter `backend/.venv-disease-import/Scripts/python.exe` launches Python 3.10.9 with SQLAlchemy, psycopg, pytest and FastAPI available. The separately checked `backend/.venv` still points to a missing Microsoft Store Python runtime. The configured PostgreSQL database is reachable.

Read-only live checks verified these active SSC → Reasoning chapters:

| Chapter | ID | Active Normal | Active PYQ | Total records | Easy / Medium / Hard |
|---|---|---:|---:|---:|---|
| Calendar (Recorded) | `12bc9994-13ee-4522-88c7-9a98371eb900` | 30 | 0 | 30 | 10 / 10 / 10 |
| Series | `782b2b35-1c76-47e6-9e26-73ed87f6b6bb` | 32 | 0 | 32 | 10 / 12 / 10 |
| Clock (Recorded) | `43e38225-b6f7-4fd0-a35b-cf2a75a86f7d` | 33 | 0 | 33 | 11 / 11 / 11 |

The Calendar canonical batch was verified against all 30 stored rows. Guarded dry-run reported 30 duplicates, zero planned inserts, rejects, or errors; the `--apply` path returned idempotently without changing records. Authenticated live API checks confirmed its catalog entry, 10-question availability at all three difficulties, zero PYQs, supported mixed-practice sizes, and the 30 question payloads. Focused Calendar/Series/Clock/importer tests passed (14 passed, one API fixture deselected), and catalog/session service regressions passed (15). Python compilation, `npm run build`, and `git diff --check` passed. A broader TestClient availability fixture did not complete in the test runner; equivalent authenticated live API checks succeeded. No browser flow was run.

The sections that follow preserve the earlier broad repository audit snapshot. Their claims that database access and Python dependencies were unavailable describe that earlier check; broader Maths chapter populations, migrations, security and deployment readiness remain unaudited in this follow-up.

## 1. Executive Summary

**Verified:** This is a React 18 + TypeScript + Vite frontend and a Python FastAPI + SQLAlchemy backend intended to use PostgreSQL. The frontend production build passed. A syntax-only parse passed for 192 Python files. The worktree contains pre-existing local changes, which were preserved.

**Not verified:** PostgreSQL is not reachable at the configured `localhost:5432`; the Python virtual environments refer to a missing Microsoft Store Python executable, and the available Python 3.10 lacks `psycopg` and `pytest`. Therefore no live chapter IDs, counts, difficulty distributions, active/inactive records, duplicate/invalid database findings, or backend test results can be responsibly reported. The three named Series PDFs are not present in the workspace search.

**Immediate blockers:** Restore a working database connection and Python test runtime to complete the live audit. Obtain/access the three Series PDFs before source-based question curation. No application or question-bank data was changed; this report is the only requested new file.

## 2. Verified Technology Stack

- **Frontend:** React 18, TypeScript, Vite 5, React Router 6, Tailwind CSS 3, PostCSS. NPM scripts provide dev, build, preview and TypeScript lint; there is no frontend test script in `frontend/package.json`.
- **Backend:** Python FastAPI, synchronous SQLAlchemy 2, Pydantic Settings, Alembic, PostgreSQL through psycopg v3. API routers cover health, auth, catalog, question management/import and test sessions.
- **Authentication:** Argon2 password hashing and signed JWT bearer tokens (`python-jose`). Protected backend routers/dependencies validate tokens and active users.
- **Database and migrations:** PostgreSQL schema is represented by SQLAlchemy models under `backend/app/models` and Alembic revisions under `backend/migrations/versions`. Runtime URL is loaded through `backend/app/config.py` from `backend/.env`; the checked-in example defaults to `localhost:5432/ssc_prep`. Alembic has a configured migration environment. No migration was run.
- **Frontend/backend communication:** Browser `fetch` API client calls `/api` (or `VITE_API_URL`); Vite dev server proxies `/api` to `http://localhost:8000`. Authenticated calls pass bearer JWTs.
- **Styling/build:** Tailwind utility classes and project CSS; `npm run build` runs `tsc -b && vite build`.
- **Development/deployment:** README describes local Vite and Uvicorn development. Vite proxy and CORS settings are local-development oriented. Repository search found no Docker Compose/Dockerfile, Procfile, Render, Vercel, Netlify or GitHub Actions deployment/CI configuration. **Deployment readiness is not established.**

## 3. Repository Structure

- `frontend/src`: React application, routes, layout, auth context, API clients and pages.
- `backend/app`: FastAPI entry point, routers, services, schemas, models, auth and database setup/catalog/seed modules.
- `backend/migrations`: Alembic environment and four numbered migration revisions.
- `backend/data`: verified question batch JSON, answer ledgers and review reports for many chapters.
- `backend/scripts`: chapter batch builders/importers, reviews and other utilities.
- `backend/tests`: pytest suite for auth, catalog, test sessions, importers and batch artifacts.
- `database/`, `question-bank/`, `docs/`: short READMEs and project documentation/import guide.
- `tmp/`: existing PDF review renders, extracted text, diagnostic scripts and logs; preserved.
- Root also contains the existing untracked `maximum_and_minimum_value_verified_batch.json`.

Important entry points include `frontend/src/App.tsx`, `frontend/src/routes/index.tsx`, `frontend/src/services/api.ts`, `backend/app/main.py`, `backend/app/routers/`, `backend/app/services/`, `backend/app/database/session.py`, and `backend/migrations/`.

## 4. Maths Chapter Status

Expected counts below come from the supplied audit request. **Live DB counts, IDs and integrity status are unverified because PostgreSQL is unavailable. Do not treat expected values as observed values.** The static catalog source is not a substitute for live records.

| Chapter | Chapter ID | Active total | Easy / Medium / Hard | Normal / PYQ | Inactive | Expected check | Duplicates / invalid |
|---|---|---:|---|---|---:|---|---|
| Compound Interest | Not queried | Not queried | Not queried | Not queried | Not queried | 90 expected; unverified | Not queried |
| Ratio & Proportion | Not queried | Not queried | Not queried | Not queried | Not queried | 90 expected; unverified | Not queried |
| Profit & Loss | Not queried | Not queried | Not queried | Not queried | Not queried | 90 expected; unverified | Not queried |
| Simple Interest | Not queried | Not queried | Not queried | Not queried | Not queried | 90 expected; unverified | Not queried |
| Average | Not queried | Not queried | Not queried | Not queried | Not queried | 90 expected; unverified | Not queried |
| Speed, Time & Distance | Not queried | Not queried | Not queried | Not queried | Not queried | 90 expected; unverified | Not queried |
| Discount | Not queried | Not queried | Not queried | Not queried | Not queried | 90 expected; unverified | Not queried |
| **Expected total** | — | **630 expected** | — | — | — | **Not DB-verified** | — |

## 5. Reasoning Chapter Status

| Chapter | Chapter ID | Active total | Easy / Medium / Hard | Normal / PYQ | Inactive | Expected check | Duplicates / invalid |
|---|---|---:|---|---|---:|---|---|
| Coding-Decoding | Not queried | Not queried | Not queried | Prior claim 54 Normal + 4 PYQ; unverified | Not queried | No expected total specified; unverified | Not queried |
| Alphanumerical Test | Not queried | Not queried | Not queried | Prior claim 30 Normal; unverified | Not queried | Unverified | Not queried |
| Analogy | Not queried | Not queried | Not queried | Prior claim 30 Normal; unverified | Not queried | Unverified | Not queried |
| Classification | Not queried | Not queried | Not queried | Prior claim 30 Normal; unverified | Not queried | Unverified | Not queried |
| Blood Relation | Not queried | Not queried | Not queried | Prior claim 30 Normal; unverified | Not queried | Unverified | Not queried |
| Mathematical Operations | Not queried | Not queried | Not queried | Prior claim 30 Normal; unverified | Not queried | Unverified | Not queried |

No chapter-level SQL query could be run. Existing JSON batches and answer-ledger files show local artifacts exist for these topics, but their contents do not prove what is currently active in PostgreSQL.

## 6. Remaining Chapters

**Live database inventory: blocked.** The database could not be queried, so this audit cannot list database chapter IDs, mark chapters empty/partial, or determine missing/inactive question records. No chapter is declared empty based on assumption.

The checked-in `backend/app/database/ssc_catalog.py` statically configures these remaining Reasoning chapters after the six named as completed: **Series, Syllogism, Dice, Sitting Arrangement, Puzzle, Venn Diagram, Direction and Distance, Ranking and Order, Word Building, Inequality, Non-Verbal Reasoning, Statement Based Questions, Insert the Missing Number, Decision Making, Calendar (Recorded), Clock (Recorded).** This is a source-code catalog listing, not a live database finding. It also lists further Maths chapters (including Percentage, Partnership, Age, Mixture, Alligation, Time & Work, Pipe & Cistern, Train, Boat & Stream, Data Interpretation, Race and Advanced Maths topics) and GK/GS and English chapters; their live population status is likewise unverified.

**Series specifically:** Static catalog includes a Reasoning chapter named `Series`, but its database ID, active status and question count could not be confirmed.

## 7. Series Chapter Readiness

- **Source PDFs:** `Series 01_.pdf`, `Series 02_.pdf` and `Series 03_.pdf` were not found by searching files in the current workspace. They are not accessible here under those names.
- **Database row/questions:** Not inspectable without PostgreSQL. Do not infer that the live chapter is empty.
- **Series-specific batch/ledger/importer/test:** No Series-named JSON batch, answer ledger, importer script or automated test was found in `backend/data`, `backend/scripts`, `backend/tests` or the workspace file search.
- **Reusable infrastructure exists:** `backend/app/services/question_import_service.py` validates CSV/JSON records, active subject/chapter association, non-empty question text and four options, a valid correct option, difficulty, PYQ metadata and field lengths; it scans for duplicate question text and supports dry-run/atomic import behavior. The authenticated management API exposes the importer. Existing per-chapter `*_verified_batch.json`, `*_answer_ledger.json`, build/import scripts and artifact tests establish patterns that could be reused. They do not constitute Series data or a Series test.
- **Needed before safe addition:** restore read-only DB visibility and verify the live Series chapter/records; make the three source PDFs available; agree/derive a canonical batch and separate answer ledger/review evidence following established formats; add Series validation/artifact tests; only then review any proposed import plan. No extraction or import was done.

## 8. Question Bank and Database Integrity

**Code inspection:** The question model separates difficulty (`EASY`, `MEDIUM`, `HARD`) from `is_pyq`, stores active state and options, and has a chapter/difficulty/PYQ/active index. Schema constraints include unique option keys per question. Generic importer validation requires A–D option text and a valid single correct-option label, and checks the selected active chapter/subject and PYQ metadata.

**Test-session code inspection:** Selection filters to active chapters and active questions, separates Normal/PYQ, optionally filters difficulty and validates MCQ option completeness. Sampling uses `SystemRandom().sample`, preventing duplicate IDs inside one attempt. Insufficient counts are reported as unavailable/conflict; Reasoning count choices require the configured standard counts. Correct answer and explanation are attached to result review, not the active-test question payload.

**Not verified:** Current database totals, all chapters, difficulty coverage, PYQ coverage, inactive rows, cross-row duplicates, malformed database records, orphaned data, and any difference between source batches and stored records. The server was unavailable and the local Python installation lacks the PostgreSQL driver.

## 9. Frontend Functionality

- **Code inspection:** Routes exist for landing, sign-up, login, dashboard, SSC selection, test session and results. Protected routes wrap dashboard/practice/test/result pages. SSC flow code provides exam, subject, chapter/category, source/difficulty and question-count selection. Test page supports previous/next and question palette navigation, timer display, answer saving and submission. Results page displays score/counts, correct/incorrect answers and explanations/review.
- **Automated test evidence:** No frontend test runner or test script is configured, so browser behavior was not independently verified. `npm run build` did compile the TypeScript project successfully.
- **Not verified:** Runtime against live API/database, real browser interaction, refresh/resume behavior and end-to-end auth/test flows.

## 10. Backend Functionality

- **Code inspection:** FastAPI routers expose health/auth/catalog/question/test APIs. Test service creates user-owned attempts, stores selected question order, saves answers, finalizes on submit/timeout, computes +2/−0.5/0 score and serves review details. Protected test and question-management routes require a bearer user; question management also has admin checks where applicable.
- **Automated test sources:** `backend/tests/test_auth.py`, `test_catalog.py`, `test_question_bank.py`, and `test_test_sessions.py` plus chapter artifact/import tests cover auth, catalog, selection, partial-pool behavior, session lifecycle and review. They were not executed in this audit.
- **Not verified:** API startup, DB-backed request behavior, migrations/schema compatibility and live import behavior.

## 11. Authentication and Security Observations

- Password hashing uses Argon2; JWTs carry subject, issued-at and expiry claims; protected routes resolve an active user from the token.
- Frontend persists the bearer token in browser storage (see `frontend/src/services/auth.ts`) and clears it locally at logout. There is no server-side token revocation endpoint; a copied JWT remains valid until expiration unless its user is deactivated or the signing key changes.
- The checked-in `.env.example` contains a placeholder secret and local CORS origin. Production secret management, HTTPS/reverse-proxy behavior, deployment CORS and operational controls were not verified. The real `.env` secret is intentionally not reproduced in this report.
- Auth unit/API tests exist but did not run because pytest/runtime dependencies are unavailable.

## 12. Test and Build Results

| Check | Result | Evidence / reason |
|---|---|---|
| Frontend production build | **PASS** | `npm run build`: `tsc -b` and Vite production bundle completed; 52 modules transformed. |
| Frontend tests | **Not available** | `frontend/package.json` has no test script or test runner. |
| Backend focused pytest suite | **Not run** | Project `backend/venv` and `backend/.venv` both point to missing `...WindowsApps/PythonSoftwareFoundation.Python.3.11.../python.exe`; available Python 3.10.9 has no pytest. No dependencies were installed. |
| Backend syntax parse | **PASS (syntax only)** | Python 3.10.9 AST-parsed 192 files under `backend/app`, `backend/tests`, `backend/scripts`; 0 syntax errors. Does not verify imports/runtime. |
| PostgreSQL connection | **BLOCKED** | Configured host `localhost`, port `5432`, database `ssc_prep`; TCP checks failed. The available Python 3.10 also lacks `psycopg`. |
| `git diff --check` | **PASS with Git line-ending notices** | No whitespace errors; Git warned modified LF files would be converted to CRLF on a future Git touch. |
| Migrations/importers | **Not run** | Explicitly excluded from this audit. |

## 13. Git Working Tree Status

Read-only Git checks at audit time:

- Branch: `main`.
- Latest commits: `2434aa7 feat: add verified reasoning question banks`; `077e335 fix(math): reconcile verified question bank artifacts`; `45cface feat(math): add Advanced Maths question banks`; `e4ba160 feat(math): add verified arithmetic question banks`; `447db14 feat: add verified alligation, mixture, partnership, and pipe-cistern question banks`.
- Modified tracked files: `backend/app/services/test_service.py` (+38/−4), `backend/tests/test_test_sessions.py` (+88), `frontend/src/pages/SSCPage.tsx` (+13/−12). Diff summary: 139 insertions, 16 deletions. Code context suggests test-pool/count selection changes, not question-bank content; attribution/intent is unknown and the changes were left untouched.
- Existing untracked files: `backend/check_db.py`, `maximum_and_minimum_value_verified_batch.json`, and `tmp/` (including many diagnostic scripts, logs, extracted PDF text and rendered images). Preserved.
- `git diff --check`: no whitespace errors. It emitted only LF-to-CRLF working-copy warnings for the three modified files.
- `git status` before writing this report did not include this report. Creating the requested report adds `docs/PROJECT_AUDIT_REPORT.md` as a new file; no other worktree changes were made by this audit.

## 14. Disk Space and Environment Issues

- Python available: Python 3.10.9 at `C:\Users\shikh\AppData\Local\Programs\Python\Python310\python.exe`; `python`/`py` Windows Store aliases are broken. The two main project venv configs identify Python 3.11.9 under a missing WindowsApps path.
- Python test/DB packages: `pytest` and `psycopg` unavailable to the usable Python 3.10; no install attempted.
- Node: v24.22.1. npm: 11.19.1. Existing `frontend/node_modules` supports the successful build.
- PostgreSQL: no listener at localhost:5432; configured credentials exist in local environment configuration but are not included here.
- Workspace drive C: about 6.87 GiB free at inspection (7,367,047,424 bytes).
- Repository footprint: about 1.31 GiB (1,404,388,209 bytes) across files at inspection. Approximate large directories: `.git` 408 MiB, `backend` 381 MiB, `frontend` 160 MiB, `tmp` 391 MiB. `tmp/` contains extensive retained PDF render/review output. No cleanup was performed; these sizes indicate storage usage, not a confirmed storage failure.

## 15. Known Bugs and Risks

- **Confirmed audit blocker:** Live PostgreSQL data cannot be audited while the configured service is unavailable.
- **Confirmed verification blocker:** Backend pytest and DB driver unavailable in usable Python; both main project virtual environments refer to a missing Python executable.
- **Confirmed Series input gap:** The three named PDFs were not found in this workspace.
- **Risk, not a proven defect:** Local JWT storage and lack of revocation mean token logout is client-side only until token expiry.
- **Risk, not a proven defect:** No deployment/CI configuration was found in the repository; production deployment and security posture remain unverified.
- **Unknown:** Whether any live chapter has duplicates, invalid options, partial difficulty coverage, inactive rows or a count mismatch. No such issue should be asserted without database access.

## 16. Recommended Development Roadmap

- **P0 — Restore audit/development verification:** Start/restore PostgreSQL at the configured host or provide the intended connection through a safe local config; restore a valid Python runtime/venv and install only through the project’s normal setup after authorization. Re-run the read-only chapter integrity query and focused tests once dependencies and DB are available. Preserve all current worktree changes.
- **P1 — Complete Series safely:** Make `Series 01_.pdf`, `Series 02_.pdf`, `Series 03_.pdf` accessible; confirm the live Series chapter and existing records; prepare reviewed canonical batch, answer ledger, importer and artifact tests using existing conventions. Import only in a separately authorized development step after review.
- **P2 — Remaining Reasoning chapters:** After confirming live deficits, prioritize the configured chapters: Series, Syllogism, Dice, Sitting Arrangement, Puzzle, Venn Diagram, Direction and Distance, Ranking and Order, Word Building, Inequality, Non-Verbal Reasoning, Statement Based Questions, Insert the Missing Number, Decision Making, Calendar (Recorded), Clock (Recorded). Validate target counts/levels with the owner before assuming a universal count.
- **P3 — Remaining platform improvements:** Use the live inventory to sequence the other configured Maths, GK/GS and English deficits; add frontend automated/e2e tests; review token revocation/storage and production CORS/secret handling.
- **P4 — Final testing and deployment:** Run full backend and frontend suites, database migration compatibility checks against a disposable/staging database, production build and deployment/security smoke checks; document repeatable CI/deployment setup before release.

---

**Evidence labels:** “Verified” means observed from files or command output during this audit. “Code inspection” means behavior was inferred from implementation without executing that workflow. “Not verified” means no live/runtime evidence was available. No expected count or static catalog entry in this document is presented as a database measurement.
