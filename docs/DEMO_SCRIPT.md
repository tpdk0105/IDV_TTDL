# KỊCH BẢN THUYẾT TRÌNH BẢO VỆ ĐỒ ÁN CUỐI KỲ (CHUYÊN SÂU)
## TRỰC QUAN HÓA DỮ LIỆU CHÁY RỪNG CALIFORNIA 20 NĂM (2006–2025)
### Hệ thống 4 Dashboards (D1 – D4) & 2 Tableau Stories (`Story_California_Wildfires` và `Year Fire Trend Forecast`)

---

> **Đề tài**: Nghiên cứu – Phân tích tần suất, quy mô và mức độ tàn phá của các trận cháy rừng tại California giai đoạn 2006–2025  
> **Người thực hiện**: Nhóm 17  
> **Sản phẩm trực quan**: Workbook Tableau Public (`CK_17913924077470`), bao gồm 4 Dashboards chuyên đề (15 Worksheets), 2 Tableau Stories, Star Schema 5 bảng CSV  
> **Thời lượng chuẩn**: 8 – 10 phút (Có kịch bản rút gọn 4 – 5 phút khi Hội đồng yêu cầu tóm tắt)

---

# PHẦN 1: TỔNG QUAN KIẾN TRÚC BÀI THUYẾT TRÌNH

```
[MỞ ĐẦU] Giới thiệu đề tài & 5 nguồn dữ liệu Star Schema (1 phút)
   │
   ├──► [STORY 1] Story_California_Wildfires (5.5 phút)
   │       ├── Story Point 1 ──► Dashboard D1: Bức tranh 20 năm & Mùa vụ cháy rừng
   │       ├── Story Point 2 ──► Dashboard D2: Không gian địa lý & Quy luật Pareto 80/20
   │       └── Story Point 3 ──► Dashboard D3: Căn nguyên bùng phát & Mô hình Hồi quy
   │
   ├──► [STORY 2] Year Fire Trend Forecast (2 phút)
   │       └── Story Point Forecast ──► Dashboard D4: Dự báo xu thế 10 năm (2026–2035)
   │
   └──► [KẾT LUẬN] 3 Khuyến nghị chính sách & Phiên hỏi đáp Q&A (1.5 phút)
```

---

# PHẦN 2: KỊCH BẢN CHI TIẾT TỪNG PHÚT (FULL SPOKEN SCRIPT & THAO TÁC)

---

## ⏱️ PHÚT 0:00 – 1:00 | MỞ ĐẦU: BỐI CẢNH DỮ LIỆU & KIẾN TRÚC HỆ THỐNG

### 🎯 Mục tiêu:
Tạo ấn tượng học thuật mạnh mẽ, làm rõ quy mô dữ liệu sạch và khẳng định tính hoàn chỉnh của mô hình phân tích.

### 🎙️ Lời thoại trình bày:
> *"Kính thưa Thầy Cô trong Hội đồng và các bạn!  
> Cháy rừng tại bang California từ lâu đã không còn là hiện tượng tự nhiên đơn thuần, mà đã trở thành cuộc khủng hoảng khí hậu và thảm họa nhân đạo mang tính chu kỳ.  
> Để giải bài toán phân tích đa chiều này, nhóm chúng em đã tích hợp và chuẩn hóa **5 nguồn dữ liệu chính thống của chính phủ Hoa Kỳ**:
> 1. **CAL FIRE FRAP**: Hồ sơ không gian của hơn 7.300 vụ cháy từ năm 1878 đến 2025;
> 2. **CAL FIRE DINS**: Cơ sở dữ liệu kiểm định thiệt hại chi tiết từng cấu trúc kiến trúc (2013–2025);
> 3. **USDA / NIFC (ICS-209-PLUS)**: Bộ dữ liệu liên bang để khỏa lấp khoảng trống thiệt hại giai đoạn 2006–2012, bảo đảm tính liên tục 20 năm trọn vẹn;
> 4. **NOAA Storm Events**: Hồ sơ thương vong nhân mạng chính xác;
> 5. **U.S. Census Bureau**: Ranh giới và dân số 58 Hạt.
>
> Toàn bộ dữ liệu được tổ chức theo **Mô hình Star Schema chuẩn gồm 2 bảng Fact và 3 bảng Dimension**, trải qua kiểm định 7 tiêu chí toàn vẹn đạt 100%.  
> Trên nền tảng Tableau, nhóm đã xây dựng **4 Dashboards chuyên đề (15 biểu đồ)** và dẫn dắt người xem thông qua **2 Tableau Storyboards**: `Story_California_Wildfires` và `Year Fire Trend Forecast`."*

