# Current Story Pack — S6 Magic Attribute Parity

**Feature:** full-equipment-system-port  
**Epic:** E2 Formula, requirements, and combat stat parity  
**Mode:** `high_risk_feature`  
**Prepared after:** S5 formula ledger passed and compounding completed.

## Story Outcome

Make magic-attribute coverage source-backed and fail-fast. Every attribute key emitted into the H5 catalog from VHCND normal/magic/gold equipment must be identifiable by the PC `MAGIC_ATTRIB` enum and must either have runtime stat semantics implemented or be recorded as an explicit unsupported gap that blocks full parity stories.

## Entry State

- S5 created `data/vltk-normalized/equipment-formula-ledger.json` and upgraded formula parity audit.
- Current catalog contains 59 attribute keys, including many `magic_unknown_*` keys from attr types present in VHCND tables but missing from the seed builder's hard-coded `MAGIC_NAMES` map.
- `scripts/vltk-audit-equipment-stat-coverage.py` currently exempts `magic_unknown_*` from missing runtime case failures; this is too weak for S6 because unknown keys can silently hide real VHCND options.
- Several known keys are intentionally no-op in `equipment.ts` (`magic_life_v`, `magic_mana_v`, resist max keys, etc.), but they need source-backed status rather than silent `break` cases.

## Exit State

This story is done only when current repo evidence proves:

1. The seed/catalog generation maps VHCND attribute ids through a source-backed enum map from `KMagicAttrib.h`, so catalog keys are no longer `magic_unknown_*` merely because the local hard-coded map is incomplete.
2. A deterministic magic-attribute parity audit exists and reports every catalog attribute key with:
   - catalog count,
   - source enum id/name when available,
   - runtime implementation status,
   - explicit unsupported/blocker status when semantics are not ported yet.
3. Existing stat coverage no longer silently ignores unknown keys for S6; unknown or unsupported keys must be visible in an audit artifact.
4. Validation proves runtime isolation remains clean.

## Files Likely Touched

- `/var/www/vltk-h5-survivors/game-source/scripts/vltk-build-equipment-seed.py`
- `/var/www/vltk-h5-survivors/game-source/scripts/vltk-audit-equipment-magic-attribute-parity.py`
- `/var/www/vltk-h5-survivors/game-source/scripts/vltk-audit-equipment-stat-coverage.py`
- `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/equipment-magic-attribute-parity.audit.json`
- `/var/www/vltk-h5-survivors/game-source/src/data/equipmentCatalog.json`
- Targeted tests if audit behavior is covered in TS/Python smoke.

## Verification Targets

- `python3 scripts/vltk-build-equipment-seed.py`
- `python3 scripts/vltk-audit-equipment-magic-attribute-parity.py`
- `python3 scripts/vltk-audit-equipment-stat-coverage.py`
- `npm run test:pbt`
- `npm run typecheck`
- `npm run check:runtime-isolation`

## Out Of Scope For This Story

- Full numeric stat-vector equality fixtures (S8).
- Tooltip redesign (S10), except labels exposed by the parity audit.
- Full condition parity (S7), except requirement keys already surfaced by catalog generation.
