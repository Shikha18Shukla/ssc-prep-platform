# Controlled Public Beta Operations Guide

This guide describes the Render Static Site + Render Free Web Service + Neon Free architecture prepared for a time-limited, non-commercial beta. It does not mean that provider accounts, services, a Neon database, secrets, monitoring, backup policy, or deployment have been configured. No deployment, production database change, or paid infrastructure action is authorized by this document.

## Readiness state

### Implemented in the application

- Alembic migrations `0006_user_question_rotation`, `0007_question_rotation_modes`, and `0008_beta_access_and_rate_limits` form a linear chain after `0005_question_images`.
- PostgreSQL-backed, atomic fixed-window request counters are shared by all API workers. Login has per-IP and per-email limits; registration, test creation, answer save, submit, and admin actions also have limits. A gateway/WAF limit is still recommended to absorb traffic before it reaches PostgreSQL.
- Production registration requires an unredeemed invitation bound to the same normalized email. Invitation codes are random, stored only as SHA-256 digests, returned once to an admin, and expire after 14 days by default (admin may choose up to 30 days). Existing accounts remain usable and count toward the 200 account limit. Pending invites reserve capacity. The 200 limit is enforced under a database row lock.
- Admin APIs create/revoke invitations, view capacity, and activate/deactivate accounts. Deactivation is checked on authenticated requests, so a disabled user's existing access token stops working. At least one active admin must remain.
- Passwords use Argon2id; unknown-user logins perform a dummy hash verification. Access JWTs expire after 30 minutes by default (production accepts 5–60 minutes); there is no refresh-token flow. Frontend tokens are held in `sessionStorage`, with a one-time migration from legacy `localStorage`; both are readable by same-origin JavaScript, so preventing XSS remains important.
- Production config validates a strong non-placeholder signing key, explicit HTTPS CORS origins, PostgreSQL TLS, invitations and catalog scope. `/api/health` is process liveness; `/api/ready` also checks database reachability, the expected Alembic head, and beta capacity setup.
- Production API errors return a generic message and request ID. Logs include request ID, route, exception type, and sanitized stack locations, not exception messages, request bodies, credentials, or local variables. Production API docs are disabled.
- The beta catalog scope exposes the 31 Maths, 22 Reasoning, and 28 Science chapters previously verified in the configured database. Other SSC categories/chapters are hidden from the production catalog and question selection. This is an API catalog scope, not a change to or deletion of stored question-bank records.
- Backend and frontend container recipes run as unprivileged users and contain health checks. The backend does not run migrations at process startup.

### Prepared configuration, not yet provisioned

Portable container recipes and environment templates are available alongside the Render-specific Blueprint. `requirements-prod.lock` freezes the runtime dependencies. For other providers, the backend container and frontend static bundle can be used with the ingress pattern below.

### Owner action still required

Create the Render and Neon accounts/projects; choose whether to use the generated Render URLs or a custom domain; set secrets and the exact API/frontend origins; create an isolated staging database; seed only approved beta question/catalog data; bootstrap an administrator; stage and smoke-test the release; configure external monitoring; test backups; and run the 10/25/50/70-user workload. No backup, alert integration, external uptime monitor, restore rehearsal, production image build, or load test is claimed complete. Account count limit does not establish concurrent-user capacity.

## Beta content scope

| Section | Chapters exposed |
| --- | ---: |
| Maths (Arithmetic + Advanced) | 31 |
| Reasoning | 22 |
| General Science under GK/GS | 28 |
| **Total** | **81** |

Production must set `BETA_CATALOG_SCOPE=true`. The database may contain additional categories or incomplete chapters; the application scope hides them without modifying question records.

## Files

Deployment and runtime:

- `backend/Dockerfile`, `backend/.dockerignore`
- `backend/requirements-prod.lock`
- `backend/.env.production.example`
- `frontend/Dockerfile`, `frontend/.dockerignore`
- `frontend/.env.production.example`
- `frontend/nginx.conf`, `frontend/security-headers.conf`

Application controls and migrations:

