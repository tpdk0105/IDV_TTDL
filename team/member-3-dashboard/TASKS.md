# NHIỆM VỤ THÀNH VIÊN 3: KỸ SƯ DASHBOARD, TABLEAU STORY & TRIỂN KHAI (DATA VISUALIZATION & DEVOPS)

> **Họ và tên**: [TÊN THÀNH VIÊN 3]  
> **MSSV**: [Điền MSSV]  
> **Nhánh Git phụ trách**: `member-3-dashboard`  
> **Trọng tâm**: Thiết kế 3 Dashboards & Tableau Story (3 Story Points) trên Tableau Public; Phụ trách 4 biểu đồ Tableau #7–#10; Đóng gói file `.twbx`, nhúng vào GitHub Pages & Báo cáo tổng thể IEEE.

---

## 1. Mục Tiêu Chính
1. Cài đặt và thiết lập **Tableau Desktop / Tableau Public App**, kết nối nguồn dữ liệu sạch từ `data/clean/master_clean.csv`.
2. Phụ trách thực hiện 4 Worksheets chuyên sâu của mình: **#7 (Pareto 80/20 Nhà bị phá hủy), #8 (Donut 2 tầng Nguyên nhân), #9 (Choropleth Map 58 Hạt California), #10 (Symbol Map Điểm cháy lớn)**.
3. Thiết kế **3 Dashboards** chuyên đề giải quyết trọn vẹn câu chuyện phân tích:
   - **D1: Bức tranh 20 năm Cháy rừng California** (ghép #1, #2, #3 + KPI Cards + Filter năm + **Đường dự báo Linear Regression**).
   - **D2: Điểm nóng & Phân cấp thiệt hại theo 58 Hạt** (ghép #4, #7, #9 + Filter Hạt/Vùng).
   - **D3: Mùa vụ, Căn nguyên & Siêu đám cháy** (ghép #5, #6, #8, #10 + Filter nguyên nhân & diện tích).
4. Xây dựng **Tableau Story với 3 Story Points** dẫn dắt câu chuyện phân tích logic theo đúng barem yêu cầu, có chú thích Annotation làm nổi bật phát hiện từ dữ liệu thật.
5. Đóng gói và lưu trữ tệp Workbook `tableau/wildfire_disaster_analysis.twbx` vào repo.
6. Xuất bản Workbook lên **Tableau Public** và nhúng mã nhúng tương tác vào `dashboard/index.html`.
7. Duy trì pipeline tự động hóa CI/CD `.github/workflows/deploy.yml` tự động xuất bản Dashboard lên **GitHub Pages**.
8. Hoàn thiện tài liệu tổng thể: `README.md`, `docs/REPORT_OUTLINE.md`, `docs/DEMO_SCRIPT.md`.

---

## 2. Bảng Theo Dõi Trạng Thái Công Việc

| Hạng mục công việc | Trạng thái | Deadline | Ghi chú cá nhân |
|---|---|---|---|
| Thiết lập môi trường & nhánh `member-3-dashboard` | Sẵn sàng | Tuần 1 | Giai đoạn 1 |
| Cấu hình GitHub Actions CI/CD `deploy.yml` | Hoàn thành | Tuần 1 | Deploy GitHub Pages |
| Worksheet #7: `Sheet_07_Combo_Pareto` (Top 10 Hạt bị tàn phá 80/20) | Chưa bắt đầu | *[Điền]* | Cột + Đường % lũy kế |
| Worksheet #8: `Sheet_08_Donut_Cause` (Nguyên nhân 2 tầng) | Chưa bắt đầu | *[Điền]* | Tự nhiên vs Con người |
| Worksheet #9: `Sheet_09_Choropleth_Map` (Bản đồ phân vùng 58 Hạt) | Chưa bắt đầu | *[Điền]* | Bản đồ Map bắt buộc |
| Worksheet #10: `Sheet_10_Proportional_Map` (Bản đồ điểm siêu đám cháy) | Chưa bắt đầu | *[Điền]* | Proportional Symbol Map |
| Thiết kế 3 Dashboards (D1, D2, D3) trên Tableau | Chưa bắt đầu | *[Điền]* | KPI cards + Bộ lọc |
| Dựng Tableau Story với 3 Story Points | Chưa bắt đầu | *[Điền]* | Dẫn dắt cốt truyện + Annotation |
| Lưu file đóng gói `wildfire_disaster_analysis.twbx` | Chưa bắt đầu | *[Điền]* | Lưu vào `tableau/` |
| Xuất bản Tableau Public & nhúng vào `dashboard/` | Chưa bắt đầu | *[Điền]* | Embed mã iframe / API v3 |
| Quay Video Demo & Video Backup tóm tắt (Bắt buộc) | Chưa bắt đầu | *[Điền]* | Gắn link vào báo cáo & README |
| Hoàn thiện `README.md`, `REPORT_OUTLINE.md`, `DEMO_SCRIPT.md` | Chưa bắt đầu | *[Điền]* | Báo cáo chuẩn IEEE $\ge 40$ trang |

---

## 3. Danh Sách Checklist Chi Tiết

### A. Thiết Kế 3 Dashboards Trong Tableau
- [ ] **Dashboard D1 – Bức tranh 20 năm Cháy rừng California**:
  - [ ] Kéo thả `Sheet_01_Combo_Trend`, `Sheet_02_Stacked_Area`, `Sheet_03_Diverging_Bar`.
  - [ ] Thêm 3 thẻ KPI: Tổng số vụ cháy, Tổng diện tích cháy (Acres), Tổng số nhà bị phá hủy.
  - [ ] Thêm bộ lọc dải năm (Slider) áp dụng đồng thời cho cả 3 Sheet.
  - [ ] **Trực quan hóa Dự báo trên Dashboard D1 (0.5 đ barem)**: Nhận kết quả mô hình dự báo từ TV1, hiển thị đường **Trend Line (Linear Regression)** trên `Sheet_01_Combo_Trend` thể hiện rõ xu thế diện tích tàn phá.
  - [ ] Thêm hộp văn bản Insight tóm tắt xu hướng 20 năm và cảnh báo từ mô hình dự báo.
- [ ] **Dashboard D2 – Điểm nóng & Phân cấp thiệt hại theo 58 Hạt**:
  - [ ] Kéo thả `Sheet_04_Treemap_Damage`, `Sheet_07_Combo_Pareto`, `Sheet_09_Choropleth_Map`.
  - [ ] Thêm bộ lọc Hạt / Vùng địa lý; gán Filter Action click Hạt trên bản đồ để highlight Treemap và Pareto.
  - [ ] Thêm hộp văn bản Insight tóm tắt nguyên lý 80/20 về nhà cửa bị phá hủy.
- [ ] **Dashboard D3 – Mùa vụ, Căn nguyên & Siêu đám cháy**:
  - [ ] Kéo thả `Sheet_05_Bubble_Scatter`, `Sheet_06_Combo_Histogram`, `Sheet_08_Donut_Cause`, `Sheet_10_Proportional_Map`.
  - [ ] Thêm bộ lọc nhóm nguyên nhân và quy mô diện tích siêu đám cháy.
  - [ ] Thêm hộp văn bản Insight tóm tắt căn nguyên con người vs tự nhiên và các bài học can thiệp.

### B. Xây Dựng Tableau Story & Khai Phá Insight (Storytelling - 1.0 Điểm Barem)
- [ ] Tạo Story mới trong Tableau với bố cục thanh điều hướng Story Navigator rõ ràng.
- [ ] **Story Point 1**: Nhúng Dashboard D1 $\to$ Tiêu đề: *"1. Bức tranh 20 năm Cháy rừng California: Tần suất & Mức độ khốc liệt"* $\to$ Gắn Annotation tại năm 2020 và chú thích đường dự báo tương lai của TV1.
- [ ] **Story Point 2**: Nhúng Dashboard D2 $\to$ Tiêu đề: *"2. Điểm nóng 58 Hạt California: Phân cấp tổn thất 80/20"* $\to$ Gắn Annotation đường 80% Pareto và làm nổi bật Hạt Butte, Sonoma.
- [ ] **Story Point 3**: Nhúng Dashboard D3 $\to$ Tiêu đề: *"3. Căn nguyên, Siêu đám cháy & Thách thức Tương lai"* $\to$ Gắn Annotation siêu đám cháy $\ge 100.000$ mẫu và căn nguyên do thiết bị/điện của con người.

### C. Xuất Bản & Nhúng Lên Web
- [ ] Lưu file `tableau/wildfire_disaster_analysis.twbx`.
- [ ] Đăng tải lên tài khoản Tableau Public.
- [ ] Nhúng mã nhúng tương tác vào `dashboard/index.html`.
- [ ] Kiểm tra hiển thị trang web trên GitHub Pages.

---

## 4. Các Biểu Đồ Phụ Trách (4 Worksheets: #7, #8, #9, #10 trên Tableau)

### Worksheet #7: `Sheet_07_Combo_Pareto` (Top 10 Hạt bị tàn phá 80/20)
- [ ] (a) Lọc Top 10 `[county]` theo `SUM([structures_destroyed])`, sắp xếp giảm dần.
- [ ] (b) Trục 1: `SUM([structures_destroyed])` (Marks: Bar); Trục 2: `[Cumulative Destroyed %]` (Marks: Line, Dual Axis).
- [ ] (c) Thêm Reference Line tại mốc 80% (0.8); định dạng màu đỏ mận và cam nhấn.

### Worksheet #8: `Sheet_08_Donut_Cause` (Donut 2 tầng nguyên nhân cháy)
- [ ] (a) Dựng Donut 2 tầng: Vòng trong `[Cause Group High Level]`, vòng ngoài `[cause_name]`.
- [ ] (b) Định dạng màu: Tự nhiên (Xanh lá), Con người (Đỏ cam), Khác (Xám).

### Worksheet #9: `Sheet_09_Choropleth_Map` (Bản đồ phân vùng 58 Hạt California)
- [ ] (a) Kéo `[Longitude]` và `[Latitude]` vào Columns/Rows; kéo `[county]` vào Detail; chọn Marks: Map.
- [ ] (b) Kéo `SUM([structures_destroyed])` vào Color với dải tuần tự Orange-Red.

### Worksheet #10: `Sheet_10_Proportional_Map` (Bản đồ điểm các đại vụ cháy lớn)
- [ ] (a) Kéo `[longitude]` vào Columns, `[latitude]` vào Rows; chọn Marks: Circle.
- [ ] (b) Kéo `[acres_burned]` vào Size; kéo `[structures_destroyed]` vào Color (Đỏ cam, Opacity = 70%).
- [ ] (c) Kéo `[fire_name]` vào Detail và Tooltip.
