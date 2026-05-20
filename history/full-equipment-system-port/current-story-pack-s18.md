# Current Story Pack — S18 Heavy Artifact / Gitignore Policy

**Feature:** full-equipment-system-port
**Epic:** E5 Isolation, validation, and release hygiene
**Mode:** `high_risk_feature`
**Prepared after:** S17 reference/runtime isolation audit passed and pushed.

## Story Outcome

Audit current heavy generated/debug artifacts and tighten ignore policy so local-only playtest/debug outputs stay out of git, while required runtime assets and canonical evidence files remain intentionally tracked.

## Entry State

- User explicitly allowed putting unused/heavy outputs into gitignore.
- `game-source` already ignores `dist/`, `.gitnexus/`, map full-background debug JPGs, local wardrobe-debug copies outside `public/`, and equipment visual runner/compose scratch summaries.
- `public/assets/character/vhcnd/wardrobe-debug/` is heavy, but it is currently runtime-wired by `GameScene` through `/assets/character/vhcnd/wardrobe-debug/catalog.json`, so it cannot be blindly ignored or removed in this hygiene slice.

## Acceptance Criteria

1. Large local-only artifacts are identified with size/path evidence.
2. `.gitignore` ignores local browser/playtest evidence dumps under `artifacts/`.
3. Existing local-only heavy paths remain ignored: `.gitnexus/`, `dist/`, `public/assets/maps/vhcnd/*/background.jpg`, and non-runtime `assets/character/vhcnd/wardrobe-debug/`.
4. Required runtime/evidence assets are not accidentally newly ignored, especially `public/assets/character/vhcnd/wardrobe-debug/`.
5. Runtime isolation guard still passes.
6. Validation report records which heavy paths are intentionally tracked vs ignored.

## Non-Goals

- Do not remove tracked runtime assets from git in S18.
- Do not redesign the wardrobe debugger or visual resolver.
- Do not rewrite generated catalog/data files unless a later story proves a safer runtime/evidence split.

## Expected Files / Impact Surface

- `/var/www/vltk-h5-survivors/game-source/.gitignore`
- `history/full-equipment-system-port/validation-s18.md`
- `history/full-equipment-system-port/review-report-s18.md`

## Planning Handoff

S18 is a small hygiene slice. If the `.gitignore` change is limited to local artifacts and validation proves runtime assets are not newly ignored, execution can proceed directly after validation.
