# Current Story Pack — S44 Mask Template Visual Gap Classification

**Date:** 2026-05-20
**Feature:** full-equipment-system-port
**Mode:** bounded audit/data correction
**Source context:** S43 deliberately left `mask=1764` unresolved because VHCND mask items can affect visual state through `m_MaskType`. S44 separates this path from generic equipment NpcRes mapping.

## Story Outcome

Classify mask rows as `missing-mask-template-mapping` instead of generic `missing-npcres-mapping`, preserving the correct VHCND visual path: mask item `GetBaseMagic()`/`ItemResIdx` sets `m_MaskType`, then `KNpc::ReSetRes` resolves an NPC template and `NpcResType` before sprite lookup.

## Source Evidence

- `/var/www/vhcnd/sources/Client/Classes/gamecore/KItemList.cpp:1280-1288` — equipping mask sets `Npc[nNpcIdx].m_MaskType` from `ItemResIdx` or `GetBaseMagic()`.
- `/var/www/vhcnd/sources/Client/Classes/gamecore/KItem.h:383-388` — `GetBaseMagic()` returns `m_aryBaseAttrib[0].nValue[0]`.
- `/var/www/vhcnd/sources/Client/Classes/gamecore/KNpc.cpp:10628-10641` — nonzero `m_MaskType` changes shape by copying frame/template data and reading `NpcResType`.
- `/var/www/vhcnd/sources/Client/Classes/gamecore/ScriptFuns.cpp:2466-2496` — `LuaGetMaskActionSpr` documents template/action sprite lookup through `NpcResType`, `人物类型.txt`, and `普通npc资源.txt`.

## Acceptance Criteria

1. All 1764 mask rows are counted as `missing-mask-template-mapping`.
2. Mask rows no longer inflate generic `missing-npcres-mapping`.
3. Mask rows remain unresolved with no candidate sprite/resolved sprites until template-to-sprite mapping is source-backed.
4. Visual audit exposes `missingMaskTemplateMapping=1764`, `missingNpcResMapping=916`, and `unresolvedVisualItems=2972`.
5. Tests, runtime isolation, build, and changed-scope check pass.

## Evidence

- Game-source commit: `8339d52 fix(equipment): separate mask template visual gaps`.
- `npm run test:pbt`: 24 files / 257 tests passed.
- `python3 tests/test_vltk_porting_smoke.py -k test_equipment_visual_status_audit_quantifies_current_catalog_safety`: passed.
- `npm run build`: passed; runtime isolation prebuild check passed.
- GitNexus `impact(normalize_row)`: LOW risk before edit.
- GitNexus `detect_changes(scope="unstaged")`: MEDIUM risk, affected processes limited to generated-magic parse flows from line-shift/touched-symbol attribution; targeted equipment visual tests/build passed.

## Remaining Gap

S44 does not map mask templates to runtime sprites. Remaining true unresolved visual buckets are: `missing-local-source-spr=204`, `missing-mask-template-mapping=1764`, `missing-npcres-mapping=916` (`horse=37`, `pifeng=38`, `shiping=648`, `yinjian=193`), `missing-npcres-row=6`, and `missing-resource-row-no-fallback=82`.
