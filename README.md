# IDV_TTDL: Nghiên Cứu – Phân Tích Tần Suất và Thiệt Hại Cháy Rừng & Thảm Họa Thiên Nhiên (2006–2025)

[![Deploy Dashboard to GitHub Pages](https://github.com/tpdk0105/IDV_TTDL/actions/workflows/deploy.yml/badge.svg)](https://github.com/tpdk0105/IDV_TTDL/actions/workflows/deploy.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![Apache ECharts: 6.1.0](https://img.shields.io/badge/Apache%20ECharts-6.1.0-orange.svg)](https://echarts.apache.org/)

> **Môn học**: Tương tác Dữ liệu Trực quan (Interactive Data Visualization)  
> **Đồ án cuối kỳ**: Nhóm 3 sinh viên  
> **Kho lưu trữ chính thức**: [https://github.com/tpdk0105/IDV_TTDL](https://github.com/tpdk0105/IDV_TTDL)  
> **Trang trải nghiệm trực tiếp (Dashboard)**: [https://tpdk0105.github.io/IDV_TTDL/](https://tpdk0105.github.io/IDV_TTDL/)

---

## 1. Giới Thiệu Đề Tài & Trọng Tâm Nghiên Cứu
Dự án tập trung nghiên cứu, làm sạch, mô hình hóa và trực quan hóa tương tác đa chiều về **tần suất và thiệt hại của các trận cháy rừng toàn cầu trong 20 năm qua (2006–2025)**. Các thảm họa thiên nhiên khác (lũ lụt, bão nhiệt đới, hạn hán, động đất, núi lửa...) được đặt song song làm bối cảnh so sánh quy mô tác động kinh tế và sinh mạng.

### Điểm nổi bật về kỹ thuật:
- **Kỹ thuật dữ liệu vững chắc**: Pipeline tự động tái lập từ dữ liệu thô $\to$ làm sạch bằng quy tắc $\to$ làm sạch thông minh bằng **Học máy (Isolation Forest, LOF, KNN/Iterative Imputer)** $\to$ cam kết tập dữ liệu sạch đạt $\ge 5.000$ dòng.
- **Mô hình hóa chuẩn hình sao (Star Schema)**: Tách dữ liệu đạt chuẩn tối thiểu 3NF, lưu trữ trên SQLite với toàn bộ hệ thống ràng buộc toàn vẹn tham chiếu (PK, FK, CHECK, UNIQUE, NOT NULL).
- **Giao diện trực quan hóa tương tác (Dashboard)**: Xây dựng bằng Apache ECharts (chạy offline local vendor), bản đồ GeoJSON thế giới, bộ lọc toàn cục, liên kết chéo (Cross-filtering), hỗ trợ giao diện Sáng / Tối, chuẩn khả năng tiếp cận WCAG 2.1 AA và bảng màu thân thiện người mù màu (Okabe-Ito, OrRd, RdBu).

---

## 2. Bảng Phân Công Nhiệm Vụ 3 Thành Viên

| Thành viên | Phụ trách chính | Nhánh Git | Phạm vi công việc | 4 Biểu đồ đảm nhiệm |
|------------|-----------------|-----------|-------------------|----------------------|
| **Thành viên 1** | Kỹ sư Dữ liệu (Data Engineer) | `member-1-data` | Thu thập dữ liệu $\ge 3$ nguồn, EDA, Làm sạch theo quy tắc & Học máy ($\ge 2$ mô hình), Từ điển dữ liệu, Báo cáo chất lượng | **#1, #2, #3, #4** |
| **Thành viên 2** | Kỹ sư Mô hình Dữ liệu (Data Modeling) | `member-2-model` | Star Schema 3NF, DDL CSDL SQLite, Ràng buộc PK/FK/CHECK, Kiểm thử toàn vẹn tự động, Viết truy vấn SQL | **#5, #6, #7, #8** |
| **Thành viên 3** | Kỹ sư Dashboard & Triển khai (DevOps) | `member-3-dashboard` | Khung Dashboard ECharts, GeoJSON, Bộ lọc toàn cục, Bảng màu chung, CI/CD GitHub Pages, Báo cáo & Kịch bản thuyết trình | **#9, #10, #11, #12** |

---

## 3. Hệ Thống 12 Biểu Đồ Trực Quan Hóa Bắt Buộc

| # | Tên Biểu Đồ | Dạng Đồ Thị | Kiểu Dữ Liệu | Bảng Màu Quy Chuẩn | Người Làm |
|---|-------------|-------------|--------------|-------------------|-----------|
| 1 | Tần suất & Thiệt hại theo năm | **Combo** Bar (Số vụ) + Line (Thiệt hại USD) trục kép | Thời gian + 2 số | Categorical (2 màu tương phản) | Thành viên 1 |
| 2 | Cơ cấu thảm họa theo thời gian | Stacked Area (Diện tích xếp chồng) | Thời gian $\times$ Phân loại | Categorical (Okabe-Ito chuẩn) | Thành viên 1 |
| 3 | Bản đồ thiệt hại / số vụ thế giới | Choropleth Map (Bản đồ phân vùng) | Không gian $\times$ Số | Sequential (OrRd) | Thành viên 1 |
| 4 | Ma trận chu kỳ mùa cháy rừng | Heatmap (Tháng $\times$ Năm) | Chu kỳ $\times$ Thời gian $\times$ Số | Sequential (YlOrRd) | Thành viên 1 |
| 5 | Biến động so với trung bình 20 năm | Diverging Bar (Cột phân kỳ) | Độ lệch $\times$ Thời gian | Diverging (RdBu, tâm = 0) | Thành viên 2 |
| 6 | Phân cấp thiệt hại kinh tế | Treemap (Châu lục $\to$ Quốc gia, drill-down) | Phân cấp $\times$ Định lượng | Sequential / Categorical cấp 1 | Thành viên 2 |
| 7 | Diện tích cháy vs Thiệt hại | Bubble Scatter (Trục Log-Log) | 3 số + Phân loại | Categorical (Châu lục) | Thành viên 2 |
| 8 | Phân phối diện tích cháy rừng | **Combo** Histogram + KDE/Lũy kế | Phân phối biến số | Sequential đơn sắc | Thành viên 2 |
| 9 | Top 10 quốc gia tử vong | **Combo Pareto** Bar + Line (% Lũy kế) | Xếp hạng $\times$ Tích lũy | Sequential + Màu nhấn | Thành viên 3 |
| 10 | Cơ cấu nguyên nhân cháy rừng | Sunburst / Donut nhiều tầng | Cấu phần phân cấp | Categorical (Nguyên nhân) | Thành viên 3 |
| 11 | Dòng chuyển giao tác động | Sankey Diagram (Nguyên nhân $\to$ Loại $\to$ Thiệt hại) | Luồng quan hệ | Categorical (Độ dốc luồng) | Thành viên 3 |
| 12 | Bản đồ điểm các vụ cháy lớn | Proportional Symbol Map (Bản đồ điểm định lượng) | Không gian (Kinh/Vĩ) + Số | Sequential (Kích thước & Màu) | Thành viên 3 |

---

## 4. Cấu Trúc Thư Mục Repository

```
IDV_TTDL/
├── README.md                  # Giới thiệu tổng quan, cách chạy, link dashboard
├── PROJECT_GUIDE.md           # Hướng dẫn chi tiết, tiến độ, quy ước nhánh và mốc tuần
├── SETUP.md                   # Hướng dẫn cài đặt môi trường cho cả 3 HĐH
├── team/                      # Phân công nhiệm vụ chi tiết từng thành viên
│   ├── member-1-data/TASKS.md
│   ├── member-2-model/TASKS.md
│   └── member-3-dashboard/TASKS.md
├── data/                      # Dữ liệu qua các công đoạn (không commit file > 90MB)
│   ├── raw/                   # Dữ liệu gốc thu thập từ nguồn chính thức
│   ├── interim/               # master_rules_cleaned.csv (sau làm sạch quy tắc)
│   ├── clean/                 # master_clean.csv (sau làm sạch ML, >= 5.000 dòng)
│   └── tables/                # Các bảng Star Schema CSV + database.sqlite
├── notebooks/                 # Jupyter Notebooks thực hiện EDA và kiểm thử ML
├── sql/                       # Mã nguồn CSDL SQLite
│   ├── schema.sql             # CREATE TABLE + PK/FK/CHECK/UNIQUE/INDEX
│   ├── load.sql               # Kịch bản nạp dữ liệu
│   └── queries_for_charts.sql # Truy vấn phục vụ 12 biểu đồ (có chú thích TV)
├── src/                       # Mã nguồn pipeline tự động
│   ├── 01_download.py         # Thu thập dữ liệu thô (TV1)
│   ├── 02_eda.py              # Khám phá dữ liệu và thống kê thiếu (TV1)
│   ├── 03_clean.py            # Làm sạch theo quy tắc (TV1)
│   ├── 03b_ml_clean.py        # Làm sạch bằng học máy Isolation Forest & MICE (TV1)
│   ├── 04_split_tables.py     # Tách bảng Star Schema chuẩn 3NF (TV2)
│   ├── 05_build_db.py         # Nạp CSDL database.sqlite kích hoạt FK (TV2)
│   ├── 06_export_json.py      # Xuất JSON cho dashboard (TV2/TV3)
│   └── 07_validate.py         # Kiểm thử tự động toàn vẹn tham chiếu và CHECK (TV2)
├── tests/                     # Bộ kiểm thử pytest
│   └── test_pipeline.py
├── docs/                      # Hồ sơ tài liệu kỹ thuật hoàn chỉnh
│   ├── DATA_SOURCES.md        # Đánh giá & so sánh nguồn dữ liệu
│   ├── DATA_DICTIONARY.md     # Từ điển dữ liệu và ý nghĩa các cờ ML
│   ├── DATA_QUALITY_REPORT.md # Báo cáo EDA chất lượng ban đầu
│   ├── CLEANING_LOG.md        # Nhật ký các bước làm sạch và quyết định ngoại lai
│   ├── ML_CLEANING_REPORT.md  # Báo cáo thực nghiệm ML và so sánh sai số
│   ├── ERD.md                 # Sơ đồ quan hệ thực thể Mermaid
│   ├── CHART_SPEC.md          # Đặc tả chi tiết 12 biểu đồ trực quan
│   ├── COLOR_GUIDE.md         # Quy chuẩn màu sắc WCAG AA & Okabe-Ito
│   ├── REPORT_OUTLINE.md      # Dàn ý báo cáo đồ án và cấu trúc slide thuyết trình
│   └── DEMO_SCRIPT.md         # Kịch bản demo từng phút
├── dashboard/                 # Web tĩnh (Deploy tự động lên GitHub Pages)
│   ├── index.html             # Giao diện tổng quan responsive
│   ├── css/style.css          # Định dạng giao diện Light/Dark
│   ├── js/
│   │   ├── app.js             # Quản lý bộ lọc toàn cục và Cross-filtering
│   │   ├── palette.js         # Bảng màu dùng chung
│   │   ├── vendor/            # Thư viện ECharts offline (không phụ thuộc CDN)
│   │   └── charts/            # 12 mô-đun biểu đồ độc lập (chart-01.js .. chart-12.js)
│   └── data/                  # Dữ liệu JSON phục vụ các biểu đồ
├── scripts/                   # Script thực thi một lệnh
│   ├── run_all.ps1            # Chạy toàn bộ pipeline trên PowerShell Windows
│   ├── run_all.sh             # Chạy toàn bộ pipeline trên Linux/macOS
│   └── copy_vendor.js         # Copy thư viện ECharts offline
├── .github/workflows/deploy.yml # CI/CD tự động deploy dashboard lên GitHub Pages
├── requirements.txt           # Thư viện Python đã ghim phiên bản
├── environment.yml            # Môi trường Conda idv-ttdl
├── package.json               # Gói phụ thuộc npm
├── .editorconfig              # Quy chuẩn định dạng mã nguồn
├── .gitignore                 # Loại trừ file lớn > 90MB, database, node_modules
└── Makefile                   # Lệnh tắt chuẩn hóa
```

---

## 5. Hướng Dẫn Cài Đặt & Chạy Thử Môi Trường

Xem chi tiết tại [SETUP.md](SETUP.md).

### 5.1. Cài đặt nhanh
```bash
# Clone repo
git clone https://github.com/tpdk0105/IDV_TTDL.git
cd IDV_TTDL

# Cài đặt thư viện Python
pip install -r requirements.txt

# Cài đặt công cụ giao diện và sao chép ECharts offline
npm install
npm run vendor
```

### 5.2. Chạy toàn bộ Pipeline dữ liệu (Một lệnh duy nhất)
- **Trên Windows PowerShell**:
  ```powershell
  .\scripts\run_all.ps1
  ```
- **Trên Linux / macOS**:
  ```bash
  bash scripts/run_all.sh
  ```

### 5.3. Khởi chạy xem trước Dashboard cục bộ
```bash
npm run start
```
Truy cập trình duyệt: `http://localhost:8080`.
