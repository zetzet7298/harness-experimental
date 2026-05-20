# Validation — S46 Special Slot Visual Gap Classification

**Date:** 2026-05-20  
**Feature:** full-equipment-system-port

## Commands

```bash
python3 scripts/vltk-normalize-equipment-index.py
python3 scripts/vltk-build-equipment-seed.py
python3 scripts/vltk-audit-equipment-missing-resources.py
python3 scripts/vltk-apply-equipment-missing-resource-rows.py --apply
python3 scripts/vltk-apply-equipment-visual-missing-sources.py --apply
python3 scripts/vltk-audit-equipment-visual-candidates.py
python3 scripts/vltk-audit-equipment-visual-status.py
npm run test:pbt
python3 tests/test_vltk_porting_smoke.py -k test_equipment_visual_status_audit_quantifies_current_catalog_safety
npm run build
agent-browser open http://localhost:5173 && agent-browser wait --load networkidle && agent-browser errors
```

## Results

- Special-slot visual routing is explicit: ShiPin/YinJian use `missing-itemresidx-visual-mapping`, and gold PiFeng direct `m_PifengType` rows resolve into source-checked sprite gaps.
- Visual status after regeneration: `candidate=0`, `missingLocalSourceSprites=217`, `missingMaskTemplateMapping=1764`, `missingItemResIdxVisualMapping=841`, `missingNpcResMapping=0`, `missingNpcResRows=6`, `missingResourceRowsNoFallback=87`, `previewPassedLoadoutEvidence=2527`, `unsafeResolvedVisualItems=0`, `unresolvedVisualItems=2915`.
- Candidate audit: `candidateItemCount=0`, `missingPreviewSpriteCount=0`, `actionableLocalSourceSpriteCount=0`, `missingLocalSourceSpriteCount=0`.
- Property tests: PASS — 26 files, 262 tests.
- Targeted Python smoke: PASS.
- Runtime isolation: PASS — no runtime `/var/www/vhcnd` literals and no symlinks under `src/` or `public/`.
- Production build: PASS — Vite built successfully; existing large chunk warning remains non-blocking.
- Browser smoke: PASS — localhost page loaded, one canvas present, EquipmentScene active.

## Remaining Gap

Visual parity remains incomplete while `missing-local-source-spr`, `missing-mask-template-mapping`, `missing-itemresidx-visual-mapping`, `missing-npcres-row`, and `missing-resource-row-no-fallback` are nonzero.
