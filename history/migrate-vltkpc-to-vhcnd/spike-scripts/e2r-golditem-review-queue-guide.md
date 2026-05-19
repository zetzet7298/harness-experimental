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
