# Đặc Tả 10 Biểu Đồ & Tableau Story (CHART SPECIFICATIONS)

> **Nhóm thực hiện**: Phân chia tối ưu công việc **2 / 4 / 4**:
> - **Thành viên 1 (Data & ML)**: 2 biểu đồ (`Sheet_01`, `Sheet_02`) — Giảm tải để tập trung toàn lực vào Crawl/Làm sạch dữ liệu và Mô hình dự báo Linear/Logistic.
> - **Thành viên 2 (Modeling & SQL)**: 4 biểu đồ (`Sheet_03`, `Sheet_04`, `Sheet_05`, `Sheet_06`).
> - **Thành viên 3 (Dashboard & Story)**: 4 biểu đồ (`Sheet_07`, `Sheet_08`, `Sheet_09`, `Sheet_10`).
>
> **Cam kết Barem đề thi**:
> - Tổng cộng **10 biểu đồ**, trong đó có **9 loại biểu đồ hoàn toàn khác nhau** (vượt chuẩn tối thiểu 8 loại của môn học):
>   1. *Dual-Axis Combo Bar + Line*
>   2. *Stacked Area Chart*
>   3. *Diverging Bar Chart*
>   4. *Treemap Chart*
>   5. *Bubble / Scatter Plot (Log-Log)*
>   6. *Combo Histogram + Cumulative Line*
>   7. *Combo Pareto Chart (80/20)*
>   8. *Donut / Sunburst Chart*
>   9. *Bản đồ địa lý bắt buộc (Map)*: Gồm cả *Choropleth Map* và *Proportional Symbol Map*.
> - **Tương thích tự động với dữ liệu mới**: Tất cả công thức và trường dữ liệu đều được thiết kế tổng quát theo Data Dictionary chuẩn. Khi Thành viên 1 crawl/bổ sung dữ liệu mới vào `data/raw/` $\to$ chạy pipeline làm sạch $\to$ Tableau chỉ cần bấm **Refresh Data Source** là 10 biểu đồ, 3 Dashboard và Story Points sẽ tự động cập nhật chính xác 100%.

---

## 1. CẤU TRÚC 3 DASHBOARD CHUYÊN ĐỀ (Mỗi Dashboard 3–4 Biểu Đồ)

Mười biểu đồ được tích hợp thành 3 Dashboards chuyên đề chặt chẽ, tạo thành mạch dẫn dắt câu chuyện phân tích logic:

| Dashboard | Chủ đề & Câu hỏi phân tích | Biểu đồ trong dashboard | Mục tiêu phân tích |
|---|---|---|---|
| **D1 – Bức tranh 20 năm** (Xu hướng vĩ mô) | Thảm họa thiên nhiên và cháy rừng có gia tăng theo thời gian không? Mức độ biến động ra sao? | • #1 `Combo_Trend` (TV1)<br>• #2 `Stacked_Area` (TV1)<br>• #3 `Diverging_Bar` (TV2) | Phân tích xu hướng dài hạn 2006–2025, cơ cấu thảm họa và độ lệch so với mức chuẩn 20 năm. |
| **D2 – Điểm nóng & Phân cấp thiệt hại** (Không gian & 80/20) | Khu vực nào chịu tổn thất nặng nề nhất? Tổn thất có tập trung theo nguyên lý 80/20 không? | • #4 `Treemap_Damage` (TV2)<br>• #7 `Combo_Pareto` (TV3)<br>• #9 `Choropleth_Map` (TV3) | Nhận diện bất bình đẳng địa lý và mức độ tập trung thiệt hại sinh mạng/kinh tế theo quốc gia. |
| **D3 – Cháy rừng: Mùa vụ, Quy mô & Tác nhân** (Chi tiết chuyên sâu) | Cháy rừng bùng phát mạnh khi nào, quy mô diện tích ra sao, căn nguyên tự nhiên hay con người? | • #5 `Bubble_Scatter` (TV2)<br>• #6 `Combo_Histogram` (TV2)<br>• #8 `Donut_Cause` (TV3)<br>• #10 `Proportional_Map` (TV3) | Đào sâu vào phân phối diện tích đám cháy, căn nguyên kích hoạt và vị trí không gian các vụ đại thảm họa. |

---

