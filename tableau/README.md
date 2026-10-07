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
   - `acres_burned`, `burned_area_ha`, `structures_destroyed`, `damage_property_usd`, `deaths_direct`: Kiểu **Number (decimal / whole)**.
4. Mở file [tableau/CALCULATED_FIELDS.md](CALCULATED_FIELDS.md) và tạo đầy đủ các trường tính toán cần thiết.

---

## 2. Quy Trình Phân Chia 10 Biểu Đồ (Worksheets)

Hệ thống gồm **10 Worksheets** (được chia theo tỷ lệ 2/4/4: TV1 làm 2 biểu đồ, TV2 làm 4 biểu đồ, TV3 làm 4 biểu đồ), đặt tên Sheet theo quy ước: `Sheet_01`, `Sheet_02`... để quản lý đồng bộ.

### 👤 Thành viên 1: Biểu đồ #1 – #2 (Data & ML Engineer: 2 Sheets)
> *Ghi chú*: TV1 phụ trách 2 biểu đồ để tập trung toàn lực vào Pipeline xử lý dữ liệu và Xây dựng Mô hình dự báo Linear/Logistic Regression.
- **Worksheet #1**: `Sheet_01_Combo_Trend` (Combo Dual-Axis: Cột số vụ cháy + Đường diện tích cháy Acres theo năm 2006–2025; **tích hợp đường Trend Line Forward 10 năm dự báo 2026–2035 đạt tiêu chí Barem 0.5 điểm**).
- **Worksheet #2**: `Sheet_02_Stacked_Area` (Stacked Area: Cơ cấu nguyên nhân cháy theo thời gian 2006–2025).

### 👤 Thành viên 2: Biểu đồ #3 – #6 (Data Modeling & SQL Engineer: 4 Sheets)
- **Worksheet #3**: `Sheet_03_Diverging_Bar` (Cột phân kỳ: Chênh lệch số vụ cháy của từng năm so với trung bình chuẩn 20 năm, tâm = 0).
- **Worksheet #4**: `Sheet_04_Treemap_Damage` (Treemap: Phân cấp tỷ trọng nhà cửa bị phá hủy từ Hạt $\to$ Loại công trình).
- **Worksheet #5**: `Sheet_05_Bubble_Scatter` (Bubble Chart: Tương quan Diện tích cháy vs Số nhà phá hủy vs Thương vong, trục Log-Log).
- **Worksheet #6**: `Sheet_06_Combo_Histogram` (Combo Histogram diện tích cháy theo bin logarit + Đường phân vị lũy kế).

### 👤 Thành viên 3: Biểu đồ #7 – #10 (Dashboard & Storytelling Specialist: 4 Sheets)
- **Worksheet #7**: `Sheet_07_Combo_Pareto` (Combo Pareto Chart: Cột số nhà bị phá hủy top 10 Hạt + Đường % lũy kế 80/20).
- **Worksheet #8**: `Sheet_08_Donut_Cause` (Donut 2 tầng phân tích cơ cấu nguyên nhân: Tự nhiên vs Con người).
- **Worksheet #9**: `Sheet_09_Choropleth_Map` (Bản đồ phân vùng 58 Hạt California theo mức độ thiệt hại/số nhà bị cháy - Map #1).
- **Worksheet #10**: `Sheet_10_Proportional_Map` (Bản đồ điểm phân bố không gian các đại vụ cháy lớn California - Map #2).

---

## 3. Tạo 3 Dashboards Trong Tableau (D1 – D3)

Nhấn nút **New Dashboard** ở thanh dưới để tạo 3 Dashboard tương ứng với 3 câu hỏi nghiên cứu:

1. **Dashboard D1: Bức tranh 20 năm Cháy rừng California** (Xu hướng vĩ mô & Dự báo)
   - **Kích thước**: Fixed size (1200 $\times$ 800 px) hoặc Automatic.
   - **Thành phần**: Header tiêu đề + Thẻ KPI Cards (Tổng số vụ, Tổng diện tích cháy, Tổng nhà phá hủy) + Kéo thả `Sheet_01` (TV1), `Sheet_02` (TV1), `Sheet_03` (TV2).
   - **Tương tác**: Bộ lọc năm dạng Slider gắn cho cả 3 sheet (**Apply to Worksheets $\to$ Selected Worksheets**).
   - **Tích hợp Dự báo**: Thể hiện rõ đường Trend Line Forward 10 năm (2026–2035) kèm dải tin cậy 95% trên `Sheet_01`.
   - **Hộp Insight**: Tóm tắt xu hướng 20 năm và xu hướng dự báo thiệt hại trong tương lai.

2. **Dashboard D2: Điểm nóng & Phân cấp thiệt hại theo 58 Hạt** (Không gian & Nguyên lý 80/20)
   - **Thành phần**: Kéo thả `Sheet_04` (TV2), `Sheet_07` (TV3), `Sheet_09` (TV3).
   - **Tương tác**: Bộ lọc Hạt / Vùng, click vào Hạt trên bản đồ để highlight biểu đồ Treemap và Pareto.
   - **Hộp Insight**: Tóm tắt các điểm nóng 58 Hạt và sự tập trung theo nguyên lý 80/20.

3. **Dashboard D3: Mùa vụ, Căn nguyên & Siêu đám cháy** (Chi tiết chuyên sâu)
   - **Thành phần**: Kéo thả `Sheet_05` (TV2), `Sheet_06` (TV2), `Sheet_08` (TV3), `Sheet_10` (TV3).
   - **Tương tác**: Bộ lọc nguyên nhân, bộ lọc quy mô diện tích siêu đám cháy (>100.000 Acres).
   - **Hộp Insight & Kết luận**: Kết luận mối tương quan diện tích vs phá hủy công trình, tác nhân con người vs sấm sét và khuyến nghị phòng ngừa.

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
