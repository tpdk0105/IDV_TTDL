# Hướng Dẫn Thực Hiện Trực Quan Hóa Trên Tableau Public

> **Đề tài**: "Nghiên cứu – phân tích tần suất và thiệt hại của các trận cháy rừng tại California / Bắc Mỹ trong 20 năm qua (2006–2025)"  
> **Công cụ trực quan hóa**: Tableau Desktop / Tableau Public  
> **Sản phẩm bàn giao**: 
> 1. File workbook đóng gói: `tableau/wildfire_disaster_analysis.twbx`
> 2. Đường link xuất bản trực tuyến: **Tableau Public URL**
> 3. Bản nhúng tương tác trực tiếp trên giao diện web GitHub Pages (`dashboard/index.html`).

---

## 1. Kết Nối Dữ Liệu Vào Tableau

1. Mở **Tableau Desktop** hoặc **Tableau Public App**.
2. Tại mục **Connect** (Kết nối dữ liệu):
   - Chọn **Text file** $\to$ Chọn file dữ liệu đã làm sạch: `data/clean/master_clean.csv` (hoặc kết nối qua SQLite Driver nếu dùng CSDL `database.sqlite`).
3. Đảm bảo các trường dữ liệu nhận đúng kiểu:
   - `alarm_date`, `cont_date`: Kiểu **Date** (Lịch).
   - `latitude`: Kiểu **Geographic Role $\to$ Latitude**.
   - `longitude`: Kiểu **Geographic Role $\to$ Longitude**.
   - `county`: Kiểu **Geographic Role $\to$ County** (thiết lập State: California).
   - `acres_burned`, `burned_area_ha`, `structures_destroyed`, `deaths_direct`: Kiểu **Number (decimal / whole)**.
4. Mở file [tableau/CALCULATED_FIELDS.md](CALCULATED_FIELDS.md) và tạo đầy đủ các trường tính toán cần thiết.

---

## 2. Quy Trình Phân Chia 10 Biểu Đồ Tinh Gọn (Worksheets)

Hệ thống gồm **10 Worksheets** tinh gọn, không rối mắt (chia theo tỷ lệ 2/4/4: TV1 làm 2 biểu đồ, TV2 làm 4 biểu đồ, TV3 làm 4 biểu đồ), gồm **8 biểu đồ cơ bản + 1 biểu đồ kết hợp dự báo 10 năm (2026–2035) + 1 bản đồ địa lý bắt buộc**:

### 👤 Thành viên 1: Biểu đồ #1 – #2 (Data & ML Engineer: 2 Sheets)
- **Worksheet #1**: `Sheet_01_Line_Yearly_Trend` (Line Chart cơ bản: Xu hướng biến động số vụ cháy qua 20 năm 2006–2025, thấy rõ đỉnh 2017 & 2020).
- **Worksheet #2**: `Sheet_02_Combo_Forecast` (Combo Dual-Axis: Cột số vụ + Đường diện tích cháy + **Trend Line hồi quy dự báo 10 năm 2026–2035 đạt Barem 0.5 điểm**).

### 👤 Thành viên 2: Biểu đồ #3 – #6 (Data Modeling & SQL Engineer: 4 Sheets)
- **Worksheet #3**: `Sheet_03_Divergence_Bar` (Diverging Bar quanh 0: Độ lệch số vụ từng năm so với chuẩn 20 năm; cột đỏ vượt chuẩn, cột xanh dưới chuẩn).
- **Worksheet #4**: `Sheet_04_Monthly_Heatmap` (Heatmap / Highlight Table: Ma trận mùa vụ 12 Tháng $\times$ 20 Năm, thấy rõ mùa cháy đỏ rực từ tháng 7–10).
- **Worksheet #5**: `Sheet_05_Pie_Cause_Share` (Pie Chart: Biểu đồ tròn 3 múi tỷ trọng căn nguyên: Con người 36.4%, Sét đánh 20.9%, Khác 42.7%).
- **Worksheet #6**: `Sheet_06_Scatter_County_Risk` (Scatter Plot: Tương quan diện tích vs nhà bị phá hủy vs dân số tập hợp theo **58 Hạt**, không bị đè chấm).

### 👤 Thành viên 3: Biểu đồ #7 – #10 (Dashboard & Storytelling Specialist: 4 Sheets)
- **Worksheet #7**: `Sheet_07_Treemap_Damage` (Treemap 1 tầng: Cơ cấu loại công trình bị thiêu rụi; Single Family Residence chiếm >80%).
- **Worksheet #8**: `Sheet_08_Top10_Counties_Bar` (Horizontal Bar Chart: Cột ngang xếp hạng Top 10 Hạt bị thiệt hại nặng nhất: Butte, Los Angeles, Sonoma...).
- **Worksheet #9**: `Sheet_09_Choropleth_Map` (Geographic Map: Bản đồ phân vùng 58 Hạt California theo thiệt hại - **Bản đồ bắt buộc đạt 0.5 điểm Map của PDF**).
- **Worksheet #10**: `Sheet_10_Stacked_Area_Cause` (Stacked Area Chart: Cơ cấu nguyên nhân biến thiên theo 20 năm 2006–2025).

---

## 3. Tạo 3 Dashboards Tinh Gọn Trong Tableau (D1 – D3)

Nhấn nút **New Dashboard** ở thanh dưới để tạo 3 Dashboard (Kích thước Fixed size 1366 $\times$ 768 px):

