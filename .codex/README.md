# Bộ quy tắc phát triển website AML Blockchain

Phiên bản tài liệu: `1.0.0` — ngày 15/10/2026 (Asia/Saigon).
Nguồn nghiệp vụ: [Ke-hoach-AML-Blockchain.md](../Ke-hoach-AML-Blockchain.md),
bản kế hoạch ngày 08/09/2026. Khi khởi tạo, repository chỉ có kế hoạch; không có
source code ứng dụng, Git metadata, dependency lockfile hoặc bộ test.

## Cách nạp hướng dẫn

[AGENTS.md](../AGENTS.md) tại root chứa các bất biến và bảng định tuyến đến rule.
[agent.md](../agent.md) là sổ tay vai trò; [config.toml](config.toml) khai báo tên
fallback `agent.md` và giới hạn discovery 32 KiB. Codex chọn tối đa một file
hướng dẫn trong mỗi thư mục, ưu tiên override rồi `AGENTS.md` rồi fallback.
Các quy tắc Markdown được đọc theo chỉ dẫn trong `AGENTS.md`; liên kết không
đồng nghĩa nội dung file tự được chèn vào context.

Thư mục `rules/` ở đây chứa chuẩn lập trình dạng `.md`. `.rules` là định dạng
khác để kiểm soát lệnh ngoài sandbox. Bộ này không tạo command allowlist hoặc
thay đổi quyền của máy. Project config chỉ được client nạp khi dự án được trust;
việc trust là trạng thái client, không được tự ý sửa trong thiết lập tài liệu.
Không đổi `CODEX_HOME` thành thư mục `.codex` của repo.

Tham chiếu cơ chế: [OpenAI Docs — AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md),
[Config basics](https://learn.chatgpt.com/docs/config-file/config-basic),
[Rules](https://learn.chatgpt.com/docs/agent-configuration/rules).
Khởi động phiên mới tại root để client khám phá hướng dẫn vừa tạo.

## Danh mục

| Tài liệu | Nội dung |
| --- | --- |
| [00-scope](rules/00-scope.md) | MVP, giới hạn, thứ tự ưu tiên yêu cầu |
| [01-architecture](rules/01-architecture.md) | Stack, ranh giới module, tổ chức mã và dependency |
| [02-ledger-simulation](rules/02-ledger-simulation.md) | Tiền, genesis, nonce/fee, canonical hash, generator, replay |
| [03-database-contracts](rules/03-database-contracts.md) | Schema, FK/index, atomicity/outbox, versioned contracts |
| [04-aml-graph-scoring](rules/04-aml-graph-scoring.md) | Rules, tracing/haircut, TI, ML, score/floors/evidence |
| [05-api-realtime](rules/05-api-realtime.md) | Endpoint contracts, job, pagination, SSE, errors |
| [06-frontend-ux](rules/06-frontend-ux.md) | Ba màn hình, timeline, Cytoscape, tiền, accessibility |
| [07-security](rules/07-security.md) | RBAC, secrets, validation, import/export và audit |
| [08-testing-evaluation](rules/08-testing-evaluation.md) | T01–T22, leakage, metrics, split, ablation, benchmark |
| [09-repository-operations](rules/09-repository-operations.md) | Git, Windows, CI, Docker, observability và phục hồi |
| [10-docker-local](rules/10-docker-local.md) | Stack local, credentials, privileges, migration/health, recovery và CI |
| [Requirements map](requirements-map.md) | Truy vết 5 mục kế hoạch, 22 test IDs, mục tiêu và bàn giao |
| [Decision register](decision-register.md) | Điểm phải chốt khi triển khai phần phụ thuộc |
| [Implementation](workflows/implementation.md) | Chu trình tính năng và milestone |
| [Bugfix](workflows/bugfix.md) | Tái lập, sửa, kiểm tra hồi quy |
| [Release](workflows/release.md) | Chuẩn bị và xác minh phát hành |
| [Definition of Done](checklists/definition-of-done.md) | Tiêu chí hoàn thành theo loại thay đổi |
| [Task template](templates/task.md) | Mẫu kế hoạch tác vụ |
| [ADR template](templates/adr.md) | Mẫu quyết định kỹ thuật |
| [Benchmark report](templates/benchmark-report.md) | Mẫu báo cáo số liệu thực đo |

## Bảo trì

- Quy tắc nghiệp vụ dẫn về kế hoạch; không đổi threshold để khớp demo.
- Chuẩn kỹ thuật bổ sung được ghi rõ là bổ sung; mặc định đề xuất phải được chốt
  khi scaffold. Không coi tên đường dẫn/lệnh minh họa là cấu trúc đã tồn tại.
- Khi sửa kế hoạch, đối chiếu requirements map, rules, contracts, fixtures,
  version và decision register. Không cập nhật checksum để che việc chưa đối chiếu.
- Sửa quy tắc ở file chuyên trách; giữ root `AGENTS.md` gọn và bảng định tuyến đúng.
- Mẫu là tài liệu, không phải tính năng đã hoàn thành hoặc test đã pass.

Checksum SHA-256 của kế hoạch tại thời điểm tạo bộ quy tắc:

```text
CC05F86162FE13FA53474DCA104ED6147DFCDC2DE75D4C42479136EE7BC86232
```
