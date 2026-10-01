# HƯỚNG DẪN DỰ ÁN & PHÂN CÔNG NHIỆM VỤ (PROJECT GUIDE)

> **Môn học**: Tương tác dữ liệu trực quan (Interactive Data Visualization)  
> **Đề tài**: Nghiên cứu – phân tích tần suất và thiệt hại của các trận cháy rừng / thảm họa thiên nhiên trong 20 năm qua (2006–2025)  
> **Kho lưu trữ (Repository)**: `https://github.com/tpdk0105/IDV_TTDL`  

---

## 1. Giới Thiệu Đề Tài & Mục Tiêu

### 1.1. Bối cảnh & Tính cấp thiết
Trong giai đoạn 20 năm qua (2006–2025), biến đổi khí hậu toàn cầu diễn biến phức tạp với sự gia tăng mạnh mẽ cả về tần suất, cường độ và mức độ tàn phá của các thảm họa thiên nhiên. Trong đó, **cháy rừng (Wildfires)** nổi lên như một trong những thách thức nghiêm trọng nhất đối với môi trường sinh thái, an ninh con người và nền kinh tế toàn cầu (các đợt siêu cháy rừng tại Úc 2019–2020, California, Hy Lạp, Canada 2023, Maui 2023).

### 1.2. Mục tiêu nghiên cứu
- Thu thập, làm sạch và tích hợp dữ liệu thảm họa thiên nhiên toàn cầu giai đoạn 2006–2025 từ các nguồn dữ liệu khoa học uy tín (EM-DAT, NASA FIRMS, USFS/NOAA, Our World in Data).
- Áp dụng các kỹ thuật Kỹ thuật Dữ liệu (Data Engineering) hiện đại kết hợp Học máy (Machine Learning) để chuẩn hóa, phát hiện ngoại lai bất thường (Isolation Forest/LOF) và xử lý giá trị khuyết thiếu (KNN/Iterative Imputer).
- Thiết kế mô hình dữ liệu chuẩn hình sao (Star Schema) tối ưu hóa trên SQLite với hệ thống ràng buộc toàn vẹn nghiêm ngặt (PK, FK, CHECK, UNIQUE, NOT NULL).
- Xây dựng hệ thống bảng điều khiển trực quan hóa tương tác (Interactive Dashboard) bằng Apache ECharts với 12 biểu đồ trực quan chuyên sâu, phục vụ đa chiều các câu hỏi phân tích, hỗ trợ Cross-filtering và tuân thủ các chuẩn mực thiết kế trực quan (WCAG AA, bảng màu thân thiện người mù màu).

---

## 2. Bảng Danh Sách Thành Viên & Vai Trò

| Thành viên | Họ và tên | MSSV / Email liên hệ | Vai trò chính | Nhánh Git riêng |
|------------|-----------|----------------------|---------------|-----------------|
| **Thành viên 1** | [TÊN THÀNH VIÊN 1] | *[Điền MSSV/Email]* | Kỹ sư Dữ liệu (Data Engineer): Thu thập, EDA, Làm sạch dữ liệu (Quy tắc + Học máy) | `member-1-data` |
| **Thành viên 2** | [TÊN THÀNH VIÊN 2] | *[Điền MSSV/Email]* | Kỹ sư Mô hình Dữ liệu (Data Modeling Engineer): Star Schema, Ràng buộc CSDL, SQL & Xuất dữ liệu | `member-2-model` |
| **Thành viên 3** | [TÊN THÀNH VIÊN 3] | *[Điền MSSV/Email]* | Kỹ sư Trực quan hóa & Triển khai (Data Visualization & DevOps): Dashboard ECharts, CI/CD, Báo cáo | `member-3-dashboard` |

---

## 3. Bảng Tổng Hợp Tiến Độ Toàn Nhóm

> **Nguyên tắc phân công**: Mỗi đầu việc chỉ do **ĐÚNG MỘT** thành viên chịu trách nhiệm độc lập. Không ghi cột "người review" hay "người cùng làm". Nhóm tự cập nhật cột Trạng thái và Deadline.

