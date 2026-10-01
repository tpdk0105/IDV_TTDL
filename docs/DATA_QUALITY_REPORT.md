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
| `damage_usd` | *TODO* | *TODO* | Cao | Imputation bằng KNN/Iterative hoặc giữ NULL |
| `burned_area_ha` | *TODO* | *TODO* | Cao | Đối soát từ diện tích thô / Imputation ML |
| `deaths` | *TODO* | *TODO* | Thấp/TB | Kiểm tra 0 vs NULL / Điền giá trị |
| `cause_name` | *TODO* | *TODO* | TB | Phân loại bằng Random Forest Classifier |
| `latitude`/`longitude` | *TODO* | *TODO* | Thấp | Không điền tọa độ giả, chỉ giữ nếu hợp lệ |

*Biểu đồ trực quan ma trận thiếu (Missingno Matrix): Sẽ được đính kèm sau khi chạy EDA.*

---

## 3. Phân Tích Dữ Liệu Trùng Lặp (Duplicate Analysis)
- Số dòng trùng lặp hoàn toàn (Exact Duplicates): *[TODO]*
- Số dòng trùng lặp logic (Cùng vị trí, cùng ngày, cùng loại thảm họa nhưng khác ID): *[TODO]*
- Tỷ lệ trùng lặp: *[TODO]* %

---

## 4. Phân Bố & Ngoại Lai Sơ Bộ (Distributions & Initial Outliers)
- **Thiệt hại (USD)**: Phân phối lệch phải cực mạnh (Right-skewed). Đa số các vụ thiệt hại nhỏ, một số ít siêu thảm họa gây thiệt hại hàng tỷ USD. Cần biến đổi thang log (`log1p`).
- **Diện tích cháy (ha)**: Phân phối lũy thừa (Power-law distribution). Cần áp dụng thang đo log để quan sát mật độ.
- **Số người tử vong (deaths)**: Chủ yếu tập trung ở 0 hoặc rất nhỏ, ngoại trừ các sự kiện dị biệt.
- **Tọa độ**: Kiểm tra các điểm có tọa độ (0, 0) ngoài khơi vịnh Guinea hoặc ngoài phạm vi địa lý của quốc gia tương ứng.
