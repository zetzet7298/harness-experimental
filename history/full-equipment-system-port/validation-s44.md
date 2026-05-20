# Validation — S44 Mask Template Visual Gap Classification

**Date:** 2026-05-20
**Feature:** full-equipment-system-port
**Game-source commit:** `8339d52 fix(equipment): separate mask template visual gaps`

## Commands

```bash
npm run test:pbt
python3 tests/test_vltk_porting_smoke.py -k test_equipment_visual_status_audit_quantifies_current_catalog_safety
npm run build
gitnexus impact normalize_row (MCP)
gitnexus detect_changes(scope="unstaged") (MCP)
```

## Results

- GitNexus pre-edit impact for `scripts/vltk-normalize-equipment-index.py::normalize_row`: LOW risk; direct caller `build_index`, transitive caller `main`.
- Property tests: PASS — 24 files, 257 tests. New S44 coverage proves all mask rows are `missing-mask-template-mapping`, no generic mask `missing-npcres-mapping` remains, and the VHCND template path evidence is pinned.
- Targeted Python smoke: PASS — current visual status audit reports `preview-passed-loadout-evidence=2470`, `no-character-visual-layer=4110`, `missing-local-source-spr=204`, `missing-mask-template-mapping=1764`, `missing-npcres-mapping=916`, `missing-npcres-row=6`, `missing-resource-row-no-fallback=82`, and `unresolvedVisualItems=2972`.
- Runtime isolation: PASS — prebuild guard reports no runtime `/var/www/vhcnd` literals and no symlinks under `src/` or `public/`.
- Production build: PASS — Vite built successfully; existing large chunk warning remains non-blocking.
- GitNexus `detect_changes(scope="unstaged")`: MEDIUM risk, affected processes were generated-magic parse flows due broad touched-symbol attribution in the regenerated normalizer diff; no visual runtime process impact was reported.

## Remaining Gap

Mask visuals are still unresolved. S44 only makes their template/NpcResType route explicit so the next slice can map template ids to source sprites without guessing or treating masks as normal equipment NpcRes layers.
