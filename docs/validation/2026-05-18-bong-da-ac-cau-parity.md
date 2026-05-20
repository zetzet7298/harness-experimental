# Bổng Đả Ác Cẩu Porting Validation Report

Date: 2026-05-18

## Scope

- Port Cái Bang skill `Bổng Đả ác Cẩu` (`SkillId=125`, `MissleId=47`) into H5 auto-fire lane.
- Preserve VHCND package-order truth and produce side-by-side visual parity artifacts.

## Commands Run

From `/var/www/vltk-h5-survivors/game-source`:

```bash
python3 scripts/vltk-port-skill.py
python3 scripts/vltk-extract-skill-assets.py
python3 scripts/vltk-compose-skill-bong-da-ac-cau.py
python3 tests/test_vltk_porting_smoke.py
npm run typecheck
npm run build
```

All commands completed successfully.

## Evidence Artifacts

- Skill packet: `data/vltk-normalized/port-packets/skill-bong-da-ac-cau.json`
- Preview gate report: `data/vltk-normalized/previews/skill-bong-da-ac-cau.report.json`
- Extract report: `data/vltk-normalized/previews/skill-bong-da-ac-cau.extract.report.json`
- Side-by-side PNG: `data/vltk-normalized/previews/skill-bong-da-ac-cau-side-by-side.png`
- Side-by-side GIF: `data/vltk-normalized/previews/skill-bong-da-ac-cau-side-by-side.gif`
- Runtime sheets/meta:
  - `public/assets/skills/vhcnd/bong-da-ac-cau-main.png`
  - `public/assets/skills/vhcnd/bong-da-ac-cau-main.json`
  - `public/assets/skills/vhcnd/bong-da-ac-cau-impact.png`
  - `public/assets/skills/vhcnd/bong-da-ac-cau-impact.json`
  - `public/assets/skills/vhcnd/bong-da-ac-cau-precast.png`
  - `public/assets/skills/vhcnd/bong-da-ac-cau-precast.json`

## Notes

- Legacy non-ASCII virtual paths are resolved using byte-accurate file-id hashing that matches engine C semantics.
- Runtime auto-fire now loads VLTK skill visual/SFX assets from copied local repo paths only.

## Re-audit 2026-05-18

Scope: review `Bổng Đả ác Cẩu` again after `Thiên Hạ Vô Cẩu` work because the earlier runtime profile could be stale.

Evidence checked:

- Active package extraction manifest: `/tmp/vltk-bdac-audit/manifest.tsv`, where `slistcache.pak` is the active first hit for `\settings\Skills.txt`, `\settings\Missles.txt`, and `\script\skill\gaibang.lua`.
- Active skill row: `/tmp/vltk-bdac-audit/pak_utf8/settings__Skills.txt__slistcache.txt:126`, `SkillId=125`, `MisslesForm=3`, `ChildSkillId=47`, `ChildSkillNum=16`, `Param1=0`, `Param2=0`, `LvlData=bangda_egou`.
- Active script profile: `/tmp/vltk-bdac-audit/pak_utf8/script__skill__gaibang.lua__slistcache.txt:82`, `bangda_egou`; level 20 has `missle_speed_v=32`, `skill_attackradius=512`, `physicsenhance_p=179`, `seriesdamage_p=50`, `firedamage_v=360..420`, `skill_cost_v=48`, and no `skill_misslenum_v` override.
- Active missile row: `/tmp/vltk-bdac-audit/pak_utf8/settings__Missles.txt__slistcache.txt:48`, `MissleId=47`, `MoveKind=1`, `LifeTime=16`, missile sprite `AnimFile2`, impact sprite `AnimFile4`, hit sound `SndFile2`.
- Engine enum: `SkillDef.h:104-115`, where `MoveKind=1` is `MISSLE_MMK_Line` and `MoveKind=5` is follow/homing.
- Engine cast formula: `KMissleSkill.cpp:729-848`, `CastCircle`; `Param1=0` means reference point is source/player and `nDirPerNum = MaxMissleDir / m_nChildSkillNum`.
- Dynamic override engine: `KMissleSkill.cpp:1239-1272`, where `skill_misslenum_v`, `skill_misslesform_v`, `skill_param1_v`, and `skill_param2_v` are the only dynamic cast-shape overrides relevant here.

Corrections applied:

- Updated H5 BDAC runtime profile from `projectileSpeed=320` to `512`, matching active level-20 `missle_speed_v=32` with the existing H5 VLTK missile-speed scale `*16`.
- Added explicit runtime metadata for `vltkSkillLevel=20`, `vltkMissileMoveKind=1`, `vltkMissileSpeed=32`, `vltkAttackRadius=512`, `projectileCount=16`, and `homing=false`.
- Enriched the normalized BDAC packet with `castProfile`, level-20 magic values, and engine evidence so later agents do not infer circle/homing behavior from memory.
- Added smoke assertions for BDAC cast profile and runtime level-20 values.

Commands run after re-audit:

```bash
npm run typecheck
python3 tests/test_vltk_porting_smoke.py
npm run build
```

Result: all passed. Browser visual replay was not rerun in this re-audit because source SPR/SFX/runtime sheet artifacts did not change; only numeric runtime profile metadata and projectile speed changed.

