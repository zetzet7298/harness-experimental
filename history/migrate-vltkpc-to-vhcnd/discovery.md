# Discovery — migrate-vltkpc-to-vhcnd

> Repo reality and prior-art findings collected during planning.
> Source: scout commands run from harness, vhcnd, vltkunity, game-source.
> Read `CONTEXT.md` first.

## Repos and roots

| Root | Indexed as | Purpose |
| --- | --- | --- |
| `/var/www/vltk-h5-survivors/harness-experimental` | (no gitnexus repo) | Agent harness/control workspace; Khuym onboarded. Branch `main`, remote `zetzet7298/harness-experimental`. |
| `/var/www/vltk-h5-survivors/game-source` | gitnexus repo `vltk-h5-survivors` | H5 Phaser/Vite game prototype. Branch `main`, remote `zetzet7298/vltk-h5-survivors`. |
| `/var/www/vltkpc` | gitnexus repo `vltkpc` (group `@vltk-porting` member `pc`) | Legacy PC source mirror. Source of US-001..US-011 evidence. |
| `/var/www/vhcnd` | not indexed | Standalone alternative source (target of D4). 50 GB. Has `sources/Client`, `sources/ServerNew`, `sources/SwordOnline`, `archives/data_cdn.zip` (3.2 GB). |
| `/var/www/vltkunity` | not indexed | Umbrella that previously held named SPR/PNG that vhcnd manifests reference. Per D5/D6, the four paths move into vhcnd. |

## Decisions already locked (from CONTEXT.md)

D1..D6 — see CONTEXT.md.

## Critical-patterns review

`history/learnings/critical-patterns.md` is a placeholder. No prior pattern
applies to this migration. Khuym priority rule 7 is satisfied because
critical-patterns existence is verified, not its contents.

## Repo evidence collected

### Harness

- 38 files reference `vltkpc` (counted by `rg -i vltkpc -l`).
- Existing skill files referencing vltkpc/vltk-porting/etc:
  `.codex/skills/vltk-{item-research, skill-porting, map-porting, spr-porting}/`.
- Story epic folder at `docs/stories/epics/E03-vltkpc-asset-porting/`.
- TEST_MATRIX has many implemented rows under E03; rebrand must preserve
  evidence.

### Game source

- 430 files reference `vltkpc` (counted by `rg -i vltkpc -l`).
- Hardcoded out-of-scope paths under `/var/www/vltkpc/extracted_build_jxwin_soucgoc_hoiquanvolam/source_from_vmdk/SourceNew/swrod3/bin/Client/Settings/item/` in:
  - `scripts/vltk-normalize-port-packet.py`
  - `scripts/build-vltk-wardrobe-debug.py`
  - `scripts/vltk-audit-equipment-stat-coverage.py`
  - `scripts/vltk-extract-skill-assets.py`
  - `scripts/vltk-extract-required-sprs.py`
  - `scripts/vltk-normalize-equipment-index.py`
  - `scripts/check-no-runtime-vltkpc.sh`
- Internal identifiers: animation prefix `player-{run,idle}-mounted-vltkpc-h{H}-a{A}`,
  localStorage key `vltkpc-wardrobe-selection-v1`, `playerSheet` constant,
  asset folder `public/assets/character/vltkpc/`, `public/assets/skills/vltkpc/`,
  `public/assets/maps/vltkpc/`.
- Two files reference `vltkunity` instead of `vltkpc`:
  `scripts/vltk-build-equipment-icon-manifest.py`,
  `public/assets/equipment-icons/manifest.json`.

### vhcnd

- Item tables at `/var/www/vhcnd/sources/ServerNew/_bin_v2_/gs/Settings/item/` (49 files) and `Settings/item/004/` (67 files). GoldItem.txt lives under `004/`.
- Tables encoded in CP-1258 / Vietnamese-Windows (sample read of `horse.txt` shows mojibake when read as utf-8).
- Engine FNV-1a hash function at `sources/Client/Classes/engine/KStrBase.cpp:881-887`:
  `hash *= 16777619; hash ^= toupper(*key);` with `hash = 0` initial value.
- Hash SPR store: 34,419 files in `datasets/data_cdn/pak_extract/data_cdn_pak_extract/{updata06, spr, ...}/<8-hex>.spr`.
- `archives/data_cdn.zip` (3.2 GB) contains only `data/*.pak` files; named SPRs are not inside.
- `web/manifest*.json` files reference `/var/www/vltkunity/...` as their `root`/`sprRoot`.
- `tools/scan_required_spr.py` argparse defaults:
  - `--config-dir` = `/var/www/vhcnd/sources/servernew_up/ServerNew/_bin_v2_/gs/Settings/item/004` (path does NOT exist; the real dir is `sources/ServerNew/...` without `servernew_up/`).
  - `--spr-root` = `/var/www/vhcnd/item_spr` (does NOT exist before E_M1 move).
- `xvme2hyr@hongnhanbinhhung.com.json` at vhcnd root contains OAuth tokens (out of scope; recorded for the user).

### vltkunity

- `/var/www/vltkunity/item_spr/` — 28 MB, 1,627 named SPR (e.g., `spr/item/equip/horse/horse003.spr`).
- `/var/www/vltkunity/item_spr_img/` — 82 MB, 13,557 named PNG.
- `/var/www/vltkunity/other-game/item_spr_like_img/` — 4.4 MB, 672 entries.
- `/var/www/vltkunity/other-game/download-source/data_cdn_spr_img/` — referenced in vhcnd manifest with 42,809 entries; the directory does NOT exist on disk (metadata-only manifest).
- Reverse direction: `rg /var/www/vhcnd /var/www/vltkunity` returns zero references; vltkunity does not consume anything from vhcnd. The migration direction is one-way.
- Other vltkunity contents NOT in scope for D6: `client/` (186 MB), `server/` (123 MB), `data.controller/` (2 GB), `item_data/`, `item_spr_img_test/`, `item_spr_img_x4/` (96 MB), `item_spr_report/`, `scripts/`, `tools/`, `vhcnd/` (an empty `.codex/`).

### Hash probe pre-result

Tested FNV-1a (init=0) for `horse003.spr` across all reasonable path prefixes:
`spr/item/equip/horse/horse003.spr`, `spr\item\equip\horse\horse003.spr`,
`/spr/...`, both cases. None of the produced 8-hex hashes match a file under
`vhcnd/datasets/.../*.spr`. This is the seed evidence for OQ-1 and the reason
E_M2 spike exists. The named SPRs in vltkunity were likely produced by a
different extraction pipeline that preserved filenames at extract time, not
hashed and re-resolved.

## Patterns reused

- Khuym priority rule 5: spike must halt pipeline if its question fails.
- US-011 audit chain (in `execplan.md`) is the canonical proof set; the
  migration must keep every audit runnable post-rebrand.

## Pre-flight reality verification (re-run during validating)

| Check | Result |
| --- | --- |
| Filesystem identity | `vhcnd` and `vltkunity` both on `/`. Move is atomic rename. |
| Free space | 37 GB free / 467 GB total. Adequate for spike report files; the move itself does not consume space. |
| vhcnd → vltkunity refs | Exactly the 5 known consumers in `web/`. No new finds. |
| vltkunity → vhcnd refs | Zero. Direction is one-way. |
| Engine hash code reference | Verified at `KStrBase.cpp:881-887` with `hash *= 16777619; hash ^= toupper(*key);` and `hash = 0` init. |
