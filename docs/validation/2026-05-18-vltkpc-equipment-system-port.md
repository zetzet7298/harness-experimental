# 2026-05-18 VLTKPC Equipment System Port Validation

## Scope

Validated the equipment-system port in `/var/www/vltk-h5-survivors/game-source`, including generated VLTKPC equipment catalog data, portrait equipment scene, localStorage-backed equip state, run inventory handoff, derived stats, HUD display, preview-gated outside-run and in-run loadout visual sync, build-time parallel SPR copy support, and parallel preview-gated visual shard execution.

## Commands

```text
python3 tests/test_vltk_porting_smoke.py
python3 -m py_compile scripts/vltk-extract-required-sprs.py scripts/vltk-normalize-equipment-index.py scripts/vltk-build-equipment-seed.py scripts/vltk-build-equipped-loadout-packet.py scripts/vltk-build-equipped-visual-loadout.py scripts/vltk-run-equipment-visual-shard.py scripts/vltk-fetch-vng-gold-name-sources.py scripts/vltk-audit-equipment-name-localization.py scripts/port-vltkpc-equipped-character.py scripts/vltk-build-equipped-visual-manifest.py
npm run typecheck
npm run build
```

## Results

- Browser smoke via Chrome headless/CDP passed: equip screen loaded, reset default equipment, `Run` handed off to game canvas, exact current-loadout textures `equipment-run-equipped-current-catalog-mounted` / `equipment-idle-equipped-current-catalog-mounted` were active; alternate `钢剑` localStorage override selected `equipment-run-equipped-alt-gang-jian-catalog` / `equipment-idle-equipped-alt-gang-jian-catalog`; outside-run preview selected `equipment-preview-equipped-current-catalog-mounted` and `equipment-preview-equipped-alt-gang-jian-catalog`; HUD showed the matching weapon name and no runtime console warnings/errors were captured.
- `python3 tests/test_vltk_porting_smoke.py`: passed, 45 tests.
- `python3 -m py_compile scripts/vltk-extract-required-sprs.py scripts/vltk-normalize-equipment-index.py scripts/vltk-build-equipment-seed.py scripts/vltk-build-equipped-loadout-packet.py scripts/vltk-build-equipped-visual-loadout.py scripts/vltk-run-equipment-visual-shard.py scripts/vltk-fetch-vng-gold-name-sources.py scripts/vltk-audit-equipment-name-localization.py scripts/port-vltkpc-equipped-character.py scripts/vltk-build-equipped-visual-manifest.py`: passed.
- `npm run typecheck`: passed.
- `npm run build`: passed; Vite reported the existing large chunk-size warning after producing `dist/`.

## Evidence

