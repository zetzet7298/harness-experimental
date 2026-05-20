# US-008 Port Kháng Long Hữu Hối Skill Parity

## Status

implemented

## Lane

normal

## Product Contract

Port Cái Bang `Kháng Long Hữu Hối` from active VHCND data into the H5 runtime with evidence-backed skill identity, level-20 spread behavior, copied local SPR/SFX assets, generated runtime sheets, and validation artifacts.

## Relevant Product Docs

- `docs/product/vhcnd-porting.md`
- `docs/TEST_MATRIX.md`

## Acceptance Criteria

- Active PAK evidence identifies the Cái Bang row as `SkillId=128`, `ChildSkillId/MissileId=48`, `MisslesForm=2`, script key `kanglong_youhui`.
- Level-20 script overrides are recorded and wired: `skill_misslenum_v=15`, `skill_param1_v=2`, `missle_speed_v=32`, `skill_attackradius=512`.
- H5 runtime uses the KLHH projectile sheet instead of reusing the Bổng Đả sheet.
- Source SPR/SFX files are copied under `game-source/public/assets/skills/vhcnd/source/skill-khang-long-huu-hoi/` before runtime composition.
- Static checks, smoke tests, build, side-by-side asset proof, and browser smoke screenshot exist.

## Design Notes

- Request type: change request / skill port.
- Risk flags: existing behavior, weak proof until visual evidence added.
- PC cast form: `SKILL_MF_Spread`, not circle/wall/follow.
- Runtime mapping: current H5 skill speed convention uses `missle_speed_v * 16`; KLHH level 20 maps `32 -> 512 px/s`.
- Visual routing: projectile entities carry texture/animation metadata so multiple active VLTK skills can render different sheets in the same run.

## Validation

| Layer | Expected proof |
| --- | --- |
| Unit | `python3 tests/test_vltk_porting_smoke.py` |
| Integration | `npm run typecheck`; `npm run build` |
| E2E | Headless Chrome screenshot under `game-source/data/vltk-normalized/previews/browser/` |
| Platform | n/a |
| Release | n/a |

## Harness Delta

No structural harness changes. Added story and test matrix evidence for the new skill port.

## Evidence

- Packet: `game-source/data/vltk-normalized/port-packets/skill-khang-long-huu-hoi.json`.
- Extract report: `game-source/data/vltk-normalized/previews/skill-khang-long-huu-hoi.extract.report.json`.
- Side-by-side proof: `game-source/data/vltk-normalized/previews/skill-khang-long-huu-hoi-side-by-side.png` and `.gif`.
- Browser smoke: `game-source/data/vltk-normalized/previews/browser/skill-khang-long-huu-hoi-smoke.png`.
- Commands passed: `npm run typecheck`, `python3 tests/test_vltk_porting_smoke.py`, `npm run build`.
