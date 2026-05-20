# Current Story Pack — S43 Non-Character Visual Slot Classification

**Date:** 2026-05-20
**Feature:** full-equipment-system-port
**Mode:** bounded audit/data correction
**Source context:** S42 made `missing-npcres-row=6` first-class. The largest remaining bucket was `missing-npcres-mapping=6276`, but VHCND engine evidence shows many of those rows are valid equipment/stat slots with no character sprite layer setter.

## Story Outcome

Classify only VHCND equipment slots that have no character visual setter/resource getter or special visual side effect as `no-character-visual-layer` instead of false `missing-npcres-mapping`, while preserving them in the catalog for equip/stat parity.

## Source Evidence

- `/var/www/vhcnd/sources/Client/Classes/gamecore/KItemList.cpp:1851-1901` proves the equipment slots exist for equip placement: boots, rings, amulet, belt, cuff, pendant, mask, pifeng, yinjian, shiping, horse, weapon, body, head.
- `/var/www/vhcnd/sources/Client/Classes/gamecore/KItemChangeRes.cpp:16-127` loads/gets character visual resources for melee/range weapon, armor, helm, horse, pifeng, chibang, plus gold/plat appearance tables.
- `/var/www/vhcnd/sources/Client/Classes/gamecore/KNpcRes.h:153-158` exposes character visual setters for helm, armor, weapon, pifeng, chibang, and horse.
- `/var/www/vhcnd/sources/Client/Classes/gamecore/KItemList.cpp:1280-1328` and `:1630-1688` prove `mask`, `shiping`, and `yinjian` can still affect visual state through `m_MaskType`, `m_WeaponType`, or `m_ArmorType`, so S43 deliberately leaves them unresolved instead of marking them nonvisual.

## Acceptance Criteria

1. Stat/equip-only slots (`amulet`, `belt`, `cuff`, `foot`, `pendant`, `ring/ring1/ring2`) are marked `no-character-visual-layer`, not `missing-npcres-mapping`.
2. Rows marked `no-character-visual-layer` remain in `equipmentCatalog.json`, keep slot/stat data, and have no runtime sprite candidate/resolved sprites.
3. Visual audit reports `noCharacterVisualLayer=4110`, `missingNpcResMapping=2680`, and unresolved visual items drop to `2972` without claiming visual completion.
4. Visual-capable or visual-affecting slots (`head`, `body`, `weapon`, `horse`, `pifeng`, `mask`, `shiping`, `yinjian`) are not hidden by this classification.
5. Tests and runtime isolation/build pass.

## Evidence

- Game-source commit: `321bf5d fix(equipment): keep special visual slots unresolved`.
- `npm run test:pbt`: 23 files / 254 tests passed.
- `python3 tests/test_vltk_porting_smoke.py -k test_equipment_visual_status_audit_quantifies_current_catalog_safety`: passed.
- `npm run build`: passed; runtime isolation prebuild check passed.
- GitNexus impact before edit on `normalize_row`: LOW risk. GitNexus `detect_changes(scope="unstaged")`: LOW risk, affected processes `[]`.

## Remaining Gap

S43 does not resolve actual visual-capable gaps. Remaining unresolved visual buckets are now: `missing-local-source-spr=204`, `missing-npcres-mapping=2680` (`horse=37`, `mask=1764`, `pifeng=38`, `shiping=648`, `yinjian=193`), `missing-npcres-row=6`, and `missing-resource-row-no-fallback=82`.
