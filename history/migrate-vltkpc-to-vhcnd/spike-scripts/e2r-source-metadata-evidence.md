# E2R Source Metadata Evidence - VHCND Probe

## Executive Summary
- **Target Source:** `/var/www/vhcnd/sources/ServerNew/_bin_v2_/gs/Settings/item/004/`
- **GoldItem Decision:** **[BLOCKED]**
- **Reason:** Deterministic remap by `(Name, ItemGenre, DetailType, ParticularType, SpritePath)` is impossible. Many items share identical identification keys but have different magic attributes (e.g., Timed vs. Permanent vs. Quest versions). In `GoldItem.txt`, 923 keys point to multiple different rows.

## File Inventory (vhcnd/item/004)

| File | Total Rows | Unique Keys* | Ambiguous Rows | Remap Status |
| :--- | ---: | ---: | ---: | :--- |
| `GoldItem.txt` | 5945 | 723 | 5222 | **BLOCKED** |
| `amulet.txt` | 20 | 20 | 0 | FEASIBLE |
| `armor.txt` | 290 | 250 | 40 | FEASIBLE |
| `belt.txt` | 20 | 20 | 0 | FEASIBLE |
| `boot.txt` | 40 | 20 | 20 | FEASIBLE |
| `cuff.txt` | 20 | 20 | 0 | FEASIBLE |
| `helm.txt` | 141 | 119 | 22 | FEASIBLE |
| `horse.txt` | 321 | 37 | 284 | FEASIBLE** |
| `meleeweapon.txt` | 70 | 52 | 18 | FEASIBLE |
| `pendant.txt` | 20 | 20 | 0 | FEASIBLE |
| `rangeweapon.txt` | 30 | 12 | 18 | FEASIBLE |
| `ring.txt` | 10 | 10 | 0 | FEASIBLE |

*\*Unique Keys defined as (ItemGenre, DetailType, ParticularType, SpritePath).*
*\*\*Horse ambiguity is high due to many "Hoàng Mã" / "Chiếu Dạ" variations with same sprite and genre/detail.*

## GoldItem Ambiguity Samples

| Key (Genre, Detail, Part, Sprite) | Matches in VHCND | Sample Names |
| :--- | :--- | :--- |
| `0, 7, 0, \spr\item\equip\cap\obj-ma-cap03-3.spr` | 5+ | Minh Long Chỉnh Hồng Tương Mạo, [Định thời] Minh Long... |
| `0, 4, 0, \Spr\item\equip\nick\obj-neck07.spr` | 3+ | An Bang Băng Tinh Thạch Hạng Liên |

## Decision Detail: [BLOCKED]
The VHCND source for `GoldItem.txt` is significantly expanded compared to legacy sources, containing thousands of item variations. Remapping existing H5 catalog items to these new rows using only standard identity keys (Name, Genre, Detail, Particular, Sprite) yields many-to-one or many-to-many results. Without a byte-identical magic attribute check or a hard-coded line mapping (which is fragile), the transition to VHCND as a source of truth for Gold items will break item stat consistency.

## Handoff / Next Steps
- E_M2R implementation must either:
    1. Implement a stat-matching algorithm to find the correct VHCND row.
    2. Request a manual "Source Line" map from the developer for the 171 critical Gold items.
    3. Block E_M3 until GoldItem provenance is resolved.


## 2026-05-19 Provisional Gold remap unblock

- Applied provisional Gold manual map from `e2r-golditem-manual-map-template.csv` after auto-filling 49 suggested rows.
- Updated `game-source/src/data/equipmentCatalog.json`:
  - `171/171` Gold items now use `ServerNew/_bin_v2_/gs/Settings/item/004/GoldItem.txt`.
  - `49` Gold items received provisional `source.line` from `selected_vhcnd_line`.
  - Remaining Gold rows keep prior line index pending human canonical review.
- Validation checks:
  - `python3 -m py_compile scripts/vltk-audit-equipment-stat-coverage.py scripts/vltk-normalize-equipment-index.py` ✅
  - `vltk-audit-equipment-stat-coverage.py ... --vltkpc-root /var/www/vhcnd/sources` ✅ (`noFabricationCheck.status=pass`, `sourceLinesValid=1231/1231`).
  - Catalog now has `0` `Client/Settings/*` source paths and no `/var/www/vltkpc`/`/var/www/vltkunity` absolute source paths.

