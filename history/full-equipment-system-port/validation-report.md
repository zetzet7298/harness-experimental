# Validation Report — S1/S2/S3 Catalog + Slot Taxonomy Foundation

**Feature:** full-equipment-system-port  
**Mode:** `high_risk_feature`  
**Current work:** S1/S2/S3 feasibility — catalog + slot taxonomy foundation  
**Date:** 2026-05-20  
**Decision:** `READY WITH CONSTRAINTS — RETURN TO PLANNING FOR CURRENT-STORY BEADS`

## Input Check

| Required input | Evidence | Result |
| --- | --- | --- |
| Context | `history/full-equipment-system-port/CONTEXT.md` | PASS |
| Xia research brief | `history/full-equipment-system-port/research-brief.md` | PASS |
| Approved work shape | User invoked `$khuym:validating` after `approach.md` approval request; `.khuym/state.json` now marks `work_shape=true` | PASS |
| Approach / epic map | `history/full-equipment-system-port/approach.md` | PASS |
| Current-work artifact | `history/full-equipment-system-port/current-story-pack.md` | PASS |
| Beads | `bv --robot-triage` and `br ready --json` report 0 open/actionable beads | MISSING AFTER READY |

## Reality Gate Report

```text
REALITY GATE REPORT
Mode: high_risk_feature
Current work: catalog + slot taxonomy foundation for full VHCND equipment port.
MODE FIT: PASS
REPO FIT: PASS
ASSUMPTIONS: PASS WITH CONSTRAINTS
SMALLER PATH: PASS
PROOF SURFACE: PASS
Decision: proceed to current-story beads after planning creates them; no execution yet.
```

### Evidence

- `Local`: H5 implementation seams exist in `/var/www/vltk-h5-survivors/game-source/src/domain/types.ts`, `src/domain/equipment.ts`, `src/domain/equipmentStore.ts`, `src/data/equipmentCatalog.json`, `scripts/vltk-normalize-equipment-index.py`, `scripts/vltk-build-equipment-seed.py`, and property tests.
- `Local`: Current `EquipmentSlot` is 11 slots only: `head/body/belt/weapon/foot/cuff/amulet/ring1/ring2/pendant/horse`.
- `Local`: Existing `equipmentCatalog.json` has 1231 items and 0 default entries for `mask`, `pifeng`, `yinjian`, `shiping`.
- `Local`: VHCND tables exist under `/var/www/vhcnd/sources/ServerNew/_bin_v2_/gs/Settings/item/004/`: `Mask.txt`, `PiFeng.txt`, `YinJian.txt`, `ShiPin.txt`, `GoldItem.txt`, `GoldMagic.txt`, `magicattrib.txt`.
- `Local`: VHCND `GameDataDef.h:134` defines `MAX_RESIST 150`; current H5 `src/domain/equipment.ts` still hardcodes `PC_MAX_RESIST = 95`, so formula parity remains a later constrained story.
- `Command`: `npm run typecheck` passed.
- `Command`: `npm run test:pbt` passed — 17 files / 224 tests.
- `Command`: `npm run check:no-runtime-vhcnd` passed for `src/`.
- `Command`: symlink scan found 0 symlinks under `public`, `src/data`, and `data/vltk-normalized`.
- `Command`: current normalizer dry-run against ServerNew Settings wrote `/tmp/full-equipment-validation-equipment-index.json` with 754 items from currently-supported tables; it did not include extended tables, proving the gap is real but bounded.

## Feasibility Matrix

