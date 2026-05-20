# Current Story Pack — S31 Missing Source Affected-Row Handling

**Date:** 2026-05-20
**Feature:** full-equipment-system-port
**Mode:** bounded fallback/unresolved handling slice
**Source context:** S30 proved 38 dynamic-part SPRs are absent from current `/var/www/vhcnd` source/PAK evidence. The next step is to prevent affected rows from requesting absent runtime sheets while preserving source provenance.

## Story Outcome

Identify every catalog row affected by the 38 absent source SPRs, mark those visuals unresolved with source-backed evidence, and make out-of-run/in-run visual resolution skip those rows instead of guessing or borrowing assets.

## Acceptance Criteria

1. A committed impact audit lists affected rows, slots, qualities, and missing sprite basenames.
2. Affected catalog rows are marked `visual.candidateStatus = "missing-local-source-spr"` and keep `visual.missingSourceSprites` for provenance.
3. Runtime and equipment preview visual sprite collection skip `missing-local-source-spr` rows so absent sheets are not requested.
4. Visual status audit reports `missing-local-source-spr` separately from ordinary `candidate` rows.
5. Tests cover affected counts and runtime skip contract.
6. Runtime isolation, relevant property tests, build, and browser smoke pass.

## Expected Files / Impact Surface

- `/var/www/vltk-h5-survivors/game-source/scripts/vltk-apply-equipment-visual-missing-sources.py`
- `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/equipment-visual-missing-impact.audit.json`
- `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/equipment-visual-status.audit.json`
- `/var/www/vltk-h5-survivors/game-source/src/data/equipmentCatalog.json`
- `/var/www/vltk-h5-survivors/game-source/src/domain/types.ts`
- `/var/www/vltk-h5-survivors/game-source/src/game/scenes/GameScene.ts`
- `/var/www/vltk-h5-survivors/game-source/src/game/scenes/EquipmentScene.ts`
- `/var/www/vltk-h5-survivors/game-source/tests/properties/equipmentVisualMissingSource.unit.test.ts`
- `history/full-equipment-system-port/CONTEXT.md`
- `history/full-equipment-system-port/current-story-pack-s31.md`
- `history/full-equipment-system-port/validation-s31.md`
- `history/full-equipment-system-port/review-report-s31.md`

## Planning Handoff

Proceed to validation/review. S31 does not complete full visual parity; it makes the unresolved subset safe and explicit. Next work should continue reducing or source-backed resolving the remaining `candidate`, `missing-npcres-mapping`, and `missing-resource-resolution` gaps.
