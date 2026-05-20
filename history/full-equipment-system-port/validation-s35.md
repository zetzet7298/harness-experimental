# Validation — S35 Candidate Visual Preview Batch

**Date:** 2026-05-20
**Feature:** full-equipment-system-port
**Story:** `current-story-pack-s35.md`

## Commands Run

```bash
python3 scripts/vltk-preview-candidates.py \
  --input data/vltk-normalized/port-packets/equipment-visual-candidate-batch-s35.json \
  --out data/vltk-normalized/previews/equipment-visual-candidate-batch-s35.png \
  --report-out data/vltk-normalized/previews/equipment-visual-candidate-batch-s35.report.json \
  --preview-status passed \
  --reviewer-note "S35 visual inspection passed: hd007 icon/part and body007 trio decode cleanly from local equipment-visual-parts-all SPR sources."
python3 scripts/vltk-audit-equipment-visual-status.py
python3 scripts/vltk-audit-equipment-visual-candidates.py
npm run check:runtime-isolation
npm test -- tests/properties/equipmentVisualCandidates.unit.test.ts tests/properties/equipmentVisualMissingSource.unit.test.ts tests/properties/equipmentMissingResourceHandling.unit.test.ts tests/properties/equipmentScene.unit.test.ts
npm run build
```

GitNexus changed-scope:

```text
detect_changes(repo="vltk-h5-survivors", scope="all")
```

## Results

- Preview gate: PASS — `equipment-visual-candidate-batch-s35.report.json` has `status=passed`, `matched=4`, `rendered=4`, and cites local `game-source/public/assets/character/vhcnd/source/equipment-visual-parts-all/*.spr` paths.
- Visual status audit: PASS — `candidate=1960`, `preview-passed-loadout-evidence=1024`, `unsafeResolvedVisualItems=0`, `missingResourceResolution=0`, `missingResourceRowsNoFallback=82`.
- Candidate audit: PASS — `candidateItemCount=1960`, slot distribution `{body:767,cuff:74,head:510,horse:96,weapon:513}`, `missingPreviewSpriteCount=113`, `actionableLocalSourceSpriteCount=113`, `missingLocalSourceSpriteCount=0`.
- Tests: PASS — 4 files, 33 tests. This includes the D14 equipment-scene hold/drag continuous-scroll regression tests.
- Runtime isolation: PASS — no runtime `/var/www/vhcnd` literals and no symlinks under `src/` or `public/`.
- Production build: PASS — Vite built successfully; existing large chunk warning remains non-blocking.
- GitNexus changed-scope: LOW risk; changed symbol `scripts/vltk-preview-candidates.py:resolve_sprite_source`, affected processes `0`.

## Remaining Gap

S35 does not compose or wire runtime visuals. The next visual-coverage story should preview-gate another bounded subset of the 113 still-actionable local candidate sprite basenames, or explicitly promote already-passed previews through the existing composer/runtime-manifest gate if a player-facing loadout requires them.
