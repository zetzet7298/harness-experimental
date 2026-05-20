# Validation — S38 Candidate Visual Preview Batch

**Date:** 2026-05-20
**Feature:** full-equipment-system-port
**Story:** `current-story-pack-s38.md`

## Commands Run

```bash
python3 scripts/vltk-preview-candidates.py \
  --input data/vltk-normalized/port-packets/equipment-visual-candidate-batch-s38.json \
  --out data/vltk-normalized/previews/equipment-visual-candidate-batch-s38.png \
  --report-out data/vltk-normalized/previews/equipment-visual-candidate-batch-s38.report.json \
  --preview-status passed \
  --reviewer-note "S38 visual inspection passed: rw019/hd004 and body016/body019 trios decode cleanly from local equipment-visual-parts-all SPR sources."
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

- Preview gate: PASS — `equipment-visual-candidate-batch-s38.report.json` has `status=passed`, `matched=8`, `rendered=8`, and cites local `game-source/public/assets/character/vhcnd/source/equipment-visual-parts-all/*.spr` paths.
- Visual status audit: PASS — `candidate=911`, `preview-passed-loadout-evidence=2073`, `unsafeResolvedVisualItems=0`, `missingResourceResolution=0`, `missingResourceRowsNoFallback=82`.
- Candidate audit: PASS — `candidateItemCount=911`, distribution `{body:384,head:259,horse:96,weapon:172}`, `missingPreviewSpriteCount=95`, `actionableLocalSourceSpriteCount=95`, `missingLocalSourceSpriteCount=0`.
- Tests: PASS — 4 files, 33 tests, including D14 hold/drag continuous-scroll regression coverage.
- Runtime isolation: PASS — no runtime `/var/www/vhcnd` literals and no symlinks under `src/` or `public/`.
- Production build: PASS — Vite built successfully; existing large chunk warning remains non-blocking.
- GitNexus changed-scope: LOW risk; changed symbols `0`, affected processes `0` because S38 changes are generated audit/packet/preview/test data artifacts.

## Remaining Gap

S38 does not compose or wire runtime visuals. Continue preview-gating the 95 remaining actionable local candidate sprite basenames, then separately promote passed evidence through the parts-export/runtime manifest gate only when a later player-facing visual story requires it.
