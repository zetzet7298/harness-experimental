# US-005 Capture Browser Smoke

## Status

planned

## Lane

normal

## Product Contract

The H5 prototype needs a repeatable browser smoke report covering boot, runtime
rendering, HUD, stress controls, and console health.

## Relevant Product Docs

- `docs/product/roadmap.md`
- `docs/product/current-state.md`

## Acceptance Criteria

- Start the Vite dev server or preview server from game-source.
- Open the browser prototype and confirm canvas boot.
- Capture a screenshot showing mounted player, enemies/projectiles/orbs when
  available, and HUD text.
- Exercise stress target controls and record whether FPS/HUD remains responsive.
- Save console/runtime errors or confirm none were observed.

## Design Notes

- Use `game-studio:game-playtest` or `browser-navigation` when this story is
  selected.
- Do not treat build/typecheck as a substitute for browser evidence.

## Validation

| Layer | Expected proof |
| --- | --- |
| Unit | Not applicable. |
| Integration | Build/typecheck before browser smoke. |
| E2E | Browser screenshot/report. |
| Platform | Local browser runtime only. |
| Release | Not applicable. |

## Harness Delta

- Add a validation report under `docs/validation/` after smoke is run.

## Evidence

- Pending.