- `backend/app/config.py`, `backend/app/main.py`
- `backend/app/auth/security.py`
- `backend/app/database/session.py`
- `backend/app/models/beta_access.py`, `backend/app/models/__init__.py`
- `backend/app/routers/admin.py`, `backend/app/routers/auth.py`, `backend/app/routers/health.py`, `backend/app/routers/tests.py`
- `backend/app/schemas/auth.py`
- `backend/app/security/rate_limit.py`
- `backend/app/services/auth_service.py`, `backend/app/services/beta_scope.py`, `backend/app/services/catalog_service.py`, `backend/app/services/test_service.py`
- `backend/migrations/versions/0006_user_question_rotation.py`, `0007_question_rotation_modes.py`, `0008_beta_access_and_rate_limits.py`
- `backend/tests/test_production_controls.py`
- `frontend/src/context/AuthContext.tsx`, `frontend/src/pages/HomePage.tsx`, `frontend/src/pages/SignupPage.tsx`, `frontend/src/pages/SSCPage.tsx`, `frontend/src/pages/DashboardPage.tsx`, `frontend/src/pages/TestPage.tsx`, `frontend/src/pages/TestResultPage.tsx`, `frontend/src/services/api.ts`, `frontend/src/services/auth.ts`

The working tree also contains pre-existing modifications and untracked project files from prior work. Preserve them; the list above describes files relevant to this production-readiness task, not a claim that every listed file was first created in this task.

## Render Static Site + Web Service + Neon Free

The checked-in [Render Blueprint](../render.yaml) creates two free services only. It intentionally does not create a database or run a migration. `autoDeployTrigger: off` prevents a future push from automatically deploying. Its default service names yield these expected URLs:

- Frontend: `https://ssc-prep-beta.onrender.com`
- API: `https://ssc-prep-beta-api.onrender.com`
- API health check: `https://ssc-prep-beta-api.onrender.com/api/health`
- API readiness check: `https://ssc-prep-beta-api.onrender.com/api/ready`

If Render assigns different service names/URLs or a custom domain is later used, update all three matching values before the next frontend build: backend `CORS_ORIGINS`, frontend `VITE_API_URL`, and the frontend CSP `connect-src` header. Render Static Site is served from a global CDN and is not on the Render private network, so the browser calls the public API origin directly; it cannot use an internal service hostname. Do not configure `/api` as a static-site rewrite.

### Render settings

The Blueprint is the exact starting configuration. In Render, link the repository and select its root `render.yaml`, but do not sync/deploy until the owner has reviewed the URLs and supplied Neon credentials.

| Service | Setting |
| --- | --- |
| API | Web Service, Docker runtime, `backend/Dockerfile`, Free plan, Singapore region, deploy only manually, health path `/api/health` |
| API process | `PORT` from Render, one Uvicorn worker, SQLAlchemy pool 2 + overflow 0 |
| Frontend | Static Site, root `frontend`, build `npm ci && npm run build`, publish `dist`, SPA rewrite `/* → /index.html`, deploy manually |
| API URL in browser | `VITE_API_URL=https://ssc-prep-beta-api.onrender.com/api` (build-time, public, not a secret) |
| API CORS | `CORS_ORIGINS=["https://ssc-prep-beta.onrender.com"]`; exact origin only, no trailing slash |
| Forwarded client IP | `FORWARDED_ALLOW_IPS=*` for Render’s documented proxy path. Render’s edge proxy is the only public route to the Web Service port; validate this assumption if changing ingress/provider. |
| API health probe | Render health path `/api/health` (cheap liveness). Check `/api/ready` manually before student traffic; it verifies database and Alembic head. |
| Secrets | `DATABASE_URL` entered in Render’s secret/env UI; `SECRET_KEY` generated once by the Blueprint and retained across redeploys |

The API currently uses a Docker image; the Dockerfile starts Uvicorn from `PORT` and `WEB_CONCURRENCY`. Render sets its public process port to `10000` by default. Do not set a competing hard-coded port. The API image health check also calls `/api/health`.

Render does not support a free-tier pre-deploy command or one-off job. Therefore migration `alembic upgrade head` and first-admin bootstrap must be run from the owner’s secured workstation against the new Neon beta database (never `ssc_prep`). A migration job must not be added to the web service startup command: multiple worker/restart invocations could race, and schema changes need a backup/approval step.

### Neon project and connection settings

