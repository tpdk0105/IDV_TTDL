# Đặc Tả 10 Sheet Trực Quan Hóa & 4 Thẻ KPI Trên Tableau (CHART SPECIFICATIONS)

> **Tác giả / Hiệu đính**: @DiKhang · Cập nhật ngày 08/10/2026  
> **Nguồn dữ liệu**: CAL FIRE FRAP, DINS, Census Bureau, NOAA NCEI (2006–2025: 7.235 vụ cháy, 114.726 bản ghi công trình DINS)  
> **Môi trường thực thi**: Tableau Public (bản Web) & Tableau Desktop  
> **Đối chiếu thực nghiệm**: 100% số liệu đã được kiểm chứng bằng Python trên tập dữ liệu gốc sạch.

---

## 1. TỔNG QUAN DANH MỤC 10 SHEET & 4 THẺ KPI

| # | Tên Tab | Loại Biểu Đồ | Phân Nhóm | Câu Hỏi Nghiên Cứu & Trả Lời |
|---|---|---|---|---|
| **1** | `01_Line_Season` | Line Chart (2 đường) | Cơ bản | Mùa cháy rơi vào tháng nào, có đang dài ra không? |
| **2** | `02_Area_Cause_Trend` | Stacked Area Chart | Cơ bản | Cơ cấu nguyên nhân thay đổi thế nào qua 20 năm? |
| **3** | `03_Map_County` | Bản đồ 2 lớp (Map + Circle) | Cơ bản | Hạt nào cháy dày đặc nhất và Hạt nào cháy rộng nhất? |
| **4** | `04_Donut_Cause_Share` | Donut Chart (Dual-Axis) | Cơ bản | Nhóm nguyên nhân nào chiếm tỷ trọng lớn nhất? |
| **5** | `05_Bar_Top_Counties` | Horizontal Bar + Top N | Cơ bản | Những hạt nào mất nhiều công trình nhất? |
| **6** | `06_Heatmap_Cause_Size` | Heatmap (% Table across) | Cơ bản | Nhóm nguyên nhân nào hay gây ra đám cháy lớn? |
| **7** | `07_Treemap_Damage` | Treemap (1 tầng) | Cơ bản | Thiệt hại dồn vào loại công trình và Hạt nào? |
| **8** | `08_Scatter_Regression` | Scatter Plot + Hồi quy log-log | Cơ bản / Dự báo | Cháy càng rộng có phá hủy càng nhiều nhà cửa không? |
| **9** | `09_Pareto_Damage` | Pareto Chart (Cột + Đường) | Nâng cao | Bao nhiêu Hạt gây ra 80% thiệt hại toàn bang? |
| **10**| `10_Diverging_vs_Avg` | Diverging Bar Chart quanh 0 | Nâng cao | Những năm nào cháy bất thường so với mức trung bình lịch sử? |
| **KPI**| `KPI_1` $\to$ `KPI_4` | Thẻ chỉ số tổng quan | Hỗ trợ Dashboard | Tổng số vụ, diện tích cháy, công trình bị thiêu rụi, số người tử vong. |

---

## 2. ĐẶC TẢ CHI TIẾT TỪNG SHEET

### Sheet 1: `01_Line_Season` (Mùa Cháy Theo Tháng: So Sánh 2 Thập Kỷ)
* **Loại biểu đồ**: Line Chart (kết hợp Dual-Axis thêm Circle Marker trên Tableau Web).
* **Mục tiêu**: Chứng minh hiện tượng biến đổi khí hậu khiến mùa cháy rừng bị kéo dài ra ở hai đầu mùa.
* **Cấu hình trục**:
  * **Columns**: `[dim_date].[month]` (Discrete / Blue pill, đổi alias 1–12 thành T1–T12).
  * **Rows**: Kéo `[Fire Incidents Count (calc)]` vào 2 lần $\to$ Dual Axis $\to$ Synchronize Axis.
* **Marks**:
  * Thẻ Line: Color = `[Giai đoạn]` (2006–2015 màu xám, 2016–2025 màu đỏ). Bật nhãn *Min/Max*.
  * Thẻ Circle: Tắt nhãn, tạo chấm tròn mượt mà tại các mốc tháng.
* **Số kiểm tra chuẩn**:
  * T4: 77 vụ (giai đoạn 1) $\to$ 131 vụ (giai đoạn 2) (+70%).
  * T5: 245 vụ $\to$ 416 vụ (+70%).
  * T7 (Đỉnh): 803 vụ $\to$ 936 vụ (+17%).
  * T10: 167 vụ $\to$ 289 vụ (+73%).
  * Tổng số vụ 2 giai đoạn: 3.039 vụ vs 4.196 vụ (+38%).
