# Ba Lăng Huyện Map Port Validation

Date: 2026-05-18

## Scope

Validated `US-010` map port for VLTKPC `Ba Lăng huyện`: map identity, minimap image, copied runtime assets, mobile enemy templates, H5 runtime loading, and browser visual smoke.

## Commands Run

```text
python3 scripts/vltk-port-map.py
npm run typecheck
python3 tests/test_vltk_porting_smoke.py
npm run build
npm run dev -- --host 127.0.0.1 --port 5180
google-chrome --headless=new --disable-gpu --no-sandbox --window-size=1280,720 --virtual-time-budget=6000 --screenshot=artifacts/screenshots/2026-05-18-balang-huyen-smoke-loaded.png http://127.0.0.1:5180/
Chrome DevTools Protocol Runtime.evaluate: window.__vltkPrototype.game.scene.getScene('GameScene').setStressTarget(500)
Chrome DevTools Protocol Page.captureScreenshot: artifacts/screenshots/2026-05-18-balang-huyen-enemies.png
```

## Results

| Check | Result | Notes |
| --- | --- | --- |
| Typecheck | passed | `npm run typecheck` completed with no TypeScript errors. |
| Unit | passed | `python3 tests/test_vltk_porting_smoke.py` ran 19 tests. |
| Integration | passed | `python3 scripts/vltk-port-map.py` regenerated map data/assets; `npm run build` completed. |
| E2E | passed | Headless Chrome screenshots show Ba Lăng background/minimap; after visual review, the previous minimap-scaled mosaic background was replaced with a `Region_C.dat` / `Ground.dat` rendered background. Stress smoke shows spawned mobile enemies and minimap dots without NPC names. |
| Platform | n/a | Browser-only prototype. |
| Release | passed with warning | Vite reports an existing chunk-size warning above 500 kB. |

## Evidence

- `game-source/data/vltk-normalized/maps/balang-huyen.port.json`: packet status `passed`, map evidence, enemy inclusion/exclusion evidence.
- `game-source/src/data/maps.json`: runtime map definition with `mapId=53`, world size, minimap/background paths, and enemy templates `ani063`, `ani049`, `ani061`.
- `game-source/public/assets/maps/vltkpc/balang-huyen/minimap.jpg` and `background.jpg`.
- `game-source/public/assets/enemies/vltkpc/ani049-walk.png`, `ani061-walk.png`, and `ani063-walk.png` plus metadata JSON.
- `game-source/artifacts/screenshots/2026-05-18-balang-huyen-smoke-loaded.png`.
- `game-source/artifacts/screenshots/2026-05-18-balang-huyen-enemies.png`.
- `game-source/artifacts/screenshots/2026-05-18-balang-huyen-regionc-background-linear-12s.png`: corrected `Region_C.dat` background render, replacing the broken minimap-as-world-background artifact.

## Gaps

- Browser dev output still reports pre-existing missing-frame warnings for `vltkpc-equipped-tu-la-giang-sa-staff-phien-vu-idle/run`; this belongs to the equipped-character sprite sheet metadata path, not the Ba Lăng map port.
- The H5 survivor adapter ports enemy types and map/minimap visuals, not exact VLTKPC NPC dialog behavior or NPC labels. NPCs are intentionally excluded by request.
- Some `resource.pak` terrain SPR records still report unsupported compression method `0x11000000` in the local extractor; the corrected background records this as skipped source evidence instead of inventing replacement art.
