# Current Story Pack — S34 Candidate Visual Preview Queue Audit

**Date:** 2026-05-20
**Feature:** full-equipment-system-port
**Mode:** bounded candidate-queue audit
**Source context:** After S33, visual-status audit still has `candidate=2566`. These rows are not wired yet because they need preview evidence.

## Story Outcome

Turn the remaining candidate bucket into an actionable preview queue: count candidate rows by slot/quality, group missing-preview SPR basenames, and prove whether local copied source SPRs already exist for those preview candidates.

## Acceptance Criteria

1. A committed audit artifact reports remaining candidate rows and missing-preview sprite groups.
2. Audit proves whether candidate sprites already have local copied source SPRs.
3. Tests pin the candidate count, slot distribution, and local-source availability.
4. Runtime isolation and build remain green.
5. No candidate is promoted or wired without preview evidence.

## Expected Files / Impact Surface

- `/var/www/vltk-h5-survivors/game-source/scripts/vltk-audit-equipment-visual-candidates.py`
- `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/equipment-visual-candidates.audit.json`
- `/var/www/vltk-h5-survivors/game-source/tests/properties/equipmentVisualCandidates.unit.test.ts`
- `history/full-equipment-system-port/CONTEXT.md`
- `history/full-equipment-system-port/current-story-pack-s34.md`
- `history/full-equipment-system-port/validation-s34.md`
- `history/full-equipment-system-port/review-report-s34.md`

## Planning Handoff

Proceed to validation/review. S34 is an audit/prioritization slice; next work should run preview gates for selected already-local candidate sprites and only promote passed evidence.
