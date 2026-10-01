# Hướng Dẫn Tải Dữ Liệu Thủ Công EM-DAT (CRED)

> **Lưu ý**: Nguồn dữ liệu EM-DAT yêu cầu tài khoản học thuật/phi thương mại và tuân thủ chính sách bản quyền (không cho phép tự động tải qua script khi chưa có token cá nhân). Thành viên nhóm vui lòng thực hiện các bước sau để lấy dữ liệu:

---

## Các Bước Thực Hiện

1. **Đăng ký tài khoản**:
   - Truy cập cổng dữ liệu EM-DAT: [https://public.emdat.be/](https://public.emdat.be/)
   - Bấm **Register** và tạo tài khoản miễn phí bằng email trường đại học / học thuật.

2. **Tìm kiếm và xuất dữ liệu (Data Export)**:
   - Đăng nhập vào hệ thống.
   - Chọn mục **Data** $\to$ **Custom Query / Advanced Search**.
   - Thiết lập các bộ lọc:
     - **Disaster Group**: `Natural`
     - **Disaster Subgroup**: Chọn toàn bộ (`Meteorological`, `Hydrological`, `Climatological`, `Geophysical`, `Biological`).
     - **Time Period**: Từ `2006-01-01` đến `2025-12-31`.
     - **Geographical Scope**: `All Countries` (Toàn cầu).
   - Chọn định dạng xuất: **CSV** hoặc **Excel (.xlsx)**.

3. **Lưu tệp tin vào dự án**:
   - Đặt tệp tin tải về vào đúng thư mục này:
     `data/raw/emdat/emdat_raw.csv` (hoặc `emdat_raw.xlsx`)
   - Không đổi tên cột, không xóa bớt dòng, giữ nguyên bản dữ liệu gốc của CRED.

4. **Kiểm tra**:
   - Tệp tin sẽ tự động được nhận diện trong các giai đoạn xử lý tiếp theo của pipeline.
