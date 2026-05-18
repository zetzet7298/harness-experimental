# US-010 Port Ba Lăng Huyện Map

## Status

implemented

## Lane

normal

## Product Contract

Port VLTKPC map `Ba Lăng huyện` into the H5 runtime with source-backed map identity, copied local map/minimap assets, generated map metadata, and only mobile combat enemy templates. NPCs are not ported and the minimap must not render NPC names.

## Relevant Product Docs

- `docs/product/vltkpc-porting.md`
- `docs/TEST_MATRIX.md`

## Acceptance Criteria

- Active VLTKPC map evidence identifies `Ba Lăng huyện` as `mapId=53`, path `两湖区\巴陵县`, `MapType=Country`, and `MapPos=351,391`.
- H5 runtime assets are copied or generated under `game-source`; runtime does not read from `/var/www/vltkpc`.
- Map metadata records `.wor` rect `82,89,114,108`, PC region size `512x1024`, and H5 world size `16896x20480`.
- Minimap uses the VLTKPC `24.jpg` map image and renders player/enemy dots only, with no NPC labels or NPC names.
- Enemy templates come from Ba Lăng region NPC data plus active `NpcS` rows, include only `kind_normal=0` with positive `WalkSpeed` or `RunSpeed`, and exclude immobile templates such as `Bao cát`, `Cọc gỗ`, and `Mộc nhân`.
- Runtime preloads and animates copied enemy walk SPR sheets for `ani063`, `ani049`, and `ani061`.
- Runtime background must be rendered from VLTKPC `Region_C.dat` / `Ground.dat`; using `24.jpg` minimap as the world background is invalid because it creates a broken mosaic at gameplay zoom.

## Design Notes

- Commands: `python3 scripts/vltk-port-map.py`; `npm run typecheck`; `python3 tests/test_vltk_porting_smoke.py`; `npm run build`.
- Tables: active `MapList.ini` from `slistcache.pak`; active `NpcS.txt`; Ba Lăng server region `_Region_S.dat` files.
- Engine rules: `KScenePlaceC::OpenPlace` loads `\maps\<path>.wor`; `ScenePlaceMapC` uses minimap suffix `24.jpg`; `KSPNpc.shKind` with `GameDataDef.kind_normal=0` gates combat NPCs.
- Domain rules: H5 map enemy list is template-based for the survivor loop; this ports enemy types, not exact PC spawn coordinates or NPC dialogs.
- UI surfaces: map background in `GameScene`; minimap image plus player/enemy dots only.

## Validation

| Layer | Expected proof |
| --- | --- |
| Unit | `python3 tests/test_vltk_porting_smoke.py` validates map identity, skipped immobile templates, and runtime asset existence. |
| Integration | `npm run typecheck` and `npm run build` validate H5 TypeScript/runtime bundle wiring. |
| E2E | Headless Chrome screenshots validate map/minimap rendering and spawned mobile enemies. |
| Platform | n/a |
| Release | Vite build passes with existing chunk-size warning. |

## Harness Delta

- Added this story and a `US-010` test-matrix row for map/minimap/enemy porting.
- Added validation report `docs/validation/2026-05-18-balang-huyen-map-port.md`.
- Updated `docs/product/vltkpc-porting.md` so map ports have explicit gates beside item/skill ports.

## Evidence

- Map packet: `game-source/data/vltk-normalized/maps/balang-huyen.port.json`.
- Runtime map data: `game-source/src/data/maps.json`.
- Port script: `game-source/scripts/vltk-port-map.py`.
- Copied map assets: `game-source/public/assets/maps/vltkpc/balang-huyen/`.
- Copied/generated enemy assets: `game-source/public/assets/enemies/vltkpc/`.
- Browser screenshots: `game-source/artifacts/screenshots/2026-05-18-balang-huyen-smoke-loaded.png`, `game-source/artifacts/screenshots/2026-05-18-balang-huyen-enemies.png`, and corrected `game-source/artifacts/screenshots/2026-05-18-balang-huyen-regionc-background-linear-12s.png`.
