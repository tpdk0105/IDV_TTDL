# HƯỚNG DẪN DỰ ÁN & PHÂN CÔNG NHIỆM VỤ (PROJECT GUIDE)

> **Môn học**: Tương tác dữ liệu trực quan (Interactive Data Visualization)  
> **Đề tài**: Nghiên cứu – phân tích tần suất và thiệt hại của các trận cháy rừng / thảm họa thiên nhiên trong 20 năm qua (2005–2024)  
> **Kho lưu trữ (Repository)**: `https://github.com/tpdk0105/IDV_TTDL`  

---

## 1. Giới Thiệu Đề Tài & Mục Tiêu

### 1.1. Bối cảnh & Tính cấp thiết
Trong giai đoạn 20 năm qua (2005–2024), biến đổi khí hậu toàn cầu diễn biến phức tạp với sự gia tăng mạnh mẽ cả về tần suất, cường độ và mức độ tàn phá của các thảm họa thiên nhiên. Trong đó, **cháy rừng (Wildfires)** nổi lên như một trong những thách thức nghiêm trọng nhất đối với môi trường sinh thái, an ninh con người và nền kinh tế toàn cầu (các đợt siêu cháy rừng tại Úc 2019–2020, California, Hy Lạp, Canada 2023, Maui 2023).

### 1.2. Mục tiêu nghiên cứu
- Thu thập, làm sạch và tích hợp dữ liệu thảm họa thiên nhiên toàn cầu giai đoạn 2005–2024 từ các nguồn dữ liệu khoa học uy tín (EM-DAT, NASA FIRMS, USFS/NOAA, Our World in Data).
- Áp dụng các kỹ thuật Kỹ thuật Dữ liệu (Data Engineering) hiện đại kết hợp Học máy (Machine Learning) để chuẩn hóa, phát hiện ngoại lai bất thường (Isolation Forest/LOF) và xử lý giá trị khuyết thiếu (KNN/Iterative Imputer).
- Thiết kế mô hình dữ liệu chuẩn hình sao (Star Schema) tối ưu hóa trên SQLite với hệ thống ràng buộc toàn vẹn nghiêm ngặt (PK, FK, CHECK, UNIQUE, NOT NULL).
- Xây dựng hệ thống bảng điều khiển và câu chuyện dữ liệu trực quan tương tác (**Interactive Dashboard & Tableau Story**) bằng **Tableau Desktop / Tableau Public** với 12 biểu đồ trực quan chuyên sâu, phân thành 4 Dashboard (D1 $\to$ D4) và 1 Tableau Story (với 4 Story Points dẫn dắt câu chuyện phân tích), đồng thời nhúng trực tiếp vào giao diện web GitHub Pages.

---

## 2. Bảng Danh Sách Thành Viên & Vai Trò

| Thành viên | Họ và tên | MSSV / Email liên hệ | Vai trò chính | Nhánh Git riêng |
|------------|-----------|----------------------|---------------|-----------------|
| **Thành viên 1** | [TÊN THÀNH VIÊN 1] | *[Điền MSSV/Email]* | Kỹ sư Dữ liệu (Data Engineer): Thu thập, EDA, Làm sạch dữ liệu (Quy tắc + Học máy); Phụ trách 4 biểu đồ Tableau #1–#4 | `member-1-data` |
| **Thành viên 2** | [TÊN THÀNH VIÊN 2] | *[Điền MSSV/Email]* | Kỹ sư Mô hình Dữ liệu (Data Modeling Engineer): Star Schema, Ràng buộc CSDL, SQL; Phụ trách 4 biểu đồ Tableau #5–#8 | `member-2-model` |
| **Thành viên 3** | [TÊN THÀNH VIÊN 3] | *[Điền MSSV/Email]* | Kỹ sư Trực quan hóa & Triển khai (Data Visualization & DevOps): Thiết kế 4 Dashboard & Tableau Story (4 Story Points), CI/CD, Phụ trách 4 biểu đồ Tableau #9–#12 | `member-3-dashboard` |

---

## 3. Bảng Tổng Hợp Tiến Độ Toàn Nhóm

> **Nguyên tắc phân công**: Mỗi đầu việc chỉ do **ĐÚNG MỘT** thành viên chịu trách nhiệm độc lập. Không ghi cột "người review" hay "người cùng làm". Nhóm tự cập nhật cột Trạng thái và Deadline.