> Note: This is an unblock pass for swarming continuity. Final canonical Gold mapping still requires reviewer confirmation for non-suggested rows.


## 2026-05-19 Heuristic assist for remaining 100 Gold rows

To reduce manual review load for gate `mig-ja5`, generated:
- `history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-golditem-manual-map-heuristic-assist.csv`

Scope:
- Only rows still missing `selected_vhcnd_line` (100 rows).
- No template overwrite performed.

Heuristic currently emitted:
- Parse `H5_ID` old-line token and pick nearest candidate line in `candidate_vhcnd_lines`.
- Marked all recommendations as `low` confidence (assist-only, non-canonical).

Use:
1. Reviewer cross-checks each `recommended_line` in `GoldItem.txt`.
2. Copy confirmed values into `e2r-golditem-manual-map-template.csv`.
3. Re-run stat audit to confirm no-fabrication remains pass.


## 2026-05-19 Review queue batching for gate mig-ja5

Added queue artifacts to prioritize remaining canonical review:
- `e2r-golditem-review-queue.csv` (100 rows, sorted by review priority)
- `e2r-golditem-review-batch-easy.csv` (7 rows)
- `e2r-golditem-review-batch-medium.csv` (30 rows)
- `e2r-golditem-review-batch-hard.csv` (63 rows)
- `e2r-golditem-review-queue-guide.md`

These files are assist-only and do not mutate canonical mapping.


## 2026-05-19 Checklist pack for human canonical review

Added markdown checklist pack so reviewer can process queue in tracked batches:
- `e2r-golditem-review-checklist-master.md`
- `e2r-golditem-review-checklist-easy.md`
- `e2r-golditem-review-checklist-medium.md`
- `e2r-golditem-review-checklist-hard.md`

Master checklist includes canonical target reminder + stat-audit verify command.


## 2026-05-19 Progress snapshot automation

Added tracking script and generated baseline snapshot:
- `e2r-golditem-progress-snapshot.py`
- `e2r-golditem-progress-snapshot.md`
- `e2r-golditem-progress-snapshot.json`

Baseline at generation time:
- canonical selected rows: 49/149
- remaining rows: 100
- checklist ticks: easy 0/7, medium 0/30, hard 0/63


## 2026-05-19 Snapshot diff tracking

Progress snapshot automation upgraded with history + latest diff artifacts:
- `e2r-golditem-progress-history/snapshot-*.json`
- `e2r-golditem-progress-diff-latest.md`
- `e2r-golditem-progress-diff-latest.json`

This allows quick verification of reviewer movement between consecutive checks.


## 2026-05-19 Gate readiness automation

Added gate-check artifacts for `mig-ja5` close criteria:
- `e2r-gate-readiness-check.py`
- `e2r-gate-readiness.md`
- `e2r-gate-readiness.json`
- `e2r-gate-decision.json` (human-controlled provisional acceptance flag)

Current computed status: `blocked` (remaining Gold rows 100, provisional acceptance flag false).


## 2026-05-19 One-shot operator status

Added one-shot wrapper for swarming operator loop:
- `e2r-ops-one-shot.py`
- `e2r-ops-one-shot-summary.md`
- `e2r-ops-one-shot-summary.json`

Current one-line output:
`E2R_GATE status=blocked selected=49/149 remaining=100 completion=32.89% delta_selected=0 delta_remaining=0`


## 2026-05-19 Manual map validation artifact

Added manual-map validator to catch invalid canonical inputs early:
- `e2r-golditem-manual-map-validate.py`
- `e2r-golditem-manual-map-validate.md`
- `e2r-golditem-manual-map-validate.json`

Current baseline: `status=fail`, `issue_count=48` (mostly `not-in-candidate-list` on provisional selected rows).
Gate checker now surfaces this validation status for operator visibility.


## 2026-05-19 Candidate-safe repair proposals

Generated proposal set for 48 invalid selected lines (`not-in-candidate-list`):
- `e2r-golditem-selected-repair-proposals.csv`
- `e2r-golditem-selected-repair-proposals.md`
- `e2r-golditem-selected-repair-simulation.json`

Simulation result indicates proposal application would reduce validator issues from 48 to 0 without changing selected-row count.


## 2026-05-19 Repair apply helper

Added helper script to operationalize repair proposals:
- `e2r-golditem-apply-repair-proposals.py`
- `e2r-golditem-apply-repair-report.json`

