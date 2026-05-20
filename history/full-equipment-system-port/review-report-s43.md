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
- `scripts/vltk-normalize-equipment-index.py` now records `NO_CHARACTER_VISUAL_STATUS` only for stat/equip-only slots; it leaves visual-capable or special visual-affecting head/body/weapon/horse/pifeng/mask/shiping/yinjian gaps unresolved.
- `equipment-visual-status.audit.json` now separates `no-character-visual-layer=4110` from unresolved visual gaps and keeps audit status `incomplete` with `unresolvedVisualItems=2972`.
- `tests/properties/equipmentNoCharacterVisualLayer.unit.test.ts` pins counts, nonvisual slots, no runtime sprites, uncertainty notes, and source evidence strings.
- Validation commands in `validation-s43.md` passed, and GitNexus `detect_changes(scope="unstaged")` returned LOW risk with no affected processes.

## Remaining Risk

The `missing-npcres-mapping=2680` rows are now concentrated on special visual-capable or visual-affecting slots: horse, mask, pifeng, shiping, and yinjian. They require a later source-backed mapping investigation; do not classify them as nonvisual and do not synthesize fallback visuals.
