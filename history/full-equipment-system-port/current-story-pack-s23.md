# Current Story Pack — S23 Resist Cap Evidence Reconciliation

**Date:** 2026-05-20  
**Feature:** full-equipment-system-port  
**Mode:** small evidence/validation slice  
**Source context:** `CONTEXT.md` deferred planning item: reconcile H5 `PC_MAX_RESIST` with VHCND `MAX_RESIST`.

## Story Outcome

Close the stale `MAX_RESIST` uncertainty by proving the active VHCND client constant and H5 formula gate agree on `PC_MAX_RESIST = 150`, while preserving per-call `resistMax` override behavior for tests that deliberately use `95` as an example cap.

## Entry State

- H5 already exports `PC_MAX_RESIST = 150` and has tests around `applyPcResistDamage`.
- `CONTEXT.md` still lists the old uncertainty: reconcile H5 `PC_MAX_RESIST = 95` with VHCND `MAX_RESIST = 150`.
- Some test comments still mention stale `MAX_RESIST = 95` source anchors even though the code/test constants now use `150`.

## Acceptance Criteria

1. VHCND source evidence is cited for `MAX_RESIST = 150`.
2. H5 source/tests have no stale claim that active `MAX_RESIST` is `95`.
3. Tests still cover both:
   - global PC cap `150`; and
   - per-call tighter cap examples such as `resistMax = 95`.
4. `CONTEXT.md` deferred item is marked resolved with S23 evidence.
5. Validation includes targeted tests plus a stale-text scan.

## Non-Goals

- Do not change unrelated stat formulas.
- Do not reinterpret all elemental damage formulas in this story.
- Do not claim full formula parity beyond the resist-cap uncertainty.

## Expected Files / Impact Surface

- `/var/www/vltk-h5-survivors/game-source/tests/properties/equipment.unit.test.ts`
- `history/full-equipment-system-port/CONTEXT.md`
- `history/full-equipment-system-port/validation-s23.md`
- `history/full-equipment-system-port/review-report-s23.md`

## Planning Handoff

Proceed directly to validation/repair: update stale comments/test titles only if code already matches `150`; run targeted property tests and stale scans.
