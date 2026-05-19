# GoldItem Manual Mapping Guide

## Context
The migration of Gold items (Hoàng Kim) from legacy H5 to VHCND cannot be fully automated due to catalog reorganization in VHCND.
- Algorithmic matching produced score ties for 149/171 items.
- VHCND contains multiple versions of the same item (Timed, Permanent, Enhanced) with identical base identification keys.

## Template Instructions
Please use `e2r-golditem-manual-map-template.csv` to provide the canonical mapping.

### Columns
1. **H5_ID**: The unique identifier in the current H5 game.
2. **candidate_vhcnd_lines**: A pipe-separated list of potential line indices from VHCND `GoldItem.txt`. Format: `LineIndex(ItemName)`.
3. **selected_vhcnd_line**: **(REQUIRED)** Enter the single chosen line index (integer) for the migration.
4. **reviewer_note**: (Optional) Add any notes regarding the choice or discrepancies.

### How to verify
- Open `/var/www/vhcnd/sources/ServerNew/_bin_v2_/gs/Settings/item/004/GoldItem.txt`.
- Use the line index (0-based, matching the candidate list) to inspect full stats, requirements, and set associations.
- The `selected_vhcnd_line` must exist in `GoldItem.txt`.

## Submission
Save the completed CSV and return it to the Codex agent to proceed with the `E_M2R` implementation phase.
