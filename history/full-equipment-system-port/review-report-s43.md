# Review Report — S43 Non-Character Visual Slot Classification

**Date:** 2026-05-20
**Scope:** VHCND engine evidence, catalog visual status classification, audit counts, tests, and runtime isolation.

## Verdict

PASS — no P1 findings.

## Findings

- P1: none.
- P2: none.
- P3: none.

## Evidence Checked

- VHCND source evidence distinguishes equip placement from character visual setters/resource getters.
- `scripts/vltk-normalize-equipment-index.py` now records `NO_CHARACTER_VISUAL_STATUS` only for stat/equip-only slots; it leaves visual-capable head/body/weapon/horse/pifeng gaps unresolved.
- `equipment-visual-status.audit.json` now separates `no-character-visual-layer=6715` from unresolved visual gaps and keeps audit status `incomplete` with `unresolvedVisualItems=367`.
- `tests/properties/equipmentNoCharacterVisualLayer.unit.test.ts` pins counts, nonvisual slots, no runtime sprites, uncertainty notes, and source evidence strings.
- Validation commands in `validation-s43.md` passed, except GitNexus `detect_changes` timed out and was documented as a tooling limitation on the generated diff.

## Remaining Risk

The `missing-npcres-mapping=75` rows are now concentrated on visual-capable horse and pifeng gold/normal cases. They require a later source-backed mapping investigation; do not classify them as nonvisual and do not synthesize fallback visuals.
