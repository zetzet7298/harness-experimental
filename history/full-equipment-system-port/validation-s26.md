# Validation — S26 Extended Slot Portrait Layout Decision

**Date:** 2026-05-20
**Feature:** full-equipment-system-port
**Story:** S26 Extended Slot Portrait Layout Decision

## Evidence

- Source layout: `src/game/scenes/EquipmentScene.ts:30-63`
  - `SLOT_LABELS` contains all 15 slots.
  - `EQUIPMENT_SLOT_LAYOUT` places seven left-column slots, seven right-column slots, and centered `horse`.
- Slot coverage tests: `tests/properties/equipmentScene.unit.test.ts:109-164`
  - Verifies exactly 15 H5 slots.
  - Verifies `SLOT_LABELS` covers `EQUIPMENT_SLOT_ORDER`.
  - Verifies every slot appears in `EQUIPMENT_SLOT_LAYOUT`.
  - Verifies every slot button/caption stays inside `PAPER_DOLL_BOUNDS` and above `BAG_TOP`.
- Grid disjointness tests: `tests/properties/prop07-grid-disjointness.test.ts:146-220`
  - Verifies every visible bag cell is inside the bag panel.
  - Verifies bag cells are disjoint from the paper-doll and stats panels.

## Commands

- `npm test -- tests/properties/equipmentScene.unit.test.ts tests/properties/prop07-grid-disjointness.test.ts`
  - Result: 2 test files passed, 31 tests passed.

## Acceptance Criteria Mapping

1. `CONTEXT.md` records the decision: satisfied.
2. All 15 labels/layout entries exist: satisfied by source and unit tests.
3. Slot buttons/captions fit inside paper-doll bounds and above bag: satisfied by `equipmentScene.unit.test.ts`.
4. Inventory grid remains disjoint: satisfied by `prop07-grid-disjointness.test.ts`.
5. No runtime/code change required: evidence supports existing layout, so S26 is docs/evidence only.
