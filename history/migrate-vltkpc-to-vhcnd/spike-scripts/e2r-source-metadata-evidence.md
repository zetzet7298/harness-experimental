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
