# Báo cáo kiểm thử và benchmark: <tên run/bản phát hành>

Mẫu báo cáo, chưa phải số liệu đo. Báo cáo thực nằm ở docs/reports khi triển khai.
Đọc [08-testing-evaluation](../rules/08-testing-evaluation.md) trước khi điền.

## Phạm vi và kết luận được số đo hỗ trợ

<Pipeline/detector/model đã triển khai, dataset/đơn vị đánh giá, kết quả chính
và giới hạn; không suy rộng từ dữ liệu tổng hợp sang hệ thống thực.>

## Manifest tái lập

| Thuộc tính | Giá trị thực |
| --- | --- |
| Source version | <commit/tag hoặc checksum nếu chưa có Git> |
| Schema/generator/rule/analysis versions | <values> |
| Model/feature/feed versions, mode | <values; baseline/online/retrospective> |
| Dataset/run/seed/config/split manifests | <artifact paths + hashes> |
| OS/CPU/logical cores/RAM | <machine measured> |
| Python/Node/PostgreSQL/dependency versions | <versions từ môi trường đo> |
| Lệnh và thư mục chạy | <lệnh tái lập, không secret> |
| Warmup/repeats/sample counts/cache | <method> |
| Time definitions | <event/simulated time, observed/indexed, evidence completion, wall latency> |

## Kiểm thử hành vi

| ID | Kỳ vọng | Pass/fail/chưa chạy | Evidence/log/test path |
| --- | --- | --- | --- |
| <Txx/Wxx/check> | <assert> | <thực tế> | <artifact> |

## Đánh giá detection

| Dataset/pattern/mode/unit | N, prevalence, TI coverage | TP/FP/FN/TN | Precision/recall/F1/FPR/AP | CI/dispersion |
| --- | --- | --- | --- | --- |
| <online tx / retrospective tx / campaign riêng> | <values> | <values> | <values> | <values/method> |

Nêu campaign matching/core>=50%/one-to-one/dedup/multi-label, zero-denominator
policy và đủ-evidence timestamp. Báo >=5 seed test, hard negatives/confounders,
0% known TI và per-pattern results. Không loại sample khó để target đạt.

## Hiệu năng và alert burden

| Đại lượng / điều kiện | Target kế hoạch | Measured | Samples / hạn chế |
| --- | --- | --- | --- |
| Rule+graph D-standard throughput | >=100 tx/s trên 8 logical CPU/16 GB | <thực đo> | <N/machine> |
| Alert từ indexed evidence completion | p95<=2s | <p50/p95> | <N> |
| Dashboard graph <=1.000 nodes/3.000 edges | p95<=1s | <hot/cold riêng> | <N> |
| Peak RAM / backlog / truncation | <không tự bịa target> | <thực đo> | <conditions> |
| Alerts/1.000 tx / duplicate rate | <budget validation nếu có> | <thực đo> | <definition> |
| Delay onset→alert / sufficient evidence→alert | <báo riêng> | <thực đo> | <event vs wall> |

## Ablation

| Baseline | Same split / FPR hoặc alert budget | Per-pattern recall / precision | Latency / RAM | Nhận xét được số đo hỗ trợ |
| --- | --- | --- | --- | --- |
| B0 blacklist | <conditions> | <values> | <values> | <finding> |
| B1 local rules | <conditions> | <values> | <values> | <finding> |
| B2 rule+temporal graph | <conditions> | <values> | <values> | <finding> |
| B3 B2+Isolation Forest | <values hoặc chưa triển khai> | <values/N/A> | <values/N/A> | <finding> |

## Raw artifacts và hạn chế

<Paths raw metrics/confusion matrix/PR curves/seeds/config/replay/test logs;
giả định haircut, coverage, truncated queries, model outages, failed/chưa chạy
checks, dataset realism và điều kiện không đủ để kết luận.>