| Part / Assumption | Risk | Proof Required | Evidence | Result |
| --- | --- | --- | --- | --- |
| Normalizer can be extended to parse `Mask/PiFeng/YinJian/ShiPin` without full rewrite | HIGH | Existing tables have tabular rows compatible enough for parser extension; current script gap is bounded | Table probe: `Mask.txt` 967 rows/51 cols, `PiFeng.txt` 15 rows/53 cols, `YinJian.txt` 14 rows/53 cols, `ShiPin.txt` 261 rows/45 cols. Current `TABLES` lacks those paths. | READY WITH CONSTRAINTS |
| Slot taxonomy can expand safely | HIGH | Identify slot declarations/order/sanitize/snapshot seams and tests | `types.ts` slot union, `equipment.ts` `EQUIPMENT_SLOT_ORDER`, `equipmentStore.ts`, `buildInventorySnapshot`, and PBT suite exist. Tests currently pass for 11 slots only. | READY WITH CONSTRAINTS |
| Source table inventory is reachable | HIGH | Concrete source paths exist and are readable | `srcwalk files` confirmed all required table filenames in VHCND `item/004`. | READY |
| Current catalog gap is real | HIGH | Current catalog has no extended slot rows | Python catalog probe: 1231 items; extended default counts all 0. | READY |
| `MAX_RESIST` discrepancy can be isolated from this story | HIGH | Exact evidence and constraint | VHCND client `GameDataDef.h:134` says `MAX_RESIST 150`; H5 formula audit still passes current markers for `95`. Formula parity beads must not be mixed into S1/S2/S3 except to document/block later work. | READY WITH CONSTRAINTS |
| Seed/test workflow is extensible | MEDIUM | Existing seed builder/audit prove current coverage and cap behavior | `vltk-audit-equipment-seed-coverage.py` passed for current 125-item seed and 11-slot expected set. New slots require updating expected slot list and possibly test catalog/filter policy. | READY WITH CONSTRAINTS |
| Isolation guard is present | HIGH | No runtime VHCND references/symlinks in current runtime surfaces | `npm run check:no-runtime-vhcnd` passed; symlink scan found 0 symlinks in runtime/data roots. | READY |
| Beads exist for execution | HIGH | `bv`/`br` show current-story tasks | `bv --robot-triage` open/actionable=0; `br ready --json` = `[]`. | NOT READY FOR SWARMING |

## Validation Questions Answered

1. **Can the normalizer read the four extended VHCND tables and produce rows with stable slots/qualities?**  
   **Answer:** feasible but not implemented. Current `TABLES` only covers weapon/body/head/foot/belt/amulet/ring/cuff/pendant/horse/gold. Extended source tables are present and parseable as tabular data, so create bounded normalizer beads for `mask`, `pifeng`, `yinjian`, `shiping`.

2. **Which `MAX_RESIST` value is authoritative now?**  
   **Answer:** current VHCND evidence inspected during validation is `MAX_RESIST 150` in `/var/www/vhcnd/sources/Client/Classes/gamecore/GameDataDef.h:134`. The existing H5 `PC_MAX_RESIST = 95` is a known contradiction. This blocks formula-parity execution, not the catalog/slot foundation, if S1/S2/S3 explicitly avoids formula changes except recording the constraint.

3. **Do existing tests/audits cover every new slot and option key?**  
   **Answer:** no. Existing typecheck/PBT/audits pass for the current 11-slot catalog. Current-story beads must update slot expectations, catalog coverage audits, seed coverage expectations, and persistence/snapshot tests for the extended slots.

4. **Can seed/test workflow expose every equipment slot without a 1000+ item normal bag?**  
   **Answer:** feasible with constraints. Existing greedy seed builder supports coverage bins and 125-item cap. New slots require extending expected slot bins and possibly adding a catalog/test browser or filters later; the S1/S2/S3 slice must at least seed representative items for every new slot.

## Integration Readiness

**PASS WITH CONSTRAINTS**

- The catalog/slot slice can be implemented without UI redesign or visual batch porting.
- `ring1/ring2` dual-slot behavior must be preserved when slot order expands.
- Formula parity and visual parity remain queued epics and must not be silently mixed into this foundation slice.
- The direct runtime isolation guard is already present, but execution must add/reference a symlink scan in validation docs or scripts before visual work closes.

## Current Story Readiness

**PASS WITH CONSTRAINTS**

