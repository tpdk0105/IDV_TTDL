# Dàn Ý Báo Cáo & Slide Thuyết Trình (REPORT OUTLINE & SLIDES)

> **Người phụ trách**: Thành viên 3 - Kỹ sư Dashboard & Báo cáo  
> **Trạng thái**: Khung dàn ý báo cáo đồ án và cấu trúc bài thuyết trình (Giai đoạn 1)

---

## Phần A: Cấu Trúc Báo Cáo Khoa Học Bắt Buộc (Chuẩn IEEE, Tối Thiểu 40 Trang)

Theo yêu cầu chính thức của môn học Tương tác Dữ liệu Trực quan (IDV), báo cáo đồ án được trình bày theo cấu trúc khoa học (định dạng IEEE, tối thiểu 40 trang) gồm 7 phần bắt buộc sau:

### 1. Giới Thiệu Đề Tài & Mô Tả Tập Dữ Liệu
- **1.1. Bối cảnh & Mục tiêu nghiên cứu**: Bài toán phân tích tần suất, diện tích rừng bị thiêu rụi và thiệt hại nhà cửa/sinh mạng của các trận cháy rừng tại California giai đoạn 20 năm qua (2006–2025).
- **1.2. Khảo sát nguồn dữ liệu thực tế**: Dẫn nguồn & minh chứng hợp lệ từ 5 nguồn dữ liệu uy tín của chính quyền California và Liên bang Hoa Kỳ (CAL FIRE FRAP, CAL FIRE DINS, USDA Forest Service & NIFC ICS-209-PLUS, NOAA NCEI Storm Events, US Census Bureau / CA Dept of Finance Demographics). Đảm bảo bao phủ liên tục 20/20 năm (2006–2025), quy mô hơn 140.000 bản ghi thô và kiến trúc đa bảng Star Schema ($\ge 3$ bảng).
- **1.3. Từ điển dữ liệu (Data Dictionary)**: Mô tả chi tiết từng thuộc tính, ý nghĩa nghiệp vụ và kiểu dữ liệu chuẩn hóa.

### 2. Quy Trình Tiền Xử Lý & Khám Phá Dữ Liệu (EDA)
- **2.1. Quy trình xử lý (Pipeline) rõ ràng**: Sơ đồ kiến trúc luồng dữ liệu viết bằng Python/R.
- **2.2. Khám phá dữ liệu (EDA) bằng thư viện biểu đồ tĩnh**: Dùng **Matplotlib** và **Seaborn** vẽ tối thiểu **3 – 5 biểu đồ tĩnh** (phân phối Histogram/KDE diện tích cháy, ngoại lai sơ bộ Boxplot, bản đồ nhiệt tương quan Heatmap, ma trận khuyết thiếu) trước khi đưa dữ liệu lên Dashboard.
- **2.3. Làm sạch dữ liệu triệt để**:
  - Xử lý thiếu (Missing Values): KNN Imputer / Iterative Imputer (MICE) gắn cờ `<col>_is_imputed`.
  - Xử lý ngoại lai (Outliers): Mô hình không giám sát **Isolation Forest** & LOF gắn cờ `is_outlier_ml`.
  - Chuẩn hóa định dạng ngày tháng, chuỗi, mã FIPS, tên 58 Hạt California, tọa độ địa lý (Bounding Box California: vĩ độ $32^{\circ}$–$42^{\circ}$N, kinh độ $-125^{\circ}$–$-114^{\circ}$W) và đơn vị diện tích (Acres và Ha).
- **2.4. Biến đổi dữ liệu (Data Transformation) & Tạo Calculated Fields**:
  - Tạo các trường dữ liệu tính toán mới có ý nghĩa (phân loại đám cháy Megafire, chu kỳ mùa, log scale, Pareto lũy kế...).
  - Thiết kế Star Schema (3NF) và kết nối/phân rã bảng chính xác trong CSDL SQLite.

### 3. Thiết Kế Dashboard & Luồng Tương Tác
- **3.1. Bố cục (Layout) & Trải nghiệm người dùng (UI/UX)**: Bố cục hợp lý, màu sắc hài hòa (WCAG AA, dải màu Okabe-Ito, OrRd), có tiêu đề và chú thích (Legend) rõ ràng.
- **3.2. Hệ thống biểu đồ đa dạng**: Hệ thống 10 biểu đồ gồm **9 loại biểu đồ hoàn toàn khác nhau** (vượt chuẩn tối thiểu 8 loại của môn học): Dual-Axis Combo Bar+Line, Stacked Area, Diverging Bar, Treemap, Bubble Scatter Log-Log, Combo Histogram, Combo Pareto 80/20, Donut 2 tầng, và **2 Bản đồ địa lý bắt buộc (Map)**: Choropleth Map (58 Hạt California) và Proportional Symbol Map (các đại vụ cháy lớn).
- **3.3. Tính tương tác cao**: Bộ lọc đa cấp (Multi-level Filters), Đi sâu chi tiết (Drill-down), Tooltip khi hover chuột, và Tương tác liên kết giữa các biểu đồ (Cross-filtering / Filter Actions).
- **3.4. Giải thích ý nghĩa từng biểu đồ**: Lý do chọn biểu đồ, trục đo và câu hỏi quản lý rủi ro mà biểu đồ giải quyết.

