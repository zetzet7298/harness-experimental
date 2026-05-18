# Test Matrix

This file maps product behavior to proof for the brownfield H5 game source at
`/var/www/vltk-h5-survivors/game-source`.

## Status Values

| Status | Meaning |
| --- | --- |
| planned | Accepted as intended behavior, not implemented |
| in_progress | Actively being built |
| implemented | Implemented and proof exists |
| changed | Contract changed after earlier implementation |
| retired | No longer part of the product contract |

## Matrix

| Story | Contract | Unit | Integration | E2E | Platform | Status | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `US-001` | Brownfield state is documented in harness product docs | n/a | `srcwalk` inspection | n/a | n/a | implemented | `docs/product/current-state.md`; `docs/stories/epics/E01-brownfield-baseline/US-001-document-brownfield-state.md` |
| `US-002` | Offline Phaser survivor loop boots and runs from local fixtures | no | passed: `npm run typecheck`, `npm run build` | planned browser smoke | n/a | implemented | `game-source/src/game/*`; `game-source/src/systems/simulation.ts`; `docs/validation/2026-05-17-brownfield-docs.md` |
| `US-003` | VLTKPC porting gates preserve packet, preview, copied source, and alias behavior | passed: `python3 tests/test_vltk_porting_smoke.py` | script/report artifacts present | planned browser visual smoke | n/a | implemented | `docs/product/vltkpc-porting.md`; `docs/validation/2026-05-17-brownfield-docs.md` |
| `US-004` | Real VLTK table import replaces/expands fixture bridge data | planned | planned | n/a | n/a | planned | `docs/stories/epics/E03-vltkpc-asset-porting/US-004-import-real-vltk-tables.md` |
| `US-005` | Browser smoke report captures runtime visual/HUD/console health | n/a | build/typecheck prerequisite | planned | local browser | planned | `docs/stories/epics/E02-h5-survivors-prototype/US-005-capture-browser-smoke.md` |
| `US-006` | Known VLTKPC equipped character renders 4-item loadout with 8-direction run, mounted idle, and touch joystick input | passed: `python3 tests/test_vltk_porting_smoke.py` | passed: `npm run typecheck`, `npm run build` | passed: local Playwright smoke screenshot | local browser | implemented | `docs/stories/epics/E03-vltkpc-asset-porting/US-006-fix-equipped-character-visuals-and-8-direction-input.md`; `docs/validation/2026-05-17-equipped-character-8dir-joystick.md`; `/tmp/vltk-h5-smoke.png` |
| `US-007` | Cái Bang `Bổng Đả ác Cẩu` skill packet + runtime profile are ported with side-by-side visual/SFX parity artifacts and `MS_DoCollision` impact wiring | passed: `python3 tests/test_vltk_porting_smoke.py` | passed: `npm run typecheck`, `npm run build` | passed: side-by-side PNG/GIF proof artifacts | local browser | implemented | `docs/stories/epics/E03-vltkpc-asset-porting/US-007-port-bong-da-ac-cau-skill-parity.md`; `docs/validation/2026-05-18-bong-da-ac-cau-parity.md`; `game-source/data/vltk-normalized/port-packets/skill-bong-da-ac-cau.json`; `game-source/data/vltk-normalized/previews/skill-bong-da-ac-cau-side-by-side.png`; `game-source/data/vltk-normalized/previews/skill-bong-da-ac-cau-side-by-side.gif` |
| `US-008` | Cái Bang `Kháng Long Hữu Hối` skill packet + level-20 movement-facing spread runtime profile is ported with side-by-side visual/SFX artifacts and `MS_DoCollision` impact wiring | passed: `python3 tests/test_vltk_porting_smoke.py` | passed: `npm run typecheck`, `npm run build` | passed: headless Chrome smoke screenshot | local browser | implemented | `docs/stories/epics/E03-vltkpc-asset-porting/US-008-port-khang-long-huu-hoi-skill-parity.md`; `docs/validation/2026-05-18-khang-long-huu-hoi-parity.md`; `game-source/data/vltk-normalized/port-packets/skill-khang-long-huu-hoi.json`; `game-source/data/vltk-normalized/previews/skill-khang-long-huu-hoi-side-by-side.png`; `game-source/data/vltk-normalized/previews/browser/skill-khang-long-huu-hoi-smoke.png` |
| `US-009` | Cái Bang `Phi Long Tại Thiên` level-20 Wall/Follow skill and THVC forward-origin/visibility/scale/collision-effect correction and PLTT lane separation/collision-effect wiring are source-backed and wired into H5 runtime | passed: `python3 tests/test_vltk_porting_smoke.py` | passed: `npm run typecheck`, `npm run build` | passed: side-by-side PNG/GIF + all-frames FLTT proof artifacts | local browser/user runtime review | implemented | `docs/stories/epics/E03-vltkpc-asset-porting/US-009-port-phi-long-tai-thien-skill-parity.md`; `docs/validation/2026-05-18-phi-long-tai-thien-parity.md`; `game-source/data/vltk-normalized/port-packets/skill-phi-long-tai-thien.json`; `game-source/data/vltk-normalized/port-packets/skill-thien-ha-vo-cau.json`; `game-source/data/vltk-normalized/previews/skill-phi-long-tai-thien-allframes.png`; `game-source/data/vltk-normalized/previews/browser/skill-impact-smoke.png` |

## Evidence Rules

- Unit proof covers pure domain and application rules.
- Integration proof covers backend enforcement, data integrity, provider
  behavior, jobs, or service contracts.
- E2E proof covers user-visible browser flows.
- Platform proof covers only shell, deployment, mobile, desktop, or runtime
  behavior that cannot be proven in lower layers.
- A story can be implemented without every proof column if the story packet
  explains why.
