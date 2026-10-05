# Hướng Dẫn Thực Hiện Trực Quan Hóa Trên Tableau Public

> **Đồ án**: "Nghiên cứu – phân tích tần suất và thiệt hại của các trận cháy rừng / thảm họa thiên nhiên trong 20 năm qua (2006–2025)"  
> **Công cụ trực quan hóa**: Tableau Desktop / Tableau Public  
> **Sản phẩm bàn giao**: 
> 1. File workbook đóng gói: `tableau/wildfire_disaster_analysis.twbx`
> 2. Đường link xuất bản trực tuyến: **Tableau Public URL**
> 3. Bản nhúng tương tác trực tiếp trên giao diện web GitHub Pages (`dashboard/index.html`).

---

## 1. Kết Nối Dữ Liệu Vào Tableau

1. Mở **Tableau Desktop** hoặc **Tableau Public App**.
2. Tại mục **Connect** (Kết nối dữ liệu):
   - Chọn **Text file** $\to$ Chọn file dữ liệu đã làm sạch: `data/clean/master_clean.csv` (hoặc kết nối qua SQLite Driver nếu dùng database).
3. Đảm bảo các trường dữ liệu nhận đúng kiểu:
   - `start_date`, `end_date`: Kiểu **Date** (Lịch).
   - `latitude`: Kiểu **Geographic Role $\to$ Latitude**.
   - `longitude`: Kiểu **Geographic Role $\to$ Longitude**.
   - `iso3`: Kiểu **Geographic Role $\to$ Country/Region**.
   - `damage_usd`, `burned_area_ha`, `deaths`, `affected`: Kiểu **Number (decimal / whole)**.
