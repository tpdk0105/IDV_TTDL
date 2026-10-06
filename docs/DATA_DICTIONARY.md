# Từ Điển Dữ Liệu (DATA DICTIONARY)

> **Người phụ trách**: Thành viên 1 - Kỹ sư Dữ liệu (Data Engineer)  
> **Phạm vi nghiên cứu**: Cháy rừng Bang California / Bắc Mỹ giai đoạn 2006–2025  
> **Trạng thái**: Đặc tả chuẩn hóa các trường dữ liệu và khóa liên kết

---

## 1. Tổng Quan Cấu Trúc Tập Dữ Liệu `master_clean.csv`
Tập dữ liệu sau làm sạch và tích hợp `data/clean/master_clean.csv` đóng vai trò là bảng nguồn tổng thể (Master Dataset), kết nối 4 nguồn dữ liệu thô:
1. `California_Fire_Perimeters_all.csv` (CAL FIRE FRAP - 23.334 dòng lịch sử, 7.342 vụ 2006–2025).
2. `CAL_FIRE_Damage_Inspection_DINS.csv` (CAL FIRE DINS - 132.522 dòng công trình kiểm kê thiệt hại tài sản).
3. `California_Counties_Demographics.csv` (Cục Dân số / CDTFA - 58 Hạt của California).
4. `NOAA_California_Wildfires_Casualties.csv` (NOAA NCEI - 139 sự kiện thương vong và thiệt hại USD).

- **Số dòng tối thiểu cam kết**: $\ge 5.000$ dòng (bảng thực thể công trình/vụ cháy tích hợp $\approx 10.000 - 130.000$ dòng tùy mức độ phân rã).
- **Phạm vi thời gian**: 2006–2025.
- **Quy tắc đặt tên cột**: Tiếng Anh, chữ thường, nối bằng dấu gạch dưới (`snake_case`).

---

## 2. Danh Mục Các Trường Dữ Liệu (Field Specifications)

| Tên Cột | Kiểu Dữ Liệu | Đơn Vị / Miền Giá Trị | Cho Phép NULL | Mô Tả Ý Nghĩa | Nguồn & Quy Tắc Xử Lý |
|---------|--------------|------------------------|---------------|---------------|------------------------|
| `incident_id` | String | Mã chuỗi (vd: `CALFIRE-2020-00123`) | Không | Khóa định danh duy nhất của từng vụ cháy rừng | Chuẩn hóa từ FRAP `FIRE_NUM` / `GlobalID` |
| `fire_name` | String | Tên chuẩn hóa (vd: `CAMP`, `AUGUST COMPLEX`) | Không | Tên chính thức của vụ cháy rừng | Chuẩn hóa Upper case, gỡ ký tự đặc biệt (`CMPLX` $\to$ `COMPLEX`) |
| `year` | Integer | [2006, 2025] | Không | Năm bùng phát vụ cháy | Trích xuất từ FRAP `YEAR_` hoặc `alarm_date` |
| `alarm_date` | Date | `YYYY-MM-DD` | Có | Ngày phát lệnh báo động cháy | Chuẩn hóa từ `ALARM_DATE` |
| `cont_date` | Date | `YYYY-MM-DD` | Có | Ngày khống chế / dập tắt đám cháy | Chuẩn hóa từ `CONT_DATE` ($\ge$ `alarm_date`) |
| `duration_days` | Float | $\ge 0.0$ ngày | Có | Thời gian đám cháy hoành hành | Hiệu số giữa `cont_date` và `alarm_date` |
| `county` | String | Tên 58 Hạt (vd: `Butte`, `Sonoma`, `Shasta`...) | Không | Tên Hạt (County) tại California nơi xảy ra cháy | Chuẩn hóa từ DINS `County` hoặc FRAP |
| `county_fips` | String | 5 chữ số (vd: `06007` cho Butte) | Có | Mã định danh địa lý FIPS chuẩn Hoa Kỳ | Tra cứu từ `California_Counties_Demographics` |
| `county_population` | Integer | $\ge 0$ người | Có | Dân số của Hạt theo điều tra Census | Lấy từ `California_Counties_Demographics` |
| `county_area_sqmi` | Float | $\ge 0.0$ dặm vuông | Có | Tổng diện tích tự nhiên của Hạt | Lấy từ `California_Counties_Demographics` |
| `cause_code` | Integer | [1, 19] | Có | Mã nguyên nhân gốc CAL FIRE (1: Lightning, 2: Equipment...) | Lấy từ FRAP `CAUSE` |
| `cause_name` | String | `Lightning`, `Equipment Use`, `Arson`, `Powerline`... | Không | Tên nguyên nhân chi tiết | Tra cứu từ bảng mã CAL FIRE |
| `cause_group` | String | `Natural`, `Human`, `Undetermined` | Không | Nhóm nguyên nhân phân loại lớn | Quy nạp: Lightning $\to$ Natural; Equipment, Powerline, Arson $\to$ Human |
| `acres_burned` | Float | $\ge 0.0$ Acres (mẫu Anh) | Không | Diện tích rừng bị thiêu rụi (Acres) | Lấy từ FRAP `GIS_ACRES` |
| `burned_area_ha` | Float | $\ge 0.0$ Hecta (ha) | Không | Diện tích quy đổi chuẩn quốc tế ($1 \text{ acre} \approx 0.404686 \text{ ha}$) | Tính toán từ `acres_burned` |
| `burned_area_is_imputed` | Boolean | `True`, `False` | Không | Cờ xác định diện tích được điền bởi mô hình ML (KNN/Iterative) | Đánh dấu độ tin cậy dữ liệu |
| `structure_id` | String | Định dạng `DINS-XXXXX` | Có | Mã định danh công trình tài sản kiểm kê | Lấy từ DINS `GlobalID` |
| `structure_type` | String | `Single Family`, `Commercial`, `Outbuilding`... | Có | Loại công trình kiến trúc bị ảnh hưởng | Lấy từ DINS `StructureType` |
| `damage_level` | String | `Destroyed (>50%)`, `Major (26-50%)`, `Minor`... | Có | Cấp độ hư hại của công trình | Lấy từ DINS `Damage` |
| `structures_destroyed` | Integer | $\ge 0$ công trình | Có | Tổng số công trình bị phá hủy hoàn toàn (>50%) | Tổng hợp từ DINS theo từng vụ cháy |
| `structures_damaged` | Integer | $\ge 0$ công trình | Có | Tổng số công trình bị hư hại một phần | Tổng hợp từ DINS theo từng vụ cháy |
| `deaths_direct` | Integer | $\ge 0$ người | Có | Số người thiệt mạng trực tiếp | Đối soát từ NOAA Casualties |
| `injuries_direct` | Integer | $\ge 0$ người | Có | Số người bị thương trực tiếp | Đối soát từ NOAA Casualties |
| `damage_property_usd` | Float | $\ge 0.0$ USD | Có | Ước tính thiệt hại tài sản quy đổi ra USD | Đối soát từ NOAA Casualties |
| `damage_property_is_imputed`| Boolean | `True`, `False` | Không | Cờ xác định thiệt hại USD được điền bởi ML | Đánh dấu độ tin cậy dữ liệu |
| `latitude` | Float | [32.0, 42.0] | Có | Vĩ độ tọa độ tâm vụ cháy / công trình | Kiểm tra phạm vi Bang California |
| `longitude` | Float | [-125.0, -114.0] | Có | Kinh độ tọa độ tâm vụ cháy / công trình | Kiểm tra phạm vi Bang California |
| `is_outlier_ml` | Boolean | `True`, `False` | Không | Cờ phát hiện bất thường bởi Isolation Forest & LOF | Phân tích ngoại lai ML trên log diện tích |
| `outlier_score` | Float | Số thực (Điểm bất thường) | Có | Điểm số ngoại lai do Isolation Forest tính | Điểm càng âm mức bất thường càng cao |
| `cause_is_predicted` | Boolean | `True`, `False` | Không | Cờ xác định nguyên nhân được dự đoán bởi Random Forest | Gán True khi xác suất $\ge 0.7$ |

