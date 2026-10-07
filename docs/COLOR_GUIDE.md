# Quy Chuẩn Màu Sắc Trực Quan Hóa (COLOR GUIDE)

> **Người phụ trách**: Thành viên 3 - Kỹ sư Dashboard & Trực quan hóa (Data Visualization Engineer)  
> **Trạng thái**: Hướng dẫn dùng chung toàn bộ Dashboard và Báo cáo (Giai đoạn 1)

---

## 1. Triết Lý & Nguyên Tắc Thiết Kế Màu Sắc
Màu sắc trong trực quan hóa dữ liệu không chỉ mang tính thẩm mỹ mà là một kênh mã hóa thị giác (visual encoding) mang ngữ nghĩa chính xác. Nhóm áp dụng nghiêm ngặt các nguyên tắc khoa học màu sắc:
1. **Tuân thủ ngữ nghĩa dữ liệu**: Lựa chọn bảng màu chuẩn xác theo kiểu dữ liệu (Sequential, Diverging, Categorical).
2. **Khả năng tiếp cận (Accessibility - WCAG 2.1 AA)**: Độ tương phản giữa chữ và nền đạt tối thiểu 4.5:1. Tuyệt đối không chỉ dựa vào màu sắc đơn thuần để phân biệt các lớp thông tin (kết hợp tooltip, ký hiệu hình dạng, nhãn trực tiếp).
3. **Thân thiện với người mù màu (Colorblind-Safe)**: Loại bỏ triệt để dải màu cầu vồng (Rainbow/Jet) và không sử dụng cặp Đỏ – Xanh lá cây (Red-Green) làm kênh phân biệt nhị phân duy nhất.
4. **Nhất quán toàn hệ thống**: Mỗi nhóm nguyên nhân, mỗi loại công trình kiến trúc, mỗi vùng địa lý California phải được gán một mã màu cố định, không thay đổi xuyên suốt 10 biểu đồ.

---

## 2. Các Bảng Màu Tiêu Chuẩn

### 2.1. Bảng Màu Tuần Tự (Sequential Palette)
- **Áp dụng**: Dữ liệu định lượng có thứ tự từ thấp đến cao (Số lượng vụ cháy, Tổng thiệt hại USD, Diện tích cháy rừng hecta, Mật độ không gian).
- **Quy tắc**: Giá trị thấp $\to$ Màu sáng/nhạt; Giá trị cao $\to$ Màu đậm/bão hòa cao.
- **Dải màu chính (Fire/Heat Sequential - OrRd / YlOrRd)**:
  - Cấp 1 (Rất thấp): `#FFF5EB`
  - Cấp 2 (Thấp): `#FEE6CE`
  - Cấp 3 (Trung bình thấp): `#FDD0A2`
  - Cấp 4 (Trung bình): `#FDAE6B`
  - Cấp 5 (Trung bình cao): `#FD8D3C`
  - Cấp 6 (Cao): `#F16913`
  - Cấp 7 (Rất cao): `#D94801`
  - Cấp 8 (Cực đoan): `#8C2D04`
- **Dải màu thứ cấp (General Disasters - Blues)**: `#EFF3FF` $\to$ `#C6DBEF` $\to$ `#9ECAE1` $\to$ `#6BAED6` $\to$ `#4292C6` $\to$ `#2171B5` $\to$ `#084594`.

### 2.2. Bảng Màu Phân Kỳ (Diverging Palette)
- **Áp dụng**: Biểu diễn độ lệch (Anomaly / Difference) so với mốc tham chiếu có ý nghĩa (Mốc 0, hoặc giá trị trung bình 20 năm 2006–2025).
- **Quy tắc**: Điểm giữa (Neutral Midpoint) mang màu xám nhạt trung tính; hai đầu mang hai tông màu tương phản rõ rệt.
- **Dải màu RdBu (Diverging Red-Blue)**:
  - Cực âm (Dưới mức trung bình / Giảm sâu): `#2166AC` (Xanh dương đậm)
  - Âm vừa: `#4393C3`
  - Âm nhẹ: `#92C5DE`
  - **Mốc trung tính (Giá trị chuẩn / Điểm 0)**: `#F7F7F7` hoặc `#E0E0E0`
  - Dương nhẹ: `#F4A582`
  - Dương vừa: `#D6604D`
  - Cực dương (Vượt mức trung bình / Tăng vọt): `#B2182B` (Đỏ sẫm cảnh báo)

