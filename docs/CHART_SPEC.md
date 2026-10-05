# Đặc Tả 12 Biểu Đồ & Tableau Story (CHART SPECIFICATIONS)

> **Nhóm thực hiện**: Phân chia đều 4/4/4 (TV1: #1–#4, TV2: #5–#8, TV3: #9–#12)  
> **Công cụ chính**: **Tableau Desktop / Tableau Public** (Xuất bản trực tuyến + lưu trữ file `.twbx`)  
> **Kiến trúc trình bày**: 4 Dashboards (D1 $\to$ D4) + **Tableau Story với 4 Story Points** dẫn dắt cốt truyện

---

## 1. CẤU TRÚC 4 DASHBOARD (Mỗi Dashboard 3 Biểu Đồ, 1 Câu Hỏi Chính)

Bốn dashboard nối nhau như một câu chuyện hoàn chỉnh: **Bức tranh chung $\to$ Ở đâu $\to$ Cháy rừng cụ thể $\to$ Vì sao và hệ quả**.

| Dashboard | Câu hỏi chính | Biểu đồ trong dashboard | Mục tiêu phân tích |
|---|---|---|---|
| **D1 – Bức tranh 20 năm** (Tổng quát) | Thảm họa thiên nhiên có xảy ra nhiều hơn và thiệt hại lớn hơn qua các năm không? | #1 Combo số vụ + thiệt hại<br>#2 Stacked area theo loại thảm họa<br>#5 Diverging bar chênh lệch vs trung bình | Nhìn nhận xu hướng vĩ mô toàn cầu trong 2 thập kỷ qua. |
| **D2 – Ở đâu chịu thiệt hại?** (Không gian) | Quốc gia và khu vực nào chịu ảnh hưởng nặng nhất? | #3 Choropleth map thế giới<br>#6 Treemap châu lục $\to$ quốc gia<br>#9 Combo Pareto top 10 tử vong | Phân tích bất bình đẳng địa lý và tập trung rủi ro (Nguyên lý 80/20). |
| **D3 – Cháy rừng: Khi nào & lớn cỡ nào?** (Chi tiết cháy rừng) | Cháy rừng tập trung vào mùa nào, quy mô ra sao, vụ lớn nằm ở đâu? | #4 Heatmap tháng $\times$ năm<br>#8 Combo histogram + mật độ<br>#12 Bản đồ điểm vụ cháy lớn | Đi sâu vào hình thái mùa vụ và các siêu đám cháy (Mega-fires). |
| **D4 – Vì sao & Hệ quả** (Nguyên nhân & Tác động) | Nguyên nhân chính là gì và quy mô liên hệ thế nào với thiệt hại? | #10 Sunburst/Donut nguyên nhân<br>#11 Sankey luồng chuyển giao<br>#7 Bubble scatter diện tích vs thiệt hại | Phân tích căn nguyên (Con người vs Tự nhiên) và bài toán tương quan thiệt hại. |

---

## 2. ĐẶC TẢ TABLEAU STORY (Storytelling với 4 Story Points)

Tableau Story là tầng trình bày cao nhất, kết nối các Dashboard thành một bài thuyết trình trực quan sống động:

```
[Story Point 1: Xu Hướng 20 Năm] 
       ↓
[Story Point 2: Phân Bố Không Gian] 
       ↓
[Story Point 3: Trọng Tâm Cháy Rừng] 
       ↓
[Story Point 4: Căn Nguyên & Tác Động]
```

### 📍 Story Point 1: "Thảm họa 20 năm: Tần suất và Thiệt hại có đang gia tăng?"
- **Nội dung nhúng**: Dashboard **D1 – Bức tranh 20 năm**.
- **Tiêu đề thanh dẫn**: `1. Bức tranh 20 năm`
- **Thông điệp chính (Key Takeaway)**: Số lượng các thảm họa và tổn thất kinh tế gia tăng rõ rệt từ sau năm 2017, với đỉnh điểm kỷ lục năm 2020.
- **Chú thích nổi bật (Annotation)**: Gắn nhãn mũi tên tại cột năm 2020 trên biểu đồ #1 và #5: *"Năm 2020 đạt đỉnh thiệt hại vượt 45% mức trung bình 20 năm do tác động cộng hưởng của cháy rừng và bão nhiệt đới."*

### 📍 Story Point 2: "Điểm nóng toàn cầu: Châu lục & Quốc gia nào tổn thất nặng nề nhất?"
- **Nội dung nhúng**: Dashboard **D2 – Ở đâu chịu thiệt hại?**.
- **Tiêu đề thanh dẫn**: `2. Điểm nóng toàn cầu`
- **Thông điệp chính (Key Takeaway)**: Thiệt hại tài chính và sinh mạng phân bổ bất đối xứng nghiêm trọng theo nguyên lý 80/20.
- **Chú thích nổi bật**: Gắn đường tham chiếu 80% (Reference Line) trên Pareto chart #9 và nhãn nổi bật các quốc gia Châu Á - Châu Mỹ trên Choropleth #3.

### 📍 Story Point 3: "Trọng tâm Cháy rừng: Chu kỳ mùa vụ và sự trỗi dậy của siêu đám cháy"
- **Nội dung nhúng**: Dashboard **D3 – Cháy rừng: Khi nào & Lớn cỡ nào?**.
- **Tiêu đề thanh dẫn**: `3. Mùa vụ & Siêu đám cháy`
- **Thông điệp chính (Key Takeaway)**: Cháy rừng bùng phát mạnh mẽ vào các tháng mùa hè - đầu thu (tháng 6–9). Mặc dù các vụ cháy $\ge 10.000$ ha chiếm tỷ lệ nhỏ (< 5%), chúng gây ra hơn 70% tổng diện tích rừng bị tàn phá.
- **Chú thích nổi bật**: Đóng khung vùng nhiệt cao độ trên Heatmap #4 và đánh dấu cụm điểm cháy lớn trên Symbol Map #12.

### 📍 Story Point 4: "Căn nguyên & Hệ quả: Con người hay Tự nhiên?"
- **Nội dung nhúng**: Dashboard **D4 – Vì sao & Hệ quả**.
- **Tiêu đề thanh dẫn**: `4. Nguyên nhân & Tác động`
- **Thông điệp chính (Key Takeaway)**: Tác động của con người (bất cẩn, đốt nương rẫy, phá hoại) chiếm tỷ trọng số vụ áp đảo, trong khi sét đánh tự nhiên thường gây ra các vụ cháy ở vùng sâu khó tiếp cận; diện tích cháy và thiệt hại kinh tế tuân theo phân phối hàm mũ (Power law).
- **Chú thích nổi bật & Đoạn kết luận**: Tóm tắt 3 khuyến nghị hành động cho chính sách phòng chống thiên tai và giới hạn của nguồn dữ liệu mở.

---

## 3. PHÂN CHIA 12 BIỂU ĐỒ (TABLEAU WORKSHEETS)

| # | Tên Sheet | Dashboard | Kiểu Dữ Liệu | Bảng Màu Tableau | Người Phụ Trách |
|---|---|---|---|---|---|
| **1** | `Sheet_01_Combo_Trend` | D1 | Thời gian + 2 Số liên tục (Dual Axis) | `Tableau 10` (Xanh dương & Cam đỏ) | **TV1** |
| **2** | `Sheet_02_Stacked_Area` | D1 | Thời gian $\times$ Phân loại | `Color Blind` (Okabe-Ito chuẩn) | **TV1** |
| **3** | `Sheet_03_Choropleth_Map` | D2 | Không gian địa lý $\times$ Số | `Orange-Red` (Sequential) | **TV1** |
| **4** | `Sheet_04_Heatmap_Season` | D3 | Chu kỳ (Tháng) $\times$ Năm $\times$ Số | `YlOrRd` (Sequential nhiệt) | **TV1** |
| **5** | `Sheet_05_Diverging_Bar` | D1 | Độ lệch số học $\times$ Thời gian | `Red-Blue Diverging` (Tâm = 0) | **TV2** |
| **6** | `Sheet_06_Treemap_Damage` | D2 | Dữ liệu phân cấp (Châu lục $\to$ Nước) $\times$ Số | Phân màu theo Châu lục | **TV2** |
| **7** | `Sheet_07_Bubble_Scatter` | D4 | 3 Số liên tục (Trục Log-Log) $\times$ Phân loại | Categorical theo Châu lục | **TV2** |
| **8** | `Sheet_08_Combo_Histogram` | D3 | Phân phối biến số $\times$ Lũy kế | Đơn sắc Cam đất + Đường xanh | **TV2** |
| **9** | `Sheet_09_Combo_Pareto` | D2 | Xếp hạng Ordinal $\times$ Tích lũy 80/20 | Đỏ mận + Đường Cam nhấn | **TV3** |
| **10** | `Sheet_10_Donut_Cause` | D4 | Phân cấp nguyên nhân 2 tầng | Xanh (Tự nhiên) / Cam đỏ (Con người) | **TV3** |
| **11** | `Sheet_11_Sankey_Flow` | D4 | Luồng quan hệ đa tầng | Gradient theo loại thảm họa | **TV3** |
| **12** | `Sheet_12_Proportional_Map` | D3 | Tọa độ (Kinh/Vĩ) + 2 Biến số (Size, Color) | Kích thước vòng tròn + Màu đỏ cam | **TV3** |

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
- **Rows**: `YEAR([start_date])` (Discrete 2006..2025).
- **Marks Card**: Chọn kiểu **Square**.
- **Color**: Kéo `CNT([event_id])` vào **Color** $\to$ Chọn dải màu `YlOrRd`.

---

### Sheet 05: Biến Động Số Vụ So Với Trung Bình 20 Năm (Diverging Bar)
- **Người phụ trách**: Thành viên 2
- **Columns**: `[Diff from 20Yr Avg]` (Calculated Field CF7).
- **Rows**: `YEAR([start_date])` (Discrete).
- **Marks Card**: Chọn kiểu **Bar**.
- **Color**: Kéo `[Divergence Flag]` (Calculated Field CF8) vào **Color** (Vượt trung bình: Đỏ, Dưới trung bình: Xanh lam).
- **Reference Line**: Thêm đường tham chiếu cố định tại `Constant = 0`.

---

### Sheet 06: Cơ Cấu Thiệt Hại Phân Cấp: Châu Lục $\to$ Quốc Gia (Treemap)
- **Người phụ trách**: Thành viên 2
- **Marks Card**: Chọn kiểu **Square** (Treemap trong Show Me).
- **Color**: Kéo `[continent]` vào **Color**.
- **Detail**: Kéo `[country_name]` vào **Detail**.
- **Size**: Kéo `SUM([damage_usd])` vào **Size**.
- **Label**: Hiển thị tên nước và % tỷ trọng.

---

### Sheet 07: Tương Quan Diện Tích Cháy vs Thiệt Hại (Bubble Scatter Log-Log)
- **Người phụ trách**: Thành viên 2
- **Filters**: `[disaster_type] = 'Wildfire'` AND `[burned_area_ha] > 0` AND `[damage_usd] > 0`.
- **Columns**: `[Log10 Burned Area]` (hoặc chọn trục X $\to$ Edit Axis $\to$ chọn **Logarithmic**).
- **Rows**: `[Log10 Damage USD]` (hoặc chọn trục Y $\to$ chọn **Logarithmic**).
- **Marks Card**: Chọn kiểu **Circle**.
- **Size**: Kéo `SUM([affected])` hoặc `SUM([deaths])` vào **Size**.
- **Color**: Kéo `[continent]` vào **Color**.

---

### Sheet 08: Phân Phối Quy Mô Diện Tích Cháy (Combo Histogram + Pareto Line)
- **Người phụ trách**: Thành viên 2
- **Columns**: `[Burned Area Bin]` (Calculated Field CF11).
- **Rows**: 
  - Trục 1: `CNT([event_id])` (Marks: **Bar**).
  - Trục 2: `RUNNING_SUM(CNT([event_id])) / TOTAL(CNT([event_id]))` (Marks: **Line**, Dual Axis).
- **Color**: Cột màu cam đất, đường màu xanh đậm.

---

### Sheet 09: Top 10 Quốc Gia Tử Vong & Tỷ Lệ Lũy Kế (Combo Pareto Chart)
- **Người phụ trách**: Thành viên 3
- **Filters**: Lọc Top 10 `[country_name]` theo `SUM([deaths])`.
- **Columns**: `[country_name]` (Sắp xếp giảm dần theo `SUM([deaths])`).
- **Rows**:
  - Trục 1: `SUM([deaths])` (Marks: **Bar**).
  - Trục 2: `[Cumulative Death %]` (Calculated Field CF12, Marks: **Line**, Dual Axis).
- **Reference Line**: Kéo đường mốc 80% (0.8) trên trục thứ hai để minh họa nguyên lý 80/20.

---

### Sheet 10: Phân Tích Cơ Cấu Nguyên Nhân Cháy Rừng (Sunburst / Multi-level Donut)
- **Người phụ trách**: Thành viên 3
- **Filters**: `[disaster_type] = 'Wildfire'`.
- **Cách dựng**: Sử dụng kỹ thuật Donut chart 2 tầng (Pie marks lồng nhau qua Dual Axis của trục `MIN(1)`):
  - Tầng trong: Nhóm nguyên nhân khái quát `[Cause Group High Level]` (Tự nhiên vs Tác động con người).
  - Tầng ngoài: Từng tác nhân chi tiết `[cause_name]`.
- **Color**: Tự nhiên $\to$ Xanh lá cây; Nhân tạo $\to$ Đỏ cam; Khác $\to$ Xám.

---

### Sheet 11: Luồng Chuyển Giao Tác Động Thảm Họa (Sankey / Flow Matrix)
- **Người phụ trách**: Thành viên 3
- **Nguồn $\to$ Trung gian $\to$ Đích**: `[Cause Group]` $\to$ `[disaster_type]` $\to$ `[Damage Severity Level]`.
- **Thực hiện trong Tableau**: Có thể sử dụng bảng luồng phân nhánh (Multi-level Bar / Highlight Table) hoặc template Sankey với đường cong Sigmoid.

---

### Sheet 12: Bản Đồ Điểm Các Đại Vụ Cháy Lớn (Proportional Symbol Map)
- **Người phụ trách**: Thành viên 3
- **Filters**: `[disaster_type] = 'Wildfire'`.
- **Columns**: `[longitude]` (Continuous Measure / AVG).
- **Rows**: `[latitude]` (Continuous Measure / AVG).
- **Marks Card**: Chọn kiểu **Circle**.
- **Size**: Kéo `[burned_area_ha]` vào **Size**.
- **Color**: Kéo `[damage_usd]` vào **Color** (Dải màu cam đỏ, Opacity = 70% để nhìn thấu các điểm chồng lấp).
- **Detail**: `[event_name]` hoặc `[event_id]`.
- **Tooltip**: Tên vụ cháy, ngày bùng phát, diện tích (ha), thiệt hại (USD).

---

## 5. BÀN GIAO SẢN PHẨM TRỰC QUAN HÓA

1. **File Workbook đóng gói**: Lưu tại `tableau/wildfire_disaster_analysis.twbx`.
2. **Xuất bản trực tuyến**: Đăng tải lên tài khoản Tableau Public cá nhân của nhóm.
3. **Nhúng vào Web**: Cập nhật đường link vào `README.md` và mã nhúng trong `dashboard/index.html`.
