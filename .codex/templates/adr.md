# ADR-<số>: <quyết định cụ thể>

Mẫu quyết định. Tài liệu thực nên nằm ở docs/decisions khi triển khai.

- Trạng thái: <proposed/accepted/superseded>.
- Ngày: <YYYY-MM-DD, timezone nếu cần>.
- Requirement/decision IDs: <Rxx/Dxx>; source: <mục kế hoạch>.
- Người thực hiện/quyền quyết định: <phạm vi được giao>.
- Thay thế ADR: <path hoặc N/A>.

## Vấn đề và ràng buộc

<Điểm kế hoạch chưa nêu đủ, invariant phải giữ và các boundary phụ thuộc.>

## Các phương án đã xét

| Phương án | Lợi ích | Chi phí/hạn chế |
| --- | --- | --- |
| <A> | <cụ thể> | <cụ thể> |
| <B> | <cụ thể> | <cụ thể> |

## Quyết định

<Lựa chọn cuối, vì sao, semantics chính xác: units, ordering, rounding, boundaries,
version, failure policy; ví dụ nhỏ có kết quả dự kiến nếu hữu ích.>

## Tác động và compatibility

<Module/schema/API/config/rule/model versions bị ảnh hưởng, migration/replay,
historical artifacts và producer/consumer compatibility.>

## Kiểm chứng và phục hồi

<Golden fixtures/positive/boundary/negative/invariant/tests/benchmarks cần chạy,
kết quả thực, cách rollback/recovery và giới hạn.>

## Cập nhật tài liệu

<Decision register/rules/contracts/requirements map đã cập nhật ở đâu.>
