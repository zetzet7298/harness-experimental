# Current Story Pack — S47 Mask Template Evidence Preflight

**Date:** 2026-05-20  
**Feature:** full-equipment-system-port  
**Mode:** bounded audit/data correction  
**Source context:** S46 closed `missing-npcres-mapping` and left `missing-mask-template-mapping=1764`. Mask visuals require a separate VHCND template flow, not ordinary equipment NpcRes rows.

## Story Outcome

Replace the generic mask visual gap with source-backed mask template identity evidence, without wiring runtime mask visuals yet:

- Derive `maskTemplateId` from the VHCND mask item row field used by `GetBaseMagic()` / `m_MaskType`.
- Resolve the VHCND `NpcS.txt` template row (`maskTemplateId + 2`) enough to record `maskNpcName` and `maskNpcResType`.
- Keep masks unresolved until the NPC resource kind/action tables and required SPRs are mapped, copied locally, preview-gated, and reviewed.

## Source Evidence

- `/var/www/vhcnd/sources/Client/Classes/gamecore/KItemList.cpp:1280-1288` — mask equip path sets `m_MaskType` from positive `ItemResIdx`, otherwise `GetBaseMagic()`.
- `/var/www/vhcnd/sources/Client/Classes/gameui/KuiItemdesc.cpp:959-976` — item tooltip path reads `GetBaseMagic()`, adds `+2`, gets `NpcResType`, then reads NPC resource/action sprite.
- `/var/www/vhcnd/sources/Client/Classes/gamecore/KNpc.cpp:10575-10641` — `ReSetRes(0)` transforms character visuals through `m_MaskType + 2` and `NpcResType`.
- `/var/www/vhcnd/sources/ServerNew/_bin_v2_/gs/Settings/item/004/Mask.txt:1-12` — generated mask rows carry the template id in the first base value slot (`Min1`, e.g. 54/56/57/59/63).
- `/var/www/vhcnd/sources/ServerNew/_bin_v2_/gs/Settings/item/004/GoldItem.txt:4369-4372` — gold mask rows also carry first base values such as 1311/1310 while `ItemResIdx` remains unavailable for safe visual wiring.
- `/var/www/vhcnd/item_data/settings/npcs.txt` — decoded `NpcS.txt` evidence source for row-level `Name` and `NpcResType`.

## Acceptance Criteria

1. Mask rows in normalized data/catalog include source-backed mask template fields (`maskTemplateId`, template row number, NPC name, and `NpcResType` when found).
2. The visual audit no longer hides all mask rows in a generic `missing-mask-template-mapping` bucket; it reports more precise source-backed unresolved mask statuses.
3. No mask row becomes a runtime visual `candidate` until NPC resource/action table mapping and local SPR preview evidence exist.
4. Visual audit remains safe: `candidate=0`, `unsafeResolvedVisualItems=0`, no runtime `/var/www/vhcnd` literals, and no symlinked runtime assets.
5. Tests, build, browser smoke, and changed-scope checks pass.

## Evidence

- Game-source commit: pending.
- Validation: pending.
- GitNexus impact before edit: pending.

## Remaining Gap

S47 does not copy or compose mask SPRs. After S47, a later slice must map the NPC resource kind/action tables and run the normal packet → local-copy → preview → compose/runtime gate before mask visuals can be user-facing.
