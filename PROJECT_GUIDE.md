# HƯỚNG DẪN DỰ ÁN & PHÂN CÔNG NHIỆM VỤ (PROJECT GUIDE)

> **Môn học**: Tương tác dữ liệu trực quan (Interactive Data Visualization)  
> **Đề tài**: Nghiên cứu – phân tích tần suất và thiệt hại của các trận cháy rừng tại California / Bắc Mỹ trong 20 năm qua (2006–2025)  
> **Kho lưu trữ (Repository)**: `https://github.com/tpdk0105/IDV_TTDL`  

---

## 1. Giới Thiệu Đề Tài & Mục Tiêu

### 1.1. Bối cảnh & Tính cấp thiết
Trong giai đoạn 20 năm qua (2006–2025), biến đổi khí hậu cùng các đợt hạn hán kéo dài và gió mùa khô hạn (Santa Ana, Diablo) đã biến **Bang California (Hoa Kỳ)** thành tâm điểm cháy rừng khốc liệt nhất Bắc Mỹ. Những trận cháy rừng thảm khốc như *Camp Fire (2018)*, *August Complex (2020)*, *Dixie Fire (2021)* hay *Tubbs Fire (2017)* không chỉ thiêu rụi hàng triệu mẫu rừng (Acres) mà còn phá hủy hàng chục nghìn công trình nhà cửa, gây thiệt hại hàng chục tỷ USD và cướp đi sinh mạng của nhiều người dân.

### 1.2. Mục tiêu nghiên cứu
- Thu thập, làm sạch và tích hợp dữ liệu cháy rừng chuyên sâu California giai đoạn 2006–2025 từ 5 cơ quan quản lý và khoa học hàng đầu: **CAL FIRE FRAP** (California Department of Forestry and Fire Protection), **CAL FIRE DINS** (Damage Inspection Database), **USDA Forest Service & NIFC** (ICS-209-PLUS Incident Reports), **Cục Điều tra Dân số / CDTFA** (California Counties Demographics) và **NOAA NCEI** (National Oceanic and Atmospheric Administration).
- Đảm bảo tập dữ liệu kết nối đa bảng ($\ge 3$ bảng thực thể) với quy mô lớn ($> 157.000$ dòng thô, $\ge 5.000$ dòng sau làm sạch và tích hợp).
- Đảm bảo chuỗi dữ liệu phủ **đầy đủ 20/20 năm liên tục (2006–2025)** trên tất cả các chiều phân tích cốt lõi: Tần suất vụ cháy, Diện tích thiêu rụi (Acres/ha), Thiệt hại công trình/nhà cửa (`structures_destroyed`), và Thương vong sinh mạng (`deaths`, `injuries`).
- Áp dụng các kỹ thuật Kỹ thuật Dữ liệu (Data Engineering) hiện đại kết hợp Học máy (Machine Learning) để chuẩn hóa, phát hiện ngoại lai bất thường (Isolation Forest/LOF) và xử lý giá trị khuyết thiếu (KNN/Iterative Imputer).
- Thiết kế mô hình dữ liệu chuẩn hình sao (Star Schema) tối ưu hóa trên SQLite với hệ thống ràng buộc toàn vẹn nghiêm ngặt (PK, FK, CHECK, UNIQUE, NOT NULL).
- Xây dựng hệ thống bảng điều khiển và câu chuyện dữ liệu trực quan tương tác (**Interactive Dashboard & Tableau Story**) bằng **Tableau Desktop / Tableau Public** với 10 biểu đồ trực quan chuyên sâu (thuộc 9 loại biểu đồ khác nhau), phân thành 3 Dashboard (D1 $\to$ D3) và 1 Tableau Story (với 3 Story Points dẫn dắt câu chuyện phân tích), đồng thời nhúng trực tiếp vào giao diện web GitHub Pages.

---

## 2. Bảng Danh Sách Thành Viên & Vai Trò (Mô Hình Pipeline Tuần Tự - Bàn Giao Độc Lập)

