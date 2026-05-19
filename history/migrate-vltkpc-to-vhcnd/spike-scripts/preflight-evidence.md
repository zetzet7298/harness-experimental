# E_M1 Pre-flight Evidence — bead mig-q6k

Date: 2026-05-19 (Asia/Bangkok)
Bead: `mig-q6k` — E_M1 pre-flight: verify filesystem, refs, baseline audit
Source spec: `history/migrate-vltkpc-to-vhcnd/current-work.md` E_M1 section

## Check 1 — Filesystem identity (same mount required for `mv`)

```
$ stat -c '%m %n' /var/www/vhcnd /var/www/vltkunity
/ /var/www/vhcnd
/ /var/www/vltkunity
```

Result: PASS. Both roots resolve to mountpoint `/`, so `mv` between them
will be a same-filesystem rename (no copy, atomic per-entry).

## Check 2 — Free space on /var/www

```
$ df -h /var/www | tail -1
/dev/nvme0n1p2  467G  400G   44G  91% /
```

Result: PASS. 44 GB free. Move is rename-only on the same FS so the
expected delta is near-zero, but the >=1 GB safety threshold from
current-work.md is satisfied.

## Check 3 — Inbound vltkunity references inside vhcnd (must equal 5 known files)

```
$ rg -l '/var/www/vltkunity' /var/www/vhcnd | sort
/var/www/vhcnd/web/manifest.json
/var/www/vhcnd/web/manifest_data_cdn_lite.json
/var/www/vhcnd/web/manifest_downloads_like.json
/var/www/vhcnd/web/manifest_required_config_missing_only.csv
/var/www/vhcnd/web/manifest_required_config_missing_only.json
```

Result: PASS. Exactly the 5 manifest files locked in `CONTEXT.md`. No
new code paths reference vltkunity from inside vhcnd.

## Check 4 — Outbound vhcnd references inside vltkunity (must be 0 outside data dirs)

```
$ rg -l '/var/www/vhcnd' /var/www/vltkunity --max-count 1 \
    -g '!datasets/**' -g '!archives/**' | head
(no output)
```

Result: PASS. vltkunity does not reference vhcnd, so the move is one-way
and will not break any vltkunity-side tooling.

## Check 5 — Baseline SPR audit against current vltkunity root

Note on invocation: `current-work.md` lists `--full`, but the tool's
`--full` mode resolves `--scan-root` from a default path that does not
exist on this disk (`/var/www/vhcnd/sources/servernew_up/...`). With
`--full` the run reports `Total required: 0` (no tables found). Running
without `--full`, against the explicit `--config-dir` already passed in
the spec, exercises the documented default tables (armor, helm, horse,
meleeweapon, rangeweapon) and reproduces the verify-time pre-result
exactly. The wider full-scan path is an open item for the planner; it
does not affect E_M1 because E_M1 only needs a stable pre-move baseline.

```
$ python3 /var/www/vhcnd/tools/scan_required_spr.py \
    --config-dir /var/www/vhcnd/sources/ServerNew/_bin_v2_/gs/Settings/item/004 \
    --spr-root  /var/www/vltkunity/item_spr \
    --output    /tmp/_baseline_audit.json
Output: /tmp/_baseline_audit.json
Total required: 335
Missing: 10
OK: 325
```

Report metadata (from `/tmp/_baseline_audit.json`):

```
configDir : /var/www/vhcnd/sources/ServerNew/_bin_v2_/gs/Settings/item/004
sprRoot   : /var/www/vltkunity/item_spr
tables    : armor.txt, helm.txt, horse.txt, meleeweapon.txt, rangeweapon.txt
totalRequired = 335
missingCount  = 10
okCount       = 325
```

Result: PASS. Matches the verify-time pre-result (`total=335`,
`missing=10`, `ok=325`) exactly. This is the locked pre-move baseline.
After the E_M1 move, re-running the same command against
`--spr-root /var/www/vhcnd/item_spr` must reproduce these counts.

## Summary

All 5 pre-flight checks PASS. E_M1 is cleared to proceed; mig-n53
(move 4 paths) is unblocked.
