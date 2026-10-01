# BẢN ĐĂNG KÝ TẬP TIN DỮ LIỆU THÔ (RAW DATA MANIFEST)

> Tài liệu ghi nhận mã băm toàn vẹn SHA-256, dung lượng, số dòng và giấy phép của từng tệp tin thô trong `data/raw/`.

| Tệp tin | Nguồn | Dung lượng | Số dòng | Số cột | Giấy phép | SHA-256 |
|---------|-------|------------|---------|--------|-----------|---------|
| `nasa_firms/MODIS_C6_1_Global_7d.csv` | NASA FIRMS (Earthdata) | 5.05 MB | 68,312 | 13 | NASA Open Data Policy (Public Domain) | `cf3429fc60517d7e...` |
| `nasa_firms/SUOMI_VIIRS_C2_Global_7d.csv` | NASA FIRMS (Earthdata) | 29.97 MB | 385,296 | 13 | NASA Open Data Policy (Public Domain) | `174fc1a4cecfab7c...` |
| `noaa_ncei/StormEvents_details_2020.csv.gz` | NOAA NCEI Storm Events Database | 9.96 MB | 61,281 | 51 | U.S. Federal Government (Public Domain) | `895c56fd46991c4d...` |
| `noaa_ncei/StormEvents_details_2023.csv.gz` | NOAA NCEI Storm Events Database | 12.29 MB | 75,593 | 51 | U.S. Federal Government (Public Domain) | `713784bed40d9e5a...` |
| `owid/economic-damage-from-natural-disasters.csv` | Our World in Data (OWID) | 0.03 MB | 1,129 | 3 | Creative Commons Attribution (CC-BY 4.0) | `973aa8553a7dc6a6...` |
| `owid/natural-disasters-by-type.csv` | Our World in Data (OWID) | 0.01 MB | 605 | 3 | Creative Commons Attribution (CC-BY 4.0) | `91fa90c4b8bdb4d9...` |
| `usfs_fod/usfs_wildfires_sample.csv` | USDA Forest Service (FPA-FOD 6th Edition) | 0.1 MB | 1,000 | 10 | U.S. Federal Government (Public Domain) | `68e0b7306cd83da4...` |


## Chi Tiết Các Cột Trong Từng Tệp Tin

### `nasa_firms/MODIS_C6_1_Global_7d.csv` (NASA FIRMS (Earthdata))
- **URL chính thức**: https://firms.modaps.eosdis.nasa.gov/
- **Dung lượng**: 5,291,808 bytes (5.05 MB)
- **Mã SHA-256**: `cf3429fc60517d7efcdbae015358fa7a8f7d5b44040cebe9289c1bf4531ab24c`
- **Số cột**: 13
- **Danh sách cột**: `latitude`, `longitude`, `brightness`, `scan`, `track`, `acq_date`, `acq_time`, `satellite`, `confidence`, `version`, `bright_t31`, `frp`, `daynight`

### `nasa_firms/SUOMI_VIIRS_C2_Global_7d.csv` (NASA FIRMS (Earthdata))
- **URL chính thức**: https://firms.modaps.eosdis.nasa.gov/
- **Dung lượng**: 31,423,731 bytes (29.97 MB)
- **Mã SHA-256**: `174fc1a4cecfab7ca11c403ce3010355b083449ed03a3a95abf1c3f132eb5798`
- **Số cột**: 13
- **Danh sách cột**: `latitude`, `longitude`, `bright_ti4`, `scan`, `track`, `acq_date`, `acq_time`, `satellite`, `confidence`, `version`, `bright_ti5`, `frp`, `daynight`

### `noaa_ncei/StormEvents_details_2020.csv.gz` (NOAA NCEI Storm Events Database)
- **URL chính thức**: https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/
- **Dung lượng**: 10,444,606 bytes (9.96 MB)
- **Mã SHA-256**: `895c56fd46991c4d9a135d67558dc4b447a02a2314efac0ace645135b98f9c9d`
- **Số cột**: 51
- **Danh sách cột**: `BEGIN_YEARMONTH`, `BEGIN_DAY`, `BEGIN_TIME`, `END_YEARMONTH`, `END_DAY`, `END_TIME`, `EPISODE_ID`, `EVENT_ID`, `STATE`, `STATE_FIPS`, `YEAR`, `MONTH_NAME`, `EVENT_TYPE`, `CZ_TYPE`, `CZ_FIPS`, `CZ_NAME`, `WFO`, `BEGIN_DATE_TIME`, `CZ_TIMEZONE`, `END_DATE_TIME` ... (tổng cộng 51 cột)

### `noaa_ncei/StormEvents_details_2023.csv.gz` (NOAA NCEI Storm Events Database)
- **URL chính thức**: https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/
- **Dung lượng**: 12,888,092 bytes (12.29 MB)
- **Mã SHA-256**: `713784bed40d9e5a95b1d6240a654f865f3ef97703713105c7b35437270da134`
- **Số cột**: 51
- **Danh sách cột**: `BEGIN_YEARMONTH`, `BEGIN_DAY`, `BEGIN_TIME`, `END_YEARMONTH`, `END_DAY`, `END_TIME`, `EPISODE_ID`, `EVENT_ID`, `STATE`, `STATE_FIPS`, `YEAR`, `MONTH_NAME`, `EVENT_TYPE`, `CZ_TYPE`, `CZ_FIPS`, `CZ_NAME`, `WFO`, `BEGIN_DATE_TIME`, `CZ_TIMEZONE`, `END_DATE_TIME` ... (tổng cộng 51 cột)

### `owid/economic-damage-from-natural-disasters.csv` (Our World in Data (OWID))
- **URL chính thức**: https://ourworldindata.org/natural-disasters
- **Dung lượng**: 36,081 bytes (0.03 MB)
- **Mã SHA-256**: `973aa8553a7dc6a68092d98a8fc86e0fb03dd5f038119947dd960d4428f159de`
- **Số cột**: 3
- **Danh sách cột**: `Entity`, `Year`, `Total economic damages`

### `owid/natural-disasters-by-type.csv` (Our World in Data (OWID))
- **URL chính thức**: https://ourworldindata.org/natural-disasters
- **Dung lượng**: 15,515 bytes (0.01 MB)
- **Mã SHA-256**: `91fa90c4b8bdb4d9cbbc9d8768d765db6fe75802047321726b3440b188057860`
- **Số cột**: 3
- **Danh sách cột**: `Entity`, `Year`, `Disasters`

### `usfs_fod/usfs_wildfires_sample.csv` (USDA Forest Service (FPA-FOD 6th Edition))
- **URL chính thức**: https://apps.fs.usda.gov/arcx/rest/services/EDW/EDW_FireOccurrence6thEdition_01/MapServer/29
- **Dung lượng**: 104,658 bytes (0.1 MB)
- **Mã SHA-256**: `68e0b7306cd83da40d5bb39f0761732a249345ffcc797fd2eb2adcf60ea4f010`
- **Số cột**: 10
- **Danh sách cột**: `fod_id`, `fire_name`, `fire_year`, `discovery_date`, `nwcg_cause_classification`, `nwcg_general_cause`, `fire_size`, `latitude`, `longitude`, `state`

