# Troubleshooting (thực chiến)

## 1) Express route wildcard lỗi khi boot server
- **Triệu chứng**: `PathError: Missing parameter name at index ... /v1/*`
- **Nguyên nhân thường gặp**: đang dùng Express 5, route cũ viết theo Express 4.
- **Kiểm tra nhanh**:
  ```bash
  npm ls express
  ```
- **Cách xử lý**:
  ```bash
  npm install express@4
  ```

## 2) Cổng bị chiếm (`EADDRINUSE`)
- **Triệu chứng**: server không start, báo `listen EADDRINUSE :7770`.
- **Kiểm tra nhanh**:
  ```bash
  lsof -i :7770
  ```
- **Cách xử lý**: kill process cũ hoặc đổi `PORT` trong `.env`.

## 3) Mongo auth fail / thiếu user admin
- **Triệu chứng**:
  - `MongoServerError: command ... requires authentication`
  - `Authentication failed`
  - `UserNotFound: Could not find user "root" for db "admin"`
- **Nguyên nhân thường gặp**: container chạy `--auth` nhưng chưa có admin user.
- **Kiểm tra nhanh**:
  ```bash
  docker logs <mongo-container> | tail -n 100
  ```
- **Cách xử lý**:
  1. Tạo admin user trong Mongo.
  2. Cập nhật `MONGODB_URI` có `authSource=admin`.
  3. Restart server và retest `/health`.

## 4) CLI thiếu dependency
- **Triệu chứng**: `ERR_MODULE_NOT_FOUND` (ví dụ thiếu `commander`).
- **Nguyên nhân thường gặp**: chỉ cài deps ở `server/`, chưa cài ở root source.
- **Cách xử lý**:
  ```bash
  cd /var/www/vhst/tools/gpttranslator/source
  npm install
  ```

## 5) Upstream/model lỗi (401, model_not_found, no active credentials)
- **Triệu chứng**:
  - `No active credentials for provider`
  - `model_not_found`
  - `401 invalid key`
- **Checklist xử lý**:
  1. Kiểm tra `UPSTREAM_BASE_URL` có đúng `/v1`.
  2. Kiểm tra `UPSTREAM_API_KEY` còn hiệu lực.
  3. Đổi `UPSTREAM_MODEL` sang model đã xác thực chạy được (ví dụ `cx/gpt-5.4-mini`).
  4. Gọi lại `/v1/models` để xác nhận.

## 6) Register trả `Email already exists`
- **Triệu chứng**: test register liên tục dính `409 Email already exists`.
- **Nguyên nhân thường gặp**:
  - Dùng lại email cũ.
  - Bật `ONE_ACCOUNT_PER_IP=true`.
- **Cách xử lý**:
  - Dùng email unique theo timestamp.
  - Khi test local, có thể set `ONE_ACCOUNT_PER_IP=false`.

## 7) Dịch không ra file output
- **Triệu chứng**: command chạy xong nhưng output rỗng.
- **Checklist xử lý**:
  1. Đảm bảo chạy lệnh tại thư mục chứa `config.env`.
  2. `Path_Input` và `path_output` là đường dẫn hợp lệ.
  3. Input có extension nằm trong tập CLI hỗ trợ.
  4. Xem log server để kiểm tra lỗi upload/upstream.
