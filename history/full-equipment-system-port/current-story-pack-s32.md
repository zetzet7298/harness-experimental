# Current Story Pack — S32 Missing Resource Row Audit

**Date:** 2026-05-20
**Feature:** full-equipment-system-port
**Mode:** bounded resource-resolution investigation
**Source context:** After S31, visual-status audit still has `missing-resource-resolution=82`, all under weapon rows.

## Story Outcome

Identify exactly which VHCND resource tables/rows are missing for the 82 unresolved weapon visuals and prove whether any configured `/var/www/vhcnd` table candidate can supply a fallback row.

## Acceptance Criteria

1. A committed audit artifact lists all 82 affected rows and their resource table candidates.
2. Audit groups the gap by table and row number.
3. Audit confirms whether fallback rows are available in any configured VHCND table candidate.
4. Tests cover the grouping and fallback-absence contract.
5. Runtime isolation and build remain green.

## Expected Files / Impact Surface

- `/var/www/vltk-h5-survivors/game-source/scripts/vltk-audit-equipment-missing-resources.py`
- `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/equipment-visual-missing-resource.audit.json`
- `/var/www/vltk-h5-survivors/game-source/tests/properties/equipmentMissingResource.unit.test.ts`
- `history/full-equipment-system-port/CONTEXT.md`
- `history/full-equipment-system-port/current-story-pack-s32.md`
- `history/full-equipment-system-port/validation-s32.md`
- `history/full-equipment-system-port/review-report-s32.md`

## Planning Handoff

Proceed to validation/review. S32 is evidence-only: it does not synthesize missing resource rows. Next work should decide unresolved handling or source recovery for these weapon rows.
