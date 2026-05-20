# Validation — S25 Active Equipment Table Precedence

**Date:** 2026-05-20
**Feature:** full-equipment-system-port
**Story:** S25 Active Equipment Table Precedence

## Scope

S25 makes active equipment source-table precedence explicit in generated data and audit-checked before more catalog generation. It also preserves the user-requested D14 inventory interaction refinement that landed in the same worktree: hold/drag vertical continuous scroll, not page-by-page pagination.

## Evidence

- Normalizer regeneration: `python3 scripts/vltk-normalize-equipment-index.py`
  - Result: `wrote data/vltk-normalized/equipment-index.json items=7972 candidates=0`.
- Table inventory audit: `python3 scripts/vltk-audit-equipment-table-inventory.py`
  - Result: `status=pass`, `failures=[]`, `inventoryCount=18`.
  - Every required kind has `sourceResolution.status == selected-first-existing`.
- Focused S25 smoke: `python3 -m unittest discover -s tests -p 'test_vltk_porting_smoke.py' -k table_inventory`
  - Result: 1 test passed.
- Full VLTK smoke file: `python3 -m unittest discover -s tests -p 'test_vltk_porting_smoke.py'`
  - Result: 60 tests passed.
- Equipment scene unit tests for D14 scroll: `npm test -- tests/properties/equipmentScene.unit.test.ts`
  - Result: 25 tests passed.
- TypeScript check: `npm run typecheck`
  - Result: pass.
- Runtime isolation: `npm run check:runtime-isolation`
  - Result: `OK: runtime isolation clean (no /var/www/vhcnd literals and no symlinks under src/ or public/)`.
- Production build: `npm run build`
  - Result: pass. Vite still reports the known large chunk warning.
- Browser validation on `http://localhost:5173` with `agent-browser`:
  - Fresh session had `errors=[]`.
  - Catalog/body slot held 1073 visible candidates; scroll down wrapped to offset 775 and scroll up wrapped to offset 1050.
  - Screenshot: `/tmp/equipment-infinite-scroll-final.png`.
- GitNexus changed-scope review: `detect_changes(repo="vltk-h5-survivors", scope="unstaged")`
  - Result: critical because the whole current diff includes generated catalog/script touch points and EquipmentScene; reviewed as expected S25 + D14 surface.
- GitNexus targeted impact: `impact(target="EquipmentScene", direction="upstream", includeTests=true)`
  - Result: LOW, direct importer `src/game/createGame.ts`, depth-2 `src/main.ts`.

## Acceptance Criteria Mapping

1. Generated table inventory includes precedence chain: satisfied by `equipment-index.summary.json::activeTableInventory[*].sourceResolution.precedence`.
2. Audit verifies selected table is first existing candidate: satisfied by `equipment-table-inventory.audit.json` and focused smoke test.
3. Tests assert active rows come from ServerNew mirror: satisfied by `test_equipment_table_inventory_records_active_servernew_precedence`.
4. `CONTEXT.md` updated: S25 deferred planning checkbox now resolved with precedence rule.
5. Validation commands run: listed above.

## Notes

- S25 did not add new catalog rows beyond deterministic regeneration.
- Runtime still consumes generated/copied game-source artifacts; no runtime direct read from `/var/www/vhcnd` or symlink was introduced.
- D14 scroll work is validated here because it was a direct user clarification in this active goal and touched the same equipment scene.
