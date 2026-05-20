# Current Story Pack — S26 Extended Slot Portrait Layout Decision

**Date:** 2026-05-20
**Feature:** full-equipment-system-port
**Mode:** small audit/evidence slice
**Source context:** `CONTEXT.md` deferred planning item: decide how to represent extended slots in portrait UI without hiding any slot.

## Story Outcome

Lock a concrete portrait equipment slot layout decision for all VHCND-supported H5 equipment slots. The layout must keep every slot visible and selectable without pagination or hidden/collapsed slot groups.

## Decision

Use the current all-visible two-column paper-doll layout:

- Left column: `head`, `body`, `belt`, `weapon`, `foot`, `mask`, `pifeng`.
- Right column: `cuff`, `amulet`, `ring1`, `ring2`, `pendant`, `yinjian`, `shiping`.
- Center bottom: `horse`.

This preserves D3 full slot coverage and is preferable to collapsible side groups for the current portrait viewport because every slot and caption already fits within the paper-doll band above the bag.

## Acceptance Criteria

1. `CONTEXT.md` records the chosen extended-slot representation.
2. Evidence proves all 15 slot labels and layout entries exist.
3. Evidence proves slot buttons/captions remain inside the paper-doll bounds and above the bag.
4. Inventory grid remains disjoint from the paper-doll and stats panels.
5. No runtime/code change is required unless the evidence contradicts the decision.

## Expected Files / Impact Surface

- `history/full-equipment-system-port/CONTEXT.md`
- `history/full-equipment-system-port/current-story-pack-s26.md`
- `history/full-equipment-system-port/validation-s26.md`
- `history/full-equipment-system-port/review-report-s26.md`
- Evidence source: `/var/www/vltk-h5-survivors/game-source/src/game/scenes/EquipmentScene.ts`
- Evidence tests: `/var/www/vltk-h5-survivors/game-source/tests/properties/equipmentScene.unit.test.ts` and `tests/properties/prop07-grid-disjointness.test.ts`

## Planning Handoff

Proceed directly to validation/review because this is an evidence-backed decision slice. Do not redesign code unless tests or browser evidence show a hidden/overlapping slot.
