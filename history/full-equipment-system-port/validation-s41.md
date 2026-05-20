# Validation — S41 Remaining Candidate Visual Preview Batch

**Date:** 2026-05-20
**Feature:** full-equipment-system-port
**Story:** `current-story-pack-s41.md`

## Commands Run

```bash
python3 scripts/vltk-preview-candidates.py \
  --input data/vltk-normalized/port-packets/equipment-visual-candidate-batch-s41.json \
  --out data/vltk-normalized/previews/equipment-visual-candidate-batch-s41.png \
  --report-out data/vltk-normalized/previews/equipment-visual-candidate-batch-s41.report.json \
  --preview-status passed \
  --reviewer-note "S41 visual inspection passed: all 80 remaining local candidate sprites after S40 decode cleanly from local equipment-visual-parts-all SPR sources." \
  --limit 100
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

- Preview gate: PASS — `equipment-visual-candidate-batch-s41.report.json` has `status=passed`, `matched=80`, `rendered=80`, and cites local `game-source/public/assets/character/vhcnd/source/equipment-visual-parts-all/*.spr` paths.
- Visual status audit: PASS — `candidate=0`, `preview-passed-loadout-evidence=2984`, `unsafeResolvedVisualItems=0`, `missingResourceResolution=0`, `missingResourceRowsNoFallback=82`.
- Candidate audit: PASS — `candidateItemCount=0`, `candidateBySlot={}`, `missingPreviewSpriteCount=0`, `actionableLocalSourceSpriteCount=0`, `missingLocalSourceSpriteCount=0`.
- Tests: PASS — 4 files, 33 tests, including D14 hold/drag continuous-scroll regression coverage.
- Runtime isolation: PASS — no runtime `/var/www/vhcnd` literals and no symlinks under `src/` or `public/`.
- Production build: PASS — Vite built successfully; existing large chunk warning remains non-blocking.
- GitNexus changed-scope: LOW risk; changed symbols `0`, affected processes `0` because S41 changes are generated audit/packet/preview/test data artifacts.

## Remaining Gap

S41 closes the generic preview-candidate bucket. Full visual coverage is still incomplete because explicit unresolved buckets remain: `missing-local-source-spr=204`, `missing-npcres-mapping=6276`, `missing-npcres-row=6`, and `missing-resource-row-no-fallback=82`. S41 does not compose or wire runtime visuals; later stories must address those unresolved buckets or promote passed evidence through parts export/runtime manifest for player-facing visuals.
