# NHIỆM VỤ THÀNH VIÊN 3: KỸ SƯ DASHBOARD, TABLEAU STORY & TRIỂN KHAI (DATA VISUALIZATION & DEVOPS)

> **Họ và tên**: [TÊN THÀNH VIÊN 3]  
> **MSSV**: [Điền MSSV]  
> **Nhánh Git phụ trách**: `member-3-dashboard`  
> **Trọng tâm**: Thiết kế 4 Dashboard & Tableau Story (4 Story Points) trên Tableau Public; Phụ trách 4 biểu đồ Tableau #9–#12; Đóng gói file `.twbx`, nhúng vào GitHub Pages & Báo cáo tổng thể.

---

## 1. Mục Tiêu Chính
1. Cài đặt và thiết lập **Tableau Desktop / Tableau Public App**, kết nối nguồn dữ liệu sạch từ `data/clean/master_clean.csv`.
2. Phụ trách thực hiện 4 Worksheets chuyên sâu của mình: **#7 (Pareto Top 10), #8 (Donut Nguyên nhân), #9 (Choropleth Map Thế giới), #10 (Symbol Map Điểm cháy lớn)**.
3. Thiết kế **3 Dashboards** chuyên đề giải quyết trọn vẹn câu chuyện phân tích:
   - **D1: Bức tranh 20 năm** (ghép #1, #2, #3 + KPI Cards + Filter năm).
   - **D2: Điểm nóng & Phân cấp thiệt hại** (ghép #4, #7, #9 + Filter châu lục).
   - **D3: Cháy rừng: Mùa vụ, Quy mô & Tác nhân** (ghép #5, #6, #8, #10 + Filter nguyên nhân & tháng).
4. Xây dựng **Tableau Story với 3 Story Points** dẫn dắt câu chuyện phân tích logic theo đúng barem yêu cầu (ít nhất 3 Story Points), có chú thích Annotation làm nổi bật phát hiện từ dữ liệu thật.
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
| Worksheet #7: Combo Pareto Chart (Top 10 tử vong) | Chưa bắt đầu | *[Điền]* | Cột + Đường % lũy kế |
| Worksheet #8: Donut / Sunburst nguyên nhân cháy | Chưa bắt đầu | *[Điền]* | Tự nhiên vs Nhân tạo |
| Worksheet #9: Bản đồ phân vùng Choropleth toàn cầu | Chưa bắt đầu | *[Điền]* | Bản đồ Map bắt buộc |
| Worksheet #10: Bản đồ điểm đại thảm họa cháy rừng | Chưa bắt đầu | *[Điền]* | Proportional Symbol Map |
| Thiết kế 3 Dashboards (D1, D2, D3) trên Tableau | Chưa bắt đầu | *[Điền]* | KPI cards + Bộ lọc |
| Dựng Tableau Story với 3 Story Points | Chưa bắt đầu | *[Điền]* | Dẫn dắt cốt truyện + Annotation |
| Lưu file đóng gói `wildfire_disaster_analysis.twbx` | Chưa bắt đầu | *[Điền]* | Lưu vào `tableau/` |
| Xuất bản Tableau Public & nhúng vào `dashboard/` | Chưa bắt đầu | *[Điền]* | Embed mã iframe / API v3 |
| Quay Video Demo & Video Backup tóm tắt (Bắt buộc) | Chưa bắt đầu | *[Điền]* | Gắn link vào báo cáo & README |
| Hoàn thiện `README.md`, `REPORT_OUTLINE.md`, `DEMO_SCRIPT.md` | Chưa bắt đầu | *[Điền]* | Báo cáo chuẩn IEEE $\ge 40$ trang |

---

## 3. Danh Sách Checklist Chi Tiết

### A. Thiết Kế 3 Dashboards Trong Tableau
- [ ] **Dashboard D1 – Bức tranh 20 năm**:
  - [ ] Kéo thả `Sheet_01_Combo_Trend`, `Sheet_02_Stacked_Area`, `Sheet_03_Diverging_Bar`.
  - [ ] Thêm 3 thẻ KPI: Tổng số sự kiện, Tổng thiệt hại USD, Tổng diện tích rừng cháy.
  - [ ] Thêm bộ lọc dải năm (Slider) áp dụng đồng thời cho cả 3 Sheet.
  - [ ] Thêm hộp văn bản Insight tóm tắt xu hướng 20 năm.
- [ ] **Dashboard D2 – Điểm nóng & Phân cấp thiệt hại**:
  - [ ] Kéo thả `Sheet_04_Treemap_Damage`, `Sheet_07_Combo_Pareto`, `Sheet_09_Choropleth_Map`.
  - [ ] Thêm bộ lọc Châu lục; gán Filter Action click bản đồ highlight các sheet còn lại.
  - [ ] Thêm hộp văn bản Insight tóm tắt nguyên lý 80/20.
- [ ] **Dashboard D3 – Cháy rừng: Mùa vụ, Quy mô & Tác nhân**:
  - [ ] Kéo thả `Sheet_05_Bubble_Scatter`, `Sheet_06_Combo_Histogram`, `Sheet_08_Donut_Cause`, `Sheet_10_Proportional_Map`.
  - [ ] Thêm bộ lọc nhóm nguyên nhân và quy mô diện tích.
  - [ ] Thêm hộp văn bản Insight tóm tắt căn nguyên và khuyến nghị.

### B. Xây Dựng Tableau Story (3 Story Points Trọng Tâm)
- [ ] Tạo Story mới trong Tableau với bố cục thanh điều hướng Story Navigator dạng Text Boxes hoặc Numbers.
- [ ] **Story Point 1**: Nhúng Dashboard D1 $\to$ Tiêu đề: *"1. Bức tranh 20 năm: Tần suất & Thiệt hại"* $\to$ Gắn Annotation tại năm 2020.
- [ ] **Story Point 2**: Nhúng Dashboard D2 $\to$ Tiêu đề: *"2. Điểm nóng toàn cầu: Phân cấp tổn thất 80/20"* $\to$ Gắn Annotation đường 80% Pareto.
- [ ] **Story Point 3**: Nhúng Dashboard D3 $\to$ Tiêu đề: *"3. Trọng tâm Cháy rừng: Quy mô, Căn nguyên & Dự báo"* $\to$ Gắn Annotation đám cháy $\ge 10.000$ ha và tác nhân con người.

### C. Xuất Bản & Nhúng Lên Web
- [ ] Chọn **File $\to$ Export Packaged Workbook...** $\to$ Lưu file `tableau/wildfire_disaster_analysis.twbx`.
- [ ] Chọn **Server $\to$ Tableau Public $\to$ Save to Tableau Public As...** $\to$ Đăng tải lên trang cá nhân Tableau Public.
- [ ] Nhúng mã nhúng tương tác vào `dashboard/index.html`.
- [ ] Kiểm tra hiển thị trang web trên GitHub Pages.

---

## 4. Các Biểu Đồ Phụ Trách (4 Worksheets: #7, #8, #9, #10 trên Tableau)

### Worksheet #7: `Sheet_07_Combo_Pareto` (Combo Pareto Chart: Top 10 tử vong)
- [ ] (a) Lọc Top 10 `[country_name]` theo `SUM([deaths])`, sắp xếp giảm dần.
- [ ] (b) Trục 1: `SUM([deaths])` (Marks: Bar); Trục 2: `[Cumulative Death %]` (Marks: Line, Dual Axis).
- [ ] (c) Thêm Reference Line tại mốc 80% (0.8); định dạng màu đỏ mận và cam nhấn.
- [ ] (d) Ghi nhận insight từ dữ liệu thật vào `docs/CHART_SPEC.md` để đưa vào Story Point 2.

### Worksheet #8: `Sheet_08_Donut_Cause` (Donut / Sunburst nguyên nhân cháy rừng)
- [ ] (a) Dựng Donut 2 tầng: Vòng trong `[Cause Group High Level]`, vòng ngoài `[cause_name]`.
- [ ] (b) Định dạng màu sắc: Tự nhiên (Xanh lá), Con người (Đỏ cam), Khác (Xám).
- [ ] (c) Định dạng Tooltip hiển thị tỷ lệ % của từng tác nhân cụ thể.
- [ ] (d) Ghi nhận insight từ dữ liệu thật vào `docs/CHART_SPEC.md` để đưa vào Story Point 3.

### Worksheet #9: `Sheet_09_Choropleth_Map` (Choropleth Map Toàn cầu: Thiệt hại / Số vụ theo quốc gia)
- [ ] (a) Kéo `[Longitude]` và `[Latitude]` vào Columns/Rows; kéo `[iso3]` vào Detail; chọn Marks: Map.
- [ ] (b) Kéo `SUM([Damage Bil USD])` vào Color với dải tuần tự Orange-Red.
- [ ] (c) Định dạng Tooltip hiển thị tên quốc gia, tổng số vụ thảm họa và tổng thiệt hại tài chính.
- [ ] (d) Ghi nhận insight từ dữ liệu thật vào `docs/CHART_SPEC.md` để đưa vào Story Point 2.

### Worksheet #10: `Sheet_10_Proportional_Map` (Bản đồ điểm các đại vụ cháy lớn)
- [ ] (a) Lọc `[disaster_type] = 'Wildfire'`; kéo `[longitude]` vào Columns, `[latitude]` vào Rows.
- [ ] (b) Chọn Marks: Circle; kéo `[burned_area_ha]` vào Size, kéo `[damage_usd]` vào Color.
- [ ] (c) Đặt Opacity 70% để nhìn xuyên điểm chồng lấp; Tooltip hiển thị tên vụ cháy, ngày giờ, diện tích và thiệt hại.
- [ ] (d) Ghi nhận insight từ dữ liệu thật vào `docs/CHART_SPEC.md` để đưa vào Story Point 3.

---

## 5. Đầu Vào & Đầu Ra (Deliverables)
- **Đầu vào**:
  - `data/clean/master_clean.csv` từ Thành viên 1 và bảng phân rã từ TV2.
  - Tài liệu quy chuẩn màu sắc `docs/COLOR_GUIDE.md` và công thức tính toán `tableau/CALCULATED_FIELDS.md`.
  - 2 Worksheets của TV1 (#1, #2) và 4 Worksheets của TV2 (#3..#6).
- **Đầu ra**:
  - 4 Worksheets của TV3 (#7..#10).
  - 3 Dashboards (D1, D2, D3) trên Tableau.
  - 1 Tableau Story với 3 Story Points hoàn chỉnh.
  - File đóng gói `tableau/wildfire_disaster_analysis.twbx`.
  - Liên kết xuất bản trực tuyến Tableau Public.
  - `dashboard/index.html` (nhúng Tableau Story) và triển khai GitHub Pages.
  - `README.md`, `docs/REPORT_OUTLINE.md`, `docs/DEMO_SCRIPT.md`.

---

## 6. Definition of Done (DoD) Cá Nhân
1. 4 Worksheets Tableau (#7–#10) hoạt động mượt mà, đúng dữ liệu và bảng màu.
2. 3 Dashboards (D1 $\to$ D3) được bố cục chuẩn mực, bộ lọc và KPI cards đồng bộ.
3. Tableau Story có 3 Story Points dẫn dắt câu chuyện mạch lạc.
4. Tệp Workbook đóng gói `wildfire_disaster_analysis.twbx` mở lên bình thường mà không đòi hỏi kết nối ngoài.
5. Bản nhúng trên `dashboard/index.html` hiển thị trơn tru trên GitHub Pages.
