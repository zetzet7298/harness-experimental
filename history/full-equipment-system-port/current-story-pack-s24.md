# Current Story Pack — S24 Visual Coverage Quantification

**Date:** 2026-05-20  
**Feature:** full-equipment-system-port  
**Mode:** small audit/reporting slice  
**Source context:** `CONTEXT.md` deferred planning item: quantify visual coverage statuses and copied local sources.

## Story Outcome

Make the visual coverage state explicit and machine-checkable: how many catalog items are missing NpcRes mapping, missing resource resolution, candidate, preview-passed, and how many local source SPR copies/runtime manifest entries exist. Use that evidence to close the visual-coverage quantification deferred item without claiming full visual parity.

## Entry State

- `data/vltk-normalized/equipment-visual-status.audit.json` already tracks status counts and unsafe resolved visuals.
- S22 increased runtime manifest entries to 9 and added one no-horse smoke loadout.
- `CONTEXT.md` still has an unchecked item asking to quantify visual coverage.

## Acceptance Criteria

1. The visual status audit includes a concise `coverageQuantification` object with the requested counts.
2. Tests assert the quantification matches the current generated catalog and remains safe (`unsafeResolvedVisualItemCount = 0`).
3. `CONTEXT.md` is updated with current S24 counts and remains clear that full visual coverage is incomplete.
4. Validation includes audit regeneration, Python smoke, runtime isolation, and GitNexus changed-scope review.

## Non-Goals

- Do not resolve new NpcRes mappings in this story.
- Do not compose or preview more runtime visuals.
- Do not claim full visual parity.

## Expected Files / Impact Surface

- `/var/www/vltk-h5-survivors/game-source/scripts/vltk-audit-equipment-visual-status.py`
- `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/equipment-visual-status.audit.json`
- `/var/www/vltk-h5-survivors/game-source/tests/test_vltk_porting_smoke.py`
- `history/full-equipment-system-port/CONTEXT.md`
- `history/full-equipment-system-port/validation-s24.md`
- `history/full-equipment-system-port/review-report-s24.md`

## Planning Handoff

Proceed directly to repair/validation. This is an audit clarity slice, not a runtime visual expansion slice.
