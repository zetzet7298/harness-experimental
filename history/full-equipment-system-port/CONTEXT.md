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
- **D11:** All user-facing equipment/runtime/UI text must be Vietnamese only; do not show Chinese text or mixed Chinese/Vietnamese labels to the player. Source Chinese/Vietnamese/mojibake aliases may remain as internal provenance only, not UI copy.
  - Rationale: the user explicitly requires Vietnamese-only user-facing output.
- **D12:** Mounts/horses must not be assigned the green quality tier. If VHCND source tables expose mount-like rows through generic quality logic, the H5 catalog/seed/UI must classify them according to VHCND evidence while excluding green mount quality.
  - Rationale: the user explicitly clarified that mounts do not have green quality.
- **D13:** The equipment detail popup/panel opened by tapping an item must be centered on the screen, while still fitting portrait mobile layout and preserving VLTK-style tooltip hierarchy.
  - Rationale: the user explicitly clarified the popup placement requirement.
- **D14:** The equipment/bag browsing interaction should not use page-by-page pagination. It should be redesigned as a hold/drag vertical continuous scroll, behaving like an infinite-feeling scroll list/grid for mobile equipment browsing.
  - Rationale: the user explicitly rejected the current pagination feel and requested hold-and-slide vertical scrolling.

### Agent's Discretion

Agents may choose the internal data schema, continuous-scroll implementation details, responsive layout details, script sharding, and validation implementation as long as they preserve D1-D14 and remain evidence-first.

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
- User-facing strings must be Vietnamese-only; decoded Chinese names/aliases are allowed only in source provenance, audits, or internal matching metadata.
- Mount/horses are a special quality case: do not synthesize or display green-quality mounts.
- Equipment detail popup/panel must open centered on the viewport; do not anchor it only beside the tapped slot/item.
- Equipment/bag browsing should use hold/drag vertical continuous scrolling instead of page-by-page pagination.

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

