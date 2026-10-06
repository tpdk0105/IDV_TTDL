# NHIỆM VỤ THÀNH VIÊN 1: KỸ SƯ DỮ LIỆU (DATA ENGINEER)

> **Họ và tên**: [TÊN THÀNH VIÊN 1]  
> **MSSV**: [Điền MSSV]  
> **Nhánh Git phụ trách**: `member-1-data`  
> **Trọng tâm**: Thu thập, khám phá (EDA) và làm sạch dữ liệu (Quy tắc + Học máy); Thực hiện 4 biểu đồ #1–#4.

---

## 1. Mục Tiêu Chính
1. Khảo sát và lựa chọn tối thiểu 3 nguồn dữ liệu quốc tế đáng tin cậy về thảm họa thiên nhiên và cháy rừng giai đoạn 2006–2025.
2. Xây dựng quy trình tự động hóa thu thập dữ liệu thô vào `data/raw/` bằng script có khả năng tái lập.
3. Thực hiện phân tích khám phá dữ liệu (EDA), phát hiện các khiếm khuyết và lập báo cáo chất lượng ban đầu.
4. Triển khai quy trình làm sạch 2 giai đoạn:
   - *Giai đoạn 1 (Rule-based)*: Chuẩn hóa đơn vị, định dạng ngày, mã quốc gia ISO3, sửa giá trị âm và loại trùng lặp $\to$ `data/interim/master_rules_cleaned.csv`.
   - *Giai đoạn 2 (Machine Learning)*: Áp dụng **Isolation Forest** (kết hợp LOF) để phát hiện và gắn cờ ngoại lai; áp dụng **KNN Imputer / Iterative Imputer (MICE)** để điền giá trị thiếu; áp dụng **Random Forest** phân loại nhóm nguyên nhân $\to$ `data/clean/master_clean.csv`.
5. Đảm bảo tập dữ liệu làm sạch cuối cùng đạt tối thiểu **5.000 dòng** (có lệnh `assert`).
6. **Xây dựng Mô hình dự báo (Predictive Modeling - Barem 1.0 Điểm)**:
   - Áp dụng thuật toán **Hồi quy tuyến tính (Linear Regression)** để dự báo xu hướng thiệt hại tài chính / diện tích cháy theo thời gian, hoặc **Hồi quy Logistic (Logistic Regression)** để phân lớp cấp độ rủi ro thảm họa.
   - Báo cáo các chỉ số đánh giá ($R^2$, RMSE / Accuracy, F1).
   - Tích hợp kết quả dự báo (đường xu hướng, phân lớp rủi ro) lên biểu đồ trực quan trong Dashboard Tableau (`Sheet_01_Combo_Trend` hoặc phối hợp các sheet).
