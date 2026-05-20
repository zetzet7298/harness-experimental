# Review Report — S42 PiFeng Missing NpcRes Row Audit Hardening

**Date:** 2026-05-20
**Scope:** Visual status audit hardening, current audit data, property regression, and targeted smoke expectation refresh.

## Verdict

PASS — no P1 findings.

## Findings

- P1: none.
- P2: none.
- P3: none.

## Evidence Checked

- New property coverage in `tests/properties/equipmentNpcResRowHandling.unit.test.ts` proves the six unresolved rows are PiFeng normal/magic pairs with `PiFengRes` table values 12/13/14 and no candidate/resolved sprites.
- `equipment-visual-status.audit.json` now includes `missingNpcResRows=6` and `unresolvedVisualItems=6568`.
- Targeted smoke test aligns to current generated counts and rejects stale `missing-resource-resolution` expectations.
- Runtime isolation and production build passed in S42 validation.

## Remaining Risk

The six PiFeng rows are still unresolved visually. This review only verifies they are truthfully represented as unresolved and cannot be mistaken for complete coverage.
