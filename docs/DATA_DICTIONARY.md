# Từ Điển Dữ Liệu (DATA DICTIONARY)

> **Người phụ trách**: Thành viên 1 - Kỹ sư Dữ liệu (Data Engineer)  
> **Phạm vi nghiên cứu**: Cháy rừng Bang California / Bắc Mỹ giai đoạn 2006–2025  
> **Trạng thái**: Đặc tả chuẩn hóa các trường dữ liệu và khóa liên kết

---

## 1. Tổng Quan Cấu Trúc Tập Dữ Liệu `master_clean.csv`
Tập dữ liệu sau làm sạch và tích hợp `data/clean/master_clean.csv` đóng vai trò là bảng nguồn tổng thể (Master Dataset), kết nối 5 nguồn dữ liệu thô uy tín:
1. `California_Fire_Perimeters_all.csv` (CAL FIRE FRAP - 23.334 dòng lịch sử, **7.342 vụ trong 2006–2025**).
2. `CAL_FIRE_Damage_Inspection_DINS.csv` (CAL FIRE DINS - 132.522 dòng công trình kiểm kê thiệt hại tài sản giai đoạn **2013–2025**, 70.390 nhà phá hủy hoàn toàn).
3. `ICS209_California_Wildfires_2006_2012.csv` (USDA Forest Service / NIFC - 1.127 vụ cháy, 7.206 nhà bị phá hủy giai đoạn **2006–2012**).
4. `NOAA_California_Wildfires_Casualties.csv` (NOAA NCEI - **993 sự kiện đủ 20/20 năm 2006–2025**, 255 người chết, 887 người bị thương và thiệt hại USD).
5. `California_Counties_Demographics.csv` (Cục Dân số / CDTFA - **58 Hạt của California** kèm diện tích dặm vuông và dân số Census).

- **Số dòng tối thiểu cam kết**: $\ge 5.000$ dòng (Bảng vụ cháy sạch `data/interim/master_rules_cleaned.csv` có **7.235 vụ** sau khi gộp polygon từ 7.342 dòng FRAP; Bảng công trình kiểm kê chi tiết có 132.522 dòng $\implies$ **Vượt xa barem $\ge 5.000$ dòng**).
- **Phạm vi thời gian**: **20/20 năm liên tục từ 2006 đến 2025**, không bị khuyết bất kỳ năm nào trên tất cả các thước đo.
- **Quy tắc đặt tên cột**: Tiếng Anh, chữ thường, nối bằng dấu gạch dưới (`snake_case`).

---

## 2. Danh Mục Các Trường Dữ Liệu (Field Specifications)

