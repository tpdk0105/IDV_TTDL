-- ==============================================================================
-- CSDL THẢM HỌA THIÊN NHIÊN & CHÁY RỪNG TOÀN CẦU (2005 - 2024)
-- Tệp tin DDL: sql/schema.sql
-- Người phụ trách: Thành viên 2 (Kỹ sư Mô hình Dữ liệu)
-- Trạng thái: Khung cấu trúc DDL hoàn chỉnh (Giai đoạn 1)
-- ==============================================================================

-- Bật hỗ trợ khóa ngoại trên SQLite
PRAGMA foreign_keys = ON;

-- ------------------------------------------------------------------------------
-- 1. BẢNG CHIỀU THỜI GIAN (dim_date)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_date (
  date_id INTEGER PRIMARY KEY,                      -- Surrogate Key: YYYYMMDD
  full_date TEXT NOT NULL UNIQUE,                   -- Định dạng ISO: YYYY-MM-DD
  year INTEGER NOT NULL CHECK (year BETWEEN 2005 AND 2024),
  quarter INTEGER NOT NULL CHECK (quarter BETWEEN 1 AND 4),
  month INTEGER NOT NULL CHECK (month BETWEEN 1 AND 12),
  month_name TEXT NOT NULL,                         -- Jan, Feb, ... Dec
  season TEXT NOT NULL,                             -- Spring, Summer, Autumn, Winter
  is_fire_season INTEGER NOT NULL DEFAULT 0 CHECK (is_fire_season IN (0, 1))
);

-- ------------------------------------------------------------------------------
-- 2. BẢNG CHIỀU VỊ TRÍ ĐỊA LÝ (dim_location)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_location (
  location_id INTEGER PRIMARY KEY AUTOINCREMENT,
  country_iso3 TEXT NOT NULL UNIQUE,                -- Chuẩn ISO 3166-1 alpha-3
  country_name TEXT NOT NULL,
  region TEXT,
  continent TEXT NOT NULL CHECK (continent IN ('Asia', 'Europe', 'Americas', 'Africa', 'Oceania')),
  subregion TEXT,
  default_latitude REAL CHECK (default_latitude BETWEEN -90.0 AND 90.0),
  default_longitude REAL CHECK (default_longitude BETWEEN -180.0 AND 180.0)
);

-- ------------------------------------------------------------------------------
-- 3. BẢNG CHIỀU PHÂN LOẠI THẢM HỌA (dim_disaster_type)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_disaster_type (
  type_id INTEGER PRIMARY KEY AUTOINCREMENT,
  type_name TEXT NOT NULL UNIQUE,                   -- Wildfire, Flood, Storm, etc.
  group_name TEXT,                                  -- Natural, Meteorological, etc.
  subtype_name TEXT                                 -- Forest fire, Land fire, etc.
);

-- ------------------------------------------------------------------------------
-- 4. BẢNG CHIỀU NGUYÊN NHÂN GÂY HỎA HOẠN / THẢM HỌA (dim_cause)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_cause (
  cause_id INTEGER PRIMARY KEY AUTOINCREMENT,
  cause_name TEXT NOT NULL UNIQUE,                  -- Lightning, Arson, Debris burning, etc.
  cause_group TEXT NOT NULL CHECK (cause_group IN ('Natural', 'Human', 'Unknown'))
);

-- ------------------------------------------------------------------------------
-- 5. BẢNG CHIỀU NGUỒN GỐC DỮ LIỆU (dim_source)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_source (
  source_id INTEGER PRIMARY KEY AUTOINCREMENT,
  source_name TEXT NOT NULL UNIQUE,                 -- EM-DAT, NASA FIRMS, USFS, etc.
  url TEXT,
  license TEXT
);

-- ------------------------------------------------------------------------------
-- 6. BẢNG SỰ KIỆN CHÍNH - FACT THẢM HỌA THIÊN NHIÊN (fact_disaster_event)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS fact_disaster_event (
  event_id INTEGER PRIMARY KEY AUTOINCREMENT,
  event_code TEXT NOT NULL UNIQUE,                  -- DIS-YYYY-XXXXX
  date_id INTEGER NOT NULL,
  location_id INTEGER NOT NULL,
  type_id INTEGER NOT NULL,
  cause_id INTEGER NOT NULL,
  source_id INTEGER NOT NULL,
  deaths INTEGER NOT NULL DEFAULT 0 CHECK (deaths >= 0),
  injured INTEGER NOT NULL DEFAULT 0 CHECK (injured >= 0),
  affected INTEGER NOT NULL DEFAULT 0 CHECK (affected >= 0),
  damage_usd REAL CHECK (damage_usd IS NULL OR damage_usd >= 0.0),
  latitude REAL CHECK (latitude IS NULL OR (latitude BETWEEN -90.0 AND 90.0)),
  longitude REAL CHECK (longitude IS NULL OR (longitude BETWEEN -180.0 AND 180.0)),
  is_outlier_ml INTEGER NOT NULL DEFAULT 0 CHECK (is_outlier_ml IN (0, 1)),
  outlier_score REAL,
  deaths_is_imputed INTEGER NOT NULL DEFAULT 0 CHECK (deaths_is_imputed IN (0, 1)),
  damage_usd_is_imputed INTEGER NOT NULL DEFAULT 0 CHECK (damage_usd_is_imputed IN (0, 1)),
  cause_is_predicted INTEGER NOT NULL DEFAULT 0 CHECK (cause_is_predicted IN (0, 1)),
  
  -- Ràng buộc khóa ngoại
  FOREIGN KEY (date_id) REFERENCES dim_date(date_id) ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (location_id) REFERENCES dim_location(location_id) ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (type_id) REFERENCES dim_disaster_type(type_id) ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (cause_id) REFERENCES dim_cause(cause_id) ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (source_id) REFERENCES dim_source(source_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ------------------------------------------------------------------------------
-- 7. BẢNG SỰ KIỆN CHI TIẾT CHUYÊN BIỆT CHÁY RỪNG (fact_wildfire_detail)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS fact_wildfire_detail (
  event_id INTEGER PRIMARY KEY,                     -- Vừa là PK vừa là FK tham chiếu 1-1 tới fact_disaster_event
  burned_area_ha REAL CHECK (burned_area_ha IS NULL OR burned_area_ha >= 0.0),
  burned_area_is_imputed INTEGER NOT NULL DEFAULT 0 CHECK (burned_area_is_imputed IN (0, 1)),
  duration_days REAL CHECK (duration_days IS NULL OR duration_days >= 0.0),
  fire_radiative_power REAL CHECK (fire_radiative_power IS NULL OR fire_radiative_power >= 0.0),
  severity_level TEXT CHECK (severity_level IS NULL OR severity_level IN ('Low', 'Moderate', 'High', 'Extreme')),
  
  FOREIGN KEY (event_id) REFERENCES fact_disaster_event(event_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ------------------------------------------------------------------------------
-- 8. TỐI ƯU HÓA CHỈ MỤC (INDEXES) PHỤC VỤ TRUY VẤN
-- ------------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_fact_date ON fact_disaster_event(date_id);
CREATE INDEX IF NOT EXISTS idx_fact_location ON fact_disaster_event(location_id);
CREATE INDEX IF NOT EXISTS idx_fact_type ON fact_disaster_event(type_id);
CREATE INDEX IF NOT EXISTS idx_fact_cause ON fact_disaster_event(cause_id);
CREATE INDEX IF NOT EXISTS idx_date_year ON dim_date(year);
CREATE INDEX IF NOT EXISTS idx_location_iso3 ON dim_location(country_iso3);
