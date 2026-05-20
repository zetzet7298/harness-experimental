# Overview

## Current Behavior

The H5 prototype previously had a fixture inventory and a known equipped-character spritesheet path. Equipment slots, item requirements, catalog-wide PC equipment data, outside-run equipment UI, and runtime stat application were not generalized.

## Target Behavior

Port the VHCND equipment system as a source-backed vertical slice: all PC equipment slots are represented, generated equipment catalog data comes from decoded VHCND tables, outside-run equipment can equip/unequip and persist with `localStorage`, run startup reads the same equipped loadout, and derived combat stats/HUD values are calculated from equipped items.

## Affected Users

- Player testing mobile portrait equipment flow before a run.
- Porting agents validating VHCND item identity, requirements, quality, and visual mappings.

## Affected Product Docs

- `docs/product/current-state.md`
- `docs/product/vhcnd-porting.md`
- `docs/TEST_MATRIX.md`

## Non-Goals

- Claiming every VHCND magic attribute formula is complete before PC engine parity tests exist.
- Runtime-reading `/var/www/vhcnd`; all runtime assets remain copied/generated under `game-source/public/assets`.
- Prebuilding every possible weapon/horse/body/helm visual combination; current implementation loads available approved wardrobe combo sheets on demand.
