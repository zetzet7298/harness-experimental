# E2R Decision Simulation (Preview Only)

Generated (UTC): `2026-05-19T16:15:59.311184+00:00`

| Path | apply | gate_status | bead_closed | audit |
|---|:---:|---|:---:|---|
| provisional | False | blocked | False | incomplete |
| canonical | False | blocked | False | incomplete |

Kết quả preview cho thấy cả hai nhánh chưa thay đổi trạng thái vì chưa `--apply` (đúng guard).

## Apply commands
```bash
python3 history/migrate-vhcnd-to-vhcnd/spike-scripts/e2r-approve-and-finalize.py --decided-by "<human>" --mode accept-provisional --note "Provisional accepted by human" --apply
```
```bash
python3 history/migrate-vhcnd-to-vhcnd/spike-scripts/e2r-approve-and-finalize.py --decided-by "<human>" --mode canonical-first --note "Canonical completion required" --apply
```
