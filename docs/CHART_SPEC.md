# Đặc Tả 12 Biểu Đồ Trực Quan Hóa (CHART SPECIFICATIONS)

> **Nhóm thực hiện**: Phân chia đều 4/4/4 (TV1: #1–#4, TV2: #5–#8, TV3: #9–#12)  
> **Thư viện chính**: Apache ECharts  
> **Kiến trúc trình bày**: 4 Dashboard theo mạch câu chuyện (Storytelling)

---

### CẤU TRÚC 4 DASHBOARD (mỗi dashboard 3 biểu đồ, 1 câu hỏi chính)
Bốn dashboard nối nhau như một câu chuyện: **bức tranh chung → ở đâu → cháy rừng cụ thể → vì sao và hệ quả**.

| Dashboard | Câu hỏi chính | Biểu đồ trong dashboard |
|-----------|---------------|-------------------------|
| **D1 – Bức tranh 20 năm** (tổng quát) | Thảm họa thiên nhiên có xảy ra nhiều hơn và thiệt hại lớn hơn qua các năm không? | #1 Combo số vụ + thiệt hại; #2 Stacked area theo loại thảm họa; #5 Diverging bar chênh lệch so với trung bình |
| **D2 – Ở đâu chịu thiệt hại?** (không gian) | Quốc gia và khu vực nào chịu ảnh hưởng nặng nhất? | #3 Choropleth; #6 Treemap châu lục → quốc gia; #9 Combo Pareto top 10 quốc gia |
| **D3 – Cháy rừng: khi nào và lớn cỡ nào?** (chi tiết cháy rừng) | Cháy rừng tập trung vào mùa nào, quy mô ra sao, vụ lớn nằm ở đâu? | #4 Heatmap tháng × năm; #8 Combo histogram + mật độ; #12 Bản đồ điểm vụ cháy lớn |
| **D4 – Vì sao và hệ quả** (nguyên nhân & mức độ) | Nguyên nhân chính là gì và quy mô liên hệ thế nào với thiệt hại? | #10 Sunburst/donut nguyên nhân; #11 Sankey nguyên nhân → loại → mức thiệt hại; #7 Bubble scatter |

**Bố cục mỗi dashboard**: Dải tiêu đề (tên + câu hỏi chính) $\to$ 2–3 KPI card $\to$ 3 biểu đồ (1 biểu đồ lớn + 2 biểu đồ nhỏ, hoặc 3 cột) $\to$ Hộp "Insight" 1–2 câu $\to$ Chuyển sang dashboard kế tiếp.

---

### KỂ CHUYỆN BẰNG DỮ LIỆU (giữ đơn giản)
- Mỗi dashboard có:
  1. Tiêu đề dạng câu hỏi định hướng phân tích.
  2. Hộp "Insight" 1–2 câu nêu phát hiện chính yếu.
  3. Câu dẫn kết nối mạch tư duy sang dashboard kế tiếp. Dashboard cuối có thêm đoạn "Kết luận & Hạn chế dữ liệu" ngắn gọn.
- **Mọi con số trong Insight phải được TÍNH TỪ DỮ LIỆU THẬT** (tính bằng JavaScript từ `events.json` hoặc kiểm chứng đối chiếu bằng SQL), tuyệt đối không viết tay số liệu theo cảm tính, và phải tự động cập nhật theo bộ lọc nếu có thể.
- Tối đa 1 chú thích / annotation nổi bật trên mỗi dashboard (ví dụ đánh dấu năm đỉnh điểm thiệt hại). Không làm hoạt ảnh rườm rà, không làm chế độ trình chiếu.

---

### PHÂN CHIA 12 BIỂU ĐỒ (chia đều 4/4/4; MỖI BIỂU ĐỒ CHỈ DO 1 NGƯỜI THỰC HIỆN; mỗi người có 1 biểu đồ kết hợp)

| # | Biểu đồ | Dashboard | Kiểu dữ liệu | Bảng màu | Người phụ trách |
|---|---------|-----------|--------------|----------|-----------------|
| 1 | **Combo** cột số vụ + đường thiệt hại USD theo năm (trục kép) | D1 | thời gian + 2 số | categorical (2 màu) | **TV1** |
| 2 | Stacked area tần suất theo loại thảm họa theo năm | D1 | thời gian × phân loại | categorical | **TV1** |
| 3 | Choropleth thế giới: thiệt hại/số vụ theo quốc gia | D2 | không gian + số | sequential | **TV1** |
| 4 | Heatmap tháng × năm số vụ cháy rừng | D3 | chu kỳ × năm × số | sequential | **TV1** |
| 5 | Diverging bar chênh lệch số vụ so với trung bình 20 năm | D1 | độ lệch × thời gian | diverging (tâm = 0) | **TV2** |
| 6 | Treemap châu lục → quốc gia theo thiệt hại | D2 | phân cấp × số | categorical cấp 1 | **TV2** |
| 7 | Bubble scatter diện tích cháy vs thiệt hại USD vs người ảnh hưởng | D4 | 3 số liên tục (log-log) | categorical theo châu lục | **TV2** |
| 8 | **Combo** histogram diện tích cháy + đường phân vị lũy kế | D3 | phân phối 1 số | sequential | **TV2** |
| 9 | **Combo Pareto** cột số người chết top 10 quốc gia + đường % lũy kế | D2 | xếp hạng × lũy kế | sequential + nhấn | **TV3** |
| 10 | Sunburst/donut 2 tầng nguyên nhân tự nhiên / nhân tạo | D4 | phân cấp | categorical | **TV3** |
| 11 | Sankey nguyên nhân → loại thảm họa → mức thiệt hại | D4 | luồng đa chiều | categorical | **TV3** |
| 12 | Bản đồ điểm các vụ cháy lớn (kích thước = diện tích, màu = thiệt hại) | D3 | tọa độ + 2 số | sequential | **TV3** |

---

### TƯƠNG TÁC (giữ đơn giản, không làm quá)
- **Mọi biểu đồ**: Tooltip tiếng Việt rõ ràng, có đơn vị đo chuẩn; bấm legend để ẩn/hiện chuỗi dữ liệu tương ứng.
- **Bộ lọc chung trên thanh điều khiển**:
  - Khoảng năm (slider hoặc 2 ô chọn năm bắt đầu - kết thúc).
  - Loại thảm họa (dropdown).
  - Khi người dùng đổi bộ lọc, cả 3 biểu đồ trong dashboard hiện tại tự động cập nhật và vẽ lại mượt mà.
- **Phạm vi kiểm soát**: KHÔNG CẦN cross-filtering phức tạp giữa các biểu đồ, KHÔNG CẦN brush-and-link nếu chưa thạo, KHÔNG CẦN chế độ tối (dark mode), KHÔNG CẦN xuất PDF. Tập trung làm 12 biểu đồ đúng chuẩn dữ liệu, đẹp mắt, chạy mượt mà.

---

### QUY TRÌNH 4 BƯỚC CHO MỖI THÀNH VIÊN KHI LÀM BIỂU ĐỒ
1. **Viết query SQL** trích đúng dữ liệu cần cho biểu đồ của mình, lưu vào `sql/queries_for_charts.sql`.
2. **Tạo file JS** `dashboard/js/charts/chart-XX.js` export một hàm `renderChartXX(containerId, data, filters)` dùng ECharts.
3. **Thêm tương tác tối thiểu**: Tooltip có định dạng tiền tệ / số lượng / đơn vị rõ ràng + click bật/tắt legend.
4. **Ghi vào `CHART_SPEC.md`**: Câu hỏi phân tích, kiểu dữ liệu, vì sao chọn dạng biểu đồ này, vì sao chọn bảng màu này, và 1 câu insight rút ra từ số liệu thật.

---

## Chi Tiết Kỹ Thuật Từng Biểu Đồ

### Biểu Đồ 1: Tần suất & Tổng Thiệt hại theo năm (2006–2025)
- **Thuộc Dashboard**: D1 – Bức tranh 20 năm
- **Người phụ trách**: Thành viên 1
- **File mã nguồn**: `dashboard/js/charts/chart-01.js`
- **Câu hỏi phân tích**: Thảm họa thiên nhiên có xảy ra nhiều hơn và thiệt hại lớn hơn qua các năm không? Xu hướng số lượng các sự kiện thảm họa và quy mô thiệt hại kinh tế biến thiên như thế nào?
- **Nguồn dữ liệu & Truy vấn gợi ý**: `fact_disaster_event` JOIN `dim_date`.
  ```sql
  SELECT d.year, COUNT(f.event_id) AS event_count, SUM(f.damage_usd) / 1e9 AS total_damage_bil_usd
  FROM fact_disaster_event f JOIN dim_date d ON f.date_id = d.date_id
  GROUP BY d.year ORDER BY d.year;
  ```
- **Kiểu dữ liệu**: Thời gian rời rạc (Năm) + 2 đại lượng định lượng có đơn vị đo khác nhau (Số vụ vs Tỷ USD).
- **Lý do chọn biểu đồ**: Dạng biểu đồ kết hợp (**Combo** Bar + Line) trục kép là giải pháp trực quan kinh điển và tối ưu nhất để đặt hai thước đo khác đơn vị lên cùng một không gian thời gian.
- **Lý do chọn màu**: Hai màu tương phản cao (Cột xanh `#4A90E2` và Đường cam đỏ `#D55E00`) giúp thị giác phân biệt tức thì hai trục đo.
- **Tương tác**: Hover tooltip hiển thị song song hai chỉ số; bấm legend ẩn/hiện cột hoặc đường; phản hồi bộ lọc năm.

---

### Biểu Đồ 2: Diễn Biến Cơ Cấu Thảm Họa Theo Thời Gian
- **Thuộc Dashboard**: D1 – Bức tranh 20 năm
- **Người phụ trách**: Thành viên 1
- **File mã nguồn**: `dashboard/js/charts/chart-02.js`
- **Câu hỏi phân tích**: Tỷ trọng và số lượng của thảm họa Cháy rừng (Wildfire) so với Lũ lụt, Bão, Hạn hán thay đổi như thế nào trong 20 năm qua?
- **Nguồn dữ liệu & Truy vấn gợi ý**: `fact_disaster_event`, `dim_date`, `dim_disaster_type`.
- **Kiểu dữ liệu**: Chuỗi thời gian liên tục $\times$ Biến phân loại (Categorical).
- **Lý do chọn biểu đồ**: Stacked Area Chart trực quan hóa đồng thời sự biến thiên của tổng thể lẫn xu hướng thay đổi thành phần đóng góp của từng loại thảm họa.
- **Lý do chọn màu**: Áp dụng bảng màu Okabe-Ito chuẩn cho `disaster_type`, Wildfire luôn giữ màu `#D55E00`.
- **Tương tác**: Bật/tắt từng loại thảm họa trên Legend; tooltip hiển thị số vụ và tỷ lệ phần trăm theo năm.

---

### Biểu Đồ 3: Bản Đồ Thiệt Hại / Tần Suất Toàn Cầu (Choropleth Map)
- **Thuộc Dashboard**: D2 – Ở đâu chịu thiệt hại?
- **Người phụ trách**: Thành viên 1
- **File mã nguồn**: `dashboard/js/charts/chart-03.js`
- **Câu hỏi phân tích**: Quốc gia và khu vực nào trên thế giới chịu ảnh hưởng nặng nề nhất về tần suất và tổng thiệt hại tài chính?
- **Nguồn dữ liệu & Truy vấn gợi ý**: `fact_disaster_event` JOIN `dim_location`.
- **Kiểu dữ liệu**: Không gian địa lý (GeoJSON polygons theo ISO3) $\times$ Đại lượng số.
- **Lý do chọn biểu đồ**: Choropleth là phương tiện chuẩn mực để truyền tải bức tranh phân bố vĩ mô toàn cầu.
- **Lý do chọn màu**: Dải màu tuần tự Sequential (OrRd: `#FFF5EB` $\to$ `#8C2D04`), phân vị theo Quantile để tránh bão hòa ở các nước có số liệu quá cao.
- **Tương tác**: Tooltip chi tiết tên quốc gia, số vụ và tổng thiệt hại; VisualMap slider điều khiển ngưỡng giá trị.

---

### Biểu Đồ 4: Ma Trận Mùa Vụ Cháy Rừng (Tháng $\times$ Năm)
- **Thuộc Dashboard**: D3 – Cháy rừng: khi nào và lớn cỡ nào?
- **Người phụ trách**: Thành viên 1
- **File mã nguồn**: `dashboard/js/charts/chart-04.js`
- **Câu hỏi phân tích**: Cháy rừng tập trung vào các tháng nào trong năm? Mùa cháy có xu hướng kéo dài hơn hoặc dịch chuyển sang các tháng bất thường trong những năm gần đây không?
- **Nguồn dữ liệu & Truy vấn gợi ý**: `fact_disaster_event`, `dim_date`, `dim_disaster_type` WHERE `type_name = 'Wildfire'`.
- **Kiểu dữ liệu**: Chu kỳ thời gian $\times$ Năm $\times$ Số vụ cháy.
- **Lý do chọn biểu đồ**: Heatmap 2D trực quan hóa mật độ tập trung cực kỳ hiệu quả cho dữ liệu chu kỳ thời gian.
- **Lý do chọn màu**: Dải Sequential YlOrRd phản ánh đúng ngữ nghĩa "nhiệt độ/cháy".
- **Tương tác**: Tooltip chi tiết tháng, năm và số vụ cháy; phản hồi bộ lọc loại thảm họa.

---

### Biểu Đồ 5: Biến Động Số Vụ Cháy So Với Mức Chuẩn Trung Bình 20 Năm
- **Thuộc Dashboard**: D1 – Bức tranh 20 năm
- **Người phụ trách**: Thành viên 2
- **File mã nguồn**: `dashboard/js/charts/chart-05.js`
- **Câu hỏi phân tích**: Những năm nào số vụ thiên tai/cháy rừng vượt ngưỡng trung bình lịch sử (năm khốc liệt), và những năm nào dưới mức chuẩn?
- **Nguồn dữ liệu & Truy vấn gợi ý**: `fact_disaster_event`, `dim_date`, tính toán độ lệch: $\Delta_y = N_y - \bar{N}_{20\text{yr}}$.
- **Kiểu dữ liệu**: Độ lệch số học mang dấu (Âm/Dương) so với giá trị tham chiếu 0.
- **Lý do chọn biểu đồ**: Diverging Bar Chart là chuẩn mực tối ưu cho việc quan sát giá trị thặng dư / thiếu hụt so với chuẩn (Baseline).
- **Lý do chọn màu**: Bảng màu phân kỳ Diverging (Đỏ: vượt mức trung bình, Xanh: thấp hơn trung bình, Trắng/Xám: điểm cân bằng 0).
- **Tương tác**: Hover hiển thị số vụ thực tế, mức trung bình 20 năm và độ lệch tuyệt đối / %.

---

### Biểu Đồ 6: Cơ Cấu Thiệt Hại Kinh Tế Phân Cấp Theo Châu Lục $\to$ Quốc Gia
- **Thuộc Dashboard**: D2 – Ở đâu chịu thiệt hại?
- **Người phụ trách**: Thành viên 2
- **File mã nguồn**: `dashboard/js/charts/chart-06.js`
- **Câu hỏi phân tích**: Thiệt hại tài chính phân bổ thế nào giữa các châu lục, và trong từng châu lục quốc gia nào chiếm tỷ trọng thiệt hại chi phối?
- **Nguồn dữ liệu & Truy vấn gợi ý**: `fact_disaster_event` JOIN `dim_location`. Cấu trúc cây 2 cấp: Continent $\to$ Country.
- **Kiểu dữ liệu**: Dữ liệu phân cấp (Hierarchical Tree) $\times$ Biến định lượng (Tổng thiệt hại USD).
- **Lý do chọn biểu đồ**: Treemap tối ưu hóa diện tích hiển thị tỷ trọng phân cấp mà không bị rối như Pie chart nhiều phần tử.
- **Lý do chọn màu**: Phân màu theo Châu lục (Categorical), độ đậm nhạt trong từng khối thể hiện quy mô giá trị.
- **Tương tác**: Tooltip hiển thị tỷ lệ % đóng góp và số tiền thiệt hại quy đổi.

---

### Biểu Đồ 7: Tương Quan Diện Tích Cháy vs Thiệt Hại Kinh Tế vs Người Ảnh Hưởng
- **Thuộc Dashboard**: D4 – Vì sao và hệ quả
- **Người phụ trách**: Thành viên 2
- **File mã nguồn**: `dashboard/js/charts/chart-07.js`
- **Câu hỏi phân tích**: Quy mô đám cháy liên hệ thế nào với thiệt hại? Có phải diện tích cháy rừng càng lớn thì thiệt hại kinh tế và số người ảnh hưởng càng cao không?
- **Nguồn dữ liệu & Truy vấn gợi ý**: `fact_wildfire_detail` JOIN `fact_disaster_event` JOIN `dim_location`.
- **Kiểu dữ liệu**: 3 biến số liên tục (Trục X: Diện tích ha; Trục Y: Thiệt hại USD; Kích thước bóng: Số người ảnh hưởng) $\times$ 1 biến danh mục (Màu bóng: Châu lục).
- **Lý do chọn biểu đồ**: Bubble Scatter trên hệ tọa độ Log-Log ($\log_{10} X, \log_{10} Y$) giải quyết triệt để hiện tượng lệch phải và co cụm điểm của dữ liệu thảm họa.
- **Lý do chọn màu**: Categorical theo Châu lục để so sánh hình thái ảnh hưởng theo địa lý.
- **Tương tác**: Tooltip chi tiết tên vụ cháy, tọa độ, diện tích và thiệt hại.

---

### Biểu Đồ 8: Phân Phối Quy Mô Diện Tích Cháy (Combo Histogram + Lũy Kế)
- **Thuộc Dashboard**: D3 – Cháy rừng: khi nào và lớn cỡ nào?
- **Người phụ trách**: Thành viên 2
- **File mã nguồn**: `dashboard/js/charts/chart-08.js`
- **Câu hỏi phân tích**: Các vụ cháy rừng tập trung ở quy mô diện tích nào? Tần suất xuất hiện của các siêu đám cháy (Mega-fires) hiếm gặp ra sao?
- **Nguồn dữ liệu & Truy vấn gợi ý**: `fact_wildfire_detail` (`burned_area_ha` chia theo các bin logarit).
- **Kiểu dữ liệu**: Phân phối tần suất 1 biến số liên tục.
- **Lý do chọn biểu đồ**: **Combo** Histogram (Cột tần số) kết hợp Đường phân vị lũy kế giúp người xem nắm bắt cả số lượng tuyệt đối lẫn tỷ lệ phần trăm tích lũy.
- **Lý do chọn màu**: Sequential đơn sắc cam đất cho cột và đường nét liền xanh sẫm cho đường phân vị.
- **Tương tác**: Tooltip hiển thị khoảng khoảng bin (ha) và số lượng vụ cháy tương ứng.

---

### Biểu Đồ 9: Xếp Hạng Thiệt Hại Sinh Mạng Quốc Gia (Combo Pareto Chart)
- **Thuộc Dashboard**: D2 – Ở đâu chịu thiệt hại?
- **Người phụ trách**: Thành viên 3
- **File mã nguồn**: `dashboard/js/charts/chart-09.js`
- **Câu hỏi phân tích**: Top 10 quốc gia nào chiếm phần lớn tổng số ca tử vong do thảm họa thiên nhiên? Nguyên lý 80/20 có thể hiện rõ không?
- **Nguồn dữ liệu & Truy vấn gợi ý**: `fact_disaster_event` JOIN `dim_location`, sắp xếp giảm dần theo tổng `deaths`, tính đường % lũy kế.
- **Kiểu dữ liệu**: Dữ liệu xếp hạng thứ bậc (Ordinal/Ranking) $\times$ Số lượng tuyệt đối + Tỷ lệ % tích lũy.
- **Lý do chọn biểu đồ**: **Combo Pareto** (Cột số người chết kết hợp Đường tỷ lệ phần trăm lũy kế) làm nổi bật nhóm thiểu số gây ra hậu quả chiếm đa số.
- **Lý do chọn màu**: Cột tông màu đỏ tím cảnh báo, đường lũy kế màu vàng cam nổi bật kèm đường mốc tham chiếu 80%.
- **Tương tác**: Hover xem chi tiết số ca tử vong và tỷ lệ tích lũy của từng quốc gia.

---

### Biểu Đồ 10: Phân Tích Cơ Cấu Nguyên Nhân Cháy Rừng (Sunburst / Multi-level Donut)
- **Thuộc Dashboard**: D4 – Vì sao và hệ quả
- **Người phụ trách**: Thành viên 3
- **File mã nguồn**: `dashboard/js/charts/chart-10.js`
- **Câu hỏi phân tích**: Nguyên nhân chính gây cháy rừng là gì? Đâu là nguồn gốc chính (Yếu tố tự nhiên như sấm sét vs Tác động của con người)? Tỷ lệ từng tác nhân cụ thể là bao nhiêu?
- **Nguồn dữ liệu & Truy vấn gợi ý**: `fact_disaster_event` JOIN `dim_cause` (Cấp 1: Tự nhiên / Nhân tạo, Cấp 2: Nguyên nhân chi tiết).
- **Kiểu dữ liệu**: Biến danh mục phân cấp 2 tầng (Hierarchical Categorical).
- **Lý do chọn biểu đồ**: Sunburst / Donut 2 tầng thể hiện xuất sắc mối quan hệ cha–con từ nhóm nguyên nhân tổng quát đến từng tác nhân cụ thể theo góc tỏa tròn.
- **Lý do chọn màu**: Bảng màu phân loại chuẩn (Xanh cho Tự nhiên, Cam đỏ cho Con người, Xám cho Chưa xác định).
- **Tương tác**: Click vào một phân vùng để zoom-in; giữa tâm hiển thị thông số tổng hợp khi hover.

---

### Biểu Đồ 11: Dòng Chuyển Giao Tác Động Thảm Họa (Sankey Diagram)
- **Thuộc Dashboard**: D4 – Vì sao và hệ quả
- **Người phụ trách**: Thành viên 3
- **File mã nguồn**: `dashboard/js/charts/chart-11.js`
- **Câu hỏi phân tích**: Mối liên hệ luồng di chuyển từ Nhóm nguyên nhân $\to$ Loại thảm họa $\to$ Mức độ thiệt hại diễn ra như thế nào?
- **Nguồn dữ liệu & Truy vấn gợi ý**: `dim_cause` $\to$ `dim_disaster_type` $\to$ Phân nhóm mức độ thiệt hại (`damage_level`: Thấp, Trung bình, Nghiêm trọng, Thảm họa).
- **Kiểu dữ liệu**: Dữ liệu mạng lưới đa tầng (Multi-stage Flow Graph) có trọng số luồng.
- **Lý do chọn biểu đồ**: Sankey Diagram là công cụ trực quan hóa duy nhất thể hiện được sự phân luồng và hội tụ giữa nhiều biến phân loại qua từng giai đoạn tác động.
- **Lý do chọn màu**: Màu các node tương ứng với loại thảm họa; màu đường dẫn (links) kế thừa độ dốc màu (gradient).
- **Tương tác**: Hover vào luồng để làm sáng rực rỡ (highlight) toàn bộ đường đi từ đầu đến cuối.

---

### Biểu Đồ 12: Bản Đồ Điểm Các Đại Vụ Cháy Lớn (Proportional Symbol Map)
- **Thuộc Dashboard**: D3 – Cháy rừng: khi nào và lớn cỡ nào?
- **Người phụ trách**: Thành viên 3
- **File mã nguồn**: `dashboard/js/charts/chart-12.js`
- **Câu hỏi phân tích**: Các vụ cháy lớn nằm ở đâu trên bản đồ? Quy mô diện tích và thiệt hại phân bổ ra sao theo không gian tọa độ?
- **Nguồn dữ liệu & Truy vấn gợi ý**: `fact_disaster_event` JOIN `fact_wildfire_detail` lấy `latitude`, `longitude`, `burned_area_ha`, `damage_usd`.
- **Kiểu dữ liệu**: Tọa độ địa lý (Point / Coordinates) $\times$ 2 biến định lượng (Kích thước vòng tròn = Diện tích cháy; Màu vòng tròn = Mức độ thiệt hại).
- **Lý do chọn biểu đồ**: Bản đồ điểm định lượng (Proportional Symbol Map) biểu diễn chính xác tọa độ thực tế của tâm đám cháy mà không bị giới hạn bởi ranh giới hành chính.
- **Lý do chọn màu**: Dải màu tuần tự Sequential cảnh báo nhiệt độ cao (Đỏ cam), độ trong suốt để nhìn thấu các điểm chồng lấn.
- **Tương tác**: Click vào điểm cháy để hiển thị popup thông tin chi tiết tên vụ cháy, tọa độ, diện tích và thiệt hại.
