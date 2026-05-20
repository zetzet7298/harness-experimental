# Current Story Pack — S11 Seed/Test Inventory Workflow

**Feature:** full-equipment-system-port  
**Epic:** E3 Portrait equipment UI + inventory/seed workflow  
**Mode:** `high_risk_feature`  
**Prepared after:** S10 review/compounding passed and pushed.

## Story Outcome

Make the outside-run equipment bag useful for QA across the full VHCND equipment catalog without breaking the normal mobile seed bag. The normal bag remains a bounded 5×5 paginated seed set, while a test/catalog mode lets agents browse all catalog items valid for the selected slot, still using one item per cell and the same equip/unequip/popup flow.

## Entry State

- `src/data/equipmentCatalog.json` contains the generated VHCND equipment catalog.
- `src/data/inventory.json` contains a bounded seed list (`bagItemIds`) and all 15 equipped slots.
- `EquipmentScene.filteredItems()` currently reads only `seedBagItemIds`, filters by selected slot, and removes equipped IDs.
- `bagPageCount()` currently caps every bag list at `MAX_BAG_PAGES = 5`; this is correct for normal seed mode but prevents browsing all catalog rows for testing.
- Existing bag grid is a 5×5 matrix, so S11 can preserve one equipment per mobile cell.

## Source / Local Evidence

- `/var/www/vltk-h5-survivors/game-source/src/game/scenes/EquipmentScene.ts:248-318` — bag grid and pagination actions.
- `/var/www/vltk-h5-survivors/game-source/src/game/scenes/EquipmentScene.ts:324-360` — current seed-only `filteredItems()` and capped `bagPageCount()`.
- `/var/www/vltk-h5-survivors/game-source/tests/properties/equipmentScene.unit.test.ts:217-310` — current pagination contract tests.
- GitNexus impact for `filteredItems` reported `CRITICAL` because bag filtering feeds create/equip/unequip/refresh flows. S11 must run the full validation chain and keep scope minimal.

## Acceptance Criteria

1. Normal seed bag remains bounded: 5×5 cells, at most 5 pages, sourced from `inventory.json` seed IDs.
2. Test/catalog mode is available from the EquipmentScene UI and uses the full generated catalog for the selected slot.
3. Test/catalog mode still shows exactly one equipment per cell and excludes currently equipped items from the visible bag list.
4. Page count is capped in seed mode but can exceed 5 in catalog mode so every valid item for a slot can be reached.
5. Existing equip/unequip/popup/stat snapshot behavior remains unchanged.
6. Regression tests cover both seed-mode cap and catalog-mode unbounded page count/source selection.
7. Validation passes: `npm run typecheck`, `npm run test:pbt -- tests/properties/equipmentScene.unit.test.ts`, `npm run check:no-runtime-vhcnd`, `npm run build`, and GitNexus `detect_changes` review.

## Non-Goals

- No new formulas, visual SPR wiring, or item translations.
- No browser screenshot requirement unless layout changes break the node-level UI contract.
- No direct `/var/www/vhcnd` runtime reads and no symlinks.
