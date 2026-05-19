# Exec Plan

## Goal

Create a source-backed equipment catalog and portrait equipment flow that persists equipped items and feeds run-time stats/visual selection.

## Scope

In scope:

- Normalize VLTKPC normal/gold equipment tables into a generated H5 catalog.
- Preserve all PC equipment slots: head, body, belt, weapon, foot, cuff, amulet, ring1, ring2, pendant, horse.
- Seed a one-mobile-cell-per-item inventory for easy testing.
- Apply supported item requirements and derived stats in H5 runtime.
- Add a portrait Phaser equipment scene before run start.
- Parallelize long SPR copy extraction with `--workers auto`.

Out of scope:

- Full PC engine formula proof for every magic attribute not yet mapped in `src/domain/equipment.ts`.
- Generating every possible visual loadout combination before preview approval.
- Backend persistence or economy integration.

## Risk Classification

Risk flags:

- Cross-platform: redesigns equipment UX for portrait mobile.
- Existing behavior: changes run startup, inventory, HUD, and simulation stats.
- Weak proof: many legacy magic attributes need more PC formula coverage.
- Multi-domain: data import, UI, runtime simulation, asset tooling, and docs all change.

Hard gates:

- None, but source-backed VLTKPC evidence and runtime-local asset rules apply.

## Work Phases

1. Decode and normalize equipment tables.
2. Generate catalog and seed inventory.
3. Implement equip validation and stat aggregation.
4. Add portrait equipment UI and run handoff.
5. Wire run startup to persisted equipped state.
6. Validate smoke tests, TypeScript, and production build.
7. Update product docs and test matrix.

## Stop Conditions

Pause for human confirmation if:

- A formula cannot be traced to VLTKPC source and would require guessing.
- Runtime visual assets would need direct reads from `/var/www/vltkpc`.
- Validation gates need to be weakened.
