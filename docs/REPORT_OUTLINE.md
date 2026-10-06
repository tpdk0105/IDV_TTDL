# Dàn Ý Báo Cáo & Slide Thuyết Trình (REPORT OUTLINE & SLIDES)

> **Người phụ trách**: Thành viên 3 - Kỹ sư Dashboard & Báo cáo  
> **Trạng thái**: Khung dàn ý báo cáo đồ án và cấu trúc bài thuyết trình (Giai đoạn 1)

---

## Phần A: Cấu Trúc Báo Cáo Khoa Học Bắt Buộc (Chuẩn IEEE, Tối Thiểu 40 Trang)

Theo yêu cầu chính thức của môn học Tương tác Dữ liệu Trực quan (IDV), báo cáo đồ án được trình bày theo cấu trúc khoa học (định dạng IEEE, tối thiểu 40 trang) gồm 7 phần bắt buộc sau:

### 1. Giới Thiệu Đề Tài & Mô Tả Tập Dữ Liệu
- **1.1. Bối cảnh & Mục tiêu nghiên cứu**: Bài toán phân tích tần suất, mức độ thiệt hại tài chính và sinh mạng của thảm họa thiên nhiên và cháy rừng giai đoạn 2006–2025.
- **1.2. Khảo sát nguồn dữ liệu thực tế**: Dẫn nguồn & minh chứng hợp lệ (EM-DAT, NASA FIRMS, USFS/NOAA, Our World in Data). Cam kết quy mô $\ge 5.000$ dòng và kiến trúc đa bảng ($\ge 3$ bảng).
- **1.3. Từ điển dữ liệu (Data Dictionary)**: Mô tả chi tiết từng thuộc tính, ý nghĩa nghiệp vụ và kiểu dữ liệu.

### 2. Quy Trình Tiền Xử Lý & Khám Phá Dữ Liệu (EDA)
- **2.1. Quy trình xử lý (Pipeline) rõ ràng**: Sơ đồ kiến trúc luồng dữ liệu viết bằng Python/R.
- **2.2. Khám phá dữ liệu (EDA) bằng thư viện biểu đồ tĩnh**: Dùng **Matplotlib** và **Seaborn** vẽ tối thiểu **3 – 5 biểu đồ tĩnh** (phân phối Histogram/KDE, ngoại lai sơ bộ Boxplot, bản đồ nhiệt tương quan Heatmap, ma trận khuyết thiếu) trước khi đưa dữ liệu lên Dashboard.
- **2.3. Làm sạch dữ liệu triệt để**:
  - Xử lý thiếu (Missing Values): KNN Imputer / Iterative Imputer (MICE) gắn cờ `<col>_is_imputed`.
  - Xử lý ngoại lai (Outliers): Mô hình không giám sát **Isolation Forest** & LOF gắn cờ `is_outlier_ml`.
  - Chuẩn hóa định dạng ngày tháng, chuỗi, mã ISO3, tọa độ địa lý và đơn vị đo chuẩn (ha, USD).
- **2.4. Biến đổi dữ liệu (Data Transformation) & Tạo Calculated Fields**:
  - Tạo các trường dữ liệu tính toán mới có ý nghĩa (phân nhóm mức độ thiệt hại, chu kỳ mùa, log scale...).
  - Thiết kế Star Schema (3NF) và kết nối/phân rã bảng chính xác trong CSDL SQLite.

### 3. Thiết Kế Dashboard & Luồng Tương Tác
- **3.1. Bố cục (Layout) & Trải nghiệm người dùng (UI/UX)**: Bố cục hợp lý, màu sắc hài hòa (WCAG AA, dải màu Okabe-Ito, OrRd), có tiêu đề và chú thích (Legend) rõ ràng.
- **3.2. Hệ thống biểu đồ đa dạng**: Sử dụng $\ge 8$ loại biểu đồ khác nhau (Bar, Line, Area, Scatter, Heatmap, Treemap, Donut/Pie, Pareto...), trong đó **BẮT BUỘC có ít nhất 1 Bản đồ địa lý (Geographic Map)**.
- **3.3. Tính tương tác cao**: Bộ lọc đa cấp (Multi-level Filters), Đi sâu chi tiết (Drill-down), Tooltip khi hover chuột, và Tương tác liên kết giữa các biểu đồ (Cross-filtering / Filter Actions).
- **3.4. Giải thích ý nghĩa từng biểu đồ**: Lý do chọn biểu đồ, trục đo và câu hỏi kinh doanh mà biểu đồ trả lời.

