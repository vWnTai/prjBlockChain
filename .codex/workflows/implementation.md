# Workflow — Triển khai tính năng

Áp dụng cho tính năng mới hoặc refactor nhiều module. Root instructions:
[AGENTS.md](../../AGENTS.md); phạm vi: [00-scope](../rules/00-scope.md).

## 1. Xác định lát cắt

Đọc phần kế hoạch và rule đúng trigger. Ghi hành vi hiện tại/thực trạng file,
kết quả mong muốn, scope và tiêu chí kiểm tra theo [task template](../templates/task.md).
Gắn [requirement/test IDs](../requirements-map.md). Không bắt sửa nhỏ dùng kế
hoạch dài; nhiều module/migration/thuật toán mới cần kế hoạch đủ theo dõi.

## 2. Chốt contract trước phụ thuộc

Đọc [decision register](../decision-register.md) với phần việc hiện tại.
Chốt amount/order/version/as_of/coverage, API DTO, DB constraints và error states.
ADR dùng [template](../templates/adr.md) cho quyết định có tác động dài hạn.
Chọn kỹ thuật routine trong quyền được giao và ghi lý do; chỉ xin quyết định
khi scope/ý nghĩa nghiệp vụ bị đổi hoặc thiếu thông tin không thể suy ra.

## 3. Triển khai

Làm domain invariant/persistence trước, worker/API boundary kế tiếp, UI/metrics
sau khi dữ liệu có nghĩa. Một feature có thể triển khai lát cắt end-to-end nhỏ
để demo sớm nhưng không mock domain rồi tuyên bố hoàn tất. Contract change
cập nhật cả schema/migration/producer/consumer/fixtures/version/docs cùng nhau.
Giữ thay đổi nhỏ đủ review, không tạo hai backend hay dependency ngoài nhu cầu.

## 4. Kiểm chứng

Chạy tests/checks phù hợp [08-testing](../rules/08-testing-evaluation.md).
Sửa failures do thay đổi gây ra, kiểm boundaries/negative/coverage và diff.
Với UI, kiểm màn hình/interaction thực ở viewport đại diện, loading/error/empty,
tiền lớn/timeline/evidence. Không suy ra UI tốt chỉ vì build pass.
Lưu lệnh/output summary, không secret. Nếu thiếu runner/env, ghi hạn chế thật
và hoàn thành kiểm tra độc lập; không ghi “pass” cho kiểm tra chưa chạy.

## 5. Hoàn tất

Đối chiếu [Definition of Done](../checklists/definition-of-done.md) theo scope,
cập nhật task/ADR/contracts/readme. Bàn giao kết quả reviewable và trạng thái
kiểm chứng; không dừng ở kế hoạch khi được giao thực hiện code.

## Thứ tự milestone theo kế hoạch

| Mốc | Nội dung | Gate trước mốc kế tiếp |
| --- | --- | --- |
| M1 | Schema/Compose/genesis/ledger/canonical hash | Money/balance/fee/nonce/hash + deterministic fixtures |
| M2 | Nền/campaign/truth riêng/indexer/outbox/replay | 5.000 tx ledger hợp lệ, no label leakage, restart/dedup |
| M3 | Windows/motifs/reasons/evidence | Positive/boundary/negative cho từng rule |
| M4 | Temporal haircut/TI/scoring/history | No future leakage, conservation, floors, baseline validation metrics |
| M5 | API/SSE và ba màn hình dashboard | Demo tạo run→alert→inspect evidence→review; bounded queries |
| M6 | E2E/100k benchmark/split/ablation/reports | Số đo thực, config/seeds/versions, limits và demo tái lập |

ML là mở rộng sau baseline. Các tuần trong kế hoạch là ước lượng; thứ tự phụ
thuộc và gate quan trọng hơn việc tự đánh dấu đúng lịch khi kiểm chứng chưa xong.
