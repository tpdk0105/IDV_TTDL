# Danh Mục Các Trường Tính Toán Trong Tableau (CALCULATED FIELDS)

> **Dự án**: Trực quan hóa dữ liệu Cháy rừng Bang California 2006–2025 (IDV_TTDL)  
> **Tác giả / Hiệu đính**: @DiKhang · Cập nhật ngày 08/10/2026  
> **Đối chiếu thực nghiệm**: Đã đối chiếu 100% bằng Python trên dữ liệu gốc (7.235 vụ cháy, 114.726 bản ghi công trình DINS, 73.818 công trình bị phá hủy).

---

## 1. MÔ HÌNH DỮ LIỆU & QUAN HỆ (DATA SOURCE RELATIONSHIPS)

Bảng gốc trung tâm là `fact_fire_incident.csv`, nối hình sao (Star Schema Relationship / Noodle) ra 4 bảng vệ tinh:
* `fact_fire_incident` ↔ `dim_date`: `date_id` = `date_id`
* `fact_fire_incident` ↔ `dim_cause`: `cause_id` = `cause_id`
* `fact_fire_incident` ↔ `dim_county`: `county_id` = `county_id`
* `fact_fire_incident` ↔ `fact_structure_damage`: `incident_id` = `incident_id`

> **LƯU Ý QUAN TRỌNG**: Không nối `fact_structure_damage` với `dim_county` theo `county_id`, vì mã hạt giữa hai bảng fact bị lệch nhau ở khoảng 12% số dòng kiểm định.

---

## 2. BẢNG TỔNG HỢP CALCULATED FIELDS CHÍNH THỨC

| Tên Calculated Field | Dùng ở Sheet | Mục đích & Ý nghĩa kỹ thuật |
|---|---|---|
| `[Fire Incidents Count (calc)]` | Sheet 1, 2, 3, 4, 6, 10, KPI_1 | Đếm số vụ cháy duy nhất (`COUNTD`), tránh nhân đôi dòng khi kết nối với bảng chi tiết công trình |
| `[Giai đoạn]` | Sheet 1 | Phân tách 2 thập kỷ (2006–2015 vs 2016–2025) để kiểm định hiện tượng mùa cháy kéo dài |
| `[Mật độ cháy (vụ/1.000 dặm²)]` | Sheet 3 | Chuẩn hóa tần suất cháy theo diện tích địa lý của từng Hạt |
| `[State]` | Sheet 3 | Gán cố định giá trị `"California"` để định vị địa lý chính xác, tránh nhầm các Hạt trùng tên ở bang khác |
| `[Acres Bin Log (calc)]` | Sheet 6 | Chia 6 mức quy mô diện tích đám cháy theo cấp số nhân |
| `[Nhóm công trình]` | Sheet 7 | Chuẩn hóa và gộp 21 loại công trình kiểm định thành 6 nhóm kiến trúc chính, sửa lỗi chính tả |
| `[Log Diện tích]` | Sheet 8 | Biến đổi logarit cơ số 10 cho diện tích cháy phục vụ mô hình hồi quy log-log |
| `[Log Công trình phá hủy]` | Sheet 8 | Biến đổi logarit cơ số 10 cho số công trình bị phá hủy phục vụ mô hình hồi quy log-log |
| `[Diff from 20Yr Avg (calc)]` | Sheet 10 | Đo lường độ chênh lệch số vụ cháy mỗi năm so với mức trung bình 20 năm |
| `[Divergence Flag (calc)]` | Sheet 10 | Gắn nhãn phân kỳ: "Vượt trung bình" hoặc "Dưới trung bình" để tô màu trực quan |
| `[Nhóm Pareto (tuỳ chọn)]` | Sheet 9 | Table calculation phân loại nhóm Hạt gây ra 80% tổng thiệt hại tài sản |

---

## 3. CÔNG THỨC CHI TIẾT (COPY/PASTE VÀO TABLEAU)

### 3.1. `[Fire Incidents Count (calc)]`
* **Công thức**:
  ```tableau
  COUNTD([incident_id])
  ```
