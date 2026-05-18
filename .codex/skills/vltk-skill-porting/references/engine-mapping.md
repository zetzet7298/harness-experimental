# Engine Mapping Reference

## Required Source Files

- `SwordOnline/Sources/Core/Src/Skill/SkillDef.h`: `eMisslesForm` and `eMissleMoveKind` enums.
- `SwordOnline/Sources/Core/Src/Skill/KMissleSkill.cpp`: `CastWall`, `CastLine`, `CastSpread`, `CastCircle`, `CastZone`, `ParseString2MagicAttrib`.
- `SwordOnline/Sources/Core/Src/Skill/KMissle.cpp`: missile movement implementation such as `MISSLE_MMK_Follow`.
- `decoded_evidence_vltkcache/Skills.txt` and `Missles.txt`: decoded table evidence.
- Extracted active PAK script: `/tmp/.../pak_utf8/script__skill__<school>.lua__<pak>.txt`.

## MisslesForm Mapping

Use the enum and the exact active skill row, not intuition and not another skill port:

- `0`: `SKILL_MF_Wall`; cast a wall centered on target/reference point. Formula: start at `-Param1 * ChildSkillNum / 2`, add `Param1` each child, direction is perpendicular to source-target direction.
- `1`: `SKILL_MF_Line`; cast child missiles along source-target direction with `Param1 * (i + 1)` spacing.
- `2`: `SKILL_MF_Spread`; cast fan/spread. Read `CastSpread` before wiring.
- `3`: `SKILL_MF_Circle`; cast around source or target depending on `Param1`; step is `MaxMissleDir / ChildSkillNum`. This applies only when the current skill evidence says form 3 or a dynamic override changes it to 3.
- `4`: `SKILL_MF_Random`; do not implement without reading engine branch.
- `5`: `SKILL_MF_Zone`; cast in area. Read `CastZone`.
- `6`: `SKILL_MF_AtTarget`; spawn at target.
- `7`: `SKILL_MF_AtFirer`; spawn at firer.

## Dynamic Skill Overrides

`KMissleSkill::ParseString2MagicAttrib` applies level-script overrides:

- `skill_misslenum_v` sets `m_nChildSkillNum`.
- `skill_misslesform_v` sets `m_eMisslesForm`.
- `skill_param1_v` sets `m_nValue1`.
- `skill_param2_v` sets `m_nValue2`.

Always extract active `script/skill/*.lua` from PAK when a skill row references `LvlSetting/LvlData` keys.

## MoveKind Mapping

Use `Missles.txt MoveKind` plus `SkillDef.h`:

- `0`: stand.
- `1`: line.
- `2`: random.
- `3`: circle.
- `4`: helix.
- `5`: follow/homing.
- `8`: single-line.

Do not set H5 `homing` unless `MoveKind=5` and engine code confirms `MISSLE_MMK_Follow`.
