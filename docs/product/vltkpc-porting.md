# VLTKPC Porting Contract

## Scope

This contract covers legacy VLTKPC/JX data and SPR assets used by the H5 game
prototype. It applies whenever work touches item identity, equipment visuals,
map identity, minimap/background assets, enemy visual types, source SPRs,
normalized packets, preview reports, or runtime spritesheets.

## Required Workflow

1. Resolve item identity and row evidence before visual work.
2. Normalize item/equipment evidence into packet or index artifacts under
   `game-source/data/vltk-normalized/`.
3. Generate or update preview PNG/report evidence before runtime wiring.
4. Copy required raw SPR/map sources into `game-source/public/assets/**/vltkpc/` before runtime use.
5. Compose runtime sheets or generated map backgrounds from local copied sources only.
6. For map ports, derive map identity from active `MapList`, `.wor`, minimap image, and server region/NPC evidence before selecting enemy templates.
7. Update this harness when the product contract, validation gates, or repeated
   porting workflow changes.

## Equipment System

- Generated equipment catalog: `game-source/src/data/equipmentCatalog.json`.
- Seed inventory: `game-source/src/data/inventory.json`, schema v2, all VLTKPC equip
  slots represented as `head`, `body`, `belt`, `weapon`, `foot`, `cuff`,
  `amulet`, `ring1`, `ring2`, `pendant`, and `horse`.
- Mobile bag policy: every equipment item occupies one grid cell even when the
  source VLTKPC item has larger legacy width/height.
- Runtime persistence key: `vltkpc-equipment-state-v1`.
- Supported formula coverage lives in `game-source/src/domain/equipment.ts`;
  every key present in the current generated equipment catalog must be mapped into
  stat/audit fields or explicitly tracked in `unsupportedAttributes` until PC
  source parity is implemented.
- Long SPR copy/extract phases should use the auto parallel worker path such as
  `scripts/vltk-extract-required-sprs.py --workers auto`.

## Current Known Loadout

- Horse: `Phiên Vũ`.
- Weapon: `Địch Khái Trúc Trượng`.
- Helm: `Tu La phát kết` resolves through `GetHelmRes` (`tableValue - 2`) for the NPC field, but `KNpcRes::SetHelm` indexes the NpcRes table with the resource table value as `equipNo`, so the mounted-run head sprite is `MA_HD_010_HR01.spr`; optional hair part is absent in current PAK evidence.
- Armor: `Giáng Sa bào` resolves through `GetArmorRes` (`tableValue - 2`) for the NPC field, but `KNpcRes::SetArmor` indexes body/hand NpcRes tables with the resource table value as `equipNo`, so mounted-run armor sprites are `MA_BD/LH/RH_034_HR01.spr`; optional shoulder part is absent in current PAK evidence.
- Runtime sheet: `public/assets/character/vltkpc/equipped-tu-la-giang-sa-staff-phien-vu-run.png`.
- Packet evidence:
  `data/vltk-normalized/port-packets/equipped-phien-vu-dich-khai.json` and
  `data/vltk-normalized/port-packets/equipped-phien-vu-dich-khai-loadout.json`.
- Preview evidence:
  `data/vltk-normalized/previews/equipped-phien-vu-dich-khai-loadout.png` and
  `data/vltk-normalized/previews/equipped-phien-vu-dich-khai-loadout.report.json`.

## Gates

- Data gate: decoded names, source paths, row identity, requirements/options, and
  uncertainty notes must be recorded before product claims rely on legacy data.
- Preview gate: candidate visuals remain non-runtime until reviewed preview
  evidence is present.
- Runtime gate: H5 runtime loads only assets copied into `game-source`; it must
  never load directly from `/var/www/vltkpc`.
- Validation gate: packet, alias, equipment catalog, slot coverage, seed inventory,
  and known item option behavior must remain covered by smoke tests when porting
  scripts or generated equipment artifacts change.
- Skill gate: VLTKPC skill/effect packets (for example `Bổng Đả ác Cẩu` and `Kháng Long Hữu Hối`) require
  source SPR/SFX copy plus side-by-side parity artifacts before any `100%` claim.
- Map gate: VLTKPC map ports require active `MapList` identity, `.wor`/minimap PAK extraction evidence, copied local runtime assets, client `Region_C.dat` ground-layer evidence for gameplay background, and server region/NPC filtering evidence.
- Enemy gate: Map enemy templates may include only mobile combat NPC rows (`kind_normal=0` and positive `WalkSpeed` or `RunSpeed`); NPC dialogs and immobile templates such as `Bao cát` must remain excluded unless a later story explicitly changes scope.

## Current Limits

- The workflow now imports the equipment catalog and maps every attribute key
  present in that catalog; future attributes outside the current catalog must be
  traced to PC source before being claimed.
- SPR extraction and composition are build-time/tooling operations, not runtime
  direct reads from legacy PC folders.
- Visual approval is still manual unless a later story adds automated screenshot
  comparison or browser playtest artifacts.
- The known runtime sheets now cover 8 mounted-run directions and 8 mounted-idle
  directions. Runtime can select approved head/body wardrobe combo sheets from
  equipped items when a generated combo exists; arbitrary weapon/horse visual
  composition remains a preview-gated follow-up.
- The `Bổng Đả ác Cẩu` skill packet and runtime assets now include byte-accurate
  legacy-path extraction evidence, generated skill sheets, and side-by-side
  PNG/GIF parity artifacts.

- The `Kháng Long Hữu Hối` skill packet and runtime assets now include active PAK row evidence, `SKILL_MF_Spread` level-20 behavior, frame-compressed SPR extraction, generated skill sheets, and side-by-side PNG/GIF artifacts.

- The `Phi Long Tại Thiên` skill packet and runtime assets now include active PAK row evidence, `SKILL_MF_Wall` level-20 behavior, `MISSLE_MMK_Follow` homing, frame-compressed SPR extraction, generated skill sheets, all-directions visual proof, and a documented H5 `player-forward` adapter for forward-launch Wall/Follow skills.
- `Thiên Hạ Vô Cẩu` runtime evidence was corrected to active `SkillId=359`, `MissileId=168`, `tianxia_wugou` level-20 data, including 3 follow projectiles launched from the `player-forward` adapter.
- Current Cái Bang skill hit visuals are wired from VLTKPC `MS_DoCollision` / `AnimFile4`: BDAC and THVC use `mag_bz_huo3`, while KLHH and PLTT use `mag_gb_bz5`; H5 spawns the effect at the enemy collision point instead of inventing a new explosion.
- The `Ba Lăng huyện` map port now includes active `MapList` identity (`mapId=53`, path `两湖区\巴陵县`), `.wor`/`24.jpg` extraction evidence from `maps.pak`, generated runtime map metadata, a copied minimap, a `Region_C.dat`/`Ground.dat` rendered background, and mobile enemy templates `ani063`, `ani049`, and `ani061`; NPC labels and immobile templates are intentionally excluded.