| Tên Cột | Kiểu Dữ Liệu | Đơn Vị / Miền Giá Trị | Cho Phép NULL | Mô Tả Ý Nghĩa | Nguồn & Quy Tắc Xử Lý |
|---------|--------------|------------------------|---------------|---------------|------------------------|
| `incident_id` | String | `CALFIRE-YYYY-NNNNN` (vd: `CALFIRE-2018-00396`) | Không | Khóa định danh duy nhất của từng vụ cháy rừng | Sinh trong `03_clean.py`: số thứ tự trong năm, sắp theo `alarm_date`, `fire_name`, `unit_id` |
| `frap_global_id` | String | UUID | Không | Mã `GlobalID` của polygon FRAP lớn nhất thuộc vụ cháy | Lấy từ FRAP `GlobalID`, dùng để truy vết về dữ liệu gốc |
| `n_polygons` | Integer | $\ge 1$ | Không | Số polygon FRAP được gộp thành vụ cháy này | Gộp theo (`year`, `fire_name`, `unit_id`) |
| `fire_name` | String | Tên chuẩn hóa (vd: `CAMP`, `AUGUST`); vụ không tên = `UNNAMED` | Không | Tên chính thức của vụ cháy rừng | Upper case, `CMPLX` $\to$ `COMPLEX`, gỡ hậu tố `FIRE` / `INCIDENT` / `COMPLEX` (`normalize_fire_name()`) |
| `fire_name_raw` | String | Tên gốc | Có | Tên vụ cháy trước chuẩn hóa (lưu vết) | FRAP `Fire Name` (38 vụ không tên = `NULL`) |
| `year` | Integer | [2006, 2025] | Không | Năm bùng phát vụ cháy | Trích xuất từ FRAP `Year` hoặc `alarm_date` |
| `alarm_date` | Date | `YYYY-MM-DD` | Có | Ngày phát lệnh báo động cháy | Chuẩn hóa từ `Alarm Date` |
| `cont_date` | Date | `YYYY-MM-DD` | Có | Ngày khống chế / dập tắt đám cháy | Chuẩn hóa từ `Containment Date` ($\ge$ `alarm_date`) |
| `duration_days` | Float | [0, 365] ngày | Có | Thời gian đám cháy hoành hành | Hiệu số giữa `cont_date` và `alarm_date`; ngoài [0, 365] coi là lỗi nhập liệu $\to$ `NULL` |
| `county` | String | Tên ngắn 58 Hạt, khớp Demographics `CDT_NAME_SHORT` (vd: `Butte`, `Los Angeles`) | Có | Tên Hạt (County) tại California nơi xảy ra cháy | Ưu tiên DINS `County` / ICS-209 `POO_COUNTY`; còn thiếu thì suy từ Hạt phổ biến nhất của `unit_id`. 840 vụ `NULL` |
| `county_fips` | String | 5 chữ số (vd: `06007` cho Butte) | Có | Mã định danh địa lý FIPS chuẩn Hoa Kỳ | Tra cứu từ `California_Counties_Demographics` |
| `county_population` | Integer | $\ge 0$ người | Có | Dân số của Hạt theo điều tra Census | ⚠️ Cột `CENSUS_POPULATION` trong `California_Counties_Demographics` trống 100% $\to$ hiện toàn bộ `NULL`, cần nguồn dân số khác |
| `county_area_sqmi` | Float | $\ge 0.0$ dặm vuông | Có | Tổng diện tích tự nhiên của Hạt | Lấy từ `California_Counties_Demographics` |
| `unit_id` | String | Mã đơn vị CAL FIRE / USFS (vd: `BTU`, `LNU`, `MVU`, `LAC`) | Có | Mã đơn vị tác chiến quản lý địa bàn đám cháy | Lấy từ FRAP `Unit ID` (Khóa 3) |
| `agency` | String | `CDF`, `USF`, `CCO`, `BLM`, `NPS`, `LRA`, `FWS`, `DOD`, `BIA`, `OTH` | Có | Cơ quan quản lý đám cháy | Lấy từ FRAP `Agency` (polygon lớn nhất) |
| `cause_code` | Integer | [1, 19] | Có | Mã nguyên nhân gốc CAL FIRE (1: Lightning, 2: Equipment...) | Lấy từ FRAP `Cause` |
| `cause_name` | String | `Lightning`, `Equipment Use`, `Arson`, `Powerline`... | Không | Tên nguyên nhân chi tiết | Tra cứu từ bảng mã CAL FIRE |
| `cause_group` | String | `Natural`, `Human`, `Undetermined` | Không | Nhóm nguyên nhân phân loại lớn | Mã 1, 17 (Lightning, Volcanic) $\to$ Natural; mã 9, 14 (Miscellaneous, Unknown) $\to$ Undetermined; còn lại $\to$ Human |
| `acres_burned` | Float | $\ge 0.0$ Acres (mẫu Anh) | Không | Diện tích rừng bị thiêu rụi (Acres) | Lấy từ FRAP `GIS Calculated Acres` |
| `burned_area_ha` | Float | $\ge 0.0$ Hecta (ha) | Không | Diện tích quy đổi chuẩn quốc tế ($1 \text{ acre} \approx 0.404686 \text{ ha}$) | Tính toán từ `acres_burned` |
| `burned_area_is_imputed` | Boolean | `True`, `False` | Không | Cờ xác định diện tích được điền bởi mô hình ML (KNN/Iterative) | Đánh dấu độ tin cậy dữ liệu |
| `structure_id` | String | Định dạng `DINS-XXXXX` | Có | Mã định danh công trình tài sản kiểm kê | Lấy từ DINS `GlobalID` |
| `structure_type` | String | `Single Family`, `Commercial`, `Outbuilding`... | Có | Loại công trình kiến trúc bị ảnh hưởng | Lấy từ DINS `StructureType` |
| `damage_level` | String | `Destroyed (>50%)`, `Major (26-50%)`, `Minor`... | Có | Cấp độ hư hại của công trình | Lấy từ DINS `* Damage` |
| `structures_destroyed` | Integer | $\ge 0$ công trình | Có | Tổng số công trình bị phá hủy hoàn toàn (>50%) | Hợp nhất 20 năm: ICS-209 (2006–2012) + DINS (2013–2025) |
| `structures_damaged` | Integer | $\ge 0$ công trình | Có | Tổng số công trình bị hư hại một phần | Hợp nhất 20 năm: ICS-209 (2006–2012) + DINS (2013–2025) |
| `damage_source` | String | `CAL_FIRE_DINS`, `USDA_ICS_209`, `NONE` | Không | Nguồn dữ liệu kiểm kê thiệt hại công trình | Ghi nhận xuất xứ dữ liệu thiệt hại |
| `damage_match` | String | `exact`, `name_year_unique`, `name_year_largest`, `none` | Không | Cách ghép thiệt hại vào vụ cháy (độ tin cậy) | `exact` = khớp 3 khóa; `name_year_unique` = khác `unit_id`, tên duy nhất trong năm; `name_year_largest` = nhiều vụ trùng tên, gán cho vụ lớn nhất (**có thể nhầm**); `none` = không có thiệt hại. Xem `CLEANING_LOG.md` mục 2.1 |
| `deaths_direct` | Integer | $\ge 0$ người | Có | Số người thiệt mạng trực tiếp | Đối soát từ NOAA Casualties (2006–2025: 255 người) |
| `injuries_direct` | Integer | $\ge 0$ người | Có | Số người bị thương trực tiếp | Đối soát từ NOAA Casualties (2006–2025: 887 người) |
| `damage_property_usd` | Float | $\ge 0.0$ USD | Có | Ước tính thiệt hại tài sản quy đổi ra USD | Đối soát từ NOAA Casualties |
| `damage_property_is_imputed`| Boolean | `True`, `False` | Không | Cờ xác định thiệt hại USD được điền bởi ML | Đánh dấu độ tin cậy dữ liệu |
| `latitude` | Float | [32.0, 42.0] | Có | Vĩ độ tọa độ tâm vụ cháy / công trình | Kiểm tra phạm vi Bang California |
| `longitude` | Float | [-125.0, -114.0] | Có | Kinh độ tọa độ tâm vụ cháy / công trình | Kiểm tra phạm vi Bang California |
| `is_outlier_ml` | Boolean | `True`, `False` | Không | Cờ phát hiện bất thường bởi Isolation Forest & LOF | Phân tích ngoại lai ML trên log diện tích |
| `outlier_score` | Float | Số thực (Điểm bất thường) | Có | Điểm số ngoại lai do Isolation Forest tính | Điểm càng âm mức bất thường càng cao |
| `cause_is_predicted` | Boolean | `True`, `False` | Không | Cờ xác định nguyên nhân được dự đoán bởi Random Forest | Gán True khi xác suất $\ge 0.7$ |

