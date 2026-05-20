# Validation — S23 Resist Cap Evidence Reconciliation

**Date:** 2026-05-20  
**Feature:** full-equipment-system-port  
**Story:** `current-story-pack-s23.md`  
**Result:** PASS

## Evidence

VHCND active client source:

- `/var/www/vhcnd/sources/Client/Classes/gamecore/GameDataDef.h:134`:
  - `#define MAX_RESIST 150`
  - This is the authoritative active source for the global H5 `PC_MAX_RESIST` mirror.

H5 source/test state:

- `/var/www/vltk-h5-survivors/game-source/src/domain/equipment.ts` exports `PC_MAX_RESIST = 150`.
- `tests/properties/equipment.unit.test.ts` asserts `PC_MAX_RESIST` is `150`.
- `tests/properties/prop03-resist-cap.test.ts` covers global cap behavior including resist values greater than `150`.
- Stale comments that claimed active `MAX_RESIST = 95` were repaired. Remaining `95` references are per-call `resistMax = 95` examples, not global cap claims.

## Commands / Results

From `/var/www/vltk-h5-survivors/game-source`:

```bash
npm test -- tests/properties/equipment.unit.test.ts tests/properties/prop03-resist-cap.test.ts
python3 tests/test_vltk_porting_smoke.py
rg -n "MAX_RESIST\\s*=\\s*95|MAX_RESIST 95|PC_MAX_RESIST\\s*=\\s*95|GameDataDef\\.h:128" src tests scripts docs data || true
```

Results:

- Targeted Vitest: `2 passed`, `90 tests passed`.
- Python smoke: `Ran 59 tests`, `OK`.
- Stale global-cap scan: no matches.

GitNexus:

- `detect_changes(repo="vltk-h5-survivors", scope="all")` — `risk_level: low`, `changed_files: 1`, `changed_symbols: 0`.

## Context Update

`CONTEXT.md` deferred planning item for `PC_MAX_RESIST` reconciliation is now checked. The resolved rule is:

- Global PC cap: `PC_MAX_RESIST = 150` from active VHCND `GameDataDef.h:134`.
- Per-call cap examples like `resistMax = 95` are valid tighter override tests and must not be mistaken for the global cap.
