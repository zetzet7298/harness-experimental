---
name: vltk-skill-porting
description: "Port VHCND/JX combat skills into the H5 game with strict source-backed parity. Use whenever porting or fixing skill behavior, projectile count/direction/speed/cooldown, homing, hit/collision impact effects, skill animation/effect/SFX, PAK/.spr/.wav extraction, active Skills.txt/Missles.txt/script evidence, visual mismatch, wrong sprite scale, or proving PC-vs-H5 parity. Requires 100% evidence-first workflow: no invented mechanics, no guessed level scaling, no reused visuals/scales from another skill, and no runtime wiring unless active VHCND table/script/engine plus visual proof is recorded."
---

# VLTK Skill Porting

## Non-Negotiables

- Treat `/var/www/vhcnd` as legacy source evidence and `/var/www/vltk-h5-survivors/game-source` as the only H5 runtime/edit target.
- Do not make the H5 app read `/var/www/vhcnd` at runtime; copy/extract assets into `game-source` first.
- Do not infer projectile count, form, direction, speed, cooldown, homing, hit/collision impact, animation, or SFX from names or memory.
- Stop and report `blocked: missing evidence` when active table/script/engine proof is unavailable.
- Mark any user-requested deviation as `explicit override`, never as VHCND parity.
- Treat every skill as an independent PC profile. Prior successful ports such as `Bổng Đả Ác Cẩu` are examples of workflow only, not templates for missile form, count, scale, homing, spawn origin, flight animation, collision animation, or SFX.

## Required Flow

1. Resolve active package order from `bin/Client/package.ini`.
2. Extract active PAK data before trusting loose files.
3. Resolve skill identity from active `Skills.txt` row and duplicate-name rows.
4. Resolve missile identity from active `Missles.txt` row.
5. Extract active `script/skill/*.lua` and level-scaling key for the exact `LvlData` token.
6. Read engine C/C++ implementation for the exact `MisslesForm`, `MoveKind`, and missile status rendering.
7. Map every active missile status asset before editing H5: `AnimFile1` wait/precast, `AnimFile2` fly, `AnimFile3` vanish/end, `AnimFile4` collision/hit. Confirm this in engine code, not by column names alone.
8. Build an evidence map before editing H5.
9. Patch H5 behavior/assets only for values in the evidence map.
10. Validate with typecheck/build plus browser/screenshot proof when visuals changed.
11. For visual ports, inspect source SPR frames across all directions and confirm runtime scale/texture selection before marking preview passed.
12. Final response must include evidence paths/lines, validation commands, visual artifacts, and remaining gaps.

## Evidence Commands

Use the project extractor for active PAK script/table evidence:

```bash
python3 /var/www/vltk-h5-survivors/harness-experimental/.codex/skills/vltk-item-research/scripts/vltk_extract_tables.py \
  --client-dir /var/www/vhcnd/extracted_build_jxwin_soucgoc_hoiquanvolam/source_from_vmdk/SourceNew/swrod3/bin/Client \
  --source-root /var/www/vhcnd/extracted_build_jxwin_soucgoc_hoiquanvolam/source_from_vmdk/SourceNew/swrod3 \
  --out /tmp/vltk-skill-evidence \
  --paths '\settings\Skills.txt' '\settings\Missles.txt' '\script\skill\gaibang.lua' \
  --all-matches --include-loose
```

For target-specific scripts, replace `gaibang.lua` with the skill's school script. Search the extracted `pak_utf8` files, then choose the first hit according to `package.ini` order.

## H5 Edit Targets

- Skill data: `/var/www/vltk-h5-survivors/game-source/src/data/skills.json`
- Skill types: `/var/www/vltk-h5-survivors/game-source/src/domain/types.ts`
- Simulation behavior: `/var/www/vltk-h5-survivors/game-source/src/systems/simulation.ts`
- Runtime assets: `/var/www/vltk-h5-survivors/game-source/public/assets/skills/vhcnd/`
- Port packets/reports: `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/`

## Engine Evidence Checklist

Read `references/engine-mapping.md` before changing simulation formulas. The common trap: `MisslesForm=0` is `SKILL_MF_Wall`, not line.

Record these fields before edits:

