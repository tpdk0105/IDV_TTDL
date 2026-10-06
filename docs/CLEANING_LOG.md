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
| 1 | Nạp dữ liệu thô | Gộp các nguồn từ `data/raw/` | *TODO* | *TODO* | *TODO* | Nạp file CSV/Excel |
| 2 | Lọc khoảng thời gian | `year BETWEEN 2005 AND 2024` | *TODO* | *TODO* | *TODO* | Giới hạn nghiên cứu 20 năm |
| 3 | Khử trùng lặp chính xác | Duplicate trên tập thuộc tính định danh | *TODO* | *TODO* | *TODO* | Loại bỏ bản ghi trùng |
| 4 | Chuẩn hóa mã quốc gia | Ánh xạ tên nước về ISO 3166-1 alpha-3 | *TODO* | *TODO* | *TODO* | Dùng thư viện country-converter |
| 5 | Chuẩn hóa tọa độ | Vĩ độ [-90, 90], Kinh độ [-180, 180] | *TODO* | *TODO* | *TODO* | Loại hoặc set NULL tọa độ lỗi |
| 6 | Chuẩn hóa đơn vị đo lường | Quy đổi diện tích về Hecta (ha), thiệt hại về USD | *TODO* | *TODO* | *TODO* | Acres/km2 -> ha; nghìn/triệu -> USD |
| 7 | Xử lý giá trị âm bất hợp lý | `deaths >= 0`, `damage_usd >= 0`, `burned_area_ha >= 0` | *TODO* | *TODO* | *TODO* | Chuyển thành NULL hoặc loại bỏ nếu sai toàn phần |
| **Tổng kết** | **Xuất `data/interim/master_rules_cleaned.csv`** | | | | | Đạt điều kiện tiền xử lý cho ML |

---

## 3. Nhật Ký Xử Lý Ngoại Lai & Bất Thường Thủ Công
*(Kiểm tra mẫu top 20 dòng bất thường nhất do mô hình ML Isolation Forest gắn cờ trong Giai đoạn 2)*

| STT | `event_id` | Tên sự kiện / Quốc gia / Năm | Thuộc tính nghi ngờ | Giá trị bất thường | Quyết định (GIỮ / SỬA / LOẠI) | Căn cứ & Nguồn đối soát |
|-----|------------|------------------------------|----------------------|--------------------|--------------------------------|--------------------------|
| 1 | *TODO* | *TODO* | *TODO* | *TODO* | *TODO* | *TODO* |
| 2 | *TODO* | *TODO* | *TODO* | *TODO* | *TODO* | *TODO* |
| 3 | *TODO* | *TODO* | *TODO* | *TODO* | *TODO* | *TODO* |
