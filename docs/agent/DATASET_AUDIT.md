# D-010 supplied-file audit — 2026-11-08

All **15** inventory-listed files are present under data/curated. None are missing or misplaced. The starter's absence report is historical.

Raw SHA-256 hashes differ for all files because of CRLF line endings. LF-normalized bytes match **15/15** expected hashes. Originals were not rewritten. [Machine-readable report](dataset-presence-audit.json) records actual hashes, fields, counts and IDs; scripts/audit_data.py reproduces it.

| File/group | Records | Findings |
|---|---:|---|
| datasets/credits.yaml | 2 | Compost/legume credits; pounds and cubic-yard/area bases; unreviewed. |
| datasets/crops.yaml | 21 | Crop families/demand and numeric targets; no approved crop/region coverage. |
| datasets/lime_table.yaml | 15 | Explicit placeholders referencing SRC-PLACEHOLDER. Not a permissible fallback. |
| datasets/nutrient_recs.yaml | 8 | Pounds per 1,000 ft²; needs exact method/source/scope review. |
| datasets/practices.yaml | 13 | Source-linked practice text; not automatically eligible. |
| datasets/problems.yaml | 13 | Problem/family/rotation metadata; unreviewed. |
| datasets/products.yaml | 5 | Pounds/bag, nutrient percentages and USD/bag; placeholder/datetied comment-level prices without per-row source/time evidence. Not live prices. |
| datasets/rotation_rules.yaml | 3 | Templates with limited history/applicability requiring independent review. |
| datasets/soil_test_levels.yaml | 2 | P/K thresholds specify Mehlich-1/conversion assumptions; no cross-method equivalence is inferred. |
| research/source_notes.yaml | 122 | Paraphrases with source IDs and page/section locators; accuracy/rights unverified. |
| rule_reviews/sources.yaml | 40 | Source catalog, **not rule approvals**. No license metadata. Placeholder/report entries lack public URLs. |
| fixtures/*.json | 4 files | Synthetic grower examples only, not imported as user records. |

No duplicate IDs were found within the YAML files. Every explicit source reference resolves to the catalog. Catalog/notes also pass import-time Pydantic schema and reference validation. URL syntax is checked; current publication content, accessibility and reuse permissions have **not** been independently verified.

The catalog's legacy verified:true grower-report entry is historical metadata only. Every imported version remains **unreviewed**, regardless of that boolean. No authoritative reviewer/rule/source/scope approvals exist.

## Remaining gates

- Source/notes engineering slice: immutable versions, semantic hashes, original-file provenance, rollback, repeat-import deduplication and changed-note history are implemented and tested.
- Numeric datasets are excluded from ingestion/execution. Product rows lack source/time provenance; lime placeholders are prohibited. Exact method/unit applicability requires review.
- No original research PDFs were supplied. Embedding provider/model/dimensions are unselected. PDF extraction and embedding remain unimplemented.
- License status for all 40 entries remains unknown. G-010 needs a named independent reviewer approving exact versions and crop/region/method scope. Local checks do not constitute review.

Local inventory/schema work is complete; external source/license/scientific eligibility audit remains open. F-040 source/notes engineering verification is separate from full eligible ingestion and scientific activation.
