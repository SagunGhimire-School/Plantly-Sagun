# PLANTLY — ARCHITECTURE.md

> **Document:** Final architecture planning baseline, version 1.0  
> **Prepared:** 2026-11-07  
> **Status:** **APPROVED ARCHITECTURAL BASELINE — RELEASE GATES REMAIN OPEN**  
> **Target:** Publicly accessible, temporary hackathon MVP  
> **Application:** Plantly — evidence-conscious seasonal planning for home gardeners and small growers  
> **Source of authority:** Team decisions from Rounds 1–8, ARC-047 and ARC-048; `PRODUCT.md`; `DESIGN.md`; and the source-inspection report `PLANTLY_TEAMMATE_RAG_AUDIT.md`.  
> **Prototype inspected:** [`Ankit0200/Plantly`](https://github.com/Ankit0200/Plantly/tree/main), commit `d666bce0a5aa68867062c5bf8744425dedcf0e18` (read-only code audit, 2026-11-07). No runtime or scientific verification is implied.

## How to use this document

This is the **engineering source of truth** for *how* the approved Plantly product is built. `PRODUCT.md` determines **what/why**, and `DESIGN.md` determines **UI language, tokens, and interaction standards**. If these conflict, stop the affected work and request a product/architecture decision; do not silently reinterpret the documents.

**Status legend**

| Status | Meaning | Agent behavior |
|---|---|---|
| **LOCKED** | Team explicitly selected the architectural principle or behavior. | Implement as specified; propose changes instead of overriding. |
| **DESIGN CONTRACT** | The concrete implementation interpretation of a locked decision, documented here for consistency. | Implement unless contradicted by a newer team decision; flag infeasible contracts. |
| **DEFAULT / PROPOSED** | Sensible implementation detail, not separately approved as a product decision. | Safe to implement when reversible and not scientifically/business-material; document deviations. |
| **OPEN / RELEASE GATE** | Important unknown, missing evidence, or unselected provider. | Do not fabricate it; block dependent production functionality and expose honest disabled/unknown states. |
| **OBSERVED IN PROTOTYPE** | Confirmed by reading teammate code at the pinned commit, not by running it. | Reuse selectively; never confuse observed code with independently verified science. |

**Final** in the title refers to a coherent *architecture plan*, not a claim that every external provider, reviewed rule, or release configuration is decided. This file deliberately documents unresolved gates so Codex can build the approved system without inventing science or credentials.

---

## 1. Architecture in one page

### 1.1 Product and release boundary

Plantly creates a saved, per-plot/per-season **season blueprint** from user-entered facts, observed soil measurements, reviewed agronomic rules, approved research excerpts, and optional current weather/input prices. Gemini supplies constrained explanations and proposals; FastAPI validates and persists the result. Growers use the dashboard to understand and act on the saved plan and a context-bound chat drawer to ask *why* or explore *what if*.

**The MVP's functioning vertical slice**

1. Visitor sees marketing → creates account/logs in.
2. User saves and resumes a structured, multi-step plot/season intake draft.
3. User reviews and confirms their data; missing measurements are clearly unknown.
4. User requests a **generation job** after passing ownership, data and scientific-coverage gates.
5. Worker runs *only* reviewed rules applicable to the input, retrieves eligible research, calls Gemini for constrained narrative/proposals, validates all references, and persists an immutable `PlanBlueprintV1`.
6. Dashboard loads saved plan/action cards and honest soil, cost and weather states; generation status is truthful across refreshes.
7. User asks persistent plan-bound questions; authorized tools supply saved facts, evidence and non-persistent what-if comparisons.
8. User may edit plot inputs and request a new version; previous versions and evidence remain traceable.

**Outside the committed hackathon core:** native app, full farm ERP, IoT/sensors, satellite imagery, guaranteed yield/savings, automatic retailer checkout, unreviewed quantitative advice, enterprise/multi-user teams, automated code-written agronomic rules, real subscription charging, and autonomous alteration of saved plans. Product proposals for planting schedules, seasonal logs, trial pricing, automated pest notifications, file-based AI intake and extensive cost optimization must not be misrepresented as implemented unless separately delivered and tested.

### 1.2 Locked stack

| Concern | Selection | Status |
|---|---|---|
| Repository | One monorepo: `frontend/`, `backend/`, `docs/`, `data/curated/` | LOCKED |
| Frontend | Next.js **App Router**, **JavaScript** (`.js/.jsx`) | LOCKED |
| UI | Tailwind CSS v4, selective customized shadcn/ui, authoritative Plantly design tokens | LOCKED |
| Rendering | Server-rendered marketing/protected app shell; client-fetched interactive workspace | LOCKED |
| Client server-state | TanStack Query | LOCKED |
| Forms | React Hook Form + Zod; Pydantic independently on backend | LOCKED |
| Navigation | Desktop sidebar, mobile drawer; one navigation definition | LOCKED |
| API | Same-origin browser `/api/v1/*` proxy; FastAPI owns business logic | LOCKED |
| Backend | Python **FastAPI**, modular monolith, feature-based modules | LOCKED |
| DB access | **Synchronous** SQLAlchemy 2.x, psycopg 3, Alembic | LOCKED |
| Persistence | PostgreSQL; immutable JSONB plan versions + relational metadata | LOCKED |
| Retrieval | Repository-curated sources → PostgreSQL + pgvector | LOCKED |
| AI | Gemini behind provider adapter; rules + retrieval + validated constrained model output | LOCKED |
| Planning execution | PostgreSQL-backed queue, separate long-running Python worker | LOCKED |
| Identity | Custom Argon2id-password auth, random opaque DB-backed cookie sessions, CSRF and ownership checks | LOCKED contract direction |
| Session expiration | 12h inactivity, 7d absolute | LOCKED |
| Accounts | Public signup, temporary demo data; verification and reset deferred **for demo only** | LOCKED |
| Planning context | Grower-wide `seasons` joined to individual plots by `plot_seasons` | LOCKED |
| Scientific gate | Strict supported-scope and human-reviewed-rule enforcement | LOCKED |
| Scientific MVP | **Mixed scope**: reviewed crop rotation, soil interpretation, lab-backed lime arithmetic, narrowly approved fertilizer pathways | LOCKED (ARC-048) |
| Weather / prices | Live integrations when feasible; explicit stale/unavailable/unknown fallback | LOCKED |
| Model, embedding, crop/region, providers, hosting, cleanup interval | **Not yet selected** | OPEN |

### 1.3 Logical diagram

```text
             PUBLIC HTTPS ORIGIN
                      |
          Browser — Next.js App Router
       marketing | login | workspace | drawer
                      |
      browser fetch('/api/v1/...')
              same-origin proxy
                      |
               FASTAPI SERVICE
    authentication | ownership | REST | validation
     onboarding | plots | seasons | plans | chat
                      |
          +-----------+-------------+
          |                         |
      PostgreSQL               Plan job table
   + pgvector                     |
          |                   Python worker
          |                         |
    Research ingestion       Intelligence facade
    from data/curated       rules | retrieval | Gemini
          |                         |
          +-------------------------+
                       |
         versioned plans, source snapshots
                       |
                dashboard GETs

Independent external adapters: weather provider, retailer/product data,
Gemini generation model, embedding model. Never contact these from browser.
```

**Trust boundaries:** The Next.js application never accesses business tables directly. Browsers never receive API keys, database URLs, internal prompts or raw user session tokens. FastAPI checks session and resource ownership even for calls originating from Next server rendering. The worker does not trust model-proposed rule IDs, source IDs, numbers or instruction-bearing retrieved documents.

---

## 2. Decisions register and source reconciliation

### 2.1 Consolidated decision register

The historical ARC IDs are retained where assigned. The following is the canonical summary; full details appear in later sections.

| ID(s) | Decision | Status |
|---|---|---|
| R1–R2 | Next.js App Router + JS, FastAPI, PostgreSQL, custom auth, same-origin proxy, hybrid rendering, opaque sessions, monorepo, public demo | LOCKED |
| ARC-014 | Routes separate from feature implementations | LOCKED |
| ARC-015 | Integrated dashboard/plots/plan, weather/cost modules, chat drawer | LOCKED |
| ARC-016 | TanStack Query | LOCKED |
| ARC-017 | React Hook Form + Zod | LOCKED |
| ARC-018 | Tailwind v4 + selective shadcn/ui | LOCKED |
| ARC-019 | Login before onboarding | LOCKED |
| ARC-020 | Selected plot/season represented in URL | LOCKED |
| ARC-021 | Onboarding draft stored server-side | LOCKED |
| ARC-022 | Server shell + client-fetched interactive workspace | LOCKED |
| ARC-023 | Sidebar desktop / drawer mobile | LOCKED |
| ARC-024 | Persist chat bound to plot and plan version | LOCKED |
| ARC-025 | SQLAlchemy + Alembic | LOCKED |
| ARC-026 | PostgreSQL + pgvector research retrieval | LOCKED |
| ARC-027 | Repository-curated knowledge ingested into DB | LOCKED |
| ARC-028 | Gemini initial LLM provider | LOCKED |
| ARC-029 | Hybrid model: deterministic reviewed rules constrain model | LOCKED |
| ARC-030 | DB-backed independent planning worker | LOCKED |
| ARC-031 | Synchronous SQLAlchemy + psycopg 3 | LOCKED |
| ARC-032 | Immutable JSONB saved plans + relational metadata | LOCKED |
| ARC-033 | Evaluate embedding family/dimension first | **OPEN selection by design** |
| ARC-034 | Human-reviewed rules required for quantitative recommendations | LOCKED |
| ARC-035 | Live weather/pricing with truthful fallback | LOCKED |
| ARC-036 | Initial supported crop/region scope | **OPEN** |
| ARC-037 | Grower-wide seasons and plot-season associations | LOCKED |
| ARC-038 | Public signup | LOCKED |
| ARC-039 | Email verification/recovery deferred for temporary demo | LOCKED |
| ARC-040 | Session 12h idle / 7d absolute | LOCKED |
| ARC-041 | Strict scientific scope enforcement | LOCKED |
| ARC-042 | Feature-based backend modules, single lightweight bounded-retry worker | LOCKED |
| ARC-043 | Normalized domain schema and phased Alembic migrations | LOCKED |
| ARC-044 | Proposed REST/API/auth contracts approved in Round 8 | LOCKED |
| ARC-045 | Temporary demo user-data lifecycle; duration not chosen | LOCKED direction / OPEN duration |
| ARC-046 | Source-inventory template required | LOCKED |
| ARC-047 | Per-rule, per-version execution gate; unreviewed numerical rules disabled | LOCKED |
| ARC-048 | Small reviewed blend of qualitative and quantitative science | LOCKED |

### 2.2 Sources and which claims they support

1. `PRODUCT.md` (product baseline): target users, plot-specific seasonal blueprint, evidence, weather, costs, dashboard, plan-first chat, honesty, and scope. It contains `[PROPOSED]` product ideas and unapproved commercial language; this document cannot silently promote them to shipped commitments.
2. `DESIGN.md` / Plantly master design system: brand palette, spacing, typography direction, layout, accessibility, page modes. **Do not supersede its tokens in code.**
3. `PLANTLY_ARCHITECTURE_WORKING_DRAFT(1).md`: approved engineering decisions through Round 8; its statement that teammate code was not yet inspected is superseded by the subsequent audit.
4. `PLANTLY_TEAMMATE_RAG_AUDIT(1).md`: pinned, read-only code inspection. Not an execution test or agronomic peer review.
5. `PLANTLY_KNOWLEDGE_INVENTORY_TEMPLATE(1).csv`: the columns to use for research-source inventory; **a blank template is not proof of approved source coverage.**
6. Later explicit user decision: scientific MVP combines limited rotation/soil interpretation with reviewed lab-based lime and narrowly reviewed fertilizer calculations (ARC-048).

**Conflict resolution:** newer explicit team choices override earlier tentative suggestions. Examples: login-first overrides the product document's then-open gate; Gemini is approved even though teammate chat currently uses Claude; approved Next.js/JS/FastAPI architecture is not replaced by the teammate's Flask/Vite/TypeScript prototype.

---

## 3. Repository layout and module boundaries

### 3.1 Canonical proposed tree

Files marked `[when needed]` should **not** be generated empty for appearances. The tree names are a concrete implementation blueprint; folder ownership is fixed, while individual helper filenames are adjustable without changing public contracts.

```text
plantly/
├── AGENTS.md
├── README.md
├── .gitignore
├── .env.example
├── compose.yaml                         # local dev topology [DEFAULT]
├── docs/
│   ├── PRODUCT.md
│   ├── DESIGN.md
│   ├── ARCHITECTURE.md                  # this file
│   ├── TESTING.md                       # detailed test plan
│   ├── SCIENTIFIC_REVIEW.md             # review log and coverage [REQUIRED]
│   ├── DEPLOYMENT.md                    # fill after hosting decision
│   └── adr/                             # changes to locked decisions [when needed]
├── data/
│   └── curated/
│       ├── README.md
│       ├── sources.yaml                  # source manifest; validate against inventory
│       ├── research/                     # reviewed notes/excerpts, licensed where permitted
│       ├── datasets/                     # crop, rotation, method-specific tables, products
│       ├── rule_reviews/                 # versioned human-approval records
│       └── fixtures/                     # synthetic examples, never unlabeled live data
│
├── frontend/
│   ├── AGENTS.md
│   ├── package.json
│   ├── next.config.mjs
│   ├── jsconfig.json
│   ├── eslint.config.mjs
│   ├── components.json                  # shadcn selected pieces [when needed]
│   ├── .env.local.example
│   ├── public/
│   │   ├── brand/
│   │   ├── images/
│   │   └── icons/
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.jsx
│   │   │   ├── globals.css
│   │   │   ├── providers.jsx
│   │   │   ├── not-found.jsx
│   │   │   ├── (marketing)/
│   │   │   │   ├── layout.jsx
│   │   │   │   ├── page.jsx             # /
│   │   │   │   └── pricing/page.jsx
│   │   │   ├── (auth)/
│   │   │   │   ├── layout.jsx
│   │   │   │   ├── login/page.jsx
│   │   │   │   └── signup/page.jsx
│   │   │   └── (workspace)/
│   │   │       ├── layout.jsx
│   │   │       ├── dashboard/page.jsx
│   │   │       ├── onboarding/page.jsx
│   │   │       ├── plots/page.jsx
│   │   │       ├── plots/new/page.jsx
│   │   │       ├── plots/[plotId]/page.jsx
│   │   │       ├── plots/[plotId]/edit/page.jsx
│   │   │       ├── plans/[planId]/page.jsx
│   │   │       └── plans/generating/[jobId]/page.jsx
│   │   ├── api/
│   │   │   ├── client.js                # browser relative /api/v1 client
│   │   │   ├── server.js                # server-only credential-forwarding client
│   │   │   └── errors.js                # uniform API errors
│   │   ├── layouts/
│   │   │   ├── MarketingShell.jsx
│   │   │   ├── AuthShell.jsx
│   │   │   ├── WorkspaceShell.jsx
│   │   │   └── WorkspaceNavigation.jsx
│   │   ├── features/
│   │   │   ├── auth/
│   │   │   ├── onboarding/
│   │   │   ├── plots/                   # includes soil UI for MVP
│   │   │   ├── seasons/
│   │   │   ├── dashboard/
│   │   │   ├── plans/
│   │   │   ├── weather/
│   │   │   ├── costs/
│   │   │   ├── research/
│   │   │   └── chat/
│   │   ├── components/
│   │   │   ├── ui/                      # generic design primitives
│   │   │   └── feedback/                # loading/empty/error/status components
│   │   ├── context/                     # only truly shared transient UI context
│   │   ├── lib/
│   │   │   ├── formatters/
│   │   │   └── constants/
│   │   └── styles/tokens.css
│   └── tests/
│       ├── components/
│       └── e2e/
│
└── backend/
    ├── AGENTS.md
    ├── pyproject.toml
    ├── alembic.ini
    ├── .env.example
    ├── app/
    │   ├── main.py
    │   ├── api/v1/router.py
    │   ├── core/
    │   │   ├── config.py
    │   │   ├── security.py
    │   │   ├── exceptions.py
    │   │   └── logging.py
    │   ├── db/
    │   │   ├── base.py
    │   │   └── session.py
    │   ├── modules/
    │   │   ├── auth/
    │   │   ├── onboarding/
    │   │   ├── plots/                   # soil readings nested here
    │   │   ├── seasons/
    │   │   ├── plans/
    │   │   ├── research/
    │   │   ├── weather/
    │   │   ├── costs/
    │   │   └── chat/
    │   │       └── tools/               # authorized readonly / what-if tools
    │   ├── intelligence/
    │   │   ├── orchestrator.py
    │   │   ├── context_builder.py
    │   │   ├── validator.py
    │   │   ├── schemas.py
    │   │   ├── agronomy/
    │   │   │   ├── rule_registry.py
    │   │   │   ├── rotation.py
    │   │   │   ├── soil.py
    │   │   │   ├── lime.py
    │   │   │   └── nutrients.py
    │   │   └── costing/calculations.py
    │   ├── integrations/
    │   │   ├── llm/
    │   │   │   ├── base.py
    │   │   │   └── gemini.py
    │   │   ├── embeddings/
    │   │   │   ├── base.py
    │   │   │   └── gemini.py
    │   │   ├── weather/
    │   │   └── pricing/
    │   └── workers/
    │       ├── main.py
    │       └── plan_worker.py
    ├── migrations/versions/
    ├── scripts/
    │   ├── ingest_knowledge.py
    │   ├── seed_demo.py
    │   └── verify_sources.py
    └── tests/
        ├── unit/
        ├── integration/
        ├── contracts/
        ├── security/
        └── fixtures/
```

### 3.2 Ownership rules: frontend

- `src/app/`: only routing, segment layouts, route-level loading/error/empty handling and page composition; **no** agronomy calculations or bespoke business HTTP logic.
- `src/features/<domain>/`: feature components, `api.js` endpoint wrappers, `hooks/`, `queryKeys.js`, Zod `schema.js` and domain-specific view transformations. Create only the files a feature needs.
- `src/api/client.js`: centralized browser `fetch` with credentials, CSRF header for mutations, safe JSON parsing and typed-ish error normalization. **No feature endpoint knowledge.**
- `src/api/server.js`: marked `server-only`; calls internal FastAPI URL with allowed forwarded cookies; private responses not shared in cross-user Next caches.
- `src/components/ui/`: feature-neutral accessible primitives from approved design system; custom shadcn/ui pieces are styled to match Plantly.
- `src/components/feedback/`: reusable loading skeletons, problem/retry states, `MissingEvidence`, `StaleData`, `SourceStatus`, etc.; no fake numerical content.
- `src/layouts/`: shells/navigation responsive composition; navigation labels and destinations defined once.
- `src/context/`: transient, widely shared UI state **only if required**. No duplicate `AuthContext` user model, selected plot state or copied query cache.
- Pure formatting belongs in `lib/`, but formatting may never invent scientific precision or change units without a declared conversion.
- `features/dashboard/` composes cards from `plans`, `plots`, `weather`, `costs` and `research`; it does **not** own their calculations.

**Suggested feature anatomy:**

```text
features/plots/
  api.js
  queryKeys.js
  schema.js
  hooks/usePlot.js
  hooks/useUpdatePlot.js
  components/PlotCard.jsx
  components/PlotForm.jsx
  components/SoilMeasurementsForm.jsx
```

### 3.3 Ownership rules: backend

Each implemented feature uses a *thin* version of this convention:

```text
modules/plots/
  router.py       # FastAPI routes, dependencies, status codes
  schemas.py      # Pydantic input/output contracts
  service.py      # authorization, invariants, transactions
  repository.py   # SQLAlchemy reads/writes only
  models.py       # ORM tables/relationships
```

- Route handlers may call services; not repositories directly. They do not perform model calls or SQL.
- Services handle ownership and cross-table rules, coordinate transactions and invoke explicit public interfaces of other modules.
- Repositories never generate scientific recommendations or call external providers.
- `modules/plans` owns **lifecycle** (requests, jobs, plan versions). `intelligence/orchestrator` owns **computation** from immutable context and does not commit a plan independently.
- `modules/research` owns source catalog, versioning, retrieval/ingestion. `intelligence/agronomy` owns pure deterministic rules with review gating; do not duplicate review logic in chat and plan service.
- `integrations` wraps Gemini, embeddings, weather and pricing SDK/API behavior; adapters do not make final scientific decisions.
- Worker uses the same modules as API (one codebase), **not** its own duplicate rules engine.
- Database `Session` is process/request/worker-operation local; no global mutable Session, and no transaction spanning an external LLM request.

### 3.4 Explicit dependency direction

```text
Next app/routes ──> frontend features ──> frontend api transport
                     |                  └──> FastAPI REST
                     └──> shared UI/lib
FastAPI router ──> service ──> repository ──> database
                     |
                     └──> intelligence facade ──> pure agronomy rules
                                      |           └──> research service
                                      └───────────────> integrations
Worker ──> plans service + intelligence facade; no HTTP self-calls required
```

Forbidden cycles: dashboard owns weather/cost logic; chat invokes raw plot repositories bypassing plan ownership; SQLAlchemy ORM models import FastAPI routers; Gemini adapter imports presentation components; scientific rules import the persistence framework.

---

## 4. Frontend routes, rendering, state and interaction

### 4.1 Route inventory

Route groups do **not** contribute URL segments.

| Browser URL | Public? | Responsibility | UI state owner |
|---|---|---|---|
| `/` | Yes | Landing in approved marketing design | Server-rendered marketing |
| `/pricing` | Yes | Honest informational pricing/availability; **no invented plans/trial terms** | Marketing |
| `/signup` | Yes | Create account / establish session | RHF form; auth endpoint |
| `/login` | Yes | Authenticate, safe return destination | RHF form; auth endpoint |
| `/onboarding` | No | Resumable step wizard and review | RHF + DB draft |
| `/dashboard?plot=<uuid>&season=<uuid>` | No | Read-only assembled current context and actionable plan overview | URL + TanStack Query |
| `/plots` | No | List/add/choose owned plots | TanStack Query |
| `/plots/new` | No | Create an additional plot | RHF mutation |
| `/plots/[plotId]` | No | Plot profile, soil history, associated seasons | Route param + query |
| `/plots/[plotId]/edit` | No | Revise plot/soil values, explicit save | RHF mutation |
| `/plans/[planId]` | No | Immutable version, claims, evidence, limits | Route param + query |
| `/plans/generating/[jobId]` | No | Durable job status and genuine progress | Job polling query |

Dashboard query parameter names are `plot` and `season`; the FastAPI aggregator accepts `plot_id` and `season_id`. Routing helpers must map them explicitly, not pass arbitrary user query params into SQL.

**Routing decisions:**
- No selected plot stored in React Context. If URL parameters are absent, resolve an authorized default and navigate to a canonical URL; don't guess the first record if no valid default exists.
- No saved plot or no completed plan → helpful setup/next-action state, not fabricated dashboard numbers.
- Login-first: unauthenticated user is redirected to `/login` with a validated internal return URL; post-login users with incomplete onboarding resume the draft.
- Layout authentication gates improve UX but FastAPI endpoints are always protected independently. If a user is signed out during an active view, clear private query cache and route to login.
- The generating screen reads actual job phase; growing-plant animation is decorative/progressive, not an invented completion percentage; respect reduced-motion preferences.
- No dedicated weather/cost/research page in core MVP; modules appear inside dashboard/plan/plot details. Chat is drawer, not a separate core route.

### 4.2 Rendering and React state ownership

| Data | Authority | Frontend owner | Invalidation/navigation |
|---|---|---|---|
| User identity/session | FastAPI DB session | `GET /auth/me` TanStack Query | Clear on logout or 401 |
| Selected plot/season | Validated server resources | URL path/search params | Navigation updates URL |
| Persisted plot/soil/season | PostgreSQL | TanStack Query | Invalidate on mutation |
| Current draft editing | RHF | Component/form tree | Save at step boundary with revision |
| Saved onboarding draft | PostgreSQL | TanStack Query draft record | Optimistic revision conflict → reload/resolve |
| Generation progress | `plan_jobs` | TanStack Query polling | Stop at terminal state |
| Saved plan | Immutable DB version | TanStack Query | New version is distinct key; never overwrite old |
| Chat messages | PostgreSQL | Conversation query; composer React state | Invalidate on send; server validates all messages |
| Drawer open, tabs, mobile menu | Browser UI | Local React state; narrow Context only if needed | No backend mutation |
| Provider observations and timestamps | Source snapshots in FastAPI | TanStack Query | Refetch/invalidate based on provider age and explicit user action |

Proposed key conventions:

```javascript
export const queryKeys = {
  auth: ['auth', 'me'],
  plots: ['plots', 'list'],
  plot: (id) => ['plots', 'detail', id],
  seasons: ['seasons', 'list'],
  dashboard: (plotId, seasonId) => ['dashboard', plotId, seasonId],
  plan: (planId) => ['plans', 'detail', planId],
  job: (jobId) => ['plans', 'job', jobId],
  chat: (conversationId) => ['chat', 'messages', conversationId],
};
```

Configure query invalidation based on authoritative response changes; do not use a second global store to mirror fetched objects. Server-side authenticated data, if prefetched later, must be request-isolated; current locked rendering policy keeps server prefetch minimal.

### 4.3 UI component contracts

**MVP dashboard composition, top to bottom:**
1. Context bar: selected plot, grower-wide season, location generality, last plan/version and status.
2. Primary recommended next action(s) / plan limitation banner (what matters now).
3. Small set of grounded metrics: plot area, actual measurements, observed/forecast weather, plan-estimated input costs **only if available**.
4. Crop rotation and soil-interpretation cards with evidence/conditions.
5. Approved lime/fertilizer action cards; otherwise explicitly indicate what lab field/review is required.
6. Season plan/timeline (only evidence-backed windows and tasks; no invented planting dates).
7. Cost/product options and current source freshness where available; no misleading savings.
8. Source notes, assumptions and `Talk to your data` drawer.

Cards accept a common meaningful data state: `ready | partial | insufficient_data | unsupported | unavailable | stale | sample`. A numerical field is `{value, unit, provenance, observed_at, source_ref}` or explicitly null/unavailable, not a bare string disguised as a measurement. Warnings are text plus icon, not color alone.

**Design authority (do not redefine):** emerald `#1B3625`, emerald hover `#244B33`, bright green `#4E9F3D`, lime `#76B947`, ink `#111813`, white `#FFFFFF`, soft white `#F9F9F9`, border `#E5EAE6`; canonical 1360px maximum container and 20px / 14px / 10px cards/panels/controls. Marketing = **PERSUADE**; workspace = **OPERATE**; assistant = **EXPLAIN**. Exact responsive breakpoints and accessibility checks belong to `DESIGN.md`; do not import the teammate prototype's UI aesthetics by default.

### 4.4 Frontend accessibility and failure behavior

Use semantic labels/errors, keyboard navigation, visible focus, accessible modal/drawer focus traps, reduced-motion preference, appropriate contrast, unit labels, stable layout and no horizontal overflow at the design document's review sizes. Render generative text as **escaped text** or carefully sanitized Markdown with allowlisted links; never raw unsanitized HTML or `dangerouslySetInnerHTML` from model strings. Every API action provides idle/loading/error/success feedback and an actionable retry when safe.

---

## 5. Authentication, authorization, sessions, CSRF and account lifecycle

### 5.1 Identity model

Custom email/password sign-up, login and logout; Argon2id password hash with maintained library. Accounts are user-scoped (no teams/organizations in MVP). Public signup is supported, with explicit demo restrictions and rate limits. Email verification and recovery are deferred **only for this temporary demo**; no UI should claim an unverified address is verified. Real public launch requires revisiting recovery and abuse controls.

### 5.2 Session lifecycle contract

1. On successful login/signup, issue cryptographically secure random opaque bearer token (e.g. 32 random bytes); never make it predictable from user/time.
2. Save a hash/verifier of token in `user_sessions`, associated with user, created time, last activity, absolute expiry and revocation state. Never persist raw bearer token.
3. Set browser cookie in production: `__Host-plantly_session`, `Secure`, `HttpOnly`, `SameSite=Lax`, `Path=/`, **no Domain**.
4. On every protected request FastAPI verifies token hash, user status, `revoked_at`, absolute age and idle limit. Locked limits: **12 hours inactivity**, **7 days absolute**.
5. Ordinary eligible user actions may refresh `last_seen_at` with throttled DB writes; background status polling alone must not keep the session alive indefinitely.
6. On logout, revoke server session, expire cookie, clear authenticated TanStack Query caches and navigate to login. On expired session, protected endpoints return `401`, not a new anonymous plan.
7. HTTP local development may use a clearly different dev-only cookie configuration; production refuses insecure cookies.

**Same-origin proxy:** Browser sends cookies to Next.js origin; requests to `/api/v1/*` are forwarded to FastAPI. Preserve appropriate `Set-Cookie`, headers, methods and status codes. FastAPI must validate `Origin` against a configured public application origin, not trust spoofable forwarded host data indiscriminately. Avoid exposing an alternative credentialed public API origin with weaker controls.

### 5.3 CSRF strategy

Use server-generated, session-bound CSRF protection on **all authenticated mutations**, including logout and chat submission; browser sends `X-CSRF-Token`. Check allowed `Origin` and relevant Fetch Metadata headers as defense-in-depth. Public login/signup need a short-lived **pre-auth challenge** or equivalently reviewed CSRF approach plus strict Origin checks; the cookie's `SameSite` attribute is not the only defense. Safe `GET` routes must have no persistence side effects. Store only the minimally required CSRF state in approved server-side/session configuration, do not place session bearer token in JS-readable storage.

### 5.4 Authorization ownership patterns

- Every plot query/mutation scopes to authenticated `user_id`.
- Every `season` belongs to one user; `plot_seasons` may associate only plot and season of the **same owner**.
- Every job, plan version, chat and source disclosure tied to user content validates the entire ownership chain. Knowing a UUID is never authorization.
- Where masking resource existence is appropriate, return `404` rather than confirming another user's plot exists.
- Use filtered repository queries and transactional invariants; Next layouts do **not** substitute for backend authorization.
- Rate limits separately cover signup/login, chat, plan generation, and provider-cost budget. Use appropriate safe rejection (`429`) and server logs with redaction.
- Passwords, tokens, prompts with personal context, exact private coordinates, provider credentials and raw document uploads must not be logged.

### 5.5 Temporary-demo retention

**LOCKED:** accounts and user content are temporary. **OPEN:** deletion window in days and log-retention policy. A user-facing notice must communicate this before public signup. Implement user-initiated deletion or an explicit admin cleanup workflow; deletion covers user sessions, drafts, plots, seasons, plans, chat, and identifiable provider-context snapshots while preserving only permitted anonymous operational logs. Do not launch the public demo before retention, deletion job, and operator responsibility are documented.

---

## 6. PostgreSQL domain model and integrity

### 6.1 General conventions

Use UUID primary keys, `timestamptz` for instants, SQL `DATE` for local planting calendar dates, `NUMERIC` for meaningful precise quantities/currency, JSONB for incomplete draft and versioned generated snapshots, and explicit units/currencies. Make migrations explicit and reviewed; never run `Base.metadata.create_all()` in production startup. Index lookups by owner and foreign key, not only by opaque UUID.

### 6.2 Identity and onboarding tables

| Table | Required fields | Required constraints |
|---|---|---|
| `users` | `id`, `email_normalized`, `password_hash`, `created_at`, `disabled_at` | unique email, valid hash |
| `user_sessions` | `id`, `user_id`, `token_hash`, `created_at`, `last_seen_at`, `expires_at`, `revoked_at` | unique verifier, foreign key to user, expiration checks |
| `onboarding_drafts` | `id`, `user_id`, `draft_data JSONB`, `revision`, `schema_version`, `status`, `updated_at` | one active draft per user in MVP; optimistic version; partial validation |

Drafts may be incomplete; they are **not** finalized plots. A draft has `draft | completed | abandoned` semantic state as appropriate (exact enum field implementation is adjustable). Completion validates all required fields, is transactional and idempotent, and creates the intended plot/season/plot-season association **once**.

### 6.3 Growing records and scientific observations

| Table | Required fields | Required constraints |
|---|---|---|
| `plots` | `id`, `user_id`, `name`, `area_m2`, `location_data`, `revision`, timestamps | positive area, owner FK; canonical square meters |
| `seasons` | `id`, `user_id`, `label`, `year`, `start_date`, `end_date`, `status` | owner FK; date bounds validated |
| `plot_seasons` | `id`, `plot_id`, `season_id`, `goals JSONB`, `budget_amount`, `currency`, `revision` | unique `(plot_id, season_id)`; same owner |
| `season_crops` | `id`, `plot_season_id`, `crop_code`, `state`, `planted_on`, `harvested_on` | valid plot-season; declared crop catalog ID and state |
| `soil_tests` | `id`, `plot_id`, `sampled_at`, `laboratory`, `extraction_method`, `sample_depth`, `report_ref` | provenance preserved; user authorization |
| `soil_measurements` | `id`, `plot_id`, nullable `soil_test_id`, `metric`, `value NUMERIC`, `unit`, `source_type`, `observed_at` | consistent source type; unit compatibility; metric bounds |

Soil pH or N/P/K must never default to fake non-null readings. `soil_test_id` is nullable for independently entered observations, but those observations are **not labeled lab verified**. A lab lime rate, if present, must retain its original lab method/unit, user confirmation and report provenance. Model soil nutrient testing method and sample depth explicitly before using numeric interpretation thresholds; raw `ppm` alone does not establish comparability across laboratories.

Scope-dependent inputs (compost availability, irrigation, pest history, past input usage, budget) may initially be in typed plot-season/draft records and captured input snapshots; introduce independent event/inventory tables only when real CRUD or reporting requires them. Do not create fake measurements to satisfy a schema.

### 6.4 Research, embeddings and reviewed rules

| Table | Required fields | Purpose |
|---|---|---|
| `research_sources` | stable source ID, title, organization, URL/DOI, license/status | publication identity |
| `research_source_versions` | version ID, source ID, content hash, review status, reviewer/date, applicability | immutable reviewed source revision |
| `research_chunks` | ID, source-version ID, chunk index, text, section/page, topics, metadata/hash | retrievable evidence passage |
| `embedding_models` | ID, provider/model, dimensions, task/configuration, embedding family | prevent mixed vector spaces |
| `research_embeddings` | chunk ID, embedding-model ID, vector | semantic index, dimension-specific |

**Additional execution-gate metadata required by ARC-047/048:** versioned reviewed rule manifests (`rule_id`, `rule_version`, evidence version IDs, reviewer/time, allowed crop/region/method, required inputs, enabled status, validated tests). **Physical storage choice is a DEFAULT**: mirror versioned `data/curated/rule_reviews/` into `scientific_rule_versions` and `rule_approvals` tables, or another equivalent auditable immutable store. This is an implementation refinement to the Round-8 approved research model, not license to mark existing YAML rows reviewed. A rule is executable only if an authoritative current approval record exists.

The vector index's model and dimensionality are **OPEN**. Do not create a falsely dimensioned migration before choosing/pinning an embedding model and verifying provider access. If the ingestion index supports multiple embedding families, searches must select one compatible index.

### 6.5 Planning and immutable results

| Table | Required fields | Guarantees |
|---|---|---|
| `plan_jobs` | `id`, owner, `plot_season_id`, `idempotency_key`, `request_hash`, `input_snapshot JSONB`, input fingerprint, status/phase/attempt, retry/lease fields, timestamps/errors | durable, owner-scoped generation command |
| `plan_versions` | `id`, `plot_season_id`, `generation_job_id`, version/schema number, `blueprint JSONB`, `input_snapshot JSONB`, corpus/rules/model versions, created time | immutable historically explainable result |
| `plan_evidence` | plan version, recommendation ID, reviewed source/chunk version ID | saved claim-to-evidence association |

Constraints: `UNIQUE(plan_versions.generation_job_id)` and `UNIQUE(plot_season_id, version_number)`; idempotency key unique in its owner/request namespace. Version allocation must serialize safely under concurrency. Once a plan is saved, **do not mutate its blueprint or historical evidence**. Determine `is_outdated` from saved fingerprint compared with current applicable inputs; if cached, it is a derived state with documented invalidation.

### 6.6 Conversations and external snapshots

| Table | Required fields | Note |
|---|---|---|
| `chat_conversations` | ID, user ID, plot-season ID, bound plan-version ID, timestamps | fixed plan context |
| `chat_messages` | ID, conversation ID, role, content, citations/provenance, timestamps | orderable and owner-protected |
| `weather_snapshots` | ID, location scope, provider, forecast/observation validity, retrieved_at, typed data/payload | distinguishes observation vs forecast |
| `price_observations` | ID, item/retailer ref, URL, package unit/size, currency, price, observed_at, availability | source/time-specific price, not current by assumption |

The same historical plan may reference specific weather/price snapshots; current dashboard cards can show fresher data without changing the saved plan's original assumptions. Prices used for calculations must identify package size, currency and whether delivery/tax is included; missing price means **unknown**, not zero.

### 6.7 Indexes and deletion semantics

At minimum: `users(email_normalized)`, `user_sessions(token_hash)`, `plots(user_id)`, `seasons(user_id)`, `plot_seasons(plot_id,season_id)` unique, `soil_measurements(plot_id,observed_at)`, `plan_jobs(status,next_retry_at,created_at)`, `plan_versions(plot_season_id,version_number)` unique, `chat_messages(conversation_id,created_at,id)`, research review/applicability filters, and embedding similarity index when justified by corpus size/model. Small corpus retrieval may use exact pgvector similarity without approximate indexes.

Use explicit `ON DELETE` policies: user deletion cascades or orchestrates personal records, but reviewed research source versions referenced by retained plans are not silently deleted or changed. If removing a user requires removing the corresponding plan evidence edges, distinguish shared research metadata from user-specific evidence links.

---

## 7. Alembic migration and bootstrap plan

| Logical migration | Creates | Dependencies / gate |
|---|---|---|
| `0001_identity` | `users`, `user_sessions` | auth design |
| `0002_growing` | `plots`, `seasons`, `plot_seasons`, `onboarding_drafts` | identity |
| `0003_science_inputs` | `season_crops`, `soil_tests`, `soil_measurements` | growing |
| `0004_knowledge` | `research_sources`, `research_source_versions`, `research_chunks`, approval metadata | research schema |
| `0005_vectors` | pgvector extension, embedding models, vector storage | **BLOCKED until model/dimension chosen** |
| `0006_planning` | `plan_jobs`, `plan_versions`, `plan_evidence` | growing/research |
| `0007_chat` | `chat_conversations`, `chat_messages` | planning/auth |
| `0008_external` | weather and price snapshots | integration interfaces |

These are logical phases, not promises that all migrations will have those literal Alembic IDs. A migration's table set may be refined to satisfy dependency ordering without changing domain ownership. Alembic autogenerate is a review aid, **not** proof that migration SQL is correct. A clean database must migrate deterministically; test upgrade from the previous known revision and pgvector compatibility. Deployment applies migrations **once** before API/worker startup; failure blocks rollout.

**Fresh development bootstrap (design contract):**

```text
1. Copy example env; provide locally scoped secrets (not committed).
2. Start PostgreSQL with pgvector-supported image/extension.
3. Install backend and frontend pinned dependencies.
4. Apply Alembic migrations.
5. Ingest vetted source manifest, datasets and review records.
6. Embed approved chunks once chosen model/dimensions are configured.
7. Start FastAPI + independent worker + Next.js.
8. Run health, auth, onboarding, job, dashboard and chat smoke tests.
```

**Do not use SQLite as a substitute** for PostgreSQL concurrency, JSONB or pgvector integration tests. No silent database destructive reset in production. `seed_demo.py` must create conspicuously labeled synthetic data in a demo/test environment only.

---

## 8. HTTP API contract (`/api/v1`)

### 8.1 API conventions

- Browser always calls same-origin `/api/v1`; server-only Next API client uses private FastAPI base URL and forwards only necessary authenticated credentials.
- Success returns resource-specific JSON body; no redundant universal `data` wrapper mandated.
- Errors use stable machine codes, safe user-facing message, field error mapping and correlation ID.
- Every protected endpoint performs owner/permission checks; `GET` never mutates persistent data.
- UUIDs are path parameters, not ownership claims.
- Pagination and list size caps are **DEFAULT** for growing lists; exact caps configurable. Server request body/file limits mandatory.
- API schemas are Pydantic with `extra='forbid'` for sensitive command DTOs (especially model proposals). Avoid silently accepting unknown scientific fields.
- OpenAPI generated by FastAPI is a review artifact, not a substitute for domain tests.

**Canonical error JSON:**

```json
{
  "error": {
    "code": "INPUT_REVISION_CONFLICT",
    "message": "Your saved information changed. Reload it before continuing.",
    "fields": {},
    "request_id": "request-uuid"
  }
}
```

Suggested semantics: `200` read/update, `201` new resource, `202` async accepted, `204` successful no body, `400` malformed, `401` unauthenticated, `403` forbidden, `404` unavailable/masked, `409` conflict, `422` invalid or unsupported scientific inputs, `429` throttled, `503` temporarily unavailable critical dependency. Exact error codes and mappings must be reflected in contract tests.

### 8.2 Endpoint inventory

| Area | HTTP routes | Owner / purpose |
|---|---|---|
| Auth | `POST /auth/signup`, `POST /auth/login`, `POST /auth/logout`, `GET /auth/me`, `GET /auth/csrf` | account + secure session |
| Onboarding | `GET /onboarding/draft`, `PUT /onboarding/draft`, `POST /onboarding/complete` | persisted revision-controlled draft and completion |
| Plots | `GET /plots`, `POST /plots`, `GET /plots/{plot_id}`, `PATCH /plots/{plot_id}` | owned plot CRUD |
| Soil | `GET /plots/{plot_id}/soil-measurements`, `POST /plots/{plot_id}/soil-measurements` | dated observations |
| Seasons | `GET /seasons`, `POST /seasons`, `GET /seasons/{season_id}`, `GET /seasons/{season_id}/plots` | grower-wide season membership |
| Planning | `POST /plots/{plot_id}/plan-generations`, `GET /plan-jobs/{job_id}`, `GET /plans/{plan_id}` | async command, job state, versioned result |
| Dashboard | `GET /dashboard?plot_id=...&season_id=...` | read-only aggregate |
| Chat | `POST /chat/conversations`, `GET /chat/conversations/{id}/messages`, `POST /chat/conversations/{id}/messages` | persistent plan-bound chat |
| Research/status | `GET /research/sources/{source_id}` or plan-scoped evidence detail | **PROPOSED** safe citation lookup; public catalog exposure undecided |
| Weather/prices | dedicated versioned read/refresh endpoints | **OPEN** provider and refresh policy; do not invent |
| Account deletion | `DELETE /auth/me` or equivalent reviewed workflow | **OPEN** exact route/retention policy |

API routes under the table are relative to `/api/v1`. The additional proposed research/deletion routes are not part of the Round-8 approved fixed route list; require contract review when implemented.

### 8.3 Onboarding example and state transition

`PUT /api/v1/onboarding/draft`

```json
{
  "expected_revision": 4,
  "step": "soil",
  "draft_data": {
    "plot_name": "Raised Bed A",
    "soil": {"ph": null, "p": null, "k": null}
  }
}
```

This is **illustrative DTO structure**, not the final step JSON schema. Draft update must reject revision mismatch (`409`) and return updated draft/revision. Unfilled fields remain null. `POST /onboarding/complete` uses stricter validation and commits user-scoped plot, season, plot-season records atomically. Onboarding can be completed without a full soil test when the current product requirements allow it; the scientific engine will abstain for dependent calculations instead of silently using defaults.

### 8.4 Plan generation command

`POST /api/v1/plots/{plot_id}/plan-generations` with `Idempotency-Key` header:

```json
{
  "season_id": "season-uuid",
  "expected_input_hash": "canonical-sha256-input-fingerprint"
}
```

FastAPI validates session, same owner for plot/season, `plot_seasons`, input version/fingerprint, required fields, approved crop+region+soil-method applicability and quotas. Then it stores an **immutable** normalized snapshot and inserts a job in the same transaction. `expected_input_hash` is computed server-side and presented to the client during review; the client does **not** supply raw authoritative research context.

First accepted response (`202`):

```json
{
  "job_id": "job-uuid",
  "status": "queued",
  "status_url": "/api/v1/plan-jobs/job-uuid"
}
```

Same owner/idempotency key/identical request hash returns the existing job; same key/different request returns conflict. Enforce request capacity and at-most-one-active-job policy per plot-season if selected by implementation configuration; concurrent plan version allocation must still be safe.

### 8.5 Status and result

`GET /api/v1/plan-jobs/{job_id}` returns:

```json
{
  "job_id": "job-uuid",
  "status": "running",
  "phase": "retrieving_evidence",
  "attempt": 1,
  "plan_id": null,
  "error": null
}
```

On success, `status='succeeded'`, `plan_id` references immutable saved result. On terminal failure return a stable code and user-safe actionable explanation, not an internal prompt/stack trace. Do not invent `progress_percent` based on time.

`GET /api/v1/plans/{plan_id}` returns a `PlanBlueprintV1` or a wrapper with stable `id`, `version`, timestamps and blueprint. Do not return raw Gemini text as the product contract.

### 8.6 Dashboard aggregator

`GET /api/v1/dashboard?plot_id=<uuid>&season_id=<uuid>` composes *saved* plan + related stored observations + available fresh/stale external context. It never invokes Gemini per page request. Proposed shape:

```json
{
  "context": {"plot_id": "plot-uuid", "season_id": "season-uuid"},
  "plan": {"id": "plan-uuid", "status": "ready", "is_outdated": false},
  "next_actions": [],
  "soil": {"observations": [], "missing_data": []},
  "weather": {"status": "unavailable", "observed_at": null},
  "costs": {"status": "insufficient_data", "estimated_total": null},
  "limitations": []
}
```

`ready` is an illustrative *view status*, not a separate requirement to persist a mutable status on immutable plan rows. An absent plan must be represented as absent. Pricing and weather freshness must be independent from plan staleness.

---

## 9. Scientific MVP: reviewed-rule gate and release science policy

### 9.1 Locked mixed-scope behavior (ARC-047, ARC-048)

Plantly enables **a narrow reviewed subset of both qualitative and quantitative agronomy**:

| Feature | Allowed when | Failure/unknown behavior |
|---|---|---|
| Rotation warning/alternative | Approved crop-family/problem history rule applies to selected crop/region/history | General missing/unsupported notice; no unreviewed crop-specific proposal |
| Soil interpretation | Dated measurement with compatible unit, extraction method/region and reviewed threshold | Show observed value but do not classify from inapplicable thresholds |
| Lab-backed lime quantity | User-supplied lab recommendation and compatible unit/plot area, confirmed provenance and reviewed calculation path | Request laboratory rate; never use placeholder pH→rate table |
| Limited fertilizer amount | Exact reviewed rule version, compatible soil-test extraction method, relevant crop/region, method, and all required measured fields | `insufficient_data` or `unsupported`; never model-invent a rate |
| Product quantity/cost | Scientifically authorized quantity plus product assay/package/price provenance | Distinguish quantity from uncertain price; omit unsupported totals |

**No specific crop, geographic region or nutrient method has been scientifically approved yet.** The initial execution set is therefore **empty until completed human review**. Synthetic fixtures may demonstrate mechanics only when visibly labeled; they cannot masquerade as accepted real-user recommendations.

### 9.2 Rule approval record

Store review information per version, not a mutable blanket `verified: true` toggle:

```yaml
rule_id: ROT-01
rule_version: 1
review:
  status: pending_review         # pending_review | approved | disabled
  reviewer: null
  reviewed_at: null
applicability:
  crop_ids: []
  region_ids: []
  soil_test_methods: []
required_inputs: [crop_history, planned_crop]
evidence:
  source_version_ids: []
  approved_claim_ids: []
execution:
  enabled: false
  implementation_ref: intelligence.agronomy.rotation
```

This is a **schema template**, not approval of `ROT-01`. The gate checks: rule/implementation version, `approved` state, reviewer, evidence version, scope, measurement method/unit, required inputs and required regression tests. A rule with any unmet condition **must abstain**. AI prompts and UI flags never override this gate.

### 9.3 First review queue (all pending)

| Candidate | Prototype evidence | Review requirement | Initial execution |
|---|---|---|---|
| `ROT-01`, `ROT-02`, `ROT-03` | `rotation_rules.yaml` and `soil_engine.py` | Review crop families, cross-family disease exceptions, lookback, applicability | disabled until review |
| Crop-specific pH targets | `crops.yaml` | Verify exact crops/region/condition and interpretation wording | disabled until review |
| `STL-P`, `STL-K` | `soil_test_levels.yaml` | Check extraction method, soil type, sample units, thresholds | disabled until review |
| `LAB-LIME` | lab-rate branch in `soil_engine.py` | Confirm actual lab-reported rate, area/unit conversion, review of prescribed calculation | disabled until reviewed, though formula can be unit-tested |
| `LIME-*` | `lime_table.yaml` | Prototype explicitly says rates are **placeholders** | **quarantined; no live fallback** |
| Selected `NUT-*` | `nutrient_recs.yaml` | Narrow soil method + region + crop + primary publication review | disabled until review |
| `CRED-*` | `credits.yaml` | Compost analysis, previous-legume assumptions, bounded use | disabled until review |
| Product facts | `products.yaml` | Verify N-P2O5-K2O assay and package; price separately verified | not a scientific rate authorization |

### 9.4 Scientific review checklist

For each candidate action or formula, a reviewer records:

- Stable rule ID/version, source version, exact page/section or reviewed excerpt, publication, method, license and hash.
- Crop/crop-family, geographic/soil/climate applicability, exclusions and date/validity.
- Required measurements (unit, method, sampling depth, lab methodology), input conversions and allowed precision.
- Written derivation of numerical computation (if any) and independently expected test examples.
- Risk/limitation language, absence behavior, cross-rule precedence and conflicts.
- Reviewer name/date, approval decision and commit/reference that activates the version.
- Evidence quality: do citations actually support that claim, rather than merely share keywords?

The source inventory template `PLANTLY_KNOWLEDGE_INVENTORY_TEMPLATE(1).csv` contains complementary metadata columns and should be populated from **actual** papers and datasets. The team must review original source text or its permitted authoritative excerpts; an AI-written summary is not a human review.

### 9.5 Scientific uncertainty and claims

- Distinguish `measured`, `user_entered`, `lab_reported`, `calculated`, `estimated`, `forecast`, `sample`, and `unknown`.
- Never invent sensor data, soil-health percentages, yield gains, pest reduction, or saved-money claims.
- Source and rule IDs exist for the output, but source identity alone does not prove the cited claim is supported.
- Never silently assume `P ppm` or `K ppm` are equivalent across laboratory extraction methods.
- Unsupported inputs might permit storing a plot and displaying a data-gap dashboard, but **not** a falsely complete crop-specific blueprint.
- Show local-extension/qualified-agronomist guidance for important or unsupported interventions.

---

## 10. Teammate prototype: migration rather than replacement

### 10.1 Observed implementation (pinned GitHub commit)

The inspected teammate repository contains:

- Flask `/api/check`, synchronous `/api/plan`, `/api/chat`, `/api/intake`, `/api/explain-line` endpoints.
- `backend/engine/soil_engine.py`: deterministic ordered YAML lookup/calculation pipeline: rotation → lime → P/K interpretation → nutrient needs → credits/compost → fertilizer/products → warnings → prevention → totals.
- `backend/ai/ai_tools.py`: `get_plan`, `run_what_if`, `explain_rule`, `lookup_data`, `search_notes`; local BM25-style note search.
- `backend/ai/chat.py`: Claude/Anthropic tool-calling loop; heuristic warning for some unsupported numbers (not sufficient enforcement).
- `backend/ai/intake.py`: Claude-assisted free-form/PDF/image extraction (not needed for manual-entry core).
- `/api/explain-line`: separate Gemini call; it is **not** the main RAG loop.
- Frontend Vite+TypeScript, local-only state; no accounts, PostgreSQL, immutable plan persistence, pgvector or worker.

Inventory from the pinned inspection: **21 crop entries, 40 source entries, 122 research notes, 3 rotation rules, 15 placeholder lime rows, 8 nutrient rows, 2 soil rating rows, 2 credit rows, 5 product entries and 4 synthetic fixtures**. These counts are implementation inventory, **not coverage approval**.

### 10.2 Reuse and replacement decisions

| Prototype element | Action | Destination / safeguard |
|---|---|---|
| Deterministic steps and per-line `rule_id`, `source_id`, `inputs_used` | **ADAPT** | Pure `intelligence/agronomy/`; review gate before numeric execution |
| YAML source IDs / data digest | **ADAPT** | `data/curated/` + idempotent PostgreSQL ingestion/versioning |
| `search_notes` BM25-style retrieval | **RETAIN AS BASELINE/FALLBACK** | Evaluate beside metadata-filtered pgvector |
| Tool vocabulary | **ADAPT** | Authorized saved-plan tools in `modules/chat/tools/` |
| Read-only `run_what_if` deep-copy behavior | **PRESERVE** | Separate non-persistent comparison; saving needs explicit confirmation/new job |
| Anthropic chat client | **REPLACE PROVIDER LAYER** | Gemini adapter with constrained function calling and validations |
| Flask routes | **REIMPLEMENT TRANSPORT** | Approved FastAPI modules, preserve useful domain semantics |
| Vite/TS frontend | **REFERENCE UX ONLY** | Approved Next.js/JS design-system implementation |
| Claude intake/extraction | **DEFER** | Optional validated document upload later, not a hackathon dependency |
| Regex unsupported-number guard | **REPLACE ENFORCEMENT** | Pydantic typed claims/quantities, authorized-source reference checking |
| `dangerouslySetInnerHTML` explanation rendering | **DO NOT PORT** | Escaped text/sanitized Markdown |
| Fake preset soil pH/NPK form values | **DO NOT PORT** | null/unknown, clear sample fixture distinction |
| Placeholder lime/pseudo-current product price rows | **QUARANTINE** | Not live scientific/retailer evidence |

The prototype's existing offline tests are useful regression references, but the code audit did not execute them and they do **not** establish agronomic correctness. Preserve tests that prove deterministic behavior; change expected quantitative fixtures as review decisions require.

---

## 11. Research ingestion, metadata filtering, pgvector retrieval

### 11.1 Knowledge classes and storage choices

| Knowledge class | Canonical authoring | Runtime storage | Retrieval method |
|---|---|---|---|
| Reviewed crop taxonomy/rule inputs | `data/curated/datasets/` + rule-review records | relational SQL catalog/typed rows | exact scoped SQL |
| Research source metadata | source manifest + original reference | `research_sources`/versions | exact IDs and metadata filters |
| Reviewed explanatory passages | Markdown/approved extracted segments with page refs | `research_chunks` | scoped keyword/full-text and pgvector similarity |
| Vector representation | regenerated by ingestion | `research_embeddings` | same-model/cosine or configured distance |
| User soil/plot/history | user data via FastAPI | owned relational tables | authenticated exact SQL |
| Weather/retail price | provider records | timestamped snapshots | typed queries, freshness constraints |

### 11.2 Ingestion command contract

`python -m scripts.ingest_knowledge` (illustrative command path; exact CLI may differ) should:

1. Load a manifest and structured dataset files; check known schema, fields, source IDs and allowed media/license.
2. Verify content hashes and source versioning; preserve old versions referenced by plans.
3. Record review status and reviewer evidence; **never auto-approve** a newly ingested source.
4. Normalize approved structured tables and units, rejecting invalid crop codes/method combinations.
5. Chunk scientific notes by meaning/section, preserve original page/section and source version; no invented page numbers.
6. Embed only eligible chunks in the selected embedding space; batch + rate-limit with retry; no mixed dimensions.
7. Upsert idempotently by stable ID/version/content hash, with explicit report of new, unchanged, superseded and invalid rows.
8. Produce an audit log/report without exposing proprietary full documents or API secrets.

For external copyrighted PDFs, store citations and permitted excerpts/notes in Git; do not redistribute originals without permission. Unreviewed notes may be retained for future human analysis but **must be excluded from claim-authorizing retrieval**.

### 11.3 Retrieval contract

Proposed service interface:

```python
retrieve_evidence(
    query: str,
    crop_ids: list[str],
    region_id: str | None,
    soil_test_method: str | None,
    approved_only: bool = True,
    limit: int = 6,
) -> list[EvidenceChunk]
```

**Required sequence:**
1. Validate available scope and query intent; no unsupported crop/region authorization.
2. SQL metadata filters: reviewed source version, applicable crop/region/method/topic, allowed source use, current corpus version.
3. Semantic similarity among eligible chunks in a selected *compatible* embedding space; optionally combine with reviewed keyword search for small corpora.
4. Return stable chunk/version ID, excerpt, section/page, title/URL, applicability, review status and ranking metadata.
5. Downstream validator checks that each final claim is supported by its cited chunk and relevant conditions; ranking scores are **not scientific confidence percentages**.

For a small library, exact pgvector search is adequate. No additional vector DB or RAG framework is needed for the MVP. The **exact embedding model, dimensions, semantic threshold, hybrid ranking, and evaluation results remain OPEN**; these are configuration/release gates, not an invitation to invent values.

### 11.4 Evaluation before model selection

Create representative questions from the approved small scientific scope; for each, have the reviewer label the expected supporting source chunks and hard negatives. Measure relevant retrieval at top-k, source correctness, coverage/abstention and wrong-method/region rejection. Benchmark the selected embedding candidate against teammate's BM25-style baseline. Pin generation and embedding model identifiers separately; changing embedding families requires complete re-embedding and index versioning.

---

## 12. Hybrid intelligence engine: exact responsibility split

### 12.1 Generation phases

```text
[1] User reviews saved plot-season input fingerprint
       ↓
[2] FastAPI checks ownership and supported scientific scope
       ↓
[3] Job captures IMMUTABLE normalized input snapshot
       ↓
[4] Worker validates units, provenance, measurement method and data gaps
       ↓
[5] Reviewed-rule registry yields ALLOWED actions + safe calculated quantities
       ↓
[6] Eligible research chunks retrieved with metadata + pgvector
       ↓
[7] Optional weather/pricing snapshots fetched or marked unavailable
       ↓
[8] Gemini asked for CONSTRAINED action selection/explanations only
       ↓
[9] Pydantic schema + semantic checks + source/claim checks
       ↓
[10] Backend assembler builds PlanBlueprintV1, attaches provenance
       ↓
[11] Atomic plan save and job completion
       ↓
[12] Dashboard GET renders persisted resource
```

If stage 2 or 5 reveals that an essential user request lies outside approved coverage, the worker **must not continue to a fabricated full plan**. It may persist an explicit partial/unsupported result if that resource contract is implemented, or fail with actionable `UNSUPPORTED_SCIENTIFIC_SCOPE`/`INSUFFICIENT_DATA`. The precise partial-persistence representation is a **DEFAULT to finalize in tests**, but data honesty is LOCKED.

### 12.2 The LLM does not own calculations

- The rule engine owns eligibility and approved agronomic numbers; the cost module calculates prices using qualified price snapshots.
- Weather provider owns observed/forecast numbers, with timestamps and locality; model may explain weather risks only if supported by rules/source data.
- Gemini may select/explain among **known** eligible action IDs, suggest textual sequencing that passes validation, and phrase limitations. It cannot create arbitrary `crop_id`, `rule_id`, `source_id`, nutrient rate, planting-date assumption or soil reading.
- Do not transmit entire research library or raw account identity to Gemini. Build bounded, minimum-necessary context with source IDs and excerpts. Retrieved text is untrusted content (prompt-injection resistant: no instructions executed from papers).
- Schema-correct output is **not** substantively correct. Post-generation validator rejects unsupported actions, numeric claims, invalid evidence, scope mismatches, and missing warnings.

### 12.3 Suggested model-proposal schema

Illustrative Pydantic shape (implementation must include all required source/claim checks):

```python
from typing import Literal
from pydantic import BaseModel, ConfigDict

class RecommendationProposal(BaseModel):
    model_config = ConfigDict(extra='forbid')
    eligible_action_id: str
    explanation: str
    source_chunk_ids: list[str]
    evidence_status: Literal['supported', 'conditional', 'insufficient_evidence']
    limitations: list[str]

class PlanProposal(BaseModel):
    model_config = ConfigDict(extra='forbid')
    summary: str
    recommendations: list[RecommendationProposal]
    missing_information: list[str]
```

**Do not add a free-form `fertilizer_rate` or `soil_health_score` field to the model proposal.** Approved calculation objects are constructed separately by deterministic code and referenced by action ID.

### 12.4 Saved `PlanBlueprintV1` logical schema

`plan_versions.blueprint JSONB` is validated against an explicit versioned Pydantic model with:

| Section | Stable meaning / required provenance |
|---|---|
| `context` | plot, grower-wide season, input fingerprint, relevant goals/location scope |
| `summary` | short explanatory text, with limitations |
| `soil_assessment` | observations, units, methods, interpretation state, missing fields |
| `recommendations` | action ID, kind, explanation, approved rule version, evidence refs, status |
| `schedule` | tasks/dates only if valid; unknown windows explicitly unknown |
| `input_strategies` | approved quantities and options with method/units; nullable |
| `cost_estimates` | comparable product/quantity/retailer snapshots, currency and freshness |
| `weather_context` | observed vs forecast, location, valid period, retrieved timestamp, risk qualifications |
| `evidence` | actual persisted source/chunk version and reviewed claim IDs |
| `limitations` | missing data, unsupported science, provider outage, assumptions |
| `provenance` | input, rule-set, corpus, model, prompt and schema versions, source snapshot IDs |

A recommendation's numeric value (if any) references a validated calculation record, not a random model-provided string. Save the **exact input snapshot** used, not the user profile's later state. Persist enough evidence or immutable source-version references to explain a historical plan even if corpus changes. Do not silently reinterpret `schema_version=1` using a later schema without an explicit converter.

### 12.5 Suggested output states

| Status | When displayed | Display rule |
|---|---|---|
| `ready` | Approved plan constructed for supported conditions | Show evidence and limitations, not guarantees |
| `partial` | Some optional modules unavailable but core scientific plan remains valid | Identify unavailable pieces |
| `insufficient_data` | Missing required observation or lab method | Specify exact needed field |
| `unsupported` | Crop/region/method outside reviewed coverage | No unauthorized crop-specific prescription |
| `outdated` | Saved input fingerprint differs from current relevant data | Historical plan remains readable; prompt regeneration |
| `sample` | Synthetic fixture explicitly selected by demo operator | Prominent sample label, never mixed with real user state |

`failed` is a **job state**, not automatically a valid saved plan. These logical view states need not all become physical database enums.

---

## 13. PostgreSQL job queue and lifecycle

### 13.1 State machine

```text
queued ──claim──> running ──complete──> succeeded
                      |
                      ├── transient failure ──> retry_wait ──> queued
                      └── permanent/exhausted ─> failed
```

Actual phases are separate: `validating_inputs`, `evaluating_rules`, `retrieving_evidence`, `fetching_external_context`, `generating_explanations`, `validating_output`, `persisting_plan` (names are defaults). Processing phase updates only when actual phase changes; frontend displays phase labels rather than fabricated progress percentages.

### 13.2 Claim, lease and retry

1. Worker runs independently of FastAPI with its own DB engine and one Session per operation.
2. Claim eligible queued/retryable row via `SELECT ... FOR UPDATE SKIP LOCKED` in a **short** transaction.
3. Assign unique lease/fencing token, attempt count, lease expiry and current status; commit **before** calling Gemini or other providers.
4. Run pipeline outside long-lived DB transaction; heartbeat/extend lease safely during long execution.
5. When result ready, begin one final short transaction: verify current lease, allocate version, insert immutable plan and evidence, mark job `succeeded`. `UNIQUE(generation_job_id)` prevents duplicate persisted plan.
6. On process death, expired lease is reclaimable; stale prior attempt cannot finalize after replacement. On transient quota/timeouts, bounded backoff; on unsupported science/validation failures, **do not blindly retry**.
7. Do not store raw private context in public worker logs. The job's internal error may hold operational code/details; frontend receives safe stable codes.

**Initial configurable defaults:** one worker process, one generation at a time, up to three attempts, client polling approximately every 2–3 seconds while active. Hard wall-clock deadline, retry delays, heartbeat/lease windows and queue quotas are **OPEN until hosting/load tests**. No Redis/Celery service in first MVP unless separately approved.

### 13.3 Input fingerprint and staleness

Input hash includes the canonical, normalized scientific inputs and references that materially affect recommendation validity: plot size/location scope, plot-season goals, crop selections/history, soil measurements/methods, approved rule-set snapshot and relevant user assumptions. Do not hash arbitrary mutable display metadata. On generation start, compare `expected_input_hash` with backend-computed hash; on mismatch return `409`. A plan generated from a historical snapshot stays saved; after edits, its staleness can be determined without rewriting the plan.

### 13.4 Failure contract

- Optional price API failure: omit live price and shopping claims; retain scientifically valid plan.
- Optional weather API failure: show unavailable/stale context; do not fabricate average temperature/humidity.
- Research/gating failure for essential action: abstain or return a safe error; do not manufacture citations.
- Invalid Gemini schema: reject, bounded retry if applicable, otherwise job fails safely.
- Crashed worker, lost lease, duplicate claim: recover without duplicate plans.
- User refreshes progress page: job state recovers from DB; no repeated POST.
- User logs out while job runs: job may finish against captured snapshot under operator policy, but protected results remain inaccessible without valid session.

---

## 14. Contextual AI chat and what-if tools

### 14.1 Binding and permissions

Each saved conversation belongs to user + `plot_season_id` + immutable `plan_version_id`. Start a **new** conversation for a new plan version rather than silently updating historical context. The backend loads stored plan/input/evidence; browser cannot submit arbitrary `grower` JSON as authoritative context. Limit token/context budget, chat quotas and saved message retention under the temporary-demo policy.

### 14.2 Tool interface (adapt teammate's vocabulary)

| Tool | Reads/does | Restriction |
|---|---|---|
| `get_plan` | Load authorized persisted blueprint/version | No recompute in chat; no cross-user access |
| `explain_rule` | Return reviewed rule/version and exact source evidence | No unreviewed source promoted to evidence |
| `lookup_data` | Bounded eligible catalog lookups | All returned metadata labeled with review status |
| `search_notes` | Scoped approved research retrieval | Metadata-filter first; page/section citations |
| `run_what_if` | Deep-copy approved snapshot, apply validated temporary modifications, compute comparable eligible result | **Never persists** changes or bypasses rules; approval required for changed user plan |

Gemini's tool calling can select these actions but cannot invoke arbitrary Python, SQL or HTTP URLs. Dispatcher uses explicit name allowlist, Pydantic input validation, per-turn/tool-call limits and execution timeouts. Tool result IDs and exact sources are available to the response validator.

### 14.3 Chat response contract

```json
{
  "message_id": "message-uuid",
  "reply": "Explanation based on the selected saved plan.",
  "citations": [],
  "tools_used": ["get_plan", "explain_rule"],
  "limitations": [],
  "context": {"plan_version_id": "plan-uuid"}
}
```

Illustrative only. We may persist internal tool trace separately but **must not** expose secrets or unreviewed raw prompt context to browser. A legacy regex that detects some unsupported numbers is diagnostic only; real enforcement checks typed calculation references and evidence. On no reviewed supporting passage, assistant admits missing support rather than supplying crop-specific facts from memory. Render as safe text/Markdown, never injected HTML.

---

## 15. Weather, pricing, products and shopping suggestions

### 15.1 Adapter boundaries

`integrations/weather/` converts a selected provider's readings/forecasts into a typed canonical `WeatherObservation/Forecast` with location granularity, timezone, valid time, retrieval time, units and source. `modules/weather` controls caching, persisted snapshots, freshness and user/plot access.

`integrations/pricing/` reads legal APIs/feeds/allowed data sources and normalizes product title/brand, composition, bag/package quantity, total price, unit price, currency, store/vendor, availability, link, observed time and shipping/tax inclusion. `modules/costs` composes viable offers and cost comparisons; user-specific cost plans remain source-linked.

**Provider identities, geographic coverage, rate limits and thresholds are OPEN.** Do not claim real-time coverage or invent external APIs. Prefer official APIs and retailer-provided feeds; do not scrape against terms, anti-bot controls or unclear usage rights. No autonomous checkout or payment behavior in MVP.

### 15.2 Financial correctness

A valid cost estimate is an arithmetic result from **approved quantity** × **qualified product unit price**, with package rounding and optional tax/shipping clearly indicated. Keep the cost calculation separate from whether the scientific quantity is justified. Missing prices are unknown, not $0. Show `estimated`, `last checked`, and retailer/source appropriately.

Comparative *estimated difference* is allowed only with an explicit comparable baseline. Never render `money saved` as an achieved outcome without actual historical purchase evidence. Dated national farm price-survey examples from the teammate prototype are not equivalent to local store offers.

### 15.3 Weather correctness

Current forecast, historical climatology and measured observation are different data types. A weather risk may inform timing only if the scientific rule allows it for selected crop/region and valid forecast horizon. Avoid invented **average humidity, average temperature, soil moisture, rain risk, hardiness-zone certainty or planting suitability scores**. The UI must reflect provider outage, stale forecast and overly coarse location independently.

### 15.4 Staleness and resilience

Each external card has `source`, `status`, `valid_at/observed_at`, `retrieved_at` and freshness interpretation. Actual cache TTL and maximum tolerated age are OPEN provider-specific configuration decisions. API failure must not overwrite a prior source snapshot with fake empty data; respond with `unavailable` or `stale` as appropriate. Prevent expensive upstream refresh on every dashboard render by caching/scheduling server-side.

---

## 16. Deployment, environments and operations

### 16.1 Required topology; provider OPEN

```text
Public HTTPS domain
  └── Next.js service
        └── /api/v1/* -> internal FastAPI service
                               ├── PostgreSQL (+ pgvector)
                               ├── external provider adapters
                               └── queued planning jobs
Long-running Python worker ───────────┘
```

Choose actual host(s) only after confirming: Next.js runtime support, FastAPI persistent service, separate worker process support, PostgreSQL with compatible pgvector extension, private networks/SSL, migrations, backups and free/paid quota constraints. A serverless function that may terminate during generation is not equivalent to the approved independent worker.

### 16.2 Environment contracts

- **local:** Docker Compose or equivalent Postgres + pgvector; Next/FastAPI/worker via dev processes. Dummy/fixture provider integrations permitted only when visibly labeled.
- **test/CI:** disposable real Postgres; safe fake Gemini/weather/pricing adapters; migration and security tests.
- **demo/staging:** real HTTPS/cookies; provider limits and secrets; cleanup policy published; limited observed crop/region coverage.
- **production later:** not automatically implied by hackathon release; separate account recovery, monitoring, privacy/security and quality gates.

Recommended environment variables (names **DEFAULT**, values never committed):

```text
APP_ENV=
PUBLIC_APP_ORIGIN=
DATABASE_URL=
SESSION_COOKIE_NAME=
SESSION_IDLE_HOURS=12
SESSION_ABSOLUTE_DAYS=7
CSRF_SECRET=                        # only if chosen CSRF scheme requires it
INTERNAL_API_BASE_URL=
GEMINI_API_KEY=
GEMINI_GENERATION_MODEL=           # OPEN exact model ID
GEMINI_EMBEDDING_MODEL=            # OPEN exact model ID
EMBEDDING_DIMENSIONS=              # OPEN
WEATHER_PROVIDER=                  # OPEN
PRICING_PROVIDER=                  # OPEN
PLAN_WORKER_CONCURRENCY=1
PLAN_MAX_ATTEMPTS=3
MAX_AI_REQUESTS_PER_ACCOUNT=       # OPEN
DEMO_RETENTION_DAYS=               # OPEN
```

Never expose backend-only secrets with `NEXT_PUBLIC_` prefixes. Use a secret manager/environment storage appropriate to the selected platform. `.env.example` has placeholders only; `.env.local` and real credentials are ignored by Git.

### 16.3 Release/boot order

1. Build immutable artifact from reviewed commit; run lint/tests.
2. Provision PostgreSQL + pgvector and verify extension privileges/version compatibility.
3. Back up existing state where relevant; apply reviewed Alembic migrations once.
4. Run idempotent curated source ingestion; verify approval records and embedded corpus readiness.
5. Start FastAPI + worker + Next.js; perform `/health` and dependency readiness probes.
6. Run functional smoke test with **synthetic** demo user and reviewed rule scope.
7. Enable real public signup only after secure cookies, CSRF, retention disclosure, account/AI abuse limits and cleanup job are validated.
8. On rollback, do not corrupt plan/version schema; document schema and artifact rollback compatibility.

### 16.4 Observability and incident policy

Structured logs: request ID, route, user pseudonymous ID where permitted, job ID, phase durations, provider status/latency and model ID; avoid raw passwords/cookies/document contents. Monitor backlog, lease expiry, 401/403/429 rates, provider quota failures, ingestion counts/review changes, citation validator failures and dashboard stale-data rates. Support manual worker restart/queue reaping without data loss. Retain only necessary logs for the defined temporary demo window (OPEN).

---

## 17. Security and failure matrix

| Boundary | Threat/failure | Required mitigation/test |
|---|---|---|
| Auth | credential stuffing, enumeration | generic errors, rate limits, Argon2id, audit logging without secrets |
| Session | stolen/replayed/stale token | opaque entropy, hashed verifier, secure cookie, expiry/revocation |
| CSRF | cross-site mutation | session/pre-auth CSRF, Origin and Fetch Metadata checks |
| Broken access control | other user's plot/plan/chat | backend owner filters, same-owner join, `404` masking as appropriate |
| Draft racing | stale browser tab overwrites newer draft | optimistic `expected_revision` + `409` |
| Input poisoning | forged lab measurements / wrong method | source provenance, unit/method validation, no false 'lab' state |
| Prompt injection | untrusted research says override rules | treat passages as data, constrained action IDs, validation |
| Citation hallucination | nonexistent/mismatched citation | only retrieved approved ID/version; claim-to-passage validator |
| Unsupported fertilizer | unreviewed formula executes | approval gate fails closed, no model fallback |
| HTML/script injection | generative output rendered as HTML | escape/sanitize safe Markdown; no raw HTML sinks |
| Worker concurrency | double claim, stale lease, duplicate version | DB short lock, fencing, uniqueness, idempotency |
| Provider outage | empty/false weather, cost, plan | clear degraded states, bounded retries, no fabricated value |
| PII leakage | logs/prompts/cache crossing users | minimize external context; per-user server caching off; log redaction |
| Research integrity | source text revised after plan | immutable source versions, hashes, plan evidence refs |
| Public demo resource abuse | account spam / free Gemini quota drain | throttles, queue caps, operator control, cleanup |

No unverified developer shortcut may weaken these invariants in the hosted demo. Tests need to exercise the actual same-origin proxy and cookie behavior, not just isolated Flask/FastAPI routes.

---

## 18. Testing strategy and non-negotiable acceptance gates

### 18.1 Test organization

- `backend/tests/unit/`: pure agricultural calculations, unit conversions, fingerprint determinism, rule eligibility, validation, price arithmetic, JSON schema versioning.
- `backend/tests/integration/`: real PostgreSQL CRUD/transaction, Alembic migration, pgvector retrieval, job `SKIP LOCKED` and unique/fencing behavior, research ingestion idempotency, cleanup behavior.
- `backend/tests/contracts/`: request/response Pydantic, OpenAPI examples, error codes, dashboard and plan schema.
- `backend/tests/security/`: owner isolation, cookie/CSRF/session, file/HTML prompt injection, rate limits, data redaction.
- `frontend/tests/`: component states, routing/auth redirects, RHF form draft resume/conflicts, navigation accessibility, mobile drawer, client cache invalidation, live job polling.
- End-to-end: use disposable environment and synthetic accounts, mocked cost/AI provider paths plus at least one controlled live-model smoke test when quota/consent available.

### 18.2 Acceptance criteria (must pass before public demo)

| Scenario | Pass condition |
|---|---|
| Fresh install | PostgreSQL extension, Alembic, vetted corpus ingestion, API and worker start from documented commands |
| Public sign-up + login/logout | correct secure cookie, session, CSRF, server revocation and navigation |
| Session timeouts | 12h idle/7d absolute enforced, automatic polling does not keep sessions alive |
| User A accesses User B plot/job/plan/chat | rejected; nothing private disclosed |
| Onboarding interruption | draft resumes with correct revision; incomplete soil remains null |
| Multi-plot same season | same-owner plot-season associations; invalid cross-owner join rejected |
| Input changes while processing | worker uses original snapshot; saved result marked outdated when appropriate |
| Duplicate POST/idempotency | exactly one job for identical key/payload; conflicting reuse returns `409` |
| Worker crash/double completion | lease recovery succeeds; at most one plan per job |
| Unsupported crop/region/method | no crop-specific unauthorized plan; actionable scope/requirements message |
| Unreviewed `LIME-*` row | cannot issue a real user prescription |
| Lab lime conversion with approved rules | correct units/area and verified report reference; bad method rejected |
| Selected fertilizer rule | only exact approved crop/method/source path computes a quantity |
| LLM invented action/citation/number | validator rejects or safely strips unsupported claim; never shown as authority |
| Gemini outage/rate limit | bounded retry/failure state; original plans survive |
| Pricing/weather failure | dashboard marks unavailable/stale; core eligible plan unaffected |
| Chat tool `run_what_if` | no persisted mutation; results tied to actual authorized plan |
| XSS attempt in source or Gemini text | rendered as escaped text; no script execution |
| Query/logout privacy | authenticated query caches cleared; no shared server private cache |
| Source revision after saved plan | historical version retains original evidence/provenance |
| Demo cleanup | owner data erased according to configured and disclosed lifecycle |

**Agronomy caution:** passing existing teammate tests proves program consistency with expected fixtures, not correctness of agronomic recommendations. A separate, documented human review is mandatory to activate live rules.

### 18.3 Design/UX quality gate

Meet `DESIGN.md` at **320×700, 390×844, 768×1024, 1440×900 and 1920×1080**. No clipped fields or horizontal overflow; keyboard controls and focus; actual source/status text; no fake soil-health score; reduced-motion for loading; contextual chat visually tied to selected plot/version; plan summary prioritizes what the grower should do.

---

## 19. Incremental engineering execution plan

Implement as vertical slices, not by creating every folder/table before a user can complete anything. Every slice needs tests and demonstrable behavior.

### Phase 0 — Contracts and source audit (already prepared conceptually)

- Freeze `PRODUCT.md`, `DESIGN.md`, this `ARCHITECTURE.md` as baseline; retain read-only teammate audit.
- Populate scientific source inventory from actual PDFs/datasets/links; review licensing and row-level notes.
- Select first eligible crop/region/method and reviewer **before** enabling scientific recommendations.
- Choose Gemini generation and embedding model IDs/dimensions; benchmark retrieval; check quotas.
- Record host/retention/provider gates in decision log.

### Phase 1 — Foundation and authentication

- Monorepo skeleton, FastAPI app factory/API router, sync SQLAlchemy session, Alembic identity/growing migrations.
- Next App Router shells/tokens/nav; same-origin proxy with production-like cookies.
- Signup/login/logout/me/CSRF and true owner isolation; ephemeral demo account policy.
- CI lint/tests, disposable PostgreSQL test DB, env examples and startup scripts.

**Gate:** two user accounts cannot read/edit one another's records; session expires/revokes; frontend integrates auth correctly.

### Phase 2 — Onboarding, plots, seasons and persistent input

- RHF/Zod step wizard and backend Pydantic draft schema; save/revision/resume.
- Plot CRUD, grower-wide seasons, plot-season joins, dated soil observations; canonical units and provenance.
- Review screen with input fingerprint; incomplete/unknown soil remains null, never sample data unless fixture mode.

**Gate:** create, resume, complete, view and edit a plot across refresh and sign-in.

### Phase 3 — Reviewed scientific core and research ingestion

- Port pure deterministic functions from teammate `soil_engine.py` with regression fixtures, but gate all real-output rules.
- Implement source/version/chunk import and per-rule approval manifest; quarantine unreviewed/placeholder rates.
- Review selected rotation + soil interpretation + lab lime calculation; select only justified fertilizer method.
- Choose embedding model, vector migration and scoped retrieval with BM25 comparison.

**Gate:** approved case yields actual supported actions and traceable citations; unapproved case abstains.

### Phase 4 — Generation worker, saved plan and dashboard

- Capture snapshot/idempotency; PostgreSQL job claim, worker, retries and fencing.
- Gemini adapter and constrained `PlanProposal`; substantive validator; assemble `PlanBlueprintV1`.
- Persist plan/evidence and expose dashboard; real job phases/growing animation and reload survival.

**Gate:** successful end-to-end saved plan and tested crash/duplicate cases; no raw hallucinated data reaches dashboard.

### Phase 5 — Contextual chat and what-if

- Persistent chat bound to immutable version; port `get_plan`, `explain_rule`, `search_notes`, `lookup_data`, `run_what_if` safely.
- Provenance-rich answers with source links and allowed-action references; refusal/abstention on unsupported numbers.
- Drawer UI, semantic statuses and safe rendering.

**Gate:** chat explains actual saved plan; refresh retains messages; cross-user access blocked; what-if doesn't mutate.

### Phase 6 — External data and hardening

- Add selected weather and price adapters; typed source snapshots/freshness and honest degradation.
- Configure public hosting, TLS/proxy/worker/db, secrets, backups, quotas and cleanup.
- Run tests, cross-browser/device audit, demo walkthrough and release readiness checks.

**Gate:** real provider data is correctly labeled; outages are safe; public-demo account/data requirements fulfilled.

---

## 20. Explicit OPEN decisions, owners and blocking consequences

**Coding agents must not decide these by silent assumption.** Identify the smallest blocking milestone, leave integration disabled/typed and request human input.

| Open item | Responsible decision owner | Blocks |
|---|---|---|
| Exact supported crops, climate/region(s), soil-test methods | Team + scientific reviewer | real crop-specific plan claims |
| Named rule/paper reviewer, claim/source approvals | Team + reviewer | enabling live agronomic rates/interpretations |
| Gemini generation model ID, API quota and budget | Team/engineering | live generation and chat settings |
| Gemini or other embedding model, vector dimension, semantic benchmark | Engineering | pgvector DDL/index and production retrieval |
| Weather provider, geocoding/location granularity, freshness threshold | Team/engineering | live weather cards and weather-aware plan rules |
| Retailer product source(s), allowed data access, freshness/currency/package rules | Team/engineering | real current product offers and cost comparison |
| Hosting provider and service topology, TLS/private networking | Team/engineering | public deployed demo |
| Job deadlines, lease/heartbeat/retry intervals, queue limits | Engineering after host load test | dependable worker operations |
| Exact temporary account/data cleanup period and log retention | Team/product | public sign-up release |
| Email recovery/verification for sustained public launch | Product/security | non-temporary operation |
| Pricing, trial, payments, subscription entitlements | Product/business | true commercial pricing/trial promises |
| Weather/retailer offline fallback artifacts | Product/engineering | demo behavior under outage |
| AI-assisted PDF/soil report intake | Product/engineering | optional feature only; not core blocker |
| User-visible scope-limitation UX wording | Product/design | reviewed science release clarity |

### Release gating rules

- **Public demo may not display live fertilizer/lime prescriptions until specific rule versions are reviewed, activated and tested.**
- **Public demo may not claim true live retailer/weather integration until provider and freshness requirements are met.**
- **Public signup may not open without a real temporary data lifecycle policy, cleanup capability and documented recovery limitation.**
- **Final deployment cannot be certified without checking its ability to run the independent worker and pgvector, secure cookies and same-origin route.**

A deliberately limited demo with reviewed rotation, explanatory soil readings and a **clearly labeled** synthetic sample is acceptable while science review is incomplete. It is not acceptable to present test fixtures as live user recommendations.

---

## 21. Agent rules: what Codex may and may not infer

### 21.1 Allowed engineering discretion

Choose internal function/helper names, validation library micro-usage consistent with locked stack, test fixture setup, paginated list defaults, reversible component composition and other local implementation details where they do not change public API semantics, scientific results, authorization or UX design authority. Record nontrivial assumptions in implementation notes.

### 21.2 Requires team approval

Any new technology/service/ORM/state manager; migration of frontend to TypeScript; replacing FastAPI or Gemini; changing URL/HTTP contracts or ownership model; changing session/CSRF mechanism; new scientific numeric rule; changing required inputs to silently supplied defaults; publishing new crop/region coverage; adding payment checkout, provider scraping or data retention changes; AI intake upload with unreviewed file handling; plan edits not represented as versioned records.

### 21.3 Forbidden implementation shortcuts

- No mock API response, fake loading percentage, invented weather/price/soil/yield/savings presented as live output.
- No blanket `verified=true` for all imported research, no embedding or citation generation that invents sources.
- No fallback to Gemini's memory for missing agronomic rates or unsupported crop-specific recommendations.
- No raw session token in DB, localStorage, logs or telemetry.
- No trusting client-provided user ID/plot ownership or client-supplied AI context in chat.
- No uncontrolled web scraping, silent checkout or external network access from browser with server secrets.
- No unsanitized model HTML in the frontend.
- No DB transaction held during Gemini/weather/retailer requests.
- No production migration at every API process startup; no destructive seed/reset without explicit operator intent.
- No silent upgrade of source versions or rule approvals referenced by saved plans.

### 21.4 Definition of done per feature

A feature is done only when: (1) its authorized API exists and returns the documented contract, (2) it persists or retrieves real state as appropriate, (3) error/empty/loading/unsupported/stale states behave honestly, (4) ownership and security tests pass, (5) relevant source/units provenance is represented, (6) mobile/accessibility review passes, and (7) README/architecture decisions and any implementation deviation are documented. A visually complete static page is **not** functional completion.

---

## 22. Decision change process and project handoff

1. Submit a proposed change with affected ADR ID, product behavior, implementation modules, migration/API effects, alternatives and testing impact.
2. Check `PRODUCT.md` and `DESIGN.md` for related intentions. Conflicts require human approval before code changes.
3. Record acceptance in `docs/adr/` or the decision log; update this file and `TESTING.md`.
4. Version Pydantic response contracts, DB migrations and reviewed rule/content versions when changing behavior.
5. Run regression tests for changed science/ownership/worker flows, then update release gates.

**Source provenance for engineers:** See `PLANTLY_TEAMMATE_RAG_AUDIT(1).md` for original code paths and scientific caveats; `PLANTLY_KNOWLEDGE_INVENTORY_TEMPLATE(1).csv` for required source inventory columns. These source documents may live under `docs/reference/` in the actual repository; this architecture does not assume they have already been copied there.

### Final implementation-readiness checklist

- [x] Core stack and monorepo architecture chosen.
- [x] Frontend route, feature and state-ownership contracts defined.
- [x] Backend module and DB model ownership defined.
- [x] REST/API, session/CSRF and worker boundaries defined.
- [x] Research ingestion, retrieval and versioning boundaries defined.
- [x] Teammate prototype inspected and mapped to reuse/adapt/reject decisions.
- [x] Narrow mixed qualitative/quantitative scientific MVP approved conceptually.
- [ ] Actual source and rule review completed; supported crop/region/method matrix published.
- [ ] Gemini generation/embedding models evaluated and pinned; pgvector migration completed.
- [ ] Weather and retailer providers/freshness/terms selected.
- [ ] Hosting selected and worker/database/proxy support verified.
- [ ] Temporary-demo retention period, disclosure and erasure implementation approved.
- [ ] Real integrated tests executed, including reviewed agronomic cases.
- [ ] Hosted demo deployed and operational checks passed.

---

## Appendix A — Evidence/reference file mapping

| Artifact | Role in this architecture | Important limitation |
|---|---|---|
| `PRODUCT(1).md` | User journey, value, dashboard, honest status language | contains proposals/open business terms |
| `PLANTLY_MASTER_DESIGN_SYSTEM(1).md` | Global visual language, tokens, accessible UX | some design extensions and font candidates remain proposed |
| `PLANTLY_ARCHITECTURE_WORKING_DRAFT(1).md` | Prior locked decision consolidation | superseded by this document and later scientific decisions |
| `PLANTLY_TEAMMATE_RAG_AUDIT(1).md` | Pinned read-only teammate code inspection | no runtime test or independent source verification |
| `PLANTLY_RAG_AUDIT_PROMPT(1).md` | Audit method/checklist | instructions, not evidence of runtime behavior |
| `PLANTLY_KNOWLEDGE_INVENTORY_TEMPLATE(1).csv` | Empty source inventory schema | no scientific review records populated |
| `Ankit0200/Plantly` pinned commit | Observed prototype implementation | code is not equivalent to approved agronomy |

## Appendix B — Glossary

- **Plot:** a discrete growing area owned by a user.
- **Season:** a grower-wide calendar/planning period, potentially containing multiple plots.
- **Plot-season:** the association and season-specific plan context for one plot.
- **Onboarding draft:** partially saved profile inputs; not an approved scientific plan.
- **Scientific rule version:** auditable rule implementation with reviewed applicability/evidence and execution status.
- **Source version:** immutable reviewed edition or excerpt of a paper/dataset, tied to content hash.
- **Chunk:** a bounded citation-preserving passage for retrieval.
- **RAG:** retrieval-augmented generation; retrieving applicable evidence to ground a model response, with pgvector as one retrieval mechanism.
- **Plan job:** the queued/running/finalized operation that attempts plan generation.
- **Plan version:** immutable validated output and provenance from one successful job.
- **Input fingerprint:** hash of canonical material generation inputs for optimistic concurrency/staleness detection.
- **Abstention:** explicit refusal to issue unsupported scientific recommendation, not a silent fallback.
- **Observed vs forecast vs sample:** independently labeled data provenance classes; never interchangeable.

## Appendix C — Changelog

- **2026-11-07, v1.0:** Consolidated Rounds 1–8 and ARC-047/ARC-048; superseded prior pre-audit working draft; integrated teammate code audit and reviewed-rule gate; specified frontend/back-end contracts, normalized schema, migration phases, RAG, worker, auth, deployment criteria, source inventory, scientific review and release blockers.
