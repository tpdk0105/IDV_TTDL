# Danh Mục Nguồn Dữ Liệu (DATA SOURCES)

> **Người phụ trách**: Thành viên 1 - Kỹ sư Dữ liệu (Data Engineer)  
> **Trạng thái**: Đã hoàn thành thu thập dữ liệu thô (Giai đoạn 2)  
> **Cập nhật ngày**: 2026-10-01  

---

## 1. Mục Tiêu & Tiêu Chí Đánh Giá Nguồn Dữ Liệu

Đề tài nghiên cứu: **"Nghiên cứu – phân tích tần suất và thiệt hại của các trận cháy rừng / thảm họa thiên nhiên trong 20 năm qua (2005–2024)"**.  
Trọng tâm là cháy rừng (Wildfire / Forest Fire); các thảm họa thiên nhiên khác (Lũ lụt, Bão, Hạn hán, Động đất, Núi lửa...) được sử dụng để so sánh và đặt vào bối cảnh toàn cục.

### Tiêu chí lựa chọn nguồn:
1. **Tính xác thực & Uy tín học thuật**: Dữ liệu từ các cơ quan chính phủ, viện nghiên cứu khoa học hoặc tổ chức quốc tế uy tín (NASA, NOAA, USDA Forest Service, CRED UCLouvain, Our World in Data).
2. **Phạm vi thời gian**: Bao quát giai đoạn 2005–2024 (hoặc các năm đại diện trong giai đoạn).
3. **Mức độ chi tiết (Granularity)**: Ưu tiên dữ liệu cấp sự kiện (Event-level) có tọa độ, thời gian bùng phát, nguyên nhân, diện tích thiệt hại và tác động kinh tế/sinh mạng.
4. **Quy mô mẫu**: Đảm bảo sau khi tiền xử lý và làm sạch đạt tối thiểu 5.000 bản ghi hợp lệ.
5. **Tính mở & Tái lập (Reproducibility)**: Có thể tải tự động bằng script (`src/01_download.py`), giấy phép rõ ràng (Public Domain, Open Access, CC-BY 4.0).

---

## 2. Bảng So Sánh Chi Tiết Các Nguồn Dữ Liệu

