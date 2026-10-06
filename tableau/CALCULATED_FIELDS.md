# Danh Mục Các Trường Tính Toán Trong Tableau (CALCULATED FIELDS)

> Tài liệu hướng dẫn Thành viên 1, Thành viên 2, Thành viên 3 tạo các trường tính toán (Calculated Fields) trong Tableau Desktop / Tableau Public phục vụ cho 10 biểu đồ, 3 Dashboard và Tableau Story về Cháy rừng California (2006–2025).

---

## 1. Các Trường Tính Toán Chung (Common Fields)

### CF1: Năm Sự Kiện (Event Year)
- **Tên trường**: `[Event Year]`
- **Công thức**:
  ```tableau
  YEAR([alarm_date])
  ```
- **Ý nghĩa**: Trích xuất năm dạng số nguyên hoặc thứ bậc thời gian (nếu dùng trường `year` thì không cần tính).

### CF2: Tháng Bùng Phát (Event Month)
- **Tên trường**: `[Event Month]`
- **Công thức**:
  ```tableau
  MONTH([alarm_date])
  ```
- **Ý nghĩa**: Phục vụ phân tích chu kỳ mùa vụ cháy rừng.

### CF3: Quy Đổi Diện Tích Sang Hecta (Burned Area Hectares)
- **Tên trường**: `[Burned Area Ha]`
- **Công thức**:
  ```tableau
  ZN([acres_burned]) * 0.404686
  ```
- **Ý nghĩa**: Quy đổi đơn vị mẫu Anh (Acres) sang Hecta (ha) chuẩn quốc tế.

### CF4: Phân Loại Quy Mô Đám Cháy (Fire Size Class)
- **Tên trường**: `[Fire Size Class]`
- **Công thức**:
  ```tableau
  IF ISNULL([acres_burned]) OR [acres_burned] = 0 THEN "Chưa ghi nhận"
  ELSEIF [acres_burned] < 1000 THEN "Nhỏ (< 1.000 Acres)"
  ELSEIF [acres_burned] < 10000 THEN "Trung bình (1.000 - 10.000 Acres)"
  ELSEIF [acres_burned] < 100000 THEN "Lớn (10.000 - 100.000 Acres)"
  ELSE "Siêu đám cháy (≥ 100.000 Acres - Megafire)"
  END
  ```
- **Ý nghĩa**: Phân cấp quy mô đám cháy theo chuẩn phân loại lâm nghiệp Hoa Kỳ.

---

## 2. Các Trường Tính Toán Cho Thành Viên 1 (#1 – #2)

### CF5: Số Vụ Cháy Hàng Năm (Annual Fire Count)
- **Tên trường**: `[Fire Incidents Count]`
- **Công thức**:
  ```tableau
  COUNTD([incident_id])
  ```
