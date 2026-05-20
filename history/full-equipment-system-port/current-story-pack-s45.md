# Current Story Pack — S45 Gold Detail Visual Resource Mapping

**Date:** 2026-05-20  
**Feature:** full-equipment-system-port  
**Mode:** bounded audit/data correction  
**Source context:** S44 left true visual gaps unresolved. S45 fixes a H5 normalizer mapping bug where gold detail 7 was incorrectly treated as horse and detail 8 as helm, contradicting VHCND `EQUIPDETAILTYPE` and `KItemList::Equip` evidence.

## Story Outcome

Correct gold-item visual resource routing so helm/head rows use `HelmRes`, horse rows use `HorseRes`, cuff rows stay stat-only, and newly exposed absent source/resource rows remain unresolved with explicit provenance instead of becoming runtime candidates.

## Source Evidence

- `/var/www/vhcnd/sources/Client/Classes/gamecore/KItem.h:52-68` — `EQUIPDETAILTYPE`: `equip_helm=7`, `equip_cuff=8`, `equip_horse=10`.
- `/var/www/vhcnd/sources/Client/Classes/gamecore/KItemList.cpp:1156-1328` — equip visual flow calls `GetHelmRes` for `itempart_head`, `GetHorseRes` for `itempart_horse`, and does not give cuff a character visual setter.
- `/var/www/vhcnd/sources/Client/Classes/gamecore/KItemChangeRes.cpp:78-88` — `GetHelmRes` row formula and `m_Helm` table lookup.
- `/var/www/vhcnd/sources/Client/Classes/gamecore/KItemChangeRes.cpp:117-126` — `GetHorseRes` row formula and `m_Horse` table lookup.
- `/tmp/s45-missing-horse-sprs/manifest.tsv` — all 27 newly exposed horse `MA_HB/MA_HH/MA_HT_*_HR01.spr` source candidates are `MISS` through all configured PAK matches.

## Acceptance Criteria

1. `DETAIL_RESOURCE` maps detail 7 → `item/HelmRes.txt` / `head` and detail 10 → `item/HorseRes.txt` / `horseMid`.
2. `DETAIL_RESOURCE` no longer maps detail 8/cuff to `HelmRes`.
3. No head catalog row resolves from `item/HorseRes.txt`.
4. Visual audit remains safe: `candidate=0`, `unsafeResolvedVisualItems=0`, and `missingResourceResolution=0`.
5. Updated status counts are exposed: `preview-passed-loadout-evidence=2527`, `missing-local-source-spr=179`, `missing-npcres-mapping=879`, `missing-resource-row-no-fallback=87`, `unresolvedVisualItems=2915`.
6. Tests, runtime isolation, build, browser smoke, and changed-scope check pass.

## Evidence

- Game-source commit: `c56e0dc fix(equipment): correct gold visual resource mapping`.
- `npm run test:pbt`: 25 files / 260 tests passed.
- `python3 tests/test_vltk_porting_smoke.py -k test_equipment_visual_status_audit_quantifies_current_catalog_safety`: passed.
- `npm run build`: passed; runtime isolation prebuild check passed.
- Browser smoke on `http://localhost:5173`: page loaded with no browser errors; EquipmentScene debug state reachable.
- GitNexus `impact(DETAIL_RESOURCE)`: LOW risk before edit.
- GitNexus `impact(normalize_row)`: LOW risk before edit.
- GitNexus `detect_changes(scope="staged")`: LOW risk; no affected processes.

## Remaining Gap

S45 does not recover absent horse/head/pifeng source SPRs and does not resolve mask, pifeng, shiping, or yinjian mapping. Remaining true visual buckets are: `missing-local-source-spr=179`, `missing-mask-template-mapping=1764`, `missing-npcres-mapping=879`, `missing-npcres-row=6`, and `missing-resource-row-no-fallback=87`.
