# Local development and verification

Requires Node.js 20.9+ (tested: 24.11.1), Python 3.12+ (tested: 3.12.0), and Docker Desktop with Linux containers. Service ports bind to loopback. No public deployment or paid calls are involved.

## Windows PATH

Python initially resolved to an inaccessible Windows Store alias and Docker was absent from PATH. Both installations exist. If needed, run this in each terminal:

```powershell
$env:PATH = "$env:LOCALAPPDATA\Programs\Python\Python312;$env:LOCALAPPDATA\Programs\DockerDesktop\resources\bin;" + $env:PATH
```

The Docker directory also exposes its credential helper. Use npm.cmd if PowerShell blocks npm.ps1. This does not change permanent system PATH.

## Fresh installation

From the project root:

```powershell
python -m venv backend/.venv
backend/.venv/Scripts/python.exe -m pip install -r backend/requirements.lock.txt
backend/.venv/Scripts/python.exe -m pip install --no-deps -e "backend[dev]"
cd frontend
npm.cmd ci
node node_modules/@playwright/test/cli.js install chromium
```

requirements.lock.txt records exact Python dependencies. package-lock.json and exact frontend versions record JavaScript dependencies.

## Run

From the root:

```powershell
docker compose up -d --wait db
```

Backend terminal:

```powershell
cd backend
$env:APP_ENV = 'local'
$env:PUBLIC_APP_ORIGIN = 'http://localhost:3000'
$env:DATABASE_URL = 'postgresql+psycopg://plantly:local-development-only@127.0.0.1:5432/plantly'
.venv/Scripts/python.exe -m alembic upgrade head
.venv/Scripts/python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Frontend terminal:

```powershell
cd frontend
$env:INTERNAL_API_BASE_URL = 'http://127.0.0.1:8000'
npm.cmd run dev
```

Open **http://localhost:3000**. Visiting 127.0.0.1:3000 instead intentionally fails mutation Origin checks unless PUBLIC_APP_ORIGIN is changed to match. FastAPI /health checks liveness; /api/v1/health checks database connectivity. Browser API traffic uses the same-origin Next.js proxy.

The backend reads process environment variables. Copying an example environment file does not load it automatically. Next.js supports frontend/.env.local. Never use NEXT_PUBLIC_ for credentials/internal URLs. Local defaults match Compose; non-local environments require HTTPS and secure __Host- cookies, plus G-020 release approval.

GEMINI_API_KEY and GEMINI_GENERATION_MODEL remain unset. Keep AI_ENABLED=false. No user route invokes the adapter; configuring credentials alone does not clear scientific review, budget or output-validation gates. No generation worker is implemented yet.

## Backend checks

From the root:

```powershell
docker compose --profile test up -d --wait test-db
cd backend
$env:TEST_DATABASE_URL = 'postgresql+psycopg://plantly:local-test-only@127.0.0.1:5433/plantly_test'
.venv/Scripts/python.exe -m ruff check .
.venv/Scripts/python.exe -m pytest -q
```

Missing TEST_DATABASE_URL fails integration checks rather than silently skipping them. The URL must use PostgreSQL/psycopg and database plantly_test. Point it only at the disposable Compose service: tests downgrade/re-upgrade migrations. Checks include schema drift, pgvector distance, rollback, sessions/CSRF, ownership, concurrent saves, provenance and immutable imports. Do not run backend migration tests while browser tests use that database.

The small database-independent subset is pytest -m "not integration".

## Frontend and browser checks

From frontend:

```powershell
npm.cmd run lint
npm.cmd test
npm.cmd run build
```

For browser verification, use an API on port 8001 with the disposable database. After backend checks finish, in a backend terminal:

```powershell
$env:DATABASE_URL = 'postgresql+psycopg://plantly:local-test-only@127.0.0.1:5433/plantly_test'
$env:PUBLIC_APP_ORIGIN = 'http://localhost:3000'
.venv/Scripts/python.exe -m alembic upgrade head
.venv/Scripts/python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8001
```

Stop any existing frontend, then start a test frontend in another terminal:

```powershell
cd frontend
$env:INTERNAL_API_BASE_URL = 'http://127.0.0.1:8001'
npm.cmd run dev
```

In another frontend terminal:

```powershell
node node_modules/@playwright/test/cli.js test
```

The suite reuses the running frontend. Manual startup avoids the Windows child-process teardown hang observed with the initial npm-launched test server. Tests create labeled synthetic accounts and remove their own accounts after success; failures may leave test rows until the next migration round-trip.

Checks cover 320×700, 390×844, 768×1024, 1440×900 and 1920×1080, with screenshots under frontend/test-results. Keyboard focus, mobile dialog Escape/focus return, reduced motion, overflow and axe checks accompany signup/draft/edit/logout/login interactions. errors.spec.js injects network failures only to verify unavailable UI; real PostgreSQL tests remain independent. F-015 pricing checks live in smoke.spec.js.

After tests, stop the test frontend/API and restart the normal frontend with INTERNAL_API_BASE_URL=http://127.0.0.1:8000. PLAYWRIGHT_BASE_URL can select another frontend origin; match the backend Origin and frontend port.

## Manual source import and audit

From backend, with the local development database:

```powershell
.venv/Scripts/python.exe -m app.ingest --root ../data/curated
```

Imports rule_reviews/sources.yaml and research/*.yaml notes atomically. Validates IDs/references/schemas, hashes semantic content, preserves old versions and prints JSON success/failure. Re-running detects unchanged content. All versions remain **unreviewed**. Database constraints prevent approval/mutation in this slice.

Numeric datasets and synthetic grower fixtures are excluded. No original PDFs, embeddings, folder watchers, rule activation or automatic plan regeneration are implemented. Source licenses, scientific applicability and provider choices remain open.

From the root:

```powershell
backend/.venv/Scripts/python.exe scripts/preflight.py
backend/.venv/Scripts/python.exe scripts/audit_data.py
```

Preflight distinguishes CRLF-only checksum differences without rewriting originals.

## Shutdown

Ctrl+C stops owned API/frontend terminals. docker compose stop db preserves development data. docker compose --profile test rm -sf test-db removes only the disposable test service/tmpfs. Do not delete the development volume during routine testing. On macOS/Linux use .venv/bin/python and shell-appropriate environment assignment.
