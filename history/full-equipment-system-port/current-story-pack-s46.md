# Current Story Pack — S46 Special Slot Visual Gap Classification

**Date:** 2026-05-20  
**Feature:** full-equipment-system-port  
**Mode:** bounded audit/data correction  
**Source context:** S45 corrected gold helm/horse detail mapping and left `missing-npcres-mapping=879`. S46 separates true special visual paths for PiFeng, ShiPin, and YinJian so generic NpcRes mapping no longer hides the real blocker.

## Story Outcome

Close the generic `missing-npcres-mapping` bucket without guessing visuals:

- Gold PiFeng rows use VHCND's direct `m_PifengType` from item level and resolve through `KNpcRes::SetPifeng`; their absent source sprites remain `missing-local-source-spr`.
- ShiPin and YinJian rows use VHCND's `ItemResIdx > 0` special cases, not a normal resource table; they are classified as `missing-itemresidx-visual-mapping` until source-backed ItemResIdx evidence exists.

## Source Evidence

- `/var/www/vhcnd/sources/Client/Classes/gamecore/KItemList.cpp:1290-1315` — PiFeng equip path sets `m_PifengType` from `ItemResIdx`, gold item level, or `GetPifengRes`.
- `/var/www/vhcnd/sources/Client/Classes/gamecore/KNpcRes.cpp:969-1002` — `SetPifeng` resolves filenames by `nPifengType` across PiFeng body parts/layers.
- `/var/www/vhcnd/sources/Client/Classes/gamecore/KItemList.cpp:1318-1327` — ShiPin sets `m_WeaponType` and YinJian sets `m_ArmorType` only when `GetItemResIdx() > 0`.
- `/var/www/vhcnd/sources/Client/Classes/gamecore/KItem.h:218-219` — `GetItemResIdx()` reads `m_CommonAttrib.nRes`.
- `/var/www/vhcnd/sources/Client/Classes/gamecore/KItem.cpp:1580-1605` — gold equipment default `nRes = 0`, so source-backed ItemResIdx mapping must be found before runtime visuals are wired.

## Acceptance Criteria

1. `missing-npcres-mapping` is removed from status counts and `coverageQuantification.catalogItems.missingNpcResMapping = 0`.
2. `missing-itemresidx-visual-mapping=841`, split as `shiping=648`, `yinjian=193`.
3. Gold PiFeng level-driven rows are no longer generic missing NpcRes rows; PiFeng source-missing rows become `missing-local-source-spr=60`.
4. Visual audit remains safe: `candidate=0`, `unsafeResolvedVisualItems=0`, and no runtime `/var/www/vhcnd`/symlink use.
5. Tests, build, browser smoke, and changed-scope checks pass.

## Evidence

- Game-source commit: `884671e fix(equipment): classify special slot visual gaps`.
- `npm run test:pbt`: 26 files / 262 tests passed.
- `python3 tests/test_vltk_porting_smoke.py -k test_equipment_visual_status_audit_quantifies_current_catalog_safety`: passed.
- `npm run build`: passed; runtime isolation prebuild check passed.
- Browser smoke on `http://localhost:5173`: page loaded, one canvas present, EquipmentScene active.
- GitNexus `impact(npcres_candidate)`: LOW risk before edit.
- GitNexus `impact(normalize_row)`: LOW risk before edit.
- GitNexus `impact(build_item)`: LOW risk before edit.
- GitNexus `detect_changes(scope="staged")`: HIGH risk due expected generator/seed/audit and smoke-test flow changes; reviewed against affected `main` seed processes and covered by full S46 validation.

## Remaining Gap

S46 is a classification/route-correction slice. It does not recover absent SPRs, does not map mask templates, and does not invent ItemResIdx values. Remaining visual buckets are `missing-local-source-spr=217`, `missing-mask-template-mapping=1764`, `missing-itemresidx-visual-mapping=841`, `missing-npcres-row=6`, and `missing-resource-row-no-fallback=87`.
