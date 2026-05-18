# 2026-05-18 Phi Long Tại Thiên Parity Validation

## Scope

Port Cái Bang `Phi Long Tại Thiên` level 20 and correct Cái Bang Wall/Follow forward-launch origin for `Phi Long Tại Thiên` and `Thiên Hạ Vô Cẩu` in the H5 survivor runtime.

## Source Evidence

- Package order: `/var/www/vltkpc/extracted_build_jxwin_soucgoc_hoiquanvolam/source_from_vmdk/SourceNew/swrod3/bin/Client/package.ini:3-31`, where `slistcache.pak` is the first active source for the extracted rows.
- FLTT skill row: `/tmp/vltk-thvc-fltt-port/pak_utf8/settings__Skills.txt__slistcache.txt:358`.
- FLTT missile row: `/tmp/vltk-thvc-fltt-port/pak_utf8/settings__Missles.txt__slistcache.txt:167`.
- FLTT script block: `/tmp/vltk-thvc-fltt-port/pak_utf8/script__skill__gaibang.lua__slistcache.txt:142-194`.
- THVC skill row: `/tmp/vltk-thvc-fltt-port/pak_utf8/settings__Skills.txt__slistcache.txt:360`.
- THVC missile row: `/tmp/vltk-thvc-fltt-port/pak_utf8/settings__Missles.txt__slistcache.txt:169`.
- THVC script block: `/tmp/vltk-thvc-fltt-port/pak_utf8/script__skill__gaibang.lua__slistcache.txt:276-290`.
- `Param2PCoordinate`: `/var/www/vltkpc/extracted_build_jxwin_soucgoc_hoiquanvolam/source_from_vmdk/SourceNew/swrod3/SwordOnline/Sources/Core/Src/KSkills.cpp:93-128`.
- `CastWall`: `/var/www/vltkpc/extracted_build_jxwin_soucgoc_hoiquanvolam/source_from_vmdk/SourceNew/swrod3/SwordOnline/Sources/Core/Src/KSkills.cpp:604-665` and `:1398-1514`.
- `MoveKind=5` Follow: `/var/www/vltkpc/extracted_build_jxwin_soucgoc_hoiquanvolam/source_from_vmdk/SourceNew/swrod3/SwordOnline/Sources/Core/Src/Skill/SkillDef.h:104-115`; movement update in `/var/www/vltkpc/extracted_build_jxwin_soucgoc_hoiquanvolam/source_from_vmdk/SourceNew/swrod3/SwordOnline/Sources/Core/Src/KMissle.cpp:745-767`.

## Confirmed FLTT Values

- `SkillId=357`.
- `ChildSkillId/MissileId=166`.
- Base `MisslesForm=0`, `SKILL_MF_Wall`.
- Base `ChildSkillNum=3`; level 20 effective `skill_misslenum_v=4`.
- `Param1=32`, `Param2=65537`.
- `MslsGenerate=5`, `SKILL_MGS_CENTEREXTENDLINE`; `MslsGenerateData=0`.
- Level 20 `missle_speed_v=24`, `skill_attackradius=512`, `skill_cost_v=65`, `seriesdamage_p=60`, `firedamage_v=750`.
- Missile `MoveKind=5`, so H5 `homing=true`.
- Main flight animation `AnimFile2=\spr\skill\ỉỒù\mag_gb_05_ẴẲẦỳểéằẾ.spr`, `AnimFileInfo2=80,16,1`.

## THVC Correction

- Active THVC is `SkillId=359`, `MissileId=168`, `scriptKey=tianxia_wugou`.
- Level 20 effective `skill_misslenum_v=3`, `missle_speed_v=24`, `skill_attackradius=512`.
- Missile `MoveKind=5`, so H5 `homing=true`.
- Runtime data was corrected from mixed BDAC evidence to active THVC evidence.

## H5 Adapter

PC `CastWall` centers the wall on a target/reference coordinate. In VLTKPC this coordinate comes from the player cast target or click point. In the H5 survivor loop, target selection is automatic and can be far from the character, which made THVC/FLTT appear to originate at the enemy. For these forward-launch Cái Bang Wall/Follow skills, H5 now uses:

- `vltkWallOrigin=player-forward`.
- `vltkWallForwardOffset=32`.
- `vltkWallOffsetAxis=perpendicular`.
- `vltkWallProjectileDirection=target`.

This keeps projectile count, spacing, direction, speed, homing, and asset identity from PC evidence while adapting the reference point to the H5 control model so the visible skill launches from in front of the character.

## Runtime Artifacts

- FLTT packet: `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/port-packets/skill-phi-long-tai-thien.json`.
- THVC packet: `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/port-packets/skill-thien-ha-vo-cau.json`.
- Runtime skill data: `/var/www/vltk-h5-survivors/game-source/src/data/skills.json`.
- Simulation adapter: `/var/www/vltk-h5-survivors/game-source/src/systems/simulation.ts`.
- FLTT runtime main sheet/meta: `/var/www/vltk-h5-survivors/game-source/public/assets/skills/vltkpc/phi-long-tai-thien-main.png` and `.json`.
- FLTT all-frames proof: `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/previews/skill-phi-long-tai-thien-allframes.png`.

## Validation Commands

- `npm run typecheck` passed.
- `python3 tests/test_vltk_porting_smoke.py` passed, 16 tests.
- `npm run build` passed with the existing Vite chunk-size warning and Vite plugin timing notice.

## Known Limits

- H5 damage remains the simplified arcade model; PC damage formulas are recorded in packets but not fully simulated.
- The H5 adapter is explicitly documented because the H5 survivor control model auto-targets enemies instead of using the PC click/target reference directly.

