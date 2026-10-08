# Hướng Dẫn Thực Hiện Trực Quan Hóa Trên Tableau (Quy Trình Chuẩn)

> **Dự án**: Nghiên cứu – phân tích tần suất và thiệt hại của các trận cháy rừng tại California 20 năm qua (2006–2025)  
> **Tác giả / Hiệu đính**: @DiKhang · Cập nhật ngày 08/10/2026  
> **Công cụ**: Tableau Public (Bản Web) & Tableau Desktop  
> **Dữ liệu nguồn**: 5 bảng CSV chuẩn hóa Star Schema trong thư mục `data/tables/` (7.235 vụ cháy, 114.726 bản ghi công trình DINS).

---

## 1. NẠP DỮ LIỆU & THIẾT LẬP DATA SOURCE RELATIONSHIP

1. Mở **Tableau Public** hoặc **Tableau Desktop**.
2. Chọn **Text file** $\to$ Chọn file trung tâm: `data/tables/fact_fire_incident.csv`.
3. Kéo 4 bảng Dimension và Fact chi tiết thả vào Canvas để tạo liên kết hình sao (Relationship Model):
   * `fact_fire_incident` ↔ `dim_date`: `date_id` = `date_id`
   * `fact_fire_incident` ↔ `dim_cause`: `cause_id` = `cause_id`
   * `fact_fire_incident` ↔ `dim_county`: `county_id` = `county_id`
   * `fact_fire_incident` ↔ `fact_structure_damage`: `incident_id` = `incident_id`
4. *Lưu ý*: **Không nối `fact_structure_damage` với `dim_county`**, do mã Hạt giữa hai bảng fact bị lệch nhau ở 12% số dòng kiểm định.

---

## 2. QUY HOẠCH 10 WORKSHEETS & 4 THẺ KPI CHUẨN

Hệ thống gồm đúng **10 Worksheets** (8 biểu đồ cơ bản + 2 biểu đồ nâng cao/kết hợp) và **4 thẻ KPI** hỗ trợ:

### 👤 Thành viên 1: Sheet 01 – 03 (Vĩ Mô & Không Gian Địa Lý)
* **Sheet 1**: `01_Line_Season` (Line Chart 2 đường: Mùa cháy theo tháng, so sánh 2 thập kỷ 2006–2015 vs 2016–2025. 80% vụ rơi vào T6–T10; đầu mùa và cuối mùa tăng tới ~70%).
* **Sheet 2**: `02_Area_Cause_Trend` (Stacked Area Chart: Biến thiên cơ cấu 3 nhóm nguyên nhân qua 20 năm. Con người đỏ, Tự nhiên xanh, Chưa xác định xám).
* **Sheet 3**: `03_Map_County` (Bản đồ 2 lớp: Layer 1 Map phân vùng theo Mật độ cháy; Layer 2 Circle theo Diện tích cháy; định vị chuẩn bang California).

### 👤 Thành viên 2: Sheet 04 – 07 (Căn Nguyên & Thiệt Hại Chi Tiết)
* **Sheet 4**: `04_Donut_Cause_Share` (Donut Chart: Tỷ trọng 7.235 vụ cháy theo nhóm nguyên nhân; Con người 36,4%, Tự nhiên 20,9%, Chưa xác định 42,7%).
* **Sheet 5**: `05_Bar_Top_Counties` (Horizontal Bar Chart + Parameter Top N: Xếp hạng các Hạt mất nhiều công trình nhất; Butte 23.834, Los Angeles 19.066...).
* **Sheet 6**: `06_Heatmap_Cause_Size` (Heatmap ma trận: Nhóm nguyên nhân $\times$ Quy mô đám cháy; tính % theo hàng Table across).
* **Sheet 7**: `07_Treemap_Damage` (Treemap 1 tầng: Phân bổ công trình bị phá hủy theo loại nhà và Top 8 Hạt; Nhà 1 hộ Single Family chiếm ưu thế).

