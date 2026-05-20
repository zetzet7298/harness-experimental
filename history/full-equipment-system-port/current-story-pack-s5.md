# Current Story Pack — S5 Formula Ledger

**Feature:** full-equipment-system-port  
**Epic:** E2 Formula, requirements, and combat stat parity  
**Mode:** `high_risk_feature`  
**Prepared after:** S1/S2/S3/S4 foundation review passed and compounding completed on 2026-05-20.

## Story Outcome

Create the evidence-backed formula ledger required before changing/expanding equipment stat parity. The story must reconcile active VHCND formula/constant pivots against H5 implementation and turn the ledger into a fail-fast audit so future S6/S7/S8 work cannot silently use stale constants or fabricated formulas.

## Entry State

- Foundation story has generated a complete slot/table catalog surface and runtime isolation gate.
- `CONTEXT.md` deferred question still unresolved: H5 currently contains `PC_MAX_RESIST = 95`, while active VHCND source evidence under `/var/www/vhcnd/sources/Client/Classes/gamecore/GameDataDef.h:134` shows `MAX_RESIST 150`.
- Current `scripts/vltk-audit-equipment-formula-parity.py` is marker-based and still expects `PC_MAX_RESIST = 95`; it is too weak for S5 because it checks substrings rather than a source-backed ledger.
- Formula work must remain build/audit-time only when reading VHCND; runtime code must not read `/var/www/vhcnd` or symlink out-of-scope roots.

## Source Evidence Already Observed

- `/var/www/vhcnd/sources/Client/Classes/gamecore/KPlayer.h:36-46`
  - `STRENGTH_SET_DAMAGE_VALUE 5`
  - `DEXTERITY_SET_DAMAGE_VALUE 5`
  - base resist max constants are `150` for fire/cold/poison/lightning/physics and `75` for all-base defense.
- `/var/www/vhcnd/sources/Client/Classes/gamecore/GameDataDef.h:134-135`
  - `MAX_RESIST 150`
  - `MAX_BASE_RESIST 75`
- `/var/www/vhcnd/sources/Client/Classes/gamecore/KPlayer.cpp:1075-1121`
  - Active client `SetNpcPhysicsDamage()` adds strength/5 for melee weapons and dexterity/5 for range weapons before `SetPhysicsDamage`.
- `/var/www/vhcnd/sources/SwordOnline/jxOnline/gameserver/Sources/Core/Src/KPlayer.cpp:2859-2877`
  - Server mirror has the same melee strength/5 and range dexterity/5 damage rule.

## Exit State

This story is done only when current repo evidence proves:

1. A source-backed formula ledger exists in `game-source` and lists at minimum:
   - resist cap constants (`MAX_RESIST`, `MAX_BASE_RESIST`, per-channel base resist max),
   - strength/dexterity damage divisors,
   - melee/range hand damage rule,
   - current H5 formula locations for those pivots,
   - status for each pivot: `matched`, `mismatch`, or `unsupported`.
2. `PC_MAX_RESIST` is reconciled to the active VHCND value with evidence, or the story explicitly blocks downstream formula parity with a failing audit. Because active local source says `150`, this story should not keep a passing audit that asserts `95`.
3. `scripts/vltk-audit-equipment-formula-parity.py` reads/validates the ledger rather than only checking loose substrings.
4. H5 formula code/comments and stat audits agree with the ledger for the covered pivots.
5. Validation chain proves no runtime isolation regression.

## Files Likely Touched

- `/var/www/vltk-h5-survivors/game-source/docs/` or `data/vltk-normalized/` for the formula ledger artifact.
- `/var/www/vltk-h5-survivors/game-source/scripts/vltk-audit-equipment-formula-parity.py`
- `/var/www/vltk-h5-survivors/game-source/scripts/vltk-audit-equipment-stat-coverage.py`
- `/var/www/vltk-h5-survivors/game-source/src/domain/equipment.ts`
- `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/equipment-formula-parity.audit.json`
- Targeted property tests if constants/formulas change.
- Harness `history/full-equipment-system-port/validation-report.md` and review notes.

## Feasibility Assumptions To Validate

| Assumption | Risk | Validation proof required |
| --- | --- | --- |
| Active VHCND source for resist cap is the `/var/www/vhcnd/sources/Client/Classes/gamecore` tree, not an older packaged variant. | HIGH | Source path/line evidence in ledger and audit. |
| Changing `PC_MAX_RESIST` from 95 to 150 does not break current PBT unexpectedly. | HIGH | Targeted formula tests + `npm run test:pbt`/`npm run typecheck`. |
| Marker-based audit can be upgraded without requiring full S6/S7/S8 implementation. | MEDIUM | Ledger covers only S5 pivots; unsupported formulas are allowed only if explicitly marked for downstream stories. |
| Runtime isolation remains intact even with VHCND source path citations in docs/data. | HIGH | `npm run check:runtime-isolation`; formula ledger must not live under runtime-served `public/` with absolute source paths. |

## Verification Targets

Execution must expect at least:

- `python3 scripts/vltk-audit-equipment-formula-parity.py`
- `python3 scripts/vltk-audit-equipment-stat-coverage.py`
- `npm run test:pbt`
- `npm run typecheck`
- `npm run check:runtime-isolation`
- `npm run build`

## Out Of Scope For This Story

- Full implementation of every magic attribute key (S6).
- Full equip condition/faction/sex parity (S7).
- Broad loadout equality fixtures for all stats (S8), except targeted fixtures needed to validate the S5 constants.
- Portrait UI/tooltip redesign and visual batch port.
