# 03 — Database, hợp đồng dữ liệu và xử lý bền vững

Áp dụng cho model/DTO, query, migration, outbox, checkpoint và cache.
Nguồn: mục 2 và 4 của [kế hoạch](../../Ke-hoach-AML-Blockchain.md).

## Cách ly run và schema

PostgreSQL là source of truth. Các thực thể theo run dùng PK/FK ghép `(run_id,id)`;
mọi query/update/join và cache đều mang run_id. Không chỉ kiểm tra ID tồn tại
toàn cục. Một run chỉ một network/asset; amount của asset khác phải bị từ chối
trong MVP. `TIMESTAMPTZ` cho thời gian, `NUMERIC(78,0)` cho tiền.

| Thực thể | Ràng buộc cần giữ |
| --- | --- |
| simulation_runs | Seed, model network, asset/decimals, full config, generator version, genesis time, status/created_at |
| wallets | PK(run,id); UNIQUE(run,address); balance>=0; next_nonce>=0; first/last_seen; is_system |
| blocks | UNIQUE(run,height), UNIQUE(run,block_hash); parent FK cùng run; timestamp/header/checksum/tx_root/count/gas/fees |
| transactions | UNIQUE(run,tx_hash), UNIQUE(run,block_id,tx_index), UNIQUE(run,from_wallet_id,nonce); block/from/to FK cùng run |
| risk_assessments | Run/tx/analysis_version/as_of_order; E/P/V/Q/A/blend/floors/final score; mode, rule/model/feed versions và coverage |
| risk_alerts | Trigger/subject cùng run; detector, reason/snapshot/window/detected_at/version/dedup/coverage; score 0..100 |
| alert_transactions | Nhiều-nhiều alert/evidence tx cùng run; evidence_role và path_order |
| alert_rule_hits | Rule code/version, observed value/threshold, source snapshot; blacklist_rule_id nullable cho heuristic |
| blacklist_rules | Network/address/category, severity/confidence, source/ref, known_at, validity, list_version, enabled |
| outbox_events / worker_checkpoints | Event identity/order/status, durable checkpoint và analysis version |
| analyst_reviews | Lịch sử người thực hiện/status/comment/time; không ghi đè engine history |

`risk_alerts.risk_score` có thể lưu `NUMERIC(5,2)` theo kế hoạch, nhưng final R
của công thức là integer half-up; API/UI dùng cùng semantics. Không nhầm score
database scale với độ chính xác của tiền.

Feed không cần FK đến wallet vì địa chỉ có thể chưa xuất hiện. Match network và
address exact sau normalization; confidence 0..1, severity 0..100,
valid_to>valid_from nếu có. Rule hành vi ở YAML/rule_configs có version, không
nhét threshold motif vào blacklist_rules.

CHECK tối thiểu: value>0, fee/gas price>=0, nonce/height/tx_index/gas>=0,
gas_used<=gas_limit; fee đúng tích trong profile simulator. FK/CHECK không đủ
cho balance conservation, parent height liên tục hoặc order: cần domain logic.

## Atomicity, outbox và checkpoint

- Ledger balances/nonces, block, transactions và outbox phải commit cùng nhau.
- At-least-once delivery; ingestion unique keys và worker idempotency là bắt buộc.
  Work key `(run_id,tx_hash,analysis_version)`; assessment history thêm as_of_order
  để ghi nhận phát hiện sau này mà không overwrite đánh giá online trước đó.
- Durable result, allocation/feature state cần thiết và checkpoint phải nhất
  quán. Nếu graph ở RAM đã apply nhưng DB commit lỗi, dựng lại/rollback state
  đến checkpoint trước retry; không apply lần hai trên RAM bị lệch.
- Checkpoint chỉ tiến sau khi assessment/evidence và processing state được lưu.
  Claim/retry/lease phải tránh hai worker thay đổi state theo hai thứ tự; MVP
  ưu tiên một logical consumer cho mỗi run/version, có khóa/lease rõ.
- Không bỏ event lỗi để giả đã hoàn tất. Lưu failure/retry count, chặn hoặc báo
  job failed khi vi phạm invariant; chỉ retry lỗi tạm thời với budget/backoff.
- Rebuild từ ledger/checkpoint khi restart; graph RAM không được là nơi duy
  nhất lưu exposure allocation hoặc assessment state quan trọng.

## Dedup và history

Ingest dedup khác alert dedup. Alert key dựa `(run_id,detector_code,anchor,
episode_id,analysis_version)`; episode đóng theo quiet-time cấu hình/version.
Chốt canonical anchor/episode trước implement; không dùng hash tùy process.
Evidence mới trong cùng episode bổ sung vào alert, cập nhật last_detected_at
và history; không nhân alert mỗi poll. Dữ liệu version mới không bị dedup mất.
Online assessment, retrospective assessment và analyst decision là ba loại
record khác nhau; giữ chronology để biết lúc nào hệ thống thực sự biết mẫu.

## Query, index và cache

Index khởi tạo: (run,from_wallet,timestamp), (run,to_wallet,timestamp),
(run,block_id,tx_index), alerts(run,status,severity,detected_at),
feed(network,address,known_at). Order-aware query cần tie-break bằng tx_index/
block_height; index bổ sung theo EXPLAIN/bottleneck, không thêm mù quáng.
Cache mang run, asset/network nếu áp dụng, as_of/order, rule/model/feed/analysis
version và query limits; tránh dùng kết quả live mới nhất cho timeline lịch sử.

## Versioned contracts và migration

DTO công khai chứa schema_version và số tiền dạng chuỗi; không serialize ORM
object/truth/secret trực tiếp. Transaction/block fields theo mục 2 của kế hoạch;
nullable fields/defaults/enums/validation phải được mô tả trong contract.
JSONB evidence/source snapshots có schema; không coi dữ liệu tùy ý là an toàn.

Mọi đổi schema có migration được review. Kiểm tra trên PostgreSQL thật từ DB
rỗng và DB có dữ liệu đại diện; SQLite không chứng minh NUMERIC/FK/concurrency.
Schema evolution có kế hoạch backfill, compatibility và rollback/recovery;
không reset DB hoặc sửa migration đã dùng chung để thay cho migration mới.
DDL dài hoặc destructive cần thực hiện theo quyền đã có và môi trường đã xác minh.
