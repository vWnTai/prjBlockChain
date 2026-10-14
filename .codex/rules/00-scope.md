# 00 — Phạm vi và tính trung thực của sản phẩm

Áp dụng khi chốt tính năng, sửa requirement, viết nội dung UI hoặc báo cáo.
Nguồn: mục tiêu, phạm vi và mục 1–5 của [kế hoạch](../../Ke-hoach-AML-Blockchain.md).

## MVP bắt buộc

- Mạng account-based giả lập; mỗi run có một network và tài sản `SIM`, decimals=6.
- Tạo nền giao dịch hợp lệ và chiến dịch Structuring/Smurfing, Peeling,
  Mixing, Rapid Movement có nguồn TI; giữ ground truth độc lập.
- Ledger hợp lệ, hash chain, indexer/outbox, temporal features/graph, engine
  rule + tracing, score, assessments, alert/evidence và review history.
- API và dashboard phục vụ Simulation Control, Graph Explorer, Alert & Evaluation.
- Evaluator với split độc lập, test fixtures, số liệu thực đo và replay tái lập.
- Baseline rule + graph là sản phẩm chính trước khi thêm Isolation Forest.

## Giới hạn không được tự thay đổi

Simulator không tái hiện EVM, chữ ký, đồng thuận PoW/PoS hoặc P2P security.
`sim-sha256-v1`, `state_checksum` và `simulated_final` phải được gọi đúng tên,
không mô tả là Ethereum tx hash/state root/finality thật.

UTXO, Hardhat adapter, EVM contracts, token/internal transfer, reorg,
cross-chain/bridge và GNN là mở rộng riêng. Chỉ triển khai khi nằm trong yêu cầu
được giao, có schema, data contracts, test và quyết định kiến trúc tương ứng.
Không thêm ví crypto thật, ký/chuyển tiền thật hoặc private keys vào MVP.

## Ý nghĩa kết quả

- Dùng nhãn “nghi vấn mẫu …”, “ưu tiên xem xét”, “phơi nhiễm theo mô hình”.
- Score không phải xác suất hoặc kết luận pháp lý. Không đặt tên field/UI như
  `criminal_probability` hoặc coi alert là bằng chứng phạm tội.
- Ngưỡng `T`, rule và điểm là tham số thí nghiệm; không quảng bá thành ngưỡng
  pháp lý. Không đưa tư vấn pháp lý mới vào sản phẩm nếu chưa có yêu cầu xác minh.
- Một topology có thể vừa là dịch vụ hợp lệ vừa giống chiến dịch giả lập.
  Giữ false positives trong kết quả và cho analyst review.
- Engine MVP giám sát sau final; không hoàn tác/chặn ledger. Nếu được yêu cầu
  policy trước phát intent, lưu policy decision riêng với AML assessment.

## Quản lý yêu cầu

Gắn thay đổi với mục kế hoạch và ID trong [requirements map](../requirements-map.md).
Chi tiết kế hoạch chưa nêu phải được phân biệt với bổ sung kỹ thuật. Quyết định
đổi ý nghĩa nghiệp vụ cần ADR và quyền phù hợp; lựa chọn triển khai routine có
thể chốt trong phạm vi tác vụ, không yêu cầu duyệt cho mọi dependency/module nhỏ.

Không sửa kế hoạch gốc như một tác dụng phụ của việc code. Khi người dùng yêu cầu
đổi kế hoạch, cập nhật các tài liệu phụ thuộc và ghi rõ tác động đến version/test.
Các mốc 6 tuần cho nhóm hoặc 8–10 tuần một người là ước lượng, không phải deadline
đã được cam kết. Mục tiêu performance/recall chỉ là mục tiêu cho tới khi có số đo.