| Mã | Giai đoạn & Hạng mục công việc | Người phụ trách | Trạng thái | Deadline | Ghi chú |
|----|--------------------------------|-----------------|------------|----------|---------|
| **G1** | Khởi tạo repo, cấu trúc thư mục, môi trường, tài liệu phân công | Cả nhóm | **Hoàn thành** | Tuần 1 | Giai đoạn 1 |
| **G2.1** | Tìm, đánh giá $\ge 3$ nguồn dữ liệu, viết `DATA_SOURCES.md` | Thành viên 1 | **Hoàn thành** | Tuần 2 | OWID, NASA, NOAA, USFS |
| **G2.2** | Viết script tải dữ liệu thô `01_download.py` | Thành viên 1 | **Hoàn thành** | Tuần 2 | Lưu 7 file vào `data/raw/` |
| **G2.3** | Phân tích khám phá dữ liệu `02_eda.py` + `DATA_QUALITY_REPORT.md` | Thành viên 1 | Chưa bắt đầu | *[Điền]* | Kèm notebook EDA |
| **G2.4** | Làm sạch theo quy tắc `03_clean.py` $\to$ `master_rules_cleaned.csv` | Thành viên 1 | Chưa bắt đầu | *[Điền]* | Chuẩn ISO3, ha, USD |
| **G2.5** | Làm sạch bằng Học máy `03b_ml_clean.py` (Isolation Forest, MICE/KNN) | Thành viên 1 | Chưa bắt đầu | *[Điền]* | $\ge 2$ mô hình ML |
| **G2.6** | Đánh giá mô hình ML, viết `ML_CLEANING_REPORT.md`, `CLEANING_LOG.md` | Thành viên 1 | Chưa bắt đầu | *[Điền]* | Cam kết $\ge 5.000$ dòng |
| **G2.7** | Hoàn thiện từ điển dữ liệu `DATA_DICTIONARY.md` | Thành viên 1 | Chưa bắt đầu | *[Điền]* | Mô tả các cột cờ ML |
| **G3.1** | Thiết kế Star Schema (Fact, Dims, ERD Mermaid) | Thành viên 2 | Chưa bắt đầu | *[Điền]* | Hoàn thiện `ERD.md` |
| **G3.2** | Viết script tách bảng `04_split_tables.py` vào `data/tables/` | Thành viên 2 | Chưa bắt đầu | *[Điền]* | Tối thiểu 3NF |
| **G3.3** | Soạn thảo DDL `sql/schema.sql` (PK, FK, CHECK, UNIQUE, INDEX) | Thành viên 2 | Chưa bắt đầu | *[Điền]* | Ràng buộc toàn vẹn |
| **G3.4** | Viết script nạp DB `05_build_db.py` (`database.sqlite`) | Thành viên 2 | Chưa bắt đầu | *[Điền]* | Bật foreign_keys = ON |
| **G3.5** | Viết script kiểm thử toàn vẹn `07_validate.py` & bộ test `tests/` | Thành viên 2 | Chưa bắt đầu | *[Điền]* | Kiểm tra không có FK mồ côi |
| **G3.6** | Viết truy vấn SQL cho biểu đồ trong `sql/queries_for_charts.sql` | Thành viên 2 | Chưa bắt đầu | *[Điền]* | Chuẩn bị dữ liệu cho Tableau |
| **G4.1** | Dựng 12 Worksheets trong Tableau Desktop / Tableau Public | Cả nhóm (4/4/4) | Chưa bắt đầu | *[Điền]* | TV1: #1–#4, TV2: #5–#8, TV3: #9–#12 |
| **G4.2** | Thiết kế 4 Dashboard (D1 $\to$ D4) trên Tableau | Thành viên 3 | Chưa bắt đầu | *[Điền]* | Ghép biểu đồ + bộ lọc + KPI |
| **G4.3** | Xây dựng Tableau Story với ít nhất 3 Story Points (chuẩn 4 Points) | Thành viên 3 | Chưa bắt đầu | *[Điền]* | Cốt truyện dẫn dắt + Annotation |
| **G4.4** | Lưu file `wildfire_disaster_analysis.twbx` vào `tableau/` & xuất bản Tableau Public | Thành viên 3 | Chưa bắt đầu | *[Điền]* | Lưu file đóng gói .twbx |
| **G4.5** | Nhúng Tableau Story vào `dashboard/index.html` | Thành viên 3 | Chưa bắt đầu | *[Điền]* | Hiển thị trên GitHub Pages |
| **G5.1** | Cấu hình GitHub Actions CI/CD `.github/workflows/deploy.yml` | Thành viên 3 | **Hoàn thành** | Tuần 1 | Deploy GitHub Pages |
| **G5.2** | Tổng hợp các phát hiện chính (Key Insights) trong từng Story Point | Cả nhóm | Chưa bắt đầu | *[Điền]* | Dữ liệu thật 20 năm |
| **G5.3** | Hoàn thiện `README.md`, `REPORT_OUTLINE.md`, `DEMO_SCRIPT.md` | Thành viên 3 | Chưa bắt đầu | *[Điền]* | Link Tableau Public + .twbx |
| **G5.4** | Kiểm thử tổng thể (Không lỗi Tableau, .twbx mở tốt, pytest pass) | Cả nhóm | Chưa bắt đầu | *[Điền]* | Nghiệm thu đồ án |

