# Đặc Tả 10 Biểu Đồ & Tableau Story (CHART SPECIFICATIONS)

> **Phạm vi nghiên cứu**: Cháy rừng Bang California / Bắc Mỹ giai đoạn 2006–2025 (CAL FIRE FRAP, DINS, Census & NOAA)  
> **Nhóm thực hiện**: Phân chia tối ưu công việc **2 / 4 / 4**:
> - **Thành viên 1 (Data & ML)**: 2 biểu đồ (`Sheet_01`, `Sheet_02`) — Tập trung toàn lực vào Crawl/Làm sạch dữ liệu và Huấn luyện Mô hình dự báo Linear/Logistic trên Python.
> - **Thành viên 2 (Modeling & SQL)**: 4 biểu đồ (`Sheet_03`, `Sheet_04`, `Sheet_05`, `Sheet_06`).
> - **Thành viên 3 (Dashboard & Story)**: 4 biểu đồ (`Sheet_07`, `Sheet_08`, `Sheet_09`, `Sheet_10`).
>
> **Cam kết Barem đề thi**:
> - Tổng cộng **10 biểu đồ**, trong đó có **9 loại biểu đồ hoàn toàn khác nhau** (vượt chuẩn tối thiểu 8 loại của môn học):
>   1. *Dual-Axis Combo Bar + Line (kèm Trend Line dự báo)*
>   2. *Stacked Area Chart*
>   3. *Diverging Bar Chart (Tâm = 0)*
>   4. *Treemap Chart (Phân cấp Hạt $\to$ Loại công trình)*
>   5. *Bubble / Scatter Plot (Log-Log: Diện tích vs Nhà phá hủy)*
>   6. *Combo Histogram + Cumulative Pareto Line*
>   7. *Combo Pareto Chart (Top 10 Hạt bị tàn phá 80/20)*
>   8. *Donut / Sunburst Chart (Tự nhiên vs Con người)*
>   9. *Bản đồ địa lý bắt buộc (Map)*: Gồm cả *Choropleth Map (58 Hạt California)* và *Proportional Symbol Map (Điểm các đại vụ cháy lớn)*.
> - **Tương thích tự động với dữ liệu mới**: Tất cả công thức và trường dữ liệu đều được thiết kế tổng quát theo Data Dictionary chuẩn. Khi Thành viên 1 refresh dữ liệu mới vào `data/raw/` $\to$ chạy pipeline làm sạch $\to$ Tableau chỉ cần bấm **Refresh Data Source** là 10 biểu đồ, 3 Dashboard và Story Points sẽ tự động cập nhật chính xác 100%.

---

## 1. CẤU TRÚC 3 DASHBOARD CHUYÊN ĐỀ (Mỗi Dashboard 3–4 Biểu Đồ)

Mười biểu đồ được tích hợp thành 3 Dashboards chuyên đề chặt chẽ, tạo thành mạch dẫn dắt câu chuyện phân tích logic:

| Dashboard | Chủ đề & Câu hỏi phân tích | Biểu đồ trong dashboard | Mục tiêu phân tích |
|---|---|---|---|
| **D1 – Bức tranh 20 năm Cháy rừng California** (Xu hướng vĩ mô) | Tần suất và diện tích rừng bị thiêu rụi biến động thế nào qua 20 năm? Có xu hướng gia tăng và dự báo tương lai ra sao? | • #1 `Combo_Trend` (TV1)<br>• #2 `Stacked_Area` (TV1)<br>• #3 `Diverging_Bar` (TV2) | Phân tích xu hướng dài hạn 2006–2025, cơ cấu nguyên nhân bùng phát và độ lệch số vụ so với mức chuẩn 20 năm. |
| **D2 – Điểm nóng & Phân cấp thiệt hại theo 58 Hạt** (Không gian & 80/20) | Những Hạt (Counties) nào chịu thiệt hại nhà cửa và tài sản nặng nề nhất? Có tuân theo quy luật Pareto 80/20? | • #4 `Treemap_Damage` (TV2)<br>• #7 `Combo_Pareto` (TV3)<br>• #9 `Choropleth_Map` (TV3) | Nhận diện mức độ tập trung thiệt hại công trình/nhà ở theo 58 Hạt và phân cấp cấu trúc tài sản bị tàn phá. |
| **D3 – Mùa vụ, Căn nguyên & Siêu đám cháy** (Chi tiết chuyên sâu) | Cháy rừng bùng phát mạnh vào tháng nào, quy mô diện tích ra sao, căn nguyên do con người hay tự nhiên và siêu đám cháy ở đâu? | • #5 `Bubble_Scatter` (TV2)<br>• #6 `Combo_Histogram` (TV2)<br>• #8 `Donut_Cause` (TV3)<br>• #10 `Proportional_Map` (TV3) | Đào sâu vào phân phối diện tích đám cháy, căn nguyên kích hoạt và vị trí tọa độ các siêu thảm họa (>100.000 Acres). |

