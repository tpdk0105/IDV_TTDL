"""
Test suite for IDV_TTDL pipeline.
Kiểm thử cấu trúc thư mục, quy chuẩn tập tin và tính sẵn sàng của pipeline.
"""

from pathlib import Path
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