1. Create a **new Neon Free project** for the beta, separate from the existing `ssc_prep` database and from the staging/load-test project. Select a region close to the Render Singapore service if Neon offers it for the account. Keep both staging and beta projects on Free and confirm the console says `$0` before creating anything.
2. Use the project’s main branch and its default database/role unless there is a reason to separate roles. Do not import existing student accounts, attempts, or answers. If chapter questions need copying, the owner should import a reviewed, content-only dataset into the new beta database; this task does not copy data.
3. In Neon’s connection details, select the **pooled** connection string for the API. Replace the URL scheme with SQLAlchemy’s `postgresql+psycopg://` and preserve Neon’s TLS query options (`sslmode=require`). The hostname should be the Neon pooled endpoint (usually contains `-pooler`). This app’s production validator accepts `require`, `verify-ca`, or `verify-full`.
4. Use the direct Neon connection string only for the one-time migration/bootstrap commands when available; keep it in a temporary environment variable, not a file or command argument recorded in Git. Do not print either URL.
5. For API connections set `DB_POOL_SIZE=2`, `DB_MAX_OVERFLOW=0`, and `WEB_CONCURRENCY=1`. The app then holds at most two application-side PostgreSQL connections. Neon’s pooled endpoint provides PgBouncer in front of compute. Confirm the current compute’s `SHOW max_connections` from Neon SQL Editor and watch active/idle sessions in the dashboard.

