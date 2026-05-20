# 2026-05-18 Kháng Long Hữu Hối Parity Validation

## Scope

Port Cái Bang `Kháng Long Hữu Hối` to H5 from active VHCND evidence, including level-20 spread behavior and copied local SPR/SFX runtime assets.

## Source Evidence

- Active extraction manifest: `/tmp/vltk-klhh-port/manifest.tsv`.
- Active skill row: `/tmp/vltk-klhh-port/pak_utf8/settings__Skills.txt__slistcache.txt:129`.
- Active missile row: `/tmp/vltk-klhh-port/pak_utf8/settings__Missles.txt__slistcache.txt:49`.
- Active level script: `/tmp/vltk-klhh-port/pak_utf8/script__skill__gaibang.lua__slistcache.txt:109-132`.
- Engine form enum: `/var/www/vhcnd/extracted_build_jxwin_soucgoc_hoiquanvolam/source_from_vmdk/SourceNew/swrod3/SwordOnline/Sources/Core/Src/Skill/SkillDef.h:214-224`.
- Engine move enum: `/var/www/vhcnd/extracted_build_jxwin_soucgoc_hoiquanvolam/source_from_vmdk/SourceNew/swrod3/SwordOnline/Sources/Core/Src/Skill/SkillDef.h:104-115`.
- Engine spread formula: `/var/www/vhcnd/extracted_build_jxwin_soucgoc_hoiquanvolam/source_from_vmdk/SourceNew/swrod3/SwordOnline/Sources/Core/Src/Skill/KMissleSkill.cpp:870-1019`.
- Dynamic override handling: `/var/www/vhcnd/extracted_build_jxwin_soucgoc_hoiquanvolam/source_from_vmdk/SourceNew/swrod3/SwordOnline/Sources/Core/Src/Skill/KMissleSkill.cpp:1239-1272`.

## Confirmed Values

- `SkillId=128`.
- `ChildSkillId/MissileId=48`.
- Base `MisslesForm=2`, `SKILL_MF_Spread`.
- Base `ChildSkillNum=8`; level 20 effective `skill_misslenum_v=15`.
- Base `Param1=3`; level 20 effective `skill_param1_v=2`.
- `Param2=1`.
- Level 20 `missle_speed_v=32`, `skill_attackradius=512`, `skill_cost_v=50`, `seriesdamage_p=50`, `firedamage_v=536`.
- Missile `MoveKind=1`, so H5 `homing=false`.
- Main animation `AnimFileInfo=80,16,1`, composed as 16 directions and 5 frames per direction.

## Runtime Artifacts

- Packet: `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/port-packets/skill-khang-long-huu-hoi.json`.
- Runtime main sheet/meta: `/var/www/vltk-h5-survivors/game-source/public/assets/skills/vhcnd/khang-long-huu-hoi-main.png` and `.json`.
- Copied source: `/var/www/vltk-h5-survivors/game-source/public/assets/skills/vhcnd/source/skill-khang-long-huu-hoi/`.
- Side-by-side proof: `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/previews/skill-khang-long-huu-hoi-side-by-side.png` and `.gif`.
- Browser smoke: `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/previews/browser/skill-khang-long-huu-hoi-smoke.png`.

## Validation Commands

- `npm run typecheck` passed.
- `python3 tests/test_vltk_porting_smoke.py` passed, 13 tests.
- `npm run build` passed with the existing Vite chunk-size warning.
- `google-chrome --headless=new --disable-gpu --no-sandbox --window-size=390,844 --virtual-time-budget=9000 --screenshot=data/vltk-normalized/previews/browser/skill-khang-long-huu-hoi-smoke.png http://127.0.0.1:5174/` wrote a screenshot.

## Known Limits

- H5 combat damage remains the simplified arcade damage model; PC magic damage values are recorded in the packet but not fully simulated.
- Browser screenshot proves runtime load/no crash with active projectiles. The deterministic headless capture is not a frame-perfect PC-vs-H5 gameplay comparison.
- Browser dev-server console still reports pre-existing equipped-character frame warnings for `vhcnd-equipped-tu-la-giang-sa-staff-phien-vu-idle` frames 98-111 and run frames 70-79. This pass did not address character sheet metadata.


## 2026-05-18 visual correction

Human review caught that the first runtime pass made `Kháng Long Hữu Hối` look unlike the PC dragon effect. Re-check showed the copied source SPR `mag_gb_05_...spr` is the flying fire-dragon body, but H5 had inherited `Bổng Đả ác Cẩu` projectile scale `0.28`, making the dragon body render as a tiny streak. Runtime `projectileScale` for KLHH is now `1.0` to preserve the native SPR size. Added all-directions preview artifact: `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/previews/skill-khang-long-huu-hoi-allframes.png`.


## H5 survivor targeting note

PC `CastSpread` computes direction from source to target/reference. In the H5 survivor loop the reference is auto-selected from the nearest enemy rather than a clicked point. To preserve the user-visible PC behavior of dragons launching in front of the character, H5 spawns KLHH spread projectiles at the player and uses the player-to-enemy direction for the spread fan. Count and angle step remain sourced from active PC level-20 data.

## 2026-05-18 Movement-Facing Correction

Human runtime review requested `Kháng Long Hữu Hối` launch in front of the character and follow the direction the character is moving. H5 now sets `vltkDirectionSource=movement-facing` for KLHH. Runtime records the latest non-zero movement vector and uses that angle as the spread fan direction; before the player has moved, it falls back to target direction.

This is an H5 control-model adapter. PC parity fields remain unchanged: `SkillId=128`, `MissileId=48`, level-20 `skill_misslenum_v=15`, `skill_param1_v=2`, `MisslesForm=2`, `MoveKind=1`, `missle_speed_v=32`, and active dragon `AnimFile2`.

Validation rerun after this correction:

- `npm run typecheck` passed.
- `python3 tests/test_vltk_porting_smoke.py` passed, 16 tests.
- `npm run build` passed with the existing Vite chunk-size warning.
