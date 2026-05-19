# field-edit-evidence — mig-piy (E_M1 manifest + tool field edits)

> Status: **BLOCKED** (no edits performed; evidence is pre-edit only).
> Worker: Patch · Bead: mig-piy · Date: 2026-05-19

This bead asked the worker to edit 6 files in `/var/www/vhcnd/` and then verify
that `rg /var/www/vltkunity /var/www/vhcnd` returns zero. Pre-flight grep
revealed scope divergence between the bead's edit list and acceptance #2; the
worker stopped before editing per the parent instruction:

> Halt and emit [BLOCKED] if … any "old" value in the table above does not
> match what's actually in the file (do not assume; grep first, report the
> divergence) … or `rg /var/www/vltkunity /var/www/vhcnd` is non-zero
> (revert your edits in this case before reporting).

No revert is required because no edits were made.

## Pre-edit state — bead's 6 listed targets

Confirmed by `python3 -c "import json; …"` and `head -1`:

| File | Field | Pre-edit value | Bead-expected "old" | Match? |
| --- | --- | --- | --- | --- |
| `web/manifest.json` | top-level `root` | `/var/www/vltkunity/item_spr_img` | `/var/www/vltkunity/item_spr_img` | ✓ |
| `web/manifest_required_config_missing_only.json` | top-level `sprRoot` | `/var/www/vltkunity/item_spr` | `/var/www/vltkunity/item_spr` | ✓ |
| `web/manifest_required_config_missing_only.csv` | header row | `path,name,configFile,configLine,absPath` (no vltkunity) | `/var/www/vltkunity/item_spr` | **✗ divergence** |
| `web/manifest_data_cdn_lite.json` | top-level `root` | `/var/www/vltkunity/other-game/download-source/data_cdn_spr_img` | same | ✓ |
| `web/manifest_downloads_like.json` | top-level `root` | `/var/www/vltkunity/other-game/item_spr_like_img` | same | ✓ |
| `tools/scan_required_spr.py` argparse `--config-dir` default | line 140 | `/var/www/vhcnd/sources/servernew_up/ServerNew/_bin_v2_/gs/Settings/item/004` | same | ✓ |
| `tools/scan_required_spr.py` argparse `--scan-root` default | line 161 | `/var/www/vhcnd/sources/servernew_up/ServerNew/_bin_v2_/gs/Settings/item` | same | ✓ |
| `tools/scan_required_spr.py` argparse `--spr-root` default | line 145 | `/var/www/vhcnd/item_spr` | unchanged | ✓ |

5 of 6 file targets match the bead's `old` values exactly. The CSV is
the only divergence at the field level.

### CSV divergence detail

The bead's row for `manifest_required_config_missing_only.csv` says:

> | `web/manifest_required_config_missing_only.csv` | header containing path | `/var/www/vltkunity/item_spr` | `/var/www/vhcnd/item_spr` |

The actual file has no metadata header containing `vltkunity`. The first
line is the literal column header `path,name,configFile,configLine,absPath`.
820 of the 4,686 data rows contain `/var/www/vltkunity/...` in the
`configFile` and/or `absPath` columns:

```
$ head -3 /var/www/vhcnd/web/manifest_required_config_missing_only.csv
path,name,configFile,configLine,absPath
"Spr/item/equip/bangle/obj-bangle32.spr","Minh Phượng Không Minh Tụ","/var/www/vltkunity/item_data/settings/item/004/goldequip.txt","2939","/var/www/vltkunity/item_spr/Spr/item/equip/bangle/obj-bangle32.spr"
"Spr/item/equip/bangle/obj-bangle33.spr","Độc Cô Kim Uyển","/var/www/vltkunity/item_data/settings/item/004/goldequip.txt","5663","/var/www/vltkunity/item_spr/Spr/item/equip/bangle/obj-bangle33.spr"

$ grep -c 'vltkunity' /var/www/vhcnd/web/manifest_required_config_missing_only.csv
820
```

A naïve `s|/var/www/vltkunity/item_spr|/var/www/vhcnd/item_spr|g`
would only rewrite the `absPath` cells (which is correct, because
`item_spr/` was moved from vltkunity to vhcnd by mig-n53). It would NOT
touch `configFile` cells whose paths point to `item_data/settings/...`,
which was NOT included in the D6 move scope (still lives in vltkunity).
That partial rewrite is consistent with the migration's locked decisions,
but it is not "header" replacement — the bead's textual instruction is
out of step with the actual file format.

## Out-of-scope vltkunity references inside /var/www/vhcnd

Acceptance #2 of the bead asks for:

> `rg /var/www/vltkunity /var/www/vhcnd` returns ZERO matches.

Pre-edit scan shows 832 matches across 12 files. The bead's edit list
covers 6 of these files. The other 6 files contain references that the
bead does not address:

```
$ rg -l '/var/www/vltkunity' /var/www/vhcnd
/var/www/vhcnd/other-game/item_spr_like_img/report.json
/var/www/vhcnd/web/manifest_required_config_missing_only.json     ← in bead scope
/var/www/vhcnd/web/manifest_required_config_missing_only.csv      ← in bead scope
/var/www/vhcnd/web/manifest_downloads_like.json                   ← in bead scope
/var/www/vhcnd/web/manifest.json                                  ← in bead scope
/var/www/vhcnd/item_spr_img/manifest_required_config.json
/var/www/vhcnd/item_spr_img/manifest_downloads.json
/var/www/vhcnd/item_spr_img/manifest_downloads_like.json
/var/www/vhcnd/web/manifest_data_cdn_lite.json                    ← in bead scope
/var/www/vhcnd/item_spr_img/manifest_required_config_scan_full.json
/var/www/vhcnd/item_spr_img/manifest.json
/var/www/vhcnd/item_spr_img/manifest_data_cdn_lite.json
```

