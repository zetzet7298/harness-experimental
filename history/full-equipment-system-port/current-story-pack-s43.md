# Current Story Pack — S43 Non-Character Visual Slot Classification

**Date:** 2026-05-20
**Feature:** full-equipment-system-port
**Mode:** bounded audit/data correction
**Source context:** S42 made `missing-npcres-row=6` first-class. The largest remaining bucket was `missing-npcres-mapping=6276`, but VHCND engine evidence shows many of those rows are valid equipment/stat slots with no character sprite layer setter.

## Story Outcome

Classify VHCND equipment slots that do not have character visual setters/resource getters as `no-character-visual-layer` instead of false `missing-npcres-mapping`, while preserving them in the catalog for equip/stat parity.

## Source Evidence

- `/var/www/vhcnd/sources/Client/Classes/gamecore/KItemList.cpp:1851-1901` proves the equipment slots exist for equip placement: boots, rings, amulet, belt, cuff, pendant, mask, pifeng, yinjian, shiping, horse, weapon, body, head.
- `/var/www/vhcnd/sources/Client/Classes/gamecore/KItemChangeRes.cpp:16-127` only loads/gets character visual resources for melee/range weapon, armor, helm, horse, pifeng, chibang, plus gold/plat appearance tables.
- `/var/www/vhcnd/sources/Client/Classes/gamecore/KNpcRes.h:153-158` exposes character visual setters only for helm, armor, weapon, pifeng, chibang, and horse.

## Acceptance Criteria

1. Stat/equip-only slots (`amulet`, `belt`, `cuff`, `foot`, `mask`, `pendant`, `ring/ring1/ring2`, `shiping`, `yinjian`) are marked `no-character-visual-layer`, not `missing-npcres-mapping`.
2. Rows marked `no-character-visual-layer` remain in `equipmentCatalog.json`, keep slot/stat data, and have no runtime sprite candidate/resolved sprites.
3. Visual audit reports `noCharacterVisualLayer=6715`, `missingNpcResMapping=75`, and unresolved visual items drop to `367` without claiming visual completion.
4. Visual-capable slots (`head`, `body`, `weapon`, `horse`, `pifeng`) are not hidden by this classification.
5. Tests and runtime isolation/build pass.

## Evidence

- Game-source commit: `6c28523 fix(equipment): classify non visual equipment slots`.
- `npm run test:pbt`: 23 files / 254 tests passed.
- `python3 tests/test_vltk_porting_smoke.py -k test_equipment_visual_status_audit_quantifies_current_catalog_safety`: passed.
- `npm run build`: passed; runtime isolation prebuild check passed.
- GitNexus impact before edit on `normalize_row`: LOW risk. `detect_changes` MCP timed out twice at 120s on the large generated diff, so validation relied on targeted tests, build, runtime-isolation guard, source evidence, and git diff scope.

## Remaining Gap

S43 does not resolve actual visual-capable gaps. Remaining unresolved visual buckets are now: `missing-local-source-spr=204`, `missing-npcres-mapping=75` (`horse=37`, `pifeng=38`), `missing-npcres-row=6`, and `missing-resource-row-no-fallback=82`.
