-- ==============================================================================
-- TỔNG HỢP CÁC TRUY VẤN SQL PHỤC VỤ 12 BIỂU ĐỒ TRỰC QUAN HÓA
-- Tệp tin: sql/queries_for_charts.sql
-- Ghi chú: Mỗi biểu đồ là một khối truy vấn riêng có chú thích rõ người phụ trách
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- Chart #1 | Thành viên 1: Combo cột số vụ + đường thiệt hại USD theo năm (trục kép)
-- ------------------------------------------------------------------------------
SELECT 
  d.year,
  COUNT(f.event_id) AS total_events,
  COALESCE(SUM(f.damage_usd) / 1e9, 0.0) AS total_damage_billion_usd
FROM fact_disaster_event f
JOIN dim_date d ON f.date_id = d.date_id
GROUP BY d.year
ORDER BY d.year ASC;

-- ------------------------------------------------------------------------------
-- Chart #2 | Thành viên 1: Stacked area tần suất theo loại thảm họa theo năm
-- ------------------------------------------------------------------------------
SELECT 
  d.year,
  t.type_name,
  COUNT(f.event_id) AS event_count
FROM fact_disaster_event f
JOIN dim_date d ON f.date_id = d.date_id
JOIN dim_disaster_type t ON f.type_id = t.type_id
GROUP BY d.year, t.type_name
ORDER BY d.year ASC, t.type_name ASC;

-- ------------------------------------------------------------------------------
-- Chart #3 | Thành viên 1: Choropleth thế giới (Thiệt hại hoặc số vụ theo quốc gia)
-- ------------------------------------------------------------------------------
SELECT 
  l.country_iso3,
  l.country_name,
  COUNT(f.event_id) AS total_events,
  COALESCE(SUM(f.damage_usd) / 1e6, 0.0) AS total_damage_million_usd,
  COALESCE(SUM(f.deaths), 0) AS total_deaths
FROM fact_disaster_event f
JOIN dim_location l ON f.location_id = l.location_id
GROUP BY l.country_iso3, l.country_name
ORDER BY total_damage_million_usd DESC;

-- ------------------------------------------------------------------------------
-- Chart #4 | Thành viên 1: Heatmap tháng × năm số vụ cháy (Mùa cháy)
-- ------------------------------------------------------------------------------
SELECT 
  d.year,
  d.month,
  COUNT(f.event_id) AS wildfire_count
FROM fact_disaster_event f
JOIN dim_date d ON f.date_id = d.date_id
JOIN dim_disaster_type t ON f.type_id = t.type_id
WHERE t.type_name = 'Wildfire'
GROUP BY d.year, d.month
ORDER BY d.year ASC, d.month ASC;

-- ------------------------------------------------------------------------------
-- Chart #5 | Thành viên 2: Diverging bar (Chênh lệch số vụ mỗi năm so với TB 20 năm)
-- ------------------------------------------------------------------------------
WITH yearly_counts AS (
  SELECT 
    d.year,
    COUNT(f.event_id) AS event_count
  FROM fact_disaster_event f
  JOIN dim_date d ON f.date_id = d.date_id
  GROUP BY d.year
),
benchmark AS (
  SELECT AVG(event_count) AS avg_20yr_events FROM yearly_counts
)
SELECT 
  y.year,
  y.event_count,
  ROUND(b.avg_20yr_events, 2) AS benchmark_avg,
  ROUND(y.event_count - b.avg_20yr_events, 2) AS difference_from_avg
FROM yearly_counts y
CROSS JOIN benchmark b
ORDER BY y.year ASC;

-- ------------------------------------------------------------------------------
-- Chart #6 | Thành viên 2: Treemap thiệt hại phân cấp (Châu lục → Quốc gia)
-- ------------------------------------------------------------------------------
SELECT 
  l.continent,
  l.country_name,
  l.country_iso3,
  COALESCE(SUM(f.damage_usd) / 1e6, 0.0) AS total_damage_million_usd
FROM fact_disaster_event f
JOIN dim_location l ON f.location_id = l.location_id
GROUP BY l.continent, l.country_name, l.country_iso3
HAVING total_damage_million_usd > 0
ORDER BY l.continent, total_damage_million_usd DESC;

-- ------------------------------------------------------------------------------
-- Chart #7 | Thành viên 2: Bubble scatter (Diện tích cháy vs Thiệt hại, Log-Log)
-- ------------------------------------------------------------------------------
SELECT 
  f.event_code,
  w.burned_area_ha,
  f.damage_usd,
  f.affected,
  l.continent,
  l.country_name