| Tiêu chí | 1. Our World in Data (OWID) | 2. NASA FIRMS (MODIS & VIIRS) | 3. NOAA NCEI Storm Events | 4. USFS FPA-FOD (Wildfires) | 5. EM-DAT (CRED UCLouvain) |
|---|---|---|---|---|---|
| **Tổ chức quản lý** | Global Change Data Lab / Oxford | NASA Earthdata | NOAA (National Centers for Env. Information) | USDA Forest Service (Karen Short) | CRED, UCLouvain (Bỉ) |
| **URL chính thức** | [ourworldindata.org](https://ourworldindata.org/natural-disasters) | [firms.modaps.eosdis.nasa.gov](https://firms.modaps.eosdis.nasa.gov/) | [ncei.noaa.gov](https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/) | [apps.fs.usda.gov](https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_FireOccurrence6thEdition_01/MapServer/29) | [public.emdat.be](https://public.emdat.be/) |
| **Khoảng năm có sẵn** | 1900–2024+ | 2000–nay (File 7 ngày gần nhất) | 1950–2024+ (Theo từng năm) | 1992–2020 (Phiên bản thứ 6) | 1900–2025 |
| **Phạm vi địa lý** | Toàn cầu (theo quốc gia/khu vực) | Toàn cầu | Hoa Kỳ & Lãnh thổ | Hoa Kỳ | Toàn cầu |
| **Cấp dữ liệu** | Tổng hợp theo năm / quốc gia | Điểm ảnh vệ tinh phát hiện nhiệt (Hotspots) | Cấp sự kiện thiên tai chi tiết | Cấp sự kiện cháy rừng | Cấp sự kiện thảm họa vĩ mô |
| **Số dòng quan sát thực tế** | 605 dòng (số vụ), 1.129 dòng (thiệt hại) | 68.312 dòng (MODIS), 385.296 dòng (VIIRS) | 61.281 dòng (2020), 75.593 dòng (2023) | 1.000 dòng mẫu (từ 2,3+ triệu bản ghi) | 8.111 dòng (2005–2024) |
| **Dung lượng tải** | ~50 KB | ~35 MB (2 file) | ~22 MB (2 năm gzip) | ~104 KB (mẫu) | ~5–10 MB |
| **Giấy phép** | Creative Commons Attribution (CC-BY 4.0) | NASA Open Data Policy (Public Domain) | U.S. Federal Government (Public Domain) | U.S. Federal Government (Public Domain) | Nghiên cứu phi thương mại (Đăng ký tài khoản) |
| **Phương thức thu thập** | Tải tự động qua HTTP GET trực tiếp | Tải tự động qua HTTP GET trực tiếp | Tải tự động qua HTTP GET trực tiếp | Tải tự động qua REST API (ArcGIS MapServer) | Tải thủ công sau khi đăng nhập tài khoản |
| **Điểm mạnh** | Dễ tải, đối soát xu hướng 20 năm toàn cầu rất chuẩn | Tọa độ chuẩn xác, thời gian thực, độ phân giải cao | Dữ liệu sự kiện cực kỳ phong phú (51 cột, gồm cả Wildfire, Flood, Tornado...) | Dữ liệu cháy rừng chuyên sâu nhất: nguyên nhân NWCG, diện tích đám cháy | Đầy đủ thiệt hại USD, số người chết, số người ảnh hưởng trên toàn cầu |
| **Hạn chế** | Không có cấp sự kiện chi tiết, không có nguyên nhân | Là hotspot nhiệt vệ tinh chứ không trực tiếp đo thiệt hại USD | Giới hạn lãnh thổ Mỹ | API bị nghẽn nếu query diện rộng; cần chia năm | Yêu cầu đăng nhập, không tải tự động trực tiếp bằng script không có token |
| **Quyết định sử dụng** | **CHỌN (Dữ liệu vĩ mô)**: Dùng đối soát xu hướng Dashboard D1 & D2 | **CHỌN (Bản đồ & Mật độ)**: Dùng cho Dashboard D3 (Bản đồ điểm & Heatmap) | **CHỌN (Cấp sự kiện so sánh)**: Dùng để so sánh Cháy rừng vs Thảm họa khác | **CHỌN (Cấp sự kiện cháy rừng)**: Cung cấp cột nguyên nhân, diện tích đám cháy | **CHỌN (Nguồn bổ trợ thủ công)**: Dùng làm nguồn tham chiếu quốc tế |

---

## 3. Nhật Ký Thu Thập Dữ Liệu Thô (Raw Data Manifest Log)

Toàn bộ các tệp tin dưới đây đã được tải tự động và kiểm tra tính toàn vẹn thông qua mã băm SHA-256 (ghi nhận tại `data/raw/MANIFEST.md` và `data/raw/manifest.json`):

| Tệp tin lưu tại `data/raw/` | Nguồn dữ liệu | Dung lượng | Số dòng | Số cột | Giấy phép | Mã băm SHA-256 |
|---|---|---|---|---|---|---|
| `owid/natural-disasters-by-type.csv` | Our World in Data | 15.515 bytes (0.01 MB) | 605 | 3 | CC-BY 4.0 | `91fa90c4b8bdb4d9cbbc9d8768d765db6fe75802047321726b3440b188057860` |
| `owid/economic-damage-from-natural-disasters.csv` | Our World in Data | 36.081 bytes (0.03 MB) | 1.129 | 3 | CC-BY 4.0 | `973aa8553a7dc6a68092d98a8fc86e0fb03dd5f038119947dd960d4428f159de` |
| `nasa_firms/MODIS_C6_1_Global_7d.csv` | NASA FIRMS (Terra/Aqua) | 5.291.808 bytes (5.05 MB) | 68.312 | 13 | Public Domain | `cf3429fc60517d7efcdbae015358fa7a8f7d5b44040cebe9289c1bf4531ab24c` |
| `nasa_firms/SUOMI_VIIRS_C2_Global_7d.csv` | NASA FIRMS (Suomi NPP) | 31.423.731 bytes (29.97 MB) | 385.296 | 13 | Public Domain | `174fc1a4cecfab7ca11c403ce3010355b083449ed03a3a95abf1c3f132eb5798` |
| `noaa_ncei/StormEvents_details_2020.csv.gz` | NOAA NCEI Storm Events | 10.444.606 bytes (9.96 MB) | 61.281 | 51 | Public Domain | `895c56fd46991c4d9a135d67558dc4b447a02a2314efac0ace645135b98f9c9d` |
| `noaa_ncei/StormEvents_details_2023.csv.gz` | NOAA NCEI Storm Events | 12.888.092 bytes (12.29 MB) | 75.593 | 51 | Public Domain | `713784bed40d9e5a95b1d6240a654f865f3ef97703713105c7b35437270da134` |
| `usfs_fod/usfs_wildfires_sample.csv` | USDA Forest Service (FPA-FOD) | 104.658 bytes (0.1 MB) | 1.000 | 10 | Public Domain | `68e0b7306cd83da40d5bb39f0761732a249345ffcc797fd2eb2adcf60ea4f010` |

---

## 4. Hướng Dẫn Tải Dữ Liệu Thủ Công Bổ Trợ (EM-DAT)

Do cổng dữ liệu **EM-DAT** yêu cầu xác thực tài khoản học thuật và không hỗ trợ tải trực tiếp qua script không có API Key, người dùng có thể tải thủ công tệp bổ trợ theo các bước sau:

1. **Truy cập cổng dữ liệu**: [https://public.emdat.be/](https://public.emdat.be/)
2. **Đăng nhập**: Sử dụng tài khoản cá nhân / học thuật (đăng ký miễn phí).
3. **Thiết lập bộ lọc dữ liệu**:
   - Tab **Disaster Classification**: Chọn `Natural` (bao gồm `Wildfire`, `Flood`, `Storm`, `Drought`, `Earthquake`, `Extreme temperature`, `Volcanic activity`).
   - Tab **Period**: Chọn từ năm `2005` đến năm `2024`.
   - Tab **Geography**: Chọn `All Continents` / `All Countries`.
4. **Tải về**:
   - Nhấn **Download** $\to$ Chọn định dạng **CSV** (hoặc Excel `.xlsx`).
5. **Vị trí lưu trữ trong dự án**:
   - Đổi tên tệp thành `emdat_raw.csv`.
   - Di chuyển vào thư mục: `data/raw/emdat/emdat_raw.csv`.
   - Xem chi tiết tại [data/raw/emdat/README.md](file:///c:/Users/ASUS/Documents/Tương tác dữ liệu/đồ án ck/IDV_TTDL/data/raw/emdat/README.md).

---

## 5. Trích Dẫn Chuẩn Học Thuật (Citations)

1. **Our World in Data**:
   > Ritchie, H., Roser, M., & Rosado, P. (2024). *Natural Disasters*. Published online at OurWorldInData.org. Retrieved from: https://ourworldindata.org/natural-disasters [Online Resource].
2. **NASA FIRMS**:
   > NASA Land, Atmosphere Near real-time Capability for EOS (LANCE) / Fire Information for Resource Management System (FIRMS). *MODIS and VIIRS Active Fire Data*. NASA Goddard Space Flight Center. DOI: 10.5067/FIRMS/MODIS/MCD14DL.NRT.0061.
3. **NOAA NCEI Storm Events**:
   > National Oceanic and Atmospheric Administration (NOAA) National Centers for Environmental Information (NCEI). *Storm Events Database*. https://www.ncei.noaa.gov/stormevents/
4. **USDA Forest Service (FPA-FOD)**:
   > Short, Karen C. (2022). *Spatial wildfire occurrence data for the United States, 1992-2020 [FPA_FOD_20221014]*. 6th Edition. Fort Collins, CO: Forest Service Research Data Archive. https://doi.org/10.2737/RDS-2013-0009.6.
5. **EM-DAT**:
   > CRED / UCLouvain. (2024). *EM-DAT: The International Disaster Database*. Brussels, Belgium. https://www.emdat.be.