---

## 2. ĐẶC TẢ TABLEAU STORY (Tableau Story với 3 Story Points Trọng Tâm)

Cấu trúc Story Point dẫn dắt mạch lạc theo đúng barem yêu cầu (ít nhất 3 Story Points):

```
┌────────────────────────────────────────────────────────┐
│ [Point 1: 20 Năm Cháy rừng California: Tần suất & Xu thế]│
│                           │                            │
│                           ▼                            │
│ [Point 2: Điểm nóng 58 Hạt: Phân cấp tổn thất 80/20]  │
│                           │                            │
│                           ▼                            │
│ [Point 3: Căn nguyên, Siêu đám cháy & Thách thức tương lai]│
└────────────────────────────────────────────────────────┘
```

### 📍 Story Point 1: "20 Năm Cháy rừng California: Tần suất & Mức độ khốc liệt có đang tăng tốc?"
- **Nội dung nhúng**: Dashboard **D1 – Bức tranh 20 năm Cháy rừng California**.
- **Tiêu đề thanh dẫn**: `1. Bức tranh 20 năm California`
- **Thông điệp cốt lõi**: Trong 20 năm (2006–2025), tần suất các vụ cháy lớn tăng vọt, đặc biệt chu kỳ sau năm 2017 với các đợt đại hạn hán. Năm 2020 ghi nhận đỉnh kỷ lục thiêu rụi hơn 4.3 triệu Acres rừng. Đường xu thế Hồi quy tuyến tính cảnh báo diện tích tàn phá tiếp tục gia tăng.
- **Chú thích (Annotation)**: Gắn mũi tên ghi chú tại cột mốc năm 2020 và đường xu hướng dự báo Hồi quy tuyến tính: *"Kỷ lục 2020: Mùa cháy rừng lịch sử với hơn 4.3 triệu mẫu rừng bị thiêu rụi và hàng loạt siêu đám cháy phức hợp."*

### 📍 Story Point 2: "Điểm nóng 58 Hạt California: Phân cấp tổn thất nhà cửa theo nguyên lý 80/20"
- **Nội dung nhúng**: Dashboard **D2 – Điểm nóng & Phân cấp thiệt hại theo 58 Hạt**.
- **Tiêu đề thanh dẫn**: `2. Điểm nóng 58 Hạt (80/20)`
- **Thông điệp cốt lõi**: Thiệt hại về nhà cửa và công trình kiến trúc (theo CAL FIRE DINS) tuân theo chặt chẽ nguyên lý Pareto 80/20: Dưới 20% số Hạt (như Butte, Sonoma, Shasta, Lake, Napa) gánh chịu trên 80% tổng số nhà cửa bị thiêu rụi hoàn toàn (điển hình thảm họa Camp Fire 2018 tại Butte xóa sổ hơn 18.000 công trình).
- **Chú thích (Annotation)**: Gắn Reference Line 80% trên biểu đồ Pareto và tô sáng Hạt Butte, Sonoma trên bản đồ Choropleth 58 Hạt.

### 📍 Story Point 3: "Căn nguyên, Siêu đám cháy & Thách thức Tương lai"
- **Nội dung nhúng**: Dashboard **D3 – Mùa vụ, Căn nguyên & Siêu đám cháy**.
- **Tiêu đề thanh dẫn**: `3. Căn nguyên & Siêu đám cháy`
- **Thông điệp cốt lõi**: Mặc dù sét đánh tự nhiên gây ra các vụ cháy diện tích lớn nhất (như các đợt Lightning Complex 2020), nhưng hoạt động của con người (thiết bị, đường dây điện, bất cẩn) chiếm trên 85% tổng số vụ bùng phát gần khu dân cư. Các siêu đám cháy $\ge 100.000$ mẫu phân bố tập trung dọc sườn núi Sierra Nevada và vùng Bắc California.
- **Chú thích (Annotation)**: Đánh dấu các cụm siêu đám cháy (August Complex, Dixie, Mendocino) trên bản đồ điểm Proportional Symbol Map.

