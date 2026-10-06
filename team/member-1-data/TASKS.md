# NHIỆM VỤ THÀNH VIÊN 1: KỸ SƯ DỮ LIỆU & HỌC MÁY (DATA & ML ENGINEER)

> **Họ và tên**: [TÊN THÀNH VIÊN 1]  
> **MSSV**: [Điền MSSV]  
> **Nhánh Git phụ trách**: `member-1-data`  
> **Trọng tâm**: Thu thập dữ liệu California, EDA (3–5 hình tĩnh Seaborn/Matplotlib), Làm sạch (Quy tắc + ML), **Huấn luyện Mô hình dự báo Linear/Logistic trên Python**; Thực hiện 2 biểu đồ #1, #2.

---

## 1. Mục Tiêu Chính
1. Thu thập và làm sạch 4 bộ dữ liệu chuyên sâu về Cháy rừng California giai đoạn 2006–2025: **CAL FIRE FRAP** (Perimeters), **CAL FIRE DINS** (Damage Inspection), **California Demographics** (58 Hạt) và **NOAA NCEI** (Casualties).
2. Tự động hóa tải dữ liệu vào `data/raw/calfire/` bằng script [src/01_download.py](../../src/01_download.py) kèm sinh mã băm SHA-256 trong `data/raw/MANIFEST.md`.
3. Thực hiện phân tích khám phá dữ liệu (EDA), phát hiện các khiếm khuyết và lập báo cáo chất lượng ban đầu [docs/DATA_QUALITY_REPORT.md](../../docs/DATA_QUALITY_REPORT.md).
4. Triển khai quy trình làm sạch 2 giai đoạn:
   - *Giai đoạn 1 (Rule-based)*: Chuẩn hóa tên vụ cháy (`fire_name`), tên Hạt (`county`), đơn vị diện tích (Acres và Hecta), sửa giá trị âm và loại trùng lặp $\to$ `data/interim/master_rules_cleaned.csv`.
   - *Giai đoạn 2 (Machine Learning)*: Áp dụng **Isolation Forest** (kết hợp LOF) để phát hiện và gắn cờ ngoại lai; áp dụng **KNN Imputer / Iterative Imputer (MICE)** để điền giá trị thiếu; áp dụng **Random Forest** phân loại nguyên nhân $\to$ `data/clean/master_clean.csv`.
5. Đảm bảo tập dữ liệu làm sạch cuối cùng đạt tối thiểu **5.000 dòng** (có lệnh `assert len(df) >= 5000`).
6. **Xây dựng Mô hình dự báo (Predictive Modeling - Barem 1.0 Điểm)**:
   - Áp dụng thuật toán **Hồi quy tuyến tính (Linear Regression)** để dự báo diện tích rừng cháy / mức độ thiệt hại tài sản theo thời gian (hoặc **Hồi quy Logistic** phân loại cấp độ rủi ro).
   - Đánh giá các chỉ số sai số ($R^2$, RMSE, MAE).
   - Xuất file kết quả dự báo `data/clean/forecast_results.csv` bàn giao cho TV2/TV3 sử dụng trên Dashboard.