---

## 4. Quy Ước Làm Việc & Hợp Tác Kỹ Thuật

1. **Quy tắc phân nhánh (Branching Model)**:
   - Nhánh `main`: Chứa mã nguồn ổn định, đã kiểm thử và sẵn sàng triển khai.
   - Nhánh `member-1-data`: Thành viên 1 thực hiện các tác vụ dữ liệu và biểu đồ #1–#4.
   - Nhánh `member-2-model`: Thành viên 2 thực hiện các tác vụ mô hình hóa, CSDL và biểu đồ #5–#8.
   - Nhánh `member-3-dashboard`: Thành viên 3 thực hiện khung giao diện, CI/CD và biểu đồ #9–#12.
   - Merge vào `main` thông qua **Pull Request (PR)** sau khi chạy kiểm thử thành công.
2. **Quy ước thông điệp Commit (Conventional Commits)**:
   - `feat:` Thêm tính năng mới (vd: `feat: implement isolation forest cleaning in 03b_ml_clean.py`)
   - `fix:` Sửa lỗi (vd: `fix: handle negative values in damage_usd`)
   - `docs:` Thêm hoặc cập nhật tài liệu (vd: `docs: update DATA_DICTIONARY.md with ML flags`)
   - `data:` Thao tác liên quan đến dữ liệu (vd: `data: update interim rules cleaned dataset`)
   - `chore:` Cấu hình công cụ, môi trường (vd: `chore: pin requirements versions`)
3. **Giới hạn kích thước tập tin**:
   - **Tuyệt đối không commit file $> 90$ MB** lên Git (GitHub giới hạn 100 MB).
   - Thư mục `data/raw/` chứa file thô lớn được cấu hình trong `.gitignore`. Khi cần chia sẻ file lớn, sử dụng lấy mẫu đại diện hoặc nén/tổng hợp.
4. **Bảo mật & Biến môi trường**:
   - Không commit khóa API (Kaggle API key, Token EM-DAT). Sử dụng file `.env` (đã nằm trong `.gitignore`) và hướng dẫn khai báo qua `.env.example`.
5. **Tôn trọng phạm vi tập tin (Ownership of Code)**:
   - Mỗi thành viên phụ trách các tập tin riêng của mình. Không tự ý chỉnh sửa tập tin của thành viên khác để tránh xung đột mã nguồn (merge conflict).

---

## 5. Lịch Mốc Triển Khai (Milestones Timeline)

| Mốc thời gian | Tên Mốc | Mục tiêu bàn giao chính | Thời hạn (Deadline) |
|---------------|---------|-------------------------|---------------------|
| **Tuần 1** | Mốc 1: Khởi tạo | Hoàn thành cấu trúc repo, file phân công, cấu hình môi trường chuẩn | *[Nhóm điền]* |
| **Tuần 2** | Mốc 2: Dữ liệu sạch | Hoàn tất thu thập, EDA, làm sạch quy tắc & làm sạch ML $\ge 5.000$ dòng | *[Nhóm điền]* |
| **Tuần 3** | Mốc 3: CSDL & Quan hệ | Hoàn tất tách bảng, nạp `database.sqlite`, kiểm thử ràng buộc, xuất JSON | *[Nhóm điền]* |
| **Tuần 4** | Mốc 4: Trực quan hóa | Hoàn thành khung dashboard, hoàn tất 12 biểu đồ tương tác, bộ lọc | *[Nhóm điền]* |
| **Tuần 5** | Mốc 5: Hoàn thiện | Triển khai GitHub Pages, viết báo cáo hoàn chỉnh, kịch bản thuyết trình demo | *[Nhóm điền]* |