Out-of-bead-scope files (6) and what they reference:

| File | Reference type |
| --- | --- |
| `item_spr_img/manifest.json` | `root: "/var/www/vltkunity/item_spr_img"` (item_spr_img/ tree was moved; this manifest sits *inside* the moved tree as a duplicate of `web/manifest.json`) |
| `item_spr_img/manifest_data_cdn_lite.json` | `root: "/var/www/vltkunity/other-game/download-source/data_cdn_spr_img"` (duplicate of `web/manifest_data_cdn_lite.json`) |
| `item_spr_img/manifest_downloads.json` | `root: "/var/www/vltkunity/other-game/downloads_spr_img_struct"` — `downloads_spr_img_struct/` is NOT in D6 move scope (still in vltkunity) |
| `item_spr_img/manifest_downloads_like.json` | `root: "/var/www/vltkunity/other-game/item_spr_like_img"` (duplicate) |
| `item_spr_img/manifest_required_config.json` | `root: "/var/www/vltkunity/item_data/settings/item/004"` — `item_data/` is NOT in D6 move scope |
| `item_spr_img/manifest_required_config_scan_full.json` | `scanScope: "/var/www/vltkunity/item_data/settings/item"` AND `sprRoot: "/var/www/vltkunity/item_spr"` — first not moved, second moved |
| `other-game/item_spr_like_img/report.json` | `spr_root: "/var/www/vltkunity/other-game/item_spr_like"` (NOT moved) AND `out_root: "/var/www/vltkunity/other-game/item_spr_like_img"` (moved) |

These 6 files contain a mix of:
- (a) references to paths that were already moved by mig-n53 (should become `/var/www/vhcnd/...`), and
- (b) references to paths that were NOT moved by D6 (`item_data/`, `downloads_spr_img_struct/`, `item_spr_like/`) and therefore should still legitimately point at vltkunity until those paths also get moved or the references get neutralised.

A blanket `s|/var/www/vltkunity|/var/www/vhcnd|g` over these files would
rewrite (b) to a path that does not exist on disk. It is not safe.

## Why this is BLOCKED, not partially executed

Per the parent prompt's halt rule, two conditions hold simultaneously:

1. **CSV row "old" value mismatch** — the literal textual instruction
   ("header containing path") cannot be satisfied as written; the file
   has no such header, only data-row occurrences spread across two
   different `vltkunity/...` prefixes (one in D6 move scope, one not).
2. **Acceptance #2 unachievable from the listed scope** — even with all
   6 listed files perfectly edited, 6 other files in `/var/www/vhcnd/`
   still contain `/var/www/vltkunity` strings, some of which legitimately
   point at paths excluded by D6.

The worker did not edit anything because per spec the worker would have
to revert on a non-zero `rg` result. Reverting after partial edits would
produce no net progress, churn, and a misleading evidence trail.

## Recommended planner moves (not done by this worker)

Pick one or split into beads:

A. **Tighten acceptance #2** to scope-bounded grep:
   ```
   rg /var/www/vltkunity /var/www/vhcnd/web /var/www/vhcnd/tools
   ```
   then this bead can edit just the 6 listed files (with a clarified
   CSV instruction) and pass cleanly.

B. **Expand bead scope** to also rewrite the 6 files under
   `/var/www/vhcnd/item_spr_img/` and `/var/www/vhcnd/other-game/...`,
   but specify *per-field* rewrite rules so paths excluded by D6
   (`item_data/`, `downloads_spr_img_struct/`, `item_spr_like/`)
   remain pointing at vltkunity (or get neutralised some other way).

C. **Move additional vltkunity paths into vhcnd** (extends D6) so a
   blanket rewrite becomes safe, then re-run this bead.

D. **Delete the duplicate manifests under `item_spr_img/`** (they
   appear to be artefacts of the original extraction in vltkunity that
   got dragged into vhcnd by the mig-n53 directory rename) and adjust
   `report.json` similarly.

The CSV instruction also needs to be reworded — "header containing path"
does not match the actual file, and the right rewrite is per-cell on
the `absPath` column only (or per-cell on any cell whose path begins
with `/var/www/vltkunity/item_spr/`).

## Reservation

```
$ node .codex/khuym_reservations.mjs reserve --agent "Patch" --bead "mig-piy" \
    --path /var/www/vhcnd/web/manifest.json \
    --path /var/www/vhcnd/web/manifest_required_config_missing_only.json \
    --path /var/www/vhcnd/web/manifest_required_config_missing_only.csv \
    --path /var/www/vhcnd/web/manifest_data_cdn_lite.json \
    --path /var/www/vhcnd/web/manifest_downloads_like.json \
    --path /var/www/vhcnd/tools/scan_required_spr.py \
    --path history/migrate-vltkpc-to-vhcnd/spike-scripts/field-edit-evidence.md \
    --ttl 3600 --json
{ ok: true, reservation.id: "resv-mpcly4ip-ehnmmp", conflicts: [] }
```

Released at end of session (no edits performed).
