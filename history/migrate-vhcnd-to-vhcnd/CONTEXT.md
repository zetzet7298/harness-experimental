# CONTEXT — Migrate vhcnd references to vhcnd

> Locked decisions for downstream Khuym agents. Source of truth.

## Feature

`migrate-vhcnd-to-vhcnd` — replace every `vhcnd` reference (path, identifier,
asset key, animation prefix, gitnexus repo name, localStorage key, group alias,
documentation, .codex skill) across the harness, the H5 game source, and any
future skills with `vhcnd`. Make `/var/www/vhcnd/` self-contained by moving
required assets from `/var/www/vhcnd/` into vhcnd. After completion, the
codebase must contain zero `vhcnd` mentions and `/var/www/vhcnd/` must not
be required by anything in vhcnd, harness, or game-source.

## Scope (boundary)

In scope:
- Harness repo `/var/www/vltk-h5-survivors/harness-experimental` — AGENTS.md,
  README, docs/HARNESS.md, docs/TEST_MATRIX.md, docs/product/*, docs/decisions/0004,
  docs/stories/backlog.md, docs/validation/* (38 files referencing vhcnd).
- Game source repo `/var/www/vltk-h5-survivors/game-source` — 23 scripts with
  hardcoded `/var/www/vhcnd/...` paths, 1 doc, 59 data JSON, 11 src ts, 5
  tests (430 files referencing vhcnd).
- `.codex/skills/{vltk-item-research, vltk-skill-porting, vltk-map-porting,
  vltk-spr-porting}/` — references to `/var/www/vhcnd` and the `vhcnd` repo
  identifier.
- `/var/www/vhcnd/` itself — `web/manifest*.json`, `tools/scan_required_spr.py`
  default `--spr-root`, AGENTS.md (needs canonical workspace routing).
- `/var/www/vhcnd/` — source of named SPR/PNG assets that must be moved
  into vhcnd to break the coupling.
- GitNexus configuration — repo registrations and the `@vltk-porting` group
  alias (must become `@vhcnd-porting` or equivalent).

Out of scope (deferred or unrelated):
- The OAuth token file at `/var/www/vhcnd/xvme2hyr@hongnhanbinhhung.com.json`
  (flagged as a security observation; the user will decide whether to remove).
- Touching `data.controller/` (2 GB) inside vltkunity beyond verifying it is
  not needed by vhcnd.
- Decoding the engine FNV-1a hash and rebuilding a name→hash map (recorded as
  `Open Question OQ-1` for planning to address if needed).

## Domain types

- `ORGANIZE` — repository layout, asset roots, gitnexus repo names, ignored
  paths.
- `READ` — AGENTS.md, docs/HARNESS.md, story packets, validation reports,
  skill SKILL.md files.
- `RUN` — porting scripts (`scripts/vltk-*.py`, `scripts/build-vltk-wardrobe-debug.py`,
  `scripts/check-no-runtime-vhcnd.sh`), test runners (`tests/test_vltk_porting_smoke.py`,
  `npm run test:smoke`, `npm run typecheck`, `npm run build`).
- `SEE` — the H5 runtime asset paths (`/assets/character/vhcnd/...`),
  Playwright baseline screenshot, equipment scene, animation prefixes.
- `CALL` — none (no external API surface).

## Locked decisions

| ID | Decision | Rationale |
| --- | --- | --- |
| D1 | Pre-migration snapshot pushed to `main` in both `harness-experimental` (`62063e8..998bdba`) and `game-source` (`2857628..dd141dd`). | User explicitly chose A "push thẳng main". Snapshot is the rollback point if migration must be reverted. |
| D2 | Minimal `.gitignore` adopted: harness ignores `.khuym/`, `.kiro/`, `*.code-workspace`, OS noise; game-source adds `equipment-visual-runner-summary-*.json` and `equipment-visual-compose-summary-*.json` (scratch summaries). All other US-011 evidence committed. | User approved A. Snapshot is faithful; canonical evidence (`build-plan.json`, `shard-000.json`) is preserved. |
| D3 | Rebrand is exhaustive. Every textual occurrence of `vhcnd` becomes `vhcnd`: `/var/www/vhcnd/...`, asset keys (`vhcnd-equipped-tu-la-...`), animation prefixes (`player-run-mounted-vhcnd-h*-a*`), localStorage keys (`vhcnd-wardrobe-selection-v1`), gitnexus repo (`vhcnd` → `vhcnd`), group alias (`@vltk-porting` → `@vhcnd-porting`), folder names (`public/assets/character/vhcnd/` → `public/assets/character/vhcnd/`), file slugs in scripts and packets. | User chose B; "đổi triệt để mọi nơi". Accepts regenerated US-011 evidence and Playwright baseline. |
| D4 | Single canonical source-of-truth root for legacy data is `/var/www/vhcnd/` standalone. `/var/www/vhcnd/` and `/var/www/vhcnd/` are no longer canonical sources after migration. | User chose B. Accepts that vhcnd must absorb whatever it currently borrows from vltkunity. |
| D5 | Coupling break strategy: MOVE assets from vltkunity into vhcnd, do not copy and leave duplicates. After the move, `/var/www/vhcnd/` should not be required by vhcnd, harness, game-source, or any .codex skill. | User stated "cần giải quyết luôn tính cô lập" and "nếu vhcnd đang dùng gì liên quan đến vltkunity thì cần move từ vltkunity qua vhcnd luôn". |
| D6 | Move scope = the 7 paths vhcnd manifests currently reference: `item_spr/`, `item_spr_img/`, `other-game/download-source/data_cdn_spr_img/` (manifest target; ghost on disk), `other-game/item_spr_like_img/`. Final layout inside vhcnd preserves the same relative names so existing manifests keep working. | User chose A. Matches the existing `web/manifest*.json` configuration; no manifest rewrite needed beyond root path update. |

## Scout evidence (paths read or counted)

- `/var/www/vhcnd/AGENTS.md` — workspace routing for vhcnd; Python tools live in `tools/`.
- `/var/www/vhcnd/web/manifest.json` → `root: "/var/www/vhcnd/item_spr_img"` (13,557 PNG).
- `/var/www/vhcnd/web/manifest_required_config_missing_only.json` → `sprRoot: "/var/www/vhcnd/item_spr"` (1,627 named SPR available, 820 still missing for 2,230 required).
- `/var/www/vhcnd/web/manifest_data_cdn_lite.json` → `root: "/var/www/vhcnd/other-game/download-source/data_cdn_spr_img"` (42,809 entries; the disk path does not exist; metadata-only).
- `/var/www/vhcnd/web/manifest_downloads_like.json` → `root: "/var/www/vhcnd/other-game/item_spr_like_img"` (672 entries).
- `/var/www/vhcnd/tools/scan_required_spr.py` default `--spr-root=/var/www/vhcnd/item_spr` (path does not exist on disk; tool fails with 5,011/5,011 missing).
- `/var/www/vhcnd/datasets/data_cdn/pak_extract/data_cdn_pak_extract/{updata06,spr,...}/*.spr` — 34,419 hash-named SPR.
- `/var/www/vhcnd/sources/Client/Classes/engine/KStrBase.cpp` lines 881-887 — engine hash = FNV-1a (multiplier 16777619, XOR after multiply) on `toupper(*key)`, init `hash = 0`.
- `/var/www/vhcnd/archives/data_cdn.zip` (3.2 GB) contents = `data/*.pak` only (no named files).
- `/var/www/vhcnd/item_spr/spr/item/equip/horse/horse003.spr` exists; FNV-1a of any prefix variant does NOT match a file in `/var/www/vhcnd/datasets/...`.
- `/var/www/vhcnd/` lacks any reference to `/var/www/vhcnd` (verified by ripgrep across config-like files).
- Game source files referencing `vhcnd`: hardcoded paths in `scripts/vltk-normalize-port-packet.py`, `scripts/build-vltk-wardrobe-debug.py`, `scripts/vltk-audit-equipment-stat-coverage.py`, `scripts/vltk-extract-skill-assets.py`, `scripts/vltk-extract-required-sprs.py`, `scripts/check-no-runtime-vhcnd.sh`, `scripts/vltk-normalize-equipment-index.py`. Identifier strings in `src/game/scenes/PreloadScene.ts`, `src/game/scenes/EquipmentScene.ts`, `src/game/scenes/GameScene.ts`, `src/game/constants.ts`. Asset roots under `public/assets/character/vhcnd/`, `public/assets/skills/vhcnd/`, `public/assets/maps/vhcnd/`. Test snapshot baseline at `tests/smoke/equipment-loadout.spec.ts-snapshots/equipment-loadout-3piece-chromium-linux.png`.
- Game source files referencing `vltkunity`: `scripts/vltk-build-equipment-icon-manifest.py`, `public/assets/equipment-icons/manifest.json`.
- Harness file referencing `vltkunity`: `docs/validation/2026-05-18-vhcnd-equipment-formula-icon-parity.md`.

## Counts at lock time

| Surface | vhcnd refs |
| --- | --- |
| harness-experimental | 38 files |
| game-source | 430 files |
| .codex skills (in harness) | 7 files (vltk-item-research, vltk-skill-porting, vltk-map-porting, vltk-spr-porting) |
| vhcnd internal manifests pointing at vltkunity | 5 files (`web/manifest.json`, `web/manifest_data_cdn_lite.json`, `web/manifest_downloads_like.json`, `web/manifest_required_config_missing_only.{json,csv}`) |

| Asset move (vltkunity → vhcnd) | Size |
| --- | --- |
| `item_spr/` | 28 MB (1,627 named SPR) |
| `item_spr_img/` | 82 MB (13,557 named PNG) |
| `other-game/data_cdn_spr_img/` | metadata only; physical path missing |
| `other-game/item_spr_like_img/` | 4.4 MB (672 entries) |

Free disk on `/var/www`: 37 GB free / 467 GB total (92% used). The move is feasible without copy because both roots are on the same filesystem (`/`).

## Open questions for planning (not blocking lock)

- **OQ-1**: Is name→hash mapping required for the migration to succeed? Engine hash function is FNV-1a custom (KStrBase.cpp), but `horse003.spr` does not match any hash on disk under tested path variants. Either the engine reads from the unhashed `data_cdn.zip` extract through a different path, or the named SPRs in vltkunity were produced by a separate extraction pipeline (named at extraction time). Planning must answer this before any item-table-driven SPR resolution work.
- **OQ-2**: Should `data.controller/` (2 GB) inside vltkunity also move? Not currently referenced by vhcnd; deferred.
- **OQ-3**: Should the gitnexus group `@vltk-porting` be renamed to `@vhcnd-porting`, or split (game-source repo + vhcnd repo with no umbrella)? Default per D3 is rename.
- **OQ-4**: How does this migration interact with the planned US-004 (real VLTK table import)? Tables now live at `/var/www/vhcnd/sources/ServerNew/_bin_v2_/gs/Settings/item/`, encoded in CP-1258 / GBK based on samples; US-004 likely subsumed.

## Deferred ideas (not in this feature)

- Removing the OAuth token file at `/var/www/vhcnd/xvme2hyr@...json`.
- Building a name→hash mapping pipeline for the 34,419 hash SPRs in vhcnd datasets.
- Cleaning up vltkunity entirely after migration (the user has not authorized deletion of items not used by vhcnd).
- Updating Playwright baseline screenshot proactively (regenerate is expected, but timing is for planning).

## Refs (for downstream agents)

- Pre-migration commits — harness `998bdba`, game-source `dd141dd`. Either commit can be used as a rollback target.
- Engine hash function — `/var/www/vhcnd/sources/Client/Classes/engine/KStrBase.cpp:881-887`.
- Existing runtime guard against out-of-scope vhcnd — `/var/www/vltk-h5-survivors/game-source/scripts/check-no-runtime-vhcnd.sh` (must be renamed and the needle updated to vhcnd).
- US-011 story packet — `/var/www/vltk-h5-survivors/harness-experimental/docs/stories/epics/E03-vhcnd-asset-porting/US-011-port-vhcnd-equipment-system/`.

## Handoff

CONTEXT.md is the source of truth. Invoke `khuym:planning` to produce work
shape, phase plan or epic map, current-story preparation, and to surface
spike requirements for OQ-1 (name→hash mapping) before implementation.