---

## 6. Phân Công Chi Tiết & Nhiệm Vụ 3 Thành Viên

### Thành viên 1 – DỮ LIỆU (Thu thập $\to$ Làm sạch bằng Quy tắc & Học máy)
- [x] Tìm và đánh giá $\ge 3$ nguồn dữ liệu (EM-DAT, NASA FIRMS, USFS/Kaggle, Our World in Data); lập bảng so sánh trong `docs/DATA_SOURCES.md`.
- [x] Tải dữ liệu vào `data/raw/` bằng script tự động `src/01_download.py` (kèm hướng dẫn tải thủ công nếu nguồn yêu cầu đăng nhập).
- [ ] Phân tích khám phá dữ liệu (EDA) qua `src/02_eda.py` và notebook `notebooks/01_initial_eda.ipynb`; xuất báo cáo chất lượng ban đầu `docs/DATA_QUALITY_REPORT.md`.
- [ ] **Làm sạch bước 1 theo quy tắc (`src/03_clean.py`)**: Chuẩn hóa mã ISO3, ngày giờ, đơn vị (ha, USD), loại trùng lặp, xử lý giá trị âm và xuất `data/interim/master_rules_cleaned.csv`.
- [ ] **Làm sạch bước 2 bằng Học máy (`src/03b_ml_clean.py`) với TỐI THIỂU 2 MÔ HÌNH**:
  1. *Isolation Forest & LOF*: Phát hiện bất thường trên biến đổi log1p; chỉ gắn cờ `is_outlier_ml` và tính `outlier_score`, đối soát thủ công top 20 mẫu bất thường, ghi lý do trong `docs/CLEANING_LOG.md`.
  2. *KNN Imputer hoặc Iterative Imputer (MICE)*: Điền giá trị thiếu cho biến số (không điền cột thiếu $> 60\%$), gắn cờ `<col>_is_imputed`. Đánh giá bằng che ngẫu nhiên 10–20% đối chiếu MAE/RMSE so với Median Baseline.
  3. *(Khuyến khích)*: *Random Forest Classifier* dự đoán `cause_group` khi xác suất $\ge 0.7$, gắn cờ `cause_is_predicted`.
- [ ] **Yêu cầu cứng**: `data/clean/master_clean.csv` sau khi xử lý phải có $\ge 5.000$ dòng; script phải có lệnh `assert len(df) >= 5000`.
- [ ] Hoàn thiện `docs/ML_CLEANING_REPORT.md`, `docs/CLEANING_LOG.md` và `docs/DATA_DICTIONARY.md`.
- [ ] Chịu trách nhiệm thực hiện trọn vẹn 4 biểu đồ: **#1, #2, #3, #4**.

### Thành viên 2 – MÔ HÌNH DỮ LIỆU (Tách bảng $\to$ Quan hệ $\to$ Ràng buộc CSDL)
- [ ] Thiết kế Star Schema từ `master_clean.csv`: `dim_date`, `dim_location`, `dim_disaster_type`, `dim_cause`, `dim_source`, `fact_disaster_event`, `fact_wildfire_detail`. Mỗi bảng đạt tối thiểu 3NF, có surrogate key. Bảo toàn các cột cờ ML trong bảng fact (`is_outlier_ml`, `*_is_imputed`, `cause_is_predicted`).
- [ ] Viết `src/04_split_tables.py` tách bảng thành các file CSV lưu tại `data/tables/`.
- [ ] Viết DDL `sql/schema.sql` với đầy đủ: PRIMARY KEY, FOREIGN KEY (`ON DELETE RESTRICT ON UPDATE CASCADE`), NOT NULL, UNIQUE, CHECK constraints (`deaths >= 0`, `damage_usd >= 0`, `burned_area_ha >= 0`, `year BETWEEN 2005 AND 2024`, `latitude BETWEEN -90 AND 90`, `longitude BETWEEN -180 AND 180`), DEFAULT hợp lý, và INDEX tối ưu truy vấn JOIN/WHERE.
- [ ] Viết script `src/05_build_db.py` tạo `database.sqlite`, kích hoạt `PRAGMA foreign_keys = ON;`, nạp dữ liệu và kiểm tra vi phạm ràng buộc.
- [ ] Vẽ sơ đồ thực thể liên kết `docs/ERD.md` bằng Mermaid `erDiagram` với đầy đủ bản số quan hệ (Cardinality 1–N).
- [ ] Viết `src/07_validate.py` và bộ kiểm thử `tests/`: kiểm tra toàn vẹn tham chiếu (không có FK mồ côi), không trùng khóa chính, fact $\ge 5.000$ dòng, toàn bộ ràng buộc CHECK đạt chuẩn, cột cờ nhận 0/1.
- [ ] Viết script `src/06_export_json.py` (xuất JSON vào `dashboard/data/`) và các truy vấn SQL cho biểu đồ của mình trong `sql/queries_for_charts.sql`.
- [ ] Chịu trách nhiệm thực hiện trọn vẹn 4 biểu đồ: **#5, #6, #7, #8**.

