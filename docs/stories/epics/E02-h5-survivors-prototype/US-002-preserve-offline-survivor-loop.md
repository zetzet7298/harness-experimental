# US-002 Preserve Offline Survivor Loop

## Status

implemented

## Lane

normal

## Product Contract

The browser prototype must boot locally, run an offline survivor loop, render the
mounted VLTKPC player sheet, and expose HUD/stress signals useful for debugging.

## Relevant Product Docs

- `docs/product/overview.md`
- `docs/product/current-state.md`

## Acceptance Criteria

- Phaser scene stack loads Boot, Preload, Game, and HUD scenes.
- Offline gateway loads local fixtures without requiring a backend.
- Simulation updates player, enemies, projectiles, XP orbs, kills, levels, and
  stress target state.
- HUD reports debug stats and stress controls.
- Runtime player sheet is served from `game-source/public/assets`, not `/var/www/vltkpc`.

## Design Notes

- Runtime stack: Vite, TypeScript, Phaser.
- UI surface: portrait browser canvas.
- Data source: local JSON fixtures through `LocalOfflineGateway`.
- Runtime asset: `PLAYER_SHEET.path` points at a copied/composed public asset.

## Validation

| Layer | Expected proof |
| --- | --- |
| Unit | No dedicated unit tests yet. |
| Integration | `npm run typecheck` and `npm run build` in game-source passed on 2026-05-17. |
| E2E | Planned browser smoke/playtest report. |
| Platform | Not applicable until deployment/native shell exists. |
| Release | Not defined. |

## Harness Delta

- Added product/current-state contract and matrix row for the offline prototype.

## Evidence

- `game-source/package.json` defines `build` and `typecheck`.
- `game-source/src/game/createGame.ts` wires the scene stack.
- `game-source/src/game/scenes/PreloadScene.ts` loads the player sheet and
  creates placeholder textures.
- `game-source/src/game/scenes/GameScene.ts` renders simulation snapshots.
- `game-source/src/game/scenes/HudScene.ts` displays debug stats and stress
  buttons.
- `game-source/src/systems/simulation.ts` owns the offline survivor loop.
- `npm run typecheck` passed in `game-source` on 2026-05-17.
- `npm run build` passed in `game-source` on 2026-05-17 with only the existing
  large chunk warning for the bundled Phaser app.
