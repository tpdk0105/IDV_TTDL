# NHIỆM VỤ THÀNH VIÊN 2: KỸ SƯ MÔ HÌNH DỮ LIỆU (DATA MODELING ENGINEER)

> **Họ và tên**: [TÊN THÀNH VIÊN 2]  
> **MSSV**: [Điền MSSV]  
> **Nhánh Git phụ trách**: `member-2-model`  
> **Trọng tâm**: Mô hình hóa dữ liệu (Star Schema $\ge 3$ bảng), Chuẩn hóa 3NF, Ràng buộc CSDL SQLite (PK, FK, CHECK) & Kiểm thử toàn vẹn tự động; Thực hiện 4 biểu đồ #3–#6.

---

## 1. Mục Tiêu Chính
1. Thiết kế mô hình dữ liệu đa chiều hình sao (Star Schema $\ge 3$ bảng) từ tập dữ liệu `master_clean.csv`, đảm bảo mỗi bảng đạt chuẩn tối thiểu 3NF.
2. Xây dựng cấu trúc các bảng Dimension (`dim_county`, `dim_cause`, `dim_date`) và bảng Fact (`fact_fire_incident`, `fact_structure_damage`).
3. Bảo toàn đầy đủ các cột cờ chất lượng dữ liệu ML (`is_outlier_ml`, `outlier_score`, `burned_area_is_imputed`, `cause_is_predicted`) trong bảng Fact dưới dạng `INTEGER (0, 1)` với ràng buộc `CHECK`.
4. Phát triển script [src/04_split_tables.py](../../src/04_split_tables.py) tách dữ liệu thành các bảng CSV độc lập trong `data/tables/`.
5. Soạn thảo DDL [sql/schema.sql](../../sql/schema.sql) với toàn bộ hệ thống ràng buộc: PRIMARY KEY, FOREIGN KEY (`ON DELETE RESTRICT ON UPDATE CASCADE`), NOT NULL, UNIQUE, CHECK, DEFAULT và INDEX.
6. Xây dựng CSDL `database.sqlite` qua [src/05_build_db.py](../../src/05_build_db.py), kích hoạt `PRAGMA foreign_keys = ON;`.
7. Vẽ sơ đồ quan hệ thực thể [docs/ERD.md](../../docs/ERD.md) bằng Mermaid ERD kèm bản số (Cardinality).
8. Viết script kiểm thử tự động [src/07_validate.py](../../src/07_validate.py) và bộ kiểm thử [tests/test_pipeline.py](../../tests/test_pipeline.py).
9. Viết truy vấn SQL trong [sql/queries_for_charts.sql](../../sql/queries_for_charts.sql) tổng hợp số liệu cho 4 biểu đồ của mình (#3–#6).
10. Hoàn thành 4 biểu đồ được giao (**#3 `Sheet_03_Diverging_Bar`**, **#4 `Sheet_04_Treemap_Damage`**, **#5 `Sheet_05_Bubble_Scatter`**, **#6 `Sheet_06_Combo_Histogram`**) trên Tableau.

---

## 2. Bảng Theo Dõi Trạng Thái Công Việc

| Hạng mục công việc | Trạng thái | Deadline | Ghi chú cá nhân |
|--------------------|------------|----------|-----------------|
| Thiết lập môi trường & nhánh `member-2-model` | Hoàn thành | Tuần 1 | Đã đồng bộ nhánh Git |
| Thiết kế Star Schema $\ge 3$ bảng & vẽ `docs/ERD.md` | Hoàn thành | Tuần 2 | Chuẩn 3NF, Cardinality 1–N |
| Viết script tách bảng `04_split_tables.py` | Hoàn thành | Tuần 2 | 5 bảng CSV chuẩn trong `data/tables/` |
| Viết DDL CSDL `sql/schema.sql` | Hoàn thành | Tuần 2 | Đầy đủ PK/FK/CHECK/INDEX |
| Viết script tạo CSDL `05_build_db.py` | Hoàn thành | Tuần 2 | Nạp `database.sqlite` (Zero Orphan FK) |
| Viết script kiểm thử `07_validate.py` & tests | Hoàn thành | Tuần 2 | PASS 7/7 test toàn vẹn & Pytest 7/7 |
| Viết SQL cho biểu đồ #3–#6 trong `queries_for_charts.sql` | Hoàn thành | Tuần 2 | Đầy đủ khối truy vấn cho 4 biểu đồ |
| Biểu đồ #3: `Sheet_03_Diverging_Bar` | Sẵn sàng vẽ | Tuần 3 | Công thức Calculated Fields đã sẵn sàng cho Tableau |
| Biểu đồ #4: `Sheet_04_Treemap_Damage` | Sẵn sàng vẽ | Tuần 3 | Cấu trúc dữ liệu đã sẵn sàng cho Tableau |
| Biểu đồ #5: `Sheet_05_Bubble_Scatter` | Sẵn sàng vẽ | Tuần 3 | Thang đo Logarit đã sẵn sàng cho Tableau |
| Biểu đồ #6: `Sheet_06_Combo_Histogram` | Sẵn sàng vẽ | Tuần 3 | Công thức Phân nhóm Logarit sẵn sàng cho Tableau |

---

## 3. Danh Sách Checklist Chi Tiết

### A. Thiết Kế Mô Hình & Phân Tách Dữ Liệu
- [x] Thiết kế kiến trúc Star Schema từ `master_clean.csv` liên kết các vụ cháy với thiệt hại công trình (DINS + ICS-209).
- [x] Soạn thảo sơ đồ Mermaid ERD chi tiết trong `docs/ERD.md` với đầy đủ kiểu dữ liệu và ghi chú khóa.
- [x] Viết `src/04_split_tables.py`:
  - [x] Tạo khóa thay thế (surrogate keys) tự tăng hoặc định dạng số nguyên có quy tắc (`date_id = YYYYMMDD`).
  - [x] Tách các bảng chiều: `dim_county.csv` (58 Hạt + 1 Unknown), `dim_cause.csv` (19 mã), `dim_date.csv` (7.305 ngày 2006–2025).
  - [x] Tách các bảng sự kiện: `fact_fire_incident.csv` (7.235 vụ cháy $\ge 5.000$ dòng) và `fact_structure_damage.csv` (114.726 bản ghi thiệt hại công trình hợp nhất 20 năm từ ICS-209 và DINS).
  - [x] Đảm bảo chuẩn hóa tối thiểu 3NF.

### B. Thiết Lập CSDL & Ràng Buộc Toàn Vẹn
- [x] Soạn thảo `sql/schema.sql`:
  - [x] Khóa chính PRIMARY KEY cho từng bảng.
  - [x] Khóa ngoại FOREIGN KEY với hành vi `ON DELETE RESTRICT ON UPDATE CASCADE`.
  - [x] Ràng buộc UNIQUE (`full_date`, `county_name`, `cause_name`).
  - [x] Ràng buộc CHECK:
    - [x] `acres_burned >= 0.0`, `burned_area_ha >= 0.0`
    - [x] `total_structures_destroyed >= 0`, `total_structures_damaged >= 0`
    - [x] `year BETWEEN 2006 AND 2025`
    - [x] `latitude BETWEEN 32.0 AND 42.0` (Phạm vi California)
    - [x] `longitude BETWEEN -125.0 AND -114.0` (Phạm vi California)
    - [x] Các cột cờ: `CHECK (col IN (0, 1))`
  - [x] Tạo INDEX cho các cột thường xuyên JOIN và WHERE (`date_id`, `county_id`, `cause_id`, `fire_name`, `year`, `county_name`).
- [x] Viết `src/05_build_db.py`:
  - [x] Kết nối SQLite và thực thi lệnh `PRAGMA foreign_keys = ON;`.
  - [x] Tạo bảng từ `sql/schema.sql`.
  - [x] Nạp dữ liệu từ `data/tables/` vào `data/tables/database.sqlite`.

### C. Kiểm Thử Toàn Vẹn Dữ Liệu & Ràng Buộc
- [x] Viết script kiểm thử độc lập `src/07_validate.py`:
  - [x] Kiểm tra không tồn tại khóa ngoại mồ côi (Zero Orphan Foreign Keys: PRAGMA foreign_key_check = 0 lỗi).
  - [x] Kiểm tra không trùng lặp khóa chính (100% Unique PKs).
  - [x] Kiểm tra bảng fact đạt $\ge 5.000$ dòng (fact_fire_incident: 7.235 dòng, fact_structure_damage: 114.726 dòng).
  - [x] Kiểm tra 100% các điều kiện CHECK constraints đều thỏa mãn.
  - [x] Kiểm tra các cột cờ nhị phân chỉ nhận giá trị 0 hoặc 1.
### D. Truy Vấn SQL Cho Biểu Đồ
- [x] Viết các câu truy vấn SQL tối ưu hóa cho biểu đồ #3–#6 trong `sql/queries_for_charts.sql`.
- [x] Soạn thảo hướng dẫn công thức Calculated Fields tương ứng trong `tableau/CALCULATED_FIELDS.md`.

---

## 4. Các Biểu Đồ Phụ Trách (4 Worksheets: #3, #4, #5, #6 trên Tableau)

### Worksheet #3: `Sheet_03_Diverging_Bar` (Biến động số vụ so với trung bình 20 năm)
- [x] Truy vấn SQL trong `sql/queries_for_charts.sql` tính chênh lệch so với TB 20 năm (Tâm = 0).
- [ ] Xây dựng trên Tableau:
  - (a) Tạo Calculated Fields `[Diff from 20Yr Avg]` và `[Divergence Flag]`.
  - (b) Kéo `[Diff from 20Yr Avg]` vào Columns, `[year]` vào Rows; Marks: Bar.
  - (c) Kéo `[Divergence Flag]` vào Color (Đỏ: Vượt TB, Xanh: Dưới TB); thêm Reference Line tại `0`.

### Worksheet #4: `Sheet_04_Treemap_Damage` (Cơ cấu công trình bị phá hủy: Hạt $\to$ Loại công trình)
- [x] Truy vấn SQL phân cấp Hạt $\to$ Loại công trình kiến trúc.
- [ ] Xây dựng trên Tableau:
  - (a) Kéo `[county]` vào Color, `[structure_type]` vào Detail.
  - (b) Kéo `CNT([record_id])` hoặc `SUM([structures_destroyed])` vào Size; Marks: Square (Treemap).

### Worksheet #5: `Sheet_05_Bubble_Scatter` (Tương quan Diện tích cháy vs Nhà phá hủy)
- [x] Truy vấn SQL trích xuất tương quan diện tích, số nhà và thương vong.
- [ ] Xây dựng trên Tableau:
  - (a) Trục X: `[acres_burned]` (Logarithmic scale); Trục Y: `[structures_destroyed]` (Logarithmic scale).
  - (b) Size: `[acres_burned]`; Color: `[cause_group]`; Detail: `[fire_name]`; Marks: Circle.

### Worksheet #6: `Sheet_06_Combo_Histogram` (Phân phối diện tích cháy rừng)
- [x] Truy vấn SQL phân chia các bin logarit diện tích cháy rừng.
- [ ] Xây dựng trên Tableau:
  - (a) Columns: `[Acres Bin Log]`.
  - (b) Trục 1: `CNT([incident_id])` (Marks: Bar); Trục 2: `% Lũy kế Running Sum` (Marks: Line, Dual Axis).
