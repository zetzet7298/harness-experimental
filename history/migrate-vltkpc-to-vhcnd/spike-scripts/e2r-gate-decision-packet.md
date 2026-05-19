# E2R Gate Decision Packet (mig-ja5)

Generated (UTC): `2026-05-19T15:32:17.154940+00:00`

## Current state

- `E2R_GATE status=blocked selected=49/149 remaining=100 completion=32.89% delta_selected=0 delta_remaining=0`
- map issues: **48**

## Option A — Canonical first

- Mục tiêu: chỉ mở gate khi canonical mapping hoàn tất 100%.
- Kỳ vọng: `ready-canonical`

Commands:
```bash
Hoàn tất selected_vhcnd_line cho 100 dòng còn lại trong e2r-golditem-manual-map-template.csv
python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-golditem-manual-map-validate.py
python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-ops-one-shot.py
```

## Option B — Provisional accept

- Mục tiêu: mở gate nhanh theo nhánh provisional có kiểm soát.
- Kỳ vọng: `ready-provisional-approved`

Commands:
```bash
python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-golditem-apply-repair-proposals.py --apply --verify
Sửa e2r-gate-decision.json: accept_provisional_for_e_m3_to_e_m7=true + decided_by + decided_at
python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-gate-readiness-check.py
python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-ops-one-shot.py
```

## Operator note

- Option B yêu cầu quyết định human minh bạch trong `e2r-gate-decision.json`.
- Sau khi gate chuyển ready, cập nhật `e2r-verdict.md` addendum và đóng bead `mig-ja5`.
