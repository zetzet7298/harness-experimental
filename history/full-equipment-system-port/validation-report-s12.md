# Validation Report — S12 Persistence Migration

**Feature:** full-equipment-system-port  
**Mode:** `high_risk_feature`  
**Date:** 2026-05-20  
**Decision:** `READY WITH CONSTRAINTS — CREATE CURRENT-STORY BEADS`

## Reality Gate

S12 is feasible as a focused hardening slice. The current persistence implementation is already slot-order driven, so old/sparse payloads can be accepted without adding a risky migration framework. The gap is proof and stale comments/tests: current tests say "eleven slots" and do not explicitly cover extended-slot save/load cases.

## Feasibility Matrix

| Assumption | Evidence | Result |
| --- | --- | --- |
| The current schema knows all expanded slots. | `EquipmentSlot` and `EQUIPMENT_SLOT_ORDER` both include `mask`, `pifeng`, `yinjian`, `shiping`. | PASS |
| Sparse legacy payloads can be expanded safely. | `emptyLoadout()` initializes every `EQUIPMENT_SLOT_ORDER` entry to `null`; `sanitizeEquipmentState()` only fills valid string ids it sees. | PASS |
| Extended-slot saves are possible without schema redesign. | `saveEquipmentState()` iterates `EQUIPMENT_SLOT_ORDER` and writes any string value, not a fixed legacy allowlist. | PASS |
| The work can be validated without visual/runtime formula changes. | Changes are expected in `equipmentStore` comments/tests; runtime logic should remain unchanged unless tests reveal a gap. | PASS WITH TEST-FIRST CONSTRAINT |

## Required Current-Story Beads

1. **S12A persistence wording cleanup** — update stale "eleven slots" comments/docs in `equipmentStore.ts` and `persistence.unit.test.ts` to current slot-order language.
2. **S12B extended/legacy persistence tests** — add tests for sparse legacy original-slot payloads expanding to 15 slots, valid extended-slot save/load, and extended-slot mismatch rejection.
3. **S12C validation and handoff** — run typecheck, targeted persistence tests, runtime isolation, build, GitNexus detect_changes, update review/compounding docs if pass.

## Execution Constraints

- Prefer test/comment hardening only; do not bump `EQUIPMENT_STATE_VERSION` unless a failing proof requires it.
- Do not seed-merge structurally valid persisted payloads; unknown/missing/invalid slots must remain null per existing Req 10.8 behavior.
- Do not alter equip formulas, catalog generation, or visual asset wiring.
- Do not introduce `/var/www/vhcnd` runtime literals or symlinks.

## Execution Evidence — 2026-05-20

- Implemented S12A wording cleanup in `game-source/src/domain/equipmentStore.ts`, `tests/properties/persistence.unit.test.ts`, and `tests/properties/prop12-persistence-safety.test.ts`: persistence docs now refer to the current `EQUIPMENT_SLOT_ORDER` instead of the stale eleven-slot wording.
- Implemented S12B in `game-source/tests/properties/persistence.unit.test.ts`: added extended-slot test fixtures for `mask`, `pifeng`, `yinjian`, and `shiping`; proved legacy sparse original-slot persisted payloads expand to the current full loadout with extended slots present as `null`; proved valid extended slots sanitize/load/save; proved extended slot/item mismatch still drops the mismatched slot.
- GitNexus impact pre-check: `sanitizeEquipmentState` and `saveEquipmentState` low risk; `loadEquipmentState` critical blast radius because EquipmentScene/offline gateway depend on it. Execution stayed test/comment-only and did not change runtime behavior.
- GitNexus `detect_changes(repo="vltk-h5-survivors", scope="all")`: low risk, changed files limited to persistence tests/comment docs, no affected execution processes.

## Validation Commands

| Check | Result | Evidence |
| --- | --- | --- |
| `npx vitest --run tests/properties/persistence.unit.test.ts` | PASS | 1 file / 33 tests passed during S12B edit loop. |
| `npm run typecheck` | PASS | `tsc --noEmit` completed with exit 0. |
| `npm run test:pbt -- tests/properties/persistence.unit.test.ts` | PASS | 17 property files / 241 tests passed. |
| `npm run check:no-runtime-vhcnd` | PASS | `OK: runtime isolation clean (no /var/www/vhcnd literals and no symlinks under src/ or public/)`. |
| `npm run build` | PASS | Vite build completed; large bundle warning only. |
| Browser smoke on `http://127.0.0.1:5173` | PASS | Screenshot: `/tmp/s12-persistence-smoke.png`; EquipmentScene rendered after persistence test changes; no browser errors. |

## Beads Closed

- `mig-z2s` — S12A persistence wording cleanup.
- `mig-0lj` — S12B extended and legacy persistence tests.
- `mig-t7a` — S12C validation chain for persistence migration.
