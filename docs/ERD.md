# Sơ Đồ Quan Hệ Thực Thể (ENTITY RELATIONSHIP DIAGRAM - ERD)

> **Người phụ trách**: Thành viên 2 - Kỹ sư Mô hình Dữ liệu (Data Modeling Engineer)  
> **Trạng thái**: Thiết kế Star Schema (Giai đoạn 1)

---

## 1. Thiết Kế Mô Hình Dạng Sao (Star Schema Architecture)
Mô hình dữ liệu được thiết kế nhằm phục vụ truy vấn phân tích đa chiều (OLAP) và trực quan hóa hiệu năng cao cho 12 biểu đồ tương tác:
- **Bảng Fact Trung Tâm**: `fact_disaster_event` (lưu vết toàn bộ sự kiện thảm họa thiên nhiên 2005–2024).
- **Bảng Fact Mở Rộng**: `fact_wildfire_detail` (chi tiết hóa các chỉ số kỹ thuật chuyên biệt cho cháy rừng: diện tích, công suất bức xạ FRP, thời gian kéo dài).
- **Các Bảng Dimension**: `dim_date`, `dim_location`, `dim_disaster_type`, `dim_cause`, `dim_source`.
- **Cột cờ kiểm soát chất lượng**: Các cờ ML (`is_outlier_ml`, `deaths_is_imputed`, `damage_usd_is_imputed`, `cause_is_predicted`) được bảo toàn trực tiếp trong bảng fact để hỗ trợ tính năng lọc dữ liệu gốc/ước lượng trên Dashboard.

---

## 2. Sơ Đồ Mermaid ERD

```mermaid
erDiagram
    dim_date ||--o{ fact_disaster_event : "occurs_on"
    dim_location ||--o{ fact_disaster_event : "located_at"
    dim_disaster_type ||--o{ fact_disaster_event : "classified_as"
    dim_cause ||--o{ fact_disaster_event : "caused_by"
    dim_source ||--o{ fact_disaster_event : "recorded_by"
    fact_disaster_event ||--o| fact_wildfire_detail : "detailed_in"

    dim_date {
        integer date_id PK "Surrogate Key (YYYYMMDD)"
        date full_date "NOT NULL, UNIQUE"
        integer year "CHECK (year BETWEEN 2005 AND 2024)"
        integer quarter "CHECK (quarter BETWEEN 1 AND 4)"
        integer month "CHECK (month BETWEEN 1 AND 12)"
        text month_name "Jan, Feb, ... Dec"
        text season "Spring, Summer, Autumn, Winter"
        integer is_fire_season "CHECK (is_fire_season IN (0, 1))"
    }

    dim_location {
        integer location_id PK "Surrogate Key Auto-inc"
        text country_iso3 "NOT NULL, UNIQUE (ISO 3166-1 alpha-3)"
        text country_name "NOT NULL"
        text region "Sub-national region / state"
        text continent "NOT NULL (Asia, Europe, Americas, Africa, Oceania)"
        text subregion "UN Subregion"
        real default_latitude "CHECK (default_latitude BETWEEN -90 AND 90)"
        real default_longitude "CHECK (default_longitude BETWEEN -180 AND 180)"
    }

    dim_disaster_type {
        integer type_id PK "Surrogate Key Auto-inc"
        text type_name "NOT NULL, UNIQUE (Wildfire, Flood, Storm...)"
        text group_name "Natural, Meteorological, Hydrological..."
        text subtype_name "Forest fire, Land fire, Riverine flood..."
    }

    dim_cause {
        integer cause_id PK "Surrogate Key Auto-inc"
        text cause_name "NOT NULL, UNIQUE (Lightning, Arson, Debris...)"
        text cause_group "NOT NULL (Natural, Human, Unknown)"
    }

    dim_source {
        integer source_id PK "Surrogate Key Auto-inc"
        text source_name "NOT NULL, UNIQUE (EM-DAT, NASA FIRMS, USFS...)"
        text url "Official data portal URL"
        text license "CC-BY, Public Domain, etc."
    }

    fact_disaster_event {
        integer event_id PK "Surrogate Key Auto-inc"
        text event_code "NOT NULL, UNIQUE (DIS-YYYY-XXXXX)"
        integer date_id FK "REFERENCES dim_date(date_id)"
        integer location_id FK "REFERENCES dim_location(location_id)"
        integer type_id FK "REFERENCES dim_disaster_type(type_id)"
        integer cause_id FK "REFERENCES dim_cause(cause_id)"
        integer source_id FK "REFERENCES dim_source(source_id)"
        integer deaths "DEFAULT 0, CHECK (deaths >= 0)"
        integer injured "DEFAULT 0, CHECK (injured >= 0)"
        integer affected "DEFAULT 0, CHECK (affected >= 0)"
        real damage_usd "CHECK (damage_usd >= 0.0)"
        real latitude "CHECK (latitude BETWEEN -90 AND 90)"
        real longitude "CHECK (longitude BETWEEN -180 AND 180)"
        integer is_outlier_ml "DEFAULT 0, CHECK (is_outlier_ml IN (0, 1))"
        real outlier_score "Anomaly score from Isolation Forest"
        integer deaths_is_imputed "DEFAULT 0, CHECK (deaths_is_imputed IN (0, 1))"
        integer damage_usd_is_imputed "DEFAULT 0, CHECK (damage_usd_is_imputed IN (0, 1))"
        integer cause_is_predicted "DEFAULT 0, CHECK (cause_is_predicted IN (0, 1))"
    }

    fact_wildfire_detail {
        integer event_id PK, FK "REFERENCES fact_disaster_event(event_id)"
        real burned_area_ha "CHECK (burned_area_ha >= 0.0)"
        integer burned_area_is_imputed "DEFAULT 0, CHECK (burned_area_is_imputed IN (0, 1))"
        real duration_days "CHECK (duration_days >= 0.0)"
        real fire_radiative_power "FRP in MW (from satellite)"
        text severity_level "Low, Moderate, High, Extreme"
    }
```

---

## 3. Quy Tắc Toàn Vẹn Tham Chiếu & Ràng Buộc
1. **Khóa ngoại (Foreign Keys)**: Bật `PRAGMA foreign_keys = ON;`. Mọi quan hệ đều cấu hình `ON DELETE RESTRICT ON UPDATE CASCADE`.
2. **Cam kết không có khóa mồ côi (Zero Orphaned FKs)**: Bảng fact chỉ được tham chiếu đến các ID đã tồn tại trong các bảng dimension.
3. **Ràng buộc kiểm tra (CHECK constraints)**: Đảm bảo miền giá trị vật lý và logic nghiệp vụ được bảo vệ ở tầng cơ sở dữ liệu.
4. **Chỉ mục tăng tốc (Indexes)**: Đánh index trên toàn bộ các cột FK và các trường thường xuyên `GROUP BY` / `WHERE` (ví dụ: `year`, `country_iso3`, `type_name`, `cause_group`).
