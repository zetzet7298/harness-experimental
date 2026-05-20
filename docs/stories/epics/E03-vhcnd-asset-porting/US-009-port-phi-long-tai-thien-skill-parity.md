# US-009 Port Phi Long Tại Thiên Skill Parity

## Status

implemented

## Lane

normal

## Product Contract

Port Cái Bang `Phi Long Tại Thiên` level 20 from active VHCND data into the H5 runtime with evidence-backed skill identity, level-20 Wall/Follow behavior, copied local SPR/SFX assets, generated runtime sheets, and validation artifacts.

## Relevant Product Docs

- `docs/product/vhcnd-porting.md`
- `docs/TEST_MATRIX.md`

## Acceptance Criteria

- Active PAK evidence identifies `Phi Long Tại Thiên` as `SkillId=357`, `ChildSkillId/MissileId=166`, `MisslesForm=0`, script key `feilong_zaitian`.
- Level-20 script overrides are recorded and wired: `skill_misslenum_v=4`, `missle_speed_v=24`, `skill_attackradius=512`, `skill_cost_v=65`.
- Missile movement is `MoveKind=5`, so runtime projectiles home/follow the selected enemy.
- H5 runtime uses the FLTT projectile sheet and `projectileScale=1.0` from active `AnimFile2` evidence, not Bổng Đả scale.
- H5 survivor adapter launches the Wall from in front of the character while preserving player-to-target direction, because auto-targeting otherwise places the PC target/reference point far away from the character.
- Source SPR/SFX are copied under `game-source/public/assets/skills/vhcnd/source/skill-phi-long-tai-thien/` and runtime sheets are generated under `game-source/public/assets/skills/vhcnd/`.
- Validation covers packet values, runtime skill data, source asset resolution, all-directions/all-frames visual proof, and enemy-hit collision effects from PC `MS_DoCollision` / `AnimFile4`.

## Evidence

- Active extraction manifest: `/tmp/vltk-thvc-fltt-port/manifest.tsv`.
- Active skill row: `/tmp/vltk-thvc-fltt-port/pak_utf8/settings__Skills.txt__slistcache.txt:358`.
- Active missile row: `/tmp/vltk-thvc-fltt-port/pak_utf8/settings__Missles.txt__slistcache.txt:167`.
- Active level script: `/tmp/vltk-thvc-fltt-port/pak_utf8/script__skill__gaibang.lua__slistcache.txt:142-194`.
- Engine dynamic overrides: `/var/www/vhcnd/extracted_build_jxwin_soucgoc_hoiquanvolam/source_from_vmdk/SourceNew/swrod3/SwordOnline/Sources/Core/Src/Skill/KMissleSkill.cpp:1238-1279`.
- Engine Wall formula: `/var/www/vhcnd/extracted_build_jxwin_soucgoc_hoiquanvolam/source_from_vmdk/SourceNew/swrod3/SwordOnline/Sources/Core/Src/KSkills.cpp:604-665` and `:1398-1514`.
- Engine Follow movement: `/var/www/vhcnd/extracted_build_jxwin_soucgoc_hoiquanvolam/source_from_vmdk/SourceNew/swrod3/SwordOnline/Sources/Core/Src/KMissle.cpp:745-767`.
- Enemy-hit collision effect uses PC `MS_DoCollision` / `AnimFile4`: `SkillDef.h:127-132`, `KMissle.cpp:1011-1022`, `KMissle.cpp:1094-1124`.

## Validation

- `npm run typecheck` passed.
- `python3 tests/test_vltk_porting_smoke.py` passed, 16 tests.
- `npm run build` passed with existing Vite chunk-size warning.
- Visual proof artifacts:
  - `game-source/data/vltk-normalized/previews/skill-phi-long-tai-thien-side-by-side.png`
  - `game-source/data/vltk-normalized/previews/skill-phi-long-tai-thien-side-by-side.gif`
  - `game-source/data/vltk-normalized/previews/skill-phi-long-tai-thien-allframes.png`

## Notes

- `Thiên Hạ Vô Cẩu` was corrected in the same pass because its packet/runtime profile was still mixed with Bổng Đả evidence. Active THVC evidence is `SkillId=359`, `MissileId=168`, `scriptKey=tianxia_wugou`, level-20 `skill_misslenum_v=3`, `MoveKind=5`.
- PC `CastWall` uses a target/reference coordinate. In the H5 survivor loop, the target is auto-selected and often far away; forward-launch Cái Bang Wall/Follow skills use a documented `player-forward` adapter to match the visible PC behavior of the skill launching from in front of the character.
