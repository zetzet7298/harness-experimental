# Current Story Pack — S36 Candidate Visual Preview Batch

**Date:** 2026-05-20
**Feature:** full-equipment-system-port
**Mode:** bounded preview-gate execution
**Source context:** S35 reduced the remaining candidate visual queue to `candidateItemCount=1960` with 113 missing-preview sprite basenames, all still backed by local copied source SPRs. D9 requires preview evidence before any candidate promotion or runtime wiring.

## Story Outcome

Preview-gate another small, already-local high-impact candidate sprite batch (`ma_hb_005_hr01.spr`, `ma_rw_020_hr01.spr`, and the `ma_bd/ma_lh/ma_rh_010_hr01.spr` body trio), record the passed preview report/image, and refresh visual audits without wiring unreviewed visuals.

## Acceptance Criteria

1. A committed S36 packet lists only local VHCND source SPR candidates from the post-S35 actionable queue.
2. Preview report is `status=passed`, renders all packet candidates, and cites local `game-source` source SPR paths only.
3. The candidate and visual-status audits are regenerated so preview-passed sprites are removed from the remaining queue.
4. Tests pin the new remaining candidate count, slot distribution, and local-source availability.
5. Runtime isolation and build remain green; no runtime path reads or symlinks to `/var/www/vhcnd` are introduced.
6. No candidate is composed or wired into runtime visuals without a later explicit promotion story.

## Expected Files / Impact Surface

- `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/port-packets/equipment-visual-candidate-batch-s36.json`
- `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/previews/equipment-visual-candidate-batch-s36.png`
- `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/previews/equipment-visual-candidate-batch-s36.report.json`
- `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/equipment-visual-candidates.audit.json`
- `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/equipment-visual-status.audit.json`
- `/var/www/vltk-h5-survivors/game-source/tests/properties/equipmentVisualCandidates.unit.test.ts`
- `history/full-equipment-system-port/CONTEXT.md`
- `history/full-equipment-system-port/current-story-pack-s36.md`
- `history/full-equipment-system-port/validation-s36.md`
- `history/full-equipment-system-port/review-report-s36.md`

## Planning Handoff

Proceed through validation/review. S36 is evidence-only preview gating; continue reducing the remaining visual candidate queue through preview/local-copy gates before any runtime visual promotion.