### 🖱️ Thao tác trực tiếp trên màn hình:
1. Mở màn hình Tableau Public ở chế độ Toàn màn hình (F11).
2. Trỏ chuột nhanh vào thanh điều hướng bên trên để Hội đồng thấy rõ 2 Story Tab: **`Story_California_Wildfires`** và **`Year Fire Trend Forecast`**.
3. Bắt đầu bấm vào Story Tab thứ nhất: **`Story_California_Wildfires`**.

---

## ⏱️ PHÚT 1:00 – 3:00 | STORY 1 – POINT 1: BỨC TRANH 20 NĂM & MÙA VỤ CHÁY RỪNG (DASHBOARD D1)

### 📌 Tiêu đề Story Point 1:
> *"80% số vụ cháy tập trung từ tháng 6 đến tháng 10. Đáng chú ý, tần suất đầu mùa (tháng 4–5) và cuối mùa (tháng 10) đã tăng vọt ~70% trong thập kỷ 2016–2025."*

### 🎙️ Lời thoại trình bày:
> *"Bắt đầu tại **Story Point 1**, chúng ta quan sát Dashboard D1: **Bức tranh 20 năm & Mùa vụ cháy rừng**.  
> Ngay ở đầu trang, **4 Thẻ KPI vĩ mô** khẳng định quy mô tàn phá khốc liệt trong 2 thập kỷ qua:
> - **7.235 vụ cháy rừng** được ghi nhận;
> - **19,39 triệu mẫu Anh (acres)** — tương đương gần 7,85 triệu hecta rừng đã bị thiêu rụi;
> - **73.818 công trình kiến trúc** bị phá hủy hoàn toàn;
> - Và đau xót nhất là **207 sinh mạng đã tử vong** cùng **792 người bị thương**.
>
> Đi sâu vào **Sheet 01 (Line Chart 2 đường so sánh mùa vụ giữa 2 thập kỷ)**:
> - Dữ liệu cho thấy tính mùa vụ cực kỳ rõ nét: **80,3% số vụ cháy (5.813 vụ)** tập trung từ tháng 6 đến tháng 10.
> - Nhưng phát hiện đột phá nằm ở sự so sánh giữa 2 thập kỷ: Trong khi tháng cao điểm là **Tháng 7 chỉ tăng 17%** (từ 803 lên 936 vụ), thì các tháng đầu mùa (**Tháng 4 và Tháng 5 đều tăng vọt 70%**) và tháng cuối mùa (**Tháng 10 tăng 73%**, từ 167 lên 289 vụ).
> 👉 **Insight đắt giá**: Biến đổi khí hậu không chỉ làm đám cháy dữ dội hơn, mà thực chất đang **kéo dài mùa cháy ra cả hai đầu**, biến hiểm họa cháy rừng tại California từ 'mùa vụ' thành hiện tượng 'quanh năm'.
>
> Nhìn xuống **Sheet 10 (Diverging Bar Chart)**:
> - Trục chuẩn trung bình 20 năm là **362 vụ/năm**. Trước năm 2017, hầu hết các năm đều có màu xanh (dưới trung bình), thấp nhất là năm 2010 với âm 156 vụ.
> - Tuy nhiên, từ năm 2017 đến nay đã xuất hiện **bước ngoặt khí hậu**: 5 trong 9 năm đỏ rực vượt xa mức chuẩn, lập đỉnh vào năm 2017 với **+243 vụ**, năm 2024 **+174 vụ** và năm 2025 **+148 vụ**.
>
> Đồng thời, **Sheet 02 (Stacked Area)** minh chứng tỷ lệ các vụ 'Chưa xác định' tăng mạnh từ 24% lên 61%, phản ánh các vụ cháy hiện đại quá dữ dội, thiêu rụi toàn bộ hiện trường khiến công tác điều tra pháp y gặp thách thức lớn."*

