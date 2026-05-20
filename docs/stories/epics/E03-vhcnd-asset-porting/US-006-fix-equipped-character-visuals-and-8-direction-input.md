# US-006 Fix Equipped Character Visuals And 8-Direction Input

## Status

implemented

## Lane

high-risk

## Product Contract

The H5 prototype must render the known mounted VHCND loadout with `Tu La phát kết`, `Giáng Sa bào`, `Phiên Vũ`, and `Địch Khái Trúc Trượng`, using copied local SPR sources, preview-gated runtime composition, 8-direction mounted-run animation, mounted-idle standing visuals, and touch-anywhere joystick movement.

## Relevant Product Docs

- `docs/product/vhcnd-porting.md`
- `docs/product/current-state.md`

## Acceptance Criteria

- Loadout packet records source rows and SPR parts for helm, armor, horse, and weapon.
- Runtime sheet is composed as 8 direction rows by 10 frames per direction after preview passes.
- Mounted idle uses `骑马站立` RD01 sprites when the player is not moving.
- Mounted run animation plays slightly faster than before.
- Phaser preload creates one mounted-run animation per direction and gameplay chooses direction from movement vector.
- Touch input starts a joystick at the touch position while keyboard/WASD and stress buttons remain usable.
- Smoke tests, typecheck, and build pass in `game-source`.

## Design Notes

- Runtime assets remain under `game-source/public/assets/character/vhcnd/` and never load from `/var/www/vhcnd`.
- Optional `MA_HR_010_HR01.spr` and `MA_SH_034_HR01.spr` are recorded as missing optional PAK evidence rather than guessed.
- Helm and armor visual rows mirror the working horse/weapon path: PC computes NPC fields with `tableValue - 2`, then `KNpcRes` indexes NpcRes `equipNo` rows, yielding `MA_HD_010_*` and `MA_BD/LH/RH_034_*`.
- Direction metadata uses south-first SPR row order: south, southwest, west, northwest, north, northeast, east, southeast.
- Run animation frame rate is 12fps; idle animation frame rate is 6fps.

## Validation

| Layer | Expected proof |
| --- | --- |
| Unit | `python3 tests/test_vltk_porting_smoke.py` passed 7 tests on 2026-05-17. |
| Integration | `npm run typecheck` and `npm run build` passed on 2026-05-17. |
| E2E | Local Playwright smoke loaded one canvas, exercised pointer/keyboard input, and captured `/tmp/vltk-h5-smoke.png` with no fatal console errors. |
| Platform | Not applicable. |
| Release | Not defined. |

## Harness Delta

- Added this story and updated product/test matrix references for the new runtime visual/input contract.

## Evidence

- `game-source/data/vltk-normalized/port-packets/equipped-phien-vu-dich-khai-loadout.json`
- `game-source/data/vltk-normalized/previews/equipped-phien-vu-dich-khai-loadout.report.json`
- `game-source/public/assets/character/vhcnd/equipped-tu-la-giang-sa-staff-phien-vu-run.json`
- `game-source/public/assets/character/vhcnd/equipped-tu-la-giang-sa-staff-phien-vu-idle.json`
- `python3 tests/test_vltk_porting_smoke.py`
- `npm run typecheck`
- `npm run build`
- `/tmp/vltk-h5-smoke.png`
- `docs/validation/2026-05-17-equipped-character-8dir-joystick.md`
