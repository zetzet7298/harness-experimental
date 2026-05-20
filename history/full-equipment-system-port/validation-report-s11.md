# Validation Report — S11 Seed/Test Inventory Workflow

**Feature:** full-equipment-system-port  
**Mode:** `high_risk_feature`  
**Date:** 2026-05-20  
**Decision:** `READY WITH CONSTRAINTS — CREATE CURRENT-STORY BEADS`

## Reality Gate

S11 is feasible but high-risk because `filteredItems()` participates in bag display, selected item, equip, unequip, and refresh flows. The implementation must preserve normal seed-bag behavior while adding a test/catalog mode that exposes all generated catalog rows for the selected slot.

## Feasibility Matrix

| Assumption | Evidence | Result |
| --- | --- | --- |
| Full catalog is already available to the scene. | `EquipmentScene` already loads `equipmentCatalogData` and stores `this.catalog`. | PASS |
| Normal seed bag is bounded and should remain bounded. | `seedBagItemIds`, `PAGE_SIZE`, `MAX_BAG_PAGES`, and `MAX_BAG_ITEMS` already enforce ≤125 seed items. | PASS |
| Catalog browsing needs a separate mode. | Current `bagPageCount` cap prevents reaching all catalog rows; CONTEXT deferred question explicitly allows generated test-mode catalog browser. | PASS |
| Impact needs full validation. | GitNexus impact for `filteredItems` is CRITICAL. | PASS WITH FULL VALIDATION REQUIRED |

## Required Current-Story Beads

1. **S11A catalog browser mode** — add a seed/catalog bag mode toggle and update filtering/page counts so catalog mode can browse all valid slot items while seed mode remains capped.
2. **S11B regression tests** — strengthen `equipmentScene.unit.test.ts` for seed-vs-catalog source selection, capped vs uncapped page counts, and one-cell grid contract.
3. **S11C validation and handoff** — run typecheck, equipment scene PBT/unit tests, runtime isolation, build, GitNexus detect_changes; update review/compounding docs if pass.

## Execution Constraints

- Keep every visible item one cell in the existing 5×5 matrix.
- Do not make normal gameplay inventory a 9k item bag by default.
- Do not change equip-condition/stat semantics.
- Do not introduce runtime reads from `/var/www/vhcnd` or symlinks.

## Execution Evidence — 2026-05-20

- Implemented S11A in `game-source/src/game/scenes/EquipmentScene.ts`: footer `Kho: Seed` / `Kho: Catalog` toggle, mode-aware bag source, catalog-mode uncapped page count, next-page clamp through `bagPageCount()`.
- Implemented S11B in `game-source/tests/properties/equipmentScene.unit.test.ts`: regression coverage for toggle labels, source selection, capped seed mode, uncapped catalog mode, mode-aware next-page logic, and existing 5×5 one-cell grid contract.
- GitNexus `detect_changes(repo="vltk-h5-survivors", scope="all")`: `critical` risk because `EquipmentScene`/equip flows are intentionally affected; reviewed affected processes and constrained changes to inventory browsing only.

## Validation Commands

| Check | Result | Evidence |
| --- | --- | --- |
| `npm run typecheck` | PASS | `tsc --noEmit` completed with exit 0. |
| `npm run test:pbt -- tests/properties/equipmentScene.unit.test.ts` | PASS | 17 files / 236 tests passed. |
| `npm run check:no-runtime-vhcnd` | PASS | `OK: runtime isolation clean (no /var/www/vhcnd literals and no symlinks under src/ or public/)`. |
| `npm run build` | PASS | Vite build completed; large bundle warning only. |
| Browser E2E on `http://127.0.0.1:5173` | PASS | Screenshots: `/tmp/s11-equipment-full2.png`, `/tmp/s11-equipment-catalog.png`, `/tmp/s11-equipment-catalog-page2.png`, `/tmp/s11-equipment-popup.png`. Verified seed mode `1/1`, catalog mode `1/26`, next page `2/26`, and popup opens from catalog cell. |

## Beads Closed

- `mig-6k8` — S11A catalog browser mode.
- `mig-97j` — S11B seed/catalog bag regression tests.
- `mig-75p` — S11C validation chain for seed/catalog inventory.