### 🖱️ Thao tác trực tiếp trên màn hình:
1. Rê chuột qua 4 Thẻ KPI trên đỉnh dashboard để điểm qua các con số chủ chốt.
2. Tại **Sheet 01 (Line Chart)**: Hover chuột vào điểm đỉnh Tháng 7 và điểm lệch Tháng 4, Tháng 10 để Tooltip hiện chi tiết số liệu so sánh giữa 2 thập kỷ (xám: 2006–2015, đỏ: 2016–2025).
3. Tại **Sheet 10 (Diverging Bar)**: **Nhấp chuột (Click) vào cột năm 2017**.
   - Trình diễn **Cross-Filtering**: Toàn bộ Dashboard D1 (Sheet 01 và Sheet 02) tự động lọc theo năm 2017.
   - Nhấp lại lần nữa để khôi phục trạng thái ban đầu.

---

## ⏱️ PHÚT 3:00 – 4:30 | STORY 1 – POINT 2: TÂM CHẤN ĐỊA LÝ & QUY LUẬT PARETO 80/20 (DASHBOARD D2)

### 📌 Tiêu đề Story Point 2:
> *"Quy luật bất cân xứng cực đoan: Chỉ 7 trong tổng số 58 Hạt đã gánh chịu tới 82% tổng thiệt hại nhà cửa toàn bang, dẫn đầu là Butte (Camp Fire) và Los Angeles."*

### 🎙️ Lời thoại trình bày:
> *"Bước sang **Story Point 2** tại Dashboard D2, chúng ta trả lời câu hỏi cốt tử: **Thiệt hại tài sản tập trung ở đâu và gõ cửa những ai?**
>
> Quan sát **Sheet 09 (Combo Pareto Chart)** kết hợp **Sheet 05 (Top N Counties Bar Chart)**:
> - Phân tích dữ liệu 20 năm đã phát hiện một quy luật kinh điển: **Hiệu ứng Pareto 80/20 trong tổn thất thiên tai**.
> - Trong 58 Hạt của California, có 49 Hạt ghi nhận thiệt hại nhà cửa. Tuy nhiên, **chỉ 7 Hạt đầu bảng (chiếm 14% số Hạt) đã phải gánh chịu tới 82% tổng số công trình bị phá hủy toàn bang** (vượt qua đường mốc tham chiếu 80% màu đỏ).
> - Riêng 2 Hạt dẫn đầu là **Butte (23.834 công trình)** và **Los Angeles (19.066 công trình)** đã chiếm tới **58,1%** tổng thiệt hại toàn bang!
> - Đáng sợ hơn, nếu xét theo từng trận cháy: **Chỉ đúng 17 vụ cháy thảm họa (chiếm 0,23% tổng số vụ) đã xóa sổ 80% tổng số nhà cửa suốt 2 thập kỷ qua**.
>
> Nhìn sang **Sheet 03 (Bản đồ địa lý 2 lớp)**:
> - Lớp Choropleth thể hiện mật độ cháy (vụ/1.000 dặm²), màu cam đậm tập trung ở **Yuba (466)** và **Lake (239)**.
> - Nhưng vòng tròn bong bóng diện tích lớn nhất lại nằm ở **Butte (2 triệu mẫu)** và **Kern**. Hạt nhiều vụ nhất (Kern với 1.015 vụ) hoàn toàn khác với Hạt chịu thiệt hại nặng nhất (Butte).
>
> Khi nhìn vào **Sheet 07 (Treemap thiệt hại công trình)**:
> - Loại hình kiến trúc bị hủy diệt nhiều nhất là **Nhà ở riêng lẻ đơn lập (Single Family Residence)** với **36.057 căn (52%)**.
> - Kế đến là **Nhà di động (Mobile Home) với 7.396 căn**, tập trung bi kịch tại thị trấn Paradise thuộc Hạt Butte trong thảm họa Camp Fire 2018 (mất 4.190 nhà di động).
> 👉 **Insight đắt giá**: Cháy rừng California không chỉ là cháy cây cỏ trong rừng sâu, mà là **cuộc khủng hoảng nhà ở đô thị ven rừng (Wildland-Urban Interface - WUI)**."*

### 🖱️ Thao tác trực tiếp trên màn hình:
1. Tại **Sheet 03 (Bản đồ địa lý)**: **Click vào Hạt Butte**.
   - Toàn bộ Dashboard D2 lập tức lọc: Sheet 05 phóng to Butte, Sheet 07 hiển thị cơ cấu 18.804 nhà bị phá hủy của Butte (chủ yếu là Camp Fire).
