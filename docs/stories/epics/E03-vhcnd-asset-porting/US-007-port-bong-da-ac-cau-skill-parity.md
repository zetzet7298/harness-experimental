# US-007 Port Bổng Đả Ác Cẩu Skill Parity

## Status

implemented

## Lane

high-risk

## Product Contract

H5 prototype must port Cái Bang skill `Bổng Đả ác Cẩu` from VHCND into the current auto-fire loop with verified skill identity (`SkillId=125`, `MissleId=47`), level-20 cast profile, and preview-gated visual+SFX parity artifacts before claiming 100% match.

## Relevant Product Docs

- `docs/product/vhcnd-porting.md`
- `docs/product/current-state.md`

## Acceptance Criteria

- A normalized skill packet exists with source row, package-order evidence, script key, and missile/effect rows.
- Auto-fire runtime skill profile is updated to `Bổng Đả ác Cẩu` level-20 numeric behavior.
- Runtime wiring uses extracted source SPR/SFX and side-by-side PNG/GIF proofs are attached.
- Validation includes Python smoke + typecheck + build.

## Design Notes

- Source-of-truth package order remains `Client/package.ini` with active `slistcache.pak` rows.
- Extraction flow now supports non-ASCII legacy virtual paths via byte-accurate C hash semantics.
- Runtime now loads generated VLTK skill sheets and SFX in the auto-fire projectile lane.

## Validation

| Layer | Expected proof |
| --- | --- |
| Unit | `python3 tests/test_vltk_porting_smoke.py` includes skill packet identity and resolved/parity gate assertions. |
| Integration | `npm run typecheck` and `npm run build` must pass after runtime data update. |
| E2E | Passed: side-by-side PNG/GIF artifacts generated from extracted PC SPR frames and H5 runtime sheets. |
| Platform | Not applicable. |
| Release | Not defined. |

## Harness Delta

- Added this story and test-matrix row for skill-porting parity lane.

## Evidence

- `game-source/data/vltk-normalized/port-packets/skill-bong-da-ac-cau.json`
- `game-source/data/vltk-normalized/previews/skill-bong-da-ac-cau.report.json`
- `game-source/data/vltk-normalized/previews/skill-bong-da-ac-cau-side-by-side.png`
- `game-source/data/vltk-normalized/previews/skill-bong-da-ac-cau-side-by-side.gif`
- `game-source/src/data/skills.json`
- `game-source/scripts/vltk-extract-skill-assets.py`
- `game-source/scripts/vltk-compose-skill-bong-da-ac-cau.py`
- `game-source/tests/test_vltk_porting_smoke.py`

## Re-audit Notes

- 2026-05-18 re-audit corrected runtime level-20 speed to `missle_speed_v=32 -> projectileSpeed=512`, recorded `CastCircle`/`MoveKind=1` evidence, and added smoke assertions for 16 non-homing BDAC projectiles.

