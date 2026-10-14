# agent.md — Sổ tay thực hiện dự án AML Blockchain

## Điểm vào và cách sử dụng

[AGENTS.md](AGENTS.md) là hướng dẫn chính để Codex khám phá theo tên chuẩn.
File này cung cấp cách phân vai và thực hiện tương ứng với bộ quy tắc trong
[.codex/README.md](.codex/README.md); tránh sao chép toàn bộ rulebook sang đây.
Trong cấu hình dự án, `agent.md` là tên fallback nếu không có `AGENTS.md`/override
tại thư mục đó. Khi cả hai cùng tồn tại, agent vẫn phải đọc file này khi cần
phân vai hoặc tổ chức công việc; không giả định cả hai tự được nạp.

## Trách nhiệm chung

Hoàn thành phần việc được giao từ yêu cầu đến kiểm chứng. Giữ hợp đồng dữ liệu,
bất biến ledger và giới hạn AML trong [kế hoạch gốc](Ke-hoach-AML-Blockchain.md).
Phân biệt ba mức: yêu cầu từ kế hoạch; chuẩn kỹ thuật bổ sung; đề xuất chưa chốt.
Không tuyên bố website hay benchmark đã hoàn tất chỉ vì scaffold/config đã có.

## Vai trò chuyên môn

Một agent có thể đảm nhiệm tất cả vai trò dưới đây. Đây là phân công trách nhiệm
để đọc đúng tài liệu, không tạo agent runtime hoặc bật multi-agent.

| Vai trò | Phần chịu trách nhiệm | Bằng chứng cần bàn giao |
| --- | --- | --- |
| Điều phối/kiến trúc | Phạm vi, dependency, data contracts, ADR, thứ tự milestone | Thiết kế bám kế hoạch, quyết định có lý do, task có tiêu chí nhận |
| Data/Ledger | Genesis, generator, canonical hash, balances/nonce/fee, ingest/outbox | Fixture ledger hợp lệ, bảo toàn, determinism, crash/replay recovery |
| AML/Graph | Windows, motif, tracing/haircut, TI, floors, history, coverage | Positive/boundary/negative fixtures, evidence và no-leakage checks |
| API/Database | Migration/FK/index, DTO, job/SSE, RBAC/audit | Contract tests, run isolation, integration với PostgreSQL thật |
| Dashboard | Simulation Control, Graph Explorer, Alert & Evaluation | Luồng thao tác thật, tiền chính xác, timeline đúng, trạng thái lỗi/thiếu dữ liệu |
| QA/Evaluation | T01–T22, split, metrics, ablation, benchmark | Lệnh tái lập, kết quả thực đo, false positives và giới hạn được công bố |

## Một chu trình làm việc

1. Xác định kết quả người dùng cần và phạm vi đã cho phép. Đọc `AGENTS.md`, phần
   kế hoạch liên quan và rule theo trigger; ghi lại trạng thái thực của repository.
2. Chọn requirement/test IDs từ [.codex/requirements-map.md](.codex/requirements-map.md).
   Với việc phức tạp, tạo task bằng [.codex/templates/task.md](.codex/templates/task.md).
3. Chốt hợp đồng hoặc quyết định còn thiếu từ [.codex/decision-register.md](.codex/decision-register.md)
   khi phần đang làm phụ thuộc vào nó. ADR dùng [.codex/templates/adr.md](.codex/templates/adr.md).
4. Triển khai một lát cắt có thể kiểm tra, ưu tiên logic domain và persistence
   trước giao diện thể hiện kết quả. Thay đổi contract phải cập nhật cả producer,
   consumer, schema, fixtures và tài liệu.
5. Kiểm tra phần bị ảnh hưởng, xử lý lỗi do thay đổi gây ra và review diff. Khi
   kiểm tra chưa chạy được, ghi đúng nguyên nhân và tiếp tục việc độc lập có ích.
6. Đối chiếu checklist hoàn thành, cập nhật trạng thái và bàn giao trung thực.

## Khi gặp điểm khó hoặc mâu thuẫn

- Nếu có thể chọn một cách local, có thể đảo ngược và phù hợp kế hoạch: chọn,
  ghi lý do và tiếp tục. Không dừng vì mọi chi tiết nhỏ chưa được định nghĩa.
- Nếu quyết định đổi mô hình network, ý nghĩa score, quyền dữ liệu hoặc phạm vi
  sản phẩm: chuẩn bị phương án cụ thể; chỉ xin quyết định khi chưa được giao quyền.
- Với lỗi không thể tái lập: thu thập input, seed, order, version và logs đã che
  secret; không kết luận đã sửa bằng một lần chạy không gặp lỗi.
- Nếu việc mới làm thay đổi yêu cầu cũ, giữ mục tiêu ban đầu và điều chỉnh task;
  không tự hủy phần còn lại hoặc mở rộng thêm tính năng ngoài yêu cầu.

## Hình thức báo cáo

Tiến độ: nêu điều đã xác minh, quyết định vừa đưa ra và bước kiểm tra tiếp theo.
Kết quả: nêu hành vi đã thay đổi, file chính, kiểm tra đã chạy và hạn chế còn lại.
Số liệu luôn kèm run/seed/config/version và phân biệt mục tiêu với kết quả đo.
Không ghi token, mật khẩu, toàn bộ connection string hoặc dữ liệu nhạy cảm vào báo cáo.
