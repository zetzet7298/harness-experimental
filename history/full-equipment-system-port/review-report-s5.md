# Review Report — S5 Formula Ledger

**Feature:** full-equipment-system-port  
**Date:** 2026-05-20  
**Phase:** `khuym:reviewing`  
**Decision:** PASS

## What Changed

- Added source-backed formula ledger: `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/equipment-formula-ledger.json`.
- Reconciled H5 `PC_MAX_RESIST` from stale `95` to active VHCND `MAX_RESIST = 150`.
- Added `PC_RESIST_CAP_LEDGER` in `src/domain/equipment.ts` for S5 resist-cap pivots:
  - `maxResist: 150`
  - `maxBaseResist: 75`
  - per-channel base resist max values: `150`
- Replaced loose marker-only formula audit with ledger-backed validation in `scripts/vltk-audit-equipment-formula-parity.py`.
- Updated stat audit and PBT/unit tests to agree with the active VHCND cap. The tests now explicitly allow the raw PC attenuation helper to produce negative output for resist values above 100 when the cap is 150; no artificial clamp was added without a source pivot.

## Source Evidence

- VHCND `sources/Client/Classes/gamecore/GameDataDef.h:134-135`: `MAX_RESIST 150`, `MAX_BASE_RESIST 75`.
- VHCND `sources/Client/Classes/gamecore/KPlayer.h:36-46`: strength/dexterity divisors are `5`, per-channel base resist caps are `150`, all-base defense cap is `75`.
- VHCND `sources/Client/Classes/gamecore/KPlayer.cpp:1075-1121`: client active `SetNpcPhysicsDamage()` uses strength/5 for melee and dexterity/5 for range.
- VHCND `SwordOnline/jxOnline/gameserver/Sources/Core/Src/KPlayer.cpp:2859-2877`: server mirror has the same melee/range damage divisor rule.

## Validation Commands

From `/var/www/vltk-h5-survivors/game-source`:

1. `python3 scripts/vltk-audit-equipment-formula-parity.py` ✅
2. `python3 scripts/vltk-audit-equipment-stat-coverage.py` ✅
3. `npm run test:pbt` ✅ (`17 files`, `225 tests`)
4. `npm run typecheck` ✅
5. `npm run check:runtime-isolation` ✅
6. `npm run build` ✅

## Review Notes

- S5 does not claim full S6/S7/S8 parity. It creates the fail-fast source ledger needed before those stories.
- The ledger lives under `data/vltk-normalized`, not `public`, so absolute VHCND paths remain build/audit evidence and are not runtime-served assets.
- `src/` comments avoid absolute `/var/www/vhcnd` literals so the reusable runtime isolation gate remains green.
