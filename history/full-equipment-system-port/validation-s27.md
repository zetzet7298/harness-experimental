# Validation — S27 Seed Inventory vs Catalog Browser Decision

**Date:** 2026-05-20
**Feature:** full-equipment-system-port
**Story:** S27 Seed Inventory vs Catalog Browser Decision

## Evidence

- Runtime source: `src/game/scenes/EquipmentScene.ts:108-120`
  - Seed bag item ids are deduped and capped by `MAX_SEED_BAG_ITEMS`.
- Runtime source: `src/game/scenes/EquipmentScene.ts:320-329`
  - The bottom action row toggles `bagMode` between `seed` and `catalog`.
- Runtime source: `src/game/scenes/EquipmentScene.ts:396-424`
  - Seed mode sources `this.seedBagItemIds`.
  - Catalog mode sources `this.catalog.items`.
  - Both modes filter by `item.allowedSlots.includes(this.selectedSlot)`.
- Data audit during validation:
  - Current catalog total: 9552 rows.
  - Current seed bag: 125 rows, one-equipment-per-mobile-cell.
  - All catalog items have at least one allowed slot; each slot has reachable catalog rows.

## Commands

- `python3 -m unittest discover -s tests -p 'test_vltk_porting_smoke.py' -k seed_inventory`
  - Result: 1 test passed.
- `python3 -m unittest discover -s tests -p 'test_vltk_porting_smoke.py'`
  - Result: 61 tests passed.

## Acceptance Criteria Mapping

1. `CONTEXT.md` records strategy: satisfied.
2. Visible/tappable Seed ↔ Catalog toggle: satisfied by `createActions()` source.
3. Seed mode capped and one-cell: satisfied by inventory data and smoke test.
4. Catalog mode uses full catalog: satisfied by `filteredItems()` source and smoke test.
5. Every catalog row reachable: satisfied by `test_seed_inventory_stays_sampled_while_catalog_mode_can_reach_every_item`.
