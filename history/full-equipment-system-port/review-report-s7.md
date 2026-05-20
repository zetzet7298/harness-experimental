# Review Report — S7 Equip Condition Parity

**Feature:** full-equipment-system-port  
**Date:** 2026-05-20  
**Decision:** PASS for S7 requirement parity slice

## What Changed

- Added source-backed requirement parity audit:
  - `scripts/vltk-audit-equipment-requirement-parity.py`
  - `data/vltk-normalized/equipment-requirement-parity.audit.json`
- Runtime `canEquipItem` now handles the full known VHCND `EnoughAttrib` requirement surface available to current H5 state:
  - Existing supported: level, str, dex, vit, eng, series, faction, sex.
  - Newly source-backed: prohibited faction (`magic_item_nouser`) and prohibited series (`magic_item_noseries`).
  - Newly fail-closed: need skill, reborn, city owner, bangzhu, companion slot.
- Labels now cover all observed catalog attributes and requirements, including previously missing `magic_item_needreborn` and `magic_item_needtongban`.
- Seed coverage now includes representative items for `magic_item_needreborn` and `magic_item_needtongban` while keeping one-cell mobile bag policy and the 125-item cap.
- Added unit coverage for fail-closed reborn/companion requirements, prohibited faction/series gates, and VHCND requirement labels.

## Validation Commands

From `/var/www/vltk-h5-survivors/game-source`:

1. `python3 scripts/vltk-build-equipment-seed.py` ✅
2. `python3 scripts/vltk-audit-equipment-requirement-parity.py` ✅
3. `python3 scripts/vltk-audit-equipment-seed-coverage.py` ✅
4. `python3 scripts/vltk-audit-equipment-label-coverage.py` ✅
5. `python3 scripts/vltk-audit-equipment-stat-coverage.py` ✅
6. `npm run test:pbt` ✅ (`17` files, `230` tests)
7. `npm run typecheck` ✅
8. `npm run check:runtime-isolation` ✅
9. `npm run build` ✅

## Remaining Parity Blockers

S7 does not implement full learned-skill, reborn, city/tong, or companion systems. Current behavior is intentionally fail-closed for those requirement keys until those player-state systems are ported. The next E2 story should move to broader stat-vector parity (S8) unless planning finds a stricter prerequisite.


## S7D Follow-up Review

PASS. Completion audit found and fixed one S7 gap: `magic_item_nouser` can be emitted as a magic/base attribute, so `canEquipItem` now evaluates requirement-like attributes in addition to explicit `requirements`. The magic attribute parity audit now classifies `magic_item_nouser` as implemented instead of unsupported, and PBT increased to 231 tests.
