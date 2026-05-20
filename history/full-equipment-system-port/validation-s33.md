# Validation — S33 Missing Resource Row Handling

**Date:** 2026-05-20
**Feature:** full-equipment-system-port
**Story:** `current-story-pack-s33.md`

## Commands Run

```bash
python3 scripts/vltk-apply-equipment-missing-resource-rows.py --apply
python3 scripts/vltk-audit-equipment-visual-status.py --no-require-safe
npm run check:runtime-isolation
npm test -- tests/properties/equipmentMissingResourceHandling.unit.test.ts tests/properties/equipmentMissingResource.unit.test.ts tests/properties/equipmentVisualMissingSource.unit.test.ts
npm run build
```

GitNexus changed-scope check:

```text
detect_changes(repo="vltk-h5-survivors", scope="all")
```

## Results

- Missing-resource impact audit: PASS — `affectedItemCount=82`, `affectedByTableRow={item/MeleeRes.txt#72:63,item/RangeRes.txt#32:19}`, `affectedBySlot={weapon:82}`.
- Visual status audit: PASS — `missing-resource-row-no-fallback=82`, `missingResourceResolution=0`, `candidate=2566`, `missing-local-source-spr=182`, `missing-npcres-mapping=6304`, `preview-passed-loadout-evidence=418`, `unsafeResolvedVisualItemCount=0`.
- Runtime isolation: PASS — no runtime `/var/www/vhcnd` literals and no symlinks under `src/` or `public/`.
- Tests: PASS — 3 files, 8 tests.
- Production build: PASS — Vite built successfully; existing large chunk warning remains non-blocking.
- GitNexus changed-scope: LOW risk — one indexed symbol touched (`EquipmentItem` type), no affected processes.

## Remaining Gap

Full visual parity is still incomplete. Remaining visual buckets after S33 are `candidate=2566` and `missing-npcres-mapping=6304`, plus preview/local-copy coverage is still partial.
