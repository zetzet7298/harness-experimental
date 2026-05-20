# Current Story Pack — S12 Persistence Migration

**Feature:** full-equipment-system-port  
**Epic:** E3 Portrait equipment UI + inventory/seed workflow  
**Mode:** `high_risk_feature`  
**Prepared after:** S11 review/compounding passed and pushed.

## Story Outcome

Prove and harden the equipment persistence path so old/sparse saved loadouts from before the expanded VHCND slot model load safely into the current 15-slot schema, while new saves can persist extended slots (`mask`, `pifeng`, `yinjian`, `shiping`) without corrupting existing equipment or crashing the outside-run UI / run-start inventory snapshot.

## Entry State

- `EquipmentSlot` and `EQUIPMENT_SLOT_ORDER` currently include 15 slots: the original equipment set plus `mask`, `pifeng`, `yinjian`, and `shiping`.
- `src/data/inventory.json` seed `equippedBySlot` already includes all 15 slots and representative extended-slot item ids.
- `equipmentStore.sanitizeEquipmentState()` loops over `EQUIPMENT_SLOT_ORDER`, so missing keys from older saved payloads naturally become `null` in the full loadout.
- `equipmentStore.saveEquipmentState()` loops over `EQUIPMENT_SLOT_ORDER`, so it should be able to serialize extended slots when they hold valid item ids.
- Persistence comments/tests still contain stale wording such as "eleven slots" and do not explicitly prove legacy sparse 11-slot payloads or extended-slot save/load cases.

## Source / Local Evidence

- `/var/www/vltk-h5-survivors/game-source/src/domain/types.ts:1` — `EquipmentSlot` includes 15 values.
- `/var/www/vltk-h5-survivors/game-source/src/domain/equipment.ts:4` — `EQUIPMENT_SLOT_ORDER` includes 15 values.
- `/var/www/vltk-h5-survivors/game-source/src/domain/equipmentStore.ts:37-68` — full loadout construction and seed fallback are order-driven.
- `/var/www/vltk-h5-survivors/game-source/src/domain/equipmentStore.ts:81-103` — sanitize iterates every current slot, drops unknown ids, drops slot/item mismatches.
- `/var/www/vltk-h5-survivors/game-source/src/domain/equipmentStore.ts:160-177` — save iterates every current slot and writes sparse persisted JSON.
- `/var/www/vltk-h5-survivors/game-source/tests/properties/persistence.unit.test.ts` — existing defensive persistence tests, but no explicit extended-slot / legacy sparse migration assertions yet.

## Acceptance Criteria

1. Persistence docs/comments no longer claim the full loadout has only eleven slots.
2. Tests explicitly prove an old/sparse persisted payload containing only original slots loads into a full 15-slot loadout, with all extended slots present and `null`.
3. Tests explicitly prove valid extended-slot ids can be sanitized, saved, and loaded for `mask`, `pifeng`, `yinjian`, and `shiping`.
4. Slot/item mismatch protection still applies to extended slots.
5. Existing fallback behavior remains unchanged: malformed JSON, wrong version, unavailable storage, and missing ids do not crash.
6. Validation passes: `npm run typecheck`, targeted persistence tests, full property suite if needed, `npm run check:no-runtime-vhcnd`, `npm run build`, and GitNexus `detect_changes` review.

## Non-Goals

- Do not add server persistence or a new migration framework unless validation proves the current versioned shape cannot support sparse legacy payloads.
- Do not change formula/stat/equip semantics.
- Do not change visual SPR wiring.
- Do not introduce runtime reads from `/var/www/vhcnd` or symlinks.