## 2. ĐẶC TẢ TABLEAU STORY (Tableau Story với 3 Story Points Trọng Tâm)

Cấu trúc Story Point dẫn dắt mạch lạc theo đúng barem yêu cầu (ít nhất 3 Story Points):

```
┌────────────────────────────────────────────────────────┐
│ [Point 1: Bức tranh 20 năm & Biến động xu thế]        │
│                           │                            │
│                           ▼                            │
│ [Point 2: Điểm nóng toàn cầu & Quy luật 80/20]        │
│                           │                            │
│                           ▼                            │
│ [Point 3: Trọng tâm Cháy rừng & Dự báo rủi ro tương lai]│
└────────────────────────────────────────────────────────┘
```

### 📍 Story Point 1: "Thảm họa 20 năm: Tần suất & Tổn thất có đang gia tăng?"
- **Nội dung nhúng**: Dashboard **D1 – Bức tranh 20 năm**.
- **Tiêu đề thanh dẫn**: `1. Bức tranh 20 năm`
- **Thông điệp cốt lõi**: Thiệt hại kinh tế và tần suất thảm họa có xu hướng gia tăng rõ rệt trong thập niên gần đây. Đỉnh kỷ lục năm 2020 ghi nhận thiệt hại tài chính vượt xa mức trung bình 20 năm.
- **Chú thích (Annotation)**: Gắn mũi tên ghi chú tại cột mốc năm 2020 và đường xu hướng dự báo Hồi quy tuyến tính: *"Tác động kép của cháy rừng khốc liệt đẩy thiệt hại năm 2020 lên đỉnh điểm."*

### 📍 Story Point 2: "Điểm nóng toàn cầu: Nơi gánh chịu hậu quả nặng nề nhất"
- **Nội dung nhúng**: Dashboard **D2 – Điểm nóng & Phân cấp thiệt hại**.
- **Tiêu đề thanh dẫn**: `2. Điểm nóng toàn cầu`
- **Thông điệp cốt lõi**: Thiệt hại phân bổ bất đối xứng sâu sắc theo nguyên lý Pareto 80/20: Dưới 20% số quốc gia (chủ yếu tại Châu Á và Châu Mỹ) gánh chịu hơn 80% tổng số sinh mạng thương vong và thiệt hại vật chất.
- **Chú thích (Annotation)**: Gắn Reference Line 80% trên biểu đồ Pareto và làm nổi bật top quốc gia trên bản đồ thế giới.

### 📍 Story Point 3: "Trọng tâm Cháy rừng: Quy mô, Căn nguyên & Dự báo tương lai"
- **Nội dung nhúng**: Dashboard **D3 – Cháy rừng: Mùa vụ, Quy mô & Tác nhân**.
- **Tiêu đề thanh dẫn**: `3. Trọng tâm Cháy rừng`
- **Thông điệp cốt lõi**: Dù các siêu đám cháy ($\ge 10.000$ ha) chỉ chiếm thiểu số về số vụ, chúng tàn phá phần lớn diện tích rừng. Hoạt động bất cẩn của con người là tác nhân hàng đầu, và mô hình dự báo cho thấy nguy cơ ngày càng mở rộng diện tích nếu không có can thiệp sớm.
- **Chú thích (Annotation)**: Đánh dấu các cụm siêu đám cháy trên bản đồ điểm Proportional Symbol Map và biểu đồ tán xạ Bubble Scatter.

---

## 3. DANH MỤC PHÂN CHIA 10 BIỂU ĐỒ TABLEAU (2 / 4 / 4)