* **Insight**: 80% số vụ (5.813/7.235) tập trung từ T6–T10. Giữa mùa chỉ tăng 17% nhưng đầu mùa (T4-T5) và cuối mùa (T10) tăng tới ~70-73%, chứng minh mùa cháy rừng đang dài ra rõ rệt.

---

### Sheet 2: `02_Area_Cause_Trend` (Cơ Cấu Nguyên Nhân Theo Năm)
* **Loại biểu đồ**: Stacked Area Chart.
* **Cấu hình trục**:
  * **Columns**: `[dim_date].[year]` (Continuous / Green pill, Fixed 2006–2025).
  * **Rows**: `[Fire Incidents Count (calc)]`.
* **Marks**: Chọn **Area**. Color = `[cause_group]` (Con người: Đỏ `#D95F02`, Tự nhiên: Xanh `#2CA02C`, Chưa xác định: Xám `#7F7F7F`). Kéo Con người xuống dưới cùng legend để nằm sát trục hoành.
* **Số kiểm tra**:
  * Toàn giai đoạn: Con người 2.635 vụ, Tự nhiên 1.509 vụ, Chưa xác định 3.091 vụ.
  * Năm 2008 bão sét kỷ lục: Sấm sét 249 vụ (57% số vụ năm đó).
* **Insight**: Nhóm "Chưa xác định" tăng mạnh từ 24% (2006) lên 61% (2024), phản ánh thách thức điều tra hiện trường vụ cháy ngày càng phức tạp.

---

### Sheet 3: `03_Map_County` (Mật Độ & Diện Tích Cháy Theo Hạt)
* **Loại biểu đồ**: Bản đồ địa lý 2 lớp (Marks Layer: Map + Circle).
* **Cấu hình địa lý**:
  * Nhấp đúp `[county_name]` (Geographic Role: County).
  * Kéo calculated field `[State]` = `"California"` vào thẻ **Detail** của cả 2 lớp để định vị chính xác bang California.
  * **Filter**: Loại bỏ giá trị `Unknown`.
* **Lớp 1 (Bản đồ phân vùng)**: Marks = Map, Color = `[Mật độ cháy (vụ/1.000 dặm²)]`, bảng màu Orange tuần tự, viền trắng.
* **Lớp 2 (Bong bóng diện tích)**: Thả `[county_name]` vào ô *Add a Marks Layer* $\to$ Marks = Circle, Size = `SUM([acres_burned])`, màu xám 50% trong suốt.
* **Số kiểm tra**: Tổng diện tích xác định hạt là 17.623.077 acres. Hạt Kern nhiều vụ nhất (1.015 vụ). Hạt Yuba có mật độ cao nhất (~466 vụ/1.000 dặm²). Vòng tròn diện tích lớn nhất là Hạt Butte (2.000.214 acres).
* **Insight**: Hạt có nhiều vụ nhất (Kern) không đồng nghĩa với mật độ dày đặc nhất (Yuba, Lake) hay diện tích bị thiêu rụi lớn nhất (Butte).

---

### Sheet 4: `04_Donut_Cause_Share` (Tỷ Trọng 7.235 Vụ Cháy Theo Nhóm Nguyên Nhân)
* **Loại biểu đồ**: Donut Chart (Dual-Axis Pie + Circle).
* **Cấu hình trục**:
  * **Rows**: Gõ trực tiếp `MIN(0)` hai lần $\to$ Dual Axis $\to$ Synchronize Axis $\to$ Ẩn Header.
* **Thẻ 1 (Pie ngoài)**: Color = `[cause_group]`, Angle = `[Fire Incidents Count (calc)]`. Label = `[cause_group]` và Quick Table Calc `Percent of Total`.
* **Thẻ 2 (Vòng tròn trong)**: Circle màu trắng `#FFFFFF`, Size nhỏ hơn Pie ngoài để khoét lỗ rỗng ở giữa.
* **Số kiểm tra**: Chưa xác định 3.091 vụ (42,7%), Con người 2.635 vụ (36,4%), Tự nhiên 1.509 vụ (20,9%).
* **Insight**: Trong số các vụ đã xác định nguyên nhân, con người chiếm tới 64% (2.635/4.144 vụ), chủ yếu do tia lửa thiết bị (762), phương tiện giao thông (488), cố ý đốt phá (363) và lưới điện (335).

---

### Sheet 5: `05_Bar_Top_Counties` (Top N Hạt Có Nhiều Công Trình Bị Phá Hủy Nhất)
* **Loại biểu đồ**: Horizontal Bar Chart có tham số điều khiển Top N.
* **Cấu hình trục**:
  * **Rows**: `[dim_county].[county_name]`.
  * **Columns**: `SUM([total_structures_destroyed])`.
  * Sắp xếp: Sort giảm dần.
