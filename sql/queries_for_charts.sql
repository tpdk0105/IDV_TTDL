-- ==============================================================================
-- TỔNG HỢP CÁC TRUY VẤN SQL PHỤC VỤ 10 BIỂU ĐỒ TRỰC QUAN HÓA CHÁY RỪNG CALIFORNIA (2006 - 2025)
-- Tệp tin: sql/queries_for_charts.sql
-- Ghi chú: Mỗi biểu đồ là một khối truy vấn riêng có chú thích rõ người phụ trách và Dashboard
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- Chart #1 | Sheet_01_Combo_Trend (Dashboard D1 - TV1 phụ trách)
-- Dual-Axis Combo: Cột số vụ cháy + Đường tổng diện tích cháy (Acres) theo năm
-- ------------------------------------------------------------------------------
SELECT 
  d.year,
  COUNT(f.incident_id) AS total_fires,
  ROUND(SUM(f.acres_burned), 2) AS total_acres_burned,
  ROUND(SUM(f.burned_area_ha), 2) AS total_ha_burned,
  COALESCE(SUM(f.total_structures_destroyed), 0) AS total_structures_destroyed
FROM fact_fire_incident f
JOIN dim_date d ON f.date_id = d.date_id
GROUP BY d.year
ORDER BY d.year ASC;

-- ------------------------------------------------------------------------------
-- Chart #2 | Sheet_02_Stacked_Area (Dashboard D1 - TV1 phụ trách)
-- Stacked Area: Cơ cấu nguyên nhân cháy theo thời gian 2006–2025
-- ------------------------------------------------------------------------------
SELECT 
  d.year,
  c.cause_name,
  c.cause_group,
  COUNT(f.incident_id) AS fire_count
FROM fact_fire_incident f
JOIN dim_date d ON f.date_id = d.date_id
JOIN dim_cause c ON f.cause_id = c.cause_id
GROUP BY d.year, c.cause_name, c.cause_group
ORDER BY d.year ASC, fire_count DESC;

-- ------------------------------------------------------------------------------
-- Chart #3 | Sheet_03_Diverging_Bar (Dashboard D1 - TV2 phụ trách)
-- Diverging Bar: Biến động số vụ mỗi năm so với mức trung bình chuẩn 20 năm (Tâm = 0)
-- ------------------------------------------------------------------------------
WITH yearly_counts AS (
  SELECT 
    d.year,
    COUNT(f.incident_id) AS fire_count
  FROM fact_fire_incident f
  JOIN dim_date d ON f.date_id = d.date_id
  GROUP BY d.year
),
benchmark AS (
  SELECT AVG(fire_count) AS avg_20yr_fires FROM yearly_counts
)
SELECT 
  y.year,
  y.fire_count,
  ROUND(b.avg_20yr_fires, 2) AS benchmark_avg,
  ROUND(y.fire_count - b.avg_20yr_fires, 2) AS diff_from_20yr_avg,
  CASE 
    WHEN (y.fire_count - b.avg_20yr_fires) > 0 THEN 'Vượt trung bình (+)'
    ELSE 'Dưới trung bình (-)'
  END AS divergence_flag
FROM yearly_counts y
CROSS JOIN benchmark b
ORDER BY y.year ASC;

-- ------------------------------------------------------------------------------
-- Chart #4 | Sheet_04_Treemap_Damage (Dashboard D2 - TV2 phụ trách)
-- Treemap: Phân cấp tổn thất nhà cửa: Hạt → Loại công trình kiến trúc (Single Family, Commercial...)
-- ------------------------------------------------------------------------------
SELECT 
  cty.county_name,
  s.structure_type,
  SUM(s.structures_destroyed) AS destroyed_count,
  SUM(s.structures_damaged) AS damaged_count
FROM fact_structure_damage s
JOIN dim_county cty ON s.county_id = cty.county_id
GROUP BY cty.county_name, s.structure_type
HAVING destroyed_count > 0
ORDER BY destroyed_count DESC;

-- ------------------------------------------------------------------------------
-- Chart #5 | Sheet_05_Bubble_Scatter (Dashboard D3 - TV2 phụ trách)
-- Bubble Scatter Log-Log: Tương quan Diện tích cháy vs Số nhà phá hủy vs Thương vong
-- ------------------------------------------------------------------------------
SELECT 
  f.incident_id,
  f.fire_name,
  d.year,
  cty.county_name,
  c.cause_group,
  f.acres_burned,
  f.total_structures_destroyed,
  f.deaths_direct,
  f.injuries_direct
FROM fact_fire_incident f
JOIN dim_date d ON f.date_id = d.date_id
JOIN dim_county cty ON f.county_id = cty.county_id
JOIN dim_cause c ON f.cause_id = c.cause_id
WHERE f.acres_burned > 0 AND f.total_structures_destroyed >= 0
ORDER BY f.acres_burned DESC;