| # | Tên Sheet trong Tableau | Dashboard | Loại Biểu Đồ (Đảm bảo đa dạng) | Bảng Màu Quy Định | Người Phụ Trách |
|---|---|---|---|---|---|
| **1** | `Sheet_01_Combo_Trend` | D1 | **Combo Chart** (Dual-Axis Bar + Line) | Cột xanh dương `#4A90E2`, Đường cam `#D55E00` | **TV1 (1/2)** |
| **2** | `Sheet_02_Stacked_Area` | D1 | **Stacked Area Chart** (Cơ cấu theo thời gian) | Bảng màu `Color Blind` (Okabe-Ito) | **TV1 (2/2)** |
| **3** | `Sheet_03_Diverging_Bar` | D1 | **Diverging Bar Chart** (Độ lệch so với trung bình) | Dải phân kỳ `Red-Blue Diverging` (Tâm = 0) | **TV2 (1/4)** |
| **4** | `Sheet_04_Treemap_Damage` | D2 | **Treemap Chart** (Phân cấp Châu lục $\to$ Quốc gia) | Phân màu theo Châu lục | **TV2 (2/4)** |
| **5** | `Sheet_05_Bubble_Scatter` | D3 | **Bubble Scatter Plot** (Trục Log-Log + Kích cỡ) | Categorical theo Châu lục | **TV2 (3/4)** |
| **6** | `Sheet_06_Combo_Histogram` | D3 | **Combo Histogram** (Cột tần suất + Đường lũy kế) | Đơn sắc Cam đất + Đường xanh | **TV2 (4/4)** |
| **7** | `Sheet_07_Combo_Pareto` | D2 | **Pareto Chart** (Cột xếp hạng + Đường 80/20) | Cột đỏ mận + Đường cam nhấn | **TV3 (1/4)** |
| **8** | `Sheet_08_Donut_Cause` | D3 | **Donut / Sunburst Chart** (Tác nhân 2 tầng) | Xanh (Tự nhiên) / Đỏ cam (Con người) | **TV3 (2/4)** |
| **9** | `Sheet_09_Choropleth_Map` | D2 | **Bản Đồ Phân Vùng** (Choropleth Map thế giới) | Dải tuần tự `Orange-Red` | **TV3 (3/4)** |
| **10**| `Sheet_10_Proportional_Map`| D3 | **Bản Đồ Điểm** (Proportional Symbol Map) | Kích cỡ = Diện tích, Màu = Thiệt hại | **TV3 (4/4)** |

---

## 4. CHI TIẾT KỸ THUẬT KÉO THẢ TỪNG SHEET TRONG TABLEAU

### Sheet 01: Tần Suất & Tổng Thiệt Hại Theo Năm (Dual-Axis Combo)
- **Người phụ trách**: Thành viên 1
- **Columns**: `YEAR([start_date])` (Discrete / Dimension).
- **Rows**: 
  - Trục 1: `CNT([event_id])` $\to$ Marks: **Bar** (Cột màu xanh `#4A90E2`).
  - Trục 2: `SUM([Damage Bil USD])` $\to$ Marks: **Line** (Đường màu cam `#D55E00`).
- **Thao tác Dual Axis**: Chuột phải vào trục thứ 2 $\to$ chọn **Dual Axis** $\to$ bỏ đồng bộ trục (hoặc giữ 2 thang đo độc lập vì đơn vị khác nhau: Số vụ vs Tỷ USD).
- **Tooltip**: Hiển thị rõ số vụ và số tiền thiệt hại quy đổi.

---

### Sheet 02: Diễn Biến Cơ Cấu Thảm Họa Theo Thời Gian (Stacked Area)
- **Người phụ trách**: Thành viên 1
- **Columns**: `YEAR([start_date])` (Continuous / Date).
- **Rows**: `CNT([event_id])`.
- **Marks Card**: Chọn kiểu **Area**.
- **Color**: Kéo trường `[disaster_type]` vào **Color**.
- **Sắp xếp**: Đặt `Wildfire` ở dưới cùng để theo dõi rõ nét nhất.

---

### Sheet 03: Bản Đồ Thiệt Hại & Số Vụ Toàn Cầu (Choropleth Map)
- **Người phụ trách**: Thành viên 1
- **Columns**: `[Longitude]` (Generated).
- **Rows**: `[Latitude]` (Generated).
- **Marks Card**: Chọn kiểu **Map**.
- **Detail**: Kéo `[iso3]` hoặc `[country_name]` vào **Detail**.
- **Color**: Kéo `SUM([Damage Bil USD])` vào **Color** $\to$ Chọn dải màu `Orange-Red`.
- **Tooltip**: Tên quốc gia, số vụ thảm họa, tổng thiệt hại tài chính.

---

### Sheet 04: Ma Trận Chu Kỳ Mùa Vụ Cháy Rừng (Heatmap Tháng $\times$ Năm)
- **Người phụ trách**: Thành viên 1
- **Bộ lọc (Filters)**: `[disaster_type] = 'Wildfire'`.
- **Columns**: `MONTH([start_date])` (Discrete 1..12).
- **Rows**: `YEAR([start_date])` (Discrete 2005..2024).
- **Marks Card**: Chọn kiểu **Square**.
- **Color**: Kéo `CNT([event_id])` vào **Color** $\to$ Chọn dải màu `YlOrRd`.

