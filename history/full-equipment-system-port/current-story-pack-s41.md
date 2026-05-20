# Current Story Pack — S41 Remaining Candidate Visual Preview Batch

**Date:** 2026-05-20
**Feature:** full-equipment-system-port
**Mode:** bounded preview-gate execution
**Source context:** S40 reduced the remaining candidate visual queue to `candidateItemCount=654` with 80 missing-preview sprite basenames, all still backed by local copied source SPRs. D9 requires preview evidence before any candidate promotion or runtime wiring.

## Story Outcome

Preview-gate all 80 remaining post-S40 actionable local candidate sprite basenames in one explicit packet, record the passed preview report/image with `matched=80` and `rendered=80`, and refresh visual audits so the generic `candidate` bucket is closed without wiring runtime visuals.

## Acceptance Criteria

1. A committed S41 packet lists all remaining local VHCND source SPR candidates from the post-S40 actionable queue.
2. Preview report is `status=passed`, `matched=80`, `rendered=80`, and cites local `game-source` source SPR paths only.
3. The candidate and visual-status audits are regenerated so `candidateItemCount=0` and `missingPreviewSpriteCount=0`.
4. Tests pin the closed candidate queue and local-source availability counters.
5. Runtime isolation and build remain green; no runtime path reads or symlinks to `/var/www/vhcnd` are introduced.
6. No candidate is composed or wired into runtime visuals without a later explicit promotion story.

## Expected Files / Impact Surface

- `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/port-packets/equipment-visual-candidate-batch-s41.json`
- `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/previews/equipment-visual-candidate-batch-s41.png`
- `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/previews/equipment-visual-candidate-batch-s41.report.json`
- `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/equipment-visual-candidates.audit.json`
- `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/equipment-visual-status.audit.json`
- `/var/www/vltk-h5-survivors/game-source/tests/properties/equipmentVisualCandidates.unit.test.ts`
- `history/full-equipment-system-port/CONTEXT.md`
- `history/full-equipment-system-port/current-story-pack-s41.md`
- `history/full-equipment-system-port/validation-s41.md`
- `history/full-equipment-system-port/review-report-s41.md`

## Planning Handoff

Proceed through validation/review. S41 closes the preview-candidate bucket only. Remaining visual coverage gaps are the explicit unresolved buckets: missing local source SPRs, missing NpcRes mapping, and missing resource rows/no fallback.