- Current exact loadout preview contact sheets were agent-reviewed and regenerated with `status=passed`: `game-source/data/vltk-normalized/previews/equipped-current-catalog-mounted-run-preview.png`, `game-source/data/vltk-normalized/previews/equipped-current-catalog-mounted-run-preview.report.json`, `game-source/data/vltk-normalized/previews/equipped-current-catalog-mounted-idle-preview.png`, and `game-source/data/vltk-normalized/previews/equipped-current-catalog-mounted-idle-preview.report.json`.
- Current exact loadout SPR extraction copied 9/9 run and 9/9 idle source SPRs with `missing=0` into `game-source/public/assets/character/vltkpc/source/equipped-current-catalog-mounted-run/` and `game-source/public/assets/character/vltkpc/source/equipped-current-catalog-mounted-idle/`.
- Current exact loadout packets are generated from catalog+inventory with preview gate passed and runtime output generated: `game-source/data/vltk-normalized/port-packets/equipped-current-catalog-mounted-run.json` and `game-source/data/vltk-normalized/port-packets/equipped-current-catalog-mounted-idle.json`; composed sheets live at `game-source/public/assets/character/vltkpc/equipped-current-catalog-mounted-run.png` and `game-source/public/assets/character/vltkpc/equipped-current-catalog-mounted-idle.png`. Alternate slot override packets/sheets for `钢剑` live at `game-source/data/vltk-normalized/port-packets/equipped-alt-gang-jian-catalog-mounted-run.json`, `game-source/data/vltk-normalized/port-packets/equipped-alt-gang-jian-catalog-mounted-idle.json`, `game-source/public/assets/character/vltkpc/equipped-alt-gang-jian-catalog-run.png`, and `game-source/public/assets/character/vltkpc/equipped-alt-gang-jian-catalog-idle.png`.
- Catalog visual metadata now expands runtime character SPR parts for horse (`HH/HB/HT`), armor (`BD/LH/RH`), and weapon (`RW/LW`) so build-time extraction can gather exact loadout parts from `src/data/equipmentCatalog.json`.
- Seed default now prefers source names `修罗发结`, `绛纱袍`, and `敌忾竹杖` when present in the generated catalog; `Phiên Vũ`/`翻羽` is still absent from the generated catalog and remains part of the arbitrary horse visual gap.
- Browser screenshots/report: `game-source/artifacts/screenshots/2026-05-18-equipment-exact-reset-initial.png`, `game-source/artifacts/screenshots/2026-05-18-equipment-exact-reset-run.png`, `game-source/artifacts/screenshots/2026-05-18-equipment-exact-visual-smoke-report.json`, `game-source/artifacts/screenshots/2026-05-18-equipment-alt-gang-jian-initial.png`, `game-source/artifacts/screenshots/2026-05-18-equipment-alt-gang-jian-run.png`, `game-source/artifacts/screenshots/2026-05-18-equipment-alt-gang-jian-smoke-report.json`, `game-source/artifacts/screenshots/2026-05-18-equipment-preview-seed.png`, `game-source/artifacts/screenshots/2026-05-18-equipment-preview-alt-gang-jian.png`, and `game-source/artifacts/screenshots/2026-05-18-equipment-preview-sync-report.json`.
- Catalog seed: `game-source/src/data/equipmentCatalog.json` contains 1,231 generated equipment items and all 11 PC equipment slots.
- Runtime seed: `game-source/src/data/inventory.json` uses schema v2, all 11 equipped slots, and `one-equipment-per-mobile-cell` bag policy.
- Domain rules: `game-source/src/domain/equipment.ts` validates supported requirements and applies every magic/base attribute key present in the generated equipment catalog to `CharacterStats` or explicit item/audit fields; the audit found no catalog attribute key left in the no-op block.
- Runtime handoff: `game-source/src/gateway/offlineGateway.ts` rebuilds inventory from seed or persisted `localStorage` equipment.
- UI: `game-source/src/game/scenes/EquipmentScene.ts` provides portrait slots, bag grid, equip/unequip, detail/stat panels, manifest-based generated visual preview, and run entry.
- Visual sync slice: `game-source/src/game/scenes/GameScene.ts` matches equipped SPR basenames against `game-source/public/assets/character/vltkpc/equipped-visual-manifest.json` first, then falls back to approved wardrobe combo sheets when no exact generated sheet exists. Arbitrary loadout generation is now scripted through `game-source/scripts/vltk-build-equipped-visual-loadout.py` with preview-gated compose enforcement. Coverage audit `game-source/data/vltk-normalized/equipment-visual-coverage.audit.json` records `complete=false`, 8 manifest entries, and 136,492 remaining theoretical combinations for the conservative precomposed fallback. Fast-path plan `game-source/data/vltk-normalized/equipment-visual-parts-plan.json` records 278 unique run/idle part sheets instead of 273,000 brute-force combo sheets. Stat audit `game-source/data/vltk-normalized/equipment-stat-coverage.audit.json` records 45 current catalog attribute keys with no missing runtime cases and no missing formula markers for lực tay/HP/attack/all-resist handling. Quality audit `game-source/data/vltk-normalized/equipment-quality-coverage.audit.json` records normal/magic/gold present. `game-source/data/vltk-normalized/phien-vu-research.audit.json` records the local source search proving `Phiên Vũ`/`翻羽` is not in active decoded item rows in this workspace.

## Known Limits

- Current generated equipment-catalog attribute keys are all handled by stat/audit fields. VLTKPC magic attributes not present in this catalog still require source-backed handling before future expansion claims.
- Current in-run visual sync covers generated manifest entries, including the default seed horse/weapon/body/head loadout and an alternate `钢剑` weapon override. Conservative combo audit reports 136,492 remaining unique visual-signature combinations, while dynamic part coverage reports all 278 dedicated PNG part assets exported and the runtime layered compositor wired; quality audit reports normal/magic/gold coverage, so dynamic visual fast-path assets are covered; Hoàng Kim row-name matching is partially applied via the verified row map and remains incomplete for 47 CJK display names.
- Browser equip/unequip/run screenshot smoke passed after `PLAYER_SHEET`/`PLAYER_IDLE_SHEET` frame heights were corrected to generated metadata.

## Completion Audit

- See `docs/validation/2026-05-18-vltkpc-equipment-completion-audit.md`; active goal is complete for the current audited source-backed H5 scope. Hoàng Kim names now have `verified=171`, `ambiguous=0`, `unmatched=0`, and `cjkCanonicalNameCount=0`.
