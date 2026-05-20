# Validation — S18 Heavy Artifact / Gitignore Policy

**Date:** 2026-05-20
**Feature:** full-equipment-system-port
**Story:** `current-story-pack-s18.md`
**Result:** PASS — `.gitignore` tightened without hiding required runtime assets.

## Heavy Artifact Inventory

From `/var/www/vltk-h5-survivors/game-source`:

- Tracked large evidence/runtime files:
  - `src/data/equipmentCatalog.json` — 23M, canonical runtime catalog.
  - `data/vltk-normalized/equipment-visual-jobs/shard-000.json` — 22M, canonical visual shard evidence.
  - `data/vltk-normalized/equipment-index.json` — 18M, canonical normalized equipment index.
  - `public/assets/character/vhcnd/equipment-visual-parts-manifest.json` — 5.7M, runtime visual manifest.
  - `public/assets/character/vhcnd/wardrobe-debug/**` — tracked and runtime-wired by `GameScene`, so not ignored in this slice.
- Ignored local/generated heavy paths:
  - `.gitnexus/` — local GitNexus cache, includes `lbug` around 102M.
  - `dist/` — build output.
  - `public/assets/maps/vhcnd/*/background.jpg` — generated full background debug image, example around 60M.
  - `assets/character/vhcnd/wardrobe-debug/` — non-runtime wardrobe debug scratch around 95M.
  - `artifacts/` — local browser/playtest evidence dumps; now explicitly ignored.

## Change Made

`game-source/.gitignore` now:

- explicitly ignores `artifacts/` under local screenshots/recordings/evidence dumps;
- documents that `public/assets/character/vhcnd/wardrobe-debug/` is intentionally tracked because runtime code uses it.

## Commands / Evidence

```bash
git check-ignore -v artifacts/some-new-proof.png artifacts/screenshots/existing.png \
  public/assets/character/vhcnd/wardrobe-debug/new.png \
  assets/character/vhcnd/wardrobe-debug/new.png \
  public/assets/maps/vhcnd/balang-huyen/background.jpg \
  .gitnexus/lbug
```

Evidence:

- `artifacts/some-new-proof.png` and `artifacts/screenshots/existing.png` match `.gitignore:64:artifacts/`.
- `assets/character/vhcnd/wardrobe-debug/new.png` matches `.gitignore:77:assets/character/vhcnd/wardrobe-debug/`.
- `public/assets/maps/vhcnd/balang-huyen/background.jpg` matches `.gitignore:70:public/assets/maps/vhcnd/*/background.jpg`.
- `.gitnexus/lbug` matches `.gitignore:85:.gitnexus/`.
- `public/assets/character/vhcnd/wardrobe-debug/new.png` produced no ignore match, preserving the runtime-wired public path.
- `npm run check:no-runtime-vhcnd` passed.

## Decision

S18 is complete. No tracked runtime/evidence files were removed; only local artifact ignore policy was tightened.