### 👤 Thành viên 3: Sheet 08 – 10 & 4 Thẻ KPI (Dự Báo, Phân Tích Nâng Cao & Story)
* **Sheet 8**: `08_Scatter_Regression` (Scatter Plot + Hồi quy log-log: Mô hình $\log_{10}(Y) = 0{,}433436 \times \log_{10}(X) - 0{,}377417$, $R^2 = 0{,}356$, $p < 0{,}0001$. Đạt chuẩn Barem Dự báo).
* **Sheet 9**: `09_Pareto_Damage` (Pareto Dual-Axis: 7 Hạt chịu 82% tổng số công trình bị phá hủy toàn bang; Reference Line mốc 80%).
* **Sheet 10**: `10_Diverging_vs_Avg` (Diverging Bar quanh 0: Số vụ cháy từng năm so với trung bình 20 năm = 362 vụ/năm; năm 2017 vượt đỉnh +243 vụ).
* **Hệ thống 4 KPI**: `KPI_1_So_vu` (7.235 vụ), `KPI_2_Dien_tich` (19,39M mẫu), `KPI_3_Pha_huy` (73.818 công trình), `KPI_4_Tu_vong` (255 người).

---

## 3. THIẾT KẾ 3 DASHBOARDS CHUYÊN ĐỀ (1366 $\times$ 768 px)

1. **Dashboard D1: Bức Tranh 20 Năm & Mùa Vụ Cháy Rừng**
   * **Thành phần**: 4 Thẻ KPI trên cùng + `01_Line_Season` + `02_Area_Cause_Trend` + `10_Diverging_vs_Avg`.
   * **Tương tác**: Filter theo giai đoạn thập kỷ hoặc năm.

2. **Dashboard D2: Không Gian Địa Lý & Quy Luật Thiệt Hại Pareto 80/20**
   * **Thành phần**: `03_Map_County` (Bản đồ 2 lớp) + `09_Pareto_Damage` (Combo Pareto) + `05_Bar_Top_Counties` + `07_Treemap_Damage`.
   * **Tương tác**: Click chọn Hạt trên Bản đồ $\to$ Lọc chi tiết thiệt hại loại nhà tương ứng.

3. **Dashboard D3: Căn Nguyên Bùng Phát & Mô Hình Hồi Quy Dự Báo**
   * **Thành phần**: `04_Donut_Cause_Share` + `06_Heatmap_Cause_Size` + `08_Scatter_Regression` (kèm đường xu thế log-log và dải tin cậy 95%).
   * **Tương tác**: Highlight nhóm nguyên nhân giữa Donut, Heatmap và Scatter.

---

## 4. XÂY DỰNG TABLEAU STORY (3 STORY POINTS)

1. **Story Point 1: Biến Động Chu Kỳ 20 Năm & Xu Thế Mùa Cháy Kéo Dài**
   * Nhúng **Dashboard D1**. Nêu bật phát hiện: Mùa cháy T6–T10 chiếm 80% vụ, các tháng đầu mùa và cuối mùa tăng vọt ~70% trong thập kỷ gần đây.
2. **Story Point 2: Tâm Chấn Thảm Họa Địa Lý & Quy Luật Bất Cân Xứng Pareto**
   * Nhúng **Dashboard D2**. Nhấn mạnh quy luật 80/20: Chỉ 7 Hạt đã gánh chịu 82% tổng số nhà cửa bị thiêu rụi toàn bang, dẫn đầu là Butte và Los Angeles.
3. **Story Point 3: Nghịch Lý Căn Nguyên & Khả Năng Dự Báo Thiệt Hại**
   * Nhúng **Dashboard D3**. Minh họa mô hình hồi quy log-log ($R^2 = 0{,}356$): Diện tích tăng 10 lần thì thiệt hại tăng ~2,7 lần; hoạt động con người gần khu dân cư là nguyên nhân chính gây mất mát tài sản.