-- ------------------------------------------------------------------------------
-- Chart #6 | Sheet_06_Combo_Histogram (Dashboard D3 - TV2 phụ trách)
-- Combo Histogram: Phân phối diện tích cháy theo nhóm quy mô logarit + Số lượng
-- ------------------------------------------------------------------------------
SELECT 
  CASE 
    WHEN f.acres_burned < 300 THEN '< 300 Acres'
    WHEN f.acres_burned BETWEEN 300 AND 999.99 THEN '300 - 1.000 Acres'
    WHEN f.acres_burned BETWEEN 1000 AND 4999.99 THEN '1.000 - 5.000 Acres'
    WHEN f.acres_burned BETWEEN 5000 AND 24999.99 THEN '5.000 - 25.000 Acres'
    WHEN f.acres_burned BETWEEN 25000 AND 99999.99 THEN '25.000 - 100.000 Acres'
    ELSE '≥ 100.000 Acres (Siêu đám cháy)'
  END AS acres_bin,
  COUNT(f.incident_id) AS fire_count,
  ROUND(SUM(f.acres_burned), 2) AS total_acres_in_bin
FROM fact_fire_incident f
WHERE f.acres_burned IS NOT NULL AND f.acres_burned > 0
GROUP BY acres_bin
ORDER BY MIN(f.acres_burned) ASC;

-- ------------------------------------------------------------------------------
-- Chart #7 | Sheet_07_Combo_Pareto (Dashboard D2 - TV3 phụ trách)
-- Combo Pareto 80/20: Top 10 Hạt bị tàn phá nhà cửa nặng nhất + Đường % lũy kế
-- ------------------------------------------------------------------------------
WITH county_destroyed AS (
  SELECT 
    cty.county_name,
    SUM(f.total_structures_destroyed) AS total_destroyed
  FROM fact_fire_incident f
  JOIN dim_county cty ON f.county_id = cty.county_id
  GROUP BY cty.county_name
  HAVING total_destroyed > 0
  ORDER BY total_destroyed DESC
),
state_total AS (
  SELECT SUM(total_destroyed) AS grand_total FROM county_destroyed
)
SELECT 
  cd.county_name,
  cd.total_destroyed,
  ROUND(SUM(cd.total_destroyed) OVER (ORDER BY cd.total_destroyed DESC) * 100.0 / st.grand_total, 2) AS cumulative_pct
FROM county_destroyed cd
CROSS JOIN state_total st
ORDER BY cd.total_destroyed DESC
LIMIT 10;

-- ------------------------------------------------------------------------------
-- Chart #8 | Sheet_08_Donut_Cause (Dashboard D3 - TV3 phụ trách)
-- Donut 2 tầng: Cơ cấu nguyên nhân cháy Tự nhiên vs Con người → Từng tác nhân
-- ------------------------------------------------------------------------------
SELECT 
  c.cause_group,
  c.cause_name,
  COUNT(f.incident_id) AS fire_count,
  ROUND(SUM(f.acres_burned), 2) AS total_acres_burned,
  SUM(f.total_structures_destroyed) AS total_destroyed
FROM fact_fire_incident f
JOIN dim_cause c ON f.cause_id = c.cause_id
GROUP BY c.cause_group, c.cause_name
ORDER BY c.cause_group, fire_count DESC;

-- ------------------------------------------------------------------------------
-- Chart #9 | Sheet_09_Choropleth_Map (Dashboard D2 - TV3 phụ trách)
-- Bản đồ phân vùng bắt buộc: Mức độ thiệt hại và nhà cửa bị phá hủy theo 58 Hạt California
-- ------------------------------------------------------------------------------
SELECT 
  cty.county_fips,
  cty.county_name,
  cty.census_population,
  COUNT(f.incident_id) AS total_fires,
  ROUND(SUM(f.acres_burned), 2) AS total_acres_burned,
  SUM(f.total_structures_destroyed) AS total_structures_destroyed,
  SUM(f.deaths_direct) AS total_deaths
FROM dim_county cty
LEFT JOIN fact_fire_incident f ON cty.county_id = f.county_id
GROUP BY cty.county_fips, cty.county_name, cty.census_population
ORDER BY total_structures_destroyed DESC;

-- ------------------------------------------------------------------------------
-- Chart #10 | Sheet_10_Proportional_Map (Dashboard D3 - TV3 phụ trách)
-- Bản đồ điểm: Phân bố không gian các đại vụ cháy lớn California (Acres & Nhà cháy)
-- ------------------------------------------------------------------------------
SELECT 
  f.incident_id,
  f.fire_name,
  d.year,
  cty.county_name,
  f.latitude,
  f.longitude,
  f.acres_burned,
  f.total_structures_destroyed,
  c.cause_name
FROM fact_fire_incident f
JOIN dim_date d ON f.date_id = d.date_id
JOIN dim_county cty ON f.county_id = cty.county_id
JOIN dim_cause c ON f.cause_id = c.cause_id
WHERE f.latitude IS NOT NULL AND f.longitude IS NOT NULL
ORDER BY f.acres_burned DESC;

