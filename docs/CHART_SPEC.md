# Đặc Tả 10 Biểu Đồ & Tableau Story Tinh Gọn (CHART SPECIFICATIONS)

> **Phạm vi nghiên cứu**: Cháy rừng Bang California giai đoạn 2006–2025 (CAL FIRE FRAP, DINS, Census & NOAA)  
> **Cấu trúc phân chia**: 10 Biểu đồ tinh gọn, không rối mắt: **8 Biểu đồ cơ bản + 1 Biểu đồ kết hợp dự báo 10 năm (2026–2035) + 1 Bản đồ địa lý bắt buộc (Map)**.  
> **Cam kết Barem đề thi**:
> - Đảm bảo **9 loại biểu đồ hoàn toàn khác biệt** (Vượt chuẩn tối thiểu 8 loại của môn học):
>   1. *Line Chart (Đường đơn trục)*
>   2. *Combo Dual-Axis Chart (Cột + Đường + Trend Line dự báo 10 năm 2026–2035)*
>   3. *Diverging Bar Chart (Cột phân kỳ quanh tâm 0)*
>   4. *Heatmap / Highlight Table (Bản đồ nhiệt 12 Tháng x 20 Năm)*
>   5. *Pie Chart (Biểu đồ tròn 3 múi tỷ trọng nguyên nhân)*
>   6. *Scatter Plot (Phân tán tương quan 58 Hạt — Không bị đè chấm rối mắt)*
>   7. *Treemap (Cơ cấu loại công trình bị phá hủy)*
>   8. *Horizontal Bar Chart (Cột ngang xếp hạng Top 10 Hạt)*
>   9. *Geographic Choropleth Map (Bản đồ phân vùng 58 Hạt California bắt buộc)*
>   10. *Stacked Area Chart (Miền xếp chồng biến thiên theo thời gian)*
> - **Tích hợp mô hình dự báo**: Thể hiện trực quan đường Hồi quy tuyến tính Forward 10 năm (2026–2035) đạt trọn vẹn 0.5 điểm Barem.

---

## 1. CẤU TRÚC 3 DASHBOARDS CHUYÊN ĐỀ TINH GỌN (Kích Thước 1366 x 768 px)

| Dashboard | Chủ đề & Câu hỏi phân tích | Biểu đồ tích hợp | Mục tiêu phân tích |
|---|---|---|---|
| **D1 – Bức tranh 20 năm & Dự báo tương lai** | Tần suất và diện tích cháy biến động ra sao qua 20 năm? Dự báo 10 năm tới (2026–2035) diễn biến thế nào? | • #1 `Sheet_01_Line_Yearly_Trend`<br>• #2 `Sheet_02_Combo_Forecast`<br>• #3 `Sheet_03_Divergence_Bar` | Phân tích xu hướng dài hạn, năm dị thường vượt chuẩn và đường xu thế hồi quy dự báo 10 năm tới. |
| **D2 – Không gian địa lý & Phân cấp thiệt hại 58 Hạt** | Hạt nào chịu thiệt hại nặng nhất? Cấu trúc nhà cửa bị san phẳng gồm những loại công trình nào? | • #7 `Sheet_07_Treemap_Damage`<br>• #8 `Sheet_08_Top10_Counties_Bar`<br>• #9 `Sheet_09_Choropleth_Map` | Nhận diện điểm nóng địa lý 58 Hạt, xếp hạng Top 10 và cơ cấu nhà ở dân sinh (Single Family) bị phá hủy. |
| **D3 – Mùa vụ, Căn nguyên & Đánh giá rủi ro** | Cháy rừng bùng phát mạnh vào tháng nào? Nguyên nhân do con người hay tự nhiên? Tương quan rủi ro giữa các Hạt? | • #4 `Sheet_04_Monthly_Heatmap`<br>• #5 `Sheet_05_Pie_Cause_Share`<br>• #6 `Sheet_06_Scatter_County_Risk`<br>• #10 `Sheet_10_Stacked_Area_Cause` | Đào sâu ma trận nhiệt 12 Tháng x 20 Năm, tỷ trọng căn nguyên và phân tán tương quan 58 Hạt. |

---

## 2. ĐẶC TẢ TABLEAU STORY (3 STORY POINTS TRỌNG TÂM)