FROM fact_disaster_event f
JOIN fact_wildfire_detail w ON f.event_id = w.event_id
JOIN dim_location l ON f.location_id = l.location_id
WHERE w.burned_area_ha > 0 AND f.damage_usd > 0;

-- ------------------------------------------------------------------------------
-- Chart #8 | Thành viên 2: Combo histogram diện tích cháy + Đường mật độ/Lũy kế
-- ------------------------------------------------------------------------------
SELECT 
  CASE 
    WHEN w.burned_area_ha < 100 THEN '< 100 ha'
    WHEN w.burned_area_ha BETWEEN 100 AND 999.99 THEN '100 - 1.000 ha'
    WHEN w.burned_area_ha BETWEEN 1000 AND 9999.99 THEN '1.000 - 10.000 ha'
    WHEN w.burned_area_ha BETWEEN 10000 AND 49999.99 THEN '10.000 - 50.000 ha'
    ELSE '>= 50.000 ha (Mega-fire)'
  END AS area_bin,
  COUNT(w.event_id) AS fire_count
FROM fact_wildfire_detail w
WHERE w.burned_area_ha IS NOT NULL AND w.burned_area_ha > 0
GROUP BY area_bin;

-- ------------------------------------------------------------------------------
-- Chart #9 | Thành viên 3: Combo Pareto Top 10 quốc gia tử vong + % Lũy kế
-- ------------------------------------------------------------------------------
WITH ranked_deaths AS (
  SELECT 
    l.country_name,
    SUM(f.deaths) AS total_deaths
  FROM fact_disaster_event f
  JOIN dim_location l ON f.location_id = l.location_id
  GROUP BY l.country_name
  ORDER BY total_deaths DESC
  LIMIT 10
),
total_top AS (
  SELECT SUM(total_deaths) AS grand_total FROM ranked_deaths
)
SELECT 
  r.country_name,
  r.total_deaths,
  ROUND(SUM(r.total_deaths) OVER (ORDER BY r.total_deaths DESC) * 100.0 / t.grand_total, 2) AS cumulative_pct
FROM ranked_deaths r
CROSS JOIN total_top t
ORDER BY r.total_deaths DESC;

-- ------------------------------------------------------------------------------
-- Chart #10 | Thành viên 3: Sunburst nguyên nhân cháy (Tự nhiên / Con người / Không rõ)
-- ------------------------------------------------------------------------------
SELECT 
  c.cause_group,
  c.cause_name,
  COUNT(f.event_id) AS event_count
FROM fact_disaster_event f
JOIN dim_cause c ON f.cause_id = c.cause_id
JOIN dim_disaster_type t ON f.type_id = t.type_id
WHERE t.type_name = 'Wildfire'
GROUP BY c.cause_group, c.cause_name
ORDER BY c.cause_group, event_count DESC;

-- ------------------------------------------------------------------------------
-- Chart #11 | Thành viên 3: Sankey (Nguyên nhân → Loại thảm họa → Mức độ thiệt hại)
-- ------------------------------------------------------------------------------
SELECT 
  c.cause_group,
  t.type_name,
  CASE 
    WHEN f.damage_usd IS NULL OR f.damage_usd = 0 THEN 'Không xác định / Không đáng kể'
    WHEN f.damage_usd < 10000000 THEN 'Thiệt hại Thấp (< 10M USD)'
    WHEN f.damage_usd BETWEEN 10000000 AND 500000000 THEN 'Thiệt hại Vừa (10M - 500M USD)'
    ELSE 'Thiệt hại Thảm họa (> 500M USD)'
  END AS damage_tier,
  COUNT(f.event_id) AS flow_volume
FROM fact_disaster_event f
JOIN dim_cause c ON f.cause_id = c.cause_id
JOIN dim_disaster_type t ON f.type_id = t.type_id
GROUP BY c.cause_group, t.type_name, damage_tier;

-- ------------------------------------------------------------------------------
-- Chart #12 | Thành viên 3: Bản đồ điểm các vụ cháy lớn (Proportional Symbol Map)
-- ------------------------------------------------------------------------------
SELECT 
  f.event_code,
  d.year,
  f.latitude,
  f.longitude,
  w.burned_area_ha,
  f.damage_usd,
  l.country_name
FROM fact_disaster_event f
JOIN fact_wildfire_detail w ON f.event_id = w.event_id
JOIN dim_date d ON f.date_id = d.date_id
JOIN dim_location l ON f.location_id = l.location_id
WHERE f.latitude IS NOT NULL AND f.longitude IS NOT NULL
ORDER BY w.burned_area_ha DESC;
