# Harness Backlog

Use this file when an agent discovers a missing harness capability but should
not change the operating model immediately.

## Template

```md
## Missing Harness Capability

### Title

Short name.

### Discovered While

Task or story that exposed the gap.

### Current Pain

What was hard, repeated, ambiguous, or unsafe?

### Suggested Improvement

What should be added or changed?

### Risk

Tiny, normal, or high-risk.

### Status

proposed | accepted | implemented | rejected
```

## Items

## Missing Harness Capability

### Title

Browser smoke driver for equipment loadout

### Discovered While

Spec task 13.1 of `vltk-equipment-system` — wire the browser smoke driver at
`game-source/tests/smoke/equipment-loadout.smoke.ts` that opens the dev
server, equips the canonical 3-piece loadout (`Tu La phát kết` /
`Giáng Sa bào` / `Địch Khái Lục Ngọc Trượng`), taps `Run`, and screenshot
diffs the first idle frame of `GameScene` against
`tests/smoke/equipment-loadout.spec.ts-snapshots/equipment-loadout-3piece-chromium-linux.png`.

### Current Pain

(Resolved.) `game-source/package.json` previously had no browser-automation
dependency, so requirements 11.1, 11.2, 11.3, and 11.6 could not be proven
end-to-end. `@playwright/test` is now installed and the smoke is wired.

### Suggested Improvement

(Resolved.) Implementation:

- Added `@playwright/test` as a `devDependency` of `game-source`.
- Added `npm run test:smoke` script that runs `playwright test`.
- Added `playwright.config.ts` that boots `npm run dev` via `webServer`
  and targets a 390×844 portrait viewport.
- The driver at `game-source/tests/smoke/equipment-loadout.spec.ts`
  pre-seeds `localStorage[EQUIPMENT_STORAGE_KEY]` with the 3-piece loadout
  (canvas hit-testing avoided on purpose), invokes
  `EquipmentScene.startRun()` directly, waits for `GameScene` activation
  and the first idle frame, hides simulation sprite pools (enemies,
  projectiles, orbs, impacts), pauses the scene + global anims +
  Phaser main loop, and screenshot-diffs the canvas at a 10% threshold.
- A deterministic LCG-stubbed `Math.random` keeps enemy spawn positions
  byte-stable across reloads (`SurvivorSimulation` reads `Math.random`
  on spawn).
- The baseline PNG was captured on first run with
  `npm run test:smoke -- --update-snapshots` and verified stable across
  5 consecutive reruns.

### Risk

Normal. Adds a `devDependency` and a CI job, but the runtime impact is
contained to the smoke command. The screenshot baseline must be regenerated
whenever the SPR pipeline regenerates the manifest entry; refresh with
`npm run test:smoke -- --update-snapshots`.

### Status

implemented

