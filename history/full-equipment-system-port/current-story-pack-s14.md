# Current Story Pack — S14 Visual Manifest Coverage Audit

**Feature:** full-equipment-system-port  
**Epic:** E4 Equipped visual parity pipeline  
**Mode:** `high_risk_feature`  
**Prepared after:** S13 review/compounding passed and pushed.

## Story Outcome

Make equipment visual coverage measurable and safe at catalog scale. The repo must report how many current catalog items are preview-passed/resolved, missing resource resolution, or missing NpcRes mapping; it must fail if any catalog row exposes runtime visual sprites without passed preview evidence and repo-local source copies.

## Entry State

- S13 repaired the smoke loadout only: three catalog rows now have `visual.resolvedSprites` with passed preview evidence and local copied SPRs.
- The current catalog has 9552 items, but only 3 rows expose resolved character visual sprites.
- Existing `equipment-visual-coverage.audit.json` focuses on sample/loadout coverage and no longer quantifies the full catalog visual status distribution.
- `tests/test_vltk_porting_smoke.py` still contains stale assertions from the older 1231-row catalog and stale 136500-combination visual plan; this weakens future validation because the Python smoke file no longer matches current generated data.

## Acceptance Criteria

1. A deterministic visual-status audit exists and writes `data/vltk-normalized/equipment-visual-status.audit.json`.
2. The audit reports current catalog counts by `candidateStatus`/resolution status, slot, and quality.
3. The audit fails by default when a catalog row has `candidateSprite`/`resolvedSprites` without passed preview evidence for every basename.
4. Passed/resolved visual rows also require local source SPR files under `public/assets/character/vhcnd/source/`; no symlink or direct runtime VHCND path is allowed.
5. Python smoke tests are repaired so they assert catalog-driven invariants for the current 9552-row catalog instead of stale fixed counts.
6. Validation passes: visual-status audit, existing visual coverage/part audits, Python smoke test file, runtime isolation, typecheck/build, and targeted browser proof only if runtime visual wiring changes.

## Non-Goals

- Do not batch-port all remaining missing visual rows in S14.
- Do not mark missing NpcRes/resource rows as failures unless they are wired/resolved unsafely.
- Do not add symlinks or runtime reads from `/var/www/vhcnd`.

## Execution Evidence — 2026-05-20

- Added `scripts/vltk-audit-equipment-visual-status.py` and `data/vltk-normalized/equipment-visual-status.audit.json`.
- Current visual status distribution is 9552 total items: 6304 `missing-npcres-mapping`, 3245 `missing-resource-resolution`, and 3 `preview-passed-loadout-evidence` rows.
- Unsafe resolved visual rows: `0`; every resolved basename has passed preview evidence and local copied source SPRs, with no symlink sources.
- Repaired `tests/test_vltk_porting_smoke.py` so Python smoke assertions match the current expanded 9552-row catalog and new visual-status audit.
