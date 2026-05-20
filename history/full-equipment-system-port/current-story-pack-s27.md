# Current Story Pack — S27 Seed Inventory vs Catalog Browser Decision

**Date:** 2026-05-20
**Feature:** full-equipment-system-port
**Mode:** small audit/evidence slice
**Source context:** `CONTEXT.md` deferred planning item: decide whether seed inventory remains coverage-sampled or adds a generated test-mode catalog browser for all equipment rows.

## Story Outcome

Lock the equipment browsing strategy so QA can test the full generated catalog without making the normal mobile bag unusable.

## Decision

Keep two browsing modes:

- `Kho: Seed`: coverage-sampled/easy-test inventory capped at 125 one-cell items.
- `Kho: Catalog`: uncapped generated catalog browser sourced from `this.catalog.items`, filtered by the currently selected slot.

This satisfies D8 because the seed bag remains compact for equip/unequip smoke testing, while catalog mode lets agents inspect every generated equipment row by selecting its valid slot.

## Acceptance Criteria

1. `CONTEXT.md` records the chosen strategy.
2. Runtime code has a visible/tappable Seed ↔ Catalog toggle.
3. Seed mode remains capped and one-cell-per-item.
4. Catalog mode sources the full generated catalog, not the seed list.
5. Tests prove every current catalog item is reachable through at least one allowed slot.

## Expected Files / Impact Surface

- `/var/www/vltk-h5-survivors/game-source/src/game/scenes/EquipmentScene.ts` (evidence only)
- `/var/www/vltk-h5-survivors/game-source/tests/test_vltk_porting_smoke.py`
- `history/full-equipment-system-port/CONTEXT.md`
- `history/full-equipment-system-port/current-story-pack-s27.md`
- `history/full-equipment-system-port/validation-s27.md`
- `history/full-equipment-system-port/review-report-s27.md`

## Planning Handoff

Proceed to validation/review. Only test coverage is required because runtime already implements the two-mode strategy.
