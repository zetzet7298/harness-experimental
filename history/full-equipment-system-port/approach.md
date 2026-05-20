# Approach — Full Equipment System Port

**Mode:** `high_risk_feature`  
**Shape:** Epic map + current-story candidate; no current story pack, execution beads, or implementation until the work shape is approved and `khuym:validating` accepts feasibility.  
**Date:** 2026-05-20

## Mode Gate

This is not a direct/small change because it crosses the catalog generator, persisted slot schema, equipment formulas, portrait UI, runtime run-start snapshot, character visual assets, and isolation guards. It is not safe to implement as one technical bucket: data completeness, formula parity, and visual correctness each need separate proof gates. `high_risk_feature` is required because mistakes can silently fabricate VHCND stats, equip invalid items, or wire runtime assets from the wrong source root.

## Recommendation

Extend the existing H5 equipment stack in `/var/www/vltk-h5-survivors/game-source` instead of replacing it.

- `Local`: current H5 already has `src/domain/equipment.ts`, `src/domain/types.ts`, `src/domain/equipmentStore.ts`, `src/game/scenes/EquipmentScene.ts`, `src/gateway/offlineGateway.ts`, `src/game/visualResolver.ts`, generated `src/data/equipmentCatalog.json`, seed inventory, VHCND normalization scripts, visual port scripts, and audit scripts.
- `Local`: `equipmentCatalog.json` currently contains 1231 items: 560 normal, 500 magic, 171 gold; default slots are limited to `head/body/belt/weapon/foot/cuff/amulet/ring1/pendant/horse` and currently no `mask/pifeng/yinjian/shiping` rows are represented.
- `Local`: PC `KItemList::Fit` maps `equip_mask`, `equip_pifeng`, `equip_yinjian`, and `equip_shiping` to distinct equipment places, so the current 11-slot H5 model is incomplete.
- `Local`: PC `KItemGenerator::GetEquipmentCommonAttrib` dispatches extended detail types through `GetMaskRecord`, `GetPifengRecord`, `GetYinjianRecord`, and `GetShipinRecord`, so base stats/formulas must include those tables rather than treating them as cosmetic extras.
- `Docs`: Phaser API docs support Grid / Container / Image / Text style UI building blocks, but Context7 only surfaced version-matched docs for Phaser `v3_90_0` while this repo depends on Phaser `4.1.0`; UI validation must rely on local compile/runtime smoke in addition to docs.
- `Inference`: the lightest credible route is incremental expansion with audit gates, because replacing the stack would discard existing source provenance, stat equality, persistence, and asset-isolation tests.

### Rejected Alternatives

1. **Full rewrite of equipment domain/UI.** Rejected because the current stack already has catalog provenance, requirement checks, stat aggregation, persistence, run-start snapshot parity, and tests.
2. **Port visuals first.** Rejected because visual rows depend on canonical item identity, active table precedence, slot taxonomy, sex/action/resource resolution, and preview gates.
3. **Catalog-only port without formula/UI changes.** Rejected because the user explicitly requires equip/unequip, exact stat formulas, conditions, portrait UI, seed data, and in-run visual parity.
4. **Use symlinks/direct `/var/www/vhcnd` runtime reads.** Rejected by locked decision D2 and the existing `check:no-runtime-vhcnd` gate.

## Risk Map

| Area | Risk | Reason | Proof Needed Before Execution/Close |
| --- | --- | --- | --- |
| Active source precedence | HIGH | Loose/Pak/ServerNew variants can disagree; wrong table source fabricates rows. | Scripted table precedence note and generated catalog source metadata for every included row. |
| Slot taxonomy/persistence | HIGH | Adding slots changes `EquipmentSlot`, persisted loadout schema, seed fallback, UI filters, and run-start snapshot order. | Typecheck + property tests proving all slots sanitize/equip/unequip and in-run snapshot remains equal. |
| Formula parity | HIGH | `PC_MAX_RESIST` discrepancy and many magic attribute keys affect HP, lực tay, resist caps, weapon damage, five-element behavior. | Source-backed formula audit against VHCND pivots and test vectors for representative normal/magic/gold items. |
| Extended tables | HIGH | `Mask.txt`, `PiFeng.txt`, `YinJian.txt`, `ShiPin.txt` are present but not currently normalized into H5 catalog. | Catalog count/coverage audit showing all active equipment categories are represented or explicitly excluded with evidence. |
| Visual parity | HIGH | Correct character visuals require item identity -> resource row -> local copied SPR -> preview passed -> composed runtime metadata. | Preview report(s), local source copies under `game-source`, no candidate wired without passed evidence. |
| Portrait UI | MEDIUM | More slots than the sample image; needs mobile readability without hiding equipment. | Browser screenshot/UAT showing all slots accessible, tooltip readable, bag grid one-cell policy preserved. |
| Seed/test inventory | MEDIUM | Full catalog in normal bag can be unusable; sampled seed can hide missing categories. | Deterministic seed plus test/catalog browser or filter mode that exposes every slot/category for QA. |
| Isolation/git hygiene | HIGH | Large generated assets can bloat repo; runtime must never depend on out-of-scope roots or symlinks. | `npm run check:no-runtime-vhcnd`, symlink scan, gitignore review for generated/heavy non-runtime artifacts. |

