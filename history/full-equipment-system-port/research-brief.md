# Research Brief — Full Equipment System Port

## Bottom Line

- Recommendation: extend the existing local equipment stack rather than replace it; add missing VHCND equipment slots/tables, harden formula parity against source pivots, redesign `EquipmentScene` for portrait all-slot coverage, and keep the existing preview-gated local asset pipeline for visuals.
- Why this is the lightest credible path: the repo already has a generated catalog, seed builder, stat engine, persistence, out-of-run/in-run gateway parity, visual resolver, SPR gate scripts, and property tests. Reusing them avoids rebuilding the system while still allowing full coverage.
- Confidence (`0-100%`): 82% for the path, lower for exact remaining formula constants until planning reconciles active VHCND variants.
- Next step: invoke `khuym:planning` to break the port into validated slices and define audit gates before any implementation.

## Repo Snapshot

- Repo type: mixed harness + Phaser/Vite game source; this brief targets `/var/www/vltk-h5-survivors/game-source`.
- Primary languages and runtimes: TypeScript, Python scripts, Vite, Vitest, Playwright, Phaser.
- Frameworks/platforms detected: Phaser `4.1.0`, Vite `8.0.13`, TypeScript `6.0.3`, Vitest `4.1.6`, Playwright `^1.60.0`.
- Relevant packages, services, or tools: GitNexus repos `vltk-h5-survivors`, `vhcnd`, group `@vltk-porting`; Khuym harness; `srcwalk`; local VHCND extractor/SPR porting scripts.
- Detectable versions: from `package.json` in `game-source`.
- Important repo constraints or workflows: runtime must not read `/var/www/vhcnd`; no symlink; source SPR/assets must be copied/moved into `game-source`; build runs `check:no-runtime-vhcnd`.

## Feature Understanding And Assumptions

- Requested feature: continue porting the complete VHCND equipment system inside and outside runs, including UI, data, stats, requirements, quality/series/five-elements, seed data, and exact equipped visual parity.
- What success appears to mean: every VHCND equipment row/category is represented or audited; equipping outside run changes stats and in-run visual layers; popup/UI are mobile-portrait friendly; formulas are source-backed; seed data makes testing easy.
- Assumptions from the request: screenshots are visual references, not slot-count limits; all PC-supported slots must be included; one-cell mobile bag behavior is desired even when original item dimensions differ.
- Assumptions that still need confirmation: none blocking exploration; planning must verify active source/table precedence and source constants.

## Evidence Ledger

- `Local`: `game-source` already has equipment domain/types/UI/gateway/scripts/tests, with a generated 1231-item catalog and 11-slot model.
- `Local`: current H5 slot model lacks VHCND extended slots found in PC source (`mask`, `pifeng`, `yinjian`, `shiping`).
- `Local`: current catalog has 1231 items: 560 normal, 500 magic, 171 gold; no entries default to `ring2`, and visual statuses are still candidates/missing rather than preview-passed for most rows.
- `Local`: source rows for user examples already exist in catalog: Tu La Phát Kết, Giáng Sa bào, Địch Khái Lục Ngọc Trượng, and Liệt Hoàng Mã.
- `Local`: `LocalOfflineGateway.startRun()` routes through `getInventory()`, so the existing seam supports out-of-run/in-run stats parity.
- `Local`: VHCND `KItemList::Fit` confirms slot mapping and extended slots; `KItemGenerator::GetEquipmentCommonAttrib` confirms common base attribute lookup by `particular * 10 + level - 1`.
- `Docs`: Phaser docs support continuing with Containers, Images, Text, and Grid GameObjects for responsive portrait UI panels/grids.
- `Inference`: the safest path is incremental expansion with audits because data/formula/visual parity have different proof gates.

## Local Findings

- Relevant files, modules, scripts, docs, or tests:
  - `src/domain/equipment.ts`, `src/domain/types.ts`, `src/domain/equipmentStore.ts`
  - `src/game/scenes/EquipmentScene.ts`, `src/game/visualResolver.ts`, `src/gateway/offlineGateway.ts`
  - `src/data/equipmentCatalog.json`, `src/data/inventory.json`, `src/data/profile.json`
  - `scripts/vltk-build-equipment-seed.py`, `scripts/vltk-normalize-equipment-index.py`, `scripts/vltk-port-loadout.py`, `scripts/vltk-extract-required-sprs.py`, `scripts/vltk-audit-equipment-*.py`
  - `tests/properties/*.test.ts`, `tests/smoke/equipment-loadout.*`, `tests/test_vltk_porting_smoke.py`