2. Tại **Sheet 09 (Pareto Chart)**: Trỏ vào đường phần trăm tích lũy chạy qua Hạt thứ 7 (Napa - 81,6%) để làm nổi bật đường tham chiếu 80%.
3. Điều chỉnh **Thanh trượt Tham số Top N** từ 10 xuống 5 hoặc lên 15 để trình diễn tính năng Dynamic Parameter.

---

## ⏱️ PHÚT 4:30 – 6:00 | STORY 1 – POINT 3: CĂN NGUYÊN BÙNG PHÁT & HỒI QUY DỰ BÁO (DASHBOARD D3)

### 📌 Tiêu đề Story Point 3:
> *"Sét đánh dễ tạo siêu đám cháy ở vùng hẻo lánh, nhưng hoạt động con người chiếm 64% các vụ đã rõ nguyên nhân và đe dọa trực tiếp khu dân cư. Mô hình hồi quy log-log (R² = 0,356) chứng minh diện tích tăng 10 lần thì tổn thất tăng ~2,71 lần."*

### 🎙️ Lời thoại trình bày:
> *"Chuyển tiếp đến **Story Point 3** tại Dashboard D3, chúng ta tiến hành giải mã: **Đâu là nguồn gốc kích hoạt và mối tương quan giữa quy mô đám cháy với mức độ tàn phá tài sản?**
>
> Quan sát **Sheet 04 (Donut Chart 2 tầng)**:
> - Trong toàn bộ 7.235 vụ, có 42,7% chưa rõ nguyên nhân. Nhưng trong các vụ đã điều tra rõ ràng: **Con người kích hoạt tới 64% (2.635 vụ)**, so với tự nhiên sấm sét chỉ là 36% (1.509 vụ).
> - Nguồn gốc nhân tạo chủ yếu do: Thiết bị máy móc (762 vụ), Phương tiện giao thông (488 vụ), Cố ý phóng hỏa (363 vụ) và Sự cố đường dây điện lưới (335 vụ).
>
> Tuy nhiên, **Sheet 06 (Heatmap ma trận Nguyên nhân × Quy mô)** lại chỉ ra một **nghịch lý sinh thái**:
> - Mặc dù sấm sét tự nhiên chỉ chiếm tỷ lệ nhỏ, nhưng có tới **11,9% số vụ do sét phát triển thành đám cháy lớn ≥ 5.000 mẫu Anh** (gấp tới 4 lần tỷ lệ 3,0% của con người). Lý do là sét thường đánh ở đỉnh núi cao hiểm trở, khó tiếp cận khống chế ngay từ đầu.
> - Ngược lại, các đám cháy do con người tuy 81,4% là vụ nhỏ dưới 300 mẫu, nhưng khi bùng phát vào ngày gió Santa Ana khô khốc, chúng thiêu rụi hàng chục ngàn ngôi nhà ven đô.
>
> Để hoàn thiện năng lực phân tích định lượng, nhóm đã xây dựng **Sheet 08 (Scatter Plot Hồi quy tuyến tính Log-Log)**:
> - Nếu chạy hồi quy trên số liệu gốc, hệ số xác định chỉ đạt $R^2 = 0.026$ do phân phối lệch phải cực đoan.
> - Nhóm đã áp dụng **phép biến đổi Logarit cơ số 10 trên cả hai trục**, nâng hệ số $R^2$ lên **0.356 (tăng gấp 13 lần khả năng giải thích)**, kiểm định $t = 14.658$, $p < 0.0001$ cực kỳ có ý nghĩa thống kê.
> - Phương trình hồi quy: $\log_{10}(\text{Destroyed}) = 0.433436 \times \log_{10}(\text{Acres}) - 0.377417$.
> 👉 **Insight định lượng**: Khi diện tích cháy tăng gấp 10 lần, số công trình bị phá hủy sẽ tăng trung bình **2,71 lần** ($10^{0.433} \approx 2.71$). Đây là công cụ đắc lực giúp lực lượng cứu hộ dự báo nhanh thiệt hại tài sản ngay khi vệ tinh đo được diện tích đám cháy."*

### 🖱️ Thao tác trực tiếp trên màn hình:
1. Tại **Sheet 04 (Donut Chart)**: Nhấp chuột vào lát cắt màu đỏ **Human (Con người)**.
   - Quan sát hiệu ứng lọc làm sáng (Highlight) trên Heatmap và Scatter Plot.