### Thành viên 3 – DASHBOARD & TRIỂN KHAI (Tableau Public $\to$ Storytelling $\to$ DevOps)
- [ ] Thiết lập môi trường Tableau Desktop / Tableau Public, kết nối nguồn dữ liệu sạch từ `data/clean/master_clean.csv`.
- [ ] Phụ trách thực hiện 4 biểu đồ chuyên sâu của mình: **#9 (Pareto Top 10), #10 (Donut Nguyên nhân), #11 (Sankey/Flow Luồng), #12 (Symbol Map Đại vụ cháy)** dưới dạng các Tableau Worksheets.
- [ ] Thiết kế **4 Dashboards** hoàn chỉnh (D1: Bức tranh 20 năm, D2: Ở đâu chịu thiệt hại, D3: Cháy rừng: Khi nào & lớn cỡ nào, D4: Vì sao & hệ quả) với bố cục khoa học, thẻ KPI Cards và bộ lọc chung.
- [ ] Xây dựng **Tableau Story với ít nhất 3 Story Points** (chuẩn 4 Story Points dẫn dắt câu chuyện phân tích, có chú thích Annotation làm nổi bật phát hiện từ dữ liệu thật).
- [ ] Đóng gói và lưu tệp Workbook `tableau/wildfire_disaster_analysis.twbx`, xuất bản lên Tableau Public và lấy đường link nhúng vào `dashboard/index.html`.
- [ ] Triển khai pipeline CI/CD `.github/workflows/deploy.yml` tự động xuất bản trang web chứa bản nhúng Tableau lên GitHub Pages.
- [ ] Soạn thảo và hoàn thiện `README.md`, `docs/REPORT_OUTLINE.md`, `docs/DEMO_SCRIPT.md`.

---

## 7. Cấu Trúc 4 Dashboard, Tableau Story & Phân Chia 12 Biểu Đồ

### CẤU TRÚC 4 DASHBOARD (mỗi dashboard 3 biểu đồ, 1 câu hỏi chính)
Bốn dashboard nối nhau như một câu chuyện: **bức tranh chung → ở đâu → cháy rừng cụ thể → vì sao và hệ quả**.

| Dashboard | Câu hỏi chính | Biểu đồ trong dashboard |
|-----------|---------------|-------------------------|
| **D1 – Bức tranh 20 năm** (tổng quát) | Thảm họa thiên nhiên có xảy ra nhiều hơn và thiệt hại lớn hơn qua các năm không? | #1 Combo số vụ + thiệt hại; #2 Stacked area theo loại thảm họa; #5 Diverging bar chênh lệch so với trung bình |
| **D2 – Ở đâu chịu thiệt hại?** (không gian) | Quốc gia và khu vực nào chịu ảnh hưởng nặng nhất? | #3 Choropleth; #6 Treemap châu lục → quốc gia; #9 Combo Pareto top 10 quốc gia |
| **D3 – Cháy rừng: khi nào và lớn cỡ nào?** (chi tiết cháy rừng) | Cháy rừng tập trung vào mùa nào, quy mô ra sao, vụ lớn nằm ở đâu? | #4 Heatmap tháng × năm; #8 Combo histogram + mật độ; #12 Bản đồ điểm vụ cháy lớn |
| **D4 – Vì sao và hệ quả** (nguyên nhân & mức độ) | Nguyên nhân chính là gì và quy mô liên hệ thế nào với thiệt hại? | #10 Sunburst/donut nguyên nhân; #11 Sankey nguyên nhân → loại → mức thiệt hại; #7 Bubble scatter |

