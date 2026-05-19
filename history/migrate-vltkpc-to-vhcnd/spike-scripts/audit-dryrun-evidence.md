# US-011 audit dry-run rerouted to vhcnd — mig-lfz
## Verdict
`gap-recorded`: script đầu tiên trong danh sách (`vltk-audit-equipment-stat-coverage.py`) có flag `--vltkpc-root`, nhưng khi reroute sang `/var/www/vhcnd/sources` thì toàn bộ source-line gate fail vì catalog vẫn trỏ `Client/Settings/item/*.txt` và vhcnd không có layout đó dưới root này. Dừng theo stop condition; các script sau không chạy.
## Execplan
- Đã đọc `docs/stories/epics/E03-vltkpc-asset-porting/US-011-port-vltkpc-equipment-system/execplan.md`.
## Help/args inspection
- `vltk-audit-equipment-stat-coverage.py`: help_exit=0; flags=--catalog, --help, --out, --source, --vltkpc-root; assessment=has --vltkpc-root; can reroute source root but catalog source.path remains Client/Settings/...
- `vltk-audit-equipment-quality-coverage.py`: help_exit=0; flags=--catalog, --help, --out, --require-complete; assessment=no vhcnd/vltkpc/vltkunity root flag exposed; only H5-relative/default data inputs
- `vltk-audit-equipment-series-coverage.py`: help_exit=0; flags=--catalog, --domain, --help, --inventory, --no-fail, --out; assessment=no vhcnd/vltkpc/vltkunity root flag exposed; only H5-relative/default data inputs
- `vltk-audit-equipment-visual-coverage.py`: help_exit=0; flags=--catalog, --help, --inventory, --manifest, --no-require-pass, --out, --parts-manifest, --require-complete, --require-pass; assessment=no vhcnd/vltkpc/vltkunity root flag exposed; only H5-relative/default data inputs
- `vltk-audit-equipment-visual-part-coverage.py`: help_exit=0; flags=--help, --manifest, --out, --part-asset-dir, --plan, --require-complete, --runtime-source; assessment=no vhcnd/vltkpc/vltkunity root flag exposed; only H5-relative/default data inputs
- `vltk-audit-equipment-formula-parity.py`: help_exit=0; flags=--help, --out, --target; assessment=no vhcnd/vltkpc/vltkunity root flag exposed; only H5-relative/default data inputs
- `vltk-audit-equipment-label-coverage.py`: help_exit=0; flags=--catalog, --help, --labels, --out; assessment=no vhcnd/vltkpc/vltkunity root flag exposed; only H5-relative/default data inputs
- `vltk-audit-equipment-name-localization.py`: help_exit=0; flags=--catalog, --gold-name-row-map, --help, --out, --require-complete, --vng-gold-sources; assessment=no vhcnd/vltkpc/vltkunity root flag exposed; only H5-relative/default data inputs
- `vltk-audit-equipment-icon-coverage.py`: help_exit=1; flags=(none); assessment=no argparse/help path; script executes at import/read time and exposes no flags/root override

## Attempted command
```bash
python3 scripts/vltk-audit-equipment-stat-coverage.py --catalog src/data/equipmentCatalog.json --source src/domain/equipment.ts --out /var/www/vltk-h5-survivors/harness-experimental/history/migrate-vltkpc-to-vhcnd/spike-scripts/outputs/equipment-stat-coverage.audit.json --vltkpc-root /var/www/vhcnd/sources
```
- cwd: `/var/www/vltk-h5-survivors/game-source`
- exit code: `1`
- audit JSON: `/var/www/vltk-h5-survivors/harness-experimental/history/migrate-vltkpc-to-vhcnd/spike-scripts/outputs/equipment-stat-coverage.audit.json`

## Audit metrics
```json
{
  "topLevelStatus": "fail",
  "catalogAttributeKeyCount": 45,
  "missingRuntimeCaseCount": 0,
  "missingFormulaMarkerCount": 0,
  "noFabricationStatus": "fail",
  "itemsChecked": 1231,
  "sourceLinesValid": 0,
  "mismatchCount": 1231,
  "fileLineCounts": {
    "Client/Settings/item/GoldItem.txt": -1,
    "Client/Settings/item/amulet.txt": -1,
    "Client/Settings/item/armor.txt": -1,
    "Client/Settings/item/belt.txt": -1,
    "Client/Settings/item/boot.txt": -1,
    "Client/Settings/item/cuff.txt": -1,
    "Client/Settings/item/helm.txt": -1,
    "Client/Settings/item/horse.txt": -1,
    "Client/Settings/item/meleeweapon.txt": -1,
    "Client/Settings/item/pendant.txt": -1,
    "Client/Settings/item/rangeweapon.txt": -1,
    "Client/Settings/item/ring.txt": -1
  },
  "sourceRoot": "/var/www/vhcnd/sources"
}
```

