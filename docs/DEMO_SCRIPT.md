# Kịch Bản Thuyết Trình Demo (DEMO SCRIPT)

> **Đề tài**: "Nghiên cứu – phân tích tần suất và thiệt hại của các trận cháy rừng tại California / Bắc Mỹ trong 20 năm qua (2006–2025)"  
> **Người phụ trách thuyết trình**: Thành viên 3 - Kỹ sư Dashboard & Storytelling (với sự phối hợp kết quả mô hình từ Thành viên 1 & Thành viên 2)  
> **Thời lượng dự kiến**: 5–7 phút (Thao tác trực tiếp trên Tableau Public / Tableau Story nhúng GitHub Pages)  
> **Sản phẩm demo**: Tableau Story (3 Story Points), 3 Dashboards (D1, D2, D3), 10 Worksheets, Video Demo & Video Backup.

---

## 1. Chuẩn Bị Trước Khi Demo
- [ ] Mở sẵn đường dẫn Dashboard trên trình duyệt: GitHub Pages URL hoặc Tableau Public URL (hoặc cục bộ `http://localhost:8080`).
- [ ] Bật chế độ Fullscreen (F11), kiểm tra tỷ lệ hiển thị ở mức 100%.
- [ ] Đặt sẵn các bộ lọc ở trạng thái mặc định (Default: Toàn bộ 20 năm 2006–2025, toàn bộ 58 Hạt California).
- [ ] Mở sẵn file Workbook đóng gói `tableau/wildfire_disaster_analysis.twbx` trên Tableau Desktop để dự phòng ngoại tuyến.
- [ ] Chuẩn bị sẵn liên kết Video Demo chính thức và Video Backup tóm tắt theo đúng barem yêu cầu.

---

## 2. Kịch Bản Chi Tiết Từng Phút (Timeline 5–7 Phút)

### Phút 0:00 – 1:00 | Giới Thiệu Tổng Quan & Bối Cảnh 20 Năm California
- **Lời dẫn (Presenter)**:  
  *"Kính thưa Thầy Cô và các bạn, đây là sản phẩm trực quan hóa dữ liệu nghiên cứu 20 năm cháy rừng tại bang California giai đoạn 2006–2025. Nhóm chúng em đã tích hợp và làm sạch 5 nguồn dữ liệu uy tín của chính phủ Hoa Kỳ: CAL FIRE FRAP (7.342 vụ cháy rừng), DINS và USFS ICS-209 (hơn 133.000 hồ sơ kiểm kê thiệt hại công trình liên tục 20/20 năm), NOAA Storm Events (thương vong sinh mạng) và Dữ liệu nhân khẩu 58 Hạt.  
  Toàn bộ báo cáo được cấu trúc thành một **Tableau Story gồm 3 Story Points** dẫn dắt người xem từ Bức tranh vĩ mô & Mô hình dự báo, Điểm nóng 58 Hạt theo nguyên lý 80/20, đến Căn nguyên kích hoạt và các Siêu thảm họa."*
- **Thao tác**:  
  Giới thiệu thanh điều hướng Story Navigator trên đầu trang; chỉ rõ 3 Story Points logic.

---

### Phút 1:00 – 2:30 | Story Point 1: Bức Tranh 20 Năm & Trực Quan Hóa Mô Hình Dự Báo (Dashboard D1)
- **Lời dẫn**:  
  *"Ở **Story Point 1**, chúng ta quan sát Dashboard D1: Bức tranh 20 năm Cháy rừng California.  
  - Trên **Biểu đồ #1 (Dual-Axis Combo Bar + Line)**: Cột màu xanh thể hiện số vụ cháy hàng năm, còn đường màu cam phản ánh diện tích rừng bị thiêu rụi (Acres). Nhìn vào đây ta thấy rõ sự khốc liệt: Năm 2020 là đỉnh điểm lịch sử với hơn 4,3 triệu mẫu rừng bị thiêu rụi.  
  - **Tích hợp Mô hình Dự báo của Thành viên 1 (Barem 0.5 đ)**: Nhóm đã huấn luyện mô hình Hồi quy tuyến tính (Linear Regression) trên Python và trực quan hóa đường **Trend Line** dốc lên ngay trên Biểu đồ #1. Đường xu thế này cảnh báo diện tích tàn phá trung bình có xu hướng leo thang theo chu kỳ biến đổi khí hậu.  
  - Phía dưới, **Biểu đồ #2 (Stacked Area)** phân tích cơ cấu nguyên nhân biến thiên theo thời gian; và **Biểu đồ #3 (Diverging Bar)** thể hiện độ lệch số vụ từng năm so với mức chuẩn 20 năm, làm nổi bật các năm cực đoan đỏ rực như 2017, 2020 và 2021."*
- **Thao tác**:  
  Kéo thanh trượt Filter Năm để thu hẹp giai đoạn 2017–2021; hover chuột vào điểm đỉnh năm 2020 để xem Tooltip diện tích; hover vào đường Trend Line để giải thích xu thế dự báo.

---

