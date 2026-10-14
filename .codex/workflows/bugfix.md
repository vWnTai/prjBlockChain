# Workflow — Điều tra và sửa lỗi

Root instructions: [AGENTS.md](../../AGENTS.md).
Tests/rules: [requirements map](../requirements-map.md).

1. Tái lập bằng input/run/seed/config/order/version cụ thể; ghi actual vs expected.
   Với lỗi UI, thêm thao tác, run selection, timeline, viewport và request response.
   Che secret; không lấy truth làm dữ liệu đầu vào detector để giúp tái lập.
2. Đọc module/rule liên quan và tìm nguyên nhân ở boundary đầu tiên sai.
   Kiểm amount/order/scope/version/state; không giả lỗi graph do frontend nếu
   API evidence đã sai, hoặc sửa UI formatting để che lỗi tiền backend.
3. Với lỗi nghiệp vụ, thêm regression fixture độc lập chứng minh lỗi và boundary
   lân cận. Với lỗi copy/layout nhỏ, kiểm trực tiếp thay vì test mirror implementation.
4. Sửa nguyên nhân trong phạm vi; không tắt detector, bỏ floor, nới balance check,
   skip test hoặc hardcode wallet/seed để bản demo xanh.
5. Chạy kiểm tra bị ảnh hưởng. Với ledger/tracing/outbox, kiểm conservation,
   determinism, restart/replay/duplicate; với auth kiểm cả role được phép và bị từ chối.
6. Nếu persisted state/history đã sai, ghi recovery/reanalysis plan có version,
   nguyên nhân và ảnh hưởng. Không chỉnh trực tiếp ledger final hoặc xóa audit để
   khiến kết quả cũ giống mới; data correction vượt quyền cần xử lý theo scope đã cấp.
7. Review diff và ghi bằng chứng sửa: trigger, hành vi sau sửa, test/result và
   limitation. Không nói đã sửa khi chỉ không tái hiện ở một seed khác.

Lỗi cũ không liên quan vẫn được ghi nhận; chỉ sửa khi thuộc phạm vi hoặc cản
trở kiểm chứng cần thiết. Lỗi infra/config không phải lý do sửa expected label
hoặc bỏ kiểm tra tích hợp PostgreSQL.
