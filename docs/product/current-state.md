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
- HUD displays level, XP, weapon, FPS, elapsed time, kills, pool sizes, and stress
  target instructions.
- VLTKPC equipped character runtime sheets are loaded by `PreloadScene` using
  player sheet constants, with 8 mounted-run direction animations and separate
  mounted-idle standing animations.
- `GameScene` supports keyboard/WASD and touch-anywhere joystick movement, with
  player facing selected from the movement vector.
- VLTKPC asset/data porting scripts exist under `scripts/` with documented packet,
  preview, source-copy, and compose workflow.
- Normalized VLTKPC data artifacts exist under `data/vltk-normalized/`, including
  aliases, equipment index, packets, previews, and a PAK SPR manifest.
- Runtime-copied SPR sources exist under `public/assets/character/vltkpc/source/`.
- Smoke tests exist for the VLTKPC porting packet and alias behavior in
  `tests/test_vltk_porting_smoke.py`.

## In Progress

- Brownfield harness synchronization is now established; future game-source work
  must keep product docs, story packets, validation matrix, and architecture docs
  current.
- VLTKPC porting workflow is packet/preview/report based, but still centered on a
  known equipped loadout rather than generalized runtime equipment swapping.
- Prototype data remains fixture-based; real table import is documented as a
  later story in `game-source/src/data/README.md`.

## Not Done

- No production persistence, backend, auth, economy, networking, deployment, or
  release pipeline is defined.
- No end-to-end browser smoke test has been captured in the harness yet.
- No visual approval artifact is tracked in the harness beyond paths to preview
  PNG/report files in game-source.
- No generalized VLTK item/stat import has replaced `src/data/vltk-samples.json`.
- No generalized action animation set beyond the current mounted-run sheet is
  wired into the gameplay runtime.
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