- `SkillId`, skill name, duplicate rows, active PAK source
- `MisslesForm`, `ChildSkillId`, base `ChildSkillNum`, dynamic `skill_misslenum_v`
- `Param1`, `Param2`, `MslsGenerate`, `MslsGenerateData`, `TimePerCast`
- missile `MoveKind`, `FollowKind`, `ColFollowTarget`, `LifeTime`, `Speed`, `CollidRange`, `ColVanish`, sprite/SFX paths, and every `AnimFileInfo*`
- missile status mapping from engine (`MS_DoWait`, `MS_DoFly`, `MS_DoVanish`, `MS_DoCollision`) so the main flight sheet is not confused with precast/hit/end sheets
- collision/hit effect evidence: `AnimFile4`, `AnimFileInfo4`, `SndFile4`, source SPR header, whether `CreateSpecialEffect(MS_DoCollision, ...)` follows the enemy/NPC, and runtime impact texture/animation keys
- source SPR header fields: native width/height, total frames, directions, frames per direction, interval, and frame-compression method when relevant
- runtime texture key, animation prefix, frame metadata, and chosen scale with evidence for why it is not inherited from another skill
- engine function lines for cast form and move kind

## Skill Profile Isolation

Before editing H5, write a short profile summary for this exact skill:

- identity: `SkillId`, active row, school script key, duplicate-name rows
- cast shape: effective `MisslesForm`, `ChildSkillNum`, `Param1`, `Param2`, level overrides
- movement: missile `MoveKind`, `FollowKind`, homing or non-homing evidence
- visual: exact active `AnimFile*`, `AnimFileInfo*`, native SPR dimensions, intended runtime scale
- collision: exact active `AnimFile4`, `AnimFileInfo4`, `SndFile4`, whether the engine uses `MS_DoCollision`, and whether the effect follows the hit target
- adapter: whether H5 auto-targeting changes spawn/reference point compared with PC

Use this profile as the only source for runtime behavior. Do not copy another skill's known values. For example, `Bổng Đả Ác Cẩu` being a 16-projectile circle does not imply `Thiên Hạ Vô Cẩu` or `Kháng Long Hữu Hối` should be circle, use 16 projectiles, share BDAC scale, share BDAC flight assets, or omit their own collision-effect profile.

## Collision And Impact Gate

VHCND missile hit visuals are status-specific. Do not treat hit sound or projectile vanish as a complete collision port. Before wiring any skill that can collide with an enemy:

1. Confirm `eMissleStatus` in engine source. In the known PC source, `MS_DoCollision` is a separate status from `MS_DoFly`.
2. Confirm missile loading code maps `AnimFile4`/`AnimFileInfo4`/`SndFile4` into the `MS_DoCollision` resource slot.
3. Confirm the collision call site, usually `CreateSpecialEffect(MS_DoCollision, ...)`, and record whether it passes an NPC index when `ColFollowTarget=1`. If the PC effect follows the target, H5 should spawn or update the impact at the hit enemy, not at the player or arbitrary projectile origin.
4. Decode/copy the `AnimFile4` SPR separately from the flight SPR. Record native width/height, frames, directions, interval, and runtime sheet metadata. If the active table says `18,1,2` but the copied SPR decodes to fewer visible frames, record both the table value and decoded source header instead of guessing.
5. Add runtime impact fields separate from projectile flight fields, such as `impactTextureKey`, `impactAnimationKey`, `impactFrameCount`, `impactFrameRate`, `impactScale`, and `impactDepth`. Do not reuse projectile animation keys for impact.
6. Browser proof must show both projectile flight and enemy-hit impact. A skill is not visually complete if only the flight projectile appears.

When multiple skills share the same active PC collision SPR, sharing the PNG source is allowed, but each skill still needs isolated runtime texture/animation names or an explicit audit note explaining why sharing is safe.

## Runtime Wiring Rules

