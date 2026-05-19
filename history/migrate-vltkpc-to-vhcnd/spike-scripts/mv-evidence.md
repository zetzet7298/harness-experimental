# E_M1 Move Evidence — bead mig-n53

Date: 2026-05-19 (Asia/Bangkok)
Bead: `mig-n53` — E_M1 move: 4 paths vltkunity → vhcnd
Worker: worker-mig-n53 (Khuym executing)
Source spec: `history/migrate-vltkpc-to-vhcnd/current-work.md` E_M1 "Move steps"
Pre-flight ref: `history/migrate-vltkpc-to-vhcnd/spike-scripts/preflight-evidence.md` (mig-q6k)

## Re-verify (Check 3) immediately before mv

```
$ rg -l '/var/www/vltkunity' /var/www/vhcnd | sort
/var/www/vhcnd/web/manifest.json
/var/www/vhcnd/web/manifest_data_cdn_lite.json
/var/www/vhcnd/web/manifest_downloads_like.json
/var/www/vhcnd/web/manifest_required_config_missing_only.csv
/var/www/vhcnd/web/manifest_required_config_missing_only.json
```

Result: PASS. Same 5 manifest files as preflight; no new vhcnd→vltkunity refs.

## Pre-state of source/destination

Source paths (vltkunity) all exist:
- `/var/www/vltkunity/item_spr` ✓
- `/var/www/vltkunity/item_spr_img` ✓
- `/var/www/vltkunity/other-game/item_spr_like_img` ✓
- `/var/www/vltkunity/other-game/download-source/` ✓ (exists but EMPTY — `data_cdn_spr_img` ghost confirmed)

Destinations (vhcnd) all absent (clean target):
- `/var/www/vhcnd/item_spr` — absent
- `/var/www/vhcnd/item_spr_img` — absent
- `/var/www/vhcnd/other-game/item_spr_like_img` — absent
- `/var/www/vhcnd/other-game/download-source/data_cdn_spr_img` — absent
- `/var/www/vhcnd/other-game` — absent (must be created)

## OP1 — Move named SPR root

```
$ mv /var/www/vltkunity/item_spr /var/www/vhcnd/item_spr
exit=0
$ ls -d /var/www/vhcnd/item_spr
/var/www/vhcnd/item_spr
$ ls /var/www/vhcnd/item_spr/spr/item/equip/horse/horse003.spr
/var/www/vhcnd/item_spr/spr/item/equip/horse/horse003.spr
```

Result: PASS.

## OP2 — Move named PNG root

```
$ mv /var/www/vltkunity/item_spr_img /var/www/vhcnd/item_spr_img
exit=0
$ ls -d /var/www/vhcnd/item_spr_img
/var/www/vhcnd/item_spr_img
$ ls /var/www/vhcnd/item_spr_img/Spr/item/equip/armor/obj-ma-cloth11-3.png
/var/www/vhcnd/item_spr_img/Spr/item/equip/armor/obj-ma-cloth11-3.png
```

Result: PASS.

## OP3a — mkdir vhcnd/other-game (parent for OP3b)

```
$ mkdir -p /var/www/vhcnd/other-game
exit=0
$ ls -d /var/www/vhcnd/other-game
/var/www/vhcnd/other-game
```

Result: PASS.

## OP3b — Move like-img mirror

```
$ mv /var/www/vltkunity/other-game/item_spr_like_img /var/www/vhcnd/other-game/item_spr_like_img
exit=0
$ ls -d /var/www/vhcnd/other-game/item_spr_like_img
/var/www/vhcnd/other-game/item_spr_like_img
$ find /var/www/vhcnd/other-game/item_spr_like_img -type f | wc -l
673
$ du -sh /var/www/vhcnd/other-game/item_spr_like_img
4.4M	/var/www/vhcnd/other-game/item_spr_like_img/
```

Result: PASS. 673 files, 4.4 MB — matches CONTEXT.md baseline (672 entries / 4.4 MB; 673 vs 672 differs by `report.json` being counted in find vs not in original `ls` count).

## OP4 — Metadata-only ghost path

`/var/www/vltkunity/other-game/download-source/` exists in vltkunity but
contains no `data_cdn_spr_img` directory (confirmed `du -sh` = 4.0K, only
`.` and `..`). Per spec, this is metadata-only in the manifest; create the
empty target directory in vhcnd.

```
$ mkdir -p /var/www/vhcnd/other-game/download-source/data_cdn_spr_img
exit=0
$ ls -d /var/www/vhcnd/other-game/download-source/data_cdn_spr_img
/var/www/vhcnd/other-game/download-source/data_cdn_spr_img
```

Result: PASS (empty ghost directory created as expected).

## Acceptance criteria — final verification

| # | Criterion | Result |
| --- | --- | --- |
| 1 | `ls /var/www/vhcnd/item_spr/spr/item/equip/horse/horse003.spr` resolves | PASS |
| 2 | `ls /var/www/vhcnd/item_spr_img/Spr/item/equip/armor/obj-ma-cloth11-3.png` resolves | PASS |
| 3 | `ls /var/www/vhcnd/other-game/item_spr_like_img/` non-empty (673 files, 4.4 MB) | PASS |
| 4 | `ls /var/www/vhcnd/other-game/download-source/data_cdn_spr_img/` exists (empty) | PASS |
| 5 | `ls /var/www/vltkunity/item_spr` returns "No such file or directory" | PASS |
| 5 | `ls /var/www/vltkunity/item_spr_img` returns "No such file or directory" | PASS |
| 5 | `ls /var/www/vltkunity/other-game/item_spr_like_img` returns "No such file or directory" | PASS |

```
$ ls /var/www/vltkunity/item_spr 2>&1
ls: cannot access '/var/www/vltkunity/item_spr': No such file or directory
$ ls /var/www/vltkunity/item_spr_img 2>&1
ls: cannot access '/var/www/vltkunity/item_spr_img': No such file or directory
$ ls /var/www/vltkunity/other-game/item_spr_like_img 2>&1
ls: cannot access '/var/www/vltkunity/other-game/item_spr_like_img': No such file or directory
```

## Summary

All 4 mv/mkdir operations completed successfully on first try. Atomic
same-filesystem renames worked as predicted by mig-q6k. vhcnd is now the
self-contained owner of the named SPR / PNG / like-img assets. Next bead
mig-piy (manifest+tool field edits in /var/www/vhcnd) is unblocked.

Re-running the locked baseline audit against the new vhcnd root is the
responsibility of mig-piy (post-edit verification).