## Stdout tail
```text
      {
        "fileLineCount": null,
        "itemId": "vltkpc-to-mau-luc-gioi-chi-7-6-magic",
        "reason": "source-file-unreadable",
        "sourceLine": 7,
        "sourcePath": "Client/Settings/item/ring.txt"
      },
      {
        "fileLineCount": null,
        "itemId": "vltkpc-hai-lam-bao-thach-gioi-chi-8-7",
        "reason": "source-file-unreadable",
        "sourceLine": 8,
        "sourcePath": "Client/Settings/item/ring.txt"
      },
      {
        "fileLineCount": null,
        "itemId": "vltkpc-hai-lam-bao-thach-gioi-chi-8-7-magic",
        "reason": "source-file-unreadable",
        "sourceLine": 8,
        "sourcePath": "Client/Settings/item/ring.txt"
      },
      {
        "fileLineCount": null,
        "itemId": "vltkpc-hong-bao-thach-gioi-chi-9-8",
        "reason": "source-file-unreadable",
        "sourceLine": 9,
        "sourcePath": "Client/Settings/item/ring.txt"
      },
      {
        "fileLineCount": null,
        "itemId": "vltkpc-hong-bao-thach-gioi-chi-9-8-magic",
        "reason": "source-file-unreadable",
        "sourceLine": 9,
        "sourcePath": "Client/Settings/item/ring.txt"
      },
      {
        "fileLineCount": null,
        "itemId": "vltkpc-lam-bao-thach-gioi-chi-10-9",
        "reason": "source-file-unreadable",
        "sourceLine": 10,
        "sourcePath": "Client/Settings/item/ring.txt"
      },
      {
        "fileLineCount": null,
        "itemId": "vltkpc-lam-bao-thach-gioi-chi-10-9-magic",
        "reason": "source-file-unreadable",
        "sourceLine": 10,
        "sourcePath": "Client/Settings/item/ring.txt"
      },
      {
        "fileLineCount": null,
        "itemId": "vltkpc-toan-thach-gioi-chi-11-10",
        "reason": "source-file-unreadable",
        "sourceLine": 11,
        "sourcePath": "Client/Settings/item/ring.txt"
      },
      {
        "fileLineCount": null,
        "itemId": "vltkpc-toan-thach-gioi-chi-11-10-magic",
        "reason": "source-file-unreadable",
        "sourceLine": 11,
        "sourcePath": "Client/Settings/item/ring.txt"
      }
    ],
    "sourceLinesValid": 0,
    "sourcePathPrefixRequired": "Client/Settings/",
    "sourceRoot": "/var/www/vhcnd/sources",
    "status": "fail"
  },
  "noopKeysPresentInCatalog": [],
  "notes": [
    "flags[].status=pass means equipment.ts contains the literal PC-parity marker for that flag (Req 14.3).",
    "noFabricationCheck enforces every catalog item has a non-empty source.path under Client/Settings/ and a source.line within the actual VLTKPC source file (Req 14.5).",
    "catalogAttributeCounts + missingRuntimeCases + noopKeysPresentInCatalog audit runtime stat-handling coverage for every key produced by the seed builder (Req 14.7).",
    "Output is sort_keys=True / UTF-8 / trailing newline so reruns produce byte-identical files (Req 13.6 spillover for audit determinism)."
  ],
  "schemaVersion": 2,
  "source": "src/domain/equipment.ts",
  "status": "fail"
}
```

## Stderr tail
```text
(empty)
```

## First source gaps
```json
[
  {
    "fileLineCount": null,
    "itemId": "vltkpc-梦龙法冠-2-10",
    "reason": "source-file-unreadable",
    "sourceLine": 2,
    "sourcePath": "Client/Settings/item/GoldItem.txt"
  },
  {
    "fileLineCount": null,
    "itemId": "vltkpc-梦龙戒衫-3-10",
    "reason": "source-file-unreadable",
    "sourceLine": 3,
    "sourcePath": "Client/Settings/item/GoldItem.txt"
  },
  {
    "fileLineCount": null,
    "itemId": "vltkpc-梦龙软绦-4-10",
    "reason": "source-file-unreadable",
    "sourceLine": 4,
    "sourcePath": "Client/Settings/item/GoldItem.txt"
  },
  {
    "fileLineCount": null,
    "itemId": "vltkpc-梦龙护腕-5-1-10",
    "reason": "source-file-unreadable",
    "sourceLine": 5,
    "sourcePath": "Client/Settings/item/GoldItem.txt"
  },
  {
    "fileLineCount": null,
    "itemId": "vltkpc-梦龙僧鞋-6-10",
    "reason": "source-file-unreadable",
    "sourceLine": 6,
    "sourcePath": "Client/Settings/item/GoldItem.txt"
  }
]
```

## Not attempted due stop condition
- `vltk-audit-equipment-quality-coverage.py` — not attempted because first ordered audit needs unavailable vhcnd `Client/Settings/item/*.txt` inputs.
- `vltk-audit-equipment-series-coverage.py` — not attempted because first ordered audit needs unavailable vhcnd `Client/Settings/item/*.txt` inputs.
- `vltk-audit-equipment-visual-coverage.py` — not attempted because first ordered audit needs unavailable vhcnd `Client/Settings/item/*.txt` inputs.
- `vltk-audit-equipment-visual-part-coverage.py` — not attempted because first ordered audit needs unavailable vhcnd `Client/Settings/item/*.txt` inputs.
- `vltk-audit-equipment-formula-parity.py` — not attempted because first ordered audit needs unavailable vhcnd `Client/Settings/item/*.txt` inputs.
- `vltk-audit-equipment-label-coverage.py` — not attempted because first ordered audit needs unavailable vhcnd `Client/Settings/item/*.txt` inputs.
- `vltk-audit-equipment-name-localization.py` — not attempted because first ordered audit needs unavailable vhcnd `Client/Settings/item/*.txt` inputs.
- `vltk-audit-equipment-icon-coverage.py` — not attempted because first ordered audit needs unavailable vhcnd `Client/Settings/item/*.txt` inputs.

## Canonical output mutation
Không target canonical `game-source/data/vltk-normalized/*.audit.json`; attempted output được redirect vào harness `history/.../outputs/`.
