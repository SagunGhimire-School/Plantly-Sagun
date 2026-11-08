# Plantly — minimal, newly created starter roadmap

**This ROADMAP was created for this handoff; no original team roadmap was supplied.** Its IDs and acceptance criteria are provisional coordination aids. The original `AGENTS.md`, `PRODUCT.md`, and `ARCHITECTURE.md` remain authoritative. Build the **smallest dependency-ready vertical slice**, not every proposed module at once. Mark a milestone verified only with observed checks, not generated TODOs.

| ID | Deliverable (in order) | Minimum acceptance / human gate |
|---|---|---|
| **M-001** | Local full-stack skeleton | Next.js App Router JS/Tailwind v4 landing using Plantly tokens; FastAPI liveness + `/api/v1/health`; working same-origin proxy; local Postgres topology; minimal SQLAlchemy/Alembic scaffolding; actual smoke tests and install instructions |
| M-002 | Secure account flow | Real signup/login/logout/me with Argon2id, DB-backed opaque cookie sessions and CSRF; expiry and isolation tests. No fake session logic |
| M-003 | Persistent input slice | Owner-scoped plot, season, plot-season, and resumable onboarding draft; basic forms, Pydantic validation, unknown/null provenance, revision-safe save/resume; tests across refresh/login |
| **D-010** | Curated dataset/source audit | Original 15 inventory-listed files physically supplied; checksums, schemas, source links, units, licenses and scientific eligibility audited. Block until data actually arrives. Not a rule approval |
| **F-015** | Truthful pricing/marketing | A minimal pricing route with explicitly unavailable/unset real offers; no fake signup charge, subscription, trial or outcomes |
| **F-040** | Validated incremental data ingestion | Depends on D-010. Manual idempotent versioned source import into Postgres; preserves evidence/history; no automatically enabled agronomic rules; behavior tested on disposable DB |
| M-004 | Reviewed science | Depends on human G-010 review and selected crop/region/method. Guarded deterministic rules; unreviewed quantities disabled; exact provenance and abstention tests |
| M-005 | Generation and saved dashboard | Depends on real source/review and model selections. Durable PostgreSQL job + worker, constrained Gemini narrative, validated immutable plans, honest processing and reload behavior |
| M-006 | Plan-bound assistant | Secured context-bound persistent chat, genuine evidence references, no uncontrolled plan mutation; transparent unsupported states |
| M-007 | Weather/pricing integrations, release hardening | Provider choices and observations; live data freshness indicators; secure deployment checks only with authorization |
| **G-010** | Scientific human review | **OPEN:** named independent reviewer must actually approve precise source, method, crop/region and rule versions. No approvals supplied |
| **G-020** | Public-release governance | **OPEN:** hosting, TLS, secure cookies, rate limits, privacy/cleanup retention and account-recovery limitations approved and tested. Never deploy on assumption |

**Current order for Codex:** M-001 → M-002 → M-003; work on the D-010 audit *only if source files arrive*. Do not start live science or model calls with placeholder data. F-015 can be done early as a small independent truthful route. See `docs/DEVELOPMENT.md` for specific real verification commands once code exists.
