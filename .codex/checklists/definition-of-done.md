# Definition of Done — Tiêu chí hoàn thành theo phạm vi

Đây là mẫu checklist; kết quả phiên bản local ở [báo cáo](../../docs/reports/local-validation.md). Chọn phần áp dụng cho task;
đánh dấu N/A kèm lý do thay vì chạy mọi kiểm tra cho sửa tài liệu nhỏ.
Nguồn: [kế hoạch](../../Ke-hoach-AML-Blockchain.md) và [requirements map](../requirements-map.md).

## Mọi thay đổi

- [ ] Scope/yêu cầu và file bị ảnh hưởng rõ; không ghi đè thay đổi người dùng.
- [ ] Rule/doc liên quan được đọc; không có mâu thuẫn mới với kế hoạch gốc.
- [ ] Không secret, nhãn truth rò vào pipeline hoặc tuyên bố kết quả chưa có.
- [ ] Diff tự review, kiểm tra phù hợp có lệnh/kết quả và limitation trung thực.
- [ ] Tài liệu/contract/task cập nhật khi hành vi đổi; links/file names đúng.

## Ledger / generator

- [ ] Money chính xác end-to-end; genesis supply/fee_sink/balance/nonce đúng.
- [ ] Self-transfer/cycles/convergence, rejected intents và fee đều có semantics đúng.
- [ ] Canonical hashing/golden vectors/version và cùng-seed determinism pass.
- [ ] Generator có background/confounders/campaigns hợp lệ và truth riêng.
- [ ] Ledger+block+outbox nguyên tử; concurrency và replay không apply hai lần.

## Database / worker

- [ ] Run-scoped PK/FK/unique/query; asset/network isolation và bounds đúng.
- [ ] Migration trên PostgreSQL thật từ empty/data cũ, compatibility/recovery rõ.
- [ ] Outbox retry/checkpoint/RAM rebuild nhất quán và crash tests phù hợp pass.
- [ ] Assessment/alert/review history/version/dedup đúng, index/cache có scope.

## AML / graph / ML

- [ ] Positive/boundary/negative/confounder cho detector và T01–T22 liên quan pass.
- [ ] No future/ground-truth leakage; order cùng timestamp được kiểm.
- [ ] Temporal path/haircut conservation, dust, self-transfer/cycle/convergence đúng.
- [ ] TI exact network/address, known_at/validity/source/version/mode đúng.
- [ ] Blend/components/floors/half-up/severity dùng chung và có fixtures.
- [ ] Evidence/threshold/source/amount/hop/detected_at/as_of/version truy xét được.
- [ ] Partial/truncated/unavailable đúng; baseline A=0 không chia lại trọng số.
- [ ] Nếu có ML: artifact/features/splits/quantiles/random_state/version đã khóa.

## API / UI

- [ ] DTO money strings/order/version, errors/bounds/pagination/as_of đúng.
- [ ] Backend RBAC/data scope, audit/review concurrency được kiểm.
- [ ] Durable job, SSE reconnect/dedup/resync/auth/backpressure đúng.
- [ ] Ba màn hình hoạt động với API thật; demo mocks ghi rõ nếu còn dùng.
- [ ] Timeline/score lịch sử không lấy tương lai; evidence click highlight đúng.
- [ ] Exact large money, loading/empty/error/offline/partial và stale-request đúng.
- [ ] Graph bounded; keyboard/labels/text severity/responsive được kiểm trực tiếp.

## Evaluation / release MVP

- [ ] D-smoke, D-standard và D-stress trong scope có manifest tái lập.
- [ ] Split 60/20/20 độc lập, >=5 seed test, prevalence/TI coverage/confounders báo đủ.
- [ ] Online vs retrospective vs campaign metrics riêng, matching đã khóa.
- [ ] TP/FP/FN/TN/mẫu số, per-pattern/AP/FPR/alert burden/delay/RAM/latency có số đo.
- [ ] B0–B3 ablation theo phần đã triển khai; ML không có thì ghi N/A, không bịa B3.
- [ ] Target và measured tách; môi trường/warmup/cache/time definitions được công bố.
- [ ] Source/lockfiles/Compose/migrations/contracts/config/seeds/rulebook/fixtures/
  reports/raw metrics/demo/kiến trúc/phương pháp/giới hạn đầy đủ.
- [ ] Auth/security/backup/restore/migration/recovery/readiness kiểm theo đích release.
- [ ] Publish/deploy trong quyền đã cấp và có artifact/môi trường cụ thể.
