# Validation — S16 Equipment UI Centered Popup + Continuous Bag Scroll

**Date:** 2026-05-20
**Feature:** full-equipment-system-port
**Story:** `current-story-pack-s16.md`
**Result:** FEASIBLE — execution may proceed with one UI/test bead.

## Reality Gate

- `EquipmentScene.ts` currently violates D14: footer `‹` / `›` buttons update `bagOffset` by `PAGE_SIZE`, and `pageIndicator` renders page text.
- `EquipmentScene.ts` currently violates D13: `showItemPopup()` uses `panelY = 342` and lower-panel placement instead of viewport center math.
- Current `equipmentScene.unit.test.ts` protects old pagination; these tests must be updated so the new contract is enforced.
- GitNexus impact for `EquipmentScene` is LOW: direct importer `src/game/createGame.ts`, then `src/main.ts`; no affected execution flows reported.

## Feasibility Answers

1. The patch can keep the current 5×5 visible matrix and replace page stepping with scroll state: keep one-cell-per-item visible cells, use `bagOffset` as first visible item, and change it by row increments from pointer/wheel drag instead of page increments.
2. Tap-vs-drag is feasible with a movement threshold: record pointer-down position and suppress selection if movement exceeds threshold.
3. Popup centering is feasible with `panelWidth`, `panelHeight`, `panelX = (GAME_WIDTH - panelWidth) / 2`, and `panelY = (GAME_HEIGHT - panelHeight) / 2`.
4. Browser proof is feasible through `agent-browser`/Playwright by exposing non-user-facing debug getters or by inspecting Phaser scene objects; source/property tests can cover most structural UI contract.

## Approved Execution Surface

Create one bead:

- Remove footer page buttons and page-count indicator.
- Add hold/drag and wheel-style vertical bag scrolling with clamp and tap-vs-drag threshold.
- Center `showItemPopup()` panel in the viewport.
- Update property tests to reject old pagination and require scroll handlers, centered-popup math, and Vietnamese UI labels.
- Validate with `npm run typecheck`, `npm run test:pbt`, `npm run check:no-runtime-vhcnd`, and browser proof on port 5173.

## Blockers

None.

## Execution Proof — 2026-05-20

- Implemented S16 in `game-source/src/game/scenes/EquipmentScene.ts`: removed footer page arrows/page indicator, added hold/drag vertical bag scroll with tap-vs-drag suppression, kept 5×5 one-cell inventory matrix, and centered item popup using viewport center math.
- Updated `game-source/tests/properties/equipmentScene.unit.test.ts` to reject pagination APIs and require scroll handlers, centered popup math, Vietnamese-safe popup title, and scroll hint text.
- Validation passed:
  - `npm run typecheck`
  - `npm run test:pbt` — 17 files / 239 tests passed
  - `npm run check:no-runtime-vhcnd` — runtime isolation clean
- Browser proof on `http://127.0.0.1:5173` with `agent-browser` viewport `390x844`:
  - switched bag to Catalog mode and hold/dragged upward; debug state changed `bagOffset` from `0` to `10`, proving scroll-driven browsing.
  - tapped visible bag cell after scroll; popup debug state reported `popupCentered: true` with bounds `{ x: 18, y: 209, width: 354, height: 426 }`.
  - screenshots saved at `/tmp/s16-equipment-scrolled.png` and `/tmp/s16-equipment-centered-popup.png`.
  - browser console had only normal Vite/Phaser startup logs; no page errors reported.