7. Hoàn thành 2 biểu đồ độc lập được giao (**#1 `Sheet_01_Combo_Trend`**, **#2 `Sheet_02_Stacked_Area`**) trên Tableau.

---

## 2. Bảng Theo Dõi Trạng Thái Công Việc

| Hạng mục công việc | Trạng thái | Deadline | Ghi chú cá nhân |
|--------------------|------------|----------|-----------------|
| Thiết lập môi trường & nhánh `member-1-data` | Sẵn sàng | Tuần 1 | Giai đoạn 1 |
| Đánh giá 4 nguồn California & viết `DATA_SOURCES.md` | Hoàn thành | Tuần 2 | CAL FIRE, DINS, Census, NOAA |
| Viết script thu thập dữ liệu `01_download.py` | Hoàn thành | Tuần 2 | Lưu 4 file vào `data/raw/calfire/` |
| EDA & viết `DATA_QUALITY_REPORT.md` | Chưa bắt đầu | *[Điền]* | Kèm notebook EDA |
| Làm sạch theo quy tắc `03_clean.py` | Chưa bắt đầu | *[Điền]* | Xuất interim |
| Làm sạch bằng Học máy `03b_ml_clean.py` | Chưa bắt đầu | *[Điền]* | $\ge 2$ mô hình ML |
| Viết báo cáo ML `ML_CLEANING_REPORT.md` | Chưa bắt đầu | *[Điền]* | Báo cáo sai số MAE/RMSE |
| Xây dựng Mô hình dự báo (Linear/Logistic) | Chưa bắt đầu | *[Điền]* | scikit-learn (Barem 1.0 đ) |
| Hoàn thiện `CLEANING_LOG.md` & `DATA_DICTIONARY.md` | Chưa bắt đầu | *[Điền]* | Ghi chú cờ ML |
| Biểu đồ #1: `Sheet_01_Combo_Trend` (Số vụ + Diện tích + Trend Line) | Chưa bắt đầu | *[Điền]* | Tần suất & Diện tích cháy |
| Biểu đồ #2: `Sheet_02_Stacked_Area` (Cơ cấu nguyên nhân) | Chưa bắt đầu | *[Điền]* | Diễn biến nguyên nhân |

---

## 3. Danh Sách Checklist Chi Tiết

### A. Thu Thập Dữ Liệu
- [x] Thu thập 4 bộ dữ liệu chuyên sâu về Cháy rừng California: CAL FIRE FRAP, CAL FIRE DINS, California Demographics, NOAA Casualties.
- [x] Lập bảng so sánh chi tiết trong `docs/DATA_SOURCES.md`.
- [x] Viết `src/01_download.py` tự động tải dữ liệu vào `data/raw/calfire/` và sinh checksum SHA-256.

### B. Khám Phá Dữ Liệu (EDA) - Trọng số Barem: 0.75 Điểm
- [ ] Viết `src/02_eda.py` và tạo Jupyter Notebook `notebooks/01_initial_eda.ipynb`.
- [ ] Sử dụng **Matplotlib** và **Seaborn** vẽ tối thiểu **3 – 5 biểu đồ tĩnh**:
  - [ ] `eda_01_missing_values.png`: Biểu đồ ma trận khuyết thiếu.
  - [ ] `eda_02_distributions.png`: Biểu đồ phân phối Histogram + KDE cho diện tích cháy (`acres_burned`) trên thang logarit.
  - [ ] `eda_03_outliers_boxplot.png`: Biểu đồ hộp Boxplot phát hiện ngoại lai số công trình bị phá hủy (`structures_destroyed`).
  - [ ] `eda_04_correlation_heatmap.png`: Bản đồ nhiệt tương quan giữa diện tích cháy, thời gian dập lửa và số công trình phá hủy.
  - [ ] `eda_05_temporal_trend.png`: Biểu đồ đường xu hướng số vụ cháy rừng California qua 20 năm.
- [ ] Xuất toàn bộ biểu đồ vào thư mục `reports/figures/`.
- [ ] Lập tài liệu `docs/DATA_QUALITY_REPORT.md`.

### C. Làm Sạch Theo Quy Tắc (Rule-based Cleaning)
- [ ] Viết `src/03_clean.py`:
  - [ ] Lọc phạm vi thời gian 2006–2025.
  - [ ] Chuẩn hóa tên vụ cháy (`fire_name`: viết hoa, chuẩn hóa `CMPLX` $\to$ `COMPLEX`) để khớp giữa FRAP và DINS.
  - [ ] Chuẩn hóa tên Hạt (`county`) khớp với 58 Hạt California.
  - [ ] Quy đổi diện tích mẫu Anh (Acres) sang Hecta (`burned_area_ha`).
  - [ ] Xử lý giá trị âm bất hợp lý, loại bỏ trùng lặp.
  - [ ] Xuất kết quả vào `data/interim/master_rules_cleaned.csv`.

### D. Làm Sạch Bằng Học Máy (Machine Learning Cleaning - $\ge 2$ Mô Hình)
- [ ] Viết `src/03b_ml_clean.py`:
  - [ ] **Mô hình 1 (Phát hiện ngoại lai)**: Áp dụng **Isolation Forest** (đối soát với LOF) trên biến `log1p(acres_burned)` và `log1p(structures_destroyed)`. Gắn cờ `is_outlier_ml = True/False` và tính `outlier_score`.
  - [ ] Đối soát thủ công top 20 mẫu bất thường, ghi nhật ký vào `docs/CLEANING_LOG.md`.
  - [ ] **Mô hình 2 (Điền giá trị thiếu)**: Áp dụng **KNN Imputer** hoặc **Iterative Imputer (MICE)** điền các biến định lượng có tỷ lệ thiếu vừa phải. Gắn cờ `<col>_is_imputed`. Thử nghiệm che 10–20% đối soát MAE/RMSE so với Median.
  - [ ] *(Khuyến khích)*: Áp dụng **Random Forest Classifier** dự đoán nhóm nguyên nhân (`cause_group`) khi khuyết thiếu, gắn cờ `cause_is_predicted`.
  - [ ] **Yêu cầu cứng**: Đặt câu lệnh `assert len(df) >= 5000` ở cuối script.
  - [ ] Xuất kết quả ra `data/clean/master_clean.csv`.
- [ ] Viết báo cáo thực nghiệm chi tiết `docs/ML_CLEANING_REPORT.md`.
- [ ] Cập nhật định nghĩa các trường dữ liệu và các cột cờ vào `docs/DATA_DICTIONARY.md`.

### E. Xây Dựng Mô Hình Dự Báo Trên Python (Barem 0.5 Điểm)
- [ ] Viết script `src/08_predictive_model.py` bằng `scikit-learn`:
  - [ ] Huấn luyện mô hình **Hồi quy tuyến tính (Linear Regression)** dự báo diện tích cháy rừng hoặc thiệt hại qua các năm theo chuỗi thời gian 2006–2025.
  - [ ] Đánh giá các chỉ số sai số: $R^2$, MAE, RMSE.
- [ ] **Đầu ra bàn giao cho Pipeline**:
  - Xuất bảng kết quả dự báo `data/clean/forecast_results.csv` (chứa các mốc năm tương lai và giá trị dự báo).
  - Bàn giao kết quả này cho TV2 nạp vào DB và TV3 sử dụng trực tiếp để hiển thị lên Dashboard.

---

## 4. Các Biểu Đồ Phụ Trách (2 Worksheets: #1, #2 trên Tableau)

### Worksheet #1: `Sheet_01_Combo_Trend` (Tần suất & Diện tích cháy theo năm)
- [ ] (a) Kéo `[year]` vào Columns; trục 1: `CNT([incident_id])` (Marks: Bar, Xanh); trục 2: `SUM([acres_burned])` (Marks: Line, Cam).
- [ ] (b) Chuột phải trục 2 $\to$ chọn **Dual Axis**.
- [ ] (c) Bật đường **Trend Line (Linear)** minh họa xu hướng dự báo của mô hình Hồi quy tuyến tính.

### Worksheet #2: `Sheet_02_Stacked_Area` (Cơ cấu nguyên nhân cháy theo thời gian)
- [ ] (a) Kéo `[year]` vào Columns; kéo `CNT([incident_id])` vào Rows; Marks: Area.
- [ ] (b) Kéo `[cause_name]` hoặc `[cause_group]` vào Color.
- [ ] (c) Sắp xếp `Lightning` (Sét) và `Equipment Use` ở dưới cùng để quan sát rõ nhất.