---

## 3. DANH MỤC PHÂN CHIA 10 BIỂU ĐỒ TABLEAU (2 / 4 / 4)

| # | Tên Sheet trong Tableau | Dashboard | Loại Biểu Đồ (Đảm bảo đa dạng) | Bảng Màu Quy Định | Người Phụ Trách |
|---|---|---|---|---|---|
| **1** | `Sheet_01_Combo_Trend` | D1 | **Combo Chart** (Dual-Axis Bar + Line + Trend Line) | Cột xanh dương `#4A90E2`, Đường cam `#D55E00` | **TV1 (1/2)** |
| **2** | `Sheet_02_Stacked_Area` | D1 | **Stacked Area Chart** (Cơ cấu nguyên nhân theo năm) | Bảng màu `Color Blind` (Okabe-Ito) | **TV1 (2/2)** |
| **3** | `Sheet_03_Diverging_Bar` | D1 | **Diverging Bar Chart** (Độ lệch số vụ so với trung bình 20 năm) | Dải phân kỳ `Red-Blue Diverging` (Tâm = 0) | **TV2 (1/4)** |
| **4** | `Sheet_04_Treemap_Damage` | D2 | **Treemap Chart** (Phân cấp Hạt $\to$ Loại công trình phá hủy) | Phân màu theo Nhóm Hạt | **TV2 (2/4)** |
| **5** | `Sheet_05_Bubble_Scatter` | D3 | **Bubble Scatter Plot** (Trục Log-Log: Diện tích vs Nhà cháy vs Thương vong) | Phân loại theo Vùng Địa lý | **TV2 (3/4)** |
| **6** | `Sheet_06_Combo_Histogram` | D3 | **Combo Histogram** (Cột diện tích theo Bin log + Đường lũy kế) | Đơn sắc Cam đất + Đường xanh | **TV2 (4/4)** |
| **7** | `Sheet_07_Combo_Pareto` | D2 | **Pareto Chart** (Top 10 Hạt nhà bị cháy + Đường 80/20) | Cột đỏ mận + Đường cam nhấn | **TV3 (1/4)** |
| **8** | `Sheet_08_Donut_Cause` | D3 | **Donut / Sunburst Chart** (Nguyên nhân 2 tầng: Tự nhiên vs Con người) | Xanh (Tự nhiên) / Đỏ cam (Con người) | **TV3 (2/4)** |
| **9** | `Sheet_09_Choropleth_Map` | D2 | **Bản Đồ Phân Vùng** (Choropleth Map 58 Hạt California) | Dải tuần tự `Orange-Red` | **TV3 (3/4)** |
| **10**| `Sheet_10_Proportional_Map`| D3 | **Bản Đồ Điểm** (Proportional Symbol Map các đại vụ cháy lớn) | Kích cỡ = Acres, Màu = Nhà phá hủy | **TV3 (4/4)** |

---

## 4. CHI TIẾT KỸ THUẬT KÉO THẢ 10 SHEETS TRONG TABLEAU

### Sheet 01: Tần Suất & Diện Tích Cháy Theo Năm (Dual-Axis Combo + Trend Line)
- **Người phụ trách**: **Thành viên 1 (1/2)** (Dashboard D1)
- **Columns**: `YEAR([alarm_date])` hoặc `[year]` (Discrete / Dimension).
- **Rows**: 
  - Trục 1: `CNT([incident_id])` $\to$ Marks: **Bar** (Cột màu xanh `#4A90E2`).
  - Trục 2: `SUM([acres_burned])` $\to$ Marks: **Line** (Đường màu cam `#D55E00`).
