# Current Story Pack — S7 Equip Condition Parity

**Feature:** full-equipment-system-port  
**Epic:** E2 Formula, requirements, and combat stat parity  
**Mode:** `high_risk_feature`  
**Prepared after:** S6 magic attribute parity passed, reviewed, compounded, committed, and pushed.

## Story Outcome

Make equipment eligibility/equip-condition behavior source-backed and fail-fast against VHCND `KItemList::CanEquip` / `KItemList::EnoughAttrib`. H5 must not silently allow, deny, or display requirements differently from the active PC source for requirement attributes present in the catalog.

## Entry State

- S6 eliminated catalog `magic_unknown_*` keys for enum-defined VHCND attributes and added `equipment-magic-attribute-parity.audit.json`.
- Current H5 `canEquipItem` supports these requirement keys: `magic_requirelevel`, `magic_requirestr`, `magic_requiredex`, `magic_requirevit`, `magic_requireeng`, `magic_requireseries`, `magic_requiremenpai`, `magic_requiresex`.
- VHCND source evidence shows `KItemList::CanEquip` calls `Fit` first, then iterates `Item[nIdx].GetRequirement(nCount)` and delegates each row to `EnoughAttrib`.
- VHCND `EnoughAttrib` includes additional requirement/prohibition branches not currently represented in H5: `magic_item_nouser`, `magic_item_noseries`, `magic_item_needskill`, `magic_item_needreborn`, `magic_item_needcity`, `magic_item_needbangzhu`, and `magic_item_needtongban`.
- Current `PlayerProfile` has level, sex, series, faction, and base attributes, but no learned-skill, reborn-count, tong/guild, city-owner, or companion-slot state.
- Current label/seed coverage scripts only expect the eight supported requirement keys, so unsupported requirement semantics could remain invisible if new rows appear.

## Source Evidence

- `/var/www/vhcnd/sources/Client/Classes/gamecore/KItemList.cpp:868-893` — `KItemList::CanEquip(int nIdx, int nPlace)` validates equip kind, `Fit`, then every requirement via `EnoughAttrib`.
- `/var/www/vhcnd/sources/Client/Classes/gamecore/KItemList.cpp:917-1040` — `KItemList::EnoughAttrib` source branches for strength, dexterity, vitality, energy, level, faction/menpai, series, sex, prohibited faction/series, need-skill, need-reborn, need-city, need-bangzhu, and need-companion slot.
- `/var/www/vltk-h5-survivors/game-source/src/domain/equipment.ts:315-356` — current H5 `canEquipItem` implementation and unsupported default reason.
- `/var/www/vltk-h5-survivors/game-source/src/domain/equipmentLabels.ts:368-402` — current popup/eligibility requirement labels.
- `/var/www/vltk-h5-survivors/game-source/scripts/vltk-build-equipment-seed.py:138-149` — current seed requirement coverage list.

## Exit State

S7 is done only when current repo evidence proves:

1. A source-backed requirement parity audit exists and enumerates every requirement key observed in `src/data/equipmentCatalog.json`, including source enum id/name when available, catalog count, H5 runtime status, label status, seed coverage status, and explicit unsupported/deferred status.
2. `canEquipItem` behavior matches every supported VHCND `EnoughAttrib` branch that can be represented with current H5 player state.
3. Requirement keys that need missing player state (for example learned skills, reborn count, tong/city ownership, companion slot) are not silently accepted: they either have implemented state-backed checks or are explicit fail-closed unsupported blockers with Vietnamese popup/verdict labels.
4. `formatEquipmentRequirement` and popup text are consistent with `canEquipItem` reasons for all catalog requirement keys.
5. Seed/test coverage includes every reachable catalog requirement key without fabricating items; keys with no catalog evidence are reported separately.
6. Slot mismatch still routes through `item.allowedSlots`/`Fit` parity and ring dual-slot behavior remains intact.
7. Runtime isolation remains clean: no runtime source path reads from `/var/www/vhcnd`, no symlink runtime asset dependency, and no reintroduction of the old PC source name.

## Files Likely Touched

- `/var/www/vltk-h5-survivors/game-source/src/domain/types.ts`
- `/var/www/vltk-h5-survivors/game-source/src/domain/equipment.ts`
- `/var/www/vltk-h5-survivors/game-source/src/domain/equipmentLabels.ts`
- `/var/www/vltk-h5-survivors/game-source/scripts/vltk-build-equipment-seed.py`
- `/var/www/vltk-h5-survivors/game-source/scripts/vltk-audit-equipment-requirement-parity.py`
- `/var/www/vltk-h5-survivors/game-source/scripts/vltk-audit-equipment-seed-coverage.py`
- `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/equipment-requirement-parity.audit.json`
- `/var/www/vltk-h5-survivors/game-source/src/data/inventory.json`
- `/var/www/vltk-h5-survivors/game-source/tests/properties/equipment.unit.test.ts`
- `/var/www/vltk-h5-survivors/game-source/tests/properties/prop05-slot-allowlist.test.ts`

## Feasibility Assumptions To Validate

| Assumption | Risk | Proof Needed |
| --- | --- | --- |
| Catalog currently has only the eight already-supported requirement keys, or otherwise unsupported keys can be surfaced deterministically. | MEDIUM | Requirement audit over generated catalog with counts and source enum names. |
| Fail-closed unsupported checks will not break existing seeded smoke loadouts unexpectedly. | MEDIUM | Seed rebuild + unit/PBT tests; if a seed item becomes unequippable, audit must explain why. |
| Current `PlayerProfile` can support all common gates except skill/reborn/tong/city/companion without schema churn. | MEDIUM | Typecheck + focused tests for level/stat/faction/series/sex/prohibition branches. |
| Label coverage can stay source-backed without inventing unsupported semantics. | LOW | Label audit passes; unsupported labels explicitly say unsupported/blocked. |

## Verification Targets

From `/var/www/vltk-h5-survivors/game-source`:

1. `python3 scripts/vltk-build-equipment-seed.py`
2. `python3 scripts/vltk-audit-equipment-requirement-parity.py`
3. `python3 scripts/vltk-audit-equipment-seed-coverage.py`
4. `python3 scripts/vltk-audit-equipment-label-coverage.py`
5. `python3 scripts/vltk-audit-equipment-stat-coverage.py`
6. `npm run test:pbt`
7. `npm run typecheck`
8. `npm run check:runtime-isolation`
9. `npm run build`

## Out Of Scope For This Story

- Numeric stat-vector equality for all equipment effects (S8), except stats needed to evaluate equip requirements.
- Portrait UI redesign and tooltip layout work (S10), except requirement labels used by existing popup text.
- Visual SPR/resource porting (S11+), except preserving run/out-of-run equipment identity and slot compatibility.
- Implementing full guild/city/companion systems if no H5 state exists; those requirement keys may remain explicit fail-closed blockers for later state stories.

## Bead Mapping

Execution beads are intentionally not created in planning. `khuym:validating` must first run the requirement audit spike/proof and decide whether S7 can proceed as one bounded story or must split into a small state-model spike plus runtime parity bead.
