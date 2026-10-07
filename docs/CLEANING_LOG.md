# Nhật Ký Làm Sạch Dữ Liệu (CLEANING LOG)

> **Người phụ trách**: Thành viên 1 - Kỹ sư Dữ liệu (Data Engineer)  
> **Trạng thái**: Khung tài liệu ghi vết toàn bộ quy trình làm sạch (Giai đoạn 1)

---

## 1. Nguyên Tắc & Quy Chuẩn Làm Sạch
- **Không chỉnh sửa thủ công**: Mọi thao tác biến đổi dữ liệu phải thông qua mã nguồn Python có khả năng tái lập (`src/03_clean.py` và `src/03b_ml_clean.py`).
- **Bảo toàn dữ liệu gốc**: Giữ lại các cột thô ban đầu song song với cột chuẩn hóa (vd: `damage_usd_raw` song song `damage_usd`).
- **Gắn cờ kiểm soát**: Mọi giá trị được điền (imputed), dự đoán (predicted), hoặc nghi ngờ ngoại lai (outlier) đều có cột cờ nhị phân riêng.
- **Cam kết số lượng mẫu**: Sau toàn bộ quy trình làm sạch, tập dữ liệu `master_clean.csv` phải đạt tối thiểu **5.000 dòng**.

---

## 2. Bảng Theo Dõi Các Bước Làm Sạch Theo Quy Tắc (`03_clean.py`)

| Bước # | Thao tác thực hiện | Điều kiện / Quy tắc | Số dòng trước | Số dòng sau | Số dòng loại bỏ | Lý do & Ghi chú |
|--------|---------------------|----------------------|---------------|-------------|-----------------|-----------------|
| 1 | Nạp dữ liệu thô | Gộp 5 nguồn từ `data/raw/calfire/` | *TODO* | *TODO* | *TODO* | Nạp 5 file CSV chính thức |
| 2 | Lọc khoảng thời gian | `year BETWEEN 2006 AND 2025` | *TODO* | *TODO* | *TODO* | Bao phủ đủ 20/20 năm liên tục |
| 3 | Khử trùng lặp chính xác | Duplicate trên tập thuộc tính định danh | *TODO* | *TODO* | *TODO* | Loại bỏ bản ghi trùng |
| 4 | Chuẩn hóa địa danh & Hạt | Ánh xạ 58 Hạt California, mã FIPS và mã viết tắt | *TODO* | *TODO* | *TODO* | Chuẩn hóa tên Hạt viết hoa/thường |
| 5 | Chuẩn hóa tọa độ | Vĩ độ [32.0, 42.0], Kinh độ [-125.0, -114.0] | *TODO* | *TODO* | *TODO* | Giữ trong Bounding Box California |
| 6 | Chuẩn hóa đơn vị đo lường | Lưu song song Mẫu Anh (Acres) & Hecta (ha) | *TODO* | *TODO* | *TODO* | 1 Acre = 0.404686 Ha |
| 7 | Hợp nhất thiệt hại 20 năm | ICS-209 (2006-2012) + DINS (2013-2025) | *TODO* | *TODO* | *TODO* | Đảm bảo cột structures_destroyed đủ 20 năm |
| 8 | Xử lý giá trị âm bất hợp lý | `deaths_direct >= 0`, `structures_destroyed >= 0`, `acres_burned >= 0` | *TODO* | *TODO* | *TODO* | Chuyển thành NULL hoặc loại bỏ nếu sai toàn phần |
| **Tổng kết** | **Xuất `data/interim/master_rules_cleaned.csv`** | | | | | Đạt điều kiện tiền xử lý cho ML |

---

## 3. Nhật Ký Xử Lý Ngoại Lai & Bất Thường Thủ Công
*(Kiểm tra mẫu top 20 dòng bất thường nhất do mô hình ML Isolation Forest gắn cờ trong Giai đoạn 2)*

| STT | `incident_id` | Tên vụ cháy / Hạt / Năm | Thuộc tính nghi ngờ | Giá trị bất thường | Quyết định (GIỮ / SỬA / LOẠI) | Căn cứ & Nguồn đối soát |
|-----|------------|------------------------------|----------------------|--------------------|--------------------------------|--------------------------|
| 1 | *TODO* | *TODO* | *TODO* | *TODO* | *TODO* | *TODO* |
| 2 | *TODO* | *TODO* | *TODO* | *TODO* | *TODO* | *TODO* |
| 3 | *TODO* | *TODO* | *TODO* | *TODO* | *TODO* | *TODO* |
