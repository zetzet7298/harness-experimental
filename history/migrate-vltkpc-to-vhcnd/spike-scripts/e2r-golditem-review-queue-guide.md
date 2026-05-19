# E2R GoldItem Review Queue Guide

Mục tiêu: tăng tốc review 100 dòng Gold còn thiếu `selected_vhcnd_line`.

## Files
- `e2r-golditem-review-queue.csv`: danh sách đầy đủ, đã sắp thứ tự ưu tiên.
- `e2r-golditem-review-batch-easy.csv` (7 dòng): ưu tiên xử lý trước.
- `e2r-golditem-review-batch-medium.csv` (30 dòng).
- `e2r-golditem-review-batch-hard.csv` (63 dòng).

## Cách dùng
1. Mở batch easy trước, đối chiếu trực tiếp với `GoldItem.txt` ở vhcnd.
2. Điền kết quả vào file canonical:
   - `e2r-golditem-manual-map-template.csv` (cột `selected_vhcnd_line`).
3. Khi hoàn tất các batch, chạy lại stat audit để xác nhận no-fabrication vẫn pass.

## Rule phân tier
- T1-easy: `candidate_count <= 2`
- T2-medium: `3 <= candidate_count <= 5`
- T3-hard: `candidate_count > 5`

> Queue này là artifact hỗ trợ review, không tự động cập nhật template canonical.


## Theo dõi tiến độ

- Xem diff so với snapshot trước:
  - `e2r-golditem-progress-diff-latest.md`
  - `e2r-golditem-progress-diff-latest.json`
- Lịch sử snapshot theo thời gian:
  - thư mục `e2r-golditem-progress-history/`
- Chạy snapshot:
  - `python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-golditem-progress-snapshot.py`
- Xem kết quả:
  - `e2r-golditem-progress-snapshot.md`
  - `e2r-golditem-progress-snapshot.json`


## Gate readiness check
- Chạy kiểm tra gate:
  - `python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-gate-readiness-check.py`
- Xem kết quả:
  - `e2r-gate-readiness.md`
  - `e2r-gate-readiness.json`
- File quyết định provisional (human-controlled):
  - `e2r-gate-decision.json`


## One-shot operator command
- Chạy toàn bộ vòng theo dõi (snapshot + gate check) và in 1 dòng trạng thái:
  - `python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-ops-one-shot.py`
- Output:
  - `e2r-ops-one-shot-summary.md`
  - `e2r-ops-one-shot-summary.json`


## Validate manual selections
- Kiểm tra các dòng đã điền `selected_vhcnd_line` có hợp lệ không:
  - `python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-golditem-manual-map-validate.py`
- Output:
  - `e2r-golditem-manual-map-validate.md`
  - `e2r-golditem-manual-map-validate.json`


## Repair proposals cho selected line lỗi
- `e2r-golditem-selected-repair-proposals.csv`
- `e2r-golditem-selected-repair-proposals.md`
- `e2r-golditem-selected-repair-simulation.json`

Dùng để xử lý nhanh các lỗi `not-in-candidate-list` trước khi đóng gate.


## Apply repair proposals (operator-safe)
- Dry-run (không sửa template):
  - `python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-golditem-apply-repair-proposals.py`
- Apply thật (ghi vào template):
  - `python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-golditem-apply-repair-proposals.py --apply`
- Báo cáo thay đổi:
  - `e2r-golditem-apply-repair-report.json`


## Preview impact (không đụng canonical)
- Chạy mô phỏng áp repair proposals trên template preview:
  - `python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-preview-repair-impact.py`
- Artifacts:
  - `e2r-golditem-manual-map-template.preview.csv`
  - `e2r-preview-repair-impact.json`
  - `e2r-preview-repair-impact.md`
