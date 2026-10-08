# Nhật Ký Làm Sạch Dữ Liệu (CLEANING LOG)

> **Người phụ trách**: Thành viên 1 - Kỹ sư Dữ liệu (Data Engineer)  
> **Trạng thái**: Khung tài liệu ghi vết toàn bộ quy trình làm sạch (Giai đoạn 1)

---

## 1. Nguyên Tắc & Quy Chuẩn Làm Sạch
- **Không chỉnh sửa thủ công**: Mọi thao tác biến đổi dữ liệu phải thông qua mã nguồn Python có khả năng tái lập (`src/03_clean.py` và `src/03b_ml_clean.py`).
- **Bảo toàn dữ liệu gốc**: Giữ lại các cột thô ban đầu song song với cột chuẩn hóa (vd: `fire_name_raw` song song `fire_name`).
- **Gắn cờ kiểm soát**: Mọi giá trị được điền (imputed), dự đoán (predicted), hoặc nghi ngờ ngoại lai (outlier) đều có cột cờ nhị phân riêng.
- **Cam kết số lượng mẫu**: Sau toàn bộ quy trình làm sạch, tập dữ liệu `master_clean.csv` phải đạt tối thiểu **5.000 dòng**.

---

## 2. Bảng Theo Dõi Các Bước Làm Sạch Theo Quy Tắc (`03_clean.py`)

*(Số liệu in ra tự động khi chạy `python src/03_clean.py`. Đơn vị đếm ghi rõ ở từng dòng: dòng FRAP, công trình DINS, hoặc bản ghi thiệt hại.)*

| Bước # | Thao tác thực hiện | Điều kiện / Quy tắc | Số dòng trước | Số dòng sau | Số dòng loại bỏ | Lý do & Ghi chú |
|--------|---------------------|----------------------|---------------|-------------|-----------------|-----------------|
| 1 | Nạp dữ liệu thô | Gộp 5 nguồn từ `data/raw/calfire/` | 158.034 | 158.034 | 0 | 5 file CSV chính thức (`eda.load_raw_data()`) |
| 2 | Lọc khoảng thời gian | FRAP `Year BETWEEN 2006 AND 2025` | 23.334 | 7.342 | 15.992 | Bỏ vụ cháy trước 2006 và 77 dòng thiếu `Year`. Bao phủ đủ 20/20 năm |
| 3a | Gộp trùng lặp logic (FRAP) | Gộp theo khóa (`year`, `fire_name`, `unit_id`): cộng diện tích, `alarm_date` sớm nhất, `cont_date` muộn nhất | 7.342 | 7.235 | 107 | 1 vụ cháy gồm nhiều polygon (93 vụ có > 1 polygon). 38 vụ không tên giữ riêng, không gộp. Trùng hoàn toàn: 0 dòng |
| 3b | Khử trùng lặp logic (DINS) | Trùng (tên vụ, ngày bắt đầu, số nhà, tên đường, thành phố, loại công trình, tọa độ) | 132.522 | 132.413 | 109 | Công trình bị kiểm kê lặp. Số nhà bị phá hủy giảm từ 77.596 còn 77.503 |
| 4 | Chuẩn hóa địa danh & Hạt | Hạt lấy từ DINS `County` / ICS-209 `POO_COUNTY`; còn thiếu thì suy từ Hạt phổ biến nhất của `unit_id`. Ghép FIPS 5 số + diện tích từ Demographics | 7.235 | 7.235 | 0 | 5.951 vụ suy Hạt từ `unit_id`; **840 vụ không xác định được Hạt** (FRAP không có tọa độ). Tổng 51 Hạt |
| 5 | Chuẩn hóa tọa độ | Vĩ độ [32.0, 42.0], Kinh độ [-125.0, -114.0] | 7.235 | 7.235 | 0 | **Không áp dụng** cho bảng vụ cháy: FRAP không có cột lat/lon. Tọa độ DINS / ICS-209 đều nằm trong California (xem `DATA_QUALITY_REPORT.md`) |
| 6 | Chuẩn hóa đơn vị đo lường | Lưu song song `acres_burned` & `burned_area_ha` | 7.235 | 7.235 | 0 | 1 Acre = 0.404686 Ha. Ngày chuẩn ISO 8601 `YYYY-MM-DD` |
| 7 | Hợp nhất thiệt hại 20 năm | ICS-209 (2006-2012) + DINS (2013-2025), ghép vào vụ FRAP theo 3 khóa, rồi theo (`year`, `fire_name`) | 682 bản ghi thiệt hại | 476 khớp | 206 không khớp | Khớp **73.818 / 77.503** công trình bị phá hủy (**95,2%**), vào 447 vụ cháy. Xem cách khớp (`damage_match`) và 10 vụ chưa khớp ở mục 2.1 |
| 8a | Thời gian dập lửa bất hợp lý | `cont_date < alarm_date` hoặc > 365 ngày → `NULL` | 7.235 | 7.235 | 0 | 2 vụ bị đặt `NULL` (không xóa dòng). Tổng 109 vụ thiếu `duration_days` |
| 8b | Xử lý giá trị âm bất hợp lý | `acres_burned`, `burned_area_ha`, `structures_destroyed`, `structures_damaged` ≥ 0 | 7.235 | 7.235 | 0 | Không có ô âm nào. Quy tắc vẫn giữ trong code để bảo vệ khi cập nhật dữ liệu |
| 9a | Chọn cột thương vong (NOAA) | Giữ `DEATHS_*`, `INJURIES_*`; tách tên vụ cháy từ narrative ("The Camp Fire" → `CAMP`) | 993 | 993 | 0 | Bỏ `DAMAGE_PROPERTY` / `DAMAGE_CROPS` (thiệt hại tài sản lấy từ DINS + ICS-209) và 21 cột trống. Tách được tên ở 634 dòng |
| 9b | Gộp trùng vùng dự báo (NOAA) | Gộp theo (`EPISODE_ID`, tên vụ cháy), lấy giá trị lớn nhất; dòng không tách được tên giữ riêng | 993 | 897 | 96 | 1 vụ cháy lan qua nhiều vùng dự báo bị ghi lặp (vd Woolsey 2018: 5 dòng × 3 người). Người chết trực tiếp **255 → 207**, bị thương **887 → 792**. Xuất `data/interim/noaa_casualties_cleaned.csv` |
| **Tổng kết** | **Xuất `data/interim/master_rules_cleaned.csv`** | `assert len(df) >= 5000`, `incident_id` duy nhất, `year` ∈ [2006, 2025] | | **7.235 vụ × 24 cột** | | Đạt điều kiện tiền xử lý cho ML |

