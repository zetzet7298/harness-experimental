# Current Story Pack — S42 PiFeng Missing NpcRes Row Audit Hardening

**Date:** 2026-05-20
**Feature:** full-equipment-system-port
**Mode:** bounded audit/test hardening
**Source context:** After PiFeng resource mapping, current visual status reports `missing-local-source-spr=204`, `missing-npcres-mapping=6276`, `missing-npcres-row=6`, and `missing-resource-row-no-fallback=82`. The six `missing-npcres-row` entries are PiFeng rows whose `item/PiFengRes.txt` values point beyond the available male/female PiFeng NpcRes tables.

## Story Outcome

Make the six PiFeng out-of-range NpcRes rows first-class unresolved visual gaps in generated audit output and tests, so later agents cannot accidentally treat the catalog as complete or synthesize/guess cloak visuals.

## Acceptance Criteria

1. `equipment-visual-status.audit.json` exposes `coverageQuantification.catalogItems.missingNpcResRows=6`.
2. The visual status audit `status` remains `incomplete` until all unresolved visual buckets are zero, including missing local source SPRs, missing NpcRes mapping, missing NpcRes rows, and no-fallback resource rows.
3. Property tests prove the six rows are PiFeng, qualities normal/magic, `tableValue` 12/13/14 pairs, with no `candidateSprite` or `resolvedSprites`.
4. Smoke test expectations match the current generated visual audit counts.
5. Runtime isolation and production build stay green.

## Evidence

- Game-source commit: `36d54a9 test(equipment): audit unresolved pifeng npcres rows`.
- `npm run test:pbt`: 22 files / 251 tests passed.
- `python3 tests/test_vltk_porting_smoke.py -k test_equipment_visual_status_audit_quantifies_current_catalog_safety`: passed.
- `npm run build`: passed; runtime isolation prebuild check passed.
- GitNexus `detect_changes(scope="all")`: LOW risk, no affected processes.

## Remaining Gap

S42 is audit hardening only. Full visual coverage remains incomplete until the unresolved buckets are actually resolved or source-backed no-fallback decisions are accepted: `missing-local-source-spr=204`, `missing-npcres-mapping=6276`, `missing-npcres-row=6`, and `missing-resource-row-no-fallback=82`.
