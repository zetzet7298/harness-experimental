# Current Story Pack — S33 Missing Resource Row Handling

**Date:** 2026-05-20
**Feature:** full-equipment-system-port
**Mode:** bounded unresolved-handling slice
**Source context:** S32 proved 82 weapon visual rows need resource rows absent from configured `/var/www/vhcnd` `MeleeRes`/`RangeRes` candidates.

## Story Outcome

Mark the 82 weapon rows as explicitly unresolved due to absent source-backed resource rows, instead of leaving them in the generic `missing-resource-resolution` bucket or synthesizing table rows.

## Acceptance Criteria

1. A committed impact audit lists the 82 affected weapon rows and groups them by missing table row.
2. Affected catalog rows are marked `visual.candidateStatus = "missing-resource-row-no-fallback"` and keep `visual.missingResourceRows` provenance.
3. Visual-status audit separates `missing-resource-row-no-fallback` from ordinary candidates and reports `missingResourceResolution=0`.
4. Tests cover the exact 82-row grouping and no-fallback contract.
5. Runtime isolation, relevant tests, build, and GitNexus changed-scope check pass.

## Expected Files / Impact Surface

- `/var/www/vltk-h5-survivors/game-source/scripts/vltk-apply-equipment-missing-resource-rows.py`
- `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/equipment-visual-missing-resource-impact.audit.json`
- `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/equipment-visual-status.audit.json`
- `/var/www/vltk-h5-survivors/game-source/src/data/equipmentCatalog.json`
- `/var/www/vltk-h5-survivors/game-source/src/domain/types.ts`
- `/var/www/vltk-h5-survivors/game-source/tests/properties/equipmentMissingResourceHandling.unit.test.ts`
- `history/full-equipment-system-port/CONTEXT.md`
- `history/full-equipment-system-port/current-story-pack-s33.md`
- `history/full-equipment-system-port/validation-s33.md`
- `history/full-equipment-system-port/review-report-s33.md`

## Planning Handoff

Proceed to validation/review. S33 makes the weapon resource-row absence explicit and safe; it does not close full visual parity. Next work should reduce the remaining `candidate=2566` and `missing-npcres-mapping=6304` buckets.
