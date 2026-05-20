# Current Story Pack — S16 Equipment UI Centered Popup + Continuous Bag Scroll

**Feature:** full-equipment-system-port
**Epic:** E3 Portrait equipment UI and inventory usability
**Mode:** `high_risk_feature`
**Prepared after:** S15 review/compounding passed and pushed.

## Story Outcome

Redesign the current equipment scene interaction so item detail popup opens centered on the portrait viewport and the equipment bag no longer uses page-by-page pagination. The bag should use mobile-friendly hold/drag vertical scrolling over the visible matrix while preserving one-cell-per-item, slot filtering, equip/unequip flow, and browser-testable Vietnamese-only user-facing UI.

## Entry State

- `CONTEXT.md` D13 requires the equipment detail popup/panel to be centered on screen.
- `CONTEXT.md` D14 rejects the current page-by-page pagination and requires hold/drag vertical continuous scrolling.
- Current `EquipmentScene.ts` uses footer `‹` / `›` page buttons, `bagPageCount()`, `PAGE_SIZE`, `bagOffset += PAGE_SIZE`, and page indicator text like `1/4`.
- Current popup starts at `panelY = 342` and anchors the panel near the lower half of the screen, not centered.
- Current tests explicitly expect pagination; S16 must rewrite those tests to protect the new interaction instead of preserving old behavior.

## Acceptance Criteria

1. Item detail popup/panel is centered in the viewport using explicit center coordinates, not anchored only to a tapped bag cell or lower panel.
2. Footer pagination controls `‹` / `›` are removed from the equipment scene; bag browsing is via hold/drag vertical scroll or equivalent pointer/wheel scroll.
3. The visible bag remains a clear 5×5 matrix with each equipment item occupying exactly one cell.
4. Scrolling clamps to available filtered items, keeps slot filtering and seed/catalog modes, and selection opens the correct item popup after tap/click without accidental selection during drag.
5. User-facing strings touched by S16 are Vietnamese-only and contain no Chinese characters; internal item ids/provenance can remain non-user-facing.
6. Validation includes typecheck, property tests covering UI source contracts, runtime isolation, and browser proof on port 5173 showing centered popup and scroll interaction.
7. S16 must not introduce green-quality mounts or direct/symlink runtime reads from `/var/www/vhcnd`.

## Non-Goals

- Do not batch-port new item data, formulas, or visuals in S16.
- Do not solve full catalog virtualization for every future UI requirement beyond making current seed/catalog browsing scroll-driven and testable.
- Do not change combat formulas or in-run resolver behavior.

## Validation Questions

1. What is the smallest safe change to replace page buttons with scroll while preserving the existing bag cell grid and tests?
2. Can property tests prove the scene no longer has pagination buttons/handlers and has scroll handlers instead?
3. Can browser automation open an item popup and check its center approximately matches the viewport center?
4. How should tap vs drag be disambiguated to avoid opening a popup while the user scrolls?

## Expected Files / Impact Surface

- `/var/www/vltk-h5-survivors/game-source/src/game/scenes/EquipmentScene.ts`
- `/var/www/vltk-h5-survivors/game-source/tests/properties/equipmentScene.unit.test.ts`
- Optional smoke/browser test notes under harness review artifacts

## Planning Handoff

S16 is ready for `khuym:validating`. If validation confirms low impact and existing tests can be updated in one slice, create one execution bead for the UI patch and browser proof.