* **Giải thích**: Bắt buộc dùng `COUNTD` thay vì `COUNT` vì bảng `fact_structure_damage` có nhiều dòng cho cùng 1 vụ cháy.

---

### 3.2. `[Giai đoạn]`
* **Công thức**:
  ```tableau
  IF [year] <= 2015 THEN "2006–2015" ELSE "2016–2025" END
  ```
* **Giải thích**: Chia đôi chuỗi 20 năm thành 2 giai đoạn 10 năm để so sánh sự dịch chuyển của đường cong mùa cháy.

---

### 3.3. `[Mật độ cháy (vụ/1.000 dặm²)]`
* **Công thức**:
  ```tableau
  [Fire Incidents Count (calc)] / MIN([area_sqmi]) * 1000
  ```
* **Giải thích**: `MIN([area_sqmi])` lấy diện tích của Hạt từ `dim_county` để làm mẫu số chuẩn hóa.

---

### 3.4. `[State]`
* **Công thức**:
  ```tableau
  "California"
  ```
* **Thiết lập**: Chuột phải vào field $\to$ **Geographic Role** $\to$ Chọn **State/Province**. Đưa vào Detail của bản đồ để Tableau không bị nhầm Hạt Orange, Lake, Kern với các bang khác.

---

### 3.5. `[Acres Bin Log (calc)]`
* **Công thức**:
  ```tableau
  IF ISNULL([acres_burned]) OR [acres_burned] < 300 THEN "< 300"
  ELSEIF [acres_burned] < 1000 THEN "300–1k"
  ELSEIF [acres_burned] < 5000 THEN "1k–5k"
  ELSEIF [acres_burned] < 25000 THEN "5k–25k"
  ELSEIF [acres_burned] < 100000 THEN "25k–100k"
  ELSE "≥ 100k"
  END
  ```
* **Giải thích**: Chia các khoảng diện tích lũy tiến theo cấp số nhân phù hợp với phân phối hàm mũ của cháy rừng.

---

### 3.6. `[Nhóm công trình]`
* **Công thức**:
  ```tableau
  IF CONTAINS([structure_type], "Single Fam") THEN "Nhà 1 hộ"
  ELSEIF CONTAINS([structure_type], "Multi Family") THEN "Nhà nhiều hộ"
  ELSEIF CONTAINS([structure_type], "Mobile Home") OR CONTAINS([structure_type], "Motor Home") THEN "Nhà di động"
  ELSEIF CONTAINS([structure_type], "Commercial") OR CONTAINS([structure_type], "Mixed") THEN "Thương mại"
  ELSEIF CONTAINS([structure_type], "Utility") THEN "Công trình phụ"
  ELSE "Công cộng/Khác"
  END
  ```
* **Giải thích**: Gộp 21 phân loại DINS thành 6 nhóm lớn, gom đúng các biến thể tên gọi trong dữ liệu CAL FIRE.

---

### 3.7. `[Log Diện tích]`
* **Công thức**:
  ```tableau
  IF [acres_burned] > 0 THEN LOG([acres_burned]) END
  ```
* **Giải thích**: Biến đổi logarit thập phân $\log_{10}(X)$. Giá trị bằng 0 hoặc âm sẽ tự trả về `NULL` và được Tableau tự động loại khỏi hồi quy.

---

### 3.8. `[Log Công trình phá hủy]`
* **Công thức**:
  ```tableau
  IF [total_structures_destroyed] > 0 THEN LOG([total_structures_destroyed]) END
  ```
* **Giải thích**: Biến đổi $\log_{10}(Y)$. Giúp đưa hệ số xác định hồi quy từ $R^2 = 0{,}026$ (số gốc) lên $R^2 = 0{,}356$ (log-log).

---

### 3.9. `[Diff from 20Yr Avg (calc)]`
* **Công thức**:
  ```tableau
  [Fire Incidents Count (calc)] - WINDOW_AVG([Fire Incidents Count (calc)])
  ```
