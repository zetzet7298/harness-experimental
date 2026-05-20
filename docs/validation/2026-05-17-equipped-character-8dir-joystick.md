# Equipped Character 8-Direction + Joystick Validation

Date: 2026-05-17

## Scope

Validated the H5 runtime change for the known VHCND mounted loadout:
`Phiên Vũ`, `Địch Khái Trúc Trượng`, `Tu La phát kết`, and `Giáng Sa bào`,
including mounted-run and mounted-idle visuals.

## Commands

```bash
cd /var/www/vltk-h5-survivors/game-source
python3 tests/test_vltk_porting_smoke.py
npm run typecheck
npm run build
npm run dev -- --host 127.0.0.1 --port 5174
node /tmp/vltk-playwright-smoke/smoke.js
```

## Results

- `python3 tests/test_vltk_porting_smoke.py`: passed 7 tests.
- `npm run typecheck`: passed.
- `npm run build`: passed; Vite emitted only the existing chunk-size warning.
- Browser smoke: loaded one canvas, captured idle and run screenshots, exercised
  pointer and keyboard input, and reported no fatal console errors.

## Evidence

- Preview report: `game-source/data/vltk-normalized/previews/equipped-phien-vu-dich-khai-loadout.report.json`
- Runtime metadata: `game-source/public/assets/character/vhcnd/equipped-tu-la-giang-sa-staff-phien-vu-run.json`
- Idle runtime metadata: `game-source/public/assets/character/vhcnd/equipped-tu-la-giang-sa-staff-phien-vu-idle.json`
- Idle screenshot: `/tmp/vltk-h5-idle-after-move-smoke.png`
- Run screenshot: `/tmp/vltk-h5-run-smoke.png`
- Corrected visual mapping screenshot: `/tmp/vltk-h5-touch-down-release-idle-smoke.png`

## Notes

- Optional `MA_HR_010_HR01.spr` and `MA_SH_034_HR01.spr` remain absent in current PAK evidence and were not guessed.
- Runtime still loads only copied repo-local assets under `game-source/public/assets/character/vhcnd/`.
- Run animation frame rate is 12fps; idle animation frame rate is 6fps.
- Follow-up correction: mirrored the working horse/weapon pipeline through `KNpcRes`: `KItemChangeRes` returns `tableValue - 2` into NPC fields, while `KNpcRes::SetHelm` and `SetArmor` use the NpcRes `equipNo` rows that correspond to the resource table value, so `Tu La phát kết` uses `MA_HD_010_*` and `Giáng Sa bào` uses `MA_BD/LH/RH_034_*`.
