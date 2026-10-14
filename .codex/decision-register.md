# Những quyết định cần chốt khi triển khai phần phụ thuộc

Kế hoạch đã khóa stack, MVP, công thức blend/floors và các ngưỡng khởi tạo.
Bảng này ghi phần chưa đủ chi tiết để implement deterministically. Không thay
đổi các quyết định đã rõ và không bắt tất cả mục phải có câu trả lời trước khi
làm việc độc lập. Baseline local đã chốt trong
[ADR-0001](../docs/decisions/0001-local-architecture.md) và các lockfiles/contracts;
D09 (ML) và thiết kế đánh giá nghiên cứu mở rộng còn deferred. Các mục dưới đây
là checklist chi tiết cho lần mở rộng/thay đổi, không còn đồng nghĩa tất cả chưa chốt.

Khi được giao module liên quan, agent chọn phương án trong phạm vi đã cho phép,
ghi ADR bằng [template](templates/adr.md), cập nhật bảng với path/status và tests.
Chỉ xin quyết định người dùng khi tác động nghiệp vụ/scope hoặc quyền chưa có;
đừng biến bảng này thành quy trình duyệt mọi chi tiết kỹ thuật.

| ID | Phần phải chốt | Thời điểm | Nội dung cần ghi / kiểm chứng |
| --- | --- | --- | --- |
| D01 | Toolchain/bootstrap | Scaffold | Cấu trúc repo, Python/Node/PostgreSQL versions, package manager/lockfile, TS/Vite/ORM/migrations/test runners; theo môi trường/dependency thực |
| D02 | Canonical hashing/genesis/address | Trước ledger hashes | Key/value encoding, domain fields, Merkle odd/empty, genesis/checksum ordering, normalization/format địa chỉ; golden vectors và run-ID độc lập |
| D03 | As-of và TI validity | Trước TI/online query | as_of_time vs event/observed/analysis time, tx order cutoff, valid_to inclusive/exclusive, tie/conflicting feed snapshots; boundary fixtures |
| D04 | Haircut rounding và source initialization | Trước allocation | Rounding đa nguồn/value/fee, remainder giữ sender khi khả thi, full-spend không để exposure>remaining balance, genesis/source top-up/overlapping TI; conservation fixtures |
| D05 | Ví hệ thống/fee_sink | Trước public intents | Có cho user intent chuyển đến/từ system wallet không; fee-only flow/exposure bookkeeping; graph exclusion và supply invariant |
| D06 | Mixing region/candidate/budget | Trước graph rules | Region merge/canonical ordering, snapshot B0, dwell/flow fractions, candidate bounds, partial reasons; không cộng edge nội bộ hay phí hai lần |
| D07 | Alert episodes/dedup/history | Trước alert service | Anchor, episode start/quiet-time/end, key encoding, evidence append, phát hiện lại/as_of revision và version boundaries; duplicate tests |
| D08 | Direct counterparty component | Trước E blend | E_direct_counterparty từ category/severity/confidence/direction, direct blacklist floor giữ 95, phân biệt nguồn tiền với recipient risk; score fixtures |
| D09 | ML failure/artifact policy | Trước optional ML | Feature schema/order, quantile/scaler/artifact, declared A fallback khi hybrid unavailable, coverage/model status, baseline không outage, safe trusted loading |
| D10 | Run/analysis/job lifecycle | Trước jobs/SSE | States/transitions, progress units, terminal/failed, one writer run, leases/retries, idempotency; cancel/pause/resume chỉ nếu được yêu cầu và an toàn |
| D11 | Auth và quyền ngoài review | Trước protected API | Identity/session source, auth transport/SSE, role/scope checks, ai tạo run/replay/export/quản lý users; local-demo profile boundaries |
| D12 | Review state machine | Trước PATCH review | Statuses/transitions/reopen, actor/comment rules, concurrency/version, audit; analyst không sửa engine assessment |
| D13 | API DTO/cursor/event contracts | Trước frontend integration | Money parser/capacity/identifier bounds, error envelope, scoped IDs, sort/cursor, as_of/order, event IDs/buffer/resync và maximum limits |
| D14 | Dataset identity/splits | Trước evaluation datasets | Seed/namespace tạo địa chỉ độc lập split nhưng reproducible, generator variants/core evidence labels, multi-label và prevalence denominator; manifest checks |
| D15 | Evaluation edge policies | Trước test scoring | Matching tie-break one-to-one/core>=50%, duplicate definition, zero denominator/AP, CI/resampling, đủ-evidence timestamp oracle; khóa trước test |
| D16 | Vận hành/recovery/retention | Trước durable workloads/release | Checkpoint state/schema, graph rebuild, feed/model/metrics/audit/event retention, queue bounds/backup/restore, cache TTL/version, health/readiness |

Các default từ kế hoạch (seed=42, 12s/block, 100 tx/block, trace 5 hop/24h,
20.000 visited edges/100 paths, UI 1.000 nodes/3.000 edges) không bị mở lại bởi
bảng này. Thay chúng là đổi versioned config có lý do/validation tương ứng.

Điểm cần cẩn trọng D04: chỉ nói “round down và giữ remainder ở sender” chưa đủ
cho một giao dịch tiêu hết balance hoặc nhiều phần vốn. Trước implementation,
cần quy tắc phân bổ nguyên bảo toàn, không âm và không để remainder vượt số dư.
Không dùng float hoặc bỏ remainder như một cách xử lý nhanh.
