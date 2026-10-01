# Đặc Tả 12 Biểu Đồ Trực Quan Hóa (CHART SPECIFICATIONS)

> **Nhóm thực hiện**: Phân chia đều 4/4/4 (TV1: #1–#4, TV2: #5–#8, TV3: #9–#12)  
> **Thư viện chính**: Apache ECharts  
> **Trạng thái**: Khung đặc tả kỹ thuật kiến trúc biểu đồ (Giai đoạn 1)

---

## Danh Mục Phân Chia Trách Nhiệm 12 Biểu Đồ

| # | Tên Biểu Đồ | Dạng Biểu Đồ | Kiểu Dữ Liệu | Bảng Màu | Người Phụ Trách |
|---|-------------|--------------|--------------|----------|-----------------|
| 1 | Tần suất & Thiệt hại theo năm | **Combo** Bar (Số vụ) + Line (Thiệt hại USD) trục kép | Thời gian + 2 Số liên tục | Categorical (2 màu tương phản) | Thành viên 1 |
| 2 | Diễn biến cơ cấu thảm họa theo thời gian | Stacked Area (Diện tích xếp chồng) | Thời gian $\times$ Phân loại | Categorical (Okabe-Ito thảm họa) | Thành viên 1 |
| 3 | Bản đồ thiệt hại / số vụ toàn cầu | Choropleth Map (Bản đồ phân vùng thế giới) | Không gian $\times$ Số liên tục | Sequential (OrRd) | Thành viên 1 |
| 4 | Ma trận chu kỳ mùa cháy rừng | Heatmap (Tháng $\times$ Năm) | Chu kỳ thời gian $\times$ Thời gian $\times$ Số | Sequential (YlOrRd) | Thành viên 1 |
| 5 | Biến động tần suất so với chuẩn 20 năm | Diverging Bar (Cột phân kỳ) | Độ lệch $\times$ Thời gian | Diverging (RdBu, tâm = 0) | Thành viên 2 |
| 6 | Cơ cấu thiệt hại kinh tế phân cấp | Treemap (Châu lục $\to$ Quốc gia) | Phân cấp $\times$ Định lượng | Sequential / Categorical cấp 1 | Thành viên 2 |
| 7 | Tương quan Diện tích – Thiệt hại – Quy mô | Bubble Scatter (Biểu đồ bong bóng, trục log) | 3 Số liên tục $\times$ Phân loại | Categorical (Màu theo Châu lục) | Thành viên 2 |
| 8 | Phân phối quy mô diện tích cháy rừng | **Combo** Histogram + Mật độ KDE / Lũy kế | Phân phối 1 biến liên tục | Sequential đơn sắc | Thành viên 2 |
| 9 | Xếp hạng thiệt hại sinh mạng quốc gia | **Combo Pareto** Bar (Tử vong) + Line (% Lũy kế) | Xếp hạng $\times$ Tỷ trọng lũy kế | Sequential + Màu nhấn | Thành viên 3 |
| 10 | Phân tích cơ cấu nguyên nhân cháy rừng | Sunburst / Donut nhiều tầng | Cấu phần phân cấp | Categorical (Nguyên nhân) | Thành viên 3 |
| 11 | Dòng chuyển giao tác động thảm họa | Sankey Diagram (Nguyên nhân $\to$ Thảm họa $\to$ Thiệt hại) | Luồng quan hệ đa chiều | Categorical | Thành viên 3 |
| 12 | Bản đồ phân bố không gian các vụ cháy lớn | Proportional Symbol Map (Bản đồ điểm định lượng) | Tọa độ (Kinh/Vĩ) + 2 Số liên tục | Sequential / Kích thước | Thành viên 3 |

---

## Chi Tiết Kỹ Thuật Từng Biểu Đồ

### Biểu Đồ 1: Tần suất & Tổng Thiệt hại theo năm (2006–2025)
- **Người phụ trách**: Thành viên 1
- **File mã nguồn**: `dashboard/js/charts/chart-01.js`
- **Câu hỏi phân tích**: Xu hướng số lượng các sự kiện thảm họa và quy mô thiệt hại kinh tế biến thiên như thế nào qua 20 năm? Có sự bùng nổ đột biến ở các năm gần đây không?
- **Nguồn dữ liệu & Truy vấn**: `fact_disaster_event` JOIN `dim_date`.
  ```sql
  SELECT d.year, COUNT(f.event_id) AS event_count, SUM(f.damage_usd) / 1e9 AS total_damage_bil_usd
  FROM fact_disaster_event f JOIN dim_date d ON f.date_id = d.date_id
  GROUP BY d.year ORDER BY d.year;
  ```
- **Kiểu dữ liệu**: Thời gian rời rạc (Năm) + 2 đại lượng định lượng có đơn vị đo khác nhau (Số vụ vs Tỷ USD).
- **Lý do chọn biểu đồ**: Dạng biểu đồ kết hợp (Combo Bar + Line) trục kép là giải pháp trực quan kinh điển và tối ưu nhất để đặt hai thước đo khác đơn vị lên cùng một không gian thời gian.
- **Lý do chọn màu**: Hai màu tương phản cao (Cột xám xanh `#4A90E2` và Đường cam đỏ `#D55E00`) giúp thị giác phân biệt tức thì hai trục đo.
- **Tương tác**: Hover tooltip hiển thị song song hai chỉ số; Brush chọn dải năm trên trục hoành để đồng bộ bộ lọc toàn cục.
- **Insight sơ bộ (Dữ liệu thật)**: *[Sẽ cập nhật sau khi nạp dữ liệu Giai đoạn 2]*

---

### Biểu Đồ 2: Diễn Biến Cơ Cấu Thảm Họa Theo Thời Gian
- **Người phụ trách**: Thành viên 1
- **File mã nguồn**: `dashboard/js/charts/chart-02.js`
- **Câu hỏi phân tích**: Tỷ trọng và số lượng của thảm họa Cháy rừng (Wildfire) so với Lũ lụt, Bão, Hạn hán thay đổi như thế nào trong 20 năm qua?
- **Nguồn dữ liệu & Truy vấn**: `fact_disaster_event`, `dim_date`, `dim_disaster_type`.
- **Kiểu dữ liệu**: Chuỗi thời gian liên tục $\times$ Biến phân loại (Categorical).
- **Lý do chọn biểu đồ**: Stacked Area Chart trực quan hóa đồng thời sự biến thiên của tổng thể lẫn xu hướng thay đổi thành phần đóng góp của từng loại thảm họa.
- **Lý do chọn màu**: Áp dụng bảng màu Okabe-Ito chuẩn cho `disaster_type`, Wildfire luôn giữ màu `#D55E00`.
- **Tương tác**: Bật/tắt từng loại thảm họa trên Legend; Click vào diện tích của một loại thảm họa để cross-filter các biểu đồ khác.
- **Insight sơ bộ**: *[Sẽ cập nhật sau khi nạp dữ liệu Giai đoạn 2]*

---

### Biểu Đồ 3: Bản Đồ Thiệt Hại / Tần Suất Toàn Cầu (Choropleth Map)
- **Người phụ trách**: Thành viên 1
- **File mã nguồn**: `dashboard/js/charts/chart-03.js`
- **Câu hỏi phân tích**: Những quốc gia hoặc vùng lãnh thổ nào chịu ảnh hưởng nặng nề nhất về tần suất và tổng thiệt hại tài chính?
- **Nguồn dữ liệu & Truy vấn**: `fact_disaster_event` JOIN `dim_location`.
- **Kiểu dữ liệu**: Không gian địa lý (GeoJSON polygons theo ISO3) $\times$ Đại lượng số.
- **Lý do chọn biểu đồ**: Choropleth là phương tiện chuẩn mực để truyền tải bức tranh phân bố vĩ mô toàn cầu.
- **Lý do chọn màu**: Dải màu tuần tự Sequential (OrRd: `#FFF5EB` $\to$ `#8C2D04`), phân vị theo Quantile để tránh bão hòa ở các nước có số liệu quá cao.
- **Tương tác**: Công tắc chuyển đổi giữa 2 chỉ số: "Số lượng vụ" và "Tổng thiệt hại USD"; Click vào quốc gia để lọc dữ liệu toàn dashboard cho quốc gia đó; VisualMap slider.
- **Insight sơ bộ**: *[Sẽ cập nhật sau khi nạp dữ liệu Giai đoạn 2]*

---

### Biểu Đồ 4: Ma Trận Mùa Vụ Cháy Rừng (Tháng $\times$ Năm)
- **Người phụ trách**: Thành viên 1
- **File mã nguồn**: `dashboard/js/charts/chart-04.js`
- **Câu hỏi phân tích**: Mùa cao điểm cháy rừng diễn ra vào các tháng nào trong năm? Mùa cháy có xu hướng kéo dài hơn hoặc dịch chuyển sang các tháng bất thường trong những năm gần đây không?
- **Nguồn dữ liệu & Truy vấn**: `fact_disaster_event`, `dim_date`, `dim_disaster_type` WHERE `type_name = 'Wildfire'`.
- **Kiểu dữ liệu**: Hai biến chu kỳ/thời gian (Tháng: 1..12 $\times$ Năm: 2006..2025) $\times$ Số vụ cháy.
- **Lý do chọn biểu đồ**: Heatmap 2D trực quan hóa mật độ tập trung cực kỳ hiệu quả cho dữ liệu chu kỳ thời gian.
- **Lý do chọn màu**: Dải Sequential YlOrRd phản ánh đúng ngữ nghĩa "nhiệt độ/cháy".
- **Tương tác**: Tooltip chi tiết ngày tháng; Click chọn ô tháng/năm cụ thể để lọc.
- **Insight sơ bộ**: *[Sẽ cập nhật sau khi nạp dữ liệu Giai đoạn 2]*

---

### Biểu Đồ 5: Biến Động Số Vụ Cháy So Với Mức Chuẩn Trung Bình 20 Năm
- **Người phụ trách**: Thành viên 2
- **File mã nguồn**: `dashboard/js/charts/chart-05.js`
- **Câu hỏi phân tích**: Những năm nào số vụ cháy vượt ngưỡng trung bình lịch sử (năm khốc liệt), và những năm nào dưới mức chuẩn?
- **Nguồn dữ liệu & Truy vấn**: `fact_disaster_event`, `dim_date`, tính toán độ lệch: $\Delta_y = N_y - \bar{N}_{20\text{yr}}$.
- **Kiểu dữ liệu**: Độ lệch số học mang dấu (Âm/Dương) so với giá trị tham chiếu 0.
- **Lý do chọn biểu đồ**: Diverging Bar Chart là chuẩn mực tối ưu cho việc quan sát giá trị thặng dư / thiếu hụt so với chuẩn (Baseline).
- **Lý do chọn màu**: Bảng màu phân kỳ Diverging RdBu (Đỏ: vượt mức trung bình, Xanh: thấp hơn trung bình, Trắng/Xám: điểm cân bằng 0).
- **Tương tác**: Hover hiển thị số vụ thực tế, mức trung bình và % độ lệch; Hover highlight thanh cột.
- **Insight sơ bộ**: *[Sẽ cập nhật sau khi nạp dữ liệu Giai đoạn 2]*

---

### Biểu Đồ 6: Phân Cấp Thiệt Hại Kinh Tế Theo Châu Lục $\to$ Quốc Gia
- **Người phụ trách**: Thành viên 2
- **File mã nguồn**: `dashboard/js/charts/chart-06.js`
- **Câu hỏi phân tích**: Thiệt hại tài chính phân bổ thế nào giữa các châu lục, và trong từng châu lục quốc gia nào chiếm tỷ trọng thiệt hại chi phối?
- **Nguồn dữ liệu & Truy vấn**: `fact_disaster_event` JOIN `dim_location`. Cấu trúc cây 2 cấp: Continent $\to$ Country.
- **Kiểu dữ liệu**: Dữ liệu phân cấp (Hierarchical Tree) $\times$ Biến định lượng (Tổng thiệt hại USD).
- **Lý do chọn biểu đồ**: Treemap tối ưu hóa diện tích hiển thị tỷ trọng phân cấp mà không bị rối như Pie chart nhiều phần tử tử.
- **Lý do chọn màu**: Phân màu theo Châu lục (Categorical), độ đậm nhạt trong từng khối thể hiện quy mô giá trị (Sequential).
- **Tương tác**: Click vào Châu lục để drill-down phóng to xem chi tiết các quốc gia; Breadcrumb điều hướng quay lại cấp trên.
- **Insight sơ bộ**: *[Sẽ cập nhật sau khi nạp dữ liệu Giai đoạn 2]*

---

### Biểu Đồ 7: Tương Quan Diện Tích Cháy vs Thiệt Hại Kinh Tế
- **Người phụ trách**: Thành viên 2
- **File mã nguồn**: `dashboard/js/charts/chart-07.js`
- **Câu hỏi phân tích**: Có phải diện tích cháy rừng càng lớn thì thiệt hại kinh tế càng cao không? Số lượng người bị ảnh hưởng có liên hệ thế nào với hai đại lượng trên?
- **Nguồn dữ liệu & Truy vấn**: `fact_wildfire_detail` JOIN `fact_disaster_event` JOIN `dim_location`.
- **Kiểu dữ liệu**: 3 biến số liên tục (Trục X: Diện tích ha; Trục Y: Thiệt hại USD; Kích thước bóng: Số người ảnh hưởng) $\times$ 1 biến danh mục (Màu bóng: Châu lục).
- **Lý do chọn biểu đồ**: Bubble Chart trên hệ tọa độ Log-Log ($\log_{10} X, \log_{10} Y$) giải quyết triệt để hiện tượng lệch phải và co cụm điểm của dữ liệu thảm họa.
- **Lý do chọn màu**: Categorical theo Châu lục để so sánh hình thái ảnh hưởng theo địa lý.
- **Tương tác**: Brush chọn một cụm điểm trên đồ thị để lọc đồng bộ; Tooltip chi tiết tên thảm họa và quy mô.
- **Insight sơ bộ**: *[Sẽ cập nhật sau khi nạp dữ liệu Giai đoạn 2]*

---

### Biểu Đồ 8: Phân Phối Quy Mô Diện Tích Cháy (Combo Histogram + KDE/Lũy Kế)
- **Người phụ trách**: Thành viên 2
- **File mã nguồn**: `dashboard/js/charts/chart-08.js`
- **Câu hỏi phân tích**: Các vụ cháy rừng tập trung ở quy mô diện tích nào? Tần suất xuất hiện của các siêu đám cháy (Mega-fires) hiếm gặp ra sao?
- **Nguồn dữ liệu & Truy vấn**: `fact_wildfire_detail` (cột `burned_area_ha` chia theo các bin logarit: $<100$ha, $100-1.000$ha, $1.000-10.000$ha, $>10.000$ha).
- **Kiểu dữ liệu**: Phân phối tần suất 1 biến số liên tục.
- **Lý do chọn biểu đồ**: Combo Histogram (Cột tần số) kết hợp Đường cong mật độ tích lũy (Cumulative line / KDE) giúp người xem nắm bắt cả số lượng tuyệt đối lẫn tỷ lệ phần trăm phân vị.
- **Lý do chọn màu**: Sequential đơn sắc cam đất `#E65100` cho cột và đường nét liền xanh sẫm `#0D47A1` cho đường phân vị.
- **Tương tác**: Tooltip hiển thị khoảng bin và số lượng vụ; Thanh trượt điều chỉnh số lượng bin hoặc chuyển đổi thang đo.
- **Insight sơ bộ**: *[Sẽ cập nhật sau khi nạp dữ liệu Giai đoạn 2]*

---

### Biểu Đồ 9: Xếp Hạng Thiệt Hại Sinh Mạng (Combo Pareto Chart)
- **Người phụ trách**: Thành viên 3
- **File mã nguồn**: `dashboard/js/charts/chart-09.js`
- **Câu hỏi phân tích**: Nguyên lý 80/20 có xảy ra với thiệt hại về người không? Top 10 quốc gia nào chiếm phần lớn tổng số ca tử vong do thảm họa thiên nhiên?
- **Nguồn dữ liệu & Truy vấn**: `fact_disaster_event` JOIN `dim_location`, sắp xếp giảm dần theo tổng `deaths`, tính đường % lũy kế `SUM(deaths) OVER (...) / TOTAL * 100`.
- **Kiểu dữ liệu**: Dữ liệu xếp hạng thứ bậc (Ordinal/Ranking) $\times$ Số lượng tuyệt đối + Tỷ lệ % tích lũy.
- **Lý do chọn biểu đồ**: Pareto Chart (Cột số ca tử vong kết hợp Đường tỷ lệ phần trăm lũy kế) làm nổi bật nhóm thiểu số gây ra hậu quả chiếm đa số (Vital Few).
- **Lý do chọn màu**: Cột tông màu đỏ tím cảnh báo `#882255`, đường lũy kế màu vàng cam nổi bật `#E69F00` kèm đường mốc tham chiếu 80%.
- **Tương tác**: Click vào cột quốc gia để kích hoạt bộ lọc toàn hệ thống cho quốc gia đó; Hover xem chi tiết số ca tử vong.
- **Insight sơ bộ**: *[Sẽ cập nhật sau khi nạp dữ liệu Giai đoạn 2]*

---

### Biểu Đồ 10: Phân Tích Cơ Cấu Nguyên Nhân Cháy Rừng (Sunburst / Multi-level Donut)
- **Người phụ trách**: Thành viên 3
- **File mã nguồn**: `dashboard/js/charts/chart-10.js`
- **Câu hỏi phân tích**: Đâu là nguồn gốc chính gây bùng phát các vụ cháy rừng (Yếu tố tự nhiên như sét đánh vs Tác động của con người)? Tỷ lệ từng nguyên nhân chi tiết trong từng nhóm là bao nhiêu?
- **Nguồn dữ liệu & Truy vấn**: `fact_disaster_event` JOIN `dim_cause` (Cấp 1: `cause_group`, Cấp 2: `cause_name`).
- **Kiểu dữ liệu**: Biến danh mục phân cấp 2 tầng (Hierarchical Categorical).
- **Lý do chọn biểu đồ**: Sunburst Chart thể hiện xuất sắc mối quan hệ cha–con từ nhóm nguyên nhân tổng quát đến từng tác nhân cụ thể theo góc tỏa tròn.
- **Lý do chọn màu**: Áp dụng bảng màu phân loại chuẩn của nhóm nguyên nhân (Xanh cho Tự nhiên, Cam đỏ cho Con người, Xám cho Chưa xác định).
- **Tương tác**: Click vào một nhánh để phóng to góc nhìn (zoom-in); Giữa tâm hiển thị thông số tổng hợp khi hover.
- **Insight sơ bộ**: *[Sẽ cập nhật sau khi nạp dữ liệu Giai đoạn 2]*

---

### Biểu Đồ 11: Dòng Chuyển Giao Tác Động Thảm Họa (Sankey Diagram)
- **Người phụ trách**: Thành viên 3
- **File mã nguồn**: `dashboard/js/charts/chart-11.js`
- **Câu hỏi phân tích**: Mối liên hệ luồng di chuyển từ Nguồn gốc phát sinh $\to$ Loại thảm họa $\to$ Mức độ thiệt hại kinh tế diễn ra như thế nào?
- **Nguồn dữ liệu & Truy vấn**: `dim_cause` $\to$ `dim_disaster_type` $\to$ Phân nhóm mức độ thiệt hại (`damage_level`: Thấp, Trung bình, Nghiêm trọng, Thảm họa).
- **Kiểu dữ liệu**: Dữ liệu mạng lưới đa tầng (Multi-stage Flow Graph) có trọng số luồng (Lưu lượng = Số vụ hoặc Tổng thiệt hại).
- **Lý do chọn biểu đồ**: Sankey Diagram là công cụ trực quan hóa duy nhất thể hiện được sự phân luồng và hội tụ giữa nhiều biến phân loại qua từng giai đoạn tác động.
- **Lý do chọn màu**: Màu các node tương ứng với định danh loại thảm họa; màu đường dẫn (links) kế thừa độ dốc màu (gradient) giữa nguồn và đích.
- **Tương tác**: Hover vào luồng để sáng rực rỡ (highlight) toàn bộ đường đi từ đầu đến cuối; kéo thả vị trí các node để quan sát trực quan.
- **Insight sơ bộ**: *[Sẽ cập nhật sau khi nạp dữ liệu Giai đoạn 2]*

---

### Biểu Đồ 12: Bản Đồ Điểm Các Đại Thảm Họa Cháy Rừng (Proportional Symbol Map)
- **Người phụ trách**: Thành viên 3
- **File mã nguồn**: `dashboard/js/charts/chart-12.js`
- **Câu hỏi phân tích**: Vị trí tọa độ chính xác của các vụ cháy rừng lớn nhất thế giới nằm ở đâu? Mức độ nghiêm trọng và diện tích cháy phân bố ra sao theo không gian?
- **Nguồn dữ liệu & Truy vấn**: `fact_disaster_event` JOIN `fact_wildfire_detail` lấy `latitude`, `longitude`, `burned_area_ha`, `damage_usd`, `year`.
- **Kiểu dữ liệu**: Tọa độ địa lý (Point / Coordinates) $\times$ 2 biến định lượng (Kích thước vòng tròn = Diện tích cháy; Màu vòng tròn = Mức độ thiệt hại).
- **Lý do chọn biểu đồ**: Proportional Symbol Map biểu diễn chính xác tọa độ thực tế của tâm đám cháy mà không bị giới hạn bởi ranh giới hành chính quốc gia.
- **Lý do chọn màu**: Dải màu tuần tự Sequential cảnh báo nhiệt độ cao (Đỏ sẫm/Cam đậm `#D94801`), độ trong suốt `opacity = 0.7` để nhìn thấu các điểm chồng lấn (Overlapping points).
- **Tương tác**: Thanh trượt thời gian động (Timeline Player) lọc theo năm; Click vào điểm cháy để hiển thị popup thông tin chi tiết tên vụ cháy, ngày bắt đầu và tọa độ.
- **Insight sơ bộ**: *[Sẽ cập nhật sau khi nạp dữ liệu Giai đoạn 2]*
