# Dàn Ý Báo Cáo & Slide Thuyết Trình (REPORT OUTLINE & SLIDES)

> **Người phụ trách**: Thành viên 3 - Kỹ sư Dashboard & Báo cáo  
> **Trạng thái**: Khung dàn ý báo cáo đồ án và cấu trúc bài thuyết trình (Giai đoạn 1)

---

## Phần A: Dàn Ý Báo Cáo Chi Tiết Đồ Án (Report Outline)

### Chương 1: Giới Thiệu Đề Tài & Bối Cảnh Nghiên Cứu
1.1. Tính cấp thiết của đề tài: Tác động biến đổi khí hậu toàn cầu và sự gia tăng các vụ cháy rừng khốc liệt (2005–2024).  
1.2. Mục tiêu nghiên cứu: Phân tích tần suất, mức độ thiệt hại tài chính và sinh mạng; so sánh vị thế của cháy rừng trong tổng thể các thảm họa thiên nhiên.  
1.3. Phạm vi dữ liệu & Phương pháp tiếp cận: Dữ liệu đa nguồn (EM-DAT, NASA FIRMS, USFS/NOAA), quy trình Data Engineering kết hợp Machine Learning và Visual Analytics.

### Chương 2: Thu Thập & Kỹ Thuật Làm Sạch Dữ Liệu
2.1. Đánh giá và so sánh các nguồn dữ liệu quốc tế.  
2.2. Phân tích khám phá dữ liệu ban đầu (EDA) & phát hiện các khiếm khuyết dữ liệu thô.  
2.3. Quy trình làm sạch dữ liệu dựa trên quy tắc (Rule-based cleaning): Chuẩn hóa ISO3, tọa độ, tiền tệ và diện tích.  
2.4. Ứng dụng Học máy trong làm sạch dữ liệu:
- Phát hiện bất thường đa biến bằng **Isolation Forest** và **Local Outlier Factor (LOF)**.
- Xử lý giá trị khuyết thiếu bằng **KNN Imputer** / **Iterative Imputer (MICE)** với cơ chế đánh giá sai số nghiêm ngặt.
- Dự đoán phân loại nguyên nhân cháy bằng **Random Forest Classifier**.
2.5. Minh bạch hóa và kiểm soát chất lượng: Các cột cờ độ tin cậy và hạn chế dữ liệu.

### Chương 3: Thiết Kế Mô Hình Dữ Liệu (Star Schema & Ràng Buộc Cơ Sở Dữ Liệu)
3.1. Phân rã dữ liệu đạt chuẩn tối thiểu 3NF và kiến trúc hình sao (Star Schema).  
3.2. Chi tiết các bảng Dimension và Fact (`fact_disaster_event`, `fact_wildfire_detail`).  
3.3. Hệ thống ràng buộc toàn vẹn: Primary Key, Foreign Key, CHECK constraints, UNIQUE, NOT NULL và các Indexes tối ưu hóa truy vấn.  
3.4. Kiểm thử toàn vẹn dữ liệu tự động (`07_validate.py` & pytest).

### Chương 4: Hệ Thống 12 Biểu Đồ Trực Quan Hóa Tương Tác
4.1. Quy chuẩn mã hóa thị giác và bảng màu thân thiện người dùng (WCAG AA, Okabe-Ito, OrRd, RdBu).  
4.2. Phân tích chi tiết 12 biểu đồ (Mục tiêu phân tích, kiểu dữ liệu, kỹ thuật tương tác).  
4.3. Các biểu đồ kết hợp (Combo charts) và biểu đồ phân cấp (Treemap, Sunburst, Sankey).  
4.4. Trực quan hóa không gian: Bản đồ phân vùng Choropleth và bản đồ điểm Proportional Symbol Map.

### Chương 5: Thiết Kế Dashboard & Triển Khai Hệ Thống
5.1. Kiến trúc web tĩnh hiệu năng cao với Apache ECharts và thuần JavaScript (Vanilla JS).  
5.2. Hệ thống bộ lọc toàn cục tương tác, Cross-filtering, cơ chế lọc dữ liệu gốc/ước lượng.  
5.3. Quy trình CI/CD tự động triển khai lên GitHub Pages.

### Chương 6: Phát Hiện Chính (Key Insights), Hạn Chế & Hướng Phát Triển
6.1. 5–7 phát hiện cốt lõi từ số liệu thực tế 2005–2024.  
6.2. Các hạn chế tồn đọng về độ trễ dữ liệu và phạm vi thống kê của các quốc gia.  
6.3. Đề xuất mở rộng mô hình dự báo nguy cơ cháy rừng theo thời gian thực.

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