---

### Sheet 02: Diễn Biến Cơ Cấu Thảm Họa Theo Thời Gian (Stacked Area)
- **Người phụ trách**: **Thành viên 1 (2/2)** (Dashboard D1)
- **Columns**: `YEAR([start_date])` (Continuous / Date).
- **Rows**: `CNT([event_id])`.
- **Marks Card**: Chọn kiểu **Area**.
- **Color**: Kéo trường `[disaster_type]` vào **Color**.
- **Sắp xếp**: Đặt `Wildfire` ở dưới cùng để theo dõi rõ nét nhất.

---

### Sheet 03: Biến Động Số Vụ So Với Trung Bình 20 Năm (Diverging Bar)
- **Người phụ trách**: **Thành viên 2 (1/4)** (Dashboard D1)
- **Columns**: `[Diff from 20Yr Avg]` (Calculated Field CF7).
- **Rows**: `YEAR([start_date])` (Discrete).
- **Marks Card**: Chọn kiểu **Bar**.
- **Color**: Kéo `[Divergence Flag]` (Calculated Field CF8) vào **Color** (Vượt trung bình: Đỏ, Dưới trung bình: Xanh lam).
- **Reference Line**: Thêm đường tham chiếu cố định tại `Constant = 0`.

---

### Sheet 04: Cơ Cấu Thiệt Hại Phân Cấp: Châu Lục $\to$ Quốc Gia (Treemap)
- **Người phụ trách**: **Thành viên 2 (2/4)** (Dashboard D2)
- **Marks Card**: Chọn kiểu **Square** (Treemap trong Show Me).
- **Color**: Kéo `[continent]` vào **Color**.
- **Detail**: Kéo `[country_name]` vào **Detail**.
- **Size**: Kéo `SUM([damage_usd])` vào **Size**.
- **Label**: Hiển thị tên nước và % tỷ trọng.

---

### Sheet 05: Tương Quan Diện Tích Cháy vs Thiệt Hại (Bubble Scatter Log-Log)
- **Người phụ trách**: **Thành viên 2 (3/4)** (Dashboard D3)
- **Filters**: `[disaster_type] = 'Wildfire'` AND `[burned_area_ha] > 0` AND `[damage_usd] > 0`.
- **Columns**: `[Log10 Burned Area]` (hoặc chọn trục X $\to$ Edit Axis $\to$ chọn **Logarithmic**).
- **Rows**: `[Log10 Damage USD]` (hoặc chọn trục Y $\to$ chọn **Logarithmic**).
- **Marks Card**: Chọn kiểu **Circle**.
- **Size**: Kéo `SUM([affected])` hoặc `SUM([deaths])` vào **Size**.
- **Color**: Kéo `[continent]` vào **Color**.

---

### Sheet 06: Phân Phối Quy Mô Diện Tích Cháy (Combo Histogram + Pareto Line)
- **Người phụ trách**: **Thành viên 2 (4/4)** (Dashboard D3)
- **Columns**: `[Burned Area Bin]` (Calculated Field CF11).
- **Rows**: 
  - Trục 1: `CNT([event_id])` (Marks: **Bar**).
  - Trục 2: `RUNNING_SUM(CNT([event_id])) / TOTAL(CNT([event_id]))` (Marks: **Line**, Dual Axis).
- **Color**: Cột màu cam đất, đường màu xanh đậm.

---

### Sheet 07: Top 10 Quốc Gia Tử Vong & Tỷ Lệ Lũy Kế (Combo Pareto Chart)
- **Người phụ trách**: **Thành viên 3 (1/4)** (Dashboard D2)
- **Filters**: Lọc Top 10 `[country_name]` theo `SUM([deaths])`.
- **Columns**: `[country_name]` (Sắp xếp giảm dần theo `SUM([deaths])`).
- **Rows**:
  - Trục 1: `SUM([deaths])` (Marks: **Bar**).
  - Trục 2: `[Cumulative Death %]` (Calculated Field CF12, Marks: **Line**, Dual Axis).
