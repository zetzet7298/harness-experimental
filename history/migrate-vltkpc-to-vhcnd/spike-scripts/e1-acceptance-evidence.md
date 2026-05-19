# E_M1 acceptance evidence — mig-6dg

Date: 2026-05-19
Agent: mig-6dg-worker
Feature: migrate-vltkpc-to-vhcnd

## Result

PASS. All requested E_M1 post-move acceptance checks passed.

## Baseline

Pre-move baseline from mig-q6k: `totalRequired=335`, `missingCount=10`, `okCount=325`.

## Checks

### 1. Zero `/var/www/vltkunity` refs under `/var/www/vhcnd`

Command requested:

```sh
find /var/www/vhcnd -type f \( -name '*.json' -o -name '*.csv' -o -name '*.html' -o -name '*.md' -o -name '*.txt' -o -name '*.py' -o -name '*.sh' -o -name '*.js' -o -name '*.mjs' -o -name '*.ts' -o -name '*.tsx' -o -name '*.yml' -o -name '*.yaml' -o -name '*.xml' \) -print0 | xargs -0 grep -Il '/var/www/vltkunity'
```

Output: no matching file paths.

Observed shell status under `set -o pipefail`: `123` from `xargs` because `grep` found no matches. Acceptance criterion is zero returned refs; this passed.

### 2. Required moved horse SPR resolves

Command:

```sh
ls /var/www/vhcnd/item_spr/spr/item/equip/horse/horse003.spr
```

Output:

```text
/var/www/vhcnd/item_spr/spr/item/equip/horse/horse003.spr
```

Exit: `0`.

### 3. `scan_required_spr.py` default run

Command:

```sh
python3 /var/www/vhcnd/tools/scan_required_spr.py
```

Output:

```text
Output: /var/www/vhcnd/web/manifest_required_config_scan.json
Total required: 335
Missing: 10
OK: 325
```

Exit: `0`.

### 4. Parsed scan manifest

Parsed `/var/www/vhcnd/web/manifest_required_config_scan.json`:

```text
totalRequired=335
okCount=325
missingCount=10
manifest_path=/var/www/vhcnd/web/manifest_required_config_scan.json
```

Comparison: `totalRequired` matches baseline `335`; `missingCount=10` is equal to baseline limit `10`, so `missingCount <= 10` passes.

## Decision

Comparable to pre-move baseline and within acceptance threshold. E_M1 acceptance passed.
