# E2R Ready For Human Approval (mig-ja5)

Trạng thái kỹ thuật hiện tại:
- map validator: pass (issue_count=0)
- gate: blocked
- bead: mig-ja5 in_progress
- completion audit blockers: R3 (chưa close bead), R4 (chưa có quyết định human)

## Nhánh khuyến nghị (provisional)
Chạy đúng 1 lệnh:

```bash
cd /var/www/vltk-h5-survivors/harness-experimental
python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-approve-and-finalize.py   --decided-by "<human>"   --mode accept-provisional   --note "Provisional accepted by human"   --apply
```

## Nhánh thay thế (canonical)
Nếu không chấp nhận provisional:
1. Hoàn tất canonical mapping 149/149.
2. Chạy:

```bash
cd /var/www/vltk-h5-survivors/harness-experimental
python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-approve-and-finalize.py   --decided-by "<human>"   --mode canonical-first   --note "Canonical completion required"   --apply
```


## One-command execution after approval

```bash
E2R_DECIDED_BY="<human>" E2R_MODE="accept-provisional" E2R_NOTE="Provisional accepted by human" bash history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-run-on-approval.sh
```


## Print command helper (avoid typo)

```bash
python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-print-approval-command.py   --decided-by "<human>"   --mode accept-provisional   --note "Provisional accepted by human"
```
