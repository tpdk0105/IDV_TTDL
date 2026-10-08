-- ==============================================================================
-- CSDL CHÁY RỪNG BANG CALIFORNIA / BẮC MỸ (2006 - 2025)
-- Tệp tin DDL: sql/schema.sql
-- Người phụ trách: Thành viên 2 (Kỹ sư Mô hình Dữ liệu)
-- Trạng thái: Kiến trúc Star Schema chuẩn tối thiểu 3NF, liên kết 5 bảng
-- ==============================================================================

-- Bật hỗ trợ khóa ngoại trên SQLite
PRAGMA foreign_keys = ON;

-- ------------------------------------------------------------------------------
-- 1. BẢNG CHIỀU THỜI GIAN (dim_date)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_date (
  date_id INTEGER PRIMARY KEY,                      -- Surrogate Key: YYYYMMDD
  full_date TEXT NOT NULL UNIQUE,                   -- Định dạng ISO: YYYY-MM-DD
  year INTEGER NOT NULL CHECK (year BETWEEN 2006 AND 2025),
  quarter INTEGER NOT NULL CHECK (quarter BETWEEN 1 AND 4),
  month INTEGER NOT NULL CHECK (month BETWEEN 1 AND 12),
  month_name TEXT NOT NULL,                         -- Jan, Feb, ... Dec
  season TEXT NOT NULL,                             -- Spring, Summer, Autumn, Winter
  is_fire_season INTEGER NOT NULL DEFAULT 0 CHECK (is_fire_season IN (0, 1))
);

-- ------------------------------------------------------------------------------
-- 2. BẢNG CHIỀU 58 HẠT CALIFORNIA (dim_county)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_county (
  county_id INTEGER PRIMARY KEY AUTOINCREMENT,
  county_name TEXT NOT NULL UNIQUE,                 -- Tên chuẩn hóa 58 Hạt California
  county_fips TEXT,                                 -- Mã FIPS (vd: 06007 cho Butte)
  census_population INTEGER,                        -- Dân số theo Cục Điều tra Dân số Hoa Kỳ
  area_sqmi REAL CHECK (area_sqmi IS NULL OR area_sqmi > 0.0),
  cdt_abbr TEXT                                     -- Mã viết tắt CAL FIRE (BUT, SON, SHA...)
);

-- ------------------------------------------------------------------------------
-- 3. BẢNG CHIỀU NGUYÊN NHÂN CHÁY RỪNG (dim_cause)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dim_cause (
  cause_id INTEGER PRIMARY KEY AUTOINCREMENT,
  cause_code INTEGER,                               -- Mã CAL FIRE CAUSE (1-19)
  cause_name TEXT NOT NULL UNIQUE,                  -- Lightning, Equipment Use, Arson...
  cause_group TEXT NOT NULL CHECK (cause_group IN ('Natural', 'Human', 'Undetermined'))
);

