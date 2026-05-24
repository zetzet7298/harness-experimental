---
name: translate-game
description: "Chạy workflow end-to-end cho gpttranslator/translate-game: audit an toàn source tải về, self-host server + 9router, debug lỗi runtime (Express/Mongo/auth/model), và test dịch không phá source bằng workspace tạm. Luôn dùng skill này khi user muốn review tool dịch game, triển khai local/VPS, hoặc xác thực kết quả dịch trên nhiều thư mục."
---

## Mục tiêu skill
Chuẩn hóa quy trình vận hành `gpttranslator` từ lúc nhận source tải về đến lúc dịch thử thành công và báo cáo output, với ưu tiên:
1. An toàn (không lộ secret, không chạy mù).
2. Tái lập được (có smoke test và test không chạm source).
3. Debug được (ghi rõ lỗi và hướng xử lý).

## Khi nào phải dùng skill này
Dùng ngay khi user yêu cầu một trong các việc sau:
- Review độ an toàn của tool dịch game tải từ internet.
- Move/deploy tool dịch vào repo để chạy local hoặc VPS.
- Cấu hình upstream 9router/API key/model cho server proxy.
- Sửa lỗi pipeline dịch (Express/Mongo/auth/model/dependency).
- Test dịch trên nhiều folder game mà không được sửa file gốc.

## Nguyên tắc bắt buộc
- Không commit hoặc in ra secret (API key, JWT, mật khẩu DB, SSH key).
- Không dịch hoặc phá vỡ `ID`, `key`, placeholder (`{0}`, `%s`, `${var}`), URL, timestamp, định dạng cấu hình.
- Luôn tách `input` và `output`; mặc định test trên workspace tạm.
- Trước khi kết luận “OK”, phải có bằng chứng chạy test thực tế.

## Quy trình chuẩn

### Bước 1: Thu thập input tối thiểu
Lấy đủ các thông tin trước khi thao tác:
- Source tool ở đâu (zip/folder/path).
- Mục tiêu chạy local hay self-host.
- Upstream endpoint/model mong muốn.
- Phạm vi test (folder/file nào cần kiểm chứng).

Nếu thiếu thông tin bắt buộc, hỏi rõ và chỉ hỏi phần còn thiếu.

### Bước 2: Audit source trước khi chạy
Audit tĩnh trước, chưa vội start:
- `package.json`, `src/cli.*`, `server/*`, `.env*`.
- Tìm pattern nguy hiểm: thực thi lệnh hệ thống không kiểm soát, download-run script, exfil dữ liệu, hardcode secret.
- Kết luận theo mức: **không thấy dấu hiệu mã độc rõ ràng** vs **còn rủi ro vận hành**.

Mẫu kết luận cần nêu:
1. Điểm an toàn đã xác thực.
2. Rủi ro còn lại (thường là upload file lên server/upstream).
3. Điều kiện để chạy an toàn hơn.

### Bước 3: Setup local/self-host
Thực hiện cài đặt theo checklist:
1. Giải nén/copy source vào vị trí user yêu cầu.
2. Cài dependency cho cả root CLI và server.
3. Cấu hình `server/.env` (PORT, MONGODB_URI, JWT_SECRET, UPSTREAM_*).
4. Nếu dùng 9router, map đúng `UPSTREAM_BASE_URL`, `UPSTREAM_API_KEY`, `UPSTREAM_MODEL`.

Lệnh mẫu dùng trong `references/commands.md`.

### Bước 4: Bring-up và health check
- Start server nền.
- Kiểm tra process + cổng + `/health`.
- Nếu fail, xử lý theo `references/troubleshooting.md` trước khi sang bước tiếp.

### Bước 5: Smoke test end-to-end
Luồng tối thiểu phải chạy được:
1. Register user test.
2. Lấy CLI key.
3. `gpttranslator login`.
4. Gọi `/v1/models` hoặc endpoint tương đương để xác nhận upstream/model.
5. Gọi `/api/cli/translate` trên input mẫu nhỏ.

Nếu có lỗi, giữ vòng lặp debug tới khi ra nguyên nhân gốc, không dừng ở workaround mơ hồ.

### Bước 6: Test không phá source theo từng folder
Khi user yêu cầu test an toàn:
1. Tạo workspace tạm (`/tmp/...`).
2. Copy mẫu đại diện từng folder vào `input`.
3. Chạy dịch vào `output` tách riêng.
4. Xác nhận file output được tạo và source gốc không đổi.
5. Trả lại path output đầy đủ cho user kiểm.

### Bước 7: Báo cáo kết quả
Báo ngắn gọn, có bằng chứng:
- Trạng thái server.
- Model/upstream đang chạy.
- Kết quả smoke test.
- Kết quả test folder-by-folder.
- Đường dẫn output cuối cùng.
- Vấn đề còn mở (nếu có) + bước tiếp theo đề xuất.

## Done criteria (không đạt thì chưa kết thúc)
- Server sống và trả health thành công.
- Luồng login + translate chạy thành công ít nhất 1 mẫu thật.
- Test không phá source có output kiểm chứng được.
- Không để lộ secret trong log/phản hồi.

## Tài liệu tham chiếu
- `references/commands.md`: bộ lệnh chuẩn theo workflow.
- `references/troubleshooting.md`: lỗi thực chiến + cách xử lý nhanh.
