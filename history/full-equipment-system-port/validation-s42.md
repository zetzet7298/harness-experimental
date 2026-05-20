# Validation — S42 PiFeng Missing NpcRes Row Audit Hardening

**Date:** 2026-05-20
**Feature:** full-equipment-system-port
**Game-source commit:** `36d54a9 test(equipment): audit unresolved pifeng npcres rows`

## Commands

```bash
npm run test:pbt
python3 tests/test_vltk_porting_smoke.py -k test_equipment_visual_status_audit_quantifies_current_catalog_safety
npm run build
gitnexus detect_changes(repo="vltk-h5-survivors", scope="all")
```

## Results

- Property tests: PASS — 22 files, 251 tests. New S42 coverage proves six PiFeng rows stay `missing-npcres-row` with no candidate/runtime sprites.
- Targeted Python smoke: PASS — visual status audit counts match current generated catalog (`preview-passed-loadout-evidence=2984`, `missing-local-source-spr=204`, `missing-npcres-mapping=6276`, `missing-npcres-row=6`, `missing-resource-row-no-fallback=82`).
- Runtime isolation: PASS — prebuild guard reports no `/var/www/vhcnd` runtime literals and no symlinks under `src/` or `public/`.
- Production build: PASS — Vite built successfully; existing large chunk warning remains non-blocking.
- GitNexus changed-scope: LOW risk; no affected processes.

## Remaining Gap

S42 does not resolve PiFeng visual rows; it prevents false completion by making `missing-npcres-row=6` part of the unresolved visual total. Later work must resolve or explicitly source-backed-defer the four visual buckets before visual parity can be complete.