Baseline dry-run result: `change_count=48` (no template mutation in dry-run mode).


## 2026-05-19 Preview repair impact

Added non-destructive preview impact script:
- `e2r-preview-repair-impact.py`
- `e2r-golditem-manual-map-template.preview.csv`
- `e2r-preview-repair-impact.json`
- `e2r-preview-repair-impact.md`

Latest preview result:
- applied changes in preview: 48
- canonical issues: 48
- preview issues: 0
- delta issues: -48


## 2026-05-19 Apply helper hardening

`e2r-golditem-apply-repair-proposals.py` now supports:
- automatic canonical backup on `--apply` (`e2r-golditem-manual-map-backups/`)
- optional post-apply verify chain via `--verify`:
  - run `e2r-golditem-manual-map-validate.py`
  - run `e2r-ops-one-shot.py`

This reduces operator risk when moving from proposal to canonical update.


## 2026-05-19 Gate forecast scenarios

Added scenario forecast artifact to help human decision speed:
- `e2r-gate-forecast.py`
- `e2r-gate-forecast.md`
- `e2r-gate-forecast.json`

Forecast highlights:
- current-state: blocked
- after-apply-proposals + provisional accept: ready-provisional-approved


## 2026-05-19 Decision packet for mig-ja5 close

Added structured decision packet to accelerate final gate choice:
- `e2r-gate-decision-packet.md`
- `e2r-gate-decision-packet.json`

Packet includes Option A (canonical-first) and Option B (provisional-accept) with expected gate status and command sequence.


## 2026-05-19 Option runbook scripts

Added executable runbooks aligned to decision packet:
- `e2r-run-option-a.py`
- `e2r-run-option-b.py`
- reports: `e2r-run-option-a-report.json`, `e2r-run-option-b-report.json`

Current Option A baseline run result: `gate_status=blocked`.


## 2026-05-19 Safe gate close automation

Added guarded close utility:
- `e2r-close-mig-ja5.py`
- `e2r-close-mig-ja5-report.json`

Behavior:
- never closes unless `gate_status` is ready (`ready-canonical` or `ready-provisional-approved`) AND `--confirm` is provided.
- optional verdict addendum write with `--append-verdict-note`.


## 2026-05-19 Option B technical prep executed

Executed `e2r-run-option-b.py` without provisional accept flag.

Resulting technical state:
- manual-map validator: `status=pass`, `issue_count=0`
- gate status remains `blocked` only because human provisional decision flag is still false
- decision packet refreshed to reflect new baseline (map issues now 0)


## 2026-05-19 Guarded provisional finalize runner

Added final-step runner with hard human-approval guard:
- `e2r-finalize-provisional.py`
- `e2r-finalize-provisional-report.json`

Baseline precheck run result:
- `result_status=blocked-missing-human-approval`
- `bead_closed=false`


## 2026-05-19 Control dashboard

Added consolidated control dashboard:
- `e2r-control-dashboard.py`
- `e2r-control-dashboard.md`
- `e2r-control-dashboard.json`

Current snapshot:
- gate_status=blocked
- map_issue_count=0
- remaining_rows=100
- accept_provisional=false

This confirms only human decision path remains for provisional opening.


## 2026-05-19 Swarming completion audit artifact

Added requirement-by-requirement completion audit:
- `e2r-swarming-completion-audit.json`
- `e2r-swarming-completion-audit.md`

Current audit result: `overall=incomplete`, blocked by:
- R3: bead close not executed yet
- R4: human provisional acceptance not set


## 2026-05-19 Finalize preflight artifact

Added preflight checker before running final close paths:
- `e2r-finalize-preflight.py`
- `e2r-finalize-preflight.md`
- `e2r-finalize-preflight.json`

Current preflight indicates technical readiness for provisional decision request, with human approval still required to finalize/close.


## 2026-05-19 Next-step generator

Added preflight-driven next-step generator:
- `e2r-generate-next-step.py`
- `e2r-next-step.md`
- `e2r-next-step.json`

Current generated label:
- `await-human-approval-then-finalize-provisional`


## 2026-05-19 Operator pulse artifact

Added consolidated operator pulse:
- `e2r-operator-pulse.py`
- `e2r-operator-pulse.md`
- `e2r-operator-pulse.json`

Current pulse next-step label:
- `await-human-approval-then-finalize-provisional`
