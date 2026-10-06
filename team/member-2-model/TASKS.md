# NHIỆM VỤ THÀNH VIÊN 2: KỸ SƯ MÔ HÌNH DỮ LIỆU (DATA MODELING ENGINEER)

> **Họ và tên**: [TÊN THÀNH VIÊN 2]  
> **MSSV**: [Điền MSSV]  
> **Nhánh Git phụ trách**: `member-2-model`  
> **Trọng tâm**: Mô hình hóa dữ liệu (Star Schema), Chuẩn hóa 3NF, Ràng buộc CSDL & Kiểm thử toàn vẹn; Thực hiện 4 biểu đồ #5–#8.

---

## 1. Mục Tiêu Chính
1. Thiết kế mô hình dữ liệu đa chiều hình sao (Star Schema) từ tập dữ liệu `master_clean.csv`, đảm bảo mỗi bảng đạt chuẩn tối thiểu 3NF.
2. Xây dựng cấu trúc các bảng Dimension (`dim_date`, `dim_location`, `dim_disaster_type`, `dim_cause`, `dim_source`) và Fact (`fact_disaster_event`, `fact_wildfire_detail`).
3. Bảo toàn đầy đủ các cột cờ chất lượng dữ liệu ML (`is_outlier_ml`, `outlier_score`, `deaths_is_imputed`, `damage_usd_is_imputed`, `burned_area_is_imputed`, `cause_is_predicted`) trong bảng Fact dưới dạng `INTEGER (0, 1)` với ràng buộc `CHECK`.
4. Phát triển script `src/04_split_tables.py` tách dữ liệu thành các bảng CSV độc lập trong `data/tables/`.
5. Soạn thảo DDL `sql/schema.sql` với toàn bộ hệ thống ràng buộc: PRIMARY KEY, FOREIGN KEY (`ON DELETE RESTRICT ON UPDATE CASCADE`), NOT NULL, UNIQUE, CHECK, DEFAULT và INDEX.
6. Xây dựng CSDL `database.sqlite` qua `src/05_build_db.py`, kích hoạt `PRAGMA foreign_keys = ON;`.
7. Vẽ sơ đồ quan hệ thực thể `docs/ERD.md` bằng Mermaid ERD kèm bản số (Cardinality).
8. Viết script kiểm thử tự động `src/07_validate.py` và kiểm thử `tests/test_pipeline.py`.
9. Viết truy vấn SQL và script `src/06_export_json.py` xuất dữ liệu cho các biểu đồ của mình (#5–#8).
10. Hoàn thành 4 biểu đồ được giao (#5, #6, #7, #8) theo đúng đặc tả và bảng màu chuẩn.

---

## 2. Bảng Theo Dõi Trạng Thái Công Việc

| Hạng mục công việc | Trạng thái | Deadline | Ghi chú cá nhân |
|--------------------|------------|----------|-----------------|
| Thiết lập môi trường & nhánh `member-2-model` | Sẵn sàng | Tuần 1 | Giai đoạn 1 |
| Thiết kế Star Schema & vẽ `docs/ERD.md` | Chưa bắt đầu | *[Điền]* | Cardinality 1–N |
| Viết script tách bảng `04_split_tables.py` | Chưa bắt đầu | *[Điền]* | Lưu vào `data/tables/` |
| Viết DDL CSDL `sql/schema.sql` | Chưa bắt đầu | *[Điền]* | Ràng buộc PK/FK/CHECK |
| Viết script tạo CSDL `05_build_db.py` | Chưa bắt đầu | *[Điền]* | Nạp `database.sqlite` |
| Viết script kiểm thử `07_validate.py` & tests | Chưa bắt đầu | *[Điền]* | Kiểm tra FK mồ côi |
| Viết SQL cho biểu đồ #5–#8 trong `queries_for_charts.sql` | Chưa bắt đầu | *[Điền]* | Truy vấn tối ưu |
| Viết script xuất JSON `06_export_json.py` (biểu đồ TV2) | Chưa bắt đầu | *[Điền]* | Xuất `dashboard/data/` |
| Biểu đồ #5: Diverging Bar Chart | Chưa bắt đầu | *[Điền]* | Lệch so với trung bình |
| Biểu đồ #6: Treemap phân cấp | Chưa bắt đầu | *[Điền]* | Châu lục $\to$ Quốc gia |
| Biểu đồ #7: Bubble Scatter (Trục Log-Log) | Chưa bắt đầu | *[Điền]* | Diện tích vs Thiệt hại |
| Biểu đồ #8: Combo Histogram + KDE/Lũy kế | Chưa bắt đầu | *[Điền]* | Phân phối diện tích |

---

## 3. Danh Sách Checklist Chi Tiết

### A. Thiết Kế Mô Hình & Phân Tách Dữ Liệu
- [ ] Thiết kế kiến trúc Star Schema từ `master_clean.csv`.
- [ ] Soạn thảo sơ đồ Mermaid ERD chi tiết trong `docs/ERD.md` với đầy đủ kiểu dữ liệu và ghi chú khóa.
- [ ] Viết `src/04_split_tables.py`:
  - [ ] Tạo khóa thay thế (surrogate keys) tự tăng hoặc định dạng số nguyên có quy tắc (vd: `YYYYMMDD` cho `dim_date`).
  - [ ] Tách `dim_date.csv`, `dim_location.csv`, `dim_disaster_type.csv`, `dim_cause.csv`, `dim_source.csv`.
  - [ ] Tách `fact_disaster_event.csv` và `fact_wildfire_detail.csv`.
  - [ ] Đảm bảo tính nhất quán và loại bỏ dư thừa dữ liệu (chuẩn hóa tối thiểu 3NF).

### B. Thiết Lập CSDL & Ràng Buộc Toàn Vẹn
- [ ] Soạn thảo `sql/schema.sql`:
  - [ ] Khóa chính PRIMARY KEY cho từng bảng.
  - [ ] Khóa ngoại FOREIGN KEY với hành vi `ON DELETE RESTRICT ON UPDATE CASCADE`.
  - [ ] Ràng buộc UNIQUE (vd: `country_iso3`, `(year, month)` trong `dim_date`, `type_name`, `cause_name`).
  - [ ] Ràng buộc CHECK:
    - [ ] `deaths >= 0`, `injured >= 0`, `affected >= 0`
    - [ ] `damage_usd >= 0.0`
    - [ ] `burned_area_ha >= 0.0`
    - [ ] `year BETWEEN 2005 AND 2024`
    - [ ] `latitude BETWEEN -90.0 AND 90.0`
    - [ ] `longitude BETWEEN -180.0 AND 180.0`
    - [ ] Các cột cờ: `CHECK (col IN (0, 1))`
  - [ ] Tạo INDEX cho các cột thường xuyên JOIN và WHERE (`date_id`, `location_id`, `type_id`, `cause_id`, `year`, `country_iso3`).
- [ ] Soạn thảo `sql/load.sql` hoặc cơ chế nạp bulk insert bằng Python.
- [ ] Viết `src/05_build_db.py`:
  - [ ] Kết nối SQLite và thực thi lệnh `PRAGMA foreign_keys = ON;`.
  - [ ] Tạo bảng từ `sql/schema.sql`.
  - [ ] Nạp toàn bộ dữ liệu từ `data/tables/` vào `database.sqlite`.
  - [ ] Bắt lỗi và ghi log cảnh báo nếu phát sinh vi phạm bất kỳ ràng buộc nào.

### C. Kiểm Thử Toàn Vẹn Dữ Liệu & Ràng Buộc
- [ ] Viết script kiểm thử độc lập `src/07_validate.py`:
  - [ ] Kiểm tra không tồn tại khóa ngoại mồ côi (Zero Orphan Foreign Keys).
  - [ ] Kiểm tra không trùng lặp khóa chính.
  - [ ] Kiểm tra số dòng bảng `fact_disaster_event` đạt $\ge 5.000$ dòng.
  - [ ] Kiểm tra 100% các điều kiện CHECK constraints đều thỏa mãn.
  - [ ] Kiểm tra các cột cờ nhị phân chỉ nhận giá trị 0 hoặc 1.
- [ ] Viết bộ kiểm thử tự động `tests/test_pipeline.py` để tích hợp chạy bằng `pytest`.

### D. Truy Vấn & Xuất Dữ Liệu JSON
- [ ] Viết các câu truy vấn SQL tối ưu hóa cho biểu đồ #5–#8 trong `sql/queries_for_charts.sql` (đánh dấu chú thích rõ `-- Chart #N | Thành viên 2`).
- [ ] Phát triển mô-đun xuất JSON trong `src/06_export_json.py` cho các biểu đồ của mình, đảm bảo định dạng nén nhẹ để tải trang nhanh.

---

## 4. Các Biểu Đồ Phụ Trách (#5, #6, #7, #8 trên Tableau)

### Worksheet #5: `Sheet_05_Diverging_Bar` (Biến động số vụ so với trung bình 20 năm)
- [ ] (a) Tạo Calculated Fields `[Diff from 20Yr Avg]` và `[Divergence Flag]` theo [tableau/CALCULATED_FIELDS.md](file:///c:/Users/ASUS/Documents/Tương tác dữ liệu/đồ án ck/IDV_TTDL/tableau/CALCULATED_FIELDS.md).
- [ ] (b) Kéo `[Diff from 20Yr Avg]` vào Columns, `YEAR([start_date])` vào Rows; chọn Marks: Bar.
- [ ] (c) Kéo `[Divergence Flag]` vào Color (Đỏ: Vượt trung bình, Xanh: Dưới trung bình); thêm Reference Line tại `Constant = 0`.
- [ ] (d) Ghi nhận insight từ dữ liệu thật vào `docs/CHART_SPEC.md` để đưa vào Story Point 1.

### Worksheet #6: `Sheet_06_Treemap_Damage` (Cơ cấu thiệt hại phân cấp: Châu lục $\to$ Quốc gia)
- [ ] (a) Kéo `[continent]` vào Color, `[country_name]` vào Detail; kéo `SUM([damage_usd])` vào Size.
- [ ] (b) Chọn Marks: Square (Treemap); hiển thị Label tên nước và số tiền thiệt hại.
- [ ] (c) Định dạng Tooltip hiển thị tỷ trọng % đóng góp của từng quốc gia trong châu lục.
- [ ] (d) Ghi nhận insight từ dữ liệu thật vào `docs/CHART_SPEC.md` để đưa vào Story Point 2.

### Worksheet #7: `Sheet_07_Bubble_Scatter` (Tương quan Diện tích cháy vs Thiệt hại trên trục Log-Log)
- [ ] (a) Lọc `[disaster_type] = 'Wildfire'`; kéo `[Log10 Burned Area]` vào Columns, `[Log10 Damage USD]` vào Rows.
- [ ] (b) Chọn Marks: Circle; kéo `SUM([affected])` vào Size, kéo `[continent]` vào Color.
- [ ] (c) Thêm Trend Line (đường xu hướng) dạng hàm mũ/logarit để minh họa mối tương quan.
- [ ] (d) Ghi nhận insight từ dữ liệu thật vào `docs/CHART_SPEC.md` để đưa vào Story Point 4.

### Worksheet #8: `Sheet_08_Combo_Histogram` (Phân phối quy mô diện tích cháy + Đường phân vị lũy kế)
- [ ] (a) Tạo trường phân vị `[Burned Area Bin]`; kéo `[Burned Area Bin]` vào Columns.
- [ ] (b) Trục 1: `CNT([event_id])` (Marks: Bar); Trục 2: Đường % lũy kế `RUNNING_SUM(CNT([event_id])) / TOTAL(CNT([event_id]))` (Marks: Line, Dual Axis).
- [ ] (c) Định dạng màu sắc cột cam đất, đường xanh đậm; hiển thị Tooltip số lượng vụ cháy từng khoảng.
- [ ] (d) Ghi nhận insight từ dữ liệu thật vào `docs/CHART_SPEC.md` để đưa vào Story Point 3.

---

## 5. Đầu Vào & Đầu Ra (Deliverables)
- **Đầu vào**:
  - `data/clean/master_clean.csv` từ Thành viên 1.
  - Tài liệu quy chuẩn màu sắc `docs/COLOR_GUIDE.md` và công thức tính toán `tableau/CALCULATED_FIELDS.md`.
- **Đầu ra**:
  - `docs/ERD.md` (Mermaid ERD).
  - `src/04_split_tables.py`, `src/05_build_db.py`, `src/07_validate.py`.
  - `sql/schema.sql`, `sql/load.sql`, `sql/queries_for_charts.sql`.
  - `data/tables/*.csv` và file CSDL `data/tables/database.sqlite`.
  - `tests/test_pipeline.py`.
  - 4 Worksheets Tableau (`Sheet_05` $\to$ `Sheet_08`) hoàn chỉnh.

---

## 6. Definition of Done (DoD) Cá Nhân
1. Mô hình Star Schema chuẩn hóa đạt tối thiểu 3NF, không vi phạm toàn vẹn dữ liệu.
2. File CSDL `data/tables/database.sqlite` được nạp thành công với `PRAGMA foreign_keys = ON;`.
3. Script `src/07_validate.py` và `pytest tests/` vượt qua 100% các bài kiểm tra toàn vẹn và ràng buộc.
4. Bảng fact đạt $\ge 5.000$ dòng.
5. 4 Worksheets Tableau (#5–#8) hiển thị chuẩn xác, đúng màu sắc quy định và sẵn sàng ghép vào Dashboard D1, D2, D4.
