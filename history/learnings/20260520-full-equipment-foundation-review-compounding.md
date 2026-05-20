# Learning — Full Equipment Foundation Review Compounding

**Date:** 2026-05-20  
**Feature:** full-equipment-system-port  
**Story:** S1/S2/S3 catalog + slot taxonomy foundation  
**Evidence:** `history/full-equipment-system-port/review-report.md`, commits `234b478` (`game-source`) and `cd7656f` (`harness-experimental`)

## What Actually Happened

The first equipment foundation slice reached swarming completion, but review found acceptance gaps that normal validation did not catch:

1. The normalizer exposed `activeTableInventory`, but no gate failed when required tables such as `GoldMagic.txt` and `magicattrib.txt` were absent from the inventory surface.
2. Several audits still encoded the original 11-slot model, so the new extended slots (`mask`, `pifeng`, `yinjian`, `shiping`) could regress without failing.
3. EquipmentScene tests proved slot tuple presence only; they did not prove the portrait layout kept the extended slot buttons/captions inside the paper-doll panel.
4. Runtime isolation only scanned `src/`; public runtime artifacts still had absolute `/var/www/vhcnd` provenance strings, and symlink checking was not a reusable package gate.

Review fixes added a table-inventory audit, expanded stat/series audits to all 15 slots, added layout bounds tests, and promoted runtime isolation to `npm run check:runtime-isolation` scanning `src/` and `public/` for absolute VHCND literals and symlinks.

## Durable Patterns

- Acceptance criteria that say "document/prove inventory" need a dedicated fail-fast audit, not just a generated JSON field.
- When a domain taxonomy expands, every audit/test with hard-coded expected keys must be treated as a migration target. A type-level compile pass is not enough.
- UI source tests that only check presence can miss layout regressions. For portrait/mobile work, include panel-bound and disjointness invariants early.
- Runtime isolation should be one package command and part of `prebuild`; ad-hoc shell snippets in reports are easy to skip.

## Decisions Carried Forward

- Build/audit scripts may read `/var/www/vhcnd` as evidence/input, but runtime-served surfaces must not contain absolute `/var/www/vhcnd` literals or symlinks.
- Public runtime manifests should use local/runtime-safe provenance identifiers instead of absolute local source paths.
- Extended H5 slots are part of the canonical equipment taxonomy for future formula, UI, seed, and visual stories.

## Failure Modes To Watch In Next Stories

- Formula parity (S5-S8) can repeat the same mistake if constants and option keys are only documented, not audited against source pivots.
- UI stories (S9-S11) can pass unit tests while still failing mobile readability unless screenshot/UAT gates are part of the story exit.
- Visual stories (S13-S16) can reintroduce unsafe provenance if generated reports are placed under `public/` with absolute local source paths.

## Future Rule

For every new equipment slice, define a narrow acceptance audit before claiming review readiness. The audit must fail on the exact class of omission the story is meant to prevent: missing table provenance, missing slot keys, missing formula pivots, missing visual preview pass, or unsafe runtime path/symlink.