2. Tại **Sheet 08 (Scatter Plot)**: Hover chuột vào đường **Trend Line** màu đen có dải xám mờ để bật Tooltip hiển thị phương trình hồi quy, hệ số $R^2$ và $p$-value.
3. Hover vào các điểm dị biệt phía trên (như Camp Fire, Tubbs Fire) để xem chi tiết số nhà bị thiêu rụi so với dự báo mô hình.

---

## ⏱️ PHÚT 6:00 – 8:00 | STORY 2: YEAR FIRE TREND FORECAST (DASHBOARD D4)

### 📌 Tiêu đề Story 2:
> *"Dự báo xu thế cháy rừng giai đoạn 2026–2035 bằng hồi quy tuyến tính, với khoảng dự báo 95% thể hiện mức độ bất định của kết quả."*

### 🎙️ Lời thoại trình bày:
> *"Kính thưa Thầy Cô, sau khi nhìn lại quá khứ và giải mã hiện tại, chúng ta bước sang **Story thứ 2: `Year Fire Trend Forecast`** nhúng trực tiếp **Dashboard D4 (Dự báo xu thế 10 năm tới 2026–2035)**.  
> Để đáp ứng trọn vẹn tiêu chí barem môn học về Mô hình dự báo chuỗi thời gian, nhóm đã triển khai thuật toán trên Python với kiểm định **Rolling Origin (Walk-forward 5 folds)** và trực quan hóa kết quả lên Tableau với **dải độ tin cậy 95% (Prediction Interval)**.
>
> 1. **Sheet F1 (Dự báo Số vụ cháy hàng năm - Dual-Axis Area & Circle Points)**:
>    - Đường xu thế tuyến tính màu xám dốc lên rõ rệt. Dải phễu màu xanh nhạt thể hiện khoảng biến thiên 95%.
>    - Nhãn dự báo tại mốc năm 2035: **515 vụ [251 – 780 vụ/năm]**.
>    - So với mức trung bình lịch sử 20 năm qua là 362 vụ/năm, tần suất cháy rừng dự phóng **tăng thêm 42%**, chính thức xác lập tình trạng 'bình thường mới' (The New Normal) với trên 500 vụ cháy lớn mỗi năm.
>
> 2. **Sheet F2 (Dự báo Diện tích cháy - Trục Logarit & Đường Exponential)**:
>    - Do diện tích cháy có sự biến động cực lớn từ năm thấp nhất 41 nghìn ha (2010) đến năm cao nhất gần 1,7 triệu ha (2020), nhóm sử dụng **thang đo Logarit** để bảo đảm tính chuẩn xác thị giác.
>    - Dự phóng năm 2035: Diện tích cháy trung bình là **425.612 ha**.
>    - Đặc biệt, dải cận trên 95% cảnh báo: Trong những năm chu kỳ hạn hán cực đoan (kết hợp El Niño/La Niña), diện tích cháy có thể bùng phát chạm mốc **4,56 triệu ha**.
>
> 3. **Sheet F3 (Dự báo Số công trình bị phá hủy - Trục Logarit & Đường Exponential)**:
>    - Xu thế tổn thất tài sản leo thang nhanh nhất: Từ mức trung bình khoảng 370 công trình vào năm 2006, mô hình dự phóng đến năm 2035 con số này sẽ là **7.041 công trình/năm** (khoảng tin cậy [65 – 751.461 công trình]).
>    - Sự gia tăng đột biến này phản ánh tốc độ đô thị hóa lấn sâu vào rừng đang biến các đám cháy bình thường thành thảm họa dân sinh."*

### 🖱️ Thao tác trực tiếp trên màn hình:
1. Bấm chuột chuyển từ tab Story 1 sang tab **`Year Fire Trend Forecast`**.
2. Trỏ chuột vào mốc tham chiếu phân cách quá khứ – tương lai (đường Reference Line tại năm 2025.5).
3. Hover vào điểm nhãn mốc năm 2035 trên cả 3 biểu đồ:
   - F1: Chỉ rõ giá trị dự báo `515 [251 - 780]`.
   - F2: Chỉ rõ giá trị `425612 [39667 - 4566518]`.
   - F3: Chỉ rõ giá trị `7041 [65 - 751461]`.
4. Nhấn mạnh với Hội đồng: Dải phễu mở rộng phản ánh trung thực tính bất định của biến đổi khí hậu theo đúng phương pháp luận khoa học.