## 2026-05-18 THVC Visual Correction

Human runtime review confirmed `Phi Long Tại Thiên` now launches correctly, but `Thiên Hạ Vô Cẩu` was not visually readable. Runtime data now sets THVC visual fields explicitly instead of relying on fallback projectile rendering:

- `projectileTextureKey=vltkpc-bong-da-ac-cau-main`.
- `projectileAnimationKeyPrefix=bong-da-ac-cau-main`.
- `projectileDirections=16`.
- `projectileScale=0.36`.

This is evidence-backed for asset identity because active `Missles.txt:slistcache:169` uses `AnimFile2=\spr\skill\ỉỒù\mag_gb_04_èỡẽẨẻịạã.spr`, the same runtime source sheet as Bổng Đả. The scale increase is an H5 visual readability adjustment for the three forward THVC projectiles, recorded separately from PC table parity.

Validation rerun after this correction:

- `npm run typecheck` passed.
- `python3 tests/test_vltk_porting_smoke.py` passed, 16 tests.
- `npm run build` passed with the existing Vite chunk-size warning.

## 2026-05-18 THVC Visibility Correction

Human runtime review still did not show `Thiên Hạ Vô Cẩu` clearly. Runtime now isolates THVC from Bổng Đả rendering even though active PC evidence points to the same `mag_gb_04` flight SPR:

- `projectileTextureKey=vltkpc-thien-ha-vo-cau-main`.
- `projectileAnimationKeyPrefix=thien-ha-vo-cau-main`.
- `projectileScale=0.5`.
- `projectileDepth=18`.

The dedicated texture key loads the same composed source sheet as Bổng Đả, preserving active `Missles.txt:slistcache:169` asset identity while preventing the three THVC forward projectiles from being hidden by simultaneous Bổng Đả projectiles in the H5 multi-skill scene.

Validation rerun after this correction:

- `npm run typecheck` passed.
- `python3 tests/test_vltk_porting_smoke.py` passed, 16 tests.
- `npm run build` passed with the existing Vite chunk-size warning.

## 2026-05-18 PLTT/THVC Lane Separation

Human runtime review confirmed THVC is visible but still visually covered by the larger four-dragon PLTT cast. H5 now separates the two simultaneous Wall/Follow launch lanes:

- THVC remains `player-forward`, `vltkWallForwardOffset=32`, `projectileDepth=18`.
- PLTT uses `vltkWallLaunchAngleOffsetDeg=65`, `vltkWallForwardOffset=96`, `projectileDepth=14`.

This is a H5 multi-skill readability adapter only. PC parity fields for PLTT remain unchanged: `SkillId=357`, `MissileId=166`, level-20 `skill_misslenum_v=4`, `MisslesForm=0`, `MoveKind=5`, `missle_speed_v=24`, and active dragon `AnimFile2`. PLTT still homes to the selected enemy after spawning from the side-forward lane.

Validation rerun after this correction:

- `npm run typecheck` passed.
- `python3 tests/test_vltk_porting_smoke.py` passed, 16 tests.
- `npm run build` passed with the existing Vite chunk-size warning.

## 2026-05-18 Stick Projectile Scale Up

Human runtime review requested the stick projectile visuals for `Thiên Hạ Vô Cẩu` and `Bổng Đả Ác Cẩu` be slightly larger. This is a H5 readability adjustment only; PC table identity/count/speed/form are unchanged.

- THVC `projectileScale` increased from `0.5` to `0.58`.
- Bổng Đả `projectileScale` set explicitly to `0.34`; its fallback sheet scale was also increased from `0.28` to `0.34`.

Validation rerun after this correction:

- `npm run typecheck` passed.
- `python3 tests/test_vltk_porting_smoke.py` passed, 16 tests.
- `npm run build` passed with the existing Vite chunk-size warning.


## 2026-05-18 Collision Effect Wiring

Human runtime review identified the missing enemy-hit visual: VLTKPC creates a collision special effect, not only a hit sound. Evidence used:

- `SkillDef.h:127-132` maps `MS_DoCollision` as missile status 3.
- `KMissle.cpp:120-170` loads `AnimFile1..4` into status resources, so `AnimFile4` is the collision resource.
- `KMissle.cpp:1011-1022` calls `CreateSpecialEffect(MS_DoCollision, ...)` when an enemy is hit, passing the enemy NPC when `ColFollowTarget=1`.
- `KMissle.cpp:1094-1124` binds the special effect to the status resource and stores the effect end time from `AnimFileInfo`.
- Active `Missles.txt` rows: BDAC row 48 and THVC row 169 use `mag_bz_huo3` / `18,1,2`; KLHH row 49 and PLTT row 167 use `mag_gb_bz5` / `6,1,2`.

Runtime update:

- Added per-skill `impactTextureKey`, `impactAnimationKey`, frame count/rate, scale, and depth in `src/data/skills.json`.
- Added `ImpactEntity` simulation pool and spawn-on-projectile-hit at enemy position.
- Preloaded all impact spritesheets and created non-looping Phaser impact animations.
- Rendered impact sprites independently from projectile sprites so BDAC/THVC/KLHH/PLTT keep isolated collision visuals.
- Stick projectile readability was increased again: THVC `0.58 -> 0.64`, BDAC `0.34 -> 0.38`; this remains an H5 readability adapter, not a PC table change.

Validation rerun after this correction:

- `npm run typecheck` passed.
- `python3 tests/test_vltk_porting_smoke.py` passed, 16 tests.
- `npm run build` passed with the existing Vite chunk-size warning.
- Headless Chrome smoke screenshot captured at `game-source/data/vltk-normalized/previews/browser/skill-impact-smoke.png`.
