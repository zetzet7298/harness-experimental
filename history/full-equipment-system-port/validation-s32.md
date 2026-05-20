# Validation — S32 Missing Resource Row Audit

**Date:** 2026-05-20
**Feature:** full-equipment-system-port
**Story:** `current-story-pack-s32.md`

## Commands Run

```bash
python3 scripts/vltk-audit-equipment-missing-resources.py
npm run check:runtime-isolation
npm test -- tests/properties/equipmentMissingResource.unit.test.ts tests/properties/equipmentVisualMissingSource.unit.test.ts
npm run build
```

## Results

- Missing resource audit: PASS — `missingResourceItemCount=82`, `fallbackRowAvailableCount=0`.
- Grouping: PASS — `item/MeleeRes.txt` row `72` affects 63 rows; `item/RangeRes.txt` row `32` affects 19 rows.
- Tests: PASS — 2 files, 6 tests.
- Runtime isolation: PASS — no runtime `/var/www/vhcnd` literals and no symlinks under runtime paths.
- Production build: PASS — Vite built successfully; existing large chunk warning remains non-blocking.
- GitNexus changed-scope check after this evidence-only addition reported no indexed symbol changes because the new files are audit/test/script additions outside currently indexed execution symbols.

## Remaining Gap

S32 proves there is no fallback row in the configured VHCND table candidates. Next work must either recover a new source table with these rows or mark the 82 weapon visuals unresolved with the same no-guessing policy used by S31.
