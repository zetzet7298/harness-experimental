# Current Story Pack — S29 Canonical Parts Source Report Repair

**Date:** 2026-05-20
**Feature:** full-equipment-system-port
**Mode:** small validation/repair slice
**Source context:** S28 revealed that the canonical `equipment-visual-parts-all` source folder contained 284 local copied SPRs, but its `required-sprs.report.json` still counted rerun-satisfied local files as missing.

## Story Outcome

Make the required-SPR extraction report rerunnable and truthful: existing non-symlinked local copied SPRs inside the destination folder must satisfy the source-copy gate, so the report matches the dynamic part coverage audit.

## Acceptance Criteria

1. `vltk-extract-required-sprs.py` treats an already-local destination SPR as copied/satisfied on rerun.
2. `public/assets/character/vhcnd/source/equipment-visual-parts-all/required-sprs.report.json` reports `required=322`, `copied=284`, `missing=38`.
3. The remaining 38 missing entries match the dedicated part asset gap and are not hidden.
4. Runtime isolation and equipment scene tests remain green.
5. Production build remains green.

## Expected Files / Impact Surface

- `/var/www/vltk-h5-survivors/game-source/scripts/vltk-extract-required-sprs.py`
- `/var/www/vltk-h5-survivors/game-source/public/assets/character/vhcnd/source/equipment-visual-parts-all/required-sprs.report.json`
- `history/full-equipment-system-port/current-story-pack-s29.md`
- `history/full-equipment-system-port/validation-s29.md`
- `history/full-equipment-system-port/review-report-s29.md`

## Planning Handoff

Proceed to validation/review. S29 is a report truthfulness repair, not a visual coverage expansion; next work still needs to resolve the 38 missing source SPRs or document why VHCND lacks them.
