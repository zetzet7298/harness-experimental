# residual-ref-patch-evidence — mig-428

- Timestamp: 2026-05-19T13:07:25.501779+00:00
- Scope: text files under `/var/www/vhcnd` with extensions `.css, .csv, .html, .js, .json, .log, .md, .mjs, .py, .sh, .ts, .tsx, .txt, .xml, .yaml, .yml`
- Target root check: PASS (9 mapped destinations exist)
- Pre-patch files containing `/var/www/vltkunity`: 14
- Touched files: 14
- Post-patch files containing `/var/www/vltkunity`: 0

## Mapping counts

| Source prefix | Destination prefix | Before refs | Replaced refs | After refs in touched files |
| --- | --- | ---: | ---: | ---: |
| `/var/www/vltkunity/other-game/download-source/data_cdn_pak_extract` | `/var/www/vhcnd/datasets/data_cdn/pak_extract/data_cdn_pak_extract` | 2 | 2 | 0 |
| `/var/www/vltkunity/other-game/download-source/data_cdn_spr_img` | `/var/www/vhcnd/other-game/download-source/data_cdn_spr_img` | 3 | 3 | 0 |
| `/var/www/vltkunity/other-game/downloads_spr_img_struct` | `/var/www/vhcnd/other-game/downloads_spr_img_struct` | 2 | 2 | 0 |
| `/var/www/vltkunity/other-game/downloads_pak_extract` | `/var/www/vhcnd/other-game/downloads_pak_extract` | 1 | 1 | 0 |
| `/var/www/vltkunity/other-game/item_spr_like_img` | `/var/www/vhcnd/other-game/item_spr_like_img` | 3 | 3 | 0 |
| `/var/www/vltkunity/other-game/item_spr_like` | `/var/www/vhcnd/other-game/item_spr_like` | 4 | 1 | 0 |
| `/var/www/vltkunity/item_spr_img` | `/var/www/vhcnd/item_spr_img` | 2 | 2 | 0 |
| `/var/www/vltkunity/item_data` | `/var/www/vhcnd/item_data` | 3859 | 3859 | 0 |
| `/var/www/vltkunity/item_spr` | `/var/www/vhcnd/item_spr` | 3861 | 3859 | 0 |

## Pre-patch file list

- `/var/www/vhcnd/web/manifest_data_cdn_lite.json`
- `/var/www/vhcnd/web/manifest.json`
- `/var/www/vhcnd/web/manifest_required_config_missing_only.json`
- `/var/www/vhcnd/web/manifest_required_config_missing_only.csv`
- `/var/www/vhcnd/web/manifest_downloads_like.json`
- `/var/www/vhcnd/item_spr_img/manifest_data_cdn_lite.json`
- `/var/www/vhcnd/item_spr_img/manifest.json`
- `/var/www/vhcnd/item_spr_img/manifest_required_config_scan_full.json`
- `/var/www/vhcnd/item_spr_img/manifest_downloads_like.json`
- `/var/www/vhcnd/item_spr_img/manifest_downloads.json`
- `/var/www/vhcnd/item_spr_img/manifest_required_config.json`
- `/var/www/vhcnd/other-game/item_spr_like_img/report.json`
- `/var/www/vhcnd/other-game/downloads_spr_img_struct/downloads_spr_img_struct/report.json`
- `/var/www/vhcnd/reports/pipeline_reports/data_cdn_spr_img_report.json`

## JSON parse checks

- Pre-patch JSON files parsed: 13
  - PASS pre `/var/www/vhcnd/web/manifest_data_cdn_lite.json`
  - PASS pre `/var/www/vhcnd/web/manifest.json`
  - PASS pre `/var/www/vhcnd/web/manifest_required_config_missing_only.json`
  - PASS pre `/var/www/vhcnd/web/manifest_downloads_like.json`
  - PASS pre `/var/www/vhcnd/item_spr_img/manifest_data_cdn_lite.json`
  - PASS pre `/var/www/vhcnd/item_spr_img/manifest.json`
  - PASS pre `/var/www/vhcnd/item_spr_img/manifest_required_config_scan_full.json`
  - PASS pre `/var/www/vhcnd/item_spr_img/manifest_downloads_like.json`
  - PASS pre `/var/www/vhcnd/item_spr_img/manifest_downloads.json`
  - PASS pre `/var/www/vhcnd/item_spr_img/manifest_required_config.json`
  - PASS pre `/var/www/vhcnd/other-game/item_spr_like_img/report.json`
  - PASS pre `/var/www/vhcnd/other-game/downloads_spr_img_struct/downloads_spr_img_struct/report.json`
  - PASS pre `/var/www/vhcnd/reports/pipeline_reports/data_cdn_spr_img_report.json`
- Touched JSON files parsed after patch: 13
  - PASS post `/var/www/vhcnd/web/manifest_data_cdn_lite.json`
  - PASS post `/var/www/vhcnd/web/manifest.json`
  - PASS post `/var/www/vhcnd/web/manifest_required_config_missing_only.json`
  - PASS post `/var/www/vhcnd/web/manifest_downloads_like.json`
  - PASS post `/var/www/vhcnd/item_spr_img/manifest_data_cdn_lite.json`
  - PASS post `/var/www/vhcnd/item_spr_img/manifest.json`
  - PASS post `/var/www/vhcnd/item_spr_img/manifest_required_config_scan_full.json`
  - PASS post `/var/www/vhcnd/item_spr_img/manifest_downloads_like.json`
  - PASS post `/var/www/vhcnd/item_spr_img/manifest_downloads.json`
  - PASS post `/var/www/vhcnd/item_spr_img/manifest_required_config.json`
  - PASS post `/var/www/vhcnd/other-game/item_spr_like_img/report.json`
  - PASS post `/var/www/vhcnd/other-game/downloads_spr_img_struct/downloads_spr_img_struct/report.json`
  - PASS post `/var/www/vhcnd/reports/pipeline_reports/data_cdn_spr_img_report.json`

## CSV checks

- PASS `/var/www/vhcnd/web/manifest_required_config_missing_only.csv` header `path,name,configFile,configLine,absPath`

## Final zero-ref proof

- Command: `grep -RIl '/var/www/vltkunity' /var/www/vhcnd`
- Result: PASS (zero files)
