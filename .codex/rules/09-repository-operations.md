# 09 — Repository, Windows, CI, Docker và vận hành

Áp dụng cho tooling, scripts, Git, environment, deployment và recovery.
Nguồn: Docker Compose, replay và sản phẩm bàn giao trong [kế hoạch](../../Ke-hoach-AML-Blockchain.md).
Quy tắc thao tác và vận hành dưới đây bổ sung cho implementation.

## Repository và thay đổi

Kiểm cấu trúc/config hiện có bằng `rg --files`, đọc script/lockfile trước chạy.
Không giả định đã có Git hoặc scaffold. Giữ file UTF-8 và không đổi nội dung kế
hoạch ngoài yêu cầu. Nếu PowerShell hiển thị sai tiếng Việt, đọc với Encoding
UTF8; không “sửa” văn bản vì console decode sai.

Đổi mã trong phạm vi tác vụ; không format toàn repo, đổi package manager hoặc
refactor module không liên quan như tác dụng phụ. Review diff/trạng thái; không
ghi đè hoặc hoàn tác thay đổi của người dùng. Commit source/contracts/migration/
lockfile phù hợp, không commit build output/cache/env/DB volume/run artifacts
lớn không cần thiết. Git commit/PR/push thực hiện theo quyền đã có; không tự
publish/merge từ một yêu cầu chỉ xây dựng local.

## Thao tác shell trên Windows

- Dùng đúng shell môi trường; không trộn PowerShell với bash syntax trong cùng lệnh.
- Với file operations dùng `-LiteralPath`, resolve absolute path trước recursive
  remove/move; xác minh đích nằm trong workspace hoặc đích cụ thể được cho phép.
- Không enumerate đường dẫn bằng PowerShell rồi truyền sang cmd/batch để xóa.
  Không destructive wildcard/root path/reset volume khi chưa có scope rõ.
- Không dùng shell interpolation từ JSON/user text như quoting an toàn;
  tránh backticks, `$()` hoặc command-building làm chạy nội dung không chủ định.
- Không thay execution policy/global trust/firewall để một lệnh tài liệu chạy.
  Nếu `.ps1` shim bị chặn và có `.cmd` tương đương hợp lệ, dùng shim đó.
- Background helper không mở cửa sổ nếu không cần tương tác; PID/cleanup rõ.
  Không để process thử nghiệm/stream tiếp tục vô hạn sau tác vụ.

## Lệnh chạy và dependency

Khi scaffold, định nghĩa lệnh thực trong README/pyproject/package.json và khóa
version/package manager. Các ví dụ sau chỉ áp dụng sau khi file/tool tương ứng
đã có; chọn lệnh đã cấu hình trong repo thay vì đoán tên script/service:

| Kiểm tra | Ví dụ có điều kiện |
| --- | --- |
| Python unit/integration | `python -m pytest` trong backend env đã cài |
| Python lint/type | Ruff/type checker theo pyproject đã chọn |
| Frontend lint/type/test/build | Scripts tương ứng trong package.json và package manager đã khóa |
| E2E | Runner Playwright đã cấu hình, app+DB test profile sẵn sàng |
| Compose validate | `docker compose config --quiet` với compose/env test hợp lệ |
| Migration | Alembic/script thực của dự án trên DB test đã xác minh |
| Benchmark | CLI/script dự án với dataset manifest, seed/config/version đã khóa |

Không cài thêm tool chỉ để chạy lệnh tưởng rằng repo có sẵn. Không in đầy đủ
`docker compose config` nếu substitution chứa secret. CI tương đương local:
install từ lockfile, lint/type/build, tests cần thiết và migration check.
Test profile dùng dữ liệu/DB disposable được chỉ rõ; không dùng URL production.

## Docker Compose và cấu hình

API/worker cùng code/version, process riêng, PostgreSQL durable volume. Cấu
hình env có `.env.example` placeholders, schema/bounds và startup validation.
Không embed secrets; bind ports đúng môi trường, DB nội bộ/local theo nhu cầu.
Healthcheck/readiness cho DB/API/worker; startup không giả depends_on là đủ để
DB sẵn sàng. Migration có một owner/step rõ, không hai service cùng chạy DDL.

Pin image/dependency phù hợp phiên bản đã kiểm tra. Giới hạn tài nguyên/retry
và graceful shutdown; worker kết thúc boundary an toàn hoặc replay được.
Không chạy `docker compose down -v` để “sửa” lỗi mà mất ledger/truth/metrics.
Đóng/mở run, retry/replay và reset dataset phải có scope thao tác riêng.

## Observability và phục hồi

Log cấu trúc: request_id/job_id/run_id/analysis_version, order, detector/rule,
duration/status/error code; che secrets và không log truth vào scoring pipeline.
Metric: ingest count, rejection reason, outbox backlog, checkpoint lag, retries,
worker error, throughput, alert latency, graph budget/truncation, cache, model
availability và RAM. Không dùng high-cardinality wallet/tx_hash làm metric label.

Readiness phân biệt API sống với DB/worker/model sẵn sàng; baseline không ML
không bị coi như model outage. Backup PostgreSQL/config/feed/models và artifacts
cần replay; kiểm restore vào môi trường tách biệt. Graph dựng lại từ ledger;
không chỉ backup RAM cache. Quy trình recover nêu checkpoint/version và cách
kiểm invariants/dedup sau restart. Chỉ mở rộng storage/engine sau đo bottleneck.

## Bàn giao

README lệnh thực, lockfiles, Compose, migrations/contracts, config/seeds,
versioned rulebook/score, fixtures/test report, raw measured metrics, demo,
kiến trúc/phương pháp/kết quả/giới hạn. Không gọi repo “production ready” khi
chưa kiểm auth/backup/recovery/migration và chất lượng thực của pipeline.