---

## 3. Khóa Liên Kết Giữa Các Bảng Nguồn (Join Keys Specification)

Mô hình dữ liệu liên kết 5 bảng dữ liệu thô thông qua **3 Thuộc tính Khóa cốt lõi**:

1. **Khóa 1 (Tên vụ cháy - Primary Link)**:
   - `California_Fire_Perimeters_all.csv` (`Fire Name` chuẩn hóa) $\longleftrightarrow$ `CAL_FIRE_Damage_Inspection_DINS.csv` (`* Incident Name` chuẩn hóa) $\longleftrightarrow$ `ICS209_California_Wildfires_2006_2012.csv` (`INCIDENT_NAME` chuẩn hóa).
   - *Chuẩn hóa*: Viết hoa toàn bộ (`UPPER`), cắt khoảng trắng (`TRIM`), loại bỏ các hậu tố dư thừa (`FIRE`, `INCIDENT`, `COMPLEX`).

2. **Khóa 2 (Năm xảy ra vụ cháy - Temporal Check)**:
   - `FRAP` (`Year`) $\longleftrightarrow$ `DINS` (Năm trích xuất từ `Incident Start Date`) $\longleftrightarrow$ `ICS-209` (`START_YEAR`).
   - *Tác dụng*: Đối soát tránh ghép nhầm các vụ cháy có cùng tên xảy ra ở các năm khác nhau.

3. **Khóa 3 (Không gian địa lý & Đơn vị tác chiến - Spatial Disambiguation)**:
   - `FRAP` (`Unit ID`) $\longleftrightarrow$ `DINS` (`* CAL FIRE Unit`, 100% mã có trong FRAP) $\longleftrightarrow$ `ICS-209` (mã đơn vị tách từ `INCIDENT_NUMBER`, vd `CA-RRU-062485` $\to$ `RRU`; tách được 1.120 / 1.127 dòng).
   - *Tác dụng*: Khử trùng lặp và phân biệt chính xác các vụ cháy trùng tên cùng xảy ra trong 1 năm (ví dụ phân biệt Camp Fire 2018 tại Butte (`BTU`) với vụ cháy nhỏ cùng tên tại San Luis Obispo (`SLU`)).
   - **Tỷ lệ khớp thực tế** (`src/03_clean.py`): ghép thiệt hại vào **447 vụ cháy**, bắt trọn **73.818 / 77.503 công trình bị phá hủy (95,2%)** sau khi khử 109 dòng DINS trùng.

4. **Liên kết Dimension Không gian**:
   - `county` $\longleftrightarrow$ `California_Counties_Demographics.csv` (`CDT_NAME_SHORT`; cột `CDTFA_COUNTY` có hậu tố " County" nên không dùng làm khóa). Khớp 100% (51 Hạt có trong bảng vụ cháy). FIPS = `CENSUS_GEOID` đệm đủ 5 số (vd `06007`).

---

## 4. Quy Ước Giá Trị Thiếu (Missing Values)
- Chuỗi ký tự thiếu: Biểu diễn bằng `NULL` (tránh các chuỗi `"None"`, `"N/A"`, `"-"`, `""`).
- Biến số thiếu: Giá trị `NULL` trong SQLite / `NaN` trong Pandas.
- Cột có tỷ lệ thiếu $> 60\%$: Tuyệt đối không điền bằng ML, giữ nguyên `NULL` và công bố trong báo cáo hạn chế dữ liệu.

