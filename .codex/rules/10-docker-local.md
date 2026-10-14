# 10 — Docker Desktop và khung local AML

Áp dụng khi sửa Dockerfile/Compose/DB bootstrap/start scripts/CI/recovery.
Đọc cùng [repository operations](09-repository-operations.md),
[security](07-security.md), [README local](../../README.md).
User đã cho phép Docker Desktop/database local và push main/develop/dev-sec trong
tác vụ xây khung; không suy ra quyền với database không thuộc dự án hay public hosting.

## Stack và isolation

- Giữ project `aml-blockchain`; db PostgreSQL 17, migrate one-shot, API/worker
  cùng backend image/code, web Nginx build React. Worker không chạy trong API.
- Ports bind `127.0.0.1`: web 8080, API 8000, DB 5433; không đổi thành all-interface
  hoặc mở firewall như tác dụng phụ. Không đụng MySQL đang có.
- Named volume `aml-data` giữ ledger. Test chỉ `aml_test`; trước reset test phải
  assert database name. Không `down -v`, prune volumes hoặc truncate `aml` để sửa lỗi.
- `aml_owner` migration, `aml_app` public data, evaluator riêng. Migration mới
  cấp đúng table/sequence privileges và không vô tình mở evaluation cho app role.

## Startup và build

- `node scripts/setup.mjs` chỉ tạo `.env` nếu chưa có; random passwords/session
  secret, không hardcode/print/commit. Không regenerate env khi volume còn dùng
  credentials cũ. `.env.example` giữ placeholders, không actual secrets.
- Validate `docker compose config --quiet`; không in config substituted secrets.
- db healthcheck trước migrate; migrate success trước API/worker; API healthy
  trước web. Lỗi migration phải chặn startup, không dùng create_all tại API startup.
- Dependency lockfile/hash giữ trong source; image official version được kiểm
  bằng build. Python non-root, no-new-privileges cho app, CPU/RAM worker/API bounded.
- Build/start có thể làm trong quyền local đã cấp; không yêu cầu duyệt từng lần.
  Không sửa global execution policy/trust để scripts chạy; có Node helper thay `.ps1`.

## Worker và recovery

Advisory lock một worker local; health heartbeat, signal shutdown tại boundary,
running jobs requeue khi restart. Ledger/outbox/chunks nguyên tử; checkpoint chỉ
sau assessment/snapshot/outbox commit. Khi RAM state lệch do DB error, job restart
dựng lại từ ledger, không tiếp tục trên state bị apply hai lần. Retry giữ snapshot
feed/config/version; replay mới là version mới, không đổi wallet/nonce/hash ledger.

Sau đổi pipeline, kiểm `docker compose --profile test run --rm test`, smoke
restart/replay và health. Chỉ rebuild service/image bị ảnh hưởng; không repeat
benchmark nếu code liên quan không đổi. Số liệu thực đo/đích benchmark tách rõ.
Tham chiếu startup semantics: [Docker Docs](https://docs.docker.com/compose/how-tos/startup-order/).
