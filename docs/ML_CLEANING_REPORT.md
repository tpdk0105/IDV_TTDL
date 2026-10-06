# Báo Cáo Làm Sạch Dữ Liệu Bằng Học Máy (ML CLEANING REPORT)

> **Người phụ trách**: Thành viên 1 - Kỹ sư Dữ liệu (Data Engineer)  
> **Trạng thái**: Khung tài liệu phương pháp luận và kết quả thực nghiệm ML (Giai đoạn 1)

---

## 1. Mục Đích & Nguyên Tắc Áp Dụng Học Máy
Trong bài toán phân tích thảm họa thiên nhiên và cháy rừng giai đoạn 2005–2024, dữ liệu thu thập từ các nguồn quốc tế thường gặp hai vấn đề lớn:
1. **Giá trị ngoại lai cực đoan (Extreme Outliers)**: Các thảm họa có quy mô lớn bất thường, lỗi nhập thừa chữ số (sai lệch bậc độ lớn $10^3, 10^6$), hoặc lỗi đơn vị đo.
2. **Giá trị khuyết thiếu (Missing Data)**: Nhiều sự kiện thảm họa chỉ ghi nhận thiệt hại người (`deaths`, `affected`) nhưng thiếu diện tích cháy (`burned_area_ha`) hoặc thiếu thiệt hại kinh tế (`damage_usd`).

### Nguyên tắc bắt buộc:
- **Tối thiểu 2 mô hình học máy độc lập**:
  1. *Phát hiện ngoại lai đa biến*: **Isolation Forest** kết hợp đối soát **Local Outlier Factor (LOF)**.
  2. *Điền giá trị thiếu đa biến*: **KNN Imputer** hoặc **Iterative Imputer (MICE)**.
  3. *(Mở rộng)*: **Random Forest Classifier** dự đoán nhóm nguyên nhân (`cause_group`) khi xác suất dự đoán $P \ge 0.7$.
- **Không tự động xóa hàng loạt**: Mô hình ngoại lai chỉ GẮN CỜ (`is_outlier_ml`) và tính điểm bất thường (`outlier_score`). Quyết định loại bỏ chỉ áp dụng sau khi đối soát thủ công có căn cứ rõ ràng.
- **Minh bạch hóa**: Mỗi giá trị được điền phải đi kèm cờ `<cột>_is_imputed = True`. Cột thiếu $> 60\%$ tuyệt đối không điền.
- **Đánh giá nghiêm ngặt, không rò rỉ dữ liệu (Data Leakage)**: Sử dụng kỹ thuật che ngẫu nhiên (masking 10–20%) và so sánh với phương pháp nền tảng (Median Imputation) bằng MAE / RMSE.

---

## 2. Mô Hình 1 – Phát Hiện Ngoại Lai (Isolation Forest & LOF)

### 2.1. Lựa chọn đặc trưng & tiền xử lý
- **Tập đặc trưng đầu vào**: `deaths`, `affected`, `damage_usd`, `burned_area_ha`.
- **Biến đổi phân phối**: Áp dụng $\log_{1p}(x) = \ln(1 + x)$ do các chỉ số thảm họa có phân phối lệch phải cực nặng.
- **Chuẩn hóa**: `RobustScaler` (sử dụng Median và Interquartile Range) nhằm tránh bị ảnh hưởng bởi chính các giá trị ngoại lai cực đại.

### 2.2. Siêu tham số (Hyperparameters)
- `n_estimators`: 200
- `contamination`: 0.02 (dự kiến ~2% quan sát bất thường)
- `random_state`: 42 (đảm bảo tính tái lập)
- Đối chiếu: `LocalOutlierFactor(n_neighbors=20, contamination=0.02)`

