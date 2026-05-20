# Validation — S45 Gold Detail Visual Resource Mapping

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

- Source-backed mapping fix applied: gold detail 7 uses `HelmRes`, detail 10 uses `HorseRes`, and detail 8/cuff no longer borrows a visual resource table.
- Visual safety audit after regeneration: `candidate=0`, `missingLocalSourceSprites=179`, `missingMaskTemplateMapping=1764`, `missingNpcResMapping=879`, `missingNpcResRows=6`, `missingResourceRowsNoFallback=87`, `previewPassedLoadoutEvidence=2527`, `unsafeResolvedVisualItems=0`, `unresolvedVisualItems=2915`.
- Missing-source evidence: 27 newly exposed horse `MA_HB/MA_HH/MA_HT_*_HR01.spr` candidates were absent from `/var/www/vhcnd` filesystem search and PAK all-match extraction (`/tmp/s45-missing-horse-sprs/manifest.tsv`, `nonmiss=0`).
- Property tests: PASS — 25 files, 260 tests.
- Targeted Python smoke: PASS.
- Runtime isolation: PASS — no runtime `/var/www/vhcnd` literals and no symlinks under `src/` or `public/`.
- Production build: PASS — Vite built successfully; existing large chunk warning remains non-blocking.
- Browser smoke: PASS — localhost page loaded and `agent-browser errors` reported no errors before debug eval.

## Remaining Gap

The 179 source-missing visual rows remain unresolved by design. S45 improves formula/resource routing and audit truth; it does not fabricate missing SPRs or map mask/yinjian/shiping special visual paths.