The current-story exit is executable and testable, but swarming is blocked until current-story beads are created and reviewed.

Required bead themes for planning prep:

1. **Table inventory + normalizer extension** — add `Mask/PiFeng/YinJian/ShiPin` and source provenance.
2. **Slot taxonomy + persistence/snapshot tests** — expand `EquipmentSlot`, labels, `EQUIPMENT_SLOT_ORDER`, sanitize/default snapshot behavior.
3. **Seed/audit updates** — include extended slots in seed coverage, catalog quality/stat/label coverage, one-cell policy.
4. **Isolation/reference verification** — keep `check:no-runtime-vhcnd`, no symlink, no old-source-name regression in touched docs/scripts/code.

## Bead Review

Not possible yet: there are no open/current beads. Per `khuym:validating`, after `READY WITH CONSTRAINTS` and missing beads, route back to planning to create only current-story/work beads, then resume validation for bead review and execution approval.

## Final Gate

```text
VALIDATION COMPLETE - BEADS REQUIRED BEFORE EXECUTION
Mode: high_risk_feature
Work: S1/S2/S3 catalog + slot taxonomy foundation
Reality gate: PASS
Feasibility: READY WITH CONSTRAINTS
Structure: PASS after 1 iteration
Spikes: none required before bead creation
Integration readiness: PASS WITH CONSTRAINTS
Bead review: blocked — no current-story beads exist
Current story/work readiness: PASS WITH CONSTRAINTS
Unresolved concerns: MAX_RESIST formula contradiction is deferred/blocked for formula story; current normalizer lacks extended tables; tests/audits cover current 11 slots only.
Next action: return to khuym:planning to create current-story beads only, then resume khuym:validating for bead review and execution approval.
```

## Bead Repair And Review Addendum

After the initial validation report, the missing-beads blocker was repaired by creating current-story beads only:

| Bead | Scope | Dependency status | Review verdict |
| --- | --- | --- | --- |
| `mig-tka` | S1 inventory VHCND extended equipment tables | Ready first | PASS |
| `mig-8zw` | S2 expand H5 equipment slot taxonomy | Depends on `mig-tka` | PASS |
| `mig-v8f` | S3 update seed and coverage audits for extended slots | Depends on `mig-tka`, `mig-8zw` | PASS |
| `mig-ntg` | S4 isolation and validation chain for equipment foundation | Depends on `mig-tka`, `mig-8zw`, `mig-v8f` | PASS |

### Bead Review Report

```text
BEAD REVIEW REPORT
Work: S1/S2/S3 catalog + slot taxonomy foundation
Beads reviewed: 4
CRITICAL FLAGS: none
MINOR FLAGS: bv suggested extra labels/priority reductions; not required for execution because all four are high-risk current-story P1 tasks and dependencies now express the actual order.
CLEAN BEADS: mig-tka, mig-8zw, mig-v8f, mig-ntg
REVISIONS MADE: added dependencies so only mig-tka is initially ready; S2 waits on S1, S3 waits on S1/S2, S4 waits on S1/S2/S3.
SUMMARY: Current-story beads are scoped to the validated slice and exclude future visual/UI/formula work. `bv --robot-plan` shows one actionable first bead (`mig-tka`) and three blocked downstream beads, matching the intended execution order.
```

### Final Validation Gate After Bead Repair

```text
VALIDATION COMPLETE - APPROVAL REQUIRED BEFORE EXECUTION
Mode: high_risk_feature
Work: S1/S2/S3 catalog + slot taxonomy foundation
Current story: Current Story Pack — S1/S2/S3 Feasibility
Reality gate: PASS
Feasibility: READY WITH CONSTRAINTS
Structure: PASS after 2 iterations
Spikes: none required before execution
Integration readiness: PASS WITH CONSTRAINTS
Bead review: done
Current story/work readiness: PASS WITH CONSTRAINTS
Unresolved concerns: formula MAX_RESIST contradiction is deferred out of this slice; extended table support is work to execute; visual/UI/formula epics remain queued.
  Approve execution for this work only? (yes/no)
  ```

