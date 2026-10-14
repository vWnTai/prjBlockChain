# 02 — Ledger, generator, tiền, hash và replay

Áp dụng cho mọi thay đổi số dư, giao dịch, simulator, block hoặc replay.
Nguồn: mục 1–2 và các ca T15–T18/T21 của [kế hoạch](../../Ke-hoach-AML-Blockchain.md).

## Tiền và thời gian

`1 SIM = 1_000_000 base units`; `T=1_000_000_000 base units`.
Money/fee/gas price/balance dùng Python `int`, PostgreSQL `NUMERIC(78,0)`, JSON
chuỗi số nguyên base-10. Kiểm tra giá trị nguyên nằm trong capacity schema;
không cho bool, fraction, NaN, scientific notation hay chuỗi không hợp lệ lọt
qua parser. Khi ORM trả Decimal, chỉ chuyển `int` sau khi xác minh không có phần lẻ.
Mức điểm và feature thống kê có thể dùng số thực; không đưa chúng về ledger money.

Default đề xuất từ kế hoạch: seed=42, block_interval_seconds=12,
max_transactions_per_block=100, asset_decimals=6, trace_max_hops=5,
trace_lookback_hours=24. Khóa toàn bộ config thực dùng, genesis và generator version.
Đồng hồ mô phỏng tách khỏi wall clock benchmark/observed_at. Timestamps UTC có
timezone; order `(block_height, tx_index)` phân biệt transaction cùng timestamp.

## Validate và apply một intent

1. Normalize network/asset/address; xác minh sender/recipient và `value>0`.
2. Xác minh nonce đúng `next_nonce`, gas không âm, `gas_used<=gas_limit`,
   `effective_gas_price_base>=0` và fee đúng tích. Không dùng client fee để bỏ qua phép tính.
3. Xác minh sender có `balance>=value+fee`. Serial hóa apply trong một run hoặc
   dùng locking phù hợp để hai request/worker không cùng tiêu một balance/nonce.
4. Debit sender `value+fee`, credit recipient `value`, credit `fee_sink` bằng fee;
   tăng nonce một lần khi được chấp nhận. Sender=recipient phải chỉ giảm fee;
   dùng tổng delta theo wallet, không overwrite hai bản copy của cùng state.
5. Ghi block/transactions/state/outbox trong cùng database transaction.
   Khi lỗi, rollback toàn bộ và không công bố block giả thành công.

Không balance âm; tổng cung gồm fee_sink không đổi. Fee_sink là ví hệ thống,
không dùng làm candidate/edge chuyển tiền AML thông thường. Intent sai được
lưu log thí nghiệm riêng, không sinh ledger success hoặc edge. MVP chỉ có
status=`success` trong ledger; revert/fee burn thuộc contract adapter mở rộng.
Chốt chính sách giao dịch value với ví hệ thống khi triển khai (decision register).

## Hash và block

- Transaction hash dùng canonical JSON intent: network, sender, recipient,
  value, nonce và gas config; scheme=`sim-sha256-v1`. Không chứa block_hash,
  observed_at, risk score, scenario/truth hoặc run UUID tùy tiện.
- Block header canonical gồm parent, height, timestamp, tx_root,
  state_checksum; không chứa chính block_hash. Parent null tại genesis;
  height liên tục, timestamp không giảm, transaction timestamp khớp block.
- `state_checksum` mô tả ledger sau block; không đặt tên Ethereum state root.
  `tx_hashes` giữ đúng order, tx_count/gas/fees khớp transactions.
- Trước implement hash, chốt key ordering, UTF-8, serialization money, byte/hex
  encoding, Merkle odd leaves/empty root, genesis format và wallet ordering trong
  checksum bằng golden vectors. Không dùng Python `hash()` hoặc object `repr()`.
- Schema/hash đổi thì bump version, giữ khả năng kiểm tra artifact cũ; không
  đổi hash của ledger đã final như tác dụng phụ của sửa detector.

## Generator không làm lộ nhãn

Nền gồm P2P, merchant, payroll, treasury/service sweeps và chuyển ví cá nhân;
amount nhiều phân phối, time có nhịp ngày đêm/burst, reuse ví và giao dịch xen kẽ.
Campaign và nền dùng cùng cơ chế địa chỉ/cấp vốn/fee. Không đặt address/hash như
`mixing_wallet`, `bad_actor`, hoặc mã hóa pattern bằng prefix/range dành riêng.

| Campaign khởi tạo | Ràng buộc generator |
| --- | --- |
| Structuring | 12 lệnh 800–990 SIM trong 30 phút, đều dưới T |
| Smurfing | A → 12 trung gian → B trong 60 phút; đủ vốn và fee ở mọi bước |
| Peeling | 20.000 SIM, 6 tầng, khoảng 8% peel, 1–5 phút/tầng; tối thiểu 2 tx/tầng |
| Mixing | 8 nguồn, 3 trung gian, 2–3 tầng giao dịch chéo, 12 đích; 5–30 phút |
| Rapid | TI hợp lệ, chuỗi nhiều hop, giữ dưới 2 phút/hop, chuyển tiếp phần lớn |

Ví dụ peeling: 20.000 − 1.600 − 2×0,021 = 18.399,958 SIM nối tiếp.
Mixing trừ tất cả phí/số dư giữ lại, chia số nguyên và xử lý phần dư xác định.
Không sinh dataset vi phạm ledger rồi sửa balance hậu kỳ để pattern chạy được.

Truth ở schema/file riêng: run_id, campaign_id, pattern_labels[], tx_hashes[],
actor_id, role, onset_order, completion_order. Cho phép multi-label; không gắn
truth vào DTO, graph attrs, feature inputs, logs hoặc role UI dùng cho detection.
Metadata dịch vụ quan sát được phải từ nguồn độc lập, có thời điểm/nguồn/version.

## Replay và determinism

Ingest đệm block đến muộn/sai thứ tự; worker chỉ tiến dãy liên tục. Khi sửa dữ
liệu đã phân tích, replay từ checkpoint hợp lệ hoặc full replay, không chèn ngầm.
Replay phân tích giữ ledger bất biến, tạo analysis version/job mới; không ghi lại
giao dịch, nonce hoặc số dư lần hai. Chạy lại generator cùng seed/config/version
phải tạo cùng nội dung/hash ledger theo canonical rules đã chốt.

Run UUID, observed_at, job runtime và audit time có thể khác; không dùng chúng
để đánh giá hash determinism. Dùng RNG riêng với seed khóa, iteration order
ổn định; không dựa set ordering, clock máy hoặc RNG toàn cục. Mọi nondeterminism
phải được loại bỏ hoặc ghi rõ và không tuyên bố output tái lập nếu chưa chứng minh.