- **Ý nghĩa**: Trục cột cho biểu đồ Combo Trend (#1).

---

## 3. Các Trường Tính Toán Cho Thành Viên 2 (#3 – #6)

### CF6: Trung Bình Số Vụ Cháy 20 Năm (20-Year Benchmark Average)
- **Tên trường**: `[Avg Events 20Yr]`
- **Công thức**:
  ```tableau
  WINDOW_AVG(COUNTD([incident_id]))
  ```
- **Thiết lập bảng**: Compute using `[year]`.

### CF7: Độ Lệch So Với Trung Bình (Divergence from Average)
- **Tên trường**: `[Diff from 20Yr Avg]`
- **Công thức**:
  ```tableau
  COUNTD([incident_id]) - [Avg Events 20Yr]
  ```
- **Ý nghĩa**: Trục đo cho Diverging Bar (#3), giá trị âm (xanh) hoặc dương (đỏ cam).

### CF8: Màu Phân Kỳ (Diverging Color Flag)
- **Tên trường**: `[Divergence Flag]`
- **Công thức**:
  ```tableau
  IF [Diff from 20Yr Avg] > 0 THEN "Vượt trung bình (+)"
  ELSE "Dưới trung bình (-)"
  END
  ```

### CF9: Log10 Diện Tích Cháy (Log10 Acres Burned)
- **Tên trường**: `[Log10 Acres Burned]`
- **Công thức**:
  ```tableau
  LOG(ZN([acres_burned]) + 1, 10)
  ```
- **Ý nghĩa**: Trục hoành cho Bubble Scatter (#5) (hoặc có thể chọn trực tiếp Logarithmic Scale trên trục của Tableau).

### CF10: Log10 Nhà Cửa Phá Hủy (Log10 Structures Destroyed)
- **Tên trường**: `[Log10 Structures Destroyed]`
- **Công thức**:
  ```tableau
  LOG(ZN([structures_destroyed]) + 1, 10)
  ```
- **Ý nghĩa**: Trục tung cho Bubble Scatter (#5).

### CF11: Nhóm Phân Vị Diện Tích (Burned Acres Bin)
- **Tên trường**: `[Acres Bin Log]`
- **Công thức**:
  ```tableau
  IF ISNULL([acres_burned]) OR [acres_burned] < 300 THEN "< 300 Acres"
  ELSEIF [acres_burned] < 1000 THEN "300 - 1.000 Acres"
  ELSEIF [acres_burned] < 5000 THEN "1.000 - 5.000 Acres"
  ELSEIF [acres_burned] < 25000 THEN "5.000 - 25.000 Acres"
  ELSEIF [acres_burned] < 100000 THEN "25.000 - 100.000 Acres"
  ELSE "≥ 100.000 Acres (Siêu đám cháy)"
  END
  ```
- **Ý nghĩa**: Trục phân loại cho Histogram (#6).

---

## 4. Các Trường Tính Toán Cho Thành Viên 3 (#7 – #10)

### CF12: Tỷ Lệ % Lũy Kế Nhà Cửa Bị Phá Hủy (Cumulative Destroyed %)
- **Tên trường**: `[Cumulative Destroyed %]`
- **Công thức**:
  ```tableau
  RUNNING_SUM(SUM([structures_destroyed])) / TOTAL(SUM([structures_destroyed]))
  ```
- **Thiết lập bảng**: Compute using `[county]` (đã sắp xếp giảm dần theo `SUM([structures_destroyed])`).
- **Ý nghĩa**: Đường cong Pareto lũy kế (#7) so sánh với ngưỡng tham chiếu 80%.

### CF13: Phân Loại Nhóm Nguyên Nhân (Cause Group High Level)
- **Tên trường**: `[Cause Group High Level]`
- **Công thức**:
  ```tableau
  IF CONTAINS(LOWER([cause_name]), "lightning") OR [cause_code] = 1 THEN "Tự nhiên (Sấm sét)"
  ELSEIF [cause_code] IN (2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 16) OR CONTAINS(LOWER([cause_group]), "human") THEN "Tác động con người (Thiết bị, Điện, Đốt phá)"
  ELSE "Chưa xác định / Khác"
  END
  ```
- **Ý nghĩa**: Vòng trong của biểu đồ Donut 2 tầng (#8).

---

## 5. Quy Chuẩn Bảng Màu Trong Tableau

Khi chọn màu trên thẻ **Color (Marks)**:
- **Biểu đồ thời gian / Số lượng**: Bảng màu `Tableau Classic 10` hoặc `Color Blind` (Okabe-Ito).
- **Cháy rừng / Thiệt hại**: Luôn cố định dải màu Đỏ Cam `#D55E00` (hoặc `Orange-Red`).
- **Bản đồ phân vùng 58 Hạt (Choropleth Map)**: Chọn dải tuần tự `Orange-Red`.
- **Biểu đồ phân kỳ (#3)**: Chọn dải phân kỳ `Red-Blue Diverging` (Tâm = 0).
