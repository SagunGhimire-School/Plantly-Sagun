# Issues and blockers — 2026-11-08

## Open

- **G-010:** No named independent reviewer or exact source/rule/crop/region/method approvals. All imported content remains unreviewed. No agronomic rules execute.
- **D-010 / full F-040:** External publication accuracy, URL accessibility and licenses are unverified. Numeric datasets contain placeholders or inadequate row-level provenance. Original PDFs and approved embedding configuration are absent. Source/notes import is implemented separately.
- **M-005/M-006:** Gemini key and generation model, embedding model/dimensions, quota/budget and reviewed science are missing. No generation jobs, immutable plan output, or plan-bound chat have been activated or represented as complete.
- **M-007/G-020:** Weather/retailer providers, real commercial terms, hosting/TLS, retention/cleanup and account recovery/release approvals remain open. Account deletion cascades locally, but no approved timed cleanup policy exists. The in-process login limiter requires shared ingress limits before public release.
- **Artwork:** Original premium emblem and two historical references remain absent. Supplied images/SVG are inventoried in ASSETS.md. Barebones UI is intentionally text-led.
- **Version control:** git status reports “not a git repository”; no commits or Git diff evidence are claimed.
- **Dev dependency audit:** Initial npm audit reported eight moderate findings in the eslint-config-next → typescript-eslint → minimatch chain (GHSA-g3hv-75wg-m249). npm suggested a major config downgrade. No forced downgrade/override was applied. npm audit --omit=dev currently reports zero vulnerabilities.
- **Nonblocking runtime warnings:** Starlette warns that its httpx TestClient integration is deprecated in favor of httpx2; tests pass. Next warns about an unrelated home-directory package-lock.json, then ignores it; the production build succeeds.

## Resolved during implementation

- Python Store alias was inaccessible and py reported no registered interpreter. Explicit Python312 executable worked; virtual environment installed. Docker Desktop and its helper were absent from PATH; process-local PATH adjustment resolved startup. Paths are in DEVELOPMENT.md.
- npm registry access failed with EACCES under the initial sandbox. Authorized dependency installation succeeded with reviewed network access.
- Docker initial pull failed because docker-credential-desktop was absent from PATH. Adding Docker Desktop/resources/bin resolved it; both Compose PostgreSQL services are healthy.
- Preflight initially showed 0/15 raw checksum matches. LF normalization matches all 15; originals are unchanged. Preflight now distinguishes line endings from modified content.
- Images were all under public/brand/images. Tractor/logo moved to canonical public locations; four internal reference screenshots moved to docs/references.
- Initial Playwright run completed five checks but hung while tearing down its npm-owned Windows dev-server tree. Only identified Plantly processes were stopped. Reusing an explicitly started frontend produced an exiting, passing suite; config now launches Next directly if needed.
- Initial Ruff import and Depends-default warnings were fixed through formatting/import cleanup and explicit recognition of FastAPI Depends. Current Ruff passes.
- Error-state test initially matched both the form alert and Next's route announcer. Scoped the assertion by the actual alert text; both fault-handling tests pass. This was a test selector collision, not a suppressed application failure.
- Form-level soil/date validation errors were not described specifically. Unmapped backend field errors now render in the alert while preserving entries; browser verification covers this and stale drafts.
- Importer now rejects a missing research directory rather than treating an incomplete source tree as an intentional notes deletion; covered by a regression check.

No public deployment, production-data destruction or paid API requests occurred.
