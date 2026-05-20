# Full Equipment System Port - Context

**Feature slug:** full-equipment-system-port  
**Date:** 2026-05-20  
**Exploring session:** complete  
**Scope:** Deep  
**Domain types:** SEE | RUN | ORGANIZE | READ

## Feature Boundary

Port the full VHCND equipment system into `/var/www/vltk-h5-survivors/game-source`, covering data, stats/formulas, equip conditions, inventory/equipment UI, seed data, and out-of-run to in-run visual parity; runtime assets must be local copied/moved assets inside `game-source`, never symlinked or read directly from `/var/www/vhcnd`.

## Locked Decisions

These are fixed. Planning must implement them exactly.

- **D1:** The canonical legacy source is `/var/www/vhcnd`, queried through GitNexus repo `vhcnd` or group member `@vltk-porting/pc`; no new work may reference or use the old `old PC source name` source name.
  - Rationale: existing workspace routing already migrated source truth to VHCND and the user explicitly requires continuing from VHCND.
- **D2:** The game runtime, build outputs, data catalogs, source SPR copies, generated PNGs, previews, and metadata must live under `/var/www/vltk-h5-survivors/game-source`; no runtime read, hardcoded runtime dependency, or symlink to `/var/www/vhcnd` is allowed.
  - Rationale: preserves repo isolation and matches the existing `check:no-runtime-vhcnd` guardrail.
- **D3:** The port must be complete by VHCND evidence, not by the example screenshots: include every equip slot and equipment category that VHCND supports, including slots currently missing from H5 if source evidence confirms them.
  - Known missing H5 slot candidates from VHCND quick scout: `mask`, `pifeng`/cape, `yinjian`/signet, and `shiping`/ornament, in addition to existing `head`, `body`, `belt`, `weapon`, `foot`, `cuff`, `amulet`, `ring1`, `ring2`, `pendant`, and `horse`.
- **D4:** The portrait equipment screen should borrow the vertical mobile density and card/grid affordances from Image #2, but the item tooltip/popup style should mimic the VLTK-style equipment popup in Image #1.
- **D5:** Bag items occupy exactly one mobile grid cell regardless of original PC item width/height; the UI must still preserve original `width`/`height` fields in item provenance/data for evidence and formula parity.
- **D6:** Out-of-run equipped visuals are the authority for in-run character visuals. If the user equips Tu La Phát Kết + Giáng Sa bào + Địch Khái Lục Ngọc Trượng outside a run, the running character must show the matching head/body/weapon layers for the active sex/mount/action/direction.
- **D7:** Equipment stats must be source-backed and formula-backed: base stats, generated magic options, gold options, requirements, series/five-element values, quality tiers, resistances, hand damage, HP/mana/stamina, attack rating, armor/defense, physical/element damage, skill bonuses, and other supported magic attributes must map to VHCND source rows or explicit unsupported audit entries.
- **D8:** Equipment seed data is required for testing: the seed inventory should make equip/unequip easy, contain representative and coverage-driven items across slots/quality/series/stat bins, and include known smoke loadouts; any cap such as current 125-item seed limit must be revisited if it conflicts with full coverage.
- **D9:** Visual asset porting remains gated: resolve aliases and item rows, verify engine resource mapping, create packet, copy/move required source SPR/assets into `game-source`, generate preview report, pass preview, then compose/wire runtime assets. Candidate status cannot be treated as visual proof.
- **D10:** Planning must separate evidence extraction, formula parity, UI redesign, runtime visual wiring, and validation into independently reviewable slices because the feature is high-risk and cross-cutting.

### Agent's Discretion

Agents may choose the internal data schema, pagination, responsive layout details, script sharding, and validation implementation as long as they preserve D1-D10 and remain evidence-first.

## Specific Ideas And References

