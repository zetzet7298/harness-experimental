# VLTKPC Porting Contract

## Scope

This contract covers legacy VLTKPC/JX data and SPR assets used by the H5 game
prototype. It applies whenever work touches item identity, equipment visuals,
source SPRs, normalized packets, preview reports, or runtime spritesheets.

## Required Workflow

1. Resolve item identity and row evidence before visual work.
2. Normalize item/equipment evidence into packet or index artifacts under
   `game-source/data/vltk-normalized/`.
3. Generate or update preview PNG/report evidence before runtime wiring.
4. Copy required raw SPR sources into `game-source/public/assets/character/vltkpc/source/`.
5. Compose runtime sheets from local copied sources only.
6. Update this harness when the product contract, validation gates, or repeated
   porting workflow changes.

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
- Validation gate: packet and alias behavior must remain covered by smoke tests
  when the porting scripts or known loadout artifacts change.
- Skill gate: VLTKPC skill/effect packets (for example `Bổng Đả ác Cẩu` and `Kháng Long Hữu Hối`) require
  source SPR/SFX copy plus side-by-side parity artifacts before any `100%` claim.

## Current Limits

- The workflow proves one known equipped character path, not the full VLTKPC
  equipment catalog.
- SPR extraction and composition are build-time/tooling operations, not runtime
  gameplay systems.
- Visual approval is still manual unless a later story adds automated screenshot
  comparison or browser playtest artifacts.
- The known runtime sheets now cover 8 mounted-run directions and 8 mounted-idle
  directions with 10 frames per direction; this is still one known loadout, not
  generalized equipment swapping.
- The `Bổng Đả ác Cẩu` skill packet and runtime assets now include byte-accurate
  legacy-path extraction evidence, generated skill sheets, and side-by-side
  PNG/GIF parity artifacts.

- The `Kháng Long Hữu Hối` skill packet and runtime assets now include active PAK row evidence, `SKILL_MF_Spread` level-20 behavior, frame-compressed SPR extraction, generated skill sheets, and side-by-side PNG/GIF artifacts.

- The `Phi Long Tại Thiên` skill packet and runtime assets now include active PAK row evidence, `SKILL_MF_Wall` level-20 behavior, `MISSLE_MMK_Follow` homing, frame-compressed SPR extraction, generated skill sheets, all-directions visual proof, and a documented H5 `player-forward` adapter for forward-launch Wall/Follow skills.
- `Thiên Hạ Vô Cẩu` runtime evidence was corrected to active `SkillId=359`, `MissileId=168`, `tianxia_wugou` level-20 data, including 3 follow projectiles launched from the `player-forward` adapter.
- Current Cái Bang skill hit visuals are wired from VLTKPC `MS_DoCollision` / `AnimFile4`: BDAC and THVC use `mag_bz_huo3`, while KLHH and PLTT use `mag_gb_bz5`; H5 spawns the effect at the enemy collision point instead of inventing a new explosion.
