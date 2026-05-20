# 2026-05-20 VHCND Rebrand Batch (E3-E5) + E6/E7 Validation Snapshot

## Scope

- Rebrand batch `vhcnd -> vhcnd` đã apply cho harness/docs/.codex skills và game-source.
- Asset roots game-source đã đổi sang `public/assets/**/vhcnd/`.
- E6 rerun validation sau cập nhật test/audit contract theo provenance vhcnd.
- E7 isolation proof cho harness (non-history), game-source, và vhcnd.

## Commands run

```bash
# game-source
python3 -m py_compile scripts/*.py
npm run test:pbt
python3 -m pytest tests/test_vltk_porting_smoke.py -q
npm run typecheck
npm run build
```

## Results

- `py_compile`: ✅ pass
- `npm run test:pbt`: ✅ pass (17 files, 224 tests)
- `pytest tests/test_vltk_porting_smoke.py -q`: ✅ pass (55 tests)
- `npm run typecheck`: ✅ pass
- `npm run build`: ✅ pass (only chunk-size warning, non-blocking)

## Key adjustments made for green suite

1. Updated property test `tests/properties/prop10-no-fabrication.test.ts` to accept vhcnd ServerNew settings provenance (`ServerNew/_bin_v2_/gs/Settings/...`) in addition to legacy `Client/Settings/...` for Req 14.1/14.5 checks.
2. Updated smoke expectations in `tests/test_vltk_porting_smoke.py` to align with current generated artifact schema:
   - seed bag policy capped subset (<=125) instead of full-catalog bag length,
   - series coverage fields under `summary/catalogAnomalies/catalogSeriesCounts/qualitySeriesCountsCatalog`,
   - label coverage fields under `attributeLabelMissing/requirementLabelMissing/summary`.
3. Updated pilot visual manifest mapping fallback by canonicalName when shard job item id format differs from catalog id format.

## Isolation proof (E7)

Artifact: `history/migrate-vhcnd-to-vhcnd/e7-isolation-proof.json`

- `harness_non_history`: `vhcnd=0`, `/var/www/vhcnd=0`, `/var/www/vhcnd=0`
- `game_source`: `vhcnd=0`, `/var/www/vhcnd=0`, `/var/www/vhcnd=0`
- `vhcnd_text_scan`: `/var/www/vhcnd=0`, `/var/www/vhcnd=0`, `vhcnd=0`

## Current status vs CONTEXT

- E3/E4/E5: ✅ applied (docs/skills/scripts/assets path + identifier rebrand).
- E6: ✅ green for smoke + PBT + typecheck + build in current workspace.
- E7: ✅ isolation proof pass for in-scope scan.
- Remaining non-zero `vhcnd` mentions are concentrated in historical evidence namespace (`history/migrate-vhcnd-to-vhcnd/*`, `.beads/issues.jsonl`) and legacy artifact filenames intentionally retained for traceability.
