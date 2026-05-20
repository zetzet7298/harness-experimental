# Review Report — S44 Mask Template Visual Gap Classification

**Date:** 2026-05-20
**Scope:** Mask visual source evidence, catalog/audit classification, tests, build, and runtime isolation.

## Verdict

PASS — no P1 findings.

## Findings

- P1: none.
- P2: none.
- P3: none.

## Evidence Checked

- VHCND source evidence shows masks use `m_MaskType -> KNpc::ReSetRes -> NpcResType`, not the ordinary equipment NpcRes layer tables.
- `scripts/vltk-normalize-equipment-index.py` now emits `missing-mask-template-mapping` with explicit source evidence for mask rows.
- `equipment-visual-status.audit.json` separates `missing-mask-template-mapping=1764` from `missing-npcres-mapping=916`; unresolved visual total remains `2972` because this is a reclassification, not a visual resolution.
- `tests/properties/equipmentMaskTemplateVisual.unit.test.ts` and updated S42/S43 tests pin the status counts and unresolved-total formula.
- Validation commands in `validation-s44.md` passed. GitNexus changed-scope was MEDIUM due touched generated-magic symbols in the normalizer diff, but targeted tests/build cover the intended visual-audit behavior.

## Remaining Risk

A later mask porting slice must resolve `m_MaskType` values to NPC template rows, `NpcResType`, resource table rows, local source SPRs, preview reports, and runtime wiring. Until then, mask visuals must stay unresolved and must not be guessed.
