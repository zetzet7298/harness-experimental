# Current Story Pack — S8 Stat Vector Fixtures and Internal Magic Damage

**Feature:** full-equipment-system-port  
**Epic:** E2 Formula, requirements, and combat stat parity  
**Mode:** `high_risk_feature`  
**Prepared after:** S7 equip condition parity passed, reviewed, compounded, and pushed.

## Story Outcome

Reduce the largest remaining S6/S7 runtime stat-parity gap by porting source-backed internal magic damage equipment attributes and adding deterministic stat-vector fixtures. H5 must prove representative equipment loadouts produce expected HP, mana, lực tay/physical damage, resists, and elemental/internal damage fields from VHCND evidence without fabricating unsupported systems.

## Entry State

- S5 formula ledger proved constants/formula pivots for resist caps, weapon damage divisors, and damage attenuation.
- S6 audit classifies 59 catalog attribute keys: after S7D, 24 implemented and 35 explicit unsupported/deferred.
- S7 added requirement parity and fail-closed equip-condition handling, including requirement-like magic attributes such as `magic_item_nouser`.
- Largest remaining numeric-combat unsupported group by source-backed catalog count is `internal-magic-damage-story-s8`: six keys, 355 catalog rows:
  - `magic_addphysicsmagic_v` — 153 rows
  - `magic_addphysicsmagic_p` — 157 rows
  - `magic_addfiremagic_v` — 12 rows
  - `magic_addcoldmagic_v` — 9 rows
  - `magic_addlightingmagic_v` — 12 rows
  - `magic_addpoisonmagic_v` — 12 rows
- Current `CharacterStats` has external additive elemental fields (`fireDamage`, `coldDamage`, `lightningDamage`, `poisonDamage`) and min/max placeholders, but no explicit internal magic damage vector.
- Current stat tests cover edge cases but not generated catalog fixtures asserting complete stat vectors for representative source rows.

## Source Evidence

- `/var/www/vhcnd/sources/Client/Classes/gamecore/KNpcAttribModify.cpp:2528-2534` — `AddPhysicsMagic` adds `nValue[0]` to current physics magic min and max.
- `/var/www/vhcnd/sources/Client/Classes/gamecore/KNpcAttribModify.cpp:2536-2546` — `Add_neiphysicsenhance_p` adds percent magic physical min/max and normalizes negative ranges.
- `/var/www/vhcnd/sources/Client/Classes/gamecore/KNpcAttribModify.cpp:2556-2570` — `AddColdMagic` adds cold magic min/max and sets normal cold time when positive.
- `/var/www/vhcnd/sources/Client/Classes/gamecore/KNpcAttribModify.cpp:2573-2586` — `AddFireMagic` adds fire magic min/max and normalizes negative ranges.
- `/var/www/vhcnd/sources/Client/Classes/gamecore/KNpcAttribModify.cpp:2588-2599` — `AddLightingMagic` adds lightning magic min/max and normalizes negative ranges.
- `/var/www/vhcnd/sources/Client/Classes/gamecore/KNpcAttribModify.cpp:2601-2619` — `AddPoisonMagic` adds poison magic value and sets duration/interval when positive.
- `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/equipment-magic-attribute-parity.audit.json` — source-backed unsupported counts and blocker categories.
- `/var/www/vltk-h5-survivors/game-source/src/domain/equipment.ts` — current stat aggregation and unsupported attribute dispatcher.

## Exit State

S8 is done only when current repo evidence proves:

1. `CharacterStats` has source-backed fields for internal magic damage values needed by the six `internal-magic-damage-story-s8` keys.
2. `applyAttribute` implements those six keys from source evidence and no longer reports them as unsupported in `equipment-magic-attribute-parity.audit.json`.
3. Deterministic stat-vector fixtures exist for representative source-backed normal/magic/gold loadouts or synthetic source-cited items, proving HP, mana, physical/hand damage, resists, and internal magic damage fields together.
4. Existing formula/stat/label/seed audits remain green and runtime isolation remains clean.
5. Any still-unsupported semantics from S6 remain explicit blockers with counts; S8 must not claim full stat parity if other groups remain deferred.
6. No runtime code reads `/var/www/vhcnd` and no runtime asset/code uses symlinks to out-of-scope roots.

## Files Likely Touched

- `/var/www/vltk-h5-survivors/game-source/src/domain/types.ts`
- `/var/www/vltk-h5-survivors/game-source/src/domain/equipment.ts`
- `/var/www/vltk-h5-survivors/game-source/tests/properties/equipment.unit.test.ts`
- `/var/www/vltk-h5-survivors/game-source/tests/properties/equipment-stat-vector-fixtures.test.ts` or equivalent
- `/var/www/vltk-h5-survivors/game-source/scripts/vltk-audit-equipment-magic-attribute-parity.py`
- `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/equipment-magic-attribute-parity.audit.json`
- `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/equipment-stat-coverage.audit.json`

## Feasibility Assumptions To Validate

| Assumption | Risk | Proof Needed |
| --- | --- | --- |
| Internal magic damage can be represented as additive min/max or scalar fields without breaking existing external skill damage semantics. | MEDIUM | Focused tests and no regressions in `resolveSkillDamageBreakdown` tests. |
| The six S8 keys use only `nValue[0]` for positive catalog rows, so deterministic catalog values can be applied without RNG. | MEDIUM | Audit/probe examples from generated catalog plus source lines. |
| Stat-vector fixtures can be source-backed without needing a full PC executable oracle. | MEDIUM | Fixtures cite VHCND source formulas and generated catalog row provenance; expected vector is computed from those formulas. |
| Magic attribute parity audit will show implemented count increase and unsupported count decrease. | LOW | Rerun audit and record summary. |

## Verification Targets

From `/var/www/vltk-h5-survivors/game-source`:

1. `python3 scripts/vltk-build-equipment-seed.py`
2. `python3 scripts/vltk-audit-equipment-magic-attribute-parity.py`
3. `python3 scripts/vltk-audit-equipment-stat-coverage.py`
4. `python3 scripts/vltk-audit-equipment-requirement-parity.py`
5. `python3 scripts/vltk-audit-equipment-label-coverage.py`
6. `npm run test:pbt`
7. `npm run typecheck`
8. `npm run check:runtime-isolation`
9. `npm run build`

## Out Of Scope For This Story

- Block/enhance-hit, revive, triggered skills, yin-yang resist/anti-resist, poison-to-mana drain, companion-only stats, and visual/movement-shadow systems unless validation proves they are trivial and source-backed within S8.
- Browser portrait UI/tooltip redesign and SPR visual porting.
- Full executable PC oracle comparison; S8 fixtures are source-formula-backed, not binary runtime captures.

## Bead Mapping

Execution beads are intentionally not created in planning. `khuym:validating` must first prove the six internal-magic keys and fixture strategy are feasible. If validation passes, create only current-story beads for internal magic fields, fixture tests, audit refresh, and final validation.