- Use dynamic level script values over base row values when `LvlSetting/LvlData` references a key such as `skill_misslenum_v`.
- Preserve engine cast formula names in code/reports: `Wall`, `Line`, `Spread`, `Circle`, `Zone`, `AtTarget`, `AtFirer`.
- Preserve missile move semantics: `MoveKind=5` is follow/homing only when engine enum confirms it.
- Keep skill visuals isolated: every ported skill that has its own PC `AnimFile*` must get its own texture key, animation prefix, metadata, source folder, packet, and cache-busted runtime path. Do not reuse another skill sheet or scale unless the active PC row points to the same source asset and the audit says so.
- Keep flight and impact visuals isolated from each other. `AnimFile2`/`MS_DoFly` drives the moving projectile; `AnimFile4`/`MS_DoCollision` drives the enemy-hit effect. Wire both when present.
- Do not add lateral offsets, spread angles, target locking, or visual separation unless the PC engine/table/script evidence supports it or the final report labels it as an explicit non-parity override.

## Visual Proof Gate

A side-by-side preview of only the first few frames is not enough for VLTK skill parity. Directional SPRs often hide the recognizable silhouette outside the first direction. Before marking `previewEvidence.status=passed`:

1. Decode the active missile flight SPR from the status used by engine drawing. In PC `eMissleStatus`, `MS_DoFly` is status 1, so `AnimFile2/AnimFileInfo2` is usually the main flying projectile; verify this in `KMissle.cpp`/`KMissleRes.cpp` instead of guessing.
2. Generate an all-directions/all-frames contact sheet from the copied source SPR and inspect it. The artifact should show every direction and every frame-per-direction group, not just frame 0.
3. Compare native SPR size and frame bounding boxes to the H5 runtime scale. If the source asset is large (for example a dragon body), do not inherit a small scale from a previous skill such as `Bổng Đả Ác Cẩu`. Record the scale rationale in the packet.
4. Verify the runtime texture key actually switches per projectile/skill. If all projectiles use a default texture key, multiple skills can appear as the same visual even when assets are correct.
5. Browser proof must show the corrected runtime visual after wiring, not only a generated PNG/GIF. Save the screenshot path and note console warnings separately.

## H5 Runtime Adapter Rule

PC targeting can be click/target based, while the H5 survivor loop auto-selects enemies. When adapting a PC formula:

- Preserve PC-count, form, angle step, speed, movement kind, and asset identity exactly from evidence.
- If the H5 control model changes the reference point (for example auto-target instead of clicked target), document it as an H5 adapter note, not as raw PC parity.
- For forward-launch skills, spawn at/near the player and use the player-to-target direction unless engine evidence proves the missile should originate at the target point. This prevents a correct PC asset from appearing in the wrong place in H5.
- For multi-skill visibility conflicts, prefer preserving PC values and adding a clearly labeled H5 visual adapter only when the human/runtime review confirms overlap hides one skill. Record the adapter separately from PC parity data.
- Scale changes for readability are allowed only as documented H5 adapters. Never use a previous skill scale as evidence for a new skill; compare native SPR bounds and runtime screenshots.

## Validation Gate

Run the narrowest relevant checks, then broader checks:

```bash
npm run typecheck
python3 tests/test_vltk_porting_smoke.py
npm run build
```

Use browser proof when behavior or visuals changed. Save screenshots/video paths in the final audit. For visual ports, also save an all-directions/all-frames source SPR contact sheet and compare runtime scale/texture selection against it.

## Repeated Failure Patterns To Avoid

- Do not confuse similarly named Cái Bang skills. `Bổng Đả Ác Cẩu`, `Thiên Hạ Vô Cẩu`, `Kháng Long Hữu Hối`, and `Phi Long Tại Thiên` can share school/script files or some SPRs, but their active skill rows, missile rows, level-20 overrides, forms, counts, move kinds, and collision effects must be proven independently.
- Do not assume `MisslesForm=0` means a simple line projectile. Confirm the engine formula; in this codebase it maps to `SKILL_MF_Wall`.
- Do not stop after the projectile appears. Check hit/collision visuals, hit SFX, and vanish/end statuses. Missing `MS_DoCollision` is a visual parity bug even if damage and flight look correct.
- Do not let large dragon/body effects hide smaller stick effects and then declare a skill missing. First verify texture key isolation, depth, scale, and browser screenshot evidence.
- If the user says the visual is wrong, re-open PC evidence before editing. Treat memory-based corrections as hypotheses until active table/script/engine proof confirms them.

## References

- `references/engine-mapping.md`: C/C++ enum and formula mapping to H5.
- `references/porting-playbook.md`: end-to-end checklist.
- `references/parity-audit-template.md`: final report format.