Neon Free allowances change over time. As checked on **5 November 2026**, Neon documents 100 CU-hours per project/month, 1 GB PostgreSQL storage per project, 5 GB public transfer per project/month, autoscaling up to 2 CU, 10 branches, and a six-hour instant-restore window (up to 1 GB of changes). Compute scales to zero after five idle minutes. At a continuously active 0.25 CU, 15 days would consume about 90 CU-hours; autoscaling above 0.25 CU, staging runs, or background activity can exhaust the allowance sooner. When a Free quota is reached, compute can suspend until reset/upgrade and writes that exceed storage limits fail. Free Neon does not replace an external backup. Review the live [Neon Free plan limits](https://neon.com/docs/introduction/plans) before launch.

### Render and Neon free-tier limits to tell students

- Render Free Web Services sleep after 15 minutes without inbound traffic; first requests can take about a minute to wake the API. Neon can independently sleep after five minutes idle, adding another cold start. Displayed wait/loading pages and temporary 502/503s are possible.
- Render Free Web Service is 0.1 CPU / 512 MB RAM, single instance only, no persistent disk, no shell/SSH, and no service pre-deploy job. Render can restart a free service. Only static frontend content remains continuously served.
- Render gives a workspace 750 free instance-hours per calendar month shared by free web services. Free usage also consumes build-pipeline minutes and outbound bandwidth; if no payment method is present, reaching the included limits suspends services/builds rather than charging, but confirm billing settings and keep the spend controls at zero. External-database traffic may also trigger Render’s free-service outbound traffic safeguards.
- Neon Free compute is metered, not an always-on database SLA. Connection limits depend on compute size; keep the application pool small and use the pooled URL. Free plan metrics/restore retention is limited. A six-hour instant restore is not a backup policy.
- Render explicitly positions Free instances for testing/hobby/preview use and advises against production use. This is a temporary beta compromise. Do not promise uptime, recovery, or 50–70 concurrent users until the staged load runs succeed. If predictable availability or recovery is required, stop and obtain owner approval for paid infrastructure.

### Exact manual migration sequence (new Neon beta DB only)

Use the dedicated beta configuration template for URL shape and pool sizing. Do not copy it over `.env`; the helper below prompts for the pooled URL with masked input, exports it to the current process only, and restores/removes the prior process value when finished. From PowerShell in `backend`, first run the read-only identity/TLS check:

```powershell
.\scripts\Invoke-NeonBeta.ps1 -Action verify
```

Only after the target identity is verified, review the Neon snapshot/backup state and run the guarded upgrade if the database is not yet at head:

```powershell
.\scripts\Invoke-NeonBeta.ps1 -Action upgrade
```

After migration, inspect the required schema, capacity, and data counts without changing rows:

```powershell
.\scripts\Invoke-NeonBeta.ps1 -Action inspect
```

The report includes only counts and schema names, no user identities or invitation contents. It must show revision `0008_beta_access_and_rate_limits`, expected tables/constraints/indexes, capacity 200, and counts for users, invitations, subjects, chapters and questions. The inspection is a read-only transaction. The beta guard refuses any database/role other than `neondb` / `neondb_owner`, a non-Neon or unpooled host, or missing TLS. The upgrade action additionally checks the Alembic head, repeats read-only identity verification, and requires typed confirmation before Alembic runs `upgrade head` (migrations 0001–0008). Alembic reads explicit process `DATABASE_URL`, which takes precedence over `.env`; the helper never edits `.env`. Do not substitute a direct URL or the existing `ssc_prep` connection.

After confirming that the beta database contains no existing user accounts and no admin, create the first admin through the same masked, beta-targeted helper:

```powershell
.\scripts\Invoke-NeonBeta.ps1 -Action bootstrap
```

The wrapper sets production/invitation settings only for the child process, creates a temporary random signing key for that one CLI process, and restores the prior process environment afterward. It does not edit `.env` or Render settings. The existing bootstrap command then checks migration 0008/capacity, requires zero existing user accounts, no existing admin, a typed confirmation, and a password prompt without echo. It also enforces the beta Neon pooled host, database, role, and TLS guard. After the owner chooses to run it, sign in through the deployed app and issue invitations. The bootstrap has not been run as part of this inspection.

### Seeding only completed beta content

Never use a full `pg_dump`/restore from the local or existing `ssc_prep` database to seed beta; that would copy user accounts, attempts, answers, and unrelated catalog data. The existing `backend/scripts/seed.py` seeds the broad SSC catalog, including chapters outside this beta scope, so do not run it unchanged if the beta should contain only the completed 31 Maths, 22 Reasoning, and 28 General Science chapters.

Instead, create the beta catalog rows for only those 81 approved chapters (and their required SSC exam/subject/subcategory rows), then use the existing reviewed per-chapter question batches/importers. Each importer resolves the chapter by catalog slugs and should first run in dry-run mode against the beta URL; review accepted/duplicate/conflict counts before any apply. Run importers with `DATABASE_URL` set only in that PowerShell process using the masked URL prompt; do not set it in `.env` or allow the importer to fall back to the local default. Keep seed files content-only: question text/options/explanations/provenance, no users, invitations, attempts, or answers. Confirm the final beta catalog and question totals from the Neon beta URL after imports. No catalog or question seed has been run here.

## Provider-independent deployment

For a provider other than Render/Neon, use this fallback only if it supports OCI/Docker containers, environment secrets, HTTPS ingress, backend and frontend health checks, private service-to-service networking, managed PostgreSQL with TLS, automated backups and preferably point-in-time recovery, deploy logs, and database connection/storage metrics. Avoid exposing PostgreSQL publicly.

1. Build the backend container from `backend/`. Build the frontend container from `frontend/`, passing `VITE_API_URL=/api`. Pin image tags/digests in the selected provider's release record.
2. Create separate staging and production services/databases. Set secrets through the host's secret store, never a checked-in `.env` file. Keep staging data separate from production.
3. Configure the HTTPS ingress to serve the frontend and proxy `/api/*` to the backend. Preserve the original client IP only from known trusted proxy addresses; set `FORWARDED_ALLOW_IPS` to those exact addresses/CIDRs supported by Uvicorn. Do not trust arbitrary forwarded headers. Apply ingress request/body limits and a coarse IP/WAF rate limit.
4. Use `frontend/.env.production.example` as the frontend build-time checklist. With same-origin `/api`, no API hostname needs to be embedded in browser assets. If frontend and API are split-origin, set the exact HTTPS API URL at build time and update the CSP `connect-src` to that exact origin, then add the exact frontend origin to backend `CORS_ORIGINS` and test preflight. Do not leave a broad `https:` CSP source.
5. Set every backend variable listed in the next section. Use a unique random `SECRET_KEY`; changing it invalidates all existing JWTs. Use a restricted application DB role and a separate migration role if the provider permits it.
6. Run the backup and restore drill, staging deployment, migration rehearsal, and smoke checks before scheduling a production release. Use the exact same immutable backend image for the migration job and API release.
7. Run the one-off migration command as a controlled release step, then start the API. Do not auto-run migrations in every worker. Verify `/api/health`, `/api/ready`, auth/invite, all three beta sections, test lifecycle, and database counters. `/api/ready` must return 200 before ingress sends student traffic.
8. Deploy the frontend and verify HTTPS, CSP, signup invitation requirement, catalog scope, browser console, and API routing from a clean browser session.

## Environment variable checklist

Copy values from `backend/.env.production.example` into the provider's secret/configuration interface; never copy placeholder values literally.

| Variable | Production requirement |
| --- | --- |
| `ENVIRONMENT` | `production` |
| `DEBUG` | `false` |
| `SECRET_KEY` | Unique cryptographically random secret, at least 32 characters; rotate only with a planned all-session invalidation |
| `DATABASE_URL` | `postgresql+psycopg://...` to managed PostgreSQL with `sslmode=verify-full`; percent-encode special password characters |
| `CORS_ORIGINS` | JSON array of exact HTTPS frontend origins; no wildcard, paths or localhost |
| `BETA_INVITATIONS_REQUIRED` | `true` |
| `BETA_CATALOG_SCOPE` | `true` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | 5–60; default 30; no refresh endpoint exists |
| `DB_POOL_SIZE`, `DB_MAX_OVERFLOW` | Set from global worker/replica budget below |
| `DB_POOL_TIMEOUT_SECONDS`, `DB_POOL_RECYCLE_SECONDS` | Start with template values and tune from actual database metrics |
| `WEB_CONCURRENCY` | Set per instance after checking memory/CPU and database budget |
| `FORWARDED_ALLOW_IPS` | Exact trusted proxy addresses only; match ingress topology |
| `RATE_LIMIT_CLEANUP_SECONDS` | At least 60; default 900 |
| `PORT` | Set by many container hosts; otherwise backend listens on 8000 |
| `VITE_API_URL` | Render Blueprint uses `https://ssc-prep-beta-api.onrender.com/api`; rebuild after changing the API host |

The generic template’s starting DB allocation is 2 workers × (3 pooled + 2 overflow) = **10 possible database connections per backend replica**. The Render Blueprint overrides this to 1 worker × (2 pooled + 0 overflow) = **2 application connections**. At `R` replicas the formula is `R × workers × (pool + overflow)`. Add migration/admin/monitoring connections and keep the total under the DB limit. Pool settings apply per process, not per container. These numbers are not validated under load.

## Beta notice and student workflow

The app displays a temporary-beta notice in the shared layout: the API may sleep and take about a minute to wake, confirmed answers are saved, and beta data may be reset after the test period.

After the connectivity changes in `TestPage`, an answer is first held in a per-attempt `sessionStorage` draft, sent to the API, and removed from the draft only after server confirmation. Drafts are restored on a page refresh in the same browser tab and retried after the browser's `online` event or the visible Retry action. If an answer is still unconfirmed at submit/expiry, the test does not pretend it was saved; the results view warns that it was not scored. The auth profile is also cached per tab so a transient API/Neon cold start does not automatically clear a valid bearer token; definite 401/403 rejection clears it. These protections were TypeScript-build checked, but a browser/network-disconnect journey was not run in this environment. `sessionStorage` does not survive closing the tab/browser or moving to another device.

The expected journey remains: owner issues invitation → student registers with matching email/code → logs in → opens dashboard → selects an available subject/chapter → starts an attempt → answers are saved and can be reloaded → submit → result/review explanations → dashboard history. API endpoints enforce attempt ownership for read/save/submit/review/history. The user-facing flow must still be smoke-tested against the deployed disposable beta database before sending invitations.

The beta notice warns that data can be reset. This does not replace a backup. Tell students that local drafts only cover unsent answers within the same browser tab; only server-confirmed answers are stored durably.

## Staging load scenarios (do not run against the live beta or `ssc_prep`)

The k6 workflow at `backend/loadtest/exam_flow.js` reuses one disposable login per virtual user, loads the student's history, starts a 10-question Easy chapter test, validates unique questions/four options/no answer leakage, saves answers with a think-time delay, reloads the attempt to confirm persistence, submits, checks result scoring/explanations, then verifies the dashboard lists the attempt. It records k6 HTTP failures/latency plus `answer_save_reliability`, `submission_reliability`, and `submission_correctness`. Built-in thresholds are <1% failed HTTP requests, p95 <1.5 s, and each custom reliability metric >99%.

Use a **separate Neon Free staging project** with disposable student accounts and test question data. Do not reuse the beta or existing database. Each account needs a unique login; the script caches a JWT for repeated iterations. The SQL data created by the scenario (attempts/answers/history/rate-limit rows) is persistent on that staging project. Do not auto-clean it; use a disposable project and only remove it after the owner reviews and approves that destructive action.

Create one `USER_CSV` row per VU (`email,password`; test passwords must not contain commas), choose a Maths chapter with at least 10 Easy active ordinary questions, and set these PowerShell values from the staging catalog:

```powershell
$env:BASE_URL = 'https://<staging-api>.onrender.com'
$env:USER_CSV = 'C:\secure\ssc-beta-stage-users.csv'
$env:EXAM_ID = '<staging SSC id>'
$env:SUBJECT_ID = '<staging Maths subject id>'
$env:CHAPTER_ID = '<staging completed Maths chapter id>'
$env:DIFFICULTY = 'EASY'
$env:DURATION = '5m'
$env:THINK_TIME_SECONDS = '3'
$env:VUS = '10'
k6 run backend/loadtest/exam_flow.js
```

Repeat with `VUS=25`, `50`, and `70`. The login IP policy allows 100 logins per 10 minutes; each test run needs up to 70 simultaneous initial logins. Leave at least ten minutes between run starts or use a separate staging ingress/source IP, so repeated runs do not collide with the shared IP window. Run one cold-start trial and a separate warm trial; keep the cold-start latency/failures in the report instead of discarding them. Do not call a run successful if thresholds fail.

Alongside k6 output, record Render API CPU, memory, restarts and deploy events; from Neon record compute/CU-hours, connections (including pooler), storage, egress, cold starts, and query latency. Record whether every answer-save request returned success and whether result counts match the review. Do not run any load scenario until the owner confirms that the staging URL and database are disposable. No 10/25/50/70 load scenario has been run; therefore no capacity claim is established.

## Migration chain and safe production procedure

The current migration chain is linear: `0005_question_images` → `0006_user_question_rotation` → `0007_question_rotation_modes` → `0008_beta_access_and_rate_limits` (head). Migrations 0006 and 0007 preserve the pre-existing question and user rows. Migration 0008 adds beta capacity/invitation/rate-limit tables and seeds the singleton limit at 200.

Before the first production migration:

1. Confirm deployment target and `DATABASE_URL` identity using the provider console and a read-only SQL session. Stop if it is unclear which database is selected.
2. Confirm current `alembic_version`, compare the exact release image's Alembic heads, and rehearse the complete upgrade on a production-like staging clone.
3. Require a fresh provider backup/snapshot plus a successful restore rehearsal or a verified PITR checkpoint. Record backup ID/time and have a tested restore target. Do not proceed if no recoverable backup is available.
4. Put the app in maintenance/read-only mode or stop writes for the migration window. Ensure one migration job only.
5. From the exact backend image and production secret injection, first inspect `alembic current` and `alembic heads`; then execute `alembic upgrade head`. Do not run this against production during preparation. Review migration logs and `alembic_version`, then run schema/data smoke checks.
6. Deploy the matching API code and require `/api/ready` 200. Re-enable student writes only after smoke tests pass.

Production rollback policy: prefer rolling the application image back while leaving additive schema in place. Do not automatically run `alembic downgrade` during a failed deploy. Migration 0007 downgrade merges per-mode history counters and removes duplicate rows; that is lossy because mode-specific history is collapsed. Migration 0006 downgrade drops all question-history/rotation state. Migration 0008 downgrade deletes invitation, beta-capacity, and rate-limit records. Downgrade can therefore lose operational/student state and may not be compatible with already-running code.

For a failed or corrupt production migration, stop writes and follow the selected provider's recovery plan. Prefer restoring a snapshot/PITR point to a **new isolated database**, validating users/questions/attempts, schema revision, and API behavior there, then switch traffic only through an approved cutover plan. Do not restore over the original database until impact, data-loss window, and owner authorization are explicit. Production migration/restore is a manual owner approval gate.

## Backup and restore

Configure automated encrypted managed-database backups at least daily and point-in-time recovery where offered. Set and document retention with the owner. Alert when the last successful backup is older than the approved RPO. The application repository does not configure provider backup schedules.

For an additional logical backup, use a secured operator workstation with PostgreSQL client tools. Never echo the database URL or put it in command history if it contains a password. Example PowerShell (the password-bearing value should be populated securely from the secret manager):

```powershell
$env:PGURL = Read-Host 'Paste the protected PostgreSQL URL'
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
pg_dump --format=custom --no-owner --file="C:\secure-backups\ssc-prep-$stamp.dump" "$env:PGURL"
pg_restore --list "C:\secure-backups\ssc-prep-$stamp.dump" | Select-Object -First 20
Remove-Item Env:\PGURL
```

Protect the backup with encrypted storage and restricted access; transfer it off the database provider/account if the recovery plan requires. Verify dump completion and archive listing. A dump listing alone is not a restore test.

Restore rehearsal: provision a fresh isolated database, create the required DB role/permissions, then restore without destructive clean flags:

```powershell
$env:RESTORE_DATABASE_URL = Read-Host 'Paste the isolated restore database URL'
pg_restore --no-owner --no-privileges --dbname="$env:RESTORE_DATABASE_URL" "C:\secure-backups\ssc-prep-YYYYMMDD-HHMMSS.dump"
Remove-Item Env:\RESTORE_DATABASE_URL
```

Check table counts, Alembic revision, account and question sampling, test attempts, and API readiness against the isolated copy. Record duration and issues. Provider PITR should likewise target a separate database first. No backup or restore rehearsal was run as part of repository changes.

## Monitoring and recovery configuration

Configure these in the selected provider/monitoring service. Thresholds below are starting alerts to tune after observing normal beta traffic, not measured service-level objectives.

| Signal | Initial alert | Automation / response |
| --- | --- | --- |
| External uptime | Probe HTTPS landing page and `/api/health` every minute; alert after 2 consecutive failures | Monitor can page/email automatically; operator checks provider deploy/network events |
| Readiness | `/api/ready` non-200 for 2 consecutive probes | Provider may remove unhealthy API instances; investigate DB/schema/connectivity |
| Backend errors | 5xx >2% for 5 min or sudden error increase | Log/error monitor can alert; inspect request IDs and sanitized exception locations |
| Latency | API p95 >1 s for 5 min (tune from baseline) | Alert only; operator inspects DB slow queries, CPU and saturation |
| CPU / memory | >80% for 5 min; memory >85% or OOM restart | Provider metric alert/autoscaling if deliberately configured; check worker count and memory |
| PostgreSQL connections | >75% of max for 5 min; alert at >90% urgently | Provider metric alert; reduce unnecessary workers/traffic or scale DB after owner review |
| DB storage | >75% warning; >85% urgent | Provider metric alert/autoscale storage only if explicitly enabled and priced |
| Backups / PITR | Missing scheduled backup or failed backup; verify latest recoverable point meets owner RPO | Provider backup automation plus alert; restore is an operator action |
| Deployment | Health/readiness check fails after rollout | Host should stop routing/restart or roll back only if explicitly configured; keep prior immutable image and operator rollback runbook |
| Browser errors | Capture JS exceptions and failed API requests without tokens, passwords or student answer payloads | Select and configure frontend monitoring SDK/provider; not integrated in this repo |

Application logs are structured enough to correlate by `X-Request-ID`, but external error monitoring is not wired in. Keep access restricted, set retention, and never attach auth headers, invitation codes, passwords, full request bodies, or sensitive student data to monitoring events. Configure external uptime checks from outside the hosting provider to catch provider-level failures.

Provider automation can usually restart unhealthy containers, route around failed replicas, schedule backups, retain logs, and alert on managed DB metrics. A human must decide whether to roll back a release, restore PITR, promote a replacement database, rotate secrets, investigate account/security incidents, contact students, or scale paid infrastructure. Do not enable automatic destructive recovery.

## Admin and beta operation

Bootstrap the first administrator only after migration 0008 and read-only inspection confirms the target and zero users. The beta wrapper prompts for the pooled URL and calls the existing first-admin command; the Python command prompts for the owner email, typed confirmation, and password (without echo):

```powershell
.\scripts\Invoke-NeonBeta.ps1 -Action bootstrap
```

It requires the Neon beta target, invitation-only production settings, zero existing users, no existing admin, and the typed confirmation. For an existing account in a database that already has an administrator, the previous grant/revoke command remains available: `python -m app.scripts.set_admin --email owner@example.com --grant` (use only with an explicitly verified beta connection).

Admin APIs are under `/api/admin` and require an active admin JWT:

- `GET /api/admin/beta-capacity`
- `POST /api/admin/invitations` (batch email list; returns codes once)
- `DELETE /api/admin/invitations/{invitation_id}` (unused invite only)
- `PATCH /api/admin/users/{user_id}/activation` with `{"is_active": false}` to suspend access

Deliver invitation codes to the intended email addresses using an approved secure channel. The API does not send mail. Store no copy of plaintext invitation codes. Revocation/disable is a human admin action; do not automate account deletion. Existing student accounts can be deactivated but not deleted by these controls. Preserve the only active admin account.

The cap includes all existing users (including inactive) plus pending, unexpired invites. Expired invitations do not reserve slots. Invite only after the owner approves eligibility and privacy/terms requirements.

## Security notes

- Keep the API and database private behind HTTPS ingress; DB TLS certificate verification is required by the production URL validator.
- Use separate least-privilege runtime and migration credentials if supported. Rotate DB and JWT secrets in a planned maintenance window; JWT-key rotation signs out all users.
- The application uses short-lived bearer JWTs and no refresh mechanism; students sign in again after expiry. Disabled-account checks occur on API requests.
- Browser `sessionStorage` reduces token lifetime across browser sessions versus persistent local storage but is not an XSS boundary. Keep dependencies patched and CSP strict; avoid third-party scripts.
- DB-backed fixed windows are atomic across app workers but add a DB write to rate-limited routes and can permit bursts at fixed-window boundaries. Add provider edge/WAF limits and alert on DB pressure. The implemented limits are starting policy values and should be tuned with measured traffic.
- On Render, Uvicorn must trust Render's forwarding headers (`FORWARDED_ALLOW_IPS=*`) so login IP limits see the originating IP. This trust is appropriate only for requests arriving through Render's managed proxy; do not reuse `*` on an API directly exposed to arbitrary clients or on another provider without a trusted-proxy design.
- Configure login/register ingress limits, TLS, request size limits, CORS, secrets, least privilege, log retention, admin MFA/SSO if available, and incident contact procedures at the chosen provider. No provider account setting has been applied here.
- Do not expose exception details or credentials in logs, browser monitoring, support tickets, or shell output.

## Release, rollback, and incident checklist

Before launch: verify backup and restore; confirm staged migration from current revision; confirm all production variables and exact host/proxy values; bootstrap and test two owner-controlled admins if possible; verify invitations, deactivation, catalog scope, exam start/answer/reload/submit/review; verify external uptime and alerts; confirm a known-good previous image and release ID; and agree on an operator contact/maintenance window.

If rollout health checks fail: stop further rollout, remove failing instances from ingress, preserve logs/request IDs, and roll back to the prior application image with the schema left at the new additive head. Confirm readiness and smoke tests. If the DB itself is damaged, stop writes and use the documented isolated restore/PITR process; determine the expected data-loss point before cutover. Production data changes require owner approval.

## Verification completed in this preparation

- The Alembic graph resolves to one head, `0008_beta_access_and_rate_limits`, and its declared parent is `0007_question_rotation_modes`. This is static migration-graph verification; no database was contacted and no migration was applied here.
- Prior project work reported migrations 0006 and 0007 and PostgreSQL question-rotation concurrency tests completed on staging; those checks were not repeated here absent a concrete failure.
- No migration 0008 upgrade/downgrade or schema verification is claimed for this preparation. Do not infer the revision of any configured database from the source graph.
- No invitation-cap or rate-limit concurrency test against PostgreSQL was run in this review. Code serializes invite issuance and registration against the `beta_capacity` row with `SELECT ... FOR UPDATE`, and registration also locks each invitation row; the rate limiter uses PostgreSQL atomic upserts. These are code-path observations, not live concurrent test results.
- The focused backend HTTP subset passed **114 tests** using the project's existing local test database fixture. The complete backend suite passed **430 tests in 903.39 seconds** with that same fixture. These SQLite-backed tests exercise HTTP routes but are not PostgreSQL concurrency or live deployment checks.
- The frontend production build (`tsc -b && vite build`) passed. Relevant application, migration, and test Python files compiled successfully; `git diff --check` passed. `render.yaml` parsed as YAML with two services and auto deploy disabled, but no Render Blueprint validator was available.
- No live PostgreSQL API journey, Render Blueprint CLI validation, Docker image build, Render deployment, Neon provisioning, backup/restore rehearsal, external monitoring integration, or load test is claimed complete.

## Community Wisdom

Developer reports on FastAPI rate limiting note that per-process memory counters diverge across workers, so shared state is required; this app uses atomic PostgreSQL counters and should pair them with edge limits to avoid concentrating all abuse-control writes on the application database ([R.A. Olanrewaju's DEV article](https://dev.to/jpegcreate/building-a-distributed-rate-limiter-for-fastapi-with-redis-sliding-window-algorithm-5h10)). A production deployment walkthrough also emphasizes separating ingress, API, and managed PostgreSQL while treating secrets and readiness as deployment concerns; this guide applies those principles without assuming Kubernetes or a vendor ([Jesus Manrique's DEV article](https://dev.to/guayoyo_tech/zero-to-kubernetes-part-4-fastapi-backend-postgresql-in-production-1p6b)). These are community write-ups, not provider guarantees or formal security audits.