- **Thao tác Dual Axis**: Chuột phải vào trục thứ 2 $\to$ chọn **Dual Axis** (hai thang đo độc lập: Số vụ cháy vs Mẫu rừng thiêu rụi).
- **Tích hợp mô hình dự báo**: Thêm đường **Trend Line** tuyến tính trên trục diện tích cháy để minh họa kết quả Linear Regression của TV1 (hoặc nạp bảng `forecast_results.csv`).
- **Tooltip**: Hiển thị năm, số vụ cháy xảy ra, tổng diện tích cháy (Acres và Hecta).

---

### Sheet 02: Cơ Cấu Nguyên Nhân Cháy Theo Thời Gian (Stacked Area)
- **Người phụ trách**: **Thành viên 1 (2/2)** (Dashboard D1)
- **Columns**: `YEAR([alarm_date])` hoặc `[year]` (Continuous / Date).
- **Rows**: `CNT([incident_id])`.
- **Marks Card**: Chọn kiểu **Area**.
- **Color**: Kéo trường `[cause_name]` hoặc `[cause_group]` vào **Color**.
- **Sắp xếp**: Đặt `Lightning` (Sét đánh) và `Equipment Use` ở dưới cùng để theo dõi sự biến thiên rõ nét nhất.

---

### Sheet 03: Biến Động Số Vụ So Với Mức Trung Bình 20 Năm (Diverging Bar)
- **Người phụ trách**: **Thành viên 2 (1/4)** (Dashboard D1)
- **Columns**: `[Diff from 20Yr Avg]` (Calculated Field: số vụ của năm trừ đi trung bình chuẩn 20 năm).
- **Rows**: `[year]` (Discrete).
- **Marks Card**: Chọn kiểu **Bar**.
- **Color**: Kéo `[Divergence Flag]` vào **Color** (Vượt trung bình: Đỏ cam, Dưới trung bình: Xanh lam).
- **Reference Line**: Thêm đường tham chiếu cố định tại `Constant = 0`.

---

### Sheet 04: Cơ Cấu Nhà Cửa Bị Phá Hủy: Hạt $\to$ Loại Công Trình (Treemap)
- **Người phụ trách**: **Thành viên 2 (2/4)** (Dashboard D2)
- **Marks Card**: Chọn kiểu **Square** (Treemap).
- **Color**: Kéo `[county]` vào **Color**.
- **Detail**: Kéo `[structure_type]` vào **Detail** (Single Family, Commercial, Outbuilding...).
- **Size**: Kéo `CNT([record_id])` hoặc `SUM([structures_destroyed])` vào **Size**.
- **Label**: Hiển thị tên Hạt, loại công trình và số lượng bị phá hủy.

---

### Sheet 05: Tương Quan Diện Tích Cháy vs Công Trình Phá Hủy (Bubble Scatter Log-Log)
- **Người phụ trách**: **Thành viên 2 (3/4)** (Dashboard D3)
- **Filters**: `[acres_burned] > 0` AND `[structures_destroyed] >= 0`.
- **Columns**: `[acres_burned]` $\to$ Edit Axis $\to$ chọn **Logarithmic scale**.
- **Rows**: `[structures_destroyed]` $\to$ Edit Axis $\to$ chọn **Logarithmic scale**.
- **Marks Card**: Chọn kiểu **Circle**.
- **Size**: Kéo `SUM([deaths_direct])` hoặc `SUM([acres_burned])` vào **Size**.
- **Color**: Kéo `[cause_group]` hoặc Vùng Hạt vào **Color**.
- **Detail**: `[fire_name]`.

---

### Sheet 06: Phân Phối Quy Mô Diện Tích Cháy Rừng (Combo Histogram + Cumulative Line)
- **Người phụ trách**: **Thành viên 2 (4/4)** (Dashboard D3)
- **Columns**: `[Acres Bin Log]` (Tạo Bin theo nhóm diện tích: <1k, 1k-5k, 5k-25k, 25k-100k, >100k Acres).
- **Rows**: 
  - Trục 1: `CNT([incident_id])` (Marks: **Bar**).
  - Trục 2: `RUNNING_SUM(CNT([incident_id])) / TOTAL(CNT([incident_id]))` (Marks: **Line**, Dual Axis).
- **Color**: Cột màu cam đất, đường màu xanh đậm.

---