7. Hoàn thành 4 biểu đồ được giao (#1, #2, #3, #4) theo đúng đặc tả và bảng màu chuẩn.

---

## 2. Bảng Theo Dõi Trạng Thái Công Việc

| Hạng mục công việc | Trạng thái | Deadline | Ghi chú cá nhân |
|--------------------|------------|----------|-----------------|
| Thiết lập môi trường & nhánh `member-1-data` | Sẵn sàng | Tuần 1 | Giai đoạn 1 |
| Đánh giá $\ge 3$ nguồn & viết `DATA_SOURCES.md` | Hoàn thành | Tuần 2 | OWID, NASA, NOAA, USFS, EM-DAT |
| Viết script thu thập dữ liệu `01_download.py` | Hoàn thành | Tuần 2 | Lưu 7 file vào `data/raw/` + manifest |
| EDA & viết `DATA_QUALITY_REPORT.md` | Chưa bắt đầu | *[Điền]* | Kèm notebook EDA |
| Làm sạch theo quy tắc `03_clean.py` | Chưa bắt đầu | *[Điền]* | Xuất interim |
| Làm sạch bằng Học máy `03b_ml_clean.py` | Chưa bắt đầu | *[Điền]* | $\ge 2$ mô hình ML |
| Viết báo cáo ML `ML_CLEANING_REPORT.md` | Chưa bắt đầu | *[Điền]* | Báo cáo sai số MAE/RMSE |
| Xây dựng Mô hình dự báo (Linear/Logistic) | Chưa bắt đầu | *[Điền]* | scikit-learn (Barem 1.0 đ) |
| Hoàn thiện `CLEANING_LOG.md` & `DATA_DICTIONARY.md` | Chưa bắt đầu | *[Điền]* | Ghi chú cờ ML |
| Biểu đồ #1: Combo Bar + Line trục kép | Chưa bắt đầu | *[Điền]* | Tần suất & Thiệt hại |
| Biểu đồ #2: Stacked Area Chart | Chưa bắt đầu | *[Điền]* | Cơ cấu thảm họa theo năm |
| Biểu đồ #3: Choropleth Map thế giới | Chưa bắt đầu | *[Điền]* | Thiệt hại/vụ theo nước |
| Biểu đồ #4: Heatmap Tháng $\times$ Năm | Chưa bắt đầu | *[Điền]* | Chu kỳ mùa cháy rừng |

---

## 3. Danh Sách Checklist Chi Tiết

### A. Thu Thập Dữ Liệu
- [x] Tìm hiểu và khảo sát $\ge 3$ nguồn dữ liệu: NASA FIRMS, EM-DAT, USFS/Kaggle Wildfires, Our World in Data, NOAA NCEI.
- [x] Lập bảng so sánh chi tiết trong `docs/DATA_SOURCES.md` (phạm vi, quy mô, giấy phép, độ tin cậy).
- [x] Viết `src/01_download.py` tự động tải dữ liệu vào `data/raw/`.
- [x] Hướng dẫn tải thủ công chi tiết trong `docs/DATA_SOURCES.md` và `data/raw/emdat/README.md` đối với nguồn yêu cầu đăng ký (EM-DAT).

### B. Khám Phá Dữ Liệu (EDA) - Trọng số Barem: 0.75 Điểm
- [ ] Viết `src/02_eda.py` và tạo Jupyter Notebook `notebooks/01_initial_eda.ipynb`.
- [ ] Sử dụng **Matplotlib** và **Seaborn** vẽ tối thiểu **3 – 5 biểu đồ tĩnh** để phân tích phân phối trước khi đưa lên Dashboard (theo đúng barem Mục II.1):
  - [ ] `eda_01_missing_values.png`: Biểu đồ cột / ma trận khuyết thiếu (`missingno` / `seaborn`).
  - [ ] `eda_02_distributions.png`: Biểu đồ phân phối Histogram + KDE cho diện tích cháy (`burned_area_ha`) và thiệt hại (`damage_usd`).
  - [ ] `eda_03_outliers_boxplot.png`: Biểu đồ hộp (Boxplot) phát hiện ngoại lai sơ bộ cho số người chết và số người ảnh hưởng.
  - [ ] `eda_04_correlation_heatmap.png`: Bản đồ nhiệt tương quan (Correlation Heatmap) giữa các biến số định lượng.
  - [ ] `eda_05_temporal_trend.png`: Biểu đồ đường xu hướng sơ bộ số vụ thảm họa qua các năm.
- [ ] Xuất toàn bộ biểu đồ vào thư mục `reports/figures/`.
- [ ] Lập tài liệu `docs/DATA_QUALITY_REPORT.md` phản ánh tình trạng dữ liệu trước làm sạch.

### C. Làm Sạch Theo Quy Tắc (Rule-based Cleaning)
- [ ] Viết `src/03_clean.py`:
  - [ ] Lọc phạm vi thời gian 2006–2025.
  - [ ] Chuẩn hóa tên quốc gia về chuẩn ISO 3166-1 alpha-3 bằng `country_converter` hoặc `pycountry`.
  - [ ] Chuẩn hóa tọa độ địa lý (Vĩ độ: [-90, 90], Kinh độ: [-180, 180]).
  - [ ] Chuẩn hóa đơn vị đo: diện tích về Hecta (ha), thiệt hại quy về USD.
  - [ ] Xử lý các giá trị âm bất hợp lý, loại bỏ trùng lặp.
  - [ ] Bảo toàn các cột dữ liệu gốc song song (`damage_usd_raw`, `burned_area_ha_raw`).
  - [ ] Xuất kết quả vào `data/interim/master_rules_cleaned.csv`.

### D. Làm Sạch Bằng Học Máy (Machine Learning Cleaning - $\ge 2$ Mô Hình)
- [ ] Viết `src/03b_ml_clean.py`:
  - [ ] **Mô hình 1 (Phát hiện ngoại lai)**: Áp dụng **Isolation Forest** (đối soát với **Local Outlier Factor**) trên các biến `log1p`: `deaths`, `affected`, `damage_usd`, `burned_area_ha`.
  - [ ] Gắn cờ `is_outlier_ml = True/False` và tính `outlier_score`. Không tự động xóa hàng loạt.
  - [ ] Kiểm tra thủ công top 20 dòng bất thường nhất, đối soát nguồn và ghi quyết định (giữ/sửa/loại) vào `docs/CLEANING_LOG.md`.
  - [ ] **Mô hình 2 (Điền giá trị thiếu)**: Áp dụng **KNN Imputer** hoặc **Iterative Imputer (MICE)** cho các biến số có tỷ lệ thiếu vừa phải. Cột thiếu $> 60\%$ giữ nguyên `NULL`.
  - [ ] Gắn cờ `<col>_is_imputed = True/False` cho từng biến được điền.
  - [ ] Thực hiện thử nghiệm che ngẫu nhiên 10–20% giá trị đã biết, so sánh sai số MAE / RMSE với phương pháp Baseline (Median).
  - [ ] *(Khuyến khích)*: Áp dụng **Random Forest Classifier** dự đoán `cause_group` khi xác suất $\ge 0.7$, gắn cờ `cause_is_predicted`.
  - [ ] **Yêu cầu cứng**: Đặt câu lệnh `assert len(df) >= 5000` ở cuối script.
  - [ ] Xuất kết quả ra `data/clean/master_clean.csv`.
- [ ] Viết báo cáo thực nghiệm chi tiết `docs/ML_CLEANING_REPORT.md`.
- [ ] Ghi lại mọi quyết định xử lý vào `docs/CLEANING_LOG.md`.
- [ ] Cập nhật định nghĩa tất cả các trường dữ liệu và các cột cờ vào `docs/DATA_DICTIONARY.md`.

### E. Xây Dựng Mô Hình Dự Báo (Predictive Model - Barem 1.0 Điểm)
- [ ] Viết script `src/08_predictive_model.py` (hoặc tích hợp phân tích) bằng `scikit-learn`:
  - [ ] **Mô hình Hồi quy tuyến tính (Linear Regression)**: Dự báo xu hướng thiệt hại tài chính (`damage_usd`) hoặc diện tích rừng bị cháy (`burned_area_ha`) qua các năm theo yếu tố thời gian và khí hậu.
  - [ ] Hoặc **Mô hình Hồi quy Logistic (Logistic Regression)**: Phân loại nhị phân/đa lớp xác suất thảm họa trở thành "Đại thảm họa / Mức độ nghiêm trọng cao" (`Damage Severity Level >= Serious`).
- [ ] Tính toán và báo cáo các chỉ số đánh giá độ chuẩn xác: $R^2$, MAE, RMSE (với Linear) hoặc Accuracy, Precision, Recall, F1, ROC-AUC (với Logistic).
- [ ] Tích hợp thành công kết quả dự báo (đường xu hướng Trend Line / phân lớp rủi ro) lên biểu đồ trực quan trong Dashboard Tableau (`Sheet_01_Combo_Trend` hoặc phối hợp cùng TV2/TV3).

---

### 4. Các Biểu Đồ Phụ Trách (2 Worksheets: #1 và #2 trên Tableau)

> **Lưu ý quan trọng khi nạp/crawl dữ liệu mới**:  
> Toàn bộ pipeline làm sạch (`03_clean.py`) xuất ra định dạng chuẩn mực khớp 100% với `docs/DATA_DICTIONARY.md`. Khi Thành viên 1 crawl thêm dữ liệu mới hoặc cập nhật nguồn, chỉ cần chạy lại pipeline làm sạch $\to$ trong Tableau nhấn **Refresh Data Source** là 2 biểu đồ này (và toàn bộ hệ thống 10 biểu đồ) sẽ tự động đồng bộ hóa chuẩn xác mà không cần chỉnh sửa lại đồ họa.

### Worksheet #1: `Sheet_01_Combo_Trend` (Combo Cột số vụ + Đường thiệt hại USD theo năm)
- [ ] (a) Kéo `YEAR([start_date])` vào Columns; kéo `CNT([event_id])` (Bar) và `SUM([Damage Bil USD])` (Line) vào Rows.
- [ ] (b) Thiết lập trục kép Dual Axis trong Tableau, gán màu chuẩn: Cột xanh `#4A90E2`, Đường cam `#D55E00`.
- [ ] (c) Bật đường **Trend Line** (Linear Regression) để tích hợp trực quan mô hình dự báo thiệt hại.
- [ ] (d) Định dạng Tooltip tiếng Việt rõ ràng (Số vụ, Tỷ USD).
- [ ] (e) Ghi nhận insight từ dữ liệu thật vào `docs/CHART_SPEC.md` để đưa vào Story Point 1.

### Worksheet #2: `Sheet_02_Stacked_Area` (Stacked Area Tần suất theo loại thảm họa theo năm)
- [ ] (a) Kéo `YEAR([start_date])` vào Columns; kéo `CNT([event_id])` vào Rows; chọn Marks: Area.
- [ ] (b) Kéo `[disaster_type]` vào Color, áp dụng bảng màu chuẩn; ghim Wildfire ở lớp dưới cùng.
- [ ] (c) Định dạng Tooltip hiển thị tỷ lệ % cơ cấu theo năm.
- [ ] (d) Ghi nhận insight từ dữ liệu thật vào `docs/CHART_SPEC.md` để đưa vào Story Point 1.

---

## 5. Đầu Vào & Đầu Ra (Deliverables)
- **Đầu vào**:
  - Dữ liệu thô từ các cổng dữ liệu mở quốc tế (EM-DAT, NASA FIRMS, USFS, OWID).
  - Tài liệu quy chuẩn màu sắc `docs/COLOR_GUIDE.md` và công thức tính toán `tableau/CALCULATED_FIELDS.md`.
- **Đầu ra**:
  - `data/raw/` (dữ liệu thô và nhật ký tải/crawl).
  - `src/01_download.py`, `src/02_eda.py`, `src/03_clean.py`, `src/03b_ml_clean.py`, `src/08_predictive_model.py`.
  - `notebooks/01_initial_eda.ipynb` (kèm 3–5 biểu đồ tĩnh xuất vào `reports/figures/`).
  - `data/clean/master_clean.csv` ($\ge 5.000$ dòng, tự động tương thích với Tableau).
  - `docs/DATA_SOURCES.md`, `docs/DATA_QUALITY_REPORT.md`, `docs/CLEANING_LOG.md`, `docs/ML_CLEANING_REPORT.md`, `docs/DATA_DICTIONARY.md`.
  - 2 Worksheets Tableau (`Sheet_01`, `Sheet_02`) hoàn chỉnh.

---

## 6. Definition of Done (DoD) Cá Nhân
1. Mọi script thực thi từ đầu đến cuối không phát sinh lỗi (`python src/01_...` $\to$ `python src/03b_...` $\to$ `python src/08_...`).
2. Tập dữ liệu `data/clean/master_clean.csv` sau khi áp dụng đầy đủ quy tắc làm sạch đạt tối thiểu 5.000 dòng, sẵn sàng mở rộng khi có dữ liệu crawl mới.
3. Báo cáo ML phản ánh đầy đủ mô hình Hồi quy Linear/Logistic và tích hợp đường dự báo.
4. 2 Worksheets Tableau (#1, #2) hiển thị chuẩn xác, đúng màu sắc quy định và sẵn sàng ghép vào Dashboard D1.
5. Không commit file lớn $> 90$ MB và commit thông điệp chuẩn Conventional Commits.
