# Workflow — Chuẩn bị và xác minh phát hành

Chỉ áp dụng khi được giao chuẩn bị/phát hành. Tạo quy tắc hoặc chạy demo local
không tự cho phép publish, push, merge hoặc sửa hạ tầng bên ngoài.
Root instructions: [AGENTS.md](../../AGENTS.md).

## Chuẩn bị artifact reviewable

- Chốt source/lockfile/image/contract/rule/model/feed/analysis versions và
  config/seeds; liệt kê scope hỗ trợ thực. Không gắn nhãn mở rộng chưa có tests.
- Hoàn thành [Definition of Done](../checklists/definition-of-done.md) phần release.
  Test/migration/security/build và benchmark chạy theo phạm vi phát hành.
- Môi trường đích, auth/RBAC, secret provisioning, listeners/CORS/TLS, volumes,
  limits và worker readiness rõ; không để demo bypass vào public deployment.
- Prepare migrations/backfill, backup/recovery/rollback và compatibility producer/
  consumer. Kiểm restore/replay trong môi trường tách biệt với artifact sẽ dùng.
- Tạo release notes: thay đổi hành vi, schema/API compatibility, seed/version,
  test/metric thực, known limits và thao tác migration/recovery.

## Thực hiện theo quyền đã có

Nếu chưa có quyền cho hành động external, xin duyệt cuối cùng trên artifact và
môi trường cụ thể đã chuẩn bị. Nếu đã được cho phép trong session, tiếp tục theo
scope; không hỏi lại. Không tự tắt sandbox, sửa global trust hoặc dùng production
data để vượt blocker. Thao tác destructive phải đúng đích và quyền được cấp.

## Sau phát hành

Health/readiness, schema version, API contract, writer/worker lease và outbox lag;
smoke run, stream reconnect, graph limits, alert evidence và review audit.
Kiểm tiền/version/isolation và không nhân đôi khi restart. Khi lỗi, dừng thay
đổi tiếp và thực hiện recovery đã chuẩn bị trong scope; không reset volume.
Ghi deployment version/time/environment, kết quả checks và vấn đề còn lại.
