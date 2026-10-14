# ADR-0001 — Khung local B2

Trạng thái accepted, 15/10/2026. D01–D16 được cụ thể hóa cho baseline dưới đây;
D09 ML deferred. Stack theo kế hoạch: Python 3.12/FastAPI/SQLAlchemy/Alembic,
PostgreSQL 17, NetworkX, React/TypeScript/Vite/Cytoscape, Node 24, Compose.
Phiên bản packages được khóa trong requirements.lock/package-lock.json.

Database owner chỉ migration. aml_app chỉ public schema, không đọc evaluation.
aml_evaluator đọc public và ghi truth schema riêng. API không có evaluator DSN.
Worker generator/evaluator sử dụng connection riêng; AML pure không nhận truth.

Hash canonical JSON sorted keys, separators không khoảng trắng, ASCII neutral
addresses/UTF-8, money strings; SHA256 hex; Merkle leaf=raw tx hash bytes, odd
leaf duplicate, empty root=SHA256(empty bytes). Checksum sorted address/balance/
nonce; run UUID/observed_at không tham gia. Genesis 2026-09-08T00:00:00Z.

Order strict height/index; cutoff height (cuối block) hoặc height+index. TI
known_at<=event analysis as_of_time, validity [valid_from,valid_to); replay mới
giữ snapshot feed/mode và version riêng. Direct counterparty=max(confidence×severity).
Baseline A=0/model_status=not_configured, giữ nguyên trọng số/floors/half-up.

Haircut: integer largest-remainder apportionment trên các phần vốn rời nhau,
rút value rồi fee; ties deterministic. Full spend phân bổ hết, không để remainder
trên balance=0. Provenance paths bounded 5 hop; vốn vẫn bảo toàn khi path hết scope.
System wallet không nhận user intent; fee_sink chỉ thu fee, không edge AML.

Job queued/running/completed/failed; PostgreSQL advisory lock một worker local;
restart requeue running jobs, rebuild state từ ledger/checkpoint và replay idempotent.
Không có pause/cancel UI. Replay tạo analysis version mới trên ledger cũ.
Episode: detector+anchor+analysis_version, đóng sau 30 phút event-time im lặng;
mixing regions chồng lấn được gom khi vùng candidate mở rộng. Evidence union và
snapshot theo order; crossing clock bucket không tự tạo alert mới.

Cookie signed HttpOnly/SameSite=Lax 8h, CSRF header; password Argon2. Tài khoản
local admin/analyst/viewer dùng mật khẩu random .env. Admin create/replay/feed;
Analyst/Admin review; Viewer read. Review open/in_review/closed với revision conflict.
App local single-user installation, roles cùng scope runs; chưa đa tenant.

SSE durable events có ID; reconnect replay hoặc resync; query limits server;
cursor transaction là global order offset kèm run/version/filter signature.
Campaign matching theo pattern/core>=50%, one-to-one; zero denominator=null.
Online metrics và evidence retrospective metrics tách. Chưa chạy full train/test
split nghiên cứu; per-run demo metrics không đại diện unseen-run quality.
