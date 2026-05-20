---
name: vltk-map-porting
description: "Port and fix VHCND/JX maps into the H5 Phaser runtime with source-backed parity. Use when Codex needs to port a map, minimap, Region_C/Region_S data, Ground.dat, BuildinObj.Dat, map object rendering, map enemy templates, map camera/zoom/aspect, tile backgrounds, collision/obstacle interpretation, or debug visual issues such as stretched maps, oversized gates/buildings, broken house seams, missing trees/objects, wrong minimap scale, or runtime map cache problems."
---

# VLTK Map Porting

## Core Rule

Port maps evidence-first. Do not tune map scale, object size, or offsets by eye until the PC source/table/render path has been checked and the uncertainty is recorded.

Never make the H5 runtime read `/var/www/vhcnd` directly. Copy or generate runtime assets under `/var/www/vltk-h5-survivors/game-source`.

## Required Context

Work from `/var/www/vltk-h5-survivors/game-source` for game code and assets. Use `/var/www/vhcnd` only as PC evidence. Use explicit GitNexus repos when querying:

- H5: `repo: "vltk-h5-survivors"`
- PC: `repo: "vhcnd"`
- Cross-repo: `repo: "@vltk-porting"`

Use `srcwalk` before raw source search. Use `git diff` to inspect recent map fixes before converting them into reusable rules.

## Workflow

1. Identify the exact map target: user-facing name, VLTK map id, PC path, minimap, and whether enemies/NPCs/obstacles are in scope.
2. Extract or verify active PC data sources: `MapList.ini`, `.wor`, minimap image, `Region_C.dat`, `Region_S.dat`, `Ground.dat`, `BuildinObj.Dat`, and NPC tables.
3. Decode/copy source assets into `game-source`; do not wire assets from `/var/www/vhcnd` at runtime.
4. Parse map rect from `.wor`; preserve both source dimensions and render dimensions.
5. Render ground from `Ground.dat` and build-in objects from `BuildinObj.Dat` using PC coordinate rules.
6. Generate tiled runtime backgrounds and metadata under `public/assets/maps/vhcnd/<slug>/` and `data/vltk-normalized/maps/`.
7. Wire `src/data/maps.json`, preload initial visible tiles, lazy-load remaining tiles, minimap, and enemy templates.
8. Bump the map asset query-string version after every regenerate.
9. Validate with smoke tests, `npm run typecheck`, `npm run build`, and a screenshot or crop artifact when visuals changed.

## PC Render Guardrails

Use these rules unless PC evidence proves otherwise:

- `Region_C.dat` combined sections: ground layer index `4`, build-in object index `5`.
- Region source size is `512 x 1024`.
- PC scene render coordinates use source `y / 2`. Runtime render height should be source height divided by 2.
- Do not post-bake stretch a prerendered background from `sourceHeight / 2` back to full source height. That makes gates/buildings look too tall.
- Preserve `sourceWorldSize` separately from runtime `worldSize`. For Ba Lang Huyen, source is `16896 x 20480`; runtime render is `16896 x 10240`.
- `KRepresentShell2/3::CoordinateTransform`: `x - left`, `y / 2 - top - ((z * 887) >> 10)`.
- Static build-ins use `RUIMAGE_RENDER_FLAG_FRAME_DRAW`; do not add SPR frame offsets for those.
- Animated build-ins use ref-spot positioning from `oPos1` and SPR center fallback.
- `POINT` build-ins may be visually scaled only if needed for H5 readability.
- `LINE`/`TREE`/quad build-ins are often multi-part buildings, walls, gates, or roofs. Do not scale those pieces independently unless implementing group-scale, or seams/gaps will appear.

For the concrete Ba Lang Huyen failure/fix history, read `references/map-porting-lessons.md`.

## Enemy And NPC Rules

- Port combat enemies from map NPC data only when they can move.
- Exclude immobile objects such as `Bao cat`, `Moc nhan`, `Coc go`, or any NPC with zero usable movement.
- Do not port NPCs when the user explicitly requests no NPCs.
- Keep minimap free of NPC labels unless explicitly requested.
- Resolve enemy SPRs through NpcRes table evidence and copy SPRs into `public/assets/enemies/vhcnd/` before runtime use.

## Runtime Wiring Checklist

When modifying map runtime code, check these surfaces:

- `src/domain/types.ts`: `MapDefinition`, `EnemyDefinition`, optional source/render size metadata.
- `src/data/maps.json`: generated runtime map catalog.
- `src/game/scenes/PreloadScene.ts`: initial map tile preload, minimap, enemy sheets.
- `src/game/scenes/GameScene.ts`: camera bounds, lazy tile loading, tile positions, minimap projection.
- `src/systems/simulation.ts`: simulation bounds from runtime `map.worldSize`.
- `src/gateway/offlineGateway.ts`: selected map in `RunStart`.
- `tests/test_vltk_porting_smoke.py`: map identity, cache version, tile count, render/source size, build-in render metadata, enemies skipped/ported.

## Validation

Run from `/var/www/vltk-h5-survivors/game-source`:

```bash
python3 scripts/vltk-port-map.py --out-root .
python3 tests/test_vltk_porting_smoke.py
npm run typecheck
npm run build
```

Capture a screenshot or a crop from `public/assets/maps/vhcnd/<slug>/background.jpg` when visual scale/aspect changed.

## Report Back

Answer in Vietnamese when the user is Vietnamese. Include:

- PC source evidence used.
- Generated files and runtime asset paths.
- Source vs render world size.
- Build-in object scale policy.
- Enemy/NPC include/exclude rule.
- Validation commands and screenshot/crop artifact.
- Any unresolved missing SPR or unsupported PAK decode counts.
