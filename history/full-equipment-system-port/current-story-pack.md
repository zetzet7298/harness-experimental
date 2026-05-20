# Current Story Pack — S1/S2/S3 Feasibility: Catalog + Slot Taxonomy Foundation

**Feature:** full-equipment-system-port  
**Epic:** E1 Canonical VHCND catalog + slot taxonomy  
**Mode:** `high_risk_feature`  
**Prepared after:** human selected `$khuym:validating`, treated as approval of `history/full-equipment-system-port/approach.md` work shape.

## Story Outcome

Make the first executable slice ready for swarming: prove and then implement the catalog/slot foundation needed before formula, UI, seed, and visual parity stories can safely proceed.

## Entry State

- H5 source is `/var/www/vltk-h5-survivors/game-source`; VHCND evidence/build input is `/var/www/vhcnd` only.
- `EquipmentSlot` currently has 11 values: `head`, `body`, `belt`, `weapon`, `foot`, `cuff`, `amulet`, `ring1`, `ring2`, `pendant`, `horse`.
- Current catalog has 1231 rows and no default rows for `mask`, `pifeng`, `yinjian`, or `shiping`.
- VHCND source shows extended detail types in both slot fit and common base attribute dispatch.
- Runtime must not directly read `/var/www/vhcnd`, use symlink, or reintroduce `old PC source name` source references.

## Exit State

This story is done only when current repo evidence proves:

1. Active VHCND equipment table inventory is documented for the current slice, including `Mask.txt`, `PiFeng.txt`, `YinJian.txt`, `ShiPin.txt`, `GoldItem.txt`, `GoldMagic.txt`, `magicattrib.txt`, and related base property/resource tables.
2. H5 slot taxonomy and labels represent every PC equipment slot needed by this slice, preserving `ring1/ring2` dual-slot behavior.
3. Normalizer support for missing extended tables is implemented with `source.path`, `encoding`, `line`, item fields, quality, requirements, attributes, and provenance.
4. Seed/test policy includes representative items for every slot while preserving one-cell mobile inventory cells.
5. Audits/tests prove catalog slot/quality/stat-label coverage and no unsafe runtime VHCND/symlink reference.

## Files Likely Touched

- `/var/www/vltk-h5-survivors/game-source/src/domain/types.ts`
- `/var/www/vltk-h5-survivors/game-source/src/domain/equipment.ts`
- `/var/www/vltk-h5-survivors/game-source/src/domain/equipmentLabels.ts`
- `/var/www/vltk-h5-survivors/game-source/src/domain/equipmentStore.ts`
- `/var/www/vltk-h5-survivors/game-source/scripts/vltk-normalize-equipment-index.py`
- `/var/www/vltk-h5-survivors/game-source/scripts/vltk-build-equipment-seed.py`
- `/var/www/vltk-h5-survivors/game-source/scripts/vltk-audit-equipment-*.py`
- `/var/www/vltk-h5-survivors/game-source/src/data/equipmentCatalog.json`
- `/var/www/vltk-h5-survivors/game-source/src/data/inventory.json`
- `/var/www/vltk-h5-survivors/game-source/tests/properties/*.test.ts`

## Feasibility Assumptions To Validate

| Assumption | Risk | Validation proof required |
| --- | --- | --- |
| Normalizer can parse the four extended VHCND tables without schema rewrite. | HIGH | Script/source inspection plus a dry probe over `Mask/PiFeng/YinJian/ShiPin` rows. |
| Slot taxonomy can expand without breaking persistence/run snapshot. | HIGH | Type/source inspection identifies all slot-order/sanitize/build-snapshot touchpoints and tests exist or are planned. |
| `MAX_RESIST` source discrepancy is resolvable before formula work. | HIGH | Exact VHCND evidence for current active value or a validation constraint that blocks formula beads. |
| Seed/test workflow can expose all slots without huge normal bag. | MEDIUM | Existing seed builder/audit behavior inspected; validation constraint recorded if a test catalog browser is needed. |
| Isolation guard can prove no direct runtime VHCND/symlink use for this slice. | HIGH | Existing `check:no-runtime-vhcnd` plus symlink/reference scan requirement. |

## Verification Targets

Validation may refine this list, but execution must expect at least:

- `python3 scripts/vltk-normalize-equipment-index.py`
- `python3 scripts/vltk-build-equipment-seed.py`
- `python3 scripts/vltk-audit-equipment-stat-coverage.py`
- `python3 scripts/vltk-audit-equipment-quality-coverage.py`
- `python3 scripts/vltk-audit-equipment-seed-coverage.py`
- `npm run typecheck`
- `npm run test:pbt`
- `npm run check:no-runtime-vhcnd`
- symlink scan for runtime asset folders before any visual story closes

## Out Of Scope For This Story

- Full formula parity implementation beyond constraints needed for catalog/slot foundation.
- Portrait UI redesign beyond slot model readiness.
- Visual SPR batch port beyond preserving isolation and provenance gates.
- Multiplayer/server persistence/trading/crafting/monetization.

## Bead Mapping

Pending validation. If validation is `READY WITH CONSTRAINTS`, create only current-story beads for the slice above; do not create future visual/UI/formula beads.
