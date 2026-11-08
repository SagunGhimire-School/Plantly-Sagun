# Copy/paste this into Codex with the extracted `plantly` folder open

```text
Build Plantly from this repository, beginning NOW with the smallest useful, runnable, testable full-stack skeleton. I want BARE-BONES functionality and an honest development state — not a polished mockup, not speculative features and not a replacement for the approved architecture.

Read root AGENTS.md, README.md, SETUP_CHECKLIST.md, docs/agent/ROADMAP.md, docs/agent/PROGRESS.md; read relevant sections of docs/PRODUCT.md, docs/ARCHITECTURE.md, docs/DESIGN.md, docs/LANDING_DESIGN.md and docs/DEVELOPMENT.md as required. Respect LOCKED/OPEN/GATE distinctions and don't silently override these documents. Preserve supplied contents. Current user instruction: implement incrementally, with the first priority being M-001 in the starter ROADMAP; future functionality remains minimal.

FIRST MILESTONE (M-001):
1. Create minimal working Next.js App Router in JavaScript/JSX, Tailwind CSS v4, and the approved Plantly token colors. Make one simple responsive landing page with visible links to login/pricing only when actual pages/routes exist; placeholder/coming-soon behavior must be truthful. Do not spend time on cinematic visuals, animation, stock art or optional component libraries yet. Use clearly marked missing-art slots where necessary.
2. Create a minimal Python FastAPI service and /health + /api/v1/health endpoints (liveness vs DB readiness must be distinguishable). Add a Next.js same-origin /api/v1/* proxy to the backend and verify the browser can reach it. Do not hardcode secrets or CORS shortcuts.
3. Use the supplied compose.yaml for local PostgreSQL with pgvector-capable image. Add minimal sync SQLAlchemy + psycopg3 and Alembic scaffolding where justified. Never invent model/embedding dimensions or apply agriculture rules. Create dependency/lock manifests and environment examples. Leave genuinely unneeded modules uncreated.
4. Make a basic verification path (at least frontend build/lint and backend health/test; DB check when Docker works), run real commands when tools are installed. Do not report missing tests as passed. Make startup and testing instructions work on Windows PowerShell.
5. Update docs/agent/PROGRESS.md with exact code delivered, actual checks, blockers and the next smallest step. Document any decisions/issues in the proper files.

AFTER M-001: If the foundation is really verified, advance in SMALL TESTABLE VERTICAL SLICES to actual secure auth, then persisted plot/onboarding, according to ROADMAP. Keep the design as simple as possible. Do not generate the whole architecture's empty file tree. No fake authenticated state or hardcoded demo authorization.

IMPORTANT LIMITS: `docs/curated_inventory.json` describes 15 source datasets/research files but their bytes are NOT supplied. Don't create pretend datasets or mark them ingested. No source or agronomy rule has been independently approved here. Disable real agronomic calculations until exact-rule human reviews and a supported crop/region/method are supplied. Do not invent laboratory values, weather, current prices, savings or research citations. Do not activate real AI/embedding calls without my model choices, provider credentials, and permission for any potential charges. Missing Gemini credentials must not block the initial non-AI functionality.

You may create/revise ordinary local files and run reversible local tests; don't deploy, spend money, alter unrelated projects, delete user data, or use destructive Git commands. Before installing an external service, dependency requiring payment or skill/plugin, tell me what's needed. If a required runtime isn't installed, create the code and report exactly which verification was blocked. At the end, tell me exactly what YOU built, what commands passed, what still needs my input or installations and how I can launch it.
```

The full product goal remains in the uploaded documents; the prompt prioritizes an **incremental minimal implementation** rather than pretending the entire application exists from the first pass.
