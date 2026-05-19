# manifest-validation-evidence — mig-yv0

- Timestamp: 2026-05-19T20:18:20+07:00
- Scope: validation only after mig-428 residual reference patch

## 1. Text-aware zero-ref scan under /var/www/vhcnd

Command:
```bash
find /var/www/vhcnd -type f \( -name '*.json' -o -name '*.csv' -o -name '*.html' -o -name '*.md' -o -name '*.txt' -o -name '*.py' -o -name '*.sh' -o -name '*.js' -o -name '*.mjs' -o -name '*.ts' -o -name '*.tsx' -o -name '*.yml' -o -name '*.yaml' -o -name '*.xml' \) -print0 | xargs -0 grep -Il '/var/www/vltkunity'
```
Output:
```text
```
Exit status: 123

## 2-5. JSON, CSV, Python AST, and default path validation

Command:
```bash
python3 - <<'PY'
import ast, csv, json, sys
from pathlib import Path
json_files = [
    '/var/www/vhcnd/web/manifest_data_cdn_lite.json',
    '/var/www/vhcnd/web/manifest.json',
    '/var/www/vhcnd/web/manifest_required_config_missing_only.json',
    '/var/www/vhcnd/web/manifest_downloads_like.json',
    '/var/www/vhcnd/item_spr_img/manifest_data_cdn_lite.json',
    '/var/www/vhcnd/item_spr_img/manifest.json',
    '/var/www/vhcnd/item_spr_img/manifest_required_config_scan_full.json',
    '/var/www/vhcnd/item_spr_img/manifest_downloads_like.json',
    '/var/www/vhcnd/item_spr_img/manifest_downloads.json',
    '/var/www/vhcnd/item_spr_img/manifest_required_config.json',
    '/var/www/vhcnd/other-game/item_spr_like_img/report.json',
    '/var/www/vhcnd/other-game/downloads_spr_img_struct/downloads_spr_img_struct/report.json',
    '/var/www/vhcnd/reports/pipeline_reports/data_cdn_spr_img_report.json',
]
failed = False
print('JSON parse checks:')
for path in json_files:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            json.load(f)
        print(f'PASS json {path}')
    except Exception as exc:
        failed = True
        print(f'FAIL json {path}: {exc}')

csv_path = Path('/var/www/vhcnd/web/manifest_required_config_missing_only.csv')
print('\nCSV checks:')
try:
    text = csv_path.read_text(encoding='utf-8')
    first_line = text.splitlines()[0] if text.splitlines() else ''
    expected = 'path,name,configFile,configLine,absPath'
    if first_line == expected:
        print(f'PASS csv header {csv_path}: {first_line}')
    else:
        failed = True
        print(f'FAIL csv header {csv_path}: {first_line!r}')
    if '/var/www/vltkunity' in text:
        failed = True
        print(f'FAIL csv contains /var/www/vltkunity: {csv_path}')
    else:
        print(f'PASS csv no /var/www/vltkunity: {csv_path}')
except Exception as exc:
    failed = True
    print(f'FAIL csv {csv_path}: {exc}')

py_path = Path('/var/www/vhcnd/tools/scan_required_spr.py')
print('\nPython AST/default checks:')
try:
    py_text = py_path.read_text(encoding='utf-8')
    ast.parse(py_text, filename=str(py_path))
    print(f'PASS ast {py_path}')
    required = [
        '/var/www/vhcnd/sources/ServerNew/_bin_v2_/gs/Settings/item/004',
        '/var/www/vhcnd/sources/ServerNew/_bin_v2_/gs/Settings/item',
        '/var/www/vhcnd/item_spr',
    ]
    for needle in required:
        if needle in py_text:
            print(f'PASS default contains {needle}')
        else:
            failed = True
            print(f'FAIL default missing {needle}')
    if 'servernew_up' in py_text:
        failed = True
        print('FAIL default/text contains servernew_up')
    else:
        print('PASS no servernew_up in scan_required_spr.py')
except Exception as exc:
    failed = True
    print(f'FAIL python {py_path}: {exc}')

sys.exit(1 if failed else 0)
PY
```
Output:
```text
JSON parse checks:
PASS json /var/www/vhcnd/web/manifest_data_cdn_lite.json
PASS json /var/www/vhcnd/web/manifest.json
PASS json /var/www/vhcnd/web/manifest_required_config_missing_only.json
PASS json /var/www/vhcnd/web/manifest_downloads_like.json
PASS json /var/www/vhcnd/item_spr_img/manifest_data_cdn_lite.json
PASS json /var/www/vhcnd/item_spr_img/manifest.json
PASS json /var/www/vhcnd/item_spr_img/manifest_required_config_scan_full.json
PASS json /var/www/vhcnd/item_spr_img/manifest_downloads_like.json
PASS json /var/www/vhcnd/item_spr_img/manifest_downloads.json
PASS json /var/www/vhcnd/item_spr_img/manifest_required_config.json
PASS json /var/www/vhcnd/other-game/item_spr_like_img/report.json
PASS json /var/www/vhcnd/other-game/downloads_spr_img_struct/downloads_spr_img_struct/report.json
PASS json /var/www/vhcnd/reports/pipeline_reports/data_cdn_spr_img_report.json

CSV checks:
PASS csv header /var/www/vhcnd/web/manifest_required_config_missing_only.csv: path,name,configFile,configLine,absPath
PASS csv no /var/www/vltkunity: /var/www/vhcnd/web/manifest_required_config_missing_only.csv

Python AST/default checks:
PASS ast /var/www/vhcnd/tools/scan_required_spr.py
FAIL default missing /var/www/vhcnd/sources/ServerNew/_bin_v2_/gs/Settings/item/004
FAIL default missing /var/www/vhcnd/sources/ServerNew/_bin_v2_/gs/Settings/item
PASS default contains /var/www/vhcnd/item_spr
FAIL default/text contains servernew_up
```
Exit status: 1

