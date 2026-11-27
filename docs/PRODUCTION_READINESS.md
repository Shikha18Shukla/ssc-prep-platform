# Production Readiness Guide

This guide describes the current application configuration and the controls that must be verified before public traffic. It does **not** claim that provider accounts, secrets, email delivery, Google OAuth credentials, monitoring, backups, or a production deployment have been configured.

## Current implementation state

### Authentication

- Signup accepts full name, email, password, and password confirmation. Emails are normalized for uniqueness; the original email text is preserved on the account.
- Passwords are stored only as Argon2id hashes. Password hashes, reset tokens, provider tokens, and client secrets are never returned by the API or written to frontend code.
- Login verifies the stored hash, rejects disabled and no-password accounts, and returns uniform `Invalid email or password` failures for unknown accounts and bad credentials.
- Access tokens are short-lived JWTs with `iss`, `aud`, `jti`, `iat`, `exp`, `sub`, and an explicit algorithm allowlist. Each token has a server-side `AuthSession` row that logout, password changes, and admin deactivation revoke.
- Google sign-in uses the authorization-code flow with server-generated state, nonce, PKCE, HttpOnly browser binding, server-side ID-token signature/issuer/audience verification, and verified-email enforcement. The stable Google `sub` is the identity key; a verified matching email links to an existing account instead of creating a duplicate. See `docs/GOOGLE_OAUTH_SETUP.md`.
- Password setup/recovery tokens are hashed at rest, single-use, time-limited, and revocable. With `EMAIL_PROVIDER=none`, the API explicitly reports that email delivery is not configured and never claims a message was sent.
- Rate limits cover registration, login, password setup, and each Google step, using database-backed atomic counters.

### Data preservation

- Migration `0012_auth_replacement` follows `0011_current_affairs_sections` and is the current Alembic head.
- It adds normalized email and password metadata, creates session/OAuth/reset tables, and removes the obsolete access-control tables only after confirming they contain no outstanding records.
- User IDs, original emails, Argon2id hashes, attempts, attempt questions, answers, rotations, history, and result totals are preserved. Provider-only accounts with no local password are supported.

### Catalog and learning flows

- `BETA_CATALOG_SCOPE=true` remains an intentional catalog-visibility setting. It hides unapproved content from API selection without deleting stored question-bank rows.
- Protected dashboard/test routes, test creation/submission/result/review/history, Banking flows, Clerk/PO content, three-section chapters, and Maths Sets 1–6 regressions remain covered by the backend suite and must be smoke-tested after deployment.

## Required configuration

Set all secrets through the deployment secret manager. Do not copy a populated `.env` into source control.

| Variable | Required value / behavior |
| --- | --- |
| `ENVIRONMENT` | `production` |
| `DEBUG` | `false` |
| `DATABASE_URL` | Managed PostgreSQL URL with `sslmode=verify-full` or equivalent |
| `SECRET_KEY` | Unique random value of at least 32 characters |
| `ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | 5–60 |
| `JWT_ISSUER`, `JWT_AUDIENCE` | Stable application identifiers; tokens with other values are rejected |
| `CORS_ORIGINS` | JSON list of exact HTTPS frontend origins |
| `BETA_CATALOG_SCOPE` | `true` |
| `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REDIRECT_URI` | Either all set or all unset; redirect must be the exact HTTPS backend callback |
| `GOOGLE_SUCCESS_REDIRECT_URL` | Exact HTTPS frontend callback route when Google is enabled |
| `GOOGLE_COOKIE_SECURE`, `GOOGLE_COOKIE_SAMESITE` | `true` and `none` when Google is enabled across origins |
| `EMAIL_PROVIDER` | `none` (no mail sent) or `smtp` |
| `PASSWORD_RESET_URL` | Exact HTTPS frontend reset route; required when SMTP is enabled |
| `SMTP_HOST`, `SMTP_USERNAME`, `SMTP_PASSWORD`, `SMTP_FROM_EMAIL` | Required when `EMAIL_PROVIDER=smtp` |

Google sign-in must not be represented as operational until real Google credentials are configured and an end-to-end test succeeds. Password recovery must not be represented as delivered until an email provider is configured and delivery is verified.

## Deployment checklist

1. Create an isolated staging database and restore the verified pre-release backup into it.
2. Run `alembic upgrade head` as a controlled release step; do not auto-run migrations in every worker.
3. Confirm `/api/health` and `/api/ready`; readiness requires the database to be at head `0012_auth_replacement`.
4. Verify signup, duplicate-email rejection, login, logout revocation, `/api/auth/me`, and disabled-account behavior.
5. If Google is enabled, complete the setup in `docs/GOOGLE_OAUTH_SETUP.md` and test authorization, callback, account linking, and single-use exchange from a clean browser session.
6. If SMTP is enabled, request a recovery link, confirm delivery, verify expiry and single use, and confirm old sessions are revoked.
7. Smoke-test dashboard navigation, catalog selection, test creation, answer saving, submission, results, history, Clerk/PO content, three-section chapters, and Banking Maths Sets 1–6.
8. Check browser console/network logs for token leakage, mixed content, CORS failures, and CSP violations.
9. Configure external uptime checks and alerts. Never attach auth headers, passwords, reset tokens, client secrets, or full request bodies to monitoring events.

## Rollback

Prefer rolling back the application image while leaving additive schema in place. Do not automatically run `alembic downgrade` in a failed deploy. Downgrade from `0012_auth_replacement` is intentionally refused when provider-only accounts exist and would otherwise discard session/OAuth/reset state.

## Local verification already performed

Before the local production-grade schema change, a custom-format backup was created outside the repository, its table of contents was verified, and it was restored into a disposable database. Migration `0012_auth_replacement` was applied to that restored copy and then to the live local database. In both cases the three existing user IDs and Argon2id hashes, 69 attempts, 2,797 attempt questions, 272 answers, 4 rotations, 92 history rows, and all completed-result totals were unchanged. Backup files are not committed.
