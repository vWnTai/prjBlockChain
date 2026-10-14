# AGENTS.md — Quy tắc cho agent của dự án AML Blockchain

## Mục tiêu và nguồn yêu cầu

Xây dựng website mô phỏng, phân tích và giải thích dấu hiệu AML theo
[Ke-hoach-AML-Blockchain.md](Ke-hoach-AML-Blockchain.md). Đây là kế hoạch triển
khai; không được mô tả tính năng, kiểm thử hoặc benchmark chưa thực hiện là đã có.
Giao tiếp với người dùng bằng tiếng Việt; tên mã, trường dữ liệu và API bằng tiếng Anh.

Tuân thủ chỉ dẫn cấp hệ thống, môi trường và yêu cầu hiện tại của người dùng.
Trong tài liệu dự án, kế hoạch gốc là nguồn yêu cầu nghiệp vụ; bộ `.codex` diễn giải
và bổ sung chuẩn kỹ thuật. Nếu hai nguồn mâu thuẫn, nêu rõ và sửa tài liệu liên
quan, không âm thầm đổi kế hoạch. Quy tắc phạm vi thư mục sâu hơn có thể cụ thể hóa
quy trình; thay đổi bất biến nghiệp vụ phải có yêu cầu hoặc quyết định được ghi nhận.

## Những bất biến phải giữ

1. MVP: account-based, một network và một tài sản `SIM`, 6 chữ số thập phân,
   chuyển tài sản gốc. Stack: Python/FastAPI, PostgreSQL, NetworkX,
   React/Cytoscape.js, Docker Compose. API và worker là hai tiến trình.
2. Tiền: Python `int`, PostgreSQL `NUMERIC(78,0)`, JSON là chuỗi base unit.
   Không dùng `float`, JavaScript `Number` hoặc phép làm tròn UI cho hạch toán.
   `1 SIM = 1_000_000` base units; `T = 1_000_000_000` base units.
3. Ledger: balance không âm; nonce đúng; `fee = gas_used × effective_gas_price_base`;
   tổng balance kể cả `fee_sink` bằng genesis supply. Intent bị từ chối không
   tạo transaction thành công hoặc cạnh AML. Self-transfer chỉ mất fee.
4. Thời gian UTC; thứ tự `(block_height, tx_index)`. Feature, graph, feed và UI
   timeline phải tôn trọng `as_of`; không đọc dữ liệu tương lai hoặc sửa lịch sử
   online để làm đẹp kết quả.
5. Ground truth, actor và campaign labels chỉ dành cho generator/evaluator.
   AML engine, feature pipeline và API phân tích không được dùng chúng để dự đoán.
6. PostgreSQL là nguồn dữ liệu bền vững. Ledger + block + outbox ghi nguyên tử;
   worker xử lý idempotent, giữ thứ tự và chỉ tiến checkpoint sau khi lưu kết quả.
   Mọi thực thể/query của một run phải cách ly bằng `run_id`.
7. Graph là `MultiDiGraph`, giữ từng giao dịch. Tracing phải đúng order, bảo toàn
   lượng phân bổ và công khai giả định haircut. Reachability không chứng minh lượng tiền.
8. TI match đúng `network_id` + địa chỉ, thời gian biết/hiệu lực và phiên bản.
   Score cao từ engine không tự biến ví thành blacklist hoặc nguồn lan truyền.
9. Giữ đúng score blend và floor theo rulebook: blacklist 95, rapid 80,
   motif 70; làm tròn half-up. Baseline `A=0`, không tự chia lại trọng số.
10. Alert phải có reason codes, thresholds, evidence, thời điểm phát hiện,
    version và coverage. Thiếu lịch sử, hết budget hoặc lỗi ML phải thể hiện
    `partial`/`truncated`/`unavailable`; không suy ra an toàn.
11. Viewer/Analyst/Admin được kiểm tra quyền ở backend. Feed/config là dữ liệu
    có schema, không phải biểu thức được thực thi. Không đưa secret vào repo/log/UI.
12. Score là ưu tiên xem xét, không phải xác suất phạm tội. MVP không chặn hoặc
    hoàn tác giao dịch final. Không tự mở rộng EVM, UTXO, reorg, token, bridge hay GNN.

## Đọc quy tắc đúng theo công việc

Khi bắt đầu triển khai hoặc thay đổi nghiệp vụ, đọc phần liên quan của kế hoạch
gốc và các file theo bảng dưới. Với sửa lỗi chính tả hoặc tài liệu nhỏ, chỉ đọc
nguồn bị ảnh hưởng. Các tài liệu được dẫn chiếu là yêu cầu phải đọc khi đúng trigger;
không giả định toàn bộ `.codex/rules/*.md` được Codex tự động nạp.

