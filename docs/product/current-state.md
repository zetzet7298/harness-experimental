# Brownfield Current State

## Done

- Vite/TypeScript/Phaser project exists in `/var/www/vltk-h5-survivors/game-source`.
- Package scripts exist for `dev`, `build`, `preview`, and `typecheck`.
- Phaser scene stack exists: `BootScene`, `PreloadScene`, `GameScene`, and
  `HudScene`.
- Offline gateway loads local profile, inventory, skills, waves, and VLTK bridge
  sample fixtures from `src/data/`.
- Survivor simulation exists with fixed-step update, pooled enemies/projectiles,
  XP orbs, leveling, collision checks, and stress target controls.
- HUD displays level, XP, equipped weapon, physical damage, defense, poison/all
  resist, unsupported equipment attribute count, FPS, elapsed time, kills, pool
  sizes, and stress target instructions.
- VLTKPC equipped character runtime sheets are loaded by `PreloadScene` using
  player sheet constants, with 8 mounted-run direction animations and separate
  mounted-idle standing animations.
- `GameScene` supports keyboard/WASD and touch-anywhere joystick movement, with
  player facing selected from the movement vector.
- VLTKPC asset/data porting scripts exist under `scripts/` with documented packet,
  preview, source-copy, and compose workflow.
- Normalized VLTKPC data artifacts exist under `data/vltk-normalized/`, including
  aliases, equipment index, packets, previews, and a PAK SPR manifest.
- Generated VLTKPC equipment catalog and seed inventory exist in
  `game-source/src/data/equipmentCatalog.json` and `game-source/src/data/inventory.json`,
  covering all 11 PC equipment slots with one mobile bag cell per item.
- Portrait `EquipmentScene` starts before runs, supports equip/unequip with
  `localStorage` persistence, and run startup applies the same equipped loadout to
  inventory-derived stats.
- Equipment catalog visual metadata expands horse/body/weapon runtime SPR parts so
  build-time tools can extract exact loadout source sprites from catalog items.
- Current exact equipped loadout packets can be generated from catalog+inventory
  for mounted run/idle; they remain preview-gated and are not runtime-wired until
  visual review passes.
- Runtime-copied SPR sources exist under `public/assets/character/vltkpc/source/`.
- Smoke tests exist for the VLTKPC porting packet and alias behavior in
  `tests/test_vltk_porting_smoke.py`.
- Equipment browser smoke screenshots exist under
  `game-source/artifacts/screenshots/2026-05-18-equipment-*.png` with a JSON
  report for equip/unequip/run handoff.
- Normalized skill packet for Cái Bang `Bổng Đả ác Cẩu` (`SkillId=125`,
  `MissleId=47`) is wired into auto-fire with extracted source SPR/SFX, generated
  runtime sheets, and side-by-side PNG/GIF parity artifacts.

## In Progress

- Brownfield harness synchronization is now established; future game-source work
  must keep product docs, story packets, validation matrix, and architecture docs
  current.
- VLTKPC porting workflow is packet/preview/report based. Equipment data now has
  catalog-wide table import, while arbitrary in-run visual composition still
  requires preview-gated asset generation for weapon/horse/body combinations.
- Prototype data is partially generated from VLTKPC tables; non-equipment real
  table import remains documented as a later story in `game-source/src/data/README.md`.

## Not Done

- No production persistence, backend, auth, economy, networking, deployment, or
  release pipeline is defined.
- Visual approval is still manual; side-by-side PNG/GIF artifacts now exist for
  `Bổng Đả ác Cẩu`, but no automatic pixel-diff gate exists yet.
- No generalized non-equipment VLTK item/stat import has replaced `src/data/vltk-samples.json`.
- Every magic/base attribute key present in the generated equipment catalog is now
  mapped into runtime stat or audit fields; VLTKPC attributes outside the current
  catalog still require source-backed handling before future expansion claims.
- In-run equipment visual sync currently selects approved head/body combo sheets
  when available; arbitrary weapon/horse visual composition remains a later
  preview-gated step.
- No generalized multi-skill VLTK action animation set beyond the current mounted
  loadout plus Cái Bang skill lanes is wired into runtime gameplay.
- No CI exists for `game-source` validation commands.

## Evidence Snapshot

- `game-source/package.json` defines `build` and `typecheck` scripts.
- `game-source/src/game/constants.ts` points the player sheet at the VLTKPC
  equipped runtime PNG.
- `game-source/scripts/README.md` documents the one-command loadout gate and
  preview-before-compose rule.
- `game-source/docs/VLTKPC_SPR_PORTING_PLAYBOOK.md` documents the project-wide
  asset porting workflow.
- `game-source/tests/test_vltk_porting_smoke.py` verifies known good packet SPRs
  and alias resolution.

- `game-source/src/domain/equipment.ts` contains the supported equipment requirement/stat aggregation rules.
- `docs/validation/2026-05-18-vltkpc-equipment-system-port.md` records the equipment-system validation pass.
