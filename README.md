# Plantly — local development preview

Plantly has a working Next.js App Router frontend, FastAPI API and PostgreSQL/pgvector database. This is a local input-management preview, **not the completed scientific MVP**.

You can create an account, log in, save/resume an onboarding draft, create plots, share a season across plots, edit plot details and reload your saved dashboard. Passwords use Argon2id; database sessions, CSRF checks and owner-scoped queries protect account data.

AI planning displays **“AI planning is not configured yet.”** No generated answers, scientific recommendations, live weather, prices or savings are fabricated. No paid API calls or public deployment are required.

## Run locally

Start Docker Desktop. From the project root:

```powershell
docker compose up -d --wait db
```

Backend terminal:

```powershell
cd backend
.venv/Scripts/python.exe -m alembic upgrade head
.venv/Scripts/python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Frontend terminal:

```powershell
cd frontend
npm.cmd run dev
```

Open **http://localhost:3000**. Use localhost, matching the configured CSRF origin. Dependencies are installed in this workspace. For fresh installation, Python/Docker PATH fixes, configuration, tests and source imports, see [DEVELOPMENT.md](docs/DEVELOPMENT.md).

## Data and artwork

All 15 inventory-listed data files are present. Contents match the inventory after CRLF-to-LF normalization; original bytes were preserved. See [DATASET_AUDIT.md](docs/agent/DATASET_AUDIT.md) for units, placeholders and unresolved source/license checks.

The tractor and SVG logo are under frontend/public/images and frontend/public/brand. Four internal references were moved out of the public directory into docs/references. [ASSETS.md](docs/agent/ASSETS.md) lists exact paths and missing originals. The initial UI intentionally uses a text wordmark and simple layout.

## Remaining work

Source/rule/scope approvals, generation/embedding model selection, Gemini credentials and call authorization, eligible numeric ingestion, generation jobs and immutable plans, plan-bound chat, provider choices and release governance remain open. Adding a key alone does not activate scientific planning.

[PROGRESS.md](docs/agent/PROGRESS.md) records actual checks and next actions. Product, architecture and design contracts remain in docs/. UPLOADED_FILE_CHECKSUMS.json is the historical upload manifest, not a checksum of the evolving application. This extracted folder currently has no Git repository.