1. **Dashboard D1: Bức tranh 20 năm Cháy rừng California & Dự báo** (Xu hướng vĩ mô & Dự báo 2026–2035)
   - **Thành phần**: Header + Kéo thả `Sheet_01` (Line), `Sheet_02` (Combo Forecast 10 năm), `Sheet_03` (Diverging Bar).
   - **Tương tác**: Biểu tượng phễu (*Use as Filter*) trên `Sheet_03` để click vào năm bất kỳ sẽ lọc toàn bộ Dashboard.

2. **Dashboard D2: Không gian địa lý & Phân cấp thiệt hại 58 Hạt** (Địa lý & Điểm nóng)
   - **Thành phần**: Kéo thả `Sheet_09` (Bản đồ 58 Hạt), `Sheet_08` (Top 10 Hạt), `Sheet_07` (Treemap loại công trình).
   - **Tương tác**: Click vào Hạt Butte trên bản đồ `Sheet_09` $\to$ Treemap tự động phóng to cơ cấu loại nhà bị cháy tại Hạt Butte.

3. **Dashboard D3: Mùa vụ, Căn nguyên & Đánh giá rủi ro** (Chi tiết chuyên sâu)
   - **Thành phần**: Bố cục lưới 2x2: `Sheet_04` (Monthly Heatmap), `Sheet_05` (Pie Cause), `Sheet_10` (Stacked Area), `Sheet_06` (Scatter 58 Hạt).
   - **Tương tác**: Lọc theo mùa vụ và nguyên nhân.

---

## 4. Xây Dựng Tableau Story (3 Story Points Trọng Tâm) & Phối Hợp Tuần Tự (TV1 $\to$ TV3)

> **MÔ HÌNH BÀN GIAO TUẦN TỰ GIỮA THÀNH VIÊN 1 VÀ THÀNH VIÊN 3 (BAREM 2.0 ĐIỂM)**:
> 
> Barem môn học quy định **Mục 3. Phân tích Insight & Dự báo (2.0 điểm)** gồm 3 tiêu chí:
> 1. *Mô hình Dự báo (0.5 đ)*: Áp dụng đúng thuật toán Hồi quy tuyến tính (Linear Regression) hoặc Logistic Regression.
> 2. *Trực quan Dự báo (0.5 đ)*: Tích hợp thành công kết quả dự báo lên một biểu đồ trực quan trong Dashboard.
> 3. *Khai phá Insight / Storytelling (1.0 đ)*: Rút ra câu chuyện dẫn dắt có chiều sâu, chỉ ra nguyên nhân, xu hướng.
>
> **Quy trình bàn giao tuần tự**:
> - **Bước 1 (TV1 thực hiện trên Python)**: Huấn luyện Linear Regression trong `src/08_predictive_model.py`, xuất kết quả dự báo ra `data/clean/forecast_results.csv` và bàn giao cho pipeline.
> - **Bước 2 (TV3 tiếp nhận kết quả & dựng trên Dashboard)**: Đưa kết quả dự báo vào **Dashboard D1** (bật đường Trend Line tuyến tính trên `Sheet_01`). Hoàn thành 0.5 đ Trực quan Dự báo.
> - **Bước 3 (TV3 độc lập xây dựng Tableau Story)**: Tự chủ toàn bộ việc thiết kế **3 Story Points**, sử dụng toàn bộ hệ thống biểu đồ và kết quả dự báo của TV1 để dẫn dắt câu chuyện phân tích sâu sắc. Hoàn thành 1.0 đ Khai phá Insight.

Nhấn nút **New Story** (biểu tượng cuốn sách mở ở thanh dưới cùng) để tạo **Story**:

### 📖 Cấu trúc 3 Story Points hoàn chỉnh:

1. **Story Point 1**: 
   - **Tiêu đề thanh dẫn (Story Navigator)**: `1. Bức tranh 20 năm Cháy rừng California: Tần suất & Mức độ khốc liệt`
   - **Nội dung nhúng**: Kéo thả **Dashboard D1** vào (chứa `Sheet_01` với đường xu hướng dự báo của TV1).
   - **Chú thích nổi bật (Caption / Annotation)**: Nêu bật đỉnh điểm năm 2020 (hơn 4.3 triệu Acres) và kết quả dự báo Linear Regression cho thấy xu thế gia tăng diện tích tàn phá.

2. **Story Point 2**:
   - **Tiêu đề thanh dẫn**: `2. Điểm nóng 58 Hạt California: Phân cấp tổn thất 80/20`
   - **Nội dung nhúng**: Kéo thả **Dashboard D2** vào.
   - **Chú thích nổi bật**: Làm nổi bật nguyên lý 80/20: dưới 20% số Hạt (Butte, Sonoma, Shasta...) chiếm hơn 80% tổng số nhà cửa bị thiêu rụi.

3. **Story Point 3**:
   - **Tiêu đề thanh dẫn**: `3. Căn nguyên, Siêu đám cháy & Thách thức Tương lai`
   - **Nội dung nhúng**: Kéo thả **Dashboard D3** vào.
   - **Chú thích nổi bật**: Phân tích các siêu đám cháy $\ge 100.000$ mẫu, tác động của hoạt động con người gần khu dân cư và các bài học phòng ngừa khẩn cấp.

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
   - Đặt tên Workbook: `California Wildfire Disaster Analysis 2006-2025`.
   - Sau khi xuất bản, sao chép đường link công khai (URL) và cập nhật vào `README.md`.

3. **Nhúng vào trang web GitHub Pages**:
   - Mở file `dashboard/index.html`, dán mã nhúng Tableau Public vào vị trí khung hiển thị để trang web tự động tải Story tương tác.
