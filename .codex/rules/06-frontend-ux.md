# 06 — React dashboard, graph explorer và chất lượng trải nghiệm

Áp dụng cho website, UI copy, graph render, forms, timeline và API client.
Nguồn: mục 4 của [kế hoạch](../../Ke-hoach-AML-Blockchain.md).
Accessibility, error states và responsive dưới đây là chuẩn kỹ thuật bổ sung.

## Ba màn hình chính

| Màn hình | Yêu cầu |
| --- | --- |
| Simulation Control | Form config/seed có validation; tạo run; xem config/versions/progress; replay analysis; lỗi job và trạng thái SSE rõ |
| Graph Explorer | Chọn run/center/time/hops/as_of; node/edge đúng hướng; tiền/time/order; filter, inspect wallet/tx và highlight evidence |
| Alert & Evaluation | List/filter/detail, reason/threshold/score/source/evidence/coverage; review history; online/retrospective metrics và benchmark metadata |

Điều hướng lưu run và filter hợp lệ trong URL/state; chuyển run phải reset
selection/cursor/graph/history phù hợp. Deep-link resource luôn có run scope.
Không thêm trang token trade, marketplace, wallet signing hoặc blockchain thật.
Demo mock, nếu dùng khi API chưa có, phải hiện rõ “dữ liệu minh họa” và không
được dùng làm bằng chứng rằng backend/benchmark đã chạy.

## Tiền và dữ liệu chính xác

Giữ money string hoặc BigInt xuyên suốt. Formatter tách chuỗi nguyên thành
SIM với 6 chữ số, locale tiếng Việt ở presentation. Không dùng parseFloat,
Number(value_base), toFixed hoặc chart library numeric conversion cho raw money.
Input người dùng chuyển SIM→base unit chính xác theo chuỗi; >6 decimal phải
báo lỗi hoặc theo policy đã chốt, không âm thầm làm tròn. BigInt khi JSON phải
serialize thành chuỗi. Test boundary T và số vượt 2^53 ở parse/render/filter.

Nếu chart cần scale số thực, chuyển bản sao có đơn vị/scaling được ghi rõ;
tooltip/detail giữ amount chính xác. Không dùng giá trị scale để tính lại score
hoặc evidence. Date display có timezone label; API UTC, UI có thể local theo
preference nhưng time filtering/as_of phải chuyển đúng và kiểm tra ở server.

## Graph và timeline

- Cytoscape chỉ render/interaction. Backend chấm AML và cung cấp evidence.
- Giới hạn mặc định <=1.000 node/3.000 edge, tải thêm theo vùng; trạng thái
  truncated/partial và cách thu hẹp/tải tiếp rõ ràng. Không layout full graph.
- Giữ edge song song/direction, tx_hash và chọn được từng giao dịch. Khi gộp
  visual edges, mở được danh sách cạnh gốc và evidence không bị lẫn.
- Risk node hiển thị score/severity, assessed_at/as_of và analysis_version.
  Blacklist badge chỉ từ TI hợp lệ, tách khỏi engine score/service metadata.
- Click alert highlight đúng path/tx IDs cùng run, order và version; side panel
  chứa observed value, threshold, source/confidence, amount/hop, components/floors.
- Timeline chỉ dùng ledger và assessments sẵn có tại cutoff đã chọn. Không lấy
  current score hoặc alert phát hiện sau cutoff rồi tô như đã biết từ trước.
  Retrospective overlay, nếu có, phải explicit và phân biệt mode.
- Chuyển run/filter/timeline thì abort request cũ và không cho response muộn
  overwrite selection mới. Cache keys có run/as_of/version.
- Có loading, empty, failure, offline/reconnecting và partial states riêng.
  “Không có alert” không đồng nghĩa “an toàn” hoặc “đã phân tích đủ”.

## Tương tác và quyền

Forms có labels, defaults theo config thực, field error và submit progress.
Prevent double submit, xử lý retry theo idempotency server. Chỉ hiển thị action
đúng role nhưng luôn dựa backend authorize. Review có status/comment/audit
feedback; conflict do review đồng thời phải hiển thị dữ liệu mới và cho xử lý.
Không tạo optimistic score hoặc xóa alert khỏi history trước server xác nhận.

## Accessibility và responsive

- Dùng HTML semantic, focus rõ, keyboard navigation; input có label, bảng có
  headers, button có accessible name, thông báo async phù hợp screen reader.
- Không dùng màu làm dấu hiệu duy nhất; severity có text/icon/legend. Đồ thị
  có bảng/list evidence tương đương để thao tác không bắt buộc mouse.
- Desktop cho graph + inspector, tablet/mobile có panel thu gọn và filter
  truy cập được; không để action quan trọng bị cắt hoặc scroll ngang toàn trang.
- Typography/khoảng cách/các trạng thái nhất quán; dark/light chỉ triển khai
  nếu nằm trong scope. Respect reduced-motion, không animation quá nhiều trên graph.
- Bảng dữ liệu có pagination/virtualization khi cần; graph updates batch, tránh
  re-layout mọi event; cleanup Cytoscape instance/listeners/EventSource khi unmount.

## Hiển thị kết quả có trách nhiệm

Score 87 là ưu tiên 87/100; không viết “87% rửa tiền”. Hiển thị “nghi vấn mẫu…”
và giả định tracing. Metrics có pattern/dataset/split/seed/version/sample count,
online hoặc retrospective, measured hay target. Không dùng progress giả, số
liệu random hoặc biểu đồ trang trí để mô tả benchmark chưa được thực hiện.
