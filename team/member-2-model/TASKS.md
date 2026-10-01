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
    - [ ] `year BETWEEN 2006 AND 2025`
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

## 4. Các Biểu Đồ Phụ Trách (#5, #6, #7, #8)

### Biểu Đồ #5: Diverging Bar Chart (Biến động số vụ so với trung bình 20 năm)
- [ ] (a) Viết truy vấn SQL tính độ lệch so với trung bình 20 năm trong `sql/queries_for_charts.sql`.
- [ ] (b) Xuất file JSON `dashboard/data/chart_05_data.json`.
- [ ] (c) Dựng biểu đồ cột phân kỳ ECharts trong `dashboard/js/charts/chart-05.js` với bảng màu RdBu (tâm = 0).
- [ ] (d) Gắn tương tác hover tooltip hiển thị số liệu tuyệt đối và % chênh lệch.
- [ ] (e) Hoàn thiện mục Biểu đồ 5 trong `docs/CHART_SPEC.md` và ghi nhận insight từ dữ liệu thật.

### Biểu Đồ #6: Treemap Thiệt Hại Phân Cấp (Châu lục $\to$ Quốc gia)
- [ ] (a) Viết truy vấn SQL gom nhóm thiệt hại 2 cấp (Châu lục $\to$ Quốc gia).
- [ ] (b) Xuất file JSON dạng cây phân cấp `dashboard/data/chart_06_data.json`.
- [ ] (c) Dựng biểu đồ Treemap ECharts trong `dashboard/js/charts/chart-06.js` với phân màu theo châu lục.
- [ ] (d) Gắn tương tác click drill-down xem sâu vào từng quốc gia và breadcrumb điều hướng.
- [ ] (e) Hoàn thiện mục Biểu đồ 6 trong `docs/CHART_SPEC.md` và ghi nhận insight từ dữ liệu thật.

### Biểu Đồ #7: Bubble Scatter (Diện tích cháy vs Thiệt hại USD trên trục Log-Log)
- [ ] (a) Viết truy vấn SQL trích xuất bộ ba chỉ số: Diện tích, Thiệt hại, Số người ảnh hưởng và Châu lục.
- [ ] (b) Xuất file JSON `dashboard/data/chart_07_data.json`.
- [ ] (c) Dựng biểu đồ bong bóng ECharts trong `dashboard/js/charts/chart-07.js` với hệ trục tọa độ Logarit và màu theo Châu lục.
- [ ] (d) Gắn tương tác brush chọn vùng để đồng bộ lọc chéo toàn bộ dashboard.
- [ ] (e) Hoàn thiện mục Biểu đồ 7 trong `docs/CHART_SPEC.md` và ghi nhận insight từ dữ liệu thật.

### Biểu Đồ #8: Combo Histogram Diện tích cháy + Đường Mật độ KDE / Lũy kế
- [ ] (a) Viết truy vấn SQL chia khoảng bin logarit cho diện tích cháy và đếm tần suất.
- [ ] (b) Xuất file JSON `dashboard/data/chart_08_data.json`.
- [ ] (c) Dựng biểu đồ kết hợp ECharts trong `dashboard/js/charts/chart-08.js` với cột cam đất và đường phân vị xanh sẫm.
- [ ] (d) Gắn tương tác hover xem khoảng bin và số lượng vụ; nút chuyển đổi tích lũy.
- [ ] (e) Hoàn thiện mục Biểu đồ 8 trong `docs/CHART_SPEC.md` và ghi nhận insight từ dữ liệu thật.

---

## 5. Đầu Vào & Đầu Ra (Deliverables)
- **Đầu vào**:
  - `data/clean/master_clean.csv` từ Thành viên 1.
  - Tài liệu quy chuẩn màu sắc `docs/COLOR_GUIDE.md`.
- **Đầu ra**:
  - `docs/ERD.md` (Mermaid ERD).
  - `src/04_split_tables.py`, `src/05_build_db.py`, `src/07_validate.py`.
  - `sql/schema.sql`, `sql/load.sql`, `sql/queries_for_charts.sql` (phần biểu đồ #5–#8).
  - `data/tables/*.csv` và file CSDL `data/tables/database.sqlite`.
  - `tests/test_pipeline.py`.
  - `dashboard/js/charts/chart-05.js`, `chart-06.js`, `chart-07.js`, `chart-08.js`.

---

## 6. Definition of Done (DoD) Cá Nhân
1. Mô hình Star Schema chuẩn hóa đạt tối thiểu 3NF, không vi phạm toàn vẹn dữ liệu.
2. File CSDL `data/tables/database.sqlite` được nạp thành công với `PRAGMA foreign_keys = ON;`.
3. Script `src/07_validate.py` và `pytest tests/` vượt qua 100% các bài kiểm tra toàn vẹn và ràng buộc.
4. Bảng fact đạt $\ge 5.000$ dòng.
5. 4 biểu đồ (#5–#8) hoạt động ổn định trên Dashboard, hiển thị chuẩn xác và đúng quy chuẩn thị giác.