## Epic Map

**Feature outcome:** the H5 game has complete VHCND equipment coverage with source-backed data/formulas, mobile portrait equipment management, one-cell inventory seed/testing flow, local-only runtime assets, and out-of-run to in-run visual/stat parity.

**Architecture / reality basis:**

- H5 code lives in `/var/www/vltk-h5-survivors/game-source`; harness docs/planning live here in `harness-experimental`.
- VHCND legacy source/tables live in `/var/www/vhcnd` and are evidence/build input only, not runtime dependencies.
- `LocalOfflineGateway.startRun()` already goes through `getInventory()`/`buildInventorySnapshot`, so one source of derived stats can serve both outside-run and in-run.
- Current runtime build has `prebuild -> check:no-runtime-vhcnd` and the asset playbook requires preview-gated local source copies.

| Epic | Capability/Risk Area | Why It Exists | Stories | Proof Needed |
| --- | --- | --- | --- | --- |
| E1 | Canonical VHCND catalog + slot taxonomy | All later work depends on complete item identities, table provenance, and PC slot mapping. | S1 active table/source precedence; S2 extended slot model; S3 normalize missing tables; S4 catalog audits. | Catalog counts by table/slot/quality; no missing slot categories; source path/line/encoding retained. |
| E2 | Formula, requirements, and combat stat parity | User requires HP, lực tay, resists, damage, quality, conditions, five-elements, and option formulas to match VHCND. | S5 source-pivot formula ledger; S6 magic attribute coverage; S7 requirements/faction/sex/series fit; S8 stat vectors. | Formula parity audit, representative VHCND-derived fixtures, property tests. |
| E3 | Portrait equipment UI + inventory/seed workflow | More PC slots than sample UI; mobile one-cell bag and easy test equip/unequip are required. | S9 all-slot portrait layout; S10 tooltip redesign; S11 seed/test catalog browser; S12 persistence migration. | Browser screenshots, UI smoke, slot/filter tests, storage compatibility tests. |
| E4 | Equipped visual parity pipeline | Wearing examples outside run must render correct in-run head/body/weapon/horse/other visual parts. | S13 loadout visual gate for smoke set; S14 equipment visual manifest coverage; S15 in-run resolver parity; S16 batch preview plan. | Passed preview reports, copied source SPRs, generated metadata, runtime screenshots. |
| E5 | Isolation, validation, and release hygiene | Prevent regressions to `old PC source name`, direct VHCND reads, symlinks, or oversized generated artifacts. | S17 reference audit; S18 gitignore/heavy artifact policy; S19 full validation chain; S20 handoff/review pack. | `check:no-runtime-vhcnd`, reference scan, symlink scan, git status, pushed commits after execution phase. |

## Story Queue

