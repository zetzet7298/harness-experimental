# Current Story Pack — S25 Active Equipment Table Precedence

**Date:** 2026-05-20  
**Feature:** full-equipment-system-port  
**Mode:** small audit/evidence slice  
**Source context:** `CONTEXT.md` deferred planning item: determine exact VHCND active package/table precedence before generating more catalog rows.

## Story Outcome

Make the equipment table precedence used by the normalizer explicit, generated, and test-checked for every equipment source table. The current build should say which candidate path won, which candidates were checked first, and why item rows come from the active VHCND ServerNew settings mirror rather than an implicit or stale table.

## Entry State

- `scripts/vltk-normalize-equipment-index.py` resolves table paths through `resolve_item_table_path()` but the generated summary only records the selected source path.
- `data/vltk-normalized/equipment-index.summary.json::activeTableInventory` records active table source and row counts but not the full precedence chain.
- `CONTEXT.md` still has an unchecked package/table precedence gap.

## Acceptance Criteria

1. Generated table inventory includes the candidate precedence chain for every required equipment/meta table.
2. The audit verifies that the selected table is the first existing candidate in that chain.
3. Tests assert current active rows are sourced from the expected active VHCND ServerNew mirror and keep row-count/provenance checks green.
4. `CONTEXT.md` is updated with the resolved precedence rule.
5. Validation includes normalizer regeneration, table inventory audit, smoke tests, runtime isolation, and GitNexus changed-scope review.

## Non-Goals

- Do not generate new catalog rows beyond deterministic regeneration.
- Do not change item formula/stat logic.
- Do not change runtime asset behavior.

## Expected Files / Impact Surface

- `/var/www/vltk-h5-survivors/game-source/scripts/vltk-normalize-equipment-index.py`
- `/var/www/vltk-h5-survivors/game-source/scripts/vltk-audit-equipment-table-inventory.py`
- `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/equipment-index.summary.json`
- `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/equipment-table-inventory.audit.json`
- `/var/www/vltk-h5-survivors/game-source/tests/test_vltk_porting_smoke.py`
- `history/full-equipment-system-port/CONTEXT.md`
- `history/full-equipment-system-port/validation-s25.md`
- `history/full-equipment-system-port/review-report-s25.md`

## Planning Handoff

Proceed to repair/validation. This is a provenance audit slice; if deterministic regeneration changes item contents unexpectedly, stop and document before committing.