- [x] Determine exact VHCND active package/table precedence for every equipment source table before generating more catalog rows: S25 records `sourceResolution.precedence` for each active table and audits `selected-first-existing`. Precedence is Client root → Client item/004 → ServerNew root → ServerNew item/004; the active rows currently selected all come from `ServerNew/_bin_v2_/gs/Settings/...`, with rank 3 for root tables and rank 4 for item/004-only tables.
- [x] Reconcile H5 `PC_MAX_RESIST` with active VHCND `GameDataDef.h` value: S23 confirmed `sources/Client/Classes/gamecore/GameDataDef.h:134` defines `MAX_RESIST = 150`; H5 `PC_MAX_RESIST = 150` is correct, while `resistMax = 95` remains only a per-call tighter-cap test example.
- [x] Decide how to represent extended slots in the portrait UI without hiding any slot: S26 locks the current all-visible two-column portrait paper-doll layout. Left column shows `head/body/belt/weapon/foot/mask/pifeng`, right column shows `cuff/amulet/ring1/ring2/pendant/yinjian/shiping`, and `horse` is centered below; no collapsible group is needed because tests prove all 15 slot buttons/captions fit inside the paper-doll band above the bag.
- [x] Quantify visual coverage (S24, refreshed by S28): current catalog has `candidate=2748`, `missing-npcres-mapping=6276`, `missing-npcres-row=6`, `missing-resource-resolution=82`, `preview-passed-loadout-evidence=418`, `unsafeResolvedVisualItems=0`; local copied SPR evidence has `uniqueBasenames=296`, `fileCopies=509`, `resolvedItemsWithAllLocalSources=418`; dynamic layered parts coverage has `dedicatedPartAssetCountsByAction={run:142,idle:142}`, `remainingDedicatedPartAssetGap=38`, and `remainingPartSheetGap=272`; runtime manifest still has `passedGeneratedEntries=9`. S30 further confirms the 38 remaining dedicated source SPRs are absent from `/var/www/vhcnd` exact filename search and `vltk_extract_tables.py --all-matches`. S31 originally marked 182 affected catalog rows (`head=74`, `horse=108`); the current regenerated audit now marks 204 rows after PiFeng resource mapping added 22 unresolved pifeng rows (`head=74`, `horse=108`, `pifeng=22`) as `missing-local-source-spr`, keeps provenance in `missingSourceSprites`, and makes out-of-run/in-run visual collectors skip those unresolved rows instead of requesting absent sheets or guessing visuals. S32 also audits the 82 `missing-resource-resolution` weapon rows: all are missing row 72 from `item/MeleeRes.txt` (63 rows) or row 32 from `item/RangeRes.txt` (19 rows), and no configured `/var/www/vhcnd` table candidate has a fallback row. S33 marks those 82 weapon rows as `missing-resource-row-no-fallback`, records `missingResourceRows`, and removes the generic `missing-resource-resolution` bucket from visual-status audit (`missingResourceResolution=0`, `missingResourceRowsNoFallback=82`) without synthesizing resource rows. S34 audits the remaining candidate bucket: `candidateItemCount=2566` across body/cuff/head/horse/weapon, with `missingPreviewSpriteCount=117`, `actionableLocalSourceSpriteCount=117`, and `missingLocalSourceSpriteCount=0`. S35 preview-gates the local `ma_hd_007_hr01.spr` candidate and `ma_bd/ma_lh/ma_rh_007_hr01.spr` body trio with passed local-source preview evidence, reducing the remaining candidate bucket to `candidateItemCount=1960` (`body=767`, `cuff=74`, `head=510`, `horse=96`, `weapon=513`) and `missingPreviewSpriteCount=113`. S36 preview-gates the next high-impact local batch (`ma_hb_005_hr01.spr`, `ma_rw_020_hr01.spr`, and `ma_bd/ma_lh/ma_rh_010_hr01.spr`), reducing the bucket to `candidateItemCount=1545` (`body=637`, `cuff=74`, `head=369`, `horse=96`, `weapon=369`) and `missingPreviewSpriteCount=108`. S37 preview-gates `ma_hb_008_hr01.spr`, `ma_rw_022_hr01.spr`, and `ma_bd/ma_lh/ma_rh_004_hr01.spr`, reducing the bucket to `candidateItemCount=1247` (`body=542`, `cuff=74`, `head=271`, `horse=96`, `weapon=264`) and `missingPreviewSpriteCount=103`. S38 preview-gates `ma_rw_019_hr01.spr`, `ma_hd_004_hr01.spr`, and `ma_bd/ma_lh/ma_rh_016_hr01.spr` plus `ma_bd/ma_lh/ma_rh_019_hr01.spr`, reducing the bucket to `candidateItemCount=911` (`body=384`, `head=259`, `horse=96`, `weapon=172`) and `missingPreviewSpriteCount=95`. S39 preview-gates `ma_hb_007_hr01.spr`, `ma_hb_004_hr01.spr`, `ma_rw_024_hr01.spr`, and `ma_bd/ma_lh/ma_rh_002_hr01.spr`, reducing the bucket to `candidateItemCount=750` (`body=352`, `head=168`, `horse=96`, `weapon=134`) and `missingPreviewSpriteCount=89`. S40 preview-gates body trios 008/011/014, reducing the bucket to `candidateItemCount=654` (`body=256`, `head=168`, `horse=96`, `weapon=134`) and `missingPreviewSpriteCount=80`. S41 preview-gates all 80 remaining local candidate sprite basenames with `matched=80` and `rendered=80`, closing the generic candidate bucket at `candidateItemCount=0`, `missingPreviewSpriteCount=0`, and `actionableLocalSourceSpriteCount=0`. S42 hardens the visual status audit so the six PiFeng rows whose `PiFengRes` values point beyond the available NpcRes table are counted as `missing-npcres-row=6` and included in unresolved visual totals rather than guessed. S43 uses VHCND engine evidence (`KItemList::GetEquipPlace`, `KItemChangeRes`, `KNpcRes` setters, and the `KItemList::Equip`/`UnEquip` special cases for mask/yinjian/shiping) to classify 4110 stat/equip-only rows as `no-character-visual-layer`; these rows stay in catalog/stat/equip coverage but no longer count as missing character visuals. Mask, yinjian, and shiping are deliberately left unresolved because VHCND can affect `m_MaskType`, `m_WeaponType`, or `m_ArmorType` for them. S44 further separates the mask path: all 1764 mask rows are now `missing-mask-template-mapping` because VHCND resolves them through `m_MaskType -> KNpc::ReSetRes -> NpcResType`, not ordinary equipment NpcRes layers. S45 fixes the gold-item visual detail mapping from VHCND enum/equip evidence: detail 7 now resolves through `HelmRes`, detail 10 through `HorseRes`, and cuff/detail 8 no longer borrows `HelmRes`. This promotes 57 head gold rows to existing preview-passed evidence, moves the remaining absent-source horse/head rows into source-backed `missing-local-source-spr`, and records 5 horse `HorseRes#352` rows as `missing-resource-row-no-fallback`; the generic candidate bucket stays closed at 0. The remaining true visual unresolved total is now 2915 rows: `missing-local-source-spr=179` (`head=17`, `horse=140`, `pifeng=22`), `missing-mask-template-mapping=1764`, `missing-npcres-mapping=879` (`pifeng=38`, `shiping=648`, `yinjian=193`), `missing-npcres-row=6`, and `missing-resource-row-no-fallback=87` (`horse=5`, `weapon=82`). Full visual coverage remains incomplete and must continue through explicit unresolved buckets: `missing-local-source-spr`, `missing-mask-template-mapping`, `missing-npcres-mapping`, `missing-npcres-row`, and `missing-resource-row-no-fallback`, plus any later parts-export/runtime-manifest promotion needed for player-facing visuals.
- [x] Decide whether seed inventory remains coverage-sampled or adds a generated test-mode catalog browser for all equipment rows: S27 keeps normal `Kho: Seed` coverage-sampled/capped at 125 one-cell items for easy equip testing, and uses `Kho: Catalog` as the uncapped generated catalog browser. Catalog mode sources `this.catalog.items` and slot filters via `allowedSlots`, so all 9552 current catalog rows are reachable through at least one slot without making the normal bag unusable.

## Deferred Ideas

- Multiplayer, server persistence, trading, crafting, and monetization are out of scope unless needed to validate equipment equip/unequip and stats.
- Drag-and-drop inventory is optional; explicit tap/select/equip is sufficient for the first portrait mobile port if it is clear and testable.

## Handoff Note

CONTEXT.md is the source of truth. Decision IDs are stable. Planning reads locked decisions, code context, canonical references, and deferred-to-planning questions. Validating and reviewing use locked decisions for coverage and UAT.