| Story | Epic | Outcome | Depends On | Feasibility Status |
| --- | --- | --- | --- | --- |
| S1 Source precedence + table inventory | E1 | Planning/validation knows exactly which VHCND tables feed the catalog and what is missing. | CONTEXT locked | Needs validating proof |
| S2 Slot taxonomy expansion | E1 | H5 has a planned slot list including PC extended slots with migration boundaries. | S1 | Needs validating proof |
| S3 Catalog normalization expansion | E1 | Missing `mask/pifeng/yinjian/shiping` rows can be generated with provenance. | S1, S2 | Needs validating proof |
| S4 Catalog coverage audits | E1 | Fail-on-gap audits cover all active tables, qualities, slots, labels, icons, visuals. | S3 | Needs validating proof |
| S5 Formula ledger | E2 | Every H5 formula/constant maps to VHCND source/table evidence or an explicit gap. | S1 | Needs validating proof |
| S6 Magic attribute parity | E2 | Attribute keys/options used by normal/magic/gold items are implemented or fail audit. | S5 | Deferred |
| S7 Equip condition parity | E2 | Level/series/sex/faction/stat conditions follow VHCND semantics. | S5 | Deferred |
| S8 Stat vector fixtures | E2 | Representative loadouts prove HP/lực tay/resists/damage equality. | S6, S7 | Deferred |
| S9 All-slot portrait UI | E3 | Equipment scene exposes every PC slot in portrait without hiding slot groups. | S2 | Deferred |
| S10 VLTK-style tooltip | E3 | Popup shows quality/name/requirements/durability/stat/skill/value hierarchy. | S6, S7 | Deferred |
| S11 Seed/test inventory workflow | E3 | QA can equip/unequip every category easily; each equipment consumes one mobile cell. | S3 | Deferred |
| S12 Persistence migration | E3 | Existing saves sanitize into expanded slot schema without crashing. | S2, S11 | Deferred |
| S13 Smoke loadout visual gate | E4 | Tu La Phát Kết + Giáng Sa bào + Địch Khái Lục Ngọc Trượng visual path has passed preview and local source copies. | S1, S3 | Deferred |
| S14 Visual manifest coverage | E4 | Catalog visual statuses quantify candidate/missing/passed states and fail on unsafe wiring. | S13 | Deferred |
| S15 In-run resolver parity | E4 | In-run visual uses the same equipped loadout as outside-run scene. | S12, S13 | Deferred |
| S16 Batch preview plan | E4 | Large visual coverage can be processed in shards without wiring unreviewed SPRs. | S14 | Deferred |
| S17 Reference/isolation audit | E5 | Docs/skills/scripts/code do not point to `old PC source name` or runtime-read `/var/www/vhcnd`. | Any implementation slice | Deferred |
| S18 Heavy artifact/gitignore policy | E5 | Non-runtime/generated heavy artifacts are ignored; required runtime assets are tracked intentionally. | Visual work | Deferred |
| S19 Full validation chain | E5 | Typecheck/tests/audits/build/browser smoke prove the slice. | Current slice | Deferred |
| S20 Review/handoff pack | E5 | Reviewer has exact changed files, evidence, blockers, and next slice. | Current slice | Deferred |

## Current Story Candidate To Prepare After Approval: S1/S2/S3 Feasibility — Catalog + Slot Taxonomy Foundation

**Epic:** E1 Canonical VHCND catalog + slot taxonomy

### Candidate Entry State

- `EquipmentSlot` currently has 11 values: `head`, `body`, `belt`, `weapon`, `foot`, `cuff`, `amulet`, `ring1`, `ring2`, `pendant`, `horse`.
- Current catalog has 1231 rows and no default rows for `mask`, `pifeng`, `yinjian`, or `shiping`.
- VHCND source shows those four extended detail types in both slot fit and common base attribute dispatch.
- The active feature context requires no symlink/direct runtime `/var/www/vhcnd` access and no new `old PC source name` dependency.

### Candidate Exit State

If the work shape is approved and validation accepts feasibility, this story should exit with:

1. A source-backed table inventory for active VHCND equipment tables, including `Mask.txt`, `PiFeng.txt`, `YinJian.txt`, `ShiPin.txt`, `GoldItem.txt`, `GoldMagic.txt`, `magicattrib.txt`, and related base property/resource tables.
2. Expanded H5 slot taxonomy and labels that represent every PC equipment slot, with `ring1/ring2` dual-slot behavior preserved.
3. Normalizer support for the missing extended tables, retaining `source.path`, `encoding`, `line`, item fields, quality, requirements, attributes, and provenance.
4. A deterministic seed/test policy that includes representative items for every slot while preserving one-cell inventory cells.
5. Audits/tests proving catalog slot/quality/stat-label coverage and no unsafe runtime VHCND/symlink reference.

### Likely File Boundaries For Later Story Prep

- `/var/www/vltk-h5-survivors/game-source/src/domain/types.ts`
- `/var/www/vltk-h5-survivors/game-source/src/domain/equipment.ts`
- `/var/www/vltk-h5-survivors/game-source/src/domain/equipmentLabels.ts`
- `/var/www/vltk-h5-survivors/game-source/src/domain/equipmentStore.ts`
- `/var/www/vltk-h5-survivors/game-source/scripts/vltk-normalize-equipment-index.py`
- `/var/www/vltk-h5-survivors/game-source/scripts/vltk-build-equipment-seed.py`
- `/var/www/vltk-h5-survivors/game-source/scripts/vltk-audit-equipment-*.py`
- `/var/www/vltk-h5-survivors/game-source/src/data/equipmentCatalog.json`
- `/var/www/vltk-h5-survivors/game-source/src/data/inventory.json`
- `/var/www/vltk-h5-survivors/game-source/tests/properties/*.test.ts`
- Harness story/test docs if validation requests them.

