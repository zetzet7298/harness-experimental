# Validation — S15 In-Run Resolver Parity

**Date:** 2026-05-20  
**Feature:** full-equipment-system-port  
**Story:** `current-story-pack-s15.md`  
**Result:** FEASIBLE — execution may proceed with a small runtime/test bead.

## Reality Gate

- `GameScene.loadEquipmentVisuals()` already tries resolver paths in the required order: whole-loadout manifest → layered parts → unresolved audit/report → hard fallback when report write fails.
- `src/game/visualResolver.ts` already performs the pure whole-loadout gate: only `status === 'passed-generated'` and exact run/idle SPR basename set equality can select a manifest entry.
- Current manifest includes a matching `passed-generated` entry for the canonical smoke loadout: `equipped-tu-la-giang-sa-staff-phien-vu` with the expected run/idle basenames including `ma_hd_010`, `ma_bd_034`, `ma_lh_034`, `ma_rh_034`, `ma_rw_026`, and horse parts.
- Current browser smoke enters `GameScene` and screenshots the canvas, but no explicit resolver status/debug seam exists (`equipmentVisualDebug`, `visualResolverStatus`, `selectedPath` searches returned 0 matches). Tests can inspect private texture keys only indirectly, which is too weak for S15 AC2/AC3.

## Validation Commands Run

From `/var/www/vltk-h5-survivors/game-source`:

- `python3 scripts/vltk-audit-equipment-visual-status.py` — pass; 9552 catalog rows, 3 resolved visual rows, 0 unsafe resolved rows.
- `python3 scripts/vltk-audit-equipment-visual-coverage.py` — pass; canonical smoke loadout complete, no unresolved combinations.
- `python3 scripts/vltk-audit-equipment-visual-part-coverage.py` — pass; dynamic layered parts complete, 0 missing run/idle part sheets, runtime dynamic layering markers present.
- `npm run check:no-runtime-vhcnd` — pass; no `/var/www/vhcnd` runtime literals and no symlinks under `src/` or `public/`.
- `npm run typecheck` — pass.
- `npm run test:pbt` — pass; 17 files / 241 tests.

## Feasibility Answers

1. **Current resolver path observability:** not sufficient. There is no explicit status object for tests; S15 needs a non-user-facing getter/status field.
2. **Expected smoke path:** browser proof showed the current 3-piece seed selects `parts`, not `manifest`, because no horse is equipped in the seed while the closest whole-loadout manifest includes horse parts. This is acceptable for S15 because visual part coverage is complete and preview-backed; the strengthened smoke must fail only on audit/hard fallback or wrong basenames.
3. **Smallest seam:** add a debug/status snapshot in `GameScene` that records equipped item ids, run/idle basenames, selected path, selected manifest id or part filenames, and fallback reason. Expose via a method for Playwright/tests only; do not render to UI.
4. **Coverage gap:** current property tests cover pure gate ordering and fallback harness, but not the actual `GameScene` runtime status nor smoke failure on fallback. Strengthen unit/smoke tests.
5. **User-facing text check:** feasible in browser by reading visible canvas-independent DOM text is limited because most UI is canvas. For S15, ensure no new visible text is introduced; a broader canvas OCR/UI text gate belongs to a later UI story.

## Approved Execution Surface

Create one execution bead for S15:

- Add resolver status/debug snapshot in `GameScene`.
- Assert the canonical Playwright smoke sees `selectedPath === 'parts'`, expected equipped ids, exact run/idle basename sets, expected part filenames, and no audit/hard fallback.
- Add/extend property tests around resolver status/fallback behavior where practical.
- Re-run audits, typecheck, property tests, runtime isolation, and Playwright smoke on port 5173.

## Blockers

None. Execution can proceed.