Bố cục mỗi dashboard: dải tiêu đề (tên + câu hỏi chính) → 2–3 KPI card → 3 biểu đồ (1 biểu đồ lớn + 2 biểu đồ nhỏ, hoặc 3 cột) → hộp "Insight" 1–2 câu → chuyển sang dashboard kế tiếp.

### KỂ CHUYỆN BẰNG TABLEAU STORY (Ít nhất 3 Story Points)
- **Tableau Story** kết nối 4 Dashboard thành một chuỗi trình bày phân tích với **4 Story Points**:
  1. **Point 1**: *Bức tranh 20 năm: Tần suất & Thiệt hại* (Nhúng D1, chú thích đỉnh điểm năm 2020).
  2. **Point 2**: *Điểm nóng toàn cầu: Châu lục & Quốc gia tổn thất nặng* (Nhúng D2, chú thích nguyên lý 80/20).
  3. **Point 3**: *Trọng tâm Cháy rừng: Mùa cao điểm & Siêu đám cháy* (Nhúng D3, chú thích mùa khô tháng 6–9 và các đám cháy $\ge 10.000$ ha).
  4. **Point 4**: *Căn nguyên & Tác động: Tự nhiên vs Con người* (Nhúng D4, đúc kết khuyến nghị hành động).
- Mọi con số trong Insight và Annotation phải được **TÍNH TỪ DỮ LIỆU THẬT**, không viết số liệu cảm tính.

### PHÂN CHIA 12 BIỂU ĐỒ (chia đều 4/4/4; MỖI BIỂU ĐỒ CHỈ DO 1 NGƯỜI THỰC HIỆN; mỗi người có 1 biểu đồ kết hợp)
| # | Tên Sheet Tableau | Dashboard | Kiểu dữ liệu | Bảng màu | Người phụ trách |
|---|-------------------|-----------|--------------|----------|-----------------|
| 1 | `Sheet_01_Combo_Trend` (Combo cột số vụ + đường thiệt hại USD theo năm) | D1 | thời gian + 2 số | categorical (2 màu) | **TV1** |
| 2 | `Sheet_02_Stacked_Area` (Stacked area tần suất theo loại thảm họa) | D1 | thời gian × phân loại | categorical | **TV1** |
| 3 | `Sheet_03_Choropleth_Map` (Choropleth thế giới: thiệt hại/số vụ theo nước) | D2 | không gian + số | sequential | **TV1** |
| 4 | `Sheet_04_Heatmap_Season` (Heatmap tháng × năm số vụ cháy rừng) | D3 | chu kỳ × năm × số | sequential | **TV1** |
| 5 | `Sheet_05_Diverging_Bar` (Diverging bar chênh lệch số vụ so với trung bình 20 năm) | D1 | độ lệch × thời gian | diverging (tâm = 0) | **TV2** |
| 6 | `Sheet_06_Treemap_Damage` (Treemap châu lục → quốc gia theo thiệt hại) | D2 | phân cấp × số | categorical cấp 1 | **TV2** |
| 7 | `Sheet_07_Bubble_Scatter` (Bubble scatter diện tích cháy vs thiệt hại USD vs người ảnh hưởng) | D4 | 3 số liên tục (log-log) | categorical theo châu lục | **TV2** |
| 8 | `Sheet_08_Combo_Histogram` (Combo histogram diện tích cháy + đường phân vị lũy kế) | D3 | phân phối 1 số | sequential | **TV2** |
| 9 | `Sheet_09_Combo_Pareto` (Combo Pareto cột số người chết top 10 quốc gia + đường % lũy kế) | D2 | xếp hạng × lũy kế | sequential + nhấn | **TV3** |
| 10 | `Sheet_10_Donut_Cause` (Donut 2 tầng nguyên nhân tự nhiên / nhân tạo) | D4 | phân cấp | categorical | **TV3** |
| 11 | `Sheet_11_Sankey_Flow` (Luồng chuyển giao nguyên nhân → loại thảm họa → mức thiệt hại) | D4 | luồng đa chiều | categorical | **TV3** |
| 12 | `Sheet_12_Proportional_Map` (Bản đồ điểm các vụ cháy lớn: cỡ = diện tích, màu = thiệt hại) | D3 | tọa độ + 2 số | sequential | **TV3** |

