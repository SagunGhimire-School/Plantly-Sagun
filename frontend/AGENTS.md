# Frontend scoped instructions (starter helper)

Follow root `AGENTS.md`, `docs/ARCHITECTURE.md` and `docs/DESIGN.md`. Next.js App Router with **JavaScript/JSX**, not a TypeScript conversion. Tailwind CSS v4 and shared Plantly tokens. Use server-rendered shell and local client interactive components only where needed. Route logic stays separate from features. Browser API requests must be same-origin `/api/v1/*`; never ship credentials, database URLs or provider tokens to the browser. Keep pages truly responsive and keyboard accessible. Do not invent artwork, current data, scientifically backed results or working auth when absent. First create only the files required for the minimal M-001 landing/proxy/health flow; no empty feature directories for show.

<!-- BEGIN:nextjs-agent-rules -->

## This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify at `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->
