# Danh Mục Nguồn Dữ Liệu (DATA SOURCES)

> **Người phụ trách**: Thành viên 1 - Kỹ sư Dữ liệu & Học máy (Data & ML Engineer)  
> **Trạng thái**: Đã hoàn thành thu thập dữ liệu thô (Đạt chỉ tiêu $\ge 5.000$ dòng và $\ge 3$ bảng)  
> **Cập nhật ngày**: 2026-10-06  
> **Phân vùng nghiên cứu trọng tâm**: Bang California (Hoa Kỳ / Bắc Mỹ) — Tâm điểm thảm họa cháy rừng khốc liệt nhất thế giới.

---

## 1. Mục Tiêu & Tiêu Chí Đánh Giá Nguồn Dữ Liệu

Đề tài nghiên cứu: **"Nghiên cứu – phân tích tần suất và thiệt hại của các trận cháy rừng tại California / Bắc Mỹ trong 20 năm qua (2006–2025)"**.  
Theo thống nhất chuyên môn, tập dữ liệu tập trung toàn diện vào 2 khía cạnh cốt lõi:
1. **Tần suất bùng phát cháy rừng**: Thời gian, chu kỳ theo tháng/mùa vụ, phân bố không gian theo từng hạt (County).
2. **Thiệt hại toàn diện**:
   - *Thiệt hại diện tích*: Số mẫu Anh (Acres) / Hecta (ha) rừng bị thiêu rụi, phân cấp quy mô đám cháy.
   - *Thiệt hại tài sản & hạ tầng*: Số lượng công trình, nhà ở đơn lập, công trình tiện ích bị phá hủy hoàn toàn (>50%) hoặc hư hại một phần (DINS).
   - *Thiệt hại con người*: Thương vong trực tiếp và gián tiếp (tử vong, bị thương) theo báo cáo NOAA.
   - *Căn nguyên kích hoạt*: Phân loại chi tiết nguyên nhân Tự nhiên (Sét đánh) vs Tác nhân con người (Tia lửa máy móc, bất cẩn, phóng hỏa...).

---

## 2. Bảng So Sánh Chi Tiết Các Nguồn Dữ Liệu Thực Tế

