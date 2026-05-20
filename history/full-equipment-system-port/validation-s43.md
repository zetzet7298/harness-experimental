# Validation — S43 Non-Character Visual Slot Classification

**Date:** 2026-05-20
**Feature:** full-equipment-system-port
**Game-source commit:** `321bf5d fix(equipment): keep special visual slots unresolved`

## Commands

```bash
npm run test:pbt
python3 tests/test_vltk_porting_smoke.py -k test_equipment_visual_status_audit_quantifies_current_catalog_safety
npm run build
gitnexus impact normalize_row (MCP)
gitnexus detect_changes(scope="unstaged")
```

## Results

- GitNexus pre-edit impact for `scripts/vltk-normalize-equipment-index.py::normalize_row`: LOW risk; direct caller `build_index`, transitive caller `main`.
- Property tests: PASS — 23 files, 254 tests. New S43 coverage proves stat/equip-only slots are `no-character-visual-layer` and carry engine-evidence source strings.
- Targeted Python smoke: PASS — current visual status audit reports `preview-passed-loadout-evidence=2470`, `no-character-visual-layer=4110`, `missing-local-source-spr=204`, `missing-npcres-mapping=2680`, `missing-npcres-row=6`, `missing-resource-row-no-fallback=82`, and `unresolvedVisualItems=2972`.
- Runtime isolation: PASS — prebuild guard reports no runtime `/var/www/vhcnd` literals and no symlinks under `src/` or `public/`.
- Production build: PASS — Vite built successfully; existing large chunk warning remains non-blocking.
- GitNexus `detect_changes(scope="unstaged")`: PASS — LOW risk, affected processes `[]`.

## Remaining Gap

Full visual parity remains incomplete. S43 removes false visual-gap pressure for slots the VHCND engine does not render as character layers, but visual-capable unresolved buckets remain at `2972` total rows.