| Mã | Giai đoạn & Hạng mục công việc | Người phụ trách | Trạng thái | Deadline | Ghi chú |
|----|--------------------------------|-----------------|------------|----------|---------|
| **G1** | Khởi tạo repo, cấu trúc thư mục, môi trường, tài liệu phân công | Cả nhóm | **Hoàn thành** | Tuần 1 | Giai đoạn 1 |
| **G2.1** | Tìm, đánh giá $\ge 3$ nguồn dữ liệu, viết `DATA_SOURCES.md` | Thành viên 1 | Chưa bắt đầu | *[Điền]* | EM-DAT, NASA, USFS... |
| **G2.2** | Viết script tải dữ liệu thô `01_download.py` | Thành viên 1 | Chưa bắt đầu | *[Điền]* | Lưu vào `data/raw/` |
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
| **G3.6** | Viết truy vấn SQL cho biểu đồ #5–#8 trong `sql/queries_for_charts.sql` | Thành viên 2 | Chưa bắt đầu | *[Điền]* | Kèm xuất JSON `06_export_json.py` |
| **G4.1** | Xây dựng khung Dashboard HTML/CSS responsive, hỗ trợ Light/Dark | Thành viên 3 | Chưa bắt đầu | *[Điền]* | Apache ECharts local vendor |
| **G4.2** | Tích hợp GeoJSON thế giới và bản đồ cục bộ | Thành viên 3 | Chưa bắt đầu | *[Điền]* | Đặt sẵn trong repo |
| **G4.3** | Xây dựng bộ lọc toàn cục, hàng thẻ KPI, công tắc lọc dữ liệu gốc | Thành viên 3 | Chưa bắt đầu | *[Điền]* | Cross-filtering |
| **G4.4** | Triển khai mô-đun bảng màu dùng chung `dashboard/js/palette.js` | Thành viên 3 | Chưa bắt đầu | *[Điền]* | Chuẩn Okabe-Ito, OrRd, RdBu |
| **G4.5** | Thực hiện 4 biểu đồ của TV1 (#1, #2, #3, #4) | Thành viên 1 | Chưa bắt đầu | *[Điền]* | Viết SQL, JS, spec |
| **G4.6** | Thực hiện 4 biểu đồ của TV2 (#5, #6, #7, #8) | Thành viên 2 | Chưa bắt đầu | *[Điền]* | Viết SQL, JS, spec |
| **G4.7** | Thực hiện 4 biểu đồ của TV3 (#9, #10, #11, #12) | Thành viên 3 | Chưa bắt đầu | *[Điền]* | Viết SQL, JS, spec |
| **G5.1** | Cấu hình GitHub Actions CI/CD `.github/workflows/deploy.yml` | Thành viên 3 | Chưa bắt đầu | *[Điền]* | Tự động deploy GitHub Pages |
| **G5.2** | Tổng hợp 5–7 phát hiện chính (Key Insights) trên Dashboard | Thành viên 3 | Chưa bắt đầu | *[Điền]* | Dữ liệu thật 20 năm |
| **G5.3** | Hoàn thiện `README.md`, `REPORT_OUTLINE.md`, `DEMO_SCRIPT.md` | Thành viên 3 | Chưa bắt đầu | *[Điền]* | Kèm ảnh minh họa & link |
| **G5.4** | Kiểm thử tổng thể (Không lỗi console, JSON tải < 3s, pytest pass) | Cả nhóm | Chưa bắt đầu | *[Điền]* | Nghiệm thu đồ án |

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
- [ ] Viết DDL `sql/schema.sql` với đầy đủ: PRIMARY KEY, FOREIGN KEY (`ON DELETE RESTRICT ON UPDATE CASCADE`), NOT NULL, UNIQUE, CHECK constraints (`deaths >= 0`, `damage_usd >= 0`, `burned_area_ha >= 0`, `year BETWEEN 2006 AND 2025`, `latitude BETWEEN -90 AND 90`, `longitude BETWEEN -180 AND 180`), DEFAULT hợp lý, và INDEX tối ưu truy vấn JOIN/WHERE.
- [ ] Viết script `src/05_build_db.py` tạo `database.sqlite`, kích hoạt `PRAGMA foreign_keys = ON;`, nạp dữ liệu và kiểm tra vi phạm ràng buộc.
- [ ] Vẽ sơ đồ thực thể liên kết `docs/ERD.md` bằng Mermaid `erDiagram` với đầy đủ bản số quan hệ (Cardinality 1–N).
- [ ] Viết `src/07_validate.py` và bộ kiểm thử `tests/`: kiểm tra toàn vẹn tham chiếu (không có FK mồ côi), không trùng khóa chính, fact $\ge 5.000$ dòng, toàn bộ ràng buộc CHECK đạt chuẩn, cột cờ nhận 0/1.
- [ ] Viết script `src/06_export_json.py` (xuất JSON vào `dashboard/data/`) và các truy vấn SQL cho biểu đồ của mình trong `sql/queries_for_charts.sql`.
- [ ] Chịu trách nhiệm thực hiện trọn vẹn 4 biểu đồ: **#5, #6, #7, #8**.

### Thành viên 3 – DASHBOARD & TRIỂN KHAI (Giao diện $\to$ Tương tác $\to$ DevOps)
- [ ] Xây dựng khung Dashboard web tĩnh: HTML5 / CSS3 / Vanilla JS + **Apache ECharts** (bản cục bộ ghim phiên bản trong `dashboard/js/vendor/`, không phụ thuộc CDN); tích hợp GeoJSON bản đồ thế giới trong repo; hỗ trợ responsive và chuyển đổi Light / Dark theme.
- [ ] Phát triển bộ lọc toàn cục tương tác: thanh trượt dải năm, chọn loại thảm họa, châu lục/quốc gia, nhóm nguyên nhân; cơ chế Cross-filtering; tooltip tiếng Việt chi tiết; drill-down; brush; nút reset; hàng thẻ KPI card đồng bộ dữ liệu. Bổ sung công tắc *"Chỉ hiển thị số liệu gốc (Ẩn giá trị ước lượng/điền thiếu)"*. Cung cấp kiến trúc mở để các biểu đồ cắm vào độc lập qua `dashboard/js/charts/chart-XX.js`.
- [ ] Triển khai `docs/COLOR_GUIDE.md` và mô-đun dùng chung `dashboard/js/palette.js`.
- [ ] Xây dựng pipeline CI/CD `.github/workflows/deploy.yml` tự động đóng gói và xuất bản thư mục `dashboard/` lên GitHub Pages khi có commit trên `main`.
- [ ] Soạn thảo và hoàn thiện `README.md`, `docs/REPORT_OUTLINE.md`, `docs/DEMO_SCRIPT.md`.
- [ ] Chịu trách nhiệm thực hiện trọn vẹn 4 biểu đồ: **#9, #10, #11, #12**.

---

## 7. Cấu Trúc Dashboard & Phân Chia 12 Biểu Đồ

### CẤU TRÚC 4 DASHBOARD (mỗi dashboard 3 biểu đồ, 1 câu hỏi chính)
Bốn dashboard nối nhau như một câu chuyện: **bức tranh chung → ở đâu → cháy rừng cụ thể → vì sao và hệ quả**.

| Dashboard | Câu hỏi chính | Biểu đồ trong dashboard |
|-----------|---------------|-------------------------|
| **D1 – Bức tranh 20 năm** (tổng quát) | Thảm họa thiên nhiên có xảy ra nhiều hơn và thiệt hại lớn hơn qua các năm không? | #1 Combo số vụ + thiệt hại; #2 Stacked area theo loại thảm họa; #5 Diverging bar chênh lệch so với trung bình |
| **D2 – Ở đâu chịu thiệt hại?** (không gian) | Quốc gia và khu vực nào chịu ảnh hưởng nặng nhất? | #3 Choropleth; #6 Treemap châu lục → quốc gia; #9 Combo Pareto top 10 quốc gia |
| **D3 – Cháy rừng: khi nào và lớn cỡ nào?** (chi tiết cháy rừng) | Cháy rừng tập trung vào mùa nào, quy mô ra sao, vụ lớn nằm ở đâu? | #4 Heatmap tháng × năm; #8 Combo histogram + mật độ; #12 Bản đồ điểm vụ cháy lớn |
| **D4 – Vì sao và hệ quả** (nguyên nhân & mức độ) | Nguyên nhân chính là gì và quy mô liên hệ thế nào với thiệt hại? | #10 Sunburst/donut nguyên nhân; #11 Sankey nguyên nhân → loại → mức thiệt hại; #7 Bubble scatter |

Bố cục mỗi dashboard: dải tiêu đề (tên + câu hỏi chính) → 2–3 KPI card → 3 biểu đồ (1 biểu đồ lớn + 2 biểu đồ nhỏ, hoặc 3 cột) → hộp "Insight" 1–2 câu → chuyển sang dashboard kế tiếp.

### KỂ CHUYỆN BẰNG DỮ LIỆU (giữ đơn giản)
- Mỗi dashboard có: (1) tiêu đề dạng câu hỏi, (2) hộp "Insight" 1–2 câu nêu phát hiện chính, (3) câu dẫn sang dashboard kế tiếp. Dashboard cuối có thêm đoạn "Kết luận & hạn chế dữ liệu" ngắn.
- Mọi con số trong Insight phải được TÍNH TỪ DỮ LIỆU THẬT (tính bằng JS từ `events.json` hoặc kiểm chứng bằng SQL), không viết tay số liệu theo cảm tính, và phải đổi theo bộ lọc nếu có thể.
- Tối đa 1 chú thích/annotation nổi bật trên mỗi dashboard (ví dụ đánh dấu năm cao nhất). Không làm hoạt ảnh, không làm chế độ trình chiếu.

### PHÂN CHIA 12 BIỂU ĐỒ (chia đều 4/4/4; MỖI BIỂU ĐỒ CHỈ DO 1 NGƯỜI THỰC HIỆN; mỗi người có 1 biểu đồ kết hợp)
| # | Biểu đồ | Dashboard | Kiểu dữ liệu | Bảng màu | Người phụ trách |
|---|---------|-----------|--------------|----------|-----------------|
| 1 | **Combo** cột số vụ + đường thiệt hại USD theo năm (trục kép) | D1 | thời gian + 2 số | categorical (2 màu) | TV1 |
| 2 | Stacked area tần suất theo loại thảm họa theo năm | D1 | thời gian × phân loại | categorical | TV1 |
| 3 | Choropleth thế giới: thiệt hại/số vụ theo quốc gia | D2 | không gian + số | sequential | TV1 |
| 4 | Heatmap tháng × năm số vụ cháy rừng | D3 | chu kỳ × năm × số | sequential | TV1 |
| 5 | Diverging bar chênh lệch số vụ so với trung bình 20 năm | D1 | độ lệch × thời gian | diverging (tâm = 0) | TV2 |
| 6 | Treemap châu lục → quốc gia theo thiệt hại | D2 | phân cấp × số | categorical cấp 1 | TV2 |
| 7 | Bubble scatter diện tích cháy vs thiệt hại USD vs người ảnh hưởng | D4 | 3 số liên tục (log-log) | categorical theo châu lục | TV2 |
| 8 | **Combo** histogram diện tích cháy + đường phân vị lũy kế | D3 | phân phối 1 số | sequential | TV2 |
| 9 | **Combo Pareto** cột số người chết top 10 quốc gia + đường % lũy kế | D2 | xếp hạng × lũy kế | sequential + nhấn | TV3 |
| 10 | Sunburst/donut 2 tầng nguyên nhân tự nhiên / nhân tạo | D4 | phân cấp | categorical | TV3 |
| 11 | Sankey nguyên nhân → loại thảm họa → mức thiệt hại | D4 | luồng đa chiều | categorical | TV3 |
| 12 | Bản đồ điểm các vụ cháy lớn (kích thước = diện tích, màu = thiệt hại) | D3 | tọa độ + 2 số | sequential | TV3 |

### TƯƠNG TÁC (giữ đơn giản, không làm quá)
- Mọi biểu đồ: tooltip tiếng Việt rõ ràng, có đơn vị; bấm legend để ẩn/hiện chuỗi.
- Bộ lọc chung trên thanh điều khiển: khoảng năm (slider hoặc 2 ô chọn), loại thảm họa (dropdown). Khi đổi bộ lọc, cả 3 biểu đồ trong dashboard hiện tại tự vẽ lại.
- KHÔNG CẦN cross-filtering phức tạp giữa các biểu đồ, KHÔNG CẦN brush-and-link nếu chưa thạo, KHÔNG CẦN chế độ tối (dark mode), KHÔNG CẦN xuất PDF. Tập trung làm 12 biểu đồ đúng, đẹp, chạy mượt.

### QUY TRÌNH 4 BƯỚC CHO MỖI THÀNH VIÊN KHI LÀM BIỂU ĐỒ
1. **Viết query SQL** trích đúng dữ liệu cần cho biểu đồ của mình, lưu vào `sql/queries_for_charts.sql`.
2. **Tạo file JS** `dashboard/js/charts/chart-XX.js` export một hàm `renderChartXX(containerId, data, filters)` dùng ECharts.
3. **Thêm tương tác tối thiểu**: tooltip có định dạng tiền tệ/đơn vị + click legend.
4. **Ghi vào `CHART_SPEC.md`**: câu hỏi phân tích, kiểu dữ liệu, vì sao chọn biểu đồ này, vì sao chọn bảng màu này, 1 câu insight rút ra từ dữ liệu thật.

---

## 8. Định Nghĩa Hoàn Thành (Definition of Done - DoD)

### DoD Giai đoạn 1 (Khởi tạo dự án & Môi trường):
- Cấu trúc thư mục được khởi tạo đầy đủ kèm `.gitkeep`.
- Các file khung `.py`, `.sql`, `.md`, `.html` có tiêu đề, docstring, mục đích và người phụ trách rõ ràng.
- `PROJECT_GUIDE.md` và 3 file `team/*/TASKS.md` được biên soạn chi tiết, không vi phạm nguyên tắc phân công.
- Các file môi trường (`requirements.txt`, `environment.yml`, `package.json`, `.editorconfig`) được ghim phiên bản ổn định và kiểm tra cài đặt thành công.
- Đẩy thành công lên Git nhánh `main` và 3 nhánh thành viên `member-1-data`, `member-2-model`, `member-3-dashboard`.

### DoD Giai đoạn 2 (Dữ liệu):
- Dữ liệu thô lưu tại `data/raw/` có nguồn gốc rõ ràng, ghi trong `DATA_SOURCES.md`.
- `master_clean.csv` đạt $\ge 5.000$ dòng và có lệnh `assert` kiểm tra.
- Quy trình ML áp dụng $\ge 2$ mô hình (Isolation Forest, KNN/Iterative Imputer); có báo cáo thực nghiệm so sánh với Baseline trong `ML_CLEANING_REPORT.md`.
- Toàn bộ cột cờ và dữ liệu được ghi nhận đầy đủ trong `DATA_DICTIONARY.md` và `CLEANING_LOG.md`.

### DoD Giai đoạn 3 (Mô hình Dữ liệu):
- CSDL `database.sqlite` được tạo bằng `05_build_db.py` với `PRAGMA foreign_keys = ON;`.
- Bảng fact đạt $\ge 5.000$ dòng, không có khóa ngoại mồ côi, toàn bộ ràng buộc CHECK đạt chuẩn.
- Script `07_validate.py` và bộ test `pytest` thực thi kiểm thử tự động đạt 100% pass.
- Các truy vấn SQL trong `queries_for_charts.sql` được tối ưu và `06_export_json.py` xuất đầy đủ dữ liệu cho 12 biểu đồ.

### DoD Giai đoạn 4 (Dashboard & Trực quan hóa):
- 12 biểu đồ hoạt động ổn định, không phát sinh lỗi console trên trình duyệt.
- Đầy đủ 3 biểu đồ kết hợp (Combo charts); toàn bộ các biểu đồ đều hỗ trợ tương tác và Cross-filtering.
- Bảng màu tuân thủ nghiêm ngặt `COLOR_GUIDE.md` và chuẩn WCAG AA.
- Cung cấp công tắc chuyển đổi giữa dữ liệu gốc và dữ liệu sau ML.
- Tốc độ nạp dữ liệu và vẽ trang hiển thị dưới 3 giây.

### DoD Giai đoạn 5 (Triển khai & Hoàn thiện):
- Dashboard được tự động triển khai thành công qua GitHub Pages bằng GitHub Actions.
- `README.md` có đầy đủ ảnh chụp, link demo và hướng dẫn chạy pipeline một lệnh (`scripts/run_all.ps1` / `scripts/run_all.sh`).
- Hoàn thành đầy đủ báo cáo tổng kết và kịch bản thuyết trình demo.
