# Decisions and approvals

- 2026-11-08 starter-kit packaging: keep the eight supplied files unchanged; normalize architecture/design/product filenames to canonical names referenced by `AGENTS.md`. This is a file-path normalization, not a product decision.
- 2026-11-08 development preference: implement the **smallest real vertical slice first**, defer premium landing imagery and optional components until the foundation is testable. This does not override LOCKED architecture, security or science gates.
- OPEN: supported crop/region/soil method; named scientific reviewer and approval record; generation and embedding model ID/dimension; AI quota/budget; weather/retailer providers; hosting/retention; real commercial terms. Codex must not choose these silently.

Record future material decisions and their owner/date before building dependent functionality.

## Implementation decisions — 2026-11-08

- User explicitly requested local, barebones development and no animations/advanced visuals. Kept documented Plantly colors/geometry and system font fallback; deferred the full landing composition and custom artwork integration. Preserved installed skills/assets.
- All original curated bytes remain unchanged. Inventory comparisons distinguish CRLF-only changes. Internal reference screenshots moved outside public; no fabricated imagery or metrics.
- Local app uses a development cookie name; non-local configuration requires HTTPS and secure __Host- cookies. Sessions last at most seven days and expire after 12 idle hours; GET polling does not renew them.
- Basic intake stores typed optional user facts in the draft and a plot-season JSONB snapshot, with null unknowns and explicit user-reported pH provenance. These are not normalized laboratory records or approved scientific inputs. Method-specific measurements and rule consumption remain future gated work.
- Partial drafts can save without all completion fields. Completion requires plot name, positive area, region and either a new season label/year or an owned existing season. Existing seasons can be shared across plots; compound foreign keys enforce same ownership.
- Source/notes ingestion is a separate manual command, atomic and idempotent. Import legacy verified fields as metadata only; all source versions remain unreviewed and immutable. No vectors/model dimensions chosen. Numeric datasets and fixtures are excluded until suitable provenance/validation is available.
- Gemini adapter is server-only. AI_ENABLED defaults false; no application route invokes the provider. Adding credentials alone does not activate planning or clear review/cost gates.
- Password-reset/email-verification and timed retention remain explicitly unavailable/open. Local self-account deletion API cascades personal records; shared research history is preserved.
- User explicitly authorized installing DietrichGebert/ponytail; CLI verified ponytail@ponytail 5.3.3 installed and enabled. This did not authorize deployment, provider charges, new model selections or scientific approval.
