# Validation — S28 Equipment Visual Parts Expansion

**Date:** 2026-05-20
**Feature:** full-equipment-system-port
**Story:** `current-story-pack-s28.md`

## Current Evidence

- `data/vltk-normalized/equipment-visual-status.audit.json` now reports:
  - `resolvedVisualItemCount=418`
  - `candidate=2748`
  - `missing-npcres-mapping=6304`
  - `missing-resource-resolution=82`
  - `preview-passed-loadout-evidence=418`
  - `unsafeResolvedVisualItemCount=0`
- `data/vltk-normalized/equipment-visual-part-coverage.audit.json` reports:
  - `dedicatedPartAssetCountsByAction={run:142,idle:142}`
  - `remainingDedicatedPartAssetGap=38`
  - `remainingPartSheetGap=272`
  - `runtimeDynamicLayeringImplemented=true`
- `data/vltk-normalized/equipment-visual-parts-export.report.json` reports:
  - `requestedTaskCount=284`
  - `exportedCount=284`
  - `failedCount=0`
  - `missingSourceCountsByAction={run:19,idle:19}`

## Commands Run

```bash
python3 scripts/vltk-export-equipment-visual-parts.py
python3 scripts/vltk-audit-equipment-visual-part-coverage.py
npm run check:runtime-isolation
npm test -- tests/properties/equipmentScene.unit.test.ts
npm run build
agent-browser open http://localhost:5173
agent-browser wait 2000
agent-browser screenshot /var/www/vltk-h5-survivors/game-source/artifacts/equipment-s28-browser.png
agent-browser eval "({title:document.title, text:document.body.innerText.slice(0,500), canvases:document.querySelectorAll('canvas').length, errors:(window.__errors||[])})"
agent-browser eval "window.__vltkPrototype.game.scene.getScenes(true).map(s=>s.scene.key)"
agent-browser eval "window.__vltkPrototype.game.scene.getScene('EquipmentScene').getEquipmentUiDebugStatus()"
```

## Results

- Runtime isolation: PASS — no `/var/www/vhcnd` literals and no symlinks under `src/` or `public/`.
- Equipment scene unit/property test: PASS — 25/25 tests passed.
- Production build: PASS — Vite built successfully; existing large chunk warning remains non-blocking.
- Browser smoke: PASS — title `VLTK H5 Survivors Prototype`, `canvases=1`, active scene `EquipmentScene`, no reported `window.__errors`.
- Browser screenshot artifact: `/var/www/vltk-h5-survivors/game-source/artifacts/equipment-s28-browser.png` (ignored local evidence, not committed).

## Gaps Remaining

S28 is incomplete for total feature parity by design. Remaining visual gaps are explicit: `remainingDedicatedPartAssetGap=38`, `remainingPartSheetGap=272`, plus unresolved catalog rows in `candidate`, `missing-npcres-mapping`, and `missing-resource-resolution` states. Continue with the next visual coverage story; do not claim full equipment visual parity yet.