| Công việc | Tài liệu phải dùng |
| --- | --- |
| Chốt phạm vi, chọn dependency, tổ chức mã | [.codex/rules/00-scope.md](.codex/rules/00-scope.md), [.codex/rules/01-architecture.md](.codex/rules/01-architecture.md) |
| Generator, ledger, hash, replay | [.codex/rules/02-ledger-simulation.md](.codex/rules/02-ledger-simulation.md) |
| Schema, migration, query, data contracts | [.codex/rules/03-database-contracts.md](.codex/rules/03-database-contracts.md) |
| Feature, graph, TI, rule, score, ML | [.codex/rules/04-aml-graph-scoring.md](.codex/rules/04-aml-graph-scoring.md) |
| Endpoint, background job, SSE | [.codex/rules/05-api-realtime.md](.codex/rules/05-api-realtime.md) |
| React, Cytoscape, dashboard, timeline | [.codex/rules/06-frontend-ux.md](.codex/rules/06-frontend-ux.md) |
| Auth, quyền, import/export, deployment | [.codex/rules/07-security.md](.codex/rules/07-security.md) |
| Test, evaluator, benchmark, thay đổi detector | [.codex/rules/08-testing-evaluation.md](.codex/rules/08-testing-evaluation.md), [.codex/requirements-map.md](.codex/requirements-map.md) |
| Tooling, Git, CI, Docker, vận hành | [.codex/rules/09-repository-operations.md](.codex/rules/09-repository-operations.md) |
| Docker Desktop, Compose/startup, DB bootstrap và local recovery | [.codex/rules/10-docker-local.md](.codex/rules/10-docker-local.md) |

## Cách thực hiện và bàn giao

- Kiểm tra file, cấu hình và thay đổi hiện có trước khi sửa. Không ghi đè công
  việc của người dùng; không giả định repo đã có Git, dependency hay test runner.
- Với tính năng nhiều module, dùng [.codex/workflows/implementation.md](.codex/workflows/implementation.md)
  và ghi kế hoạch đủ theo dõi. Lỗi dùng [.codex/workflows/bugfix.md](.codex/workflows/bugfix.md).
  Phát hành dùng [.codex/workflows/release.md](.codex/workflows/release.md).
- Giải quyết lựa chọn kỹ thuật thường lệ và công việc local có thể đảo ngược trong
  phạm vi được giao. Chỉ hỏi khi thiếu quyết định ảnh hưởng đáng kể hoặc hành động
  vượt quyền đã có; không hỏi lại quyền đã được cấp. Chuẩn bị kết quả cụ thể trước
  khi xin duyệt cho hành động bên ngoài chưa được cho phép.
- Không sinh sub-agent chỉ vì có nhiều module. Chỉ dùng khi yêu cầu người dùng
  hoặc chỉ dẫn đang áp dụng cho phép; [agent.md](agent.md) mô tả vai trò chuyên môn,
  không phải cấu hình tự khởi chạy agent.
- Quyết định chưa được kế hoạch xác định: xem [.codex/decision-register.md](.codex/decision-register.md),
  chốt bằng ADR khi triển khai; không dùng TODO làm hành vi runtime mặc định.
- Chạy kiểm tra phù hợp với phần đã sửa. Báo đúng lệnh, kết quả và phần chưa chạy.
  Không skip test, giảm assertion hoặc thay fixture để che lỗi. Với thay đổi tài
  liệu thuần túy, kiểm tra liên kết và sự nhất quán; không cần chạy benchmark ứng dụng.
- Trước bàn giao, áp dụng [.codex/checklists/definition-of-done.md](.codex/checklists/definition-of-done.md)
  theo phạm vi. Nêu kết quả, file chính, bằng chứng kiểm tra và giới hạn còn lại.

## Code Review Rules

Ưu tiên tìm sai số tiền; lẫn run/asset/network; leakage thời gian/nhãn; hash không
tái lập; outbox/checkpoint làm mất hoặc nhân đôi việc; tracing cộng trùng; score
floor sai; evidence không khớp version; phân quyền chỉ nằm ở UI; timeline hiển thị
dữ liệu tương lai; coverage thiếu nhưng được trình bày như đã phân tích đầy đủ.
Mỗi nhận xét cần vị trí, điều kiện gây lỗi và ảnh hưởng; không suy diễn lỗi chưa có bằng chứng.
