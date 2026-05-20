# E2R Gate Decision Packet (mig-ja5)

Generated (UTC): `2026-05-19T15:41:59.033810+00:00`

## Current state

- `E2R_GATE status=blocked selected=49/149 remaining=100 completion=32.89% delta_selected=0 delta_remaining=0`
- map issues: **0**

## Option A — Canonical first

- Mục tiêu: chỉ mở gate khi canonical mapping hoàn tất 100%.
- Kỳ vọng: `ready-canonical`

Commands:
```bash
Hoàn tất selected_vhcnd_line cho 100 dòng còn lại trong e2r-golditem-manual-map-template.csv
python3 history/migrate-vhcnd-to-vhcnd/spike-scripts/e2r-golditem-manual-map-validate.py
python3 history/migrate-vhcnd-to-vhcnd/spike-scripts/e2r-ops-one-shot.py
```

## Option B — Provisional accept

- Mục tiêu: mở gate nhanh theo nhánh provisional đã sạch lỗi selected mapping.
- Kỳ vọng: `ready-provisional-approved`

Commands:
```bash
python3 history/migrate-vhcnd-to-vhcnd/spike-scripts/e2r-run-option-b.py --accept-provisional --decided-by "<human>"
python3 history/migrate-vhcnd-to-vhcnd/spike-scripts/e2r-close-mig-ja5.py --confirm --reason "Provisional accepted by human" --append-verdict-note
```

## Operator note

- Technical blocker hiện tại đã giảm còn quyết định human (accept_provisional).
- Sau khi gate chuyển ready, dùng safe-close script để đóng bead mig-ja5.
