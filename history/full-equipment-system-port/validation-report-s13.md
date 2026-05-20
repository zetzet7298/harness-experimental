# Validation Report — S13 Smoke Loadout Visual Gate

**Feature:** full-equipment-system-port  
**Mode:** `high_risk_feature`  
**Date:** 2026-05-20  
**Decision:** `READY WITH CONSTRAINTS — CREATE CURRENT-STORY BEADS`

## Reality Gate

S13 is necessary before claiming visual parity for the user's smoke equipment examples. Existing local source copies and preview-passed runtime manifest entries are promising, but current catalog-gate repeatability is broken: default ids are stale, catalog rows have empty `visual.resolvedSprites`, and the user-facing Địch Khái staff identity is ambiguous because name search currently selects a ring row.

## Feasibility Matrix

| Assumption | Evidence | Result |
| --- | --- | --- |
| Existing local copied smoke SPRs are present. | `equipment-port-loadout.audit.json` lists six copied SPRs in `public/assets/character/vhcnd/source/smoke-3piece-tu-la-giang-sa-dich-khai/`; filesystem probe confirmed those files exist and are not symlinks before the dry-run was reverted. | PASS |
| Preview-passed evidence exists for smoke basenames. | `equipped-visual-manifest.json` includes `passed-generated` entries such as `equipped-current-catalog-mounted`; audit entries cite `origin=equipped-visual-manifest`, `status=passed`. | PASS |
| Catalog gate is repeatable from current catalog defaults. | `python3 scripts/vltk-port-loadout.py --mode catalog-gate --dry-run` fails with `Catalog item id not found: 'vhcnd-tu-la-phat-ket-helm-31-2-10'`. | FAIL — REPAIR REQUIRED |
| Name-based smoke selection currently finds visual basenames. | Explicit name dry-run returned `required=0` because selected current catalog rows have empty `visual.resolvedSprites`; `Địch Khái Lục Ngọc Trượng` name also selects a ring row, not the staff weapon visual. | FAIL — REPAIR REQUIRED |
| Runtime isolation can be preserved. | Existing playbook and `check:no-runtime-vhcnd` gate already enforce no runtime VHCND literals/symlinks; S13 can stay local-copy-only. | PASS |

## Required Current-Story Beads

1. **S13A smoke identity repair** — map the three smoke items to current catalog ids with source-backed evidence, including resolving the Địch Khái staff/weapon vs ring-name ambiguity.
2. **S13B catalog gate repair** — update `vltk-port-loadout.py`/supporting data so catalog-gate default/current smoke selection produces nonzero required basenames and uses only passed preview evidence/local source copies.
3. **S13C visual gate validation** — rerun catalog gate dry-run/apply, assert copied SPRs exist and are not symlinks, run runtime isolation/build as needed, and capture browser screenshot if runtime visual output changes.

## Execution Constraints

- Do not fabricate visual mappings; cite existing manifest/report/source-row evidence for every basename.
- Do not silently rename the ring row into the staff weapon. If localization mapping is wrong, repair or document it with source rows.
- Do not make runtime read from `/var/www/vhcnd`; copying from build-time evidence into `game-source` is allowed.
- Do not compose/wire new runtime assets unless preview evidence is already `passed`.

## Post-Execution Validation — 2026-05-20

**Decision:** `PASSED — S13 COMPLETE`

- Identity ambiguity resolved: the user-facing staff is catalog row 98 (`GoldItem.txt:98`, weapon, `obj-staff13.spr`), while row 97 is retained as a ring and no longer satisfies the staff name.
- Catalog gate defaults are current ids and no longer stale; dry-run/apply both produced `required=12`, `copied=12`, `skipped=0`.
- All copied smoke SPRs are repo-local files under `/var/www/vltk-h5-survivors/game-source/public/assets/character/vhcnd/source/smoke-3piece-tu-la-giang-sa-dich-khai/`; symlink/runtime isolation gate passed.
- Visual coverage gate passed through dynamic layered parts for the smoke loadout (`allRequiredPassed=true`, no required failures).
- User-facing E2E proof: `$browser-navigation` against port 5173 seeded the smoke loadout, started a run, captured `/tmp/s13-equipment-screen.png` and `/tmp/s13-game-run-screen.png`, and confirmed `layeredCount=6` with staff/body part textures loaded. Playwright smoke also passed after installing the missing local Chromium browser cache.
