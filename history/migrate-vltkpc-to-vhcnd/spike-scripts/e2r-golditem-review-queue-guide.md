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
- Apply + verify chain (validate + one-shot):
  - `python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-golditem-apply-repair-proposals.py --apply --verify`
- Báo cáo thay đổi:
  - `e2r-golditem-apply-repair-report.json`


## Preview impact (không đụng canonical)
- Chạy mô phỏng áp repair proposals trên template preview:
  - `python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-preview-repair-impact.py`
- Artifacts:
  - `e2r-golditem-manual-map-template.preview.csv`
  - `e2r-preview-repair-impact.json`
  - `e2r-preview-repair-impact.md`

- Backup canonical sẽ được tạo tự động khi `--apply`:
  - thư mục `e2r-golditem-manual-map-backups/`


## Gate forecast theo kịch bản
- Chạy forecast:
  - `python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-gate-forecast.py`
- Output:
  - `e2r-gate-forecast.md`
  - `e2r-gate-forecast.json`


## Gate decision packet (A/B)
- `e2r-gate-decision-packet.md`
- `e2r-gate-decision-packet.json`

Packet này tóm tắt 2 nhánh quyết định cuối kèm lệnh thực thi từng bước.


## Runbook scripts theo Option A/B
- Option A (canonical-first check run):
  - `python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-run-option-a.py`
  - report: `e2r-run-option-a-report.json`

- Option B (provisional path execution):
  - `python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-run-option-b.py`
  - Để bật cờ provisional accept ngay trong runbook:
    - `python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-run-option-b.py --accept-provisional --decided-by "<human>"`
  - report: `e2r-run-option-b-report.json`


## Safe-close script cho mig-ja5
- Precheck (không close):
  - `python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-close-mig-ja5.py`
- Close thật (chỉ chạy khi gate ready):
  - `python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-close-mig-ja5.py --confirm --reason "<reason>"`
- Close + ghi addendum vào verdict:
  - `python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-close-mig-ja5.py --confirm --reason "<reason>" --append-verdict-note`
- Report:
  - `e2r-close-mig-ja5-report.json`


## Finalize provisional (guarded)
- Precheck (không có approve sẽ không làm gì):
  - `python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-finalize-provisional.py`
- Finalize thật (cần human explicit):
  - `python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-finalize-provisional.py --human-approved --decided-by "<human>" --reason "<reason>"`
- Report:
  - `e2r-finalize-provisional-report.json`


## Control dashboard (1-file view)
- Refresh dashboard:
  - `python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-control-dashboard.py`
- Output:
  - `e2r-control-dashboard.md`
  - `e2r-control-dashboard.json`


## Finalize preflight
- Chạy preflight trước khi finalize:
  - `python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-finalize-preflight.py`
- Output:
  - `e2r-finalize-preflight.md`
  - `e2r-finalize-preflight.json`


## Auto-generate next step
- Chạy generator:
  - `python3 history/migrate-vltkpc-to-vhcnd/spike-scripts/e2r-generate-next-step.py`
- Output:
  - `e2r-next-step.md`
  - `e2r-next-step.json`