### 4. Khai Phá Insight & Kể Chuyện Dữ Liệu (Storytelling - 1.0 Điểm Barem) *(Thành viên 3 độc lập chủ trì)*
- **4.1. Cốt truyện phân tích (Tableau Story với 3 Story Points trọng tâm)**: Thành viên 3 độc lập dẫn dắt logic người xem qua 3 chủ đề xuyên suốt (Point 1: Bức tranh 20 năm & Xu hướng $\to$ Point 2: Điểm nóng toàn cầu 80/20 $\to$ Point 3: Cháy rừng, Căn nguyên & Khuyến nghị tương lai).
- **4.2. Phân tích nguyên nhân và xu hướng từ Dashboard**: Rút ra bài học sâu sắc từ số liệu thật 2006–2025, giải thích nguyên nhân đằng sau các biến động thay vì chỉ mô tả biểu đồ.
- **4.3. Đề xuất giải pháp và khuyến nghị chính sách dựa trên dữ liệu**.

### 5. Mô Hình Dự Báo & Trực Quan Hóa (Predictive Model - 1.0 Điểm Barem)
- **5.1. Thuật toán dự báo trên Python (0.5 đ barem - Thành viên 1 thực hiện)**: 
  - Thành viên 1 áp dụng thuật toán **Hồi quy tuyến tính (Linear Regression)** dự báo xu hướng thiệt hại tài chính theo thời gian hoặc **Hồi quy Logistic** phân lớp rủi ro thảm họa nghiêm trọng bằng thư viện `scikit-learn`.
  - Đánh giá hiệu năng mô hình ($R^2$, MAE, RMSE đối với Linear; Accuracy, Precision, Recall, F1 đối với Logistic).
  - Xuất bảng kết quả dự báo `forecast_results.csv` bàn giao cho pipeline.
- **5.2. Trực quan hóa kết quả dự báo trên Dashboard (0.5 đ barem - Thành viên 3 thực hiện)**:
  - Thành viên 3 nhận kết quả dự báo của TV1, trực tiếp cấu hình đường xu hướng dự báo (Trend Line / Forecast) lên Dashboard D1.
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
| 1 | Trang bìa & Giới thiệu nhóm | Tên đề tài, Giảng viên hướng dẫn, Danh sách 3 thành viên | Trưởng nhóm |
| 2 | Đặt vấn đề & Bối cảnh 20 năm | Sự bùng nổ thảm họa cháy rừng, mục tiêu và phạm vi | Thành viên 1 |
| 3 | Pipeline Dữ liệu & Nguồn dữ liệu | Kiến trúc luồng dữ liệu từ Raw $\to$ Clean $\to$ Database $\to$ Web | Thành viên 1 |
| 4 | Làm sạch thông minh bằng ML | Isolation Forest bắt lỗi ngoại lai, MICE/KNN điền thiếu | Thành viên 1 |
| 5 | Mô hình Dữ liệu Star Schema | Sơ đồ ERD, hệ thống khóa ngoại và các ràng buộc toàn vẹn | Thành viên 2 |
| 6 | Tối ưu hóa truy vấn & Pipeline CI/CD | Các câu truy vấn SQL phức tạp, xuất JSON nén tải < 3s | Thành viên 2 |
| 7 | Tổng quan Dashboard & Nguyên tắc màu | Giao diện tổng thể, bảng màu Okabe-Ito, chuẩn tương phản | Thành viên 3 |
| 8–11 | Trực quan hóa chuyên sâu 12 biểu đồ | Điểm nhấn các biểu đồ kết hợp, Sankey, Treemap, Bản đồ | TV1, TV2, TV3 |
| 12 | Live Demo Dashboard | Thao tác lọc đa chiều, zoom, brush, drill-down thực tế | Thành viên 3 |
| 13 | 5 Phát Hiện Lớn Nhất (Key Insights) | Xu hướng biến đổi, quốc gia chịu ảnh hưởng, chu kỳ mùa cháy | Cả nhóm |
| 14 | Hạn chế dữ liệu & Bài học kinh nghiệm | Những khó khăn kỹ thuật và giải pháp khắc phục | Cả nhóm |
| 15 | Q&A / Cảm ơn | Tiếp nhận câu hỏi phản biện từ Hội đồng chấm thi | Cả nhóm |
