# E2R Finalize — Next Command

Current dashboard says only human decision remains.

## Nếu chấp nhận provisional (đề xuất nhanh)

```bash
cd /var/www/vltk-h5-survivors/harness-experimental
python3 history/migrate-vhcnd-to-vhcnd/spike-scripts/e2r-finalize-provisional.py --human-approved --decided-by "<human>" --reason "Provisional accepted by human"
python3 history/migrate-vhcnd-to-vhcnd/spike-scripts/e2r-control-dashboard.py
```

## Nếu không chấp nhận provisional

Tiếp tục điền canonical mapping tới 149/149 rồi chạy:

```bash
cd /var/www/vltk-h5-survivors/harness-experimental
python3 history/migrate-vhcnd-to-vhcnd/spike-scripts/e2r-run-option-a.py
python3 history/migrate-vhcnd-to-vhcnd/spike-scripts/e2r-close-mig-ja5.py --confirm --reason "Canonical mapping completed" --append-verdict-note
```
