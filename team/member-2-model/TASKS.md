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
9. Viết truy vấn SQL trong [sql/queries_for_charts.sql](../../sql/queries_for_charts.sql) và script [src/06_export_json.py](../../src/06_export_json.py) cho 4 biểu đồ của mình (#3–#6).
10. Hoàn thành 4 biểu đồ được giao (**#3 `Sheet_03_Diverging_Bar`**, **#4 `Sheet_04_Treemap_Damage`**, **#5 `Sheet_05_Bubble_Scatter`**, **#6 `Sheet_06_Combo_Histogram`**) trên Tableau.

---

## 2. Bảng Theo Dõi Trạng Thái Công Việc

| Hạng mục công việc | Trạng thái | Deadline | Ghi chú cá nhân |
|--------------------|------------|----------|-----------------|
| Thiết lập môi trường & nhánh `member-2-model` | Sẵn sàng | Tuần 1 | Giai đoạn 1 |
| Thiết kế Star Schema $\ge 3$ bảng & vẽ `docs/ERD.md` | Hoàn thành | Tuần 2 | Cardinality 1–N |
| Viết script tách bảng `04_split_tables.py` | Chưa bắt đầu | *[Điền]* | Lưu vào `data/tables/` |
| Viết DDL CSDL `sql/schema.sql` | Chưa bắt đầu | *[Điền]* | Ràng buộc PK/FK/CHECK |
| Viết script tạo CSDL `05_build_db.py` | Chưa bắt đầu | *[Điền]* | Nạp `database.sqlite` |
| Viết script kiểm thử `07_validate.py` & tests | Chưa bắt đầu | *[Điền]* | Kiểm tra FK mồ côi |
| Viết SQL cho biểu đồ #3–#6 trong `queries_for_charts.sql` | Chưa bắt đầu | *[Điền]* | Truy vấn tối ưu |
| Viết script xuất JSON `06_export_json.py` (biểu đồ TV2) | Chưa bắt đầu | *[Điền]* | Xuất `dashboard/data/` |
| Biểu đồ #3: `Sheet_03_Diverging_Bar` | Chưa bắt đầu | *[Điền]* | Lệch so với trung bình |
| Biểu đồ #4: `Sheet_04_Treemap_Damage` | Chưa bắt đầu | *[Điền]* | Hạt $\to$ Loại công trình |
| Biểu đồ #5: `Sheet_05_Bubble_Scatter` | Chưa bắt đầu | *[Điền]* | Diện tích vs Nhà cháy (Log) |
| Biểu đồ #6: `Sheet_06_Combo_Histogram` | Chưa bắt đầu | *[Điền]* | Phân phối diện tích cháy |

---

## 3. Danh Sách Checklist Chi Tiết

### A. Thiết Kế Mô Hình & Phân Tách Dữ Liệu
- [x] Thiết kế kiến trúc Star Schema từ `master_clean.csv` liên kết các vụ cháy với thiệt hại công trình (DINS).
- [x] Soạn thảo sơ đồ Mermaid ERD chi tiết trong `docs/ERD.md` với đầy đủ kiểu dữ liệu và ghi chú khóa.
- [ ] Viết `src/04_split_tables.py`:
  - [ ] Tạo khóa thay thế (surrogate keys) tự tăng hoặc định dạng số nguyên có quy tắc.
  - [ ] Tách các bảng chiều: `dim_county.csv` (58 Hạt), `dim_cause.csv`, `dim_date.csv`.
  - [ ] Tách các bảng sự kiện: `fact_fire_incident.csv` (7.342 vụ) và `fact_structure_damage.csv` (>130.000 công trình).
  - [ ] Đảm bảo chuẩn hóa tối thiểu 3NF.

### B. Thiết Lập CSDL & Ràng Buộc Toàn Vẹn
- [ ] Soạn thảo `sql/schema.sql`:
  - [ ] Khóa chính PRIMARY KEY cho từng bảng.
  - [ ] Khóa ngoại FOREIGN KEY với hành vi `ON DELETE RESTRICT ON UPDATE CASCADE`.
  - [ ] Ràng buộc UNIQUE (vd: `county_name`, `cause_code`).
  - [ ] Ràng buộc CHECK:
    - [ ] `acres_burned >= 0.0`, `burned_area_ha >= 0.0`
    - [ ] `total_structures_destroyed >= 0`, `total_structures_damaged >= 0`
    - [ ] `year BETWEEN 2006 AND 2025`
    - [ ] `latitude BETWEEN 32.0 AND 42.0` (Phạm vi California)
    - [ ] `longitude BETWEEN -125.0 AND -114.0` (Phạm vi California)
    - [ ] Các cột cờ: `CHECK (col IN (0, 1))`
  - [ ] Tạo INDEX cho các cột thường xuyên JOIN và WHERE (`date_id`, `county_id`, `cause_id`, `fire_name`).
- [ ] Viết `src/05_build_db.py`:
  - [ ] Kết nối SQLite và thực thi lệnh `PRAGMA foreign_keys = ON;`.
  - [ ] Tạo bảng từ `sql/schema.sql`.
  - [ ] Nạp dữ liệu từ `data/tables/` vào `data/tables/database.sqlite`.

### C. Kiểm Thử Toàn Vẹn Dữ Liệu & Ràng Buộc
- [ ] Viết script kiểm thử độc lập `src/07_validate.py`:
  - [ ] Kiểm tra không tồn tại khóa ngoại mồ côi (Zero Orphan Foreign Keys).
  - [ ] Kiểm tra không trùng lặp khóa chính.
  - [ ] Kiểm tra bảng fact đạt $\ge 5.000$ dòng.
  - [ ] Kiểm tra 100% các điều kiện CHECK constraints đều thỏa mãn.
  - [ ] Kiểm tra các cột cờ nhị phân chỉ nhận giá trị 0 hoặc 1.
- [ ] Viết bộ kiểm thử tự động `tests/test_pipeline.py` (chạy bằng `pytest`).

### D. Truy Vấn & Xuất Dữ Liệu JSON
- [ ] Viết các câu truy vấn SQL tối ưu hóa cho biểu đồ #3–#6 trong `sql/queries_for_charts.sql`.
- [ ] Phát triển mô-đun xuất JSON trong `src/06_export_json.py` cho các biểu đồ của mình.

---

## 4. Các Biểu Đồ Phụ Trách (4 Worksheets: #3, #4, #5, #6 trên Tableau)

### Worksheet #3: `Sheet_03_Diverging_Bar` (Biến động số vụ so với trung bình 20 năm)
- [ ] (a) Tạo Calculated Fields `[Diff from 20Yr Avg]` và `[Divergence Flag]`.
- [ ] (b) Kéo `[Diff from 20Yr Avg]` vào Columns, `[year]` vào Rows; Marks: Bar.
- [ ] (c) Kéo `[Divergence Flag]` vào Color (Đỏ: Vượt TB, Xanh: Dưới TB); thêm Reference Line tại `0`.

### Worksheet #4: `Sheet_04_Treemap_Damage` (Cơ cấu công trình bị phá hủy: Hạt $\to$ Loại công trình)
- [ ] (a) Kéo `[county]` vào Color, `[structure_type]` vào Detail.
- [ ] (b) Kéo `CNT([record_id])` hoặc `SUM([structures_destroyed])` vào Size; Marks: Square (Treemap).

### Worksheet #5: `Sheet_05_Bubble_Scatter` (Tương quan Diện tích cháy vs Nhà phá hủy)
- [ ] (a) Trục X: `[acres_burned]` (Logarithmic scale); Trục Y: `[structures_destroyed]` (Logarithmic scale).
- [ ] (b) Size: `[acres_burned]`; Color: `[cause_group]`; Detail: `[fire_name]`; Marks: Circle.

### Worksheet #6: `Sheet_06_Combo_Histogram` (Phân phối diện tích cháy rừng)
- [ ] (a) Columns: `[Acres Bin Log]`.
- [ ] (b) Trục 1: `CNT([incident_id])` (Marks: Bar); Trục 2: `% Lũy kế Running Sum` (Marks: Line, Dual Axis).
