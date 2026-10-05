# Danh Mục Các Trường Tính Toán Trong Tableau (CALCULATED FIELDS)

> Tài liệu hướng dẫn Thành viên 1, Thành viên 2, Thành viên 3 tạo các trường tính toán (Calculated Fields) trong Tableau Desktop / Tableau Public để phục vụ cho 12 biểu đồ và 4 Dashboard.

---

## 1. Các Trường Tính Toán Chung (Common Fields)

### CF1: Năm Sự Kiện (Event Year)
- **Tên trường**: `[Event Year]`
- **Công thức**:
  ```tableau
  YEAR([start_date])
  ```
- **Ý nghĩa**: Trích xuất năm dạng số nguyên hoặc thứ bậc thời gian.

### CF2: Tháng Sự Kiện (Event Month)
- **Tên trường**: `[Event Month]`
- **Công thức**:
  ```tableau
  MONTH([start_date])
  ```
- **Ý nghĩa**: Phục vụ biểu đồ Heatmap tháng $\times$ năm (#4).

### CF3: Thiệt Hại Kinh Tế (Tỷ USD)
- **Tên trường**: `[Damage Bil USD]`
- **Công thức**:
  ```tableau
  ZN([damage_usd]) / 1000000000
  ```
- **Ý nghĩa**: Đổi đơn vị sang Tỷ USD để hiển thị gọn gàng trên trục số.

### CF4: Phân Loại Nhóm Thiệt Hại (Damage Severity Level)
- **Tên trường**: `[Damage Severity Level]`
- **Công thức**:
  ```tableau
  IF ISNULL([damage_usd]) OR [damage_usd] = 0 THEN "Không xác định"
  ELSEIF [damage_usd] < 10000000 THEN "Thấp (< 10M USD)"
  ELSEIF [damage_usd] < 100000000 THEN "Trung bình (10M - 100M USD)"
  ELSEIF [damage_usd] < 1000000000 THEN "Nghiêm trọng (100M - 1B USD)"
  ELSE "Đại thảm họa (> 1B USD)"
  END
  ```
- **Ý nghĩa**: Phục vụ phân tầng thiệt hại trong biểu đồ Sankey / Flow (#11).

---

## 2. Các Trường Tính Toán Cho Thành Viên 1 (#1 – #4)

### CF5: Số Vụ Cháy Rừng Riêng Biệt (Wildfire Event Count)
- **Tên trường**: `[Wildfire Events]`
- **Công thức**:
  ```tableau
  IF [disaster_type] = "Wildfire" THEN 1 ELSE 0 END
  ```
- **Ý nghĩa**: Dùng cho Heatmap (#4) và so sánh cơ cấu.

---

## 3. Các Trường Tính Toán Cho Thành Viên 2 (#5 – #8)

### CF6: Trung Bình Số Vụ 20 Năm (20-Year Benchmark Average)
- **Tên trường**: `[Avg Events 20Yr]`
- **Công thức**:
  ```tableau
  WINDOW_AVG(COUNTD([event_id]))
  ```
- **Thiết lập bảng**: Compute using `[Event Year]`.

### CF7: Độ Lệch So Với Trung Bình (Divergence from Average)
- **Tên trường**: `[Diff from 20Yr Avg]`
- **Công thức**:
  ```tableau
  COUNTD([event_id]) - [Avg Events 20Yr]
  ```
- **Ý nghĩa**: Trục đo cho Diverging Bar (#5), giá trị âm (xanh) hoặc dương (đỏ).

### CF8: Màu Phân Kỳ (Diverging Color Flag)
- **Tên trường**: `[Divergence Flag]`
- **Công thức**:
  ```tableau
  IF [Diff from 20Yr Avg] > 0 THEN "Vượt trung bình (+)"
  ELSE "Dưới trung bình (-)"
  END
  ```

### CF9: Log10 Diện Tích Cháy (Log10 Burned Area)
- **Tên trường**: `[Log10 Burned Area]`
- **Công thức**:
  ```tableau
  LOG(ZN([burned_area_ha]) + 1, 10)
  ```
- **Ý nghĩa**: Trục hoành cho Bubble Scatter (#7).

### CF10: Log10 Thiệt Hại (Log10 Damage USD)
- **Tên trường**: `[Log10 Damage USD]`
- **Công thức**:
  ```tableau
  LOG(ZN([damage_usd]) + 1, 10)
  ```
- **Ý nghĩa**: Trục tung cho Bubble Scatter (#7).

### CF11: Nhóm Phân Vị Diện Tích Cháy (Burned Area Size Bin)
- **Tên trường**: `[Burned Area Bin]`
- **Công thức**:
  ```tableau
  IF ISNULL([burned_area_ha]) OR [burned_area_ha] = 0 THEN "Chưa ghi nhận"
  ELSEIF [burned_area_ha] < 100 THEN "< 100 ha (Nhỏ)"
  ELSEIF [burned_area_ha] < 1000 THEN "100 - 1.000 ha (Vừa)"
  ELSEIF [burned_area_ha] < 10000 THEN "1.000 - 10.000 ha (Lớn)"
  ELSE "≥ 10.000 ha (Siêu đám cháy)"
  END
  ```
- **Ý nghĩa**: Trục phân loại cho Histogram (#8).

---

## 4. Các Trường Tính Toán Cho Thành Viên 3 (#9 – #12)

### CF12: Tỷ Lệ % Lũy Kế Tử Vong (Cumulative Death %)
- **Tên trường**: `[Cumulative Death %]`
- **Công thức**:
  ```tableau
  RUNNING_SUM(SUM([deaths])) / TOTAL(SUM([deaths]))
  ```
- **Thiết lập bảng**: Compute using `[country_name]` (đã sắp xếp giảm dần theo `SUM([deaths])`).
- **Ý nghĩa**: Đường cong Pareto lũy kế (#9) so sánh với ngưỡng tham chiếu 80%.

### CF13: Phân Loại Nguyên Nhân 2 Cấp (Cause Category Level 1)
- **Tên trường**: `[Cause Group High Level]`
- **Công thức**:
  ```tableau
  IF CONTAINS(LOWER([cause_group]), "natural") OR CONTAINS(LOWER([cause_group]), "lightning") THEN "Tự nhiên (Sấm sét, Khí hậu)"
  ELSEIF CONTAINS(LOWER([cause_group]), "human") OR CONTAINS(LOWER([cause_group]), "arson") OR CONTAINS(LOWER([cause_group]), "accident") THEN "Tác động con người (Bất cẩn, Đốt phá)"
  ELSE "Chưa xác định / Khác"
  END
  ```
- **Ý nghĩa**: Vòng trong của biểu đồ Donut / Sunburst (#10) và nút nguồn của luồng (#11).

---

## 5. Quy Chuẩn Bảng Màu Trong Tableau

Khi chọn màu trên thẻ **Color (Marks)**:
- **Biểu đồ thời gian / Số lượng**: Bảng màu `Tableau Classic 10` hoặc `Color Blind`.
- **Cháy rừng (Wildfire)**: Luôn cố định màu Đỏ Cam `#D55E00` (hoặc `Orange-Red`).
- **Bản đồ nhiệt / Độ nghiêm trọng**: Chọn dải tuần tự `Orange-Red` hoặc `YlOrRd`.
- **Biểu đồ phân kỳ (#5)**: Chọn dải phân kỳ `Red-Blue Diverging` (Tâm = 0).
