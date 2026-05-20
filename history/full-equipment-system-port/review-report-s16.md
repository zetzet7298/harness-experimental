# Review Report — S16 Equipment UI Centered Popup + Continuous Bag Scroll

**Date:** 2026-05-20
**Story:** `current-story-pack-s16.md`
**Result:** PASS — no P1/P2/P3 review beads opened.

## Scope Reviewed

- Game commit: `f4766d7 feat(equipment): replace bag pagination with drag scroll`
- Harness commit: `dee05dc docs(equipment): record S16 scroll validation`
- Files reviewed:
  - `/var/www/vltk-h5-survivors/game-source/src/game/scenes/EquipmentScene.ts`
  - `/var/www/vltk-h5-survivors/game-source/tests/properties/equipmentScene.unit.test.ts`
  - `history/full-equipment-system-port/current-story-pack-s16.md`
  - `history/full-equipment-system-port/validation-s16.md`

## Specialist Review Summary

| Focus | Verdict | Evidence |
| --- | --- | --- |
| Code quality | PASS | `EquipmentScene.ts` now has explicit scroll constants, row-aligned `clampBagOffset`, and tap-vs-drag guard through `bagDragMoved`. |
| Architecture | PASS | Change is isolated to `EquipmentScene` UI state and property tests; no formula, gateway, visual resolver, or catalog schema coupling changed. |
| Security/isolation | PASS | `check:no-runtime-vhcnd` passed; no new symlink/direct runtime VHCND dependency introduced. |
| Test coverage | PASS | Property tests reject old pagination APIs, require scroll handlers/threshold, require centered popup math, and preserve 5×5 matrix contract. |
| Learnings | PASS | S16 is a direct UI-contract correction; no new critical reusable failure pattern beyond existing Khuym gate discipline. |

## Artifact Verification

| Artifact / Promise | EXISTS | SUBSTANTIVE | WIRED | Notes |
| --- | --- | --- | --- | --- |
| Centered popup implementation | yes | yes | yes | `panelX = (GAME_WIDTH - panelWidth) / 2`, `panelY = (GAME_HEIGHT - panelHeight) / 2`; browser debug reports `popupCentered: true`. |
| Scroll-driven bag browsing | yes | yes | yes | Scroll zone and bag cells wire `pointerdown`, `pointermove`, `pointerup`, and `wheel`; dragging changed `bagOffset` `0 → 10` in browser proof. |
| Pagination removal | yes | yes | yes | Property tests assert no `bagPageCount`, `PAGE_SIZE`, `MAX_BAG_PAGES`, or `pageIndicator`. |
| Tap-vs-drag protection | yes | yes | yes | `BAG_DRAG_THRESHOLD` and `bagDragMoved` suppress popup activation during drag. |
| Vietnamese-safe user-facing popup title | yes | yes | yes | Popup title uses `displayItemName(item)` and quality label; source/mojibake names stay internal/provenance. |
| Validation evidence | yes | yes | yes | `validation-s16.md` records typecheck, property tests, runtime isolation, and browser proof. |

## Validation Rechecked

Evidence recorded in `validation-s16.md`:

- `npm run typecheck` — passed.
- `npm run test:pbt` — 17 files / 239 tests passed.
- `npm run check:no-runtime-vhcnd` — passed.
- Browser proof on port `5173` — passed with centered popup bounds `{ x: 18, y: 209, width: 354, height: 426 }` and scroll `bagOffset` `0 → 10`.

## Findings

None.

## Handoff

S16 review is complete. Run `khuym:compounding`, then select the next incomplete story from `CONTEXT.md` / `approach.md`.