- Existing abstractions or extension points: `EquipmentSlot`, `EquipmentItem`, `CharacterStats`, `calculateEquipmentStats`, `canEquipItem`, `buildInventorySnapshot`, visual manifest resolver, seed builder, audit scripts.
- Conventions worth preserving: source provenance per row; deterministic generated option values; preview-gated visual status; one-cell mobile bag policy; local copied asset source root.
- What can likely be reused: most of the current equipment stack, with schema/slot expansion and audits.
- What appears missing locally: extended slots, full active table coverage for Mask/PiFeng/YinJian/ShiPin and related gold/quality data, complete visual preview/pass manifests, and reconciled formula constants for active VHCND source.

## Upstream Findings

- Repositories inspected: none beyond local VHCND mirror; public upstream is not necessary for source parity because VHCND local source/tables are the canonical evidence.
- Pattern or capability already present upstream: not applicable.
- Files, modules, or areas worth modeling: not applicable.
- How closely the upstream pattern matches this repo: not applicable.
- Any upstream gaps or uncertainties: no public upstream should override local VHCND evidence.

## Docs Findings

- Official sources checked: Phaser API docs via Context7 for Container, Image, Text, and Grid GameObjects.
- Version-matched vs latest-stable status: Context7 exposed Phaser docs including current API pages; local package is Phaser `4.1.0`.
- Built-in capabilities that already support the feature: Containers group relative UI elements; Images support loaded icon textures; Text supports styled/wrapped tooltip lines; Grid can render matrix-like bag cells.
- Current recommended APIs or workflows: continue using `this.add.container`, `this.add.image`, `this.add.text`, and grid/shape primitives in `EquipmentScene` instead of introducing a separate UI framework.
- Important caveats, deprecations, or migration notes: Container scroll factors affect rendering but not physics; this UI is non-physics, so it is acceptable.

## Recommendation

- Primary recommendation: reuse and expand the existing local equipment system.
- Why this is the lightest credible path: current H5 already implements a large portion of data/stat/UI/visual infrastructure and has targeted audits/tests; extension keeps existing proof intact.
- Why the next-best alternative lost: rebuilding a new equipment module from scratch would discard existing VHCND provenance, smoke loadouts, persistence, and no-runtime-VHCND guards while increasing parity risk.
- What would change the recommendation: if planning proves current generated catalog/schema is fundamentally inconsistent with active VHCND package precedence, the data normalization layer may need a larger rewrite, but runtime/UI can still reuse current seams.

## Risks, Unknowns, And Follow-Up Questions

- Technical risks: formula constants may differ between indexed source variants; complete visual coverage could be large; extended slots may require UI and activation-chain redesign; current seed cap may hide coverage gaps.
- Evidence gaps: exact active package/table precedence for every equipment table; counts for missing/candidate/passed visual coverage; definitive source for every magic option behavior.
- Version uncertainties: Phaser API is adequate; no blocking version risk found.
- Follow-up questions for the user, if any: none before planning. The feature is sufficiently specified for Khuym planning.

## Source Pack

- Local files read:
  - `AGENTS.md`
  - `.khuym/state.json`, `.khuym/HANDOFF.json`, `history/learnings/critical-patterns.md`
  - `/var/www/vltk-h5-survivors/game-source/package.json`
  - `/var/www/vltk-h5-survivors/game-source/scripts/README.md`
  - `/var/www/vltk-h5-survivors/game-source/docs/VHCND_SPR_PORTING_PLAYBOOK.md`
  - `/var/www/vltk-h5-survivors/game-source/src/domain/types.ts`
  - `/var/www/vltk-h5-survivors/game-source/src/domain/equipment.ts`
  - `/var/www/vltk-h5-survivors/game-source/src/game/scenes/EquipmentScene.ts`
  - `/var/www/vltk-h5-survivors/game-source/src/gateway/offlineGateway.ts`
  - `/var/www/vltk-h5-survivors/game-source/src/game/visualResolver.ts`
  - `/var/www/vhcnd/sources/Client/Classes/gamecore/KItemList.cpp:1912-1977`
  - `/var/www/vhcnd/sources/Client/Classes/gamecore/KItemGenerator.CPP:3227-3299`
  - `/var/www/vhcnd/sources/Client/Classes/gamecore/GameDataDef.h` search evidence
- Upstream repositories or pages checked: none; local VHCND mirror is canonical.
- Official docs domains or pages checked: `docs.phaser.io` API docs via Context7.

## Evidence Boundary

- `Local` for repository files, local VHCND source/tables, GitNexus, and srcwalk findings.
- `Docs` for Phaser API documentation.
- `Inference` for recommended implementation sequencing and risk ranking.
