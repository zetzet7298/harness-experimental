# Validation — S21 Equipment Visual Batch Preflight Repair

**Date:** 2026-05-20
**Feature:** full-equipment-system-port
**Story:** `current-story-pack-s21.md`
**Result:** PASS

## Changes Validated

- `scripts/vltk-build-equipped-loadout-packet.py`
  - Added `--clear-slot <slot>`.
  - `apply_equip_overrides()` can remove a seed slot before applying explicit overrides.
- `scripts/vltk-build-equipment-visual-shard-jobs.py`
  - Handles empty representative lists without `IndexError`.
  - Emits `omittedSlots` and `--clear-slot <slot>` for empty visual slots.
- `tests/test_vltk_porting_smoke.py`
  - Updated stale popup assertions to centered-popup S16 contract.
  - Added tests for empty-slot shard jobs and clear-slot packet behavior.

## Commands / Evidence

From `/var/www/vltk-h5-survivors/game-source`:

```bash
python3 scripts/vltk-plan-equipment-visual-build.py --out /tmp/s21-equipment-visual-build-plan.json --shards 8
python3 scripts/vltk-build-equipment-visual-shard-jobs.py --plan /tmp/s21-equipment-visual-build-plan.json --out-dir /tmp/s21-equipment-visual-jobs --shard 0
python3 scripts/vltk-run-equipment-visual-shard.py --jobs /tmp/s21-equipment-visual-jobs/shard-000.json --dry-run --limit 1 --summary-out /tmp/s21-equipment-visual-dry-run.json
python3 scripts/vltk-build-equipment-visual-shard-jobs.py --out-dir /tmp/s21-existing-jobs --shard 0
python3 scripts/vltk-run-equipment-visual-shard.py --jobs /tmp/s21-existing-jobs/shard-000.json --dry-run --limit 1 --summary-out /tmp/s21-existing-dry-run.json
python3 tests/test_vltk_porting_smoke.py
npm run typecheck
npm run test:pbt
npm run check:no-runtime-vhcnd
npm run build
```

GitNexus:

- `impact(build_job)` — LOW, direct caller `build_jobs`, process `main`.
- `impact(apply_equip_overrides)` — LOW, direct caller `main`.
- `detect_changes(repo="vltk-h5-survivors", scope="all")` — MEDIUM; affected scripts are the expected visual shard/loadout tooling plus smoke tests.

## Results

- Fresh current-catalog visual plan reported `horse: 0`, `weapon: 1`, `body: 1`, `head: 1`, `totalUniqueVisualCombinations: 1`; shard job generation no longer crashed.
- Fresh-plan dry run completed `1/1` job with `failedJobCount: 0`.
- Existing tracked build plan generated shard `0` with `4266` jobs; dry run completed `1/1` job with `failedJobCount: 0`.
- `python3 tests/test_vltk_porting_smoke.py` — `Ran 58 tests`, `OK`.
- `npm run typecheck` — passed.
- `npm run test:pbt` — `17 passed (17)` files, `239 passed (239)` tests.
- `npm run check:no-runtime-vhcnd` — passed.
- `npm run build` — passed with the existing non-blocking bundle-size warning.

## Remaining Gap

S21 repairs the batch preflight path only. Full equipment visual coverage remains incomplete and must be expanded through future preview-reviewed shards; no new previews were marked passed and no runtime sheets were composed/wired in this story.