4. Mở file [tableau/CALCULATED_FIELDS.md](file:///c:/Users/ASUS/Documents/Tương tác dữ liệu/đồ án ck/IDV_TTDL/tableau/CALCULATED_FIELDS.md) và tạo đầy đủ các trường tính toán cần thiết.

---

## 2. Quy Trình Phân Chia 12 Biểu Đồ (Worksheets)

Mỗi thành viên phụ trách **đúng 4 Worksheets** (chia đều 4/4/4), đặt tên Sheet theo quy ước: `Sheet_01`, `Sheet_02`... để dễ dàng quản lý.

### 👤 Thành viên 1: Biểu đồ #1 – #4 (Tổng quan & Mùa vụ)
- **Worksheet #1**: `Sheet_01_Combo_Trend` (Combo Dual-Axis: Cột số vụ + Đường thiệt hại USD theo năm 2006–2025).
- **Worksheet #2**: `Sheet_02_Stacked_Area` (Stacked Area: Cơ cấu phân bổ các loại thảm họa theo thời gian).
- **Worksheet #3**: `Sheet_03_Choropleth_Map` (Bản đồ thế giới phân vùng mức độ thiệt hại/số vụ theo quốc gia).
- **Worksheet #4**: `Sheet_04_Heatmap_Season` (Ma trận Heatmap mùa vụ cháy rừng: Tháng $\times$ Năm).

### 👤 Thành viên 2: Biểu đồ #5 – #8 (Phân kỳ, Phân cấp & Tương quan)
- **Worksheet #5**: `Sheet_05_Diverging_Bar` (Cột phân kỳ: Chênh lệch số vụ so với trung bình chuẩn 20 năm, tâm = 0).
- **Worksheet #6**: `Sheet_06_Treemap_Damage` (Treemap: Phân cấp tỷ trọng thiệt hại kinh tế từ Châu lục $\to$ Quốc gia).
- **Worksheet #7**: `Sheet_07_Bubble_Scatter` (Bubble Chart: Tương quan Diện tích vs Thiệt hại vs Số người ảnh hưởng, trục Log).
- **Worksheet #8**: `Sheet_08_Combo_Histogram` (Combo Histogram diện tích cháy theo bin logarit + Đường phân vị lũy kế).

### 👤 Thành viên 3: Biểu đồ #9 – #12 (Xếp hạng, Nguyên nhân & Điểm cháy)
- **Worksheet #9**: `Sheet_09_Combo_Pareto` (Combo Pareto Chart: Cột số người chết top 10 quốc gia + Đường % lũy kế 80/20).
- **Worksheet #10**: `Sheet_10_Donut_Cause` (Donut / Sunburst phân tích cơ cấu nguyên nhân: Tự nhiên vs Nhân tạo).
- **Worksheet #11**: `Sheet_11_Sankey_Flow` (Sankey / Bar luồng chuyển giao: Nguyên nhân $\to$ Loại thảm họa $\to$ Mức độ thiệt hại).
- **Worksheet #12**: `Sheet_12_Proportional_Map` (Bản đồ điểm phân bố không gian các đại vụ cháy rừng lớn).

---

## 3. Tạo 4 Dashboards Trong Tableau (D1 – D4)

Nhấn nút **New Dashboard** ở thanh dưới để tạo 4 Dashboard tương ứng với 4 câu hỏi nghiên cứu:

1. **Dashboard D1: Bức tranh 20 năm**
   - **Kích thước**: Fixed size (1200 $\times$ 800 px) hoặc Automatic.
   - **Thành phần**: Header tiêu đề câu hỏi chính + Thẻ KPI Cards + Kéo thả `Sheet_01`, `Sheet_02`, `Sheet_05`.
   - **Tương tác**: Bộ lọc năm dạng Slider gắn cho cả 3 sheet (**Apply to Worksheets $\to$ Selected Worksheets**).
   - **Hộp Insight**: Hộp văn bản (Text Object) ghi phát hiện chính từ số liệu thật.

2. **Dashboard D2: Ở đâu chịu thiệt hại?**
   - **Thành phần**: Kéo thả `Sheet_03`, `Sheet_06`, `Sheet_09`.
   - **Tương tác**: Bộ lọc Châu lục, click vào quốc gia trên bản đồ để highlight biểu đồ Treemap và Pareto.
   - **Hộp Insight**: Tóm tắt các điểm nóng toàn cầu và nguyên lý 80/20.

3. **Dashboard D3: Cháy rừng: Khi nào và lớn cỡ nào?**
   - **Thành phần**: Kéo thả `Sheet_04`, `Sheet_08`, `Sheet_12`.
   - **Tương tác**: Bộ lọc tháng cao điểm, bộ lọc diện tích siêu đám cháy.
   - **Hộp Insight**: Nhận xét chu kỳ tháng 6–9 và tần suất các siêu đám cháy.

4. **Dashboard D4: Vì sao và hệ quả**
   - **Thành phần**: Kéo thả `Sheet_10`, `Sheet_11`, `Sheet_07`.
   - **Tương tác**: Bộ lọc nhóm nguyên nhân tự nhiên / nhân tạo.
   - **Hộp Insight & Kết luận**: Kết luận mối tương quan diện tích vs thiệt hại và khuyến nghị phòng ngừa.

---

## 4. Xây Dựng Tableau Story (Ít Nhất 3 Story Points)

Nhấn nút **New Story** (biểu tượng cuốn sách mở ở thanh dưới cùng) để tạo **Story**:

### 📖 Cấu trúc 4 Story Points hoàn chỉnh:

1. **Story Point 1**: 
   - **Tiêu đề thanh dẫn (Story Navigator)**: `1. Bức tranh 20 năm: Tần suất & Thiệt hại`
   - **Nội dung nhúng**: Kéo thả **Dashboard D1** vào.
   - **Chú thích nổi bật (Caption / Annotation)**: Nêu bật đỉnh điểm năm 2020 và xu hướng thảm họa gia tăng sau chu kỳ 2017.

2. **Story Point 2**:
   - **Tiêu đề thanh dẫn**: `2. Điểm nóng toàn cầu: Nơi chịu tổn thất nặng nề`
   - **Nội dung nhúng**: Kéo thả **Dashboard D2** vào.
   - **Chú thích nổi bật**: Chỉ ra quy luật 80/20 về số người chết và top các quốc gia gánh chịu thiệt hại kinh tế lớn nhất.

3. **Story Point 3**:
   - **Tiêu đề thanh dẫn**: `3. Trọng tâm Cháy rừng: Mùa cao điểm & Siêu đám cháy`
   - **Nội dung nhúng**: Kéo thả **Dashboard D3** vào.
   - **Chú thích nổi bật**: Làm rõ chu kỳ mùa cháy rừng bùng nổ vào mùa khô (tháng 6–9) và sự lan rộng của các đám cháy quy mô $> 10.000$ ha.

4. **Story Point 4**:
   - **Tiêu đề thanh dẫn**: `4. Nguyên nhân & Tác động: Con người vs Tự nhiên`
   - **Nội dung nhúng**: Kéo thả **Dashboard D4** vào.
   - **Chú thích nổi bật**: Tổng kết tỷ trọng do tác nhân con người gây ra, bài toán tương quan phi tuyến giữa diện tích cháy và thiệt hại kinh tế, kèm khuyến nghị chính sách.

---

## 5. Lưu Trữ & Xuất Bản (Export & Publish)

1. **Lưu Workbook đóng gói trong repo**:
   - Chọn menu **File $\to$ Export Packaged Workbook...** (hoặc Save As `.twbx`).
   - Đặt tên: `wildfire_disaster_analysis.twbx`.
   - Lưu vào thư mục: `tableau/wildfire_disaster_analysis.twbx`.
   - *(Định dạng `.twbx` lưu trữ cả cấu trúc biểu đồ lẫn dữ liệu nén, giúp bất kỳ ai tải về đều mở được ngay lập tức)*.

2. **Xuất bản lên Tableau Public**:
   - Chọn menu **Server $\to$ Tableau Public $\to$ Save to Tableau Public As...**
   - Đăng nhập tài khoản Tableau Public.
   - Đặt tên Workbook: `Nghien Cuu Chay Rung Va Tham Hoa Thien Nhien 2006-2025`.
   - Sau khi xuất bản, sao chép đường link công khai (URL) và cập nhật vào `README.md`.

3. **Nhúng vào trang web GitHub Pages**:
   - Mở file `dashboard/index.html`, dán mã nhúng Tableau Public vào vị trí khung hiển thị để trang web tự động tải Story tương tác.
