# Báo Cáo Chất Lượng Dữ Liệu Ban Đầu (DATA QUALITY REPORT)

> **Người phụ trách**: Thành viên 1 - Kỹ sư Dữ liệu (Data Engineer)  
> **Trạng thái**: Khung tài liệu báo cáo EDA trước làm sạch (Giai đoạn 1)

---

## 1. Tổng Quan Tập Dữ Liệu Thô (Raw Data Overview)
*(Được trích xuất từ script `src/02_eda.py` và notebook `notebooks/01_initial_eda.ipynb` trong Giai đoạn 2)*

- **Tổng số dòng dữ liệu thô ban đầu**: *[Chưa thực hiện]*
- **Tổng số cột**: *[Chưa thực hiện]*
- **Dung lượng file thô**: *[Chưa thực hiện]*
- **Khoảng thời gian ghi nhận**: *[Chưa thực hiện]*

---

## 2. Thống Kê Giá Trị Thiếu (Missing Values Analysis)

| Tên Cột | Số Dòng Thiếu (Missing Count) | Tỷ Lệ Thiếu (%) | Mức Độ Nghiêm Trọng | Hướng Xử Lý Dự Kiến |
|---------|-------------------------------|-----------------|---------------------|----------------------|
| `acres_burned` / `burned_area_ha` | *TODO* | *TODO* | TB | Khảo sát từ diện tích FRAP / Imputation ML |
| `structures_destroyed` | *TODO* | *TODO* | Thấp | Hợp nhất từ ICS-209 (2006–2012) và DINS (2013–2025) |
| `damage_property_usd` | *TODO* | *TODO* | Cao | Lấy từ NOAA NCEI / Imputation hoặc giữ nguyên |
| `deaths_direct` / `injuries_direct` | *TODO* | *TODO* | Thấp | Đối soát từ NOAA Storm Events (mặc định 0 nếu không ghi nhận) |
| `cause_name` / `cause_code` | *TODO* | *TODO* | TB | Chuẩn hóa mã CAL FIRE 1-19 / Dự đoán Random Forest |
| `latitude`/`longitude` | *TODO* | *TODO* | Thấp | Kiểm tra Bounding Box California (32°N-42°N, -125°W đến -114°W) |

*Biểu đồ trực quan ma trận thiếu (Missingno Matrix): Sẽ được đính kèm sau khi chạy EDA.*

---

## 3. Phân Tích Dữ Liệu Trùng Lặp (Duplicate Analysis)
- Số dòng trùng lặp hoàn toàn (Exact Duplicates): *[TODO]*
- Số dòng trùng lặp logic (Cùng vụ cháy, cùng vị trí, trùng ngày nhưng khác mã hồ sơ): *[TODO]*
- Tỷ lệ trùng lặp: *[TODO]* %

---

## 4. Phân Bố & Ngoại Lai Sơ Bộ (Distributions & Initial Outliers)
- **Diện tích cháy (Acres / Ha)**: Phân phối lũy thừa cực đoan (Heavy-tailed / Power-law). Đa số các vụ cháy nhỏ, số ít siêu thảm họa (>100.000 mẫu) thiêu rụi hàng trăm ngàn mẫu. Cần biến đổi log scale (`log1p`).
- **Nhà cửa bị phá hủy (structures_destroyed)**: Tuân theo quy luật Pareto 80/20, tập trung đột biến ở các siêu đám cháy (Camp Fire, Tubbs Fire, Palisades Fire...).
- **Thiệt hại tài sản & Thương vong**: Phân phối lệch phải mạnh, kiểm tra ngoại lai qua Isolation Forest.
- **Tọa độ địa lý**: Kiểm tra các điểm có tọa độ nằm ngoài hộp giới hạn Bounding Box của bang California (vĩ độ $32^{\circ}$–$42^{\circ}$N, kinh độ $-125^{\circ}$–$-114^{\circ}$W).
