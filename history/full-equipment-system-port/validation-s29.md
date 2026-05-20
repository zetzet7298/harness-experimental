# Validation — S29 Canonical Parts Source Report Repair

**Date:** 2026-05-20
**Feature:** full-equipment-system-port
**Story:** `current-story-pack-s29.md`

## Commands Run

```bash
python3 scripts/vltk-extract-required-sprs.py --packet data/vltk-normalized/port-packets/equipment-visual-parts-all.json --slug equipment-visual-parts-all --workers auto
python3 scripts/vltk-export-equipment-visual-parts.py
python3 scripts/vltk-audit-equipment-visual-part-coverage.py
npm run check:runtime-isolation
npm test -- tests/properties/equipmentScene.unit.test.ts
npm run build
```

## Results

- Required SPR report: PASS — `required=322`, `copied=284`, `missing=38`.
- Dynamic part export: PASS — `requestedTaskCount=284`, `exportedCount=284`, `failedCount=0`, `missingSourceCountsByAction={run:19,idle:19}`.
- Dynamic part coverage audit: PASS as truthful incomplete state — `remainingDedicatedPartAssetGap=38`, `remainingPartSheetGap=272`, `runtimeDynamicLayeringImplemented=true`.
- Runtime isolation: PASS — no `/var/www/vhcnd` literals and no symlinks under runtime paths.
- Equipment scene unit/property test: PASS — 25/25 tests passed.
- Production build: PASS — Vite built successfully; existing large chunk warning remains non-blocking.

## Remaining Gap

The 38 missing SPRs are still real blockers for full dynamic part asset coverage. S29 only prevents the report from falsely listing already-local destination SPRs as missing on rerun.