- Image #1: equipment tooltip should follow VLTK-style color hierarchy, item icon, name/quality coloring, requirement lines, durability, resist/stat lines, skill bonus lines, and price/value footer.
- Image #2: portrait equipment screen can use a central character preview, side slot cards, bottom tabs, and a clear matrix bag grid, adapted to include all VHCND slots rather than the fewer sample slots.
- User examples for parity smoke: Tu La Phát Kết (head), Giáng Sa bào (body), Địch Khái Lục Ngọc Trượng (weapon), and mounted state with horse visuals.

## Existing Code Context

From the quick scout. Downstream agents read these before planning.

### Reusable Assets

- `/var/www/vltk-h5-survivors/game-source/src/domain/equipment.ts` - existing eleven-slot equipment model, stat aggregation, requirement checks, series activation/conquer helpers, weapon damage helpers, inventory snapshot builder.
- `/var/www/vltk-h5-survivors/game-source/src/domain/types.ts` - current type contract; currently defines only 11 slots and a broad `CharacterStats` shape.
- `/var/www/vltk-h5-survivors/game-source/src/game/scenes/EquipmentScene.ts` - existing portrait-ish equipment scene, slot buttons, bag grid, icon loading, equip/unequip actions, tooltip/stat refresh seams.
- `/var/www/vltk-h5-survivors/game-source/src/gateway/offlineGateway.ts` - current guarantee that `startRun()` reuses `getInventory()` so in-run derived stats equal out-of-run derived stats for the same loadout.
- `/var/www/vltk-h5-survivors/game-source/src/game/visualResolver.ts` - existing fallback chain for equipped visual manifest/layered parts/default sheet.
- `/var/www/vltk-h5-survivors/game-source/src/data/equipmentCatalog.json` - generated catalog currently has 1231 items: 560 normal, 500 magic, 171 gold; by slot: body 300, head 295, weapon 196, foot 98, belt 71, cuff 65, horse 60, amulet 54, pendant 49, ring1 43, ring2 0.
- `/var/www/vltk-h5-survivors/game-source/src/data/inventory.json` - current seed inventory and equipped-by-slot seed; current bag policy is one equipment per mobile cell.
- `/var/www/vltk-h5-survivors/game-source/scripts/vltk-build-equipment-seed.py` - deterministic seed builder with coverage pins and current 125-item cap.
- `/var/www/vltk-h5-survivors/game-source/scripts/vltk-normalize-equipment-index.py` - current VHCND equipment catalog normalization entrypoint.
- `/var/www/vltk-h5-survivors/game-source/scripts/vltk-port-loadout.py` and `scripts/vltk-extract-required-sprs.py` - current loadout/asset gate scripts.
- `/var/www/vltk-h5-survivors/game-source/scripts/vltk-audit-equipment-*.py` - current audit family for stat, quality, seed, series, formula, visual, and icon coverage.
- `/var/www/vltk-h5-survivors/game-source/tests/properties/*.test.ts` and `tests/test_vltk_porting_smoke.py` - existing property/smoke safety net for slots, stats, persistence, seed coverage, visual gate, and no-fabrication rules.

### Established Patterns

- Catalog rows carry source provenance (`source.path`, `encoding`, `line`) and original item fields; keep this pattern for every newly included slot/category.
- Magic attributes use deterministic midpoint seeding for generated test items unless a fixed gold row supplies exact values; keep explicit `valuePolicy` and source metadata.
- Rings map to `ring1` and `ring2` allowed slots even though catalog defaults to `ring1`; keep dual-slot logic and extend it carefully to new equip slots.
- Runtime visual correctness is currently enforced through preview reports and `passed-generated` manifest entries; do not bypass this with direct SPR wiring.
- Existing package scripts include `check:no-runtime-vhcnd` before build; retain and extend this isolation guard where needed.

### Integration Points

