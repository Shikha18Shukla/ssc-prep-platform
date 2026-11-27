# Authentication Replacement — Final Report

**Date:** 2026-11-28
**Scope:** Local workspace only. No staging, commit, push, `.env` modification, hosted-database connection, or production deployment was performed.

## 1. Objective and outcome

The invitation-code/beta-access login system was replaced with:

- Email/password registration and login.
- Argon2id password hashing and revocable server-side sessions.
- A real Google OAuth 2.0 authorization-code flow with PKCE, state/nonce validation, and server-side JWKS verification.
- Secure password setup/recovery tokens with explicit `EMAIL_PROVIDER=none` behavior.
- A preserved local database: existing users, IDs, hashes, attempts, answers, results, rotations, and history were not changed.

All code, migration, documentation, and validation work is complete in the working tree. Google sign-in and password-recovery email delivery are implemented but **not operationally verifiable locally** because no Google credentials or SMTP provider were configured.

### Integration review follow-up

A read-only integration review of authentication and the three-section Banking flow found several genuine gaps. All were fixed narrowly and covered by regression tests:

- Inactive accounts with a correct password returned `403 User account is inactive`; login now returns the same `401 Invalid email or password` as every other credential failure.
- The Google browser cookie could expire before the exchange code it had to authorize. Its lifetime now covers `GOOGLE_STATE_TTL_SECONDS + GOOGLE_EXCHANGE_TTL_SECONDS`.
- A concurrent Google signup race could raise a raw `IntegrityError`/500. User creation and identity linking are now guarded together, with recovery by stable `sub` and then by verified email.
- When both email and Google were unconfigured, the reset response still suggested Google sign-in. The fallback now says `Contact an administrator` unless Google is actually configured.
- Google callback errors now always redirect to the configured SPA error page instead of exposing a raw JSON/429/500 response to the browser.
- Fixed-section availability preflight now passes the required `question_count`, so an underfilled section fails before test creation.
- Three-section selection now applies the same option-validity rules as availability, so malformed imported options cannot be served.
- Switching exam/subject now clears stale mode and question-count choices in the Banking UI.
- New tests cover inactive-login uniformity, missing Google fallback honesty, cookie lifetime, tampered ID-token signature, unknown `kid`, runtime redirect-URI mismatch, concurrent Google signup, and malformed three-section options.

## 2. Backend implementation

### Removed

- Invitation-code fields, schemas, services, routes, middleware, admin utilities, tests, exports, and model files.
- `beta_access` model and invitation-related operations from active application code and deployment examples.
- Stale invitation checks from `neon_beta_db.py`, `import_beta_content.py`, and `plan_beta_content_import.py`.

Historical migration files (`0008`, `0009`) and prior reports retain their original wording as immutable history. `BETA_CATALOG_SCOPE` remains intentionally as a catalog-visibility setting, not an access-control gate.

### Added / rewritten

| Area | Result |
| --- | --- |
| `app/auth/security.py` | JWTs with `iss`, `aud`, `sub`, `jti`, `iat`, `exp`, explicit HS256 allowlist; `create_access_token(...) -> str`. |
| `app/auth/dependencies.py` | Validates signed tokens; treats `AuthSession` as optional for trusted tokens, but any existing row is authoritative for revocation/expiry. |
| `app/schemas/auth.py` | Signup/login/reset/Google exchange schemas; output schemas never expose hashes, tokens, or provider secrets. |
| `app/services/auth_service.py` | Argon2id hashing, normalized-email uniqueness, safe login errors, session issuance/revocation, hashed reset tokens. |
| `app/services/google_auth_service.py` | Authorization-code exchange, PKCE, state/nonce consumption, JWKS signature/issuer/audience checks, verified-email enforcement, stable `sub` identity, account linking. |
| `app/services/email_service.py` | Honest `none` provider and optional SMTP delivery. |
| `app/routers/auth.py` | Register, login, logout, `/me`, Google start/callback/exchange, password-reset request/confirm with database-backed rate limits. |
| `app/routers/admin.py` | Session revocation and account activation controls; regular users cannot access admin endpoints. |
| `app/models/auth_state.py` | `AuthSession`, `OAuthIdentity`, `OAuthState`, `OAuthExchangeCode`, `PasswordResetToken`, and migrated `RateLimitWindow`. |
| `app/models/user.py` | Nullable Argon2id hash, `email_normalized`, `password_changed_at`, `has_password`. |
| `app/config.py` | Google, email/SMTP, cookie, JWT, CORS, forwarded-proxy, and production validators. |
| `migrations/versions/0012_auth_replacement.py` | Linear upgrade from `0011_current_affairs_sections` to `0012_auth_replacement`. |

Security properties verified in code and tests:

- Passwords are stored only as Argon2id hashes; plaintext and hashes are never returned by the API.
- Login returns uniform `Invalid email or password` for unknown users, bad passwords, disabled accounts, and no-password accounts.
- Registration rejects duplicate normalized emails with a non-enumerating but clear `An account with this email already exists` response.
- JWTs are short-lived and revocable by `jti`; logout revokes only the current session, while password reset and admin deactivation revoke all sessions for a user.
- Google secrets, tokens, state, nonces, PKCE verifiers, and opaque exchange codes remain server-side. The browser receives only an authorization URL and a short-lived opaque exchange code, never an access/ID token.
- Password reset tokens are hashed at rest, single-use, time-limited, and revoked after use. With `EMAIL_PROVIDER=none`, the API explicitly says email delivery is not configured and does not claim a message was sent.

## 3. Frontend implementation

- Rewrote `services/auth.ts` and `context/AuthContext.tsx` for email/password, Google, and reset flows.
- Updated `LoginPage`, `SignupPage`, routes, navigation, and `User` type.
- Added `GoogleButton`, `ForgotPasswordPage`, `ResetPasswordPage`, and `GoogleCallbackPage`.
- Removed `AdminInvitationsPage` and `adminInvitations.ts`.
- Preserved session storage keys `ssc_prep_access_token` and `ssc_prep_session_user`; no refresh token is issued.
- Added loading/disabled states and repeated-submission guards.
- Preserved protected routes, dashboard, test navigation, Banking, three-section chapters, and Maths four-part chapter flows.

## 4. Migration and data preservation

### Pre-migration safeguards

- Local database revision before migration: `0011_current_affairs_sections`.
- A baseline snapshot was saved outside the repository before any schema change.
- A custom-format backup was created and verified; `pg_restore --list` confirmed 122 TOC entries. Backup files are not committed.
- Validation was performed on a restored disposable database before the live local database was migrated.

### Scratch validation

Migration `0012_auth_replacement` was applied to the restored scratch copy first. Result:

- Head advanced to `0012_auth_replacement`.
- Counts unchanged: 3 users, 69 attempts, 2,797 test questions, 272 answers, 4 rotations, 92 history rows.
- User identity digest unchanged.
- Completed-attempt totals unchanged: 34 completed, score sum `89.0`, correct `90`, wrong `182`, unanswered `390`.

### Live local application

The same migration was then applied to `ssc_prep`. Final comparison:

| Check | Before | After | Result |
| --- | --- | --- | --- |
| Alembic head | `0011_current_affairs_sections` | `0012_auth_replacement` | Advanced |
| Users | 3 | 3 | Unchanged |
| Test attempts | 69 | 69 | Unchanged |
| Test questions | 2,797 | 2,797 | Unchanged |
| User answers | 272 | 272 | Unchanged |
| Chapter rotations | 4 | 4 | Unchanged |
| Question history | 92 | 92 | Unchanged |
| User identity/hash digest | `ae01e949…dadf2` | `ae01e949…dadf2` | Unchanged |
| Completed totals | 34 / 89.0 / 90 / 182 / 390 | 34 / 89.0 / 90 / 182 / 390 | Unchanged |

No hosted or production database was contacted. The `.env` file was not modified.

Final local auth-schema state after browser smoke cleanup: head `0012_auth_replacement`, 3 users, 0 auth sessions, 0 OAuth identities, 0 password-reset tokens, and no smoke-test account remaining.

## 5. Validation

### Commands and results

| Validation | Result |
| --- | --- |
| `python -m compileall -q app migrations/versions/0012_auth_replacement.py` | Passed, no output. |
| Scoped auth suite: `tests/test_auth.py tests/test_google_auth.py tests/test_production_controls.py` | **50 passed**, 1 warning in 10.15s (pre-hardening). |
| Targeted integration suite: `tests/test_auth.py tests/test_google_auth.py tests/test_production_controls.py tests/test_banking_three_sections.py tests/test_test_sessions.py` | **134 passed**, 1 warning in 102.95s (0:01:42), after all hardening changes. |
| Full backend suite: `python -m pytest -q tests` | **477 passed**, 1 warning in 1574.33s (0:26:14), after the auth replacement and before the narrow integration fixes; not rerun because the later changes are covered by the targeted suite. |
| Frontend `npm run build` (`tsc -b && vite build`) | Passed; 57 modules transformed; final confirmation built in 35.83s after the Banking UI fix. |
| Frontend invitation-reference grep | No active invitation references in `frontend/src`. |
| Active backend invitation-reference grep | No invitation/access-code references in active `app` code; remaining occurrences are historical migration/reports only. |
| Git staging check at verification time | No staged changes; no commit or push. |

### Backend coverage highlights