-- ------------------------------------------------------------------------------
-- 4. BẢNG FACT TRUNG TÂM 1: CÁC VỤ CHÁY RỪNG (fact_fire_incident)
-- Lưu vết 7.342 vụ cháy rừng lịch sử California (2006–2025) từ CAL FIRE FRAP
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS fact_fire_incident (
  incident_id INTEGER PRIMARY KEY AUTOINCREMENT,
  fire_name TEXT NOT NULL,                          -- Tên chuẩn hóa (CAMP, TUBBS, AUGUST COMPLEX...)
  frap_fire_num TEXT,                               -- Số hiệu hồ sơ CAL FIRE FRAP
  date_id INTEGER NOT NULL,
  county_id INTEGER NOT NULL,
  cause_id INTEGER NOT NULL,
  acres_burned REAL CHECK (acres_burned IS NULL OR acres_burned >= 0.0),
  burned_area_ha REAL CHECK (burned_area_ha IS NULL OR burned_area_ha >= 0.0),
  duration_days REAL CHECK (duration_days IS NULL OR duration_days >= 0.0),
  latitude REAL CHECK (latitude IS NULL OR (latitude BETWEEN 32.0 AND 42.0)),
  longitude REAL CHECK (longitude IS NULL OR (longitude BETWEEN -125.0 AND -114.0)),
  total_structures_destroyed INTEGER DEFAULT 0 CHECK (total_structures_destroyed >= 0),
  total_structures_damaged INTEGER DEFAULT 0 CHECK (total_structures_damaged >= 0),
  deaths_direct INTEGER DEFAULT 0 CHECK (deaths_direct >= 0),
  injuries_direct INTEGER DEFAULT 0 CHECK (injuries_direct >= 0),
  is_outlier_ml INTEGER NOT NULL DEFAULT 0 CHECK (is_outlier_ml IN (0, 1)),
  outlier_score REAL,
  burned_area_is_imputed INTEGER NOT NULL DEFAULT 0 CHECK (burned_area_is_imputed IN (0, 1)),
  cause_is_predicted INTEGER NOT NULL DEFAULT 0 CHECK (cause_is_predicted IN (0, 1)),

  -- Ràng buộc khóa ngoại
  FOREIGN KEY (date_id) REFERENCES dim_date(date_id) ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (county_id) REFERENCES dim_county(county_id) ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (cause_id) REFERENCES dim_cause(cause_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ------------------------------------------------------------------------------
-- 5. BẢNG FACT MỞ RỘNG 2: THIỆT HẠI CÔNG TRÌNH KIỂM KÊ (fact_structure_damage)
-- Hợp nhất liên tục 20 năm: ICS-209 (2006–2012) + CAL FIRE DINS (2013–2025)
-- ------------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS fact_structure_damage (
  record_id INTEGER PRIMARY KEY AUTOINCREMENT,
  global_id TEXT,                                   -- DINS GlobalID hoặc ICS Incident ID
  incident_id INTEGER NOT NULL,
  county_id INTEGER NOT NULL,
  damage_source TEXT NOT NULL,                      -- 'CAL_FIRE_DINS', 'USDA_ICS_209'
  structure_type TEXT NOT NULL,                     -- Single Family, Commercial, Outbuilding...
  damage_category TEXT,                             -- Destroyed (>50%), Major, Minor, Affected
  structures_destroyed INTEGER DEFAULT 0 CHECK (structures_destroyed >= 0),
  structures_damaged INTEGER DEFAULT 0 CHECK (structures_damaged >= 0),
  latitude REAL CHECK (latitude IS NULL OR (latitude BETWEEN 32.0 AND 42.0)),
  longitude REAL CHECK (longitude IS NULL OR (longitude BETWEEN -125.0 AND -114.0)),

  -- Ràng buộc khóa ngoại
  FOREIGN KEY (incident_id) REFERENCES fact_fire_incident(incident_id) ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (county_id) REFERENCES dim_county(county_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ------------------------------------------------------------------------------
-- 6. TỐI ƯU HÓA CHỈ MỤC (INDEXES) PHỤC VỤ TRUY VẤN
-- ------------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_fire_date ON fact_fire_incident(date_id);
CREATE INDEX IF NOT EXISTS idx_fire_county ON fact_fire_incident(county_id);
CREATE INDEX IF NOT EXISTS idx_fire_cause ON fact_fire_incident(cause_id);
CREATE INDEX IF NOT EXISTS idx_fire_name ON fact_fire_incident(fire_name);
CREATE INDEX IF NOT EXISTS idx_damage_incident ON fact_structure_damage(incident_id);
CREATE INDEX IF NOT EXISTS idx_damage_county ON fact_structure_damage(county_id);
CREATE INDEX IF NOT EXISTS idx_date_year ON dim_date(year);
CREATE INDEX IF NOT EXISTS idx_county_name ON dim_county(county_name);
