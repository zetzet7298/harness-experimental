# Validation — S31 Missing Source Affected-Row Handling

**Date:** 2026-05-20
**Feature:** full-equipment-system-port
**Story:** `current-story-pack-s31.md`

## Commands Run

```bash
python3 scripts/vltk-apply-equipment-visual-missing-sources.py --apply
python3 scripts/vltk-audit-equipment-visual-status.py --no-require-safe
npm run check:runtime-isolation
npm test -- tests/properties/equipmentVisualMissingSource.unit.test.ts
npm test -- tests/properties/equipmentVisualMissingSource.unit.test.ts tests/properties/equipmentScene.unit.test.ts tests/properties/visualResolver.unit.test.ts
npm run build
agent-browser open http://localhost:5173
agent-browser wait 1500
agent-browser screenshot /var/www/vltk-h5-survivors/game-source/artifacts/equipment-s31-browser.png
agent-browser eval "({title:document.title, canvases:document.querySelectorAll('canvas').length, activeScenes:window.__vltkPrototype?.game?.scene?.getScenes(true)?.map(s=>s.scene.key) ?? [], errors:window.__errors || []})"
```

## Results

- Missing impact audit: PASS — `affectedItemCount=182`, `affectedBySlot={head:74,horse:108}`, `affectedByQuality={gold:62,magic:60,normal:60}`.
- Visual status audit: PASS — `missing-local-source-spr=182`, `candidate=2566`, `preview-passed-loadout-evidence=418`, `unsafeResolvedVisualItemCount=0`.
- Runtime isolation: PASS — no runtime `/var/www/vhcnd` literals and no symlinks under `src/` or `public/`.
- Tests: PASS — S31 test 4/4; combined relevant tests 48/48.
- Production build: PASS — Vite built successfully; existing large chunk warning remains non-blocking.
- Browser smoke: PASS — title `VLTK H5 Survivors Prototype`, active scene `EquipmentScene`, `canvases=1`, `errors=[]`.
- GitNexus changed-scope check: `detect_changes(repo="vltk-h5-survivors", scope="all")` reported medium risk, changed symbols in `EquipmentItem`, `EquipmentScene`, and `GameScene`, and affected processes `RefreshBag → EquipmentIconKey` and `LoadWardrobeCatalog → NpcResCodeFromEquipped`; this matches the expected runtime/preview impact surface.

## Remaining Gap

S31 makes absent-source rows safe and explicit, but does not claim full visual parity. Remaining gaps include `candidate=2566`, `missing-npcres-mapping=6304`, and `missing-resource-resolution=82` in the visual-status audit.
