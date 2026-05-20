# Learning — S22 No-Horse Visual Expansion

**Date:** 2026-05-20  
**Feature:** full-equipment-system-port  
**Story:** S22 No-Horse Smoke Loadout Visual Expansion  
**Category:** compounding  
**Critical promotion:** no

## What Happened

S22 added a preview-passed no-horse runtime visual entry for the user-facing smoke loadout: Địch Khái Lục Ngọc Trượng + Giáng Sa bào + Tu La phát kết, with no horse layer. The first real shard run generated packets but failed extraction because the VHCND extractor reported all required SPRs as missing even though those same raw SPR files already existed locally under `public/assets/character/vhcnd/source/**` from prior preview-gated loadouts.

A second issue appeared after the local-copy repair: the new public `required-sprs.report.json` files included the forbidden absolute external source-root literal in explanatory text, which tripped `npm run check:no-runtime-vhcnd` even though runtime code did not read that root.

## Root Cause

- The extractor treated the current decode attempt as the only valid source of raw SPR files. It did not reuse already-previewed, already-local SPR copies from earlier loadouts.
- The runtime-isolation gate correctly scans public assets and reports, so even human-readable provenance text under `public/` must avoid forbidden absolute external-root literals.

## Durable Rule

When adding a new equipment visual loadout whose SPR basenames were already copied into `game-source` by a prior preview-gated loadout:

1. Reuse those repo-local raw SPR sources by copying them into the new slug folder; never symlink and never make runtime read an external source root.
2. Still generate a new `required-sprs.report.json` for the new slug so the current loadout has its own copied/missing evidence.
3. Keep public report text free of forbidden absolute external-root literals; use neutral wording such as “external source root” in files under `public/`.
4. Run `npm run check:no-runtime-vhcnd` after generating or editing any public report, not only after code changes.

## Evidence

- Repair: `scripts/vltk-extract-required-sprs.py` now copies missing decoded hits from existing local source folders when safe.
- Test: `tests/test_vltk_porting_smoke.py::test_required_spr_extractor_reuses_existing_local_sources_without_symlink`.
- Validation: `history/full-equipment-system-port/validation-s22.md`.
- Commits:
  - game-source: `ce79085 feat(equipment): add no-horse visual loadout`
  - harness: `e6f228d docs(equipment): record s22 visual expansion`

## Why Not Critical

This is reusable and concrete, but it is not yet a repeated P1/P2 failure pattern. `critical-patterns.md` already covers the stronger general rule: resolve visual identity before copying SPRs and preserve local-asset/runtime-isolation gates.