### Sheet 07: Top 10 Hạt Chịu Thiệt Hại Nhà Cửa Nặng Nhất & Tỷ Lệ Lũy Kế (Combo Pareto 80/20)
- **Người phụ trách**: **Thành viên 3 (1/4)** (Dashboard D2)
- **Filters**: Lọc Top 10 `[county]` theo `SUM([structures_destroyed])`.
- **Columns**: `[county]` (Sắp xếp giảm dần theo số công trình phá hủy).
- **Rows**:
  - Trục 1: `SUM([structures_destroyed])` (Marks: **Bar**).
  - Trục 2: `[Cumulative Destroyed %]` (Marks: **Line**, Dual Axis).
- **Reference Line**: Kéo đường mốc 80% (0.8) trên trục thứ hai để chứng minh nguyên lý Pareto 80/20.

---

### Sheet 08: Phân Tích Cơ Cấu Nguyên Nhân Cháy: Tự Nhiên vs Con Người (Donut 2 Tầng)
- **Người phụ trách**: **Thành viên 3 (2/4)** (Dashboard D3)
- **Cách dựng**: Sử dụng kỹ thuật Donut chart 2 tầng (Pie marks lồng nhau qua Dual Axis của trục `MIN(1)`):
  - Tầng trong: Nhóm khái quát `[cause_group]` (Natural vs Human vs Undetermined).
  - Tầng ngoài: Từng tác nhân chi tiết `[cause_name]` (Lightning, Equipment, Powerline, Arson, Campfire...).
- **Color**: Natural $\to$ Xanh lá cây; Human $\to$ Đỏ cam; Khác $\to$ Xám.

---

### Sheet 09: Bản Đồ Thiệt Hại & Số Nhà Cháy Theo 58 Hạt California (Choropleth Map Bắt Buộc)
- **Người phụ trách**: **Thành viên 3 (3/4)** (Dashboard D2)
- **Columns**: `[Longitude]` (Generated).
- **Rows**: `[Latitude]` (Generated).
- **Marks Card**: Chọn kiểu **Map**.
- **Detail**: Kéo `[county]` (gán Geographic Role là **County**) vào **Detail** (kèm State/Province: California).
- **Color**: Kéo `SUM([structures_destroyed])` hoặc `SUM([acres_burned])` vào **Color** $\to$ Chọn dải màu `Orange-Red`.
- **Tooltip**: Tên Hạt, dân số, số vụ cháy, số công trình bị phá hủy.

---

### Sheet 10: Bản Đồ Điểm Các Đại Vụ Cháy Lớn California (Proportional Symbol Map)
- **Người phụ trách**: **Thành viên 3 (4/4)** (Dashboard D3)
- **Columns**: `[longitude]` (Continuous Measure / AVG).
- **Rows**: `[latitude]` (Continuous Measure / AVG).
- **Marks Card**: Chọn kiểu **Circle**.
- **Size**: Kéo `[acres_burned]` vào **Size**.
- **Color**: Kéo `[structures_destroyed]` vào **Color** (Dải màu cam đỏ, Opacity = 70% để nhìn thấu các điểm chồng lấp).
- **Detail**: `[fire_name]`.
- **Tooltip**: Tên vụ cháy (Camp, August Complex...), Hạt, năm, diện tích cháy (Acres), số công trình bị phá hủy.

---

## 5. CƠ CHẾ TỰ ĐỘNG TƯƠNG THÍCH KHI REFRESH DỮ LIỆU

Khi Thành viên 1 thực hiện làm sạch và cập nhật dữ liệu mới vào `data/clean/master_clean.csv`:
1. **Tuân thủ Data Contract**: Mọi nguồn đều chuẩn hóa theo `docs/DATA_DICTIONARY.md`.
2. **Không đổi tên trường**: Tất cả trường dữ liệu (`fire_name`, `county`, `acres_burned`, `structures_destroyed`, `cause_name`, `alarm_date`, `year`...) giữ nguyên cấu trúc logic.
3. **Cập nhật tức thì trên Tableau**:
   - Mở file `.twbx` trong Tableau Desktop $\to$ chọn menu **Data** $\to$ **Refresh All Extracts** (hoặc F5).
   - Toàn bộ 10 sheets, 3 dashboards và Story Points sẽ tự động tính toán lại mà không phát sinh lỗi.