- Slot model expansion touches `src/domain/types.ts`, `src/domain/equipment.ts`, `src/game/scenes/EquipmentScene.ts`, `src/domain/equipmentStore.ts`, tests/properties, seed builder, and audits.
- Complete catalog normalization touches VHCND tables under `sources/ServerNew/_bin_v2_/gs/Settings/item/004/` including `Mask.txt`, `PiFeng.txt`, `YinJian.txt`, `ShiPin.txt`, `GoldItem.txt`, `GoldMagic.txt`, `magicattrib.txt`, `magicscript.txt`, and resource tables.
- Formula parity touches VHCND source pivots such as `KItemGenerator::GetEquipmentCommonAttrib`, `KItemList::Fit`, `KItemList::Equip`, `KItemList::GetEquipPlace`, `KMagicDesc::GetDesc_New`, `KNpcAttribModify`, `KPlayer`, and `KPlayerSet`.
- Visual parity touches NpcRes/resource tables, source SPR copying under `public/assets/character/vhcnd/source/`, generated manifests under `public/assets/character/vhcnd/`, preview reports under `data/vltk-normalized/previews/`, and runtime resolver code.

## Canonical References

- `/var/www/vltk-h5-survivors/harness-experimental/AGENTS.md` - workspace routing, VHCND source of truth, no symlink/direct runtime VHCND asset rule.
- `/var/www/vltk-h5-survivors/game-source/scripts/README.md` - current equipped character and catalog gate commands.
- `/var/www/vltk-h5-survivors/game-source/docs/VHCND_SPR_PORTING_PLAYBOOK.md` - required preview-gated visual pipeline.
- `/var/www/vhcnd/sources/Client/Classes/gamecore/KItemList.cpp:1912-1977` - PC slot fit mapping, including current missing extended slots.
- `/var/www/vhcnd/sources/Client/Classes/gamecore/KItemGenerator.CPP:3227-3299` - common equipment attribute source lookup formula `particular * 10 + level - 1` and extended detail-type dispatch.
- `/var/www/vhcnd/sources/Client/Classes/gamecore/GameDataDef.h` - equip slot/detail enums and resist constants must be reconciled with H5 constants.
- `/var/www/vhcnd/sources/ServerNew/_bin_v2_/gs/Settings/item/004/` - active VHCND item table directory for the complete port.
- `https://docs.phaser.io/api-documentation/class/gameobjects-container`, `https://docs.phaser.io/api-documentation/class/gameobjects-image`, and `https://docs.phaser.io/api-documentation/class/gameobjects-gameobjectfactory` - Phaser UI primitives for containers, images, text, and grids.

## Outstanding Questions

### Resolve Before Planning

- None. The user has explicitly required full VHCND equipment coverage, portrait redesign, exact stat/formula parity, source-backed attributes, local asset isolation, and seed data.

### Deferred To Planning

- [ ] Determine exact VHCND active package/table precedence for every equipment source table before generating more catalog rows.
- [ ] Reconcile H5 `PC_MAX_RESIST = 95` with the currently indexed VHCND `GameDataDef.h` value of `MAX_RESIST = 150`; if package/source variants differ, choose the active engine value with evidence.
- [ ] Decide how to represent extended slots in the portrait UI without hiding any slot: likely collapsible side slot groups plus central character preview and bottom bag tabs.
- [ ] Quantify visual coverage: how many catalog items have `candidate`, `missing-npcres-mapping`, `missing-resource-resolution`, `passed-generated`, and copied local source assets.
- [ ] Decide whether seed inventory remains coverage-sampled or adds a generated test-mode catalog browser for all equipment rows; D8 requires easy testing without making the normal bag unusable.

## Deferred Ideas

- Multiplayer, server persistence, trading, crafting, and monetization are out of scope unless needed to validate equipment equip/unequip and stats.
- Drag-and-drop inventory is optional; explicit tap/select/equip is sufficient for the first portrait mobile port if it is clear and testable.

## Handoff Note

CONTEXT.md is the source of truth. Decision IDs are stable. Planning reads locked decisions, code context, canonical references, and deferred-to-planning questions. Validating and reviewing use locked decisions for coverage and UAT.
