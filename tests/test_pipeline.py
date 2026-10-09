

from pathlib import Path
import pandas as pd


def test_directory_structure():
    required_dirs = [
        "data/raw",
        "data/interim",
        "data/clean",
        "data/tables",
        "notebooks",
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
    task_files = [
        "PROJECT_GUIDE.md",
        "team/README.md",
        "team/member-1-data/TASKS.md",
        "team/member-2-model/TASKS.md",
        "team/member-3-dashboard/TASKS.md",
    ]
    for tf in task_files:
        assert Path(tf).is_file(), f"Tập tin phân công {tf} không tồn tại!"


def test_src_pipeline_scripts_exist():
    scripts = [
        "src/01_download.py",
        "src/02_eda.py",
        "src/03_clean.py",
        "src/04_split_tables.py",
        "src/07_validate.py",
    ]
    for s in scripts:
        assert Path(s).is_file(), f"Mã nguồn pipeline {s} không tồn tại!"


def test_star_schema_csv_files_exist():
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


def test_star_schema_referential_integrity_and_row_counts():
    df_date = pd.read_csv("data/tables/dim_date.csv")
    df_county = pd.read_csv("data/tables/dim_county.csv")
    df_cause = pd.read_csv("data/tables/dim_cause.csv")
    df_fact = pd.read_csv("data/tables/fact_fire_incident.csv")
    df_damage = pd.read_csv("data/tables/fact_structure_damage.csv")

    # 1. Zero Orphan FK
    orphan_date = set(df_fact["date_id"]) - set(df_date["date_id"])
    assert len(orphan_date) == 0, f"fact_fire_incident có date_id mồ côi: {len(orphan_date)}"

    orphan_county = set(df_fact["county_id"]) - set(df_county["county_id"])
    assert len(orphan_county) == 0, f"fact_fire_incident có county_id mồ côi: {len(orphan_county)}"

    orphan_cause = set(df_fact["cause_id"]) - set(df_cause["cause_id"])
    assert len(orphan_cause) == 0, f"fact_fire_incident có cause_id mồ côi: {len(orphan_cause)}"

    orphan_inc = set(df_damage["incident_id"]) - set(df_fact["incident_id"])
    assert len(orphan_inc) == 0, f"fact_structure_damage có incident_id mồ côi: {len(orphan_inc)}"

    # 2. Row count barem
    assert len(df_fact) >= 5000, f"fact_fire_incident chỉ có {len(df_fact)} dòng (< 5.000)!"
    assert len(df_damage) > 100000, f"fact_structure_damage quá ít dòng: {len(df_damage)}!"
    assert len(df_county) >= 58, f"dim_county thiếu hạt: {len(df_county)}!"
