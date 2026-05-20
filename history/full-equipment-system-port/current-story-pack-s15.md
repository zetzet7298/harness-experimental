# Current Story Pack — S15 In-Run Resolver Parity

**Feature:** full-equipment-system-port  
**Epic:** E4 Equipped visual parity pipeline  
**Mode:** `high_risk_feature`  
**Prepared after:** S14 review/compounding passed; `CONTEXT.md` updated with D11-D13.

## Story Outcome

Make the in-run character visual resolver prove that the equipment loadout equipped outside a run is the same loadout used inside `GameScene`, with source-backed visual basenames, passed preview/local-source gates, deterministic fallback reporting, and browser-visible proof for the canonical smoke loadout.

## Entry State

- S13 source-backed the canonical smoke loadout rows and local copied SPRs for Tu La Phát Kết, Giáng Sa bào, and Địch Khái Lục Ngọc Trượng.
- S14 made catalog-scale visual status measurable: 9552 total catalog rows, 3 preview-passed/resolved rows, and 0 unsafe resolved visual rows.
- `GameScene.loadEquipmentVisuals()` currently tries whole-loadout manifest, then layered parts, then unresolved-audit/report/fallback paths.
- Browser smoke already has `tests/smoke/equipment-loadout.spec.ts`, but S15 must validate that the runtime resolver state and rendered first in-run frame actually prove the out-of-run equipped loadout, not only that a screenshot exists.
- New locked constraints apply to any touched UI/runtime output: user-facing text must be Vietnamese only, no Chinese text in player-visible UI; no symlink/direct `/var/www/vhcnd` runtime dependency; popup placement and horse quality constraints must not regress even if not directly implemented in this story.

## Acceptance Criteria

1. In-run resolver proof exists for the smoke loadout: outside-run equipped item ids flow into `GameScene`, produce the expected run/idle SPR basename sets, and match a `passed-generated` manifest entry or complete layered-parts entry before rendering.
2. The proof is inspectable in code/tests without relying only on a broad screenshot diff: expose or test a deterministic resolver status/debug snapshot containing equipped item ids, selected path (`manifest`, `parts`, `audit-fallback`, or `hard-fallback`), selected manifest/part identifiers, and run/idle basenames.
3. The canonical smoke loadout test fails if the in-run resolver silently falls back to `PLAYER_IDLE_SHEET` or renders a visual not backed by passed preview/local copied source assets.
4. Validation includes runtime isolation (`check:no-runtime-vhcnd`), visual-status audit, visual part/coverage audits, typecheck, property/unit tests touching the resolver, and Playwright/browser proof on port 5173.
5. Any user-facing strings introduced or touched by the story are Vietnamese-only and contain no Chinese characters; internal provenance ids/aliases may remain non-user-facing.
6. No direct runtime read or symlink to `/var/www/vhcnd` is introduced; source assets used by runtime stay inside `game-source`.

## Non-Goals

- Do not batch-port all missing equipment visuals.
- Do not redesign the equipment popup in S15 except to avoid regressing D13 if touched.
- Do not change equipment quality taxonomy except to avoid introducing green-quality mounts.
- Do not replace the established preview-gated visual pipeline with guessed SPR mappings.

## Validation Questions

1. What runtime state is currently observable from `GameScene` after `loadEquipmentVisuals()`, and is it enough for a browser smoke to assert manifest/parts/fallback path?
2. Does the existing smoke loadout currently select the `passed-generated` manifest entry, layered parts, or fallback path when run through the browser?
3. Which smallest seam should expose resolver status for tests without leaking debug UI to players?
4. Do current tests catch a mismatch between equipped item ids, basename sets, manifest status, and rendered texture key?
5. Can the browser test assert Vietnamese-only visible text without turning internal provenance ids into a false failure?

## Expected Files / Impact Surface

- `/var/www/vltk-h5-survivors/game-source/src/game/scenes/GameScene.ts`
- `/var/www/vltk-h5-survivors/game-source/src/game/visualResolver.ts`
- `/var/www/vltk-h5-survivors/game-source/tests/properties/visualResolver.unit.test.ts`
- `/var/www/vltk-h5-survivors/game-source/tests/smoke/equipment-loadout.spec.ts`
- Existing visual audit outputs under `/var/www/vltk-h5-survivors/game-source/data/vltk-normalized/`
- Harness docs/state for this story pack and validation evidence

## Planning Handoff

S15 is ready for `khuym:validating`. Do not create execution beads until validation proves the observable resolver seam and command set. If validation finds the existing browser smoke already proves all criteria, create a small review/audit bead instead of changing runtime code.

## Execution Evidence — 2026-05-20

- Added non-user-facing `GameScene.getEquipmentVisualResolverStatus()` returning equipped ids, run/idle basenames, selected resolver path, selected manifest id, selected part filenames, active texture keys, and fallback reason.
- Strengthened Playwright smoke so the canonical 3-piece loadout fails if runtime falls to audit/hard fallback, wrong equipped ids, wrong basenames, or wrong layered part filenames.
- Browser evidence showed the 3-piece smoke loadout correctly uses dynamic `parts` rather than whole-loadout `manifest` because no horse is equipped; visual part coverage is complete and preview-backed.
- Validation passed: visual-status audit, visual coverage audit, visual part coverage audit, runtime isolation, typecheck, property tests, and Playwright smoke.
