"""
Module: src/06_export_json.py
Dự án: Nghiên cứu – phân tích tần suất và thiệt hại cháy rừng California (2006–2025)
Người phụ trách: Thành viên 2 (Mô hình Dữ liệu) & Thành viên 3 (Dashboard)
Mục đích:
    - Kết nối tới `data/tables/database.sqlite`.
    - Thực thi các câu truy vấn SQL phân tích từ `sql/queries_for_charts.sql` cho 4 biểu đồ của TV2:
        * Chart #3: `chart_03_diverging_bar.json` (Độ lệch số vụ so với TB 20 năm, tâm = 0)
        * Chart #4: `chart_04_treemap_damage.json` (Phân cấp tổn thất Hạt -> Loại công trình)
        * Chart #5: `chart_05_bubble_scatter.json` (Tương quan Diện tích vs Nhà cháy vs Thương vong)
        * Chart #6: `chart_06_combo_histogram.json` (Phân phối diện tích theo bin logarit + Lũy kế)
    - Xuất kèm thẻ chỉ số vĩ mô `summary_kpis.json` phục vụ hiển thị nhanh trên Dashboard.
    - Ghi các tệp JSON vào thư mục `dashboard/data/`.
"""

import json
from pathlib import Path
import sqlite3
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def export_charts_json() -> None:
    """Truy vấn database.sqlite và xuất các tệp tin JSON vào dashboard/data/."""
    db_path = Path("data/tables/database.sqlite")
    out_dir = Path("dashboard/data")
    out_dir.mkdir(parents=True, exist_ok=True)

    if not db_path.exists():
        raise FileNotFoundError(f"Không tìm thấy CSDL SQLite tại {db_path}! Hãy chạy 05_build_db.py trước.")

    print(f"[TV2 - EXPORT JSON] Kết nối CSDL SQLite: {db_path.resolve()}")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # -------------------------------------------------------------------------
    # 0. KPI tổng quan 20 năm (Summary KPIs)
    # -------------------------------------------------------------------------
    kpi_query = """
    SELECT 
      COUNT(incident_id) AS total_fires,
      ROUND(SUM(acres_burned), 2) AS total_acres_burned,
      ROUND(SUM(burned_area_ha), 2) AS total_ha_burned,
      SUM(total_structures_destroyed) AS total_structures_destroyed,
      SUM(total_structures_damaged) AS total_structures_damaged,
      SUM(deaths_direct) AS total_deaths,
      SUM(injuries_direct) AS total_injuries,
      ROUND(SUM(damage_property_usd), 2) AS total_damage_property_usd
    FROM fact_fire_incident;
    """
    cursor.execute(kpi_query)
    kpis = dict(cursor.fetchone())
    with open(out_dir / "summary_kpis.json", "w", encoding="utf-8") as f:
        json.dump(kpis, f, ensure_ascii=False, indent=2)
    print("  -> Xuất thành công `summary_kpis.json`.")

    # -------------------------------------------------------------------------
    # 1. Chart #3: Diverging Bar Chart (TV2)
    # -------------------------------------------------------------------------
    q3 = """
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
    """
    cursor.execute(q3)
    data_c3 = [dict(row) for row in cursor.fetchall()]
    with open(out_dir / "chart_03_diverging_bar.json", "w", encoding="utf-8") as f:
        json.dump(data_c3, f, ensure_ascii=False, indent=2)
    print(f"  -> Xuất thành công `chart_03_diverging_bar.json` ({len(data_c3)} năm).")

    # -------------------------------------------------------------------------
    # 2. Chart #4: Treemap Structure Damage by County & Type (TV2)
    # -------------------------------------------------------------------------
    q4 = """
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
    """
    cursor.execute(q4)
    data_c4 = [dict(row) for row in cursor.fetchall()]
    with open(out_dir / "chart_04_treemap_damage.json", "w", encoding="utf-8") as f:
        json.dump(data_c4, f, ensure_ascii=False, indent=2)
    print(f"  -> Xuất thành công `chart_04_treemap_damage.json` ({len(data_c4)} nhóm).")

    # -------------------------------------------------------------------------
    # 3. Chart #5: Bubble Scatter Plot (TV2)
    # -------------------------------------------------------------------------
    q5 = """
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
    WHERE f.acres_burned > 0
    ORDER BY f.acres_burned DESC;
    """
    cursor.execute(q5)
    data_c5 = [dict(row) for row in cursor.fetchall()]
    with open(out_dir / "chart_05_bubble_scatter.json", "w", encoding="utf-8") as f:
        json.dump(data_c5, f, ensure_ascii=False, indent=2)
    print(f"  -> Xuất thành công `chart_05_bubble_scatter.json` ({len(data_c5)} điểm dữ liệu).")

    # -------------------------------------------------------------------------
    # 4. Chart #6: Combo Histogram by Log Acres Bin (TV2)
    # -------------------------------------------------------------------------
    q6 = """
    WITH binned AS (
      SELECT 
        CASE 
          WHEN acres_burned < 300 THEN '1. < 300 Acres'
          WHEN acres_burned BETWEEN 300 AND 999.99 THEN '2. 300 - 1.000 Acres'
          WHEN acres_burned BETWEEN 1000 AND 4999.99 THEN '3. 1.000 - 5.000 Acres'
          WHEN acres_burned BETWEEN 5000 AND 24999.99 THEN '4. 5.000 - 25.000 Acres'
          WHEN acres_burned BETWEEN 25000 AND 99999.99 THEN '5. 25.000 - 100.000 Acres'
          ELSE '6. ≥ 100.000 Acres (Siêu đám cháy)'
        END AS acres_bin,
        acres_burned
      FROM fact_fire_incident
      WHERE acres_burned IS NOT NULL AND acres_burned > 0
    ),
    agg AS (
      SELECT 
        acres_bin,
        COUNT(*) AS fire_count,
        ROUND(SUM(acres_burned), 2) AS total_acres
      FROM binned
      GROUP BY acres_bin
      ORDER BY acres_bin ASC
    ),
    totals AS (
      SELECT SUM(fire_count) AS grand_fires, SUM(total_acres) AS grand_acres FROM agg
    )
    SELECT 
      a.acres_bin,
      a.fire_count,
      ROUND(a.fire_count * 100.0 / t.grand_fires, 2) AS fire_pct,
      a.total_acres,
      ROUND(a.total_acres * 100.0 / t.grand_acres, 2) AS acres_pct
    FROM agg a
    CROSS JOIN totals t;
    """
    cursor.execute(q6)
    data_c6 = [dict(row) for row in cursor.fetchall()]
    with open(out_dir / "chart_06_combo_histogram.json", "w", encoding="utf-8") as f:
        json.dump(data_c6, f, ensure_ascii=False, indent=2)
    print(f"  -> Xuất thành công `chart_06_combo_histogram.json` ({len(data_c6)} bins).")

    conn.close()
    print(f"[TV2 - EXPORT JSON] Hoàn thành xuất toàn bộ file JSON vào: {out_dir.resolve()}\n")


if __name__ == "__main__":
    export_charts_json()
