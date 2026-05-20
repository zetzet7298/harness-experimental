---
name: vltk-spr-porting
description: "Port VLTK/JX/SwordOnline .spr assets and character equipment animations into H5/game runtimes safely. Use this skill for port, preview, extract, convert, normalize, compose, or wire VHCND character sprites, NpcRes parts, equipment visuals, title/effect SPRs, PAK assets, Phaser, H5, spritesheets, or copied runtime assets."
---

# VLTK SPR Porting

## Core Rule

Porting is not item lookup. Resolve table evidence, verify engine mapping, preview candidate SPRs, move source SPR/assets into the target repo, then compose runtime assets from moved local source.

Never make the runtime app read `/var/www/vhcnd` directly. Never use symlink/symbolic-link from runtime asset folders to `/var/www/vhcnd`.

## Workflow

1. Start from the exact user target: item/loadout/skill/effect name, sex, mount state, action, and target runtime.
2. Read project rules first when in `/var/www/vltk-h5-survivors/game-source`: `AGENTS.md`, `scripts/README.md`, and `docs/VHCND_SPR_PORTING_PLAYBOOK.md`.
3. Prefer the loadout gate script for H5 work: resolve aliases, create packet, update PAK manifest cache, move required SPR/assets, and generate preview report.
4. Verify engine mapping before choosing NpcRes rows. Do not map table values directly unless the code path confirms it.
5. Treat preview reports as the gate: `status=pending|failed` blocks compose and runtime wiring; only `status=passed` may compose/wire.
6. Move required source SPR/assets into the target repo before compose; runtime must never read `/var/www/vhcnd` and must not rely on symlink.
7. Compose runtime spritesheets from moved local source only, update metadata, then wire runtime.
8. Validate with script smoke tests, build/typecheck, and a browser/game screenshot when runtime visuals changed.

## Runtime Debug Fast Path

Use this branch when the user says “vẫn sai visual” after a claimed fix:

1. Reproduce in browser first (`agent-browser`), capture screenshot for the exact direction/state.
2. Check whether runtime is showing default sheet or auto-applied wardrobe combo/preset.
3. If mismatch comes from saved preset, clear/reset local preset before remapping assets.
4. Check per-direction layer order, especially north (12 giờ), before remapping item rows again.
5. Patch the smallest artifact first (packet `layerOrderByDirection`, metadata, cache version), then re-test.
6. Use full combo rebuild only when necessary; prefer metadata/catalog patch for fast turnaround.

## H5 Toolchain

From `/var/www/vltk-h5-survivors/game-source`:

```bash
python3 scripts/vltk-normalize-equipment-index.py
python3 scripts/vltk-port-loadout.py "Phiên Vũ" "Địch Khái" --slug <slug>
python3 scripts/vltk-port-loadout.py "Phiên Vũ" "Địch Khái" --slug <slug> --preview-status passed --reviewer-note "Preview checked." --compose
python3 scripts/vltk-preview-candidates.py --input data/vltk-normalized/port-packets/<packet>.json --report-out data/vltk-normalized/previews/<slug>.report.json
python3 scripts/port-vhcnd-equipped-character.py --packet data/vltk-normalized/port-packets/<packet>.json --preview-report data/vltk-normalized/previews/<slug>.report.json
```

Useful outputs:

- `data/vltk-normalized/equipment-index.json`
- `data/vltk-normalized/aliases.json`
- `data/vltk-normalized/pak-spr-manifest.json`
- `data/vltk-normalized/port-packets/*.json`
- `data/vltk-normalized/previews/*.png` and `*.report.json`
- `public/assets/character/vhcnd/source/<slug>/`
- `public/assets/character/vhcnd/*.png` and matching metadata JSON

## Engine Mapping Guardrails

Check these source pivots before finalizing resource rows:

- `KItemChangeRes::GetWeaponRes`: `row = particular * 10 + level + 2`; common result uses `tableValue - 2` plus client table selector.
- `KItemChangeRes::GetHorseRes`: `row = particular * 10 + level + 2`; common result uses `tableValue - 2` plus client table selector.
- NpcRes tables may use sex, mount state, action, and part-specific selectors; preview before trusting the row.
- Runtime visual correctness also depends on per-direction layer order (`layerOrderByDirection`), not only NpcRes row mapping.

Known-good examples:

- `Phiên Vũ`: `HorseRes` row 73 value `13` resolves to white horse `MA_HH/HB/HT_012_HR01.spr`, not `*_013`.
- `Địch Khái Trúc Trượng`: `GoldItem.txt:97`, `particular=2`, `level=10`, `MeleeRes` row 32 value `28` resolves to `MA_RW_026_HR01.spr`.
- Known-good smoke tests live in `tests/test_vltk_porting_smoke.py`; keep them passing when changing mapping or alias logic.

## Failure Cases To Record

- Inventory icon SPR is not a character animation part (`obj-staff13.spr`, `horse012.spr`, `obj-ma-cap*.spr`).
- Loose tables can be stale; PAK package order can override rows.
- GBK, TCVN3, CP1258, Chinese, Vietnamese, and mojibake aliases can refer to the same item.
- Resource tables can name missing SPRs; keep `missing-*`/candidate status instead of guessing.
- Wrong sex, action, direction, layer order, center/anchor, or frame count can make a visually wrong sheet even when files decode.
- Cached runtime sheets or stale query-string versions can mask fixes; bump asset version in runtime constants after regenerate.
- Auto-applied local preset (e.g., wardrobe `localStorage`) can override newly fixed default sheets.
- Invalid spritesheet metadata (`frameWidth`/`frameHeight`/`endFrame`) can cause flicker, duplicate silhouettes, or disappearing sprites.
- Preview report paths can be stale; ensure `--local-source-root` points at the current `<slug>` source folder and report status matches human review.

## Report Back

Answer in Vietnamese when the user is Vietnamese. Include concrete file paths, table lines, resolved SPRs, preview image/report paths, copied source folder, PAK manifest entry, validation commands, and uncertainty notes.

When runtime bugfix is requested, also include:
- Repro steps used in browser automation.
- Before/after screenshot artifact paths.
- Whether preset/cache was reset and whether combo or default sheet is active.
