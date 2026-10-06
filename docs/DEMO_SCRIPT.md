# Kịch Bản Thuyết Trình Demo (DEMO SCRIPT)

> **Người phụ trách**: Thành viên 3 - Kỹ sư Dashboard & Trực quan hóa  
> **Thời lượng dự kiến**: 5–7 phút (Phần thao tác trực tiếp trên Dashboard)  
> **Trạng thái**: Khung kịch bản demo (Giai đoạn 1)

---

## 1. Chuẩn Bị Trước Khi Demo
- [ ] Mở sẵn đường dẫn Dashboard trên trình duyệt (hoặc máy chủ cục bộ: `http://localhost:8080`).
- [ ] Bật chế độ Fullscreen (F11), kiểm tra phóng to thu nhỏ ở mức 100%.
- [ ] Đặt sẵn các bộ lọc ở trạng thái mặc định (Default: Toàn bộ giai đoạn 2005–2024, tất cả loại thảm họa).
- [ ] Chuẩn bị sẵn 2 kịch bản phân tích tình huống (Use cases) để thao tác mượt mà.

---

## 2. Kịch Bản Chi Tiết Từng Phút (Timeline)

### Phút 0:00 – 1:00 | Giới Thiệu Tổng Quan & Hàng Thẻ KPI
- **Lời dẫn (Presenter)**:  
  *"Kính thưa Thầy Cô và các bạn, đây là sản phẩm Dashboard phân tích trực quan 20 năm thảm họa thiên nhiên toàn cầu (2005–2024) với trọng tâm là cháy rừng. Phía trên cùng là 4 thẻ KPI phản ánh ngay lập tức quy mô tổng quan: Tổng số sự kiện, Tổng thiệt hại tài chính quy đổi theo USD, Tổng diện tích rừng bị thiêu rụi và Tổng số sinh mạng thương vong."*
- **Thao tác**:  
  Di chuyển chuột qua các thẻ KPI, chỉ ra cơ chế hiển thị số liệu tức thời.

### Phút 1:00 – 2:30 | Khám Phá Xu Hướng Thời Gian & Phân Bố Mùa Vụ
- **Lời dẫn**:  
  *"Ở góc trên bên trái là Biểu đồ #1 (Combo Bar + Line) trục kép. Nhìn vào đây ta thấy rõ sự chênh lệch giữa số vụ và mức độ thiệt hại: Có những năm số vụ không tăng nhưng thiệt hại kinh tế lại đột biến do các siêu đám cháy tấn công vào khu dân cư đắt đỏ. Tiếp theo, Biểu đồ #4 Heatmap tháng theo năm cho thấy rõ mùa cháy rừng toàn cầu thường tập trung cao điểm từ tháng 6 đến tháng 9 ở Bắc Bán Cầu và tháng 11 đến tháng 2 ở Nam Bán Cầu."*
- **Thao tác**:  
  Dùng thanh trượt Brush trên Biểu đồ #1 để kéo chọn dải năm 2018–2021; quan sát các biểu đồ khác đồng bộ dữ liệu theo cơ chế Cross-filtering.

### Phút 2:30 – 4:00 | Phân Tích Không Gian & Phân Cấp Thiệt Hại (Drill-Down)
- **Lời dẫn**:  
  *"Chuyển sang Biểu đồ #3 Bản đồ thế giới Choropleth và Biểu đồ #6 Treemap. Chúng ta có thể thấy Châu Mỹ và Châu Đại Dương chịu tổn thất tài chính nặng nề nhất. Em xin phép click vào Châu Mỹ trên Treemap để drill-down xem cơ cấu quốc gia: Hoa Kỳ và Canada chiếm tỷ trọng áp đảo."*
- **Thao tác**:  
  Click vào khối `Americas` trên Treemap để phóng to các quốc gia; sau đó click vào Hoa Kỳ trên bản đồ thế giới để lọc toàn bộ dashboard về dữ liệu của Mỹ.

### Phút 4:00 – 5:15 | Phân Tích Chuyên Sâu Cháy Rừng: Nguyên Nhân, Quy Mô & Dòng Luồng
- **Lời dẫn**:  
  *"Để trả lời câu hỏi nguyên nhân gốc rễ, Biểu đồ #10 Sunburst cho thấy sự đối lập giữa yếu tố tự nhiên (sét) và tác động con người. Tiếp tục nhìn vào Biểu đồ #11 Sankey Diagram, chúng ta thấy đường truyền từ nguồn lửa đến mức độ thiệt hại thảm họa."*
- **Thao tác**:  
  Hover chuột vào luồng `Human` $\to$ `Wildfire` $\to$ `Catastrophic Damage` trên biểu đồ Sankey để làm sáng luồng quan hệ. Bật công tắc *"Chỉ hiển thị số liệu gốc"* để chứng minh tính minh bạch của các giá trị sau xử lý bằng Machine Learning.

### Phút 5:15 – 6:00 | Trình Diễn Mô Hình Dự Báo (Predictive Model Integration)
- **Lời dẫn**:  
  *"Thưa Thầy Cô, nhóm không chỉ dừng lại ở mô tả quá khứ mà còn tích hợp Mô hình Hồi quy tuyến tính / Logistic để dự báo xu hướng tương lai. Nhìn vào đường xu hướng dự báo (Trend Line) trên Biểu đồ #7 (Bubble Scatter) và Biểu đồ #5, mô hình cho thấy mức độ biến động thiệt hại có xu hướng dốc lên với hệ số tin cậy R-squared đạt chuẩn, giúp các nhà quản lý rủi ro lường trước kịch bản thiệt hại cho các năm tiếp theo."*
- **Thao tác**:  
  Bật đường Trend line/Dự báo trên Dashboard, hover xem phương trình hồi quy và mức độ giải thích $R^2$.

### Phút 6:00 – 7:00 | Tổng Kết & Câu Chuyện Dữ Liệu (Data Storytelling & Q&A)
- **Lời dẫn**:  
  *"Tóm lại, đóng vai trò như các Data Analyst tư vấn chiến lược cho tổ chức ứng phó thiên tai, nhóm đã rút ra được câu chuyện trọn vẹn từ nguyên nhân, chu kỳ mùa cho đến dự báo thiệt hại. Nhóm cũng đã chuẩn bị sẵn Video demo và Video backup tóm tắt dự phòng. Toàn bộ mã nguồn, tài liệu chuẩn IEEE và file .twbx đã sẵn sàng. Chúng em xin lắng nghe ý kiến đóng góp và trả lời phản biện của Thầy Cô!"*
