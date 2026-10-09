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
4. `NOAA_California_Wildfires_Casualties.csv` (NOAA NCEI - **993 sự kiện đủ 20/20 năm 2006–2025**, chỉ dùng cho thương vong: 255 người chết, 887 người bị thương trong dữ liệu thô (**207 / 792** sau khi gộp các dòng trùng giữa vùng dự báo)).
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
| `county_population` | Integer | $\ge 0$ người | Có | Dân số của Hạt theo điều tra Census | ⚠️ Cột `CENSUS_POPULATION` trong `California_Counties_Demographics` trống 100% $\to$ `NULL` trong dữ liệu sạch; `dim_county.census_population` lấy dân số US Census 2020 (`04_split_tables.py`) |
| `county_area_sqmi` | Float | $\ge 0.0$ dặm vuông | Có | Tổng diện tích tự nhiên của Hạt | Lấy từ `California_Counties_Demographics` |
| `unit_id` | String | Mã đơn vị CAL FIRE / USFS (vd: `BTU`, `LNU`, `MVU`, `LAC`) | Có | Mã đơn vị tác chiến quản lý địa bàn đám cháy | Lấy từ FRAP `Unit ID` (Khóa 3) |
| `agency` | String | `CDF`, `USF`, `CCO`, `BLM`, `NPS`, `LRA`, `FWS`, `DOD`, `BIA`, `OTH` | Có | Cơ quan quản lý đám cháy | Lấy từ FRAP `Agency` (polygon lớn nhất) |
| `cause_code` | Integer | [1, 19] | Có | Mã nguyên nhân gốc CAL FIRE (1: Lightning, 2: Equipment...) | Lấy từ FRAP `Cause` |
| `cause_name` | String | `Lightning`, `Equipment Use`, `Arson`, `Powerline`... | Không | Tên nguyên nhân chi tiết | Tra cứu từ bảng mã CAL FIRE |
| `cause_group` | String | `Natural`, `Human`, `Undetermined` | Không | Nhóm nguyên nhân phân loại lớn | Mã 1, 17 (Lightning, Volcanic) $\to$ Natural; mã 9, 14 (Miscellaneous, Unknown) $\to$ Undetermined; còn lại $\to$ Human |
| `acres_burned` | Float | $\ge 0.0$ Acres (mẫu Anh) | Không | Diện tích rừng bị thiêu rụi (Acres) | Lấy từ FRAP `GIS Calculated Acres` |
| `burned_area_ha` | Float | $\ge 0.0$ Hecta (ha) | Không | Diện tích quy đổi chuẩn quốc tế ($1 \text{ acre} \approx 0.404686 \text{ ha}$) | Tính toán từ `acres_burned` |
| `burned_area_is_imputed` | Boolean | `True`, `False` | Không | Cờ xác định diện tích được điền bởi mô hình ML (KNN/Iterative) | ⚠️ **Chưa triển khai** (`03b_ml_clean.py` chưa có) — hiện luôn `False` |
| `structure_id` | String | Định dạng `DINS-XXXXX` | Có | Mã định danh công trình tài sản kiểm kê | Lấy từ DINS `GlobalID` |
| `structure_type` | String | `Single Family`, `Commercial`, `Outbuilding`... | Có | Loại công trình kiến trúc bị ảnh hưởng | Lấy từ DINS `StructureType` |
| `damage_level` | String | `Destroyed (>50%)`, `Major (26-50%)`, `Minor`... | Có | Cấp độ hư hại của công trình | Lấy từ DINS `* Damage` |
| `structures_destroyed` | Integer | $\ge 0$ công trình | Có | Tổng số công trình bị phá hủy hoàn toàn (>50%) | Hợp nhất 20 năm: ICS-209 (2006–2012) + DINS (2013–2025) |
| `structures_damaged` | Integer | $\ge 0$ công trình | Có | Tổng số công trình bị hư hại một phần | Hợp nhất 20 năm: ICS-209 (2006–2012) + DINS (2013–2025) |
| `damage_source` | String | `CAL_FIRE_DINS`, `USDA_ICS_209`, `NONE` | Không | Nguồn dữ liệu kiểm kê thiệt hại công trình | Ghi nhận xuất xứ dữ liệu thiệt hại |
| `damage_match` | String | `exact`, `name_year_unique`, `name_year_largest`, `none` | Không | Cách ghép thiệt hại vào vụ cháy (độ tin cậy) | `exact` = khớp 3 khóa; `name_year_unique` = khác `unit_id`, tên duy nhất trong năm; `name_year_largest` = nhiều vụ trùng tên, gán cho vụ lớn nhất (**có thể nhầm**); `none` = không có thiệt hại. Xem `CLEANING_LOG.md` mục 2.1 |
| `deaths_direct` | Integer | $\ge 0$ người | Có | Số người thiệt mạng trực tiếp | NOAA Casualties, đã gộp trùng vùng dự báo (2006–2025: 207 người) |
| `injuries_direct` | Integer | $\ge 0$ người | Có | Số người bị thương trực tiếp | NOAA Casualties, đã gộp trùng vùng dự báo (2006–2025: 792 người) |
| `latitude` | Float | [32.0, 42.0] | Có | Vĩ độ tọa độ tâm vụ cháy / công trình | Kiểm tra phạm vi Bang California |
| `longitude` | Float | [-125.0, -114.0] | Có | Kinh độ tọa độ tâm vụ cháy / công trình | Kiểm tra phạm vi Bang California |
| `is_outlier_ml` | Boolean | `True`, `False` | Không | Cờ phát hiện bất thường bởi Isolation Forest & LOF | ⚠️ **Chưa triển khai** — hiện luôn `False` |
| `outlier_score` | Float | Số thực (Điểm bất thường) | Có | Điểm số ngoại lai do Isolation Forest tính | ⚠️ **Chưa triển khai** — hiện luôn `0` |
| `cause_is_predicted` | Boolean | `True`, `False` | Không | Cờ xác định nguyên nhân được dự đoán bởi Random Forest | ⚠️ **Chưa triển khai** — hiện luôn `False`; nguyên nhân không rõ được gộp vào `Undetermined` |

