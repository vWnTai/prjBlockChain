# 08 — Kiểm thử, đánh giá độc lập và benchmark

Áp dụng cho thay đổi nghiệp vụ, evaluator, rule/model/version và công bố kết quả.
Nguồn: mục 5 của [kế hoạch](../../Ke-hoach-AML-Blockchain.md).
Danh sách đủ test IDs ở [requirements map](../requirements-map.md).

## Kiểm thử phù hợp thay đổi

- Unit: integer money parser, nonce/fee/balance, canonical golden hashes,
  windows/order, rules, allocation conservation, scores/floors/half-up.
- Integration với PostgreSQL thật: constraints/FKs/run isolation, ledger+outbox
  atomicity, concurrency, replay/checkpoint, assessment history, migrations.
- Contract/API: DTO money string, validation/bounds, pagination/as_of, errors,
  RBAC, job lifecycle, SSE reconnect/resync/dedup và review concurrency.
- Frontend: exact money render, timeline/run switching, stale request, states,
  evidence highlight, roles, keyboard access. E2E cho luồng người dùng chính.
- Benchmark khi thay performance path hoặc phát hành mốc benchmark; không chạy
  D-stress cho thay đổi CSS hoặc sửa typo. Tài liệu thuần túy kiểm links/consistency.

Mỗi detector cần positive, boundary, negative, confounder và temporal cases.
Các test có invariant và oracle độc lập, không copy nguyên implementation làm
expected result. Không đặt coverage phần trăm tùy ý thay cho kiểm hành vi quan
trọng; không skip, xóa assertion hay sửa label để khiến bộ test xanh.

## Phục hồi và determinism

Inject lỗi trước commit ledger, sau commit trước consume, giữa assessment và
checkpoint, sau DB failure khi graph RAM đã apply, duplicate delivery và worker
restart. Assert không mất work, không nhân edge/score/alert/exposure, checkpoint
đúng và rebuild giống full replay. Kiểm hai run có ID giống nhau ở scope khác.

Assert tổng supply, 0<=allocation<=balance, source portions không trùng,
self-transfer/cycle/convergence không tạo tiền. Cùng seed/config/versions cho
ledger hashes/counts/scores đúng kỳ vọng; loại UUID/observed_at/runtime khỏi
deterministic comparison theo contract. Rule/feed mới giữ assessment version cũ.

## Chống leakage

- Feature/query graph chỉ đến as_of order; cùng timestamp không đọc tx_index sau.
- Feed biết ở tương lai không dùng as-known; hết hiệu lực/network khác không match.
- Truth ở evaluator riêng; tests thay label/actor/campaign mà giữ ledger+TI và
  kiểm predictions giống nhau. Kiểm cả suppression/metadata không leak.
- Train/validation/test split theo run/campaign/actor/seed/variant group, không
  random chia từng tx khiến cùng chiến dịch đi vào hai split.
- Scaler, quantile, anomaly thresholds và detector tuning chỉ train/validation.
  Khóa test trước đo; không tuning bằng seed test hoặc loại confounders khó.
- Không dùng future reviews làm oracle feature; retrospective được báo riêng.

## Dataset và split

| Bộ | Quy mô khởi tạo |
| --- | --- |
| D-smoke | Khoảng 500 ví / 5.000 giao dịch, integration |
| D-standard | Khoảng 10.000 ví / 100.000 giao dịch, >=7 ngày simulated time |
| D-stress | Tới 1.000.000 giao dịch; graph window/RAM bounded |

60% independent runs train, 20% validation, 20% test; seed/address/actor/campaign/
variant group không trùng split. Có temporal holdout trong run để đo distribution
shift. Nếu deterministic address reuse phá disjoint split, sửa namespace/seed
generation theo ADR; không chỉ chứng minh run_id khác nhau.

Test prevalence 1%, 5%, 10%; known TI source coverage 0%, 50%, 100%; ít nhất 5
seed test. Báo cả no-blacklist và payroll/custody/treasury/giống hình thái hợp lệ.
Trung bình/dispersion, bootstrap theo run/campaign cho CI, không giả tx độc lập.
Giữ manifest seeds/configs/versions/split hashes; truth chỉ evaluator đọc.

## Đơn vị đánh giá và matching

Transaction online chỉ dùng prediction tồn tại ở order đang xét. Không gán nhãn
hồi cứu cho đầu chuỗi để tăng online recall. Báo retrospective transaction metrics
riêng nếu đánh dấu lại toàn bộ evidence sau phát hiện.

Campaign: alert cùng pattern và evidence khớp >=50% core tx của campaign theo
matching đã khóa trước test. Match một-một, dedup alerts/campaigns; multi-label
có cách tính theo pattern rõ. Ghi onset, đủ evidence theo rule và detected_at
để tách thời gian phải quan sát khỏi xử lý chậm. Ground truth có onset/completion
nhưng không được truyền ngược cho detector trong lúc scoring.

## Metrics phải công bố

TP/FP/FN/TN và mẫu số theo unit; precision, recall, F1/macro-F1 theo pattern,
FPR, Average Precision/PR curve, alerts/1.000 tx, duplicate rate; delay từ onset
và delay từ evidence completion. Throughput, p50/p95 latency và peak RAM theo
cấu hình máy/workload. AP không tự đồng nhất với mọi cách tích phân PR-AUC.
Mẫu số 0 phải nêu undefined/not applicable theo policy, không tự gán 100%.

Không dùng accuracy làm bằng chứng chính. Prevalence p ảnh hưởng precision:
`precision=recall*p/(recall*p+FPR*(1-p))`. Với p=1%, recall=90%, FPR=1%,
precision khoảng 47,6%; kiểm mẫu số trước khi công bố target hoặc kết quả.

Mục tiêu của kế hoạch, chỉ đánh dấu đạt sau đo:

- Direct blacklist precision/recall 100% trên valid known-feed exact-match fixture.
- Campaign recall>=85% mỗi pattern trên bộ chuẩn, báo variants khó và CI.
- Retrospective transaction tại prevalence 1%: recall>=85%, FPR<=0,2%,
  precision khoảng>=81% nếu đúng mẫu số; online độc lập.
- Rule+graph >=100 tx/s ở D-standard trên 8 logical CPU/16 GB RAM.
- Alert p95<=2s sau indexing tx hoàn thiện evidence; báo simulated block time riêng.
- Dashboard query p95<=1s cho <=1.000 nodes/3.000 edges, hot/cold cache riêng.

## Ablation và báo cáo

B0 blacklist; B1 local rules; B2 rule+temporal graph; B3 B2+Isolation Forest.
Dùng cùng test split, so sánh cùng FPR hoặc cùng alert budget; báo mỗi pattern
và latency/RAM. ML không cải thiện rõ unseen runs thì giữ B2 và báo trung thực.
Phân tích sensitivity haircut có thể dùng fixture nhỏ/giả định khác nhưng không
dùng hidden labels để chọn allocation trong online prediction.

Báo cáo theo [mẫu benchmark](../templates/benchmark-report.md), chứa source commit
nếu có, Python/Node/DB/dependency versions, CPU/RAM/OS, config/seed/version,
định nghĩa thời gian đo, warmup/repeats/sample count, raw metrics và hạn chế.
Tách target/measured, cache hot/cold, simulated time/wall clock. Không gọi kết quả
trên vài fixture nhỏ là benchmark 100k tx hoặc chất lượng trên dữ liệu thực tế.