### 2.1. Chi tiết hợp nhất thiệt hại (Bước 7)

Cột `damage_match` ghi lại cách mỗi vụ được ghép thiệt hại:

| `damage_match` | Quy tắc | Bản ghi thiệt hại | Công trình bị phá hủy | Độ tin cậy |
|----------------|---------|-------------------|-----------------------|------------|
| `exact` | Khớp đủ (`year`, `fire_name`, `unit_id`) | 357 | 55.913 | Cao |
| `name_year_unique` | Khác `unit_id` (nguồn ghi đơn vị khác, vd Palisades 2025) nhưng tên duy nhất trong năm | 85 | 13.520 | Cao |
| `name_year_largest` | Nhiều vụ FRAP trùng tên cùng năm → gán cho vụ lớn nhất | 34 | 4.385 | **Thấp**, có thể gán nhầm (vd SIERRA 2006: thiệt hại của vụ San Bernardino bị gán vào vụ Cleveland NF) |
| `none` | Vụ không có ghi nhận thiệt hại | — | 0 | — |

**10 vụ thiệt hại lớn nhất chưa khớp được với FRAP** (thường do tên khác nhau giữa các nguồn, cần đối soát thủ công):

| Năm | Tên (đã chuẩn hóa) | `unit_id` | Công trình bị phá hủy | Nguồn |
|-----|--------------------|-----------|-----------------------|-------|
| 2020 | LNU LIGHTNING | LNU | 1.491 | DINS |
| 2007 | HARRIS | MVU | 548 | ICS-209 |
| 2020 | SQF | TUU | 232 | DINS |
| 2006 | HEART-MILLARD | BDF | 221 | ICS-209 |
| 2017 | SULPHUR | LNU | 162 | DINS |
| 2021 | BECKWOURTH | LMU | 148 | DINS |
| 2008 | PARKER ROAD | FFD | 125 | ICS-209 |
| 2020 | BEU LIGHTNING | BEU | 103 | DINS |
| 2025 | TCU | TCU | 95 | DINS |
| 2017 | LAPORTE | BTU | 72 | DINS |

---

## 3. Nhật Ký Xử Lý Ngoại Lai & Bất Thường Thủ Công
*(Kiểm tra mẫu top 20 dòng bất thường nhất do mô hình ML Isolation Forest gắn cờ trong Giai đoạn 2)*

| STT | `incident_id` | Tên vụ cháy / Hạt / Năm | Thuộc tính nghi ngờ | Giá trị bất thường | Quyết định (GIỮ / SỬA / LOẠI) | Căn cứ & Nguồn đối soát |
|-----|------------|------------------------------|----------------------|--------------------|--------------------------------|--------------------------|
| 1 | *TODO* | *TODO* | *TODO* | *TODO* | *TODO* | *TODO* |
| 2 | *TODO* | *TODO* | *TODO* | *TODO* | *TODO* | *TODO* |
| 3 | *TODO* | *TODO* | *TODO* | *TODO* | *TODO* | *TODO* |