| Tiêu chí | 1. CAL FIRE Fire Perimeters (FRAP) | 2. CAL FIRE Damage Inspection (DINS) | 3. CA Counties Boundaries & Demographics | 4. NOAA Storm Events (California) |
|---|---|---|---|---|
| **Cơ quan phát hành** | CAL FIRE FRAP / California Natural Resources Agency | CAL FIRE / State of California Open Data | California Dept of Technology / US Census | NOAA NCEI (U.S. Federal Government) |
| **URL chính thức** | [gis.data.cnra.ca.gov](https://gis.data.cnra.ca.gov/datasets/CALFIRE-Forestry::california-fire-perimeters-all) | [gis.data.cnra.ca.gov](https://gis.data.cnra.ca.gov/datasets/CALFIRE-Forestry::cal-fire-damage-inspection-dins-data) | [gis.data.ca.gov](https://gis.data.ca.gov/datasets/CDB::california-county-boundaries-and-identifiers) | [ncei.noaa.gov](https://www.ncei.noaa.gov/pub/data/swdi/stormevents/) |
| **Khoảng thời gian** | 1878–2025 (Chuỗi 20 năm 2006–2025 có 7.646 vụ) | 2013–2025 (Hơn 132.500 bản ghi chi tiết) | Dữ liệu hành chính chuẩn hóa hiện tại | 2006–2025 (Sự kiện thiên tai cấp bang) |
| **Phạm vi địa lý** | Toàn bộ bang California (58 Hạt) | Toàn bộ bang California (vùng cháy SRA) | 58 Hạt (Counties) thuộc California | Toàn bộ bang California |
| **Số dòng quan sát** | **23.334 dòng** (vượt xa yêu cầu 5.000 dòng) | **132.522 dòng** (kiểm kê từng công trình) | **58 dòng** (danh mục 58 hạt chuẩn) | **139+ sự kiện** có thương vong/USD |
| **Giấy phép** | Public Domain / California Open Data | Public Domain / California Open Data | Public Domain / State Geoportal | U.S. Federal Government (Public Domain) |
| **Các trường thông tin chính** | `Fire Name`, `Year`, `Alarm Date`, `Containment Date`, `Cause`, `GIS Calculated Acres`, `Unit ID` | `* Incident Name`, `* Damage`, `* Structure Type`, `County`, `Latitude`, `Longitude`, `Assessed Improved Value` | `CDTFA_COUNTY`, `CENSUS_POPULATION`, `AREA_SQMI`, `GNIS_ID`, `CDT_COUNTY_ABBR` | `EVENT_ID`, `CZ_NAME`, `DAMAGE_PROPERTY`, `DAMAGE_CROPS`, `DEATHS_DIRECT`, `INJURIES_DIRECT` |
| **Mục đích sử dụng** | **Bảng Fact chính**: Đo lường tần suất theo năm/tháng, diện tích tàn phá, căn nguyên đám cháy | **Bảng Fact phụ / Chi tiết**: Phân tích mức độ phá hủy nhà cửa, công trình, loại hình kiến trúc | **Bảng Dimension Địa lý**: Join phân cấp từ Hạt $\to$ Khu vực, tính tỷ lệ thiệt hại trên dân số | **Bảng Đối soát Thiệt hại**: Bổ sung số liệu thương vong sinh mạng và giá trị USD quy đổi |

---

## 3. Bản Kê Chi Tiết Dữ Liệu Thô Đã Tải (`data/raw/calfire/`)

Toàn bộ các tệp dữ liệu đã được tải về lưu trữ tại `data/raw/calfire/`, tự động sinh mã băm kiểm tra tính toàn vẹn (SHA-256):

1. **`California_Fire_Perimeters_all.csv`** (Dung lượng: ~4.18 MB, **23.334 dòng**):
   - Chứa toàn bộ chu vi, diện tích mẫu Anh (Acres) và mã nguyên nhân của các vụ cháy rừng tại California từ cơ quan lâm nghiệp CAL FIRE.
2. **`CAL_FIRE_Damage_Inspection_DINS.csv`** (Dung lượng: ~60.59 MB, **132.522 dòng**):
   - Chứa cơ sở dữ liệu kiểm kê thiệt hại tài sản thực tế: 70.390 công trình bị phá hủy hoàn toàn (>50%), 7.127 công trình bị hư hại, phân loại rõ nhà ở dân cư, xe cộ, nhà phụ trợ, kèm tọa độ GPS và tên hạt.
3. **`California_Counties_Demographics.csv`** (Dung lượng: ~8.7 KB, **58 dòng**):
   - Danh mục 58 hạt của bang California kèm diện tích dặm vuông (`AREA_SQMI`) và dân số điều tra Census (`CENSUS_POPULATION`).
4. **`NOAA_California_Wildfires_Casualties.csv`** (Dung lượng: ~178 KB):
   - Các vụ cháy rừng nghiêm trọng tại California được NOAA ghi nhận thương vong trực tiếp và thiệt hại tài sản quy đổi.

---

## 4. Cam Kết Đáp Ứng Chuẩn Barem Môn Học (File PDF)

- **Quy mô dữ liệu**: Đạt **23.334 dòng** trong bảng Perimeters và **132.522 dòng** trong bảng DINS (Yêu cầu đề bài $\ge 5.000$ dòng $\implies$ **VƯỢT XA YÊU CẦU**).
- **Cấu trúc đa bảng**: Có 4 bảng độc lập với các khóa liên kết rõ ràng (`Fire Name`, `Incident Name`, `County`, `Year`) để thực hiện thao tác **Join/Merge** xây dựng mô hình Star Schema.
- **Tính khả thi của Dashboard & Storytelling**:
  - Dễ dàng dựng **Map chuyên đề California theo 58 Hạt** (Choropleth Map diện tích cháy theo hạt, Proportional Symbol Map các điểm cháy lớn).
  - Đầy đủ các chiều phân tích: Bar Chart (số vụ), Line/Dual Axis (diện tích vs công trình phá hủy theo năm), Pareto 80/20 (top các hạt chịu thiệt hại nặng nhất), Donut Chart (cơ cấu nguyên nhân), Scatter Plot (diện tích vs số nhà bị phá hủy).
