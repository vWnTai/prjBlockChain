# 07 — Bảo mật website, phân quyền và audit

Áp dụng cho auth, endpoint ghi dữ liệu, review, import/export, feed/config và
chuẩn bị triển khai. Nguồn: vai trò/RBAC/schema-validation/audit trong mục 4
của [kế hoạch](../../Ke-hoach-AML-Blockchain.md). Chi tiết còn lại là chuẩn kỹ thuật bổ sung.

## RBAC và data scope

| Vai trò | Quyền sản phẩm theo kế hoạch |
| --- | --- |
| Viewer | Đọc dữ liệu/graph/alerts/metrics trong scope được cấp |
| Analyst | Quyền đọc và review alert; không sửa feed/config hoặc engine history |
| Admin | Quản trị feed/config và các thao tác quản trị được contract cho phép |

Quyền tạo run/replay/export/quản lý người dùng phải được chốt rõ trong ADR,
không suy ra Analyst có mọi quyền ghi. Backend kiểm tra auth/role/scope ở mọi
resource và SSE connection; UI hiding không thay authorize. Run isolation và
authorization là hai lớp khác nhau: đúng run_id chưa có nghĩa được quyền xem run.
Không tin actor_id/role do client body cung cấp; actor lấy từ identity xác thực.

## Authentication/session

Chốt session/cookie/token và user source trước tính năng auth. Không tự tạo
crypto/token protocol. Nếu có password, dùng thư viện password hashing phù
hợp, rate limit và không lưu/plaintext/log password. Không hardcode account
admin/mật khẩu mặc định vào source hoặc bypass role bằng query parameter.

Cookie auth cần HttpOnly/Secure theo môi trường, SameSite và CSRF cho request
ghi. CORS theo allowlist, không wildcard credentials. Token auth có expiry,
server validation và storage policy; không giải quyết SSE bằng token URL.
Local demo profile nếu cần phải rõ, bind local và không được đem bypass auth
sang môi trường truy cập từ bên ngoài.

## Input, SQL, XSS và import

- Validate DTO, config và feed theo schema, bounds, enums và version.
  YAML dùng safe parsing; không eval/exec/user expression hoặc deserialize
  object tùy ý. Không nhận Python/JS/SQL để tạo rule.
- Query SQL có tham số; sort/column names thuộc allowlist. Không chèn string
  address, search, cursor hoặc filter vào SQL.
- Notes, source_name/ref và imported metadata là text không tin cậy.
  React escape text; tránh raw HTML. Nếu có Markdown/rich text, sanitize theo
  allowlist. Links chỉ schemes phù hợp, không javascript/data từ input.
- Import có size/count/range/duplicate checks, transaction boundary và báo lỗi
  theo record; kiểm provenance/version/validity. Không fetch URL tùy ý từ feed.
- Nếu được yêu cầu external fetch, giới hạn scheme/host/redirect/time/size;
  không cho truy cập internal/metadata endpoints hoặc đường dẫn ngoài workspace.
- Upload/export paths không lấy trực tiếp filename/path user để ghi file;
  normalize/resolve và giới hạn thư mục đích, tránh traversal và ghi đè artifact.
- CSV export escape cell bắt đầu dấu công thức nguy hiểm theo policy, giữ raw
  money contract và không vô tình xuất secret/truth cho Viewer.

## Secrets và dependencies

Secret dùng biến môi trường/secret store của môi trường; `.env.example` chỉ
placeholder. Không commit `.env`, credential, private key, DB dump nhạy cảm hoặc
file auth Codex. Không đọc/in toàn bộ environment hoặc config credential để debug.
Log che Authorization/Cookie/token/password/connection secrets. Không đưa secret
vào Vite/frontend env vì frontend bundle là public.

Dependency khóa version/lockfile, kiểm nguồn package và các vấn đề bảo mật khi
được bổ sung/cập nhật; chỉ thêm công cụ cần cho scope. Model artifact chỉ từ
nguồn build tin cậy, checksum/version rõ; không load pickle/joblib từ upload tùy ý.

## Resource limits và công khai dữ liệu

Rate/concurrency/budget cho create run, replay, graph/tracing và export; timeout,
cancellation/backpressure để không kiệt CPU/RAM/DB. Limits enforced server-side;
có error hoặc partial/truncated rõ. Không đưa DB/worker port ra public vì demo.
Dữ liệu tổng hợp là mặc định; dùng địa chỉ thật hoặc dữ liệu người dùng là thay
đổi scope có yêu cầu riêng, không nạp trong quá trình scaffold.

## Audit

Feed/config/review/role changes ghi actor, action, target/run, before/after hoặc
version, timestamp UTC, reason/request correlation. Record không chứa secret
hoặc truth bị cấp sai quyền. Config/TI version cũ phải đủ replay; không edit
nguồn cũ để diễn giải lại score quá khứ. Bảo vệ audit khỏi chỉnh sửa bằng endpoint
review thông thường; retention/access policy được chốt khi vận hành.

Trước triển khai ra ngoài: kiểm profile auth, listeners, CORS, TLS/reverse proxy,
secret provisioning, backup/recovery và quyền hệ thống. Thực hiện trong phạm vi
người dùng đã cho phép; không tự publish site hay mở firewall khi chỉ được giao code.
