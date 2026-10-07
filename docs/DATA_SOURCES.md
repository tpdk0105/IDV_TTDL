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

| Tiêu chí | 1. CAL FIRE Fire Perimeters (FRAP) | 2. CAL FIRE Damage Inspection (DINS) | 3. USDA / NIFC (ICS-209-PLUS) | 4. NOAA Storm Events (California) | 5. CA Counties Boundaries |
|---|---|---|---|---|---|
| **Cơ quan phát hành** | CAL FIRE FRAP / California CNRA | CAL FIRE / California Open Data | USDA Forest Service / NIFC | NOAA NCEI (U.S. Federal Government) | California Dept of Technology / US Census |
| **URL chính thức** | [gis.data.cnra.ca.gov](https://gis.data.cnra.ca.gov/datasets/CALFIRE-Forestry::california-fire-perimeters-all) | [gis.data.cnra.ca.gov](https://gis.data.cnra.ca.gov/datasets/CALFIRE-Forestry::cal-fire-damage-inspection-dins-data) | [figshare.com (DOI: 10.6084/m9.figshare.19858927)](https://figshare.com/articles/dataset/19858927) | [ncei.noaa.gov](https://www.ncei.noaa.gov/pub/data/swdi/stormevents/) | [gis.data.ca.gov](https://gis.data.ca.gov/datasets/CDB::california-county-boundaries-and-identifiers) |
| **Khoảng thời gian** | 1878–2025 (Chuỗi 20 năm 2006–2025 có **7.342 vụ**) | **2013–2025** (Hơn 132.500 bản ghi chi tiết công trình) | **2006–2012** (Phủ kín khoảng trống 7 năm đầu) | **2006–2025** (Đủ 20/20 năm thiên tai cấp bang) | Chuẩn hóa hành chính hiện hành |
| **Phạm vi địa lý** | Toàn bộ bang California (58 Hạt) | Toàn bộ bang California (vùng cháy SRA) | Toàn bộ bang California (vùng trách nhiệm liên bang & bang) | Toàn bộ bang California | 58 Hạt (Counties) thuộc California |
| **Số dòng quan sát** | **23.334 dòng** (vượt xa yêu cầu 5.000 dòng) | **132.522 dòng** (kiểm kê từng công trình) | **1.127 sự kiện cháy lớn** | **993 sự kiện** có thương vong/USD | **58 dòng** (danh mục 58 hạt chuẩn) |
| **Giấy phép** | Public Domain / California Open Data | Public Domain / California Open Data | U.S. Federal Government Open Research Data | U.S. Federal Government (Public Domain) | Public Domain / State Geoportal |
| **Các trường thông tin chính** | `Fire Name`, `Year`, `Alarm Date`, `Containment Date`, `Cause`, `GIS Calculated Acres`, `Unit ID` | `* Incident Name`, `* Damage`, `* Structure Type`, `County`, `Latitude`, `Longitude` | `INCIDENT_NAME`, `START_YEAR`, `POO_COUNTY`, `STR_DESTROYED_TOTAL`, `STR_DAMAGED_TOTAL` | `EVENT_ID`, `YEAR`, `CZ_NAME`, `DAMAGE_PROPERTY`, `DEATHS_DIRECT`, `INJURIES_DIRECT` | `CDTFA_COUNTY`, `CENSUS_POPULATION`, `AREA_SQMI`, `GNIS_ID`, `CDT_COUNTY_ABBR` |
| **Mục đích sử dụng** | **Bảng Fact chính**: Đo lường tần suất theo năm/tháng, diện tích tàn phá, căn nguyên đám cháy | **Bảng Fact Thiệt hại (2013–2025)**: Phân tích chi tiết từng loại nhà, mức độ phá hủy | **Bảng Bổ sung Thiệt hại (2006–2012)**: Lấp đầy dữ liệu số nhà bị phá hủy giai đoạn đầu $\implies$ Đủ 20 năm! | **Bảng Fact Thương vong (2006–2025)**: Bổ sung số người chết, bị thương và giá trị USD quy đổi | **Bảng Dimension Địa lý**: Join phân cấp từ Hạt $\to$ Khu vực, tính tỷ lệ thiệt hại trên dân số |

---

## 3. Bản Kê Chi Tiết Dữ Liệu Thô Đã Tải (`data/raw/calfire/`)

Toàn bộ 5 tệp dữ liệu đã được tải về và xác thực tính toàn vẹn tại `data/raw/calfire/`, tự động sinh mã băm SHA-256:

1. **`California_Fire_Perimeters_all.csv`** (Dung lượng: ~3.97 MB, **23.334 dòng**):
   - Chứa toàn bộ chu vi, diện tích mẫu Anh (Acres) và mã nguyên nhân của các vụ cháy rừng tại California từ CAL FIRE FRAP (giai đoạn 2006–2025 có **7.342 vụ cháy** với **19.386.513 mẫu Anh** bị thiêu rụi).
2. **`CAL_FIRE_Damage_Inspection_DINS.csv`** (Dung lượng: ~57.66 MB, **132.522 dòng**):
   - Cơ sở dữ liệu kiểm kê thiệt hại tài sản chi tiết giai đoạn 2013–2025: **70.390 công trình bị phá hủy hoàn toàn (>50%)**, **7.127 công trình bị hư hại**, phân loại rõ loại hình nhà ở dân cư, thương mại, nhà phụ trợ, kèm tọa độ GPS và hạt.
3. **`ICS209_California_Wildfires_2006_2012.csv`** (Dung lượng: ~0.96 MB, **1.127 dòng**):
   - Dữ liệu báo cáo sự cố ICS-209 từ USDA Forest Service & NIFC giai đoạn 2006–2012: ghi nhận **7.206 công trình bị phá hủy hoàn toàn** và **990 công trình bị hư hại**, lấp đầy hoàn hảo khoảng trống 7 năm đầu để chuỗi thiệt hại công trình đạt **đủ 20/20 năm liên tục (2006–2025)**.
4. **`NOAA_California_Wildfires_Casualties.csv`** (Dung lượng: ~0.86 MB, **993 dòng**):
   - Toàn bộ sự kiện cháy rừng tại California từ NOAA NCEI Storm Events phủ kín **đủ 20/20 năm (2006–2025)**: ghi nhận **255 người thiệt mạng trực tiếp**, **887 người bị thương**, và thiệt hại tài sản quy đổi USD.
5. **`California_Counties_Demographics.csv`** (Dung lượng: ~8.7 KB, **58 dòng**):
   - Danh mục chuẩn 58 hạt của bang California kèm diện tích dặm vuông (`AREA_SQMI`) và dân số điều tra Census (`CENSUS_POPULATION`).

---

## 4. Cam Kết Đáp Ứng Chuẩn Barem Môn Học (File PDF)

- **Quy mô dữ liệu**: Đạt **23.334 dòng** trong bảng Perimeters, **132.522 dòng** trong bảng DINS, **1.127 dòng** trong bảng ICS-209, **993 dòng** trong NOAA (Tổng cộng hơn **157.000 dòng**, vượt xa chỉ tiêu $\ge 5.000$ dòng).
- **Chuỗi thời gian hoàn chỉnh**: Cả 4 trụ cột phân tích (Tần suất, Diện tích, Thiệt hại công trình, Thương vong con người) đều **phủ đủ 20/20 năm liên tục từ 2006 đến 2025**, không để trống bất kỳ năm nào!
- **Cấu trúc đa bảng**: Có 5 bảng độc lập với các khóa liên kết chuẩn mực (`Fire Name`, `Incident Name`, `County`, `Year`) để thực hiện thao tác **Join/Merge/Union** xây dựng mô hình Star Schema.
- **Tính khả thi của Dashboard & Storytelling**:
  - Dễ dàng dựng **Map chuyên đề California theo 58 Hạt** (Choropleth Map diện tích cháy theo hạt, Proportional Symbol Map các điểm cháy lớn).
  - Đầy đủ các chiều phân tích: Bar Chart (số vụ theo năm/tháng), Line/Dual Axis (diện tích vs công trình phá hủy theo năm), Pareto 80/20 (top các hạt chịu thiệt hại nặng nhất), Donut Chart (cơ cấu nguyên nhân Tự nhiên vs Nhân tạo), Scatter Plot (diện tích vs số nhà bị phá hủy).