### 📍 Story Point 1: "1. Bức tranh 20 năm Cháy rừng California & Dự báo 2026–2035"
- **Nội dung nhúng**: Dashboard **D1**.
- **Thông điệp cốt lõi**: Trong 20 năm (2006–2025), tần suất cháy rừng tăng vọt sau các chu kỳ hạn hán. Đỉnh điểm năm 2020 thiêu rụi kỷ lục hơn 4.3 triệu Acres.
- **Chú thích (Annotation)**: Gắn Annotation tại mốc năm 2035 trên đường Trend Line: *"Mô hình Hồi quy tuyến tính (y = 32.967 * Year - 65.475.936) dự báo diện tích cháy rừng California tiếp tục gia tăng bình quân ~33.000 mẫu/năm và vượt mốc 1.61 triệu mẫu vào năm 2035 (Độ tin cậy 95%)."*

### 📍 Story Point 2: "2. Không gian địa lý & Điểm nóng thiệt hại 58 Hạt"
- **Nội dung nhúng**: Dashboard **D2**.
- **Thông điệp cốt lõi**: Thiệt hại tập trung cao độ tại các Hạt bìa rừng đô thị phía Bắc California.
- **Chú thích (Annotation)**: Gắn Annotation tại Hạt Butte: *"Chỉ riêng Hạt Butte đã ghi nhận gần 24.000 công trình bị san phẳng (thảm họa Camp Fire), trong đó Single Family Residence chiếm hơn 80% tổng thiệt hại."*

### 📍 Story Point 3: "3. Mùa vụ khốc liệt & Nghịch lý căn nguyên cháy"
- **Nội dung nhúng**: Dashboard **D3**.
- **Thông điệp cốt lõi**: Mùa cháy đỏ rực tập trung từ tháng 7 đến tháng 10. Hoạt động con người gây ra hơn 85% thiệt hại nhà cửa và thương vong.
- **Chú thích (Annotation)**: Gắn Annotation trên Heatmap và Pie Chart: *"Nghịch lý căn nguyên: Sét đánh gây cháy rộng ở vùng hoang dã, nhưng con người (chiếm trên 36% số vụ gần khu dân cư) lại là tác nhân hủy diệt tài sản và nhân mạng lớn nhất."*

---

## 3. BẢNG TỔNG HỢP 10 BIỂU ĐỒ TABLEAU CHI TIẾT

| # | Tên Sheet | Loại Biểu Đồ | Bảng Dữ Liệu Nguồn | Người Phụ Trách |
|---|---|---|---|---|
| **1** | `Sheet_01_Line_Yearly_Trend` | Line Chart (Đường đơn) | `dim_date`, `fact_fire_incident` | Thành viên 1 |
| **2** | `Sheet_02_Combo_Forecast` | Combo Dual-Axis (+ Forecast 10 năm) | `dim_date`, `fact_fire_incident` | Thành viên 1 |
| **3** | `Sheet_03_Divergence_Bar` | Diverging Bar quanh 0 | `dim_date`, `fact_fire_incident` | Thành viên 2 |
| **4** | `Sheet_04_Monthly_Heatmap` | Heatmap (12 Tháng x 20 Năm) | `dim_date`, `fact_fire_incident` | Thành viên 2 |
| **5** | `Sheet_05_Pie_Cause_Share` | Pie Chart 3 múi nguyên nhân | `dim_cause`, `fact_fire_incident` | Thành viên 2 |
| **6** | `Sheet_06_Scatter_County_Risk` | Scatter Plot (58 Hạt) | `dim_county`, `fact_fire_incident` | Thành viên 2 |
| **7** | `Sheet_07_Treemap_Damage` | Treemap 1 tầng loại nhà | `fact_structure_damage` | Thành viên 3 |
| **8** | `Sheet_08_Top10_Counties_Bar` | Horizontal Bar Chart | `dim_county`, `fact_fire_incident` | Thành viên 3 |
| **9** | `Sheet_09_Choropleth_Map` | Geographic Map (58 Hạt) | `dim_county`, `fact_fire_incident` | Thành viên 3 |
| **10**| `Sheet_10_Stacked_Area_Cause` | Stacked Area Chart | `dim_date`, `dim_cause`, `fact_fire_incident` | Thành viên 3 |

---

## 4. CHI TIẾT KỸ THUẬT KÉO THẢ TỪNG SHEET

