# Sổ Tay Phân Công Nhiệm Vụ & Quy Ước Đặt Tên File Khi Đưa Lên Git

> **Kho lưu trữ (Repository)**: [https://github.com/tpdk0105/IDV_TTDL](https://github.com/tpdk0105/IDV_TTDL)  
> **Đồ án**: "Nghiên cứu – phân tích tần suất và thiệt hại của các trận cháy rừng / thảm họa thiên nhiên trong 20 năm qua (2006–2025)"  
> **Áp dụng cho**: Cả 3 thành viên nhóm (`member-1-data`, `member-2-model`, `member-3-dashboard`)  

---

## PHẦN 1: CHI TIẾT CÔNG VIỆC CỦA TỪNG THÀNH VIÊN

Mỗi đầu việc chỉ do **ĐÚNG MỘT** thành viên chịu trách nhiệm chính. Mọi người làm việc độc lập trên nhánh Git riêng của mình và phối hợp thông qua Pull Request.

```
┌────────────────────────────────────────────────────────────────────────┐
│                   DÒNG CHẢY CÔNG VIỆC TOÀN NHÓM                        │
│                                                                        │
│   [Thành viên 1]        ──> master_clean.csv (>= 5.000 dòng)          │
│   (Thu thập & ML)                   │                                  │
│                                     ▼                                  │
│   [Thành viên 2]        ──> Tách bảng Star Schema & CSDL SQLite        │
│   (Mô hình hóa & SQL)               │                                  │
│                                     ▼                                  │
│   [Cả 3 thành viên]     ──> 12 Worksheets trong Tableau (4/4/4)       │
│                                     │                                  │
│                                     ▼                                  │
│   [Thành viên 3]        ──> 4 Dashboards & Tableau Story (4 Points)    │
│   (Dashboard & DevOps)  ──> Xuất bản Tableau Public & GitHub Pages     │
└────────────────────────────────────────────────────────────────────────┘
```

---

### 👤 THÀNH VIÊN 1: KỸ SƯ DỮ LIỆU (DATA ENGINEER)

- **Nhánh Git phụ trách**: `member-1-data`
- **File chi tiết công việc**: [team/member-1-data/TASKS.md](member-1-data/TASKS.md)
- **Trọng tâm**: Xây dựng toàn bộ Data Pipeline từ dữ liệu thô $\to$ làm sạch quy tắc $\to$ làm sạch học máy $\to$ phụ trách 4 biểu đồ Tableau #1–#4.

#### Danh sách công việc cụ thể:
1. **Khảo sát nguồn dữ liệu**: Đánh giá ít nhất 3–5 nguồn quốc tế uy tín (OWID, NASA FIRMS, NOAA NCEI, USFS FPA-FOD, EM-DAT), viết bảng so sánh và phân tích tại [docs/DATA_SOURCES.md](../docs/DATA_SOURCES.md).
2. **Thu thập dữ liệu thô tự động**: Viết script tái lập [src/01_download.py](../src/01_download.py) tải dữ liệu vào `data/raw/` kèm theo tự động sinh bản kiểm tra tính toàn vẹn `data/raw/MANIFEST.md` (mã băm SHA-256).
3. **Phân tích khám phá dữ liệu (EDA)**: Viết [src/02_eda.py](../src/02_eda.py) và tạo Jupyter Notebook [notebooks/01_initial_eda.ipynb](../notebooks/01_initial_eda.ipynb); xuất báo cáo chất lượng ban đầu [docs/DATA_QUALITY_REPORT.md](../docs/DATA_QUALITY_REPORT.md).
4. **Làm sạch theo quy tắc (Rule-based Cleaning)**: Viết [src/03_clean.py](../src/03_clean.py) chuẩn hóa mã quốc gia ISO3, tọa độ, đơn vị diện tích (ha), thiệt hại (USD) $\to$ xuất `data/interim/master_rules_cleaned.csv`.
5. **Làm sạch bằng Học máy (Machine Learning Cleaning)**: Viết [src/03b_ml_clean.py](../src/03b_ml_clean.py) áp dụng **tối thiểu 2 mô hình ML**:
   - *Phát hiện ngoại lai*: Áp dụng **Isolation Forest** (đối soát với LOF) trên biến logarit, gắn cờ `is_outlier_ml` và điểm số `outlier_score`.
   - *Điền giá trị khuyết thiếu*: Áp dụng **KNN Imputer** hoặc **Iterative Imputer (MICE)**, gắn cờ `<col>_is_imputed`. Thử nghiệm che ngẫu nhiên 10–20% đối soát sai số MAE/RMSE so với Baseline (Median).
   - **Cam kết số dòng**: Đặt lệnh `assert len(df) >= 5000` ở cuối script $\to$ xuất file `data/clean/master_clean.csv`.
6. **Tài liệu làm sạch**: Hoàn thiện [docs/ML_CLEANING_REPORT.md](../docs/ML_CLEANING_REPORT.md), [docs/CLEANING_LOG.md](../docs/CLEANING_LOG.md) và [docs/DATA_DICTIONARY.md](../docs/DATA_DICTIONARY.md).
7. **Phụ trách 4 Worksheets trên Tableau**:
   - `Sheet_01_Combo_Trend`: Combo Dual-Axis cột số vụ + đường thiệt hại USD theo năm 2006–2025.
   - `Sheet_02_Stacked_Area`: Stacked Area tần suất theo loại thảm họa theo thời gian.
   - `Sheet_03_Choropleth_Map`: Bản đồ thế giới phân vùng mức độ thiệt hại/số vụ theo quốc gia.
   - `Sheet_04_Heatmap_Season`: Heatmap ma trận chu kỳ mùa cháy rừng (Tháng $\times$ Năm).

---

### 👤 THÀNH VIÊN 2: KỸ SƯ MÔ HÌNH DỮ LIỆU (DATA MODELING ENGINEER)

- **Nhánh Git phụ trách**: `member-2-model`
- **File chi tiết công việc**: [team/member-2-model/TASKS.md](member-2-model/TASKS.md)
- **Trọng tâm**: Thiết kế Star Schema 3NF, CSDL SQLite với đầy đủ ràng buộc toàn vẹn, kiểm thử tự động $\to$ phụ trách 4 biểu đồ Tableau #5–#8.

#### Danh sách công việc cụ thể:
1. **Thiết kế Star Schema 3NF**:
   - Các bảng chiều (Dimensions): `dim_date`, `dim_location`, `dim_disaster_type`, `dim_cause`, `dim_source`.
   - Các bảng sự kiện (Facts): `fact_disaster_event`, `fact_wildfire_detail`. Bảo toàn đầy đủ các cột cờ ML (`is_outlier_ml`, `*_is_imputed`).
   - Vẽ sơ đồ quan hệ thực thể bằng cú pháp Mermaid `erDiagram` trong [docs/ERD.md](../docs/ERD.md).
2. **Tách bảng tự động**: Viết script [src/04_split_tables.py](../src/04_split_tables.py) đọc từ `master_clean.csv`, tạo surrogate keys và xuất các file CSV vào thư mục `data/tables/`.
3. **Soạn thảo DDL CSDL**: Viết [sql/schema.sql](../sql/schema.sql) với đầy đủ:
   - `PRIMARY KEY`, `FOREIGN KEY (ON DELETE RESTRICT ON UPDATE CASCADE)`.
   - Ràng buộc kiểm tra `CHECK` (`deaths >= 0`, `damage_usd >= 0`, `burned_area_ha >= 0`, `year BETWEEN 2006 AND 2025`, `latitude BETWEEN -90 AND 90`, `longitude BETWEEN -180 AND 180`).
   - Ràng buộc `UNIQUE`, `NOT NULL`, giá trị `DEFAULT` và chỉ mục `CREATE INDEX`.
4. **Xây dựng CSDL SQLite**: Viết script [src/05_build_db.py](../src/05_build_db.py) kích hoạt `PRAGMA foreign_keys = ON;`, tạo `data/tables/database.sqlite` và nạp dữ liệu.
5. **Kiểm thử toàn vẹn tự động**: Viết [src/07_validate.py](../src/07_validate.py) và bộ kiểm thử [tests/test_pipeline.py](../tests/test_pipeline.py) (chạy qua `pytest`), kiểm tra 100% không có khóa ngoại mồ côi (Zero Orphan FK) và bảng fact $\ge 5.000$ dòng.
6. **Viết truy vấn SQL**: Hoàn thiện [sql/queries_for_charts.sql](../sql/queries_for_charts.sql) tối ưu cho 12 biểu đồ.
7. **Phụ trách 4 Worksheets trên Tableau**:
   - `Sheet_05_Diverging_Bar`: Biến động số vụ so với mức chuẩn trung bình 20 năm (tâm = 0).
   - `Sheet_06_Treemap_Damage`: Treemap phân cấp cơ cấu thiệt hại kinh tế: Châu lục $\to$ Quốc gia.
   - `Sheet_07_Bubble_Scatter`: Bubble Scatter tương quan diện tích cháy vs thiệt hại USD (Trục Log-Log).
   - `Sheet_08_Combo_Histogram`: Combo Histogram phân phối diện tích cháy theo logarit + Đường phân vị lũy kế.

---

### 👤 THÀNH VIÊN 3: KỸ SƯ DASHBOARD, TABLEAU STORY & DEVOPS

- **Nhánh Git phụ trách**: `member-3-dashboard`
- **File chi tiết công việc**: [team/member-3-dashboard/TASKS.md](member-3-dashboard/TASKS.md)
- **Trọng tâm**: Thiết kế 4 Dashboards, xây dựng Tableau Story (4 Story Points), xuất bản Tableau Public, đóng gói file `.twbx`, quản lý CI/CD GitHub Pages $\to$ phụ trách 4 biểu đồ Tableau #9–#12.

#### Danh sách công việc cụ thể:
1. **Phụ trách 4 Worksheets trên Tableau**:
   - `Sheet_09_Combo_Pareto`: Combo Pareto Chart cột số người chết top 10 quốc gia + Đường % lũy kế 80/20.
   - `Sheet_10_Donut_Cause`: Donut / Sunburst 2 tầng phân tích nguyên nhân cháy rừng (Tự nhiên vs Con người).
   - `Sheet_11_Sankey_Flow`: Luồng chuyển giao tác động: Nhóm nguyên nhân $\to$ Loại thảm họa $\to$ Mức thiệt hại.
   - `Sheet_12_Proportional_Map`: Bản đồ điểm phân bố không gian các đại vụ cháy rừng lớn (Cỡ = ha, Màu = USD).
2. **Thiết kế 4 Dashboards chuyên đề trong Tableau**:
   - **Dashboard D1: Bức tranh 20 năm** (Ghép `Sheet_01`, `Sheet_02`, `Sheet_05` + KPI Cards + Slider dải năm).
   - **Dashboard D2: Ở đâu chịu thiệt hại?** (Ghép `Sheet_03`, `Sheet_06`, `Sheet_09` + Filter Châu lục).
   - **Dashboard D3: Cháy rừng: Khi nào & lớn cỡ nào?** (Ghép `Sheet_04`, `Sheet_08`, `Sheet_12` + Filter tháng).
   - **Dashboard D4: Vì sao & hệ quả** (Ghép `Sheet_10`, `Sheet_11`, `Sheet_07` + Filter nguyên nhân).
3. **Xây dựng Tableau Story với 4 Story Points**:
   - Dẫn dắt câu chuyện phân tích logic theo 4 chủ đề lớn.
   - Gắn chú thích (Annotation) làm nổi bật số liệu thật (đỉnh kỷ lục 2020, ngưỡng 80/20, mùa khô tháng 6–9).
4. **Đóng gói & Xuất bản**:
   - Xuất file workbook đóng gói: `tableau/wildfire_disaster_analysis.twbx`.
   - Xuất bản lên **Tableau Public** và nhúng vào `dashboard/index.html`.
5. **Vận hành DevOps & CI/CD**: Duy trì quy trình tự động hóa [.github/workflows/deploy.yml](../.github/workflows/deploy.yml) để xuất bản Dashboard lên **GitHub Pages**.
6. **Tài liệu tổng kết**: Hoàn thiện [README.md](../README.md), [docs/REPORT_OUTLINE.md](../docs/REPORT_OUTLINE.md) và [docs/DEMO_SCRIPT.md](../docs/DEMO_SCRIPT.md).

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
  - `XX`: 2 chữ số biểu thị thứ tự thực thi trong pipeline (`01`, `02`, `03`, `03b`, `04`, `05`, `06`, `07`).
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

#### B. Thư mục dữ liệu (`data/`)
- **Dữ liệu thô (`data/raw/`)**:
  - Cấu trúc: `data/raw/<ten_nguon>/<ten_file_goc>.<ext>`
  - Giữ nguyên tên file từ nhà cung cấp để bảo toàn tính nguyên bản và đối soát mã băm SHA-256 (ví dụ: `data/raw/nasa_firms/MODIS_C6_1_Global_7d.csv`, `data/raw/owid/natural-disasters-by-type.csv`).
- **Dữ liệu trung gian (`data/interim/`)**:
  - Cấu trúc: `snake_case.csv` (ví dụ: `data/interim/master_rules_cleaned.csv`).
- **Dữ liệu sạch hoàn chỉnh (`data/clean/`)**:
  - File bắt buộc: `data/clean/master_clean.csv`.
- **Dữ liệu các bảng phân rã (`data/tables/`)**:
  - Tên file CSV **bắt buộc trùng khớp 100% với tên bảng trong CSDL SQLite**:
    - ✅ `dim_date.csv`
    - ✅ `dim_location.csv`
    - ✅ `dim_disaster_type.csv`
    - ✅ `dim_cause.csv`
    - ✅ `dim_source.csv`
    - ✅ `fact_disaster_event.csv`
    - ✅ `fact_wildfire_detail.csv`
  - File CSDL SQLite duy nhất: `data/tables/database.sqlite`.

#### C. Thư mục truy vấn SQL (`sql/`)
- **Quy tắc**: `sql/<ten_tac_vu>.sql` (chữ thường `snake_case`).
- **Danh sách file chuẩn mực**:
  - ✅ `sql/schema.sql`: Định nghĩa cấu trúc bảng DDL (PK, FK, CHECK).
  - ✅ `sql/load.sql`: Kịch bản nạp dữ liệu.
  - ✅ `sql/queries_for_charts.sql`: Toàn bộ các truy vấn SQL cho 12 biểu đồ (có ghi chú rõ `-- Chart #N | Thành viên X`).

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
  - `Sheet_XX_<Ten_Bieu_Do>` (ví dụ: `Sheet_01_Combo_Trend`, `Sheet_03_Choropleth_Map`, `Sheet_09_Combo_Pareto`).
- **Quy tắc đặt tên Dashboard bên trong Tableau**:
  - `Dashboard_DX_<Ten_Chu_De>` (ví dụ: `Dashboard_D1_Buc_Tranh_20_Nam`, `Dashboard_D2_O_Dau_Chiu_Thiet_Hai`).
- **Quy tắc đặt tên Story Point trong Tableau Story**:
  - Tiêu đề thanh dẫn: `X. <Noi_Dung_Ngan_Gon>` (ví dụ: `1. Bức tranh 20 năm`, `2. Điểm nóng toàn cầu`, `3. Mùa vụ & Siêu đám cháy`, `4. Nguyên nhân & Tác động`).

#### F. Quy ước nhánh Git (Git Branches) & Commit Message
- **Tên nhánh bắt buộc**:
  - Nhánh chính: `main`
  - Nhánh TV1: `member-1-data`
  - Nhánh TV2: `member-2-model`
  - Nhánh TV3: `member-3-dashboard`
- **Quy chuẩn thông điệp Commit (Conventional Commits)**:
  - `feat:` Thêm tính năng mới / script mới (vd: `feat: add isolation forest model in 03b_ml_clean.py`)
  - `data:` Thêm hoặc cập nhật dữ liệu thô/sạch (vd: `data: add master_clean.csv with 5200 rows`)
  - `docs:` Cập nhật tài liệu kỹ thuật (vd: `docs: update chart spec with tableau shelves`)
  - `fix:` Sửa lỗi mã nguồn hoặc CSDL (vd: `fix: resolve foreign key constraint in build_db.py`)
  - `test:` Bổ sung hoặc chỉnh sửa bộ test (vd: `test: add assertions for table row count`)
  - `chore:` Cấu hình công cụ, môi trường (vd: `chore: update requirements.txt and gitignore`)

---

## PHẦN 3: BẢNG KIỂM TRA NHANH TRƯỚC KHI PUSH LÊN GIT (PRE-PUSH CHECKLIST)

Trước khi thực hiện lệnh `git push`, mỗi thành viên hãy tự kiểm tra 5 câu hỏi vàng sau:

- [ ] **1. Tên file**: Có file nào chứa dấu cách, chữ có dấu tiếng Việt, hoặc ký tự lạ không?
- [ ] **2. Kích thước**: Có file nào vượt quá 90 MB không? (Chạy lệnh kiểm tra nếu nghi ngờ).
- [ ] **3. Vị trí lưu**: File có được đặt đúng thư mục quy định (`src/`, `data/`, `sql/`, `tableau/`, `docs/`) chưa?
- [ ] **4. Thông điệp commit**: Commit message có đúng chuẩn Conventional Commits (`feat:`, `docs:`, `data:`...) không?
- [ ] **5. Nhánh làm việc**: Bạn có đang ở đúng nhánh của mình (`member-X-...`) trước khi push không?
