# Starter testing and evidence (new helper document)

Use `docs/DEVELOPMENT.md` as the primary command guide **after Codex creates actual manifests and code**. For M-001 require at least:

- A genuinely accessible frontend landing at `http://localhost:3000`.
- Backend `GET /health` liveness independent of DB readiness.
- Same-origin Next route `/api/v1/health` reaches FastAPI, with honest backend-unavailable handling.
- `npm run lint`, `npm run build` and one backend test/smoke test, if installed; otherwise report exactly which could not run.
- PostgreSQL connection/migration checks when Docker works; test DB must remain disposable.

Later verify security, session expiry, cross-user access, migrations, input revisions and scientific abstention before claiming feature completeness. Missing checks are not passes.