### 2.3. Bảng Màu Phân Loại Nhất Quán (Categorical Palette - Okabe & Ito Safe Palette)
Áp dụng cho các biến định danh. Tối đa 7–8 màu/biểu đồ, phần còn lại gom vào nhóm "Khác" (`#9E9E9E`).

#### A. Ánh xạ cố định theo Nhóm & Chi Tiết Nguyên Nhân Cháy (`cause_group` / `cause_name`):
- **Tự nhiên (Natural - Sét đánh / Lightning)**: `#009E73` (Xanh lục sinh thái)
- **Con người (Human - Thiết bị, Đường dây điện, Đốt phá, Phương tiện, Lửa trại, Bất cẩn)**: `#D55E00` (Đỏ cam lửa)
- **Không rõ / Chưa xác định (Undetermined / Misc)**: `#7F7F7F` (Xám trung tính)

#### B. Ánh xạ theo Loại Công Trình Bị Thiệt Hại (`structure_type` - DINS & ICS-209):
- **Single Family Residence (Nhà ở riêng lẻ)**: `#D55E00` (Đỏ cam cháy)
- **Commercial (Công trình thương mại)**: `#0072B2` (Xanh dương đậm)
- **Minor Outbuilding (Công trình phụ / Kho bãi)**: `#E69F00` (Vàng đất)
- **Multi Family Residence (Khu nhà nhiều hộ)**: `#CC79A7` (Hồng tím)
- **Infrastructure / Other (Hạ tầng kỹ thuật & Khác)**: `#999999` (Xám)

#### C. Ánh xạ theo Phân Vùng Địa Lý California (`california_region`):
- **Northern California (Vùng Bắc rừng rậm)**: `#0072B2` (Xanh biển)
- **Sierra Nevada / Central (Sườn núi & Miền Trung)**: `#E69F00` (Cam đất)
- **Southern California (Vùng Nam khí hậu khô)**: `#D55E00` (Đỏ cam)
- **Bay Area & Coast (Vùng Vịnh & Duyên hải)**: `#009E73` (Xanh lục)

---

## 3. Quy Cách Trình Bày Giao Diện (Light & Dark Theme)

| Thuộc tính giao diện | Giao diện Sáng (Light Theme) | Giao diện Tối (Dark Theme) | Ghi chú |
|-----------------------|------------------------------|----------------------------|---------|
| Màu nền chính (Background) | `#FFFFFF` | `#121212` | Nền trang tổng quan |
| Màu nền thẻ (Card Background)| `#F8F9FA` | `#1E1E1E` | Nền khung biểu đồ |
| Viền thẻ (Card Border) | `#E9ECEF` | `#2D2D2D` | Đường kẻ phân cách |
| Màu chữ chính (Primary Text) | `#212529` | `#E0E0E0` | Tỷ lệ tương phản $\ge 7:1$ |
| Màu chữ phụ (Secondary Text) | `#6C757D` | `#A0A0A0` | Tỷ lệ tương phản $\ge 4.5:1$ |
| Lưới tọa độ biểu đồ (Grid line)| `#F0F0F0` | `#333333` | Đường gióng mờ |
| Tooltip Background | `rgba(255, 255, 255, 0.95)` | `rgba(30, 30, 30, 0.95)` | Có bóng đổ mờ (box-shadow) |

*Mô-đun `dashboard/js/palette.js` sẽ xuất toàn bộ các bảng màu trên dưới dạng đối tượng JavaScript để tái sử dụng xuyên suốt toàn bộ các biểu đồ.*
