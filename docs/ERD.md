# Sơ Đồ Quan Hệ Thực Thể (ENTITY RELATIONSHIP DIAGRAM - ERD)

> **Người phụ trách**: Thành viên 2 - Kỹ sư Mô hình Dữ liệu (Data Modeling Engineer)  
> **Phạm vi dữ liệu**: Cháy rừng Bang California / Bắc Mỹ giai đoạn 2006–2025  
> **Trạng thái**: Thiết kế Star Schema đạt chuẩn tối thiểu 3NF, liên kết $\ge 3$ bảng

---

## 1. Thiết Kế Mô Hình Dạng Sao (Star Schema Architecture)
Mô hình dữ liệu được thiết kế nhằm phục vụ truy vấn phân tích đa chiều (OLAP) và trực quan hóa hiệu năng cao cho 10 biểu đồ tương tác, liên kết chặt chẽ giữa các vụ cháy rừng và các công trình bị tàn phá:
- **Bảng Fact Trung Tâm 1**: `fact_fire_incident` (lưu vết **7.342 vụ cháy rừng lịch sử California 2006–2025** từ CAL FIRE FRAP: diện tích Acres/ha, thời gian kéo dài, tọa độ, nguyên nhân, số nhà bị phá hủy liên tục 20 năm, thương vong NOAA).
- **Bảng Fact Mở Rộng 2**: `fact_structure_damage` (lưu vết chi tiết hơn 133.000 bản ghi kiểm kê công trình nhà ở, thương mại bị thiêu hại được **hợp nhất liên tục 20 năm: Giai đoạn 2006–2012 từ USDA Forest Service ICS-209 và Giai đoạn 2013–2025 từ CAL FIRE DINS**, liên kết $N - 1$ với `fact_fire_incident` qua `incident_id`).
- **Bảng Fact Thương Vong 3** (chỉ CSV, chưa nạp vào SQLite): `fact_casualty_event` (897 vụ cháy theo NOAA, đã gộp trùng vùng dự báo: 207 người chết, 792 người bị thương trực tiếp 2006–2025), liên kết `dim_date` qua `date_id` và `fact_fire_incident` qua `incident_id` (NULL nếu không khớp). Tổng hợp theo năm ở `data/clean/casualties_by_year.csv`.
- **Các Bảng Dimension**: `dim_county` (58 Hạt California kèm dân số, diện tích), `dim_cause` (bảng mã nguyên nhân CAL FIRE), `dim_date` (thứ bậc thời gian: ngày, tháng, quý, năm, mùa cao điểm cháy rừng).
- **Cột cờ kiểm soát chất lượng**: Các cờ ML (`is_outlier_ml`, `burned_area_is_imputed`, `cause_is_predicted`) được bảo toàn trực tiếp trong bảng fact để hỗ trợ tính năng lọc dữ liệu gốc/ước lượng trên Dashboard.

---

## 2. Sơ Đồ Mermaid ERD