* **Filters & Parameters**:
  * Tạo parameter `[Top N]` (Integer, Range 5–20, mặc định 10).
  * Filter `[county_name]` loại bỏ `Unknown` $\to$ **Add to Context**.
  * Filter `[county_name]` thứ 2 $\to$ Tab Top $\to$ Chọn `Top [Top N]` theo `SUM([total_structures_destroyed])`.
* **Số kiểm tra (Top 10 Hạt)**: Butte (23.834), Los Angeles (19.066), Sonoma (7.413), Lake (2.711), San Diego (2.553), Shasta (2.354), Napa (2.336), Santa Barbara (1.562), Santa Cruz (1.543), El Dorado (1.403).
* **Insight**: Riêng 2 Hạt dẫn đầu (Butte và Los Angeles) đã chiếm 58% tổng số công trình bị phá hủy toàn bang California.

---

### Sheet 6: `06_Heatmap_Cause_Size` (Nhóm Nguyên Nhân $\times$ Quy Mô Đám Cháy)
* **Loại biểu đồ**: Heatmap (Square ma trận).
* **Cấu hình trục**:
  * **Rows**: `[dim_cause].[cause_group]`.
  * **Columns**: `[Acres Bin Log (calc)]` (Sort Manual: `< 300`, `300–1k`, `1k–5k`, `5k–25k`, `25k–100k`, `≥ 100k`).
* **Marks**: Square.
  * Color + Label = `[Fire Incidents Count (calc)]` với Table Calculation: `Percent of Total`, Compute Using: `Table (across)` (mỗi hàng nguyên nhân cộng lại bằng 100%).
  * Edit Colors: Palette Blue, End = Custom `0.15`, Stepped 5 bước.
* **Bảng số liệu đối soát**:
  | Nhóm nguyên nhân | < 300 | 300–1k | 1k–5k | 5k–25k | 25k–100k | ≥ 100k |
  |---|:---:|:---:|:---:|:---:|:---:|:---:|
  | **Con người** | 81,4% | 10,2% | 5,3% | 1,9% | 0,8% | 0,3% |
  | **Tự nhiên** | 65,0% | 11,1% | 12,0% | 7,8% | 3,2% | 0,9% |
  | **Chưa xác định** | 82,1% | 7,4% | 5,6% | 3,0% | 1,6% | 0,3% |
* **Insight**: Tự nhiên có tới 11,9% số vụ vượt mốc 5.000 mẫu (cao gấp 4 lần so với mức 3,0% của con người), do sét đánh ở vùng rừng núi hẻo lánh khó tiếp cận dập lửa kịp thời.

---

### Sheet 7: `07_Treemap_Damage` (Công Trình Bị Phá Hủy Theo Loại Và Hạt)
* **Loại biểu đồ**: Treemap 1 tầng phẳng.
* **Nguồn dữ liệu**: Bảng chi tiết kiểm định `fact_structure_damage` (DINS).
* **Cấu hình**:
  * Marks: Chọn **Square**.
  * **Detail**: `[dim_county].[county_name]`.
  * **Color**: Hierarchy `[Loại công trình]` (hoặc field `[Nhóm công trình]`).
  * **Size**: `SUM([structures_destroyed])`.
  * *Lưu ý*: Xóa `Latitude (generated)` và `Longitude (generated)` khỏi Columns/Rows nếu Tableau tự sinh ra.
  * **Filters**: Bỏ `Unknown` (Add to Context) và lọc Top 8 Hạt theo thiệt hại.
* **Số kiểm tra**: Tổng kiểm định toàn bảng: 69.198 công trình; Top 8 Hạt chiếm 59.368 công trình. Toàn bộ: Nhà 1 hộ (36.057), Công trình phụ (17.494), Nhà di động (7.396).
* **Insight**: Nhà ở dân sinh chiếm ~64% tổng số công trình bị phá hủy, khẳng định cháy rừng tại California là thảm họa trực tiếp đe dọa khu dân cư.

---

### Sheet 8: `08_Scatter_Regression` (Hồi Quy Tuyến Tính Log-Log: Diện Tích vs Thiệt Hại)
* **Loại biểu đồ**: Scatter Plot tích hợp Mô hình Hồi quy tuyến tính log-log (Barem Dự báo 0.5 đ).
* **Cấu hình trục**:
  * **Columns**: `[Log Diện tích]` (Biến đổi $\log_{10}$ diện tích cháy).
  * **Rows**: `[Log Công trình phá hủy]` (Biến đổi $\log_{10}$ số công trình bị phá hủy).
  * **Detail**: `[incident_id]` (Dimension) $\to$ Mỗi điểm là một vụ cháy có thiệt hại.