---

## 3. Khóa Liên Kết Giữa Các Bảng Nguồn (Join Keys Specification)

Mô hình dữ liệu liên kết 4 bảng dữ liệu thô thông qua các trường khóa chuẩn:
1. **Liên kết $1 - N$ giữa Vụ cháy và Công trình hư hại**:
   - `California_Fire_Perimeters_all.csv` (`FIRE_NAME` chuẩn hóa) $\longleftrightarrow$ `CAL_FIRE_Damage_Inspection_DINS.csv` (`* Incident Name` chuẩn hóa).
   - **Tỷ lệ khớp thực tế**: Khớp thành công 301/398 vụ cháy lớn có thanh tra thiệt hại (chiếm 93.99% tổng số công trình ghi nhận trong lịch sử CAL FIRE DINS).
2. **Liên kết $N - 1$ giữa Công trình/Vụ cháy và Địa phương**:
   - `CAL_FIRE_Damage_Inspection_DINS.csv` (`County`) $\longleftrightarrow$ `California_Counties_Demographics.csv` (`CDTFA_COUNTY`).
   - Khớp chính xác 52/52 Hạt có ghi nhận cháy rừng tại California.
3. **Liên kết $N - 1$ đối soát Thương vong**:
   - `California_Fire_Perimeters_all.csv` (`YEAR_`) $\longleftrightarrow$ `NOAA_California_Wildfires_Casualties.csv` (`YEAR`).

---

## 4. Quy Ước Giá Trị Thiếu (Missing Values)
- Chuỗi ký tự thiếu: Biểu diễn bằng `NULL` (tránh các chuỗi `"None"`, `"N/A"`, `"-"`, `""`).
- Biến số thiếu: Giá trị `NULL` trong SQLite / `NaN` trong Pandas.
- Cột có tỷ lệ thiếu $> 60\%$: Tuyệt đối không điền bằng ML, giữ nguyên `NULL` và công bố trong báo cáo hạn chế dữ liệu.