### 4. Khai Phá Insight & Kể Chuyện Dữ Liệu (Storytelling - 1.0 Điểm Barem) *(Thành viên 3 độc lập chủ trì)*
- **4.1. Cốt truyện phân tích (Tableau Story với 3 Story Points trọng tâm)**: Thành viên 3 độc lập dẫn dắt logic người xem qua 3 chủ đề xuyên suốt:
  - *Point 1*: Bức tranh 20 năm California & Dự báo xu thế gia tăng khốc liệt.
  - *Point 2*: Điểm nóng 58 Hạt California & Phân cấp tổn thất nhà cửa theo nguyên lý 80/20.
  - *Point 3*: Căn nguyên kích hoạt (Tự nhiên vs Con người), Siêu đám cháy Megafires & Thách thức tương lai.
- **4.2. Phân tích nguyên nhân và xu hướng từ Dashboard**: Rút ra bài học sâu sắc từ số liệu thật 2006–2025, giải thích nguyên nhân đằng sau các biến động thay vì chỉ mô tả biểu đồ.
- **4.3. Đề xuất giải pháp và khuyến nghị chính sách dựa trên dữ liệu**.

### 5. Mô Hình Dự Báo & Trực Quan Hóa (Predictive Model - 1.0 Điểm Barem)
- **5.1. Thuật toán dự báo trên Python (0.5 đ barem - Thành viên 1 thực hiện)**: 
  - Thành viên 1 áp dụng thuật toán **Hồi quy tuyến tính (Linear Regression)** dự báo xu hướng diện tích cháy rừng / tổn thất theo thời gian hoặc **Hồi quy Logistic** phân lớp rủi ro siêu thảm họa bằng thư viện `scikit-learn`.
  - Đánh giá hiệu năng mô hình ($R^2$, MAE, RMSE đối với Linear; Accuracy, Precision, Recall, F1 đối với Logistic).
  - Xuất bảng kết quả dự báo `forecast_results.csv` bàn giao cho pipeline.
- **5.2. Trực quan hóa kết quả dự báo trên Dashboard (0.5 đ barem - Thành viên 3 thực hiện)**:
  - Thành viên 3 nhận kết quả dự báo của TV1, trực tiếp cấu hình đường xu hướng dự báo (**Trend Line / Forecast**) lên Dashboard D1 (trên `Sheet_01_Combo_Trend`).
  - Lồng ghép đường dự báo vào Story Point 1 để hoàn thiện câu chuyện phân tích.

### 6. Hướng Dẫn Cài Đặt / Sử Dụng & Link Video Demo
- **6.1. Hướng dẫn cài đặt và tái lập môi trường**: Mã nguồn tái lập (`requirements.txt`, script `src/`).
- **6.2. Hướng dẫn sử dụng Dashboard**: Thao tác tương tác với các bộ lọc và xem các điểm Story.
- **6.3. Link Video Demo (Bắt buộc có Video backup tóm tắt)**: Kịch bản demo lôi cuốn, đóng vai trò như một Data Analyst trình bày với cấp trên/khách hàng.

### 7. Kết Luận & Tài Liệu Tham Khảo (Chuẩn IEEE)
- **7.1. Tóm tắt kết quả đạt được và bài học kinh nghiệm**.
- **7.2. Hạn chế của đề tài & hướng phát triển tương lai**.
- **7.3. Danh mục tài liệu tham khảo theo định dạng chuẩn khoa học IEEE**.

---

## Phần B: Cấu Trúc Slide Thuyết Trình (15–20 Phút)

| Slide # | Tiêu đề Slide | Nội dung trọng tâm | Người trình bày dự kiến |
|---------|---------------|-------------------|--------------------------|
| 1 | Trang bìa & Giới thiệu nhóm | Tên đề tài California Wildfires 2006–2025, Giảng viên hướng dẫn, Danh sách 3 thành viên | Trưởng nhóm |
| 2 | Đặt vấn đề & Bối cảnh 20 năm | Sự bùng nổ thảm họa cháy rừng California, mục tiêu và phạm vi | Thành viên 1 |
| 3 | Nguồn dữ liệu & Hợp nhất 20 năm | 5 tập dữ liệu thô (FRAP, DINS, ICS-209, NOAA, Census), hợp nhất liên tục 20/20 năm | Thành viên 1 |
| 4 | Làm sạch thông minh bằng ML | Isolation Forest phát hiện ngoại lai, MICE/KNN điền thiếu | Thành viên 1 |
| 5 | Mô hình Dữ liệu Star Schema | Sơ đồ ERD (dim_county, dim_date, fact_fire_incident, fact_structure_damage) | Thành viên 2 |
| 6 | Tối ưu hóa truy vấn & Pipeline CI/CD | Các câu truy vấn SQL phân tích, export dữ liệu và kiểm thử tự động | Thành viên 2 |
| 7 | Tổng quan Dashboard & Nguyên tắc màu | Giao diện tổng thể 3 Dashboards, bảng màu Okabe-Ito, chuẩn tương phản | Thành viên 3 |
| 8–11 | Trực quan hóa chuyên sâu 10 biểu đồ | Điểm nhấn 3 Dashboards: D1 (Xu hướng & Dự báo), D2 (58 Hạt & Pareto 80/20), D3 (Căn nguyên & Megafires) | TV1, TV2, TV3 |
| 12 | Live Demo Dashboard & Story | Thao tác chuyển 3 Story Points, filter đa chiều, brush, drill-down thực tế | Thành viên 3 |
| 13 | 5 Phát Hiện Lớn Nhất (Key Insights) | Xu hướng gia tăng, điểm nóng 58 Hạt (80/20), tác nhân con người vs sấm sét, megafires | Cả nhóm |
| 14 | Hạn chế dữ liệu & Bài học kinh nghiệm | Thách thức hợp nhất dữ liệu lịch sử và giải pháp kỹ thuật | Cả nhóm |
| 15 | Q&A / Cảm ơn | Tiếp nhận câu hỏi phản biện từ Hội đồng chấm thi | Cả nhóm |
