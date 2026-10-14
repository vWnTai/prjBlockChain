# 01 — Kiến trúc, tổ chức mã và dependency

Áp dụng khi scaffold, refactor module, thêm dependency hoặc thay service boundary.
Nguồn: mục 1 và 5 của [kế hoạch](../../Ke-hoach-AML-Blockchain.md).

## Stack và ranh giới

Python + FastAPI + PostgreSQL + NetworkX; scikit-learn chỉ cần khi triển khai ML.
Frontend React + Cytoscape.js. Docker Compose cho môi trường local có thể tái lập.
API và worker chạy hai tiến trình dùng chung domain code. Không chạy graph/ML
nặng trong request handler hoặc React. Không thêm Kafka/Neo4j/GNN vào MVP vì thói quen.
Không dựng đồng thời backend Python và Laravel nếu chưa có ràng buộc mới.

| Module | Đầu vào được phép | Trách nhiệm |
| --- | --- | --- |
| Generator | Seed/config và genesis | Transaction intents; truth xuất qua kênh riêng |
| Ledger | Intent đã normalize, state | Validate/apply, hash/block, persistence/outbox |
| Indexer | Block/tx chuẩn | Chống trùng, order liên tục, normalization |
| Features/Graph | Ledger đã quan sát đến order | Window snapshots, candidate và allocation state |
| AML | Snapshot, graph/state, TI hợp lệ | Rule hits, tracing, score, reason/evidence |
| Alerts | Assessment/rule hits | Dedup episode, evidence, review history |
| Evaluator | Predictions đã khóa và ground truth | Matching, metrics, reports; không cấp nhãn cho AML |
| API | DTO và auth context | Validation, RBAC, job/query, serialization, SSE |
| UI | Public API contracts | Render, filter, navigation, review, coverage |

Domain logic không phụ thuộc FastAPI request, React hoặc UI formatting.
Feature/AML không import generator truth/evaluator labels. Evaluator có thể đọc
predictions nhưng không sửa predictions trong quá trình tính metrics.
I/O và transaction boundary rõ ràng; không giữ DB session toàn cục hoặc phụ thuộc
state singleton trong API để giả làm durable queue.

## Cấu trúc tham khảo khi chưa có mã nguồn

Đây là đề xuất bootstrap, chưa phải cấu trúc hiện có. Khi được giao triển khai,
chọn một cấu trúc nhất quán và ghi quyết định; không tạo thư mục rỗng chỉ để đủ sơ đồ.

```text
backend/
  app/
    api/ core/ db/ schemas/
    simulation/ ledger/ indexing/
    features/ graph/ aml/ alerts/
    workers/ evaluation/
  migrations/
  tests/
frontend/
  src/
    app/ api/ components/ features/ lib/
  tests/
configs/
docs/
  contracts/ decisions/ tasks/ reports/
fixtures/
compose.yaml
```

Quy ước bổ sung đề xuất: React với TypeScript strict và Vite; Pydantic DTO,
SQLAlchemy/Alembic cho DB; pytest, Vitest/Testing Library và Playwright cho kiểm
tra phù hợp. Chốt phiên bản/package manager khi scaffold, dựa trên dependency
đã có nếu repository được bổ sung trước đó; không tự coi đề xuất là yêu cầu gốc.

## Chuẩn mã

- Python dùng type hints cho domain/public boundaries; `snake_case`, module nhỏ
  theo trách nhiệm; lỗi domain có loại rõ và được API chuyển thành lỗi công khai.
- TypeScript không dùng `any` hoặc `@ts-ignore` để bỏ qua contract; validate dữ
  liệu bên ngoài khi cần. Domain money/order/version có type riêng dễ nhận biết.
- Không copy công thức AML/score sang frontend. Dùng một money parser/formatter
  kiểm tra chuỗi chính xác; một định nghĩa order và amount contract ở backend.
- Comments giải thích giả định, rounding, invariant hoặc lý do thuật toán;
  tránh diễn giải lại từng dòng mã. Có docstring cho boundary có semantics khó.
- Không bắt `Exception` rồi trả score=0/kết quả rỗng như thành công. Retry chỉ cho
  lỗi tạm thời; lỗi schema/invariant phải được ghi nhận và không tiến checkpoint.
- Query SQL có tham số, không N+1 ở màn hình transaction/alert. Async handler
  không gọi thư viện blocking nặng trực tiếp; CPU work đưa sang worker.

## Dependency và tính tương thích

Chọn dependency giải quyết nhu cầu cụ thể, kiểm tra tài liệu chính thức khi API
hoặc version chưa chắc chắn. Commit lockfile của từng hệ sinh thái; tránh pin
version do đoán và tránh cài package theo tên gần giống. Khi bổ sung dependency,
ghi mục đích, ảnh hưởng build/runtime và cập nhật kiểm tra phù hợp.
Đổi schema/API/rule không được để producer và consumer ở hai contract khác nhau.