> **Mô hình phối hợp tuần tự (Decoupled Pipeline)**:  
> - **Thành viên 1**: Đảm nhiệm toàn bộ phần Tiền xử lý, EDA tĩnh và Huấn luyện Mô hình ML Dự báo trên Python $\to$ Bàn giao `master_clean.csv` và kết quả dự báo `forecast_results.csv` cho TV2. (TV1 phụ trách 2 biểu đồ #1, #2).  
> - **Thành viên 2**: Nhận dữ liệu sạch từ TV1 $\to$ Thiết kế Star Schema $\ge 3$ bảng, nạp CSDL SQLite, kiểm thử toàn vẹn $\to$ Bàn giao CSDL SQLite và truy vấn dữ liệu cho TV3. (TV2 phụ trách 4 biểu đồ #3–#6).  
> - **Thành viên 3**: Nhận dữ liệu và kết quả dự báo từ TV1/TV2 $\to$ Dựng 3 Dashboard tương tác, trực quan hóa kết quả dự báo của TV1 lên Dashboard, và xây dựng toàn bộ Tableau Story (Storytelling). (TV3 phụ trách 4 biểu đồ #7–#10).

| Thành viên | Họ và tên | MSSV / Email liên hệ | Vai trò chính & Nhiệm vụ tuần tự | Nhánh Git riêng |
|------------|-----------|----------------------|-----------------------------------|-----------------|
| **Thành viên 1** | [TÊN THÀNH VIÊN 1] | *[Điền MSSV/Email]* | **Kỹ sư Dữ liệu & Học máy**: Thu thập dữ liệu ($\ge 5.000$ dòng), EDA tĩnh (3–5 hình Seaborn/Matplotlib), Làm sạch dữ liệu, **Huấn luyện Mô hình dự báo Linear/Logistic trên Python**; Phụ trách 2 biểu đồ #1, #2 | `member-1-data` |
| **Thành viên 2** | [TÊN THÀNH VIÊN 2] | *[Điền MSSV/Email]* | **Kỹ sư Mô hình Dữ liệu**: Thiết kế Star Schema $\ge 3$ bảng, Ràng buộc toàn vẹn CSDL SQLite (PK, FK, CHECK), Truy vấn SQL; Phụ trách 4 biểu đồ #3–#6 | `member-2-model` |
| **Thành viên 3** | [TÊN THÀNH VIÊN 3] | *[Điền MSSV/Email]* | **Kỹ sư Trực quan hóa & Triển khai**: Dựng 3 Dashboards (Bộ lọc, Drill-down, Tooltip), **Trực quan hóa kết quả dự báo của TV1 lên Dashboard**, **Khai phá Insight & Storytelling (3 Story Points)**, DevOps CI/CD; Phụ trách 4 biểu đồ #7–#10 | `member-3-dashboard` |

---

## 3. Bảng Tổng Hợp Tiến Độ Toàn Nhóm

> **Nguyên tắc phân công**: Mỗi đầu việc chỉ do **ĐÚNG MỘT** thành viên chịu trách nhiệm độc lập. Không ghi cột "người review" hay "người cùng làm". Nhóm tự cập nhật cột Trạng thái và Deadline.

| Mã | Giai đoạn & Hạng mục công việc | Người phụ trách | Trạng thái | Deadline | Ghi chú |
|----|--------------------------------|-----------------|------------|----------|---------|
| **G1** | Khởi tạo repo, cấu trúc thư mục, môi trường, tài liệu phân công | Cả nhóm | **Hoàn thành** | Tuần 1 | Giai đoạn 1 |
| **G2.1** | Tìm, đánh giá 5 nguồn dữ liệu California đủ 20 năm, viết `DATA_SOURCES.md` | Thành viên 1 | **Hoàn thành** | Tuần 2 | CAL FIRE FRAP, DINS, ICS-209, NOAA, Census |
| **G2.2** | Viết script tải dữ liệu thô `01_download.py` và sinh manifest | Thành viên 1 | **Hoàn thành** | Tuần 2 | Lưu 5 file vào `data/raw/calfire/` |
| **G2.3** | Phân tích EDA `02_eda.py` (3-5 biểu đồ Matplotlib/Seaborn) + `DATA_QUALITY_REPORT.md` | Thành viên 1 | Chưa bắt đầu | *[Điền]* | Lưu vào `reports/figures/` |
| **G2.4** | Làm sạch theo quy tắc `03_clean.py` $\to$ `master_rules_cleaned.csv` | Thành viên 1 | Chưa bắt đầu | *[Điền]* | Chuẩn Hạt (County), Acres, ha, USD |
| **G2.5** | Làm sạch bằng Học máy `03b_ml_clean.py` (Isolation Forest, MICE/KNN) | Thành viên 1 | Chưa bắt đầu | *[Điền]* | $\ge 2$ mô hình ML |
| **G2.6** | Đánh giá mô hình ML, viết `ML_CLEANING_REPORT.md`, `CLEANING_LOG.md` | Thành viên 1 | Chưa bắt đầu | *[Điền]* | Cam kết $\ge 5.000$ dòng |
| **G2.7** | Hoàn thiện từ điển dữ liệu `DATA_DICTIONARY.md` | Thành viên 1 | Chưa bắt đầu | *[Điền]* | Mô tả các cột cờ ML & khóa liên kết |
| **G2.8** | Xây dựng Mô hình dự báo (Linear/Logistic Regression) | Thành viên 1 | Chưa bắt đầu | *[Điền]* | scikit-learn (Barem 1.0 đ) |
| **G3.1** | Thiết kế Star Schema (Fact, Dims, ERD Mermaid) | Thành viên 2 | Chưa bắt đầu | *[Điền]* | Hoàn thiện `ERD.md` (3 bảng liên kết) |
| **G3.2** | Viết script tách bảng `04_split_tables.py` vào `data/tables/` | Thành viên 2 | Chưa bắt đầu | *[Điền]* | Tối thiểu 3NF |
| **G3.3** | Soạn thảo DDL `sql/schema.sql` (PK, FK, CHECK, UNIQUE, INDEX) | Thành viên 2 | Chưa bắt đầu | *[Điền]* | Ràng buộc toàn vẹn |
| **G3.4** | Viết script nạp DB `05_build_db.py` (`database.sqlite`) | Thành viên 2 | Chưa bắt đầu | *[Điền]* | Bật foreign_keys = ON |
| **G3.5** | Viết script kiểm thử toàn vẹn `07_validate.py` & bộ test `tests/` | Thành viên 2 | Chưa bắt đầu | *[Điền]* | Kiểm tra không có FK mồ côi |
| **G3.6** | Viết truy vấn SQL cho biểu đồ trong `sql/queries_for_charts.sql` | Thành viên 2 | Chưa bắt đầu | *[Điền]* | Chuẩn bị dữ liệu cho Tableau |
| **G4.1** | Dựng 10 Worksheets trong Tableau Desktop / Tableau Public | Cả nhóm (2/4/4) | Chưa bắt đầu | *[Điền]* | TV1: #1–#2, TV2: #3–#6, TV3: #7–#10 |
| **G4.2** | Thiết kế 3 Dashboard (D1 $\to$ D3) trên Tableau | Thành viên 3 | Chưa bắt đầu | *[Điền]* | Ghép biểu đồ + bộ lọc + KPI |
| **G4.3** | Xây dựng Tableau Story với 3 Story Points trọng tâm | Thành viên 3 | Chưa bắt đầu | *[Điền]* | Cốt truyện dẫn dắt + Annotation |
| **G4.4** | Lưu file `wildfire_disaster_analysis.twbx` vào `tableau/` & xuất bản Tableau Public | Thành viên 3 | Chưa bắt đầu | *[Điền]* | Lưu file đóng gói .twbx |
| **G4.5** | Nhúng Tableau Story vào `dashboard/index.html` | Thành viên 3 | Chưa bắt đầu | *[Điền]* | Hiển thị trên GitHub Pages |
| **G5.1** | Cấu hình GitHub Actions CI/CD `.github/workflows/deploy.yml` | Thành viên 3 | **Hoàn thành** | Tuần 1 | Deploy GitHub Pages |
| **G5.2** | Tổng hợp các phát hiện chính (Key Insights) trong từng Story Point | Cả nhóm | Chưa bắt đầu | *[Điền]* | Dữ liệu thật 20 năm California |
| **G5.3** | Quay Video Demo & Video Backup tóm tắt (Bắt buộc) | Thành viên 3 | Chưa bắt đầu | *[Điền]* | Dự phòng khi vấn đáp |
| **G5.4** | Soạn Báo cáo chuẩn khoa học IEEE ($\ge 40$ trang), README, DEMO SCRIPT | Cả nhóm | Chưa bắt đầu | *[Điền]* | Theo 7 mục bắt buộc |
| **G5.5** | Kiểm thử tổng thể (Không lỗi Tableau, .twbx mở tốt, pytest pass) | Cả nhóm | Chưa bắt đầu | *[Điền]* | Nghiệm thu đồ án |

---

## 4. Quy Ước Làm Việc & Hợp Tác Kỹ Thuật

1. **Quy tắc phân nhánh (Branching Model)**:
   - Nhánh `main`: Chứa mã nguồn ổn định, đã kiểm thử và sẵn sàng triển khai.
   - Nhánh `member-1-data`: Thành viên 1 thực hiện các tác vụ dữ liệu, ML và biểu đồ #1–#2.
   - Nhánh `member-2-model`: Thành viên 2 thực hiện các tác vụ mô hình hóa, CSDL SQLite và biểu đồ #3–#6.
   - Nhánh `member-3-dashboard`: Thành viên 3 thực hiện khung dashboard, Tableau Story, CI/CD và biểu đồ #7–#10.
   - Merge vào `main` thông qua **Pull Request (PR)** sau khi chạy kiểm thử thành công.
2. **Quy ước thông điệp Commit (Conventional Commits)**:
   - `feat:` Thêm tính năng mới (vd: `feat: implement isolation forest cleaning in 03b_ml_clean.py`)
   - `fix:` Sửa lỗi (vd: `fix: handle missing incident names in DINS join`)
   - `docs:` Thêm hoặc cập nhật tài liệu (vd: `docs: update DATA_DICTIONARY.md with California fire attributes`)
   - `data:` Thao tác liên quan đến dữ liệu (vd: `data: update interim rules cleaned dataset`)
   - `chore:` Cấu hình công cụ, môi trường (vd: `chore: pin requirements versions`)
3. **Giới hạn kích thước tập tin**:
   - **Tuyệt đối không commit file $> 90$ MB** lên Git (GitHub giới hạn 100 MB).
   - Thư mục `data/raw/` chứa file thô lớn được cấu hình trong `.gitignore`. Khi cần chia sẻ file lớn, sử dụng lấy mẫu đại diện hoặc nén/tổng hợp.
4. **Bảo mật & Biến môi trường**:
   - Không commit thông tin nhạy cảm hay API keys. Sử dụng file `.env` (đã nằm trong `.gitignore`) nếu phát sinh.
5. **Tôn trọng phạm vi tập tin (Ownership of Code)**:
   - Mỗi thành viên phụ trách các tập tin riêng của mình. Không tự ý chỉnh sửa tập tin của thành viên khác để tránh xung đột mã nguồn (merge conflict).

---

## 5. Lịch Mốc Triển Khai (Milestones Timeline)

| Mốc thời gian | Tên Mốc | Mục tiêu bàn giao chính | Thời hạn (Deadline) |
|---------------|---------|-------------------------|---------------------|
| **Tuần 1** | Mốc 1: Khởi tạo | Hoàn thành cấu trúc repo, file phân công, cấu hình môi trường chuẩn | *[Nhóm điền]* |
| **Tuần 2** | Mốc 2: Dữ liệu sạch | Hoàn tất thu thập, EDA, làm sạch quy tắc & làm sạch ML $\ge 5.000$ dòng | *[Nhóm điền]* |
| **Tuần 3** | Mốc 3: CSDL & Quan hệ | Hoàn tất tách bảng, nạp `database.sqlite` ($\ge 3$ bảng), kiểm thử ràng buộc | *[Nhóm điền]* |
| **Tuần 4** | Mốc 4: Trực quan hóa | Hoàn thành 3 dashboard, 10 biểu đồ tương tác, bộ lọc, Storytelling | *[Nhóm điền]* |
| **Tuần 5** | Mốc 5: Hoàn thiện | Triển khai GitHub Pages, viết báo cáo IEEE $\ge 40$ trang, kịch bản thuyết trình demo | *[Nhóm điền]* |

---

## 6. Phân Công Chi Tiết & Nhiệm Vụ 3 Thành Viên

### Thành viên 1 – DỮ LIỆU (Thu thập $\to$ Làm sạch bằng Quy tắc & Học máy $\to$ Mô hình Dự báo)
- [x] Tìm và thu thập 5 bộ dữ liệu chuyên sâu về Cháy rừng California (CAL FIRE FRAP, CAL FIRE DINS, USDA ICS-209-PLUS, California Demographics, NOAA Casualties); lập bảng so sánh trong `docs/DATA_SOURCES.md`.
- [x] Tải và kiểm kê toàn bộ 5 tệp dữ liệu vào `data/raw/calfire/` bằng script tự động `src/01_download.py` kèm sinh mã băm SHA-256 trong `data/raw/MANIFEST.md` và `data/raw/manifest.json`.
- [ ] Phân tích khám phá dữ liệu (EDA) qua `src/02_eda.py` và notebook `notebooks/01_initial_eda.ipynb`:
  - Dùng **Matplotlib** và **Seaborn** vẽ tối thiểu **3 – 5 biểu đồ tĩnh** (phân phối diện tích cháy log, boxplot công trình bị phá hủy, tương quan diện tích vs công trình, ma trận khuyết thiếu, xu hướng số vụ theo năm).
  - Lưu vào `reports/figures/` và xuất báo cáo chất lượng ban đầu `docs/DATA_QUALITY_REPORT.md`.
- [ ] **Làm sạch bước 1 theo quy tắc (`src/03_clean.py`)**:
  - Hợp nhất chuỗi dữ liệu thiệt hại nhà cửa liên tục 20 năm: Giai đoạn 2006–2012 từ ICS-209 và giai đoạn 2013–2025 từ DINS.
  - Chuẩn hóa Khóa 1: Tên vụ cháy (`fire_name`: viết hoa, cắt khoảng trắng, loại bỏ hậu tố `FIRE`, `INCIDENT`, `COMPLEX`).
  - Chuẩn hóa Khóa 2: Năm vụ cháy (`year`: số nguyên [2006, 2025]).
  - Chuẩn hóa Khóa 3: Đối soát không gian địa lý (`county` $\leftrightarrow$ `Unit ID`) để khử trùng lặp các đám cháy trùng tên cùng năm.
  - Quy đổi đơn vị diện tích (Acres sang ha), xử lý giá trị âm, khử trùng lặp và xuất `data/interim/master_rules_cleaned.csv`.
- [ ] **Làm sạch bước 2 bằng Học máy (`src/03b_ml_clean.py`) với TỐI THIỂU 2 MÔ HÌNH**:
  1. *Isolation Forest & LOF*: Phát hiện bất thường trên biến đổi log1p (`acres_burned`, `structures_destroyed`); chỉ gắn cờ `is_outlier_ml` và tính `outlier_score`, đối soát thủ công top 20 mẫu bất thường, ghi lý do trong `docs/CLEANING_LOG.md`.
  2. *KNN Imputer hoặc Iterative Imputer (MICE)*: Điền giá trị thiếu cho biến số (không điền cột thiếu $> 60\%$), gắn cờ `<col>_is_imputed`. Đánh giá bằng che ngẫu nhiên 10–20% đối chiếu MAE/RMSE so với Median Baseline.
  3. *(Khuyến khích)*: *Random Forest Classifier* dự đoán `cause_group` khi mã nguyên nhân khuyết thiếu, gắn cờ `cause_is_predicted`.
- [ ] **Yêu cầu cứng**: `data/clean/master_clean.csv` sau khi xử lý phải có $\ge 5.000$ dòng; script phải có lệnh `assert len(df) >= 5000`.
- [ ] **Xây dựng Mô hình dự báo trên Python (`src/08_predictive_model.py`) (Barem 0.5 điểm)**: Áp dụng thuật toán **Hồi quy tuyến tính (Linear Regression)** hoặc **Hồi quy Logistic** bằng thư viện `scikit-learn`; huấn luyện và đánh giá sai số ($R^2$, RMSE, MAE).
- [ ] **Bàn giao kết quả dự báo cho Pipeline**: Xuất tệp kết quả dự báo `data/clean/forecast_results.csv` (chứa các mốc năm tương lai và giá trị dự báo diện tích cháy / số công trình hư hại) và bàn giao lại cho TV2/TV3 sử dụng trực tiếp trên Dashboard.
- [ ] Hoàn thiện `docs/ML_CLEANING_REPORT.md`, `docs/CLEANING_LOG.md` và `docs/DATA_DICTIONARY.md`.
- [ ] Chịu trách nhiệm dựng 2 biểu đồ độc lập: **#1 (`Sheet_01_Combo_Trend`), #2 (`Sheet_02_Stacked_Area`)** (TV1 dựng khung biểu đồ cơ bản và đường Trend Line).
- [ ] Đảm bảo cơ chế tự động tương thích: Khi refresh dữ liệu trong Tableau là biểu đồ tự cập nhật.

### Thành viên 2 – MÔ HÌNH DỮ LIỆU (Tách bảng $\ge 3$ bảng $\to$ CSDL SQLite $\to$ Star Schema 3NF)
- [x] Thiết kế Star Schema $\ge 3$ bảng từ `master_clean.csv`: `dim_county`, `dim_cause`, `dim_date`, `fact_fire_incident`, `fact_structure_damage`. Mỗi bảng đạt tối thiểu 3NF, có surrogate key. Bảo toàn các cột cờ ML trong bảng fact (`is_outlier_ml`, `*_is_imputed`, `cause_is_predicted`).
- [x] Viết `src/04_split_tables.py` tách bảng thành các file CSV lưu tại `data/tables/`.
- [x] Viết DDL `sql/schema.sql` với đầy đủ: PRIMARY KEY, FOREIGN KEY (`ON DELETE RESTRICT ON UPDATE CASCADE`), NOT NULL, UNIQUE, CHECK constraints (`acres_burned >= 0`, `structures_destroyed >= 0`, `year BETWEEN 2006 AND 2025`, `latitude BETWEEN 32 AND 42`, `longitude BETWEEN -125 AND -114`), DEFAULT hợp lý, và INDEX tối ưu truy vấn JOIN/WHERE.
- [x] Viết script `src/05_build_db.py` tạo `database.sqlite`, kích hoạt `PRAGMA foreign_keys = ON;`, nạp dữ liệu và kiểm tra vi phạm ràng buộc (Zero Orphan FK).
- [x] Vẽ sơ đồ thực thể liên kết `docs/ERD.md` bằng Mermaid `erDiagram` với đầy đủ bản số quan hệ (Cardinality 1–N).
- [x] Viết `src/07_validate.py` và bộ kiểm thử `tests/`: kiểm tra toàn vẹn tham chiếu (không có FK mồ côi), không trùng khóa chính, fact $\ge 5.000$ dòng, toàn bộ ràng buộc CHECK đạt chuẩn, cột cờ nhận 0/1.
- [x] Viết các truy vấn SQL cho biểu đồ của mình trong `sql/queries_for_charts.sql` và hướng dẫn Calculated Fields trong `tableau/CALCULATED_FIELDS.md`.
- [x] Chịu trách nhiệm thực hiện trọn vẹn 4 biểu đồ trên Tableau: **#3 (`Sheet_03_Diverging_Bar`), #4 (`Sheet_04_Treemap_Damage`), #5 (`Sheet_05_Bubble_Scatter`), #6 (`Sheet_06_Combo_Histogram`)**.

### Thành viên 3 – DASHBOARD & TRIỂN KHAI (Tableau Public $\to$ Trực quan hóa Dự báo $\to$ Storytelling $\to$ DevOps)
- [ ] Thiết lập môi trường Tableau Desktop / Tableau Public, kết nối nguồn dữ liệu sạch từ `data/clean/master_clean.csv`.
- [ ] Phụ trách thực hiện 4 biểu đồ chuyên sâu của mình: **#7 (`Sheet_07_Combo_Pareto`), #8 (`Sheet_08_Donut_Cause`), #9 (`Sheet_09_Choropleth_Map`), #10 (`Sheet_10_Proportional_Map`)** dưới dạng các Tableau Worksheets.
- [ ] Thiết kế **3 Dashboards** hoàn chỉnh (D1: Bức tranh 20 năm Cháy rừng California, D2: Điểm nóng & Phân cấp thiệt hại theo 58 Hạt, D3: Mùa vụ, Căn nguyên & Tương quan Siêu đám cháy) với bố cục khoa học, thẻ KPI Cards, tính năng Lọc (Filter nhiều cấp) và Đi sâu chi tiết (Drill-down).
- [ ] **Trực quan hóa kết quả dự báo lên Dashboard (Barem 0.5 điểm)**: Nhận kết quả mô hình dự báo từ TV1, cấu hình hiển thị đường xu hướng dự báo (Trend Line / Forecast) trực tiếp trên Dashboard D1.
- [ ] **Khai phá Insight & Xây dựng Tableau Story (Barem 1.0 điểm)**: Dựa trên toàn bộ hệ thống 10 biểu đồ và kết quả dự báo của TV1, TV3 độc lập xây dựng **Tableau Story với 3 Story Points** dẫn dắt câu chuyện phân tích chuyên sâu (Bức tranh 20 năm California $\to$ Điểm nóng tổn thất 58 Hạt theo 80/20 $\to$ Căn nguyên, Siêu đám cháy & Xu thế tương lai), gắn các chú thích Annotation sắc sảo.
- [ ] Đóng gói và lưu tệp Workbook `tableau/wildfire_disaster_analysis.twbx`, xuất bản lên Tableau Public và lấy đường link nhúng vào `dashboard/index.html`.
- [ ] Triển khai pipeline CI/CD `.github/workflows/deploy.yml` tự động xuất bản trang web chứa bản nhúng Tableau lên GitHub Pages.
- [ ] Quay **Video Demo** đóng vai Data Analyst và chuẩn bị **Video backup tóm tắt** đề phòng khi bảo vệ.
- [ ] Soạn thảo và hoàn thiện Báo cáo khoa học IEEE ($\ge 40$ trang) theo 7 mục bắt buộc trong `docs/REPORT_OUTLINE.md`, kèm `README.md` và `docs/DEMO_SCRIPT.md`.

---

## 7. Cấu Trúc 3 Dashboard, Tableau Story & Phân Chia 10 Biểu Đồ

### CẤU TRÚC 3 DASHBOARD (mỗi dashboard 3–4 biểu đồ, 1 câu hỏi chính)
Ba dashboard nối nhau như một câu chuyện hoàn chỉnh: **bức tranh chung 20 năm California → phân bố theo 58 hạt & nguyên lý 80/20 → căn nguyên, siêu đám cháy & dự báo tương lai**.

| Dashboard | Câu hỏi chính | Biểu đồ trong dashboard |
|-----------|---------------|-------------------------|
| **D1 – Bức tranh 20 năm Cháy rừng California** (Xu hướng vĩ mô) | Tần suất và mức độ tàn phá của cháy rừng California biến động thế nào qua 2006–2025, và xu hướng dự báo tương lai ra sao? | #1 `Combo_Trend` (TV1); #2 `Stacked_Area` (TV1); #3 `Diverging_Bar` (TV2) |
| **D2 – Điểm nóng & Phân cấp thiệt hại theo 58 Hạt** (Không gian & 80/20) | Những Hạt (Counties) nào chịu thiệt hại nhà cửa và tài sản nặng nề nhất, có tuân theo nguyên lý 80/20 không? | #4 `Treemap_Damage` (TV2); #7 `Combo_Pareto` (TV3); #9 `Choropleth_Map` (TV3) |
| **D3 – Mùa vụ, Căn nguyên & Siêu đám cháy** (Chi tiết chuyên sâu) | Mùa cao điểm cháy rừng bùng phát khi nào, căn nguyên do tự nhiên hay con người, và các siêu đám cháy phân bố ở đâu? | #5 `Bubble_Scatter` (TV2); #6 `Combo_Histogram` (TV2); #8 `Donut_Cause` (TV3); #10 `Proportional_Map` (TV3) |

Bố cục mỗi dashboard: dải tiêu đề (tên + câu hỏi chính) → 2–3 KPI card → 3–4 biểu đồ → hộp "Insight" 1–2 câu → chuyển sang dashboard kế tiếp.

### KỂ CHUYỆN BẰNG TABLEAU STORY (3 Story Points Trọng Tâm)
- **Tableau Story** kết nối 3 Dashboard thành một chuỗi trình bày phân tích với **3 Story Points** đúng chuẩn barem:
  1. **Point 1**: *Bức tranh 20 năm Cháy rừng California: Tần suất & Thiệt hại* (Nhúng D1, chú thích đỉnh điểm năm 2020/2018 và đường xu hướng dự báo Linear Regression).
  2. **Point 2**: *Điểm nóng tổn thất 58 Hạt California: Phân cấp 80/20* (Nhúng D2, chú thích nguyên lý Pareto 80/20 về nhà cửa bị phá hủy).
  3. **Point 3**: *Căn nguyên, Siêu đám cháy & Thách thức Tương lai* (Nhúng D3, chú thích các siêu đám cháy $\ge 100.000$ Acres, tác nhân con người vs sét đánh).
- Mọi con số trong Insight và Annotation phải được **TÍNH TỪ DỮ LIỆU THẬT**, không viết số liệu cảm tính.

### PHÂN CHIA 10 BIỂU ĐỒ (Phân chia 2/4/4; MỖI BIỂU ĐỒ CHỈ DO 1 NGƯỜI THỰC HIỆN; gồm 9 loại biểu đồ khác nhau)
| # | Tên Sheet Tableau | Dashboard | Kiểu dữ liệu / Thể loại | Bảng màu | Người phụ trách |
|---|-------------------|-----------|-------------------------|----------|-----------------|
| 1 | `Sheet_01_Combo_Trend` (Combo cột số vụ cháy + đường diện tích cháy theo năm + Trend Line) | D1 | Dual-Axis Combo | Cột xanh + Đường cam | **TV1 (1/2)** |
| 2 | `Sheet_02_Stacked_Area` (Stacked area cơ cấu nguyên nhân cháy theo thời gian) | D1 | Stacked Area | Okabe-Ito | **TV1 (2/2)** |
| 3 | `Sheet_03_Diverging_Bar` (Diverging bar chênh lệch số vụ cháy so với trung bình 20 năm) | D1 | Diverging Bar | Red-Blue Diverging | **TV2 (1/4)** |
| 4 | `Sheet_04_Treemap_Damage` (Treemap phân cấp Hạt $\to$ Loại công trình bị phá hủy) | D2 | Treemap | Phân cấp theo Hạt | **TV2 (2/4)** |
| 5 | `Sheet_05_Bubble_Scatter` (Bubble scatter diện tích cháy vs số nhà phá hủy vs thương vong) | D3 | Bubble Scatter (Log-Log) | Theo Vùng Hạt | **TV2 (3/4)** |
| 6 | `Sheet_06_Combo_Histogram` (Combo histogram diện tích cháy theo logarit + đường phân vị lũy kế) | D3 | Combo Histogram | Cam đất + Đường xanh | **TV2 (4/4)** |
| 7 | `Sheet_07_Combo_Pareto` (Combo Pareto cột nhà bị phá hủy top 10 Hạt + đường % lũy kế 80/20) | D2 | Pareto Chart | Đỏ mận + Đường cam | **TV3 (1/4)** |
| 8 | `Sheet_08_Donut_Cause` (Donut 2 tầng nguyên nhân: Tự nhiên vs Con người) | D3 | Donut / Sunburst | Xanh (Tự nhiên) / Đỏ cam | **TV3 (2/4)** |
| 9 | `Sheet_09_Choropleth_Map` (Choropleth California: thiệt hại/số nhà cháy theo 58 Hạt) | D2 | Choropleth Map (Bắt buộc) | Orange-Red | **TV3 (3/4)** |
| 10| `Sheet_10_Proportional_Map` (Bản đồ điểm các đại vụ cháy lớn California: cỡ = diện tích, màu = số nhà cháy) | D3 | Proportional Symbol Map | Đỏ cam nổi bật | **TV3 (4/4)** |

### QUY TRÌNH 4 BƯỚC CHO MỖI THÀNH VIÊN KHI LÀM BIỂU ĐỒ TRÊN TABLEAU
1. **Mở Tableau và tạo Worksheet**: Kéo thả Dimensions và Measures theo đúng đặc tả tại [docs/CHART_SPEC.md](docs/CHART_SPEC.md).
2. **Tạo Calculated Fields cần thiết**: Sử dụng công thức chuẩn trong [tableau/CALCULATED_FIELDS.md](tableau/CALCULATED_FIELDS.md).
3. **Định dạng hiển thị chuẩn**: Tooltip tiếng Việt rõ ràng, có đơn vị đo lường (Acres, công trình phá hủy, người, USD), màu sắc đúng quy chuẩn.
4. **Ghi vào `CHART_SPEC.md`**: Ghi lại 1 phát hiện quan trọng (Insight) rút ra từ dữ liệu thật để đưa vào Story Point.

---

## 8. Định Nghĩa Hoàn Thành (Definition of Done - DoD)

### DoD Giai đoạn 1 (Khởi tạo dự án & Môi trường):
- Cấu trúc thư mục được khởi tạo đầy đủ kèm `.gitkeep`.
- Các file khung `.py`, `.sql`, `.md` có tiêu đề, docstring, mục đích và người phụ trách rõ ràng.
- `PROJECT_GUIDE.md` và 3 file `team/*/TASKS.md` được biên soạn chi tiết, không vi phạm nguyên tắc phân công.
- Đẩy thành công lên Git nhánh `main` và 3 nhánh thành viên `member-1-data`, `member-2-model`, `member-3-dashboard`.

### DoD Giai đoạn 2 (Dữ liệu):
- Dữ liệu thô lưu tại `data/raw/calfire/` có nguồn gốc rõ ràng, ghi trong `DATA_SOURCES.md`.
- `master_clean.csv` đạt $\ge 5.000$ dòng và có lệnh `assert` kiểm tra.
- Quy trình ML áp dụng $\ge 2$ mô hình (Isolation Forest, KNN/Iterative Imputer); có báo cáo thực nghiệm trong `ML_CLEANING_REPORT.md`.
- Toàn bộ cột cờ và dữ liệu được ghi nhận đầy đủ trong `DATA_DICTIONARY.md` và `CLEANING_LOG.md`.

### DoD Giai đoạn 3 (Mô hình Dữ liệu):
- CSDL `database.sqlite` được tạo bằng `05_build_db.py` với `PRAGMA foreign_keys = ON;`.
- Có $\ge 3$ bảng chuẩn hóa thực hiện JOIN trong SQL; Bảng fact đạt $\ge 5.000$ dòng, không có khóa ngoại mồ côi, toàn bộ ràng buộc CHECK đạt chuẩn.
- Script `07_validate.py` và bộ test `pytest` thực thi kiểm thử tự động đạt 100% pass.

### DoD Giai đoạn 4 (Tableau Dashboard & Storytelling):
- Hoàn thành đầy đủ 10 Worksheets trong Tableau (chia theo tỷ lệ 2/4/4 cho 3 thành viên, gồm 9 loại biểu đồ).
- Hoàn thành 3 Dashboards (D1 $\to$ D3) với KPI Cards, bộ lọc năm/Hạt và hộp Insight.
- Hoàn thành 1 Tableau Story với ít nhất 3 Story Points có chú thích nổi bật từ số liệu thật.
- File workbook đóng gói `tableau/wildfire_disaster_analysis.twbx` được lưu trữ trong repo và mở lên hoạt động trơn tru.

### DoD Giai đoạn 5 (Xuất bản & Nghiệm thu):
- Xuất bản thành công lên Tableau Public và nhúng liên kết vào `dashboard/index.html` (chạy trên GitHub Pages).
- `README.md` có đầy đủ ảnh chụp, link demo Tableau Public và hướng dẫn mở file `.twbx`.
- Hoàn thành đầy đủ báo cáo tổng kết IEEE ($\ge 40$ trang) và kịch bản thuyết trình demo.

