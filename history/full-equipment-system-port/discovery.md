# Discovery — Full Equipment System Port

**Feature:** full-equipment-system-port  
**Mode:** `high_risk_feature`  
**Last updated:** 2026-05-20  
**Purpose:** Repo/source reality used by Khuym planning and validation. `CONTEXT.md` remains the source of truth for decisions.

## Workspace Reality

- Harness/control workspace: `/var/www/vltk-h5-survivors/harness-experimental`.
- H5 implementation workspace: `/var/www/vltk-h5-survivors/game-source`.
- Canonical PC legacy source: `/var/www/vhcnd`.
- GitNexus repos: H5=`vltk-h5-survivors`, PC=`vhcnd`, harness=`harness-experimental`, group=`@vltk-porting`.
- Runtime assets/data/code must live in `game-source`; runtime must not read `/var/www/vhcnd` and must not use symlinks to out-of-scope roots.

## Existing H5 Equipment Stack

- `src/domain/types.ts` defines 15 slots: `head`, `body`, `belt`, `weapon`, `foot`, `cuff`, `amulet`, `ring1`, `ring2`, `pendant`, `horse`, `mask`, `pifeng`, `yinjian`, `shiping`.
- `src/domain/equipment.ts` owns equip checks, post-equip stat aggregation, stat formulas, and unsupported attribute tracking.
- `src/domain/equipmentLabels.ts` owns Vietnamese labels for attributes and requirements used by tooltip/popup text.
- `src/game/scenes/EquipmentScene.ts` owns the current portrait/equipment UI and calls `canEquipItem` from equip flow and popup checks.
- `src/data/equipmentCatalog.json` and `src/data/inventory.json` are generated H5 runtime data from VHCND-derived scripts.
- `scripts/vltk-normalize-equipment-index.py`, `scripts/vltk-build-equipment-seed.py`, and `scripts/vltk-audit-equipment-*.py` are the current source-backed catalog/seed/audit path.

## Completed Story Evidence

- S1/S2/S3 established catalog + slot taxonomy foundation and expanded H5 slot coverage to VHCND extended slots.
- S5 resolved formula ledger evidence, including source-backed `MAX_RESIST = 150` from VHCND `GameDataDef.h`.
- S6 added source-backed magic attribute enum parsing from `KMagicAttrib.h`, generated `equipment-magic-attribute-parity.audit.json`, and left unsupported runtime stat semantics explicit instead of hidden.

## S7 Equip-Condition Discovery

### PC Source

- `sources/Client/Classes/gamecore/KItemList.cpp:868-893`: `KItemList::CanEquip(int nIdx, int nPlace)` rejects invalid player/item, runs `Fit(nIdx, nPlace)` when a target place is supplied, then iterates requirement rows from `Item[nIdx].GetRequirement(nCount)` and calls `EnoughAttrib` for each row.
- `sources/Client/Classes/gamecore/KItemList.cpp:917-1040`: `KItemList::EnoughAttrib` handles:
  - `magic_requirestr`
  - `magic_requiredex`
  - `magic_requirevit`
  - `magic_requireeng`
  - `magic_requirelevel`
  - `magic_requiremenpai`
  - `magic_requireseries`
  - `magic_requiresex`
  - `magic_item_nouser`
  - `magic_item_noseries`
  - `magic_item_needskill`
  - `magic_item_needreborn`
  - `magic_item_needcity`
  - `magic_item_needbangzhu`
  - `magic_item_needtongban`
- The PC `magic_requiremenpai` branch accepts either current faction equal to value or task save value 130 equal to `value + 1`; H5 currently only has `profile.faction`, so this exception needs an explicit supported/deferred decision.
- PC city/bangzhu branches in the observed source currently return `FALSE`, so H5 must not accidentally allow these requirements.

### H5 Current State

- `src/domain/equipment.ts:315-356`: `canEquipItem` currently checks slot allowlist plus `magic_requirelevel`, stat requirements, series, faction, and sex. The default branch returns `Chưa hỗ trợ yêu cầu trang bị: <key>`.
- `src/domain/types.ts:3-18`: `PlayerProfile` has level, sex, series, faction, strength, dexterity, vitality, energy, and base combat fields, but no learned skills, reborn count, tong/guild role, city owner, companion summon, or task 130 state.
- `src/domain/equipmentLabels.ts:368-402`: `formatEquipmentRequirement` has explicit prefixes only for the eight currently supported requirement keys.
- `scripts/vltk-build-equipment-seed.py:138-149`: seed requirement coverage only lists the eight currently supported requirement keys.
- `scripts/vltk-audit-equipment-seed-coverage.py:290-295`: seed audit notes that `magic_requirevit` and `magic_requireeng` currently have no catalog evidence in the PC mirror.
- `scripts/vltk-audit-equipment-label-coverage.py` already audits label coverage for requirement keys observed in the catalog.

## S7 Constraints And Risks

| Topic | Risk | Evidence/Constraint |
| --- | --- | --- |
| Unsupported requirements | MEDIUM | PC has requirement/prohibition keys not represented in H5 player state. They must be audited and fail-closed if observed. |
| Faction exception | MEDIUM | PC `magic_requiremenpai` has task-130 exception; H5 lacks task state, so validation must decide whether current catalog needs that path or records a deferred blocker. |
| Seed coverage | MEDIUM | Seed list only covers eight requirement keys; future catalog rows could add keys without seed coverage unless S7 audit tightens it. |
| Popup/eligibility consistency | LOW | Current label formatter and equip verdict share labels for supported keys; unsupported keys need Vietnamese text to avoid hidden/default English/raw behavior. |
| Slot/Fit parity | LOW for S7 | Slot taxonomy exists and canEquip checks `allowedSlots`; S7 must preserve ring dual-slot behavior and not reopen slot taxonomy. |
| Runtime isolation | HIGH global invariant | S7 must not add runtime `/var/www/vhcnd` reads or symlinks; audits can read source paths at build/dev time only. |

## Validation Probes Needed For S7

1. Generate or run a requirement parity audit that counts every requirement key in the current catalog and classifies runtime/label/seed support.
2. Run seed rebuild and existing seed/label/stat audits to see whether unsupported requirements are currently reachable.
3. Run property/unit tests around `canEquipItem`, especially stat-self-satisfying requirements, slot mismatch, ring slots, faction/series/sex gates, and unsupported fail-closed defaults.
4. Run typecheck and runtime isolation after any execution patch.

## Open Planning Notes

- If the current catalog contains no `magic_item_*` requirement keys, S7 can still add a fail-fast audit and tests so future generated rows do not silently pass.
- If catalog contains unsupported requirement keys, validation should split S7 into an audit/provenance bead plus runtime fail-closed implementation bead before any broader player-state modeling.
- Full skill/reborn/tong/city/companion game systems are outside S7 unless validation finds they are required for current catalog items to remain testable.