### QUY TRÌNH 4 BƯỚC CHO MỖI THÀNH VIÊN KHI LÀM BIỂU ĐỒ TRÊN TABLEAU
1. **Mở Tableau và tạo Worksheet**: Kéo thả Dimensions và Measures theo đúng đặc tả tại [docs/CHART_SPEC.md](file:///c:/Users/ASUS/Documents/Tương tác dữ liệu/đồ án ck/IDV_TTDL/docs/CHART_SPEC.md).
2. **Tạo Calculated Fields cần thiết**: Sử dụng công thức chuẩn trong [tableau/CALCULATED_FIELDS.md](file:///c:/Users/ASUS/Documents/Tương tác dữ liệu/đồ án ck/IDV_TTDL/tableau/CALCULATED_FIELDS.md).
3. **Định dạng hiển thị chuẩn**: Tooltip tiếng Việt rõ ràng, có đơn vị tiền tệ (Tỷ USD, ha, người), màu sắc đúng quy chuẩn.
4. **Ghi vào `CHART_SPEC.md`**: Ghi lại 1 phát hiện quan trọng (Insight) rút ra từ dữ liệu thật để đưa vào Story Point.

---

## 8. Định Nghĩa Hoàn Thành (Definition of Done - DoD)

### DoD Giai đoạn 1 (Khởi tạo dự án & Môi trường):
- Cấu trúc thư mục được khởi tạo đầy đủ kèm `.gitkeep`.
- Các file khung `.py`, `.sql`, `.md` có tiêu đề, docstring, mục đích và người phụ trách rõ ràng.
- `PROJECT_GUIDE.md` và 3 file `team/*/TASKS.md` được biên soạn chi tiết, không vi phạm nguyên tắc phân công.
- Đẩy thành công lên Git nhánh `main` và 3 nhánh thành viên `member-1-data`, `member-2-model`, `member-3-dashboard`.

### DoD Giai đoạn 2 (Dữ liệu):
- Dữ liệu thô lưu tại `data/raw/` có nguồn gốc rõ ràng, ghi trong `DATA_SOURCES.md`.
- `master_clean.csv` đạt $\ge 5.000$ dòng và có lệnh `assert` kiểm tra.
- Quy trình ML áp dụng $\ge 2$ mô hình (Isolation Forest, KNN/Iterative Imputer); có báo cáo thực nghiệm trong `ML_CLEANING_REPORT.md`.
- Toàn bộ cột cờ và dữ liệu được ghi nhận đầy đủ trong `DATA_DICTIONARY.md` và `CLEANING_LOG.md`.

### DoD Giai đoạn 3 (Mô hình Dữ liệu):
- CSDL `database.sqlite` được tạo bằng `05_build_db.py` với `PRAGMA foreign_keys = ON;`.
- Bảng fact đạt $\ge 5.000$ dòng, không có khóa ngoại mồ côi, toàn bộ ràng buộc CHECK đạt chuẩn.
- Script `07_validate.py` và bộ test `pytest` thực thi kiểm thử tự động đạt 100% pass.

### DoD Giai đoạn 4 (Tableau Dashboard & Storytelling):
- Hoàn thành đầy đủ 12 Worksheets trong Tableau (chia đều 4/4/4 cho 3 thành viên).
- Hoàn thành 4 Dashboards (D1 $\to$ D4) với KPI Cards, bộ lọc năm/loại thảm họa và hộp Insight.
- Hoàn thành 1 Tableau Story với ít nhất 3 Story Points (chuẩn 4 Story Points) có chú thích nổi bật.
- File workbook đóng gói `tableau/wildfire_disaster_analysis.twbx` được lưu trữ trong repo và mở lên hoạt động trơn tru.

### DoD Giai đoạn 5 (Xuất bản & Nghiệm thu):
- Xuất bản thành công lên Tableau Public và nhúng liên kết vào `dashboard/index.html` (chạy trên GitHub Pages).
- `README.md` có đầy đủ ảnh chụp, link demo Tableau Public và hướng dẫn mở file `.twbx`.
- Hoàn thành đầy đủ báo cáo tổng kết và kịch bản thuyết trình demo.