* **Thiết lập Table Calculation**: Chuột phải vào viên thuốc trên Rows $\to$ **Compute Using** $\to$ `[year]`.

---

### 3.10. `[Divergence Flag (calc)]`
* **Công thức**:
  ```tableau
  IF [Diff from 20Yr Avg (calc)] >= 0 THEN "Vượt trung bình" ELSE "Dưới trung bình" END
  ```
* **Giải thích**: Dùng để kéo vào thẻ Color trên Sheet 10.

---

### 3.11. `[Nhóm Pareto (tuỳ chọn)]`
* **Công thức**:
  ```tableau
  IF (RUNNING_SUM(SUM([total_structures_destroyed])) - SUM([total_structures_destroyed])) 
     / TOTAL(SUM([total_structures_destroyed])) < 0.8
  THEN "Nhóm gây 80% thiệt hại" 
  ELSE "Các hạt còn lại" 
  END
  ```
* **Thiết lập**: Compute Using: `Table (across)` hoặc theo `county_name`.

---

## 4. DANH MỤC PARAMETERS (THAM SỐ ĐIỀU KHIỂN)

| Tên Parameter | Data Type | Giá trị cho phép | Giá trị mặc định | Mục đích sử dụng |
|---|---|---|---|---|
| `[Top N]` | Integer | Range: 5 đến 20 (Step = 1) | `10` | Lọc động Top Hạt tại Sheet 5 và tiêu đề động |
| `[Mốc 80%]` | Float | Giá trị cố định `0.8` | `0.8` | Tạo Reference Line 80% cho trục tỷ lệ Pareto (Sheet 9) |
| `[Mốc 0]` | Float | Giá trị cố định `0.0` | `0.0` | Tạo Reference Line mốc 0 cho Diverging Bar (Sheet 10) |

*(Lưu ý: Do Tableau bản Web không có lựa chọn "Constant" trực tiếp trên Reference Line nên phải dùng Parameter thay thế).*

---

## 5. HIERARCHIES, ALIASES VÀ ĐỔI TÊN TRƯỜNG

1. **Hierarchy Nguyên nhân**: Kéo `cause_name` thả đè lên `cause_group` $\to$ Đặt tên hierarchy là **Nguyên nhân**.
2. **Hierarchy Loại công trình**: Kéo `structure_type` thả đè lên `Nhóm công trình` $\to$ Đặt tên hierarchy là **Loại công trình**.
3. **Alias `cause_group`**:
   * `Human` $\to$ **Con người** (Màu đỏ `#D95F02`)
   * `Natural` $\to$ **Tự nhiên** (Màu xanh lá `#2CA02C`)
   * `Undetermined` $\to$ **Chưa xác định** (Màu xám `#7F7F7F`)
4. **Alias `month`**: Đổi số `1`–`12` thành `T1`–`T12`.
5. **Đổi tên trường**: `acres_burned` $\to$ **Diện tích cháy (acres)**.

---

## 6. DANH SÁCH CÁC HÀM CŨ ĐÃ BÃI BỎ (DEPRECATED)

| Hàm / Field cũ | Lý do loại bỏ / Khắc phục | Giải pháp thay thế mới |
|---|---|---|
| `[Cause Group High Level (calc)]` | Phân loại sai nhóm "Miscellaneous" vào Con người, làm lệch số vụ năm 2017 (193 vs 275) | Sử dụng trực tiếp trường gốc `[cause_group]` trong `dim_cause` kèm Alias tiếng Việt |
| `[Cumulative Destroyed % (calc)]` | Công thức cũ bị trộn lẫn giữa `damaged` và `destroyed`, làm sai lệch tỷ lệ | Dùng Table Calculation: Running Total + Percent of Total trên `total_structures_destroyed` |
| `[Burned Area Ha]` | Không cần thiết quy đổi, giữ nguyên mẫu Anh (Acres) thống nhất với dữ liệu CAL FIRE | Sử dụng trực tiếp `[acres_burned]` |