### 2.3. Kết quả đánh giá sơ bộ
*(Sẽ được điền sau khi chạy `src/03b_ml_clean.py` trong Giai đoạn 2)*
- Tỷ lệ mẫu bị gắn cờ `is_outlier_ml`: *[TODO]* %
- Phân phối điểm bất thường (`outlier_score`): *[TODO]*
- Danh sách sự kiện thật được giữ lại (True Events): *[TODO]*
- Danh sách bản ghi lỗi nhập liệu bị loại/sửa: *[TODO]*

---

## 3. Mô Hình 2 – Điền Dữ Liệu Thiếu (Iterative Imputer / KNN Imputer)

### 3.1. Phương pháp & Cơ sở lựa chọn
- **Iterative Imputer (Multivariate Imputation by Chained Equations - MICE)**: Mô hình hóa từng biến số bị thiếu như một hàm hồi quy của các biến còn lại theo cơ chế chuỗi lặp (Bayesian Ridge / Extra Trees).
- **KNN Imputer (K-Nearest Neighbors)**: Tìm $k$ sự kiện lân cận có đặc trưng tương đồng (cùng khu vực, quy mô tương đương) để tính trung bình có trọng số.

### 3.2. Thiết lập thực nghiệm đánh giá chéo (Cross-Validation Evaluation)
- Lấy tập con gồm các bản ghi đã có đầy đủ giá trị quan sát (Complete Cases).
- Che ngẫu nhiên (Masking) $15\%$ giá trị của biến mục tiêu (`damage_usd`, `burned_area_ha`).
- So sánh sai số dự báo của mô hình đề xuất với phương pháp chuẩn cơ sở (Baseline: Điền trung vị - Median Imputation).

### 3.3. Bảng Kết Quả Đánh Giá Sai Số (Error Metrics Table)

| Biến mục tiêu | Mô hình | MAE (Log Scale) | RMSE (Log Scale) | MAPE (%) | So với Median Baseline |
|---------------|---------|-----------------|------------------|----------|------------------------|
| `damage_usd` | Baseline (Median) | *TODO* | *TODO* | *TODO* | Chuẩn đối chiếu |
| `damage_usd` | KNN Imputer ($k=5$) | *TODO* | *TODO* | *TODO* | *TODO* |
| `damage_usd` | Iterative Imputer (MICE) | *TODO* | *TODO* | *TODO* | *TODO* |
| `burned_area_ha` | Baseline (Median) | *TODO* | *TODO* | *TODO* | Chuẩn đối chiếu |
| `burned_area_ha` | KNN Imputer ($k=5$) | *TODO* | *TODO* | *TODO* | *TODO* |
| `burned_area_ha` | Iterative Imputer (MICE) | *TODO* | *TODO* | *TODO* | *TODO* |

---

## 4. Mô Hình 3 (Khuyến khích) – Phân Loại Nhóm Nguyên Nhân (Random Forest)
- **Mục tiêu**: Phân loại các sự kiện có `cause_group` khuyết thiếu vào các nhóm: `Natural`, `Human`, `Unknown`.
- **Đặc trưng**: Tháng trong năm, Vùng địa lý, Loại phụ thảm họa, Diện tích, Chỉ số hạn hán/thời gian.
- **Điều kiện chấp nhận**: Xác suất cực đại $\max P(\text{class}) \ge 0.70$. Khi đó gán `cause_is_predicted = True`. Dưới ngưỡng trên giữ nguyên `Unknown`.

---

## 5. Danh Sách Giới Hạn Của Mô Hình & Cảnh Báo Khi Khai Thác
1. **Dữ liệu điền là giá trị ước lượng**: Các giá trị được điền bằng ML chỉ phục vụ phân tích xu hướng tổng thể và trực quan hóa vĩ mô; không đại diện cho số liệu kiểm toán thực tế của sự kiện đó.
2. **Bộ lọc trên Dashboard**: Hệ thống bắt buộc cung cấp công tắc **"Chỉ hiển thị số liệu gốc (Ẩn giá trị ước lượng/điền thiếu)"** để người dùng có thể đối chiếu giữa dữ liệu thực và dữ liệu sau ML.
