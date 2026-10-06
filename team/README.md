# Sổ Tay Phân Công Nhiệm Vụ & Quy Ước Đặt Tên File Khi Đưa Lên Git

> **Kho lưu trữ (Repository)**: [https://github.com/tpdk0105/IDV_TTDL](https://github.com/tpdk0105/IDV_TTDL)  
> **Đề tài**: "Nghiên cứu – phân tích tần suất và thiệt hại của các trận cháy rừng tại California / Bắc Mỹ trong 20 năm qua (2006–2025)"  
> **Áp dụng cho**: Cả 3 thành viên nhóm (`member-1-data`, `member-2-model`, `member-3-dashboard`)  

---

## PHẦN 1: CHI TIẾT CÔNG VIỆC CỦA TỪNG THÀNH VIÊN

Mỗi đầu việc chỉ do **ĐÚNG MỘT** thành viên chịu trách nhiệm chính. Mọi người làm việc độc lập trên nhánh Git riêng của mình và phối hợp thông qua Pull Request.

```
┌────────────────────────────────────────────────────────────────────────┐
│             DÒNG CHẢY CÔNG VIỆC TUẦN TỰ (DECOUPLED PIPELINE)            │
│                                                                        │
│   [Thành viên 1]                                                       │
│   (Kỹ sư Dữ liệu & ML)                                                 │
│        │                                                               │
│        ├─ Tiền xử lý, EDA tĩnh (3-5 hình Seaborn)                      │
│        ├─ Huấn luyện Mô hình ML Dự báo (Linear/Logistic)               │
│        ▼                                                               │
│   BÀN GIAO: master_clean.csv (>= 5.000 dòng) + forecast_results.csv    │
│        │                                                               │
│        ▼                                                               │
│   [Thành viên 2]                                                       │
│   (Kỹ sư Mô hình Dữ liệu)                                              │
│        │                                                               │
│        ├─ Thiết kế Star Schema (Fact + Dims >= 3 bảng)                 │
│        ├─ Nạp CSDL SQLite (PK, FK, CHECK constraints)                  │
│        ▼                                                               │
│   BÀN GIAO: database.sqlite + Các bảng chuẩn hóa & Views SQL           │
│        │                                                               │
│        ▼                                                               │
│   [Thành viên 3]                                                       │
│   (Kỹ sư Trực quan hóa, Storytelling & DevOps)                         │
│        │                                                               │
│        ├─ Dựng 3 Dashboards hoàn chỉnh (10 biểu đồ, Bộ lọc, Drill-down)│
│        ├─ Trực quan hóa kết quả dự báo của TV1 lên Dashboard           │
│        ├─ Xây dựng toàn bộ Tableau Story (3 Points Storytelling)       │
│        ▼                                                               │
│   BÀN GIAO: .twbx + Tableau Public + Deploy GitHub Pages               │
└────────────────────────────────────────────────────────────────────────┘
```

---

### 👤 THÀNH VIÊN 1: KỸ SƯ DỮ LIỆU & HỌC MÁY (DATA & ML ENGINEER)

- **Nhánh Git phụ trách**: `member-1-data`
- **File chi tiết công việc**: [team/member-1-data/TASKS.md](member-1-data/TASKS.md)
- **Trọng tâm**: Xây dựng toàn bộ Data Pipeline từ dữ liệu thô $\to$ làm sạch quy tắc & học máy $\to$ Huấn luyện Mô hình dự báo Linear/Logistic $\to$ phụ trách 2 biểu đồ Tableau #1, #2 (giảm tải việc vẽ đồ họa để tập trung toàn lực vào xử lý dữ liệu và ML).
- **Tính thích ứng dữ liệu**: Toàn bộ hệ thống đảm bảo khi TV1 làm sạch dữ liệu mới, Tableau tự động Refresh cập nhật toàn bộ mà không gãy vỡ layout.

#### Danh sách công việc cụ thể:
1. **Khảo sát nguồn dữ liệu**: Đánh giá 4 nguồn California uy tín (CAL FIRE FRAP, CAL FIRE DINS, California Demographics, NOAA Casualties), viết bảng so sánh và phân tích tại [docs/DATA_SOURCES.md](../docs/DATA_SOURCES.md).
2. **Thu thập dữ liệu thô tự động**: Viết script tái lập [src/01_download.py](../src/01_download.py) tải dữ liệu vào `data/raw/calfire/` kèm theo tự động sinh bản kiểm tra tính toàn vẹn `data/raw/MANIFEST.md` (mã băm SHA-256).
3. **Phân tích khám phá dữ liệu (EDA)**: Viết [src/02_eda.py](../src/02_eda.py) và tạo Jupyter Notebook [notebooks/01_initial_eda.ipynb](../notebooks/01_initial_eda.ipynb); dùng **Matplotlib** và **Seaborn** vẽ tối thiểu **3–5 biểu đồ tĩnh** (histogram phân phối, boxplot ngoại lai, heatmap tương quan, ma trận thiếu); lưu vào `reports/figures/` và xuất báo cáo chất lượng ban đầu [docs/DATA_QUALITY_REPORT.md](../docs/DATA_QUALITY_REPORT.md).
4. **Làm sạch theo quy tắc (Rule-based Cleaning)**: Viết [src/03_clean.py](../src/03_clean.py) chuẩn hóa tên vụ cháy (`fire_name`), Hạt (`county`), quy đổi đơn vị (acres sang ha), xử lý giá trị âm và loại trùng lặp $\to$ xuất `data/interim/master_rules_cleaned.csv`.
5. **Làm sạch bằng Học máy (Machine Learning Cleaning)**: Viết [src/03b_ml_clean.py](../src/03b_ml_clean.py) áp dụng **tối thiểu 2 mô hình ML**:
   - *Phát hiện ngoại lai*: Áp dụng **Isolation Forest** (đối soát với LOF) trên biến logarit, gắn cờ `is_outlier_ml` và điểm số `outlier_score`.
   - *Điền giá trị khuyết thiếu*: Áp dụng **KNN Imputer** hoặc **Iterative Imputer (MICE)**, gắn cờ `<col>_is_imputed`. Thử nghiệm che ngẫu nhiên 10–20% đối soát sai số MAE/RMSE so với Baseline (Median).
6. **Xây dựng Mô hình dự báo trên Python (Barem 0.5 Điểm)**: Áp dụng thuật toán **Hồi quy tuyến tính (Linear Regression)** hoặc **Hồi quy Logistic** bằng `scikit-learn` theo barem Mục II.3; đánh giá độ chính xác ($R^2$, MAE, RMSE); xuất bảng kết quả dự báo `data/clean/forecast_results.csv` bàn giao cho TV2/TV3 sử dụng trên Dashboard.
7. **Tài liệu làm sạch & mô hình**: Hoàn thiện [docs/ML_CLEANING_REPORT.md](../docs/ML_CLEANING_REPORT.md), [docs/CLEANING_LOG.md](../docs/CLEANING_LOG.md) và [docs/DATA_DICTIONARY.md](../docs/DATA_DICTIONARY.md).
8. **Phụ trách 2 Worksheets trên Tableau**:
   - `Sheet_01_Combo_Trend`: Combo Dual-Axis cột số vụ cháy + đường diện tích cháy theo năm 2006–2025 (kèm Trend Line dự báo).
   - `Sheet_02_Stacked_Area`: Stacked Area cơ cấu nguyên nhân cháy theo thời gian.

---

### 👤 THÀNH VIÊN 2: KỸ SƯ MÔ HÌNH DỮ LIỆU (DATA MODELING ENGINEER)

- **Nhánh Git phụ trách**: `member-2-model`
- **File chi tiết công việc**: [team/member-2-model/TASKS.md](member-2-model/TASKS.md)
- **Trọng tâm**: Thiết kế Star Schema $\ge 3$ bảng 3NF, CSDL SQLite với đầy đủ ràng buộc toàn vẹn, kiểm thử tự động $\to$ phụ trách 4 biểu đồ Tableau #3–#6.

#### Danh sách công việc cụ thể:
1. **Thiết kế Star Schema 3NF**:
   - Các bảng chiều (Dimensions): `dim_county` (58 Hạt California), `dim_cause`, `dim_date`.
   - Các bảng sự kiện (Facts): `fact_fire_incident` (7.342 vụ cháy), `fact_structure_damage` (>130.000 công trình). Bảo toàn đầy đủ các cột cờ ML (`is_outlier_ml`, `*_is_imputed`).
   - Vẽ sơ đồ quan hệ thực thể bằng cú pháp Mermaid `erDiagram` trong [docs/ERD.md](../docs/ERD.md).
2. **Tách bảng tự động**: Viết script [src/04_split_tables.py](../src/04_split_tables.py) đọc từ `master_clean.csv`, tạo surrogate keys và xuất các file CSV vào thư mục `data/tables/`.
3. **Soạn thảo DDL CSDL**: Viết [sql/schema.sql](../sql/schema.sql) với đầy đủ:
   - `PRIMARY KEY`, `FOREIGN KEY (ON DELETE RESTRICT ON UPDATE CASCADE)`.
   - Ràng buộc kiểm tra `CHECK` (`acres_burned >= 0`, `structures_destroyed >= 0`, `year BETWEEN 2006 AND 2025`, `latitude BETWEEN 32 AND 42`, `longitude BETWEEN -125 AND -114`).
   - Ràng buộc `UNIQUE`, `NOT NULL`, giá trị `DEFAULT` và chỉ mục `CREATE INDEX`.
4. **Xây dựng CSDL SQLite**: Viết script [src/05_build_db.py](../src/05_build_db.py) kích hoạt `PRAGMA foreign_keys = ON;`, tạo `data/tables/database.sqlite` và nạp dữ liệu.
5. **Kiểm thử toàn vẹn tự động**: Viết [src/07_validate.py](../src/07_validate.py) và bộ kiểm thử [tests/test_pipeline.py](../tests/test_pipeline.py) (chạy qua `pytest`), kiểm tra 100% không có khóa ngoại mồ côi (Zero Orphan FK) và bảng fact $\ge 5.000$ dòng.
6. **Viết truy vấn SQL**: Hoàn thiện [sql/queries_for_charts.sql](../sql/queries_for_charts.sql) tối ưu cho các biểu đồ.
7. **Phụ trách 4 Worksheets trên Tableau**:
   - `Sheet_03_Diverging_Bar`: Biến động số vụ cháy so với mức chuẩn trung bình 20 năm (tâm = 0).
   - `Sheet_04_Treemap_Damage`: Treemap phân cấp cơ cấu nhà cửa bị phá hủy: Hạt $\to$ Loại công trình.
   - `Sheet_05_Bubble_Scatter`: Bubble Scatter tương quan diện tích cháy vs số nhà phá hủy vs thương vong (Trục Log-Log).
   - `Sheet_06_Combo_Histogram`: Combo Histogram phân phối diện tích cháy theo logarit + Đường phân vị lũy kế.

---

### 👤 THÀNH VIÊN 3: KỸ SƯ DASHBOARD, TABLEAU STORY & DEVOPS

- **Nhánh Git phụ trách**: `member-3-dashboard`
- **File chi tiết công việc**: [team/member-3-dashboard/TASKS.md](member-3-dashboard/TASKS.md)
- **Trọng tâm**: Thiết kế 3 Dashboards, xây dựng Tableau Story (3 Story Points), xuất bản Tableau Public, đóng gói file `.twbx`, quản lý CI/CD GitHub Pages $\to$ phụ trách 4 biểu đồ Tableau #7–#10.

#### Danh sách công việc cụ thể:
1. **Phụ trách 4 Worksheets trên Tableau**:
   - `Sheet_07_Combo_Pareto`: Combo Pareto Chart cột số nhà bị phá hủy top 10 Hạt + Đường % lũy kế 80/20.
   - `Sheet_08_Donut_Cause`: Donut 2 tầng phân tích nguyên nhân cháy rừng (Tự nhiên vs Con người).
   - `Sheet_09_Choropleth_Map`: Bản đồ phân vùng 58 Hạt California theo mức độ thiệt hại/số nhà bị cháy (Bản đồ Map bắt buộc).
   - `Sheet_10_Proportional_Map`: Bản đồ điểm phân bố không gian các đại vụ cháy lớn California (Cỡ = Acres, Màu = Nhà phá hủy).
2. **Thiết kế 3 Dashboards chuyên đề trong Tableau**:
   - **Dashboard D1: Bức tranh 20 năm Cháy rừng California** (Ghép `Sheet_01`, `Sheet_02`, `Sheet_03` + KPI Cards + Slider dải năm). **Trực quan hóa kết quả dự báo của TV1 (0.5 đ barem)** qua đường xu hướng Trend Line / Forecast.
   - **Dashboard D2: Điểm nóng & Phân cấp thiệt hại theo 58 Hạt** (Ghép `Sheet_04`, `Sheet_07`, `Sheet_09` + Filter Hạt/Vùng).
   - **Dashboard D3: Mùa vụ, Căn nguyên & Siêu đám cháy** (Ghép `Sheet_05`, `Sheet_06`, `Sheet_08`, `Sheet_10` + Filter nguyên nhân & diện tích).
3. **Khai phá Insight & Xây dựng Tableau Story (1.0 đ barem)**:
   - Độc lập dẫn dắt câu chuyện phân tích logic xuyên suốt qua 3 Story Points (Bức tranh 20 năm California $\to$ Điểm nóng tổn thất 58 Hạt 80/20 $\to$ Căn nguyên, Siêu đám cháy & Thách thức tương lai).
   - Gắn chú thích (Annotation) làm nổi bật số liệu thật (đỉnh kỷ lục 2020 hơn 4.3 triệu Acres, ngưỡng 80/20, siêu đám cháy $\ge 100.000$ Acres, và kết quả mô hình dự báo của TV1).
4. **Đóng gói & Xuất bản**:
   - Xuất file workbook đóng gói: `tableau/wildfire_disaster_analysis.twbx`.
   - Xuất bản lên **Tableau Public** và nhúng vào `dashboard/index.html`.
5. **Vận hành DevOps & CI/CD**: Duy trì quy trình tự động hóa [.github/workflows/deploy.yml](../.github/workflows/deploy.yml) để xuất bản Dashboard lên **GitHub Pages**.
6. **Tài liệu tổng kết**: Hoàn thiện [README.md](../README.md), [docs/REPORT_OUTLINE.md](../docs/REPORT_OUTLINE.md), [docs/DEMO_SCRIPT.md](../docs/DEMO_SCRIPT.md) (kèm Video Demo & Video backup tóm tắt).

---

## PHẦN 2: BỘ RÀNG BUỘC NGHIÊM NGẶT VỀ ĐẶT TÊN FILE KHI ĐƯA LÊN GIT

Để đảm bảo dự án chạy tự động, tương thích hoàn hảo trên mọi hệ điều hành (Windows, Linux, macOS) và không phát sinh lỗi CI/CD, mọi thành viên **BẮT BUỘC tuân thủ 100%** các quy tắc dưới đây trước khi `git add` và `git commit`.

---

### 1. NGUYÊN TẮC CẤM TUYỆT ĐỐI (ZERO TOLERANCE)

| ❌ Hành vi bị cấm | Lý do kỹ thuật | Cách làm đúng chuẩn ✅ |
|---|---|---|
| **CẤM dùng dấu cách (space)** trong tên file/thư mục (ví dụ: `du lieu thoi tiet.csv`) | Gây gãy lệnh trong script shell, URL web bị biến thành `%20`, lỗi CI/CD. | Dùng dấu gạch dưới `_` hoặc gạch ngang `-` (`du_lieu_thoi_tiet.csv`). |
| **CẤM dùng ký tự tiếng Việt có dấu** (ví dụ: `dữ_liệu.csv`, `báo_cáo.md`) | Lỗi encoding mã hóa UTF-8 / CP1258 trên Git Windows và Linux. | Dùng tiếng Anh chuẩn hoặc tiếng Việt không dấu (`master_clean.csv`, `bao_cao.md`). |
| **CẤM dùng ký tự đặc biệt lạ** (`@`, `#`, `$`, `%`, `&`, `*`, `(`, `)`, `?`, `:`, `\`) | Xung đột cú pháp shell command và hệ điều hành. | Chỉ dùng: chữ cái thường `a-z`, số `0-9`, gạch dưới `_`, gạch ngang `-`. |
| **CẤM đặt tên file tùy tiện, tạm bợ** (`test.py`, `data1.csv`, `copy.twbx`, `final_v2.xlsx`) | Không rõ mục đích, khó bảo trì và vi phạm tiêu chuẩn kỹ thuật chuyên nghiệp. | Đặt tên mô tả đúng thực thể và hành động (`03b_ml_clean.py`, `database.sqlite`). |
| **CẤM commit file $> 90$ MB** lên Git | GitHub giới hạn cứng 100 MB / file; vi phạm sẽ bị reject toàn bộ lệnh push. | Nén dữ liệu, lấy mẫu đại diện hoặc tổng hợp trước khi commit. |
| **CẤM commit khóa bảo mật và file rác cá nhân** (`.env`, `.DS_Store`, `Thumbs.db`, `.venv/`) | Nguy cơ rò rỉ bảo mật và làm bẩn lịch sử Git. | Đã cấu hình chặn tự động trong `.gitignore`. |

---

### 2. QUY CHUẨN ĐẶT TÊN CHI TIẾT THEO TỪNG THƯ MỤC

#### A. Thư mục mã nguồn Python (`src/`)
- **Quy tắc**: `src/XX_ten_hanh_dong.py`
  - `XX`: 2 chữ số biểu thị thứ tự thực thi trong pipeline (`01`, `02`, `03`, `03b`, `04`, `05`, `06`, `07`, `08`).
  - `ten_hanh_dong`: Viết bằng tiếng Anh, kiểu `snake_case` (chữ thường nối bằng gạch dưới `_`).
- **Danh sách file chuẩn mực**:
  - ✅ `src/01_download.py`
  - ✅ `src/02_eda.py`
  - ✅ `src/03_clean.py`
  - ✅ `src/03b_ml_clean.py`
  - ✅ `src/04_split_tables.py`
  - ✅ `src/05_build_db.py`
  - ✅ `src/06_export_json.py`
  - ✅ `src/07_validate.py`
  - ✅ `src/08_predictive_model.py`

#### B. Thư mục dữ liệu (`data/`)
- **Dữ liệu thô (`data/raw/`)**:
  - Cấu trúc: `data/raw/calfire/<ten_file_goc>.<ext>`
  - Lưu trữ 4 file: `California_Fire_Perimeters_all.csv`, `CAL_FIRE_Damage_Inspection_DINS.csv`, `California_Counties_Demographics.csv`, `NOAA_California_Wildfires_Casualties.csv`.
- **Dữ liệu trung gian (`data/interim/`)**:
  - File: `data/interim/master_rules_cleaned.csv`.
- **Dữ liệu sạch hoàn chỉnh (`data/clean/`)**:
  - File bắt buộc: `data/clean/master_clean.csv` ($\ge 5.000$ dòng) và `data/clean/forecast_results.csv`.
- **Dữ liệu các bảng phân rã (`data/tables/`)**:
  - Tên file CSV **bắt buộc trùng khớp 100% với tên bảng trong CSDL SQLite**:
    - ✅ `dim_date.csv`
    - ✅ `dim_county.csv`
    - ✅ `dim_cause.csv`
    - ✅ `fact_fire_incident.csv`
    - ✅ `fact_structure_damage.csv`
  - File CSDL SQLite duy nhất: `data/tables/database.sqlite`.

#### C. Thư mục truy vấn SQL (`sql/`)
- **Quy tắc**: `sql/<ten_tac_vu>.sql` (chữ thường `snake_case`).
- **Danh sách file chuẩn mực**:
  - ✅ `sql/schema.sql`: Định nghĩa cấu trúc bảng DDL (PK, FK, CHECK).
  - ✅ `sql/load.sql`: Kịch bản nạp dữ liệu.
  - ✅ `sql/queries_for_charts.sql`: Toàn bộ các truy vấn SQL cho 10 biểu đồ.

#### D. Thư mục tài liệu kỹ thuật (`docs/`)
- **Quy tắc**: `docs/UPPER_SNAKE_CASE.md` (chữ in hoa nối bằng gạch dưới `_`).
- **Danh sách 10 file tài liệu chuẩn**:
  1. ✅ `docs/DATA_SOURCES.md`
  2. ✅ `docs/DATA_DICTIONARY.md`
  3. ✅ `docs/DATA_QUALITY_REPORT.md`
  4. ✅ `docs/CLEANING_LOG.md`
  5. ✅ `docs/ML_CLEANING_REPORT.md`
  6. ✅ `docs/ERD.md`
  7. ✅ `docs/CHART_SPEC.md`
  8. ✅ `docs/COLOR_GUIDE.md`
  9. ✅ `docs/REPORT_OUTLINE.md`
  10. ✅ `docs/DEMO_SCRIPT.md`

#### E. Thư mục Tableau (`tableau/`)
- **Quy tắc đặt tên file workbook**:
  - Tên file đóng gói: `tableau/wildfire_disaster_analysis.twbx` (`snake_case`).
- **Quy tắc đặt tên Worksheet bên trong Tableau**:
  - `Sheet_XX_<Ten_Bieu_Do>` (ví dụ: `Sheet_01_Combo_Trend`, `Sheet_09_Choropleth_Map`, `Sheet_07_Combo_Pareto`).
- **Quy tắc đặt tên Dashboard bên trong Tableau**:
  - `Dashboard_D1_Buc_Tranh_20_Nam`, `Dashboard_D2_Diem_Nong_58_Hat`, `Dashboard_D3_Mua_Vu_Can_Nguyen`.
- **Quy tắc đặt tên Story Point trong Tableau Story**:
  - Tiêu đề thanh dẫn: `1. Bức tranh 20 năm California`, `2. Điểm nóng 58 Hạt (80/20)`, `3. Căn nguyên & Siêu đám cháy`.

#### F. Quy ước nhánh Git (Git Branches) & Commit Message
- **Tên nhánh bắt buộc**:
  - Nhánh chính: `main`
  - Nhánh TV1: `member-1-data`
  - Nhánh TV2: `member-2-model`
  - Nhánh TV3: `member-3-dashboard`
- **Quy chuẩn thông điệp Commit (Conventional Commits)**:
  - `feat:` Thêm tính năng mới / script mới
  - `data:` Thêm hoặc cập nhật dữ liệu thô/sạch
  - `docs:` Cập nhật tài liệu kỹ thuật
  - `fix:` Sửa lỗi mã nguồn hoặc CSDL
  - `test:` Bổ sung hoặc chỉnh sửa bộ test
  - `chore:` Cấu hình công cụ, môi trường

---

## PHẦN 3: BẢNG KIỂM TRA NHANH TRƯỚC KHI PUSH LÊN GIT (PRE-PUSH CHECKLIST)

- [ ] **1. Tên file**: Không chứa dấu cách, chữ có dấu tiếng Việt, hoặc ký tự lạ.
- [ ] **2. Kích thước**: Không vượt quá 90 MB (dữ liệu thô lớn đã nằm trong `.gitignore`).
- [ ] **3. Vị trí lưu**: Đặt đúng thư mục quy định (`src/`, `data/`, `sql/`, `tableau/`, `docs/`).
- [ ] **4. Thông điệp commit**: Đúng chuẩn Conventional Commits (`feat:`, `docs:`, `data:`...).
- [ ] **5. Nhánh làm việc**: Đang ở đúng nhánh của mình (`member-X-...`) trước khi push.