### Validation Questions For `khuym:validating`

1. Can the normalizer read the four extended VHCND tables and produce rows with stable slots/qualities without breaking the existing 1231-row catalog assumptions?
2. Which source value is authoritative for `MAX_RESIST` in this workspace (`95` in current H5 comments vs `150` noted in CONTEXT deferred question), and what exact VHCND file/package evidence proves it?
3. Do existing tests/audits cover every new slot and option key, or must validation create a spike/audit before execution beads?
4. Can the seed/test workflow expose every equipment slot without turning normal gameplay inventory into a 1000+ item bag?

### Verification Targets

Validation should decide the exact command list, but expected proof includes:

- `python3 scripts/vltk-normalize-equipment-index.py`
- `python3 scripts/vltk-build-equipment-seed.py`
- `python3 scripts/vltk-audit-equipment-stat-coverage.py`
- `python3 scripts/vltk-audit-equipment-quality-coverage.py`
- `python3 scripts/vltk-audit-equipment-seed-coverage.py`
- `npm run typecheck`
- `npm run test:pbt`
- `npm run check:no-runtime-vhcnd`
- A symlink scan over runtime asset folders before any visual story closes.

## Planning Handoff

Planning has stopped at the approval gate with an epic map and current-story candidate. After human approval, planning recommends moving to `khuym:validating` for S1/S2/S3 feasibility only. Do not create execution beads until validation proves the source/table/slot/catalog path and updates the proof commands. Future visual/UI/formula stories stay queued, not bead-created, until their prerequisites are validated.


## S7 Planning Addendum — Equip Condition Parity

**Date:** 2026-05-20  
**Current story:** `history/full-equipment-system-port/current-story-pack-s7.md`  
**Why now:** S6 made catalog magic keys source-backed and exposed unsupported stat semantics. The next safest E2 slice is equip-condition parity because runtime equip/unequip must fail or pass exactly like VHCND before deeper stat-vector and UI stories can be trusted.

### S7 Reality Basis

- VHCND `KItemList::CanEquip` checks slot fit before looping all requirement rows.
- VHCND `EnoughAttrib` handles level, strength, dexterity, vitality, energy, faction, series, sex, prohibited faction/series, learned skill, reborn count, city-owner, bangzhu, and companion-slot requirements.
- H5 currently implements the common level/stat/faction/series/sex branches only. Missing branches need either state-backed implementation or explicit fail-closed unsupported status.

### S7 Validation Questions

1. Which requirement keys actually appear in the current generated catalog, and how many rows/items use each?
2. Does the current seed inventory include every reachable requirement key without fabricating rows?
3. Can unsupported VHCND branches be safely fail-closed without breaking existing smoke loadouts?
4. Do tests cover candidate-self-satisfying stat requirements, slot mismatch, dual-ring slots, and unsupported requirement messages?

### Planning Handoff

Planning has prepared only S7. No execution beads have been created. Next skill: `khuym:validating` for S7 feasibility and proof commands.


## S8 Planning Addendum — Stat Vector Fixtures and Internal Magic Damage

**Date:** 2026-05-20  
**Current story:** `history/full-equipment-system-port/current-story-pack-s8.md`  
**Why now:** S8 depends on S6 magic-key visibility and S7 equip-condition parity. The largest remaining source-backed numeric combat group is internal magic damage (`internal-magic-damage-story-s8`, 355 catalog rows), so implementing it gives measurable parity progress before broader unsupported systems.

### S8 Reality Basis

- H5 already computes many PC-backed fields: base stats, vitality/energy HP/mana, weapon damage, external elemental flats, resists, attack rating, and physical damage buckets.
- VHCND `KNpcAttribModify.cpp` has explicit additive handlers for internal physical/fire/cold/lightning/poison magic damage using `nValue[0]` for positive rows.
- Generated S6 audit proves those keys are source enum-backed but unsupported; after S7D, `magic_item_nouser` is no longer part of S8.

### S8 Validation Questions

1. Do all catalog rows for the six internal-magic keys carry deterministic non-negative values that can be mapped without RNG?
2. Which `CharacterStats` field names should represent internal magic scalar/min/max values without colliding with external `fireDamage/coldDamage/...` skill additive fields?
3. Can fixture tests cite generated catalog rows and source formulas strongly enough to prove stat-vector parity for this slice?
4. Does changing `CharacterStats` affect UI/run-start snapshot serialization or property tests beyond expected new fields?

### Planning Handoff

Planning has prepared only S8. No execution beads have been created. Next skill: `khuym:validating` for S8 feasibility and proof commands.
