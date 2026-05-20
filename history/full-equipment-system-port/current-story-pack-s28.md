# Current Story Pack — S28 Equipment Visual Parts Expansion

**Date:** 2026-05-20
**Feature:** full-equipment-system-port
**Mode:** bounded visual-coverage slice
**Source context:** `CONTEXT.md` D2/D6/D9/D11/D14 and the remaining visual coverage gap after S24/S27.

## Story Outcome

Expand source-backed equipment visual coverage without violating runtime isolation: improve resource resolution, export all currently available copied local part SPRs into dynamic layered runtime part sheets, and quantify the remaining visual gaps explicitly.

## Acceptance Criteria

1. Resource resolution records candidate SPR evidence from active VHCND tables instead of leaving all visual rows as unresolved when source rows exist.
2. Visual-status audit promotes only rows whose required sprite basenames have passed preview evidence and local copied source SPRs; unsafe or symlinked sources remain blocking.
3. Dynamic part export uses local copied SPRs under `game-source/public/assets/character/vhcnd/source/` only, preferring the canonical `equipment-visual-parts-all` packet when duplicate basenames exist.
4. Generated audits report updated counts and remaining gaps; no claim of full visual parity is made while gaps remain.
5. Runtime isolation, unit/property coverage, and production build remain green.
6. Browser smoke on `localhost:5173` proves the Phaser canvas still boots after the generated catalog/assets refresh.

## Expected Files / Impact Surface

- `/var/www/vltk-h5-survivors/game-source/scripts/vltk-normalize-equipment-index.py`
- `/var/www/vltk-h5-survivors/game-source/scripts/vltk-audit-equipment-visual-status.py`
- `/var/www/vltk-h5-survivors/game-source/scripts/vltk-export-equipment-visual-parts.py`
- `/var/www/vltk-h5-survivors/game-source/src/data/equipmentCatalog.json`
- `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/*.json`
- `/var/www/vltk-h5-survivors/game-source/public/assets/character/vhcnd/source/equipment-visual-parts-all/`
- `/var/www/vltk-h5-survivors/game-source/public/assets/character/vhcnd/parts/{run,idle}/`
- `history/full-equipment-system-port/CONTEXT.md`
- `history/full-equipment-system-port/current-story-pack-s28.md`
- `history/full-equipment-system-port/validation-s28.md`
- `history/full-equipment-system-port/review-report-s28.md`

## Planning Handoff

Proceed to validation/review for this bounded expansion. The next story must continue the remaining `remainingDedicatedPartAssetGap=38` / `remainingPartSheetGap=272` visual coverage gaps; S28 is not full visual completion.
