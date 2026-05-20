# US-004 Import Real VLTK Tables

## Status

planned

## Lane

high-risk

## Product Contract

Replace or expand fixture-only VLTK bridge data with verified rows from legacy PC
tables while preserving decoded names, source paths, row identity, attributes,
requirements, and uncertainty notes.

## Relevant Product Docs

- `docs/product/vhcnd-porting.md`
- `docs/product/roadmap.md`

## Acceptance Criteria

- Identify exact source tables and encodings before importing rows.
- Export normalized H5 fixture/import artifacts with provenance fields.
- Keep fixture data transport-neutral behind the gateway boundary.
- Add tests or validation scripts for representative imported equipment rows.

## Design Notes

- Expected source lane currently documented in `game-source/src/data/README.md`:
  `vhcnd/Settings/item/meleeweapon.txt`, `vhcnd/Settings/item/GoldItem.txt`,
  and `vhcnd/Settings/item/magicattrib.txt`.
- Use `vhcnd-item-research` before changing data contracts.

## Validation

| Layer | Expected proof |
| --- | --- |
| Unit | Row normalization tests for representative equipment. |
| Integration | Script/report proving decoded source rows. |
| E2E | Not required for first import unless UI changes. |
| Platform | Not applicable. |
| Release | Not defined. |

## Harness Delta

- Update product docs, test matrix, and a decision if the data contract changes.

## Evidence

- Pending.