## Execution Addendum — bead `mig-tka` (2026-05-20)

- Normalizer `scripts/vltk-normalize-equipment-index.py` now includes active extended equipment tables: `Mask.txt`, `PiFeng.txt`, `YinJian.txt`, `ShiPin.txt`.
- Added deterministic table inventory summary (`summary.activeTableInventory`) with provenance fields: `source.path`, `source.encoding`, `source.line`, `rows`, and `provenanceRange.firstLine/lastLine`.
- Added table-path fallback from `item/<name>.txt` to `item/004/<name>.txt` so VHCND `gs/Settings` source is auditable without runtime coupling.
- Extended detail slot mapping to include: `11->mask`, `12->pifeng`, `13->yinjian`, `14->shiping`.
- Dry-run verification confirms extended kinds and provenance in output index:
  - `mask` → `Client/Settings/item/004/Mask.txt`
  - `pifeng` → `Client/Settings/item/004/PiFeng.txt`
  - `yinjian` → `Client/Settings/item/004/YinJian.txt`
  - `shiping` → `Client/Settings/item/004/ShiPin.txt`

## Execution Addendum — bead `mig-ntg` (2026-05-20)

Validation chain executed from `/var/www/vltk-h5-survivors/game-source`:

1. `python3 scripts/vltk-normalize-equipment-index.py --settings-dir /var/www/vhcnd/sources/ServerNew/_bin_v2_/gs/Settings` ✅ (`items=7972`)
2. `python3 scripts/vltk-build-equipment-seed.py` ✅ (`equipmentCatalog items=9552`, `inventory equipped=15`)
3. `python3 scripts/vltk-audit-equipment-stat-coverage.py` ✅ (`status=pass`)
4. `python3 scripts/vltk-audit-equipment-quality-coverage.py --require-complete` ✅ (`completeForUserMentionedQualitySet=true`)
5. `python3 scripts/vltk-audit-equipment-seed-coverage.py` ✅ (`status=pass`, `failures=[]`)
6. `npm run typecheck` ✅
7. `npm run test:pbt` ✅ (`17 files`, `224 tests`)
8. `npm run check:no-runtime-vhcnd` ✅ (`OK: no runtime references to /var/www/vhcnd under src/`)
9. Symlink scan (`find public src data/vltk-normalized -type l -print`) ✅ (no symlink)
10. old-source-name regression scan on touched docs/scripts/code ✅ (no old source-name token match in touched file `history/full-equipment-system-port/validation-report.md`)

Notes:
- Runtime isolation rule remains intact: build/audit scripts may read VHCND source, runtime `src/` has no `/var/www/vhcnd` reference.
- MAX_RESIST formula conflict remains deferred and out of scope for bead `mig-ntg`.



## Review Fix Addendum — 2026-05-20

During `khuym:reviewing`, acceptance gaps were found and fixed:

- New `scripts/vltk-audit-equipment-table-inventory.py` verifies active source-table inventory for all required S1 tables, including `GoldMagic.txt` and `magicattrib.txt`.
- `scripts/vltk-audit-equipment-stat-coverage.py` and `scripts/vltk-audit-equipment-series-coverage.py` now cover all 15 H5 equipment slots, not just the original 11 PC base slots.
- `EquipmentScene` exports `EQUIPMENT_SLOT_LAYOUT`; the property test now asserts every slot button/caption stays in the paper-doll bounds and disjoint from the bag panel.
- Runtime isolation is now a reusable package gate (`npm run check:runtime-isolation`) and is wired into `prebuild`; it scans `src/` and `public/` for `/var/www/vhcnd` literals and symlinks.

Post-fix validation passed: normalizer, seed build, table/stat/series/quality/seed audits, `npm run test:pbt` (225 tests), `npm run typecheck`, `npm run check:runtime-isolation`, and `npm run build`.