- Password hashing, JWT claims, expiry, invalid/wrong-issuer/wrong-audience rejection.
- Registration session issuance, hidden secrets, no admin escalation, normalized duplicate rejection, validation rules.
- Uniform login failures, inactive/no-password rejection, login success.
- `/me` acceptance/rejection, current-session-only logout.
- Reset request honesty, hashed-token storage, delivery-once behavior, expiry, single use, and no user enumeration.
- Admin deactivation and session revocation, non-admin denial, last-admin protection.
- Database rate limits, production CORS, complete Google/email config validation.
- Google state/nonce/PKCE, signed ID-token verification, bad nonce/email/issuer/audience rejection, tampered signature and unknown `kid` rejection, runtime redirect-URI mismatch rejection, user creation, linked-identity login, verified-email account linking, concurrent same-email signup recovery, unverified-email rejection, single-use callback/exchange, browser binding, cookie/exchange lifetime overlap, and no token in redirects.
- Three-section Banking availability/count checks, deterministic 10/15 selection, malformed-option exclusion, and test-session answer/submit coverage.

### Browser smoke checks

Run against a local Vite dev server with the backend started using a process-only database override:

```powershell
cd backend
# supply DATABASE_URL through the process environment for an isolated local database
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Verified in the in-app browser:

- `/api/health` returned `200 healthy`; `/api/ready` returned `200 ready` at head `0012_auth_replacement`.
- `/login`, `/signup`, `/forgot-password`, `/reset-password`, and `/auth/google/complete` routes render.
- Signup form client validation; successful signup issued a session, stored only in `sessionStorage`, and redirected to `/dashboard`.
- Duplicate signup with mixed-case email returned `409 An account with this email already exists`.
- Invalid login returned uniform `Invalid email or password` (`401`).
- Successful login restored the previously requested protected route (`/banking`).
- Google button visibly reads **Continue with Google**; with no credentials configured it safely reported `Google sign-in is not configured` (`503`) and exposed no URL/token.
- Forgot-password flow reported that email delivery was not configured and never displayed a token. After the integration review, a regression test verifies the message is `Email delivery is not configured. Contact an administrator.` when Google is also unconfigured.
- Invalid reset token produced `Invalid or expired password setup link` (`400`).
- Dashboard, Practice, Banking Clerk subject list, English three-section chapters, Maths four-part chapters, and Current Affairs Tests 1–6 rendered.
- Sign-out cleared browser storage, returned `200` from logout, and the previously issued token then returned `401` from `/api/auth/me`, proving revocation.
- No console errors except expected intentional negative-path requests (401 revoked token, 409 duplicate signup). No auth token, reset token, client secret, password, or Google code appeared in frontend URLs or responses observed during smoke testing.

The temporary browser-smoke account `auth-smoke-20261128@example.com` was removed after testing; the final data-integrity comparison still shows exactly the original three users and unchanged data.

## 6. Setup documentation

- `docs/GOOGLE_OAUTH_SETUP.md` documents Google Cloud credential creation, exact redirect URI requirements, server-side-only variables, flow sequence, identity/linking behavior, and end-to-end verification steps.
- `docs/PRODUCTION_READINESS.md` was rewritten for the current auth system, required environment variables, deployment checklist, rollback guidance, and explicit honesty about unconfigured Google/SMTP.

Deployment examples were updated:

- `backend/.env.example`
- `backend/.env.production.example`
- `render.yaml`

No real credentials were invented or written to the repository.

## 7. Known limitations and honesty notes

- Google OAuth code is complete and unit-tested with a stubbed provider/JWKS, but no real Google client ID/secret/redirect was configured locally. Therefore, no successful live Google sign-in can be claimed.
- Password recovery is implemented and tested, but `EMAIL_PROVIDER=none` locally means no email was sent. No successful SMTP delivery can be claimed.
- The workspace `backend/.env` still points at a database at revision `0009_generic_beta_invites` without `questions.section` or auth-session tables. Per the stated constraint it was not modified; all local backend checks used a process-only `DATABASE_URL` override to `ssc_prep` at head `0012_auth_replacement`. Any future run that relies on the workspace `.env` must first point it at a migrated database.
- The short-lived bearer token remains in `sessionStorage`; it is not HttpOnly. This is the documented tradeoff already used by the frontend. XSS prevention/CSP still matters in production.
- The post-auth-replacement full suite completed successfully: `477 passed, 1 warning in 1574.33s (0:26:14)`. No test failed. After the integration fixes, the targeted suite passed `134 passed, 1 warning in 102.95s`; the full suite was not rerun because those changes are covered by the targeted tests.

## 8. Repository state

When verification completed, no `git add`, `git commit`, or `git push` had been performed; all changes remained in the working tree and the staging area was empty. The unrelated untracked scratch scripts and backups were deliberately left out of the publication scope.

### Files changed during the integration-review hardening phase

- `backend/app/services/auth_service.py`
- `backend/app/routers/auth.py`
- `backend/app/services/google_auth_service.py`
- `backend/app/services/test_service.py`
- `backend/tests/test_auth.py`
- `backend/tests/test_google_auth.py`
- `backend/tests/test_banking_three_sections.py`
- `frontend/src/pages/BankingPage.tsx`
- `reports/authentication_replacement_final_report.md`

Earlier implementation files for the auth replacement and three-section Banking work are listed in sections 2–6 and remain in the working tree. No hosting, staging, or production file was changed.