* **Marks**: Circle, Color = `[cause_group]`, Opacity = 75%.
* **Trend Line Model**: Tab Analytics $\to$ Kéo **Trend Line** $\to$ Linear $\to$ Bỏ chọn *Allow a trend line per color* $\to$ Bật *Show confidence bands* (95%).
* **Phương trình hồi quy**:
  $$\log_{10}(\text{Công trình phá hủy}) = 0{,}433436 \times \log_{10}(\text{Diện tích}) - 0{,}377417$$
  * $R^2 = 0{,}356$ (Cao gấp 13 lần so với hồi quy số gốc $R^2 = 0{,}026$).
  * $p\text{-value} < 0{,}0001$, $t\text{-value} = 14{,}658$.
* **Diễn giải & Dự báo**: Khi diện tích cháy tăng 10 lần, số công trình bị phá hủy tăng khoảng 2,7 lần. Dự báo: Đám cháy 1.000 mẫu $\approx 8$ công trình; 10.000 mẫu $\approx 23$ công trình; 100.000 mẫu $\approx 62$ công trình bị phá hủy.

---

### Sheet 9: `09_Pareto_Damage` (Pareto 80/20: 7 Hạt Gây Ra 82% Thiệt Hại Toàn Bang)
* **Loại biểu đồ**: Dual-Axis Combo Pareto (Bar + Line).
* **Cấu hình trục**:
  * **Columns**: `[dim_county].[county_name]`, Sort giảm dần theo `SUM([total_structures_destroyed])`.
  * **Rows**: Kéo `SUM([total_structures_destroyed])` vào 2 lần $\to$ Dual Axis.
* **Table Calculation trên trục thứ 2**:
  * Primary Calc: `Running Total` (Sum, Table across).
  * Secondary Calc: `Percent of Total` (Table across).
  * Trục phải: Định dạng Percentage 0–100%.
* **Reference Line**: Tab Analytics $\to$ Reference Line thả vào trục phải $\to$ Value chọn Parameter `[Mốc 80%]` ($0.8$) $\to$ Label: *"Ngưỡng Pareto 80%"*.
* **Số kiểm tra % tích lũy**: Butte 32,3% $\to$ Los Angeles 58,1% $\to$ Sonoma 68,2% $\to$ Lake 71,8% $\to$ San Diego 75,3% $\to$ Shasta 78,5% $\to$ **Napa 81,6% (Hạt thứ 7 chạm mốc 82%)**.
* **Insight**: Quy luật bất cân xứng cực đoan: Chỉ 7/49 Hạt có thiệt hại (14% số Hạt) đã gây ra tới 82% tổng thiệt hại nhà cửa toàn bang California.

---

### Sheet 10: `10_Diverging_vs_Avg` (Số Vụ Cháy So Với Mức Trung Bình 20 Năm)
* **Loại biểu đồ**: Diverging Bar Chart quanh mốc 0.
* **Cấu hình trục**:
  * **Columns**: `[dim_date].[year]` (Discrete).
  * **Rows**: `[Diff from 20Yr Avg (calc)]`.
* **Marks**: Bar. Color = `[Divergence Flag (calc)]` (Vượt trung bình: Cam đỏ `#D55E00`, Dưới trung bình: Xanh `#0072B2`).
* **Reference Line**: Kéo Reference Line $\to$ Value chọn Parameter `[Mốc 0]` $\to$ Label: *"Trung bình 20 năm = 362 vụ"*.
* **Số kiểm tra**: Mức trung bình 20 năm: $7.235 / 20 = 361{,}75$ vụ/năm.
  * Các năm vượt đỉnh: 2017 (+243 vụ), 2024 (+174 vụ), 2025 (+148 vụ), 2020 (+133 vụ).
  * Các năm thấp kỷ lục: 2010 (-156 vụ), 2014 (-127 vụ), 2009 (-110 vụ).
* **Insight**: Trước năm 2017 phần lớn các năm đều dưới trung bình. Từ năm 2017 đến nay có tới 5/9 năm vượt xa mức trung bình 20 năm, minh chứng xu hướng gia tăng tần suất hỏa hoạn.

---

### HỆ THỐNG 4 THẺ CHỈ SỐ KPI TỔNG QUAN

| Tên Sheet KPI | Field Kéo Thả | Định Dạng Hiển Thị | Giá Trị Đúng (Đối Soát) |
|---|---|---|---|
| `KPI_1_So_vu` | `[Fire Incidents Count (calc)]` | Số nguyên | **7.235 vụ** |
| `KPI_2_Dien_tich` | `SUM([acres_burned])` | Millions, 2 số thập phân | **19,39 triệu mẫu (acres)** |
| `KPI_3_Pha_huy` | `SUM([total_structures_destroyed])` | Số nguyên | **73.818 công trình** |
| `KPI_4_Tu_vong` | `SUM([deaths_direct])` | Số nguyên | **255 người** |
