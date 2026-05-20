# Current Story Pack — S35 Candidate Visual Preview Batch

**Date:** 2026-05-20
**Feature:** full-equipment-system-port
**Mode:** bounded preview-gate execution
**Source context:** S34 quantified `candidateItemCount=2566` with 117 missing-preview sprite basenames and proved all had local copied source SPRs. D9 requires preview evidence before any candidate promotion or runtime wiring.

## Story Outcome

Preview-gate a small, already-local candidate sprite batch (`ma_hd_007_hr01.spr` plus the `ma_bd/ma_lh/ma_rh_007_hr01.spr` body trio), record the passed preview report/image, and refresh the remaining-candidate audit without wiring unreviewed visuals.

## Acceptance Criteria

1. A committed S35 packet lists only local VHCND source SPR candidates from the S34 actionable queue.
2. Preview report is `status=passed`, renders all packet candidates, and cites local `game-source` source SPR paths only.
3. The candidate audit is regenerated so preview-passed sprites are removed from the remaining queue.
4. Tests pin the new remaining candidate count, slot distribution, and local-source availability.
5. Runtime isolation remains green; no runtime path reads or symlinks to `/var/www/vhcnd` are introduced.
6. D14 remains locked: equipment browsing uses hold/drag continuous/infinite-feeling scroll, not pagination.

## Expected Files / Impact Surface

- `/var/www/vltk-h5-survivors/game-source/scripts/vltk-preview-candidates.py`
- `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/port-packets/equipment-visual-candidate-batch-s35.json`
- `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/previews/equipment-visual-candidate-batch-s35.png`
- `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/previews/equipment-visual-candidate-batch-s35.report.json`
- `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/equipment-visual-candidates.audit.json`
- `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/equipment-visual-status.audit.json`
- `/var/www/vltk-h5-survivors/game-source/tests/properties/equipmentVisualCandidates.unit.test.ts`
- `history/full-equipment-system-port/CONTEXT.md`
- `history/full-equipment-system-port/current-story-pack-s35.md`
- `history/full-equipment-system-port/validation-s35.md`
- `history/full-equipment-system-port/review-report-s35.md`

## Planning Handoff

Proceed through validation/review. S35 is evidence-only preview gating: do not compose or wire runtime equipment visuals from this batch until a later story explicitly promotes passed preview evidence through the parts-export/runtime manifest gate.