- **Reference Line**: Kéo đường mốc 80% (0.8) trên trục thứ hai để minh họa nguyên lý 80/20.

---

### Sheet 08: Phân Tích Cơ Cấu Nguyên Nhân Cháy Rừng (Sunburst / Multi-level Donut)
- **Người phụ trách**: **Thành viên 3 (2/4)** (Dashboard D3)
- **Filters**: `[disaster_type] = 'Wildfire'`.
- **Cách dựng**: Sử dụng kỹ thuật Donut chart 2 tầng (Pie marks lồng nhau qua Dual Axis của trục `MIN(1)`):
  - Tầng trong: Nhóm nguyên nhân khái quát `[Cause Group High Level]` (Tự nhiên vs Tác động con người).
  - Tầng ngoài: Từng tác nhân chi tiết `[cause_name]`.
- **Color**: Tự nhiên $\to$ Xanh lá cây; Nhân tạo $\to$ Đỏ cam; Khác $\to$ Xám.

---

### Sheet 09: Bản Đồ Thiệt Hại & Số Vụ Toàn Cầu (Choropleth Map Bắt Buộc)
- **Người phụ trách**: **Thành viên 3 (3/4)** (Dashboard D2)
- **Columns**: `[Longitude]` (Generated).
- **Rows**: `[Latitude]` (Generated).
- **Marks Card**: Chọn kiểu **Map**.
- **Detail**: Kéo `[iso3]` hoặc `[country_name]` vào **Detail**.
- **Color**: Kéo `SUM([Damage Bil USD])` vào **Color** $\to$ Chọn dải màu `Orange-Red`.
- **Tooltip**: Tên quốc gia, số vụ thảm họa, tổng thiệt hại tài chính.

---

### Sheet 10: Bản Đồ Điểm Các Đại Vụ Cháy Lớn (Proportional Symbol Map)
- **Người phụ trách**: **Thành viên 3 (4/4)** (Dashboard D3)
- **Filters**: `[disaster_type] = 'Wildfire'`.
- **Columns**: `[longitude]` (Continuous Measure / AVG).
- **Rows**: `[latitude]` (Continuous Measure / AVG).
- **Marks Card**: Chọn kiểu **Circle**.
- **Size**: Kéo `[burned_area_ha]` vào **Size**.
- **Color**: Kéo `[damage_usd]` vào **Color** (Dải màu cam đỏ, Opacity = 70% để nhìn thấu các điểm chồng lấp).
- **Detail**: `[event_name]` hoặc `[event_id]`.
- **Tooltip**: Tên vụ cháy, ngày bùng phát, diện tích (ha), thiệt hại (USD).

---

## 5. CƠ CHẾ TỰ ĐỘNG TƯƠNG THÍCH KHI CRAWL / CẬP NHẬT DỮ LIỆU MỚI

Khi Thành viên 1 thực hiện crawl dữ liệu mới hoặc bổ sung nguồn mới vào `data/raw/`:
1. **Tuân thủ Data Contract**: Mọi nguồn mới đều đi qua `src/03_clean.py` để chuẩn hóa trường và cột về đúng schema quy định trong `docs/DATA_DICTIONARY.md`.
2. **Không đổi tên trường**: Tất cả 13 Calculated Fields và 10 Worksheets sử dụng đúng tên cột logic (`start_date`, `damage_usd`, `burned_area_ha`, `iso3`, `disaster_type`, `cause_group`).
3. **Cập nhật tức thì trên Tableau**:
   - Mở file `.twbx` trong Tableau Desktop $\to$ chọn menu **Data** $\to$ **Refresh All Extracts** (hoặc F5).
   - Toàn bộ 10 sheets, 3 dashboards và Story Points sẽ tự động tính toán lại mà không bị gãy công thức hay lỗi missing fields.

---

## 6. BÀN GIAO SẢN PHẨM TRỰC QUAN HÓA

1. **File Workbook đóng gói**: Lưu tại `tableau/wildfire_disaster_analysis.twbx`.
2. **Xuất bản trực tuyến**: Đăng tải lên tài khoản Tableau Public cá nhân của nhóm.
3. **Nhúng vào Web**: Cập nhật đường link vào `README.md` và mã nhúng trong `dashboard/index.html`.
