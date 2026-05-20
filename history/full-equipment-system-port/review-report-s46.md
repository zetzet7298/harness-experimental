# Review Report — S46 Special Slot Visual Gap Classification

**Date:** 2026-05-20  
**Scope:** PiFeng direct type mapping, ShiPin/YinJian ItemResIdx classification, regenerated visual audits, tests, build, and runtime isolation.

## Verdict

PASS — no P1 findings.

## Findings

- P1: none.
- P2: none.
- P3: none.

## Evidence Checked

- VHCND source proves PiFeng does not always use ordinary resource-row mapping: gold PiFeng uses equipment level as `m_PifengType`, then `KNpcRes::SetPifeng` resolves filenames by type.
- VHCND source proves ShiPin/YinJian only affect visuals through `ItemResIdx > 0`; catalog rows do not provide a safe normal NpcRes table fallback.
- `scripts/vltk-normalize-equipment-index.py` now models those special paths explicitly.
- `equipment-visual-status.audit.json` removes generic `missing-npcres-mapping` while preserving all unresolved rows in source-specific buckets.
- `tests/properties/equipmentSpecialItemResVisual.unit.test.ts` pins the new S46 classification.
- Validation commands in `validation-s46.md` passed.

## Remaining Risk

`missing-itemresidx-visual-mapping=841` is still a real unresolved visual bucket. A later slice must locate source-backed ItemResIdx values or keep those rows unresolved. Mask template mapping remains the largest unresolved bucket.
