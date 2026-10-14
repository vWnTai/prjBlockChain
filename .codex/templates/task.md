# Task: <tên thay đổi cụ thể>

Đây là mẫu. Tạo task thực trong thư mục docs/tasks khi cần; điền dữ liệu thật,
bỏ phần không áp dụng và không giữ placeholder trong code/runtime artifacts.

## Kết quả cần đạt

<Trigger/hành vi hiện tại, hành vi sau thay đổi và lý do người dùng cần.>

## Nguồn và phạm vi

- Yêu cầu người dùng: <nội dung được giao/quyền đã có>.
- Kế hoạch: <mục>; requirement/test IDs: <Rxx/Txx/Wxx>.
- Rule files cần đọc: <paths đúng trigger>.
- Phạm vi thực hiện: <module/hành vi>.
- Giới hạn còn lại: <scope đã khóa hoặc dependency chưa có>.

## Trạng thái đã xác minh

<Files/toolchain/commands hiện có, thay đổi người dùng, actual behavior và evidence.>

## Contract và quyết định

<Money/order/as_of/version/coverage, migration/API compatibility, decision IDs,
ADR path, lựa chọn đã chốt và giả định còn cần xác minh.>

## Các bước và tiến độ

- [ ] <Lát cắt có đầu ra kiểm tra được>.
- [ ] <Producer/consumer/schema/UI tích hợp nếu liên quan>.
- [ ] <Kiểm chứng/regression/docs/diff review>.

## Kiểm tra chấp nhận

| Kiểm tra | Lệnh hoặc thao tác | Kỳ vọng | Kết quả thực / artifact |
| --- | --- | --- | --- |
| <ID/hành vi> | <lệnh thực ở đúng thư mục> | <assert độc lập> | <chưa chạy/pass/fail + bằng chứng> |

## Rủi ro và phục hồi

<Tác động state/history/schema, recovery hoặc replay/version cần thiết.
Ghi N/A có lý do khi không áp dụng. Không tự reset dữ liệu để recover.>

## Bàn giao

<File chính, hành vi đã hoàn thành, kết quả kiểm tra, giới hạn và việc còn lại.>
