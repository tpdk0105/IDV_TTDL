"""
Test suite for IDV_TTDL pipeline.
Kiểm thử cấu trúc thư mục, quy chuẩn tập tin, CSDL SQLite và tính sẵn sàng của pipeline.
"""

from pathlib import Path
import sqlite3
import pytest


def test_directory_structure():
    """Kiểm tra các thư mục cốt lõi của dự án đã tồn tại."""
    required_dirs = [
        "data/raw",
        "data/interim",
        "data/clean",
        "data/tables",
        "notebooks",
        "sql",
        "src",
        "docs",
        "dashboard",
        "dashboard/js/vendor",
        "dashboard/js/charts",
        "dashboard/data",
        "team/member-1-data",
        "team/member-2-model",
        "team/member-3-dashboard",
        "tableau",
    ]
    for d in required_dirs:
        assert Path(d).is_dir(), f"Thư mục bắt buộc {d} không tồn tại!"


def test_required_docs_exist():
    """Kiểm tra toàn bộ 10 tài liệu kỹ thuật bắt buộc trong docs/."""
    required_docs = [
        "docs/DATA_SOURCES.md",
        "docs/DATA_DICTIONARY.md",
        "docs/DATA_QUALITY_REPORT.md",
        "docs/CLEANING_LOG.md",
        "docs/ML_CLEANING_REPORT.md",
        "docs/ERD.md",
        "docs/CHART_SPEC.md",
        "docs/COLOR_GUIDE.md",
        "docs/REPORT_OUTLINE.md",
        "docs/DEMO_SCRIPT.md",
    ]
    for doc in required_docs:
        assert Path(doc).is_file(), f"Tài liệu {doc} chưa được tạo!"


def test_team_task_files_exist():
    """Kiểm tra các file phân công nhiệm vụ của 3 thành viên."""
    task_files = [
        "PROJECT_GUIDE.md",
        "team/README.md",
        "team/member-1-data/TASKS.md",
        "team/member-2-model/TASKS.md",
        "team/member-3-dashboard/TASKS.md",
    ]
    for tf in task_files:
        assert Path(tf).is_file(), f"Tập tin phân công {tf} không tồn tại!"


def test_sql_files_exist():
    """Kiểm tra các tệp tin SQL cơ bản."""
    sql_files = [
        "sql/schema.sql",
        "sql/load.sql",
        "sql/queries_for_charts.sql",
    ]
    for sf in sql_files:
        assert Path(sf).is_file(), f"Tập tin SQL {sf} không tồn tại!"


def test_src_pipeline_scripts_exist():
    """Kiểm tra các script thực thi pipeline trong src/."""
    scripts = [
        "src/01_download.py",
        "src/02_eda.py",
        "src/03_clean.py",
        "src/03b_ml_clean.py",
        "src/04_split_tables.py",
        "src/05_build_db.py",
        "src/06_export_json.py",
        "src/07_validate.py",
    ]
    for s in scripts:
        assert Path(s).is_file(), f"Mã nguồn pipeline {s} không tồn tại!"


def test_star_schema_csv_files_exist():
    """Kiểm tra 5 bảng CSV thuộc mô hình Star Schema trong data/tables/."""
    required_tables = [
        "data/tables/dim_date.csv",
        "data/tables/dim_county.csv",
        "data/tables/dim_cause.csv",
        "data/tables/fact_fire_incident.csv",
        "data/tables/fact_structure_damage.csv",
    ]
    for tbl in required_tables:
        p = Path(tbl)
        assert p.is_file(), f"Bảng {tbl} chưa được tạo!"
        assert p.stat().st_size > 0, f"Bảng {tbl} rỗng (0 bytes)!"


def test_sqlite_database_integrity_and_row_counts():
    """Kiểm tra CSDL SQLite: tính toàn vẹn khóa ngoại (Zero Orphan FK) và fact >= 5.000 dòng."""
    db_path = Path("data/tables/database.sqlite")
    assert db_path.is_file(), "Tập tin data/tables/database.sqlite không tồn tại!"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. PRAGMA integrity_check
    integrity = cursor.execute("PRAGMA integrity_check;").fetchall()
    assert integrity == [("ok",)], f"SQLite integrity check thất bại: {integrity}"

    # 2. PRAGMA foreign_key_check (Zero Orphan Foreign Keys)
    fk_errors = cursor.execute("PRAGMA foreign_key_check;").fetchall()
    assert len(fk_errors) == 0, f"Phát hiện lỗi khóa ngoại mồ côi: {fk_errors}"

    # 3. Bảng fact trung tâm >= 5.000 dòng
    cursor.execute("SELECT COUNT(*) FROM fact_fire_incident;")
    fact_count = cursor.fetchone()[0]
    assert fact_count >= 5000, f"fact_fire_incident chỉ có {fact_count} dòng (< 5.000)!"

    # 4. Bảng fact mở rộng > 100.000 dòng
    cursor.execute("SELECT COUNT(*) FROM fact_structure_damage;")
    damage_count = cursor.fetchone()[0]
    assert damage_count > 100000, f"fact_structure_damage quá ít dòng: {damage_count}!"

    # 5. Đủ 58 hạt California (+ 1 unknown)
    cursor.execute("SELECT COUNT(*) FROM dim_county;")
    county_count = cursor.fetchone()[0]
    assert county_count >= 58, f"dim_county thiếu hạt: {county_count}!"

    conn.close()


def test_tv2_dashboard_json_exports():
    """Kiểm tra các tệp tin JSON phục vụ Dashboard và Biểu đồ TV2 (#3-#6)."""
    expected_jsons = [
        "dashboard/data/summary_kpis.json",
        "dashboard/data/chart_03_diverging_bar.json",
        "dashboard/data/chart_04_treemap_damage.json",
        "dashboard/data/chart_05_bubble_scatter.json",
        "dashboard/data/chart_06_combo_histogram.json",
    ]
    for jf in expected_jsons:
        p = Path(jf)
        assert p.is_file(), f"Tệp tin JSON {jf} chưa được xuất!"
        assert p.stat().st_size > 0, f"Tệp tin JSON {jf} rỗng!"