```mermaid
erDiagram
    dim_date ||--o{ fact_fire_incident : "occurs_on"
    dim_county ||--o{ fact_fire_incident : "located_in"
    dim_cause ||--o{ fact_fire_incident : "triggered_by"
    fact_fire_incident ||--o{ fact_structure_damage : "damages"
    dim_county ||--o{ fact_structure_damage : "located_in"

    dim_date {
        integer date_id PK "Surrogate Key (YYYYMMDD)"
        date full_date "NOT NULL, UNIQUE"
        integer year "CHECK (year BETWEEN 2006 AND 2025)"
        integer quarter "CHECK (quarter BETWEEN 1 AND 4)"
        integer month "CHECK (month BETWEEN 1 AND 12)"
        text month_name "Jan, Feb, ... Dec"
        text season "Spring, Summer, Autumn, Winter"
        integer is_fire_season "CHECK (is_fire_season IN (0, 1))"
    }

    dim_county {
        integer county_id PK "Surrogate Key Auto-inc"
        text county_name "NOT NULL, UNIQUE (58 Hạt California)"
        text county_fips "Mã FIPS (vd: 06007 cho Butte)"
        integer census_population "Dân số theo Cục Điều tra Dân số"
        real area_sqmi "CHECK (area_sqmi > 0.0)"
        text cdt_abbr "Mã viết tắt Hạt (ALA, BUT, SON...)"
    }

    dim_cause {
        integer cause_id PK "Surrogate Key Auto-inc"
        integer cause_code "Mã CAL FIRE CAUSE (1-19)"
        text cause_name "NOT NULL, UNIQUE (Lightning, Equipment Use, Arson...)"
        text cause_group "NOT NULL (Natural, Human, Undetermined)"
    }

    fact_fire_incident {
        integer incident_id PK "Surrogate Key Auto-inc"
        text fire_name "NOT NULL (Tên chuẩn hóa: CAMP, AUGUST COMPLEX...)"
        text frap_fire_num "Mã số định danh vụ cháy gốc FRAP"
        integer date_id FK "REFERENCES dim_date(date_id)"
        integer county_id FK "REFERENCES dim_county(county_id)"
        integer cause_id FK "REFERENCES dim_cause(cause_id)"
        real acres_burned "CHECK (acres_burned >= 0.0)"
        real burned_area_ha "CHECK (burned_area_ha >= 0.0)"
        real duration_days "CHECK (duration_days >= 0.0)"
        real latitude "CHECK (latitude BETWEEN 32.0 AND 42.0)"
        real longitude "CHECK (longitude BETWEEN -125.0 AND -114.0)"
        integer total_structures_destroyed "Tổng số nhà bị phá hủy >50%"
        integer total_structures_damaged "Tổng số nhà bị hư hại"
        integer deaths_direct "Thương vong sinh mạng (NOAA)"
        integer injuries_direct "Số người bị thương (NOAA)"
        integer is_outlier_ml "DEFAULT 0, CHECK (is_outlier_ml IN (0, 1))"
        real outlier_score "Anomaly score from Isolation Forest"
        integer burned_area_is_imputed "DEFAULT 0, CHECK (burned_area_is_imputed IN (0, 1))"
        integer cause_is_predicted "DEFAULT 0, CHECK (cause_is_predicted IN (0, 1))"
    }

    fact_structure_damage {
        integer record_id PK "Surrogate Key Auto-inc"
        text global_id "Mã định danh DINS GlobalID / ICS Incident ID"
        integer incident_id FK "REFERENCES fact_fire_incident(incident_id)"
        integer county_id FK "REFERENCES dim_county(county_id)"
        text damage_source "CAL_FIRE_DINS, USDA_ICS_209"
        text structure_type "Single Family, Commercial, Outbuilding, Unspecified"
        text damage_category "Destroyed (>50%), Major, Minor, Affected"
        integer structures_destroyed "Số lượng công trình bị phá hủy"
        integer structures_damaged "Số lượng công trình bị hư hại"
        real latitude "CHECK (latitude BETWEEN 32.0 AND 42.0)"
        real longitude "CHECK (longitude BETWEEN -125.0 AND -114.0)"
    }
```

---

## 3. Quy Tắc Toàn Vẹn Tham Chiếu & Ràng Buộc
1. **Khóa ngoại (Foreign Keys)**: Bật `PRAGMA foreign_keys = ON;`. Mọi quan hệ đều cấu hình `ON DELETE RESTRICT ON UPDATE CASCADE`.
2. **Cam kết không có khóa mồ côi (Zero Orphaned FKs)**: Bảng fact chỉ được tham chiếu đến các ID đã tồn tại trong các bảng dimension.
3. **Ràng buộc kiểm tra (CHECK constraints)**: Đảm bảo miền giá trị địa lý California (`latitude BETWEEN 32.0 AND 42.0`, `longitude BETWEEN -125.0 AND -114.0`) và logic nghiệp vụ được bảo vệ ở tầng cơ sở dữ liệu.
4. **Chỉ mục tăng tốc (Indexes)**: Đánh index trên toàn bộ các cột FK và các trường thường xuyên `GROUP BY` / `WHERE` (ví dụ: `year`, `county_id`, `cause_id`, `fire_name`).