### Phút 2:30 – 4:00 | Story Point 2: Điểm Nóng 58 Hạt & Phân Cấp Thiệt Hại Pareto 80/20 (Dashboard D2)
- **Lời dẫn**:  
  *"Chuyển sang **Story Point 2** tại Dashboard D2, chúng ta đi tìm câu trả lời: Thiệt hại nhà cửa tập trung ở đâu?  
  - **Biểu đồ #9 (Choropleth Map 58 Hạt California)** phân vùng mức độ tàn phá với dải màu Cam - Đỏ. Các vùng đỏ sẫm tập trung tại Bắc California (vùng Sierra Nevada) và Nam California.  
  - **Biểu đồ #7 (Combo Pareto Chart)** chứng minh một phát hiện quan trọng: **Dữ liệu tuân thủ chặt chẽ nguyên lý Pareto 80/20**. Dưới 20% số Hạt (như Butte, Sonoma, Shasta, Lake, Los Angeles, Napa) gánh chịu trên 80% trong tổng số hơn 77.500 ngôi nhà bị phá hủy suốt 20 năm. Điển hình là thảm họa Camp Fire 2018 tại Hạt Butte đã xóa sổ hơn 18.000 ngôi nhà chỉ trong một vụ cháy.  
  - Khi click vào Hạt Butte trên bản đồ, **Biểu đồ #4 (Treemap Chart)** lập tức lọc chi tiết: Loại hình chịu tổn thất nặng nề nhất là Nhà ở riêng lẻ (Single Family Residence), chiếm trên 70% tổng thiệt hại kiến trúc."*
- **Thao tác**:  
  Click vào Hạt Butte trên bản đồ Choropleth để kích hoạt Filter Action; quan sát biểu đồ Treemap và Pareto tự động highlight theo Hạt được chọn.

---

### Phút 4:00 – 5:30 | Story Point 3: Mùa Vụ, Căn Nguyên & Siêu Đám Cháy Megafires (Dashboard D3)
- **Lời dẫn**:  
  *"Tại **Story Point 3**, Dashboard D3 giải mã căn nguyên sâu xa và quy mô của các siêu thảm họa:  
  - **Biểu đồ #8 (Donut Chart 2 tầng)**: Vòng trong phân nhóm lớn cho thấy: Mặc dù hiện tượng sét đánh tự nhiên (Lightning) gây ra các vụ cháy diện tích lớn nhất (như đợt sét khô tháng 8/2020), nhưng hoạt động của con người (thiết bị máy móc, đường dây điện cao thế PG&E, đốt cỏ rác, bất cẩn) chiếm trên 85% tổng số vụ bùng phát gần khu dân cư.  
  - **Biểu đồ #5 (Bubble Scatter Log-Log)** và **Biểu đồ #6 (Combo Histogram)**: Phân phối quy mô diện tích cho thấy các vụ cháy nhỏ (<1.000 mẫu) chiếm đa số số lượng, nhưng các **Siêu đám cháy (Megafires &ge; 100.000 mẫu)** chiếm đến hơn 70% tổng diện tích tàn phá.  
  - **Biểu đồ #10 (Proportional Symbol Map)**: Định vị chính xác tọa độ các siêu vụ cháy lịch sử như August Complex (hơn 1 triệu mẫu), Dixie Fire (gần 1 triệu mẫu), Camp Fire và các đại vụ cháy mới nhất năm 2025."*
- **Thao tác**:  
  Chọn bộ lọc nguyên nhân `Human` trên Dashboard D3; hover vào bong bóng vụ cháy `CAMP` và `AUGUST COMPLEX` trên biểu đồ Bubble Scatter và Symbol Map.

---

### Phút 5:30 – 6:30 | Khuyến Nghị Chiến Lược Dựa Trên Dữ Liệu (Actionable Insights)
- **Lời dẫn**:  
  *"Dưới góc độ chuyên gia phân tích dữ liệu tham mưu cho Cơ quan Quản lý Lâm nghiệp & Khẩn cấp Bang California (CAL FIRE / FEMA), nhóm đưa ra 3 khuyến nghị hành động thiết thực dựa trên bằng chứng dữ liệu:  
  1. **Quy hoạch phòng vệ có trọng tâm**: Thay vì rải đều nguồn lực trên 58 Hạt, cần ưu tiên ngân sách phòng cháy chữa cháy vào Top 10 Hạt thuộc dải 80/20 đã xác định.  
  2. **Kiểm soát nguồn lửa nhân tạo**: Siết chặt quy chuẩn an toàn lưới điện cao áp và cấm hoàn toàn thiết bị phát tia lửa trong các đợt gió khô Santa Ana / Diablo.  
  3. **Tiêu chuẩn xây dựng chống cháy**: Bắt buộc nâng cấp vật liệu chống cháy cho các khu dân cư đơn lập (Single Family) tại vùng giao thoa giữa rừng và đô thị (WUI)."*

---

### Phút 6:30 – 7:00 | Bàn Giao, Video Backup & Trả Lời Câu Hỏi Phản Biện (Q&A)
- **Lời dẫn**:  
  *"Nhóm đã chuẩn bị đầy đủ sản phẩm bàn giao gồm: File Workbook đóng gói `wildfire_disaster_analysis.twbx`, mã nguồn pipeline tự động hóa, tài liệu báo cáo chuẩn IEEE trên 40 trang, cùng liên kết Video Demo chính thức và Video Backup dự phòng.  
  Em xin chân thành cảm ơn Thầy Cô và các bạn đã lắng nghe, nhóm chúng em rất mong nhận được ý kiến đóng góp và sẵn sàng trả lời các câu hỏi phản biện!"*

