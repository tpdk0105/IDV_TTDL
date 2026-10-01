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
6. Hoàn thành 4 biểu đồ được giao (#1, #2, #3, #4) theo đúng đặc tả và bảng màu chuẩn.

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

### B. Khám Phá Dữ Liệu (EDA)
- [ ] Viết `src/02_eda.py` và tạo Jupyter Notebook `notebooks/01_initial_eda.ipynb`.
- [ ] Thống kê phân phối, tỷ lệ khuyết thiếu (vẽ ma trận missingno), trùng lặp, giá trị âm và ngoại lai sơ bộ.
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

---

## 4. Các Biểu Đồ Phụ Trách (#1, #2, #3, #4)

### Biểu Đồ #1: Combo Cột số vụ + Đường thiệt hại USD theo năm (Trục kép)
- [ ] (a) Viết câu truy vấn SQL tổng hợp số vụ và thiệt hại theo năm trong `sql/queries_for_charts.sql`.
- [ ] (b) Xuất dữ liệu JSON tương ứng vào `dashboard/data/chart_01_data.json`.
- [ ] (c) Dựng biểu đồ ECharts trục kép trong `dashboard/js/charts/chart-01.js` với 2 màu tương phản theo `COLOR_GUIDE.md`.
- [ ] (d) Gắn tương tác Brush chọn dải năm và đồng bộ sự kiện lọc chéo (Cross-filter).
- [ ] (e) Hoàn thiện mục Biểu đồ 1 trong `docs/CHART_SPEC.md` và ghi nhận 1–2 insight từ dữ liệu thật.

### Biểu Đồ #2: Stacked Area Tần suất theo loại thảm họa theo năm
- [ ] (a) Viết câu truy vấn SQL tổng hợp số vụ theo từng loại thảm họa và theo năm.
- [ ] (b) Xuất dữ liệu JSON tương ứng vào `dashboard/data/chart_02_data.json`.
- [ ] (c) Dựng biểu đồ Stacked Area ECharts trong `dashboard/js/charts/chart-02.js` với bảng màu Okabe-Ito chuẩn.
- [ ] (d) Gắn tương tác bật/tắt Legend và click chọn loại thảm họa để lọc toàn hệ thống.
- [ ] (e) Hoàn thiện mục Biểu đồ 2 trong `docs/CHART_SPEC.md` và ghi nhận insight từ dữ liệu thật.

### Biểu Đồ #3: Choropleth Map Toàn cầu (Thiệt hại / Số vụ theo quốc gia)
- [ ] (a) Viết câu truy vấn SQL tổng hợp số vụ, thiệt hại theo mã quốc gia ISO3.
- [ ] (b) Xuất dữ liệu JSON tương ứng vào `dashboard/data/chart_03_data.json`.
- [ ] (c) Dựng bản đồ Choropleth ECharts trong `dashboard/js/charts/chart-03.js` với dải màu tuần tự Sequential (OrRd).
- [ ] (d) Tích hợp nút chuyển đổi giữa "Số vụ" và "Thiệt hại USD"; gắn sự kiện click quốc gia để lọc dashboard.
- [ ] (e) Hoàn thiện mục Biểu đồ 3 trong `docs/CHART_SPEC.md` và ghi nhận insight từ dữ liệu thật.

### Biểu Đồ #4: Heatmap Tháng $\times$ Năm (Chu kỳ mùa cháy rừng)
- [ ] (a) Viết câu truy vấn SQL đếm số vụ cháy rừng theo từng cặp (Tháng, Năm).
- [ ] (b) Xuất dữ liệu JSON tương ứng vào `dashboard/data/chart_04_data.json`.
- [ ] (c) Dựng ma trận Heatmap ECharts trong `dashboard/js/charts/chart-04.js` với dải màu nhiệt Sequential (YlOrRd).
- [ ] (d) Gắn VisualMap liên tục và tương tác click ô tháng/năm.
- [ ] (e) Hoàn thiện mục Biểu đồ 4 trong `docs/CHART_SPEC.md` và ghi nhận insight từ dữ liệu thật.

---

## 5. Đầu Vào & Đầu Ra (Deliverables)
- **Đầu vào**:
  - Dữ liệu thô từ các cổng dữ liệu mở quốc tế (EM-DAT, NASA FIRMS, USFS, OWID).
  - Tài liệu quy chuẩn màu sắc `docs/COLOR_GUIDE.md`.
- **Đầu ra**:
  - `data/raw/` (dữ liệu thô và nhật ký tải).
  - `src/01_download.py`, `src/02_eda.py`, `src/03_clean.py`, `src/03b_ml_clean.py`.
  - `notebooks/01_initial_eda.ipynb`.
  - `data/interim/master_rules_cleaned.csv` và `data/clean/master_clean.csv` ($\ge 5.000$ dòng).
  - `docs/DATA_SOURCES.md`, `docs/DATA_QUALITY_REPORT.md`, `docs/CLEANING_LOG.md`, `docs/ML_CLEANING_REPORT.md`, `docs/DATA_DICTIONARY.md`.
  - `dashboard/js/charts/chart-01.js`, `chart-02.js`, `chart-03.js`, `chart-04.js`.

---

## 6. Definition of Done (DoD) Cá Nhân
1. Mọi script thực thi từ đầu đến cuối không phát sinh lỗi (`python src/01_...` $\to$ `python src/03b_...`).
2. Tập dữ liệu `data/clean/master_clean.csv` sau khi áp dụng đầy đủ quy tắc và mô hình ML đạt tối thiểu 5.000 dòng.
3. Báo cáo ML phản ánh đầy đủ thực nghiệm kiểm chứng với Baseline.
4. 4 biểu đồ (#1–#4) hiển thị chuẩn xác trên Dashboard, tương tác mượt mà và đúng màu sắc quy định.
5. Không commit file lớn $> 90$ MB và commit thông điệp chuẩn Conventional Commits.