---

## ⏱️ PHÚT 8:00 – 9:00 | KẾT LUẬN & 3 KHUYẾN NGHỊ CHÍNH SÁCH THỰC TẾ

### 🎙️ Lời thoại trình bày:
> *"Dưới góc độ các nhà khoa học dữ liệu tư vấn chính sách cho Cơ quan Quản lý Khẩn cấp California (CAL FIRE / FEMA), từ toàn bộ các insight khai phá được, nhóm đề xuất **3 khuyến nghị hành động trọng tâm**:
>
> 1. **Tái cấu trúc lịch trực cứu hỏa theo mùa mở rộng**: Do số vụ cháy tháng 4, tháng 5 và tháng 10 đã tăng vọt hơn 70%, CAL FIRE cần huy động trạng thái sẵn sàng chiến đấu và trực thăng chữa cháy ngay từ đầu tháng 4 thay vì đợi đến tháng 6 như truyền thống.
> 2. **Phân bổ 80% ngân sách theo nguyên lý Pareto**: Thay vì chia đều cho 58 Hạt, cần tập trung 80% nguồn lực phòng ngừa, xây dựng trạm cảm biến khói và công sự chắn lửa cho **7 Hạt trọng điểm** (đặc biệt là Butte, Los Angeles, Sonoma). Đồng thời bắt buộc áp dụng khoảng đệm an toàn 100 feet cho loại hình nhà ở đơn lập (Single Family Residence).
> 3. **Kiểm soát chặt chẽ 64% nguồn phát hỏa nhân tạo**: Tăng cường áp dụng chính sách ngắt điện chủ động (PSPS) trong các đợt gió khô Santa Ana, đồng thời lắp đặt camera AI giám sát tia lửa thiết bị dọc theo các trục đường cao tốc xuyên rừng."*

---

## ⏱️ PHÚT 9:00 – 10:00 | BÀN GIAO SẢN PHẨM & LỜI CẢM ƠN

### 🎙️ Lời thoại trình bày:
> *"Nhóm chúng em đã hoàn thành toàn diện các sản phẩm bàn giao của đồ án:
> - File Workbook Tableau đóng gói `wildfire_disaster_analysis.twbx` hoạt động mượt mà cả ngoại tuyến lẫn trên Tableau Public;
> - Toàn bộ mã nguồn xử lý tự động, kiểm thử và mô hình dự báo trong kho lưu trữ Git;
> - Báo cáo khoa học hoàn chỉnh hơn 40 trang chuẩn cấu trúc IEEE;
> - Video Demo tương tác và Video Backup sẵn sàng.
>
> Chúng em xin chân thành cảm ơn Thầy Cô và các bạn đã chú ý lắng nghe! Nhóm chúng em rất mong nhận được những góp ý quý báu từ Hội đồng và sẵn sàng trả lời các câu hỏi phản biện."*

---

# PHẦN 3: BỘ CÂU HỎI & TRẢ LỜI PHẢN BIỆN DỰ PHÒNG (Q&A CHEAT-SHEET)

### ❓ Câu hỏi 1: Tại sao nhóm phải kết hợp bộ dữ liệu DINS (2013–2025) với ICS-209-PLUS (2006–2012)?
> **Trả lời**: *"Dạ thưa Thầy Cô, chương trình thanh tra thiệt hại DINS (Damage Inspection) của CAL FIRE chỉ chính thức được thể chế hóa và thu thập số hóa sau thảm họa cháy Rim Fire năm 2013. Nếu chỉ dùng DINS, phân tích của chúng em sẽ bị khuyết mất 7 năm (2006–2012). Nhóm đã nghiên cứu và kết hợp với dữ liệu kiểm kê liên bang ICS-209-PLUS của Bộ Nông nghiệp Hoa Kỳ (USDA) và NIFC. Hai bộ dữ liệu này được ánh xạ và chuẩn hóa cột `structures_destroyed`, giúp toàn bộ chuỗi thời gian 20 năm liên tục không bị đứt đoạn, bảo đảm tính toàn vẹn 20/20 năm của nghiên cứu."*

