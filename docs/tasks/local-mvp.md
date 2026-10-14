# Local MVP — baseline B2 đã kiểm chứng

Yêu cầu: source theo kế hoạch, khung local hoàn chỉnh, Docker Desktop, push main
và tạo develop/dev-sec. Repository từ xa ban đầu trống. Docker Desktop hoạt động;
host có Node 24, không có Python thực; Python chạy trong container.

Giữ PostgreSQL theo kế hoạch. Quyền MySQL đã có nhưng không có yêu cầu đổi DB;
không đụng database khác. GitHub Credential Manager đã có tài khoản vansec0812.

- [x] Domain ledger/generator/rules/tracing/scoring với fixtures độc lập.
- [x] PostgreSQL migrations, outbox/checkpoint/jobs, evaluation schema riêng.
- [x] API session/RBAC/CSRF, contracts, review, graph, metrics, SSE.
- [x] Dashboard React/Cytoscape, workflow thực, money chính xác/timeline.
- [x] Docker local start, test/build/integration/E2E, recovery và số liệu thực.
- [x] README/rules/contracts/ADR, lockfiles và CI cho main/develop/dev-sec.

Bằng chứng: [báo cáo local](../reports/local-validation.md), 44 test cases passed,
smoke 5.000 giao dịch/restart/replay, raw metrics và ảnh graph thực. Nhánh bàn giao
theo yêu cầu: main, develop, dev-sec; xác minh remote refs khi push.

Scope: baseline B2; optional Isolation Forest chưa thuộc lần bootstrap này.
Không tuyên bố mục tiêu benchmark 100k/split 5 seed đạt khi chưa đo. Giữ T01–T22
và yêu cầu web trong requirements map; báo đúng test nào đã thực hiện.
