# E2R GoldItem Selected-Line Repair Proposals

Mục tiêu: sửa nhanh các dòng đã chọn nhưng không nằm trong candidate list.

## Artifacts
- `e2r-golditem-selected-repair-proposals.csv` (48 dòng lỗi hiện tại)
- `e2r-golditem-selected-repair-simulation.json`

## Quy tắc đề xuất
- Với mỗi `H5_ID` đang lỗi `not-in-candidate-list`, chọn candidate gần nhất với `current_selected`.
- Không tự ghi đè file canonical template.

## Kết quả mô phỏng
- Trước sửa: validator báo 48 lỗi.
- Sau khi áp proposal (mô phỏng): `sim_issue_count = 0`.

## Cách dùng
1. Reviewer mở CSV proposal, kiểm tra từng dòng.
2. Copy `proposed_selected` vào `e2r-golditem-manual-map-template.csv` cho các dòng tương ứng.
3. Chạy lại:
   - `python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-golditem-manual-map-validate.py`
   - `python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-ops-one-shot.py`


## Operator command
- Dry-run: `python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-golditem-apply-repair-proposals.py`
- Apply: `python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-golditem-apply-repair-proposals.py --apply`

- Apply + verify: `python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-golditem-apply-repair-proposals.py --apply --verify`
