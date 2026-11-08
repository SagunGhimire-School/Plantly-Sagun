# Plantly development progress

Last updated: **2026-11-08**. This is a verified local preview, not the complete MVP, scientific approval or release approval.

## Current handoff

**Current:** local foundation/account/input verification complete; source/notes import engineering verified. Remaining milestone work is gated by the concrete source/science/provider decisions below.

**Next:** resolve exact source/rule/crop/region/method review and provenance for numeric ingestion; select generation/embedding configuration and authorize provider use before generation/plan/chat work. No additional scaffolding or fake outputs were added to bypass those gates.

Local services at handoff: frontend **http://localhost:3000**, API **127.0.0.1:8000**, persistent PostgreSQL **127.0.0.1:5432**. Same-origin health returned database connected after restoring the normal development connection. Temporary test API and test database were stopped. Start/stop instructions are in [DEVELOPMENT.md](../DEVELOPMENT.md); servers are ordinary local processes, not an autonomous development service.

## Milestone status

| ID | State | Evidence / remaining boundary |
|---|---|---|
| M-001 | verified | Next.js JS/App Router + Tailwind tokens, API health/proxy, real PostgreSQL/pgvector, Alembic round-trip, install/run docs, production build and browser checks. |
| M-002 | verified | Real Argon2id accounts, hashed opaque sessions, signed pre-auth CSRF, session CSRF/Origin checks, 12h idle/7d absolute expiry, logout and ownership checks; database and browser tests. Public release remains gated. |
| M-003 | verified | Minimum persistent-input slice: partial/revision-safe drafts, atomic/idempotent completion, owner-scoped plots/seasons, shared seasons, plot edits, null/unknown and user-reported pH provenance. Refresh/login/concurrency/isolation verified. Full scientific intake is not claimed. |
| F-015 | verified | Truthful landing/pricing; no checkout, prices, trial, savings or unavailable capabilities presented as working. |
| D-010 | implemented_unverified | All 15 files present; hashes match after line-ending normalization; schemas/IDs/refs/units/placeholders inspected. External publications, licenses and scientific eligibility are unverified. See DATASET_AUDIT.md. |
| F-040 | blocked | **Source/notes slice verified:** manual versioned import, hashes/provenance, deduplication, immutable history, rollback and inactive review state. Full numeric/PDF/embedding ingestion remains blocked by provenance/review and embedding choices. |
| M-004 / G-010 | blocked | No named independent reviewer or exact approved source/rule/scope versions. No agronomic rules active. |
| M-005 | blocked | Review, real generation/embedding model decisions, Gemini key and authorized budget missing. No durable generation worker or saved scientific plans implemented. Basic facts dashboard is M-003 only. |
| M-006 | blocked | Depends on reviewed saved plans and configured AI; no fabricated assistant or plan mutations. |
| M-007 / G-020 | blocked | Weather/price providers, real commercial terms, hosting/retention/recovery/release decisions missing. Unavailable states are implemented; no public deployment. |

## Current executed verification

All below were actually run on 2026-11-08:

- Backend: `.venv/Scripts/python.exe -m ruff check .` — passed.
- Backend with explicit disposable TEST_DATABASE_URL: `.venv/Scripts/python.exe -m pytest -q` — **25 passed**, one upstream Starlette/httpx deprecation warning. Includes real PostgreSQL upgrade/downgrade/re-upgrade, metadata drift, vector distance, rollback, auth/CSRF/expiry, isolation, concurrent saves, shared season ownership, revisions, cascading deletion, source version history and failure recovery.
- Frontend: `npm.cmd run lint` — passed; `npm.cmd test` — **1 passed**; `npm.cmd run build` — passed, seven application/not-found routes built (protected pages dynamically rendered).
- `node node_modules/@playwright/test/cli.js test` — **12 passed in 31.5s**, no failures. Includes account/draft/edit/logout/login at **320×700, 390×844, 768×1024, 1440×900, 1920×1080**, pricing/landing, keyboard focus/mobile dialog Escape and focus return, reduced motion, overflow, axe checks, soil validation/stale-draft preservation and injected backend/database failure states.
- Dashboard screenshots inspected at all five required sizes. Intake at 320/1440 and mobile landing additionally inspected. Captures and traces are local frontend/test-results artifacts; these may be overwritten by later browser runs. Playwright Test was used, **not Playwright MCP**.
- Development migration: **0004_sources (head)**.
- Development manual import: **40 source versions / 122 notes** created, all **unreviewed**. Immediate repeat: **0 new versions / 40 unchanged sources**.
- `npm.cmd audit --omit=dev --audit-level=moderate` — **0 vulnerabilities**. Eight initial moderate dev-tool findings remain documented in ISSUES; no forced major downgrade.
- Post-restart `GET http://localhost:3000/api/v1/health` — 200, database connected. Capabilities report planning unavailable/not configured, weather/prices unavailable and scientific rules not reviewed.
- Preflight: all 15 original data files present, **15 LF-normalized matches**, originals preserved. Node 24.11.1 and Python 3.12.0 used. Docker needs its installed per-user directory on PATH; both databases were verified healthy before the test service was stopped.

## Assets and environment

Six user-supplied visual assets inventoried. Tractor and SVG moved to public/images and public/brand; four internal AGRA references moved out of public to docs/references. Raster files inspected; SVG structure and browser rendering inspected. Missing historical originals and usage limits are in ASSETS.md.

Dependencies exist in backend/.venv and frontend/node_modules, with lockfiles. The folder is not a Git checkout; no commit/diff verification is claimed. The explicitly requested ponytail@ponytail **5.3.3** was installed and verified enabled.

Gemini remains disabled and no user route calls the provider. No paid calls, synthetic production records, active scientific rules or public deployment occurred.

## Historical execution record

The starter handoff originally contained no application code and reported data/artwork absent. Those statements became obsolete after the user's additions and this implementation.

Earlier incremental runs produced 3, 9, 20, 22 and 24 passing backend tests as features were added. An initial five-case browser run passed assertions but hung during Windows server teardown; after using a separately started server, ten-case suites exited successfully. The final expanded results above supersede these checkpoints. The interruption left shared-season/edit/navigation/import work pending verification; it is now covered by the current results. Resolved failures and exact recovery details are retained in ISSUES.md.
