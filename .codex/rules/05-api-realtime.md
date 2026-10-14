# 05 — FastAPI, data contracts, background jobs và SSE

Áp dụng cho HTTP endpoint, serializer, auth boundary, job và event stream.
Nguồn: mục 1 và 4 của [kế hoạch](../../Ke-hoach-AML-Blockchain.md).
Phần error/pagination/job/SSE chi tiết dưới đây là chuẩn kỹ thuật bổ sung.

## Hợp đồng API dự kiến

Các đường dẫn là đề xuất kế hoạch, chưa là endpoint đang chạy. Bổ sung contract
rõ trước implementation; giữ prefix `/api` thống nhất với client/OpenAPI.

| Endpoint | Hành vi cần thực hiện |
| --- | --- |
| POST /api/simulations | Validate config/seed; tạo durable job, trả 202 với run_id/job_id |
| GET /api/simulations/{run_id} | Config thực dùng, versions, state/progress/error và analysis progress |
| POST /api/simulations/{run_id}/replay | Tạo job phân tích/version mới trên ledger cũ, không apply ledger lại |
| GET /api/transactions | Lọc run/wallet/time/score; cursor pagination với order ổn định |
| GET /api/wallets/{id} | Run scope bắt buộc; balance/flows/assessment/as_of/coverage |
| GET /api/graph | Run/center/hops/time/as_of/limits; nodes/edges, coverage/truncated |
| GET /api/alerts | Run/filter/version và pagination |
| GET /api/alerts/{id} | Run scope; đầy đủ rule/source/score/evidence/history |
| PATCH /api/alerts/{id}/review | Kiểm quyền, trạng thái hợp lệ/comment; ghi analyst_reviews nguyên tử |
| GET /api/metrics | Run/dataset/pattern/model/analysis_mode/version, mẫu số và kết quả evaluator |
| GET /api/events | SSE progress/block/alert theo quyền và run |

Resource path chỉ có `{id}` vẫn cần run_id qua query hoặc route scoped đã chốt;
không tra theo id rồi trả resource từ run khác. Client không tự suy luận run
bằng selection hiện tại nếu server chưa validate. Giữ network/asset phù hợp run.

## DTO, validation và errors

- Pydantic/request schemas phân biệt config, transaction, assessment, evidence,
  review và metric. Không serialize model DB trực tiếp hoặc field truth.
- Money là string integer base units; asset/decimals kèm ngữ cảnh. UTC ISO 8601;
  order/as_of gồm height+tx_index khi cần, không chỉ timestamp.
- Seed/size/interval/hops/window/node/edge limits có bounds; time start<=end,
  enum/sort/fields thuộc allowlist. Không accept SQL/expression/rule code thực thi.
- Lỗi có code ổn định, message dễ hiểu, field details an toàn và request_id.
  HTTP semantics nhất quán: 401 chưa xác thực, 403 thiếu quyền, 404 không tìm
  resource trong scope, 409 conflict, 422 validation, 429 limit, 5xx lỗi máy chủ.
- Không trả stacktrace/DSN/secret; không chuyển DB failure thành 200 empty list.
  Detail partial khác error: dữ liệu thật nhưng thiếu phải có coverage/reason.
- Cấu hình/query/body giới hạn kích thước; server không tin limit do client gửi.

## Pagination, query và as_of

Cursor ổn định có tie-break: transactions theo block_height/tx_index/identity;
alerts theo detected_at/identity. Contract nói rõ ASC/DESC, filter và cutoff.
Cursor mang scope hoặc được validate cùng scope; đổi filter/run/version phải
reset cursor. Query historical không được dùng cached current risk của wallet.

Graph trả subgraph bounded mặc định <=1.000 nodes/3.000 edges và engine budget
riêng; báo truncated/partial khi cắt. Transaction edges giữ tx_hash, direction,
value/asset/time/order, không collapse mất evidence. Không tải toàn bộ graph
hoặc full transaction dataset để client tự pagination/lọc.

## Job và tiến độ bền vững

Khởi tạo job phải lưu trước trả 202. FastAPI BackgroundTasks/RAM thread đơn
lẻ không được thay durable queue/outbox/worker. Run generation và analysis
progress khác nhau; job completed chỉ khi phần job cam kết đã commit đầy đủ.
Run/analysis lifecycle và retry/cancel/resume cần state machine đã chốt bằng ADR.
Không thêm nút pause/cancel nếu backend chưa có boundary an toàn tương ứng.

Chuẩn bổ sung: idempotency cho thao tác tạo job/replay hoặc cơ chế dedup tương
đương; cùng key+payload không tạo job hai lần, cùng key khác payload báo conflict.
Chốt scope/retention key. Lock một writer run; replay version riêng không phá
live analysis. Errors/progress sống qua restart và không báo 100% khi worker fail.

## SSE

- Event envelope có event id/type, run_id, job/analysis_version nếu áp dụng,
  timestamp và payload theo schema_version. Event chỉ public sau durable commit.
- Không chứa truth, secret hoặc dữ liệu khác quyền. Authorize connection và
  từng phạm vi stream; không phát toàn bộ rồi để client lọc.
- Heartbeat, reconnect/backoff và cleanup; event ID/Last-Event-ID nếu có buffer
  replay. Khi cursor quá cũ/mất retention, yêu cầu snapshot/resync có contract.
- Client dedup event IDs; reconnect không nhân alert/block hoặc đảo order.
  Không coi SSE là nguồn sự thật duy nhất; HTTP snapshot xác nhận trạng thái.
- Không gửi mỗi cạnh toàn graph liên tục. Batching/rate bounds/backpressure
  để client chậm không tăng RAM không giới hạn. Nếu phải coalesce/drop progress,
  vẫn resync được kết quả durable; không âm thầm mất lifecycle event.
- Native EventSource/auth transport phải phù hợp cơ chế session được chọn;
  không đưa bearer token vào URL/query để giải quyết hạn chế header.

## Review và compatibility

Trạng thái review, ai được chuyển và optimistic concurrency được chốt trong
decision register. Audit ghi before/after/actor/time/comment; giữ rule assessment.
OpenAPI và frontend types phải đồng bộ. Contract-breaking change cần version/
migration tương thích, fixtures và integration tests; không sửa response ngầm.
