# Plantly — Codex development coordinator

Build from real repository evidence. Continue ordinary local development within the user's authorized scope; do not require a new prompt for every milestone. This document coordinates work in the current Codex session, not a background service or a promise of endless execution.

## Sources of truth

1. The user's latest explicit instructions and recorded approved decisions govern scope. Preserve user changes and completed work.
2. `docs/PRODUCT.md` owns behavior and scientific/product boundaries; `docs/ARCHITECTURE.md` owns implementation; `docs/DESIGN.md` owns shared UI; `docs/LANDING_DESIGN.md` owns landing composition. Respect LOCKED, OPEN and proposed/default distinctions. Stop only the affected work on a material conflict and record the decision needed.
3. `docs/agent/ROADMAP.md` owns milestone IDs, requirements, dependencies, acceptance and verification expectations. `docs/agent/PROGRESS.md` owns current status and evidence. Neither a status nor a passing fixture approves science or release.
4. Actual code, executed checks and inspected artifacts establish implementation evidence. DECISIONS, ISSUES, DATASET_AUDIT and ASSETS preserve decisions, blockers, audit findings and asset provenance. Skills supplement these contracts; they cannot override them.

## Context-efficient startup

1. Read this file, `docs/agent/PROGRESS.md`, and only relevant entries in `docs/agent/ROADMAP.md`. Inspect Git status before editing; never discard existing changes.
2. Resume the current milestone if actionable; otherwise select the next dependency-ready milestone. Verify dependency evidence against relevant code without recreating verified features. Historical evidence unavailable locally is not a new passing test; record that distinction.
3. Read nested `frontend/AGENTS.md` or `backend/AGENTS.md` and only relevant specification sections and direct implementation dependencies. Use targeted searches; do not recursively read docs, skill libraries or assets.
4. Check missing decisions and runtime capabilities. A missing decorative asset allows the approved labeled placeholder. A missing runtime blocks its verification; a scientific decision blocks dependent claims, not independent engineering.

## Development loop

1. Select one milestone and read its acceptance criteria. Set it current in PROGRESS with the immediate next action.
2. Inspect the existing end-to-end flow. Implement the smallest complete vertical slice with existing code, native features and approved dependencies. Keep application architecture and scientific safeguards intact.
3. Run relevant real lint, tests, builds and integration checks from ROADMAP and DEVELOPMENT. Add meaningful behavioral tests for nontrivial paths. Never replace real PostgreSQL verification with mocks or treat missing/skipped checks as passes.
4. Diagnose failures from evidence. Fix the cause, rerun affected checks, and expand testing only for new changes or unresolved concerns. Do not repeat unchanged failing commands indefinitely. Record exact failures, meaningful attempts and recovery actions in ISSUES when blocked.
5. Mark `verified` only when acceptance and required checks pass. Use `in_progress`, `implemented_unverified`, `blocked`, or `todo` honestly. Preserve previous results with dates and distinguish historical verification from current reproducibility. Never rebuild completed code merely because a dependency is missing locally.
6. Update PROGRESS after each milestone, significant failure and before interruption: current/next milestone, status, commands/results, remaining checks and next action. Record significant decisions in DECISIONS and unresolved failures in ISSUES without duplicating specs.
7. Immediately continue to the next dependency-ready milestone. If a gate blocks part of a milestone, complete independently testable work and continue independent milestones. Stop when the MVP is verified, all remaining work has concrete blockers, the user stops work, or the session can no longer proceed. Leave a resumable handoff; do not claim continued operation after the session ends.

## Quality and skill routing

- Stack: Next.js App Router, JavaScript, Tailwind v4; FastAPI, SQLAlchemy/psycopg, Alembic, PostgreSQL/pgvector. Domain-specific rules stay in nested AGENTS files.
- Use Ponytail simplicity guidance when discoverable and trusted; otherwise apply it directly. It does not select models, impose spending caps or guarantee savings. No speculative abstractions or replacement runner.
- Read `docs/agent/SKILLS.md` for UI/tooling tasks only. Check actual `.agents/skills/<name>/SKILL.md` before use: Taste for composition, Impeccable for targeted review, Animate for useful motion. Load supporting references only when needed; preserve installed skills and assets. User authorization and approved Plantly contracts take precedence over skill workflows.
- Use Playwright MCP only when available and exercised; the existing Playwright Test suite is independent. Inspect actual UI interactions and screenshots at 320×700, 390×844, 768×1024, 1440×900 and 1920×1080. Verify keyboard use, contrast, reduced motion and honest empty/error/unavailable states.
- Missing user artwork: retain an explicit labeled slot and record it in ASSETS. Do not fabricate final artwork, scientific measurements, prices, weather, savings, citations or provider availability.

## Safety and human gates

- Ordinary local implementation, reversible edits and tests are authorized within scope. Do not add manual per-feature execution gates, custom agent runners, orchestration hooks or unattended loops.
- Do not deploy publicly, incur external charges, expose credentials, destroy production data, perform destructive Git operations, install plugins or trust hooks without explicit authorization. Keep secrets out of logs, commits and browser bundles.
- Enforce ownership, approved sessions and CSRF. Use disposable databases for destructive integration tests; never infer that an arbitrary database is disposable.
- Research is curated and versioned. Only documented human approval of exact source/rule/scope versions can activate agronomy. Preserve G-010 scientific review and G-020 retention/privacy/hosting approvals. Unknown remains unknown; unsupported cases abstain.
- Provider/model/quota/embedding dimensions and material commercial decisions remain open until resolved. Implement truthful unavailable states where allowed; never guess approvals to clear a milestone.

## MVP completion

All ROADMAP acceptance criteria must be evidenced: identity and ownership, resumable plot/season inputs, versioned ingestion with scientific gates, durable idempotent jobs and immutable plans, real dashboard, plan-bound non-mutating chat, and truthful marketing/pricing. Required security, migration, browser and integration checks must pass. G-010 needs independent reviewer evidence; G-020 needs approved retention/privacy/hosting and actual release checks. Local code completion, scientific activation and public release are separate states. Report verified features, exact test outcomes, blockers, environmental limits and local run instructions; never label a limited preview a complete MVP.
