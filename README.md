# IDV_TTDL: Nghiên Cứu – Phân Tích Tần Suất và Thiệt Hại Cháy Rừng & Thảm Họa Thiên Nhiên (2006–2025)

[![Deploy Dashboard to GitHub Pages](https://github.com/tpdk0105/IDV_TTDL/actions/workflows/deploy.yml/badge.svg)](https://github.com/tpdk0105/IDV_TTDL/actions/workflows/deploy.yml)
[![Tableau Public](https://img.shields.io/badge/Tableau%20Public-Interactive%20Story-E97627.svg?logo=tableau)](https://public.tableau.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)

> **Môn học**: Tương tác Dữ liệu Trực quan (Interactive Data Visualization)  
> **Đồ án cuối kỳ**: Nhóm 3 sinh viên  
> **Kho lưu trữ chính thức**: [https://github.com/tpdk0105/IDV_TTDL](https://github.com/tpdk0105/IDV_TTDL)  
> **Trang trải nghiệm trực tiếp (Web / GitHub Pages)**: [https://tpdk0105.github.io/IDV_TTDL/](https://tpdk0105.github.io/IDV_TTDL/)  
> **Tableau Storyboard trực tuyến**: [Tableau Public Story URL](https://public.tableau.com/) *(Sẽ đính kèm link sau khi xuất bản)*  
> **File đóng gói Tableau Workbook**: [tableau/wildfire_disaster_analysis.twbx](tableau/wildfire_disaster_analysis.twbx)

---

## 1. Giới Thiệu Đề Tài & Trọng Tâm Nghiên Cứu
Dự án tập trung nghiên cứu, làm sạch, mô hình hóa và trực quan hóa tương tác đa chiều về **tần suất và thiệt hại của các trận cháy rừng toàn cầu trong 20 năm qua (2006–2025)**. Các thảm họa thiên nhiên khác (lũ lụt, bão nhiệt đới, hạn hán, động đất, núi lửa...) được đặt song song làm bối cảnh so sánh quy mô tác động kinh tế và sinh mạng.

### Điểm nổi bật về kỹ thuật:
- **Kỹ thuật dữ liệu vững chắc (Python Pipeline)**: Tự động tải từ các nguồn dữ liệu uy tín (OWID, NASA FIRMS, NOAA NCEI, USFS FPA-FOD) $\to$ làm sạch quy tắc $\to$ làm sạch thông minh bằng **Học máy (Isolation Forest, LOF, MICE/KNN)** $\to$ cam kết tập dữ liệu sạch đạt $\ge 5.000$ dòng.
- **Mô hình hóa chuẩn hình sao (Star Schema)**: Tách dữ liệu đạt chuẩn tối thiểu 3NF, nạp vào SQLite với toàn bộ hệ thống ràng buộc toàn vẹn tham chiếu (PK, FK, CHECK, UNIQUE, NOT NULL).
- **Trực quan hóa chuyên nghiệp trên Tableau Public**:
  - **12 Biểu đồ chuyên sâu (Worksheets)**: Phân chia đều 4/4/4 cho 3 thành viên.
  - **4 Dashboards theo chủ đề (D1 $\to$ D4)**: D1 (Bức tranh 20 năm), D2 (Ở đâu chịu thiệt hại?), D3 (Cháy rừng: Khi nào & lớn cỡ nào?), D4 (Vì sao & hệ quả).
  - **Tableau Story với 4 Story Points**: Dẫn dắt câu chuyện dữ liệu sinh động, có chú thích (Annotation) nổi bật từ số liệu thật và kết luận chính sách.
  - **Triển khai kép**: Nhúng trực tiếp bản Tableau Public vào GitHub Pages và lưu file đóng gói `.twbx` trong repository.

---

## 2. Bảng Phân Công Nhiệm Vụ 3 Thành Viên

| Thành viên | Phụ trách chính | Nhánh Git | Phạm vi công việc | 4 Biểu đồ đảm nhiệm |
|------------|-----------------|-----------|-------------------|----------------------|
| **Thành viên 1** | Kỹ sư Dữ liệu (Data Engineer) | `member-1-data` | Thu thập dữ liệu $\ge 3$ nguồn, EDA, Làm sạch theo quy tắc & Học máy ($\ge 2$ mô hình), Báo cáo chất lượng | **#1, #2, #3, #4** (Tableau Sheets) |
| **Thành viên 2** | Kỹ sư Mô hình Dữ liệu (Data Modeling) | `member-2-model` | Star Schema 3NF, DDL CSDL SQLite, Ràng buộc PK/FK/CHECK, Kiểm thử toàn vẹn tự động, Viết truy vấn SQL | **#5, #6, #7, #8** (Tableau Sheets) |
| **Thành viên 3** | Kỹ sư Dashboard & Triển khai (DevOps) | `member-3-dashboard` | Thiết kế 4 Dashboards, Xây dựng Tableau Story (4 Story Points), Xuất bản Tableau Public, Nhúng Web, CI/CD | **#9, #10, #11, #12** (Tableau Sheets) |

---

## 3. Cấu Trúc Trực Quan Hóa (4 Dashboards & Tableau Story)

### 3.1. Cấu trúc 4 Dashboards
1. **D1 – Bức tranh 20 năm**: #1 Combo cột số vụ + đường thiệt hại; #2 Stacked area cơ cấu thảm họa; #5 Diverging bar chênh lệch vs trung bình.
2. **D2 – Ở đâu chịu thiệt hại?**: #3 Choropleth map thế giới; #6 Treemap châu lục $\to$ quốc gia; #9 Combo Pareto top 10 tử vong 80/20.
3. **D3 – Cháy rừng: Khi nào & lớn cỡ nào?**: #4 Heatmap tháng $\times$ năm; #8 Combo histogram diện tích cháy; #12 Bản đồ điểm vụ cháy lớn.
4. **D4 – Vì sao & hệ quả**: #10 Donut nguyên nhân; #11 Sankey luồng chuyển giao; #7 Bubble scatter tương quan Log-Log.

### 3.2. Cấu trúc Tableau Story (4 Story Points)
- **Point 1**: *Bức tranh 20 năm: Tần suất & Thiệt hại* (Làm nổi bật đỉnh kỷ lục 2020 và xu hướng thảm họa gia tăng sau chu kỳ 2017).
- **Point 2**: *Điểm nóng toàn cầu: Châu lục & Quốc gia tổn thất nặng* (Làm nổi bật nguyên lý 80/20 và mức độ tập trung thiệt hại).
- **Point 3**: *Trọng tâm Cháy rừng: Mùa cao điểm & Siêu đám cháy* (Làm rõ chu kỳ khô hạn tháng 6–9 và các đám cháy $\ge 10.000$ ha).
- **Point 4**: *Căn nguyên & Tác động: Tự nhiên vs Con người* (Phân tích tỷ trọng nhân tạo vs tự nhiên và đúc kết khuyến nghị).

---

## 4. Cấu Trúc Thư Mục Repository

```
IDV_TTDL/
├── README.md                  # Giới thiệu tổng quan, link Tableau Public, cách chạy
├── PROJECT_GUIDE.md           # Hướng dẫn chi tiết, tiến độ, quy ước nhánh và mốc tuần
├── SETUP.md                   # Hướng dẫn cài đặt môi trường cho cả 3 HĐH
├── team/                      # Phân công nhiệm vụ chi tiết từng thành viên
│   ├── member-1-data/TASKS.md
│   ├── member-2-model/TASKS.md
│   └── member-3-dashboard/TASKS.md
├── tableau/                   # Không gian làm việc Tableau
│   ├── README.md              # Hướng dẫn tạo 12 sheets, 4 dashboards, story points
│   ├── CALCULATED_FIELDS.md   # Toàn bộ công thức tính toán trong Tableau
│   └── wildfire_disaster_analysis.twbx # File Workbook đóng gói của đồ án
├── data/                      # Dữ liệu qua các công đoạn (không commit file > 90MB)
│   ├── raw/                   # Dữ liệu gốc thu thập từ nguồn chính thức + MANIFEST.md
│   ├── interim/               # master_rules_cleaned.csv (sau làm sạch quy tắc)
│   ├── clean/                 # master_clean.csv (sau làm sạch ML, >= 5.000 dòng)
│   └── tables/                # Các bảng Star Schema CSV + database.sqlite
├── notebooks/                 # Jupyter Notebooks thực hiện EDA và kiểm thử ML
├── sql/                       # Mã nguồn CSDL SQLite
│   ├── schema.sql             # CREATE TABLE + PK/FK/CHECK/UNIQUE/INDEX
│   ├── load.sql               # Kịch bản nạp dữ liệu
│   └── queries_for_charts.sql # Truy vấn phục vụ các biểu đồ
├── src/                       # Mã nguồn pipeline tự động
│   ├── 01_download.py         # Thu thập dữ liệu thô (TV1)
│   ├── 02_eda.py              # Khám phá dữ liệu và thống kê thiếu (TV1)
│   ├── 03_clean.py            # Làm sạch theo quy tắc (TV1)
│   ├── 03b_ml_clean.py        # Làm sạch bằng học máy Isolation Forest & MICE (TV1)
│   ├── 04_split_tables.py     # Tách bảng Star Schema chuẩn 3NF (TV2)
│   ├── 05_build_db.py         # Nạp CSDL database.sqlite kích hoạt FK (TV2)
│   ├── 06_export_json.py      # Xuất dữ liệu hỗ trợ (TV2/TV3)
│   └── 07_validate.py         # Kiểm thử tự động toàn vẹn tham chiếu và CHECK (TV2)
├── tests/                     # Bộ kiểm thử pytest
│   └── test_pipeline.py
├── docs/                      # Hồ sơ tài liệu kỹ thuật hoàn chỉnh
│   ├── DATA_SOURCES.md        # Đánh giá & so sánh 5 nguồn dữ liệu
│   ├── DATA_DICTIONARY.md     # Từ điển dữ liệu và ý nghĩa các cờ ML
│   ├── DATA_QUALITY_REPORT.md # Báo cáo EDA chất lượng ban đầu
│   ├── CLEANING_LOG.md        # Nhật ký các bước làm sạch và quyết định ngoại lai
│   ├── ML_CLEANING_REPORT.md  # Báo cáo thực nghiệm ML và so sánh sai số
│   ├── ERD.md                 # Sơ đồ quan hệ thực thể Star Schema Mermaid
│   ├── CHART_SPEC.md          # Đặc tả 12 worksheets Tableau & 4 Story Points
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
3. Mở tệp [tableau/wildfire_disaster_analysis.twbx](tableau/wildfire_disaster_analysis.twbx). Toàn bộ 12 worksheets, 4 dashboards và Story Points sẽ tự động nạp cùng dữ liệu.

### 5.2. Chạy Pipeline Dữ Liệu Bằng Python
```bash
# Cài đặt môi trường Python
pip install -r requirements.txt

# Chạy thu thập dữ liệu thô
python src/01_download.py
```
