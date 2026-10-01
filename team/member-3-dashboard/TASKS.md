# NHIỆM VỤ THÀNH VIÊN 3: KỸ SƯ DASHBOARD & TRIỂN KHAI (DATA VISUALIZATION & DEVOPS)

> **Họ và tên**: [TÊN THÀNH VIÊN 3]  
> **MSSV**: [Điền MSSV]  
> **Nhánh Git phụ trách**: `member-3-dashboard`  
> **Trọng tâm**: Xây dựng Dashboard ECharts tương tác, Kiến trúc Cross-filtering, Bảng màu chung, CI/CD GitHub Pages & Báo cáo tổng thể; Thực hiện 4 biểu đồ #9–#12.

---

## 1. Mục Tiêu Chính
1. Thiết kế và phát triển giao diện Dashboard web tĩnh hoàn chỉnh bằng HTML5/CSS3 và JavaScript thuần (Vanilla JS), tích hợp thư viện **Apache ECharts** phiên bản ghim ổn định lưu trữ nội bộ tại `dashboard/js/vendor/` (không phụ thuộc CDN bên ngoài).
2. Tích hợp bản đồ GeoJSON ranh giới các quốc gia thế giới trực tiếp vào repo.
3. Xây dựng hệ thống bộ lọc toàn cục (Global Filters) mạnh mẽ: thanh trượt dải năm (2006–2025), dropdown chọn loại thảm họa, châu lục, quốc gia, nhóm nguyên nhân, nút reset và hàng thẻ KPI đồng bộ dữ liệu tức thời.
4. Triển khai công tắc chuyển đổi: **"Chỉ hiển thị số liệu gốc (Ẩn giá trị ước lượng/điền thiếu)"** dựa trên các cột cờ ML.
5. Xây dựng kiến trúc mô-đun hóa biểu đồ: Cung cấp giao diện kết nối (API) chung để 12 biểu đồ của cả 3 thành viên được nạp độc lập từ `dashboard/js/charts/chart-XX.js`.
6. Triển khai bảng màu chuẩn hóa `dashboard/js/palette.js` theo `docs/COLOR_GUIDE.md` (chuẩn WCAG 2.1 AA, Okabe-Ito, OrRd, RdBu).
7. Thiết lập quy trình tự động hóa CI/CD `.github/workflows/deploy.yml` tự động xuất bản Dashboard lên **GitHub Pages**.
8. Hoàn thiện tài liệu tổng thể: `README.md`, `docs/REPORT_OUTLINE.md`, `docs/DEMO_SCRIPT.md` và tổng hợp phần "Insight & Kết luận" (5–7 phát hiện từ số liệu thật).
9. Hoàn thành 4 biểu đồ được giao (#9, #10, #11, #12) theo đúng đặc tả và bảng màu chuẩn.

---

## 2. Bảng Theo Dõi Trạng Thái Công Việc

| Hạng mục công việc | Trạng thái | Deadline | Ghi chú cá nhân |
|--------------------|------------|----------|-----------------|
| Thiết lập môi trường & nhánh `member-3-dashboard` | Sẵn sàng | Tuần 1 | Giai đoạn 1 |
| Tạo khung giao diện HTML/CSS (Light & Dark) | Chưa bắt đầu | *[Điền]* | Responsive UI |
| Cài đặt vendor Apache ECharts & GeoJSON thế giới | Chưa bắt đầu | *[Điền]* | Copy vào `js/vendor/` |
| Phát triển mô-đun bảng màu `dashboard/js/palette.js` | Chưa bắt đầu | *[Điền]* | Chuẩn Okabe-Ito & OrRd |
| Xây dựng bộ lọc toàn cục & thẻ KPI | Chưa bắt đầu | *[Điền]* | Cross-filter & Công tắc ML |
| Thiết kế kiến trúc nạp biểu đồ mô-đun | Chưa bắt đầu | *[Điền]* | Hỗ trợ 12 chart-XX.js |
| Cấu hình GitHub Actions CI/CD `deploy.yml` | Chưa bắt đầu | *[Điền]* | Deploy GitHub Pages |
| Viết SQL cho biểu đồ #9–#12 trong `queries_for_charts.sql` | Chưa bắt đầu | *[Điền]* | Pareto, Sunburst, Sankey |
| Biểu đồ #9: Combo Pareto Chart (Top 10 tử vong) | Chưa bắt đầu | *[Điền]* | Cột + Đường % lũy kế |
| Biểu đồ #10: Sunburst / Donut nguyên nhân cháy | Chưa bắt đầu | *[Điền]* | Cấu phần nhiều tầng |
| Biểu đồ #11: Sankey Diagram (Nguyên nhân $\to$ Thiệt hại) | Chưa bắt đầu | *[Điền]* | Luồng quan hệ đa chiều |
| Biểu đồ #12: Bản đồ điểm đại thảm họa cháy rừng | Chưa bắt đầu | *[Điền]* | Proportional Symbol Map |
| Hoàn thiện `README.md`, `REPORT_OUTLINE.md`, `DEMO_SCRIPT.md` | Chưa bắt đầu | *[Điền]* | Tổng kết 5–7 phát hiện |

---

## 3. Danh Sách Checklist Chi Tiết

### A. Hạ Tầng Giao Diện & Thư Viện
- [ ] Dựng cấu trúc `dashboard/index.html` với bố cục khoa học, có thanh điều khiển trên cùng (Header & Filter bar), hàng thẻ KPI card, và lưới hiển thị 12 khung biểu đồ (Grid Layout).
- [ ] Soạn thảo `dashboard/css/style.css` hỗ trợ đầy đủ thiết bị (Responsive: Mobile, Tablet, Desktop) và 2 chế độ màu Light / Dark Theme.
- [ ] Chạy lệnh `npm run vendor` để copy thư viện `echarts.min.js` từ `node_modules` vào thư mục `dashboard/js/vendor/`.
- [ ] Bổ sung file GeoJSON bản đồ ranh giới thế giới vào `dashboard/data/world.json`.
- [ ] Viết mô-đun `dashboard/js/palette.js` xuất toàn bộ mã màu chuẩn (Categorical Okabe-Ito, Sequential OrRd, Diverging RdBu) dùng thống nhất cho cả nhóm.

### B. Kiến Trúc Bộ Lọc Toàn Cục & Tương Tác Đồng Bộ
- [ ] Viết `dashboard/js/app.js` quản lý trạng thái ứng dụng (State Management):
  - [ ] Bộ lọc dải thời gian: Slider từ 2006 đến 2025.
  - [ ] Bộ lọc dropdown: Loại thảm họa (Wildfire, Flood, Storm...), Châu lục, Nhóm nguyên nhân.
  - [ ] Nút Reset: Đưa toàn bộ bộ lọc và biểu đồ về trạng thái ban đầu.
  - [ ] Công tắc: "Chỉ hiển thị số liệu gốc (Ẩn giá trị ước lượng/điền thiếu)".
  - [ ] 4 thẻ KPI cards: Tổng số vụ, Tổng thiệt hại USD, Tổng diện tích cháy ha, Tổng số ca tử vong (có hiệu ứng số nhảy đếm tăng dần khi lọc).
  - [ ] Cơ chế kích hoạt vẽ lại (re-render) đồng bộ cho 12 biểu đồ khi có sự kiện lọc hoặc chọn vùng (Cross-filtering/Brush).

### C. Triển Khai CI/CD & Xuất Bản
- [ ] Soạn thảo quy trình GitHub Actions `.github/workflows/deploy.yml`:
  - [ ] Kích hoạt tự động khi có sự kiện `push` lên nhánh `main`.
  - [ ] Kiểm tra và xuất bản trực tiếp thư mục `dashboard/` lên GitHub Pages.
- [ ] Hướng dẫn bật tính năng GitHub Pages trong cài đặt repository nếu tài khoản chưa được kích hoạt tự động.

### D. Báo Cáo & Tài Liệu Hoàn Thiện
- [ ] Viết `README.md` chuyên nghiệp với ảnh chụp màn hình Dashboard, đường link trải nghiệm trực tiếp, kiến trúc pipeline và hướng dẫn chạy lại từ đầu bằng một lệnh.
- [ ] Hoàn thiện dàn ý báo cáo và slide thuyết trình trong `docs/REPORT_OUTLINE.md`.
- [ ] Soạn thảo kịch bản demo thuyết trình chi tiết trong `docs/DEMO_SCRIPT.md`.
- [ ] Tổng hợp 5–7 phát hiện cốt lõi (Key Insights) từ dữ liệu thực tế 20 năm hiển thị nổi bật trên Dashboard.

---

## 4. Các Biểu Đồ Phụ Trách (#9, #10, #11, #12)

### Biểu Đồ #9: Combo Pareto Chart (Top 10 quốc gia tử vong + % Lũy kế)
- [ ] (a) Viết câu truy vấn SQL xếp hạng Top 10 quốc gia theo số người tử vong và tính tỷ lệ % lũy kế trong `sql/queries_for_charts.sql`.
- [ ] (b) Xuất file JSON tương ứng vào `dashboard/data/chart_09_data.json`.
- [ ] (c) Dựng biểu đồ kết hợp Pareto trong `dashboard/js/charts/chart-09.js` với cột đỏ tím cảnh báo và đường lũy kế vàng cam.
- [ ] (d) Gắn tương tác click cột quốc gia để lọc dữ liệu toàn dashboard.
- [ ] (e) Hoàn thiện mục Biểu đồ 9 trong `docs/CHART_SPEC.md` và ghi nhận insight từ dữ liệu thật.

### Biểu Đồ #10: Sunburst / Donut Phân Tích Nguyên Nhân Cháy Rừng
- [ ] (a) Viết câu truy vấn SQL phân cấp 2 tầng: Nhóm nguyên nhân (`cause_group`) $\to$ Chi tiết nguyên nhân (`cause_name`).
- [ ] (b) Xuất file JSON cấu trúc phân cấp vào `dashboard/data/chart_10_data.json`.
- [ ] (c) Dựng biểu đồ Sunburst ECharts trong `dashboard/js/charts/chart-10.js` với bảng màu phân loại nguyên nhân.
- [ ] (d) Gắn tương tác click phóng to thu nhỏ (drill-down) từng phân nhánh.
- [ ] (e) Hoàn thiện mục Biểu đồ 10 trong `docs/CHART_SPEC.md` và ghi nhận insight từ dữ liệu thật.

### Biểu Đồ #11: Sankey Diagram (Dòng chuyển giao Nguyên nhân $\to$ Loại thảm họa $\to$ Mức độ thiệt hại)
- [ ] (a) Viết câu truy vấn SQL tính toán lưu lượng trọng số giữa các nút quan hệ trong `sql/queries_for_charts.sql`.
- [ ] (b) Xuất file JSON gồm danh sách nodes và links vào `dashboard/data/chart_11_data.json`.
- [ ] (c) Dựng biểu đồ Sankey ECharts trong `dashboard/js/charts/chart-11.js` với hiệu ứng màu gradient theo luồng.
- [ ] (d) Gắn tương tác hover highlight toàn bộ đường truyền và kéo thả sắp xếp các node.
- [ ] (e) Hoàn thiện mục Biểu đồ 11 trong `docs/CHART_SPEC.md` và ghi nhận insight từ dữ liệu thật.

### Biểu Đồ #12: Bản Đồ Điểm Các Đại Thảm Họa Cháy Rừng (Proportional Symbol Map)
- [ ] (a) Viết câu truy vấn SQL lấy tọa độ địa lý, diện tích cháy và mức thiệt hại trong `sql/queries_for_charts.sql`.
- [ ] (b) Xuất file JSON tọa độ vào `dashboard/data/chart_12_data.json`.
- [ ] (c) Dựng bản đồ điểm ECharts trên nền GeoJSON thế giới trong `dashboard/js/charts/chart-12.js` (Kích thước = Diện tích, Màu = Thiệt hại).
- [ ] (d) Gắn thanh trượt thời gian động (Timeline Player) và popup chi tiết khi click điểm cháy.
- [ ] (e) Hoàn thiện mục Biểu đồ 12 trong `docs/CHART_SPEC.md` và ghi nhận insight từ dữ liệu thật.

---

## 5. Đầu Vào & Đầu Ra (Deliverables)
- **Đầu vào**:
  - Dữ liệu JSON xuất bản từ `src/06_export_json.py` của TV1 và TV2.
  - Tài liệu quy chuẩn màu sắc `docs/COLOR_GUIDE.md`.
  - GeoJSON thế giới.
- **Đầu ra**:
  - `dashboard/index.html`, `dashboard/css/style.css`, `dashboard/js/app.js`, `dashboard/js/palette.js`.
  - `dashboard/js/charts/chart-09.js`, `chart-10.js`, `chart-11.js`, `chart-12.js`.
  - `.github/workflows/deploy.yml`.
  - `README.md`, `docs/REPORT_OUTLINE.md`, `docs/DEMO_SCRIPT.md`.

---

## 6. Definition of Done (DoD) Cá Nhân
1. Khung Dashboard chạy mượt mà, không có lỗi JavaScript console nào khi tải trang và khi tương tác bộ lọc.
2. Bộ lọc toàn cục và Cross-filtering hoạt động chính xác trên cả 12 biểu đồ.
3. Công tắc ẩn/hiện giá trị ML lọc đúng các bản ghi có cờ ước lượng.
4. Thời gian tải trang ban đầu và nạp toàn bộ biểu đồ dưới 3 giây.
5. GitHub Actions deploy thành công lên GitHub Pages và trang web hiển thị đúng.