### 2.1. Bảng thương vong NOAA `data/tables/fact_casualty_event.csv`
1 dòng = 1 vụ cháy theo NOAA (897 dòng), đã gộp các dòng của cùng 1 vụ bị ghi lặp ở nhiều vùng dự báo. Hiện chỉ có ở dạng CSV, chưa nạp vào `database.sqlite`.

| Tên trường | Kiểu dữ liệu | Miền giá trị / Đơn vị | Cho phép NULL | Mô tả | Ghi chú |
|---|---|---|---|---|---|
| `casualty_id` | Integer | Khóa chính | Không | Khóa đại diện | Tăng dần theo ngày bắt đầu |
| `noaa_event_id` | Integer | NOAA `EVENT_ID` | Không | `EVENT_ID` nhỏ nhất trong nhóm đã gộp | Tra lại được dòng gốc NOAA |
| `episode_id` | Integer | NOAA `EPISODE_ID` | Không | Đợt thời tiết chứa sự kiện | Khóa gộp cùng `fire_name` |
| `date_id` | Integer | `YYYYMMDD` | Không | Ngày bắt đầu sự kiện | Khóa ngoại tới `dim_date` |
| `incident_id` | Integer | Khóa của `fact_fire_incident` | Có | Vụ cháy FRAP khớp được | Khớp theo (năm, tên vụ cháy), vụ lớn nhất nếu trùng tên; NULL nếu không khớp |
| `fire_name` | String | vd `CAMP`, `WOOLSEY` | Có | Tên vụ cháy tách từ narrative NOAA | NULL khi narrative không nêu tên |
| `zone_names` | String | Tên vùng dự báo NWS, ngăn cách `; ` | Không | Các vùng dự báo đã gộp | |
| `n_zones` | Integer | $\ge 1$ | Không | Số vùng dự báo đã gộp | > 1 nghĩa là dữ liệu thô đã đếm trùng |
| `deaths_direct` / `deaths_indirect` | Integer | $\ge 0$ người | Không | Số người chết trực tiếp / gián tiếp | Tổng 2006–2025: 207 / 10 |
| `injuries_direct` / `injuries_indirect` | Integer | $\ge 0$ người | Không | Số người bị thương trực tiếp / gián tiếp | Tổng 2006–2025: 792 / 261 |

### 2.2. Thương vong theo năm `data/clean/casualties_by_year.csv`
20 dòng (2006–2025), tổng hợp từ `fact_casualty_event`; năm không có sự kiện ghi 0. Mã hóa UTF-8 có BOM để Excel đọc đúng tiếng Việt.

| Tên trường | Kiểu dữ liệu | Mô tả |
|---|---|---|
| `year` | Integer | Năm |
| `noaa_fire_events` | Integer | Số vụ cháy NOAA ghi nhận (sau khi gộp trùng) |
| `deaths_direct` / `deaths_indirect` / `deaths_total` | Integer | Người chết trực tiếp / gián tiếp / tổng |
| `injuries_direct` / `injuries_indirect` / `injuries_total` | Integer | Người bị thương trực tiếp / gián tiếp / tổng |
| `deadliest_fire` | String | Vụ cháy làm chết nhiều người nhất trong năm; `(không rõ tên) <vùng dự báo>` khi NOAA không nêu tên; trống nếu năm đó không có người chết |
| `deadliest_fire_deaths` | Integer | Số người chết trực tiếp của vụ đó |
| `deaths_share_of_period` | Float | Tỷ lệ người chết trực tiếp của năm trên tổng 2006–2025 (0–1) |

> ⚠️ NOAA ghi thiếu một số vụ (vd đợt cháy Wine Country 10/2017 ở Sonoma / Napa), nên số năm 2017 thấp hơn số chính thức.

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

