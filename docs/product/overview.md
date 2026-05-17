# VLTK H5 Survivors Overview

## Product Goal

Build a browser-playable H5 survivor prototype that can eventually reuse verified
VLTK/JX data and visual assets while preserving provenance back to the legacy PC
source.

## Current Surface

- Runtime: Vite + TypeScript + Phaser in `/var/www/vltk-h5-survivors/game-source`.
- Primary surface: browser canvas sized for portrait mobile play.
- Current mode: offline prototype with local JSON fixtures and no server API.
- Current loop: mounted player, enemy spawning, auto projectiles, XP orbs, HUD
  debug stats, and stress target controls.
- Current VLTKPC visual proof: composed equipped male run sheet loaded from
  `public/assets/character/vltkpc/equipped-tu-la-giang-sa-staff-phien-vu-run.png`.

## Source Routing

- Harness docs/process: `/var/www/vltk-h5-survivors/harness-experimental`.
- H5 implementation/runtime assets: `/var/www/vltk-h5-survivors/game-source`.
- Legacy PC tables/source/assets: `/var/www/vltkpc`.
- GitNexus H5 repo: `vltk-h5-survivors`.
- GitNexus PC repo: `vltkpc`.
- GitNexus cross-repo group: `@vltk-porting`.

## Product Principles

- Keep the game playable offline until a story explicitly introduces backend or
  account persistence.
- Do not read runtime assets directly from `/var/www/vltkpc`; copy verified SPR
  sources into `game-source` before composition.
- Treat decoded VLTKPC rows, packet JSON, copied SPRs, preview PNGs, and reports
  as provenance artifacts, not disposable scratch files.
- Keep simulation/domain logic transport-neutral so future live data can replace
  fixtures without rewriting the game loop.

## Non-Goals For Current Brownfield Slice

- No production account system, server API, monetization, deployment, or native
  shell is defined.
- No full VLTK combat/stat parity is promised yet.
- No unreviewed candidate SPR should be wired into the runtime before preview
  gate evidence exists.

