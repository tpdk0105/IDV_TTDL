# IDV_TTDL: Nghiên Cứu – Phân Tích Tần Suất và Thiệt Hại Cháy Rừng Bang California / Bắc Mỹ (2006–2025)

[![Deploy Dashboard to GitHub Pages](https://github.com/tpdk0105/IDV_TTDL/actions/workflows/deploy.yml/badge.svg)](https://github.com/tpdk0105/IDV_TTDL/actions/workflows/deploy.yml)
[![Tableau Public](https://img.shields.io/badge/Tableau%20Public-Interactive%20Story-E97627.svg?logo=tableau)](https://public.tableau.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)

> **Môn học**: Tương tác Dữ liệu Trực quan (Interactive Data Visualization)  
> **Đề tài**: Nghiên cứu – phân tích tần suất và mức độ tàn phá của các trận cháy rừng tại California / Bắc Mỹ trong 20 năm qua (2006–2025)  
> **Đồ án cuối kỳ**: Nhóm 3 sinh viên  
> **Kho lưu trữ chính thức**: [https://github.com/tpdk0105/IDV_TTDL](https://github.com/tpdk0105/IDV_TTDL)  
> **Trang trải nghiệm trực tiếp (Web / GitHub Pages)**: [https://tpdk0105.github.io/IDV_TTDL/](https://tpdk0105.github.io/IDV_TTDL/)  
> **Tableau Storyboard trực tuyến**: [Tableau Public Story URL](https://public.tableau.com/) *(Sẽ đính kèm link sau khi xuất bản)*  
> **File đóng gói Tableau Workbook**: [tableau/wildfire_disaster_analysis.twbx](tableau/wildfire_disaster_analysis.twbx)

---

## 1. Giới Thiệu Đề Tài & Trọng Tâm Nghiên Cứu
Dự án tập trung nghiên cứu, làm sạch, mô hình hóa và trực quan hóa tương tác đa chiều về **tần suất và thiệt hại của các trận cháy rừng tại Bang California trong 20 năm qua (2006–2025)**. Dữ liệu được tích hợp từ 5 nguồn chính thống uy tín của chính quyền bang và liên bang Hoa Kỳ:
1. **CAL FIRE FRAP**: 23.334 dòng lịch sử, **7.342 vụ cháy trong 2006–2025** với diện tích (Acres), nguyên nhân (Cause), thời gian, tọa độ chu vi.
2. **CAL FIRE DINS (2013–2025)**: 132.522 dòng công trình kiểm kê thiệt hại tài sản (70.390 công trình bị phá hủy hoàn toàn >50%). Khóa liên kết `Incident Name` và `Year` khớp trên 93% với `Fire Name` của FRAP.
3. **USDA Forest Service & NIFC (ICS-209-PLUS 2006–2012)**: 1.127 vụ cháy lớn với 7.206 công trình bị phá hủy hoàn toàn, lấp đầy hoàn hảo khoảng trống 7 năm đầu để chỉ số thiệt hại nhà cửa đạt **đủ 20/20 năm liên tục (2006–2025)**.
4. **NOAA NCEI Storm Events (2006–2025)**: 993 dòng sự kiện cháy rừng cấp bang phủ kín **đủ 20/20 năm**, chỉ dùng cho thiệt hại về người: **207 người chết trực tiếp, 792 người bị thương** sau khi gộp các dòng trùng giữa vùng dự báo (dữ liệu thô ghi 255 / 887). Thiệt hại tài sản lấy từ DINS + ICS-209.
5. **California Counties Demographics**: 58 Hạt của California kèm diện tích dặm vuông và dân số điều tra Census, phục vụ phân tích theo không gian và chuẩn hóa tỷ lệ thiệt hại trên đầu người.

### Điểm nổi bật về kỹ thuật:
- **Kỹ thuật dữ liệu vững chắc (Python Pipeline)**: Tự động tải từ các nguồn dữ liệu uy tín $\to$ làm sạch quy tắc $\to$ làm sạch thông minh bằng **Học máy (Isolation Forest, LOF, MICE/KNN)** *(chưa triển khai)* $\to$ cam kết tập dữ liệu sạch đạt $\ge 5.000$ dòng.
- **Mô hình hóa chuẩn hình sao (Star Schema $\ge 3$ bảng)**: Tách dữ liệu đạt chuẩn tối thiểu 3NF (`dim_county`, `dim_cause`, `dim_date`, `fact_fire_incident`, `fact_structure_damage`), nạp vào SQLite với toàn bộ hệ thống ràng buộc toàn vẹn tham chiếu (PK, FK, CHECK, UNIQUE, NOT NULL).
- **Trực quan hóa chuyên nghiệp trên Tableau Public**:
  - **10 Biểu đồ chuyên sâu (Worksheets)**: Thuộc 9 loại biểu đồ khác nhau, phân chia theo tỷ lệ 2/4/4 cho 3 thành viên.
  - **3 Dashboards theo chủ đề (D1 $\to$ D3)**: D1 (Bức tranh 20 năm California & Dự báo), D2 (Điểm nóng 58 Hạt & Tổn thất 80/20), D3 (Mùa vụ, Căn nguyên & Siêu đám cháy).
  - **Tableau Story với 3 Story Points**: Dẫn dắt câu chuyện dữ liệu sinh động, có chú thích (Annotation) nổi bật từ số liệu thật và kết luận chính sách.
  - **Triển khai kép**: Nhúng trực tiếp bản Tableau Public vào GitHub Pages và lưu file đóng gói `.twbx` trong repository.

---

## 2. Bảng Phân Công Nhiệm Vụ 3 Thành Viên (Pipeline Tuần Tự)

> 📖 **Xem chi tiết bảng phân công và bộ quy tắc đặt tên file nghiêm ngặt tại**: [team/README.md](team/README.md)

| Thành viên | Phụ trách chính | Nhánh Git | Phạm vi công việc tuần tự | Biểu đồ đảm nhiệm |
|---|---|---|---|---|
| **Thành viên 1** | Kỹ sư Dữ liệu & Học máy (ML Engineer) | `member-1-data` | Thu thập 5 nguồn California, EDA với **3–5 biểu đồ tĩnh** (Matplotlib/Seaborn), Làm sạch dữ liệu, **Huấn luyện Mô hình dự báo (Linear/Logistic Regression)** trên Python, bàn giao `master_clean.csv` và `forecast_results.csv` | **#1, #2** (2 Tableau Sheets) |
| **Thành viên 2** | Kỹ sư Mô hình Dữ liệu (Data Modeling) | `member-2-model` | Star Schema $\ge 3$ bảng 3NF, CSDL SQLite (PK, FK, CHECK), Kiểm thử toàn vẹn tự động (pytest), Tách bảng tự động, Viết truy vấn SQL, bàn giao `database.sqlite` | **#3, #4, #5, #6** (4 Tableau Sheets) |
| **Thành viên 3** | Kỹ sư Dashboard & Triển khai (DevOps) | `member-3-dashboard` | Thiết kế 3 Dashboards, **Trực quan hóa kết quả dự báo của TV1**, Xây dựng Tableau Story (3 Story Points), Xuất bản Tableau Public, Nhúng Web, **Video Demo & Backup**, Báo cáo IEEE ($\ge 40$ trang) | **#7, #8, #9, #10** (4 Tableau Sheets) |

---

## 3. Cấu Trúc Trực Quan Hóa (3 Dashboards & Tableau Story 3 Points)

### 3.1. Cấu trúc 3 Dashboards
1. **Dashboard D1 – Bức tranh 20 năm Cháy rừng California**: #1 Combo cột số vụ + đường diện tích cháy + Trend Line dự báo (TV1); #2 Stacked area cơ cấu nguyên nhân cháy (TV1); #3 Diverging bar chênh lệch số vụ vs trung bình 20 năm (TV2).
2. **Dashboard D2 – Điểm nóng & Phân cấp thiệt hại theo 58 Hạt**: #4 Treemap phân cấp Hạt $\to$ Loại công trình (TV2); #7 Combo Pareto top 10 Hạt nhà bị phá hủy 80/20 (TV3); #9 Choropleth map 58 Hạt California (TV3).
3. **Dashboard D3 – Mùa vụ, Căn nguyên & Siêu đám cháy**: #5 Bubble scatter tương quan Log-Log (TV2); #6 Combo histogram diện tích cháy (TV2); #8 Donut nguyên nhân 2 tầng (TV3); #10 Bản đồ điểm đại vụ cháy lớn California (TV3).

### 3.2. Cấu trúc Tableau Story (3 Story Points Trọng Tâm)
- **Point 1**: *Bức tranh 20 năm Cháy rừng California: Tần suất & Mức độ khốc liệt* (Làm nổi bật đỉnh kỷ lục 2020 hơn 4.3 triệu Acres và xu hướng gia tăng theo mô hình Hồi quy tuyến tính).
- **Point 2**: *Điểm nóng 58 Hạt California: Phân cấp tổn thất 80/20* (Làm nổi bật nguyên lý 80/20: dưới 20% số Hạt như Butte, Sonoma, Shasta gánh chịu trên 80% số nhà bị phá hủy).
- **Point 3**: *Căn nguyên, Siêu đám cháy & Thách thức Tương lai* (Làm rõ các siêu đám cháy $\ge 100.000$ mẫu, căn nguyên con người gần khu dân cư và các bài học can thiệp).

---

## 4. Cấu Trúc Thư Mục Repository

```
IDV_TTDL/
├── README.md                  # Giới thiệu tổng quan, link Tableau Public, cách chạy
├── PROJECT_GUIDE.md           # Hướng dẫn chi tiết, tiến độ, quy ước nhánh và mốc tuần
├── SETUP.md                   # Hướng dẫn cài đặt môi trường cho cả 3 HĐH
├── team/                      # Phân công nhiệm vụ chi tiết từng thành viên
│   ├── README.md              # Sổ tay phân công & quy ước đặt tên file
│   ├── member-1-data/TASKS.md
│   ├── member-2-model/TASKS.md
│   └── member-3-dashboard/TASKS.md
├── tableau/                   # Không gian làm việc Tableau
│   ├── README.md              # Hướng dẫn tạo 10 sheets, 3 dashboards, 3 story points
│   ├── CALCULATED_FIELDS.md   # Toàn bộ công thức tính toán trong Tableau
│   └── wildfire_disaster_analysis.twbx # File Workbook đóng gói của đồ án
├── data/                      # Dữ liệu qua các công đoạn (không commit file > 90MB)
│   ├── raw/calfire/           # Dữ liệu gốc 5 bảng chính thức (đủ 20 năm) + MANIFEST.md
│   ├── interim/               # master_rules_cleaned.csv (sau làm sạch quy tắc)
│   ├── clean/                 # master_clean.csv (sau làm sạch ML, >= 5.000 dòng) + forecast_results.csv + casualties_by_year.csv
│   └── tables/                # Các bảng Star Schema CSV + database.sqlite
├── notebooks/                 # Jupyter Notebooks thực hiện EDA và kiểm thử ML
├── sql/                       # Mã nguồn CSDL SQLite
│   ├── schema.sql             # CREATE TABLE + PK/FK/CHECK/UNIQUE/INDEX (>= 3 bảng)
│   ├── load.sql               # Kịch bản nạp dữ liệu
│   └── queries_for_charts.sql # Truy vấn phục vụ các biểu đồ
├── src/                       # Mã nguồn pipeline tự động
│   ├── 01_download.py         # Thu thập dữ liệu thô (TV1)
│   ├── 02_eda.py              # Khám phá dữ liệu và thống kê thiếu (TV1)
│   ├── 03_clean.py            # Làm sạch theo quy tắc (TV1)
│   ├── 03b_ml_clean.py        # Làm sạch bằng học máy Isolation Forest & MICE (TV1) — chưa triển khai
│   ├── 04_split_tables.py     # Tách bảng Star Schema chuẩn 3NF (TV2)
│   ├── 05_build_db.py         # Nạp CSDL database.sqlite kích hoạt FK (TV2)
│   ├── 07_validate.py         # Kiểm thử tự động toàn vẹn tham chiếu và CHECK (TV2)
│   └── 08_predictive_model.py # Huấn luyện mô hình Linear Regression trên Python (TV1)
├── tests/                     # Bộ kiểm thử pytest
│   └── test_pipeline.py
├── docs/                      # Hồ sơ tài liệu kỹ thuật hoàn chỉnh
│   ├── DATA_SOURCES.md        # Đánh giá & so sánh 5 nguồn dữ liệu California đủ 20 năm
│   ├── DATA_DICTIONARY.md     # Từ điển dữ liệu và ý nghĩa các cờ ML & khóa liên kết
│   ├── DATA_QUALITY_REPORT.md # Báo cáo EDA chất lượng ban đầu
│   ├── CLEANING_LOG.md        # Nhật ký các bước làm sạch và quyết định ngoại lai
│   ├── ML_CLEANING_REPORT.md  # Báo cáo thực nghiệm ML và so sánh sai số
│   ├── ERD.md                 # Sơ đồ quan hệ thực thể Star Schema Mermaid
│   ├── CHART_SPEC.md          # Đặc tả 10 worksheets Tableau, 3 Dashboards & 3 Story Points
│   ├── COLOR_GUIDE.md         # Quy chuẩn màu sắc WCAG AA & Tableau Palettes
│   ├── REPORT_OUTLINE.md      # Dàn ý báo cáo đồ án và cấu trúc slide thuyết trình
│   └── DEMO_SCRIPT.md         # Kịch bản demo từng phút
├── dashboard/                 # Web tĩnh (Nhúng Tableau Story & Deploy GitHub Pages)
│   ├── index.html             # Trang web nhúng Tableau Story tương tác
│   ├── css/style.css          # Định dạng giao diện khung nhúng
│   └── js/
└── .github/workflows/deploy.yml # CI/CD tự động deploy dashboard lên GitHub Pages
```

---

## 5. Hướng Dẫn Sử Dụng & Mở File Tableau

### 5.1. Mở trực tiếp trên máy tính với Tableau Desktop / Tableau Public
1. Cài đặt **Tableau Desktop** hoặc **Tableau Public** (miễn phí).
2. Tải hoặc clone repository về máy tính.
3. Mở tệp [tableau/wildfire_disaster_analysis.twbx](tableau/wildfire_disaster_analysis.twbx). Toàn bộ 10 worksheets, 3 dashboards và Story Points sẽ tự động nạp cùng dữ liệu.

### 5.2. Chạy Pipeline Dữ Liệu Bằng Python
```bash
# Cài đặt môi trường Python
pip install -r requirements.txt

# Chạy thu thập dữ liệu thô
python src/01_download.py
```
