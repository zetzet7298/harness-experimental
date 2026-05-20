# Review Report — S45 Gold Detail Visual Resource Mapping

**Date:** 2026-05-20  
**Scope:** Gold visual detail mapping, regenerated catalog/audits, missing-source/resource provenance, tests, build, and runtime isolation.

## Verdict

PASS — no P1 findings.

## Findings

- P1: none.
- P2: none.
- P3: none.

## Evidence Checked

- VHCND `EQUIPDETAILTYPE` and `KItemList::Equip` evidence proves detail 7 is helm/head, detail 8 is cuff/stat-only, and detail 10 is horse.
- `scripts/vltk-normalize-equipment-index.py` now maps gold detail 7 → `HelmRes` and detail 10 → `HorseRes`; detail 8 has no visual resource override.
- Regenerated `src/data/equipmentCatalog.json` has no head rows resolved from `HorseRes`.
- Newly exposed absent horse source candidates are not wired as candidates; they are recorded under `missing-local-source-spr` with exact-source/PAK MISS evidence.
- Visual status audit closes the candidate bucket at 0 and keeps unsafe resolved visuals at 0.
- Validation commands in `validation-s45.md` passed.

## Remaining Risk

Five horse rows now point to missing `HorseRes#352`; they are correctly blocked as `missing-resource-row-no-fallback`. Later work must either find a source-backed table/fallback or keep them unresolved. Mask, yinjian, and shiping special paths remain unresolved.
