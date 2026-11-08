# Curated data: audit before schema or import

Canonical input location: `data/curated/`. User-supplied YAML datasets and JSON fixtures are now present. See [D-010 audit](agent/DATASET_AUDIT.md) and its [file/schema inventory](curated_inventory.json); presence does not establish scientific approval.

- `datasets/`: `credits.yaml`, `crops.yaml`, `lime_table.yaml`, `nutrient_recs.yaml`, `practices.yaml`, `problems.yaml`, `products.yaml`, `rotation_rules.yaml`, `soil_test_levels.yaml`.
- `rule_reviews/sources.yaml`: actual source catalog location; retain its schema/IDs. This file is not a rule-approval manifest.
- `research/source_notes.yaml`: supplied notes with source references and page/section locators; publication accuracy and reuse permissions remain unverified.
- `fixtures/`: `beginner_grower.json`, `demo_grower.json`, `diverse_farm.json`, `high_input_grower.json` — synthetic examples only, never production grower records.
- `rule_reviews/`: future approval records must contain only real documented human approvals; the existing source catalog grants none.

**D-010 dataset audit:** examine actual schemas, source IDs, references, method/region/crop restrictions, licensing, units, placeholder flags and import order; do not rewrite original source files just to make an import pass.

**F-040 ingestion:** Alembic handles schema migrations. A separate, validated, idempotent script imports versioned source/catalog data and preserves provenance. Test repeated runs, failures, rollback and bad references on disposable PostgreSQL. Research in a database is not automatically eligible for scientific use. Existing legacy `verified` fields are not a substitute for source-version/rule review.

Do not enable placeholder lime quantities, unreviewed nutrient numbers, or unsupported agronomy. Do not select embedding provider, dimension or vector column size without a documented decision. No production ingestion occurs solely because this instruction exists.

### Incremental Research Ingestion Requirement

Plantly must support incremental ingestion of additional YAML datasets and research papers after initial database setup.

Requirements:

- Provide a repeatable manual ingestion command.
- Detect newly added, modified and unchanged source files.
- Use stable IDs, version numbers and content hashes.
- Prevent duplicate ingestion.
- Preserve existing source versions, evidence and immutable user plans.
- Validate source references, units, schemas and provenance.
- Ingest structured YAML into appropriate PostgreSQL tables.
- Extract, chunk and embed eligible research documents for pgvector retrieval.
- Keep unreviewed scientific rules inactive.
- Do not automatically regenerate existing users' plans.
- Record import success, failure and validation details.
- Test repeated imports and recovery from partial failures.
- Do not require a new Alembic migration unless database schema changes.
- Do not assume local files added after deployment are available inside a running container; support a persistent or deployable ingestion source.

Do not enable automatic folder watching or continuous re-indexing in the initial MVP.

## Implemented local source/notes slice (2026-11-08)

Run from backend: `.venv/Scripts/python.exe -m app.ingest --root ../data/curated`.

Current scope is the source catalog and research/*.yaml notes only. It validates the entire batch before writes, uses an advisory transaction lock for version allocation, preserves immutable source/note versions and file hashes, and leaves every version unreviewed. The development import created 40 source versions and 122 notes; repeating it created zero versions. Tests cover changed content, invalid references, rollback/recovery and the inactive review constraint.

This does not fulfill numeric-dataset ingestion, PDF extraction or embedding requirements above. Product row provenance, placeholder rules, publication/license review, scientific scope, and embedding provider/dimensions remain unresolved. No synthetic growers are imported and no existing plans are regenerated.