### ❓ Câu hỏi 2: Tại sao ở biểu đồ hồi quy Sheet 08 nhóm phải dùng biến đổi Log-Log?
> **Trả lời**: *"Dạ thưa Thầy Cô, phân phối của diện tích cháy và số công trình bị phá hủy đều có độ lệch phải cực kỳ nặng (Skewness > 14, Kurtosis > 280). Đa số các vụ cháy có diện tích nhỏ và thiệt hại 0 nhà, trong khi một vài siêu đám cháy như Camp Fire có diện tích hàng trăm nghìn mẫu và phá hủy gần 19.000 ngôi nhà. Nếu chạy hồi quy tuyến tính trên thang đo gốc, các điểm ngoại lai này sẽ làm lệch hoàn toàn đường hồi quy và hệ số $R^2$ chỉ đạt 0.026. Khi chuyển đổi $\log_{10}$, dữ liệu được kéo về dạng phân phối gần chuẩn, tuyến tính hóa mối quan hệ phi tuyến, giúp $R^2$ đạt 0.356 (tăng gấp 13 lần khả năng giải thích) và $p < 0.0001$."*

### ❓ Câu hỏi 3: Trên Dashboard D4, dải phễu xanh có ý nghĩa gì và tại sao cận trên diện tích lại lên tới hơn 4,5 triệu ha?
> **Trả lời**: *"Dạ thưa Thầy Cô, dải phễu xanh biểu thị Khoảng tin cậy dự báo 95% (95% Prediction Interval). Nó không chỉ đưa ra một giá trị trung bình điểm, mà chỉ ra biên độ dao động có thể xảy ra trong tương lai. Đối với diện tích cháy rừng California, biến số phụ thuộc rất lớn vào các năm xảy ra hiện tượng khí hậu cực đoan La Niña gây khô hạn kéo dài (như năm 2020 đã từng cháy gần 1,7 triệu ha). Cận trên 4,56 triệu ha là kịch bản rủi ro khí hậu cực hạn (Worst-case Scenario) nhằm cảnh báo các nhà hoạch định ngân sách phải chuẩn bị kịch bản cứu trợ khẩn cấp."*

---

# PHẦN 4: BẢNG "CON SỐ VÀNG" CẦN NHỚ KHI LÊN BỤC

| Hạng mục | Con số chính xác | Ghi nhớ nhanh |
| :--- | :--- | :--- |
| **Tổng số vụ cháy (20 năm)** | **7.235 vụ** | Hơn 7,2 nghìn vụ |
| **Tổng diện tích rừng bị cháy** | **19,39 triệu mẫu (acres)** | Gần 20 triệu mẫu (~7,85 triệu ha) |
| **Tổng công trình bị phá hủy** | **73.818 công trình** | Gần 74 nghìn công trình |
| **Thương vong nhân mạng** | **207 người chết, 792 người bị thương** | Đỉnh tang thương 2018 (97 người) |
| **Tập trung mùa cháy** | **80,3% vụ từ Tháng 6 đến Tháng 10** | T4 & T5 tăng 70%, T10 tăng 73% |
| **Mức chuẩn trung bình** | **362 vụ/năm** | Sau 2017 có 5/9 năm vượt xa mức chuẩn |
| **Quy luật Pareto Hạt** | **7/49 Hạt chịu 82% thiệt hại** | Butte (23.834) + LA (19.066) = 58% |
| **Quy luật Pareto Sự cố** | **17 vụ (0,23%) gây 80% thiệt hại** | Chỉ 17 vụ xóa sổ 80% nhà cửa |
| **Tỷ lệ nhà ở dân sinh** | **64% tổng số công trình** | Nhà 1 hộ: 36.057 căn (52%) |
| **Căn nguyên con người** | **64% trong các vụ đã rõ nguyên nhân** | Máy móc (762), Xe (488), Phóng hỏa (363) |
| **Nghịch lý sấm sét** | **11,9% vụ do sét $\ge$ 5.000 mẫu** | Gấp 4 lần tỷ lệ 3% của con người |
| **Mô hình Hồi quy Log-Log** | **$R^2 = 0.356$, $p < 0.0001$** | Diện tích tăng 10 lần $\to$ Thiệt hại tăng 2,71 lần |
| **Dự báo 2035 (Số vụ)** | **515 [251 – 780] vụ/năm** | Tăng 42% so với quá khứ |
| **Dự báo 2035 (Diện tích)** | **425.612 ha [39.667 – 4.566.518 ha]** | Cận trên 4,5 triệu ha |
| **Dự báo 2035 (Công trình)** | **7.041 [65 – 751.461] công trình** | Tăng từ 370 lên 7.041 căn/năm |