### Sheet 01: Line Chart Tần Suất Cháy (Sheet_01_Line_Yearly_Trend)
- **Columns**: `[dim_date].[year]` (Discrete).
- **Rows**: `[Fire Incidents Count]`.
- **Marks**: Line (Màu xanh `#0072B2`, bật Markers tròn tại từng điểm năm).

### Sheet 02: Combo Dual-Axis & Hồi Quy Dự Báo 10 Năm (Sheet_02_Combo_Forecast)
- **Columns**: `[dim_date].[year]` (Discrete).
- **Rows**: Trục 1: `[Fire Incidents Count]` (Bar, màu xanh `#4A90E2`); Trục 2: `SUM([acres_burned])` (Line, màu cam `#D55E00`, Dual Axis).
- **Trend Line Forecast**: Tab Analytics $\to$ Kéo Trend Line vào `SUM(acres_burned)` $\to$ Linear $\to$ Edit Trend Line $\to$ Forward: `10` periods (2026–2035) $\to$ Bật *Show Confidence Bands* (95%).

### Sheet 03: Biến Động So Với Mức Trung Bình 20 Năm (Sheet_03_Divergence_Bar)
- **Columns**: `[Diff from 20Yr Avg]` (Compute using `year`).
- **Rows**: `[dim_date].[year]`.
- **Marks**: Bar. Color: `[Divergence Flag]` (Vượt: Đỏ cam `#D55E00`, Dưới: Xanh `#0072B2`). Reference Line: Constant = 0.

### Sheet 04: Bản Đồ Nhiệt Ma Trận Mùa Vụ (Sheet_04_Monthly_Heatmap)
- **Columns**: `[dim_date].[month]` (Discrete: 1 đến 12).
- **Rows**: `[dim_date].[year]` (Discrete: 2006 đến 2025).
- **Marks**: Square. Color: `[Fire Incidents Count]` (Dải màu Orange-Red). Label: `[Fire Incidents Count]`.

### Sheet 05: Cơ Cấu Nguồn Gốc Gây Cháy (Sheet_05_Pie_Cause_Share)
- **Marks**: Pie. Color: `[dim_cause].[cause_group]` (Human: Cam, Natural: Xanh, Undetermined: Xám).
- **Angle**: `[Fire Incidents Count]`. Label: `cause_group` và Quick Table Calculation *Percent of Total*.

### Sheet 06: Tương Quan Rủi Ro 58 Hạt (Sheet_06_Scatter_County_Risk)
- **Columns**: `SUM([fact_fire_incident].[acres_burned])`.
- **Rows**: `SUM([fact_fire_incident].[total_structures_destroyed])`.
- **Detail**: `[dim_county].[county_name]` (CHỈ 58 ĐIỂM HẠT, không bị đè chấm).
- **Size**: `AVG([dim_county].[census_population])`. Label: `county_name`.

### Sheet 07: Cơ Cấu Loại Nhà Cửa Bị Phá Hủy (Sheet_07_Treemap_Damage)
- **Marks**: Square. Detail: `[fact_structure_damage].[structure_type]`.
- **Size & Color**: `SUM([fact_structure_damage].[structures_destroyed])`.
- **Label**: `structure_type` và số lượng bị phá hủy (Single Family chiếm >80%).

### Sheet 08: Xếp Hạng Top 10 Hạt Thiệt Hại Nặng Nhất (Sheet_08_Top10_Counties_Bar)
- **Columns**: `SUM([fact_fire_incident].[total_structures_destroyed])`.
- **Rows**: `[dim_county].[county_name]` (Top 10 Filter by destroyed Sum, Sort Descending).
- **Marks**: Bar (Đỏ gạch `#B22222`). Label: Hiển thị số lượng ở đầu cột.

### Sheet 09: Bản Đồ Phân Vùng 58 Hạt California (Sheet_09_Choropleth_Map)
- **Columns**: `Longitude (generated)`. Rows: `Latitude (generated)`.
- **Marks**: Map. Detail: `[dim_county].[county_name]` (Geographic Role: County, State: California).
- **Color**: `SUM([total_structures_destroyed])` (Orange-Red, viền trắng mảnh).

### Sheet 10: Cơ Cấu Nguyên Nhân Biến Thiên Theo Thời Gian (Sheet_10_Stacked_Area_Cause)
- **Columns**: `[dim_date].[year]` (Continuous).
- **Rows**: `[Fire Incidents Count]`.
- **Marks**: Area. Color: `[dim_cause].[cause_group]` (Opacity = 80%).