## Overall result

FAIL — one or more mig-yv0 validation checks failed.

## 2026-05-19 rerun after mig-x5e default patch

Command:
```bash
set -o pipefail
if rg -I --fixed-strings --line-number '/var/www/vltkunity' /var/www/vhcnd; then exit 1; fi
python3 - <<'PY'
# JSON parse checks for known residual files.
# CSV header and no-/var/www/vltkunity check for web/manifest_required_config_missing_only.csv.
# AST parse and default string checks for /var/www/vhcnd/tools/scan_required_spr.py.
PY
```

Output:
```text
Text-aware scan checks:
PASS text-aware scan no /var/www/vltkunity under /var/www/vhcnd

JSON parse checks:
PASS json /var/www/vhcnd/web/manifest_data_cdn_lite.json
PASS json /var/www/vhcnd/web/manifest.json
PASS json /var/www/vhcnd/web/manifest_required_config_missing_only.json
PASS json /var/www/vhcnd/web/manifest_downloads_like.json
PASS json /var/www/vhcnd/item_spr_img/manifest_data_cdn_lite.json
PASS json /var/www/vhcnd/item_spr_img/manifest.json
PASS json /var/www/vhcnd/item_spr_img/manifest_required_config_scan_full.json
PASS json /var/www/vhcnd/item_spr_img/manifest_downloads_like.json
PASS json /var/www/vhcnd/item_spr_img/manifest_downloads.json
PASS json /var/www/vhcnd/item_spr_img/manifest_required_config.json
PASS json /var/www/vhcnd/other-game/item_spr_like_img/report.json
PASS json /var/www/vhcnd/other-game/downloads_spr_img_struct/downloads_spr_img_struct/report.json
PASS json /var/www/vhcnd/reports/pipeline_reports/data_cdn_spr_img_report.json

CSV checks:
PASS csv header /var/www/vhcnd/web/manifest_required_config_missing_only.csv: path,name,configFile,configLine,absPath
PASS csv no /var/www/vltkunity: /var/www/vhcnd/web/manifest_required_config_missing_only.csv

Python AST/default checks:
PASS ast /var/www/vhcnd/tools/scan_required_spr.py
PASS default contains /var/www/vhcnd/sources/ServerNew/_bin_v2_/gs/Settings/item/004
PASS default contains /var/www/vhcnd/sources/ServerNew/_bin_v2_/gs/Settings/item
PASS default contains /var/www/vhcnd/item_spr
PASS no servernew_up in scan_required_spr.py

Overall result:
PASS — all mig-yv0 validation checks passed.
```

Result: PASS — rescue patch removed the previous `scan_required_spr.py` default blocker.
