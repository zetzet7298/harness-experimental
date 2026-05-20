# Current Story Pack — S30 Missing Visual Source Absence Audit

**Date:** 2026-05-20
**Feature:** full-equipment-system-port
**Mode:** bounded investigation / blocker evidence
**Source context:** S29 left 38 dedicated part source SPRs missing from the canonical dynamic parts packet.

## Story Outcome

Prove whether the remaining 38 `MA_HB/MA_HH/MA_HT/MA_HD` run/idle source SPRs are recoverable from `/var/www/vhcnd`. If they are not recoverable, record source-backed absence so future work does not guess visuals or reach into `/var/www/vltkunity`.

## Acceptance Criteria

1. Search is scoped to `/var/www/vhcnd`, not `/var/www/vltkunity`.
2. PAK extraction uses `vltk_extract_tables.py --all-matches` for all 38 missing virtual paths.
3. Exact filename filesystem search under `/var/www/vhcnd` is recorded.
4. A committed audit artifact lists the 38 missing SPRs and the evidence that they are absent.
5. `CONTEXT.md` records that the next step is fallback/unresolved-row design, not guessed visual synthesis.
6. Runtime isolation remains green.

## Expected Files / Impact Surface

- `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/equipment-visual-missing-sources.audit.json`
- `history/full-equipment-system-port/CONTEXT.md`
- `history/full-equipment-system-port/current-story-pack-s30.md`
- `history/full-equipment-system-port/validation-s30.md`
- `history/full-equipment-system-port/review-report-s30.md`

## Planning Handoff

Proceed to validation/review. S30 is a blocker-evidence story: it does not close visual parity, but it prevents unsafe guesses and defines the next required decision point.
